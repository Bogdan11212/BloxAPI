"""
Resource Monitoring Module for BloxAPI

This module provides functionality for monitoring system resources,
API performance, and application metrics.
"""

import os
import time
import logging
import threading
import json
from typing import Dict, List, Any, Optional, Union, Callable, Deque
from datetime import datetime, timedelta
from collections import defaultdict, deque
import psutil

# Configure logging
logger = logging.getLogger(__name__)

class ResourceMonitor:
    """
    Monitor system resources and API performance
    """
    
    def __init__(self, max_history_size: int = 60):
        """
        Initialize resource monitor
        
        Args:
            max_history_size: Maximum number of historical data points to keep
        """
        self.max_history_size = max_history_size
        self.cpu_history: Deque[Dict[str, Any]] = deque(maxlen=max_history_size)
        self.memory_history: Deque[Dict[str, Any]] = deque(maxlen=max_history_size)
        self.disk_history: Deque[Dict[str, Any]] = deque(maxlen=max_history_size)
        self.network_history: Deque[Dict[str, Any]] = deque(maxlen=max_history_size)
        self.request_history: Dict[str, Deque[Dict[str, Any]]] = defaultdict(
            lambda: deque(maxlen=max_history_size)
        )
        self.endpoint_stats: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "count": 0,
                "errors": 0,
                "total_time": 0,
                "min_time": float('inf'),
                "max_time": 0,
                "last_access": None
            }
        )
        self.slow_requests: Deque[Dict[str, Any]] = deque(maxlen=100)
        self.error_requests: Deque[Dict[str, Any]] = deque(maxlen=100)
        
        # Set up monitoring thread
        self.monitoring_interval = 60  # seconds
        self.stop_event = threading.Event()
        self.monitor_thread = threading.Thread(target=self._monitor_resources, daemon=True)
        self.monitor_thread.start()
    
    def _monitor_resources(self) -> None:
        """
        Periodically monitor system resources
        """
        while not self.stop_event.is_set():
            try:
                # Get current metrics
                cpu_metrics = self._get_cpu_metrics()
                memory_metrics = self._get_memory_metrics()
                disk_metrics = self._get_disk_metrics()
                network_metrics = self._get_network_metrics()
                
                # Add to history
                self.cpu_history.append(cpu_metrics)
                self.memory_history.append(memory_metrics)
                self.disk_history.append(disk_metrics)
                self.network_history.append(network_metrics)
                
                # Log if resources are reaching critical levels
                if cpu_metrics['percent'] > 80:
                    logger.warning(f"High CPU usage: {cpu_metrics['percent']}%")
                
                if memory_metrics['percent'] > 80:
                    logger.warning(f"High memory usage: {memory_metrics['percent']}%")
                
                if disk_metrics['percent'] > 80:
                    logger.warning(f"High disk usage: {disk_metrics['percent']}%")
            
            except Exception as e:
                logger.error(f"Error monitoring resources: {e}")
            
            # Wait for next check
            time.sleep(self.monitoring_interval)
    
    def _get_cpu_metrics(self) -> Dict[str, Any]:
        """
        Get CPU metrics
        
        Returns:
            Dictionary with CPU metrics
        """
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        load_avg = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else (0, 0, 0)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'percent': cpu_percent,
            'count': cpu_count,
            'load_1min': load_avg[0],
            'load_5min': load_avg[1],
            'load_15min': load_avg[2]
        }
    
    def _get_memory_metrics(self) -> Dict[str, Any]:
        """
        Get memory metrics
        
        Returns:
            Dictionary with memory metrics
        """
        memory = psutil.virtual_memory()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'free': memory.free,
            'percent': memory.percent
        }
    
    def _get_disk_metrics(self) -> Dict[str, Any]:
        """
        Get disk metrics
        
        Returns:
            Dictionary with disk metrics
        """
        # Get disk usage for current directory or root
        path = os.path.abspath(os.curdir)
        disk = psutil.disk_usage(path)
        
        io_counters = psutil.disk_io_counters() if hasattr(psutil, 'disk_io_counters') else None
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'path': path,
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
        
        if io_counters:
            metrics.update({
                'read_count': io_counters.read_count,
                'write_count': io_counters.write_count,
                'read_bytes': io_counters.read_bytes,
                'write_bytes': io_counters.write_bytes
            })
        
        return metrics
    
    def _get_network_metrics(self) -> Dict[str, Any]:
        """
        Get network metrics
        
        Returns:
            Dictionary with network metrics
        """
        net_io = psutil.net_io_counters() if hasattr(psutil, 'net_io_counters') else None
        
        metrics = {
            'timestamp': datetime.now().isoformat()
        }
        
        if net_io:
            metrics.update({
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errin': getattr(net_io, 'errin', 0),
                'errout': getattr(net_io, 'errout', 0),
                'dropin': getattr(net_io, 'dropin', 0),
                'dropout': getattr(net_io, 'dropout', 0)
            })
        
        return metrics
    
    def record_request(self, endpoint: str, duration: float, status_code: int, 
                    method: str, path: str) -> None:
        """
        Record an API request
        
        Args:
            endpoint: API endpoint
            duration: Request duration in seconds
            status_code: HTTP status code
            method: HTTP method
            path: Request path
        """
        # Record request data
        request_data = {
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'duration': duration,
            'status_code': status_code,
            'method': method,
            'path': path
        }
        
        # Add to history
        self.request_history[endpoint].append(request_data)
        
        # Update endpoint stats
        stats = self.endpoint_stats[endpoint]
        stats['count'] += 1
        stats['total_time'] += duration
        stats['min_time'] = min(stats['min_time'], duration)
        stats['max_time'] = max(stats['max_time'], duration)
        stats['last_access'] = datetime.now().isoformat()
        
        if status_code >= 400:
            stats['errors'] += 1
            
            # Track error requests
            self.error_requests.append(request_data)
        
        # Track slow requests (> 1 second)
        if duration > 1.0:
            self.slow_requests.append(request_data)
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get current system metrics
        
        Returns:
            Dictionary with system metrics
        """
        cpu_metrics = self._get_cpu_metrics()
        memory_metrics = self._get_memory_metrics()
        disk_metrics = self._get_disk_metrics()
        network_metrics = self._get_network_metrics()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': cpu_metrics,
            'memory': memory_metrics,
            'disk': disk_metrics,
            'network': network_metrics
        }
    
    def get_historical_metrics(self, metric_type: str, time_range: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get historical metrics of a specific type
        
        Args:
            metric_type: Type of metric (cpu, memory, disk, network, request)
            time_range: Time range in seconds (optional)
            
        Returns:
            List of historical metrics
        """
        history = None
        
        if metric_type == 'cpu':
            history = list(self.cpu_history)
        elif metric_type == 'memory':
            history = list(self.memory_history)
        elif metric_type == 'disk':
            history = list(self.disk_history)
        elif metric_type == 'network':
            history = list(self.network_history)
        elif metric_type == 'request':
            # Flatten request history
            history = []
            for endpoint_history in self.request_history.values():
                history.extend(list(endpoint_history))
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
    
    def get_endpoint_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics for each API endpoint
        
        Returns:
            Dictionary with endpoint statistics
        """
        # Calculate average response time for each endpoint
        result = {}
        
        for endpoint, stats in self.endpoint_stats.items():
            count = stats['count']
            total_time = stats['total_time']
            
            result[endpoint] = {
                'count': count,
                'errors': stats['errors'],
                'error_rate': (stats['errors'] / count) if count > 0 else 0,
                'avg_time': (total_time / count) if count > 0 else 0,
                'min_time': stats['min_time'] if stats['min_time'] != float('inf') else 0,
                'max_time': stats['max_time'],
                'last_access': stats['last_access']
            }
        
        return result
    
    def get_slow_requests(self) -> List[Dict[str, Any]]:
        """
        Get slow requests
        
        Returns:
            List of slow requests
        """
        return list(self.slow_requests)
    
    def get_error_requests(self) -> List[Dict[str, Any]]:
        """
        Get error requests
        
        Returns:
            List of error requests
        """
        return list(self.error_requests)
    
    def get_performance_report(self) -> Dict[str, Any]:
        """
        Get performance report
        
        Returns:
            Dictionary with performance report
        """
        # Get current metrics
        system_metrics = self.get_system_metrics()
        
        # Get endpoint stats
        endpoint_stats = self.get_endpoint_stats()
        
        # Calculate overall API stats
        total_requests = sum(stats['count'] for stats in endpoint_stats.values())
        total_errors = sum(stats['errors'] for stats in endpoint_stats.values())
        error_rate = (total_errors / total_requests) if total_requests > 0 else 0
        
        # Get average response time
        total_time = sum(stats['avg_time'] * stats['count'] for stats in endpoint_stats.values())
        avg_response_time = (total_time / total_requests) if total_requests > 0 else 0
        
        # Get slow and error requests
        slow_requests = self.get_slow_requests()
        error_requests = self.get_error_requests()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'system': system_metrics,
            'api': {
                'total_requests': total_requests,
                'total_errors': total_errors,
                'error_rate': error_rate,
                'avg_response_time': avg_response_time,
                'slow_requests_count': len(slow_requests),
                'error_requests_count': len(error_requests)
            },
            'top_endpoints': {
                endpoint: stats for endpoint, stats in sorted(
                    endpoint_stats.items(), 
                    key=lambda x: x[1]['count'], 
                    reverse=True
                )[:5]  # Top 5 endpoints by count
            },
            'slowest_endpoints': {
                endpoint: stats for endpoint, stats in sorted(
                    endpoint_stats.items(), 
                    key=lambda x: x[1]['avg_time'], 
                    reverse=True
                )[:5]  # Top 5 endpoints by average time
            }
        }
    
    def stop(self) -> None:
        """
        Stop the resource monitor
        """
        self.stop_event.set()
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)


# Global resource monitor instance
_resource_monitor = None

def get_resource_monitor() -> ResourceMonitor:
    """
    Get the global resource monitor instance
    
    Returns:
        ResourceMonitor instance
    """
    global _resource_monitor
    
    if _resource_monitor is None:
        _resource_monitor = ResourceMonitor()
    
    return _resource_monitor


def get_system_metrics() -> Dict[str, Any]:
    """
    Get current system metrics
    
    Returns:
        Dictionary with system metrics
    """
    monitor = get_resource_monitor()
    return monitor.get_system_metrics()


def get_performance_report() -> Dict[str, Any]:
    """
    Get performance report
    
    Returns:
        Dictionary with performance report
    """
    monitor = get_resource_monitor()
    return monitor.get_performance_report()


def record_request(endpoint: str, duration: float, status_code: int, 
                method: str, path: str) -> None:
    """
    Record an API request
    
    Args:
        endpoint: API endpoint
        duration: Request duration in seconds
        status_code: HTTP status code
        method: HTTP method
        path: Request path
    """
    monitor = get_resource_monitor()
    monitor.record_request(endpoint, duration, status_code, method, path)