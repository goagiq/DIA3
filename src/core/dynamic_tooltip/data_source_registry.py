"""
Data Source Registry for Dynamic Tooltips

Manages multiple data sources with health checks, fallbacks, and priority-based
data retrieval for comprehensive tooltip content.
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class DataSourceStatus(Enum):
    """Data source status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    DISABLED = "disabled"


@dataclass
class DataSourceHealth:
    """Health information for a data source."""
    status: DataSourceStatus
    last_check: float
    response_time: float
    error_count: int = 0
    success_count: int = 0
    last_error: Optional[str] = None
    uptime_percentage: float = 100.0


@dataclass
class DataSourceResult:
    """Result from a data source query."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    source_name: str = ""
    response_time: float = 0.0
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


class DataSource:
    """Base class for data sources."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.enabled = config.get("enabled", True)
        self.priority = config.get("priority", 5)
        self.timeout = config.get("timeout", 30)
        self.retry_attempts = config.get("retry_attempts", 3)
        self.retry_delay = config.get("retry_delay", 1.0)
        self.health = DataSourceHealth(
            status=DataSourceStatus.DISABLED if not self.enabled else DataSourceStatus.HEALTHY,
            last_check=time.time(),
            response_time=0.0
        )
        self._query_function: Optional[Callable] = None
    
    def set_query_function(self, func: Callable):
        """Set the query function for this data source."""
        self._query_function = func
    
    async def query(self, *args, **kwargs) -> DataSourceResult:
        """Query the data source."""
        if not self.enabled or not self._query_function:
            return DataSourceResult(
                success=False,
                error="Data source disabled or no query function set",
                source_name=self.name
            )
        
        start_time = time.time()
        error_count = 0
        
        for attempt in range(self.retry_attempts):
            try:
                # Execute query with timeout
                result = await asyncio.wait_for(
                    self._query_function(*args, **kwargs),
                    timeout=self.timeout
                )
                
                response_time = time.time() - start_time
                
                # Update health metrics
                self.health.success_count += 1
                self.health.response_time = response_time
                self.health.last_check = time.time()
                self.health.status = DataSourceStatus.HEALTHY
                self.health.error_count = 0
                self.health.last_error = None
                
                return DataSourceResult(
                    success=True,
                    data=result,
                    source_name=self.name,
                    response_time=response_time
                )
            
            except asyncio.TimeoutError:
                error_count += 1
                error_msg = f"Timeout after {self.timeout}s"
                logger.warning(f"Data source {self.name} timeout (attempt {attempt + 1})")
            
            except Exception as e:
                error_count += 1
                error_msg = str(e)
                logger.error(f"Data source {self.name} error: {e}")
            
            # Wait before retry
            if attempt < self.retry_attempts - 1:
                await asyncio.sleep(self.retry_delay)
        
        # All attempts failed
        response_time = time.time() - start_time
        self.health.error_count += 1
        self.health.last_check = time.time()
        self.health.last_error = error_msg
        
        # Update status based on error count
        if self.health.error_count >= 5:
            self.health.status = DataSourceStatus.UNHEALTHY
        elif self.health.error_count >= 2:
            self.health.status = DataSourceStatus.DEGRADED
        
        return DataSourceResult(
            success=False,
            error=error_msg,
            source_name=self.name,
            response_time=response_time
        )
    
    def get_health(self) -> DataSourceHealth:
        """Get current health status."""
        return self.health
    
    def enable(self):
        """Enable the data source."""
        self.enabled = True
        self.health.status = DataSourceStatus.HEALTHY
    
    def disable(self):
        """Disable the data source."""
        self.enabled = False
        self.health.status = DataSourceStatus.DISABLED


