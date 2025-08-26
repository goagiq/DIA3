"""
MCP Tool Manager

This module manages the discovery and execution of all available MCP tools
with caching, health monitoring, and dynamic tool discovery.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from loguru import logger

from .unified_search_orchestrator import SourceType


class ToolHealth(Enum):
    """Tool health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class ToolMetrics:
    """Metrics for MCP tool performance."""
    success_count: int = 0
    failure_count: int = 0
    total_response_time: float = 0.0
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    health_status: ToolHealth = ToolHealth.UNKNOWN
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0
    
    @property
    def average_response_time(self) -> float:
        """Calculate average response time."""
        total = self.success_count + self.failure_count
        return self.total_response_time / total if total > 0 else 0.0


class MCPTool:
    """Base class for MCP tools."""
    
    def __init__(self, name: str, source_type: SourceType):
        self.name = name
        self.source_type = source_type
        self.metrics = ToolMetrics()
    
    async def execute(self, query: str) -> Any:
        """Execute the tool with the given query."""
        raise NotImplementedError("Subclasses must implement execute method")
    
    async def health_check(self) -> ToolHealth:
        """Perform health check on the tool."""
        try:
            # Simple health check - try a basic query
            await self.execute("health_check")
            return ToolHealth.HEALTHY
        except Exception as e:
            logger.warning(f"Health check failed for {self.name}: {e}")
            return ToolHealth.UNHEALTHY


class TACSystem(MCPTool):
    """TAC (Threat Analysis Center) system integration."""
    
    def __init__(self):
        super().__init__("TAC System", SourceType.TAC)
    
    async def execute(self, query: str) -> Any:
        """Execute TAC analysis on the query."""
        try:
            # Import TAC tools dynamically
            from mcp_TAC_analyze_natural_query import mcp_TAC_analyze_natural_query
            
            result = await mcp_TAC_analyze_natural_query(query=query)
            return result
        except Exception as e:
            logger.error(f"TAC system execution failed: {e}")
            raise


class DataGovSystem(MCPTool):
    """Data.gov system integration."""
    
    def __init__(self):
        super().__init__("DataGov System", SourceType.DATAGOV)
    
    async def execute(self, query: str) -> Any:
        """Execute Data.gov search on the query."""
        try:
            # Import DataGov tools dynamically
            from mcp_datagov_package_search import mcp_datagov_package_search
            
            result = await mcp_datagov_package_search(q=query)
            return result
        except Exception as e:
            logger.error(f"DataGov system execution failed: {e}")
            raise


class ForecastingEngine(MCPTool):
    """Forecasting engine integration."""
    
    def __init__(self):
        super().__init__("Forecasting Engine", SourceType.FORECASTING_ENGINE)
    
    async def execute(self, query: str) -> Any:
        """Execute forecasting analysis on the query."""
        try:
            # Import forecasting tools dynamically
            from mcp_DIA3_run_comprehensive_analysis import mcp_DIA3_run_comprehensive_analysis
            
            result = await mcp_DIA3_run_comprehensive_analysis(
                input_content=query,
                analysis_type="forecasting"
            )
            return result
        except Exception as e:
            logger.error(f"Forecasting engine execution failed: {e}")
            raise


class ToolCache:
    """Cache for discovered MCP tools."""
    
    def __init__(self, cache_duration: int = 300):  # 5 minutes default
        self.cache = {}
        self.cache_duration = cache_duration
        self.last_discovery = None
    
    def is_expired(self) -> bool:
        """Check if the cache is expired."""
        if self.last_discovery is None:
            return True
        return datetime.now() - self.last_discovery > timedelta(seconds=self.cache_duration)
    
    async def get_tools(self) -> List[MCPTool]:
        """Get cached tools if not expired."""
        if not self.is_expired() and 'tools' in self.cache:
            return self.cache['tools']
        return []
    
    async def set_tools(self, tools: List[MCPTool]) -> None:
        """Cache discovered tools."""
        self.cache['tools'] = tools
        self.last_discovery = datetime.now()
        logger.info(f"Cached {len(tools)} MCP tools")


