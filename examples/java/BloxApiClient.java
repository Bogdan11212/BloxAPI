package com.example.bloxapi;

import java.io.IOException;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Client for interacting with the BloxAPI
 */
public class BloxApiClient {
    private final HttpClient httpClient;
    private final String baseUrl;
    private final ObjectMapper objectMapper;
    
    /**
     * Create a new BloxAPI client
     * 
     * @param baseUrl Base URL for the BloxAPI instance
     */
    public BloxApiClient(String baseUrl) {
        this.baseUrl = baseUrl;
        this.httpClient = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_2)
                .connectTimeout(Duration.ofSeconds(10))
                .build();
        this.objectMapper = new ObjectMapper();
    }
    
    /**
     * Create a new BloxAPI client with default base URL
     */
    public BloxApiClient() {
        this("http://localhost:5000");
    }
    
    /**
     * Get information about a Roblox user
     * 
     * @param userId The Roblox user ID
     * @return User information as JsonNode
     * @throws IOException If an I/O error occurs
     * @throws InterruptedException If the operation is interrupted
     */
    public JsonNode getUser(int userId) throws IOException, InterruptedException {
        return get("/api/users/" + userId);
    }
    
    /**
     * Search for Roblox users by keyword
     * 
     * @param keyword The search keyword
     * @param limit Maximum number of results (default: 10)
     * @return Search results as JsonNode
     * @throws IOException If an I/O error occurs
     * @throws InterruptedException If the operation is interrupted
     */
    public JsonNode searchUsers(String keyword, int limit) throws IOException, InterruptedException {
        Map<String, String> params = new HashMap<>();
        params.put("keyword", keyword);
        params.put("limit", String.valueOf(limit));
        
        return get("/api/users/search", params);
    }
    
    /**
     * Get information about a Roblox game by universe ID
     * 
     * @param universeId The Roblox universe ID
     * @return Game information as JsonNode
     * @throws IOException If an I/O error occurs
     * @throws InterruptedException If the operation is interrupted
     */
    public JsonNode getGame(int universeId) throws IOException, InterruptedException {
        return get("/api/games/" + universeId);
    }
    
    /**
     * Get analytics for a Roblox game
     * 
     * @param universeId The Roblox universe ID
     * @param metricType The metric type (e.g., "visits", "revenue")
     * @param timeFrame Time frame for analytics (default: "past7days")
     * @return Game analytics as JsonNode
     * @throws IOException If an I/O error occurs
     * @throws InterruptedException If the operation is interrupted
     */
    public JsonNode getGameAnalytics(int universeId, String metricType, String timeFrame) 
            throws IOException, InterruptedException {
        Map<String, String> params = new HashMap<>();
        params.put("time_frame", timeFrame);
        
        return get("/api/analytics/games/" + universeId + "/" + metricType, params);
    }
    
    /**
     * Search the Roblox catalog
     * 
     * @param keyword The search keyword
     * @param category Optional category filter
     * @param limit Maximum number of results (default: 25)
     * @return Search results as JsonNode
     * @throws IOException If an I/O error occurs
     * @throws InterruptedException If the operation is interrupted
     */
    public JsonNode searchCatalog(String keyword, String category, int limit) 
            throws IOException, InterruptedException {
        Map<String, String> params = new HashMap<>();
        params.put("keyword", keyword);
        params.put("limit", String.valueOf(limit));
        
        if (category != null && !category.isEmpty()) {
            params.put("category", category);
        }
        
        return get("/api/catalog/search", params);
    }
    
    /**
     * Get information about a Roblox asset
     * 
     * @param assetId The Roblox asset ID
     * @return Asset information as JsonNode
     * @throws IOException If an I/O error occurs
     * @throws InterruptedException If the operation is interrupted
     */
    public JsonNode getAsset(int assetId) throws IOException, InterruptedException {
        return get("/api/assets/" + assetId);
    }
    
    /**
     * Get detailed information about a Roblox asset
     * 
     * @param assetId The Roblox asset ID
     * @param includeBundles Whether to include bundles containing this asset
     * @return Detailed asset information as JsonNode
     * @throws IOException If an I/O error occurs
     * @throws InterruptedException If the operation is interrupted
     */
    public JsonNode getAssetInfo(int assetId, boolean includeBundles) 
            throws IOException, InterruptedException {
        Map<String, String> params = new HashMap<>();
        
        if (includeBundles) {
            params.put("include_bundles", "true");
        }
        
        return get("/api/assets/" + assetId + "/info", params);
    }
    
    /**
     * Get information about a Roblox badge
     * 
     * @param badgeId The Roblox badge ID
     * @return Badge information as JsonNode
     * @throws IOException If an I/O error occurs
     * @throws InterruptedException If the operation is interrupted
     */
    public JsonNode getBadge(int badgeId) throws IOException, InterruptedException {
        return get("/api/badges/" + badgeId);
    }
    
    /**
     * Check moderation status of Roblox content
     * 
     * @param contentType The content type (e.g., "asset", "game")
     * @param contentId The content ID
     * @return Moderation status as JsonNode
     * @throws IOException If an I/O error occurs
     * @throws InterruptedException If the operation is interrupted
     */
    public JsonNode checkContentModeration(String contentType, int contentId) 
            throws IOException, InterruptedException {
        return get("/api/moderation/content/" + contentType + "/" + contentId);
    }
    
    /**
     * Make a GET request to the API
     * 
     * @param endpoint API endpoint
     * @return Response as JsonNode
     * @throws IOException If an I/O error occurs
     * @throws InterruptedException If the operation is interrupted
     */
    private JsonNode get(String endpoint) throws IOException, InterruptedException {
        return get(endpoint, null);
    }
    
    /**
     * Make a GET request to the API with query parameters
     * 
     * @param endpoint API endpoint
     * @param params Query parameters
     * @return Response as JsonNode
     * @throws IOException If an I/O error occurs
     * @throws InterruptedException If the operation is interrupted
     */
    private JsonNode get(String endpoint, Map<String, String> params) 
            throws IOException, InterruptedException {
        String url = baseUrl + endpoint;
        
        if (params != null && !params.isEmpty()) {
            String queryString = params.entrySet().stream()
                .map(entry -> URLEncoder.encode(entry.getKey(), StandardCharsets.UTF_8) + "=" + 
                              URLEncoder.encode(entry.getValue(), StandardCharsets.UTF_8))
                .collect(Collectors.joining("&"));
            
            url += "?" + queryString;
        }
        
        HttpRequest request = HttpRequest.newBuilder()
                .GET()
                .uri(URI.create(url))
                .header("Accept", "application/json")
                .build();
        
        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        
        if (response.statusCode() >= 200 && response.statusCode() < 300) {
            return objectMapper.readTree(response.body());
        } else {
            throw new IOException("HTTP error: " + response.statusCode() + " - " + response.body());
        }
    }
    
    /**
     * Example program to demonstrate using the BloxApiClient
     */
    public static void main(String[] args) {
        try {
            BloxApiClient client = new BloxApiClient();
            
            // Get user information for Roblox user ID 1
            System.out.println("Getting user information for Roblox founder...");
            JsonNode userInfo = client.getUser(1);
            System.out.println(userInfo.toPrettyString());
            System.out.println();
            
            // Search for users with keyword "Roblox"
            System.out.println("Searching for users with keyword \"Roblox\"...");
            JsonNode searchResults = client.searchUsers("Roblox", 5);
            System.out.println(searchResults.toPrettyString());
            System.out.println();
            
            // Get game information for Natural Disaster Survival (189707)
            System.out.println("Getting game information for Natural Disaster Survival...");
            JsonNode gameInfo = client.getGame(189707);
            System.out.println(gameInfo.toPrettyString());
            System.out.println();
            
            // Get visits analytics for the game
            System.out.println("Getting visits analytics for the game...");
            JsonNode analytics = client.getGameAnalytics(189707, "visits", "past7days");
            System.out.println(analytics.toPrettyString());
            System.out.println();
            
            // Search for dominus hats in the catalog
            System.out.println("Searching for dominus hats in the catalog...");
            JsonNode catalogResults = client.searchCatalog("dominus", "hats", 25);
            System.out.println(catalogResults.toPrettyString());
            System.out.println();
            
            // Check moderation status of an asset
            System.out.println("Checking moderation status of an asset...");
            JsonNode moderationStatus = client.checkContentModeration("asset", 1818);
            System.out.println(moderationStatus.toPrettyString());
            
        } catch (IOException | InterruptedException e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}