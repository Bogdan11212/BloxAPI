import requests
import logging
import time
import json
import random
from functools import wraps
from .rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

# Base URLs for external APIs
ROLIMON_API_BASE = "https://api.rolimons.com/v1"
RBLX_TRADE_API_BASE = "https://api.rblx.trade/v1"
ROLIVERSE_API_BASE = "https://api.roliverse.com/v1"
RBLX_VALUES_API_BASE = "https://api.rblxvalues.com/v1"

# Connection settings
CONNECTION_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds

# Rate limiters for external APIs
rolimon_rate_limiter = RateLimiter(max_calls=30, period=60)  # 30 calls per minute
rblx_trade_rate_limiter = RateLimiter(max_calls=30, period=60)  # 30 calls per minute
roliverse_rate_limiter = RateLimiter(max_calls=30, period=60)  # 30 calls per minute
rblx_values_rate_limiter = RateLimiter(max_calls=30, period=60)  # 30 calls per minute

# Demo mode - For development and demonstration only
DEMO_MODE = True

# Demo data
with open('./utils/demo_data.json', 'w') as f:
    json.dump({
        "rolimon": {
            "item_details": {
                "1365767": {
                    "name": "Dominus Frigidus",
                    "acronym": "DF",
                    "rap": 40230000,
                    "value": 43450000,
                    "demand": 9,
                    "trend": "rising",
                    "projected": False,
                    "rare": True,
                    "hyped": False,
                    "volatility": 0.12,
                    "updated_at": "2025-04-20T18:35:04Z"
                },
                "1028606": {
                    "name": "Classic ROBLOX Fedora",
                    "acronym": "CRF",
                    "rap": 14782400,
                    "value": 15500000,
                    "demand": 8,
                    "trend": "stable",
                    "projected": False,
                    "rare": True,
                    "hyped": False,
                    "volatility": 0.05,
                    "updated_at": "2025-04-20T19:12:22Z"
                },
                "617605": {
                    "name": "Clockwork's Headphones",
                    "acronym": "CW",
                    "rap": 10600000,
                    "value": 11200000,
                    "demand": 7,
                    "trend": "stable",
                    "projected": False,
                    "rare": False,
                    "hyped": False,
                    "volatility": 0.08,
                    "updated_at": "2025-04-20T17:45:30Z"
                }
            },
            "player_rap": {
                "1234567": {"rap": 152450000, "updated_at": "2025-04-20T20:10:12Z"}
            }
        },
        "rblx_trade": {
            "trade_calculator": {
                "offer_value": 43450000 + 31000000,
                "request_value": 15500000 + 11200000,
                "value_difference": 47750000,
                "is_profitable": True,
                "is_fair": False,
                "recommendation": "Decline - Items you're offering are worth significantly more",
                "timestamp": "2025-04-20T20:15:45Z"
            },
            "player_reputation": {
                "1234567": {
                    "score": 8.5,
                    "total_trades": 138,
                    "completed_trades": 124,
                    "cancelled_trades": 14,
                    "positive_reviews": 112,
                    "negative_reviews": 9,
                    "neutral_reviews": 3,
                    "trusted_trader": True,
                    "updated_at": "2025-04-19T12:40:22Z"
                }
            }
        },
        "roliverse": {
            "market_trends": {
                "period": "week",
                "type": "limited",
                "rising_items": [
                    {"id": 1365767, "name": "Dominus Frigidus", "value": 43450000, "percentage_change": 8.2},
                    {"id": 1031429, "name": "Dominus Aureus", "value": 39500000, "percentage_change": 6.8},
                    {"id": 21070012, "name": "Dominus Venari", "value": 33780000, "percentage_change": 5.4},
                    {"id": 493933400, "name": "Ice Valk", "value": 28450000, "percentage_change": 4.9},
                    {"id": 1335900, "name": "Sparkle Time Fedora", "value": 25900000, "percentage_change": 4.7}
                ],
                "falling_items": [
                    {"id": 585851867, "name": "America's Fedora", "value": 15500000, "percentage_change": -3.8},
                    {"id": 74891470, "name": "Dominus Rex", "value": 75000000, "percentage_change": -2.9},
                    {"id": 658831150, "name": "Green Sparkle Time Fedora", "value": 18750000, "percentage_change": -2.6},
                    {"id": 11748356, "name": "Clockwork's Shades", "value": 8900000, "percentage_change": -2.1},
                    {"id": 9549352, "name": "Memorious", "value": 3400000, "percentage_change": -1.8}
                ],
                "overall_market_change": 1.2,
                "total_items_analyzed": 342,
                "timestamp": "2025-04-20T00:00:00Z"
            },
            "demand_indexes": {
                "1365767": {
                    "demand_index": 9.2,
                    "demand_category": "Very High",
                    "trading_volume": 4.3,
                    "stability_score": 8.5,
                    "updated_at": "2025-04-20T15:30:00Z"
                }
            }
        },
        "rblx_values": {
            "rising_items": {
                "items": [
                    {"id": 1365767, "name": "Dominus Frigidus", "value_change": 1200000, "time_period": "week"},
                    {"id": 1031429, "name": "Dominus Aureus", "value_change": 950000, "time_period": "week"},
                    {"id": 21070012, "name": "Dominus Venari", "value_change": 780000, "time_period": "week"},
                    {"id": 493933400, "name": "Ice Valk", "value_change": 650000, "time_period": "week"},
                    {"id": 1335900, "name": "Sparkle Time Fedora", "value_change": 600000, "time_period": "week"},
                    {"id": 31101391, "name": "Dominus Empyreus", "value_change": 580000, "time_period": "week"},
                    {"id": 1285307, "name": "Dominus Messor", "value_change": 520000, "time_period": "week"},
                    {"id": 21433562, "name": "Blue Sparkle Time Fedora", "value_change": 490000, "time_period": "week"},
                    {"id": 250395631, "name": "Purple Sparkle Time Fedora", "value_change": 450000, "time_period": "week"},
                    {"id": 1245543, "name": "Dominus Infernus", "value_change": 430000, "time_period": "week"}
                ],
                "updated_at": "2025-04-20T00:00:00Z"
            },
            "item_projected": {
                "1365767": {
                    "is_projected": False
                },
                "1028606": {
                    "is_projected": False
                },
                "617605": {
                    "is_projected": False
                }
            }
        }
    }, f, indent=2)

