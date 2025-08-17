"""
Monte Carlo Visualization API Routes - Phase 6

This module provides RESTful API endpoints for Monte Carlo simulation visualizations,
including real-time dashboards, interactive controls, and DoD/IC specific visualizations.
"""

from typing import Dict, List, Optional, Any, Union
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio
import json

from src.core.monte_carlo.visualization import (
    MonteCarloVisualization, 
    VisualizationConfig, 
    SecurityLevel,
    create_monte_carlo_visualization
)
from src.core.monte_carlo.engine import MonteCarloEngine
from src.core.monte_carlo.config import MonteCarloConfig

router = APIRouter(prefix="/api/v1/monte-carlo/visualization", tags=["Monte Carlo Visualization"])

# Global visualization instance
visualization_instance: Optional[MonteCarloVisualization] = None


class VisualizationRequest(BaseModel):
    """Base request model for visualizations."""
    title: Optional[str] = Field(None, description="Visualization title")
    security_level: SecurityLevel = Field(SecurityLevel.UNCLASSIFIED, description="Security classification level")
    theme: str = Field("plotly_white", description="Visualization theme")
    height: int = Field(600, description="Visualization height")
    width: int = Field(800, description="Visualization width")


class DistributionPlotRequest(VisualizationRequest):
    """Request model for distribution plots."""
    data: List[float] = Field(..., description="Simulation results data")
    x_label: str = Field("Value", description="X-axis label")
    y_label: str = Field("Frequency", description="Y-axis label")
    show_stats: bool = Field(True, description="Show statistical information")


class CorrelationMatrixRequest(VisualizationRequest):
    """Request model for correlation matrices."""
    correlation_matrix: List[List[float]] = Field(..., description="Correlation matrix data")
    variable_names: Optional[List[str]] = Field(None, description="Variable names")


class ScenarioComparisonRequest(VisualizationRequest):
    """Request model for scenario comparisons."""
    scenario_results: Dict[str, List[float]] = Field(..., description="Scenario results data")
    metric_name: str = Field("Value", description="Metric name for comparison")


class RiskDashboardRequest(VisualizationRequest):
    """Request model for risk dashboards."""
    risk_metrics: Dict[str, float] = Field(..., description="Risk metrics data")


class ThreatAssessmentRequest(VisualizationRequest):
    """Request model for threat assessment visualizations."""
    threat_data: Dict[str, Any] = Field(..., description="Threat assessment data")


class RealTimeDashboardRequest(VisualizationRequest):
    """Request model for real-time dashboards."""
    simulation_id: str = Field(..., description="Simulation ID to monitor")
    update_interval: float = Field(1.0, description="Update interval in seconds")


class ExportRequest(BaseModel):
    """Request model for visualization export."""
    visualization_data: Dict[str, Any] = Field(..., description="Visualization data to export")
    format: str = Field("html", description="Export format (html, png, svg, json)")
    filename: Optional[str] = Field(None, description="Optional filename")


class VisualizationResponse(BaseModel):
    """Response model for visualizations."""
    success: bool = Field(..., description="Success status")
    data: Optional[Dict[str, Any]] = Field(None, description="Visualization data")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata")
    error: Optional[str] = Field(None, description="Error message")


async def get_visualization_instance() -> MonteCarloVisualization:
    """Get or create visualization instance."""
    global visualization_instance
    
    if visualization_instance is None:
        engine = MonteCarloEngine()
        config = VisualizationConfig()
        visualization_instance = await create_monte_carlo_visualization(engine, config)
    
    return visualization_instance


