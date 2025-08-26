"""
Memory Management System

Efficient memory management for large datasets (1-10MB).
Part of Phase 3: Performance Optimization - Task 3.3

Features:
- Memory monitoring and optimization
- Garbage collection management
- Memory usage < 500MB for 10MB datasets
- Automatic memory cleanup
"""

import gc
import psutil
import os
import time
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path
import threading
import weakref

logger = logging.getLogger(__name__)


@dataclass
class MemoryConfig:
    """Configuration for memory management."""
    memory_limit_mb: int = 500
    gc_threshold: float = 0.8  # Trigger GC when 80% of limit reached
    cleanup_interval: int = 60  # Cleanup every 60 seconds
    enable_monitoring: bool = True
    aggressive_cleanup: bool = False
    memory_warning_threshold: float = 0.7  # Warning at 70% usage


@dataclass
class MemoryStats:
    """Memory usage statistics."""
    current_mb: float
    peak_mb: float
    available_mb: float
    usage_percent: float
    gc_count: int
    cleanup_count: int
    last_cleanup: float


class MemoryManagementSystem:
    """Efficient memory management system for large datasets."""
    
    def __init__(self, config: Optional[MemoryConfig] = None):
        """Initialize the memory management system."""
        self.config = config or MemoryConfig()
        self.process = psutil.Process(os.getpid())
        
        # Memory tracking
        self.memory_stats = MemoryStats(
            current_mb=0.0,
            peak_mb=0.0,
            available_mb=0.0,
            usage_percent=0.0,
            gc_count=0,
            cleanup_count=0,
            last_cleanup=time.time()
        )
        
        # Memory monitoring
        self.monitoring_active = False
        self.monitor_thread = None
        self.cleanup_callbacks: List[Callable] = []
        
        # Weak references for automatic cleanup
        self.tracked_objects: List[weakref.ref] = []
        
        logger.info("✅ Memory Management System initialized")
        logger.info(f"   Memory limit: {self.config.memory_limit_mb}MB")
        logger.info(f"   GC threshold: {self.config.gc_threshold * 100}%")
        logger.info(f"   Cleanup interval: {self.config.cleanup_interval}s")
    
    def start_monitoring(self):
        """Start memory monitoring in background thread."""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_memory, daemon=True)
        self.monitor_thread.start()
        logger.info("✅ Memory monitoring started")
    
    def stop_monitoring(self):
        """Stop memory monitoring."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("✅ Memory monitoring stopped")
    
    def _monitor_memory(self):
        """Background memory monitoring thread."""
        while self.monitoring_active:
            try:
                self.update_memory_stats()
                
                # Check if cleanup is needed
                if self.should_perform_cleanup():
                    self.perform_cleanup()
                
                # Sleep for monitoring interval
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in memory monitoring: {e}")
                time.sleep(30)  # Wait longer on error
    
    def update_memory_stats(self):
        """Update current memory statistics."""
        try:
            memory_info = self.process.memory_info()
            current_mb = memory_info.rss / 1024 / 1024
            
            # Update stats
            self.memory_stats.current_mb = current_mb
            self.memory_stats.peak_mb = max(self.memory_stats.peak_mb, current_mb)
            
            # Calculate usage percentage
            self.memory_stats.usage_percent = (current_mb / self.config.memory_limit_mb) * 100
            
            # Get available system memory
            system_memory = psutil.virtual_memory()
            self.memory_stats.available_mb = system_memory.available / 1024 / 1024
            
            # Log warnings if memory usage is high
            if self.memory_stats.usage_percent > self.config.memory_warning_threshold * 100:
                logger.warning(f"⚠️ High memory usage: {current_mb:.1f}MB ({self.memory_stats.usage_percent:.1f}%)")
            
        except Exception as e:
            logger.error(f"Error updating memory stats: {e}")
    
    def should_perform_cleanup(self) -> bool:
        """Check if memory cleanup should be performed."""
        # Check memory usage threshold
        if self.memory_stats.usage_percent > self.config.gc_threshold * 100:
            return True
        
        # Check time-based cleanup
        if time.time() - self.memory_stats.last_cleanup > self.config.cleanup_interval:
            return True
        
        return False
    
    def perform_cleanup(self):
        """Perform comprehensive memory cleanup."""
        start_time = time.time()
        initial_memory = self.memory_stats.current_mb
        
        try:
            logger.info("🧹 Starting memory cleanup")
            
            # Run garbage collection
            self._run_garbage_collection()
            
            # Clean up tracked objects
            self._cleanup_tracked_objects()
            
            # Run custom cleanup callbacks
            self._run_cleanup_callbacks()
            
            # Update stats
            self.update_memory_stats()
            self.memory_stats.cleanup_count += 1
            self.memory_stats.last_cleanup = time.time()
            
            # Calculate cleanup results
            memory_freed = initial_memory - self.memory_stats.current_mb
            cleanup_time = time.time() - start_time
            
            logger.info(f"✅ Memory cleanup completed")
            logger.info(f"   Memory freed: {memory_freed:.1f}MB")
            logger.info(f"   Cleanup time: {cleanup_time:.2f}s")
            logger.info(f"   Current usage: {self.memory_stats.current_mb:.1f}MB ({self.memory_stats.usage_percent:.1f}%)")
            
        except Exception as e:
            logger.error(f"Error during memory cleanup: {e}")
    
    def _run_garbage_collection(self):
        """Run garbage collection with optimization."""
        try:
            # Count objects before GC
            objects_before = len(gc.get_objects())
            
            # Run garbage collection
            collected = gc.collect()
            self.memory_stats.gc_count += 1
            
            # Count objects after GC
            objects_after = len(gc.get_objects())
            objects_freed = objects_before - objects_after
            
            logger.info(f"   GC collected {collected} objects, freed {objects_freed} references")
            
            # Run additional GC if aggressive cleanup is enabled
            if self.config.aggressive_cleanup:
                gc.collect()
                
        except Exception as e:
            logger.error(f"Error during garbage collection: {e}")
    
    def _cleanup_tracked_objects(self):
        """Clean up tracked objects that are no longer referenced."""
        try:
            # Remove dead weak references
            self.tracked_objects = [ref for ref in self.tracked_objects if ref() is not None]
            
            logger.info(f"   Cleaned up tracked objects, {len(self.tracked_objects)} remaining")
            
        except Exception as e:
            logger.error(f"Error cleaning up tracked objects: {e}")
    
    def _run_cleanup_callbacks(self):
        """Run registered cleanup callbacks."""
        try:
            for callback in self.cleanup_callbacks:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Error in cleanup callback: {e}")
            
            logger.info(f"   Ran {len(self.cleanup_callbacks)} cleanup callbacks")
            
        except Exception as e:
            logger.error(f"Error running cleanup callbacks: {e}")
    
    def track_object(self, obj: Any, name: str = "unnamed"):
        """Track an object for automatic cleanup."""
        try:
            ref = weakref.ref(obj, lambda r: self._object_cleanup_callback(r, name))
            self.tracked_objects.append(ref)
            logger.debug(f"Tracking object: {name}")
        except Exception as e:
            logger.error(f"Error tracking object {name}: {e}")
    
    def _object_cleanup_callback(self, ref, name: str):
        """Callback when tracked object is garbage collected."""
        logger.debug(f"Object cleaned up: {name}")
    
    def register_cleanup_callback(self, callback: Callable):
        """Register a cleanup callback function."""
        self.cleanup_callbacks.append(callback)
        logger.info(f"Registered cleanup callback: {callback.__name__}")
    
    def unregister_cleanup_callback(self, callback: Callable):
        """Unregister a cleanup callback function."""
        if callback in self.cleanup_callbacks:
            self.cleanup_callbacks.remove(callback)
            logger.info(f"Unregistered cleanup callback: {callback.__name__}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics."""
        self.update_memory_stats()
        
        return {
            "current_mb": self.memory_stats.current_mb,
            "peak_mb": self.memory_stats.peak_mb,
            "available_mb": self.memory_stats.available_mb,
            "usage_percent": self.memory_stats.usage_percent,
            "gc_count": self.memory_stats.gc_count,
            "cleanup_count": self.memory_stats.cleanup_count,
            "last_cleanup": self.memory_stats.last_cleanup,
            "tracked_objects": len(self.tracked_objects),
            "cleanup_callbacks": len(self.cleanup_callbacks),
            "memory_limit_mb": self.config.memory_limit_mb,
            "gc_threshold_percent": self.config.gc_threshold * 100,
            "warning_threshold_percent": self.config.memory_warning_threshold * 100
        }
    
    def check_memory_health(self) -> Dict[str, Any]:
        """Check memory system health and provide recommendations."""
        stats = self.get_memory_stats()
        
        health_status = "healthy"
        recommendations = []
        
        # Check memory usage
        if stats["usage_percent"] > 90:
            health_status = "critical"
            recommendations.append("Immediate memory cleanup required")
        elif stats["usage_percent"] > 80:
            health_status = "warning"
            recommendations.append("Memory usage is high, consider cleanup")
        elif stats["usage_percent"] > 70:
            health_status = "attention"
            recommendations.append("Monitor memory usage closely")
        
        # Check cleanup frequency
        time_since_cleanup = time.time() - stats["last_cleanup"]
        if time_since_cleanup > self.config.cleanup_interval * 2:
            recommendations.append("Consider more frequent cleanup")
        
        # Check tracked objects
        if stats["tracked_objects"] > 1000:
            recommendations.append("High number of tracked objects, review tracking strategy")
        
        return {
            "status": health_status,
            "recommendations": recommendations,
            "stats": stats
        }
    
    def optimize_memory_usage(self, data: Any) -> Any:
        """Optimize memory usage for large data structures."""
        try:
            if isinstance(data, dict):
                return self._optimize_dict_memory(data)
            elif isinstance(data, list):
                return self._optimize_list_memory(data)
            else:
                return data
        except Exception as e:
            logger.error(f"Error optimizing memory usage: {e}")
            return data
    
    def _optimize_dict_memory(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize dictionary memory usage."""
        optimized = {}
        
        for key, value in data.items():
            # Use more memory-efficient data types
            if isinstance(value, list) and len(value) > 1000:
                # Convert large lists to more efficient types
                if all(isinstance(item, (int, float)) for item in value):
                    try:
                        import numpy as np
                        optimized[key] = np.array(value)
                    except ImportError:
                        optimized[key] = value
                else:
                    optimized[key] = value
            elif isinstance(value, dict):
                # Recursively optimize nested dictionaries
                optimized[key] = self._optimize_dict_memory(value)
            else:
                optimized[key] = value
        
        return optimized
    
    def _optimize_list_memory(self, data: List[Any]) -> List[Any]:
        """Optimize list memory usage."""
        if not data:
            return data
        
        # Check if all items are numeric
        if all(isinstance(item, (int, float)) for item in data):
            try:
                import numpy as np
                return np.array(data).tolist()
            except ImportError:
                return data
        
        # Check if all items are strings
        if all(isinstance(item, str) for item in data):
            # Remove empty strings and strip whitespace
            return [item.strip() for item in data if item.strip()]
        
        return data
    
    def force_cleanup(self):
        """Force immediate memory cleanup."""
        logger.info("🔄 Forcing immediate memory cleanup")
        self.perform_cleanup()
    
    def reset_stats(self):
        """Reset memory statistics."""
        self.memory_stats = MemoryStats(
            current_mb=0.0,
            peak_mb=0.0,
            available_mb=0.0,
            usage_percent=0.0,
            gc_count=0,
            cleanup_count=0,
            last_cleanup=time.time()
        )
        logger.info("✅ Memory statistics reset")
    
    def __del__(self):
        """Cleanup on destruction."""
        self.stop_monitoring()


# Global instance for easy access
memory_manager = MemoryManagementSystem()