class DataSourceRegistry:
    """Registry for managing multiple data sources."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_sources: Dict[str, DataSource] = {}
        self.health_check_interval = config.get("health_check_interval", 60)
        self.health_check_task: Optional[asyncio.Task] = None
        self._start_health_checks()
    
    def _start_health_checks(self):
        """Start periodic health checks."""
        async def health_check_loop():
            while True:
                try:
                    await asyncio.sleep(self.health_check_interval)
                    await self._perform_health_checks()
                except Exception as e:
                    logger.error(f"Health check error: {e}")
        
        self.health_check_task = asyncio.create_task(health_check_loop())
    
    async def _perform_health_checks(self):
        """Perform health checks on all data sources."""
        for source in self.data_sources.values():
            if source.enabled:
                # Perform a simple health check query
                await source.query("health_check")
    
    def register_data_source(self, name: str, config: Dict[str, Any], query_func: Callable):
        """Register a new data source."""
        data_source = DataSource(name, config)
        data_source.set_query_function(query_func)
        self.data_sources[name] = data_source
        logger.info(f"Registered data source: {name}")
    
    def unregister_data_source(self, name: str):
        """Unregister a data source."""
        if name in self.data_sources:
            del self.data_sources[name]
            logger.info(f"Unregistered data source: {name}")
    
    def get_data_source(self, name: str) -> Optional[DataSource]:
        """Get a data source by name."""
        return self.data_sources.get(name)
    
    def enable_data_source(self, name: str):
        """Enable a data source."""
        if name in self.data_sources:
            self.data_sources[name].enable()
            logger.info(f"Enabled data source: {name}")
    
    def disable_data_source(self, name: str):
        """Disable a data source."""
        if name in self.data_sources:
            self.data_sources[name].disable()
            logger.info(f"Disabled data source: {name}")
    
    async def query_all_sources(self, *args, **kwargs) -> List[DataSourceResult]:
        """Query all enabled data sources."""
        tasks = []
        for source in self.data_sources.values():
            if source.enabled:
                tasks.append(source.query(*args, **kwargs))
        
        if not tasks:
            return []
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and return valid results
        valid_results = []
        for result in results:
            if isinstance(result, DataSourceResult):
                valid_results.append(result)
            else:
                logger.error(f"Data source query failed with exception: {result}")
        
        return valid_results
    
    async def query_priority_sources(self, *args, min_priority: int = 1, **kwargs) -> List[DataSourceResult]:
        """Query data sources with priority >= min_priority."""
        # Sort sources by priority (highest first)
        sorted_sources = sorted(
            [s for s in self.data_sources.values() if s.enabled and s.priority >= min_priority],
            key=lambda s: s.priority,
            reverse=True
        )
        
        results = []
        for source in sorted_sources:
            result = await source.query(*args, **kwargs)
            results.append(result)
            
            # If we got a successful result from a high-priority source, we can stop
            if result.success and source.priority >= 8:
                break
        
        return results
    
    async def query_with_fallback(self, *args, **kwargs) -> Optional[Any]:
        """Query data sources with fallback strategy."""
        # Try high-priority sources first
        results = await self.query_priority_sources(*args, min_priority=7, **kwargs)
        
        # Look for successful results
        for result in results:
            if result.success and result.data:
                return result.data
        
        # If no high-priority results, try all sources
        all_results = await self.query_all_sources(*args, **kwargs)
        
        for result in all_results:
            if result.success and result.data:
                return result.data
        
        return None
    
    def get_health_status(self) -> Dict[str, DataSourceHealth]:
        """Get health status of all data sources."""
        return {
            name: source.get_health()
            for name, source in self.data_sources.items()
        }
    
    def get_enabled_sources(self) -> List[str]:
        """Get list of enabled data sources."""
        return [
            name for name, source in self.data_sources.items()
            if source.enabled
        ]
    
    def get_healthy_sources(self) -> List[str]:
        """Get list of healthy data sources."""
        return [
            name for name, source in self.data_sources.items()
            if source.enabled and source.health.status == DataSourceStatus.HEALTHY
        ]
    
    async def close(self):
        """Close the registry and cleanup resources."""
        if self.health_check_task:
            self.health_check_task.cancel()
            try:
                await self.health_check_task
            except asyncio.CancelledError:
                pass
        
        # Disable all data sources
        for source in self.data_sources.values():
            source.disable()


# Predefined data source query functions
async def knowledge_graph_query(entity_id: str, **kwargs) -> Dict[str, Any]:
    """Query knowledge graph for entity information."""
    # This would integrate with your existing knowledge graph system
    # For now, return mock data
    return {
        "entity_id": entity_id,
        "type": "entity",
        "name": entity_id,
        "confidence": 0.85,
        "relationships": [
            {"target": "related_entity", "type": "similar_to", "strength": 0.7}
        ],
        "description": f"Information about {entity_id}",
        "recommendations": [
            "Explore related entities",
            "Check historical data",
            "Analyze trends"
        ]
    }


async def semantic_search_query(query: str, **kwargs) -> Dict[str, Any]:
    """Query semantic search for contextual information."""
    # This would integrate with your existing semantic search system
    return {
        "query": query,
        "results": [
            {"text": f"Context about {query}", "relevance": 0.8},
            {"text": f"Additional information on {query}", "relevance": 0.6}
        ],
        "suggestions": [
            f"Search for {query} trends",
            f"Find {query} relationships"
        ]
    }


async def business_intelligence_query(entity_id: str, **kwargs) -> Dict[str, Any]:
    """Query business intelligence for analytics data."""
    # This would integrate with your existing BI system
    return {
        "entity_id": entity_id,
        "metrics": {
            "trend": "increasing",
            "growth_rate": 0.15,
            "market_share": 0.25
        },
        "insights": [
            "Strong performance in Q3",
            "Growing market presence",
            "Positive customer sentiment"
        ],
        "recommendations": [
            "Continue current strategy",
            "Monitor competition",
            "Expand market reach"
        ]
    }


async def external_api_query(entity_id: str, **kwargs) -> Dict[str, Any]:
    """Query external APIs for additional information."""
    # This would integrate with external APIs
    return {
        "entity_id": entity_id,
        "external_data": {
            "news_count": 15,
            "social_mentions": 234,
            "sentiment_score": 0.7
        },
        "recent_events": [
            "Recent partnership announcement",
            "Product launch",
            "Market expansion"
        ]
    }
