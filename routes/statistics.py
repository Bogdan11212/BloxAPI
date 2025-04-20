from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema, DateRangeSchema
from utils.roblox_api_extra import (
    get_game_universe_stats,
    get_game_version_history_stats,
    get_game_playtime_stats,
    get_game_retention_stats,
    get_game_performance_stats,
    get_game_device_stats,
    get_game_demographic_stats,
    get_game_geographic_stats,
    get_game_conversion_stats,
    get_player_activity_stats,
    get_trending_games,
    get_comparison_stats,
    RobloxAPIError
)

logger = logging.getLogger(__name__)

class GameUniverseStatsResource(Resource):
    """
    Resource for getting universe statistics for a game
    """
    def get(self, universe_id):
        """
        Get universe statistics for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_date (str, required): Start date for stats (format: "YYYY-MM-DD")
            end_date (str, required): End date for stats (format: "YYYY-MM-DD")
            
        Returns:
            dict: Game universe statistics or error response
        """
        schema = DateRangeSchema()
        
        try:
            args = schema.load(request.args)
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 400
        
        start_date = args['start_date']
        end_date = args['end_date']
        
        try:
            stats_data = get_game_universe_stats(universe_id, start_date, end_date)
            
            return {
                "success": True,
                "data": stats_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game universe stats: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game universe stats: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GameVersionHistoryStatsResource(Resource):
    """
    Resource for getting version history statistics for a game
    """
    def get(self, universe_id):
        """
        Get version history statistics for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            
        Returns:
            dict: Game version history statistics or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        
        try:
            stats_data = get_game_version_history_stats(universe_id, limit)
            
            return {
                "success": True,
                "data": stats_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game version history stats: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game version history stats: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GamePlaytimeStatsResource(Resource):
    """
    Resource for getting playtime statistics for a game
    """
    def get(self, universe_id):
        """
        Get playtime statistics for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_date (str, required): Start date for stats (format: "YYYY-MM-DD")
            end_date (str, required): End date for stats (format: "YYYY-MM-DD")
            
        Returns:
            dict: Game playtime statistics or error response
        """
        schema = DateRangeSchema()
        
        try:
            args = schema.load(request.args)
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 400
        
        start_date = args['start_date']
        end_date = args['end_date']
        
        try:
            stats_data = get_game_playtime_stats(universe_id, start_date, end_date)
            
            return {
                "success": True,
                "data": stats_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game playtime stats: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game playtime stats: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GameRetentionStatsResource(Resource):
    """
    Resource for getting retention statistics for a game
    """
    def get(self, universe_id):
        """
        Get retention statistics for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_date (str, required): Start date for stats (format: "YYYY-MM-DD")
            end_date (str, required): End date for stats (format: "YYYY-MM-DD")
            
        Returns:
            dict: Game retention statistics or error response
        """
        schema = DateRangeSchema()
        
        try:
            args = schema.load(request.args)
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 400
        
        start_date = args['start_date']
        end_date = args['end_date']
        
        try:
            stats_data = get_game_retention_stats(universe_id, start_date, end_date)
            
            return {
                "success": True,
                "data": stats_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game retention stats: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game retention stats: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GamePerformanceStatsResource(Resource):
    """
    Resource for getting performance statistics for a game
    """
    def get(self, universe_id):
        """
        Get performance statistics for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_date (str, required): Start date for stats (format: "YYYY-MM-DD")
            end_date (str, required): End date for stats (format: "YYYY-MM-DD")
            
        Returns:
            dict: Game performance statistics or error response
        """
        schema = DateRangeSchema()
        
        try:
            args = schema.load(request.args)
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 400
        
        start_date = args['start_date']
        end_date = args['end_date']
        
        try:
            stats_data = get_game_performance_stats(universe_id, start_date, end_date)
            
            return {
                "success": True,
                "data": stats_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game performance stats: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game performance stats: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GameDeviceStatsResource(Resource):
    """
    Resource for getting device statistics for a game
    """
    def get(self, universe_id):
        """
        Get device statistics for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_date (str, required): Start date for stats (format: "YYYY-MM-DD")
            end_date (str, required): End date for stats (format: "YYYY-MM-DD")
            
        Returns:
            dict: Game device statistics or error response
        """
        schema = DateRangeSchema()
        
        try:
            args = schema.load(request.args)
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 400
        
        start_date = args['start_date']
        end_date = args['end_date']
        
        try:
            stats_data = get_game_device_stats(universe_id, start_date, end_date)
            
            return {
                "success": True,
                "data": stats_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game device stats: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game device stats: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GameDemographicStatsResource(Resource):
    """
    Resource for getting demographic statistics for a game
    """
    def get(self, universe_id):
        """
        Get demographic statistics for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_date (str, required): Start date for stats (format: "YYYY-MM-DD")
            end_date (str, required): End date for stats (format: "YYYY-MM-DD")
            
        Returns:
            dict: Game demographic statistics or error response
        """
        schema = DateRangeSchema()
        
        try:
            args = schema.load(request.args)
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 400
        
        start_date = args['start_date']
        end_date = args['end_date']
        
        try:
            stats_data = get_game_demographic_stats(universe_id, start_date, end_date)
            
            return {
                "success": True,
                "data": stats_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game demographic stats: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game demographic stats: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GameGeographicStatsResource(Resource):
    """
    Resource for getting geographic statistics for a game
    """
    def get(self, universe_id):
        """
        Get geographic statistics for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_date (str, required): Start date for stats (format: "YYYY-MM-DD")
            end_date (str, required): End date for stats (format: "YYYY-MM-DD")
            
        Returns:
            dict: Game geographic statistics or error response
        """
        schema = DateRangeSchema()
        
        try:
            args = schema.load(request.args)
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 400
        
        start_date = args['start_date']
        end_date = args['end_date']
        
        try:
            stats_data = get_game_geographic_stats(universe_id, start_date, end_date)
            
            return {
                "success": True,
                "data": stats_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game geographic stats: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game geographic stats: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GameConversionStatsResource(Resource):
    """
    Resource for getting conversion statistics for a game
    """
    def get(self, universe_id):
        """
        Get conversion statistics for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_date (str, required): Start date for stats (format: "YYYY-MM-DD")
            end_date (str, required): End date for stats (format: "YYYY-MM-DD")
            
        Returns:
            dict: Game conversion statistics or error response
        """
        schema = DateRangeSchema()
        
        try:
            args = schema.load(request.args)
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 400
        
        start_date = args['start_date']
        end_date = args['end_date']
        
        try:
            stats_data = get_game_conversion_stats(universe_id, start_date, end_date)
            
            return {
                "success": True,
                "data": stats_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game conversion stats: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game conversion stats: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class PlayerActivityStatsResource(Resource):
    """
    Resource for getting activity statistics for a player
    """
    def get(self, user_id):
        """
        Get activity statistics for a player
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            start_date (str, required): Start date for stats (format: "YYYY-MM-DD")
            end_date (str, required): End date for stats (format: "YYYY-MM-DD")
            
        Returns:
            dict: Player activity statistics or error response
        """
        schema = DateRangeSchema()
        
        try:
            args = schema.load(request.args)
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 400
        
        start_date = args['start_date']
        end_date = args['end_date']
        
        try:
            stats_data = get_player_activity_stats(user_id, start_date, end_date)
            
            return {
                "success": True,
                "data": stats_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting player activity stats: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting player activity stats: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class TrendingGamesResource(Resource):
    """
    Resource for getting trending games
    """
    def get(self):
        """
        Get trending games
        
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            genre (str, optional): Genre filter
            age_group (str, optional): Age group filter
            time_frame (str, optional): Time frame for trending data (default: "day", options: "day", "week", "month")
            
        Returns:
            dict: Trending games or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        genre = request.args.get('genre', None)
        age_group = request.args.get('age_group', None)
        time_frame = request.args.get('time_frame', 'day')
        
        try:
            trending_data = get_trending_games(limit, genre, age_group, time_frame)
            
            return {
                "success": True,
                "data": trending_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting trending games: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting trending games: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GameComparisonStatsResource(Resource):
    """
    Resource for getting comparison statistics for games
    """
    def get(self):
        """
        Get comparison statistics for games
        
        Query Parameters:
            universe_ids (str, required): Comma-separated list of universe IDs to compare
            metric (str, required): Metric to compare (e.g., "visits", "revenue", "playtime", etc.)
            start_date (str, required): Start date for stats (format: "YYYY-MM-DD")
            end_date (str, required): End date for stats (format: "YYYY-MM-DD")
            
        Returns:
            dict: Game comparison statistics or error response
        """
        schema = DateRangeSchema()
        
        try:
            args = schema.load(request.args)
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }, 400
        
        start_date = args['start_date']
        end_date = args['end_date']
        
        universe_ids_str = request.args.get('universe_ids', None)
        metric = request.args.get('metric', None)
        
        if not universe_ids_str:
            return {
                "success": False,
                "message": "Missing required parameter: universe_ids"
            }, 400
        
        if not metric:
            return {
                "success": False,
                "message": "Missing required parameter: metric"
            }, 400
        
        try:
            universe_ids = [int(id.strip()) for id in universe_ids_str.split(',')]
            
            stats_data = get_comparison_stats(universe_ids, metric, start_date, end_date)
            
            return {
                "success": True,
                "data": stats_data
            }
        except ValueError:
            return {
                "success": False,
                "message": "Invalid universe_ids format. Expected comma-separated list of integers"
            }, 400
        except RobloxAPIError as e:
            logger.error(f"Error getting game comparison stats: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game comparison stats: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500