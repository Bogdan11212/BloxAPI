"""
Resource Monitoring for BloxAPI

This module provides functionality for monitoring server resources,
API usage, and performance metrics in real time.
"""

import os
import time
import json
import logging
import threading
import psutil
import socket
import platform
from typing import Dict, List, Any, Optional, Union, Callable, Deque
from datetime import datetime, timedelta
from collections import deque, defaultdict
import prometheus_client as prom

# Configure logging
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = prom.Counter('bloxapi_request_count', 'Total API request count',
                           ['method', 'endpoint', 'status'])
REQUEST_LATENCY = prom.Histogram('bloxapi_request_latency_seconds', 'API request latency',
                               ['method', 'endpoint'])
ACTIVE_REQUESTS = prom.Gauge('bloxapi_active_requests', 'Number of active API requests')
ERROR_COUNT = prom.Counter('bloxapi_error_count', 'API error count',
                         ['method', 'endpoint', 'error_type'])
CACHE_HIT_COUNT = prom.Counter('bloxapi_cache_hit_count', 'Cache hit count',
                             ['cache_type'])
CACHE_MISS_COUNT = prom.Counter('bloxapi_cache_miss_count', 'Cache miss count',
                              ['cache_type'])
RATE_LIMIT_COUNT = prom.Counter('bloxapi_rate_limit_count', 'Rate limit count',
                              ['ip', 'endpoint'])
SYSTEM_MEMORY_USAGE = prom.Gauge('bloxapi_system_memory_percent', 'System memory usage percentage')
SYSTEM_CPU_USAGE = prom.Gauge('bloxapi_system_cpu_percent', 'System CPU usage percentage')
SYSTEM_DISK_USAGE = prom.Gauge('bloxapi_system_disk_percent', 'System disk usage percentage')
CONCURRENT_USERS = prom.Gauge('bloxapi_concurrent_users', 'Number of concurrent users')
DB_QUERY_COUNT = prom.Counter('bloxapi_db_query_count', 'Database query count',
                            ['query_type'])
DB_QUERY_LATENCY = prom.Histogram('bloxapi_db_query_latency_seconds', 'Database query latency',
                                ['query_type'])

