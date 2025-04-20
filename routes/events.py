from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api import (
    get_user_events,
    get_game_events,
    get_group_events,
    get_event_history,
    get_event_details,
    filter_events_by_type,
    RobloxAPIError
)

logger = logging.getLogger(__name__)

class UserEventsResource(Resource):
    """
    Resource for getting event notifications for a user
    """
    def get(self, user_id):
        """
        Get event notifications for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            event_types (str, optional): Comma-separated list of event types to include
            
        Returns:
            dict: User's event notifications or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('limit', 25)
        event_types = request.args.get('event_types', None)
        
        if event_types:
            event_types = event_types.split(',')
        
        try:
            events_data = get_user_events(user_id, max_rows)
            
            if event_types:
                events_data = filter_events_by_type(events_data, event_types)
                
            return {
                "success": True,
                "data": events_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user events: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user events: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GameEventsResource(Resource):
    """
    Resource for getting event notifications for a game
    """
    def get(self, universe_id):
        """
        Get event notifications for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            event_types (str, optional): Comma-separated list of event types to include
            
        Returns:
            dict: Game's event notifications or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('limit', 25)
        event_types = request.args.get('event_types', None)
        
        if event_types:
            event_types = event_types.split(',')
        
        try:
            events_data = get_game_events(universe_id, max_rows)
            
            if event_types:
                events_data = filter_events_by_type(events_data, event_types)
                
            return {
                "success": True,
                "data": events_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game events: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game events: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GroupEventsResource(Resource):
    """
    Resource for getting event notifications for a group
    """
    def get(self, group_id):
        """
        Get event notifications for a group
        
        Args:
            group_id (int): The Roblox group ID
            
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            event_types (str, optional): Comma-separated list of event types to include
            
        Returns:
            dict: Group's event notifications or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('limit', 25)
        event_types = request.args.get('event_types', None)
        
        if event_types:
            event_types = event_types.split(',')
        
        try:
            events_data = get_group_events(group_id, max_rows)
            
            if event_types:
                events_data = filter_events_by_type(events_data, event_types)
                
            return {
                "success": True,
                "data": events_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting group events: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting group events: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class EventHistoryResource(Resource):
    """
    Resource for getting event history for an entity
    """
    def get(self, entity_type, entity_id):
        """
        Get event history for an entity
        
        Args:
            entity_type (str): The type of entity ('user', 'game', 'group')
            entity_id (int): The ID of the entity
            
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            event_types (str, optional): Comma-separated list of event types to include
            
        Returns:
            dict: Entity's event history or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('limit', 25)
        event_types = request.args.get('event_types', None)
        
        if event_types:
            event_types = event_types.split(',')
        
        try:
            events_data = get_event_history(entity_type, entity_id, max_rows)
            
            if event_types:
                events_data = filter_events_by_type(events_data, event_types)
                
            return {
                "success": True,
                "data": events_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting event history: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting event history: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class EventDetailsResource(Resource):
    """
    Resource for getting details about a specific event
    """
    def get(self, event_id):
        """
        Get details about a specific event
        
        Args:
            event_id (int): The Roblox event ID
            
        Returns:
            dict: Event details or error response
        """
        try:
            event_data = get_event_details(event_id)
                
            return {
                "success": True,
                "data": event_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting event details: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting event details: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500