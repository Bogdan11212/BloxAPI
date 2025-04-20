from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
import logging
from utils.validators import UserIdListSchema, SearchSchema
from utils.roblox_api import (
    get_user_info, get_users_info, search_users,
    get_user_by_username, RobloxAPIError
)

logger = logging.getLogger(__name__)

class UserResource(Resource):
    """
    Resource for getting information about a specific Roblox user
    """
    def get(self, user_id):
        """
        Get information about a user by their ID
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User information or error response
        """
        try:
            user_data = get_user_info(user_id)
            return {
                "success": True,
                "data": user_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user info: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in UserResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class UserBatchResource(Resource):
    """
    Resource for getting information about multiple Roblox users
    """
    def post(self):
        """
        Get information about multiple users by their IDs
        
        JSON Body:
            userIds (list): List of Roblox user IDs
            
        Returns:
            dict: User information or error response
        """
        try:
            # Validate request data
            schema = UserIdListSchema()
            data = schema.load(request.json or {})
            
            # Get user information
            users_data = get_users_info(data["userIds"])
            
            return {
                "success": True,
                "data": users_data
            }
        except ValidationError as e:
            return {
                "success": False,
                "error": {
                    "code": 400,
                    "message": "Validation error",
                    "details": e.messages
                }
            }, 400
        except RobloxAPIError as e:
            logger.error(f"Error getting batch user info: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in UserBatchResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class UserSearchResource(Resource):
    """
    Resource for searching Roblox users
    """
    def get(self):
        """
        Search for users by keyword
        
        Query Parameters:
            keyword (str): Search term
            limit (int, optional): Maximum number of results (default: 10)
            
        Returns:
            dict: Search results or error response
        """
        try:
            # Validate query parameters
            schema = SearchSchema()
            params = schema.load(request.args)
            
            # Search for users
            search_results = search_users(params["keyword"], params.get("limit", 10))
            
            return {
                "success": True,
                "data": search_results
            }
        except ValidationError as e:
            return {
                "success": False,
                "error": {
                    "code": 400,
                    "message": "Validation error",
                    "details": e.messages
                }
            }, 400
        except RobloxAPIError as e:
            logger.error(f"Error searching users: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in UserSearchResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500
