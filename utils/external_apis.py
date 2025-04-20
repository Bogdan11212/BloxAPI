import requests
import logging
import time
from functools import wraps
from .rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

# Base URLs for external APIs
ROLIMON_API_BASE = "https://api.rolimons.com/v1"
RBLX_TRADE_API_BASE = "https://api.rblx.trade/v1"
ROLIVERSE_API_BASE = "https://api.roliverse.com/v1"
RBLX_VALUES_API_BASE = "https://api.rblxvalues.com/v1"

# Rate limiters for external APIs
rolimon_rate_limiter = RateLimiter(max_calls=30, period=60)  # 30 calls per minute
rblx_trade_rate_limiter = RateLimiter(max_calls=30, period=60)  # 30 calls per minute
roliverse_rate_limiter = RateLimiter(max_calls=30, period=60)  # 30 calls per minute
rblx_values_rate_limiter = RateLimiter(max_calls=30, period=60)  # 30 calls per minute

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

# =================== Rolimon API Functions ===================

@with_rolimon_rate_limit
def get_item_details(item_id):
    """Get details for a specific item from Rolimon's"""
    response = requests.get(f"{ROLIMON_API_BASE}/items/{item_id}")
    return handle_rolimon_response(response)

@with_rolimon_rate_limit
def get_item_values(item_ids):
    """Get values for multiple items from Rolimon's"""
    response = requests.post(
        f"{ROLIMON_API_BASE}/items/values", 
        json={"ids": item_ids}
    )
    return handle_rolimon_response(response)

@with_rolimon_rate_limit
def get_item_price_history(item_id, period=None):
    """Get price history for an item from Rolimon's"""
    params = {}
    if period:
        params["period"] = period
    response = requests.get(f"{ROLIMON_API_BASE}/items/{item_id}/history", params=params)
    return handle_rolimon_response(response)

@with_rolimon_rate_limit
def get_deals(deal_type, limit=10):
    """Get current deals from Rolimon's"""
    params = {"limit": limit, "dealType": deal_type}
    response = requests.get(f"{ROLIMON_API_BASE}/deals", params=params)
    return handle_rolimon_response(response)

@with_rolimon_rate_limit
def get_player_rap(user_id):
    """Get a player's RAP (Recent Average Price) from Rolimon's"""
    response = requests.get(f"{ROLIMON_API_BASE}/players/{user_id}/rap")
    return handle_rolimon_response(response)

@with_rolimon_rate_limit
def get_player_value(user_id):
    """Get a player's value from Rolimon's"""
    response = requests.get(f"{ROLIMON_API_BASE}/players/{user_id}/value")
    return handle_rolimon_response(response)

@with_rolimon_rate_limit
def get_player_inventory_value(user_id):
    """Get a player's inventory value from Rolimon's"""
    response = requests.get(f"{ROLIMON_API_BASE}/players/{user_id}/inventory-value")
    return handle_rolimon_response(response)

# =================== Rblx Trade API Functions ===================

@with_rblx_trade_rate_limit
def get_trade_ads(limit=50, cursor=None):
    """Get current trade advertisements from Rblx.Trade"""
    params = {"limit": limit}
    if cursor:
        params["cursor"] = cursor
    response = requests.get(f"{RBLX_TRADE_API_BASE}/trade-ads", params=params)
    return handle_rblx_trade_response(response)

@with_rblx_trade_rate_limit
def get_player_trade_reputation(user_id):
    """Get a player's trade reputation from Rblx.Trade"""
    response = requests.get(f"{RBLX_TRADE_API_BASE}/players/{user_id}/reputation")
    return handle_rblx_trade_response(response)

@with_rblx_trade_rate_limit
def get_trade_value_calculator(offer_items, request_items):
    """Calculate trade value using Rblx.Trade"""
    data = {
        "offer": offer_items,
        "request": request_items
    }
    response = requests.post(f"{RBLX_TRADE_API_BASE}/trade-calculator", json=data)
    return handle_rblx_trade_response(response)

# =================== Roliverse API Functions ===================

@with_roliverse_rate_limit
def get_player_trading_activity(user_id, limit=20):
    """Get a player's trading activity from Roliverse"""
    params = {"limit": limit}
    response = requests.get(f"{ROLIVERSE_API_BASE}/players/{user_id}/trades", params=params)
    return handle_roliverse_response(response)

@with_roliverse_rate_limit
def get_market_trends(item_type="limited", time_period="week"):
    """Get market trends from Roliverse"""
    params = {"type": item_type, "period": time_period}
    response = requests.get(f"{ROLIVERSE_API_BASE}/market/trends", params=params)
    return handle_roliverse_response(response)

@with_roliverse_rate_limit
def get_demand_index(item_id):
    """Get demand index for an item from Roliverse"""
    response = requests.get(f"{ROLIVERSE_API_BASE}/items/{item_id}/demand")
    return handle_roliverse_response(response)

# =================== Rblx Values API Functions ===================

@with_rblx_values_rate_limit
def get_item_projected_status(item_id):
    """Get projected status for an item from Rblx Values"""
    response = requests.get(f"{RBLX_VALUES_API_BASE}/items/{item_id}/projected")
    return handle_rblx_values_response(response)

@with_rblx_values_rate_limit
def get_item_stability_rating(item_id):
    """Get stability rating for an item from Rblx Values"""
    response = requests.get(f"{RBLX_VALUES_API_BASE}/items/{item_id}/stability")
    return handle_rblx_values_response(response)

@with_rblx_values_rate_limit
def get_items_rising_value(limit=20):
    """Get items with rising values from Rblx Values"""
    params = {"limit": limit}
    response = requests.get(f"{RBLX_VALUES_API_BASE}/market/rising", params=params)
    return handle_rblx_values_response(response)

@with_rblx_values_rate_limit
def get_items_falling_value(limit=20):
    """Get items with falling values from Rblx Values"""
    params = {"limit": limit}
    response = requests.get(f"{RBLX_VALUES_API_BASE}/market/falling", params=params)
    return handle_rblx_values_response(response)