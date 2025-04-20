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
GAMES_API_BASE = "https://games.roblox.com/v1"
GROUPS_API_BASE = "https://groups.roblox.com/v1"
CATALOG_API_BASE = "https://catalog.roblox.com/v1"
AVATAR_API_BASE = "https://avatar.roblox.com/v1"
INVENTORY_API_BASE = "https://inventory.roblox.com/v1"
FRIENDS_API_BASE = "https://friends.roblox.com/v1"

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
