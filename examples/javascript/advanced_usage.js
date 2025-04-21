/**
 * Advanced usage examples for BloxAPI with JavaScript
 * Features:
 * - Class-based client
 * - Error handling
 * - Rate limiting
 * - Request caching
 * - Batch operations
 */

/**
 * BloxAPI Client class for interacting with the BloxAPI
 */
class BloxAPIClient {
  /**
   * Create a new BloxAPI client
   * @param {Object} options - Configuration options
   * @param {string} options.baseUrl - Base URL for the BloxAPI instance
   * @param {number} options.maxRetries - Maximum number of retries (default: 3)
   * @param {boolean} options.enableCache - Enable response caching (default: true)
   * @param {number} options.cacheTTL - Cache time-to-live in milliseconds (default: 1 hour)
   */
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || 'http://localhost:5000';
    this.maxRetries = options.maxRetries || 3;
    this.enableCache = options.enableCache !== undefined ? options.enableCache : true;
    this.cacheTTL = options.cacheTTL || 60 * 60 * 1000; // 1 hour
    this.cache = new Map();
  }

  /**
   * Make a request to the BloxAPI
   * @param {string} method - HTTP method (GET, POST, etc.)
   * @param {string} endpoint - API endpoint (e.g., "/api/users/1")
   * @param {Object} options - Request options
   * @param {Object} options.params - Query parameters
   * @param {Object} options.body - Request body (for POST, PUT, etc.)
   * @param {boolean} options.useCache - Whether to use cache (default: true)
   * @returns {Promise<Object>} Response data
   */
  async request(method, endpoint, options = {}) {
    const { params, body, useCache = true } = options;
    const cacheKey = this.getCacheKey(method, endpoint, params);
    
    // Check cache for GET requests
    if (method === 'GET' && this.enableCache && useCache) {
      const cachedResponse = this.getFromCache(cacheKey);
      if (cachedResponse) {
        return cachedResponse;
      }
    }
    
    // Build request URL with query parameters
    let url = `${this.baseUrl}${endpoint}`;
    if (params) {
      const queryString = new URLSearchParams(params).toString();
      url = `${url}?${queryString}`;
    }
    
    // Configure request options
    const requestOptions = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    };
    
    if (body) {
      requestOptions.body = JSON.stringify(body);
    }
    
    // Make the request with retries
    let response;
    let retries = 0;
    let error;
    
    while (retries <= this.maxRetries) {
      try {
        response = await fetch(url, requestOptions);
        
        if (response.ok) {
          const data = await response.json();
          
          // Cache successful GET responses
          if (method === 'GET' && this.enableCache && useCache) {
            this.saveToCache(cacheKey, data);
          }
          
          return data;
        }
        
        // Handle API error responses
        const errorData = await response.json().catch(() => ({}));
        error = new Error(`API Error: ${response.status} ${response.statusText}`);
        error.status = response.status;
        error.data = errorData;
        
        // Don't retry 4xx errors (except 429 - rate limit)
        if (response.status >= 400 && response.status < 500 && response.status !== 429) {
          throw error;
        }
        
        // For 429 responses, respect Retry-After header if present
        if (response.status === 429) {
          const retryAfter = response.headers.get('Retry-After');
          if (retryAfter) {
            const waitTime = parseInt(retryAfter, 10) * 1000;
            await new Promise(resolve => setTimeout(resolve, waitTime));
          } else {
            await this.exponentialBackoff(retries);
          }
        } else {
          await this.exponentialBackoff(retries);
        }
      } catch (err) {
        error = err;
        await this.exponentialBackoff(retries);
      }
      
      retries++;
    }
    
    // If we've exhausted retries, throw the last error
    throw error || new Error('Request failed after maximum retries');
  }
  
  /**
   * Generate a cache key from method, endpoint, and params
   * @private
   */
  getCacheKey(method, endpoint, params) {
    if (!params) return `${method}:${endpoint}`;
    
    const sortedParams = Object.entries(params)
      .sort(([keyA], [keyB]) => keyA.localeCompare(keyB))
      .map(([key, value]) => `${key}=${value}`)
      .join('&');
      
    return `${method}:${endpoint}:${sortedParams}`;
  }
  
  /**
   * Get cached response data
   * @private
   */
  getFromCache(cacheKey) {
    if (!this.cache.has(cacheKey)) return null;
    
    const { data, timestamp } = this.cache.get(cacheKey);
    const now = Date.now();
    
    // Check if cache is expired
    if (now - timestamp > this.cacheTTL) {
      this.cache.delete(cacheKey);
      return null;
    }
    
    return data;
  }
  
  /**
   * Save response data to cache
   * @private
   */
  saveToCache(cacheKey, data) {
    this.cache.set(cacheKey, {
      data,
      timestamp: Date.now()
    });
  }
  
  /**
   * Implement exponential backoff for retries
   * @private
   */
  async exponentialBackoff(retryCount) {
    const baseDelay = 300; // 300ms
    const maxDelay = 10000; // 10 seconds
    const delay = Math.min(baseDelay * Math.pow(2, retryCount), maxDelay);
    const jitter = delay * 0.2 * Math.random(); // Add up to 20% jitter
    
    await new Promise(resolve => setTimeout(resolve, delay + jitter));
  }
  
  /**
   * Clear the cache
   */
  clearCache() {
    this.cache.clear();
  }
  
  /**
   * Make a GET request
   */
  async get(endpoint, params = null, useCache = true) {
    return this.request('GET', endpoint, { params, useCache });
  }
  
  /**
   * Make a POST request
   */
  async post(endpoint, body = null) {
    return this.request('POST', endpoint, { body, useCache: false });
  }
  
  /**
   * Get information about a Roblox user
   * @param {number} userId - The Roblox user ID
   * @returns {Promise<Object>} User information
   */
  async getUser(userId) {
    return this.get(`/api/users/${userId}`);
  }
  
  /**
   * Get multiple users in a batch
   * @param {number[]} userIds - Array of Roblox user IDs
   * @returns {Promise<Object[]>} Array of user information
   */
  async getUsers(userIds) {
    return Promise.all(userIds.map(userId => this.getUser(userId)));
  }
  
  /**
   * Search for Roblox users by keyword
   * @param {string} keyword - The search keyword
   * @param {number} limit - Maximum number of results (default: 10)
   * @returns {Promise<Object>} Search results
   */
  async searchUsers(keyword, limit = 10) {
    return this.get('/api/users/search', { keyword, limit });
  }
  
  /**
   * Get information about a Roblox game
   * @param {number} universeId - The Roblox universe ID
   * @returns {Promise<Object>} Game information
   */
  async getGame(universeId) {
    return this.get(`/api/games/${universeId}`);
  }
  
  /**
   * Get multiple games in a batch
   * @param {number[]} universeIds - Array of Roblox universe IDs
   * @returns {Promise<Object[]>} Array of game information
   */
  async getGames(universeIds) {
    return Promise.all(universeIds.map(universeId => this.getGame(universeId)));
  }
  
  /**
   * Get analytics for a Roblox game
   * @param {number} universeId - The Roblox universe ID
   * @param {string} metricType - The metric type (e.g., "visits", "revenue")
   * @param {string} timeFrame - Time frame for analytics (default: "past7days")
   * @returns {Promise<Object>} Game analytics
   */
  async getGameAnalytics(universeId, metricType, timeFrame = 'past7days') {
    return this.get(`/api/analytics/games/${universeId}/${metricType}`, { time_frame: timeFrame });
  }
  
  /**
   * Search the Roblox catalog
   * @param {string} keyword - The search keyword
   * @param {string|null} category - Optional category filter
   * @param {number} limit - Maximum number of results (default: 25)
   * @returns {Promise<Object>} Search results
   */
  async searchCatalog(keyword, category = null, limit = 25) {
    const params = { keyword, limit };
    if (category) params.category = category;
    return this.get('/api/catalog/search', params);
  }
  
  /**
   * Get information about a Roblox asset
   * @param {number} assetId - The Roblox asset ID
   * @returns {Promise<Object>} Asset information
   */
  async getAsset(assetId) {
    return this.get(`/api/assets/${assetId}`);
  }
  
  /**
   * Get detailed information about a Roblox asset
   * @param {number} assetId - The Roblox asset ID
   * @param {boolean} includeBundles - Whether to include bundles containing this asset
   * @returns {Promise<Object>} Detailed asset information
   */
  async getAssetInfo(assetId, includeBundles = false) {
    return this.get(`/api/assets/${assetId}/info`, { include_bundles: includeBundles });
  }
  
  /**
   * Get information about a Roblox badge
   * @param {number} badgeId - The Roblox badge ID
   * @returns {Promise<Object>} Badge information
   */
  async getBadge(badgeId) {
    return this.get(`/api/badges/${badgeId}`);
  }
  
  /**
   * Check if a user has a badge
   * @param {number} badgeId - The Roblox badge ID
   * @param {number} userId - The Roblox user ID
   * @returns {Promise<Object>} Badge awarded date information
   */
  async hasBadge(badgeId, userId) {
    return this.get(`/api/badges/${badgeId}/users/${userId}`);
  }
  
  /**
   * Get badges for a game
   * @param {number} universeId - The Roblox universe ID
   * @param {number} limit - Maximum number of results (default: 50)
   * @returns {Promise<Object>} Game badges
   */
  async getGameBadges(universeId, limit = 50) {
    return this.get(`/api/games/${universeId}/badges`, { limit });
  }
  
  /**
   * Check moderation status of Roblox content
   * @param {string} contentType - The content type (e.g., "asset", "game")
   * @param {number} contentId - The content ID
   * @returns {Promise<Object>} Moderation status
   */
  async checkContentModeration(contentType, contentId) {
    return this.get(`/api/moderation/content/${contentType}/${contentId}`);
  }
}

