"""
Monitoring Routes for BloxAPI

This module provides API routes for resource monitoring, performance metrics,
and system health checking.
"""

import logging
from flask import request, jsonify, make_response
from flask_restful import Resource
from utils.resource_monitor import get_resource_monitor, get_system_metrics, get_performance_report
from utils.redis_cache import get_cache

# Configure logging
logger = logging.getLogger(__name__)

class SystemResourcesResource(Resource):
    """
    Resource for system resource monitoring
    """
    
    def get(self):
        """
        Get current system resource usage
        
        Returns:
            Current system metrics or error response
        """
        try:
            # Get current metrics
            metrics = get_system_metrics()
            
            return metrics
        except Exception as e:
            logger.error(f"Error getting system resources: {e}")
            return {"error": str(e)}, 500


class HistoricalMetricsResource(Resource):
    """
    Resource for historical metrics
    """
    
    def get(self, metric_type):
        """
        Get historical metrics of a specific type
        
        Args:
            metric_type: Type of metric (cpu, memory, disk, network, request)
            
        Query Parameters:
            time_range: Time range in seconds (optional)
            
        Returns:
            Historical metrics or error response
        """
        try:
            # Get query parameters
            time_range = request.args.get('time_range')
            if time_range:
                time_range = int(time_range)
            
            # Get resource monitor
            monitor = get_resource_monitor()
            
            # Get historical metrics
            metrics = monitor.get_historical_metrics(metric_type, time_range)
            
            return {"metrics": metrics}
        except Exception as e:
            logger.error(f"Error getting historical metrics: {e}")
            return {"error": str(e)}, 500


class PerformanceResource(Resource):
    """
    Resource for API performance metrics
    """
    
    def get(self):
        """
        Get API performance metrics
        
        Returns:
            Performance metrics or error response
        """
        try:
            # Get performance report
            report = get_performance_report()
            
            return report
        except Exception as e:
            logger.error(f"Error getting performance metrics: {e}")
            return {"error": str(e)}, 500


class EndpointStatsResource(Resource):
    """
    Resource for endpoint-specific statistics
    """
    
    def get(self):
        """
        Get statistics for each API endpoint
        
        Returns:
            Endpoint statistics or error response
        """
        try:
            # Get resource monitor
            monitor = get_resource_monitor()
            
            # Get endpoint stats
            stats = monitor.get_endpoint_stats()
            
            return {"endpoints": stats}
        except Exception as e:
            logger.error(f"Error getting endpoint stats: {e}")
            return {"error": str(e)}, 500


class CacheStatsResource(Resource):
    """
    Resource for cache statistics
    """
    
    def get(self):
        """
        Get cache statistics
        
        Returns:
            Cache statistics or error response
        """
        try:
            # Get cache
            cache = get_cache()
            
            # Get cache stats
            stats = cache.get_stats()
            
            return stats
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"error": str(e)}, 500


class HealthCheckResource(Resource):
    """
    Resource for system health check
    """
    
    def get(self):
        """
        Perform a health check on the system
        
        Returns:
            Health check results
        """
        try:
            # Check system resources
            metrics = get_system_metrics()
            
            # Define health thresholds
            cpu_threshold = 90  # 90% CPU usage
            memory_threshold = 90  # 90% memory usage
            disk_threshold = 90  # 90% disk usage
            
            # Check if any resource is above threshold
            cpu_percent = metrics['cpu']['percent']
            memory_percent = metrics['memory']['percent']
            disk_percent = metrics['disk']['percent']
            
            is_healthy = (cpu_percent < cpu_threshold and 
                        memory_percent < memory_threshold and 
                        disk_percent < disk_threshold)
            
            # Prepare response
            response = {
                "status": "healthy" if is_healthy else "unhealthy",
                "timestamp": metrics.get('timestamp'),
                "checks": {
                    "cpu": {
                        "status": "ok" if cpu_percent < cpu_threshold else "warning",
                        "value": cpu_percent,
                        "threshold": cpu_threshold
                    },
                    "memory": {
                        "status": "ok" if memory_percent < memory_threshold else "warning",
                        "value": memory_percent,
                        "threshold": memory_threshold
                    },
                    "disk": {
                        "status": "ok" if disk_percent < disk_threshold else "warning",
                        "value": disk_percent,
                        "threshold": disk_threshold
                    }
                }
            }
            
            # Set HTTP status code based on health
            status_code = 200 if is_healthy else 503
            
            return make_response(jsonify(response), status_code)
        
        except Exception as e:
            logger.error(f"Error performing health check: {e}")
            return {"status": "error", "error": str(e)}, 500


class LivenessProbeResource(Resource):
    """
    Resource for Kubernetes liveness probe
    """
    
    def get(self):
        """
        Simple liveness check to verify the service is running
        
        Returns:
            Simple status response
        """
        return {"status": "ok"}


class ReadinessProbeResource(Resource):
    """
    Resource for Kubernetes readiness probe
    """
    
    def get(self):
        """
        Readiness check to verify the service can handle requests
        
        Returns:
            Readiness status response
        """
        try:
            # Check if cache is available
            cache = get_cache()
            cache_available = cache.enabled
            
            # Check system resources
            metrics = get_system_metrics()
            
            # Define readiness thresholds (more lenient than health check)
            cpu_threshold = 95  # 95% CPU usage
            memory_threshold = 95  # 95% memory usage
            
            # Check if resources allow handling requests
            cpu_percent = metrics['cpu']['percent']
            memory_percent = metrics['memory']['percent']
            
            is_ready = (cpu_percent < cpu_threshold and 
                       memory_percent < memory_threshold and
                       cache_available)
            
            # Prepare response
            response = {
                "status": "ready" if is_ready else "not_ready",
                "timestamp": metrics.get('timestamp'),
                "checks": {
                    "cpu": {
                        "status": "ok" if cpu_percent < cpu_threshold else "warning",
                        "value": cpu_percent,
                        "threshold": cpu_threshold
                    },
                    "memory": {
                        "status": "ok" if memory_percent < memory_threshold else "warning",
                        "value": memory_percent,
                        "threshold": memory_threshold
                    },
                    "cache": {
                        "status": "ok" if cache_available else "warning",
                        "available": cache_available
                    }
                }
            }
            
            # Set HTTP status code based on readiness
            status_code = 200 if is_ready else 503
            
            return make_response(jsonify(response), status_code)
        
        except Exception as e:
            logger.error(f"Error performing readiness check: {e}")
            return {"status": "error", "error": str(e)}, 500


class MetricsExportResource(Resource):
    """
    Resource for exporting metrics in Prometheus format
    """
    
    def get(self):
        """
        Export metrics in Prometheus format
        
        Returns:
            Prometheus metrics
        """
        try:
            from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
            
            # Generate metrics
            metrics_data = generate_latest()
            
            # Create response
            response = make_response(metrics_data)
            response.headers['Content-Type'] = CONTENT_TYPE_LATEST
            
            return response
        
        except Exception as e:
            logger.error(f"Error exporting metrics: {e}")
            return {"error": str(e)}, 500