#!/usr/bin/env python3
"""
Advanced usage examples for BloxAPI with Python
Features:
- Rate limiting with automated retries
- Caching responses
- Concurrent requests with asyncio
- Error handling
"""

import asyncio
import functools
import json
import os
import time
from datetime import timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

import aiohttp
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Base URL for your BloxAPI instance
BASE_URL = "http://localhost:5000"

# Cache directory
CACHE_DIR = Path("./cache")
CACHE_TTL = timedelta(hours=1)  # Cache TTL: 1 hour

# Create cache directory if it doesn't exist
os.makedirs(CACHE_DIR, exist_ok=True)

class BloxAPIClient:
    """
    Advanced client for BloxAPI with caching, rate limiting, and error handling
    """
    
    def __init__(self, base_url: str = BASE_URL, cache_dir: Path = CACHE_DIR, 
                 cache_ttl: timedelta = CACHE_TTL, max_retries: int = 3):
        """
        Initialize the BloxAPI client
        
        Args:
            base_url: Base URL for the BloxAPI instance
            cache_dir: Directory to store cached responses
            cache_ttl: Time-to-live for cached responses
            max_retries: Maximum number of retries for failed requests
        """
        self.base_url = base_url
        self.cache_dir = cache_dir
        self.cache_ttl = cache_ttl
        
        # Configure session with retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def _get_cache_key(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Generate a cache key from endpoint and params"""
        if params:
            sorted_params = sorted(params.items())
            param_str = "_".join(f"{k}={v}" for k, v in sorted_params)
            return f"{endpoint}_{param_str}"
        return endpoint
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get the cache file path for a cache key"""
        # Use SHA-256 hash or similar for longer keys
        safe_key = cache_key.replace("/", "_").replace(":", "_")
        return self.cache_dir / f"{safe_key}.json"
    
    def _get_from_cache(self, cache_path: Path) -> Optional[Dict[str, Any]]:
        """Try to get a response from cache"""
        if not cache_path.exists():
            return None
            
        # Check if cache is expired
        mtime = cache_path.stat().st_mtime
        if time.time() - mtime > self.cache_ttl.total_seconds():
            return None
            
        try:
            with open(cache_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def _save_to_cache(self, cache_path: Path, data: Dict[str, Any]) -> None:
        """Save response data to cache"""
        try:
            with open(cache_path, "w") as f:
                json.dump(data, f)
        except IOError:
            pass  # Ignore cache write errors
    
    def request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                use_cache: bool = True, **kwargs) -> Dict[str, Any]:
        """
        Make a request to the BloxAPI
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., "/api/users/1")
            params: Query parameters
            use_cache: Whether to use cache for GET requests
            **kwargs: Additional arguments to pass to requests.request
            
        Returns:
            Response data as dictionary
            
        Raises:
            requests.exceptions.RequestException: On request error
        """
        url = f"{self.base_url}{endpoint}"
        
        # Check cache for GET requests
        if method.upper() == "GET" and use_cache and params:
            cache_key = self._get_cache_key(endpoint, params)
            cache_path = self._get_cache_path(cache_key)
            cached_data = self._get_from_cache(cache_path)
            if cached_data:
                return cached_data
        
        # Make the request
        response = self.session.request(method, url, params=params, **kwargs)
        response.raise_for_status()
        data = response.json()
        
        # Cache the response for GET requests
        if method.upper() == "GET" and use_cache:
            cache_key = self._get_cache_key(endpoint, params)
            cache_path = self._get_cache_path(cache_key)
            self._save_to_cache(cache_path, data)
        
        return data
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
            use_cache: bool = True, **kwargs) -> Dict[str, Any]:
        """Make a GET request"""
        return self.request("GET", endpoint, params, use_cache, **kwargs)
    
    def post(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a POST request"""
        return self.request("POST", endpoint, json=json_data, use_cache=False, **kwargs)
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get information about a Roblox user"""
        return self.get(f"/api/users/{user_id}")
    
    def search_users(self, keyword: str, limit: int = 10) -> Dict[str, Any]:
        """Search for Roblox users by keyword"""
        params = {
            "keyword": keyword,
            "limit": limit
        }
        return self.get("/api/users/search", params=params)
    
    def get_game(self, universe_id: int) -> Dict[str, Any]:
        """Get information about a Roblox game"""
        return self.get(f"/api/games/{universe_id}")
    
    def get_game_analytics(self, universe_id: int, metric_type: str, 
                           time_frame: str = "past7days") -> Dict[str, Any]:
        """Get analytics for a Roblox game"""
        params = {"time_frame": time_frame}
        return self.get(f"/api/analytics/games/{universe_id}/{metric_type}", params=params)
    
    def search_catalog(self, keyword: str, category: Optional[str] = None, 
                       limit: int = 25) -> Dict[str, Any]:
        """Search the Roblox catalog"""
        params = {
            "keyword": keyword,
            "limit": limit
        }
        if category:
            params["category"] = category
            
        return self.get("/api/catalog/search", params=params)
    
    # Add more methods as needed for other API endpoints


class AsyncBloxAPIClient:
    """
    Asynchronous client for BloxAPI with concurrency support
    """
    
    def __init__(self, base_url: str = BASE_URL):
        """Initialize the async BloxAPI client"""
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        """Create session when used as context manager"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close session when exiting context manager"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make an async GET request"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        url = f"{self.base_url}{endpoint}"
        async with self.session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get_users(self, user_ids: List[int]) -> List[Dict[str, Any]]:
        """Get information about multiple Roblox users concurrently"""
        tasks = [self.get(f"/api/users/{user_id}") for user_id in user_ids]
        return await asyncio.gather(*tasks)
    
    async def get_games(self, universe_ids: List[int]) -> List[Dict[str, Any]]:
        """Get information about multiple Roblox games concurrently"""
        tasks = [self.get(f"/api/games/{universe_id}") for universe_id in universe_ids]
        return await asyncio.gather(*tasks)
    
    # Add more async methods as needed


