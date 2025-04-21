"""
GraphQL Schema for BloxAPI

This module defines the GraphQL schema for the BloxAPI, providing a flexible
query interface for accessing Roblox data.
"""

import graphene
from graphene import relay
from typing import Dict, List, Any, Optional
import logging
from .roblox_api import RobloxAPI

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Roblox API
roblox_api = RobloxAPI()

# User related types
class UserType(graphene.ObjectType):
    """Type representing a Roblox user"""
    class Meta:
        interfaces = (relay.Node,)
    
    id = graphene.ID(required=True, description="The user's ID")
    name = graphene.String(description="The user's username")
    display_name = graphene.String(description="The user's display name")
    description = graphene.String(description="The user's profile description")
    created = graphene.String(description="ISO timestamp of when the user was created")
    is_banned = graphene.Boolean(description="Whether the user is banned")
    external_app_display_name = graphene.String(description="External app display name")
    has_verified_badge = graphene.Boolean(description="Whether the user has a verified badge")
    
    # Profile data
    avatar_url = graphene.String(description="URL to the user's avatar image")
    is_premium = graphene.Boolean(description="Whether the user has Roblox Premium")
    
    # Connections
    friends = graphene.List(lambda: UserType, description="The user's friends",
                           limit=graphene.Int(description="Maximum number of friends to return"))
    followers = graphene.List(lambda: UserType, description="The user's followers",
                             limit=graphene.Int(description="Maximum number of followers to return"))
    following = graphene.List(lambda: UserType, description="Users the user is following",
                             limit=graphene.Int(description="Maximum number of following to return"))
    groups = graphene.List(lambda: GroupType, description="Groups the user is in",
                           limit=graphene.Int(description="Maximum number of groups to return"))
    
    # Badge counts
    badges_count = graphene.Int(description="Number of badges the user has")
    
    # Asset ownership
    owns_asset = graphene.Boolean(description="Whether the user owns a specific asset",
                                 asset_id=graphene.ID(required=True, description="Asset ID to check"))
    
    # Presence
    presence = graphene.Field(lambda: PresenceType, description="The user's current presence status")
    
    def resolve_friends(self, info, limit=10):
        try:
            friends_data = roblox_api.friends.get_friends(self.id, limit=limit)
            return [UserType(id=friend.get("id"), name=friend.get("name"), 
                            display_name=friend.get("displayName")) 
                    for friend in friends_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving friends: {e}")
            return []
    
    def resolve_followers(self, info, limit=10):
        try:
            followers_data = roblox_api.users.get_followers(self.id, limit=limit)
            return [UserType(id=follower.get("id"), name=follower.get("name"),
                            display_name=follower.get("displayName"))
                    for follower in followers_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving followers: {e}")
            return []
    
    def resolve_following(self, info, limit=10):
        try:
            following_data = roblox_api.users.get_following(self.id, limit=limit)
            return [UserType(id=following.get("id"), name=following.get("name"),
                            display_name=following.get("displayName"))
                    for following in following_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving following: {e}")
            return []
    
    def resolve_groups(self, info, limit=10):
        try:
            groups_data = roblox_api.groups.get_user_groups(self.id)
            return [GroupType(id=group.get("group", {}).get("id"),
                             name=group.get("group", {}).get("name"))
                    for group in groups_data.get("data", [])[:limit]]
        except Exception as e:
            logger.error(f"Error resolving groups: {e}")
            return []
    
    def resolve_owns_asset(self, info, asset_id):
        try:
            ownership = roblox_api.assets.check_ownership(self.id, asset_id)
            return ownership.get("owns", False)
        except Exception as e:
            logger.error(f"Error resolving asset ownership: {e}")
            return False
    
    def resolve_presence(self, info):
        try:
            presence_data = roblox_api.presence.get_user_presence(self.id)
            if presence_data:
                return PresenceType(
                    user_id=presence_data.get("userId", self.id),
                    presence_type=presence_data.get("userPresenceType", 0),
                    last_location=presence_data.get("lastLocation", ""),
                    place_id=presence_data.get("placeId"),
                    root_place_id=presence_data.get("rootPlaceId"),
                    game_id=presence_data.get("gameId"),
                    universe_id=presence_data.get("universeId"),
                    last_online=presence_data.get("lastOnline")
                )
            return None
        except Exception as e:
            logger.error(f"Error resolving presence: {e}")
            return None


class PresenceType(graphene.ObjectType):
    """Type representing a user's presence status"""
    user_id = graphene.ID(required=True)
    presence_type = graphene.Int(description="Type of presence (0=Offline, 1=Online, 2=In-Game, etc.)")
    last_location = graphene.String(description="Last known location")
    place_id = graphene.ID(description="Current place ID if in-game")
    root_place_id = graphene.ID(description="Root place ID if in-game")
    game_id = graphene.ID(description="Current game ID if in-game")
    universe_id = graphene.ID(description="Current universe ID if in-game")
    last_online = graphene.String(description="ISO timestamp of when the user was last online")


class GroupType(graphene.ObjectType):
    """Type representing a Roblox group"""
    class Meta:
        interfaces = (relay.Node,)
    
    id = graphene.ID(required=True, description="The group's ID")
    name = graphene.String(description="The group's name")
    description = graphene.String(description="The group's description")
    member_count = graphene.Int(description="Number of members in the group")
    is_builders_club_only = graphene.Boolean(description="Whether the group is Builder's Club only")
    public_entry_allowed = graphene.Boolean(description="Whether public entry is allowed")
    owner = graphene.Field(lambda: UserType, description="The group's owner")
    
    # Connections
    members = graphene.List(lambda: GroupMemberType, description="Members of the group",
                          limit=graphene.Int(description="Maximum number of members to return"))
    roles = graphene.List(lambda: GroupRoleType, description="Roles in the group")
    
    def resolve_owner(self, info):
        try:
            owner_data = roblox_api.groups.get_group_owner(self.id)
            if owner_data:
                return UserType(
                    id=owner_data.get("id"),
                    name=owner_data.get("name"),
                    display_name=owner_data.get("displayName")
                )
            return None
        except Exception as e:
            logger.error(f"Error resolving group owner: {e}")
            return None
    
    def resolve_members(self, info, limit=10):
        try:
            members_data = roblox_api.groups.get_group_members(self.id, limit=limit)
            return [GroupMemberType(
                user=UserType(
                    id=member.get("user", {}).get("userId"),
                    name=member.get("user", {}).get("username"),
                    display_name=member.get("user", {}).get("displayName")
                ),
                role=GroupRoleType(
                    id=member.get("role", {}).get("id"),
                    name=member.get("role", {}).get("name"),
                    rank=member.get("role", {}).get("rank")
                )
            ) for member in members_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving group members: {e}")
            return []
    
    def resolve_roles(self, info):
        try:
            roles_data = roblox_api.groups.get_group_roles(self.id)
            return [GroupRoleType(
                id=role.get("id"),
                name=role.get("name"),
                rank=role.get("rank"),
                member_count=role.get("memberCount")
            ) for role in roles_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving group roles: {e}")
            return []


class GroupMemberType(graphene.ObjectType):
    """Type representing a member of a group with their role"""
    user = graphene.Field(UserType, required=True, description="The user")
    role = graphene.Field(lambda: GroupRoleType, description="The user's role in the group")


class GroupRoleType(graphene.ObjectType):
    """Type representing a role in a group"""
    id = graphene.ID(required=True)
    name = graphene.String(description="Role name")
    rank = graphene.Int(description="Role rank")
    member_count = graphene.Int(description="Number of members with this role")


class GameType(graphene.ObjectType):
    """Type representing a Roblox game"""
    class Meta:
        interfaces = (relay.Node,)
    
    id = graphene.ID(required=True, description="The game's ID")
    name = graphene.String(description="The game's name")
    description = graphene.String(description="The game's description")
    creator = graphene.Field(lambda: CreatorType, description="The game's creator")
    price = graphene.Int(description="The game's price in Robux (0 if free)")
    allowed_gear_types = graphene.List(graphene.String, description="Types of gear allowed in the game")
    created = graphene.String(description="ISO timestamp of when the game was created")
    updated = graphene.String(description="ISO timestamp of when the game was last updated")
    max_players = graphene.Int(description="Maximum number of players allowed")
    playing = graphene.Int(description="Number of users currently playing")
    visits = graphene.Int(description="Total number of visits to the game")
    favorites = graphene.Int(description="Number of times the game has been favorited")
    
    # Connections
    badges = graphene.List(lambda: BadgeType, description="Badges associated with the game",
                          limit=graphene.Int(description="Maximum number of badges to return"))
    
    # Game passes
    game_passes = graphene.List(lambda: GamePassType, description="Game passes for this game",
                              limit=graphene.Int(description="Maximum number of game passes to return"))
    
    # Server instances
    servers = graphene.List(lambda: ServerType, description="Active server instances",
                           limit=graphene.Int(description="Maximum number of servers to return"))
    
    def resolve_badges(self, info, limit=50):
        try:
            badges_data = roblox_api.badges.get_game_badges(self.id, limit=limit)
            return [BadgeType(
                id=badge.get("id"),
                name=badge.get("name"),
                description=badge.get("description"),
                enabled=badge.get("enabled", True),
                icon_image_id=badge.get("iconImageId")
            ) for badge in badges_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving game badges: {e}")
            return []
    
    def resolve_game_passes(self, info, limit=50):
        try:
            passes_data = roblox_api.games.get_game_passes(self.id, limit=limit)
            return [GamePassType(
                id=game_pass.get("id"),
                name=game_pass.get("name"),
                description=game_pass.get("description"),
                price=game_pass.get("price", 0),
                icon_image_id=game_pass.get("iconImageId")
            ) for game_pass in passes_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving game passes: {e}")
            return []
    
    def resolve_servers(self, info, limit=10):
        try:
            servers_data = roblox_api.games.get_game_servers(self.id, limit=limit)
            return [ServerType(
                id=server.get("id"),
                max_players=server.get("maxPlayers", 0),
                playing=server.get("playing", 0),
                fps=server.get("fps", 0),
                ping=server.get("ping", 0)
            ) for server in servers_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving game servers: {e}")
            return []


class CreatorType(graphene.Union):
    """
    Type representing either a user or group creator
    """
    class Meta:
        types = (UserType, GroupType)


class BadgeType(graphene.ObjectType):
    """Type representing a Roblox badge"""
    id = graphene.ID(required=True)
    name = graphene.String(description="Badge name")
    description = graphene.String(description="Badge description")
    enabled = graphene.Boolean(description="Whether the badge is enabled")
    icon_image_id = graphene.ID(description="ID of the badge's icon image")
    created = graphene.String(description="ISO timestamp of when the badge was created")
    updated = graphene.String(description="ISO timestamp of when the badge was last updated")
    statistics = graphene.Field(lambda: BadgeStatisticsType, description="Statistics for this badge")
    
    # Get users who own this badge
    awarded_to = graphene.List(lambda: UserType, description="Users who own this badge",
                             limit=graphene.Int(description="Maximum number of users to return"))
    
    def resolve_statistics(self, info):
        try:
            stats_data = roblox_api.badges.get_badge_statistics(self.id)
            if stats_data:
                return BadgeStatisticsType(
                    past_day_awarded_count=stats_data.get("pastDayAwardedCount", 0),
                    awarded_count=stats_data.get("awardedCount", 0),
                    win_rate_percentage=stats_data.get("winRatePercentage", 0)
                )
            return None
        except Exception as e:
            logger.error(f"Error resolving badge statistics: {e}")
            return None
    
    def resolve_awarded_to(self, info, limit=50):
        try:
            awarded_data = roblox_api.badges.get_badge_awarded_users(self.id, limit=limit)
            return [UserType(
                id=user.get("id"),
                name=user.get("name"),
                display_name=user.get("displayName")
            ) for user in awarded_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving badge awarded users: {e}")
            return []


class BadgeStatisticsType(graphene.ObjectType):
    """Type representing statistics for a badge"""
    past_day_awarded_count = graphene.Int(description="Number of times the badge was awarded in the past day")
    awarded_count = graphene.Int(description="Total number of times the badge has been awarded")
    win_rate_percentage = graphene.Float(description="Percentage of players who have won this badge")


class GamePassType(graphene.ObjectType):
    """Type representing a game pass"""
    id = graphene.ID(required=True)
    name = graphene.String(description="Game pass name")
    description = graphene.String(description="Game pass description")
    price = graphene.Int(description="Price in Robux")
    icon_image_id = graphene.ID(description="ID of the pass's icon image")
    
    # Players who own this pass
    owners = graphene.List(lambda: UserType, description="Users who own this game pass",
                          limit=graphene.Int(description="Maximum number of users to return"))
    
    def resolve_owners(self, info, limit=50):
        try:
            owners_data = roblox_api.games.get_gamepass_owners(self.id, limit=limit)
            return [UserType(
                id=user.get("id"),
                name=user.get("name"),
                display_name=user.get("displayName")
            ) for user in owners_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving game pass owners: {e}")
            return []


class ServerType(graphene.ObjectType):
    """Type representing a game server instance"""
    id = graphene.ID(required=True)
    max_players = graphene.Int(description="Maximum number of players allowed")
    playing = graphene.Int(description="Current number of players")
    fps = graphene.Float(description="Current server FPS")
    ping = graphene.Int(description="Current server ping")
    
    # Players in this server
    players = graphene.List(lambda: UserType, description="Players in this server")
    
    def resolve_players(self, info):
        try:
            players_data = roblox_api.games.get_server_players(self.id)
            return [UserType(
                id=player.get("id"),
                name=player.get("name"),
                display_name=player.get("displayName")
            ) for player in players_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving server players: {e}")
            return []


class AssetType(graphene.ObjectType):
    """Type representing a Roblox asset"""
    id = graphene.ID(required=True)
    name = graphene.String(description="Asset name")
    description = graphene.String(description="Asset description")
    asset_type = graphene.String(description="Type of asset")
    created = graphene.String(description="ISO timestamp of when the asset was created")
    updated = graphene.String(description="ISO timestamp of when the asset was last updated")
    price = graphene.Int(description="Price in Robux (0 if free)")
    sales = graphene.Int(description="Number of sales")
    is_limited = graphene.Boolean(description="Whether the asset is limited")
    is_limited_unique = graphene.Boolean(description="Whether the asset is limited unique")
    remaining = graphene.Int(description="Number of copies remaining (if limited)")
    creator = graphene.Field(lambda: CreatorType, description="The asset's creator")
    
    # Connections
    owners = graphene.List(lambda: UserType, description="Users who own this asset",
                          limit=graphene.Int(description="Maximum number of users to return"))
    
    def resolve_owners(self, info, limit=50):
        try:
            owners_data = roblox_api.assets.get_asset_owners(self.id, limit=limit)
            return [UserType(
                id=owner.get("id"),
                name=owner.get("name"),
                display_name=owner.get("displayName")
            ) for owner in owners_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving asset owners: {e}")
            return []


# Define query root
class Query(graphene.ObjectType):
    """Root query type"""
    # Node interface for Relay
    node = relay.Node.Field()
    
    # User queries
    user = graphene.Field(
        UserType,
        id=graphene.ID(description="User ID"),
        username=graphene.String(description="Username"),
        description="Get a user by ID or username"
    )
    
    users = graphene.List(
        UserType,
        ids=graphene.List(graphene.ID, required=True, description="User IDs"),
        description="Get multiple users by their IDs"
    )
    
    # Game queries
    game = graphene.Field(
        GameType,
        id=graphene.ID(required=True, description="Game ID"),
        description="Get a game by ID"
    )
    
    games = graphene.List(
        GameType,
        ids=graphene.List(graphene.ID, required=True, description="Game IDs"),
        description="Get multiple games by their IDs"
    )
    
    search_games = graphene.List(
        GameType,
        keyword=graphene.String(required=True, description="Search keyword"),
        limit=graphene.Int(description="Maximum number of results"),
        description="Search for games by keyword"
    )
    
    # Group queries
    group = graphene.Field(
        GroupType,
        id=graphene.ID(required=True, description="Group ID"),
        description="Get a group by ID"
    )
    
    # Asset queries
    asset = graphene.Field(
        AssetType,
        id=graphene.ID(required=True, description="Asset ID"),
        description="Get an asset by ID"
    )
    
    # Badge queries
    badge = graphene.Field(
        BadgeType,
        id=graphene.ID(required=True, description="Badge ID"),
        description="Get a badge by ID"
    )
    
    def resolve_user(self, info, id=None, username=None):
        try:
            if id:
                user_data = roblox_api.users.get_user(id)
            elif username:
                user_data = roblox_api.users.get_by_username(username)
            else:
                return None
            
            if user_data:
                return UserType(
                    id=user_data.get("id"),
                    name=user_data.get("name"),
                    display_name=user_data.get("displayName"),
                    description=user_data.get("description"),
                    created=user_data.get("created"),
                    is_banned=user_data.get("isBanned", False),
                    external_app_display_name=user_data.get("externalAppDisplayName"),
                    has_verified_badge=user_data.get("hasVerifiedBadge", False)
                )
            return None
        except Exception as e:
            logger.error(f"Error resolving user: {e}")
            return None
    
    def resolve_users(self, info, ids):
        try:
            users_data = roblox_api.users.get_users(ids)
            return [UserType(
                id=user.get("id"),
                name=user.get("name"),
                display_name=user.get("displayName")
            ) for user in users_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving users: {e}")
            return []
    
    def resolve_game(self, info, id):
        try:
            game_data = roblox_api.games.get_game(id)
            if game_data:
                return GameType(
                    id=game_data.get("id"),
                    name=game_data.get("name"),
                    description=game_data.get("description"),
                    price=game_data.get("price", 0),
                    created=game_data.get("created"),
                    updated=game_data.get("updated"),
                    max_players=game_data.get("maxPlayers"),
                    playing=game_data.get("playing"),
                    visits=game_data.get("visits"),
                    favorites=game_data.get("favorites")
                )
            return None
        except Exception as e:
            logger.error(f"Error resolving game: {e}")
            return None
    
    def resolve_games(self, info, ids):
        try:
            games_data = roblox_api.games.get_games(ids)
            return [GameType(
                id=game.get("id"),
                name=game.get("name"),
                playing=game.get("playing", 0),
                visits=game.get("visits", 0)
            ) for game in games_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving games: {e}")
            return []
    
    def resolve_search_games(self, info, keyword, limit=10):
        try:
            search_data = roblox_api.games.search_games(keyword, limit=limit)
            return [GameType(
                id=game.get("id"),
                name=game.get("name"),
                description=game.get("description"),
                playing=game.get("playing", 0)
            ) for game in search_data.get("data", [])]
        except Exception as e:
            logger.error(f"Error resolving game search: {e}")
            return []
    
    def resolve_group(self, info, id):
        try:
            group_data = roblox_api.groups.get_group(id)
            if group_data:
                return GroupType(
                    id=group_data.get("id"),
                    name=group_data.get("name"),
                    description=group_data.get("description"),
                    member_count=group_data.get("memberCount"),
                    is_builders_club_only=group_data.get("isBuildersClubOnly", False),
                    public_entry_allowed=group_data.get("publicEntryAllowed", True)
                )
            return None
        except Exception as e:
            logger.error(f"Error resolving group: {e}")
            return None
    
    def resolve_asset(self, info, id):
        try:
            asset_data = roblox_api.assets.get_asset(id)
            if asset_data:
                return AssetType(
                    id=asset_data.get("id"),
                    name=asset_data.get("name"),
                    description=asset_data.get("description"),
                    asset_type=asset_data.get("assetType"),
                    created=asset_data.get("created"),
                    updated=asset_data.get("updated"),
                    price=asset_data.get("price", 0),
                    sales=asset_data.get("sales", 0),
                    is_limited=asset_data.get("isLimited", False),
                    is_limited_unique=asset_data.get("isLimitedUnique", False),
                    remaining=asset_data.get("remaining")
                )
            return None
        except Exception as e:
            logger.error(f"Error resolving asset: {e}")
            return None
    
    def resolve_badge(self, info, id):
        try:
            badge_data = roblox_api.badges.get_badge(id)
            if badge_data:
                return BadgeType(
                    id=badge_data.get("id"),
                    name=badge_data.get("name"),
                    description=badge_data.get("description"),
                    enabled=badge_data.get("enabled", True),
                    icon_image_id=badge_data.get("iconImageId"),
                    created=badge_data.get("created"),
                    updated=badge_data.get("updated")
                )
            return None
        except Exception as e:
            logger.error(f"Error resolving badge: {e}")
            return None


# Create schema
schema = graphene.Schema(query=Query, types=[
    UserType, GameType, GroupType, AssetType, BadgeType, 
    GroupMemberType, GroupRoleType, BadgeStatisticsType, 
    GamePassType, ServerType, PresenceType
])