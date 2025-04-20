from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api import (
    get_chat_conversations,
    get_chat_messages
)
from utils.roblox_api import RobloxAPIError

logger = logging.getLogger(__name__)

class ChatConversationsResource(Resource):
    """
    Resource for getting user's chat conversations
    """
    def get(self):
        """
        Get user's chat conversations
        
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 100)
            
        Returns:
            dict: User's chat conversations or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 100)
        
        try:
            conversations_data = get_chat_conversations(limit)
            return {
                "success": True,
                "data": conversations_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting chat conversations: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting chat conversations: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ChatMessagesResource(Resource):
    """
    Resource for getting messages from a chat conversation
    """
    def get(self):
        """
        Get messages from a chat conversation
        
        Query Parameters:
            conversation_id (int, required): The conversation ID
            limit (int, optional): Maximum number of results (default: 100)
            
        Returns:
            dict: Chat messages or error response
        """
        conversation_id = request.args.get('conversation_id')
        if not conversation_id:
            return {
                "success": False,
                "message": "conversation_id query parameter is required"
            }, 400
            
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 100)
        
        try:
            messages_data = get_chat_messages(conversation_id, limit)
            return {
                "success": True,
                "data": messages_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting chat messages: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting chat messages: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500