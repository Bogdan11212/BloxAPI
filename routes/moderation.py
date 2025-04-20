from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api_extra import (
    get_content_moderation_status,
    get_moderation_history,
    check_asset_moderation,
    check_text_moderation,
    check_image_moderation,
    report_abuse,
    get_safety_settings,
    RobloxAPIError
)

logger = logging.getLogger(__name__)

class ContentModerationStatusResource(Resource):
    """
    Resource for checking content moderation status
    """
    def get(self, content_id, content_type):
        """
        Check moderation status of content
        
        Args:
            content_id (int): The ID of the content
            content_type (str): The type of content ('asset', 'game', 'comment', etc.)
            
        Returns:
            dict: Content moderation status or error response
        """
        try:
            status_data = get_content_moderation_status(content_id, content_type)
            
            return {
                "success": True,
                "data": status_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error checking content moderation status: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error checking content moderation status: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ModerationHistoryResource(Resource):
    """
    Resource for getting moderation history for a user
    """
    def get(self, user_id):
        """
        Get moderation history for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 25)
            
        Returns:
            dict: User's moderation history or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 25)
        
        try:
            history_data = get_moderation_history(user_id, limit)
            
            return {
                "success": True,
                "data": history_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting moderation history: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting moderation history: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class AssetModerationCheckResource(Resource):
    """
    Resource for checking moderation status of an asset
    """
    def get(self, asset_id):
        """
        Check moderation status of an asset
        
        Args:
            asset_id (int): The Roblox asset ID
            
        Returns:
            dict: Asset moderation status or error response
        """
        try:
            moderation_data = check_asset_moderation(asset_id)
            
            return {
                "success": True,
                "data": moderation_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error checking asset moderation: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error checking asset moderation: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class TextModerationCheckResource(Resource):
    """
    Resource for checking moderation of text content
    """
    def post(self):
        """
        Check moderation of text content
        
        Request Body:
            {
                "text": "The text to check for moderation"
            }
            
        Returns:
            dict: Text moderation check results or error response
        """
        data = request.get_json()
        
        if not data or 'text' not in data:
            return {
                "success": False,
                "message": "Missing required parameter: text"
            }, 400
        
        text = data['text']
        
        try:
            moderation_data = check_text_moderation(text)
            
            return {
                "success": True,
                "data": moderation_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error checking text moderation: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error checking text moderation: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ImageModerationCheckResource(Resource):
    """
    Resource for checking moderation of image content
    """
    def post(self):
        """
        Check moderation of image content
        
        Request Body:
            {
                "image_url": "URL of the image to check"
            }
            
        Returns:
            dict: Image moderation check results or error response
        """
        data = request.get_json()
        
        if not data or 'image_url' not in data:
            return {
                "success": False,
                "message": "Missing required parameter: image_url"
            }, 400
        
        image_url = data['image_url']
        
        try:
            moderation_data = check_image_moderation(image_url)
            
            return {
                "success": True,
                "data": moderation_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error checking image moderation: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error checking image moderation: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ReportAbuseResource(Resource):
    """
    Resource for reporting abuse
    """
    def post(self):
        """
        Report abuse
        
        Request Body:
            {
                "content_id": 123,
                "content_type": "asset",
                "reason": "Inappropriate content",
                "details": "This asset contains inappropriate content"
            }
            
        Returns:
            dict: Report abuse response or error
        """
        data = request.get_json()
        
        if not data:
            return {
                "success": False,
                "message": "Missing request body"
            }, 400
        
        required_fields = ['content_id', 'content_type', 'reason']
        for field in required_fields:
            if field not in data:
                return {
                    "success": False,
                    "message": f"Missing required parameter: {field}"
                }, 400
        
        content_id = data['content_id']
        content_type = data['content_type']
        reason = data['reason']
        details = data.get('details', '')
        
        try:
            report_data = report_abuse(content_id, content_type, reason, details)
            
            return {
                "success": True,
                "data": report_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error reporting abuse: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error reporting abuse: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class SafetySettingsResource(Resource):
    """
    Resource for getting safety settings for a user
    """
    def get(self, user_id):
        """
        Get safety settings for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's safety settings or error response
        """
        try:
            settings_data = get_safety_settings(user_id)
            
            return {
                "success": True,
                "data": settings_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting safety settings: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting safety settings: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500