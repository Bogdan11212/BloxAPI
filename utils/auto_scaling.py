"""
Auto Scaling for BloxAPI

This module provides functionality for automatically scaling resources
based on load and traffic patterns. It monitors resource usage and
adjusts capacity as needed.
"""

import os
import time
import logging
import threading
import json
from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime, timedelta
import subprocess
import signal
import atexit
import psutil
from collections import deque

# Configure logging
logger = logging.getLogger(__name__)

class ResourceMonitor:
    """
    Monitor system resources like CPU, memory, and disk usage
    """
    
    def __init__(self, history_length: int = 60):
        """
        Initialize the resource monitor
        
        Args:
            history_length: Number of data points to keep in history
        """
        self.history_length = history_length
        
        # Initialize metrics history
        self.cpu_history = deque(maxlen=history_length)
        self.memory_history = deque(maxlen=history_length)
        self.disk_io_history = deque(maxlen=history_length)
        self.network_io_history = deque(maxlen=history_length)
        
        # Initialize last IO counters for rate calculation
        self.last_disk_io = None
        self.last_network_io = None
        self.last_check_time = None
    
    def get_cpu_usage(self) -> float:
        """
        Get current CPU usage percentage
        
        Returns:
            CPU usage percentage
        """
        return psutil.cpu_percent(interval=0.1)
    
    def get_memory_usage(self) -> Dict[str, float]:
        """
        Get current memory usage
        
        Returns:
            Dictionary with memory usage metrics
        """
        memory = psutil.virtual_memory()
        return {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percent": memory.percent
        }
    
    def get_disk_io(self) -> Dict[str, float]:
        """
        Get disk I/O rates
        
        Returns:
            Dictionary with disk I/O metrics
        """
        current_disk_io = psutil.disk_io_counters()
        current_time = time.time()
        
        result = {
            "read_bytes": current_disk_io.read_bytes,
            "write_bytes": current_disk_io.write_bytes,
            "read_count": current_disk_io.read_count,
            "write_count": current_disk_io.write_count,
            "read_rate": 0,
            "write_rate": 0
        }
        
        # Calculate rates if we have previous measurements
        if self.last_disk_io and self.last_check_time:
            time_diff = current_time - self.last_check_time
            
            if time_diff > 0:
                read_diff = current_disk_io.read_bytes - self.last_disk_io.read_bytes
                write_diff = current_disk_io.write_bytes - self.last_disk_io.write_bytes
                
                result["read_rate"] = read_diff / time_diff
                result["write_rate"] = write_diff / time_diff
        
        # Update last values
        self.last_disk_io = current_disk_io
        self.last_check_time = current_time
        
        return result
    
    def get_network_io(self) -> Dict[str, float]:
        """
        Get network I/O rates
        
        Returns:
            Dictionary with network I/O metrics
        """
        current_network_io = psutil.net_io_counters()
        current_time = time.time()
        
        result = {
            "bytes_sent": current_network_io.bytes_sent,
            "bytes_recv": current_network_io.bytes_recv,
            "packets_sent": current_network_io.packets_sent,
            "packets_recv": current_network_io.packets_recv,
            "send_rate": 0,
            "recv_rate": 0
        }
        
        # Calculate rates if we have previous measurements
        if self.last_network_io and self.last_check_time:
            time_diff = current_time - self.last_check_time
            
            if time_diff > 0:
                send_diff = current_network_io.bytes_sent - self.last_network_io.bytes_sent
                recv_diff = current_network_io.bytes_recv - self.last_network_io.bytes_recv
                
                result["send_rate"] = send_diff / time_diff
                result["recv_rate"] = recv_diff / time_diff
        
        # Update last values
        self.last_network_io = current_network_io
        self.last_check_time = current_time
        
        return result
    
    def update_metrics(self) -> Dict[str, Any]:
        """
        Update all metrics and add to history
        
        Returns:
            Dictionary with current metrics
        """
        # Get current metrics
        cpu = self.get_cpu_usage()
        memory = self.get_memory_usage()
        disk_io = self.get_disk_io()
        network_io = self.get_network_io()
        
        # Add to history
        self.cpu_history.append(cpu)
        self.memory_history.append(memory["percent"])
        self.disk_io_history.append({
            "read_rate": disk_io["read_rate"],
            "write_rate": disk_io["write_rate"]
        })
        self.network_io_history.append({
            "send_rate": network_io["send_rate"],
            "recv_rate": network_io["recv_rate"]
        })
        
        # Return current metrics
        return {
            "cpu": cpu,
            "memory": memory,
            "disk_io": disk_io,
            "network_io": network_io,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_average_metrics(self, window: int = 5) -> Dict[str, float]:
        """
        Get average metrics over a time window
        
        Args:
            window: Number of data points to average
            
        Returns:
            Dictionary with average metrics
        """
        window = min(window, len(self.cpu_history))
        
        if window == 0:
            return {
                "cpu": 0,
                "memory": 0,
                "disk_read": 0,
                "disk_write": 0,
                "network_send": 0,
                "network_recv": 0
            }
        
        # Calculate averages
        cpu_avg = sum(list(self.cpu_history)[-window:]) / window
        memory_avg = sum(list(self.memory_history)[-window:]) / window
        
        disk_read_rates = [d["read_rate"] for d in list(self.disk_io_history)[-window:]]
        disk_write_rates = [d["write_rate"] for d in list(self.disk_io_history)[-window:]]
        disk_read_avg = sum(disk_read_rates) / window
        disk_write_avg = sum(disk_write_rates) / window
        
        network_send_rates = [n["send_rate"] for n in list(self.network_io_history)[-window:]]
        network_recv_rates = [n["recv_rate"] for n in list(self.network_io_history)[-window:]]
        network_send_avg = sum(network_send_rates) / window
        network_recv_avg = sum(network_recv_rates) / window
        
        return {
            "cpu": cpu_avg,
            "memory": memory_avg,
            "disk_read": disk_read_avg,
            "disk_write": disk_write_avg,
            "network_send": network_send_avg,
            "network_recv": network_recv_avg
        }


class ProcessManager:
    """
    Manage worker processes for horizontal scaling
    """
    
    def __init__(self, process_cmd: List[str], min_workers: int = 1, 
                max_workers: int = 4, working_dir: Optional[str] = None):
        """
        Initialize the process manager
        
        Args:
            process_cmd: Command to run for each worker
            min_workers: Minimum number of workers
            max_workers: Maximum number of workers
            working_dir: Working directory for worker processes
        """
        self.process_cmd = process_cmd
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.working_dir = working_dir or os.getcwd()
        
        # Track worker processes
        self.workers: Dict[int, subprocess.Popen] = {}
        
        # Register cleanup handler
        atexit.register(self.cleanup)
    
    def start_worker(self) -> Optional[int]:
        """
        Start a new worker process
        
        Returns:
            Process ID of the new worker, or None if failed
        """
        try:
            # Check if we're at max workers
            if len(self.workers) >= self.max_workers:
                logger.warning(f"Already at maximum workers ({self.max_workers})")
                return None
            
            # Start the process
            process = subprocess.Popen(
                self.process_cmd,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            pid = process.pid
            self.workers[pid] = process
            
            logger.info(f"Started worker process {pid}, total workers: {len(self.workers)}")
            return pid
        
        except Exception as e:
            logger.error(f"Error starting worker: {e}")
            return None
    
    def stop_worker(self, pid: Optional[int] = None) -> bool:
        """
        Stop a worker process
        
        Args:
            pid: Process ID to stop, or None to stop any worker
            
        Returns:
            True if a worker was stopped, False otherwise
        """
        try:
            # Check if we're at min workers
            if len(self.workers) <= self.min_workers:
                logger.warning(f"Already at minimum workers ({self.min_workers})")
                return False
            
            # Choose a worker to stop
            if pid is None or pid not in self.workers:
                pid = next(iter(self.workers.keys()))
            
            # Get the process
            process = self.workers.get(pid)
            
            if process:
                # Try to terminate gracefully
                process.terminate()
                
                # Wait for process to exit (with timeout)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if it doesn't exit
                    process.kill()
                
                # Remove from workers
                del self.workers[pid]
                
                logger.info(f"Stopped worker process {pid}, total workers: {len(self.workers)}")
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Error stopping worker: {e}")
            return False
    
    def ensure_min_workers(self) -> int:
        """
        Ensure minimum number of workers are running
        
        Returns:
            Number of workers started
        """
        workers_to_start = max(0, self.min_workers - len(self.workers))
        
        for _ in range(workers_to_start):
            self.start_worker()
        
        return workers_to_start
    
    def cleanup(self) -> None:
        """
        Clean up all worker processes
        """
        logger.info("Cleaning up worker processes")
        
        for pid, process in list(self.workers.items()):
            try:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                
                logger.info(f"Stopped worker process {pid}")
            
            except Exception as e:
                logger.error(f"Error stopping worker {pid}: {e}")
        
        self.workers.clear()


class AutoScaler:
    """
    Automatic resource scaler based on system metrics
    """
    
    def __init__(self, process_manager: ProcessManager, 
                monitor: ResourceMonitor, check_interval: int = 10):
        """
        Initialize the auto scaler
        
        Args:
            process_manager: Process manager for scaling workers
            monitor: Resource monitor
            check_interval: Interval between scaling checks (seconds)
        """
        self.process_manager = process_manager
        self.monitor = monitor
        self.check_interval = check_interval
        
        # Define scaling thresholds
        self.cpu_high_threshold = 75  # Percentage
        self.cpu_low_threshold = 20   # Percentage
        self.memory_high_threshold = 80  # Percentage
        self.memory_low_threshold = 40   # Percentage
        
        # Track if scaling is active
        self.is_running = False
        self.scaling_thread = None
        
        # Scaling cooldown
        self.last_scale_up_time = None
        self.last_scale_down_time = None
        self.scale_up_cooldown = 60   # Seconds
        self.scale_down_cooldown = 120  # Seconds
    
    def start(self) -> None:
        """
        Start the auto scaler
        """
        if self.is_running:
            logger.warning("Auto scaler is already running")
            return
        
        # Ensure minimum workers are running
        self.process_manager.ensure_min_workers()
        
        # Start monitoring and scaling thread
        self.is_running = True
        self.scaling_thread = threading.Thread(target=self._monitoring_loop)
        self.scaling_thread.daemon = True
        self.scaling_thread.start()
        
        logger.info(f"Started auto scaler with {self.check_interval}s interval")
    
    def stop(self) -> None:
        """
        Stop the auto scaler
        """
        if not self.is_running:
            logger.warning("Auto scaler is not running")
            return
        
        # Stop the monitoring thread
        self.is_running = False
        
        if self.scaling_thread:
            self.scaling_thread.join(timeout=10)
        
        logger.info("Stopped auto scaler")
    
    def _monitoring_loop(self) -> None:
        """
        Main monitoring loop for auto scaling
        """
        while self.is_running:
            try:
                # Update metrics
                self.monitor.update_metrics()
                
                # Get average metrics
                avg_metrics = self.monitor.get_average_metrics(window=3)
                
                # Check if scaling is needed
                self._check_scaling(avg_metrics)
                
                # Wait for next check
                time.sleep(self.check_interval)
            
            except Exception as e:
                logger.error(f"Error in auto scaling loop: {e}")
                time.sleep(self.check_interval)
    
    def _check_scaling(self, metrics: Dict[str, float]) -> None:
        """
        Check if scaling is needed based on metrics
        
        Args:
            metrics: Current system metrics
        """
        current_time = time.time()
        cpu_percent = metrics["cpu"]
        memory_percent = metrics["memory"]
        
        logger.debug(f"Scaling check - CPU: {cpu_percent:.1f}%, Memory: {memory_percent:.1f}%, "
                   f"Workers: {len(self.process_manager.workers)}")
        
        # Check for scale up
        if (cpu_percent > self.cpu_high_threshold or memory_percent > self.memory_high_threshold):
            # Check cooldown
            if (not self.last_scale_up_time or 
                current_time - self.last_scale_up_time > self.scale_up_cooldown):
                
                logger.info(f"High load detected - CPU: {cpu_percent:.1f}%, "
                          f"Memory: {memory_percent:.1f}%")
                
                # Scale up
                if self.process_manager.start_worker():
                    self.last_scale_up_time = current_time
        
        # Check for scale down
        elif (cpu_percent < self.cpu_low_threshold and memory_percent < self.memory_low_threshold):
            # Check cooldown
            if (not self.last_scale_down_time or 
                current_time - self.last_scale_down_time > self.scale_down_cooldown):
                
                logger.info(f"Low load detected - CPU: {cpu_percent:.1f}%, "
                          f"Memory: {memory_percent:.1f}%")
                
                # Scale down
                if self.process_manager.stop_worker():
                    self.last_scale_down_time = current_time
    
    def update_thresholds(self, cpu_high: Optional[float] = None,
                         cpu_low: Optional[float] = None,
                         memory_high: Optional[float] = None,
                         memory_low: Optional[float] = None) -> None:
        """
        Update scaling thresholds
        
        Args:
            cpu_high: CPU high threshold percentage
            cpu_low: CPU low threshold percentage
            memory_high: Memory high threshold percentage
            memory_low: Memory low threshold percentage
        """
        if cpu_high is not None:
            self.cpu_high_threshold = cpu_high
        
        if cpu_low is not None:
            self.cpu_low_threshold = cpu_low
        
        if memory_high is not None:
            self.memory_high_threshold = memory_high
        
        if memory_low is not None:
            self.memory_low_threshold = memory_low
        
        logger.info(f"Updated scaling thresholds - CPU: {self.cpu_low_threshold}-{self.cpu_high_threshold}%, "
                  f"Memory: {self.memory_low_threshold}-{self.memory_high_threshold}%")
    
    def update_cooldowns(self, scale_up: Optional[int] = None,
                        scale_down: Optional[int] = None) -> None:
        """
        Update scaling cooldowns
        
        Args:
            scale_up: Scale up cooldown in seconds
            scale_down: Scale down cooldown in seconds
        """
        if scale_up is not None:
            self.scale_up_cooldown = scale_up
        
        if scale_down is not None:
            self.scale_down_cooldown = scale_down
        
        logger.info(f"Updated scaling cooldowns - Up: {self.scale_up_cooldown}s, "
                  f"Down: {self.scale_down_cooldown}s")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current auto scaler status
        
        Returns:
            Dictionary with status information
        """
        # Get current metrics
        current_metrics = self.monitor.update_metrics()
        avg_metrics = self.monitor.get_average_metrics(window=5)
        
        return {
            "is_running": self.is_running,
            "workers": {
                "current": len(self.process_manager.workers),
                "min": self.process_manager.min_workers,
                "max": self.process_manager.max_workers
            },
            "thresholds": {
                "cpu_high": self.cpu_high_threshold,
                "cpu_low": self.cpu_low_threshold,
                "memory_high": self.memory_high_threshold,
                "memory_low": self.memory_low_threshold
            },
            "cooldowns": {
                "scale_up": self.scale_up_cooldown,
                "scale_down": self.scale_down_cooldown,
                "last_scale_up": (datetime.now() - datetime.fromtimestamp(self.last_scale_up_time)).total_seconds() if self.last_scale_up_time else None,
                "last_scale_down": (datetime.now() - datetime.fromtimestamp(self.last_scale_down_time)).total_seconds() if self.last_scale_down_time else None
            },
            "current_metrics": current_metrics,
            "average_metrics": avg_metrics
        }


# Helper function to create and configure auto scaling
def setup_auto_scaling(worker_command: List[str], min_workers: int = 1,
                     max_workers: int = 4, working_dir: Optional[str] = None,
                     check_interval: int = 10) -> AutoScaler:
    """
    Set up automatic scaling for worker processes
    
    Args:
        worker_command: Command to run for each worker
        min_workers: Minimum number of workers
        max_workers: Maximum number of workers
        working_dir: Working directory for worker processes
        check_interval: Interval between scaling checks (seconds)
        
    Returns:
        Configured auto scaler
    """
    # Create resource monitor
    monitor = ResourceMonitor()
    
    # Create process manager
    process_manager = ProcessManager(
        process_cmd=worker_command,
        min_workers=min_workers,
        max_workers=max_workers,
        working_dir=working_dir
    )
    
    # Create auto scaler
    auto_scaler = AutoScaler(
        process_manager=process_manager,
        monitor=monitor,
        check_interval=check_interval
    )
    
    return auto_scaler


# Global auto scaler instance
_auto_scaler = None

def get_auto_scaler() -> Optional[AutoScaler]:
    """
    Get the global auto scaler instance
    
    Returns:
        Auto scaler instance or None if not initialized
    """
    global _auto_scaler
    return _auto_scaler

def initialize_auto_scaling(worker_command: List[str], min_workers: int = 1,
                          max_workers: int = 4, working_dir: Optional[str] = None,
                          check_interval: int = 10, start: bool = True) -> AutoScaler:
    """
    Initialize the global auto scaler
    
    Args:
        worker_command: Command to run for each worker
        min_workers: Minimum number of workers
        max_workers: Maximum number of workers
        working_dir: Working directory for worker processes
        check_interval: Interval between scaling checks (seconds)
        start: Whether to start the auto scaler immediately
        
    Returns:
        Configured auto scaler
    """
    global _auto_scaler
    
    if _auto_scaler:
        logger.warning("Auto scaler already initialized, stopping previous instance")
        _auto_scaler.stop()
    
    _auto_scaler = setup_auto_scaling(
        worker_command=worker_command,
        min_workers=min_workers,
        max_workers=max_workers,
        working_dir=working_dir,
        check_interval=check_interval
    )
    
    if start:
        _auto_scaler.start()
    
    return _auto_scaler