"""
Enhanced Report API Routes with Source Tracking

This module provides API endpoints for generating enhanced reports with comprehensive
source tracking, tooltips, and detailed references for all data points.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from loguru import logger

from src.core.enhanced_report_orchestrator import (
    get_enhanced_report_orchestrator,
    generate_enhanced_report_with_tracking,
    generate_visualization_with_enhanced_tooltips
)

# Create router
router = APIRouter(prefix="/enhanced-report", tags=["Enhanced Report with Source Tracking"])

# Pydantic models
class EnhancedReportRequest(BaseModel):
    """Request model for enhanced report generation."""
    content: str = Field(..., description="Content to analyze and generate report for")
    report_type: str = Field(default="comprehensive", description="Type of report to generate")
    include_tooltips: bool = Field(default=True, description="Include interactive tooltips")
    include_source_references: bool = Field(default=True, description="Include source references")
    include_calculations: bool = Field(default=True, description="Include calculation details")
    language: str = Field(default="en", description="Report language")
    format: str = Field(default="markdown", description="Output format")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class EnhancedReportResponse(BaseModel):
    """Response model for enhanced report generation."""
    success: bool
    enhanced_report: Optional[Dict[str, Any]] = None
    source_tracking: Optional[Dict[str, Any]] = None
    tooltip_data: Optional[Dict[str, Any]] = None
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
                detail=result.get("error", "Enhanced report generation failed")
        )
        
        return EnhancedReportResponse(
            success=True,
            enhanced_report=result.get("enhanced_report"),
            source_tracking=result.get("source_tracking"),
            tooltip_data=result.get("source_tracking", {}).get("tooltip_data"),
            metadata={
                "report_type": request.report_type,
                "generated_at": datetime.now().isoformat(),
                "enhancement_features": result.get("enhancement_features")
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating enhanced report: {e}")
        raise HTTPException(status_code=500, detail=f"Enhanced report generation failed: {str(e)}")


@router.post("/visualization", response_model=VisualizationResponse)
async def generate_visualization_with_tooltips(request: VisualizationRequest):
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
                detail=result.get("error", "Visualization generation failed")
            )
        
        return VisualizationResponse(
            success=True,
            visualization=result.get("visualization"),
            tooltip_data=result.get("tooltip_data"),
            source_tracking=result.get("source_tracking"),
            metadata={
                "visualization_type": request.visualization_type,
                "generated_at": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating visualization: {e}")
        raise HTTPException(status_code=500, detail=f"Visualization generation failed: {str(e)}")


@router.post("/source-tracking", response_model=SourceTrackingResponse)
async def manage_source_tracking(request: SourceTrackingRequest):
    """Manage source tracking operations."""
    try:
        logger.info(f"Source tracking operation: {request.operation}")
        
        orchestrator = get_enhanced_report_orchestrator()
        
        if request.operation == "get_tooltip_data":
            result = orchestrator.get_tooltip_data()
        elif request.operation == "save_session":
            filename = f"source_tracking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            result = {"filepath": orchestrator.save_tracking_session(filename)}
        elif request.operation == "generate_report":
            result = orchestrator.generate_source_report()
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported operation: {request.operation}"
            )
        
        return SourceTrackingResponse(
            success=True,
            result=result,
            metadata={
                "operation": request.operation,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error in source tracking operation: {e}")
        raise HTTPException(status_code=500, detail=f"Source tracking operation failed: {str(e)}")


@router.get("/health")
async def enhanced_report_health():
    """Health check for enhanced report service."""
    try:
        orchestrator = get_enhanced_report_orchestrator()
        
        return {
            "service": "enhanced_report",
            "status": "healthy",
            "features": [
                "comprehensive_source_tracking",
                "interactive_tooltips",
                "detailed_calculations",
                "source_references",
                "visualization_tooltips",
                "session_management"
            ],
            "capabilities": {
                "report_types": ["comprehensive", "sentiment", "business", "technical"],
                "visualization_types": ["interactive", "static", "dashboard"],
                "output_formats": ["markdown", "html", "json"],
                "tooltip_features": ["source_references", "calculations", "confidence_scores"]
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


@router.get("/capabilities")
async def get_enhanced_report_capabilities():
    """Get enhanced report capabilities and features."""
    try:
        return {
            "service": "enhanced_report",
            "version": "2.0.0",
            "features": {
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
                "POST /enhanced-report/generate - Generate enhanced report",
                "POST /enhanced-report/visualization - Generate visualization with tooltips",
                "POST /enhanced-report/source-tracking - Manage source tracking",
                "GET /enhanced-report/health - Health check",
                "GET /enhanced-report/capabilities - Get capabilities"
            ],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting capabilities: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get capabilities: {str(e)}")


@router.get("/examples")
async def get_enhanced_report_examples():
    """Get examples of enhanced report usage."""
    try:
        return {
            "service": "enhanced_report",
            "examples": {
                "basic_report": {
                    "description": "Generate a basic enhanced report",
                    "request": {
                        "content": "Sample content for analysis",
                        "report_type": "comprehensive",
                        "include_tooltips": True,
                        "include_source_references": True,
                        "include_calculations": True
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
        
    except Exception as e:
        logger.error(f"Error getting examples: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get examples: {str(e)}")