class ResourceMonitor:
    """
    Class for monitoring system and application resources
    """
    
    def __init__(self, history_size: int = 3600, check_interval: int = 10):
        """
        Initialize the resource monitor
        
        Args:
            history_size: Number of data points to keep in history (default: 1 hour at 1 second intervals)
            check_interval: Interval between resource checks in seconds
        """
        self.history_size = history_size
        self.check_interval = check_interval
        self.running = False
        self.monitor_thread = None
        
        # Metrics history for time-series data
        self.cpu_history: Deque[Dict[str, Any]] = deque(maxlen=history_size)
        self.memory_history: Deque[Dict[str, Any]] = deque(maxlen=history_size)
        self.disk_history: Deque[Dict[str, Any]] = deque(maxlen=history_size)
        self.network_history: Deque[Dict[str, Any]] = deque(maxlen=history_size)
        
        # API metrics
        self.request_history: Deque[Dict[str, Any]] = deque(maxlen=history_size)
        self.endpoint_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'count': 0,
            'errors': 0,
            'total_time': 0,
            'avg_time': 0,
            'min_time': float('inf'),
            'max_time': 0
        })
        
        # Current request tracking
        self.active_requests: Dict[str, Dict[str, Any]] = {}
        
        # Initialize Prometheus metrics endpoint if not already
        if not hasattr(prom, '_initialized'):
            try:
                prom.start_http_server(9090)
                setattr(prom, '_initialized', True)
                logger.info("Prometheus metrics server started on port 9090")
            except Exception as e:
                logger.error(f"Failed to start Prometheus server: {e}")
    
    def start(self) -> None:
        """
        Start the resource monitoring
        """
        if self.running:
            logger.warning("Resource monitor is already running")
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info(f"Resource monitor started with {self.check_interval}s interval")
    
    def stop(self) -> None:
        """
        Stop the resource monitoring
        """
        if not self.running:
            logger.warning("Resource monitor is not running")
            return
        
        self.running = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=10)
        
        logger.info("Resource monitor stopped")
    
    def _monitor_loop(self) -> None:
        """
        Main monitoring loop
        """
        while self.running:
            try:
                # Collect system metrics
                self._collect_system_metrics()
                
                # Sleep until next check
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in resource monitor loop: {e}")
                time.sleep(self.check_interval)
    
    def _collect_system_metrics(self) -> None:
        """
        Collect system resource metrics
        """
        timestamp = datetime.now().isoformat()
        
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
            cpu_load = os.getloadavg() if hasattr(os, 'getloadavg') else (0, 0, 0)
            
            cpu_info = {
                'timestamp': timestamp,
                'percent': cpu_percent,
                'per_core': cpu_per_core,
                'load_avg_1min': cpu_load[0],
                'load_avg_5min': cpu_load[1],
                'load_avg_15min': cpu_load[2]
            }
            
            self.cpu_history.append(cpu_info)
            SYSTEM_CPU_USAGE.set(cpu_percent)
            
            # Memory usage
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            memory_info = {
                'timestamp': timestamp,
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent,
                'swap_total': swap.total,
                'swap_used': swap.used,
                'swap_percent': swap.percent
            }
            
            self.memory_history.append(memory_info)
            SYSTEM_MEMORY_USAGE.set(memory.percent)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            io_counters = psutil.disk_io_counters()
            
            disk_info = {
                'timestamp': timestamp,
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent,
                'read_count': io_counters.read_count if io_counters else 0,
                'write_count': io_counters.write_count if io_counters else 0,
                'read_bytes': io_counters.read_bytes if io_counters else 0,
                'write_bytes': io_counters.write_bytes if io_counters else 0
            }
            
            self.disk_history.append(disk_info)
            SYSTEM_DISK_USAGE.set(disk.percent)
            
            # Network usage
            net_io_counters = psutil.net_io_counters()
            
            network_info = {
                'timestamp': timestamp,
                'bytes_sent': net_io_counters.bytes_sent,
                'bytes_recv': net_io_counters.bytes_recv,
                'packets_sent': net_io_counters.packets_sent,
                'packets_recv': net_io_counters.packets_recv,
                'errin': net_io_counters.errin,
                'errout': net_io_counters.errout,
                'dropin': net_io_counters.dropin,
                'dropout': net_io_counters.dropout
            }
            
            self.network_history.append(network_info)
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get basic system information
        
        Returns:
            Dictionary with system information
        """
        try:
            info = {
                'hostname': socket.gethostname(),
                'platform': platform.platform(),
                'python_version': platform.python_version(),
                'cpu_count': psutil.cpu_count(),
                'cpu_count_physical': psutil.cpu_count(logical=False),
                'cpu_freq': psutil.cpu_freq().current if psutil.cpu_freq() else None,
                'memory_total': psutil.virtual_memory().total,
                'disk_total': psutil.disk_usage('/').total,
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                'uptime_seconds': time.time() - psutil.boot_time()
            }
            
            return info
        
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {'error': str(e)}
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """
        Get current system metrics
        
        Returns:
            Dictionary with current metrics
        """
        try:
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': psutil.cpu_percent(interval=0.1),
                    'per_core': psutil.cpu_percent(interval=0.1, percpu=True),
                    'load_avg': os.getloadavg() if hasattr(os, 'getloadavg') else (0, 0, 0)
                },
                'memory': {
                    'percent': psutil.virtual_memory().percent,
                    'used': psutil.virtual_memory().used,
                    'available': psutil.virtual_memory().available,
                    'swap_percent': psutil.swap_memory().percent
                },
                'disk': {
                    'percent': psutil.disk_usage('/').percent,
                    'used': psutil.disk_usage('/').used,
                    'free': psutil.disk_usage('/').free
                },
                'network': {
                    'connections': len(psutil.net_connections()),
                    'bytes_sent': psutil.net_io_counters().bytes_sent,
                    'bytes_recv': psutil.net_io_counters().bytes_recv
                },
                'process': {
                    'count': len(psutil.pids()),
                    'this_process': {
                        'cpu_percent': psutil.Process().cpu_percent(interval=0.1),
                        'memory_percent': psutil.Process().memory_percent(),
                        'threads': psutil.Process().num_threads(),
                        'open_files': len(psutil.Process().open_files()),
                        'connections': len(psutil.Process().connections())
                    }
                }
            }
            
            return metrics
        
        except Exception as e:
            logger.error(f"Error getting current metrics: {e}")
            return {'error': str(e)}
    
    def get_historical_metrics(self, metric_type: str, 
                             time_range: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get historical metrics of a specific type
        
        Args:
            metric_type: Type of metric (cpu, memory, disk, network, request)
            time_range: Time range in seconds (None for all available data)
            
        Returns:
            List of metric data points
        """
        try:
            if metric_type == 'cpu':
                history = list(self.cpu_history)
            elif metric_type == 'memory':
                history = list(self.memory_history)
            elif metric_type == 'disk':
                history = list(self.disk_history)
            elif metric_type == 'network':
                history = list(self.network_history)
            elif metric_type == 'request':
                history = list(self.request_history)
            else:
                return []
            
            # Filter by time range if specified
            if time_range is not None:
                cutoff_time = datetime.now() - timedelta(seconds=time_range)
                cutoff_str = cutoff_time.isoformat()
                
                history = [
                    item for item in history
                    if item.get('timestamp', '') >= cutoff_str
                ]
            
            return history
        
        except Exception as e:
            logger.error(f"Error getting historical metrics: {e}")
            return []
    
    def record_request(self, request_id: str, method: str, endpoint: str, 
                     status_code: int, response_time: float,
                     error_type: Optional[str] = None) -> None:
        """
        Record an API request
        
        Args:
            request_id: Unique request ID
            method: HTTP method
            endpoint: API endpoint
            status_code: HTTP status code
            response_time: Response time in seconds
            error_type: Type of error if status code >= 400
        """
        try:
            timestamp = datetime.now().isoformat()
            
            # Record in request history
            request_data = {
                'request_id': request_id,
                'timestamp': timestamp,
                'method': method,
                'endpoint': endpoint,
                'status_code': status_code,
                'response_time': response_time,
                'error_type': error_type
            }
            
            self.request_history.append(request_data)
            
            # Update endpoint stats
            if endpoint in self.endpoint_stats:
                self.endpoint_stats[endpoint]['count'] += 1
                self.endpoint_stats[endpoint]['total_time'] += response_time
                self.endpoint_stats[endpoint]['avg_time'] = (
                    self.endpoint_stats[endpoint]['total_time'] / 
                    self.endpoint_stats[endpoint]['count']
                )
                self.endpoint_stats[endpoint]['min_time'] = min(
                    self.endpoint_stats[endpoint]['min_time'],
                    response_time
                )
                self.endpoint_stats[endpoint]['max_time'] = max(
                    self.endpoint_stats[endpoint]['max_time'],
                    response_time
                )
                
                if status_code >= 400:
                    self.endpoint_stats[endpoint]['errors'] += 1
            else:
                self.endpoint_stats[endpoint] = {
                    'count': 1,
                    'errors': 1 if status_code >= 400 else 0,
                    'total_time': response_time,
                    'avg_time': response_time,
                    'min_time': response_time,
                    'max_time': response_time
                }
            
            # Update Prometheus metrics
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=str(status_code)).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(response_time)
            
            if status_code >= 400 and error_type:
                ERROR_COUNT.labels(method=method, endpoint=endpoint, error_type=error_type).inc()
        
        except Exception as e:
            logger.error(f"Error recording request: {e}")
    
    def start_request(self, request_id: str, method: str, 
                    endpoint: str, ip: str) -> None:
        """
        Track the start of an API request
        
        Args:
            request_id: Unique request ID
            method: HTTP method
            endpoint: API endpoint
            ip: Client IP address
        """
        try:
            # Record request start
            self.active_requests[request_id] = {
                'method': method,
                'endpoint': endpoint,
                'ip': ip,
                'start_time': time.time()
            }
            
            # Update active request gauge
            ACTIVE_REQUESTS.inc()
        
        except Exception as e:
            logger.error(f"Error starting request tracking: {e}")
    
    def end_request(self, request_id: str, status_code: int,
                  error_type: Optional[str] = None) -> None:
        """
        Track the end of an API request
        
        Args:
            request_id: Unique request ID
            status_code: HTTP status code
            error_type: Type of error if status code >= 400
        """
        try:
            # Check if request exists
            if request_id in self.active_requests:
                # Calculate response time
                start_time = self.active_requests[request_id]['start_time']
                response_time = time.time() - start_time
                
                # Record request
                self.record_request(
                    request_id=request_id,
                    method=self.active_requests[request_id]['method'],
                    endpoint=self.active_requests[request_id]['endpoint'],
                    status_code=status_code,
                    response_time=response_time,
                    error_type=error_type
                )
                
                # Remove from active requests
                del self.active_requests[request_id]
                
                # Update active request gauge
                ACTIVE_REQUESTS.dec()
        
        except Exception as e:
            logger.error(f"Error ending request tracking: {e}")
    
    def record_cache_event(self, cache_type: str, hit: bool) -> None:
        """
        Record a cache hit or miss event
        
        Args:
            cache_type: Type of cache (e.g., 'redis', 'memory')
            hit: True if cache hit, False if cache miss
        """
        try:
            if hit:
                CACHE_HIT_COUNT.labels(cache_type=cache_type).inc()
            else:
                CACHE_MISS_COUNT.labels(cache_type=cache_type).inc()
        
        except Exception as e:
            logger.error(f"Error recording cache event: {e}")
    
    def record_rate_limit(self, ip: str, endpoint: str) -> None:
        """
        Record a rate limit event
        
        Args:
            ip: Client IP address
            endpoint: API endpoint
        """
        try:
            RATE_LIMIT_COUNT.labels(ip=ip, endpoint=endpoint).inc()
        
        except Exception as e:
            logger.error(f"Error recording rate limit: {e}")
    
    def record_db_query(self, query_type: str, latency: float) -> None:
        """
        Record a database query
        
        Args:
            query_type: Type of query (e.g., 'select', 'insert', 'update', 'delete')
            latency: Query latency in seconds
        """
        try:
            DB_QUERY_COUNT.labels(query_type=query_type).inc()
            DB_QUERY_LATENCY.labels(query_type=query_type).observe(latency)
        
        except Exception as e:
            logger.error(f"Error recording database query: {e}")
    
    def update_concurrent_users(self, count: int) -> None:
        """
        Update the concurrent users count
        
        Args:
            count: Number of concurrent users
        """
        try:
            CONCURRENT_USERS.set(count)
        
        except Exception as e:
            logger.error(f"Error updating concurrent users: {e}")
    
    def get_endpoint_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics for each API endpoint
        
        Returns:
            Dictionary of endpoint statistics
        """
        return dict(self.endpoint_stats)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get a summary of API performance
        
        Returns:
            Dictionary with performance summary
        """
        try:
            # Calculate overall stats
            total_requests = sum(stats['count'] for stats in self.endpoint_stats.values())
            total_errors = sum(stats['errors'] for stats in self.endpoint_stats.values())
            total_time = sum(stats['total_time'] for stats in self.endpoint_stats.values())
            
            if total_requests > 0:
                avg_time = total_time / total_requests
                error_rate = (total_errors / total_requests) * 100
            else:
                avg_time = 0
                error_rate = 0
            
            # Get top endpoints by request count
            sorted_endpoints = sorted(
                self.endpoint_stats.items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )
            top_endpoints = {
                endpoint: stats for endpoint, stats in sorted_endpoints[:10]
            }
            
            # Get top slow endpoints
            sorted_by_time = sorted(
                self.endpoint_stats.items(),
                key=lambda x: x[1]['avg_time'],
                reverse=True
            )
            top_slow_endpoints = {
                endpoint: stats for endpoint, stats in sorted_by_time[:10]
            }
            
            # Get current system resource usage
            current_metrics = self.get_current_metrics()
            
            summary = {
                'timestamp': datetime.now().isoformat(),
                'total_requests': total_requests,
                'total_errors': total_errors,
                'error_rate': error_rate,
                'avg_response_time': avg_time,
                'active_requests': len(self.active_requests),
                'top_endpoints': top_endpoints,
                'top_slow_endpoints': top_slow_endpoints,
                'system_resources': {
                    'cpu_percent': current_metrics.get('cpu', {}).get('percent', 0),
                    'memory_percent': current_metrics.get('memory', {}).get('percent', 0),
                    'disk_percent': current_metrics.get('disk', {}).get('percent', 0)
                }
            }
            
            return summary
        
        except Exception as e:
            logger.error(f"Error getting performance summary: {e}")
            return {'error': str(e)}


