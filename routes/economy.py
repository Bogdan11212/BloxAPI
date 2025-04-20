from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api import (
    get_asset_resellers,
    get_asset_resale_data,
    get_currency_exchange_rate,
    get_group_revenue,
    get_user_transactions
)
from utils.roblox_api import RobloxAPIError

logger = logging.getLogger(__name__)

class AssetResellersResource(Resource):
    """
    Resource for getting resellers of a limited asset
    """
    def get(self, asset_id):
        """
        Get resellers of a limited asset
        
        Args:
            asset_id (int): The Roblox asset ID
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 10)
            
        Returns:
            dict: Asset resellers or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 10)
        
        try:
            resellers_data = get_asset_resellers(asset_id, limit)
            return {
                "success": True,
                "data": resellers_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting asset resellers: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting asset resellers: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class AssetResaleDataResource(Resource):
    """
    Resource for getting resale data for a limited asset
    """
    def get(self, asset_id):
        """
        Get resale data for a limited asset
        
        Args:
            asset_id (int): The Roblox asset ID
            
        Returns:
            dict: Asset resale data or error response
        """
        try:
            resale_data = get_asset_resale_data(asset_id)
            return {
                "success": True,
                "data": resale_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting asset resale data: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting asset resale data: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class CurrencyExchangeRateResource(Resource):
    """
    Resource for getting the currency exchange rate for Robux to USD
    """
    def get(self):
        """
        Get the currency exchange rate for Robux to USD
        
        Returns:
            dict: Currency exchange rate or error response
        """
        try:
            exchange_rate = get_currency_exchange_rate()
            return {
                "success": True,
                "data": exchange_rate
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting currency exchange rate: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting currency exchange rate: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class GroupRevenueResource(Resource):
    """
    Resource for getting a group's revenue summary
    """
    def get(self, group_id):
        """
        Get a group's revenue summary
        
        Args:
            group_id (int): The Roblox group ID
            
        Returns:
            dict: Group revenue summary or error response
        """
        try:
            revenue_data = get_group_revenue(group_id)
            return {
                "success": True,
                "data": revenue_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting group revenue: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting group revenue: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class UserTransactionsResource(Resource):
    """
    Resource for getting a user's transactions
    """
    def get(self, user_id, transaction_type):
        """
        Get a user's transactions of a specific type
        
        Args:
            user_id (int): The Roblox user ID
            transaction_type (str): The type of transaction (e.g., "purchases", "sales", "income", "premium")
            
        Query Parameters:
            limit (int, optional): Maximum number of results (default: 100)
            
        Returns:
            dict: User's transactions or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        limit = args.get('limit', 100)
        
        try:
            transactions_data = get_user_transactions(user_id, transaction_type, limit)
            return {
                "success": True,
                "data": transactions_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting user transactions: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting user transactions: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500