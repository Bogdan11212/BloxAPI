"""
External Services API Routes
"""

from flask_restful import Resource, reqparse
from utils.response_formatter import format_response
from utils.rate_limiter import rate_limited
from utils.url_bypass import bypass_url_shortener, get_original_content
import json
import logging

logger = logging.getLogger(__name__)


class ExternalBaseResource(Resource):
    """Base class for external services resources"""
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Authorization', location='headers')
        super(ExternalBaseResource, self).__init__()


class URLShortenerBypassResource(ExternalBaseResource):
    """Resource for bypassing URL shorteners"""
    @rate_limited
    def get(self):
        """
        Bypass a URL shortener to get the destination URL
        
        Query Parameters:
            url (str, required): The shortened URL to bypass
            
        Returns:
            dict: The destination URL or error response
        """
        parser = self.parser.copy()
        parser.add_argument('url', required=True, help='The shortened URL is required')
        args = parser.parse_args()
        
        try:
            url = args['url']
            result = bypass_url_shortener(url)
            
            if result and result != url:
                return format_response({
                    "success": True,
                    "original_url": url,
                    "destination_url": result
                })
            else:
                return format_response({
                    "success": False,
                    "original_url": url,
                    "message": "Could not bypass this URL shortener or the URL is not a shortener"
                }, success=False)
                
        except Exception as e:
            logger.error(f"Error bypassing URL shortener: {e}")
            return format_response({
                "success": False,
                "message": "Error processing URL shortener bypass request",
                "error": str(e)
            }, success=False)


class URLContentExtractionResource(ExternalBaseResource):
    """Resource for extracting content from URLs"""
    @rate_limited
    def get(self):
        """
        Extract content from a URL (automatically bypasses shorteners)
        
        Query Parameters:
            url (str, required): The URL to extract content from
            
        Returns:
            dict: The extracted content or error response
        """
        parser = self.parser.copy()
        parser.add_argument('url', required=True, help='The URL is required')
        args = parser.parse_args()
        
        try:
            url = args['url']
            content = get_original_content(url)
            
            if content:
                # Determine if the URL was a shortener by comparing the bypassed URL
                bypassed_url = bypass_url_shortener(url)
                was_shortener = bypassed_url != url
                
                return format_response({
                    "success": True,
                    "original_url": url,
                    "destination_url": bypassed_url if was_shortener else url,
                    "was_shortener": was_shortener,
                    "content": content
                })
            else:
                return format_response({
                    "success": False,
                    "original_url": url,
                    "message": "Could not extract content from this URL"
                }, success=False)
                
        except Exception as e:
            logger.error(f"Error extracting content from URL: {e}")
            return format_response({
                "success": False,
                "message": "Error processing content extraction request",
                "error": str(e)
            }, success=False)


class BatchURLProcessingResource(ExternalBaseResource):
    """Resource for processing multiple URLs in a single request"""
    @rate_limited
    def post(self):
        """
        Process multiple URLs in a single request
        
        Request Body:
            urls (list, required): List of URLs to process
            extract_content (bool, optional): Whether to extract content from URLs (default: False)
            
        Returns:
            dict: Results for each URL or error response
        """
        parser = self.parser.copy()
        parser.add_argument('urls', type=list, required=True, location='json', help='List of URLs is required')
        parser.add_argument('extract_content', type=bool, default=False, location='json', help='Whether to extract content')
        args = parser.parse_args()
        
        try:
            urls = args['urls']
            extract_content = args['extract_content']
            
            results = []
            for url in urls:
                try:
                    bypassed_url = bypass_url_shortener(url)
                    was_shortener = bypassed_url != url
                    
                    result = {
                        "original_url": url,
                        "destination_url": bypassed_url,
                        "was_shortener": was_shortener
                    }
                    
                    if extract_content:
                        content = get_original_content(url)
                        result["content"] = content if content else None
                        
                    results.append(result)
                except Exception as e:
                    results.append({
                        "original_url": url,
                        "success": False,
                        "error": str(e)
                    })
            
            return format_response({
                "success": True,
                "results": results
            })
                
        except Exception as e:
            logger.error(f"Error processing batch URLs: {e}")
            return format_response({
                "success": False,
                "message": "Error processing batch URL request",
                "error": str(e)
            }, success=False)