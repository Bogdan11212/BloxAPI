from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api import (
    get_game_analytics,
    get_game_playtime,
    get_game_revenue
)
from utils.roblox_api import RobloxAPIError

logger = logging.getLogger(__name__)

class GameAnalyticsResource(Resource):
    """
    Resource for getting analytics for a game
    """
    def get(self, universe_id, metric_type):
        """
        Get analytics for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            metric_type (str): The type of metric (e.g., "visits", "revenue", "concurrent", etc.)
            
        Query Parameters:
            time_frame (str, optional): Time frame for analytics (e.g., "past1day", "past7days", "past30days")
            
        Returns:
            dict: Game analytics or error response
        """
        time_frame = request.args.get('time_frame', 'past7days')
        
        try:
            analytics_data = get_game_analytics(universe_id, metric_type, time_frame)
            return {
                "success": True,
                "data": analytics_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game analytics: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game analytics: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GamePlaytimeResource(Resource):
    """
    Resource for getting playtime analytics for a game
    """
    def get(self, universe_id):
        """
        Get playtime analytics for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_time (str, required): Start time for analytics (format: "YYYY-MM-DD")
            end_time (str, required): End time for analytics (format: "YYYY-MM-DD")
            
        Returns:
            dict: Game playtime analytics or error response
        """
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        
        if not start_time or not end_time:
            return {
                "success": False,
                "message": "Both start_time and end_time are required query parameters"
            }, 400
        
        try:
            playtime_data = get_game_playtime(universe_id, start_time, end_time)
            return {
                "success": True,
                "data": playtime_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game playtime: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game playtime: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GameRevenueAnalyticsResource(Resource):
    """
    Resource for getting revenue analytics for a game
    """
    def get(self, universe_id):
        """
        Get revenue analytics for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_time (str, required): Start time for analytics (format: "YYYY-MM-DD")
            end_time (str, required): End time for analytics (format: "YYYY-MM-DD")
            
        Returns:
            dict: Game revenue analytics or error response
        """
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        
        if not start_time or not end_time:
            return {
                "success": False,
                "message": "Both start_time and end_time are required query parameters"
            }, 400
        
        try:
            revenue_data = get_game_revenue(universe_id, start_time, end_time)
            return {
                "success": True,
                "data": revenue_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game revenue: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game revenue: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500