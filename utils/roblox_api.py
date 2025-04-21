import requests
import logging
import time
import json
import random
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

# Connection settings
CONNECTION_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds

# Rate limiter for Roblox API calls
rate_limiter = RateLimiter(max_calls=60, period=60)  # 60 calls per minute

# Demo mode - For development and demonstration only
DEMO_MODE = False

# Create demo data for Roblox API
with open('./utils/roblox_demo_data.json', 'w') as f:
    json.dump({
        "users": {
            "1234567": {
                "id": 1234567,
                "name": "RobloxDemoUser",
                "displayName": "Demo User",
                "description": "This is a demo user for BloxAPI",
                "created": "2019-08-02T18:45:26.91Z",
                "isBanned": False,
                "externalAppDisplayName": "Demo User",
                "hasVerifiedBadge": True
            },
            "987654321": {
                "id": 987654321,
                "name": "AnotherDemoUser",
                "displayName": "Another Demo",
                "description": "Another demo user for testing",
                "created": "2016-04-14T23:27:18.32Z",
                "isBanned": False,
                "externalAppDisplayName": "Another Demo",
                "hasVerifiedBadge": False
            }
        },
        "user_search": {
            "Roblox": [
                {"id": 1, "name": "Roblox", "displayName": "Roblox", "hasVerifiedBadge": True},
                {"id": 156, "name": "Builderman", "displayName": "Builder Man", "hasVerifiedBadge": True},
                {"id": 20075347, "name": "RobloxDev", "displayName": "Roblox Developer", "hasVerifiedBadge": True},
                {"id": 1567614, "name": "RobloxTester", "displayName": "Tester", "hasVerifiedBadge": False},
                {"id": 34695519, "name": "RobloxFan", "displayName": "Roblox Fan", "hasVerifiedBadge": False}
            ]
        },
        "games": {
            "1234567890": {
                "id": 1234567890,
                "name": "Demo Game",
                "description": "This is a demo game for BloxAPI",
                "creator": {
                    "id": 1234567,
                    "name": "RobloxDemoUser",
                    "type": "User"
                },
                "rootPlace": {
                    "id": 123456789,
                    "name": "Demo Game"
                },
                "created": "2022-10-15T14:30:22.54Z",
                "updated": "2025-04-01T12:15:48.76Z",
                "placeVisits": 5248679,
                "playingCount": 1254,
                "favoriteCount": 124875,
                "universeId": 4567890123,
                "maxPlayers": 50,
                "allowedGearCategories": ["MeleeWeapons", "RangedWeapons", "Navigation"],
                "genre": "Adventure",
                "price": 0,
                "copying": False
            },
            "987654321": {
                "id": 987654321,
                "name": "Another Demo Game",
                "description": "Another demo game for BloxAPI testing",
                "creator": {
                    "id": 987654321,
                    "name": "AnotherDemoUser",
                    "type": "User"
                },
                "rootPlace": {
                    "id": 987654,
                    "name": "Another Demo Game"
                },
                "created": "2023-05-28T09:12:37.81Z",
                "updated": "2025-03-25T19:42:51.38Z",
                "placeVisits": 1389452,
                "playingCount": 847,
                "favoriteCount": 78954,
                "universeId": 9876543210,
                "maxPlayers": 30,
                "allowedGearCategories": [],
                "genre": "All",
                "price": 0,
                "copying": False
            }
        },
        "game_details": {
            "1234567890": {
                "id": 1234567890,
                "name": "Demo Game",
                "description": "This is a demo game for BloxAPI with extended details",
                "creator": {
                    "id": 1234567,
                    "name": "RobloxDemoUser",
                    "type": "User",
                    "hasVerifiedBadge": True
                },
                "rootPlace": {
                    "id": 123456789,
                    "name": "Demo Game",
                    "description": "This is the main place for Demo Game"
                },
                "created": "2022-10-15T14:30:22.54Z",
                "updated": "2025-04-01T12:15:48.76Z",
                "placeVisits": 5248679,
                "playingCount": 1254,
                "favoriteCount": 124875,
                "universeId": 4567890123,
                "maxPlayers": 50,
                "allowedGearCategories": ["MeleeWeapons", "RangedWeapons", "Navigation"],
                "genre": "Adventure",
                "price": 0,
                "copying": False,
                "isForSale": False,
                "studioAccessToApisAllowed": True,
                "createVipServersAllowed": True,
                "universeAvatarType": "MorphToR15",
                "universeScaleType": "Classic",
                "universeAnimationType": "Standard",
                "universeJointPositioningType": "Standard",
                "universeCollisionType": "OuterBox",
                "universeBodyType": "Standard",
                "isArchived": False,
                "isFriendsOnly": False,
                "gameRating": {
                    "rating": 4.8,
                    "ratingCount": 1254
                },
                "badges": [
                    {
                        "id": 12345,
                        "name": "Welcome to Demo Game",
                        "description": "Join the game for the first time",
                        "enabled": True,
                        "iconImageId": 654321,
                        "created": "2022-10-15T14:35:12.34Z",
                        "updated": "2022-10-15T14:35:12.34Z",
                        "statistics": {
                            "awardedCount": 4125789,
                            "winRatePercentage": 89.5
                        }
                    },
                    {
                        "id": 23456,
                        "name": "Master Demo Player",
                        "description": "Complete all levels in Demo Game",
                        "enabled": True,
                        "iconImageId": 765432,
                        "created": "2022-10-15T14:40:25.67Z",
                        "updated": "2023-03-12T10:15:38.92Z",
                        "statistics": {
                            "awardedCount": 254789,
                            "winRatePercentage": 12.8
                        }
                    }
                ]
            },
            "987654321": {
                "id": 987654321,
                "name": "Another Demo Game",
                "description": "Another demo game for BloxAPI testing with extended details",
                "creator": {
                    "id": 987654321,
                    "name": "AnotherDemoUser",
                    "type": "User",
                    "hasVerifiedBadge": False
                },
                "rootPlace": {
                    "id": 987654,
                    "name": "Another Demo Game",
                    "description": "This is the main place for Another Demo Game"
                },
                "created": "2023-05-28T09:12:37.81Z",
                "updated": "2025-03-25T19:42:51.38Z",
                "placeVisits": 1389452,
                "playingCount": 847,
                "favoriteCount": 78954,
                "universeId": 9876543210,
                "maxPlayers": 30,
                "allowedGearCategories": [],
                "genre": "All",
                "price": 0,
                "copying": False,
                "isForSale": False,
                "studioAccessToApisAllowed": True,
                "createVipServersAllowed": True,
                "universeAvatarType": "MorphToR15",
                "universeScaleType": "Classic",
                "universeAnimationType": "Standard",
                "universeJointPositioningType": "Standard",
                "universeCollisionType": "OuterBox",
                "universeBodyType": "Standard",
                "isArchived": False,
                "isFriendsOnly": False,
                "gameRating": {
                    "rating": 4.5,
                    "ratingCount": 789
                },
                "badges": [
                    {
                        "id": 34567,
                        "name": "First Steps",
                        "description": "Complete the tutorial",
                        "enabled": True,
                        "iconImageId": 876543,
                        "created": "2023-05-28T10:32:45.12Z",
                        "updated": "2023-05-28T10:32:45.12Z",
                        "statistics": {
                            "awardedCount": 987543,
                            "winRatePercentage": 78.2
                        }
                    }
                ]
            }
        },
        "friends": {
            "1234567": [
                {
                    "id": 23456789,
                    "name": "DemoFriend1",
                    "displayName": "Demo Friend One",
                    "hasVerifiedBadge": False,
                    "isOnline": True,
                    "friendsCount": 154,
                    "created": "2020-07-15T08:45:12.38Z"
                },
                {
                    "id": 34567890,
                    "name": "DemoFriend2",
                    "displayName": "Demo Friend Two",
                    "hasVerifiedBadge": False,
                    "isOnline": False,
                    "friendsCount": 278,
                    "created": "2019-02-28T12:34:56.78Z"
                },
                {
                    "id": 45678901,
                    "name": "DemoFriend3",
                    "displayName": "Demo Friend Three",
                    "hasVerifiedBadge": True,
                    "isOnline": False,
                    "friendsCount": 457,
                    "created": "2021-04-12T18:22:47.15Z"
                }
            ]
        }
    }, f, indent=2)

