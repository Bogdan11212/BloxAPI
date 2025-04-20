from flask import request
from flask_restful import Resource
import logging
from marshmallow import Schema, fields, validate
from utils.roblox_api import (
    get_user_thumbnails,
    get_asset_thumbnails,
    get_game_thumbnails
)
from utils.roblox_api import RobloxAPIError

logger = logging.getLogger(__name__)

class UserThumbnailsResource(Resource):
    """
    Resource for getting thumbnails for users
    """
    def get(self):
        """
        Get thumbnails for users
        
        Query Parameters:
            user_ids (str, required): Comma-separated list of Roblox user IDs
            size (str, optional): Thumbnail size (default: "420x420")
            format (str, optional): Image format (default: "Png")
            is_circular (bool, optional): Whether to return circular thumbnails (default: false)
            
        Returns:
            dict: User thumbnails or error response
        """
        user_ids_str = request.args.get('user_ids')
        size = request.args.get('size', '420x420')
        format = request.args.get('format', 'Png')
        is_circular = request.args.get('is_circular', 'false').lower() == 'true'
        
        if not user_ids_str:
            return {
                "success": False,
                "message": "user_ids query parameter is required"
            }, 400
            
        try:
            user_ids = [int(user_id.strip()) for user_id in user_ids_str.split(',')]
            
            thumbnails_data = get_user_thumbnails(user_ids, size, format, is_circular)
            return {
                "success": True,
                "data": thumbnails_data
            }
        except ValueError:
            return {
                "success": False,
                "message": "Invalid user IDs provided, must be comma-separated integers"
            }, 400
        except RobloxAPIError as e:
            logger.error(f"Error getting user thumbnails: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user thumbnails: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class AssetThumbnailsResource(Resource):
    """
    Resource for getting thumbnails for assets
    """
    def get(self):
        """
        Get thumbnails for assets
        
        Query Parameters:
            asset_ids (str, required): Comma-separated list of Roblox asset IDs
            size (str, optional): Thumbnail size (default: "420x420")
            format (str, optional): Image format (default: "Png")
            
        Returns:
            dict: Asset thumbnails or error response
        """
        asset_ids_str = request.args.get('asset_ids')
        size = request.args.get('size', '420x420')
        format = request.args.get('format', 'Png')
        
        if not asset_ids_str:
            return {
                "success": False,
                "message": "asset_ids query parameter is required"
            }, 400
            
        try:
            asset_ids = [int(asset_id.strip()) for asset_id in asset_ids_str.split(',')]
            
            thumbnails_data = get_asset_thumbnails(asset_ids, size, format)
            return {
                "success": True,
                "data": thumbnails_data
            }
        except ValueError:
            return {
                "success": False,
                "message": "Invalid asset IDs provided, must be comma-separated integers"
            }, 400
        except RobloxAPIError as e:
            logger.error(f"Error getting asset thumbnails: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting asset thumbnails: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GameThumbnailsResource(Resource):
    """
    Resource for getting thumbnails for games
    """
    def get(self):
        """
        Get thumbnails for games
        
        Query Parameters:
            universe_ids (str, required): Comma-separated list of Roblox universe IDs
            size (str, optional): Thumbnail size (default: "768x432")
            format (str, optional): Image format (default: "Png")
            
        Returns:
            dict: Game thumbnails or error response
        """
        universe_ids_str = request.args.get('universe_ids')
        size = request.args.get('size', '768x432')
        format = request.args.get('format', 'Png')
        
        if not universe_ids_str:
            return {
                "success": False,
                "message": "universe_ids query parameter is required"
            }, 400
            
        try:
            universe_ids = [int(universe_id.strip()) for universe_id in universe_ids_str.split(',')]
            
            thumbnails_data = get_game_thumbnails(universe_ids, size, format)
            return {
                "success": True,
                "data": thumbnails_data
            }
        except ValueError:
            return {
                "success": False,
                "message": "Invalid universe IDs provided, must be comma-separated integers"
            }, 400
        except RobloxAPIError as e:
            logger.error(f"Error getting game thumbnails: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game thumbnails: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500