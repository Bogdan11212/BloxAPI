"""
External Integrations for BloxAPI

This module provides functionality for integrating with external services
like Discord, Twitter, and other platforms. It handles authentication,
data synchronization, and webhook notifications.
"""

import os
import json
import logging
import time
import base64
import hmac
import hashlib
import re
import uuid
from typing import Dict, List, Any, Optional, Union, Callable, Tuple
from datetime import datetime, timedelta
import requests
import tweepy
import discord
from discord.ext import commands
from discord import Webhook, RequestsWebhookAdapter

# Configure logging
logger = logging.getLogger(__name__)

class IntegrationError(Exception):
    """Exception raised for errors with external integrations"""
    pass

class BaseIntegration:
    """
    Base class for all external integrations
    """
    
    def __init__(self, credentials: Dict[str, str] = None):
        """
        Initialize the integration
        
        Args:
            credentials: Authentication credentials
        """
        self.credentials = credentials or {}
        self.client = None
        self.is_authenticated = False
    
    def authenticate(self) -> bool:
        """
        Authenticate with the external service
        
        Returns:
            True if authentication was successful
        """
        raise NotImplementedError("Subclasses must implement authenticate()")
    
    def verify_credentials(self) -> bool:
        """
        Verify that the credentials are valid
        
        Returns:
            True if credentials are valid
        """
        raise NotImplementedError("Subclasses must implement verify_credentials()")
    
    def get_auth_url(self) -> str:
        """
        Get authentication URL for OAuth flow
        
        Returns:
            Authentication URL
        """
        raise NotImplementedError("Subclasses must implement get_auth_url()")
    
    def handle_oauth_callback(self, params: Dict[str, str]) -> bool:
        """
        Handle OAuth callback
        
        Args:
            params: Callback parameters
            
        Returns:
            True if authentication was successful
        """
        raise NotImplementedError("Subclasses must implement handle_oauth_callback()")


