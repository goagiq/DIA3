"""
Redis Configuration for DIA3

Redis configuration for caching and performance optimization.
Part of Phase 3.5: Performance Optimization with Redis Integration

Features:
- Redis connection management
- Caching configuration
- Performance monitoring
- Connection pooling
"""

import os
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
import redis
from redis import Redis
from redis.connection import ConnectionPool

logger = logging.getLogger(__name__)


@dataclass
class RedisConfig:
    """Redis configuration settings."""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    decode_responses: bool = True
    socket_connect_timeout: int = 5
    socket_timeout: int = 5
    retry_on_timeout: bool = True
    health_check_interval: int = 30
    max_connections: int = 20
    cache_ttl: int = 3600  # 1 hour default
    compression_enabled: bool = True
    enable_monitoring: bool = True


class RedisManager:
    """Redis connection and cache management."""
    
    def __init__(self, config: Optional[RedisConfig] = None):
        """Initialize Redis manager."""
        self.config = config or self._load_config_from_env()
        self.redis_client: Optional[Redis] = None
        self.connection_pool: Optional[ConnectionPool] = None
        self.is_connected = False
        
        # Performance monitoring
        self.stats = {
            "cache_hits": 0,
            "cache_misses": 0,
            "cache_sets": 0,
            "cache_deletes": 0,
            "connection_errors": 0,
            "total_operations": 0
        }
        
        self._initialize_connection()
    
    def _load_config_from_env(self) -> RedisConfig:
        """Load Redis configuration from environment variables."""
        return RedisConfig(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            db=int(os.getenv("REDIS_DB", "0")),
            password=os.getenv("REDIS_PASSWORD"),
            cache_ttl=int(os.getenv("REDIS_CACHE_TTL", "3600")),
            compression_enabled=os.getenv("REDIS_COMPRESSION", "true").lower() == "true",
            enable_monitoring=os.getenv("REDIS_MONITORING", "true").lower() == "true"
        )
    
    def _initialize_connection(self):
        """Initialize Redis connection."""
        try:
            # Create connection pool
            self.connection_pool = ConnectionPool(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=self.config.decode_responses,
                socket_connect_timeout=self.config.socket_connect_timeout,
                socket_timeout=self.config.socket_timeout,
                retry_on_timeout=self.config.retry_on_timeout,
                health_check_interval=self.config.health_check_interval,
                max_connections=self.config.max_connections
            )
            
            # Create Redis client
            self.redis_client = Redis(connection_pool=self.connection_pool)
            
            # Test connection
            self.redis_client.ping()
            self.is_connected = True
            
            logger.info("✅ Redis connection established successfully")
            logger.info(f"   Host: {self.config.host}:{self.config.port}")
            logger.info(f"   Database: {self.config.db}")
            logger.info(f"   Cache TTL: {self.config.cache_ttl}s")
            logger.info(f"   Compression: {self.config.compression_enabled}")
            
        except Exception as e:
            logger.warning(f"⚠️ Redis connection failed: {e}")
            logger.info("   Falling back to in-memory caching")
            self.is_connected = False
    
    def get_client(self) -> Optional[Redis]:
        """Get Redis client if connected."""
        if self.is_connected and self.redis_client:
            return self.redis_client
        return None
    
    def is_available(self) -> bool:
        """Check if Redis is available."""
        if not self.is_connected or not self.redis_client:
            return False
        
        try:
            self.redis_client.ping()
            return True
        except Exception:
            self.is_connected = False
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache."""
        if not self.is_available():
            return None
        
        try:
            self.stats["total_operations"] += 1
            value = self.redis_client.get(key)
            
            if value is not None:
                self.stats["cache_hits"] += 1
                return value
            else:
                self.stats["cache_misses"] += 1
                return None
                
        except Exception as e:
            logger.warning(f"Redis get error for key {key}: {e}")
            self.stats["connection_errors"] += 1
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in Redis cache."""
        if not self.is_available():
            return False
        
        try:
            self.stats["total_operations"] += 1
            self.stats["cache_sets"] += 1
            
            ttl = ttl or self.config.cache_ttl
            return self.redis_client.setex(key, ttl, value)
            
        except Exception as e:
            logger.warning(f"Redis set error for key {key}: {e}")
            self.stats["connection_errors"] += 1
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from Redis cache."""
        if not self.is_available():
            return False
        
        try:
            self.stats["total_operations"] += 1
            self.stats["cache_deletes"] += 1
            
            return bool(self.redis_client.delete(key))
            
        except Exception as e:
            logger.warning(f"Redis delete error for key {key}: {e}")
            self.stats["connection_errors"] += 1
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis."""
        if not self.is_available():
            return False
        
        try:
            return bool(self.redis_client.exists(key))
        except Exception:
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get Redis performance statistics."""
        return {
            **self.stats,
            "is_connected": self.is_connected,
            "config": {
                "host": self.config.host,
                "port": self.config.port,
                "db": self.config.db,
                "cache_ttl": self.config.cache_ttl
            }
        }
    
    def close(self):
        """Close Redis connection."""
        if self.redis_client:
            self.redis_client.close()
        if self.connection_pool:
            self.connection_pool.disconnect()
        self.is_connected = False
        logger.info("Redis connection closed")


# Global Redis manager instance
redis_manager = RedisManager()


def get_redis_manager() -> RedisManager:
    """Get the global Redis manager instance."""
    return redis_manager