# Custom exceptions for external API errors
class RolimonAPIError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Rolimon API Error ({status_code}): {message}")

class RblxTradeAPIError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Rblx Trade API Error ({status_code}): {message}")

class RoliverseAPIError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Roliverse API Error ({status_code}): {message}")

class RblxValuesAPIError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Rblx Values API Error ({status_code}): {message}")

# Handler functions for API responses
def handle_rolimon_response(response):
    """
    Process the Rolimon API response and handle errors
    """
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            logger.error("Failed to parse JSON response from Rolimon API")
            raise RolimonAPIError(500, "Failed to parse response from Rolimon API")
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        logger.warning(f"Rate limit reached for Rolimon API. Retry after {retry_after} seconds")
        raise RolimonAPIError(429, f"Rate limit reached. Try again in {retry_after} seconds")
    else:
        try:
            error_data = response.json()
            error_msg = error_data.get('message', 'Unknown error')
        except ValueError:
            error_msg = f"HTTP Error: {response.status_code}"
        
        logger.error(f"Rolimon API error: {error_msg}")
        raise RolimonAPIError(response.status_code, error_msg)

def handle_rblx_trade_response(response):
    """
    Process the Rblx Trade API response and handle errors
    """
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            logger.error("Failed to parse JSON response from Rblx Trade API")
            raise RblxTradeAPIError(500, "Failed to parse response from Rblx Trade API")
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        logger.warning(f"Rate limit reached for Rblx Trade API. Retry after {retry_after} seconds")
        raise RblxTradeAPIError(429, f"Rate limit reached. Try again in {retry_after} seconds")
    else:
        try:
            error_data = response.json()
            error_msg = error_data.get('message', 'Unknown error')
        except ValueError:
            error_msg = f"HTTP Error: {response.status_code}"
        
        logger.error(f"Rblx Trade API error: {error_msg}")
        raise RblxTradeAPIError(response.status_code, error_msg)

def handle_roliverse_response(response):
    """
    Process the Roliverse API response and handle errors
    """
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            logger.error("Failed to parse JSON response from Roliverse API")
            raise RoliverseAPIError(500, "Failed to parse response from Roliverse API")
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        logger.warning(f"Rate limit reached for Roliverse API. Retry after {retry_after} seconds")
        raise RoliverseAPIError(429, f"Rate limit reached. Try again in {retry_after} seconds")
    else:
        try:
            error_data = response.json()
            error_msg = error_data.get('message', 'Unknown error')
        except ValueError:
            error_msg = f"HTTP Error: {response.status_code}"
        
        logger.error(f"Roliverse API error: {error_msg}")
        raise RoliverseAPIError(response.status_code, error_msg)

def handle_rblx_values_response(response):
    """
    Process the Rblx Values API response and handle errors
    """
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            logger.error("Failed to parse JSON response from Rblx Values API")
            raise RblxValuesAPIError(500, "Failed to parse response from Rblx Values API")
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        logger.warning(f"Rate limit reached for Rblx Values API. Retry after {retry_after} seconds")
        raise RblxValuesAPIError(429, f"Rate limit reached. Try again in {retry_after} seconds")
    else:
        try:
            error_data = response.json()
            error_msg = error_data.get('message', 'Unknown error')
        except ValueError:
            error_msg = f"HTTP Error: {response.status_code}"
        
        logger.error(f"Rblx Values API error: {error_msg}")
        raise RblxValuesAPIError(response.status_code, error_msg)

