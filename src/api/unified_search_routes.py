"""
Unified Search API Routes

This module provides API endpoints for the unified search system that routes
all queries through local knowledge first, then all available MCP tools.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from loguru import logger

# Import the unified search orchestrator
try:
    from src.core.unified_search_orchestrator import (
        unified_search_orchestrator,
        SearchResults,
        SourceType
    )
    from src.core.mcp_tool_manager import mcp_tool_manager
    UNIFIED_SEARCH_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Unified search components not available: {e}")
    UNIFIED_SEARCH_AVAILABLE = False

router = APIRouter(prefix="/unified-search", tags=["Unified Search"])


# Request/Response Models
class SearchRequest(BaseModel):
    """Request model for unified search."""
    query: str = Field(..., description="Search query")
    user_context: Optional[Dict[str, Any]] = Field(default=None, description="Additional user context")
    include_local_only: bool = Field(default=False, description="Search only local knowledge sources")
    include_mcp_only: bool = Field(default=False, description="Search only MCP tools")


class SearchResponse(BaseModel):
    """Response model for unified search."""
    query: str
    results: List[Dict[str, Any]]
    sources_queried: List[str]
    processing_time: float
    cache_hit: bool
    timestamp: datetime
    total_results: int


class ToolHealthResponse(BaseModel):
    """Response model for tool health information."""
    tool_name: str
    health_status: str
    success_rate: float
    average_response_time: float
    total_executions: int
    last_success: Optional[str]
    last_failure: Optional[str]


class HealthSummaryResponse(BaseModel):
    """Response model for health summary."""
    tools: List[ToolHealthResponse]
    overall_health: str
    healthy_tools: int
    total_tools: int


@router.post("/search", response_model=SearchResponse)
async def unified_search(request: SearchRequest):
    """
    Perform unified search through all available sources.
    
    Routes query through local knowledge first, then all available MCP tools.
    """
    if not UNIFIED_SEARCH_AVAILABLE:
        raise HTTPException(status_code=503, detail="Unified search system not available")
    
    try:
        logger.info(f"Processing unified search query: {request.query[:100]}...")
        
        # Process the query through the orchestrator
        results = await unified_search_orchestrator.process_query(
            query=request.query,
            user_context=request.user_context
        )
        
        # Convert results to response format
        response_results = []
        for result in results.results:
            response_results.append({
                "content": result.content,
                "confidence": result.confidence,
                "intelligence_type": result.intelligence_type,
                "timestamp": result.timestamp.isoformat(),
                "sources": [
                    {
                        "source_type": source.source_type.value,
                        "source_name": source.source_name,
                        "title": source.title,
                        "url": source.url,
                        "confidence": source.confidence,
                        "reliability_score": source.reliability_score
                    }
                    for source in result.sources
                ]
            })
        
        return SearchResponse(
            query=results.query,
            results=response_results,
            sources_queried=[source.value for source in results.sources_queried],
            processing_time=results.processing_time,
            cache_hit=results.cache_hit,
            timestamp=results.timestamp,
            total_results=len(results.results)
        )
        
    except Exception as e:
        logger.error(f"Error in unified search: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/health", response_model=HealthSummaryResponse)
async def get_tool_health():
    """Get health information for all MCP tools."""
    if not UNIFIED_SEARCH_AVAILABLE:
        raise HTTPException(status_code=503, detail="Unified search system not available")
    
    try:
        health_info = await mcp_tool_manager.get_tool_health()
        
        tools = []
        healthy_count = 0
        
        for tool_name, info in health_info.items():
            tools.append(ToolHealthResponse(
                tool_name=tool_name,
                health_status=info['health_status'],
                success_rate=info['success_rate'],
                average_response_time=info['average_response_time'],
                total_executions=info['total_executions'],
                last_success=info['last_success'],
                last_failure=info['last_failure']
            ))
            
            if info['health_status'] in ['healthy', 'degraded']:
                healthy_count += 1
        
        # Determine overall health
        total_tools = len(tools)
        if healthy_count == total_tools:
            overall_health = "healthy"
        elif healthy_count > total_tools / 2:
            overall_health = "degraded"
        else:
            overall_health = "unhealthy"
        
        return HealthSummaryResponse(
            tools=tools,
            overall_health=overall_health,
            healthy_tools=healthy_count,
            total_tools=total_tools
        )
        
    except Exception as e:
        logger.error(f"Error getting tool health: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.post("/refresh-tools")
async def refresh_tools():
    """Force refresh of MCP tool discovery."""
    if not UNIFIED_SEARCH_AVAILABLE:
        raise HTTPException(status_code=503, detail="Unified search system not available")
    
    try:
        tools = await mcp_tool_manager.refresh_tool_discovery()
        return {
            "message": f"Tool discovery refreshed successfully",
            "discovered_tools": len(tools),
            "tools": [tool.name for tool in tools]
        }
        
    except Exception as e:
        logger.error(f"Error refreshing tools: {e}")
        raise HTTPException(status_code=500, detail=f"Tool refresh failed: {str(e)}")


@router.get("/cache/status")
async def get_cache_status():
    """Get cache status information."""
    if not UNIFIED_SEARCH_AVAILABLE:
        raise HTTPException(status_code=503, detail="Unified search system not available")
    
    try:
        cache = unified_search_orchestrator.cache
        return {
            "cache_size": len(cache.cache),
            "cache_duration": cache.cache_duration,
            "cached_queries": list(cache.cache.keys())[:10]  # Show first 10 queries
        }
        
    except Exception as e:
        logger.error(f"Error getting cache status: {e}")
        raise HTTPException(status_code=500, detail=f"Cache status failed: {str(e)}")


@router.delete("/cache/clear")
async def clear_cache():
    """Clear the query cache."""
    if not UNIFIED_SEARCH_AVAILABLE:
        raise HTTPException(status_code=503, detail="Unified search system not available")
    
    try:
        cache = unified_search_orchestrator.cache
        cache_size = len(cache.cache)
        cache.cache.clear()
        
        return {
            "message": "Cache cleared successfully",
            "cleared_entries": cache_size
        }
        
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail=f"Cache clear failed: {str(e)}")


@router.get("/sources")
async def get_available_sources():
    """Get list of available data sources."""
    if not UNIFIED_SEARCH_AVAILABLE:
        raise HTTPException(status_code=503, detail="Unified search system not available")
    
    try:
        # Get local sources
        local_sources = []
        if unified_search_orchestrator.vector_db:
            local_sources.append("vector_database")
        if unified_search_orchestrator.knowledge_graph:
            local_sources.append("knowledge_graph")
        if unified_search_orchestrator.file_search:
            local_sources.append("local_files")
        
        # Get MCP sources
        mcp_tools = await mcp_tool_manager.discover_mcp_tools()
        mcp_sources = [tool.name for tool in mcp_tools]
        
        return {
            "local_sources": local_sources,
            "mcp_sources": mcp_sources,
            "total_sources": len(local_sources) + len(mcp_sources)
        }
        
    except Exception as e:
        logger.error(f"Error getting available sources: {e}")
        raise HTTPException(status_code=500, detail=f"Source listing failed: {str(e)}")


@router.post("/search/local-only", response_model=SearchResponse)
async def search_local_only(request: SearchRequest):
    """Search only local knowledge sources."""
    if not UNIFIED_SEARCH_AVAILABLE:
        raise HTTPException(status_code=503, detail="Unified search system not available")
    
    try:
        logger.info(f"Processing local-only search query: {request.query[:100]}...")
        
        # Search only local knowledge
        results = await unified_search_orchestrator.search_local_knowledge(request.query)
        
        # Convert results to response format
        response_results = []
        for result in results.results:
            response_results.append({
                "content": result.content,
                "confidence": result.confidence,
                "intelligence_type": result.intelligence_type,
                "timestamp": result.timestamp.isoformat(),
                "sources": [
                    {
                        "source_type": source.source_type.value,
                        "source_name": source.source_name,
                        "title": source.title,
                        "url": source.url,
                        "confidence": source.confidence,
                        "reliability_score": source.reliability_score
                    }
                    for source in result.sources
                ]
            })
        
        return SearchResponse(
            query=results.query,
            results=response_results,
            sources_queried=[source.value for source in results.sources_queried],
            processing_time=results.processing_time,
            cache_hit=False,  # Local search doesn't use cache
            timestamp=results.timestamp,
            total_results=len(results.results)
        )
        
    except Exception as e:
        logger.error(f"Error in local-only search: {e}")
        raise HTTPException(status_code=500, detail=f"Local search failed: {str(e)}")


@router.post("/search/mcp-only", response_model=SearchResponse)
async def search_mcp_only(request: SearchRequest):
    """Search only MCP tools."""
    if not UNIFIED_SEARCH_AVAILABLE:
        raise HTTPException(status_code=503, detail="Unified search system not available")
    
    try:
        logger.info(f"Processing MCP-only search query: {request.query[:100]}...")
        
        # Search only MCP tools
        results = await unified_search_orchestrator.search_all_mcp_tools(request.query)
        
        # Convert results to response format
        response_results = []
        for result in results.results:
            response_results.append({
                "content": result.content,
                "confidence": result.confidence,
                "intelligence_type": result.intelligence_type,
                "timestamp": result.timestamp.isoformat(),
                "sources": [
                    {
                        "source_type": source.source_type.value,
                        "source_name": source.source_name,
                        "title": source.title,
                        "url": source.url,
                        "confidence": source.confidence,
                        "reliability_score": source.reliability_score
                    }
                    for source in result.sources
                ]
            })
        
        return SearchResponse(
            query=results.query,
            results=response_results,
            sources_queried=[source.value for source in results.sources_queried],
            processing_time=results.processing_time,
            cache_hit=False,  # MCP search doesn't use cache
            timestamp=results.timestamp,
            total_results=len(results.results)
        )
        
    except Exception as e:
        logger.error(f"Error in MCP-only search: {e}")
        raise HTTPException(status_code=500, detail=f"MCP search failed: {str(e)}")
