from flask import request
from flask_restful import Resource
import logging
from utils.validators import PaginationSchema
from utils.roblox_api_extra import RobloxAPIError

logger = logging.getLogger(__name__)

class ContentTemplatesResource(Resource):
    """
    Resource for getting content creation templates
    """
    def get(self):
        """
        Get content creation templates
        
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            category (str, optional): Filter by template category
            
        Returns:
            dict: Content creation templates or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('max_rows', 25)
        category = request.args.get('category', None)
        
        try:
            # Demo data
            templates = [
                {
                    "id": "template-12345",
                    "name": "Battle Royale Template",
                    "description": "A fully functional battle royale game template",
                    "category": "Game",
                    "subcategory": "Battle Royale",
                    "creator": {
                        "id": 8765432,
                        "name": "GameTemplates",
                        "type": "Group"
                    },
                    "created": "2023-06-15T00:00:00Z",
                    "updated": "2023-09-10T00:00:00Z",
                    "downloads": 12345,
                    "rating": 4.5,
                    "isPublic": True,
                    "isPremium": False,
                    "thumbnailUrl": "https://example.com/thumbnails/templates/battle-royale.png"
                },
                {
                    "id": "template-23456",
                    "name": "RPG Character Controller",
                    "description": "Character controller for RPG games with inventory and stats",
                    "category": "Script",
                    "subcategory": "Character Controller",
                    "creator": {
                        "id": 9876543,
                        "name": "ScriptMaster",
                        "type": "User"
                    },
                    "created": "2023-07-20T00:00:00Z",
                    "updated": "2023-10-15T00:00:00Z",
                    "downloads": 8765,
                    "rating": 4.8,
                    "isPublic": True,
                    "isPremium": True,
                    "thumbnailUrl": "https://example.com/thumbnails/templates/rpg-character.png"
                },
                {
                    "id": "template-34567",
                    "name": "Modern UI Kit",
                    "description": "A comprehensive UI kit with modern design elements",
                    "category": "UI",
                    "subcategory": "UI Kit",
                    "creator": {
                        "id": 7654321,
                        "name": "UIDesignMasters",
                        "type": "Group"
                    },
                    "created": "2023-08-05T00:00:00Z",
                    "updated": "2023-11-01T00:00:00Z",
                    "downloads": 15432,
                    "rating": 4.7,
                    "isPublic": True,
                    "isPremium": True,
                    "thumbnailUrl": "https://example.com/thumbnails/templates/modern-ui.png"
                }
            ]
            
            # Apply category filters if provided
            if category:
                templates = [template for template in templates if template["category"].lower() == category.lower()]
            
            return {
                "success": True,
                "data": templates[:max_rows]
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting content templates: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting content templates: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ContentTemplateDetailsResource(Resource):
    """
    Resource for getting content template details
    """
    def get(self, template_id):
        """
        Get details for a content template
        
        Args:
            template_id (str): The content template ID
            
        Returns:
            dict: Template details or error response
        """
        try:
            # Demo data
            data = {
                "id": template_id,
                "name": "Battle Royale Template",
                "description": "A fully functional battle royale game template with weapon system, map generation, and match management",
                "longDescription": """
                This battle royale template provides everything you need to create your own battle royale game:
                
                - Fully functional weapon system with 10 different weapons
                - Procedural map generation with customizable settings
                - Match management system with lobby and game flow
                - Player inventory system
                - Health and shield mechanics
                - Zone system with shrinking play area
                - Leaderboard and statistics tracking
                - Customizable game settings
                """,
                "category": "Game",
                "subcategory": "Battle Royale",
                "creator": {
                    "id": 8765432,
                    "name": "GameTemplates",
                    "type": "Group"
                },
                "created": "2023-06-15T00:00:00Z",
                "updated": "2023-09-10T00:00:00Z",
                "version": "2.3.1",
                "downloads": 12345,
                "rating": 4.5,
                "reviewsCount": 578,
                "isPublic": True,
                "isPremium": False,
                "price": 0,
                "thumbnailUrl": "https://example.com/thumbnails/templates/battle-royale.png",
                "screenshotUrls": [
                    "https://example.com/screenshots/templates/battle-royale-1.png",
                    "https://example.com/screenshots/templates/battle-royale-2.png",
                    "https://example.com/screenshots/templates/battle-royale-3.png"
                ],
                "tags": ["Battle Royale", "PvP", "Shooter", "Multiplayer", "Action"],
                "requirements": {
                    "studioVersion": "2.567.0",
                    "plugins": []
                },
                "contents": [
                    {
                        "name": "Weapon System",
                        "type": "Script",
                        "description": "Complete weapon system with 10 weapons"
                    },
                    {
                        "name": "Map Generator",
                        "type": "Script",
                        "description": "Procedural map generation system"
                    },
                    {
                        "name": "Match Manager",
                        "type": "Script",
                        "description": "Handles game flow, lobby, and match states"
                    },
                    {
                        "name": "UI System",
                        "type": "UI",
                        "description": "Complete UI for the game"
                    },
                    {
                        "name": "Asset Pack",
                        "type": "Assets",
                        "description": "3D models and textures for the game"
                    }
                ],
                "license": {
                    "type": "Standard",
                    "allowsModification": True,
                    "allowsRedistribution": False,
                    "requiresAttribution": True
                }
            }
            
            return {
                "success": True,
                "data": data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting content template details: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting content template details: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class ContentTemplateReviewsResource(Resource):
    """
    Resource for getting reviews for a content template
    """
    def get(self, template_id):
        """
        Get reviews for a content template
        
        Args:
            template_id (str): The content template ID
            
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            
        Returns:
            dict: Template reviews or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('max_rows', 25)
        
        try:
            # Demo data
            reviews = [
                {
                    "id": "review-12345",
                    "user": {
                        "id": 1234567,
                        "name": "GameDeveloper123",
                        "displayName": "Pro Developer",
                        "hasVerifiedBadge": False
                    },
                    "rating": 5,
                    "title": "Amazing Template!",
                    "content": "This template saved me weeks of development time. Everything is well organized and documented.",
                    "created": "2023-11-20T14:32:45Z",
                    "updated": None,
                    "likes": 45,
                    "dislikes": 2,
                    "isVerifiedPurchase": True
                },
                {
                    "id": "review-23456",
                    "user": {
                        "id": 2345678,
                        "name": "NewDeveloper",
                        "displayName": "Learning Developer",
                        "hasVerifiedBadge": False
                    },
                    "rating": 4,
                    "title": "Great for Beginners",
                    "content": "This template is perfect for beginners. The code is clean and easy to understand. I removed one star because I found a few bugs in the weapon system.",
                    "created": "2023-11-15T09:45:12Z",
                    "updated": None,
                    "likes": 32,
                    "dislikes": 3,
                    "isVerifiedPurchase": True
                },
                {
                    "id": "review-34567",
                    "user": {
                        "id": 3456789,
                        "name": "StudioExpert",
                        "displayName": "Expert Developer",
                        "hasVerifiedBadge": True
                    },
                    "rating": 5,
                    "title": "Professional Quality",
                    "content": "The quality of this template is professional grade. The systems are robust and extensible. I highly recommend it for both beginners and experienced developers.",
                    "created": "2023-11-10T22:15:40Z",
                    "updated": "2023-11-10T22:20:15Z",
                    "likes": 67,
                    "dislikes": 1,
                    "isVerifiedPurchase": True
                }
            ]
            
            return {
                "success": True,
                "data": reviews[:max_rows]
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting content template reviews: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting content template reviews: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class AssetCreationResource(Resource):
    """
    Resource for getting asset creation statistics
    """
    def get(self, user_id):
        """
        Get asset creation statistics for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Returns:
            dict: User's asset creation statistics or error response
        """
        try:
            # Demo data
            data = {
                "totalAssetsCreated": 78,
                "assetsByType": {
                    "Image": 23,
                    "Mesh": 15,
                    "Audio": 10,
                    "Model": 30
                },
                "publishedAssets": 65,
                "pendingReviewAssets": 5,
                "rejectedAssets": 8,
                "mostPopularAsset": {
                    "id": 12345678,
                    "name": "Dragon Wings",
                    "type": "Mesh",
                    "uses": 4567
                },
                "recentCreations": [
                    {
                        "id": 87654321,
                        "name": "Medieval Sword",
                        "type": "Mesh",
                        "created": "2023-11-25T00:00:00Z",
                        "status": "Published"
                    },
                    {
                        "id": 76543210,
                        "name": "Victory Fanfare",
                        "type": "Audio",
                        "created": "2023-11-22T00:00:00Z",
                        "status": "Published"
                    },
                    {
                        "id": 65432109,
                        "name": "Space Background",
                        "type": "Image",
                        "created": "2023-11-20T00:00:00Z",
                        "status": "Published"
                    }
                ],
                "creationTrend": [
                    {"month": "2023-06", "count": 5},
                    {"month": "2023-07", "count": 7},
                    {"month": "2023-08", "count": 10},
                    {"month": "2023-09", "count": 8},
                    {"month": "2023-10", "count": 12},
                    {"month": "2023-11", "count": 9}
                ]
            }
            
            return {
                "success": True,
                "data": data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting asset creation statistics: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting asset creation statistics: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class AssetLibraryResource(Resource):
    """
    Resource for getting user's asset library
    """
    def get(self, user_id):
        """
        Get asset library for a user
        
        Args:
            user_id (int): The Roblox user ID
            
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            asset_type (str, optional): Filter by asset type
            
        Returns:
            dict: User's asset library or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('max_rows', 25)
        asset_type = request.args.get('asset_type', None)
        
        try:
            # Demo data
            assets = [
                {
                    "id": 12345678,
                    "name": "Dragon Wings",
                    "description": "Detailed dragon wings mesh",
                    "type": "Mesh",
                    "created": "2023-09-15T00:00:00Z",
                    "updated": "2023-09-15T00:00:00Z",
                    "uses": 4567,
                    "isPublic": True,
                    "status": "Published",
                    "thumbnailUrl": "https://example.com/thumbnails/assets/dragon-wings.png"
                },
                {
                    "id": 23456789,
                    "name": "Epic Battle Music",
                    "description": "Dynamic music for battle scenes",
                    "type": "Audio",
                    "created": "2023-10-10T00:00:00Z",
                    "updated": "2023-10-10T00:00:00Z",
                    "uses": 2345,
                    "isPublic": True,
                    "status": "Published",
                    "thumbnailUrl": "https://example.com/thumbnails/assets/battle-music.png"
                },
                {
                    "id": 34567890,
                    "name": "Fantasy Landscape",
                    "description": "High-quality fantasy landscape texture",
                    "type": "Image",
                    "created": "2023-11-05T00:00:00Z",
                    "updated": "2023-11-05T00:00:00Z",
                    "uses": 1234,
                    "isPublic": True,
                    "status": "Published",
                    "thumbnailUrl": "https://example.com/thumbnails/assets/fantasy-landscape.png"
                },
                {
                    "id": 45678901,
                    "name": "Sci-Fi Helmet",
                    "description": "Futuristic helmet mesh",
                    "type": "Mesh",
                    "created": "2023-11-15T00:00:00Z",
                    "updated": "2023-11-15T00:00:00Z",
                    "uses": 987,
                    "isPublic": True,
                    "status": "Published",
                    "thumbnailUrl": "https://example.com/thumbnails/assets/sci-fi-helmet.png"
                },
                {
                    "id": 56789012,
                    "name": "UI Button Set",
                    "description": "Set of modern UI buttons",
                    "type": "Model",
                    "created": "2023-11-25T00:00:00Z",
                    "updated": "2023-11-25T00:00:00Z",
                    "uses": 3456,
                    "isPublic": True,
                    "status": "Published",
                    "thumbnailUrl": "https://example.com/thumbnails/assets/ui-buttons.png"
                }
            ]
            
            # Apply asset type filters if provided
            if asset_type:
                assets = [asset for asset in assets if asset["type"].lower() == asset_type.lower()]
            
            return {
                "success": True,
                "data": assets[:max_rows]
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting asset library: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting asset library: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class AssetDetailsResource(Resource):
    """
    Resource for getting asset details
    """
    def get(self, asset_id):
        """
        Get details for an asset
        
        Args:
            asset_id (int): The asset ID
            
        Returns:
            dict: Asset details or error response
        """
        try:
            # Demo data
            data = {
                "id": asset_id,
                "name": "Dragon Wings",
                "description": "Detailed dragon wings mesh with animated textures",
                "type": "Mesh",
                "subtype": "Character Accessory",
                "creator": {
                    "id": 8765432,
                    "name": "AssetCreator123",
                    "type": "User"
                },
                "created": "2023-09-15T00:00:00Z",
                "updated": "2023-09-15T00:00:00Z",
                "version": "1.0",
                "uses": 4567,
                "favorites": 2345,
                "isPublic": True,
                "status": "Published",
                "thumbnailUrl": "https://example.com/thumbnails/assets/dragon-wings.png",
                "previewUrl": "https://example.com/previews/assets/dragon-wings.png",
                "tags": ["Wings", "Dragon", "Fantasy", "Accessory"],
                "fileSize": 1567892,  # In bytes
                "dimensions": {
                    "width": 512,
                    "height": 256,
                    "depth": 128
                },
                "polyCount": 12567,
                "usedInGames": [
                    {
                        "id": 123456789,
                        "name": "Dragon Adventure",
                        "creator": "DragonStudios",
                        "visits": 1234567
                    },
                    {
                        "id": 234567890,
                        "name": "Fantasy RPG",
                        "creator": "RPGCreations",
                        "visits": 987654
                    }
                ],
                "license": {
                    "type": "Standard",
                    "allowsModification": True,
                    "allowsRedistribution": True,
                    "requiresAttribution": True
                }
            }
            
            return {
                "success": True,
                "data": data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting asset details: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting asset details: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class AssetTagsResource(Resource):
    """
    Resource for getting popular asset tags
    """
    def get(self):
        """
        Get popular asset tags
        
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            asset_type (str, optional): Filter by asset type
            
        Returns:
            dict: Popular asset tags or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('max_rows', 25)
        asset_type = request.args.get('asset_type', None)
        
        try:
            # Demo data
            tags = [
                {
                    "name": "Fantasy",
                    "count": 12345,
                    "associatedTypes": ["Mesh", "Image", "Model"],
                    "trending": True
                },
                {
                    "name": "Sci-Fi",
                    "count": 10987,
                    "associatedTypes": ["Mesh", "Image", "Model", "Audio"],
                    "trending": True
                },
                {
                    "name": "Medieval",
                    "count": 9876,
                    "associatedTypes": ["Mesh", "Image", "Model"],
                    "trending": False
                },
                {
                    "name": "Modern",
                    "count": 8765,
                    "associatedTypes": ["Mesh", "Image", "Model"],
                    "trending": False
                },
                {
                    "name": "Weapon",
                    "count": 7654,
                    "associatedTypes": ["Mesh", "Model"],
                    "trending": True
                },
                {
                    "name": "Character",
                    "count": 6543,
                    "associatedTypes": ["Mesh", "Model"],
                    "trending": False
                },
                {
                    "name": "Vehicle",
                    "count": 5432,
                    "associatedTypes": ["Mesh", "Model"],
                    "trending": False
                },
                {
                    "name": "Nature",
                    "count": 4321,
                    "associatedTypes": ["Mesh", "Image", "Model"],
                    "trending": True
                },
                {
                    "name": "Building",
                    "count": 3210,
                    "associatedTypes": ["Mesh", "Model"],
                    "trending": False
                },
                {
                    "name": "UI",
                    "count": 2109,
                    "associatedTypes": ["Image", "Model"],
                    "trending": True
                }
            ]
            
            # Apply asset type filters if provided
            if asset_type:
                tags = [tag for tag in tags if asset_type in tag["associatedTypes"]]
            
            return {
                "success": True,
                "data": tags[:max_rows]
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting popular asset tags: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting popular asset tags: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class AssetVersionsResource(Resource):
    """
    Resource for getting asset versions
    """
    def get(self, asset_id):
        """
        Get versions for an asset
        
        Args:
            asset_id (int): The asset ID
            
        Query Parameters:
            max_rows (int, optional): Maximum number of results (default: 25)
            
        Returns:
            dict: Asset versions or error response
        """
        schema = PaginationSchema()
        args = schema.load(request.args)
        
        max_rows = args.get('max_rows', 25)
        
        try:
            # Demo data
            versions = [
                {
                    "versionNumber": 3,
                    "created": "2023-10-15T00:00:00Z",
                    "creatorId": 8765432,
                    "creatorName": "AssetCreator123",
                    "changeDescription": "Optimized mesh topology and reduced polycount",
                    "fileSize": 1567892,  # In bytes
                    "polyCount": 12567,
                    "isCurrent": True
                },
                {
                    "versionNumber": 2,
                    "created": "2023-09-30T00:00:00Z",
                    "creatorId": 8765432,
                    "creatorName": "AssetCreator123",
                    "changeDescription": "Added animated texture and improved UV mapping",
                    "fileSize": 1789456,  # In bytes
                    "polyCount": 15678,
                    "isCurrent": False
                },
                {
                    "versionNumber": 1,
                    "created": "2023-09-15T00:00:00Z",
                    "creatorId": 8765432,
                    "creatorName": "AssetCreator123",
                    "changeDescription": "Initial release",
                    "fileSize": 1854321,  # In bytes
                    "polyCount": 16789,
                    "isCurrent": False
                }
            ]
            
            return {
                "success": True,
                "data": versions[:max_rows]
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting asset versions: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting asset versions: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500

class AssetStatsResource(Resource):
    """
    Resource for getting asset statistics
    """
    def get(self, asset_id):
        """
        Get statistics for an asset
        
        Args:
            asset_id (int): The asset ID
            
        Returns:
            dict: Asset statistics or error response
        """
        try:
            # Demo data
            data = {
                "id": asset_id,
                "name": "Dragon Wings",
                "created": "2023-09-15T00:00:00Z",
                "useStats": {
                    "total": 4567,
                    "byMonth": [
                        {"month": "2023-09", "count": 567},
                        {"month": "2023-10", "count": 1234},
                        {"month": "2023-11", "count": 2766}
                    ],
                    "byGameType": {
                        "RPG": 2345,
                        "Adventure": 1234,
                        "Fighting": 988
                    }
                },
                "favoriteStats": {
                    "total": 2345,
                    "byMonth": [
                        {"month": "2023-09", "count": 345},
                        {"month": "2023-10", "count": 987},
                        {"month": "2023-11", "count": 1013}
                    ]
                },
                "performanceStats": {
                    "averageLoadTime": 0.45,  # In seconds
                    "memoryUsage": 12.4,  # In MB
                    "drawCalls": 3
                },
                "popularWith": [
                    {
                        "id": 123456789,
                        "name": "Fantasy Character Pack",
                        "type": "Bundle",
                        "uses": 567
                    },
                    {
                        "id": 234567890,
                        "name": "Dragon Avatar",
                        "type": "Avatar",
                        "uses": 432
                    }
                ]
            }
            
            return {
                "success": True,
                "data": data
            }
        except RobloxAPIError as e:
            logger.error(f"Error getting asset statistics: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }, e.status_code
        except Exception as e:
            logger.error(f"Unexpected error getting asset statistics: {str(e)}")
            return {
                "success": False,
                "message": "An unexpected error occurred"
            }, 500