class RequestTracker:
    """
    Middleware for tracking API requests
    """
    
    def __init__(self, monitor: ResourceMonitor):
        """
        Initialize the request tracker
        
        Args:
            monitor: ResourceMonitor instance
        """
        self.monitor = monitor
    
    def before_request(self, request) -> None:
        """
        Track request before processing
        
        Args:
            request: Flask request object
        """
        # Generate request ID if not already present
        request_id = request.headers.get('X-Request-ID')
        if not request_id:
            request_id = str(uuid.uuid4())
            request.request_id = request_id
        
        # Start request tracking
        self.monitor.start_request(
            request_id=request_id,
            method=request.method,
            endpoint=request.path,
            ip=request.remote_addr
        )
    
    def after_request(self, response, request) -> None:
        """
        Track request after processing
        
        Args:
            response: Flask response object
            request: Flask request object
        """
        # Get request ID
        request_id = getattr(request, 'request_id', None)
        if not request_id:
            request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        
        # End request tracking
        self.monitor.end_request(
            request_id=request_id,
            status_code=response.status_code,
            error_type=None  # No error for successful responses
        )
        
        # Add Request-ID header to response
        response.headers['X-Request-ID'] = request_id
    
    def handle_error(self, error, request) -> None:
        """
        Track request error
        
        Args:
            error: Exception object
            request: Flask request object
        """
        # Get request ID
        request_id = getattr(request, 'request_id', None)
        if not request_id:
            request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        
        # Determine error type and status code
        error_type = error.__class__.__name__
        status_code = getattr(error, 'code', 500)
        
        # End request tracking with error
        self.monitor.end_request(
            request_id=request_id,
            status_code=status_code,
            error_type=error_type
        )


