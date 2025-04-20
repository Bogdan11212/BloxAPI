from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
import logging
from utils.validators import CatalogSearchSchema
from utils.roblox_api import (
    search_catalog, get_catalog_categories,
    RobloxAPIError
)

logger = logging.getLogger(__name__)

class CatalogResource(Resource):
    """
    Resource for getting catalog information on Roblox
    """
    def get(self):
        """
        Get catalog categories
        
        Returns:
            dict: Catalog categories or error response
        """
        try:
            categories_data = get_catalog_categories()
            
            return {
                "success": True,
                "data": categories_data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting catalog categories: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in CatalogResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500

class CatalogSearchResource(Resource):
    """
    Resource for searching the Roblox catalog
    """
    def get(self):
        """
        Search for items in the catalog
        
        Query Parameters:
            keyword (str): Search term
            category (str, optional): Item category
            subcategory (str, optional): Item subcategory
            sort_type (str, optional): Sort order
            min_price (int, optional): Minimum price
            max_price (int, optional): Maximum price
            limit (int, optional): Maximum number of results (default: 10)
            cursor (str, optional): Pagination cursor
            
        Returns:
            dict: Search results or error response
        """
        try:
            # Validate query parameters
            schema = CatalogSearchSchema()
            params = schema.load(request.args)
            
            # Search the catalog
            search_results = search_catalog(
                keyword=params["keyword"],
                category=params.get("category"),
                subcategory=params.get("subcategory"),
                limit=params.get("limit", 10)
            )
            
            return {
                "success": True,
                "data": search_results
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
        except RobloxAPIError as e:
            logger.error(f"Error searching catalog: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": e.status_code,
                    "message": e.message
                }
            }, e.status_code
        except Exception as e:
            logger.exception("Unexpected error in CatalogSearchResource")
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": f"Internal server error: {str(e)}"
                }
            }, 500