# Load demo data
try:
    with open('./utils/roblox_demo_data.json', 'r') as f:
        DEMO_DATA = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error(f"Error loading demo data: {str(e)}")
    DEMO_DATA = {}

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
    if response.status_code >= 200 and response.status_code < 300:
        try:
            json_response = response.json()
            # Check if the response has an errors array (common in Roblox API)
            if 'errors' in json_response and json_response['errors'] and len(json_response['errors']) > 0:
                error = json_response['errors'][0]
                error_code = error.get('code', 0)
                error_message = error.get('message', 'Unknown error in API response')
                logger.error(f"API error in JSON response: {error_message} (Code: {error_code})")
                raise RobloxAPIError(response.status_code, error_message)
            return json_response
        except ValueError:
            logger.error(f"Failed to parse JSON response: {response.text[:200]}")
            raise RobloxAPIError(500, f"Failed to parse response from Roblox API: {response.text[:50]}...")
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        logger.warning(f"Rate limit reached. Retry after {retry_after} seconds")
        raise RobloxAPIError(429, f"Rate limit reached. Try again in {retry_after} seconds")
    elif response.status_code == 404:
        logger.warning(f"Resource not found: {response.url}")
        raise RobloxAPIError(404, f"The requested resource was not found")
    elif response.status_code == 401:
        logger.error("Unauthorized access to Roblox API")
        raise RobloxAPIError(401, "Unauthorized access to Roblox API, authentication required")
    elif response.status_code == 403:
        logger.error("Forbidden access to Roblox API")
        raise RobloxAPIError(403, "Forbidden access to Roblox API, you don't have permission to access this resource")
    else:
        try:
            error_data = response.json()
            error_msg = error_data.get('message', None)
            if not error_msg and 'errors' in error_data and error_data['errors'] and len(error_data['errors']) > 0:
                error_msg = error_data['errors'][0].get('message', 'Unknown error')
            if not error_msg:
                error_msg = f"HTTP Error: {response.status_code}"
        except ValueError:
            error_msg = f"HTTP Error: {response.status_code}, Response: {response.text[:100]}"
        
        logger.error(f"Roblox API error: {error_msg}")
        raise RobloxAPIError(response.status_code, error_msg)

