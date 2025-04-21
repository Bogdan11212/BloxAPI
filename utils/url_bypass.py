"""
URL Shortener Bypass Utility

This module provides functions to bypass common URL shorteners like Linkvertise and others by extracting
the original destination URL. It uses trafilatura for web scraping and bypass techniques.
"""

import re
import requests
import trafilatura
import logging
from urllib.parse import urlparse, parse_qs, unquote
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of common URL shortener domains
URL_SHORTENER_DOMAINS = [
    'linkvertise.com', 'link-to.net', 'linkvertise.net', 'up-to-down.net', 'link-center.net',
    'direct-link.net', 'link-target.net', 'link-hub.net', 'adbull.me', 'linkvip.io', 'shrink.world',
    'exe.io', 'exey.io', 'exee.io', 'exe.app', 'short.express', 'oke.io', 'ouo.io', 'ouo.press',
    'adfoc.us', 'ay.link', 'bc.vc', 'shrinkme.io', 'shortit.pw', 'tii.ai', 'shrinkurl.in', 
    'shrinkearn.com', 'bitly.com', 'bit.ly', 'tinyurl.com', 't.co', 'rebrand.ly', 'cutt.ly',
    'ow.ly', 'adf.ly', 'sh.st', 'viid.me', 'adblade.com', 'linktly.co', 'spaste.com',
    'za.gl', 'da.gd', 'yep.it', 'url.ie', 'clck.ru', 'is.gd', 'v.gd', 'tiny.cc'
]


