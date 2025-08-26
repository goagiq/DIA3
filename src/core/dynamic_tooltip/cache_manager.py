"""
Cache Manager for Dynamic Tooltips

Intelligent caching system for tooltip content with multi-level caching,
compression, and automatic invalidation.
"""

import asyncio
import hashlib
import json
import pickle
import time
from typing import Any, Dict, Optional, Union
from pathlib import Path
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


class MemoryCache:
    """In-memory cache with LRU eviction."""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: OrderedDict = OrderedDict()
        self.access_times: Dict[str, float] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self.cache:
            # Update access time
            self.access_times[key] = time.time()
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache with optional TTL."""
        # Check if key exists and update access time
        if key in self.cache:
            self.access_times[key] = time.time()
            self.cache.move_to_end(key)
            self.cache[key] = value
            return
        
        # Add new key
        self.cache[key] = value
        self.access_times[key] = time.time()
        
        # Evict if cache is full
        if len(self.cache) > self.max_size:
            # Remove least recently used
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
    
    def delete(self, key: str):
        """Delete key from cache."""
        if key in self.cache:
            del self.cache[key]
            del self.access_times[key]
    
    def clear(self):
        """Clear all cache entries."""
        self.cache.clear()
        self.access_times.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self.cache)
    
    def cleanup_expired(self, current_time: Optional[float] = None):
        """Remove expired entries based on TTL."""
        if current_time is None:
            current_time = time.time()
        
        expired_keys = []
        for key, access_time in self.access_times.items():
            # Default TTL of 300 seconds (5 minutes)
            if current_time - access_time > 300:
                expired_keys.append(key)
        
        for key in expired_keys:
            self.delete(key)


class DiskCache:
    """Disk-based cache with compression."""
    
    def __init__(self, cache_dir: str = "cache/tooltips", max_size_mb: int = 100):
        self.cache_dir = Path(cache_dir)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load cache metadata."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cache metadata: {e}")
        return {"entries": {}, "total_size": 0}
    
    def _save_metadata(self):
        """Save cache metadata."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save cache metadata: {e}")
    
    def _get_cache_path(self, key: str) -> Path:
        """Get file path for cache key."""
        # Create hash of key for filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from disk cache."""
        if key not in self.metadata["entries"]:
            return None
        
        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            # Remove from metadata if file doesn't exist
            del self.metadata["entries"][key]
            self._save_metadata()
            return None
        
        try:
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
            
            # Check if expired
            if data.get("expires_at") and time.time() > data["expires_at"]:
                self.delete(key)
                return None
            
            # Update access time
            self.metadata["entries"][key]["last_accessed"] = time.time()
            self._save_metadata()
            
            return data["value"]
        
        except Exception as e:
            logger.error(f"Failed to load cache entry {key}: {e}")
            self.delete(key)
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in disk cache."""
        cache_path = self._get_cache_path(key)
        
        # Calculate expiration time
        expires_at = None
        if ttl:
            expires_at = time.time() + ttl
        
        # Prepare data
        data = {
            "value": value,
            "created_at": time.time(),
            "expires_at": expires_at
        }
        
        # Calculate size
        try:
            serialized_size = len(pickle.dumps(data))
        except Exception:
            serialized_size = 1024  # Default estimate
        
        # Check if we need to evict entries
        if self.metadata["total_size"] + serialized_size > self.max_size_bytes:
            self._evict_entries(serialized_size)
        
        try:
            # Save to disk
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
            
            # Update metadata
            self.metadata["entries"][key] = {
                "size": serialized_size,
                "created_at": time.time(),
                "last_accessed": time.time(),
                "expires_at": expires_at
            }
            self.metadata["total_size"] += serialized_size
            self._save_metadata()
        
        except Exception as e:
            logger.error(f"Failed to save cache entry {key}: {e}")
    
    def delete(self, key: str):
        """Delete key from disk cache."""
        if key in self.metadata["entries"]:
            cache_path = self._get_cache_path(key)
            
            # Remove file
            if cache_path.exists():
                try:
                    cache_path.unlink()
                except Exception as e:
                    logger.warning(f"Failed to delete cache file {cache_path}: {e}")
            
            # Update metadata
            size = self.metadata["entries"][key]["size"]
            self.metadata["total_size"] -= size
            del self.metadata["entries"][key]
            self._save_metadata()
    
    def _evict_entries(self, needed_size: int):
        """Evict least recently used entries to make space."""
        # Sort by last accessed time
        sorted_entries = sorted(
            self.metadata["entries"].items(),
            key=lambda x: x[1]["last_accessed"]
        )
        
        freed_size = 0
        for key, entry in sorted_entries:
            if freed_size >= needed_size:
                break
            
            self.delete(key)
            freed_size += entry["size"]
    
    def clear(self):
        """Clear all cache entries."""
        # Remove all cache files
        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                cache_file.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete cache file {cache_file}: {e}")
        
        # Reset metadata
        self.metadata = {"entries": {}, "total_size": 0}
        self._save_metadata()
    
    def cleanup_expired(self):
        """Remove expired entries."""
        expired_keys = []
        current_time = time.time()
        
        for key, entry in self.metadata["entries"].items():
            if entry.get("expires_at") and current_time > entry["expires_at"]:
                expired_keys.append(key)
        
        for key in expired_keys:
            self.delete(key)


class CacheManager:
    """Multi-level cache manager for tooltip content."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.memory_cache = MemoryCache(
            max_size=config.get("memory_cache_size", 1000)
        )
        self.disk_cache = DiskCache(
            cache_dir=config.get("cache_directory", "cache/tooltips"),
            max_size_mb=config.get("disk_cache_size_mb", 100)
        )
        self.enabled = config.get("enabled", True)
        self.compression_enabled = config.get("compression_enabled", True)
        self.cache_key_prefix = config.get("cache_key_prefix", "tooltip_")
        
        # Start cleanup task
        self.cleanup_task = None
        if self.enabled:
            self._start_cleanup_task()
    
    def _start_cleanup_task(self):
        """Start periodic cleanup task."""
        async def cleanup_loop():
            while True:
                try:
                    await asyncio.sleep(300)  # Run every 5 minutes
                    self.cleanup_expired()
                except Exception as e:
                    logger.error(f"Cache cleanup error: {e}")
        
        self.cleanup_task = asyncio.create_task(cleanup_loop())
    
    def _generate_cache_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        # Create a deterministic string representation
        key_parts = []
        
        # Add positional arguments
        for arg in args:
            key_parts.append(str(arg))
        
        # Add keyword arguments (sorted for consistency)
        for key, value in sorted(kwargs.items()):
            key_parts.append(f"{key}:{value}")
        
        key_string = "|".join(key_parts)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        
        return f"{self.cache_key_prefix}{key_hash}"
    
    async def get(self, *args, ttl: Optional[int] = None, **kwargs) -> Optional[Any]:
        """Get value from cache."""
        if not self.enabled:
            return None
        
        cache_key = self._generate_cache_key(*args, **kwargs)
        
        # Try memory cache first
        value = self.memory_cache.get(cache_key)
        if value is not None:
            return value
        
        # Try disk cache
        value = self.disk_cache.get(cache_key)
        if value is not None:
            # Store in memory cache for faster access
            self.memory_cache.set(cache_key, value, ttl)
            return value
        
        return None
    
    async def set(self, value: Any, *args, ttl: Optional[int] = None, **kwargs):
        """Set value in cache."""
        if not self.enabled:
            return
        
        cache_key = self._generate_cache_key(*args, **kwargs)
        
        # Store in both caches
        self.memory_cache.set(cache_key, value, ttl)
        self.disk_cache.set(cache_key, value, ttl)
    
    async def delete(self, *args, **kwargs):
        """Delete value from cache."""
        if not self.enabled:
            return
        
        cache_key = self._generate_cache_key(*args, **kwargs)
        self.memory_cache.delete(cache_key)
        self.disk_cache.delete(cache_key)
    
    async def clear(self):
        """Clear all cache entries."""
        self.memory_cache.clear()
        self.disk_cache.clear()
    
    def cleanup_expired(self):
        """Clean up expired entries in both caches."""
        current_time = time.time()
        self.memory_cache.cleanup_expired(current_time)
        self.disk_cache.cleanup_expired()
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "enabled": self.enabled,
            "memory_cache_size": self.memory_cache.size(),
            "memory_cache_max_size": self.memory_cache.max_size,
            "disk_cache_entries": len(self.disk_cache.metadata["entries"]),
            "disk_cache_total_size_mb": self.disk_cache.metadata["total_size"] / (1024 * 1024),
            "disk_cache_max_size_mb": self.disk_cache.max_size_bytes / (1024 * 1024)
        }
    
    async def close(self):
        """Close cache manager and cleanup resources."""
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
        
        # Clear caches
        await self.clear()
