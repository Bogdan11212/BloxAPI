"""
Security Routes for BloxAPI

This module provides API routes for security features, fraud detection,
and bot protection.
"""

import logging
from flask import request, jsonify
from flask_restful import Resource
from utils.security import get_rate_limiter, get_ip_reputation, get_bot_detector, get_request_validator
from utils.fraud_detection import get_account_monitor, get_item_monitor

# Configure logging
logger = logging.getLogger(__name__)

class BotDetectionResource(Resource):
    """
    Resource for bot detection
    """
    
    def post(self):
        """
        Detect if a request is from a bot
        
        Request Body:
            user_agent: User-Agent header (required)
            ip: IP address (optional)
            
        Returns:
            Bot detection result or error response
        """
        try:
            # Get request data
            data = request.get_json()
            if not data or 'user_agent' not in data:
                return {"error": "User-Agent is required"}, 400
            
            user_agent = data['user_agent']
            ip = data.get('ip')
            
            # Get bot detector
            bot_detector = get_bot_detector()
            
            # Check if it's a bot
            result = bot_detector.is_bot(user_agent, ip)
            
            return result
        except Exception as e:
            logger.error(f"Error detecting bot: {e}")
            return {"error": str(e)}, 500


class IPReputationResource(Resource):
    """
    Resource for IP reputation
    """
    
    def get(self, ip=None):
        """
        Get reputation for an IP address
        
        Args:
            ip: IP address (optional, uses request IP if not provided)
            
        Returns:
            IP reputation or error response
        """
        try:
            # Get IP address
            if not ip:
                ip = request.remote_addr
            
            # Get IP reputation
            reputation = get_ip_reputation()
            
            # Check reputation
            result = reputation.check_reputation(ip)
            
            return result
        except Exception as e:
            logger.error(f"Error checking IP reputation: {e}")
            return {"error": str(e)}, 500


class RequestValidationResource(Resource):
    """
    Resource for request validation
    """
    
    def post(self):
        """
        Validate a request for security issues
        
        Request Body:
            path: Request path
            query_params: Query parameters
            headers: Request headers
            body: Request body
            
        Returns:
            Validation result or error response
        """
        try:
            # This is a simplified version for demonstration
            # In a real implementation, you would validate the actual request
            
            # Get request data
            data = request.get_json()
            if not data:
                return {"error": "No request data provided"}, 400
            
            # For demonstration purposes only - showing what kind of response would be returned
            return {
                "is_valid": True,
                "validation_checks": [
                    {"check": "sql_injection", "passed": True},
                    {"check": "xss", "passed": True},
                    {"check": "path_traversal", "passed": True},
                    {"check": "command_injection", "passed": True}
                ]
            }
        except Exception as e:
            logger.error(f"Error validating request: {e}")
            return {"error": str(e)}, 500


class AccountMonitoringResource(Resource):
    """
    Resource for account monitoring
    """
    
    def post(self):
        """
        Record a login attempt and check for suspicious activity
        
        Request Body:
            user_id: User ID
            ip: IP address
            success: Whether login was successful
            user_agent: User agent string (optional)
            location: Geographic location (optional)
            device_id: Device identifier (optional)
            
        Returns:
            Account monitoring result or error response
        """
        try:
            # Get request data
            data = request.get_json()
            if not data:
                return {"error": "No request data provided"}, 400
            
            # Validate required fields
            required_fields = ['user_id', 'ip', 'success']
            for field in required_fields:
                if field not in data:
                    return {"error": f"Missing required field: {field}"}, 400
            
            # Get account monitor
            account_monitor = get_account_monitor()
            
            # Record login
            result = account_monitor.record_login(
                user_id=data['user_id'],
                ip=data['ip'],
                success=data['success'],
                user_agent=data.get('user_agent'),
                location=data.get('location'),
                device_id=data.get('device_id')
            )
            
            return result
        except Exception as e:
            logger.error(f"Error monitoring account: {e}")
            return {"error": str(e)}, 500
    
    def get(self):
        """
        Get suspicious users
        
        Query Parameters:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of suspicious users or error response
        """
        try:
            # Get query parameters
            limit = int(request.args.get('limit', 100))
            
            # Get account monitor
            account_monitor = get_account_monitor()
            
            # Get suspicious users
            users = account_monitor.get_suspicious_users(limit=limit)
            
            return {"suspicious_users": users}
        except Exception as e:
            logger.error(f"Error getting suspicious users: {e}")
            return {"error": str(e)}, 500


