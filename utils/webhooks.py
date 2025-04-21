"""
Webhook System for BloxAPI

This module provides real-time event notifications via webhooks.
It allows users to register webhook endpoints and receive notifications
when specific events occur in the Roblox ecosystem.
"""

import os
import json
import hmac
import hashlib
import logging
import time
import uuid
import requests
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set, Union, Callable
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class WebhookSubscription:
    """Webhook subscription data structure"""
    id: str
    url: str
    secret: str
    events: List[str]
    description: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True
    
    # Optional filters to apply to events
    filters: Dict[str, Any] = field(default_factory=dict)
    
    # Rate limiting
    rate_limit: int = 60  # Maximum events per minute
    current_rate: int = 0
    last_reset: float = field(default_factory=time.time)
    
    # Delivery stats
    successful_deliveries: int = 0
    failed_deliveries: int = 0
    last_delivery_attempt: Optional[datetime] = None
    last_delivery_status: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/API"""
        return {
            "id": self.id,
            "url": self.url,
            "events": self.events,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "filters": self.filters,
            "rate_limit": self.rate_limit,
            "stats": {
                "successful_deliveries": self.successful_deliveries,
                "failed_deliveries": self.failed_deliveries,
                "last_delivery_attempt": self.last_delivery_attempt.isoformat() if self.last_delivery_attempt else None,
                "last_delivery_status": self.last_delivery_status
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WebhookSubscription':
        """Create from dictionary"""
        # Extract stats if present
        stats = data.pop("stats", {})
        
        # Parse dates
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
            
        # Create instance
        instance = cls(**data)
        
        # Apply stats
        if stats:
            instance.successful_deliveries = stats.get("successful_deliveries", 0)
            instance.failed_deliveries = stats.get("failed_deliveries", 0)
            
            if stats.get("last_delivery_attempt"):
                instance.last_delivery_attempt = datetime.fromisoformat(stats["last_delivery_attempt"])
            
            instance.last_delivery_status = stats.get("last_delivery_status")
            
        return instance


class WebhookManager:
    """Manager for webhook subscriptions and delivery"""
    
    def __init__(self, max_workers: int = 10, max_retries: int = 3, 
                 retry_delay: int = 5, timeout: int = 10):
        """
        Initialize the webhook manager.
        
        Args:
            max_workers: Maximum number of worker threads for webhook delivery
            max_retries: Maximum number of retries for failed deliveries
            retry_delay: Delay between retries in seconds
            timeout: Timeout for webhook requests in seconds
        """
        self.subscriptions: Dict[str, WebhookSubscription] = {}
        self.event_subscriptions: Dict[str, Set[str]] = {}  # event_type -> set of subscription IDs
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        
        # Middleware hooks
        self.pre_delivery_hooks: List[Callable[[Dict[str, Any], WebhookSubscription], Dict[str, Any]]] = []
        self.post_delivery_hooks: List[Callable[[Dict[str, Any], WebhookSubscription, int], None]] = []
        
        logger.info(f"Webhook manager initialized with {max_workers} workers, {max_retries} retries")
    
    def register_subscription(self, url: str, events: List[str], secret: Optional[str] = None,
                              description: Optional[str] = None, filters: Optional[Dict[str, Any]] = None,
                              rate_limit: int = 60) -> WebhookSubscription:
        """
        Register a new webhook subscription.
        
        Args:
            url: The webhook URL to send events to
            events: List of event types to subscribe to
            secret: Secret for webhook signature validation (generated if not provided)
            description: Optional description of this webhook
            filters: Optional filters to apply to events
            rate_limit: Maximum events per minute
            
        Returns:
            WebhookSubscription: The created subscription
        """
        # Generate subscription ID and secret if not provided
        subscription_id = str(uuid.uuid4())
        if not secret:
            secret = hashlib.sha256(os.urandom(32)).hexdigest()
        
        # Create subscription
        subscription = WebhookSubscription(
            id=subscription_id,
            url=url,
            secret=secret,
            events=events,
            description=description,
            filters=filters or {},
            rate_limit=rate_limit
        )
        
        # Store subscription
        self.subscriptions[subscription_id] = subscription
        
        # Update event mapping
        for event_type in events:
            if event_type not in self.event_subscriptions:
                self.event_subscriptions[event_type] = set()
            self.event_subscriptions[event_type].add(subscription_id)
        
        logger.info(f"Registered webhook subscription {subscription_id} for events: {events}")
        return subscription
    
    def unregister_subscription(self, subscription_id: str) -> bool:
        """
        Unregister a webhook subscription.
        
        Args:
            subscription_id: ID of the subscription to remove
            
        Returns:
            bool: True if successfully removed, False otherwise
        """
        if subscription_id not in self.subscriptions:
            return False
        
        # Get subscription to update event mappings
        subscription = self.subscriptions[subscription_id]
        
        # Remove from event mappings
        for event_type in subscription.events:
            if event_type in self.event_subscriptions:
                self.event_subscriptions[event_type].discard(subscription_id)
                
                # Clean up empty sets
                if not self.event_subscriptions[event_type]:
                    del self.event_subscriptions[event_type]
        
        # Remove subscription
        del self.subscriptions[subscription_id]
        logger.info(f"Unregistered webhook subscription {subscription_id}")
        
        return True
    
    def update_subscription(self, subscription_id: str, **updates) -> Optional[WebhookSubscription]:
        """
        Update a webhook subscription.
        
        Args:
            subscription_id: ID of the subscription to update
            **updates: Fields to update
            
        Returns:
            WebhookSubscription: The updated subscription, or None if not found
        """
        if subscription_id not in self.subscriptions:
            return None
        
        subscription = self.subscriptions[subscription_id]
        
        # Handle event updates separately to maintain event mappings
        if "events" in updates:
            new_events = updates["events"]
            old_events = subscription.events
            
            # Remove from old event mappings
            for event_type in old_events:
                if event_type in self.event_subscriptions:
                    self.event_subscriptions[event_type].discard(subscription_id)
            
            # Add to new event mappings
            for event_type in new_events:
                if event_type not in self.event_subscriptions:
                    self.event_subscriptions[event_type] = set()
                self.event_subscriptions[event_type].add(subscription_id)
            
            # Update subscription events
            subscription.events = new_events
            
            # Remove from updates to avoid setting twice
            del updates["events"]
        
        # Apply remaining updates
        for key, value in updates.items():
            if hasattr(subscription, key):
                setattr(subscription, key, value)
        
        # Update the updated_at timestamp
        subscription.updated_at = datetime.now(timezone.utc)
        
        logger.info(f"Updated webhook subscription {subscription_id}")
        return subscription
    
    def get_subscription(self, subscription_id: str) -> Optional[WebhookSubscription]:
        """
        Get a webhook subscription by ID.
        
        Args:
            subscription_id: ID of the subscription
            
        Returns:
            WebhookSubscription: The subscription, or None if not found
        """
        return self.subscriptions.get(subscription_id)
    
    def list_subscriptions(self, event_type: Optional[str] = None) -> List[WebhookSubscription]:
        """
        List webhook subscriptions, optionally filtered by event type.
        
        Args:
            event_type: Optional event type to filter by
            
        Returns:
            List of webhook subscriptions
        """
        if event_type:
            subscription_ids = self.event_subscriptions.get(event_type, set())
            return [self.subscriptions[sub_id] for sub_id in subscription_ids 
                    if sub_id in self.subscriptions]
        
        return list(self.subscriptions.values())
    
    def trigger_event(self, event_type: str, payload: Dict[str, Any]) -> int:
        """
        Trigger an event to be sent to all subscribed webhooks.
        
        Args:
            event_type: Type of event
            payload: Event data
            
        Returns:
            int: Number of webhook deliveries attempted
        """
        # Get subscriptions for this event type
        subscription_ids = self.event_subscriptions.get(event_type, set())
        if not subscription_ids:
            logger.debug(f"No subscriptions for event type: {event_type}")
            return 0
        
        # Add event metadata
        event_data = {
            "event_type": event_type,
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": payload
        }
        
        # Count of deliveries attempted
        delivery_count = 0
        
        # Deliver to each subscription
        for subscription_id in subscription_ids:
            subscription = self.subscriptions.get(subscription_id)
            if not subscription or not subscription.is_active:
                continue
            
            # Apply filters if any
            if subscription.filters and not self._match_filters(event_data, subscription.filters):
                logger.debug(f"Event filtered out for subscription {subscription_id}")
                continue
            
            # Check rate limiting
            current_time = time.time()
            if current_time - subscription.last_reset >= 60:
                # Reset rate limiting after a minute
                subscription.current_rate = 0
                subscription.last_reset = current_time
                
            if subscription.current_rate >= subscription.rate_limit:
                logger.warning(f"Rate limit exceeded for subscription {subscription_id}")
                continue
            
            # Increment rate counter
            subscription.current_rate += 1
            
            # Submit delivery task
            self.executor.submit(self._deliver_webhook, event_data, subscription)
            delivery_count += 1
        
        logger.info(f"Triggered event {event_type}, delivered to {delivery_count} webhooks")
        return delivery_count
    
    def _match_filters(self, event_data: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """
        Check if an event matches the subscription filters.
        
        Args:
            event_data: Event data
            filters: Filters to apply
            
        Returns:
            bool: True if event matches filters, False otherwise
        """
        payload = event_data.get("data", {})
        
        for key, filter_value in filters.items():
            # Skip metadata filters
            if key in ["event_type", "event_id", "timestamp"]:
                continue
                
            # Get the payload value using dot notation
            path = key.split('.')
            current = payload
            
            # Traverse the path
            for segment in path:
                if isinstance(current, dict) and segment in current:
                    current = current[segment]
                else:
                    # Path doesn't exist, filter doesn't match
                    return False
            
            # Check if value matches filter
            if isinstance(filter_value, list):
                # List of allowed values
                if current not in filter_value:
                    return False
            elif filter_value != current:
                # Direct value comparison
                return False
        
        # All filters passed
        return True
    
    def _deliver_webhook(self, event_data: Dict[str, Any], subscription: WebhookSubscription, 
                         retry_count: int = 0) -> None:
        """
        Deliver a webhook to a subscription.
        
        Args:
            event_data: Event data to deliver
            subscription: Webhook subscription
            retry_count: Current retry attempt
        """
        # Apply pre-delivery hooks
        for hook in self.pre_delivery_hooks:
            try:
                event_data = hook(event_data, subscription)
            except Exception as e:
                logger.error(f"Error in pre-delivery hook: {e}")
        
        # Prepare the payload
        payload = json.dumps(event_data)
        
        # Generate signature
        timestamp = str(int(time.time()))
        signature_payload = f"{timestamp}.{payload}"
        signature = hmac.new(
            subscription.secret.encode(),
            signature_payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "BloxAPI-Webhook/2.0",
            "X-BloxAPI-Event": event_data["event_type"],
            "X-BloxAPI-Delivery": event_data["event_id"],
            "X-BloxAPI-Signature": signature,
            "X-BloxAPI-Timestamp": timestamp
        }
        
        # Update delivery stats
        subscription.last_delivery_attempt = datetime.now(timezone.utc)
        
        try:
            # Send the webhook
            response = requests.post(
                subscription.url,
                data=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            status_code = response.status_code
            subscription.last_delivery_status = status_code
            
            # Check if successful (2xx status code)
            if 200 <= status_code < 300:
                subscription.successful_deliveries += 1
                logger.debug(f"Webhook delivered successfully to {subscription.url}, "
                            f"event: {event_data['event_type']}, status: {status_code}")
            else:
                subscription.failed_deliveries += 1
                logger.warning(f"Webhook delivery failed: {subscription.url}, "
                              f"event: {event_data['event_type']}, status: {status_code}")
                
                # Retry if not at max retries and status code indicates server error or timeout
                if retry_count < self.max_retries and (status_code >= 500 or status_code == 429):
                    retry_delay = self.retry_delay * (2 ** retry_count)  # Exponential backoff
                    logger.info(f"Retrying webhook delivery in {retry_delay}s, "
                               f"attempt {retry_count+1}/{self.max_retries}")
                    
                    # Schedule retry
                    time.sleep(retry_delay)
                    self._deliver_webhook(event_data, subscription, retry_count + 1)
            
            # Apply post-delivery hooks
            for hook in self.post_delivery_hooks:
                try:
                    hook(event_data, subscription, status_code)
                except Exception as e:
                    logger.error(f"Error in post-delivery hook: {e}")
                    
        except requests.RequestException as e:
            subscription.failed_deliveries += 1
            subscription.last_delivery_status = 0  # Connection error
            
            logger.warning(f"Webhook delivery error: {subscription.url}, {str(e)}")
            
            # Retry if not at max retries
            if retry_count < self.max_retries:
                retry_delay = self.retry_delay * (2 ** retry_count)  # Exponential backoff
                logger.info(f"Retrying webhook delivery in {retry_delay}s, "
                           f"attempt {retry_count+1}/{self.max_retries}")
                
                # Schedule retry
                time.sleep(retry_delay)
                self._deliver_webhook(event_data, subscription, retry_count + 1)
    
    def register_pre_delivery_hook(self, hook: Callable[[Dict[str, Any], WebhookSubscription], Dict[str, Any]]) -> None:
        """
        Register a hook to be called before delivering a webhook.
        
        Args:
            hook: Function to be called with (event_data, subscription)
                 Should return the modified event_data
        """
        self.pre_delivery_hooks.append(hook)
    
    def register_post_delivery_hook(self, hook: Callable[[Dict[str, Any], WebhookSubscription, int], None]) -> None:
        """
        Register a hook to be called after delivering a webhook.
        
        Args:
            hook: Function to be called with (event_data, subscription, status_code)
        """
        self.post_delivery_hooks.append(hook)


# Global webhook manager instance
_webhook_manager = None

def get_webhook_manager() -> WebhookManager:
    """
    Get or create the global webhook manager instance.
    
    Returns:
        WebhookManager: The webhook manager
    """
    global _webhook_manager
    if _webhook_manager is None:
        _webhook_manager = WebhookManager()
    return _webhook_manager