async def run_async_example():
    """Example of using the async client"""
    print("Running async example:")
    async with AsyncBloxAPIClient() as client:
        # Get information about multiple users concurrently
        user_ids = [1, 2, 3, 4, 5]
        print(f"Getting information for {len(user_ids)} users concurrently...")
        users = await client.get_users(user_ids)
        print(f"Retrieved {len(users)} users")
        
        # Get information about multiple games concurrently
        universe_ids = [189707, 292439477, 2753915549]
        print(f"Getting information for {len(universe_ids)} games concurrently...")
        games = await client.get_games(universe_ids)
        print(f"Retrieved {len(games)} games")
        
        return users, games


def run_sync_example():
    """Example of using the synchronous client with advanced features"""
    print("Running sync example with caching and retries:")
    client = BloxAPIClient()
    
    # Get user information with caching
    print("Getting user information (will be cached)...")
    user_info = client.get_user(1)
    print(f"User name: {user_info.get('name', '')}")
    
    # Search catalog with caching
    print("Searching catalog (will be cached)...")
    results = client.search_catalog("dominus", category="hats", limit=5)
    print(f"Found {len(results.get('data', []))} results")
    
    # Make the same requests again to use cache
    print("Getting user information again (from cache)...")
    user_info_cached = client.get_user(1)
    print(f"User name (from cache): {user_info_cached.get('name', '')}")
    
    # Get game analytics for a specific game
    print("Getting game analytics...")
    analytics = client.get_game_analytics(189707, "visits", time_frame="past30days")
    print(f"Got analytics data for past 30 days")
    
    return user_info, results, analytics


if __name__ == "__main__":
    # Run the synchronous example
    run_sync_example()
    print("\n" + "-" * 50 + "\n")
    
    # Run the asynchronous example
    asyncio.run(run_async_example())