def make_request(url, method='GET', params=None, data=None, headers=None, cookies=None, 
              timeout=CONNECTION_TIMEOUT, retries=MAX_RETRIES, use_demo_data=DEMO_MODE, demo_key=None):
    """
    Make a request to the Roblox API with error handling and retries
    
    Args:
        url (str): URL to request
        method (str, optional): HTTP method. Defaults to 'GET'.
        params (dict, optional): Query parameters. Defaults to None.
        data (dict, optional): Request body for POST/PUT. Defaults to None.
        headers (dict, optional): Request headers. Defaults to None.
        cookies (dict, optional): Request cookies. Defaults to None.
        timeout (int, optional): Request timeout. Defaults to CONNECTION_TIMEOUT.
        retries (int, optional): Number of retries. Defaults to MAX_RETRIES.
        use_demo_data (bool, optional): Use demo data instead of real API. Defaults to DEMO_MODE.
        demo_key (str, optional): Key to access demo data. Defaults to None.
    
    Returns:
        dict: Parsed response from API
    
    Raises:
        RobloxAPIError: If the API request fails
    """
    # Handle demo mode for development/testing without hitting actual API
    if use_demo_data and demo_key is not None:
        # Split the demo key by dots to navigate nested objects
        keys = demo_key.split('.')
        data = DEMO_DATA
        
        for key in keys:
            if key in data:
                data = data[key]
            else:
                logger.warning(f"Demo data key '{demo_key}' not found")
                raise RobloxAPIError(404, f"Demo data for '{demo_key}' not found")
        
        # Add random delay to simulate API response time
        time.sleep(random.uniform(0.1, 0.5))
        return data
    
    # Default headers
    if headers is None:
        headers = {}
    
    # Apply rate limiting
    rate_limiter.wait_if_needed()
    
    # Try the request with retries
    retry_count = 0
    while retry_count <= retries:
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=data if method in ['POST', 'PUT', 'PATCH'] else None,
                headers=headers,
                cookies=cookies,
                timeout=timeout
            )
            
            # Process the response
            return handle_roblox_response(response)
        
        except requests.ConnectionError as e:
            logger.warning(f"Connection error (attempt {retry_count+1}/{retries+1}): {str(e)}")
            if retry_count >= retries:
                logger.error(f"Max retries reached for connection error: {str(e)}")
                raise RobloxAPIError(503, f"Connection error to Roblox API: {str(e)}")
        
        except requests.Timeout as e:
            logger.warning(f"Timeout error (attempt {retry_count+1}/{retries+1}): {str(e)}")
            if retry_count >= retries:
                logger.error(f"Max retries reached for timeout error: {str(e)}")
                raise RobloxAPIError(504, f"Timeout error when connecting to Roblox API: {str(e)}")
        
        except RobloxAPIError as e:
            # Only retry certain status codes
            if e.status_code in [429, 500, 502, 503, 504]:
                logger.warning(f"API error (attempt {retry_count+1}/{retries+1}): {e.message}")
                if retry_count >= retries:
                    logger.error(f"Max retries reached for API error: {e.message}")
                    raise
            else:
                # Don't retry other errors (404, 403, etc)
                raise
        
        # Exponential backoff before retrying
        retry_count += 1
        if retry_count <= retries:
            sleep_time = RETRY_BACKOFF * (2 ** (retry_count - 1)) + random.uniform(0, 1)
            logger.info(f"Retrying in {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
    
    # This should never be reached due to the retry handling above
    raise RobloxAPIError(500, "Failed to get response from Roblox API after retries")


def with_rate_limit(func):
    """
    Decorator to apply rate limiting to API calls
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        rate_limiter.wait_if_needed()
        try:
            result = func(*args, **kwargs)
            # Рассмотрим успешный ответ API
            return result
        except requests.ConnectionError as e:
            logger.error(f"Connection error to Roblox API: {str(e)}")
            raise RobloxAPIError(503, f"Connection error to Roblox API: {str(e)}")
        except requests.Timeout as e:
            logger.error(f"Timeout error when connecting to Roblox API: {str(e)}")
            raise RobloxAPIError(504, f"Timeout error when connecting to Roblox API: {str(e)}")
        except requests.TooManyRedirects as e:
            logger.error(f"Too many redirects when connecting to Roblox API: {str(e)}")
            raise RobloxAPIError(500, f"Too many redirects when connecting to Roblox API: {str(e)}")
        except requests.RequestException as e:
            logger.error(f"Request error to Roblox API: {str(e)}")
            raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error in API call: {str(e)}")
            raise RobloxAPIError(500, f"Unexpected error in API call: {str(e)}")
    return wrapper

# User-related API calls
@with_rate_limit
def get_user_info(user_id):
    """Get information about a Roblox user by ID"""
    user_id = str(user_id)  # Ensure string key for dict lookup
    
    if DEMO_MODE:
        logger.info(f"Using demo data for user info: {user_id}")
        if user_id in DEMO_DATA.get("users", {}):
            return {"data": DEMO_DATA["users"][user_id]}
        else:
            raise RobloxAPIError(404, f"User not found with ID {user_id}")
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{USERS_API_BASE}/users/{user_id}", 
                timeout=CONNECTION_TIMEOUT
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for user info: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rate_limit
def get_users_info(user_ids):
    """Get information about multiple Roblox users by IDs"""
    if DEMO_MODE:
        logger.info(f"Using demo data for multiple users info")
        
        results = []
        for user_id in user_ids:
            user_id_str = str(user_id)
            if user_id_str in DEMO_DATA.get("users", {}):
                results.append(DEMO_DATA["users"][user_id_str])
        
        return {"data": results}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.post(
                f"{USERS_API_BASE}/users", 
                json={"userIds": user_ids},
                timeout=CONNECTION_TIMEOUT
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for multiple users info: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rate_limit
def search_users(keyword, limit=10):
    """Search for users by keyword"""
    if DEMO_MODE:
        logger.info(f"Using demo data for user search: {keyword}")
        
        if keyword in DEMO_DATA.get("user_search", {}):
            users = DEMO_DATA["user_search"][keyword]
            limited_users = users[:min(limit, len(users))]
            return {"data": limited_users}
        else:
            # Return empty result if keyword not found
            return {"data": []}
    
    # Проверка корректности параметров
    if not keyword or len(keyword.strip()) == 0:
        logger.warning("Empty keyword in search_users")
        return {"data": []}
    
    # Убедимся, что параметр limit находится в допустимом диапазоне
    if limit <= 0:
        limit = 10  # используем значение по умолчанию при недопустимом значении
    elif limit > 100:
        limit = 100  # API ограничивает максимальное значение 
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            # Убедимся, что параметр keyword не содержит фигурные скобки или другие недопустимые символы
            sanitized_keyword = keyword.replace("{", "").replace("}", "").replace("?", "").strip()
            
            response = requests.get(
                f"{USERS_API_BASE}/users/search", 
                params={"keyword": sanitized_keyword, "limit": limit},
                timeout=CONNECTION_TIMEOUT
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for user search: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rate_limit
def get_user_by_username(username):
    """Get user ID from username"""
    if DEMO_MODE:
        logger.info(f"Using demo data for username lookup: {username}")
        
        # Look through all demo users to find matching username
        for user_id, user_data in DEMO_DATA.get("users", {}).items():
            if user_data.get("name") == username:
                return {"id": user_data["id"], "name": user_data["name"], "displayName": user_data.get("displayName")}
        
        # Return None if not found
        return None
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.post(
                f"{USERS_API_BASE}/usernames/users", 
                json={"usernames": [username]},
                timeout=CONNECTION_TIMEOUT
            )
            data = handle_roblox_response(response)
            return data["data"][0] if data["data"] else None
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for username lookup: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

# Games-related API calls
@with_rate_limit
def get_game_details(game_id):
    """Get details about a specific game"""
    # Проверяем, что ID является валидным
    try:
        game_id_int = int(game_id)
        game_id = str(game_id_int)  # Ensure string key for dict lookup
        if game_id_int <= 0:
            logger.error(f"Invalid game ID: {game_id}")
            raise RobloxAPIError(400, f"Invalid game ID: {game_id}. Game ID must be a positive integer.")
    except ValueError:
        logger.error(f"Invalid game ID format: {game_id}")
        raise RobloxAPIError(400, f"Invalid game ID format: {game_id}. Game ID must be a positive integer.")
    
    if DEMO_MODE:
        logger.info(f"Using demo data for game details: {game_id}")
        if game_id in DEMO_DATA.get("game_details", {}):
            return {"data": DEMO_DATA["game_details"][game_id]}
        elif game_id in DEMO_DATA.get("games", {}):
            return {"data": DEMO_DATA["games"][game_id]}
        else:
            raise RobloxAPIError(404, f"Game not found with ID {game_id}")
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{GAMES_API_BASE}/games/{game_id}",
                timeout=CONNECTION_TIMEOUT,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "BloxAPI/1.0"
                }
            )
            
            # Проверяем, есть ли у нас 404 (не найдено)
            if response.status_code == 404:
                logger.warning(f"Game not found with ID {game_id}")
                raise RobloxAPIError(404, f"Game not found with ID {game_id}")
                
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for game details: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rate_limit
def get_games_by_user(user_id, limit=50):
    """Get games created by a specific user"""
    if DEMO_MODE:
        logger.info(f"Using demo data for games by user: {user_id}")
        
        user_id_str = str(user_id)
        games = []
        
        # Filter games by creator ID
        for game_id, game_data in DEMO_DATA.get("games", {}).items():
            if game_data.get("creator", {}).get("id") == int(user_id_str):
                games.append(game_data)
        
        return {"data": games[:min(limit, len(games))]}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{GAMES_API_BASE}/users/{user_id}/games", 
                params={"limit": limit},
                timeout=CONNECTION_TIMEOUT
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for games by user: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rate_limit
def get_game_social_links(game_id):
    """Get social media links for a game"""
    if DEMO_MODE:
        logger.info(f"Using demo data for game social links: {game_id}")
        return {"data": [
            {"title": "Discord", "url": "https://discord.gg/demogame", "type": "Discord"},
            {"title": "Twitter", "url": "https://twitter.com/demogame", "type": "Twitter"},
            {"title": "YouTube", "url": "https://youtube.com/c/demogame", "type": "YouTube"}
        ]}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{GAMES_API_BASE}/games/{game_id}/social-links",
                timeout=CONNECTION_TIMEOUT
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for game social links: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rate_limit
def get_game_passes(game_id, limit=50):
    """Get game passes for a specific game"""
    if DEMO_MODE:
        logger.info(f"Using demo data for game passes: {game_id}")
        
        # Generate demo game passes
        game_passes = []
        if str(game_id) in DEMO_DATA.get("games", {}):
            game_name = DEMO_DATA["games"][str(game_id)]["name"]
            
            for i in range(min(limit, 5)):  # Generate up to 5 demo passes
                game_passes.append({
                    "id": 10000 + i + int(game_id) % 10000,
                    "name": f"{game_name} VIP {i+1}",
                    "displayName": f"{game_name} VIP {i+1}",
                    "price": 99 * (i+1),
                    "productId": 20000 + i + int(game_id) % 10000,
                    "iconImageUri": f"https://roblox.com/assets/gamepass-{i+1}.png",
                    "sellerName": DEMO_DATA["games"][str(game_id)]["creator"]["name"]
                })
        
        return {"data": game_passes}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{GAMES_API_BASE}/games/{game_id}/game-passes", 
                params={"limit": limit},
                timeout=CONNECTION_TIMEOUT
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for game passes: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

# Group-related API calls
@with_rate_limit
def get_group_info(group_id):
    """Get information about a specific group"""
    # Проверка корректности ID группы
    try:
        group_id_int = int(group_id)
        if group_id_int <= 0:
            logger.error(f"Invalid group ID: {group_id}")
            raise RobloxAPIError(400, f"Invalid group ID: {group_id}. Group ID must be a positive integer.")
    except ValueError:
        logger.error(f"Invalid group ID format: {group_id}")
        raise RobloxAPIError(400, f"Invalid group ID format: {group_id}. Group ID must be a positive integer.")
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{GROUPS_API_BASE}/groups/{group_id}",
                timeout=CONNECTION_TIMEOUT,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "BloxAPI/1.0"
                }
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for group info: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rate_limit
def get_group_members(group_id, limit=100):
    """Get members of a specific group"""
    # Валидация лимита
    try:
        limit_int = int(limit)
        if limit_int <= 0:
            limit = 100  # используем значение по умолчанию при недопустимом значении
        elif limit_int > 100:
            limit = 100  # Roblox API ограничивает максимальное количество
    except ValueError:
        limit = 100  # при ошибке используем значение по умолчанию
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{GROUPS_API_BASE}/groups/{group_id}/users", 
                params={"limit": limit},
                timeout=CONNECTION_TIMEOUT,
                headers={"Accept": "application/json"}
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for group members: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rate_limit
def get_group_roles(group_id):
    """Get roles in a specific group"""
    # Проверка корректности ID группы
    try:
        group_id_int = int(group_id)
        if group_id_int <= 0:
            logger.error(f"Invalid group ID: {group_id}")
            raise RobloxAPIError(400, f"Invalid group ID: {group_id}. Group ID must be a positive integer.")
    except ValueError:
        logger.error(f"Invalid group ID format: {group_id}")
        raise RobloxAPIError(400, f"Invalid group ID format: {group_id}. Group ID must be a positive integer.")
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{GROUPS_API_BASE}/groups/{group_id}/roles",
                timeout=CONNECTION_TIMEOUT,
                headers={"Accept": "application/json"}
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for group roles: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rate_limit
def get_user_groups(user_id):
    """Get groups that a user is a member of"""
    # Проверка корректности ID пользователя
    try:
        user_id_int = int(user_id)
        if user_id_int <= 0:
            logger.error(f"Invalid user ID: {user_id}")
            raise RobloxAPIError(400, f"Invalid user ID: {user_id}. User ID must be a positive integer.")
    except ValueError:
        logger.error(f"Invalid user ID format: {user_id}")
        raise RobloxAPIError(400, f"Invalid user ID format: {user_id}. User ID must be a positive integer.")
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{GROUPS_API_BASE}/users/{user_id}/groups",
                timeout=CONNECTION_TIMEOUT,
                headers={"Accept": "application/json"}
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for user groups: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

# Friends-related API calls
@with_rate_limit
def get_user_friends(user_id):
    """Get a user's friends"""
    user_id = str(user_id)  # Ensure string key for dict lookup
    
    if DEMO_MODE:
        logger.info(f"Using demo data for user friends: {user_id}")
        
        if user_id in DEMO_DATA.get("friends", {}):
            return {"data": DEMO_DATA["friends"][user_id]}
        else:
            # Return empty list if user not in demo data
            return {"data": []}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{FRIENDS_API_BASE}/users/{user_id}/friends",
                timeout=CONNECTION_TIMEOUT
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for user friends: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rate_limit
def get_friend_requests(user_id):
    """Get a user's friend requests"""
    if DEMO_MODE:
        logger.info(f"Using demo data for friend requests: {user_id}")
        
        # Generate some demo friend requests
        friend_requests = []
        for i in range(3):  # Generate 3 demo friend requests
            friend_requests.append({
                "id": 100000 + i,
                "name": f"RequestUser{i+1}",
                "displayName": f"Request User {i+1}",
                "hasVerifiedBadge": False,
                "created": "2025-04-15T10:30:00Z"
            })
        
        return {"data": friend_requests}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{FRIENDS_API_BASE}/users/{user_id}/friends/requests",
                timeout=CONNECTION_TIMEOUT
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for friend requests: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rate_limit
def get_friends_count(user_id):
    """Get count of user's friends"""
    user_id = str(user_id)  # Ensure string key for dict lookup
    
    if DEMO_MODE:
        logger.info(f"Using demo data for friends count: {user_id}")
        
        if user_id in DEMO_DATA.get("friends", {}):
            count = len(DEMO_DATA["friends"][user_id])
            return {"count": count}
        else:
            return {"count": 0}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{FRIENDS_API_BASE}/users/{user_id}/friends/count",
                timeout=CONNECTION_TIMEOUT
            )
            return handle_roblox_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for friends count: {str(e)}")
                raise RobloxAPIError(500, f"Error connecting to Roblox API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roblox API call in {wait_time} seconds...")
            time.sleep(wait_time)

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