class DiscordIntegration(BaseIntegration):
    """
    Integration with Discord
    """
    
    def __init__(self, credentials: Dict[str, str] = None):
        """
        Initialize Discord integration
        
        Args:
            credentials: Authentication credentials (bot_token, client_id, client_secret, webhook_url)
        """
        super().__init__(credentials)
        self.bot = None
    
    def authenticate(self) -> bool:
        """
        Authenticate with Discord
        
        Returns:
            True if authentication was successful
        """
        try:
            # Check if we have a bot token
            bot_token = self.credentials.get("bot_token")
            
            if not bot_token:
                logger.error("Discord bot token is required")
                return False
            
            # Initialize Discord client
            self.client = discord.Client()
            
            # Create bot instance
            self.bot = commands.Bot(command_prefix="!")
            
            # Set up event handlers
            @self.bot.event
            async def on_ready():
                logger.info(f"Discord bot logged in as {self.bot.user}")
                self.is_authenticated = True
            
            # Start the bot (non-blocking)
            # Note: In a real application, you would run the bot in a separate process or thread
            # For demo purposes, we'll just check if the token is valid
            
            # Check if the token is valid
            headers = {
                "Authorization": f"Bot {bot_token}"
            }
            response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
            
            if response.status_code == 200:
                self.is_authenticated = True
                logger.info("Discord authentication successful")
                return True
            else:
                logger.error(f"Discord authentication failed: {response.status_code}")
                return False
            
        except Exception as e:
            logger.error(f"Discord authentication error: {str(e)}")
            return False
    
    def verify_credentials(self) -> bool:
        """
        Verify that the Discord credentials are valid
        
        Returns:
            True if credentials are valid
        """
        try:
            # Check if we have a bot token
            bot_token = self.credentials.get("bot_token")
            
            if not bot_token:
                return False
            
            # Check if the token is valid
            headers = {
                "Authorization": f"Bot {bot_token}"
            }
            response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Discord credential verification error: {str(e)}")
            return False
    
    def get_auth_url(self) -> str:
        """
        Get Discord OAuth authorization URL
        
        Returns:
            Authorization URL
        """
        client_id = self.credentials.get("client_id")
        
        if not client_id:
            raise IntegrationError("Discord client ID is required")
        
        # Redirect URI should be configured in the Discord Developer Portal
        redirect_uri = self.credentials.get("redirect_uri", "https://your-app.com/discord/callback")
        
        # Define the required permissions (scopes)
        # See https://discord.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes
        scopes = [
            "bot",
            "webhook.incoming"
        ]
        
        # Define bot permissions
        # See https://discord.com/developers/docs/topics/permissions
        permissions = 537159744  # Basic permissions for bot functionality
        
        # Build the authorization URL
        auth_url = (
            f"https://discord.com/api/oauth2/authorize"
            f"?client_id={client_id}"
            f"&permissions={permissions}"
            f"&redirect_uri={requests.utils.quote(redirect_uri)}"
            f"&response_type=code"
            f"&scope={'+'.join(scopes)}"
        )
        
        return auth_url
    
    def handle_oauth_callback(self, params: Dict[str, str]) -> bool:
        """
        Handle Discord OAuth callback
        
        Args:
            params: Callback parameters
            
        Returns:
            True if authentication was successful
        """
        try:
            # Extract the authorization code
            code = params.get("code")
            
            if not code:
                logger.error("No authorization code in Discord callback")
                return False
            
            # Exchange the code for an access token
            client_id = self.credentials.get("client_id")
            client_secret = self.credentials.get("client_secret")
            redirect_uri = self.credentials.get("redirect_uri", "https://your-app.com/discord/callback")
            
            if not client_id or not client_secret:
                logger.error("Discord client ID and secret are required")
                return False
            
            # Make the token request
            token_url = "https://discord.com/api/oauth2/token"
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri
            }
            
            response = requests.post(token_url, data=data)
            
            if response.status_code == 200:
                # Parse the response
                token_data = response.json()
                
                # Update credentials
                self.credentials["access_token"] = token_data.get("access_token")
                self.credentials["refresh_token"] = token_data.get("refresh_token")
                self.credentials["token_type"] = token_data.get("token_type")
                self.credentials["expires_at"] = time.time() + token_data.get("expires_in", 0)
                
                # Authenticate with the new token
                return self.authenticate()
            else:
                logger.error(f"Discord token exchange failed: {response.status_code}")
                return False
            
        except Exception as e:
            logger.error(f"Discord OAuth callback error: {str(e)}")
            return False
    
    def send_message(self, channel_id: str, message: str) -> bool:
        """
        Send a message to a Discord channel
        
        Args:
            channel_id: Discord channel ID
            message: Message content
            
        Returns:
            True if message was sent successfully
        """
        try:
            # Check if authenticated
            if not self.is_authenticated:
                if not self.authenticate():
                    return False
            
            # Get bot token
            bot_token = self.credentials.get("bot_token")
            
            if not bot_token:
                logger.error("Discord bot token is required")
                return False
            
            # Send message via API
            headers = {
                "Authorization": f"Bot {bot_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "content": message
            }
            
            response = requests.post(
                f"https://discord.com/api/v10/channels/{channel_id}/messages",
                headers=headers,
                json=data
            )
            
            if response.status_code in (200, 201):
                logger.info(f"Message sent to Discord channel {channel_id}")
                return True
            else:
                logger.error(f"Failed to send Discord message: {response.status_code}")
                return False
            
        except Exception as e:
            logger.error(f"Discord message error: {str(e)}")
            return False
    
    def send_webhook(self, webhook_url: str, message: str, 
                    embed: Optional[Dict[str, Any]] = None) -> bool:
        """
        Send a message to a Discord webhook
        
        Args:
            webhook_url: Discord webhook URL
            message: Message content
            embed: Optional embed data
            
        Returns:
            True if message was sent successfully
        """
        try:
            # Validate webhook URL
            if not webhook_url or not webhook_url.startswith("https://discord.com/api/webhooks/"):
                webhook_url = self.credentials.get("webhook_url")
                
                if not webhook_url or not webhook_url.startswith("https://discord.com/api/webhooks/"):
                    logger.error("Valid Discord webhook URL is required")
                    return False
            
            # Prepare payload
            payload = {
                "content": message
            }
            
            # Add embed if provided
            if embed:
                payload["embeds"] = [embed]
            
            # Send webhook
            response = requests.post(webhook_url, json=payload)
            
            if response.status_code in (200, 204):
                logger.info("Message sent to Discord webhook")
                return True
            else:
                logger.error(f"Failed to send Discord webhook: {response.status_code}")
                return False
            
        except Exception as e:
            logger.error(f"Discord webhook error: {str(e)}")
            return False
    
    def create_embed(self, title: str, description: str = None, 
                    color: int = 0x00ff00, fields: List[Dict[str, str]] = None,
                    footer: str = None, image_url: str = None,
                    thumbnail_url: str = None) -> Dict[str, Any]:
        """
        Create a Discord embed
        
        Args:
            title: Embed title
            description: Embed description
            color: Embed color (hexadecimal)
            fields: List of field dictionaries with 'name' and 'value' keys
            footer: Footer text
            image_url: URL for embed image
            thumbnail_url: URL for embed thumbnail
            
        Returns:
            Discord embed dictionary
        """
        embed = {
            "title": title,
            "type": "rich"
        }
        
        if description:
            embed["description"] = description
        
        if color:
            embed["color"] = color
        
        if fields:
            embed_fields = []
            for field in fields:
                embed_field = {
                    "name": field.get("name", ""),
                    "value": field.get("value", "")
                }
                
                # Optional inline property
                if "inline" in field:
                    embed_field["inline"] = bool(field["inline"])
                
                embed_fields.append(embed_field)
            
            embed["fields"] = embed_fields
        
        if footer:
            embed["footer"] = {"text": footer}
        
        if image_url:
            embed["image"] = {"url": image_url}
        
        if thumbnail_url:
            embed["thumbnail"] = {"url": thumbnail_url}
        
        # Add timestamp
        embed["timestamp"] = datetime.utcnow().isoformat()
        
        return embed


