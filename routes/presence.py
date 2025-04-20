from flask import request
from flask_restful import Resource
import logging
from marshmallow import Schema, fields, validate
from utils.roblox_api import (
    get_user_presence,
    get_last_online
)
from utils.roblox_api import RobloxAPIError

logger = logging.getLogger(__name__)

class UserIdsSchema(Schema):
    """Schema for validating user IDs"""
    userIds = fields.List(
        fields.Integer(validate=validate.Range(min=1)),
        required=True,
        validate=validate.Length(min=1, max=100)
    )

class UserPresenceResource(Resource):
    """
    Resource for getting presence information for users
    """
    def post(self):
        """
        Get presence information for users
        
        JSON Body:
            userIds (list): List of Roblox user IDs
            
        Returns:
            dict: User presence information or error response
        """
        schema = UserIdsSchema()
        
        try:
            data = request.get_json()
            if not data:
                return {
                    "success": False,
                    "message": "No JSON data provided"
                }, 400
                
            validated_data = schema.load(data)
            user_ids = validated_data['userIds']
            
            presence_data = get_user_presence(user_ids)
            return {
                "success": True,
                "data": presence_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user presence: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user presence: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class LastOnlineResource(Resource):
    """
    Resource for getting last online time for users
    """
    def post(self):
        """
        Get last online time for users
        
        JSON Body:
            userIds (list): List of Roblox user IDs
            
        Returns:
            dict: User last online times or error response
        """
        schema = UserIdsSchema()
        
        try:
            data = request.get_json()
            if not data:
                return {
                    "success": False,
                    "message": "No JSON data provided"
                }, 400
                
            validated_data = schema.load(data)
            user_ids = validated_data['userIds']
            
            last_online_data = get_last_online(user_ids)
            return {
                "success": True,
                "data": last_online_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting last online times: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting last online times: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500