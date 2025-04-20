from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api_extra import (
    get_game_server_instances,
    get_server_details,
    get_server_players,
    get_server_stats,
    get_server_logs,
    send_server_message,
    shutdown_server,
    get_server_join_script,
    get_vip_servers,
    create_vip_server,
    update_vip_server,
    get_vip_server_subscribers,
    get_private_servers,
    RobloxAPIError
)

logger = logging.getLogger(__name__)

class GameServerInstancesResource(Resource):
    """
    Resource for getting server instances for a game
    """
    def get(self, universe_id):
        """
        Get server instances for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 25)
            cursor (str, optional): Cursor for pagination
            min_players (int, optional): Minimum number of players
            max_players (int, optional): Maximum number of players
            exclude_full (bool, optional): Whether to exclude full servers
            
        Returns:
            dict: Game server instances or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 25)
        cursor = request.args.get('cursor', None)
        
        min_players = request.args.get('min_players', None)
        if min_players:
            min_players = int(min_players)
        
        max_players = request.args.get('max_players', None)
        if max_players:
            max_players = int(max_players)
        
        exclude_full = request.args.get('exclude_full', 'false').lower() == 'true'
        
        try:
            instances_data = get_game_server_instances(
                universe_id, 
                limit,
                cursor,
                min_players,
                max_players,
                exclude_full
            )
            
            return {
                "success": True,
                "data": instances_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game server instances: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game server instances: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ServerDetailsResource(Resource):
    """
    Resource for getting details about a server
    """
    def get(self, server_id):
        """
        Get details about a server
        
        Args:
            server_id (str): The Roblox server ID
            
        Returns:
            dict: Server details or error response
        """
        try:
            server_data = get_server_details(server_id)
            
            return {
                "success": True,
                "data": server_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting server details: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting server details: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ServerPlayersResource(Resource):
    """
    Resource for getting players in a server
    """
    def get(self, server_id):
        """
        Get players in a server
        
        Args:
            server_id (str): The Roblox server ID
            
        Returns:
            dict: Server players or error response
        """
        try:
            players_data = get_server_players(server_id)
            
            return {
                "success": True,
                "data": players_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting server players: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting server players: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ServerStatsResource(Resource):
    """
    Resource for getting stats about a server
    """
    def get(self, server_id):
        """
        Get stats about a server
        
        Args:
            server_id (str): The Roblox server ID
            
        Returns:
            dict: Server stats or error response
        """
        try:
            stats_data = get_server_stats(server_id)
            
            return {
                "success": True,
                "data": stats_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting server stats: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting server stats: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ServerLogsResource(Resource):
    """
    Resource for getting logs from a server
    """
    def get(self, server_id):
        """
        Get logs from a server
        
        Args:
            server_id (str): The Roblox server ID
            
        Query Parameters:
            limit (int, optional): Maximum number of log entries (default: 100)
            
        Returns:
            dict: Server logs or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 100)
        
        try:
            logs_data = get_server_logs(server_id, limit)
            
            return {
                "success": True,
                "data": logs_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting server logs: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting server logs: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ServerMessageResource(Resource):
    """
    Resource for sending a message to a server
    """
    def post(self, server_id):
        """
        Send a message to a server
        
        Args:
            server_id (str): The Roblox server ID
            
        Request Body:
            {
                "message": "The message to send"
            }
            
        Returns:
            dict: Response or error
        """
        data = request.get_json()
        
        if not data or 'message' not in data:
            return {
                "success": False,
                "message": "Missing required parameter: message"
            }, 400
        
        message = data['message']
        
        try:
            result = send_server_message(server_id, message)
            
            return {
                "success": True,
                "data": result
            }
        except RobloxAPIError as e:
            logger.error(f"Error sending server message: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error sending server message: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ServerShutdownResource(Resource):
    """
    Resource for shutting down a server
    """
    def post(self, server_id):
        """
        Shut down a server
        
        Args:
            server_id (str): The Roblox server ID
            
        Returns:
            dict: Response or error
        """
        try:
            result = shutdown_server(server_id)
            
            return {
                "success": True,
                "data": result
            }
        except RobloxAPIError as e:
            logger.error(f"Error shutting down server: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error shutting down server: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ServerJoinScriptResource(Resource):
    """
    Resource for getting the join script for a server
    """
    def get(self, server_id):
        """
        Get the join script for a server
        
        Args:
            server_id (str): The Roblox server ID
            
        Returns:
            dict: Server join script or error response
        """
        try:
            script_data = get_server_join_script(server_id)
            
            return {
                "success": True,
                "data": script_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting server join script: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting server join script: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class VipServersResource(Resource):
    """
    Resource for getting VIP servers for a game
    """
    def get(self, universe_id):
        """
        Get VIP servers for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 25)
            cursor (str, optional): Cursor for pagination
            
        Returns:
            dict: VIP servers or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 25)
        cursor = request.args.get('cursor', None)
        
        try:
            servers_data = get_vip_servers(universe_id, limit, cursor)
            
            return {
                "success": True,
                "data": servers_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting VIP servers: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting VIP servers: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class CreateVipServerResource(Resource):
    """
    Resource for creating a VIP server
    """
    def post(self, universe_id):
        """
        Create a VIP server
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Request Body:
            {
                "name": "Server name",
                "price": 100
            }
            
        Returns:
            dict: Created VIP server or error response
        """
        data = request.get_json()
        
        if not data:
            return {
                "success": False,
                "message": "Missing request body"
            }, 400
        
        required_fields = ['name']
        for field in required_fields:
            if field not in data:
                return {
                    "success": False,
                    "message": f"Missing required parameter: {field}"
                }, 400
        
        name = data['name']
        price = data.get('price', None)
        
        try:
            server_data = create_vip_server(universe_id, name, price)
            
            return {
                "success": True,
                "data": server_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error creating VIP server: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error creating VIP server: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UpdateVipServerResource(Resource):
    """
    Resource for updating a VIP server
    """
    def patch(self, server_id):
        """
        Update a VIP server
        
        Args:
            server_id (str): The Roblox VIP server ID
            
        Request Body:
            {
                "name": "New server name",
                "active": true,
                "joinCode": "ABC123"
            }
            
        Returns:
            dict: Updated VIP server or error response
        """
        data = request.get_json()
        
        if not data:
            return {
                "success": False,
                "message": "Missing request body"
            }, 400
        
        try:
            server_data = update_vip_server(server_id, data)
            
            return {
                "success": True,
                "data": server_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error updating VIP server: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error updating VIP server: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class VipServerSubscribersResource(Resource):
    """
    Resource for getting subscribers to a VIP server
    """
    def get(self, server_id):
        """
        Get subscribers to a VIP server
        
        Args:
            server_id (str): The Roblox VIP server ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 25)
            cursor (str, optional): Cursor for pagination
            
        Returns:
            dict: VIP server subscribers or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 25)
        cursor = request.args.get('cursor', None)
        
        try:
            subscribers_data = get_vip_server_subscribers(server_id, limit, cursor)
            
            return {
                "success": True,
                "data": subscribers_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting VIP server subscribers: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting VIP server subscribers: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class PrivateServersResource(Resource):
    """
    Resource for getting private servers for a user
    """
    def get(self, user_id):
        """
        Get private servers for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 25)
            cursor (str, optional): Cursor for pagination
            
        Returns:
            dict: Private servers or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 25)
        cursor = request.args.get('cursor', None)
        
        try:
            servers_data = get_private_servers(user_id, limit, cursor)
            
            return {
                "success": True,
                "data": servers_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting private servers: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting private servers: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500