/**
 * Run examples to demonstrate the advanced client
 */
async function runExamples() {
  // Create a client with custom options
  const client = new BloxAPIClient({
    baseUrl: 'http://localhost:5000',
    maxRetries: 3,
    enableCache: true,
    cacheTTL: 30 * 60 * 1000 // 30 minutes
  });
  
  try {
    console.log('Getting user information (will be cached)...');
    const userInfo = await client.getUser(1);
    console.log(userInfo);
    console.log('\n');
    
    console.log('Getting the same user again (from cache)...');
    const cachedUserInfo = await client.getUser(1);
    console.log('Cached data retrieved successfully');
    console.log('\n');
    
    console.log('Getting information for multiple users in parallel...');
    const users = await client.getUsers([1, 2, 3, 4, 5]);
    console.log(`Retrieved ${users.length} users`);
    console.log('\n');
    
    console.log('Searching the catalog...');
    const catalogResults = await client.searchCatalog('dominus', 'hats', 5);
    console.log(catalogResults);
    console.log('\n');
    
    console.log('Getting game information...');
    const gameInfo = await client.getGame(189707);
    console.log(gameInfo);
    console.log('\n');
    
    console.log('Getting game analytics...');
    const analytics = await client.getGameAnalytics(189707, 'visits', 'past30days');
    console.log(analytics);
    console.log('\n');
    
    console.log('Clearing cache...');
    client.clearCache();
    console.log('Cache cleared');
    
  } catch (error) {
    console.error('Error running examples:');
    console.error(`Status: ${error.status || 'Unknown'}`);
    console.error(`Message: ${error.message}`);
    if (error.data) {
      console.error('Error details:', error.data);
    }
  }
}

// Run the examples if this file is executed directly (e.g., with Node.js)
if (typeof require !== 'undefined' && require.main === module) {
  runExamples();
}

// Export the client class if this file is imported as a module
if (typeof module !== 'undefined') {
  module.exports = {
    BloxAPIClient
  };
}