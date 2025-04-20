from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api import (
    get_game_team_create_members,
    get_game_packages,
    get_game_current_version,
    get_game_version_history
)
from utils.roblox_api import RobloxAPIError

logger = logging.getLogger(__name__)

class GameTeamCreateMembersResource(Resource):
    """
    Resource for getting team create members for a game
    """
    def get(self, universe_id):
        """
        Get team create members for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Returns:
            dict: Team create members or error response
        """
        try:
            members_data = get_game_team_create_members(universe_id)
            return {
                "success": True,
                "data": members_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting team create members: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting team create members: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GamePackagesResource(Resource):
    """
    Resource for getting packages used in a game
    """
    def get(self, universe_id):
        """
        Get packages used in a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Returns:
            dict: Game packages or error response
        """
        try:
            packages_data = get_game_packages(universe_id)
            return {
                "success": True,
                "data": packages_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game packages: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game packages: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GameCurrentVersionResource(Resource):
    """
    Resource for getting current version information for a game
    """
    def get(self, universe_id):
        """
        Get current version information for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Returns:
            dict: Game current version or error response
        """
        try:
            version_data = get_game_current_version(universe_id)
            return {
                "success": True,
                "data": version_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game current version: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game current version: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GameVersionHistoryResource(Resource):
    """
    Resource for getting version history for a game
    """
    def get(self, universe_id):
        """
        Get version history for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            
        Returns:
            dict: Game version history or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        
        try:
            version_history = get_game_version_history(universe_id, limit)
            return {
                "success": True,
                "data": version_history
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game version history: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game version history: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500