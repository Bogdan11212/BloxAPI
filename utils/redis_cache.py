"""
Redis Cache Implementation for BloxAPI

This module provides a Redis-based caching system to improve API performance
by caching frequently accessed data and reducing API calls.
"""

import os
import json
import logging
import time
import redis
from functools import wraps
from typing import Any, Dict, Optional, Union, Callable, TypeVar, cast

# Configure logging
logger = logging.getLogger(__name__)

# Type variable for function return type
T = TypeVar('T')

class RedisCache:
    """Redis cache implementation for BloxAPI"""
    
    def __init__(self, redis_url: Optional[str] = None, prefix: str = "bloxapi:", 
                 default_ttl: int = 3600):
        """
        Initialize the Redis cache.
        
        Args:
            redis_url: Redis connection URL. Defaults to environment variable REDIS_URL if not provided.
            prefix: Prefix for all Redis keys to avoid collisions
            default_ttl: Default time-to-live in seconds for cached items (1 hour)
        """
        self.prefix = prefix
        self.default_ttl = default_ttl
        
        # Connect to Redis using provided URL or from environment
        redis_url = redis_url or os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
        
        try:
            self.redis = redis.from_url(redis_url)
            self.enabled = True
            logger.info(f"Redis cache initialized with connection to {redis_url}")
            
            # Test connection
            self.redis.ping()
        except redis.ConnectionError as e:
            logger.warning(f"Could not connect to Redis: {e}. Caching will be disabled.")
            self.enabled = False
        except Exception as e:
            logger.warning(f"Redis initialization error: {e}. Caching will be disabled.")
            self.enabled = False
    
    def get_prefixed_key(self, key: str) -> str:
        """Add prefix to Redis key"""
        return f"{self.prefix}{key}"
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            The cached value or None if not found
        """
        if not self.enabled:
            return None
        
        prefixed_key = self.get_prefixed_key(key)
        try:
            value = self.redis.get(prefixed_key)
            if value:
                logger.debug(f"Cache hit for key: {key}")
                return json.loads(value)
            logger.debug(f"Cache miss for key: {key}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving from Redis cache: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set a value in cache.
        
        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            ttl: Time-to-live in seconds. Uses default_ttl if not specified.
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        ttl = ttl if ttl is not None else self.default_ttl
        prefixed_key = self.get_prefixed_key(key)
        
        try:
            serialized = json.dumps(value)
            self.redis.setex(prefixed_key, ttl, serialized)
            logger.debug(f"Stored in cache: {key} (TTL: {ttl}s)")
            return True
        except (TypeError, ValueError) as e:
            logger.error(f"Cannot serialize value for key {key}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error storing in Redis cache: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False otherwise
        """
        if not self.enabled:
            return False
        
        prefixed_key = self.get_prefixed_key(key)
        try:
            result = self.redis.delete(prefixed_key)
            logger.debug(f"Deleted from cache: {key}")
            return result > 0
        except Exception as e:
            logger.error(f"Error deleting from Redis cache: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching a pattern.
        
        Args:
            pattern: Pattern to match (e.g., "users:*")
            
        Returns:
            Number of keys cleared
        """
        if not self.enabled:
            return 0
        
        prefixed_pattern = self.get_prefixed_key(pattern)
        try:
            keys = self.redis.keys(prefixed_pattern)
            if keys:
                result = self.redis.delete(*keys)
                logger.info(f"Cleared {result} keys matching pattern: {pattern}")
                return result
            return 0
        except Exception as e:
            logger.error(f"Error clearing keys from Redis cache: {e}")
            return 0
    
    def clear_all(self) -> int:
        """
        Clear all cached keys with this prefix.
        
        Returns:
            Number of keys cleared
        """
        return self.clear_pattern("*")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary of cache statistics
        """
        if not self.enabled:
            return {"status": "disabled", "keys": 0}
        
        try:
            info = self.redis.info()
            prefixed_keys = len(self.redis.keys(self.get_prefixed_key("*")))
            
            return {
                "status": "enabled",
                "keys": prefixed_keys,
                "memory_used": info.get("used_memory_human", "unknown"),
                "uptime": info.get("uptime_in_seconds", 0),
                "hit_rate": info.get("keyspace_hits", 0) / (info.get("keyspace_hits", 0) + info.get("keyspace_misses", 1) or 1),
                "total_connections": info.get("total_connections_received", 0)
            }
        except Exception as e:
            logger.error(f"Error getting Redis stats: {e}")
            return {"status": "error", "message": str(e)}


# Global cache instance
_cache_instance = None

def get_cache() -> RedisCache:
    """
    Get or create the global Redis cache instance.
    
    Returns:
        RedisCache instance
    """
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RedisCache()
    return _cache_instance


def cache_decorator(key_prefix: str, ttl: Optional[int] = None):
    """
    Decorator to cache function results in Redis.
    
    Args:
        key_prefix: Prefix for the cache key
        ttl: Time-to-live in seconds
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Get cache instance
            cache = get_cache()
            
            # Skip caching if disabled
            if not cache.enabled:
                return func(*args, **kwargs)
            
            # Create a cache key based on function arguments
            # First argument is often self/cls, so we skip it
            skip_args = 1 if args and not isinstance(args[0], (int, str, float, bool)) else 0
            
            # Create a string representation of args and kwargs
            args_str = ','.join(str(arg) for arg in args[skip_args:])
            kwargs_str = ','.join(f"{k}={v}" for k, v in sorted(kwargs.items()))
            
            # Combine into a unique cache key
            cache_key = f"{key_prefix}:{func.__name__}:{args_str}:{kwargs_str}"
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cast(T, cached_value)
            
            # Get the actual result and cache it
            result = func(*args, **kwargs)
            
            # Only cache if result is not None
            if result is not None:
                cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    
    return decorator