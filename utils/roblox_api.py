import requests
import logging
import time
from functools import wraps
from .rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

# Base Roblox API URLs
ROBLOX_API_BASE = "https://api.roblox.com"
USERS_API_BASE = "https://users.roblox.com/v1"
ECONOMY_API_BASE = "https://economy.roblox.com/v1"
ECONOMY_API_BASE_V2 = "https://economy.roblox.com/v2"
GAMES_API_BASE = "https://games.roblox.com/v1"
GAMES_API_BASE_V2 = "https://games.roblox.com/v2"
GROUPS_API_BASE = "https://groups.roblox.com/v1"
GROUPS_API_BASE_V2 = "https://groups.roblox.com/v2"
CATALOG_API_BASE = "https://catalog.roblox.com/v1"
CATALOG_API_BASE_V2 = "https://catalog.roblox.com/v2" 
AVATAR_API_BASE = "https://avatar.roblox.com/v1"
AVATAR_API_BASE_V2 = "https://avatar.roblox.com/v2"
INVENTORY_API_BASE = "https://inventory.roblox.com/v1"
INVENTORY_API_BASE_V2 = "https://inventory.roblox.com/v2"
FRIENDS_API_BASE = "https://friends.roblox.com/v1"
CHAT_API_BASE = "https://chat.roblox.com/v2"
BADGES_API_BASE = "https://badges.roblox.com/v1"
DEVELOP_API_BASE = "https://develop.roblox.com/v1"
DEVELOP_API_BASE_V2 = "https://develop.roblox.com/v2"
PREMIUMFEATURES_API_BASE = "https://premiumfeatures.roblox.com/v1"
ACCOUNTSETTINGS_API_BASE = "https://accountsettings.roblox.com/v1"
ACCOUNTINFORMATION_API_BASE = "https://accountinformation.roblox.com/v1"
PRESENCE_API_BASE = "https://presence.roblox.com/v1"
USERMODERATION_API_BASE = "https://usermoderation.roblox.com/v1"
NOTIFICATIONS_API_BASE = "https://notifications.roblox.com/v1"
TRANSLATIONS_API_BASE = "https://translations.roblox.com/v1"
THUMBNAILS_API_BASE = "https://thumbnails.roblox.com/v1"
ADCONFIGURATION_API_BASE = "https://adconfiguration.roblox.com/v1"
CLIENTSETTINGS_API_BASE = "https://clientsettings.roblox.com/v1"
CONTACTS_API_BASE = "https://contacts.roblox.com/v1"
PRIVATE_MESSAGES_API_BASE = "https://privatemessages.roblox.com/v1"

# Rate limiter for Roblox API calls
rate_limiter = RateLimiter(max_calls=60, period=60)  # 60 calls per minute

# Custom exception for Roblox API errors
class RobloxAPIError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Roblox API Error ({status_code}): {message}")

def handle_roblox_response(response):
    """
    Process the Roblox API response and handle errors
    """
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            logger.error("Failed to parse JSON response")
            raise RobloxAPIError(500, "Failed to parse response from Roblox API")
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        logger.warning(f"Rate limit reached. Retry after {retry_after} seconds")
        raise RobloxAPIError(429, f"Rate limit reached. Try again in {retry_after} seconds")
    else:
        try:
            error_data = response.json()
            error_msg = error_data.get('message', 'Unknown error')
        except ValueError:
            error_msg = f"HTTP Error: {response.status_code}"
        
        logger.error(f"Roblox API error: {error_msg}")
        raise RobloxAPIError(response.status_code, error_msg)