# Global resource monitor instance
_resource_monitor = None

def get_resource_monitor() -> ResourceMonitor:
    """
    Get or create the global resource monitor instance
    
    Returns:
        ResourceMonitor instance
    """
    global _resource_monitor
    
    if _resource_monitor is None:
        _resource_monitor = ResourceMonitor()
    
    return _resource_monitor


def get_request_tracker() -> RequestTracker:
    """
    Get a request tracker for the global resource monitor
    
    Returns:
        RequestTracker instance
    """
    monitor = get_resource_monitor()
    return RequestTracker(monitor)


def start_monitoring() -> ResourceMonitor:
    """
    Start the global resource monitor
    
    Returns:
        ResourceMonitor instance
    """
    monitor = get_resource_monitor()
    monitor.start()
    return monitor


def stop_monitoring() -> None:
    """
    Stop the global resource monitor
    """
    global _resource_monitor
    
    if _resource_monitor:
        _resource_monitor.stop()


def get_system_metrics() -> Dict[str, Any]:
    """
    Get current system metrics
    
    Returns:
        Dictionary with system metrics
    """
    monitor = get_resource_monitor()
    return monitor.get_current_metrics()


def get_performance_report() -> Dict[str, Any]:
    """
    Get API performance report
    
    Returns:
        Dictionary with performance report
    """
    monitor = get_resource_monitor()
    return monitor.get_performance_summary()