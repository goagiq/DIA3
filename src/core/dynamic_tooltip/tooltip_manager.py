"""
Dynamic Tooltip Manager

Main orchestrator for the dynamic tooltip system that coordinates data sources,
content generation, caching, and rendering for comprehensive tooltip content.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

from .configuration import TooltipConfiguration
from .data_source_registry import DataSourceRegistry
from .content_generator import ContentGenerator
from .tooltip_renderer import TooltipRenderer
from .cache_manager import CacheManager

logger = logging.getLogger(__name__)


@dataclass
class TooltipRequest:
    """Request for tooltip content."""
    object_id: str
    object_type: str
    context: Dict[str, Any]
    template_name: Optional[str] = None
    data_sources: Optional[List[str]] = None
    cache_ttl: Optional[int] = None


@dataclass
class TooltipResponse:
    """Response with tooltip content."""
    success: bool
    content: Optional[str] = None
    html_content: Optional[str] = None
    error: Optional[str] = None
    data_sources_used: List[str] = []
    response_time: float = 0.0
    cached: bool = False
    metadata: Dict[str, Any] = None


class DynamicTooltipManager:
    """Main manager for dynamic tooltip system."""
    
    def __init__(self, config: Optional[TooltipConfiguration] = None):
        self.config = config or TooltipConfiguration()
        self.cache_manager = CacheManager(self.config.cache.__dict__)
        self.data_source_registry = DataSourceRegistry({
            "health_check_interval": 60
        })
        self.content_generator = ContentGenerator(self.config)
        self.tooltip_renderer = TooltipRenderer(self.config.style.__dict__)
        
        # Initialize data sources
        self._initialize_data_sources()
        
        # Performance tracking
        self.request_count = 0
        self.cache_hit_count = 0
        self.average_response_time = 0.0
        
        logger.info("DynamicTooltipManager initialized successfully")
    
    def _initialize_data_sources(self):
        """Initialize default data sources."""
        from .data_source_registry import (
            knowledge_graph_query,
            semantic_search_query,
            business_intelligence_query,
            external_api_query
        )
        
        # Register data sources
        for name, config in self.config.data_sources.items():
            if config.enabled:
                query_functions = {
                    "knowledge_graph": knowledge_graph_query,
                    "semantic_search": semantic_search_query,
                    "business_intelligence": business_intelligence_query,
                    "external_api": external_api_query
                }
                
                if name in query_functions:
                    self.data_source_registry.register_data_source(
                        name,
                        config.__dict__,
                        query_functions[name]
                    )
        
        logger.info(f"Initialized {len(self.config.data_sources)} data sources")
    
    async def get_tooltip_content(self, request: TooltipRequest) -> TooltipResponse:
        """Get tooltip content for an object."""
        start_time = asyncio.get_event_loop().time()
        self.request_count += 1
        
        try:
            # Check cache first
            cached_content = await self.cache_manager.get(
                request.object_id,
                request.object_type,
                **request.context
            )
            
            if cached_content:
                self.cache_hit_count += 1
                return TooltipResponse(
                    success=True,
                    content=cached_content,
                    html_content=self.tooltip_renderer.render_html(cached_content),
                    cached=True,
                    response_time=asyncio.get_event_loop().time() - start_time
                )
            
            # Generate content from data sources
            content_data = await self._gather_content_data(request)
            
            if not content_data:
                return TooltipResponse(
                    success=False,
                    error="No data available from any source",
                    response_time=asyncio.get_event_loop().time() - start_time
                )
            
            # Generate content using template
            content = await self.content_generator.generate_content(
                request.object_id,
                request.object_type,
                content_data,
                template_name=request.template_name
            )
            
            if not content:
                return TooltipResponse(
                    success=False,
                    error="Failed to generate content",
                    response_time=asyncio.get_event_loop().time() - start_time
                )
            
            # Cache the result
            await self.cache_manager.set(
                content,
                request.object_id,
                request.object_type,
                ttl=request.cache_ttl or self.config.cache.cache_ttl_default,
                **request.context
            )
            
            # Render HTML
            html_content = self.tooltip_renderer.render_html(content)
            
            response_time = asyncio.get_event_loop().time() - start_time
            self._update_performance_metrics(response_time)
            
            return TooltipResponse(
                success=True,
                content=content,
                html_content=html_content,
                data_sources_used=list(content_data.keys()),
                response_time=response_time,
                metadata={"content_data": content_data}
            )
        
        except Exception as e:
            logger.error(f"Error generating tooltip content: {e}")
            return TooltipResponse(
                success=False,
                error=str(e),
                response_time=asyncio.get_event_loop().time() - start_time
            )
    
    async def _gather_content_data(self, request: TooltipRequest) -> Dict[str, Any]:
        """Gather data from multiple sources."""
        content_data = {}
        
        # Determine which data sources to query
        data_sources = request.data_sources or list(self.config.data_sources.keys())
        
        # Query data sources with fallback strategy
        for source_name in data_sources:
            if source_name in self.config.data_sources:
                source_config = self.config.data_sources[source_name]
                if not source_config.enabled:
                    continue
                
                try:
                    # Query the data source
                    result = await self.data_source_registry.get_data_source(source_name).query(
                        request.object_id,
                        **request.context
                    )
                    
                    if result.success and result.data:
                        content_data[source_name] = result.data
                        logger.debug(f"Retrieved data from {source_name}")
                    
                except Exception as e:
                    logger.warning(f"Failed to query data source {source_name}: {e}")
        
        return content_data
    
    def _update_performance_metrics(self, response_time: float):
        """Update performance tracking metrics."""
        # Update average response time
        if self.request_count > 0:
            self.average_response_time = (
                (self.average_response_time * (self.request_count - 1) + response_time) 
                / self.request_count
            )
    
    async def get_tooltip_html(self, object_id: str, object_type: str, 
                              context: Optional[Dict[str, Any]] = None,
                              template_name: Optional[str] = None) -> str:
        """Convenience method to get HTML tooltip content."""
        request = TooltipRequest(
            object_id=object_id,
            object_type=object_type,
            context=context or {},
            template_name=template_name
        )
        
        response = await self.get_tooltip_content(request)
        
        if response.success and response.html_content:
            return response.html_content
        else:
            # Return fallback HTML
            return self.tooltip_renderer.render_fallback_html(
                object_id, 
                object_type, 
                response.error
            )
    
    async def preload_tooltips(self, objects: List[Dict[str, Any]]):
        """Preload tooltip content for multiple objects."""
        tasks = []
        
        for obj in objects:
            request = TooltipRequest(
                object_id=obj.get("id", ""),
                object_type=obj.get("type", "unknown"),
                context=obj.get("context", {}),
                template_name=obj.get("template_name")
            )
            tasks.append(self.get_tooltip_content(request))
        
        # Execute all requests concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Log results
        successful = sum(1 for r in results if isinstance(r, TooltipResponse) and r.success)
        logger.info(f"Preloaded {successful}/{len(objects)} tooltips")
        
        return results
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and health information."""
        return {
            "enabled": self.config.enabled,
            "data_sources": {
                name: {
                    "enabled": config.enabled,
                    "priority": config.priority,
                    "health": self.data_source_registry.get_data_source(name).get_health().__dict__ if name in self.data_source_registry.data_sources else None
                }
                for name, config in self.config.data_sources.items()
            },
            "cache_stats": asyncio.create_task(self.cache_manager.get_cache_stats()),
            "performance": {
                "request_count": self.request_count,
                "cache_hit_rate": self.cache_hit_count / max(self.request_count, 1),
                "average_response_time": self.average_response_time
            },
            "templates": list(self.config.content_templates.keys())
        }
    
    async def update_configuration(self, new_config: TooltipConfiguration):
        """Update system configuration."""
        self.config = new_config
        
        # Reinitialize components with new config
        self.cache_manager = CacheManager(self.config.cache.__dict__)
        self.content_generator = ContentGenerator(self.config)
        self.tooltip_renderer = TooltipRenderer(self.config.style.__dict__)
        
        # Update data sources
        self._initialize_data_sources()
        
        logger.info("Configuration updated successfully")
    
    async def enable_data_source(self, source_name: str):
        """Enable a specific data source."""
        if source_name in self.config.data_sources:
            self.config.enable_data_source(source_name)
            self.data_source_registry.enable_data_source(source_name)
            logger.info(f"Enabled data source: {source_name}")
    
    async def disable_data_source(self, source_name: str):
        """Disable a specific data source."""
        if source_name in self.config.data_sources:
            self.config.disable_data_source(source_name)
            self.data_source_registry.disable_data_source(source_name)
            logger.info(f"Disabled data source: {source_name}")
    
    async def clear_cache(self):
        """Clear all cached tooltip content."""
        await self.cache_manager.clear()
        logger.info("Tooltip cache cleared")
    
    async def close(self):
        """Close the tooltip manager and cleanup resources."""
        await self.cache_manager.close()
        await self.data_source_registry.close()
        logger.info("DynamicTooltipManager closed")


# Global instance for easy access
_tooltip_manager: Optional[DynamicTooltipManager] = None


def get_tooltip_manager(config: Optional[TooltipConfiguration] = None) -> DynamicTooltipManager:
    """Get or create the global tooltip manager instance."""
    global _tooltip_manager
    
    if _tooltip_manager is None:
        _tooltip_manager = DynamicTooltipManager(config)
    
    return _tooltip_manager


async def initialize_tooltip_manager(config: Optional[TooltipConfiguration] = None) -> DynamicTooltipManager:
    """Initialize the global tooltip manager."""
    global _tooltip_manager
    
    if _tooltip_manager is not None:
        await _tooltip_manager.close()
    
    _tooltip_manager = DynamicTooltipManager(config)
    return _tooltip_manager


async def close_tooltip_manager():
    """Close the global tooltip manager."""
    global _tooltip_manager
    
    if _tooltip_manager is not None:
        await _tooltip_manager.close()
        _tooltip_manager = None
