from flask import request
from flask_restful import Resource
import logging
from utils.roblox_api import (
    get_notifications,
    get_notification_counts
)
from utils.roblox_api import RobloxAPIError

logger = logging.getLogger(__name__)

class NotificationsResource(Resource):
    """
    Resource for getting user's notifications
    """
    def get(self):
        """
        Get user's notifications
        
        Returns:
            dict: User's notifications or error response
        """
        try:
            notifications_data = get_notifications()
            return {
                "success": True,
                "data": notifications_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting notifications: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting notifications: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class NotificationCountsResource(Resource):
    """
    Resource for getting counts of user's notifications by type
    """
    def get(self):
        """
        Get counts of user's notifications by type
        
        Returns:
            dict: Notification counts or error response
        """
        try:
            counts_data = get_notification_counts()
            return {
                "success": True,
                "data": counts_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting notification counts: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting notification counts: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500