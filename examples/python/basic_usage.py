#!/usr/bin/env python3
"""
Basic usage examples for BloxAPI with Python
"""

import requests
from pprint import pprint

# Base URL for your BloxAPI instance
BASE_URL = "http://localhost:5000"

def get_user_info(user_id):
    """Get information about a Roblox user"""
    response = requests.get(f"{BASE_URL}/api/users/{user_id}")
    response.raise_for_status()  # Raise exception for HTTP errors
    return response.json()

def search_users(keyword, limit=10):
    """Search for Roblox users by keyword"""
    params = {
        "keyword": keyword,
        "limit": limit
    }
    response = requests.get(f"{BASE_URL}/api/users/search", params=params)
    response.raise_for_status()
    return response.json()

def get_game_info(universe_id):
    """Get information about a Roblox game by universe ID"""
    response = requests.get(f"{BASE_URL}/api/games/{universe_id}")
    response.raise_for_status()
    return response.json()

def get_game_analytics(universe_id, metric_type, time_frame="past7days"):
    """Get analytics for a Roblox game"""
    params = {
        "time_frame": time_frame
    }
    url = f"{BASE_URL}/api/analytics/games/{universe_id}/{metric_type}"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def search_catalog(keyword, category=None, limit=25):
    """Search the Roblox catalog"""
    params = {
        "keyword": keyword,
        "limit": limit
    }
    if category:
        params["category"] = category
        
    response = requests.get(f"{BASE_URL}/api/catalog/search", params=params)
    response.raise_for_status()
    return response.json()

def get_asset_info(asset_id):
    """Get information about a Roblox asset"""
    response = requests.get(f"{BASE_URL}/api/assets/{asset_id}")
    response.raise_for_status()
    return response.json()

def get_badge_info(badge_id):
    """Get information about a Roblox badge"""
    response = requests.get(f"{BASE_URL}/api/badges/{badge_id}")
    response.raise_for_status()
    return response.json()

def check_content_moderation(content_type, content_id):
    """Check moderation status of Roblox content"""
    url = f"{BASE_URL}/api/moderation/content/{content_type}/{content_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Example usage

    # Get user information for Roblox user ID 1
    print("Getting user information for Roblox founder...")
    user_info = get_user_info(1)
    pprint(user_info)
    print("\n")

    # Search for users with keyword "Roblox"
    print("Searching for users with keyword 'Roblox'...")
    search_results = search_users("Roblox", limit=5)
    pprint(search_results)
    print("\n")

    # Get game information for Natural Disaster Survival (189707)
    print("Getting game information for Natural Disaster Survival...")
    game_info = get_game_info(189707)
    pprint(game_info)
    print("\n")

    # Get visits analytics for the game
    print("Getting visits analytics for the game...")
    analytics = get_game_analytics(189707, "visits")
    pprint(analytics)
    print("\n")

    # Search for dominus hats in the catalog
    print("Searching for dominus hats in the catalog...")
    catalog_results = search_catalog("dominus", category="hats")
    pprint(catalog_results)
    print("\n")

    # Check moderation status of an asset
    print("Checking moderation status of an asset...")
    moderation_status = check_content_moderation("asset", 1818)
    pprint(moderation_status)