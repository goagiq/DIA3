"""
Enhanced Report API Routes with Source Tracking and Modular Report System

This module provides API endpoints for generating enhanced reports with comprehensive
source tracking, tooltips, and detailed references for all data points.
Now includes the modular report system as the default template and adaptive system.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from loguru import logger

# Import enhanced report orchestrator if available
try:
    from src.core.enhanced_report_orchestrator import (
        get_enhanced_report_orchestrator,
        generate_enhanced_report_with_tracking,
        generate_visualization_with_enhanced_tooltips
    )
    ENHANCED_REPORT_ORCHESTRATOR_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced report orchestrator not available: {e}")
    ENHANCED_REPORT_ORCHESTRATOR_AVAILABLE = False
    # Create dummy functions for fallback
    def get_enhanced_report_orchestrator():
        return None
    def generate_enhanced_report_with_tracking(*args, **kwargs):
        return {"success": False, "error": "Enhanced report orchestrator not available"}
    def generate_visualization_with_enhanced_tooltips(*args, **kwargs):
        return {"success": False, "error": "Enhanced report orchestrator not available"}

# Import modular report generator
try:
    from src.core.modular_report_generator import modular_report_generator
    MODULAR_REPORT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Modular report generator not available: {e}")
    MODULAR_REPORT_AVAILABLE = False

# Import integrated adaptive modular report generator
try:
    from src.core.integrated_adaptive_modular_report_generator import integrated_adaptive_modular_report_generator
    ADAPTIVE_MODULAR_REPORT_AVAILABLE = True
    logger.info("✅ Integrated adaptive modular report generator available")
except ImportError as e:
    logger.warning(f"Integrated adaptive modular report generator not available: {e}")
    ADAPTIVE_MODULAR_REPORT_AVAILABLE = False

# Create router
router = APIRouter(prefix="/enhanced-report", tags=["Enhanced Report with Source Tracking and Modular System"])

# Pydantic models
class EnhancedReportRequest(BaseModel):
    """Request model for enhanced report generation."""
    content: str = Field(..., description="Content to analyze and generate report for")
    report_type: str = Field(default="adaptive", description="Type of report to generate (adaptive, modular, comprehensive, basic)")
    include_tooltips: bool = Field(default=True, description="Include interactive tooltips")
    include_source_references: bool = Field(default=True, description="Include source references")
    include_calculations: bool = Field(default=True, description="Include calculation details")
    language: str = Field(default="en", description="Report language")
    format: str = Field(default="html", description="Output format (html, markdown)")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    enabled_modules: Optional[List[str]] = Field(default=None, description="List of module IDs to enable (for modular reports)")


class AdaptiveReportRequest(BaseModel):
    """Request model for enhanced adaptive report generation with contextual intelligence."""
    query: str = Field(..., description="The analysis query with automatic context detection (e.g., 'AI Healthcare Innovation', 'Cybersecurity Strategy', 'Economic Analysis')")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Optional analysis data (system will generate contextually adaptive data if not provided)")
    max_modules: Optional[int] = Field(default=None, description="Maximum number of modules to generate (default: all 22 with interactive visualizations)")
    modules: Optional[List[str]] = Field(default=None, description="Specific modules to include (e.g., ['executive_summary', 'risk_assessment']). All include interactive visualizations.")
    module_categories: Optional[List[str]] = Field(default=None, description="Module categories to include (e.g., ['strategic', 'operational', 'analytical'])")
    include_tooltips: bool = Field(default=True, description="Include advanced interactive tooltips with strategic insights")
    include_source_references: bool = Field(default=True, description="Include comprehensive source references")
    format: str = Field(default="html", description="Output format (html, markdown) with Chart.js integration")


class ModularReportRequest(BaseModel):
    """Request model for modular report generation."""
    topic: str = Field(..., description="The analysis topic")
    data: Dict[str, Any] = Field(..., description="Analysis data for all modules")
    enabled_modules: Optional[List[str]] = Field(default=None, description="List of module IDs to enable")
    report_title: Optional[str] = Field(default=None, description="Custom report title")
    custom_config: Optional[Dict[str, Any]] = Field(default=None, description="Custom configuration for modules")
    include_tooltips: bool = Field(default=True, description="Include interactive tooltips")
    include_source_references: bool = Field(default=True, description="Include source references")
    format: str = Field(default="html", description="Output format (html, markdown)")


class EnhancedReportResponse(BaseModel):
    """Response model for enhanced report generation."""
    success: bool
    enhanced_report: Optional[Dict[str, Any]] = None
    source_tracking: Optional[Dict[str, Any]] = None
    tooltip_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AdaptiveReportResponse(BaseModel):
    """Response model for adaptive report generation."""
    success: bool
    report_file: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    query: Optional[str] = None
    universal_data_sections: Optional[int] = None
    modules_generated: Optional[int] = None
    integrated_adaptive_mode: Optional[bool] = None
    generated_at: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ModularReportResponse(BaseModel):
    """Response model for modular report generation."""
    success: bool
    report_file: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    modules_used: Optional[List[str]] = None
    generated_at: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class VisualizationRequest(BaseModel):
    """Request model for visualization with tooltips."""
    data: Dict[str, Any] = Field(..., description="Data to visualize")
    visualization_type: str = Field(default="interactive", description="Type of visualization")
    include_tooltips: bool = Field(default=True, description="Include tooltips")
    chart_type: Optional[str] = Field(default=None, description="Specific chart type")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class VisualizationResponse(BaseModel):
    """Response model for visualization generation."""
    success: bool
    visualization: Optional[Dict[str, Any]] = None
    tooltip_data: Optional[Dict[str, Any]] = None
    source_tracking: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class SourceTrackingRequest(BaseModel):
    """Request model for source tracking operations."""
    operation: str = Field(..., description="Operation to perform")
    data_points: Optional[List[str]] = Field(default=None, description="Data point IDs")
    session_id: Optional[str] = Field(default=None, description="Session ID")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class SourceTrackingResponse(BaseModel):
    """Response model for source tracking operations."""
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# API Endpoints
@router.post("/generate", response_model=EnhancedReportResponse)
async def generate_enhanced_report(request: EnhancedReportRequest):
    """Generate an enhanced report with comprehensive source tracking."""
    try:
        logger.info(f"Generating enhanced report: {request.report_type}")
        
        # If adaptive report is requested and available, use adaptive system
        if request.report_type == "adaptive" and ADAPTIVE_MODULAR_REPORT_AVAILABLE:
            return await generate_adaptive_report(AdaptiveReportRequest(
                query=request.content,
                data=request.metadata or {},
                include_tooltips=request.include_tooltips,
                include_source_references=request.include_source_references,
                format=request.format
            ))
        
        # If modular report is requested and available, use modular system
        if request.report_type == "modular" and MODULAR_REPORT_AVAILABLE:
            return await generate_modular_report(ModularReportRequest(
                topic=request.content,
                data=request.metadata or {},
                enabled_modules=request.enabled_modules,
                report_title=request.metadata.get("report_title") if request.metadata else None,
                custom_config=request.metadata.get("custom_config") if request.metadata else None,
                include_tooltips=request.include_tooltips,
                include_source_references=request.include_source_references,
                format=request.format
            ))
        
        # Fall back to original enhanced report system
        result = await generate_enhanced_report_with_tracking(
            content=request.content,
            report_type=request.report_type,
            include_tooltips=request.include_tooltips,
            include_source_references=request.include_source_references,
            include_calculations=request.include_calculations,
            language=request.language,
            format=request.format,
            **(request.metadata or {})
        )
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate enhanced report: {result.get('error', 'Unknown error')}"
            )
        
        return EnhancedReportResponse(
            success=True,
            enhanced_report=result.get("enhanced_report"),
            source_tracking=result.get("source_tracking"),
            tooltip_data=result.get("tooltip_data"),
            metadata=result.get("metadata")
        )
        
    except Exception as e:
        logger.error(f"Error generating enhanced report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate enhanced report: {str(e)}")


@router.post("/generate-adaptive", response_model=AdaptiveReportResponse)
async def generate_adaptive_report(request: AdaptiveReportRequest):
    """Generate an adaptive enhanced report using the integrated adaptive modular system."""
    try:
        if not ADAPTIVE_MODULAR_REPORT_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Integrated adaptive modular report system is not available"
            )
        
        logger.info(f"Generating adaptive report for query: {request.query}")
        
        result = await integrated_adaptive_modular_report_generator.generate_adaptive_report(
            query=request.query,
            data=request.data,
            max_modules=request.max_modules,
            modules=request.modules,
            module_categories=request.module_categories
        )
        
        if result.get("success"):
            return AdaptiveReportResponse(
                success=True,
                report_file=result.get("filename"),
                file_path=result.get("file_path"),
                file_size=result.get("file_size"),
                query=request.query,
                universal_data_sections=result.get("universal_data_sections"),
                modules_generated=result.get("modules_generated"),
                integrated_adaptive_mode=result.get("integrated_adaptive_mode"),
                generated_at=result.get("generated_at"),
                metadata=result.get("metadata")
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate adaptive report: {result.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        logger.error(f"Error generating adaptive report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate adaptive report: {str(e)}")


@router.post("/generate-modular", response_model=ModularReportResponse)
async def generate_modular_report(request: ModularReportRequest):
    """Generate a modular enhanced report with configurable components."""
    try:
        if not MODULAR_REPORT_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Modular report system is not available"
            )
        
        logger.info(f"Generating modular report for topic: {request.topic}")
        
        result = await modular_report_generator.generate_modular_report(
            topic=request.topic,
            data=request.data,
            enabled_modules=request.enabled_modules,
            report_title=request.report_title,
            custom_config=request.custom_config
        )
        
        if result.get("success"):
            return ModularReportResponse(
                success=True,
                report_file=result.get("filename"),
                file_path=result.get("file_path"),
                file_size=result.get("file_size"),
                modules_used=result.get("modules_used"),
                generated_at=result.get("generated_at"),
                metadata=result.get("metadata")
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate modular report: {result.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        logger.error(f"Error generating modular report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate modular report: {str(e)}")


@router.get("/modules")
async def get_available_modules():
    """Get list of available modules and their configurations."""
    try:
        if not MODULAR_REPORT_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Modular report system is not available"
            )
        
        available_modules = modular_report_generator.get_available_modules()
        enabled_modules = [m.module_id for m in modular_report_generator.get_enabled_modules()]
        
        module_details = []
        for module_id in available_modules:
            module = modular_report_generator.get_module(module_id)
            if module:
                metadata = module.get_module_metadata()
                module_details.append({
                    "module_id": module_id,
                    "name": metadata.get("name", module_id),
                    "description": metadata.get("description", ""),
                    "enabled": module_id in enabled_modules,
                    "required_data_keys": module.get_required_data_keys(),
                    "capabilities": metadata.get("capabilities", [])
                })
        
        return {
            "success": True,
            "modules": module_details,
            "total_modules": len(module_details),
            "enabled_modules": enabled_modules,
            "available_modules": available_modules
        }
        
    except Exception as e:
        logger.error(f"Error getting available modules: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get available modules: {str(e)}")


@router.post("/configure-module")
async def configure_module(module_id: str, config: Dict[str, Any]):
    """Configure a specific module with custom settings."""
    try:
        if not MODULAR_REPORT_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Modular report system is not available"
            )
        
        module = modular_report_generator.get_module(module_id)
        if not module:
            raise HTTPException(
                status_code=404,
                detail=f"Module {module_id} not found"
            )
        
        # Configure the module
        module.configure(config)
        
        return {
            "success": True,
            "message": f"Module {module_id} configured successfully",
            "module_id": module_id,
            "config": config
        }
        
    except Exception as e:
        logger.error(f"Error configuring module {module_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to configure module: {str(e)}")


@router.post("/enable-modules")
async def enable_modules(module_ids: List[str], disable_others: bool = False):
    """Enable or disable specific modules."""
    try:
        if not MODULAR_REPORT_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Modular report system is not available"
            )
        
        # Enable specified modules
        for module_id in module_ids:
            module = modular_report_generator.get_module(module_id)
            if module:
                module.enable()
        
        # Disable other modules if requested
        if disable_others:
            available_modules = modular_report_generator.get_available_modules()
            for module_id in available_modules:
                if module_id not in module_ids:
                    module = modular_report_generator.get_module(module_id)
                    if module:
                        module.disable()
        
        enabled_modules = [m.module_id for m in modular_report_generator.get_enabled_modules()]
        
        return {
            "success": True,
            "message": f"Modules updated successfully",
            "enabled_modules": enabled_modules,
            "requested_modules": module_ids
        }
        
    except Exception as e:
        logger.error(f"Error enabling modules: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to enable modules: {str(e)}")


@router.post("/visualization", response_model=VisualizationResponse)
async def generate_visualization(request: VisualizationRequest):
    """Generate visualization with enhanced tooltips."""
    try:
        logger.info(f"Generating visualization: {request.visualization_type}")
        
        result = await generate_visualization_with_enhanced_tooltips(
            data=request.data,
            visualization_type=request.visualization_type,
            include_tooltips=request.include_tooltips,
            chart_type=request.chart_type,
            **(request.metadata or {})
        )
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate visualization: {result.get('error', 'Unknown error')}"
            )
        
        return VisualizationResponse(
            success=True,
            visualization=result.get("visualization"),
            tooltip_data=result.get("tooltip_data"),
            source_tracking=result.get("source_tracking"),
            metadata=result.get("metadata")
        )
        
    except Exception as e:
        logger.error(f"Error generating visualization: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate visualization: {str(e)}")


@router.post("/source-tracking", response_model=SourceTrackingResponse)
async def manage_source_tracking(request: SourceTrackingRequest):
    """Manage source tracking operations."""
    try:
        logger.info(f"Managing source tracking: {request.operation}")
        
        orchestrator = get_enhanced_report_orchestrator()
        result = await orchestrator.manage_source_tracking(
            operation=request.operation,
            data_points=request.data_points,
            session_id=request.session_id,
            **(request.metadata or {})
        )
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=f"Failed to manage source tracking: {result.get('error', 'Unknown error')}"
            )
        
        return SourceTrackingResponse(
            success=True,
            result=result.get("result"),
            metadata=result.get("metadata")
        )
        
    except Exception as e:
        logger.error(f"Error managing source tracking: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to manage source tracking: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check for enhanced report service."""
    try:
        return {
            "service": "enhanced_report",
            "status": "healthy",
            "version": "3.0.0",
            "modular_system_available": MODULAR_REPORT_AVAILABLE,
            "adaptive_modular_system_available": ADAPTIVE_MODULAR_REPORT_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.get("/capabilities")
async def get_capabilities():
    """Get enhanced report capabilities."""
    try:
        capabilities = {
            "service": "enhanced_report",
            "version": "3.0.0",
            "features": {
                "adaptive_modular_reports": {
                    "description": "Integrated adaptive modular report system that generates reports based on natural language queries and adapts to new data.",
                    "available": ADAPTIVE_MODULAR_REPORT_AVAILABLE,
                    "capabilities": [
                        "Natural language query processing",
                        "Adaptive data generation",
                        "Universal data sections",
                        "Multiple module integration",
                        "Professional HTML output"
                    ] if ADAPTIVE_MODULAR_REPORT_AVAILABLE else ["Not available"]
                },
                "modular_reports": {
                    "description": "Modular report system with 22 configurable components",
                    "available": MODULAR_REPORT_AVAILABLE,
                    "capabilities": [
                        "22 independent report modules",
                        "Configurable module selection",
                        "Interactive tooltips and charts",
                        "Professional HTML output",
                        "Source tracking integration"
                    ] if MODULAR_REPORT_AVAILABLE else ["Not available"]
                },
                "source_tracking": {
                    "description": "Comprehensive tracking of all data sources and calculations",
                    "capabilities": [
                        "Automatic source reference tracking",
                        "Calculation step tracking",
                        "Confidence score tracking",
                        "Execution time tracking",
                        "Metadata tracking"
                    ]
                },
                "tooltips": {
                    "description": "Interactive tooltips with detailed information",
                    "capabilities": [
                        "Source reference display",
                        "Calculation formula display",
                        "Confidence score display",
                        "Timestamp information",
                        "Metadata display"
                    ]
                },
                "reports": {
                    "description": "Enhanced reports with source tracking",
                    "capabilities": [
                        "Comprehensive source references",
                        "Calculation details",
                        "Interactive tooltips",
                        "Multiple output formats",
                        "Session management"
                    ]
                },
                "visualizations": {
                    "description": "Visualizations with tooltip integration",
                    "capabilities": [
                        "Interactive charts",
                        "Tooltip integration",
                        "Source tracking",
                        "Multiple chart types",
                        "Export capabilities"
                    ]
                }
            },
            "api_endpoints": [
                "POST /enhanced-report/generate - Generate enhanced report (adaptive by default)",
                "POST /enhanced-report/generate-adaptive - Generate adaptive report",
                "POST /enhanced-report/generate-modular - Generate modular report",
                "GET /enhanced-report/modules - Get available modules",
                "POST /enhanced-report/configure-module - Configure module",
                "POST /enhanced-report/enable-modules - Enable/disable modules",
                "POST /enhanced-report/visualization - Generate visualization with tooltips",
                "POST /enhanced-report/source-tracking - Manage source tracking",
                "GET /enhanced-report/health - Health check",
                "GET /enhanced-report/capabilities - Get capabilities"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        return capabilities
        
    except Exception as e:
        logger.error(f"Error getting capabilities: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get capabilities: {str(e)}")


@router.get("/examples")
async def get_enhanced_report_examples():
    """Get examples of enhanced report usage."""
    try:
        examples = {
            "service": "enhanced_report",
            "examples": {
                "adaptive_report": {
                    "description": "Generate an adaptive enhanced report (default)",
                    "request": {
                        "content": "Pakistan Submarine Acquisition Analysis and Deterrence Enhancement",
                        "report_type": "adaptive",
                        "include_tooltips": True,
                        "include_source_references": True,
                        "format": "html"
                    }
                },
                "modular_report": {
                    "description": "Generate a modular enhanced report",
                    "request": {
                        "content": "Sample content for analysis",
                        "report_type": "modular",
                        "include_tooltips": True,
                        "include_source_references": True,
                        "include_calculations": True
                    }
                },
                "adaptive_report_detailed": {
                    "description": "Generate adaptive report with specific query and data",
                    "request": {
                        "query": "Pakistan Submarine Acquisition Analysis",
                        "data": {
                            "executive_summary": {...},
                            "strategic_analysis": {...},
                            "economic_analysis": {...}
                        },
                        "include_tooltips": True
                    }
                },
                "visualization": {
                    "description": "Generate visualization with tooltips",
                    "request": {
                        "data": {"x": [1, 2, 3], "y": [4, 5, 6]},
                        "visualization_type": "interactive",
                        "include_tooltips": True
                    }
                },
                "source_tracking": {
                    "description": "Manage source tracking session",
                    "request": {
                        "operation": "save_session"
                    }
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return examples
        
    except Exception as e:
        logger.error(f"Error getting examples: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get examples: {str(e)}")