class TwitterIntegration(BaseIntegration):
    """
    Integration with Twitter (X)
    """
    
    def __init__(self, credentials: Dict[str, str] = None):
        """
        Initialize Twitter integration
        
        Args:
            credentials: Authentication credentials (api_key, api_secret, access_token, access_token_secret)
        """
        super().__init__(credentials)
    
    def authenticate(self) -> bool:
        """
        Authenticate with Twitter
        
        Returns:
            True if authentication was successful
        """
        try:
            # Check if we have the required credentials
            api_key = self.credentials.get("api_key")
            api_secret = self.credentials.get("api_secret")
            access_token = self.credentials.get("access_token")
            access_token_secret = self.credentials.get("access_token_secret")
            
            if not api_key or not api_secret:
                logger.error("Twitter API key and secret are required")
                return False
            
            # Initialize Twitter client
            if access_token and access_token_secret:
                # Use app authentication
                self.client = tweepy.Client(
                    consumer_key=api_key,
                    consumer_secret=api_secret,
                    access_token=access_token,
                    access_token_secret=access_token_secret
                )
            else:
                # Use bearer token authentication
                bearer_token = self.credentials.get("bearer_token")
                
                if not bearer_token:
                    # Generate bearer token
                    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
                    self.client = tweepy.API(auth)
                    bearer_token = self.client.request_bearer_token()
                    self.credentials["bearer_token"] = bearer_token
                
                self.client = tweepy.Client(bearer_token=bearer_token)
            
            # Verify credentials
            if self.verify_credentials():
                self.is_authenticated = True
                logger.info("Twitter authentication successful")
                return True
            else:
                logger.error("Twitter authentication failed")
                return False
            
        except Exception as e:
            logger.error(f"Twitter authentication error: {str(e)}")
            return False
    
    def verify_credentials(self) -> bool:
        """
        Verify that the Twitter credentials are valid
        
        Returns:
            True if credentials are valid
        """
        try:
            if not self.client:
                return False
            
            # Check if we can get user data
            if hasattr(self.client, 'verify_credentials'):
                self.client.verify_credentials()
                return True
            else:
                # For Client API, check by getting user info
                me = self.client.get_me()
                return me is not None
            
        except Exception as e:
            logger.error(f"Twitter credential verification error: {str(e)}")
            return False
    
    def get_auth_url(self) -> str:
        """
        Get Twitter OAuth authorization URL
        
        Returns:
            Authorization URL
        """
        try:
            # Check if we have the required credentials
            api_key = self.credentials.get("api_key")
            api_secret = self.credentials.get("api_secret")
            
            if not api_key or not api_secret:
                raise IntegrationError("Twitter API key and secret are required")
            
            # Initialize OAuth handler
            redirect_uri = self.credentials.get("redirect_uri", "https://your-app.com/twitter/callback")
            auth = tweepy.OAuth1UserHandler(api_key, api_secret, redirect_uri)
            
            # Get authorization URL
            auth_url = auth.get_authorization_url()
            
            # Store request token for later
            request_token = auth.request_token
            self.credentials["request_token"] = request_token
            
            return auth_url
            
        except Exception as e:
            logger.error(f"Twitter authorization URL error: {str(e)}")
            raise IntegrationError(f"Failed to get Twitter authorization URL: {str(e)}")
    
    def handle_oauth_callback(self, params: Dict[str, str]) -> bool:
        """
        Handle Twitter OAuth callback
        
        Args:
            params: Callback parameters
            
        Returns:
            True if authentication was successful
        """
        try:
            # Extract the verifier
            oauth_verifier = params.get("oauth_verifier")
            
            if not oauth_verifier:
                logger.error("No OAuth verifier in Twitter callback")
                return False
            
            # Get the request token
            request_token = self.credentials.get("request_token")
            
            if not request_token:
                logger.error("No request token found for Twitter")
                return False
            
            # Check if we have the required credentials
            api_key = self.credentials.get("api_key")
            api_secret = self.credentials.get("api_secret")
            
            if not api_key or not api_secret:
                logger.error("Twitter API key and secret are required")
                return False
            
            # Initialize OAuth handler
            redirect_uri = self.credentials.get("redirect_uri", "https://your-app.com/twitter/callback")
            auth = tweepy.OAuth1UserHandler(api_key, api_secret, redirect_uri)
            auth.request_token = request_token
            
            # Get access token
            access_token, access_token_secret = auth.get_access_token(oauth_verifier)
            
            # Update credentials
            self.credentials["access_token"] = access_token
            self.credentials["access_token_secret"] = access_token_secret
            
            # Authenticate with the new tokens
            return self.authenticate()
            
        except Exception as e:
            logger.error(f"Twitter OAuth callback error: {str(e)}")
            return False
    
    def post_tweet(self, text: str, media_ids: List[str] = None) -> Optional[str]:
        """
        Post a tweet
        
        Args:
            text: Tweet text
            media_ids: List of media IDs to attach to the tweet
            
        Returns:
            Tweet ID if successful, None otherwise
        """
        try:
            # Check if authenticated
            if not self.is_authenticated:
                if not self.authenticate():
                    return None
            
            # Post tweet
            response = self.client.create_tweet(text=text, media_ids=media_ids)
            
            if response and hasattr(response, 'data'):
                tweet_id = response.data.get('id')
                logger.info(f"Tweet posted: {tweet_id}")
                return tweet_id
            else:
                logger.error("Failed to post tweet")
                return None
            
        except Exception as e:
            logger.error(f"Twitter post error: {str(e)}")
            return None
    
    def upload_media(self, media_data: bytes, media_type: str = None) -> Optional[str]:
        """
        Upload media to Twitter
        
        Args:
            media_data: Media file data
            media_type: MIME type of the media
            
        Returns:
            Media ID if successful, None otherwise
        """
        try:
            # Check if authenticated
            if not self.is_authenticated:
                if not self.authenticate():
                    return None
            
            # Determine media type if not provided
            if not media_type:
                # Try to guess from first few bytes
                if media_data[:2] == b'\xff\xd8':
                    media_type = 'image/jpeg'
                elif media_data[:8] == b'\x89PNG\r\n\x1a\n':
                    media_type = 'image/png'
                elif media_data[:4] == b'GIF8':
                    media_type = 'image/gif'
                else:
                    media_type = 'application/octet-stream'
            
            # Upload media
            # Note: This requires the tweepy.API client, not the new Client
            if not hasattr(self.client, 'media_upload'):
                # Create API client for media upload
                api_key = self.credentials.get("api_key")
                api_secret = self.credentials.get("api_secret")
                access_token = self.credentials.get("access_token")
                access_token_secret = self.credentials.get("access_token_secret")
                
                auth = tweepy.OAuth1UserHandler(
                    api_key, api_secret, access_token, access_token_secret
                )
                api = tweepy.API(auth)
                
                # Upload media using API client
                media = api.media_upload(filename='media', file=io.BytesIO(media_data))
                media_id = media.media_id_string
            else:
                # Use client.media_upload if available
                media = self.client.media_upload(filename='media', file=io.BytesIO(media_data))
                media_id = media.media_id_string
            
            logger.info(f"Media uploaded to Twitter: {media_id}")
            return media_id
            
        except Exception as e:
            logger.error(f"Twitter media upload error: {str(e)}")
            return None


