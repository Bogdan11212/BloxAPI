"""
GraphQL Schema Module for BloxAPI

This module defines the GraphQL schema for the BloxAPI service,
enabling flexible querying across multiple API resources.
"""

import logging
import graphene
from graphene import ObjectType, String, Int, List, Field, Boolean, Float
from typing import Dict, Any, Optional, List as TypeList

# Configure logging
logger = logging.getLogger(__name__)

# Define types for GraphQL schema
class User(ObjectType):
    """User type for GraphQL schema"""
    id = Int(required=True)
    username = String()
    display_name = String()
    description = String()
    created = String()
    is_banned = Boolean()
    external_app_display_name = String()
    has_premium = Boolean()
    
class Game(ObjectType):
    """Game type for GraphQL schema"""
    id = Int(required=True)
    name = String()
    description = String()
    creator_id = Int()
    creator_name = String()
    created = String()
    updated = String()
    max_players = Int()
    visit_count = Int()
    like_count = Int()
    dislike_count = Int()
    is_featured = Boolean()
    
class Asset(ObjectType):
    """Asset type for GraphQL schema"""
    id = Int(required=True)
    name = String()
    description = String()
    asset_type = String()
    creator_id = Int()
    creator_name = String()
    created = String()
    updated = String()
    price = Int()
    sales = Int()
    is_limited = Boolean()
    is_limited_unique = Boolean()
    remaining = Int()
    
class Badge(ObjectType):
    """Badge type for GraphQL schema"""
    id = Int(required=True)
    name = String()
    description = String()
    enabled = Boolean()
    statistics = Field(lambda: BadgeStatistics)
    awarded_date = String()
    
class BadgeStatistics(ObjectType):
    """Badge statistics type for GraphQL schema"""
    win_count = Int()
    win_percentage = Float()
    
class Group(ObjectType):
    """Group type for GraphQL schema"""
    id = Int(required=True)
    name = String()
    description = String()
    member_count = Int()
    is_builders_club_only = Boolean()
    public_entry_allowed = Boolean()
    owner = Field(lambda: User)
    
class Friend(ObjectType):
    """Friend relationship type for GraphQL schema"""
    id = Int(required=True)
    username = String()
    display_name = String()
    is_online = Boolean()
    presence = String()
    is_best_friend = Boolean()
    
class Server(ObjectType):
    """Game server type for GraphQL schema"""
    id = String(required=True)
    max_players = Int()
    playing = Int()
    fps = Float()
    ping = Int()
    
class Analytics(ObjectType):
    """Analytics type for GraphQL schema"""
    date = String()
    value = Int()
    
class Presence(ObjectType):
    """User presence type for GraphQL schema"""
    user_id = Int()
    username = String()
    game_id = Int()
    game_name = String()
    place_id = Int()
    place_name = String()
    last_online = String()
    last_location = String()
    
class UserInventoryItem(ObjectType):
    """User inventory item type for GraphQL schema"""
    id = Int(required=True)
    name = String()
    asset_type = String()
    created = String()
    updated = String()
    recent_average_price = Int()
    
class SearchResult(ObjectType):
    """Search result type for GraphQL schema"""
    id = Int()
    name = String()
    description = String()
    type = String()
    thumbnail_url = String()
    