def is_url_shortener(url):
    """
    Check if a URL is from a known URL shortener service
    
    Args:
        url (str): The URL to check
        
    Returns:
        bool: True if the URL is from a known shortener, False otherwise
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # Remove www. prefix if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    # Check against known shortener domains
    for shortener in URL_SHORTENER_DOMAINS:
        if domain == shortener or domain.endswith(f'.{shortener}'):
            return True
    
    return False


def bypass_linkvertise(url):
    """
    Bypass Linkvertise and similar services
    
    Args:
        url (str): The Linkvertise URL
        
    Returns:
        str: The destination URL
    """
    try:
        # Extract the link ID from the URL
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        
        if len(path_parts) < 2:
            logger.warning(f"Invalid Linkvertise URL format: {url}")
            return None
            
        # Try the API bypass method
        try:
            # Construct the bypass API URL
            bypass_api = f"https://bypass.bot.nu/bypass2?url={url}"
            response = requests.get(bypass_api, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success') and data.get('destination'):
                        return data['destination']
                except json.JSONDecodeError:
                    pass  # Fall back to other methods
        except Exception as e:
            logger.debug(f"API bypass method failed: {e}")
        
        # Try direct scraping method
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Look for meta refresh tag
                meta_refresh = re.search(r'<meta[^>]*?http-equiv=["\']?refresh["\']?[^>]*?url=(.*?)["\']', response.text, re.IGNORECASE)
                if meta_refresh:
                    destination_url = meta_refresh.group(1)
                    return unquote(destination_url)
                
                # Look for redirect URL in JavaScript
                redirect_match = re.search(r'window\.location\s*=\s*["\'](.+?)["\']', response.text)
                if redirect_match:
                    return redirect_match.group(1)
                
                # Look for destination URL in linkvertise data
                data_match = re.search(r'<script[^>]*?>\s*?var\s+?linkvertise\s*?=\s*?(\{.+?\})\s*?;\s*?</script>', 
                                       response.text, re.DOTALL)
                if data_match:
                    try:
                        data_str = data_match.group(1)
                        # Make it valid JSON
                        data_str = re.sub(r'(\w+):', r'"\1":', data_str)
                        data_str = re.sub(r',\s*}', r'}', data_str)
                        data = json.loads(data_str)
                        if data.get('destinationUrl'):
                            return data['destinationUrl']
                    except:
                        pass
        except Exception as e:
            logger.debug(f"Scraping method failed: {e}")
        
        return None
        
    except Exception as e:
        logger.error(f"Error bypassing Linkvertise: {e}")
        return None


def bypass_adfly(url):
    """
    Bypass Adfly and similar services
    
    Args:
        url (str): The Adfly URL
        
    Returns:
        str: The destination URL
    """
    try:
        # Try direct page access
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Look for the destination in the HTML
            ysmm_match = re.search(r'var\s+ysmm\s*=\s*["\']([^"\']+)["\']', response.text)
            if ysmm_match:
                ysmm = ysmm_match.group(1)
                # Decode the ysmm parameter
                left = ''
                right = ''
                for i in range(0, len(ysmm), 2):
                    left += ysmm[i]
                for i in range(1, len(ysmm), 2):
                    right = ysmm[i] + right
                
                decoded = left + right
                decoded = decoded.replace('_', '/')
                decoded = decoded.replace('-', '+')
                import base64
                try:
                    decoded = base64.b64decode(decoded).decode('utf-8')
                    # AdF.ly adds 'http' at the start
                    if decoded.startswith('http'):
                        return decoded
                except:
                    pass
            
            # Try to find meta refresh
            meta_refresh = re.search(r'<meta[^>]*?http-equiv=["\']?refresh["\']?[^>]*?url=(.*?)["\']', 
                                     response.text, re.IGNORECASE)
            if meta_refresh:
                destination_url = meta_refresh.group(1)
                return unquote(destination_url)
        
        return None
        
    except Exception as e:
        logger.error(f"Error bypassing Adfly: {e}")
        return None


def bypass_generic_shortener(url):
    """
    Attempt to bypass a generic URL shortener by following redirects
    
    Args:
        url (str): The shortened URL
        
    Returns:
        str: The destination URL
    """
    try:
        # Try to follow the redirect without actually downloading the page
        response = requests.head(url, allow_redirects=True, timeout=10)
        if response.url != url:
            return response.url
        
        # If HEAD request doesn't work, try GET with redirect
        response = requests.get(url, allow_redirects=True, timeout=10)
        if response.url != url:
            return response.url
        
        # Try to find meta refresh tag
        html_text = response.text
        meta_refresh = re.search(r'<meta[^>]*?http-equiv=["\']?refresh["\']?[^>]*?url=(.*?)["\']', 
                                 html_text, re.IGNORECASE)
        if meta_refresh:
            destination_url = meta_refresh.group(1)
            return unquote(destination_url)
        
        # Try to find JavaScript redirect
        js_redirect = re.search(r'(?:window\.location|location\.href)\s*=\s*["\'](.+?)["\']', html_text)
        if js_redirect:
            return js_redirect.group(1)
        
        # Use trafilatura to get links from page
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            links = trafilatura.extract_metadata(downloaded).get('links', [])
            if links and len(links) > 0:
                # In many cases, the first external link is the destination
                return links[0]
            
        return None
    
    except Exception as e:
        logger.error(f"Error bypassing generic shortener: {e}")
        return None


def bypass_url_shortener(url):
    """
    Main function to bypass URL shorteners
    
    Args:
        url (str): The shortened URL
        
    Returns:
        str: The destination URL if successfully bypassed, None otherwise
    """
    if not url:
        return None
        
    # Check if it's a known URL shortener
    if not is_url_shortener(url):
        return url  # Not a shortener, return as is
    
    logger.info(f"Attempting to bypass URL shortener: {url}")
    
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # Remove www. prefix if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    # Try specific bypassing methods based on domain
    if 'linkvertise' in domain or 'link-to' in domain or 'link-center' in domain or 'up-to-down' in domain:
        destination = bypass_linkvertise(url)
        if destination:
            return destination
    
    if 'adf.ly' in domain or 'ay.link' in domain or 'j.gs' in domain:
        destination = bypass_adfly(url)
        if destination:
            return destination
    
    # For other shorteners, try generic bypass
    destination = bypass_generic_shortener(url)
    if destination:
        return destination
    
    logger.warning(f"Failed to bypass URL shortener: {url}")
    return url  # Return original URL if bypass fails


def get_original_content(url):
    """
    Get the original content from a URL, bypassing shorteners if needed
    
    Args:
        url (str): The URL, which might be a shortener
        
    Returns:
        str: The content of the final destination URL
    """
    try:
        destination_url = bypass_url_shortener(url)
        if not destination_url:
            return None
        
        # Use trafilatura to extract content
        downloaded = trafilatura.fetch_url(destination_url)
        if downloaded:
            content = trafilatura.extract(downloaded)
            return content
        
        return None
    
    except Exception as e:
        logger.error(f"Error getting original content: {e}")
        return None


# Example usage:
if __name__ == "__main__":
    test_url = "https://bit.ly/example"
    result = bypass_url_shortener(test_url)
    print(f"Original URL: {test_url}")
    print(f"Destination URL: {result}")
    
    # Get content
    content = get_original_content(test_url)
    print(f"Content excerpt: {content[:200] if content else None}")