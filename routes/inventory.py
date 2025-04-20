from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api import (
    get_user_inventory,
    get_user_collectibles
)
from utils.roblox_api import RobloxAPIError

logger = logging.getLogger(__name__)

class UserInventoryResource(Resource):
    """
    Resource for getting a user's inventory
    """
    def get(self, user_id, asset_type):
        """
        Get a user's inventory items of a specific asset type
        
        Args:
            user_id (int): The Roblox user ID
            asset_type (str): The type of asset (e.g., "Hat", "Shirt", "Pants", etc.)
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 100)
            
        Returns:
            dict: User's inventory items or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 100)
        
        try:
            inventory_data = get_user_inventory(user_id, asset_type, limit)
            return {
                "success": True,
                "data": inventory_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user inventory: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user inventory: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserCollectiblesResource(Resource):
    """
    Resource for getting a user's collectible items
    """
    def get(self, user_id):
        """
        Get a user's collectible items
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 100)
            
        Returns:
            dict: User's collectible items or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 100)
        
        try:
            collectibles_data = get_user_collectibles(user_id, limit)
            return {
                "success": True,
                "data": collectibles_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user collectibles: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user collectibles: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500