# Define Query type for GraphQL schema
class Query(ObjectType):
    """Root query type for GraphQL schema"""
    # User queries
    user = Field(User, id=Int(required=True))
    users = List(User, ids=List(Int, required=True))
    search_users = List(User, keyword=String(required=True), limit=Int())
    
    # Game queries
    game = Field(Game, id=Int(required=True))
    games = List(Game, ids=List(Int, required=True))
    trending_games = List(Game, limit=Int())
    
    # Asset queries
    asset = Field(Asset, id=Int(required=True))
    assets = List(Asset, ids=List(Int, required=True))
    
    # Badge queries
    badge = Field(Badge, id=Int(required=True))
    game_badges = List(Badge, universe_id=Int(required=True), limit=Int())
    user_badges = List(Badge, user_id=Int(required=True), limit=Int())
    
    # Group queries
    group = Field(Group, id=Int(required=True))
    user_groups = List(Group, user_id=Int(required=True), limit=Int())
    
    # Friend queries
    friends = List(Friend, user_id=Int(required=True), limit=Int())
    
    # Server queries
    servers = List(Server, universe_id=Int(required=True), limit=Int())
    
    # Analytics queries
    game_analytics = List(Analytics, universe_id=Int(required=True), metric_type=String(required=True), time_frame=String())
    
    # Presence queries
    user_presence = Field(Presence, user_id=Int(required=True))
    
    # Inventory queries
    user_inventory = List(UserInventoryItem, user_id=Int(required=True), asset_type=String(), limit=Int())
    
    # Search queries
    search = List(SearchResult, keyword=String(required=True), types=List(String), limit=Int())
    
    def resolve_user(self, info, id):
        """Resolve user query"""
        # This is where you would fetch user data from your API or database
        logger.debug(f"Resolving user query for ID: {id}")
        # For demonstration purposes, return mock data
        return {
            "id": id,
            "username": f"user_{id}",
            "display_name": f"User {id}",
            "description": "This is a user description",
            "created": "2020-01-01T00:00:00Z",
            "is_banned": False,
            "external_app_display_name": "",
            "has_premium": True
        }
    
    def resolve_users(self, info, ids):
        """Resolve users query"""
        logger.debug(f"Resolving users query for IDs: {ids}")
        return [self.resolve_user(info, id) for id in ids]
    
    def resolve_search_users(self, info, keyword, limit=10):
        """Resolve search users query"""
        logger.debug(f"Resolving search users query for keyword: {keyword}, limit: {limit}")
        # In a real implementation, you would search your database or API
        return [
            {
                "id": i,
                "username": f"{keyword}_user_{i}",
                "display_name": f"{keyword.capitalize()} User {i}",
                "description": f"User matching '{keyword}'",
                "created": "2020-01-01T00:00:00Z",
                "is_banned": False,
                "external_app_display_name": "",
                "has_premium": i % 2 == 0
            }
            for i in range(1, min(limit, 10) + 1)
        ]
    
    def resolve_game(self, info, id):
        """Resolve game query"""
        logger.debug(f"Resolving game query for ID: {id}")
        return {
            "id": id,
            "name": f"Game {id}",
            "description": "This is a game description",
            "creator_id": 1,
            "creator_name": "Creator",
            "created": "2020-01-01T00:00:00Z",
            "updated": "2020-01-02T00:00:00Z",
            "max_players": 100,
            "visit_count": 1000,
            "like_count": 500,
            "dislike_count": 50,
            "is_featured": True
        }
    
    def resolve_games(self, info, ids):
        """Resolve games query"""
        logger.debug(f"Resolving games query for IDs: {ids}")
        return [self.resolve_game(info, id) for id in ids]
    
    def resolve_trending_games(self, info, limit=10):
        """Resolve trending games query"""
        logger.debug(f"Resolving trending games query, limit: {limit}")
        return [
            {
                "id": i,
                "name": f"Trending Game {i}",
                "description": "This is a trending game",
                "creator_id": 1,
                "creator_name": "Creator",
                "created": "2020-01-01T00:00:00Z",
                "updated": "2020-01-02T00:00:00Z",
                "max_players": 100,
                "visit_count": 1000 * (10 - i + 1),
                "like_count": 500 * (10 - i + 1),
                "dislike_count": 50,
                "is_featured": True
            }
            for i in range(1, min(limit, 10) + 1)
        ]
    
    def resolve_asset(self, info, id):
        """Resolve asset query"""
        logger.debug(f"Resolving asset query for ID: {id}")
        return {
            "id": id,
            "name": f"Asset {id}",
            "description": "This is an asset description",
            "asset_type": "Hat",
            "creator_id": 1,
            "creator_name": "Creator",
            "created": "2020-01-01T00:00:00Z",
            "updated": "2020-01-02T00:00:00Z",
            "price": 100,
            "sales": 1000,
            "is_limited": False,
            "is_limited_unique": False,
            "remaining": None
        }
    
    def resolve_assets(self, info, ids):
        """Resolve assets query"""
        logger.debug(f"Resolving assets query for IDs: {ids}")
        return [self.resolve_asset(info, id) for id in ids]
    
    def resolve_badge(self, info, id):
        """Resolve badge query"""
        logger.debug(f"Resolving badge query for ID: {id}")
        return {
            "id": id,
            "name": f"Badge {id}",
            "description": "This is a badge description",
            "enabled": True,
            "statistics": {
                "win_count": 1000,
                "win_percentage": 0.5
            },
            "awarded_date": None
        }
    
    def resolve_game_badges(self, info, universe_id, limit=10):
        """Resolve game badges query"""
        logger.debug(f"Resolving game badges query for universe ID: {universe_id}, limit: {limit}")
        return [
            {
                "id": i,
                "name": f"Game {universe_id} Badge {i}",
                "description": f"Badge for game {universe_id}",
                "enabled": True,
                "statistics": {
                    "win_count": 1000 - i * 100,
                    "win_percentage": 0.5 - i * 0.05
                },
                "awarded_date": None
            }
            for i in range(1, min(limit, 10) + 1)
        ]
    
    def resolve_user_badges(self, info, user_id, limit=10):
        """Resolve user badges query"""
        logger.debug(f"Resolving user badges query for user ID: {user_id}, limit: {limit}")
        return [
            {
                "id": i,
                "name": f"User {user_id} Badge {i}",
                "description": f"Badge owned by user {user_id}",
                "enabled": True,
                "statistics": {
                    "win_count": 1000 - i * 100,
                    "win_percentage": 0.5 - i * 0.05
                },
                "awarded_date": "2020-01-01T00:00:00Z"
            }
            for i in range(1, min(limit, 10) + 1)
        ]
    
    def resolve_group(self, info, id):
        """Resolve group query"""
        logger.debug(f"Resolving group query for ID: {id}")
        return {
            "id": id,
            "name": f"Group {id}",
            "description": "This is a group description",
            "member_count": 1000,
            "is_builders_club_only": False,
            "public_entry_allowed": True,
            "owner": {
                "id": 1,
                "username": "owner",
                "display_name": "Owner",
                "description": "Group owner",
                "created": "2020-01-01T00:00:00Z",
                "is_banned": False,
                "external_app_display_name": "",
                "has_premium": True
            }
        }
    
    def resolve_user_groups(self, info, user_id, limit=10):
        """Resolve user groups query"""
        logger.debug(f"Resolving user groups query for user ID: {user_id}, limit: {limit}")
        return [
            {
                "id": i,
                "name": f"User {user_id} Group {i}",
                "description": f"Group for user {user_id}",
                "member_count": 1000 - i * 100,
                "is_builders_club_only": False,
                "public_entry_allowed": True,
                "owner": {
                    "id": user_id,
                    "username": f"user_{user_id}",
                    "display_name": f"User {user_id}",
                    "description": "Group owner",
                    "created": "2020-01-01T00:00:00Z",
                    "is_banned": False,
                    "external_app_display_name": "",
                    "has_premium": True
                }
            }
            for i in range(1, min(limit, 10) + 1)
        ]
    
    def resolve_friends(self, info, user_id, limit=10):
        """Resolve friends query"""
        logger.debug(f"Resolving friends query for user ID: {user_id}, limit: {limit}")
        return [
            {
                "id": user_id + i,
                "username": f"friend_{user_id + i}",
                "display_name": f"Friend {user_id + i}",
                "is_online": i % 2 == 0,
                "presence": "In Game" if i % 2 == 0 else "Offline",
                "is_best_friend": i == 1
            }
            for i in range(1, min(limit, 10) + 1)
        ]
    
    def resolve_servers(self, info, universe_id, limit=10):
        """Resolve servers query"""
        logger.debug(f"Resolving servers query for universe ID: {universe_id}, limit: {limit}")
        return [
            {
                "id": f"server_{universe_id}_{i}",
                "max_players": 10,
                "playing": i,
                "fps": 60.0 - i,
                "ping": 50 + i * 5
            }
            for i in range(1, min(limit, 10) + 1)
        ]
    
    def resolve_game_analytics(self, info, universe_id, metric_type, time_frame="past1day"):
        """Resolve game analytics query"""
        logger.debug(f"Resolving game analytics query for universe ID: {universe_id}, metric type: {metric_type}, time frame: {time_frame}")
        return [
            {
                "date": f"2020-01-0{i}T00:00:00Z",
                "value": 1000 - i * 100
            }
            for i in range(1, 8)
        ]
    
    def resolve_user_presence(self, info, user_id):
        """Resolve user presence query"""
        logger.debug(f"Resolving user presence query for user ID: {user_id}")
        return {
            "user_id": user_id,
            "username": f"user_{user_id}",
            "game_id": 1,
            "game_name": "Sample Game",
            "place_id": 2,
            "place_name": "Sample Place",
            "last_online": "2020-01-01T00:00:00Z",
            "last_location": "In Game"
        }
    
    def resolve_user_inventory(self, info, user_id, asset_type=None, limit=10):
        """Resolve user inventory query"""
        logger.debug(f"Resolving user inventory query for user ID: {user_id}, asset type: {asset_type}, limit: {limit}")
        items = [
            {
                "id": i,
                "name": f"Inventory Item {i}",
                "asset_type": "Hat" if i % 2 == 0 else "Shirt",
                "created": "2020-01-01T00:00:00Z",
                "updated": "2020-01-02T00:00:00Z",
                "recent_average_price": 100 * i
            }
            for i in range(1, min(limit, 10) + 1)
        ]
        
        if asset_type:
            items = [item for item in items if item["asset_type"] == asset_type]
        
        return items
    
    def resolve_search(self, info, keyword, types=None, limit=10):
        """Resolve search query"""
        logger.debug(f"Resolving search query for keyword: {keyword}, types: {types}, limit: {limit}")
        result_types = types or ["User", "Game", "Group", "Asset"]
        results = []
        
        for i in range(1, min(limit, 10) + 1):
            result_type = result_types[i % len(result_types)]
            results.append({
                "id": i,
                "name": f"{keyword} {result_type} {i}",
                "description": f"Search result for '{keyword}'",
                "type": result_type,
                "thumbnail_url": f"https://example.com/{result_type.lower()}/{i}.png"
            })
        
        return results

# Create schema
schema = graphene.Schema(query=Query)