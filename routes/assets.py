from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
import logging
from utils.validators import AssetInfoSchema
from utils.roblox_api import (
    get_asset_info, get_asset_bundles,
    RobloxAPIError
)

logger = logging.getLogger(__name__)

class AssetResource(Resource):
    """
    Resource for getting information about a specific Roblox asset
    """
    def get(self, asset_id):
        """
        Get information about an asset by its ID
        
        Args:
            asset_id (int): The Roblox asset ID
            
        Returns:
            dict: Asset information or error response
        """
        try:
            asset_data = get_asset_info(asset_id)
            return {
                "success": True,
                "data": asset_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting asset info: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in AssetResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class AssetInfoResource(Resource):
    """
    Resource for getting detailed information about a Roblox asset
    """
    def get(self, asset_id):
        """
        Get detailed information about an asset by its ID
        
        Args:
            asset_id (int): The Roblox asset ID
            
        Query Parameters:
            include_bundles (bool, optional): Whether to include bundles containing this asset
            
        Returns:
            dict: Detailed asset information or error response
        """
        try:
            # Validate query parameters
            schema = AssetInfoSchema()
            params = schema.load(request.args)
            
            # Get asset info
            asset_data = get_asset_info(asset_id)
            
            # Check if should include bundles
            include_bundles = request.args.get('include_bundles', 'false').lower() == 'true'
            if include_bundles:
                try:
                    bundles_data = get_asset_bundles(asset_id)
                    asset_data["bundles"] = bundles_data
                except RobloxAPIError as e:
                    logger.warning(f"Failed to get asset bundles: {str(e)}")
                    asset_data["bundles"] = {"error": str(e)}
            
            return {
                "success": True,
                "data": asset_data
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
            logger.error(f"Error getting detailed asset info: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in AssetInfoResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500
