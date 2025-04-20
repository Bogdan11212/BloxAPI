from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api import (
    get_user_avatar, 
    get_user_avatar_meta, 
    get_user_outfits, 
    get_outfit_details
)
from utils.roblox_api import RobloxAPIError

logger = logging.getLogger(__name__)

class UserAvatarResource(Resource):
    """
    Resource for getting a user's avatar information
    """
    def get(self, user_id):
        """
        Get a user's avatar
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's avatar information or error response
        """
        try:
            avatar_data = get_user_avatar(user_id)
            return {
                "success": True,
                "data": avatar_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user avatar: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user avatar: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserAvatarMetaResource(Resource):
    """
    Resource for getting a user's avatar metadata
    """
    def get(self, user_id):
        """
        Get metadata about a user's avatar
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's avatar metadata or error response
        """
        try:
            meta_data = get_user_avatar_meta(user_id)
            return {
                "success": True,
                "data": meta_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user avatar meta: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user avatar meta: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserOutfitsResource(Resource):
    """
    Resource for getting a user's outfits
    """
    def get(self, user_id):
        """
        Get a user's outfits
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 25)
            
        Returns:
            dict: User's outfits or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 25)
        
        try:
            outfits_data = get_user_outfits(user_id, limit)
            return {
                "success": True,
                "data": outfits_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user outfits: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user outfits: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class OutfitDetailsResource(Resource):
    """
    Resource for getting details about a specific outfit
    """
    def get(self, outfit_id):
        """
        Get details about a specific outfit
        
        Args:
            outfit_id (int): The Roblox outfit ID
            
        Returns:
            dict: Outfit details or error response
        """
        try:
            outfit_data = get_outfit_details(outfit_id)
            return {
                "success": True,
                "data": outfit_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting outfit details: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting outfit details: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500