from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api_extra import (
    get_user_subscriptions,
    get_user_subscribers,
    get_user_subscription_details,
    get_subscription_options,
    check_subscription_status,
    get_subscription_notifications,
    get_subscription_feed,
    RobloxAPIError
)

logger = logging.getLogger(__name__)

class UserSubscriptionsResource(Resource):
    """
    Resource for getting subscriptions for a user
    """
    def get(self, user_id):
        """
        Get subscriptions for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            cursor (str, optional): Cursor for pagination
            
        Returns:
            dict: User's subscriptions or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        cursor = request.args.get('cursor', None)
        
        try:
            subscriptions_data = get_user_subscriptions(user_id, limit, cursor)
            
            return {
                "success": True,
                "data": subscriptions_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user subscriptions: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user subscriptions: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserSubscribersResource(Resource):
    """
    Resource for getting subscribers for a user
    """
    def get(self, user_id):
        """
        Get subscribers for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            cursor (str, optional): Cursor for pagination
            
        Returns:
            dict: User's subscribers or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        cursor = request.args.get('cursor', None)
        
        try:
            subscribers_data = get_user_subscribers(user_id, limit, cursor)
            
            return {
                "success": True,
                "data": subscribers_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user subscribers: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user subscribers: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserSubscriptionDetailsResource(Resource):
    """
    Resource for getting details about a user's subscription
    """
    def get(self, user_id, subscription_id):
        """
        Get details about a user's subscription
        
        Args:
            user_id (int): The Roblox user ID
            subscription_id (int): The Roblox subscription ID
            
        Returns:
            dict: Subscription details or error response
        """
        try:
            details_data = get_user_subscription_details(user_id, subscription_id)
            
            return {
                "success": True,
                "data": details_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting subscription details: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting subscription details: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class SubscriptionOptionsResource(Resource):
    """
    Resource for getting subscription options for a user or entity
    """
    def get(self, entity_type, entity_id):
        """
        Get subscription options for a user or entity
        
        Args:
            entity_type (str): The type of entity ('user', 'group', 'game')
            entity_id (int): The ID of the entity
            
        Returns:
            dict: Subscription options or error response
        """
        try:
            options_data = get_subscription_options(entity_type, entity_id)
            
            return {
                "success": True,
                "data": options_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting subscription options: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting subscription options: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class SubscriptionStatusResource(Resource):
    """
    Resource for checking subscription status
    """
    def get(self, user_id, entity_type, entity_id):
        """
        Check subscription status
        
        Args:
            user_id (int): The Roblox user ID
            entity_type (str): The type of entity subscribed to ('user', 'group', 'game')
            entity_id (int): The ID of the entity
            
        Returns:
            dict: Subscription status or error response
        """
        try:
            status_data = check_subscription_status(user_id, entity_type, entity_id)
            
            return {
                "success": True,
                "data": status_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error checking subscription status: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error checking subscription status: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class SubscriptionNotificationsResource(Resource):
    """
    Resource for getting subscription notifications
    """
    def get(self, user_id):
        """
        Get subscription notifications for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            cursor (str, optional): Cursor for pagination
            
        Returns:
            dict: Subscription notifications or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        cursor = request.args.get('cursor', None)
        
        try:
            notifications_data = get_subscription_notifications(user_id, limit, cursor)
            
            return {
                "success": True,
                "data": notifications_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting subscription notifications: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting subscription notifications: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class SubscriptionFeedResource(Resource):
    """
    Resource for getting subscription feed
    """
    def get(self, user_id):
        """
        Get subscription feed for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            cursor (str, optional): Cursor for pagination
            
        Returns:
            dict: Subscription feed or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        cursor = request.args.get('cursor', None)
        
        try:
            feed_data = get_subscription_feed(user_id, limit, cursor)
            
            return {
                "success": True,
                "data": feed_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting subscription feed: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting subscription feed: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500