class WebhookIntegration(BaseIntegration):
    """
    Integration with generic webhooks
    """
    
    def __init__(self, webhook_url: str = None, secret: str = None):
        """
        Initialize webhook integration
        
        Args:
            webhook_url: Webhook URL
            secret: Secret key for signing requests
        """
        credentials = {}
        
        if webhook_url:
            credentials["webhook_url"] = webhook_url
        
        if secret:
            credentials["secret"] = secret
        
        super().__init__(credentials)
        self.is_authenticated = True  # No authentication needed for basic webhooks
    
    def authenticate(self) -> bool:
        """
        Basic webhooks don't need authentication
        
        Returns:
            True always
        """
        self.is_authenticated = True
        return True
    
    def verify_credentials(self) -> bool:
        """
        Verify that the webhook URL is valid
        
        Returns:
            True if webhook URL is valid
        """
        webhook_url = self.credentials.get("webhook_url")
        
        if not webhook_url:
            return False
        
        # Check if URL is valid
        try:
            pattern = r'^https?://[\w\-\.]+\.[a-zA-Z]{2,}(?:/[\w\-\.~:/?#[\]@!$&\'()*+,;=]*)?$'
            return bool(re.match(pattern, webhook_url))
        except Exception:
            return False
    
    def get_auth_url(self) -> str:
        """
        Not applicable for webhooks
        
        Returns:
            Empty string
        """
        return ""
    
    def handle_oauth_callback(self, params: Dict[str, str]) -> bool:
        """
        Not applicable for webhooks
        
        Args:
            params: Callback parameters
            
        Returns:
            True always
        """
        return True
    
    def send_webhook(self, data: Dict[str, Any], webhook_url: str = None) -> bool:
        """
        Send data to a webhook
        
        Args:
            data: Data to send
            webhook_url: Webhook URL (overrides the one in credentials)
            
        Returns:
            True if webhook was sent successfully
        """
        try:
            # Get webhook URL
            webhook_url = webhook_url or self.credentials.get("webhook_url")
            
            if not webhook_url:
                logger.error("Webhook URL is required")
                return False
            
            # Add timestamp
            data["timestamp"] = datetime.utcnow().isoformat()
            
            # Add signature if secret is available
            secret = self.credentials.get("secret")
            headers = {
                "Content-Type": "application/json"
            }
            
            if secret:
                payload = json.dumps(data).encode()
                signature = hmac.new(
                    secret.encode(),
                    payload,
                    hashlib.sha256
                ).hexdigest()
                headers["X-Signature"] = signature
            
            # Send webhook
            response = requests.post(
                webhook_url,
                json=data,
                headers=headers
            )
            
            if response.status_code in (200, 201, 202, 204):
                logger.info(f"Webhook sent to {webhook_url}")
                return True
            else:
                logger.error(f"Failed to send webhook: {response.status_code}")
                return False
            
        except Exception as e:
            logger.error(f"Webhook error: {str(e)}")
            return False