def with_rate_limit(func):
    """
    Decorator to apply rate limiting to API calls
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        rate_limiter.wait_if_needed()
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
    return wrapper

# User-related API calls
@with_rate_limit
def get_user_info(user_id):
    """Get information about a Roblox user by ID"""
    response = requests.get(f"{USERS_API_BASE}/users/{user_id}")
    return handle_roblox_response(response)

@with_rate_limit
def get_users_info(user_ids):
    """Get information about multiple Roblox users by IDs"""
    response = requests.post(
        f"{USERS_API_BASE}/users", 
        json={"userIds": user_ids}
    )
    return handle_roblox_response(response)

@with_rate_limit
def search_users(keyword, limit=10):
    """Search for users by keyword"""
    response = requests.get(
        f"{USERS_API_BASE}/users/search", 
        params={"keyword": keyword, "limit": limit}
    )
    return handle_roblox_response(response)

@with_rate_limit
def get_user_by_username(username):
    """Get user ID from username"""
    response = requests.post(
        f"{USERS_API_BASE}/usernames/users", 
        json={"usernames": [username]}
    )
    data = handle_roblox_response(response)
    return data["data"][0] if data["data"] else None

# Games-related API calls
@with_rate_limit
def get_game_details(game_id):
    """Get details about a specific game"""
    response = requests.get(f"{GAMES_API_BASE}/games/{game_id}")
    return handle_roblox_response(response)

@with_rate_limit
def get_games_by_user(user_id, limit=50):
    """Get games created by a specific user"""
    response = requests.get(
        f"{GAMES_API_BASE}/users/{user_id}/games", 
        params={"limit": limit}
    )
    return handle_roblox_response(response)

@with_rate_limit
def get_game_social_links(game_id):
    """Get social media links for a game"""
    response = requests.get(f"{GAMES_API_BASE}/games/{game_id}/social-links")
    return handle_roblox_response(response)

@with_rate_limit
def get_game_passes(game_id, limit=50):
    """Get game passes for a specific game"""
    response = requests.get(
        f"{GAMES_API_BASE}/games/{game_id}/game-passes", 
        params={"limit": limit}
    )
    return handle_roblox_response(response)

# Group-related API calls
@with_rate_limit
def get_group_info(group_id):
    """Get information about a specific group"""
    response = requests.get(f"{GROUPS_API_BASE}/groups/{group_id}")
    return handle_roblox_response(response)

@with_rate_limit
def get_group_members(group_id, limit=100):
    """Get members of a specific group"""
    response = requests.get(
        f"{GROUPS_API_BASE}/groups/{group_id}/users", 
        params={"limit": limit}
    )
    return handle_roblox_response(response)

@with_rate_limit
def get_group_roles(group_id):
    """Get roles in a specific group"""
    response = requests.get(f"{GROUPS_API_BASE}/groups/{group_id}/roles")
    return handle_roblox_response(response)

@with_rate_limit
def get_user_groups(user_id):
    """Get groups that a user is a member of"""
    response = requests.get(f"{GROUPS_API_BASE}/users/{user_id}/groups")
    return handle_roblox_response(response)

# Friends-related API calls
@with_rate_limit
def get_user_friends(user_id):
    """Get a user's friends"""
    response = requests.get(f"{FRIENDS_API_BASE}/users/{user_id}/friends")
    return handle_roblox_response(response)

@with_rate_limit
def get_friend_requests(user_id):
    """Get a user's friend requests"""
    response = requests.get(f"{FRIENDS_API_BASE}/users/{user_id}/friends/requests")
    return handle_roblox_response(response)

@with_rate_limit
def get_friends_count(user_id):
    """Get count of user's friends"""
    response = requests.get(f"{FRIENDS_API_BASE}/users/{user_id}/friends/count")
    return handle_roblox_response(response)

# Asset-related API calls
@with_rate_limit
def get_asset_info(asset_id):
    """Get information about a specific asset"""
    response = requests.get(f"{CATALOG_API_BASE}/assets/{asset_id}/details")
    return handle_roblox_response(response)

@with_rate_limit
def get_asset_bundles(asset_id, limit=10):
    """Get bundles containing a specific asset"""
    response = requests.get(
        f"{CATALOG_API_BASE}/assets/{asset_id}/bundles", 
        params={"limit": limit}
    )
    return handle_roblox_response(response)

# Catalog-related API calls
@with_rate_limit
def search_catalog(keyword, category=None, subcategory=None, limit=10):
    """Search the catalog for items"""
    params = {
        "keyword": keyword,
        "limit": limit
    }
    if category:
        params["category"] = category
    if subcategory:
        params["subcategory"] = subcategory
        
    response = requests.get(
        f"{CATALOG_API_BASE}/search/items", 
        params=params
    )
    return handle_roblox_response(response)

@with_rate_limit
def get_catalog_categories():
    """Get all catalog categories"""
    response = requests.get(f"{CATALOG_API_BASE}/categories")
    return handle_roblox_response(response)

@with_rate_limit
def get_bundle_details(bundle_id):
    """Get detailed information about a bundle by ID"""
    response = requests.get(f"{CATALOG_API_BASE}/bundles/{bundle_id}/details")
    return handle_roblox_response(response)

@with_rate_limit
def search_bundles(keyword, limit=10):
    """Search for bundles by keyword"""
    params = {
        "keyword": keyword,
        "limit": limit
    }
    response = requests.get(f"{CATALOG_API_BASE}/search/bundles", params=params)
    return handle_roblox_response(response)

# Avatar API calls
@with_rate_limit
def get_user_avatar(user_id):
    """Get a user's avatar"""
    response = requests.get(f"{AVATAR_API_BASE}/users/{user_id}/avatar")
    return handle_roblox_response(response)

@with_rate_limit
def get_user_avatar_meta(user_id):
    """Get metadata about a user's avatar"""
    response = requests.get(f"{AVATAR_API_BASE}/users/{user_id}/avatar/meta")
    return handle_roblox_response(response)

