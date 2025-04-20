from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
import logging
from utils.validators import GameSearchSchema, PaginationSchema
from utils.roblox_api import (
    get_game_details, get_games_by_user,
    get_game_social_links, get_game_passes,
    RobloxAPIError
)

logger = logging.getLogger(__name__)

class GameResource(Resource):
    """
    Resource for getting information about a specific Roblox game
    """
    def get(self, game_id):
        """
        Get information about a game by its ID
        
        Args:
            game_id (int): The Roblox game ID
            
        Returns:
            dict: Game information or error response
        """
        try:
            game_data = get_game_details(game_id)
            return {
                "success": True,
                "data": game_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game info: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in GameResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class GameListResource(Resource):
    """
    Resource for listing Roblox games
    """
    def get(self):
        """
        Get list of games created by a user
        
        Query Parameters:
            user_id (int): The Roblox user ID
            limit (int, optional): Maximum number of results (default: 50)
            
        Returns:
            dict: List of games or error response
        """
        try:
            # Validate query parameters
            user_id = request.args.get('user_id')
            if not user_id:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameter: user_id"
                    }
                }, 400
                
            schema = PaginationSchema()
            params = schema.load(request.args)
            
            # Get games by user
            games_data = get_games_by_user(user_id, params.get("limit", 50))
            
            return {
                "success": True,
                "data": games_data
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
            logger.error(f"Error getting games list: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in GameListResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class GameDetailsResource(Resource):
    """
    Resource for getting detailed information about a game
    """
    def get(self, game_id):
        """
        Get detailed information about a game including social links and passes
        
        Args:
            game_id (int): The Roblox game ID
            
        Returns:
            dict: Detailed game information or error response
        """
        try:
            # Get basic game details
            game_data = get_game_details(game_id)
            
            # Get additional information
            try:
                social_links = get_game_social_links(game_id)
            except RobloxAPIError as e:
                social_links = {"error": str(e)}
            
            try:
                game_passes = get_game_passes(game_id)
            except RobloxAPIError as e:
                game_passes = {"error": str(e)}
            
            # Combine all information
            detailed_data = {
                "details": game_data,
                "socialLinks": social_links,
                "gamePasses": game_passes
            }
            
            return {
                "success": True,
                "data": detailed_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game details: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in GameDetailsResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500