@router.post("/distribution-plot", response_model=VisualizationResponse)
async def create_distribution_plot(request: DistributionPlotRequest):
    """
    Create an interactive distribution plot.
    
    Args:
        request: Distribution plot request data
        
    Returns:
        Visualization response with plot data
    """
    try:
        viz = await get_visualization_instance()
        
        # Update config based on request
        viz.config.theme = request.theme
        viz.config.height = request.height
        viz.config.width = request.width
        viz.config.security_level = request.security_level
        
        result = await viz.create_distribution_plot(
            data=request.data,
            title=request.title or "Distribution Plot",
            x_label=request.x_label,
            y_label=request.y_label,
            show_stats=request.show_stats
        )
        
        if "error" in result:
            return VisualizationResponse(
                success=False,
                error=result["error"]
            )
        
        return VisualizationResponse(
            success=True,
            data=result["data"],
            metadata=result["metadata"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating distribution plot: {str(e)}")


@router.post("/correlation-matrix", response_model=VisualizationResponse)
async def create_correlation_matrix(request: CorrelationMatrixRequest):
    """
    Create an interactive correlation matrix heatmap.
    
    Args:
        request: Correlation matrix request data
        
    Returns:
        Visualization response with matrix data
    """
    try:
        viz = await get_visualization_instance()
        
        # Update config based on request
        viz.config.theme = request.theme
        viz.config.height = request.height
        viz.config.width = request.width
        viz.config.security_level = request.security_level
        
        result = await viz.create_correlation_matrix(
            correlation_matrix=request.correlation_matrix,
            variable_names=request.variable_names,
            title=request.title or "Correlation Matrix"
        )
        
        if "error" in result:
            return VisualizationResponse(
                success=False,
                error=result["error"]
            )
        
        return VisualizationResponse(
            success=True,
            data=result["data"],
            metadata=result["metadata"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating correlation matrix: {str(e)}")


@router.post("/scenario-comparison", response_model=VisualizationResponse)
async def create_scenario_comparison(request: ScenarioComparisonRequest):
    """
    Create a scenario comparison chart.
    
    Args:
        request: Scenario comparison request data
        
    Returns:
        Visualization response with comparison data
    """
    try:
        viz = await get_visualization_instance()
        
        # Update config based on request
        viz.config.theme = request.theme
        viz.config.height = request.height
        viz.config.width = request.width
        viz.config.security_level = request.security_level
        
        result = await viz.create_scenario_comparison(
            scenario_results=request.scenario_results,
            title=request.title or "Scenario Comparison",
            metric_name=request.metric_name
        )
        
        if "error" in result:
            return VisualizationResponse(
                success=False,
                error=result["error"]
            )
        
        return VisualizationResponse(
            success=True,
            data=result["data"],
            metadata=result["metadata"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating scenario comparison: {str(e)}")


@router.post("/risk-dashboard", response_model=VisualizationResponse)
async def create_risk_dashboard(request: RiskDashboardRequest):
    """
    Create a comprehensive risk assessment dashboard.
    
    Args:
        request: Risk dashboard request data
        
    Returns:
        Visualization response with dashboard data
    """
    try:
        viz = await get_visualization_instance()
        
        # Update config based on request
        viz.config.theme = request.theme
        viz.config.height = request.height
        viz.config.width = request.width
        viz.config.security_level = request.security_level
        
        result = await viz.create_risk_dashboard(
            risk_metrics=request.risk_metrics,
            title=request.title or "Risk Assessment Dashboard"
        )
        
        if "error" in result:
            return VisualizationResponse(
                success=False,
                error=result["error"]
            )
        
        return VisualizationResponse(
            success=True,
            data=result["data"],
            metadata=result["metadata"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating risk dashboard: {str(e)}")


@router.post("/threat-assessment", response_model=VisualizationResponse)
async def create_threat_assessment(request: ThreatAssessmentRequest):
    """
    Create DoD/IC specific threat assessment visualization.
    
    Args:
        request: Threat assessment request data
        
    Returns:
        Visualization response with threat assessment data
    """
    try:
        viz = await get_visualization_instance()
        
        # Update config based on request
        viz.config.theme = request.theme
        viz.config.height = request.height
        viz.config.width = request.width
        viz.config.security_level = request.security_level
        
        result = await viz.create_threat_assessment_visualization(
            threat_data=request.threat_data,
            title=request.title or "Threat Assessment Visualization"
        )
        
        if "error" in result:
            return VisualizationResponse(
                success=False,
                error=result["error"]
            )
        
        return VisualizationResponse(
            success=True,
            data=result["data"],
            metadata=result["metadata"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating threat assessment: {str(e)}")


@router.post("/real-time-dashboard", response_model=VisualizationResponse)
async def create_real_time_dashboard(request: RealTimeDashboardRequest):
    """
    Create a real-time streaming dashboard.
    
    Args:
        request: Real-time dashboard request data
        
    Returns:
        Visualization response with dashboard configuration
    """
    try:
        viz = await get_visualization_instance()
        
        # Update config based on request
        viz.config.theme = request.theme
        viz.config.height = request.height
        viz.config.width = request.width
        viz.config.security_level = request.security_level
        
        result = await viz.create_real_time_dashboard(
            simulation_id=request.simulation_id,
            update_interval=request.update_interval
        )
        
        if "error" in result:
            return VisualizationResponse(
                success=False,
                error=result["error"]
            )
        
        return VisualizationResponse(
            success=True,
            data=result,
            metadata=result.get("metadata", {})
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating real-time dashboard: {str(e)}")


@router.post("/export", response_model=VisualizationResponse)
async def export_visualization(request: ExportRequest):
    """
    Export visualization to various formats.
    
    Args:
        request: Export request data
        
    Returns:
        Visualization response with export information
    """
    try:
        viz = await get_visualization_instance()
        
        result = await viz.export_visualization(
            visualization_data=request.visualization_data,
            format=request.format,
            filename=request.filename
        )
        
        if "error" in result:
            return VisualizationResponse(
                success=False,
                error=result["error"]
            )
        
        return VisualizationResponse(
            success=True,
            data=result,
            metadata=result.get("metadata", {})
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting visualization: {str(e)}")


@router.delete("/real-time-dashboard/{simulation_id}")
async def stop_real_time_dashboard(simulation_id: str):
    """
    Stop a real-time dashboard stream.
    
    Args:
        simulation_id: ID of the simulation to stop streaming
        
    Returns:
        Success response
    """
    try:
        viz = await get_visualization_instance()
        
        result = await viz.stop_real_time_dashboard(simulation_id)
        
        if "error" in result:
            return VisualizationResponse(
                success=False,
                error=result["error"]
            )
        
        return VisualizationResponse(
            success=True,
            data=result,
            metadata={"simulation_id": simulation_id}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping real-time dashboard: {str(e)}")


@router.get("/status")
async def get_visualization_status():
    """
    Get status of all active visualizations.
    
    Returns:
        Visualization status information
    """
    try:
        viz = await get_visualization_instance()
        
        result = await viz.get_visualization_status()
        
        if "error" in result:
            return VisualizationResponse(
                success=False,
                error=result["error"]
            )
        
        return VisualizationResponse(
            success=True,
            data=result,
            metadata={"timestamp": datetime.now().isoformat()}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting visualization status: {str(e)}")


@router.get("/health")
async def visualization_health():
    """
    Health check for visualization service.
    
    Returns:
        Health status
    """
    try:
        viz = await get_visualization_instance()
        
        return {
            "status": "healthy",
            "service": "monte_carlo_visualization",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization service unhealthy: {str(e)}")


@router.get("/available-types")
async def get_available_visualization_types():
    """
    Get list of available visualization types.
    
    Returns:
        List of available visualization types
    """
    from src.core.monte_carlo.visualization import VisualizationType
    
    return {
        "available_types": [viz_type.value for viz_type in VisualizationType],
        "descriptions": {
            "distribution_plot": "Interactive distribution plots with statistical information",
            "correlation_matrix": "Correlation matrix heatmaps",
            "scenario_comparison": "Scenario comparison charts",
            "risk_dashboard": "Comprehensive risk assessment dashboards",
            "time_series": "Time series visualizations",
            "heatmap": "General heatmap visualizations",
            "box_plot": "Box plot visualizations",
            "histogram": "Histogram visualizations",
            "scatter_plot": "Scatter plot visualizations",
            "threat_assessment": "DoD/IC threat assessment visualizations",
            "intelligence_fusion": "Intelligence fusion visualizations",
            "mission_planning": "Mission planning visualizations"
        }
    }
