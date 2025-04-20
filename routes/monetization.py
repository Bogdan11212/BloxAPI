from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema, DateRangeSchema
from utils.roblox_api_extra import (
    get_developer_products,
    get_developer_product_details,
    get_game_passes,
    get_game_pass_details,
    get_premium_payouts,
    get_transaction_history,
    get_sales_summary,
    get_revenue_summary,
    get_purchases_by_product,
    check_player_ownership,
    RobloxAPIError
)

logger = logging.getLogger(__name__)

class DeveloperProductsResource(Resource):
    """
    Resource for getting developer products for a game
    """
    def get(self, universe_id):
        """
        Get developer products for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            
        Returns:
            dict: Developer products or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        
        try:
            products_data = get_developer_products(universe_id, limit)
            
            return {
                "success": True,
                "data": products_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting developer products: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting developer products: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class DeveloperProductDetailsResource(Resource):
    """
    Resource for getting details about a specific developer product
    """
    def get(self, product_id):
        """
        Get details about a specific developer product
        
        Args:
            product_id (int): The Roblox developer product ID
            
        Returns:
            dict: Developer product details or error response
        """
        try:
            product_data = get_developer_product_details(product_id)
            
            return {
                "success": True,
                "data": product_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting developer product details: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting developer product details: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GamePassesResource(Resource):
    """
    Resource for getting game passes for a game
    """
    def get(self, universe_id):
        """
        Get game passes for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 50)
            
        Returns:
            dict: Game passes or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 50)
        
        try:
            passes_data = get_game_passes(universe_id, limit)
            
            return {
                "success": True,
                "data": passes_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game passes: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game passes: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GamePassDetailsResource(Resource):
    """
    Resource for getting details about a specific game pass
    """
    def get(self, pass_id):
        """
        Get details about a specific game pass
        
        Args:
            pass_id (int): The Roblox game pass ID
            
        Returns:
            dict: Game pass details or error response
        """
        try:
            pass_data = get_game_pass_details(pass_id)
            
            return {
                "success": True,
                "data": pass_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting game pass details: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting game pass details: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class PremiumPayoutsResource(Resource):
    """
    Resource for getting premium payouts for a game
    """
    def get(self, universe_id):
        """
        Get premium payouts for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_date (str, required): Start date for payouts (format: "YYYY-MM-DD")
            end_date (str, required): End date for payouts (format: "YYYY-MM-DD")
            
        Returns:
            dict: Premium payouts or error response
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
            payouts_data = get_premium_payouts(universe_id, start_date, end_date)
            
            return {
                "success": True,
                "data": payouts_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting premium payouts: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting premium payouts: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class TransactionHistoryResource(Resource):
    """
    Resource for getting transaction history for a game
    """
    def get(self, universe_id):
        """
        Get transaction history for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_date (str, required): Start date for transactions (format: "YYYY-MM-DD")
            end_date (str, required): End date for transactions (format: "YYYY-MM-DD")
            transaction_type (str, optional): Type of transactions to filter by (e.g., "Sale", "DevEx", "GroupPayout")
            limit (int, optional): Maximum number of results (default: 100)
            
        Returns:
            dict: Transaction history or error response
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
        
        pag_schema = PaginationSchema()
        pag_args = pag_schema.load(request.args)
        
        limit = pag_args.get('limit', 100)
        transaction_type = request.args.get('transaction_type', None)
        
        try:
            transactions_data = get_transaction_history(universe_id, start_date, end_date, transaction_type, limit)
            
            return {
                "success": True,
                "data": transactions_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting transaction history: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting transaction history: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class SalesSummaryResource(Resource):
    """
    Resource for getting sales summary for a game
    """
    def get(self, universe_id):
        """
        Get sales summary for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_date (str, required): Start date for sales (format: "YYYY-MM-DD")
            end_date (str, required): End date for sales (format: "YYYY-MM-DD")
            
        Returns:
            dict: Sales summary or error response
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
            summary_data = get_sales_summary(universe_id, start_date, end_date)
            
            return {
                "success": True,
                "data": summary_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting sales summary: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting sales summary: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class RevenueSummaryResource(Resource):
    """
    Resource for getting revenue summary for a game
    """
    def get(self, universe_id):
        """
        Get revenue summary for a game
        
        Args:
            universe_id (int): The Roblox universe ID
            
        Query Parameters:
            start_date (str, required): Start date for revenue (format: "YYYY-MM-DD")
            end_date (str, required): End date for revenue (format: "YYYY-MM-DD")
            
        Returns:
            dict: Revenue summary or error response
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
            summary_data = get_revenue_summary(universe_id, start_date, end_date)
            
            return {
                "success": True,
                "data": summary_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting revenue summary: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting revenue summary: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ProductPurchasesResource(Resource):
    """
    Resource for getting purchases by product
    """
    def get(self, universe_id, product_id):
        """
        Get purchases by product
        
        Args:
            universe_id (int): The Roblox universe ID
            product_id (int): The Roblox product ID
            
        Query Parameters:
            start_date (str, required): Start date for purchases (format: "YYYY-MM-DD")
            end_date (str, required): End date for purchases (format: "YYYY-MM-DD")
            limit (int, optional): Maximum number of results (default: 100)
            
        Returns:
            dict: Product purchases or error response
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
        
        pag_schema = PaginationSchema()
        pag_args = pag_schema.load(request.args)
        
        limit = pag_args.get('limit', 100)
        
        try:
            purchases_data = get_purchases_by_product(universe_id, product_id, start_date, end_date, limit)
            
            return {
                "success": True,
                "data": purchases_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting product purchases: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting product purchases: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class PlayerOwnershipResource(Resource):
    """
    Resource for checking if a player owns a product
    """
    def get(self, user_id, asset_type, asset_id):
        """
        Check if a player owns a product
        
        Args:
            user_id (int): The Roblox user ID
            asset_type (str): The type of asset ('gamepass', 'developerproduct', 'asset')
            asset_id (int): The ID of the asset
            
        Returns:
            dict: Ownership status or error response
        """
        try:
            ownership_data = check_player_ownership(user_id, asset_type, asset_id)
            
            return {
                "success": True,
                "data": ownership_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error checking player ownership: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error checking player ownership: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500