@with_rate_limit
def get_user_outfits(user_id, limit=25):
    """Get a user's outfits"""
    params = {"limit": limit}
    response = requests.get(f"{AVATAR_API_BASE}/users/{user_id}/outfits", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_outfit_details(outfit_id):
    """Get details about a specific outfit"""
    response = requests.get(f"{AVATAR_API_BASE}/outfits/{outfit_id}")
    return handle_roblox_response(response)

# Inventory API calls
@with_rate_limit
def get_user_inventory(user_id, asset_type, limit=100):
    """Get a user's inventory items of a specific asset type"""
    params = {"limit": limit}
    response = requests.get(f"{INVENTORY_API_BASE}/users/{user_id}/items/{asset_type}", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_user_collectibles(user_id, limit=100):
    """Get a user's collectible items"""
    params = {"limit": limit}
    response = requests.get(f"{INVENTORY_API_BASE}/users/{user_id}/assets/collectibles", params=params)
    return handle_roblox_response(response)

# Economy API calls
@with_rate_limit
def get_asset_resellers(asset_id, limit=10):
    """Get resellers of a limited asset"""
    params = {"limit": limit}
    response = requests.get(f"{ECONOMY_API_BASE}/assets/{asset_id}/resellers", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_asset_resale_data(asset_id):
    """Get resale data for a limited asset"""
    response = requests.get(f"{ECONOMY_API_BASE}/assets/{asset_id}/resale-data")
    return handle_roblox_response(response)

@with_rate_limit
def get_currency_exchange_rate():
    """Get the currency exchange rate for Robux to USD"""
    response = requests.get(f"{ECONOMY_API_BASE}/currency/exchange-rate")
    return handle_roblox_response(response)

@with_rate_limit
def get_group_revenue(group_id):
    """Get a group's revenue summary"""
    response = requests.get(f"{ECONOMY_API_BASE_V2}/groups/{group_id}/revenue/summary")
    return handle_roblox_response(response)

@with_rate_limit
def get_user_transactions(user_id, transaction_type, limit=100):
    """Get a user's transactions of a specific type"""
    params = {"limit": limit}
    response = requests.get(f"{ECONOMY_API_BASE}/users/{user_id}/transactions/{transaction_type}", params=params)
    return handle_roblox_response(response)

# Game Analytics API calls
@with_rate_limit
def get_game_analytics(universe_id, metric_type, time_frame):
    """Get analytics for a game"""
    params = {"timeFrame": time_frame}
    response = requests.get(f"{DEVELOP_API_BASE_V2}/universes/{universe_id}/analytics/game-metrics/{metric_type}", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_game_playtime(universe_id, start_time, end_time):
    """Get playtime analytics for a game"""
    params = {"startTime": start_time, "endTime": end_time}
    response = requests.get(f"{DEVELOP_API_BASE_V2}/universes/{universe_id}/analytics/playtime", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_game_revenue(universe_id, start_time, end_time):
    """Get revenue analytics for a game"""
    params = {"startTime": start_time, "endTime": end_time}
    response = requests.get(f"{DEVELOP_API_BASE_V2}/universes/{universe_id}/analytics/revenue", params=params)
    return handle_roblox_response(response)

# Badge API calls
@with_rate_limit
def get_game_badges(universe_id, limit=50):
    """Get badges for a game"""
    params = {"limit": limit}
    response = requests.get(f"{BADGES_API_BASE}/universes/{universe_id}/badges", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_badge_info(badge_id):
    """Get information about a specific badge"""
    response = requests.get(f"{BADGES_API_BASE}/badges/{badge_id}")
    return handle_roblox_response(response)

@with_rate_limit
def get_badge_awarded_dates(badge_id, user_id):
    """Get date when a badge was awarded to a user"""
    response = requests.get(f"{BADGES_API_BASE}/badges/{badge_id}/awarded-dates?userId={user_id}")
    return handle_roblox_response(response)

# Chat API calls
@with_rate_limit
def get_chat_conversations(limit=100):
    """Get user's chat conversations"""
    params = {"limit": limit}
    response = requests.get(f"{CHAT_API_BASE}/get-conversations", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_chat_messages(conversation_id, limit=100):
    """Get messages from a chat conversation"""
    params = {"limit": limit}
    response = requests.get(f"{CHAT_API_BASE}/get-messages?conversationId={conversation_id}", params=params)
    return handle_roblox_response(response)

# User Presence API calls
@with_rate_limit
def get_user_presence(user_ids):
    """Get presence information for users"""
    payload = {"userIds": user_ids}
    response = requests.post(f"{PRESENCE_API_BASE}/presence/users", json=payload)
    return handle_roblox_response(response)

@with_rate_limit
def get_last_online(user_ids):
    """Get last online time for users"""
    payload = {"userIds": user_ids}
    response = requests.post(f"{PRESENCE_API_BASE}/presence/last-online", json=payload)
    return handle_roblox_response(response)

# Notifications API calls
@with_rate_limit
def get_notifications():
    """Get user's notifications"""
    response = requests.get(f"{NOTIFICATIONS_API_BASE}/notifications")
    return handle_roblox_response(response)

@with_rate_limit
def get_notification_counts():
    """Get counts of user's notifications by type"""
    response = requests.get(f"{NOTIFICATIONS_API_BASE}/notification-counts")
    return handle_roblox_response(response)

# Thumbnails API calls
@with_rate_limit
def get_user_thumbnails(user_ids, size="420x420", format="Png", is_circular=False):
    """Get thumbnails for users"""
    params = {
        "userIds": ",".join(map(str, user_ids)),
        "size": size,
        "format": format,
        "isCircular": str(is_circular).lower()
    }
    response = requests.get(f"{THUMBNAILS_API_BASE}/users/avatar-headshots", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_asset_thumbnails(asset_ids, size="420x420", format="Png"):
    """Get thumbnails for assets"""
    params = {
        "assetIds": ",".join(map(str, asset_ids)),
        "size": size,
        "format": format
    }
    response = requests.get(f"{THUMBNAILS_API_BASE}/assets", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_game_thumbnails(universe_ids, size="768x432", format="Png"):
    """Get thumbnails for games"""
    params = {
        "universeIds": ",".join(map(str, universe_ids)),
        "size": size,
        "format": format
    }
    response = requests.get(f"{THUMBNAILS_API_BASE}/games/icons", params=params)
    return handle_roblox_response(response)

# Game Universe API calls
@with_rate_limit
def get_universe_info(universe_id):
    """Get information about a game universe"""
    response = requests.get(f"{GAMES_API_BASE_V2}/universes/{universe_id}")
    return handle_roblox_response(response)

@with_rate_limit
def get_game_servers(universe_id, limit=100):
    """Get active servers for a game"""
    params = {"limit": limit}
    response = requests.get(f"{GAMES_API_BASE}/games/{universe_id}/servers/Public", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_game_version_history(universe_id, limit=50):
    """Get version history for a game"""
    params = {"limit": limit}
    response = requests.get(f"{DEVELOP_API_BASE_V2}/universes/{universe_id}/versions", params=params)
    return handle_roblox_response(response)

# Group-related API calls (additional)
@with_rate_limit
def get_group_payouts(group_id):
    """Get configured group payouts"""
    response = requests.get(f"{GROUPS_API_BASE_V2}/groups/{group_id}/payouts")
    return handle_roblox_response(response)

@with_rate_limit
def get_group_audit_log(group_id, limit=50):
    """Get group audit log entries"""
    params = {"limit": limit}
    response = requests.get(f"{GROUPS_API_BASE_V2}/groups/{group_id}/audit-log", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_group_socials(group_id):
    """Get group social media links"""
    response = requests.get(f"{GROUPS_API_BASE}/groups/{group_id}/social-links")
    return handle_roblox_response(response)

# User-related API calls (additional)
@with_rate_limit
def get_user_status(user_id):
    """Get a user's status"""
    response = requests.get(f"{USERS_API_BASE}/users/{user_id}/status")
    return handle_roblox_response(response)

@with_rate_limit
def get_user_followers(user_id, limit=50):
    """Get users who are following a user"""
    params = {"limit": limit}
    response = requests.get(f"{FRIENDS_API_BASE}/users/{user_id}/followers", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_user_followings(user_id, limit=50):
    """Get users that a user is following"""
    params = {"limit": limit}
    response = requests.get(f"{FRIENDS_API_BASE}/users/{user_id}/followings", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_user_badges(user_id, limit=50):
    """Get badges owned by a user"""
    params = {"limit": limit}
    response = requests.get(f"{BADGES_API_BASE}/users/{user_id}/badges", params=params)
    return handle_roblox_response(response)

@with_rate_limit
def get_user_experience(user_id, limit=50):
    """Get user experience (game history)"""
    params = {"limit": limit}
    response = requests.get(f"{GAMES_API_BASE}/users/{user_id}/recently-played", params=params)
    return handle_roblox_response(response)

# Game development API calls
@with_rate_limit
def get_game_team_create_members(universe_id):
    """Get team create members for a game"""
    response = requests.get(f"{DEVELOP_API_BASE_V2}/universes/{universe_id}/team-create/members")
    return handle_roblox_response(response)

@with_rate_limit
def get_game_packages(universe_id):
    """Get packages used in a game"""
    response = requests.get(f"{DEVELOP_API_BASE_V2}/universes/{universe_id}/packages")
    return handle_roblox_response(response)

@with_rate_limit
def get_game_current_version(universe_id):
    """Get current version information for a game"""
    response = requests.get(f"{DEVELOP_API_BASE_V2}/universes/{universe_id}/version")
    return handle_roblox_response(response)
