from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api_extra import RobloxAPIError

logger = logging.getLogger(__name__)

class MarketplaceItemsResource(Resource):
    """
    Resource for getting marketplace items
    """
    def get(self):
        """
        Get marketplace items
        
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            category (str, optional): Filter by category
            subcategory (str, optional): Filter by subcategory
            
        Returns:
            dict: Marketplace items or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('max_rows', 25)
        category = request.args.get('category', None)
        subcategory = request.args.get('subcategory', None)
        
        try:
            # Demo data
            items = [
                {
                    "id": 1234567,
                    "name": "Golden Crown",
                    "description": "A shiny golden crown for your avatar",
                    "type": "Hat",
                    "price": 100,
                    "creator": {
                        "id": 8765432,
                        "name": "ItemCreator123",
                        "type": "User"
                    },
                    "created": "2023-06-15T00:00:00Z",
                    "updated": "2023-06-15T00:00:00Z",
                    "sales": 4567,
                    "isLimited": False,
                    "isForSale": True
                },
                {
                    "id": 2345678,
                    "name": "Fire Sword",
                    "description": "A legendary sword engulfed in flames",
                    "type": "Gear",
                    "price": 250,
                    "creator": {
                        "id": 9876543,
                        "name": "WeaponForge",
                        "type": "Group"
                    },
                    "created": "2023-05-20T00:00:00Z",
                    "updated": "2023-05-25T00:00:00Z",
                    "sales": 2345,
                    "isLimited": True,
                    "isForSale": True
                },
                {
                    "id": 3456789,
                    "name": "Blue Mohawk",
                    "description": "Show off your style with this blue mohawk",
                    "type": "Hair",
                    "price": 50,
                    "creator": {
                        "id": 8765432,
                        "name": "ItemCreator123",
                        "type": "User"
                    },
                    "created": "2023-07-10T00:00:00Z",
                    "updated": "2023-07-10T00:00:00Z",
                    "sales": 8765,
                    "isLimited": False,
                    "isForSale": True
                }
            ]
            
            # Apply category filters if provided
            if category:
                items = [item for item in items if item["type"].lower() == category.lower()]
            
            # More filtering could be applied here for subcategory
            
            return {
                "success": True,
                "data": items[:max_rows]
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting marketplace items: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting marketplace items: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class MarketplaceItemDetailsResource(Resource):
    """
    Resource for getting marketplace item details
    """
    def get(self, item_id):
        """
        Get details for a marketplace item
        
        Args:
            item_id (int): The marketplace item ID
            
        Returns:
            dict: Item details or error response
        """
        try:
            # Demo data
            data = {
                "id": item_id,
                "name": "Golden Crown",
                "description": "A shiny golden crown for your avatar",
                "type": "Hat",
                "price": 100,
                "creator": {
                    "id": 8765432,
                    "name": "ItemCreator123",
                    "type": "User"
                },
                "created": "2023-06-15T00:00:00Z",
                "updated": "2023-06-15T00:00:00Z",
                "sales": 4567,
                "favorites": 2345,
                "isLimited": False,
                "isForSale": True,
                "isNew": False,
                "isSeasonal": False,
                "isOnSale": True,
                "genres": ["Fantasy", "Royal"],
                "assetType": "Hat",
                "priceInRobux": 100,
                "priceInTickets": None,
                "thumbnail": "https://example.com/thumbnails/items/golden-crown.png",
                "purchaseCount": 4567,
                "favoriteCount": 2345,
                "offSaleDeadline": None
            }
            
            return {
                "success": True,
                "data": data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting marketplace item details: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting marketplace item details: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class MarketplaceSimilarItemsResource(Resource):
    """
    Resource for getting similar marketplace items
    """
    def get(self, item_id):
        """
        Get similar items to a marketplace item
        
        Args:
            item_id (int): The marketplace item ID
            
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            
        Returns:
            dict: Similar items or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('max_rows', 25)
        
        try:
            # Demo data
            items = [
                {
                    "id": 1234567,
                    "name": "Silver Crown",
                    "description": "A shiny silver crown for your avatar",
                    "type": "Hat",
                    "price": 80,
                    "creator": {
                        "id": 8765432,
                        "name": "ItemCreator123",
                        "type": "User"
                    },
                    "created": "2023-05-10T00:00:00Z",
                    "sales": 3456,
                    "isLimited": False,
                    "isForSale": True,
                    "similarity": 0.95
                },
                {
                    "id": 2345678,
                    "name": "Royal Crown",
                    "description": "A majestic crown fit for royalty",
                    "type": "Hat",
                    "price": 150,
                    "creator": {
                        "id": 7654321,
                        "name": "RoyalDesigns",
                        "type": "Group"
                    },
                    "created": "2023-04-20T00:00:00Z",
                    "sales": 5678,
                    "isLimited": False,
                    "isForSale": True,
                    "similarity": 0.85
                },
                {
                    "id": 3456789,
                    "name": "Diamond Tiara",
                    "description": "A sparkling diamond tiara",
                    "type": "Hat",
                    "price": 200,
                    "creator": {
                        "id": 8765432,
                        "name": "ItemCreator123",
                        "type": "User"
                    },
                    "created": "2023-03-15T00:00:00Z",
                    "sales": 2345,
                    "isLimited": True,
                    "isForSale": True,
                    "similarity": 0.75
                }
            ]
            
            return {
                "success": True,
                "data": items[:max_rows]
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting similar marketplace items: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting similar marketplace items: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class MarketplaceItemCommentsResource(Resource):
    """
    Resource for getting comments on a marketplace item
    """
    def get(self, item_id):
        """
        Get comments for a marketplace item
        
        Args:
            item_id (int): The marketplace item ID
            
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            
        Returns:
            dict: Item comments or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('max_rows', 25)
        
        try:
            # Demo data
            comments = [
                {
                    "id": 12345,
                    "user": {
                        "id": 9876543,
                        "name": "CommentUser1",
                        "displayName": "Cool Guy",
                        "hasVerifiedBadge": False
                    },
                    "content": "This crown looks amazing with my outfit!",
                    "created": "2023-11-25T14:32:45Z",
                    "updated": None,
                    "likes": 12,
                    "dislikes": 1,
                    "isDeleted": False,
                    "replies": [
                        {
                            "id": 23456,
                            "user": {
                                "id": 8765432,
                                "name": "ItemCreator123",
                                "displayName": "Creator",
                                "hasVerifiedBadge": True
                            },
                            "content": "Thanks for the feedback!",
                            "created": "2023-11-25T15:10:20Z",
                            "updated": None,
                            "likes": 5,
                            "dislikes": 0,
                            "isDeleted": False
                        }
                    ]
                },
                {
                    "id": 34567,
                    "user": {
                        "id": 8765432,
                        "name": "CommentUser2",
                        "displayName": "Fashion Expert",
                        "hasVerifiedBadge": False
                    },
                    "content": "The price is a bit high for what you get",
                    "created": "2023-11-20T09:45:12Z",
                    "updated": None,
                    "likes": 8,
                    "dislikes": 4,
                    "isDeleted": False,
                    "replies": []
                },
                {
                    "id": 45678,
                    "user": {
                        "id": 7654321,
                        "name": "CommentUser3",
                        "displayName": "Collector",
                        "hasVerifiedBadge": False
                    },
                    "content": "I've been waiting for something like this!",
                    "created": "2023-11-18T22:15:40Z",
                    "updated": "2023-11-18T22:20:15Z",
                    "likes": 20,
                    "dislikes": 0,
                    "isDeleted": False,
                    "replies": []
                }
            ]
            
            return {
                "success": True,
                "data": comments[:max_rows]
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting marketplace item comments: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting marketplace item comments: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class MarketplaceItemRecommendationsResource(Resource):
    """
    Resource for getting personalized marketplace item recommendations
    """
    def get(self, user_id):
        """
        Get personalized marketplace item recommendations for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            category (str, optional): Filter by category
            
        Returns:
            dict: Personalized item recommendations or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('max_rows', 25)
        category = request.args.get('category', None)
        
        try:
            # Demo data
            items = [
                {
                    "id": 1234567,
                    "name": "Dragon Wings",
                    "description": "Majestic dragon wings for your avatar",
                    "type": "Back",
                    "price": 300,
                    "creator": {
                        "id": 8765432,
                        "name": "ItemCreator123",
                        "type": "User"
                    },
                    "created": "2023-09-15T00:00:00Z",
                    "sales": 7890,
                    "isLimited": False,
                    "isForSale": True,
                    "recommendationReason": "Based on your recent purchases"
                },
                {
                    "id": 2345678,
                    "name": "Ninja Headband",
                    "description": "Show your ninja skills with this headband",
                    "type": "Hat",
                    "price": 50,
                    "creator": {
                        "id": 7654321,
                        "name": "NinjaItems",
                        "type": "Group"
                    },
                    "created": "2023-10-20T00:00:00Z",
                    "sales": 5678,
                    "isLimited": False,
                    "isForSale": True,
                    "recommendationReason": "Popular in games you play"
                },
                {
                    "id": 3456789,
                    "name": "Pixel Sunglasses",
                    "description": "Retro-style pixel sunglasses",
                    "type": "Face",
                    "price": 75,
                    "creator": {
                        "id": 6543210,
                        "name": "RetroDesigns",
                        "type": "Group"
                    },
                    "created": "2023-11-05T00:00:00Z",
                    "sales": 3456,
                    "isLimited": False,
                    "isForSale": True,
                    "recommendationReason": "Trending item"
                }
            ]
            
            # Apply category filters if provided
            if category:
                items = [item for item in items if item["type"].lower() == category.lower()]
            
            return {
                "success": True,
                "data": items[:max_rows]
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting marketplace item recommendations: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting marketplace item recommendations: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class MarketplaceBundlesResource(Resource):
    """
    Resource for getting marketplace bundles
    """
    def get(self):
        """
        Get marketplace bundles
        
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            bundle_type (str, optional): Filter by bundle type
            
        Returns:
            dict: Marketplace bundles or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('max_rows', 25)
        bundle_type = request.args.get('bundle_type', None)
        
        try:
            # Demo data
            bundles = [
                {
                    "id": 12345,
                    "name": "Ninja Warrior Bundle",
                    "description": "Everything you need to become a ninja warrior",
                    "bundleType": "AvatarItems",
                    "price": 500,
                    "creator": {
                        "id": 7654321,
                        "name": "NinjaItems",
                        "type": "Group"
                    },
                    "created": "2023-09-10T00:00:00Z",
                    "updated": "2023-09-10T00:00:00Z",
                    "items": [
                        {
                            "id": 1111111,
                            "name": "Ninja Sword",
                            "type": "Gear"
                        },
                        {
                            "id": 2222222,
                            "name": "Ninja Headband",
                            "type": "Hat"
                        },
                        {
                            "id": 3333333,
                            "name": "Ninja Outfit",
                            "type": "Shirt"
                        }
                    ],
                    "sales": 2345,
                    "isForSale": True
                },
                {
                    "id": 23456,
                    "name": "Royal Bundle",
                    "description": "Look like royalty with this bundle",
                    "bundleType": "AvatarItems",
                    "price": 800,
                    "creator": {
                        "id": 8765432,
                        "name": "RoyalDesigns",
                        "type": "Group"
                    },
                    "created": "2023-08-15T00:00:00Z",
                    "updated": "2023-08-20T00:00:00Z",
                    "items": [
                        {
                            "id": 4444444,
                            "name": "Royal Crown",
                            "type": "Hat"
                        },
                        {
                            "id": 5555555,
                            "name": "Royal Cape",
                            "type": "Back"
                        },
                        {
                            "id": 6666666,
                            "name": "Royal Outfit",
                            "type": "Shirt"
                        },
                        {
                            "id": 7777777,
                            "name": "Royal Trousers",
                            "type": "Pants"
                        }
                    ],
                    "sales": 1456,
                    "isForSale": True
                },
                {
                    "id": 34567,
                    "name": "Space Explorer Bundle",
                    "description": "Explore the cosmos with this space-themed bundle",
                    "bundleType": "AvatarItems",
                    "price": 650,
                    "creator": {
                        "id": 9876543,
                        "name": "SpaceDesigns",
                        "type": "Group"
                    },
                    "created": "2023-10-25T00:00:00Z",
                    "updated": "2023-10-25T00:00:00Z",
                    "items": [
                        {
                            "id": 8888888,
                            "name": "Space Helmet",
                            "type": "Hat"
                        },
                        {
                            "id": 9999999,
                            "name": "Space Suit",
                            "type": "Shirt"
                        },
                        {
                            "id": 1010101,
                            "name": "Space Pants",
                            "type": "Pants"
                        },
                        {
                            "id": 2020202,
                            "name": "Jetpack",
                            "type": "Back"
                        }
                    ],
                    "sales": 3456,
                    "isForSale": True
                }
            ]
            
            # Apply bundle type filters if provided
            if bundle_type:
                bundles = [bundle for bundle in bundles if bundle["bundleType"].lower() == bundle_type.lower()]
            
            return {
                "success": True,
                "data": bundles[:max_rows]
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting marketplace bundles: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting marketplace bundles: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class MarketplaceBundleDetailsResource(Resource):
    """
    Resource for getting marketplace bundle details
    """
    def get(self, bundle_id):
        """
        Get details for a marketplace bundle
        
        Args:
            bundle_id (int): The marketplace bundle ID
            
        Returns:
            dict: Bundle details or error response
        """
        try:
            # Demo data
            data = {
                "id": bundle_id,
                "name": "Ninja Warrior Bundle",
                "description": "Everything you need to become a ninja warrior",
                "bundleType": "AvatarItems",
                "price": 500,
                "creator": {
                    "id": 7654321,
                    "name": "NinjaItems",
                    "type": "Group"
                },
                "created": "2023-09-10T00:00:00Z",
                "updated": "2023-09-10T00:00:00Z",
                "items": [
                    {
                        "id": 1111111,
                        "name": "Ninja Sword",
                        "type": "Gear",
                        "description": "A sharp ninja sword for combat",
                        "individualPrice": 200
                    },
                    {
                        "id": 2222222,
                        "name": "Ninja Headband",
                        "type": "Hat",
                        "description": "A traditional ninja headband",
                        "individualPrice": 150
                    },
                    {
                        "id": 3333333,
                        "name": "Ninja Outfit",
                        "type": "Shirt",
                        "description": "A stealthy ninja outfit",
                        "individualPrice": 200
                    }
                ],
                "totalIndividualValue": 550,
                "discount": 50,
                "sales": 2345,
                "favorites": 1234,
                "isForSale": True,
                "isNew": False,
                "isSeasonal": False,
                "isOnSale": True,
                "genres": ["Ninja", "Warrior", "Combat"],
                "thumbnail": "https://example.com/thumbnails/bundles/ninja-warrior.png",
                "purchaseCount": 2345,
                "favoriteCount": 1234,
                "offSaleDeadline": None
            }
            
            return {
                "success": True,
                "data": data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting marketplace bundle details: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting marketplace bundle details: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class MarketplaceFeaturedItemsResource(Resource):
    """
    Resource for getting featured marketplace items
    """
    def get(self):
        """
        Get featured marketplace items
        
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            
        Returns:
            dict: Featured marketplace items or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('max_rows', 25)
        
        try:
            # Demo data
            items = [
                {
                    "id": 1234567,
                    "name": "Legendary Dragon Wings",
                    "description": "Legendary dragon wings with animated fire effects",
                    "type": "Back",
                    "price": 500,
                    "creator": {
                        "id": 8765432,
                        "name": "PremiumDesigns",
                        "type": "Group"
                    },
                    "created": "2023-11-10T00:00:00Z",
                    "sales": 5678,
                    "isLimited": False,
                    "isForSale": True,
                    "featuredReason": "New Release",
                    "featuredUntil": "2023-12-10T00:00:00Z"
                },
                {
                    "id": 2345678,
                    "name": "Winter Wonder Bundle",
                    "description": "Complete winter outfit with special effects",
                    "type": "Bundle",
                    "price": 800,
                    "creator": {
                        "id": 9876543,
                        "name": "SeasonalCreations",
                        "type": "Group"
                    },
                    "created": "2023-11-25T00:00:00Z",
                    "sales": 3456,
                    "isLimited": False,
                    "isForSale": True,
                    "featuredReason": "Seasonal Special",
                    "featuredUntil": "2023-12-31T00:00:00Z"
                },
                {
                    "id": 3456789,
                    "name": "Golden Bloxy Award",
                    "description": "Celebrate your achievements with this golden award",
                    "type": "Gear",
                    "price": 350,
                    "creator": {
                        "id": 1234567,
                        "name": "OfficialRoblox",
                        "type": "Group"
                    },
                    "created": "2023-11-15T00:00:00Z",
                    "sales": 7890,
                    "isLimited": True,
                    "isForSale": True,
                    "featuredReason": "Limited Edition",
                    "featuredUntil": "2023-12-15T00:00:00Z"
                }
            ]
            
            return {
                "success": True,
                "data": items[:max_rows]
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting featured marketplace items: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting featured marketplace items: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class MarketplacePriceHistoryResource(Resource):
    """
    Resource for getting price history for a marketplace item
    """
    def get(self, item_id):
        """
        Get price history for a marketplace item
        
        Args:
            item_id (int): The marketplace item ID
            
        Query Parameters:
            days (int, optional): Number of days of history to retrieve (default: 30)
            
        Returns:
            dict: Item price history or error response
        """
        days = request.args.get('days', 30, type=int)
        
        try:
            # Demo data
            data = {
                "itemId": item_id,
                "name": "Legendary Dragon Wings",
                "currentPrice": 500,
                "originalPrice": 600,
                "lowestPrice": 450,
                "highestPrice": 700,
                "pricePoints": [
                    {"date": "2023-11-01", "price": 600},
                    {"date": "2023-11-05", "price": 600},
                    {"date": "2023-11-10", "price": 550},
                    {"date": "2023-11-15", "price": 500},
                    {"date": "2023-11-20", "price": 450},
                    {"date": "2023-11-25", "price": 500},
                    {"date": "2023-11-30", "price": 500}
                ],
                "saleEvents": [
                    {
                        "name": "Black Friday Sale",
                        "startDate": "2023-11-20",
                        "endDate": "2023-11-25",
                        "discountPercentage": 25
                    }
                ]
            }
            
            # Adjust data based on requested days
            if days < 30:
                # Only return the most recent prices
                data["pricePoints"] = data["pricePoints"][-days:]
            
            return {
                "success": True,
                "data": data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting marketplace item price history: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting marketplace item price history: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class MarketplaceSalesResource(Resource):
    """
    Resource for getting sales information for a marketplace item
    """
    def get(self, item_id):
        """
        Get sales information for a marketplace item
        
        Args:
            item_id (int): The marketplace item ID
            
        Returns:
            dict: Item sales information or error response
        """
        try:
            # Demo data
            data = {
                "itemId": item_id,
                "name": "Legendary Dragon Wings",
                "totalSales": 5678,
                "totalRevenue": 2839000,  # In Robux
                "salesByDay": [
                    {"date": "2023-11-24", "count": 123},
                    {"date": "2023-11-25", "count": 145},
                    {"date": "2023-11-26", "count": 132},
                    {"date": "2023-11-27", "count": 120},
                    {"date": "2023-11-28", "count": 115},
                    {"date": "2023-11-29", "count": 130},
                    {"date": "2023-11-30", "count": 125}
                ],
                "salesByPlatform": {
                    "Web": 3124,
                    "Mobile": 1982,
                    "Xbox": 572
                },
                "salesByRegion": {
                    "NorthAmerica": 2678,
                    "Europe": 1456,
                    "Asia": 987,
                    "Other": 557
                },
                "conversionRate": 0.025,  # 2.5% of viewers purchase
                "averageTimeToSale": 3.5  # Days from first view to purchase
            }
            
            return {
                "success": True,
                "data": data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting marketplace item sales information: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting marketplace item sales information: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500