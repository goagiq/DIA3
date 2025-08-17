"""
MCP Tool Management API Routes
API endpoints for dynamic MCP tool management
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import logging

from ...mcp_servers.dynamic_tool_manager import (
    dynamic_tool_manager, 
    ToolStatus, 
    ResourceLevel,
    ToolConfig
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mcp/tools", tags=["MCP Tool Management"])


# Request/Response Models
class ToolStatusResponse(BaseModel):
    name: str
    status: str
    priority: int
    resource_usage: Dict[str, float]
    last_health_check: str
    error_count: int
    description: str
    version: str


class SystemResourcesResponse(BaseModel):
    cpu_percent: float
    memory_percent: float
    memory_available_mb: float
    disk_percent: float
    disk_free_mb: float
    resource_level: str
    timestamp: float


class ToolConfigUpdate(BaseModel):
    enabled: Optional[bool] = None
    priority: Optional[int] = None
    max_cpu_percent: Optional[float] = None
    max_memory_mb: Optional[float] = None
    max_gpu_percent: Optional[float] = None
    auto_scale: Optional[bool] = None


class AutoScalingConfig(BaseModel):
    enabled: bool


class ToolActionResponse(BaseModel):
    success: bool
    message: str
    tool_name: str
    new_status: str


# API Endpoints
@router.get("/status", response_model=Dict[str, ToolStatusResponse])
async def get_all_tool_statuses():
    """Get status of all MCP tools"""
    try:
        tool_statuses = dynamic_tool_manager.get_all_tool_statuses()
        response = {}
        
        for tool_name, tool_info in tool_statuses.items():
            response[tool_name] = ToolStatusResponse(
                name=tool_info.name,
                status=tool_info.status.value,
                priority=tool_info.config.priority,
                resource_usage={
                    "cpu_percent": tool_info.resource_usage.cpu_percent,
                    "memory_mb": tool_info.resource_usage.memory_mb,
                    "gpu_percent": tool_info.resource_usage.gpu_percent,
                    "gpu_memory_mb": tool_info.resource_usage.gpu_memory_mb
                },
                last_health_check=tool_info.last_health_check.isoformat(),
                error_count=tool_info.error_count,
                description=tool_info.description,
                version=tool_info.version
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting tool statuses: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting tool statuses: {e}")


@router.get("/status/{tool_name}", response_model=ToolStatusResponse)
async def get_tool_status(tool_name: str):
    """Get status of a specific MCP tool"""
    try:
        tool_info = dynamic_tool_manager.get_tool_status(tool_name)
        
        if not tool_info:
            raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
        
        return ToolStatusResponse(
            name=tool_info.name,
            status=tool_info.status.value,
            priority=tool_info.config.priority,
            resource_usage={
                "cpu_percent": tool_info.resource_usage.cpu_percent,
                "memory_mb": tool_info.resource_usage.memory_mb,
                "gpu_percent": tool_info.resource_usage.gpu_percent,
                "gpu_memory_mb": tool_info.resource_usage.gpu_memory_mb
            },
            last_health_check=tool_info.last_health_check.isoformat(),
            error_count=tool_info.error_count,
            description=tool_info.description,
            version=tool_info.version
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tool status for {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting tool status: {e}")


@router.post("/{tool_name}/enable", response_model=ToolActionResponse)
async def enable_tool(tool_name: str, background_tasks: BackgroundTasks):
    """Enable a specific MCP tool"""
    try:
        # Add to background tasks to avoid blocking
        background_tasks.add_task(dynamic_tool_manager.enable_tool, tool_name)
        
        return ToolActionResponse(
            success=True,
            message=f"Tool {tool_name} is being enabled",
            tool_name=tool_name,
            new_status="starting"
        )
        
    except Exception as e:
        logger.error(f"Error enabling tool {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error enabling tool: {e}")


@router.post("/{tool_name}/disable", response_model=ToolActionResponse)
async def disable_tool(tool_name: str, background_tasks: BackgroundTasks):
    """Disable a specific MCP tool"""
    try:
        # Add to background tasks to avoid blocking
        background_tasks.add_task(dynamic_tool_manager.disable_tool, tool_name)
        
        return ToolActionResponse(
            success=True,
            message=f"Tool {tool_name} is being disabled",
            tool_name=tool_name,
            new_status="stopping"
        )
        
    except Exception as e:
        logger.error(f"Error disabling tool {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error disabling tool: {e}")


@router.post("/{tool_name}/pause", response_model=ToolActionResponse)
async def pause_tool(tool_name: str, background_tasks: BackgroundTasks):
    """Pause a specific MCP tool"""
    try:
        # Add to background tasks to avoid blocking
        background_tasks.add_task(dynamic_tool_manager.pause_tool, tool_name)
        
        return ToolActionResponse(
            success=True,
            message=f"Tool {tool_name} is being paused",
            tool_name=tool_name,
            new_status="paused"
        )
        
    except Exception as e:
        logger.error(f"Error pausing tool {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error pausing tool: {e}")


@router.post("/{tool_name}/resume", response_model=ToolActionResponse)
async def resume_tool(tool_name: str, background_tasks: BackgroundTasks):
    """Resume a specific MCP tool"""
    try:
        # Add to background tasks to avoid blocking
        background_tasks.add_task(dynamic_tool_manager.resume_tool, tool_name)
        
        return ToolActionResponse(
            success=True,
            message=f"Tool {tool_name} is being resumed",
            tool_name=tool_name,
            new_status="enabled"
        )
        
    except Exception as e:
        logger.error(f"Error resuming tool {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error resuming tool: {e}")


@router.get("/resources", response_model=SystemResourcesResponse)
async def get_system_resources():
    """Get current system resource usage"""
    try:
        resources = dynamic_tool_manager.get_system_resources()
        resource_level = dynamic_tool_manager.get_resource_level()
        
        return SystemResourcesResponse(
            cpu_percent=resources.get("cpu_percent", 0),
            memory_percent=resources.get("memory_percent", 0),
            memory_available_mb=resources.get("memory_available_mb", 0),
            disk_percent=resources.get("disk_percent", 0),
            disk_free_mb=resources.get("disk_free_mb", 0),
            resource_level=resource_level.value,
            timestamp=resources.get("timestamp", 0)
        )
        
    except Exception as e:
        logger.error(f"Error getting system resources: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting system resources: {e}")


@router.post("/auto-scale", response_model=Dict[str, Any])
async def set_auto_scaling(config: AutoScalingConfig):
    """Enable or disable auto-scaling"""
    try:
        dynamic_tool_manager.set_auto_scaling(config.enabled)
        
        return {
            "success": True,
            "message": f"Auto-scaling {'enabled' if config.enabled else 'disabled'}",
            "auto_scaling_enabled": config.enabled
        }
        
    except Exception as e:
        logger.error(f"Error setting auto-scaling: {e}")
        raise HTTPException(status_code=500, detail=f"Error setting auto-scaling: {e}")


@router.get("/auto-scale", response_model=Dict[str, Any])
async def get_auto_scaling_status():
    """Get auto-scaling status"""
    try:
        return {
            "auto_scaling_enabled": dynamic_tool_manager.auto_scaling_enabled,
            "resource_level": dynamic_tool_manager.get_resource_level().value
        }
        
    except Exception as e:
        logger.error(f"Error getting auto-scaling status: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting auto-scaling status: {e}")


@router.put("/{tool_name}/config", response_model=Dict[str, Any])
async def update_tool_config(tool_name: str, config_update: ToolConfigUpdate):
    """Update tool configuration"""
    try:
        # Convert Pydantic model to dict, excluding None values
        config_dict = config_update.dict(exclude_none=True)
        
        success = dynamic_tool_manager.update_tool_config(tool_name, **config_dict)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
        
        return {
            "success": True,
            "message": f"Configuration updated for tool {tool_name}",
            "tool_name": tool_name,
            "updated_fields": list(config_dict.keys())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating tool config for {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating tool config: {e}")


@router.post("/monitoring/start", response_model=Dict[str, Any])
async def start_monitoring():
    """Start resource monitoring and auto-scaling"""
    try:
        await dynamic_tool_manager.start_monitoring()
        
        return {
            "success": True,
            "message": "Resource monitoring started",
            "monitoring_active": True
        }
        
    except Exception as e:
        logger.error(f"Error starting monitoring: {e}")
        raise HTTPException(status_code=500, detail=f"Error starting monitoring: {e}")


@router.post("/monitoring/stop", response_model=Dict[str, Any])
async def stop_monitoring():
    """Stop resource monitoring and auto-scaling"""
    try:
        await dynamic_tool_manager.stop_monitoring()
        
        return {
            "success": True,
            "message": "Resource monitoring stopped",
            "monitoring_active": False
        }
        
    except Exception as e:
        logger.error(f"Error stopping monitoring: {e}")
        raise HTTPException(status_code=500, detail=f"Error stopping monitoring: {e}")


@router.get("/monitoring/status", response_model=Dict[str, Any])
async def get_monitoring_status():
    """Get monitoring status"""
    try:
        return {
            "monitoring_active": dynamic_tool_manager.running,
            "auto_scaling_enabled": dynamic_tool_manager.auto_scaling_enabled,
            "resource_level": dynamic_tool_manager.get_resource_level().value,
            "active_tools_count": len([info for info in dynamic_tool_manager.get_all_tool_statuses().values() 
                                     if info.status in [ToolStatus.ENABLED, ToolStatus.PAUSED]])
        }
        
    except Exception as e:
        logger.error(f"Error getting monitoring status: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting monitoring status: {e}")


@router.post("/bulk/enable", response_model=Dict[str, Any])
async def enable_multiple_tools(tool_names: List[str], background_tasks: BackgroundTasks):
    """Enable multiple MCP tools"""
    try:
        results = []
        
        for tool_name in tool_names:
            background_tasks.add_task(dynamic_tool_manager.enable_tool, tool_name)
            results.append({
                "tool_name": tool_name,
                "action": "enable",
                "status": "queued"
            })
        
        return {
            "success": True,
            "message": f"Enabling {len(tool_names)} tools",
            "tools": results
        }
        
    except Exception as e:
        logger.error(f"Error enabling multiple tools: {e}")
        raise HTTPException(status_code=500, detail=f"Error enabling multiple tools: {e}")


@router.post("/bulk/disable", response_model=Dict[str, Any])
async def disable_multiple_tools(tool_names: List[str], background_tasks: BackgroundTasks):
    """Disable multiple MCP tools"""
    try:
        results = []
        
        for tool_name in tool_names:
            background_tasks.add_task(dynamic_tool_manager.disable_tool, tool_name)
            results.append({
                "tool_name": tool_name,
                "action": "disable",
                "status": "queued"
            })
        
        return {
            "success": True,
            "message": f"Disabling {len(tool_names)} tools",
            "tools": results
        }
        
    except Exception as e:
        logger.error(f"Error disabling multiple tools: {e}")
        raise HTTPException(status_code=500, detail=f"Error disabling multiple tools: {e}")


@router.get("/health", response_model=Dict[str, Any])
async def get_health_status():
    """Get overall health status of MCP tool management system"""
    try:
        tool_statuses = dynamic_tool_manager.get_all_tool_statuses()
        system_resources = dynamic_tool_manager.get_system_resources()
        
        # Calculate health metrics
        total_tools = len(tool_statuses)
        active_tools = len([info for info in tool_statuses.values() 
                          if info.status in [ToolStatus.ENABLED, ToolStatus.PAUSED]])
        error_tools = len([info for info in tool_statuses.values() 
                          if info.status == ToolStatus.ERROR])
        
        health_score = 100
        if total_tools > 0:
            health_score = ((active_tools - error_tools) / total_tools) * 100
        
        return {
            "status": "healthy" if health_score > 80 else "degraded" if health_score > 50 else "unhealthy",
            "health_score": round(health_score, 2),
            "total_tools": total_tools,
            "active_tools": active_tools,
            "error_tools": error_tools,
            "system_resources": {
                "cpu_percent": system_resources.get("cpu_percent", 0),
                "memory_percent": system_resources.get("memory_percent", 0),
                "resource_level": dynamic_tool_manager.get_resource_level().value
            },
            "monitoring_active": dynamic_tool_manager.running,
            "auto_scaling_enabled": dynamic_tool_manager.auto_scaling_enabled
        }
        
    except Exception as e:
        logger.error(f"Error getting health status: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting health status: {e}")