# Decorators for rate limiting
def with_rolimon_rate_limit(func):
    """
    Decorator to apply rate limiting to Rolimon API calls
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        rolimon_rate_limiter.wait_if_needed()
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            logger.error(f"Request error for Rolimon API: {str(e)}")
            raise RolimonAPIError(500, f"Error connecting to Rolimon API: {str(e)}")
    return wrapper

def with_rblx_trade_rate_limit(func):
    """
    Decorator to apply rate limiting to Rblx Trade API calls
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        rblx_trade_rate_limiter.wait_if_needed()
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            logger.error(f"Request error for Rblx Trade API: {str(e)}")
            raise RblxTradeAPIError(500, f"Error connecting to Rblx Trade API: {str(e)}")
    return wrapper

def with_roliverse_rate_limit(func):
    """
    Decorator to apply rate limiting to Roliverse API calls
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        roliverse_rate_limiter.wait_if_needed()
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            logger.error(f"Request error for Roliverse API: {str(e)}")
            raise RoliverseAPIError(500, f"Error connecting to Roliverse API: {str(e)}")
    return wrapper

def with_rblx_values_rate_limit(func):
    """
    Decorator to apply rate limiting to Rblx Values API calls
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        rblx_values_rate_limiter.wait_if_needed()
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            logger.error(f"Request error for Rblx Values API: {str(e)}")
            raise RblxValuesAPIError(500, f"Error connecting to Rblx Values API: {str(e)}")
    return wrapper

# Load demo data
try:
    with open('./utils/demo_data.json', 'r') as f:
        DEMO_DATA = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error(f"Error loading demo data: {str(e)}")
    DEMO_DATA = {}

# =================== Rolimon API Functions ===================

