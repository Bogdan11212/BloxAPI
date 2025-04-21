"""
Security Module for BloxAPI

This module provides protection against bots, automated attacks,
and security threats. It includes rate limiting, IP reputation checks,
and request validation.
"""

import os
import re
import time
import json
import logging
import hashlib
import ipaddress
import threading
from typing import Dict, List, Any, Optional, Union, Callable, Set, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
from urllib.parse import urlparse
import requests
import uuid
import hmac

# Configure logging
logger = logging.getLogger(__name__)

class SecurityViolation(Exception):
    """Exception raised for security violations"""
    pass

class RateLimiter:
    """
    Rate limiter to prevent abuse and DoS attacks
    """
    
    def __init__(self, limit: int = 100, window: int = 60):
        """
        Initialize the rate limiter
        
        Args:
            limit: Maximum number of requests allowed per window
            window: Time window in seconds
        """
        self.limit = limit
        self.window = window
        self.ip_requests: Dict[str, List[float]] = defaultdict(list)
        self.endpoint_limits: Dict[str, Tuple[int, int]] = {}
        self.banned_ips: Set[str] = set()
        self.ban_duration = 3600  # 1 hour ban by default
        self.ban_threshold = 5  # Number of violations before ban
        self.violation_counts: Dict[str, int] = defaultdict(int)
        self.lock = threading.RLock()
    
    def add_endpoint_limit(self, endpoint: str, limit: int, window: int) -> None:
        """
        Add a specific rate limit for an endpoint
        
        Args:
            endpoint: API endpoint pattern (regex)
            limit: Maximum number of requests allowed per window
            window: Time window in seconds
        """
        self.endpoint_limits[endpoint] = (limit, window)
        logger.debug(f"Added rate limit for endpoint {endpoint}: {limit} requests per {window}s")
    
    def is_rate_limited(self, ip: str, endpoint: str = None) -> bool:
        """
        Check if a request should be rate limited
        
        Args:
            ip: Client IP address
            endpoint: Optional endpoint for specific limits
            
        Returns:
            True if request should be rate limited, False otherwise
        """
        with self.lock:
            # Check if IP is banned
            if ip in self.banned_ips:
                return True
            
            # Get current time
            current_time = time.time()
            
            # Clean up old requests
            self.ip_requests[ip] = [t for t in self.ip_requests[ip] if current_time - t <= self.window]
            
            # Check endpoint-specific limits first
            if endpoint:
                for pattern, (limit, window) in self.endpoint_limits.items():
                    if re.match(pattern, endpoint):
                        # Filter requests for this endpoint
                        endpoint_requests = [
                            t for t in self.ip_requests[ip] 
                            if current_time - t <= window
                        ]
                        
                        # Check if limit is exceeded
                        if len(endpoint_requests) >= limit:
                            # Record violation
                            self._record_violation(ip)
                            return True
            
            # Check global limit
            if len(self.ip_requests[ip]) >= self.limit:
                # Record violation
                self._record_violation(ip)
                return True
            
            # Add request timestamp
            self.ip_requests[ip].append(current_time)
            return False
    
    def _record_violation(self, ip: str) -> None:
        """
        Record a rate limit violation and potentially ban the IP
        
        Args:
            ip: Client IP address
        """
        self.violation_counts[ip] += 1
        
        # Check if threshold is exceeded
        if self.violation_counts[ip] >= self.ban_threshold:
            self.banned_ips.add(ip)
            logger.warning(f"IP {ip} banned for {self.ban_duration}s due to rate limit violations")
            
            # Schedule unbanning
            threading.Timer(
                self.ban_duration,
                lambda: self._unban_ip(ip)
            ).start()
    
    def _unban_ip(self, ip: str) -> None:
        """
        Unban an IP address
        
        Args:
            ip: IP address to unban
        """
        with self.lock:
            if ip in self.banned_ips:
                self.banned_ips.remove(ip)
                self.violation_counts[ip] = 0
                logger.info(f"IP {ip} unbanned")
    
    def ban_ip(self, ip: str, duration: int = None) -> None:
        """
        Manually ban an IP address
        
        Args:
            ip: IP address to ban
            duration: Ban duration in seconds (None for default)
        """
        with self.lock:
            self.banned_ips.add(ip)
            
            if duration is None:
                duration = self.ban_duration
            
            logger.warning(f"IP {ip} manually banned for {duration}s")
            
            # Schedule unbanning
            threading.Timer(
                duration,
                lambda: self._unban_ip(ip)
            ).start()
    
    def unban_ip(self, ip: str) -> None:
        """
        Manually unban an IP address
        
        Args:
            ip: IP address to unban
        """
        self._unban_ip(ip)
    
    def is_banned(self, ip: str) -> bool:
        """
        Check if an IP is banned
        
        Args:
            ip: IP address to check
            
        Returns:
            True if IP is banned, False otherwise
        """
        return ip in self.banned_ips
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get rate limiter statistics
        
        Returns:
            Dictionary with statistics
        """
        with self.lock:
            return {
                'limit': self.limit,
                'window': self.window,
                'active_ips': len(self.ip_requests),
                'banned_ips': len(self.banned_ips),
                'endpoint_limits': {
                    pattern: {
                        'limit': limit,
                        'window': window
                    } for pattern, (limit, window) in self.endpoint_limits.items()
                },
                'total_requests': sum(len(reqs) for reqs in self.ip_requests.values())
            }
    
    def reset(self) -> None:
        """
        Reset the rate limiter state
        """
        with self.lock:
            self.ip_requests.clear()
            self.banned_ips.clear()
            self.violation_counts.clear()


class IPReputation:
    """
    IP reputation checker for identifying malicious sources
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the IP reputation checker
        
        Args:
            api_key: API key for external reputation service
        """
        self.api_key = api_key
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_duration = 3600  # 1 hour cache
        self.known_bad_networks: List[str] = []
        self.trusted_networks: List[str] = []
        self.lock = threading.RLock()
        self._load_ip_lists()
    
    def _load_ip_lists(self) -> None:
        """
        Load known bad and trusted IP networks
        """
        # Load from environment variables if available
        bad_networks = os.environ.get('BLOXAPI_BAD_NETWORKS', '')
        trusted_networks = os.environ.get('BLOXAPI_TRUSTED_NETWORKS', '')
        
        # Parse comma-separated lists
        if bad_networks:
            self.known_bad_networks = [net.strip() for net in bad_networks.split(',')]
        
        if trusted_networks:
            self.trusted_networks = [net.strip() for net in trusted_networks.split(',')]
        
        # Default to common datacenters and VPNs if empty
        if not self.known_bad_networks:
            self.known_bad_networks = [
                # Some known proxy/VPN networks
                '185.220.101.0/24',  # Tor exit nodes
                '104.244.72.0/21',   # Twitter/X known proxy
                '163.172.0.0/16',    # OVH/SYS
                '89.234.157.0/24',   # French Data Network
            ]
        
        # Default trusted networks if empty
        if not self.trusted_networks:
            self.trusted_networks = [
                '127.0.0.0/8',       # Localhost
                '10.0.0.0/8',        # Private network
                '172.16.0.0/12',     # Private network
                '192.168.0.0/16',    # Private network
            ]
        
        logger.debug(f"Loaded {len(self.known_bad_networks)} known bad networks and "
                    f"{len(self.trusted_networks)} trusted networks")
    
    def is_trusted(self, ip: str) -> bool:
        """
        Check if an IP address is from a trusted network
        
        Args:
            ip: IP address to check
            
        Returns:
            True if IP is trusted, False otherwise
        """
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            # Check trusted networks
            for network in self.trusted_networks:
                try:
                    if ip_obj in ipaddress.ip_network(network):
                        return True
                except ValueError:
                    continue
            
            return False
        
        except ValueError:
            logger.warning(f"Invalid IP address: {ip}")
            return False
    
    def is_known_bad(self, ip: str) -> bool:
        """
        Check if an IP address is from a known bad network
        
        Args:
            ip: IP address to check
            
        Returns:
            True if IP is known bad, False otherwise
        """
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            # Check known bad networks
            for network in self.known_bad_networks:
                try:
                    if ip_obj in ipaddress.ip_network(network):
                        return True
                except ValueError:
                    continue
            
            return False
        
        except ValueError:
            logger.warning(f"Invalid IP address: {ip}")
            return False
    
    def check_reputation(self, ip: str) -> Dict[str, Any]:
        """
        Check the reputation of an IP address
        
        Args:
            ip: IP address to check
            
        Returns:
            Dictionary with reputation data
        """
        with self.lock:
            # Check cache first
            if ip in self.cache:
                cache_time = self.cache[ip].get('_timestamp', 0)
                if time.time() - cache_time < self.cache_duration:
                    return self.cache[ip]
            
            # Check if IP is trusted
            if self.is_trusted(ip):
                reputation = {
                    'ip': ip,
                    'risk_score': 0,
                    'is_trusted': True,
                    'is_known_bad': False,
                    'categories': ['trusted'],
                    '_timestamp': time.time()
                }
                self.cache[ip] = reputation
                return reputation
            
            # Check if IP is known bad
            if self.is_known_bad(ip):
                reputation = {
                    'ip': ip,
                    'risk_score': 100,
                    'is_trusted': False,
                    'is_known_bad': True,
                    'categories': ['known_bad'],
                    '_timestamp': time.time()
                }
                self.cache[ip] = reputation
                return reputation
            
            # Check external API if key is available
            if self.api_key:
                try:
                    # This is a placeholder for an actual API call
                    # Replace with your preferred IP reputation service
                    url = f"https://ip-reputation-api.example.com/v1/ip/{ip}"
                    headers = {
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    response = requests.get(url, headers=headers, timeout=5)
                    
                    if response.status_code == 200:
                        data = response.json()
                        reputation = {
                            'ip': ip,
                            'risk_score': data.get('risk_score', 50),
                            'is_trusted': data.get('risk_score', 50) < 10,
                            'is_known_bad': data.get('risk_score', 50) > 75,
                            'categories': data.get('categories', []),
                            'country': data.get('country', 'unknown'),
                            'asn': data.get('asn', 'unknown'),
                            'organization': data.get('organization', 'unknown'),
                            '_timestamp': time.time()
                        }
                        self.cache[ip] = reputation
                        return reputation
                
                except Exception as e:
                    logger.error(f"Error checking IP reputation for {ip}: {e}")
            
            # Default response if API key is not available or API call fails
            reputation = {
                'ip': ip,
                'risk_score': 50,  # Neutral score
                'is_trusted': False,
                'is_known_bad': False,
                'categories': [],
                '_timestamp': time.time()
            }
            self.cache[ip] = reputation
            return reputation
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get IP reputation statistics
        
        Returns:
            Dictionary with statistics
        """
        with self.lock:
            return {
                'cache_size': len(self.cache),
                'known_bad_networks': len(self.known_bad_networks),
                'trusted_networks': len(self.trusted_networks),
                'api_available': bool(self.api_key)
            }
    
    def add_known_bad_network(self, network: str) -> bool:
        """
        Add a network to the known bad list
        
        Args:
            network: IP network in CIDR notation
            
        Returns:
            True if added successfully, False otherwise
        """
        try:
            # Validate network
            ipaddress.ip_network(network)
            
            with self.lock:
                if network not in self.known_bad_networks:
                    self.known_bad_networks.append(network)
                    logger.info(f"Added network {network} to known bad networks")
                    return True
            
            return False
        
        except ValueError:
            logger.warning(f"Invalid network: {network}")
            return False
    
    def add_trusted_network(self, network: str) -> bool:
        """
        Add a network to the trusted list
        
        Args:
            network: IP network in CIDR notation
            
        Returns:
            True if added successfully, False otherwise
        """
        try:
            # Validate network
            ipaddress.ip_network(network)
            
            with self.lock:
                if network not in self.trusted_networks:
                    self.trusted_networks.append(network)
                    logger.info(f"Added network {network} to trusted networks")
                    return True
            
            return False
        
        except ValueError:
            logger.warning(f"Invalid network: {network}")
            return False


