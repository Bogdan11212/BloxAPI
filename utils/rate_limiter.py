import time
import threading
import logging
from collections import deque

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