class SlackIntegration(BaseIntegration):
    """
    Integration with Slack
    """
    
    def __init__(self, credentials: Dict[str, str] = None):
        """
        Initialize Slack integration
        
        Args:
            credentials: Authentication credentials (oauth_token, bot_token, app_token, webhook_url)
        """
        super().__init__(credentials)
    
    def authenticate(self) -> bool:
        """
        Authenticate with Slack
        
        Returns:
            True if authentication was successful
        """
        try:
            # Check if we have a token
            bot_token = self.credentials.get("bot_token")
            oauth_token = self.credentials.get("oauth_token")
            
            token = bot_token or oauth_token
            
            if not token:
                logger.error("Slack token is required")
                return False
            
            # Make a test API call to verify the token
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get("https://slack.com/api/auth.test", headers=headers)
            data = response.json()
            
            if data.get("ok"):
                self.is_authenticated = True
                logger.info(f"Slack authentication successful as {data.get('user')}")
                return True
            else:
                logger.error(f"Slack authentication failed: {data.get('error')}")
                return False
            
        except Exception as e:
            logger.error(f"Slack authentication error: {str(e)}")
            return False
    
    def verify_credentials(self) -> bool:
        """
        Verify that the Slack credentials are valid
        
        Returns:
            True if credentials are valid
        """
        try:
            # Check if we have a token
            bot_token = self.credentials.get("bot_token")
            oauth_token = self.credentials.get("oauth_token")
            
            token = bot_token or oauth_token
            
            if not token:
                return False
            
            # Make a test API call to verify the token
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get("https://slack.com/api/auth.test", headers=headers)
            data = response.json()
            
            return data.get("ok", False)
            
        except Exception as e:
            logger.error(f"Slack credential verification error: {str(e)}")
            return False
    
    def get_auth_url(self) -> str:
        """
        Get Slack OAuth authorization URL
        
        Returns:
            Authorization URL
        """
        client_id = self.credentials.get("client_id")
        
        if not client_id:
            raise IntegrationError("Slack client ID is required")
        
        # Redirect URI should be configured in the Slack App settings
        redirect_uri = self.credentials.get("redirect_uri", "https://your-app.com/slack/callback")
        
        # Define the required scopes
        # See https://api.slack.com/scopes
        scopes = [
            "chat:write",
            "chat:write.public",
            "channels:read",
            "incoming-webhook"
        ]
        
        # Build the authorization URL
        auth_url = (
            f"https://slack.com/oauth/v2/authorize"
            f"?client_id={client_id}"
            f"&redirect_uri={requests.utils.quote(redirect_uri)}"
            f"&scope={'+'.join(scopes)}"
        )
        
        return auth_url
    
    def handle_oauth_callback(self, params: Dict[str, str]) -> bool:
        """
        Handle Slack OAuth callback
        
        Args:
            params: Callback parameters
            
        Returns:
            True if authentication was successful
        """
        try:
            # Extract the authorization code
            code = params.get("code")
            
            if not code:
                logger.error("No authorization code in Slack callback")
                return False
            
            # Exchange the code for an access token
            client_id = self.credentials.get("client_id")
            client_secret = self.credentials.get("client_secret")
            redirect_uri = self.credentials.get("redirect_uri", "https://your-app.com/slack/callback")
            
            if not client_id or not client_secret:
                logger.error("Slack client ID and secret are required")
                return False
            
            # Make the token request
            token_url = "https://slack.com/api/oauth.v2.access"
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri
            }
            
            response = requests.post(token_url, data=data)
            
            if response.status_code == 200:
                # Parse the response
                token_data = response.json()
                
                if not token_data.get("ok"):
                    logger.error(f"Slack token exchange failed: {token_data.get('error')}")
                    return False
                
                # Update credentials
                self.credentials["oauth_token"] = token_data.get("access_token")
                self.credentials["bot_token"] = token_data.get("bot_token")
                
                # Save webhook URL if available
                incoming_webhook = token_data.get("incoming_webhook", {})
                if incoming_webhook.get("url"):
                    self.credentials["webhook_url"] = incoming_webhook.get("url")
                
                # Authenticate with the new token
                return self.authenticate()
            else:
                logger.error(f"Slack token exchange failed: {response.status_code}")
                return False
            
        except Exception as e:
            logger.error(f"Slack OAuth callback error: {str(e)}")
            return False
    
    def send_message(self, channel: str, text: str, 
                    blocks: List[Dict[str, Any]] = None) -> bool:
        """
        Send a message to a Slack channel
        
        Args:
            channel: Slack channel ID or name
            text: Message text
            blocks: Slack Block Kit blocks
            
        Returns:
            True if message was sent successfully
        """
        try:
            # Check if authenticated
            if not self.is_authenticated:
                if not self.authenticate():
                    return False
            
            # Get token
            bot_token = self.credentials.get("bot_token")
            oauth_token = self.credentials.get("oauth_token")
            
            token = bot_token or oauth_token
            
            if not token:
                logger.error("Slack token is required")
                return False
            
            # Send message
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "channel": channel,
                "text": text
            }
            
            if blocks:
                data["blocks"] = blocks
            
            response = requests.post(
                "https://slack.com/api/chat.postMessage",
                headers=headers,
                json=data
            )
            
            result = response.json()
            
            if result.get("ok"):
                logger.info(f"Message sent to Slack channel {channel}")
                return True
            else:
                logger.error(f"Failed to send Slack message: {result.get('error')}")
                return False
            
        except Exception as e:
            logger.error(f"Slack message error: {str(e)}")
            return False
    
    def send_webhook(self, text: str, blocks: List[Dict[str, Any]] = None,
                    webhook_url: str = None) -> bool:
        """
        Send a message via Slack webhook
        
        Args:
            text: Message text
            blocks: Slack Block Kit blocks
            webhook_url: Webhook URL (overrides the one in credentials)
            
        Returns:
            True if webhook was sent successfully
        """
        try:
            # Get webhook URL
            webhook_url = webhook_url or self.credentials.get("webhook_url")
            
            if not webhook_url:
                logger.error("Slack webhook URL is required")
                return False
            
            # Prepare payload
            payload = {
                "text": text
            }
            
            if blocks:
                payload["blocks"] = blocks
            
            # Send webhook
            response = requests.post(webhook_url, json=payload)
            
            if response.status_code == 200:
                logger.info("Message sent to Slack webhook")
                return True
            else:
                logger.error(f"Failed to send Slack webhook: {response.status_code}")
                return False
            
        except Exception as e:
            logger.error(f"Slack webhook error: {str(e)}")
            return False
    
    def create_blocks(self, blocks_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create Slack Block Kit blocks
        
        Args:
            blocks_data: List of block data
            
        Returns:
            Formatted blocks for Slack API
        """
        # Block Kit Builder: https://app.slack.com/block-kit-builder
        return blocks_data


# Factory function to create integrations
def create_integration(service_type: str, credentials: Dict[str, str] = None) -> BaseIntegration:
    """
    Create an integration for the specified service
    
    Args:
        service_type: Type of service to integrate with (discord, twitter, webhook, slack)
        credentials: Authentication credentials
        
    Returns:
        Integration instance
    """
    service_type = service_type.lower()
    
    if service_type == "discord":
        return DiscordIntegration(credentials)
    elif service_type in ("twitter", "x"):
        return TwitterIntegration(credentials)
    elif service_type == "webhook":
        webhook_url = credentials.get("webhook_url") if credentials else None
        secret = credentials.get("secret") if credentials else None
        return WebhookIntegration(webhook_url, secret)
    elif service_type == "slack":
        return SlackIntegration(credentials)
    else:
        raise ValueError(f"Unsupported service type: {service_type}")


# Integration manager to keep track of all integrations
class IntegrationManager:
    """
    Manager for external service integrations
    """
    
    def __init__(self):
        """Initialize the integration manager"""
        self.integrations: Dict[str, BaseIntegration] = {}
    
    def add_integration(self, service_type: str, integration: BaseIntegration) -> None:
        """
        Add an integration
        
        Args:
            service_type: Type of service
            integration: Integration instance
        """
        self.integrations[service_type.lower()] = integration
    
    def get_integration(self, service_type: str) -> Optional[BaseIntegration]:
        """
        Get an integration by service type
        
        Args:
            service_type: Type of service
            
        Returns:
            Integration instance if found, None otherwise
        """
        return self.integrations.get(service_type.lower())
    
    def create_integration(self, service_type: str, 
                         credentials: Dict[str, str] = None) -> BaseIntegration:
        """
        Create and add an integration
        
        Args:
            service_type: Type of service
            credentials: Authentication credentials
            
        Returns:
            Integration instance
        """
        integration = create_integration(service_type, credentials)
        self.add_integration(service_type, integration)
        return integration
    
    def remove_integration(self, service_type: str) -> bool:
        """
        Remove an integration
        
        Args:
            service_type: Type of service
            
        Returns:
            True if integration was removed, False otherwise
        """
        service_type = service_type.lower()
        
        if service_type in self.integrations:
            del self.integrations[service_type]
            return True
        
        return False
    
    def get_all_integrations(self) -> Dict[str, BaseIntegration]:
        """
        Get all integrations
        
        Returns:
            Dictionary of service types to integration instances
        """
        return self.integrations


# Global integration manager
_integration_manager = None

def get_integration_manager() -> IntegrationManager:
    """
    Get the global integration manager
    
    Returns:
        IntegrationManager instance
    """
    global _integration_manager
    
    if _integration_manager is None:
        _integration_manager = IntegrationManager()
    
    return _integration_manager