class RequestValidator:
    """
    Validator for HTTP requests to detect and block malicious requests
    """
    
    def __init__(self):
        """Initialize the request validator"""
        # Common SQL injection patterns
        self.sql_injection_patterns = [
            r"(?i)'\s*OR\s+'1'\s*=\s*'1",
            r"(?i)'\s*OR\s+'1'\s*=\s*1",
            r"(?i)'\s*OR\s+1\s*=\s*1",
            r"(?i)--",
            r"(?i)UNION\s+ALL\s+SELECT",
            r"(?i)DROP\s+TABLE",
            r"(?i)DELETE\s+FROM",
            r"(?i)INSERT\s+INTO",
            r"(?i)SELECT\s+.*\s+FROM"
        ]
        
        # Common XSS patterns
        self.xss_patterns = [
            r"(?i)<script.*?>",
            r"(?i)javascript:",
            r"(?i)onload\s*=",
            r"(?i)onerror\s*=",
            r"(?i)onclick\s*=",
            r"(?i)onmouseover\s*=",
            r"(?i)eval\s*\(",
            r"(?i)alert\s*\(",
            r"(?i)document\.cookie"
        ]
        
        # Common path traversal patterns
        self.path_traversal_patterns = [
            r"(?i)\.\.\/",
            r"(?i)\.\.\\",
            r"(?i)%2e%2e%2f",
            r"(?i)%2e%2e\/",
            r"(?i)\/etc\/passwd",
            r"(?i)c:\\boot\.ini",
            r"(?i)\/\/etc\/shadow"
        ]
        
        # Common command injection patterns
        self.command_injection_patterns = [
            r"(?i);\s*cat\s+",
            r"(?i);\s*rm\s+",
            r"(?i);\s*ls\s+",
            r"(?i);\s*dir\s+",
            r"(?i);\s*chmod\s+",
            r"(?i);\s*chown\s+",
            r"(?i)\|\s*cat\s+",
            r"(?i)\|\s*grep\s+"
        ]
        
        # Suspicious user agent patterns
        self.suspicious_agents = [
            r"(?i)sqlmap",
            r"(?i)nikto",
            r"(?i)nmap",
            r"(?i)masscan",
            r"(?i)zgrab",
            r"(?i)python-requests\/",
            r"(?i)curl\/",
            r"(?i)wget\/",
            r"(?i)burpsuite",
            r"(?i)scrapy",
            r"(?i)phantomjs",
            r"(?i)yslow",
            r"(?i)^$",  # Empty user agent
            r"(?i)go http package",
            r"(?i)python urllib"
        ]
        
        # Bad file extensions
        self.bad_extensions = [
            ".php", ".asp", ".aspx", ".jsp", ".cgi", ".exe", 
            ".bat", ".cmd", ".sh", ".pl", ".py"
        ]
        
        # Precompile all patterns for performance
        self.compiled_patterns = {}
        self._compile_patterns()
    
    def _compile_patterns(self) -> None:
        """Compile all regex patterns for faster matching"""
        patterns = {
            'sql_injection': self.sql_injection_patterns,
            'xss': self.xss_patterns,
            'path_traversal': self.path_traversal_patterns,
            'command_injection': self.command_injection_patterns,
            'suspicious_agents': self.suspicious_agents
        }
        
        for category, pattern_list in patterns.items():
            self.compiled_patterns[category] = [re.compile(pattern) for pattern in pattern_list]
    
    def validate_request(self, request, raise_exception: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Validate a request for security issues
        
        Args:
            request: Flask/Django request object
            raise_exception: Whether to raise an exception if validation fails
            
        Returns:
            Tuple of (is_valid, reason)
            
        Raises:
            SecurityViolation: If validation fails and raise_exception is True
        """
        # Check user agent
        user_agent = request.headers.get('User-Agent', '')
        if user_agent:
            for pattern in self.compiled_patterns['suspicious_agents']:
                if pattern.search(user_agent):
                    reason = f"Suspicious user agent: {user_agent}"
                    if raise_exception:
                        raise SecurityViolation(reason)
                    return False, reason
        
        # Check path for traversal attempts
        path = request.path
        for pattern in self.compiled_patterns['path_traversal']:
            if pattern.search(path):
                reason = f"Path traversal attempt in URL: {path}"
                if raise_exception:
                    raise SecurityViolation(reason)
                return False, reason
        
        # Check for bad file extensions
        for ext in self.bad_extensions:
            if path.lower().endswith(ext):
                reason = f"Bad file extension in URL: {path}"
                if raise_exception:
                    raise SecurityViolation(reason)
                return False, reason
        
        # Check query parameters
        for key, value in request.args.items():
            if isinstance(value, str):
                # Check for SQL injection
                for pattern in self.compiled_patterns['sql_injection']:
                    if pattern.search(value):
                        reason = f"SQL injection attempt in query param {key}"
                        if raise_exception:
                            raise SecurityViolation(reason)
                        return False, reason
                
                # Check for XSS
                for pattern in self.compiled_patterns['xss']:
                    if pattern.search(value):
                        reason = f"XSS attempt in query param {key}"
                        if raise_exception:
                            raise SecurityViolation(reason)
                        return False, reason
                
                # Check for command injection
                for pattern in self.compiled_patterns['command_injection']:
                    if pattern.search(value):
                        reason = f"Command injection attempt in query param {key}"
                        if raise_exception:
                            raise SecurityViolation(reason)
                        return False, reason
        
        # Check request body for JSON requests
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                # Get JSON data
                json_data = request.json
                if json_data:
                    # Convert to string for pattern matching
                    json_str = json.dumps(json_data)
                    
                    # Check for various attacks
                    for category in ['sql_injection', 'xss', 'command_injection']:
                        for pattern in self.compiled_patterns[category]:
                            if pattern.search(json_str):
                                reason = f"{category.replace('_', ' ').title()} attempt in JSON body"
                                if raise_exception:
                                    raise SecurityViolation(reason)
                                return False, reason
            except Exception:
                # If we can't parse JSON, just continue
                pass
        
        # Check form data
        for key, value in request.form.items():
            if isinstance(value, str):
                # Check for SQL injection
                for pattern in self.compiled_patterns['sql_injection']:
                    if pattern.search(value):
                        reason = f"SQL injection attempt in form param {key}"
                        if raise_exception:
                            raise SecurityViolation(reason)
                        return False, reason
                
                # Check for XSS
                for pattern in self.compiled_patterns['xss']:
                    if pattern.search(value):
                        reason = f"XSS attempt in form param {key}"
                        if raise_exception:
                            raise SecurityViolation(reason)
                        return False, reason
                
                # Check for command injection
                for pattern in self.compiled_patterns['command_injection']:
                    if pattern.search(value):
                        reason = f"Command injection attempt in form param {key}"
                        if raise_exception:
                            raise SecurityViolation(reason)
                        return False, reason
        
        # Check for bad referer
        referer = request.headers.get('Referer', '')
        if referer:
            try:
                parsed_referer = urlparse(referer)
                parsed_host = urlparse(request.host_url)
                
                if parsed_referer.netloc and parsed_host.netloc:
                    # Check if referer domain matches host domain
                    if parsed_referer.netloc != parsed_host.netloc:
                        # This could be a CSRF attempt, but legitimate external referrals also trigger this
                        # So we'll just log it rather than blocking
                        logger.warning(f"Request from external referer: {referer} to {request.path}")
            except Exception:
                pass
        
        # All checks passed
        return True, None
    
    def add_sql_injection_pattern(self, pattern: str) -> None:
        """
        Add a SQL injection pattern
        
        Args:
            pattern: Regex pattern string
        """
        self.sql_injection_patterns.append(pattern)
        self.compiled_patterns['sql_injection'].append(re.compile(pattern))
    
    def add_xss_pattern(self, pattern: str) -> None:
        """
        Add an XSS pattern
        
        Args:
            pattern: Regex pattern string
        """
        self.xss_patterns.append(pattern)
        self.compiled_patterns['xss'].append(re.compile(pattern))
    
    def add_path_traversal_pattern(self, pattern: str) -> None:
        """
        Add a path traversal pattern
        
        Args:
            pattern: Regex pattern string
        """
        self.path_traversal_patterns.append(pattern)
        self.compiled_patterns['path_traversal'].append(re.compile(pattern))
    
    def add_command_injection_pattern(self, pattern: str) -> None:
        """
        Add a command injection pattern
        
        Args:
            pattern: Regex pattern string
        """
        self.command_injection_patterns.append(pattern)
        self.compiled_patterns['command_injection'].append(re.compile(pattern))
    
    def add_suspicious_agent(self, pattern: str) -> None:
        """
        Add a suspicious user agent pattern
        
        Args:
            pattern: Regex pattern string
        """
        self.suspicious_agents.append(pattern)
        self.compiled_patterns['suspicious_agents'].append(re.compile(pattern))
    
    def add_bad_extension(self, extension: str) -> None:
        """
        Add a bad file extension
        
        Args:
            extension: File extension (with dot)
        """
        if not extension.startswith('.'):
            extension = f".{extension}"
        
        self.bad_extensions.append(extension.lower())


class BotDetector:
    """
    Bot detection and mitigation
    """
    
    def __init__(self):
        """Initialize the bot detector"""
        # Bot fingerprints
        self.bot_fingerprints = {
            # Common crawlers
            'googlebot': {
                'user_agent': r"(?i)googlebot",
                'verify_hostname': r".*\.googlebot\.com$",
                'is_allowed': True
            },
            'bingbot': {
                'user_agent': r"(?i)bingbot",
                'verify_hostname': r".*\.search\.msn\.com$",
                'is_allowed': True
            },
            'baiduspider': {
                'user_agent': r"(?i)baiduspider",
                'verify_hostname': r".*\.baidu\.com$",
                'is_allowed': True
            },
            'yandexbot': {
                'user_agent': r"(?i)yandexbot",
                'verify_hostname': r".*\.yandex\.(ru|com|net)$",
                'is_allowed': True
            },
            
            # Malicious bots
            'semrush': {
                'user_agent': r"(?i)semrush",
                'verify_hostname': r".*\.semrush\.com$",
                'is_allowed': False
            },
            'ahrefs': {
                'user_agent': r"(?i)ahrefs",
                'verify_hostname': r".*\.ahrefs\.com$",
                'is_allowed': False
            },
            'screaming_frog': {
                'user_agent': r"(?i)screaming.?frog",
                'verify_hostname': None,
                'is_allowed': False
            },
            'generic_crawler': {
                'user_agent': r"(?i)(crawler|spider|bot|http)",
                'verify_hostname': None,
                'is_allowed': False
            }
        }
        
        # Compile patterns
        for name, data in self.bot_fingerprints.items():
            if 'user_agent' in data and isinstance(data['user_agent'], str):
                data['user_agent_pattern'] = re.compile(data['user_agent'])
    
    def is_bot(self, user_agent: str, ip: str = None) -> Dict[str, Any]:
        """
        Check if a request is from a bot
        
        Args:
            user_agent: User-Agent header value
            ip: Client IP address for hostname verification
            
        Returns:
            Dictionary with bot detection results
        """
        if not user_agent:
            return {
                'is_bot': False,
                'bot_name': None,
                'is_allowed': True,
                'verified': False
            }
        
        for name, data in self.bot_fingerprints.items():
            pattern = data.get('user_agent_pattern')
            if pattern and pattern.search(user_agent):
                # Found a matching bot pattern
                is_allowed = data.get('is_allowed', False)
                verified = False
                
                # Verify hostname if IP is provided
                if ip and data.get('verify_hostname'):
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                        hostname_pattern = data.get('verify_hostname')
                        
                        if re.match(hostname_pattern, hostname):
                            verified = True
                            # Known good bots are allowed only if verified
                            is_allowed = data.get('is_allowed', False)
                        else:
                            # Failed verification means it's likely spoofing
                            is_allowed = False
                    except (socket.herror, socket.gaierror):
                        # Hostname lookup failed
                        is_allowed = False
                
                return {
                    'is_bot': True,
                    'bot_name': name,
                    'is_allowed': is_allowed,
                    'verified': verified
                }
        
        # No bot pattern matched
        return {
            'is_bot': False,
            'bot_name': None,
            'is_allowed': True,
            'verified': False
        }
    
    def should_block(self, user_agent: str, ip: str = None) -> bool:
        """
        Check if a bot should be blocked
        
        Args:
            user_agent: User-Agent header value
            ip: Client IP address for hostname verification
            
        Returns:
            True if the bot should be blocked, False otherwise
        """
        result = self.is_bot(user_agent, ip)
        return result['is_bot'] and not result['is_allowed']
    
    def add_bot_fingerprint(self, name: str, user_agent_pattern: str, 
                         verify_hostname: Optional[str] = None,
                         is_allowed: bool = False) -> None:
        """
        Add a bot fingerprint
        
        Args:
            name: Bot name
            user_agent_pattern: Regex pattern for User-Agent
            verify_hostname: Regex pattern for hostname verification
            is_allowed: Whether this bot is allowed
        """
        self.bot_fingerprints[name] = {
            'user_agent': user_agent_pattern,
            'user_agent_pattern': re.compile(user_agent_pattern),
            'verify_hostname': verify_hostname,
            'is_allowed': is_allowed
        }
        
        logger.info(f"Added bot fingerprint for {name}, allowed: {is_allowed}")
    
    def allow_bot(self, name: str) -> bool:
        """
        Allow a bot by name
        
        Args:
            name: Bot name
            
        Returns:
            True if successful, False otherwise
        """
        if name in self.bot_fingerprints:
            self.bot_fingerprints[name]['is_allowed'] = True
            logger.info(f"Bot {name} is now allowed")
            return True
        return False
    
    def block_bot(self, name: str) -> bool:
        """
        Block a bot by name
        
        Args:
            name: Bot name
            
        Returns:
            True if successful, False otherwise
        """
        if name in self.bot_fingerprints:
            self.bot_fingerprints[name]['is_allowed'] = False
            logger.info(f"Bot {name} is now blocked")
            return True
        return False


class CsrfProtection:
    """
    Cross-Site Request Forgery (CSRF) protection
    """
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize CSRF protection
        
        Args:
            secret_key: Secret key for token generation
        """
        self.secret_key = secret_key or os.environ.get('SECRET_KEY', str(uuid.uuid4()))
        self.tokens: Dict[str, Dict[str, Any]] = {}
        self.cookie_name = 'csrf_token'
        self.header_name = 'X-CSRF-Token'
        self.expiry = 3600  # 1 hour
        self.lock = threading.RLock()
    
    def generate_token(self, session_id: str) -> str:
        """
        Generate a CSRF token for a session
        
        Args:
            session_id: Session ID
            
        Returns:
            CSRF token
        """
        with self.lock:
            # Generate a random token
            token = str(uuid.uuid4())
            
            # Store token data
            self.tokens[session_id] = {
                'token': token,
                'created_at': time.time()
            }
            
            # Clean up expired tokens
            self._clean_expired_tokens()
            
            return token
    
    def validate_token(self, session_id: str, token: str) -> bool:
        """
        Validate a CSRF token
        
        Args:
            session_id: Session ID
            token: CSRF token to validate
            
        Returns:
            True if valid, False otherwise
        """
        with self.lock:
            # Clean up expired tokens
            self._clean_expired_tokens()
            
            # Check if token exists and matches
            if session_id in self.tokens:
                stored_token = self.tokens[session_id].get('token')
                return stored_token == token
            
            return False
    
    def _clean_expired_tokens(self) -> None:
        """
        Clean up expired tokens
        """
        current_time = time.time()
        expired_sessions = [
            session_id for session_id, data in self.tokens.items()
            if current_time - data.get('created_at', 0) > self.expiry
        ]
        
        for session_id in expired_sessions:
            if session_id in self.tokens:
                del self.tokens[session_id]
    
    def get_token_from_request(self, request) -> Optional[str]:
        """
        Extract CSRF token from request
        
        Args:
            request: Flask/Django request object
            
        Returns:
            CSRF token if found, None otherwise
        """
        # Try to get from header
        token = request.headers.get(self.header_name)
        if token:
            return token
        
        # Try to get from form
        token = request.form.get('csrf_token')
        if token:
            return token
        
        # Try to get from query string
        token = request.args.get('csrf_token')
        if token:
            return token
        
        return None
    
    def get_session_id(self, request) -> str:
        """
        Get session ID from request
        
        Args:
            request: Flask/Django request object
            
        Returns:
            Session ID
        """
        # Try to get from session
        if hasattr(request, 'session') and hasattr(request.session, 'session_key'):
            return request.session.session_key
        
        # Try to get from cookie
        if hasattr(request, 'cookies') and 'session' in request.cookies:
            return request.cookies['session']
        
        # Use IP address as fallback
        return request.remote_addr
    
    def protect(self, request) -> bool:
        """
        Check if a request is protected against CSRF
        
        Args:
            request: Flask/Django request object
            
        Returns:
            True if protected, False otherwise
        """
        # Only protect unsafe methods
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            return True
        
        # Get session ID
        session_id = self.get_session_id(request)
        
        # Get token from request
        token = self.get_token_from_request(request)
        if not token:
            return False
        
        # Validate token
        return self.validate_token(session_id, token)


# Global instances
_rate_limiter = None
_ip_reputation = None
_request_validator = None
_bot_detector = None
_csrf_protection = None

def get_rate_limiter() -> RateLimiter:
    """
    Get the global rate limiter instance
    
    Returns:
        RateLimiter instance
    """
    global _rate_limiter
    
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    
    return _rate_limiter

def get_ip_reputation() -> IPReputation:
    """
    Get the global IP reputation instance
    
    Returns:
        IPReputation instance
    """
    global _ip_reputation
    
    if _ip_reputation is None:
        _ip_reputation = IPReputation()
    
    return _ip_reputation

def get_request_validator() -> RequestValidator:
    """
    Get the global request validator instance
    
    Returns:
        RequestValidator instance
    """
    global _request_validator
    
    if _request_validator is None:
        _request_validator = RequestValidator()
    
    return _request_validator

def get_bot_detector() -> BotDetector:
    """
    Get the global bot detector instance
    
    Returns:
        BotDetector instance
    """
    global _bot_detector
    
    if _bot_detector is None:
        _bot_detector = BotDetector()
    
    return _bot_detector

def get_csrf_protection() -> CsrfProtection:
    """
    Get the global CSRF protection instance
    
    Returns:
        CsrfProtection instance
    """
    global _csrf_protection
    
    if _csrf_protection is None:
        _csrf_protection = CsrfProtection()
    
    return _csrf_protection