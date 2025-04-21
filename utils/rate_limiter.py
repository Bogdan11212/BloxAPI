import time
import threading
import logging
import functools
from collections import deque
from flask import request

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Simple rate limiter to prevent hitting Roblox API rate limits
    """
    def __init__(self, max_calls, period):
        """
        Initialize rate limiter
        
        Args:
            max_calls (int): Maximum number of calls allowed in the time period
            period (int): Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
        self.lock = threading.Lock()
        logger.debug(f"Rate limiter initialized: {max_calls} calls per {period} seconds")
    
    def wait_if_needed(self):
        """
        Check if we need to wait before making another API call
        If needed, sleep until we can make the next call
        """
        with self.lock:
            now = time.time()
            
            # Remove calls older than our period
            while self.calls and now - self.calls[0] > self.period:
                self.calls.popleft()
            
            # If we've made too many calls, calculate sleep time
            if len(self.calls) >= self.max_calls:
                sleep_time = self.period - (now - self.calls[0])
                if sleep_time > 0:
                    logger.warning(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
                    time.sleep(sleep_time)
                    # Recalculate now after sleeping
                    now = time.time()
            
            # Record this call
            self.calls.append(now)

# Global rate limiter instances for different API categories
DEFAULT_RATE_LIMITER = RateLimiter(60, 60)  # 60 calls per minute
USER_RATE_LIMITER = RateLimiter(30, 60)     # 30 calls per minute
GAME_RATE_LIMITER = RateLimiter(30, 60)     # 30 calls per minute
GROUP_RATE_LIMITER = RateLimiter(30, 60)    # 30 calls per minute
ASSET_RATE_LIMITER = RateLimiter(30, 60)    # 30 calls per minute

def rate_limited(f=None, limiter=None):
    """
    Decorator to apply rate limiting to API endpoints
    
    Args:
        f (function, optional): Function to decorate. If None, returns a 
                              decorator with the specified parameters.
        limiter (RateLimiter, optional): Rate limiter to use. Defaults to DEFAULT_RATE_LIMITER.
    
    Returns:
        function: Decorated function with rate limiting
    """
    if limiter is None:
        limiter = DEFAULT_RATE_LIMITER
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Apply rate limiting before calling the function
            limiter.wait_if_needed()
            return func(*args, **kwargs)
        return wrapper
    
    if f is None:
        return decorator
    return decorator(f)
