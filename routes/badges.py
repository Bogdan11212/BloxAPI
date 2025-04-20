from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api import (
    get_game_badges,
    get_badge_info,
    get_badge_awarded_dates,
    get_user_badges
)
from utils.roblox_api import RobloxAPIError

logger = logging.getLogger(__name__)

class GameBadgesResource(Resource):
    """
    Resource for getting badges for a game
    """
    def get(self, universe_id):
        """
        Get badges for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            
        Returns:
            dict: Game badges or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        
        try:
            badges_data = get_game_badges(universe_id, limit)
            return {
                "success": True,
                "data": badges_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game badges: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game badges: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class BadgeInfoResource(Resource):
    """
    Resource for getting information about a specific badge
    """
    def get(self, badge_id):
        """
        Get information about a specific badge
        
        Args:
            badge_id (int): The Roblox badge ID
            
        Returns:
            dict: Badge information or error response
        """
        try:
            badge_data = get_badge_info(badge_id)
            return {
                "success": True,
                "data": badge_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting badge info: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting badge info: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class BadgeAwardedDatesResource(Resource):
    """
    Resource for getting the date when a badge was awarded to a user
    """
    def get(self, badge_id, user_id):
        """
        Get date when a badge was awarded to a user
        
        Args:
            badge_id (int): The Roblox badge ID
            user_id (int): The Roblox user ID
            
        Returns:
            dict: Badge awarded date or error response
        """
        try:
            awarded_dates = get_badge_awarded_dates(badge_id, user_id)
            return {
                "success": True,
                "data": awarded_dates
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting badge awarded dates: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting badge awarded dates: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserBadgesResource(Resource):
    """
    Resource for getting badges owned by a user
    """
    def get(self, user_id):
        """
        Get badges owned by a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            
        Returns:
            dict: User badges or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        
        try:
            user_badges_data = get_user_badges(user_id, limit)
            return {
                "success": True,
                "data": user_badges_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user badges: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user badges: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500