@with_rolimon_rate_limit
def get_item_details(item_id):
    """Get details for a specific item from Rolimon's"""
    item_id = str(item_id)  # Ensure string key for dict lookup
    
    if DEMO_MODE:
        logger.info(f"Using demo data for Rolimon's item details: {item_id}")
        if item_id in DEMO_DATA.get("rolimon", {}).get("item_details", {}):
            return {"success": True, "data": DEMO_DATA["rolimon"]["item_details"][item_id]}
        else:
            raise RolimonAPIError(404, f"Item not found with ID {item_id}")
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{ROLIMON_API_BASE}/items/{item_id}", 
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rolimon_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for Rolimon's item details: {str(e)}")
                raise RolimonAPIError(500, f"Error connecting to Rolimon API: {str(e)}")
            
            # Exponential backoff
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rolimon API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rolimon_rate_limit
def get_item_values(item_ids):
    """Get values for multiple items from Rolimon's"""
    if DEMO_MODE:
        logger.info("Using demo data for Rolimon's item values")
        
        result = {}
        for item_id in item_ids:
            item_id_str = str(item_id)
            if item_id_str in DEMO_DATA.get("rolimon", {}).get("item_details", {}):
                item_data = DEMO_DATA["rolimon"]["item_details"][item_id_str]
                result[item_id_str] = {
                    "name": item_data["name"],
                    "value": item_data["value"],
                    "rap": item_data["rap"],
                    "trend": item_data["trend"]
                }
        
        return {"success": True, "data": {"items": result}}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.post(
                f"{ROLIMON_API_BASE}/items/values", 
                json={"ids": item_ids},
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rolimon_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for Rolimon's item values: {str(e)}")
                raise RolimonAPIError(500, f"Error connecting to Rolimon API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rolimon API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rolimon_rate_limit
def get_item_price_history(item_id, period=None):
    """Get price history for an item from Rolimon's"""
    if DEMO_MODE:
        logger.info(f"Using demo data for Rolimon's price history: {item_id}")
        
        # Generate some demo price history data
        end_date = time.time()
        days = 7
        if period == "day":
            days = 1
        elif period == "month":
            days = 30
        elif period == "year":
            days = 365
            
        item_id_str = str(item_id)
        if item_id_str in DEMO_DATA.get("rolimon", {}).get("item_details", {}):
            item_data = DEMO_DATA["rolimon"]["item_details"][item_id_str]
            current_value = item_data["value"]
            
            # Generate price points with some randomness
            history = []
            points_count = days * 24  # Hourly data points
            
            for i in range(points_count):
                time_point = end_date - ((points_count - i) * 3600)  # Hourly intervals
                # Add randomness: ±2% fluctuation from current value
                value_point = int(current_value * (1 + (random.random() * 0.04 - 0.02)))
                
                history.append({
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time_point)),
                    "value": value_point
                })
            
            return {"success": True, "data": {"history": history, "item_id": item_id}}
        else:
            raise RolimonAPIError(404, f"Item not found with ID {item_id}")
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            params = {}
            if period:
                params["period"] = period
                
            response = requests.get(
                f"{ROLIMON_API_BASE}/items/{item_id}/history", 
                params=params,
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rolimon_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for Rolimon's price history: {str(e)}")
                raise RolimonAPIError(500, f"Error connecting to Rolimon API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rolimon API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rolimon_rate_limit
def get_deals(deal_type, limit=10):
    """Get current deals from Rolimon's"""
    if DEMO_MODE:
        logger.info(f"Using demo data for Rolimon's deals: {deal_type}")
        
        # Generate some demo deals
        deals = []
        
        # Use items from the demo data
        item_details = DEMO_DATA.get("rolimon", {}).get("item_details", {})
        items = list(item_details.items())
        
        # Generate random deals based on deal_type
        for i in range(min(limit, len(items))):
            item_id, item_data = items[i]
            
            if deal_type == "rap":
                # RAP deals: value is lower than RAP
                deal_percentage = random.uniform(15, 35)
                item_rap = item_data["rap"]
                value = int(item_rap * (1 - deal_percentage / 100))
            elif deal_type == "demand":
                # Demand deals: high demand items at slight discount
                deal_percentage = random.uniform(5, 15)
                value = int(item_data["value"] * (1 - deal_percentage / 100))
            else:  # "value" or default
                # Value deals: general discount from current value
                deal_percentage = random.uniform(10, 25)
                value = int(item_data["value"] * (1 - deal_percentage / 100))
            
            deals.append({
                "id": item_id,
                "name": item_data["name"],
                "current_price": value,
                "original_value": item_data["value"],
                "deal_percentage": round(deal_percentage, 1),
                "updated_at": "2025-04-20T20:30:00Z"
            })
        
        return {"success": True, "data": {"deals": deals, "deal_type": deal_type}}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            params = {"limit": limit, "dealType": deal_type}
            response = requests.get(
                f"{ROLIMON_API_BASE}/deals", 
                params=params,
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rolimon_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for Rolimon's deals: {str(e)}")
                raise RolimonAPIError(500, f"Error connecting to Rolimon API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rolimon API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rolimon_rate_limit
def get_player_rap(user_id):
    """Get a player's RAP (Recent Average Price) from Rolimon's"""
    user_id = str(user_id)  # Ensure string key for dict lookup
    
    if DEMO_MODE:
        logger.info(f"Using demo data for player RAP: {user_id}")
        
        if user_id in DEMO_DATA.get("rolimon", {}).get("player_rap", {}):
            return {"success": True, "data": DEMO_DATA["rolimon"]["player_rap"][user_id]}
        else:
            # Generate random RAP
            return {"success": True, "data": {
                "rap": random.randint(10000000, 200000000),
                "updated_at": "2025-04-20T20:30:00Z"
            }}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{ROLIMON_API_BASE}/players/{user_id}/rap",
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rolimon_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for player RAP: {str(e)}")
                raise RolimonAPIError(500, f"Error connecting to Rolimon API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rolimon API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rolimon_rate_limit
def get_player_value(user_id):
    """Get a player's value from Rolimon's"""
    if DEMO_MODE:
        logger.info(f"Using demo data for player value: {user_id}")
        
        # Assume value is generally higher than RAP
        user_id = str(user_id)
        if user_id in DEMO_DATA.get("rolimon", {}).get("player_rap", {}):
            rap = DEMO_DATA["rolimon"]["player_rap"][user_id]["rap"]
            value_multiplier = random.uniform(1.05, 1.2)
            value = int(rap * value_multiplier)
            
            return {"success": True, "data": {
                "value": value,
                "rap": rap,
                "value_rap_ratio": round(value_multiplier, 2),
                "updated_at": "2025-04-20T20:30:00Z"
            }}
        else:
            # Generate random value
            rap = random.randint(10000000, 200000000)
            value_multiplier = random.uniform(1.05, 1.2)
            value = int(rap * value_multiplier)
            
            return {"success": True, "data": {
                "value": value,
                "rap": rap,
                "value_rap_ratio": round(value_multiplier, 2),
                "updated_at": "2025-04-20T20:30:00Z"
            }}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{ROLIMON_API_BASE}/players/{user_id}/value",
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rolimon_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for player value: {str(e)}")
                raise RolimonAPIError(500, f"Error connecting to Rolimon API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rolimon API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rolimon_rate_limit
def get_player_inventory_value(user_id):
    """Get a player's inventory value from Rolimon's"""
    if DEMO_MODE:
        logger.info(f"Using demo data for player inventory value: {user_id}")
        
        # Generate a more detailed inventory value response
        user_id = str(user_id)
        player_rap = 0
        
        if user_id in DEMO_DATA.get("rolimon", {}).get("player_rap", {}):
            player_rap = DEMO_DATA["rolimon"]["player_rap"][user_id]["rap"]
        else:
            player_rap = random.randint(10000000, 200000000)
        
        value_multiplier = random.uniform(1.05, 1.2)
        inventory_value = int(player_rap * value_multiplier)
        
        # Generate a list of top items in the inventory
        top_items = []
        item_details = DEMO_DATA.get("rolimon", {}).get("item_details", {})
        items = list(item_details.items())
        
        for i in range(min(5, len(items))):
            item_id, item_data = items[i]
            top_items.append({
                "id": item_id,
                "name": item_data["name"],
                "value": item_data["value"],
                "rap": item_data["rap"]
            })
        
        return {"success": True, "data": {
            "inventory_value": inventory_value,
            "inventory_rap": player_rap,
            "value_rap_ratio": round(value_multiplier, 2),
            "item_count": random.randint(20, 100),
            "top_items": top_items,
            "updated_at": "2025-04-20T20:30:00Z"
        }}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{ROLIMON_API_BASE}/players/{user_id}/inventory-value",
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rolimon_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for player inventory value: {str(e)}")
                raise RolimonAPIError(500, f"Error connecting to Rolimon API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rolimon API call in {wait_time} seconds...")
            time.sleep(wait_time)

# =================== Rblx Trade API Functions ===================

@with_rblx_trade_rate_limit
def get_trade_ads(limit=50, cursor=None):
    """Get current trade advertisements from Rblx.Trade"""
    if DEMO_MODE:
        logger.info("Using demo data for trade ads")
        
        # Generate demo trade ads
        ads = []
        item_details = DEMO_DATA.get("rolimon", {}).get("item_details", {})
        items = list(item_details.items())
        
        for i in range(min(limit, 10)):  # Generate up to 10 demo ads
            # Select random items for offering and requesting
            offer_count = random.randint(1, 3)
            request_count = random.randint(1, 3)
            
            offer_items = []
            request_items = []
            
            # Get random items for offering
            for j in range(offer_count):
                if j < len(items):
                    item_id, item_data = items[j]
                    offer_items.append({
                        "id": item_id,
                        "name": item_data["name"],
                        "value": item_data["value"]
                    })
            
            # Get random items for requesting
            for j in range(request_count):
                idx = (j + offer_count) % len(items)
                if idx < len(items):
                    item_id, item_data = items[idx]
                    request_items.append({
                        "id": item_id,
                        "name": item_data["name"],
                        "value": item_data["value"]
                    })
                    
            # Calculate total values
            offer_value = sum(item["value"] for item in offer_items)
            request_value = sum(item["value"] for item in request_items)
            
            ads.append({
                "id": f"ad-{i+1}",
                "user_id": random.randint(100000, 9999999),
                "username": f"Trader{i+1}",
                "offer_items": offer_items,
                "request_items": request_items,
                "offer_value": offer_value,
                "request_value": request_value,
                "created_at": "2025-04-20T15:30:00Z"
            })
        
        return {"success": True, "data": {
            "ads": ads,
            "total": len(ads),
            "cursor": None  # No pagination in demo
        }}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            params = {"limit": limit}
            if cursor:
                params["cursor"] = cursor
                
            response = requests.get(
                f"{RBLX_TRADE_API_BASE}/trade-ads", 
                params=params,
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rblx_trade_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for trade ads: {str(e)}")
                raise RblxTradeAPIError(500, f"Error connecting to Rblx Trade API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rblx Trade API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rblx_trade_rate_limit
def get_player_trade_reputation(user_id):
    """Get a player's trade reputation from Rblx.Trade"""
    user_id = str(user_id)  # Ensure string key for dict lookup
    
    if DEMO_MODE:
        logger.info(f"Using demo data for player trade reputation: {user_id}")
        
        if user_id in DEMO_DATA.get("rblx_trade", {}).get("player_reputation", {}):
            return {"success": True, "data": DEMO_DATA["rblx_trade"]["player_reputation"][user_id]}
        else:
            # Generate random reputation
            total_trades = random.randint(50, 200)
            completed_percent = random.uniform(0.8, 0.98)
            completed_trades = int(total_trades * completed_percent)
            cancelled_trades = total_trades - completed_trades
            
            positive_percent = random.uniform(0.85, 0.98)
            positive_reviews = int(completed_trades * positive_percent)
            negative_reviews = int(completed_trades * 0.05)
            neutral_reviews = completed_trades - positive_reviews - negative_reviews
            
            reputation_score = round((positive_reviews / completed_trades) * 10, 1)
            
            return {"success": True, "data": {
                "score": reputation_score,
                "total_trades": total_trades,
                "completed_trades": completed_trades,
                "cancelled_trades": cancelled_trades,
                "positive_reviews": positive_reviews,
                "negative_reviews": negative_reviews,
                "neutral_reviews": neutral_reviews,
                "trusted_trader": reputation_score >= 8.0,
                "updated_at": "2025-04-20T18:45:00Z"
            }}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{RBLX_TRADE_API_BASE}/players/{user_id}/reputation",
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rblx_trade_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for player trade reputation: {str(e)}")
                raise RblxTradeAPIError(500, f"Error connecting to Rblx Trade API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rblx Trade API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rblx_trade_rate_limit
def get_trade_value_calculator(offer_items, request_items):
    """Calculate trade value using Rblx.Trade"""
    if DEMO_MODE:
        logger.info("Using demo data for trade calculator")
        
        # Calculate values based on demo item details
        offer_value = 0
        request_value = 0
        
        item_details = DEMO_DATA.get("rolimon", {}).get("item_details", {})
        
        for item_id in offer_items:
            item_id_str = str(item_id)
            if item_id_str in item_details:
                offer_value += item_details[item_id_str]["value"]
            else:
                # Random value if item not found
                offer_value += random.randint(10000, 1000000)
        
        for item_id in request_items:
            item_id_str = str(item_id)
            if item_id_str in item_details:
                request_value += item_details[item_id_str]["value"]
            else:
                # Random value if item not found
                request_value += random.randint(10000, 1000000)
        
        value_difference = offer_value - request_value
        is_profitable = value_difference < 0  # Profitable if receiving more value
        
        # Determine trade recommendation
        if abs(value_difference) < 1000:  # Small difference
            recommendation = "Fair - This is an even trade"
        elif value_difference > 0:
            if value_difference > offer_value * 0.3:  # More than 30% loss
                recommendation = "Decline - Items you're offering are worth significantly more"
            else:
                recommendation = "Consider - You're giving more value, but it might be acceptable"
        else:
            if abs(value_difference) > request_value * 0.3:  # More than 30% gain
                recommendation = "Accept - Excellent deal in your favor"
            else:
                recommendation = "Accept - You're getting more value"
        
        return {"success": True, "data": {
            "offer_value": offer_value,
            "request_value": request_value,
            "value_difference": value_difference,
            "is_profitable": is_profitable,
            "is_fair": abs(value_difference) < (offer_value * 0.1),  # Fair if <10% difference
            "recommendation": recommendation,
            "timestamp": "2025-04-20T20:15:45Z"
        }}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            data = {
                "offer": offer_items,
                "request": request_items
            }
            response = requests.post(
                f"{RBLX_TRADE_API_BASE}/trade-calculator", 
                json=data,
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rblx_trade_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for trade calculator: {str(e)}")
                raise RblxTradeAPIError(500, f"Error connecting to Rblx Trade API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rblx Trade API call in {wait_time} seconds...")
            time.sleep(wait_time)

# =================== Roliverse API Functions ===================

@with_roliverse_rate_limit
def get_player_trading_activity(user_id, limit=20):
    """Get a player's trading activity from Roliverse"""
    if DEMO_MODE:
        logger.info(f"Using demo data for player trading activity: {user_id}")
        
        # Generate demo trading activity
        trades = []
        item_details = DEMO_DATA.get("rolimon", {}).get("item_details", {})
        items = list(item_details.items())
        
        for i in range(min(limit, 10)):  # Generate up to 10 demo trades
            # When the trade occurred
            days_ago = i + random.randint(0, 5)
            trade_date = time.time() - (days_ago * 86400)
            trade_date_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(trade_date))
            
            # Items exchanged
            gave_count = random.randint(1, 3)
            received_count = random.randint(1, 3)
            
            gave_items = []
            received_items = []
            
            # Items given
            for j in range(gave_count):
                if j < len(items):
                    item_id, item_data = items[j]
                    gave_items.append({
                        "id": item_id,
                        "name": item_data["name"],
                        "value": item_data["value"]
                    })
            
            # Items received
            for j in range(received_count):
                idx = (j + gave_count) % len(items)
                if idx < len(items):
                    item_id, item_data = items[idx]
                    received_items.append({
                        "id": item_id,
                        "name": item_data["name"],
                        "value": item_data["value"]
                    })
                    
            # Calculate values
            gave_value = sum(item["value"] for item in gave_items)
            received_value = sum(item["value"] for item in received_items)
            profit = received_value - gave_value
            
            trades.append({
                "id": f"trade-{i+1}",
                "trade_partner_id": random.randint(100000, 9999999),
                "trade_partner_name": f"Partner{i+1}",
                "gave_items": gave_items,
                "received_items": received_items,
                "gave_value": gave_value,
                "received_value": received_value,
                "profit": profit,
                "profit_percentage": round((profit / gave_value * 100) if gave_value > 0 else 0, 1),
                "timestamp": trade_date_str
            })
        
        return {"success": True, "data": {
            "trades": trades,
            "user_id": user_id,
            "total_count": len(trades)
        }}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            params = {"limit": limit}
            response = requests.get(
                f"{ROLIVERSE_API_BASE}/players/{user_id}/trades", 
                params=params,
                timeout=CONNECTION_TIMEOUT
            )
            return handle_roliverse_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for player trading activity: {str(e)}")
                raise RoliverseAPIError(500, f"Error connecting to Roliverse API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roliverse API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_roliverse_rate_limit
def get_market_trends(item_type="limited", time_period="week"):
    """Get market trends from Roliverse"""
    if DEMO_MODE:
        logger.info(f"Using demo data for market trends: type={item_type}, period={time_period}")
        
        # Use pre-defined market trends data
        if "roliverse" in DEMO_DATA and "market_trends" in DEMO_DATA["roliverse"]:
            trends_data = DEMO_DATA["roliverse"]["market_trends"]
            
            # Update with requested parameters
            trends_data["type"] = item_type
            trends_data["period"] = time_period
            
            return {"success": True, "data": trends_data}
        else:
            # Should never happen as we generate the demo data
            logger.error("Market trends demo data not found")
            raise RoliverseAPIError(500, "Demo data not properly initialized")
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            params = {"type": item_type, "period": time_period}
            response = requests.get(
                f"{ROLIVERSE_API_BASE}/market/trends", 
                params=params,
                timeout=CONNECTION_TIMEOUT
            )
            return handle_roliverse_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for market trends: {str(e)}")
                raise RoliverseAPIError(500, f"Error connecting to Roliverse API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roliverse API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_roliverse_rate_limit
def get_demand_index(item_id):
    """Get demand index for an item from Roliverse"""
    item_id = str(item_id)  # Ensure string key for dict lookup
    
    if DEMO_MODE:
        logger.info(f"Using demo data for demand index: {item_id}")
        
        if item_id in DEMO_DATA.get("roliverse", {}).get("demand_indexes", {}):
            return {"success": True, "data": DEMO_DATA["roliverse"]["demand_indexes"][item_id]}
        else:
            # Generate random demand data
            demand_index = round(random.uniform(1.0, 10.0), 1)
            
            # Determine category based on index
            if demand_index >= 8.0:
                demand_category = "Very High"
            elif demand_index >= 6.0:
                demand_category = "High"
            elif demand_index >= 4.0:
                demand_category = "Medium"
            elif demand_index >= 2.0:
                demand_category = "Low"
            else:
                demand_category = "Very Low"
                
            return {"success": True, "data": {
                "demand_index": demand_index,
                "demand_category": demand_category,
                "trading_volume": round(random.uniform(0.5, 10.0), 1),
                "stability_score": round(random.uniform(1.0, 10.0), 1),
                "updated_at": "2025-04-20T15:30:00Z"
            }}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{ROLIVERSE_API_BASE}/items/{item_id}/demand",
                timeout=CONNECTION_TIMEOUT
            )
            return handle_roliverse_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for demand index: {str(e)}")
                raise RoliverseAPIError(500, f"Error connecting to Roliverse API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Roliverse API call in {wait_time} seconds...")
            time.sleep(wait_time)

# =================== Rblx Values API Functions ===================

@with_rblx_values_rate_limit
def get_item_projected_status(item_id):
    """Get projected status for an item from Rblx Values"""
    item_id = str(item_id)  # Ensure string key for dict lookup
    
    if DEMO_MODE:
        logger.info(f"Using demo data for item projected status: {item_id}")
        
        if item_id in DEMO_DATA.get("rblx_values", {}).get("item_projected", {}):
            base_data = DEMO_DATA["rblx_values"]["item_projected"][item_id]
            
            # Add extra information if item is projected
            if base_data.get("is_projected", False):
                # For projected items, include additional details
                return {"success": True, "data": {
                    "is_projected": True,
                    "projected_since": "2025-04-01T00:00:00Z",
                    "real_value_estimate": int(base_data.get("real_value_estimate", 10000000)),
                    "inflation_percentage": int(base_data.get("inflation_percentage", 50)),
                    "projection_confidence": "High",
                    "updated_at": "2025-04-20T12:00:00Z"
                }}
            else:
                # For non-projected items, just return the basic info
                return {"success": True, "data": {
                    "is_projected": False,
                    "updated_at": "2025-04-20T12:00:00Z"
                }}
        else:
            # Default to not projected
            return {"success": True, "data": {
                "is_projected": False,
                "updated_at": "2025-04-20T12:00:00Z"
            }}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{RBLX_VALUES_API_BASE}/items/{item_id}/projected",
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rblx_values_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for item projected status: {str(e)}")
                raise RblxValuesAPIError(500, f"Error connecting to Rblx Values API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rblx Values API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rblx_values_rate_limit
def get_item_stability_rating(item_id):
    """Get stability rating for an item from Rblx Values"""
    if DEMO_MODE:
        logger.info(f"Using demo data for item stability rating: {item_id}")
        
        # Generate random stability data
        stability_rating = round(random.uniform(1.0, 10.0), 1)
        
        # Determine category based on rating
        if stability_rating >= 8.0:
            stability_category = "Very Stable"
            volatility = round(random.uniform(0.01, 0.05), 2)
        elif stability_rating >= 6.0:
            stability_category = "Stable"
            volatility = round(random.uniform(0.05, 0.1), 2)
        elif stability_rating >= 4.0:
            stability_category = "Moderate"
            volatility = round(random.uniform(0.1, 0.2), 2)
        elif stability_rating >= 2.0:
            stability_category = "Volatile"
            volatility = round(random.uniform(0.2, 0.3), 2)
        else:
            stability_category = "Highly Volatile"
            volatility = round(random.uniform(0.3, 0.5), 2)
            
        return {"success": True, "data": {
            "stability_rating": stability_rating,
            "stability_category": stability_category,
            "volatility": volatility,
            "price_changes_last_month": random.randint(1, 10),
            "max_value_last_month": random.randint(10000000, 50000000),
            "min_value_last_month": random.randint(5000000, 9000000),
            "updated_at": "2025-04-20T12:00:00Z"
        }}
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                f"{RBLX_VALUES_API_BASE}/items/{item_id}/stability",
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rblx_values_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for item stability rating: {str(e)}")
                raise RblxValuesAPIError(500, f"Error connecting to Rblx Values API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rblx Values API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rblx_values_rate_limit
def get_items_rising_value(limit=20):
    """Get items with rising values from Rblx Values"""
    if DEMO_MODE:
        logger.info(f"Using demo data for rising value items: limit={limit}")
        
        # Use pre-defined rising items data
        if "rblx_values" in DEMO_DATA and "rising_items" in DEMO_DATA["rblx_values"]:
            rising_items_data = DEMO_DATA["rblx_values"]["rising_items"]
            
            # Limit the number of items returned
            items = rising_items_data.get("items", [])
            limited_items = items[:min(limit, len(items))]
            
            return {"success": True, "data": {
                "items": limited_items,
                "updated_at": rising_items_data.get("updated_at", "2025-04-20T00:00:00Z")
            }}
        else:
            # Should never happen as we generate the demo data
            logger.error("Rising items demo data not found")
            raise RblxValuesAPIError(500, "Demo data not properly initialized")
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            params = {"limit": limit}
            response = requests.get(
                f"{RBLX_VALUES_API_BASE}/market/rising", 
                params=params,
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rblx_values_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for rising value items: {str(e)}")
                raise RblxValuesAPIError(500, f"Error connecting to Rblx Values API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rblx Values API call in {wait_time} seconds...")
            time.sleep(wait_time)

@with_rblx_values_rate_limit
def get_items_falling_value(limit=20):
    """Get items with falling values from Rblx Values"""
    if DEMO_MODE:
        logger.info(f"Using demo data for falling value items: limit={limit}")
        
        # Generate falling items based on rising items (with negative change)
        if "rblx_values" in DEMO_DATA and "rising_items" in DEMO_DATA["rblx_values"]:
            # Convert rising items to falling by making the changes negative
            rising_items = DEMO_DATA["rblx_values"]["rising_items"].get("items", [])
            
            falling_items = []
            for i, item in enumerate(rising_items):
                if i >= limit:
                    break
                    
                # Create a new falling item with negative change
                falling_item = item.copy()
                falling_item["value_change"] = -falling_item["value_change"]
                falling_items.append(falling_item)
            
            return {"success": True, "data": {
                "items": falling_items,
                "updated_at": "2025-04-20T00:00:00Z"
            }}
        else:
            # Should never happen as we generate the demo data
            logger.error("Rising items demo data not found (needed for falling items)")
            raise RblxValuesAPIError(500, "Demo data not properly initialized")
    
    # Real API call with retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            params = {"limit": limit}
            response = requests.get(
                f"{RBLX_VALUES_API_BASE}/market/falling", 
                params=params,
                timeout=CONNECTION_TIMEOUT
            )
            return handle_rblx_values_response(response)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error(f"Max retries reached for falling value items: {str(e)}")
                raise RblxValuesAPIError(500, f"Error connecting to Rblx Values API: {str(e)}")
            
            wait_time = RETRY_BACKOFF * (2 ** (retries - 1))
            logger.warning(f"Retrying Rblx Values API call in {wait_time} seconds...")
            time.sleep(wait_time)