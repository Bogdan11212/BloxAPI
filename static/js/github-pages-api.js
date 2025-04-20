/**
 * BloxAPI - GitHub Pages Version
 * This script provides a client-side API implementation for accessing Roblox data
 * that can be used directly from GitHub Pages without a backend server.
 */

const BloxAPI = {
    baseUrls: {
        users: 'https://users.roblox.com/v1',
        friends: 'https://friends.roblox.com/v1',
        games: 'https://games.roblox.com/v1',
        groups: 'https://groups.roblox.com/v1',
        catalog: 'https://catalog.roblox.com/v1',
        economy: 'https://economy.roblox.com/v1',
        avatar: 'https://avatar.roblox.com/v1',
        inventory: 'https://inventory.roblox.com/v1',
        badges: 'https://badges.roblox.com/v1',
        develop: 'https://develop.roblox.com/v1',
        thumbnails: 'https://thumbnails.roblox.com/v1',
        presence: 'https://presence.roblox.com/v1'
    },

    /**
     * Makes a request to the Roblox API with CORS protection via a proxy
     * @param {string} url - The API endpoint URL
     * @param {Object} options - Request options
     * @returns {Promise<Object>} - API response
     */
    async makeRequest(url, options = {}) {
        try {
            // We're using a CORS proxy to bypass cross-origin restrictions
            // In a production environment, you should use your own proxy
            const corsProxy = 'https://cors-anywhere.herokuapp.com/';
            const response = await fetch(corsProxy + url, {
                method: options.method || 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                body: options.body ? JSON.stringify(options.body) : undefined
            });

            const data = await response.json();
            
            return {
                success: response.ok,
                data: response.ok ? data : null,
                error: !response.ok ? {
                    code: response.status,
                    message: data.message || 'An error occurred'
                } : null
            };
        } catch (error) {
            return {
                success: false,
                data: null,
                error: {
                    code: 500,
                    message: error.message || 'An unexpected error occurred'
                }
            };
        }
    },

    /**
     * User API Methods
     */
    users: {
        /**
         * Get information about a user by their ID
         * @param {number} userId - The Roblox user ID
         * @returns {Promise<Object>} - User data
         */
        async getUser(userId) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.users}/users/${userId}`);
        },

        /**
         * Search for users by keyword
         * @param {string} keyword - The search term
         * @param {number} limit - Maximum number of results
         * @returns {Promise<Object>} - Search results
         */
        async searchUsers(keyword, limit = 10) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.users}/users/search?keyword=${encodeURIComponent(keyword)}&limit=${limit}`);
        },

        /**
         * Get information about multiple users
         * @param {Array<number>} userIds - Array of user IDs
         * @returns {Promise<Object>} - Multiple users data
         */
        async getUsers(userIds) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.users}/users`, {
                method: 'POST',
                body: { userIds }
            });
        }
    },

    /**
     * Friends API Methods
     */
    friends: {
        /**
         * Get a user's friends
         * @param {number} userId - The Roblox user ID
         * @returns {Promise<Object>} - User's friends
         */
        async getFriends(userId) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.friends}/users/${userId}/friends`);
        },

        /**
         * Get a user's friend requests
         * @param {number} userId - The Roblox user ID
         * @returns {Promise<Object>} - User's friend requests
         */
        async getFriendRequests(userId) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.friends}/users/${userId}/friend-requests`);
        }
    },

    /**
     * Games API Methods
     */
    games: {
        /**
         * Get information about a game
         * @param {number} gameId - The Roblox game ID
         * @returns {Promise<Object>} - Game information
         */
        async getGame(gameId) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.games}/games/${gameId}`);
        },

        /**
         * Get detailed information about a game
         * @param {number} gameId - The Roblox game ID
         * @returns {Promise<Object>} - Detailed game information
         */
        async getGameDetails(gameId) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.games}/games/${gameId}/details`);
        },

        /**
         * Get games by user
         * @param {number} userId - The Roblox user ID
         * @param {number} limit - Maximum number of results
         * @returns {Promise<Object>} - List of games
         */
        async getGamesByUser(userId, limit = 50) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.games}/games?userId=${userId}&limit=${limit}`);
        }
    },

    /**
     * Groups API Methods
     */
    groups: {
        /**
         * Get information about a group
         * @param {number} groupId - The Roblox group ID
         * @returns {Promise<Object>} - Group information
         */
        async getGroup(groupId) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.groups}/groups/${groupId}`);
        },

        /**
         * Get members of a group
         * @param {number} groupId - The Roblox group ID
         * @param {number} limit - Maximum number of results
         * @returns {Promise<Object>} - Group members
         */
        async getGroupMembers(groupId, limit = 10) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.groups}/groups/${groupId}/members?limit=${limit}`);
        },

        /**
         * Get roles of a group
         * @param {number} groupId - The Roblox group ID
         * @returns {Promise<Object>} - Group roles
         */
        async getGroupRoles(groupId) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.groups}/groups/${groupId}/roles`);
        }
    },

    /**
     * Avatar API Methods
     */
    avatar: {
        /**
         * Get a user's avatar
         * @param {number} userId - The Roblox user ID
         * @returns {Promise<Object>} - User's avatar
         */
        async getAvatar(userId) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.avatar}/users/${userId}/avatar`);
        },

        /**
         * Get metadata about a user's avatar
         * @param {number} userId - The Roblox user ID
         * @returns {Promise<Object>} - User's avatar metadata
         */
        async getAvatarMeta(userId) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.avatar}/users/${userId}/avatar/metadata`);
        }
    },

    /**
     * Economy API Methods
     */
    economy: {
        /**
         * Get currency exchange rate
         * @returns {Promise<Object>} - Currency exchange rate
         */
        async getExchangeRate() {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.economy}/currency/exchange-rate`);
        },
        
        /**
         * Get resellers of a limited asset
         * @param {number} assetId - The Roblox asset ID
         * @param {number} limit - Maximum number of results
         * @returns {Promise<Object>} - Asset resellers data
         */
        async getAssetResellers(assetId, limit = 10) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.economy}/assets/${assetId}/resellers?limit=${limit}`);
        },
        
        /**
         * Get resale data for a limited asset
         * @param {number} assetId - The Roblox asset ID
         * @returns {Promise<Object>} - Asset resale data
         */
        async getAssetResaleData(assetId) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.economy}/assets/${assetId}/resale-data`);
        },
        
        /**
         * Get a group's revenue summary
         * @param {number} groupId - The Roblox group ID
         * @returns {Promise<Object>} - Group revenue summary
         */
        async getGroupRevenue(groupId) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.economy}/groups/${groupId}/revenue`);
        }
    },
    
    /**
     * Analytics API Methods
     */
    analytics: {
        /**
         * Get analytics for a game
         * @param {number} universeId - The Roblox universe ID
         * @param {string} metricType - The type of metric (e.g., "visits", "revenue", "concurrent", etc.)
         * @param {string} timeFrame - Time frame for analytics (e.g., "past1day", "past7days", "past30days")
         * @returns {Promise<Object>} - Game analytics
         */
        async getGameAnalytics(universeId, metricType, timeFrame = "past30days") {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.develop}/universes/${universeId}/analytics/${metricType}?timeFrame=${timeFrame}`);
        },
        
        /**
         * Get playtime analytics for a game
         * @param {number} universeId - The Roblox universe ID
         * @param {string} startTime - Start time for analytics (format: "YYYY-MM-DD")
         * @param {string} endTime - End time for analytics (format: "YYYY-MM-DD")
         * @returns {Promise<Object>} - Game playtime analytics
         */
        async getGamePlaytime(universeId, startTime, endTime) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.develop}/universes/${universeId}/analytics/playtime?startTime=${startTime}&endTime=${endTime}`);
        }
    },
    
    /**
     * Notifications API Methods
     */
    notifications: {
        /**
         * Get user's notifications
         * @returns {Promise<Object>} - User's notifications
         */
        async getNotifications() {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.users}/notifications`);
        },
        
        /**
         * Get counts of user's notifications by type
         * @returns {Promise<Object>} - Notification counts
         */
        async getNotificationCounts() {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.users}/notifications/counts`);
        }
    },
    
    /**
     * Chat API Methods
     */
    chat: {
        /**
         * Get user's chat conversations
         * @param {number} limit - Maximum number of results
         * @returns {Promise<Object>} - User's chat conversations
         */
        async getConversations(limit = 100) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.friends}/chat/conversations?limit=${limit}`);
        },
        
        /**
         * Get messages from a chat conversation
         * @param {number} conversationId - The conversation ID
         * @param {number} limit - Maximum number of results
         * @returns {Promise<Object>} - Chat messages
         */
        async getMessages(conversationId, limit = 100) {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.friends}/chat/conversations/${conversationId}/messages?limit=${limit}`);
        }
    },

    /**
     * Catalog API Methods
     */
    catalog: {
        /**
         * Get catalog categories
         * @returns {Promise<Object>} - Catalog categories
         */
        async getCategories() {
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.catalog}/categories`);
        },

        /**
         * Search catalog
         * @param {string} keyword - Search term
         * @param {Object} options - Search options
         * @returns {Promise<Object>} - Search results
         */
        async searchCatalog(keyword, options = {}) {
            const queryParams = new URLSearchParams({
                keyword: keyword,
                limit: options.limit || 10,
                ...options
            });
            
            return await BloxAPI.makeRequest(`${BloxAPI.baseUrls.catalog}/search?${queryParams.toString()}`);
        }
    }
};

// Export for use with modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BloxAPI;
}