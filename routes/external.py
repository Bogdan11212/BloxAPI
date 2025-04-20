from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
import logging
from utils.validators import PaginationSchema
from utils.external_apis import (
    # Rolimon's functions
    get_item_details, get_item_values, get_item_price_history,
    get_deals, get_player_rap, get_player_value, get_player_inventory_value,
    RolimonAPIError,
    
    # Rblx.Trade functions
    get_trade_ads, get_player_trade_reputation, get_trade_value_calculator,
    RblxTradeAPIError,
    
    # Roliverse functions
    get_player_trading_activity, get_market_trends, get_demand_index,
    RoliverseAPIError,
    
    # Rblx Values functions
    get_item_projected_status, get_item_stability_rating,
    get_items_rising_value, get_items_falling_value,
    RblxValuesAPIError
)

logger = logging.getLogger(__name__)

# =================== Rolimon's API Routes ===================

class RolimonItemDetailsResource(Resource):
    """
    Resource for getting item details from Rolimon's
    """
    def get(self, item_id):
        """
        Get details about an item from Rolimon's
        
        Args:
            item_id (int): The Roblox item ID
            
        Returns:
            dict: Item details or error response
        """
        try:
            item_data = get_item_details(item_id)
            return {
                "success": True,
                "data": item_data
            }
        except RolimonAPIError as e:
            logger.error(f"Error getting item details from Rolimon's: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RolimonItemDetailsResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RolimonItemValuesResource(Resource):
    """
    Resource for getting values for multiple items from Rolimon's
    """
    def post(self):
        """
        Get values for multiple items from Rolimon's
        
        JSON Body:
            item_ids (list): List of Roblox item IDs
            
        Returns:
            dict: Item values or error response
        """
        try:
            data = request.get_json()
            if not data or 'item_ids' not in data:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required field: item_ids"
                    }
                }, 400
                
            item_ids = data['item_ids']
            if not isinstance(item_ids, list) or not all(isinstance(id, int) for id in item_ids):
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "item_ids must be a list of integers"
                    }
                }, 400
                
            values_data = get_item_values(item_ids)
            return {
                "success": True,
                "data": values_data
            }
        except RolimonAPIError as e:
            logger.error(f"Error getting item values from Rolimon's: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RolimonItemValuesResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RolimonItemPriceHistoryResource(Resource):
    """
    Resource for getting price history for an item from Rolimon's
    """
    def get(self, item_id):
        """
        Get price history for an item from Rolimon's
        
        Args:
            item_id (int): The Roblox item ID
            
        Query Parameters:
            period (str, optional): Time period for price history (e.g., "day", "week", "month", "year")
            
        Returns:
            dict: Item price history or error response
        """
        try:
            period = request.args.get('period')
            history_data = get_item_price_history(item_id, period)
            return {
                "success": True,
                "data": history_data
            }
        except RolimonAPIError as e:
            logger.error(f"Error getting item price history from Rolimon's: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RolimonItemPriceHistoryResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RolimonDealsResource(Resource):
    """
    Resource for getting current deals from Rolimon's
    """
    def get(self):
        """
        Get current deals from Rolimon's
        
        Query Parameters:
            deal_type (str, required): Type of deals (e.g., "rap", "demand", "value")
            limit (int, optional): Maximum number of results (default: 10)
            
        Returns:
            dict: Deals or error response
        """
        try:
            deal_type = request.args.get('deal_type')
            if not deal_type:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameter: deal_type"
                    }
                }, 400
                
            try:
                limit = int(request.args.get('limit', 10))
            except ValueError:
                limit = 10
                
            deals_data = get_deals(deal_type, limit)
            return {
                "success": True,
                "data": deals_data
            }
        except RolimonAPIError as e:
            logger.error(f"Error getting deals from Rolimon's: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RolimonDealsResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RolimonPlayerRapResource(Resource):
    """
    Resource for getting a player's RAP from Rolimon's
    """
    def get(self, user_id):
        """
        Get a player's RAP (Recent Average Price) from Rolimon's
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: Player RAP or error response
        """
        try:
            rap_data = get_player_rap(user_id)
            return {
                "success": True,
                "data": rap_data
            }
        except RolimonAPIError as e:
            logger.error(f"Error getting player RAP from Rolimon's: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RolimonPlayerRapResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RolimonPlayerValueResource(Resource):
    """
    Resource for getting a player's value from Rolimon's
    """
    def get(self, user_id):
        """
        Get a player's value from Rolimon's
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: Player value or error response
        """
        try:
            value_data = get_player_value(user_id)
            return {
                "success": True,
                "data": value_data
            }
        except RolimonAPIError as e:
            logger.error(f"Error getting player value from Rolimon's: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RolimonPlayerValueResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RolimonPlayerInventoryValueResource(Resource):
    """
    Resource for getting a player's inventory value from Rolimon's
    """
    def get(self, user_id):
        """
        Get a player's inventory value from Rolimon's
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: Player inventory value or error response
        """
        try:
            inventory_value_data = get_player_inventory_value(user_id)
            return {
                "success": True,
                "data": inventory_value_data
            }
        except RolimonAPIError as e:
            logger.error(f"Error getting player inventory value from Rolimon's: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RolimonPlayerInventoryValueResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

# =================== Rblx.Trade API Routes ===================

class RblxTradeAdsResource(Resource):
    """
    Resource for getting current trade advertisements from Rblx.Trade
    """
    def get(self):
        """
        Get current trade advertisements from Rblx.Trade
        
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            cursor (str, optional): Pagination cursor
            
        Returns:
            dict: Trade advertisements or error response
        """
        try:
            schema = PaginationSchema()
            params = schema.load(request.args)
            
            trade_ads_data = get_trade_ads(params.get('limit', 50), params.get('cursor'))
            return {
                "success": True,
                "data": trade_ads_data
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
        except RblxTradeAPIError as e:
            logger.error(f"Error getting trade ads from Rblx.Trade: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RblxTradeAdsResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RblxTradePlayerReputationResource(Resource):
    """
    Resource for getting a player's trade reputation from Rblx.Trade
    """
    def get(self, user_id):
        """
        Get a player's trade reputation from Rblx.Trade
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: Player trade reputation or error response
        """
        try:
            reputation_data = get_player_trade_reputation(user_id)
            return {
                "success": True,
                "data": reputation_data
            }
        except RblxTradeAPIError as e:
            logger.error(f"Error getting player trade reputation from Rblx.Trade: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RblxTradePlayerReputationResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RblxTradeValueCalculatorResource(Resource):
    """
    Resource for calculating trade values using Rblx.Trade
    """
    def post(self):
        """
        Calculate trade value using Rblx.Trade
        
        JSON Body:
            offer_items (list): List of item IDs being offered
            request_items (list): List of item IDs being requested
            
        Returns:
            dict: Trade value calculation or error response
        """
        try:
            data = request.get_json()
            if not data or 'offer_items' not in data or 'request_items' not in data:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required fields: offer_items and request_items"
                    }
                }, 400
                
            offer_items = data['offer_items']
            request_items = data['request_items']
            
            if not isinstance(offer_items, list) or not isinstance(request_items, list):
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "offer_items and request_items must be lists"
                    }
                }, 400
                
            calculation_data = get_trade_value_calculator(offer_items, request_items)
            return {
                "success": True,
                "data": calculation_data
            }
        except RblxTradeAPIError as e:
            logger.error(f"Error calculating trade value with Rblx.Trade: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RblxTradeValueCalculatorResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

# =================== Roliverse API Routes ===================

class RoliversePlayerTradingActivityResource(Resource):
    """
    Resource for getting a player's trading activity from Roliverse
    """
    def get(self, user_id):
        """
        Get a player's trading activity from Roliverse
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 20)
            
        Returns:
            dict: Player trading activity or error response
        """
        try:
            try:
                limit = int(request.args.get('limit', 20))
            except ValueError:
                limit = 20
                
            activity_data = get_player_trading_activity(user_id, limit)
            return {
                "success": True,
                "data": activity_data
            }
        except RoliverseAPIError as e:
            logger.error(f"Error getting player trading activity from Roliverse: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RoliversePlayerTradingActivityResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RoliverseMarketTrendsResource(Resource):
    """
    Resource for getting market trends from Roliverse
    """
    def get(self):
        """
        Get market trends from Roliverse
        
        Query Parameters:
            item_type (str, optional): Type of items (e.g., "limited", "ugc", "all"). Default: "limited"
            time_period (str, optional): Time period (e.g., "day", "week", "month", "year"). Default: "week"
            
        Returns:
            dict: Market trends or error response
        """
        try:
            item_type = request.args.get('item_type', 'limited')
            time_period = request.args.get('time_period', 'week')
            
            trends_data = get_market_trends(item_type, time_period)
            return {
                "success": True,
                "data": trends_data
            }
        except RoliverseAPIError as e:
            logger.error(f"Error getting market trends from Roliverse: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RoliverseMarketTrendsResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RoliverseDemandIndexResource(Resource):
    """
    Resource for getting demand index for an item from Roliverse
    """
    def get(self, item_id):
        """
        Get demand index for an item from Roliverse
        
        Args:
            item_id (int): The Roblox item ID
            
        Returns:
            dict: Item demand index or error response
        """
        try:
            demand_data = get_demand_index(item_id)
            return {
                "success": True,
                "data": demand_data
            }
        except RoliverseAPIError as e:
            logger.error(f"Error getting demand index from Roliverse: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RoliverseDemandIndexResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

# =================== Rblx Values API Routes ===================

class RblxValuesItemProjectedStatusResource(Resource):
    """
    Resource for getting projected status for an item from Rblx Values
    """
    def get(self, item_id):
        """
        Get projected status for an item from Rblx Values
        
        Args:
            item_id (int): The Roblox item ID
            
        Returns:
            dict: Item projected status or error response
        """
        try:
            projected_data = get_item_projected_status(item_id)
            return {
                "success": True,
                "data": projected_data
            }
        except RblxValuesAPIError as e:
            logger.error(f"Error getting item projected status from Rblx Values: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RblxValuesItemProjectedStatusResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RblxValuesItemStabilityResource(Resource):
    """
    Resource for getting stability rating for an item from Rblx Values
    """
    def get(self, item_id):
        """
        Get stability rating for an item from Rblx Values
        
        Args:
            item_id (int): The Roblox item ID
            
        Returns:
            dict: Item stability rating or error response
        """
        try:
            stability_data = get_item_stability_rating(item_id)
            return {
                "success": True,
                "data": stability_data
            }
        except RblxValuesAPIError as e:
            logger.error(f"Error getting item stability rating from Rblx Values: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RblxValuesItemStabilityResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RblxValuesRisingItemsResource(Resource):
    """
    Resource for getting items with rising values from Rblx Values
    """
    def get(self):
        """
        Get items with rising values from Rblx Values
        
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 20)
            
        Returns:
            dict: Rising items or error response
        """
        try:
            try:
                limit = int(request.args.get('limit', 20))
            except ValueError:
                limit = 20
                
            rising_data = get_items_rising_value(limit)
            return {
                "success": True,
                "data": rising_data
            }
        except RblxValuesAPIError as e:
            logger.error(f"Error getting rising items from Rblx Values: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RblxValuesRisingItemsResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class RblxValuesFallingItemsResource(Resource):
    """
    Resource for getting items with falling values from Rblx Values
    """
    def get(self):
        """
        Get items with falling values from Rblx Values
        
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 20)
            
        Returns:
            dict: Falling items or error response
        """
        try:
            try:
                limit = int(request.args.get('limit', 20))
            except ValueError:
                limit = 20
                
            falling_data = get_items_falling_value(limit)
            return {
                "success": True,
                "data": falling_data
            }
        except RblxValuesAPIError as e:
            logger.error(f"Error getting falling items from Rblx Values: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in RblxValuesFallingItemsResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500