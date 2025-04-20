from flask import request
from flask_restful import Resource
import logging
from utils.roblox_api import (
    get_user_friends, get_friend_requests,
    get_friends_count, RobloxAPIError
)

logger = logging.getLogger(__name__)

class FriendsResource(Resource):
    """
    Resource for getting a user's friends on Roblox
    """
    def get(self, user_id):
        """
        Get a user's friends
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            include_count (bool, optional): Whether to include friend count
            
        Returns:
            dict: User's friends or error response
        """
        try:
            # Get friends data
            friends_data = get_user_friends(user_id)
            
            # Check if should include count
            include_count = request.args.get('include_count', 'false').lower() == 'true'
            if include_count:
                try:
                    count_data = get_friends_count(user_id)
                    friends_data["count"] = count_data.get("count", 0)
                except RobloxAPIError as e:
                    logger.warning(f"Failed to get friends count: {str(e)}")
                    friends_data["count"] = {"error": str(e)}
            
            return {
                "success": True,
                "data": friends_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting friends: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in FriendsResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class FriendRequestsResource(Resource):
    """
    Resource for getting a user's friend requests on Roblox
    """
    def get(self, user_id):
        """
        Get a user's friend requests
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's friend requests or error response
        """
        try:
            requests_data = get_friend_requests(user_id)
            
            return {
                "success": True,
                "data": requests_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting friend requests: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in FriendRequestsResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500
