using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace BloxApiExample
{
    /// <summary>
    /// Client for interacting with the BloxAPI
    /// </summary>
    public class BloxApiClient
    {
        private readonly HttpClient _httpClient;
        private readonly string _baseUrl;
        private readonly JsonSerializerOptions _jsonOptions;

        /// <summary>
        /// Create a new BloxAPI client
        /// </summary>
        /// <param name="baseUrl">Base URL for the BloxAPI instance</param>
        public BloxApiClient(string baseUrl = "http://localhost:5000")
        {
            _baseUrl = baseUrl;
            _httpClient = new HttpClient();
            _httpClient.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));
                
            _jsonOptions = new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                WriteIndented = true
            };
        }

        /// <summary>
        /// Get information about a Roblox user
        /// </summary>
        /// <param name="userId">The Roblox user ID</param>
        /// <returns>User information</returns>
        public async Task<JsonElement> GetUserAsync(int userId)
        {
            return await GetAsync($"/api/users/{userId}");
        }

        /// <summary>
        /// Search for Roblox users by keyword
        /// </summary>
        /// <param name="keyword">The search keyword</param>
        /// <param name="limit">Maximum number of results (default: 10)</param>
        /// <returns>Search results</returns>
        public async Task<JsonElement> SearchUsersAsync(string keyword, int limit = 10)
        {
            var queryParams = new Dictionary<string, string>
            {
                { "keyword", keyword },
                { "limit", limit.ToString() }
            };
            
            return await GetAsync("/api/users/search", queryParams);
        }

        /// <summary>
        /// Get information about a Roblox game by universe ID
        /// </summary>
        /// <param name="universeId">The Roblox universe ID</param>
        /// <returns>Game information</returns>
        public async Task<JsonElement> GetGameAsync(int universeId)
        {
            return await GetAsync($"/api/games/{universeId}");
        }

        /// <summary>
        /// Get analytics for a Roblox game
        /// </summary>
        /// <param name="universeId">The Roblox universe ID</param>
        /// <param name="metricType">The metric type (e.g., "visits", "revenue")</param>
        /// <param name="timeFrame">Time frame for analytics (default: "past7days")</param>
        /// <returns>Game analytics</returns>
        public async Task<JsonElement> GetGameAnalyticsAsync(int universeId, string metricType, string timeFrame = "past7days")
        {
            var queryParams = new Dictionary<string, string>
            {
                { "time_frame", timeFrame }
            };
            
            return await GetAsync($"/api/analytics/games/{universeId}/{metricType}", queryParams);
        }

        /// <summary>
        /// Search the Roblox catalog
        /// </summary>
        /// <param name="keyword">The search keyword</param>
        /// <param name="category">Optional category filter</param>
        /// <param name="limit">Maximum number of results (default: 25)</param>
        /// <returns>Search results</returns>
        public async Task<JsonElement> SearchCatalogAsync(string keyword, string category = null, int limit = 25)
        {
            var queryParams = new Dictionary<string, string>
            {
                { "keyword", keyword },
                { "limit", limit.ToString() }
            };
            
            if (!string.IsNullOrEmpty(category))
            {
                queryParams.Add("category", category);
            }
            
            return await GetAsync("/api/catalog/search", queryParams);
        }

        /// <summary>
        /// Get information about a Roblox asset
        /// </summary>
        /// <param name="assetId">The Roblox asset ID</param>
        /// <returns>Asset information</returns>
        public async Task<JsonElement> GetAssetAsync(int assetId)
        {
            return await GetAsync($"/api/assets/{assetId}");
        }

        /// <summary>
        /// Get detailed information about a Roblox asset
        /// </summary>
        /// <param name="assetId">The Roblox asset ID</param>
        /// <param name="includeBundles">Whether to include bundles containing this asset</param>
        /// <returns>Detailed asset information</returns>
        public async Task<JsonElement> GetAssetInfoAsync(int assetId, bool includeBundles = false)
        {
            var queryParams = new Dictionary<string, string>();
            
            if (includeBundles)
            {
                queryParams.Add("include_bundles", "true");
            }
            
            return await GetAsync($"/api/assets/{assetId}/info", queryParams);
        }

        /// <summary>
        /// Get information about a Roblox badge
        /// </summary>
        /// <param name="badgeId">The Roblox badge ID</param>
        /// <returns>Badge information</returns>
        public async Task<JsonElement> GetBadgeAsync(int badgeId)
        {
            return await GetAsync($"/api/badges/{badgeId}");
        }

        /// <summary>
        /// Check moderation status of Roblox content
        /// </summary>
        /// <param name="contentType">The content type (e.g., "asset", "game")</param>
        /// <param name="contentId">The content ID</param>
        /// <returns>Moderation status</returns>
        public async Task<JsonElement> CheckContentModerationAsync(string contentType, int contentId)
        {
            return await GetAsync($"/api/moderation/content/{contentType}/{contentId}");
        }

        /// <summary>
        /// Make a GET request to the API
        /// </summary>
        /// <param name="endpoint">API endpoint</param>
        /// <param name="queryParams">Optional query parameters</param>
        /// <returns>Response as JsonElement</returns>
        private async Task<JsonElement> GetAsync(string endpoint, Dictionary<string, string> queryParams = null)
        {
            string url = $"{_baseUrl}{endpoint}";
            
            if (queryParams != null && queryParams.Count > 0)
            {
                var queryString = new StringBuilder("?");
                foreach (var param in queryParams)
                {
                    if (queryString.Length > 1)
                    {
                        queryString.Append("&");
                    }
                    queryString.Append($"{Uri.EscapeDataString(param.Key)}={Uri.EscapeDataString(param.Value)}");
                }
                url += queryString.ToString();
            }
            
            HttpResponseMessage response = await _httpClient.GetAsync(url);
            response.EnsureSuccessStatusCode();
            
            string responseBody = await response.Content.ReadAsStringAsync();
            return JsonDocument.Parse(responseBody).RootElement;
        }
    }
    
    /// <summary>
    /// Example program to demonstrate using the BloxApiClient
    /// </summary>
    public class Program
    {
        public static async Task Main(string[] args)
        {
            // Create a client
            var client = new BloxApiClient("http://localhost:5000");
            
            try
            {
                // Get user information for Roblox user ID 1
                Console.WriteLine("Getting user information for Roblox founder...");
                var userInfo = await client.GetUserAsync(1);
                Console.WriteLine(JsonSerializer.Serialize(userInfo, new JsonSerializerOptions { WriteIndented = true }));
                Console.WriteLine();
                
                // Search for users with keyword "Roblox"
                Console.WriteLine("Searching for users with keyword \"Roblox\"...");
                var searchResults = await client.SearchUsersAsync("Roblox", 5);
                Console.WriteLine(JsonSerializer.Serialize(searchResults, new JsonSerializerOptions { WriteIndented = true }));
                Console.WriteLine();
                
                // Get game information for Natural Disaster Survival (189707)
                Console.WriteLine("Getting game information for Natural Disaster Survival...");
                var gameInfo = await client.GetGameAsync(189707);
                Console.WriteLine(JsonSerializer.Serialize(gameInfo, new JsonSerializerOptions { WriteIndented = true }));
                Console.WriteLine();
                
                // Get visits analytics for the game
                Console.WriteLine("Getting visits analytics for the game...");
                var analytics = await client.GetGameAnalyticsAsync(189707, "visits");
                Console.WriteLine(JsonSerializer.Serialize(analytics, new JsonSerializerOptions { WriteIndented = true }));
                Console.WriteLine();
                
                // Search for dominus hats in the catalog
                Console.WriteLine("Searching for dominus hats in the catalog...");
                var catalogResults = await client.SearchCatalogAsync("dominus", "hats");
                Console.WriteLine(JsonSerializer.Serialize(catalogResults, new JsonSerializerOptions { WriteIndented = true }));
                Console.WriteLine();
                
                // Check moderation status of an asset
                Console.WriteLine("Checking moderation status of an asset...");
                var moderationStatus = await client.CheckContentModerationAsync("asset", 1818);
                Console.WriteLine(JsonSerializer.Serialize(moderationStatus, new JsonSerializerOptions { WriteIndented = true }));
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine($"Error making API request: {e.Message}");
            }
            catch (JsonException e)
            {
                Console.WriteLine($"Error parsing JSON response: {e.Message}");
            }
            catch (Exception e)
            {
                Console.WriteLine($"Unexpected error: {e.Message}");
            }
        }
    }
}