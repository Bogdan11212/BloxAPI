/**
 * Basic usage examples for BloxAPI with JavaScript
 */

// Base URL for your BloxAPI instance
const BASE_URL = 'http://localhost:5000';

/**
 * Get information about a Roblox user
 * @param {number} userId - The Roblox user ID
 * @returns {Promise<Object>} User information
 */
async function getUserInfo(userId) {
  const response = await fetch(`${BASE_URL}/api/users/${userId}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

/**
 * Search for Roblox users by keyword
 * @param {string} keyword - The search keyword
 * @param {number} limit - Maximum number of results (default: 10)
 * @returns {Promise<Object>} Search results
 */
async function searchUsers(keyword, limit = 10) {
  const params = new URLSearchParams({
    keyword,
    limit
  });
  const response = await fetch(`${BASE_URL}/api/users/search?${params}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

/**
 * Get information about a Roblox game by universe ID
 * @param {number} universeId - The Roblox universe ID
 * @returns {Promise<Object>} Game information
 */
async function getGameInfo(universeId) {
  const response = await fetch(`${BASE_URL}/api/games/${universeId}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

/**
 * Get analytics for a Roblox game
 * @param {number} universeId - The Roblox universe ID
 * @param {string} metricType - The metric type (e.g., "visits", "revenue")
 * @param {string} timeFrame - Time frame for analytics (default: "past7days")
 * @returns {Promise<Object>} Game analytics
 */
async function getGameAnalytics(universeId, metricType, timeFrame = 'past7days') {
  const params = new URLSearchParams({
    time_frame: timeFrame
  });
  const url = `${BASE_URL}/api/analytics/games/${universeId}/${metricType}?${params}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

/**
 * Search the Roblox catalog
 * @param {string} keyword - The search keyword
 * @param {string|null} category - Optional category filter
 * @param {number} limit - Maximum number of results (default: 25)
 * @returns {Promise<Object>} Search results
 */
async function searchCatalog(keyword, category = null, limit = 25) {
  const params = new URLSearchParams({
    keyword,
    limit
  });
  if (category) {
    params.append('category', category);
  }
  const response = await fetch(`${BASE_URL}/api/catalog/search?${params}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

/**
 * Get information about a Roblox asset
 * @param {number} assetId - The Roblox asset ID
 * @returns {Promise<Object>} Asset information
 */
async function getAssetInfo(assetId) {
  const response = await fetch(`${BASE_URL}/api/assets/${assetId}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

/**
 * Get information about a Roblox badge
 * @param {number} badgeId - The Roblox badge ID
 * @returns {Promise<Object>} Badge information
 */
async function getBadgeInfo(badgeId) {
  const response = await fetch(`${BASE_URL}/api/badges/${badgeId}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

/**
 * Check moderation status of Roblox content
 * @param {string} contentType - The content type (e.g., "asset", "game")
 * @param {number} contentId - The content ID
 * @returns {Promise<Object>} Moderation status
 */
async function checkContentModeration(contentType, contentId) {
  const url = `${BASE_URL}/api/moderation/content/${contentType}/${contentId}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

/**
 * Run all examples
 */
async function runExamples() {
  try {
    // Get user information for Roblox user ID 1
    console.log('Getting user information for Roblox founder...');
    const userInfo = await getUserInfo(1);
    console.log(userInfo);
    console.log('\n');
    
    // Search for users with keyword "Roblox"
    console.log('Searching for users with keyword "Roblox"...');
    const searchResults = await searchUsers('Roblox', 5);
    console.log(searchResults);
    console.log('\n');
    
    // Get game information for Natural Disaster Survival (189707)
    console.log('Getting game information for Natural Disaster Survival...');
    const gameInfo = await getGameInfo(189707);
    console.log(gameInfo);
    console.log('\n');
    
    // Get visits analytics for the game
    console.log('Getting visits analytics for the game...');
    const analytics = await getGameAnalytics(189707, 'visits');
    console.log(analytics);
    console.log('\n');
    
    // Search for dominus hats in the catalog
    console.log('Searching for dominus hats in the catalog...');
    const catalogResults = await searchCatalog('dominus', 'hats');
    console.log(catalogResults);
    console.log('\n');
    
    // Check moderation status of an asset
    console.log('Checking moderation status of an asset...');
    const moderationStatus = await checkContentModeration('asset', 1818);
    console.log(moderationStatus);
  } catch (error) {
    console.error('Error running examples:', error);
  }
}

// Run the examples if this file is executed directly (e.g., with Node.js)
if (typeof require !== 'undefined' && require.main === module) {
  runExamples();
}

// Export functions if this file is imported as a module
if (typeof module !== 'undefined') {
  module.exports = {
    getUserInfo,
    searchUsers,
    getGameInfo,
    getGameAnalytics,
    searchCatalog,
    getAssetInfo,
    getBadgeInfo,
    checkContentModeration
  };
}