class HealthMonitor:
    """Monitor health of MCP tools."""
    
    def __init__(self):
        self.health_history = {}
    
    async def record_success(self, tool: MCPTool, response_time: float = 0.0) -> None:
        """Record successful execution of a tool."""
        if tool.name not in self.health_history:
            self.health_history[tool.name] = ToolMetrics()
        
        metrics = self.health_history[tool.name]
        metrics.success_count += 1
        metrics.total_response_time += response_time
        metrics.last_success = datetime.now()
        metrics.health_status = ToolHealth.HEALTHY
        
        tool.metrics = metrics
    
    async def record_failure(self, tool: MCPTool, error: Exception) -> None:
        """Record failed execution of a tool."""
        if tool.name not in self.health_history:
            self.health_history[tool.name] = ToolMetrics()
        
        metrics = self.health_history[tool.name]
        metrics.failure_count += 1
        metrics.last_failure = datetime.now()
        
        # Update health status based on failure rate
        if metrics.success_rate < 0.5:
            metrics.health_status = ToolHealth.UNHEALTHY
        elif metrics.success_rate < 0.8:
            metrics.health_status = ToolHealth.DEGRADED
        else:
            metrics.health_status = ToolHealth.HEALTHY
        
        tool.metrics = metrics
    
    async def get_health_summary(self) -> Dict[str, ToolHealth]:
        """Get health summary for all tools."""
        return {
            tool_name: metrics.health_status
            for tool_name, metrics in self.health_history.items()
        }


class MCPToolManager:
    """
    Manager for MCP tools with discovery, caching, and health monitoring.
    """
    
    def __init__(self):
        self.tool_cache = ToolCache()
        self.health_monitor = HealthMonitor()
        self.available_tools = []
        logger.info("MCP Tool Manager initialized")
    
    async def discover_mcp_tools(self) -> List[MCPTool]:
        """Discover all available MCP tools."""
        # Check cache first
        cached_tools = await self.tool_cache.get_tools()
        if cached_tools and not self.tool_cache.is_expired():
            logger.info(f"Using cached MCP tools: {len(cached_tools)} tools")
            return cached_tools
        
        # Discover available tools
        tools = []
        
        # Try to discover TAC system
        try:
            tac_tool = TACSystem()
            await tac_tool.health_check()
            tools.append(tac_tool)
            logger.info("TAC system discovered and healthy")
        except Exception as e:
            logger.warning(f"TAC system not available: {e}")
        
        # Try to discover DataGov system
        try:
            datagov_tool = DataGovSystem()
            await datagov_tool.health_check()
            tools.append(datagov_tool)
            logger.info("DataGov system discovered and healthy")
        except Exception as e:
            logger.warning(f"DataGov system not available: {e}")
        
        # Try to discover Forecasting engine
        try:
            forecasting_tool = ForecastingEngine()
            await forecasting_tool.health_check()
            tools.append(forecasting_tool)
            logger.info("Forecasting engine discovered and healthy")
        except Exception as e:
            logger.warning(f"Forecasting engine not available: {e}")
        
        # Cache discovered tools
        await self.tool_cache.set_tools(tools)
        self.available_tools = tools
        
        logger.info(f"Discovered {len(tools)} MCP tools")
        return tools
    
    async def execute_tool_with_monitoring(self, tool: MCPTool, query: str) -> Any:
        """Execute a tool with health monitoring."""
        start_time = datetime.now()
        
        try:
            result = await tool.execute(query)
            response_time = (datetime.now() - start_time).total_seconds()
            
            await self.health_monitor.record_success(tool, response_time)
            return result
            
        except Exception as e:
            await self.health_monitor.record_failure(tool, e)
            raise
    
    async def get_tool_health(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed health information for all tools."""
        health_info = {}
        
        for tool in self.available_tools:
            health_info[tool.name] = {
                'health_status': tool.metrics.health_status.value,
                'success_rate': tool.metrics.success_rate,
                'average_response_time': tool.metrics.average_response_time,
                'total_executions': tool.metrics.success_count + tool.metrics.failure_count,
                'last_success': tool.metrics.last_success.isoformat() if tool.metrics.last_success else None,
                'last_failure': tool.metrics.last_failure.isoformat() if tool.metrics.last_failure else None
            }
        
        return health_info
    
    async def get_healthy_tools(self) -> List[MCPTool]:
        """Get only healthy tools."""
        return [
            tool for tool in self.available_tools
            if tool.metrics.health_status in [ToolHealth.HEALTHY, ToolHealth.DEGRADED]
        ]
    
    async def refresh_tool_discovery(self) -> List[MCPTool]:
        """Force refresh of tool discovery."""
        self.tool_cache.last_discovery = None  # Force cache expiration
        return await self.discover_mcp_tools()


# Global instance
mcp_tool_manager = MCPToolManager()