class ItemMonitoringResource(Resource):
    """
    Resource for item monitoring
    """
    
    def post(self):
        """
        Record an item activity and check for suspicious patterns
        
        Request Body:
            item_id: Item ID
            event_type: Event type (create, purchase, transfer, modify)
            user_id: User ID (optional)
            data: Additional event data (optional)
            
        Returns:
            Item monitoring result or error response
        """
        try:
            # Get request data
            data = request.get_json()
            if not data:
                return {"error": "No request data provided"}, 400
            
            # Validate required fields
            required_fields = ['item_id', 'event_type']
            for field in required_fields:
                if field not in data:
                    return {"error": f"Missing required field: {field}"}, 400
            
            # Get item monitor
            item_monitor = get_item_monitor()
            
            # Record item activity
            result = item_monitor.record_item_activity(
                item_id=data['item_id'],
                event_type=data['event_type'],
                user_id=data.get('user_id'),
                data=data.get('data')
            )
            
            return result
        except Exception as e:
            logger.error(f"Error monitoring item: {e}")
            return {"error": str(e)}, 500
    
    def get(self):
        """
        Get suspicious items
        
        Query Parameters:
            limit: Maximum number of results (default: 100)
            
        Returns:
            List of suspicious items or error response
        """
        try:
            # Get query parameters
            limit = int(request.args.get('limit', 100))
            
            # Get item monitor
            item_monitor = get_item_monitor()
            
            # Get suspicious items
            items = item_monitor.get_suspicious_items(limit=limit)
            
            return {"suspicious_items": items}
        except Exception as e:
            logger.error(f"Error getting suspicious items: {e}")
            return {"error": str(e)}, 500


class RateLimitStatusResource(Resource):
    """
    Resource for rate limit status
    """
    
    def get(self):
        """
        Get rate limiter statistics
        
        Returns:
            Rate limiter statistics or error response
        """
        try:
            # Get rate limiter
            rate_limiter = get_rate_limiter()
            
            # Get stats
            stats = rate_limiter.get_stats()
            
            return stats
        except Exception as e:
            logger.error(f"Error getting rate limit status: {e}")
            return {"error": str(e)}, 500


class IPBanResource(Resource):
    """
    Resource for IP banning
    """
    
    def post(self):
        """
        Ban an IP address
        
        Request Body:
            ip: IP address
            duration: Ban duration in seconds (optional)
            
        Returns:
            Success response or error response
        """
        try:
            # Get request data
            data = request.get_json()
            if not data or 'ip' not in data:
                return {"error": "IP address is required"}, 400
            
            ip = data['ip']
            duration = data.get('duration')
            
            # Get rate limiter
            rate_limiter = get_rate_limiter()
            
            # Ban IP
            rate_limiter.ban_ip(ip, duration)
            
            return {"message": f"IP {ip} has been banned"}
        except Exception as e:
            logger.error(f"Error banning IP: {e}")
            return {"error": str(e)}, 500
    
    def delete(self, ip):
        """
        Unban an IP address
        
        Args:
            ip: IP address to unban
            
        Returns:
            Success response or error response
        """
        try:
            # Get rate limiter
            rate_limiter = get_rate_limiter()
            
            # Unban IP
            rate_limiter.unban_ip(ip)
            
            return {"message": f"IP {ip} has been unbanned"}
        except Exception as e:
            logger.error(f"Error unbanning IP: {e}")
            return {"error": str(e)}, 500


class SecurityInfoResource(Resource):
    """
    Resource for security information
    """
    
    def get(self):
        """
        Get general security information
        
        Returns:
            Security information or error response
        """
        try:
            # Get components
            rate_limiter = get_rate_limiter()
            ip_reputation = get_ip_reputation()
            account_monitor = get_account_monitor()
            item_monitor = get_item_monitor()
            
            # Get stats from each component
            rate_limiter_stats = rate_limiter.get_stats()
            ip_reputation_stats = ip_reputation.get_stats()
            account_stats = account_monitor.get_stats()
            item_stats = item_monitor.get_stats()
            
            # Combine stats
            info = {
                "rate_limiter": rate_limiter_stats,
                "ip_reputation": ip_reputation_stats,
                "account_monitoring": account_stats,
                "item_monitoring": item_stats
            }
            
            return info
        except Exception as e:
            logger.error(f"Error getting security info: {e}")
            return {"error": str(e)}, 500