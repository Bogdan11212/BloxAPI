"""
SDK Generator for BloxAPI

This module provides functionality to automatically generate SDKs
for different programming languages based on the BloxAPI endpoints.
It parses the route definitions and generates appropriate client code.
"""

import inspect
import re
import os
import json
import logging
from typing import Dict, List, Any, Set, Optional, Callable, Tuple, Union
from pathlib import Path
import importlib
import pkgutil
import routes

# Configure logging
logger = logging.getLogger(__name__)

# Supported languages and their templates
SUPPORTED_LANGUAGES = {
    "python": "py",
    "javascript": "js",
    "typescript": "ts",
    "csharp": "cs",
    "java": "java",
    "go": "go",
    "php": "php",
    "ruby": "rb"
}

class EndpointInfo:
    """Information about an API endpoint"""
    
    def __init__(self, route: str, method: str, handler: Callable, 
                 route_params: List[str], query_params: Dict[str, Any],
                 docstring: str, resource_class: str, module_name: str):
        """
        Initialize endpoint information
        
        Args:
            route: API route path
            method: HTTP method (GET, POST, etc.)
            handler: Function that handles the endpoint
            route_params: List of route parameters
            query_params: Dictionary of query parameters and their info
            docstring: Extracted docstring
            resource_class: Name of the resource class
            module_name: Name of the module containing the endpoint
        """
        self.route = route
        self.method = method
        self.handler = handler
        self.route_params = route_params
        self.query_params = query_params
        self.docstring = docstring
        self.description = self._extract_description()
        self.return_info = self._extract_return_info()
        self.resource_class = resource_class
        self.module_name = module_name
        self.category = self._extract_category()
    
    def _extract_description(self) -> str:
        """Extract description from docstring"""
        if not self.docstring:
            return ""
        
        # Extract the first paragraph (description)
        match = re.search(r'\s*(.+?)(?:\n\s*\n|\n\s*Args:|\n\s*Parameters:|\n\s*Returns:|\Z)', 
                          self.docstring, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    def _extract_return_info(self) -> Dict[str, str]:
        """Extract return information from docstring"""
        if not self.docstring:
            return {}
        
        # Extract the returns section
        match = re.search(r'Returns:\s*(.+?)(?:\n\s*\n|\Z)', self.docstring, re.DOTALL)
        if match:
            return_text = match.group(1).strip()
            
            # Try to extract type and description
            type_match = re.search(r'(\w+(?:\[.+\])?|dict|list):\s*(.+)', return_text)
            if type_match:
                return {
                    "type": type_match.group(1),
                    "description": type_match.group(2).strip()
                }
            
            return {"description": return_text}
        
        return {}
    
    def _extract_category(self) -> str:
        """Extract API category from module name"""
        # Remove 'routes.' prefix and convert to title case
        if self.module_name.startswith('routes.'):
            return self.module_name[7:].replace('_', ' ').title()
        return self.module_name.replace('_', ' ').title()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for SDK generation"""
        return {
            "route": self.route,
            "method": self.method,
            "route_params": self.route_params,
            "query_params": self.query_params,
            "description": self.description,
            "returns": self.return_info,
            "resource_class": self.resource_class,
            "module_name": self.module_name,
            "category": self.category,
            "function_name": self._generate_function_name()
        }
    
    def _generate_function_name(self) -> str:
        """Generate a function name for this endpoint"""
        # Start with the HTTP method
        name_parts = []
        
        # Extract resource type from the route
        route_parts = self.route.split('/')
        resource_type = None
        
        for part in route_parts:
            if part and not part.startswith('<') and not part.startswith('api'):
                resource_type = part
                break
        
        if resource_type:
            name_parts.append(resource_type)
        
        # Add any identifier parts
        for part in route_parts:
            if part.startswith('<') and part.endswith('>'):
                # Extract the parameter name (e.g., <int:user_id> -> user)
                param_name = part[part.find(':')+1:part.find('_id')].strip() if ':' in part else part[1:-3].strip()
                if param_name and param_name not in name_parts:
                    name_parts.append(param_name)
        
        # Join with underscores and convert to lowercase
        base_name = '_'.join(name_parts).lower()
        
        # Prefix with HTTP method
        if self.method.lower() == 'get':
            if 'search' in self.route.lower():
                return f"search_{base_name}"
            return f"get_{base_name}"
        elif self.method.lower() == 'post':
            return f"create_{base_name}"
        elif self.method.lower() == 'put':
            return f"update_{base_name}"
        elif self.method.lower() == 'delete':
            return f"delete_{base_name}"
        
        # Default
        return f"{self.method.lower()}_{base_name}"


class SDKGenerator:
    """Generate SDKs for different programming languages"""
    
    def __init__(self, api_version: str = "v2", base_url: str = "https://api.bloxapi.com"):
        """
        Initialize the SDK generator
        
        Args:
            api_version: API version to use in the SDK
            base_url: Base URL for API requests
        """
        self.api_version = api_version
        self.base_url = base_url
        self.endpoints: List[EndpointInfo] = []
        self.output_dir = Path("sdks")
        
        # Templates directory
        self.templates_dir = Path("utils/templates")
        if not self.templates_dir.exists():
            self.templates_dir = Path("templates")
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load templates
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load SDK templates for all supported languages"""
        self.templates = {}
        
        for lang, ext in SUPPORTED_LANGUAGES.items():
            template_file = self.templates_dir / f"sdk_template.{ext}"
            if template_file.exists():
                with open(template_file, 'r') as f:
                    self.templates[lang] = f.read()
            else:
                logger.warning(f"Template file not found for {lang}: {template_file}")
                # Use default template
                self.templates[lang] = self._get_default_template(lang)
    
    def _get_default_template(self, language: str) -> str:
        """Get a default template for the given language"""
        if language == "python":
            return '''"""
BloxAPI Python SDK {version}

This SDK provides a Python interface to the BloxAPI.
Generated automatically from the API specification.
"""

import requests
import json
from typing import Dict, List, Any, Optional, Union

class BloxAPI:
    """Client for the BloxAPI"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "{base_url}"):
        """
        Initialize the BloxAPI client
        
        Args:
            api_key: Optional API key for authenticated requests
            base_url: Base URL for API requests
        """
        self.api_key = api_key
        self.base_url = base_url
        
        # Create API category clients
        {category_clients}
    
    def _request(self, method: str, endpoint: str, params: Dict[str, Any] = None, 
                data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make an API request
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=data,
            headers=headers
        )
        
        response.raise_for_status()
        
        if response.content:
            return response.json()
        return {}

{category_classes}
'''
        elif language == "javascript":
            return '''/**
 * BloxAPI JavaScript SDK {version}
 *
 * This SDK provides a JavaScript interface to the BloxAPI.
 * Generated automatically from the API specification.
 */

class BloxAPI {
    /**
     * Initialize the BloxAPI client
     * 
     * @param {string} [apiKey] - Optional API key for authenticated requests
     * @param {string} [baseUrl="{base_url}"] - Base URL for API requests
     */
    constructor(apiKey = null, baseUrl = "{base_url}") {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
        
        // Create API category clients
        {category_clients}
    }
    
    /**
     * Make an API request
     * 
     * @param {string} method - HTTP method
     * @param {string} endpoint - API endpoint
     * @param {Object} [params=null] - Query parameters
     * @param {Object} [data=null] - Request body data
     * @returns {Promise<Object>} - API response as a Promise
     */
    async _request(method, endpoint, params = null, data = null) {
        const url = `${this.baseUrl}/${endpoint}`;
        const headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        };
        
        if (this.apiKey) {
            headers["Authorization"] = `Bearer ${this.apiKey}`;
        }
        
        const options = {
            method,
            headers
        };
        
        // Add query parameters to URL if provided
        if (params) {
            const queryParams = new URLSearchParams();
            for (const [key, value] of Object.entries(params)) {
                if (value !== null && value !== undefined) {
                    queryParams.append(key, value);
                }
            }
            const queryString = queryParams.toString();
            if (queryString) {
                url += `?${queryString}`;
            }
        }
        
        // Add request body if provided
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        
        if (response.headers.get("content-length") === "0") {
            return {};
        }
        
        return await response.json();
    }
}

{category_classes}

export default BloxAPI;
'''
        elif language == "typescript":
            return '''/**
 * BloxAPI TypeScript SDK {version}
 *
 * This SDK provides a TypeScript interface to the BloxAPI.
 * Generated automatically from the API specification.
 */

{interfaces}

export class BloxAPI {
    private apiKey: string | null;
    private baseUrl: string;
    
    {category_properties}
    
    /**
     * Initialize the BloxAPI client
     * 
     * @param apiKey - Optional API key for authenticated requests
     * @param baseUrl - Base URL for API requests
     */
    constructor(apiKey: string | null = null, baseUrl: string = "{base_url}") {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
        
        // Create API category clients
        {category_clients}
    }
    
    /**
     * Make an API request
     * 
     * @param method - HTTP method
     * @param endpoint - API endpoint
     * @param params - Query parameters
     * @param data - Request body data
     * @returns API response as a Promise
     */
    private async _request<T>(
        method: string, 
        endpoint: string, 
        params: Record<string, any> | null = null, 
        data: Record<string, any> | null = null
    ): Promise<T> {
        let url = `${this.baseUrl}/${endpoint}`;
        const headers: HeadersInit = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        };
        
        if (this.apiKey) {
            headers["Authorization"] = `Bearer ${this.apiKey}`;
        }
        
        const options: RequestInit = {
            method,
            headers
        };
        
        // Add query parameters to URL if provided
        if (params) {
            const queryParams = new URLSearchParams();
            for (const [key, value] of Object.entries(params)) {
                if (value !== null && value !== undefined) {
                    queryParams.append(key, String(value));
                }
            }
            const queryString = queryParams.toString();
            if (queryString) {
                url += `?${queryString}`;
            }
        }
        
        // Add request body if provided
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        
        if (response.headers.get("content-length") === "0") {
            return {} as T;
        }
        
        return await response.json() as T;
    }
}

{category_classes}

export default BloxAPI;
'''
        elif language == "csharp":
            return '''using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace BloxAPI
{
    /// <summary>
    /// BloxAPI C# SDK {version}
    ///
    /// This SDK provides a C# interface to the BloxAPI.
    /// Generated automatically from the API specification.
    /// </summary>
    public class BloxApiClient
    {
        private readonly HttpClient _httpClient;
        private readonly string _apiKey;
        
        {category_properties}
        
        /// <summary>
        /// Initialize the BloxAPI client
        /// </summary>
        /// <param name="apiKey">Optional API key for authenticated requests</param>
        /// <param name="baseUrl">Base URL for API requests</param>
        public BloxApiClient(string apiKey = null, string baseUrl = "{base_url}")
        {
            _apiKey = apiKey;
            _httpClient = new HttpClient
            {
                BaseAddress = new Uri(baseUrl)
            };
            
            _httpClient.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));
                
            if (!string.IsNullOrEmpty(apiKey))
            {
                _httpClient.DefaultRequestHeaders.Authorization = 
                    new AuthenticationHeaderValue("Bearer", apiKey);
            }
            
            // Create API category clients
            {category_clients}
        }
        
        /// <summary>
        /// Make an API request
        /// </summary>
        /// <typeparam name="T">Response type</typeparam>
        /// <param name="method">HTTP method</param>
        /// <param name="endpoint">API endpoint</param>
        /// <param name="queryParams">Query parameters</param>
        /// <param name="data">Request body data</param>
        /// <returns>API response</returns>
        private async Task<T> RequestAsync<T>(
            HttpMethod method, 
            string endpoint, 
            Dictionary<string, string> queryParams = null, 
            object data = null)
        {
            var requestUri = endpoint;
            
            // Add query parameters
            if (queryParams != null && queryParams.Count > 0)
            {
                var queryString = new StringBuilder("?");
                foreach (var param in queryParams)
                {
                    if (param.Value != null)
                    {
                        queryString.Append($"{Uri.EscapeDataString(param.Key)}={Uri.EscapeDataString(param.Value)}&");
                    }
                }
                requestUri += queryString.ToString().TrimEnd('&');
            }
            
            var request = new HttpRequestMessage(method, requestUri);
            
            // Add request body
            if (data != null)
            {
                var json = JsonSerializer.Serialize(data);
                request.Content = new StringContent(json, Encoding.UTF8, "application/json");
            }
            
            // Send request
            var response = await _httpClient.SendAsync(request);
            
            // Ensure success
            response.EnsureSuccessStatusCode();
            
            // Parse response
            if (response.Content.Headers.ContentLength > 0)
            {
                var content = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<T>(content, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });
            }
            
            return default;
        }
    }
    
{category_classes}
}
'''
        # Add more default templates for other languages as needed
        return ""
    
    def parse_routes(self) -> None:
        """Parse all API routes to extract endpoint information"""
        self.endpoints = []
        
        # Get all modules in routes package
        routes_package = routes
        routes_path = routes_package.__path__
        
        # Find and process all API resource classes
        for _, module_name, _ in pkgutil.iter_modules(routes_path):
            full_module_name = f"routes.{module_name}"
            
            try:
                module = importlib.import_module(full_module_name)
                
                # Find all resource classes in the module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and hasattr(obj, 'get') or hasattr(obj, 'post') or 
                        hasattr(obj, 'put') or hasattr(obj, 'delete')):
                        
                        # Process resource class
                        self._process_resource_class(obj, name, full_module_name)
            
            except ImportError as e:
                logger.error(f"Error importing module {full_module_name}: {e}")
    
    def _process_resource_class(self, cls, class_name: str, module_name: str) -> None:
        """
        Process a resource class to extract endpoint information
        
        Args:
            cls: The resource class
            class_name: Name of the class
            module_name: Name of the module containing the class
        """
        # Get routes registered for this resource class from app.py imports
        routes = self._find_routes_for_class(class_name)
        
        if not routes:
            logger.warning(f"No routes found for class {class_name}")
            return
        
        # Process HTTP methods
        for method_name in ['get', 'post', 'put', 'delete']:
            if hasattr(cls, method_name):
                method = getattr(cls, method_name)
                
                # Extract docstring
                docstring = inspect.getdoc(method)
                
                # Extract route parameters
                for route in routes:
                    route_params = re.findall(r'<(?:int|string|float)?:?([^>]+)>', route)
                    
                    # Extract query parameters from docstring
                    query_params = self._extract_query_params(docstring)
                    
                    # Create endpoint info
                    endpoint = EndpointInfo(
                        route=route,
                        method=method_name.upper(),
                        handler=method,
                        route_params=route_params,
                        query_params=query_params,
                        docstring=docstring,
                        resource_class=class_name,
                        module_name=module_name
                    )
                    
                    self.endpoints.append(endpoint)
    
    def _find_routes_for_class(self, class_name: str) -> List[str]:
        """
        Find API routes for a resource class
        
        Args:
            class_name: Name of the resource class
            
        Returns:
            List of routes for this class
        """
        # TODO: Extract this from app.py's api.add_resource calls
        # For now, stub method to estimate routes based on class names
        
        # Convert ResourceClassName to resource_name
        words = re.findall(r'[A-Z][a-z]*', class_name.replace("Resource", ""))
        resource_name = '_'.join([w.lower() for w in words])
        
        routes = []
        
        # Check common patterns
        if "details" in resource_name.lower():
            # e.g., "/api/users/<int:user_id>/details"
            base_resource = resource_name.lower().replace("_details", "")
            routes.append(f"/api/{base_resource}s/<int:{base_resource}_id>/details")
        elif "list" in resource_name.lower():
            # e.g., "/api/games"
            base_resource = resource_name.lower().replace("_list", "")
            routes.append(f"/api/{base_resource}s")
        elif "search" in resource_name.lower():
            # e.g., "/api/users/search"
            base_resource = resource_name.lower().replace("_search", "")
            routes.append(f"/api/{base_resource}s/search")
        elif len(words) > 1:
            # e.g., "/api/game_passes/<int:game_pass_id>"
            if "user" in words[0].lower():
                routes.append(f"/api/users/<int:user_id>/{words[1].lower()}")
            else:
                parent = words[0].lower()
                child = words[1].lower()
                routes.append(f"/api/{parent}s/<int:{parent}_id>/{child}s")
        else:
            # Basic resource, e.g., "/api/users/<int:user_id>"
            routes.append(f"/api/{resource_name}s/<int:{resource_name}_id>")
        
        return routes
    
    def _extract_query_params(self, docstring: str) -> Dict[str, Dict[str, str]]:
        """
        Extract query parameters from a docstring
        
        Args:
            docstring: Method docstring
            
        Returns:
            Dictionary of query parameters
        """
        if not docstring:
            return {}
        
        query_params = {}
        
        # Find the Args/Parameters section
        match = re.search(r'(?:Args|Parameters):(.*?)(?:\n\s*\n|\n\s*Returns:|\Z)', 
                         docstring, re.DOTALL)
        
        if not match:
            return {}
        
        # Parse parameters
        params_text = match.group(1)
        param_matches = re.finditer(r'\s+(\w+)(?:\s+\(([^)]+)\))?:\s*(.+?)(?=\n\s+\w+:|$)', 
                                   params_text, re.DOTALL)
        
        for param_match in param_matches:
            name = param_match.group(1)
            type_info = param_match.group(2) if param_match.group(2) else None
            description = param_match.group(3).strip()
            
            # Check if this is a query parameter
            if name not in ["self", "cls"] and "url" in description.lower() or "optional" in description.lower():
                param_info = {
                    "description": description
                }
                
                if type_info:
                    param_info["type"] = type_info
                
                # Check if required
                param_info["required"] = "required" in description.lower()
                
                query_params[name] = param_info
        
        return query_params
    
    def generate_sdk(self, language: str) -> str:
        """
        Generate SDK code for the specified language
        
        Args:
            language: Programming language to generate SDK for
            
        Returns:
            Generated SDK code
        """
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")
        
        if not self.endpoints:
            self.parse_routes()
        
        # Group endpoints by category
        categories = {}
        for endpoint in self.endpoints:
            category = endpoint.category
            if category not in categories:
                categories[category] = []
            categories[category].append(endpoint.to_dict())
        
        # Get template for language
        template = self.templates.get(language, "")
        if not template:
            raise ValueError(f"No template available for {language}")
        
        # Generate category classes
        category_classes = []
        category_clients = []
        category_properties = []
        
        for category, endpoints in categories.items():
            category_snake = self._to_snake_case(category)
            category_camel = self._to_camel_case(category)
            category_class = f"{category_camel}Client"
            
            # Generate methods for each endpoint
            methods = []
            for endpoint in endpoints:
                methods.append(self._generate_method(endpoint, language))
            
            # Generate category class
            if language == "python":
                category_classes.append(f"""
class {category_class}:
    \"\"\"Client for {category} API endpoints\"\"\"
    
    def __init__(self, api):
        \"\"\"
        Initialize the {category} client
        
        Args:
            api: BloxAPI client
        \"\"\"
        self.api = api
    
    {self._indent(self._join_methods(methods), 4)}
""")
                category_clients.append(f"self.{category_snake} = {category_class}(self)")
            
            elif language == "javascript":
                category_classes.append(f"""
/**
 * Client for {category} API endpoints
 */
class {category_class} {{
    /**
     * Initialize the {category} client
     * 
     * @param {{BloxAPI}} api - BloxAPI client
     */
    constructor(api) {{
        this.api = api;
    }}
    
    {self._indent(self._join_methods(methods), 4)}
}}

BloxAPI.prototype.{category_snake} = function() {{
    return new {category_class}(this);
}};
""")
                category_clients.append(f"this.{category_snake} = new {category_class}(this);")
            
            elif language == "typescript":
                category_classes.append(f"""
/**
 * Client for {category} API endpoints
 */
export class {category_class} {{
    private api: BloxAPI;
    
    /**
     * Initialize the {category} client
     * 
     * @param api - BloxAPI client
     */
    constructor(api: BloxAPI) {{
        this.api = api;
    }}
    
    {self._indent(self._join_methods(methods), 4)}
}}

BloxAPI.prototype.{category_snake} = function(): {category_class} {{
    return new {category_class}(this);
}};
""")
                category_properties.append(f"public {category_snake}: {category_class};")
                category_clients.append(f"this.{category_snake} = new {category_class}(this);")
            
            elif language == "csharp":
                category_classes.append(f"""
    /// <summary>
    /// Client for {category} API endpoints
    /// </summary>
    public class {category_class}
    {{
        private readonly BloxApiClient _client;
        
        /// <summary>
        /// Initialize the {category} client
        /// </summary>
        /// <param name="client">BloxAPI client</param>
        public {category_class}(BloxApiClient client)
        {{
            _client = client;
        }}
        
        {self._indent(self._join_methods(methods), 8)}
    }}
""")
                category_properties.append(f"public {category_class} {category_camel} {{ get; }}");
                category_clients.append(f"{category_camel} = new {category_class}(this);")
            
            # Add more language-specific implementations as needed
        
        # Generate TypeScript interfaces (for TS only)
        interfaces = ""
        if language == "typescript":
            # TODO: Generate TypeScript interfaces
            pass
        
        # Replace template placeholders
        rendered = template.format(
            version=self.api_version,
            base_url=self.base_url,
            category_classes='\n'.join(category_classes),
            category_clients='\n        '.join(category_clients),
            category_properties='\n    '.join(category_properties),
            interfaces=interfaces
        )
        
        return rendered
    
    def _generate_method(self, endpoint: Dict[str, Any], language: str) -> str:
        """
        Generate a method for an endpoint in the specified language
        
        Args:
            endpoint: Endpoint information
            language: Programming language
            
        Returns:
            Generated method code
        """
        method_name = endpoint["function_name"]
        http_method = endpoint["method"].lower()
        route = endpoint["route"]
        description = endpoint["description"]
        route_params = endpoint["route_params"]
        query_params = endpoint["query_params"]
        
        # Generate route path with parameters
        path = route
        for param in route_params:
            path = path.replace(f"<int:{param}>", f"{{{param}}}")
            path = path.replace(f"<string:{param}>", f"{{{param}}}")
            path = path.replace(f"<float:{param}>", f"{{{param}}}")
            path = path.replace(f"<{param}>", f"{{{param}}}")
        
        # Remove leading /api prefix
        if path.startswith("/api/"):
            path = path[5:]
        
        if language == "python":
            params = []
            doc_params = []
            method_params = ["self"]
            
            # Add route parameters
            for param in route_params:
                params.append(f"{param}: int")
                doc_params.append(f"            {param} (int): Parameter description")
                method_params.append(param)
            
            # Add query parameters
            for name, info in query_params.items():
                param_type = info.get("type", "str")
                if not info.get("required", False):
                    params.append(f"{name}: Optional[{param_type}] = None")
                else:
                    params.append(f"{name}: {param_type}")
                
                doc_params.append(f"            {name} ({param_type}): {info.get('description', 'Parameter description')}")
                method_params.append(name)
            
            # Generate method signature
            signature = f"def {method_name}({', '.join(method_params)}):"
            
            # Generate docstring
            docstring = f'"""'
            if description:
                docstring += f"\n        {description}"
            
            if doc_params:
                docstring += "\n        \n        Args:\n"
                docstring += "\n".join(doc_params)
            
            docstring += "\n        \n        Returns:\n            dict: API response\n        \"\"\""
            
            # Generate method body
            body = []
            
            # Add query parameters handling
            if query_params:
                body.append("params = {}")
                for name in query_params.keys():
                    body.append(f"if {name} is not None:")
                    body.append(f"    params['{name}'] = {name}")
            else:
                body.append("params = None")
            
            # Generate API call
            if "{" in path:
                path_args = []
                for param in route_params:
                    path_args.append(f"{param}={param}")
                
                body.append(f"endpoint = f\"{path}\".format({', '.join(path_args)})")
            else:
                body.append(f"endpoint = \"{path}\"")
            
            body.append(f"return self.api._request(\"{http_method}\", endpoint, params=params)")
            
            # Combine everything
            return f"{signature}\n        {docstring}\n        {self._indent(self._join_lines(body), 8)}"
            
        elif language == "javascript":
            params = []
            doc_params = []
            method_params = []
            
            # Add route parameters
            for param in route_params:
                params.append(param)
                doc_params.append(f"     * @param {{{param}}} {param} - Parameter description")
                method_params.append(param)
            
            # Add query parameters
            for name, info in query_params.items():
                if not info.get("required", False):
                    params.append(f"{name} = null")
                else:
                    params.append(name)
                
                doc_params.append(f"     * @param {{{info.get('type', 'string')}}} [{name}] - {info.get('description', 'Parameter description')}")
                method_params.append(name)
            
            # Generate method signature
            signature = f"async {method_name}({params.join(', ')}) {{"
            
            # Generate JSDoc
            jsdoc = "/**"
            if description:
                jsdoc += f"\n     * {description}"
            else:
                jsdoc += f"\n     * {method_name} method"
            
            if doc_params:
                jsdoc += "\n     *"
                jsdoc += "\n" + "\n".join(doc_params)
            
            jsdoc += "\n     * @returns {Promise<Object>} API response\n     */"
            
            # Generate method body
            body = []
            
            # Add query parameters handling
            if query_params:
                body.append("const params = {};")
                for name in query_params.keys():
                    body.append(f"if ({name} !== null && {name} !== undefined) {{")
                    body.append(f"    params['{name}'] = {name};")
                    body.append("}")
            else:
                body.append("const params = null;")
            
            # Generate API call
            if "{" in path:
                path = path.replace("{", "${")
                body.append(f"const endpoint = `{path}`;")
            else:
                body.append(f"const endpoint = '{path}';")
            
            body.append(f"return await this.api._request('{http_method}', endpoint, params);")
            
            # Combine everything
            return f"{jsdoc}\n    {signature}\n        {self._indent(self._join_lines(body), 8)}\n    }}"
        
        # Add support for other languages as needed
        
        return ""
    
    def write_sdk(self, language: str) -> str:
        """
        Generate and write SDK code to a file
        
        Args:
            language: Programming language to generate SDK for
            
        Returns:
            Path to the generated file
        """
        # Generate SDK
        sdk_code = self.generate_sdk(language)
        
        # Determine file extension
        ext = SUPPORTED_LANGUAGES.get(language, language)
        
        # Create output file
        output_dir = self.output_dir / language
        os.makedirs(output_dir, exist_ok=True)
        
        # Determine output filename
        if language == "python":
            filename = "bloxapi.py"
        elif language in ["javascript", "typescript"]:
            filename = "bloxapi." + ext
        elif language == "csharp":
            filename = "BloxApi.cs"
        elif language == "java":
            filename = "BloxApi.java"
        else:
            filename = f"bloxapi.{ext}"
        
        output_file = output_dir / filename
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write(sdk_code)
        
        logger.info(f"Generated {language} SDK: {output_file}")
        return str(output_file)
    
    def write_all_sdks(self) -> Dict[str, str]:
        """
        Generate and write SDKs for all supported languages
        
        Returns:
            Dictionary of language to output file path
        """
        results = {}
        
        for language in SUPPORTED_LANGUAGES:
            try:
                output_file = self.write_sdk(language)
                results[language] = output_file
            except Exception as e:
                logger.error(f"Error generating {language} SDK: {e}")
        
        return results
    
    def _to_snake_case(self, text: str) -> str:
        """Convert text to snake_case"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _to_camel_case(self, text: str) -> str:
        """Convert text to CamelCase"""
        components = text.split(' ')
        return ''.join(x.title() for x in components)
    
    def _join_lines(self, lines: List[str]) -> str:
        """Join lines with newline characters"""
        return '\n'.join(lines)
    
    def _join_methods(self, methods: List[str]) -> str:
        """Join methods with newline characters"""
        return '\n\n'.join(methods)
    
    def _indent(self, text: str, spaces: int) -> str:
        """Indent text by a number of spaces"""
        padding = ' ' * spaces
        return '\n'.join(padding + line if line.strip() else line for line in text.split('\n'))


# Function to generate SDK for a specific language
def generate_sdk(language: str, api_version: str = "v2", 
                base_url: str = "https://api.bloxapi.com") -> str:
    """
    Generate SDK for a specific language
    
    Args:
        language: Programming language (python, javascript, typescript, csharp, etc.)
        api_version: API version
        base_url: Base URL for API requests
        
    Returns:
        Path to the generated SDK file
    """
    generator = SDKGenerator(api_version=api_version, base_url=base_url)
    return generator.write_sdk(language)


# Function to generate SDKs for all supported languages
def generate_all_sdks(api_version: str = "v2", 
                     base_url: str = "https://api.bloxapi.com") -> Dict[str, str]:
    """
    Generate SDKs for all supported languages
    
    Args:
        api_version: API version
        base_url: Base URL for API requests
        
    Returns:
        Dictionary of language to output file path
    """
    generator = SDKGenerator(api_version=api_version, base_url=base_url)
    return generator.write_all_sdks()