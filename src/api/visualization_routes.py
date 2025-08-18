"""
Interactive Visualization API Routes
Provides API endpoints for interactive forecasting and prediction charts
with distinct color schemes for historical vs future values.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import json
import logging
from loguru import logger

# Import visualization components
try:
    from src.core.visualization.interactive_forecasting_charts import (
        InteractiveForecastingCharts, 
        MonteCarloVisualizationHelper,
        ChartColors
    )
    from src.core.monte_carlo.visualization_integration import MonteCarloVisualizationIntegration
    VISUALIZATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Visualization components not available: {e}")
    VISUALIZATION_AVAILABLE = False

router = APIRouter(prefix="/api/visualization", tags=["Interactive Visualization"])

# Initialize visualization components
if VISUALIZATION_AVAILABLE:
    visualizer = InteractiveForecastingCharts()
    mc_helper = MonteCarloVisualizationHelper()
    mc_integration = MonteCarloVisualizationIntegration()


class VisualizationRequest(BaseModel):
    """Request model for visualization generation."""
    chart_type: str = Field(..., description="Type of chart to generate")
    title: str = Field(..., description="Chart title")
    data: Dict[str, Any] = Field(..., description="Chart data")
    options: Optional[Dict[str, Any]] = Field(default={}, description="Chart options")


class ForecastTimelineRequest(BaseModel):
    """Request model for forecast timeline charts."""
    historical_data: List[Dict[str, Any]] = Field(..., description="Historical data points")
    forecast_data: List[Dict[str, Any]] = Field(..., description="Forecast data points")
    title: str = Field(default="Forecast Timeline", description="Chart title")
    x_col: str = Field(default="timestamp", description="X-axis column name")
    y_col: str = Field(default="value", description="Y-axis column name")
    confidence_cols: Optional[List[str]] = Field(default=None, description="Confidence interval columns")


class MonteCarloRequest(BaseModel):
    """Request model for Monte Carlo simulation charts."""
    historical_data: List[Dict[str, Any]] = Field(..., description="Historical data points")
    simulation_results: List[List[Dict[str, Any]]] = Field(..., description="Simulation results")
    forecast_periods: int = Field(..., description="Number of forecast periods")
    title: str = Field(default="Monte Carlo Forecast", description="Chart title")


class ScenarioComparisonRequest(BaseModel):
    """Request model for scenario comparison charts."""
    scenarios: List[Dict[str, Any]] = Field(..., description="Scenario data")
    title: str = Field(default="Scenario Comparison", description="Chart title")


class RiskAssessmentRequest(BaseModel):
    """Request model for risk assessment heatmaps."""
    risk_data: List[Dict[str, Any]] = Field(..., description="Risk assessment data")
    title: str = Field(default="Risk Assessment", description="Chart title")
    x_col: str = Field(default="scenario", description="X-axis column name")
    y_col: str = Field(default="time_period", description="Y-axis column name")
    value_col: str = Field(default="risk_score", description="Value column name")


@router.get("/health")
async def health_check():
    """Health check for visualization system."""
    return {
        "status": "healthy",
        "visualization_available": VISUALIZATION_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    }


@router.post("/forecast-timeline")
async def create_forecast_timeline(request: ForecastTimelineRequest):
    """Create an interactive forecast timeline chart."""
    if not VISUALIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Visualization system not available")
    
    try:
        # Convert data to DataFrames
        historical_df = pd.DataFrame(request.historical_data)
        forecast_df = pd.DataFrame(request.forecast_data)
        
        # Create the chart
        fig = visualizer.create_forecast_timeline_chart(
            historical_data=historical_df,
            forecast_data=forecast_df,
            title=request.title,
            x_col=request.x_col,
            y_col=request.y_col,
            confidence_cols=tuple(request.confidence_cols) if request.confidence_cols else None
        )
        
        # Save the chart
        output_dir = Path("Results/api_visualization")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        chart_path = output_dir / f"forecast_timeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        fig.write_html(str(chart_path))
        
        return {
            "success": True,
            "chart_path": str(chart_path),
            "chart_type": "forecast_timeline",
            "title": request.title,
            "historical_points": len(historical_df),
            "forecast_points": len(forecast_df)
        }
        
    except Exception as e:
        logger.error(f"Error creating forecast timeline chart: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating chart: {str(e)}")


@router.post("/monte-carlo-forecast")
async def create_monte_carlo_forecast(request: MonteCarloRequest):
    """Create an interactive Monte Carlo forecast chart."""
    if not VISUALIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Visualization system not available")
    
    try:
        # Convert data to DataFrames
        historical_df = pd.DataFrame(request.historical_data)
        simulation_dfs = [pd.DataFrame(sim_data) for sim_data in request.simulation_results]
        
        # Create the chart
        fig = visualizer.create_monte_carlo_forecast_chart(
            historical_data=historical_df,
            simulation_results=simulation_dfs,
            forecast_periods=request.forecast_periods,
            title=request.title
        )
        
        # Save the chart
        output_dir = Path("Results/api_visualization")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        chart_path = output_dir / f"monte_carlo_forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        fig.write_html(str(chart_path))
        
        return {
            "success": True,
            "chart_path": str(chart_path),
            "chart_type": "monte_carlo_forecast",
            "title": request.title,
            "historical_points": len(historical_df),
            "simulation_paths": len(simulation_dfs),
            "forecast_periods": request.forecast_periods
        }
        
    except Exception as e:
        logger.error(f"Error creating Monte Carlo forecast chart: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating chart: {str(e)}")


@router.post("/scenario-comparison")
async def create_scenario_comparison(request: ScenarioComparisonRequest):
    """Create an interactive scenario comparison chart."""
    if not VISUALIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Visualization system not available")
    
    try:
        # Create the chart
        fig = visualizer.create_scenario_comparison_chart(
            scenarios=request.scenarios,
            title=request.title
        )
        
        # Save the chart
        output_dir = Path("Results/api_visualization")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        chart_path = output_dir / f"scenario_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        fig.write_html(str(chart_path))
        
        return {
            "success": True,
            "chart_path": str(chart_path),
            "chart_type": "scenario_comparison",
            "title": request.title,
            "scenarios": len(request.scenarios)
        }
        
    except Exception as e:
        logger.error(f"Error creating scenario comparison chart: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating chart: {str(e)}")


@router.post("/risk-assessment")
async def create_risk_assessment(request: RiskAssessmentRequest):
    """Create an interactive risk assessment heatmap."""
    if not VISUALIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Visualization system not available")
    
    try:
        # Convert data to DataFrame
        risk_df = pd.DataFrame(request.risk_data)
        
        # Create the chart
        fig = visualizer.create_risk_heatmap(
            risk_data=risk_df,
            x_col=request.x_col,
            y_col=request.y_col,
            value_col=request.value_col,
            title=request.title
        )
        
        # Save the chart
        output_dir = Path("Results/api_visualization")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        chart_path = output_dir / f"risk_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        fig.write_html(str(chart_path))
        
        return {
            "success": True,
            "chart_path": str(chart_path),
            "chart_type": "risk_assessment",
            "title": request.title,
            "data_points": len(risk_df)
        }
        
    except Exception as e:
        logger.error(f"Error creating risk assessment chart: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating chart: {str(e)}")


@router.post("/comprehensive-dashboard")
async def create_comprehensive_dashboard(request: VisualizationRequest):
    """Create a comprehensive dashboard with multiple charts."""
    if not VISUALIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Visualization system not available")
    
    try:
        # Extract chart data from request
        charts_data = request.data.get("charts", [])
        
        if not charts_data:
            raise HTTPException(status_code=400, detail="No charts provided for dashboard")
        
        # Create individual charts
        charts = []
        for chart_info in charts_data:
            chart_type = chart_info.get("type")
            chart_title = chart_info.get("title", "Chart")
            chart_data = chart_info.get("data", {})
            
            if chart_type == "forecast_timeline":
                historical_df = pd.DataFrame(chart_data.get("historical_data", []))
                forecast_df = pd.DataFrame(chart_data.get("forecast_data", []))
                
                fig = visualizer.create_forecast_timeline_chart(
                    historical_data=historical_df,
                    forecast_data=forecast_df,
                    title=chart_title
                )
                charts.append((chart_title, fig))
                
            elif chart_type == "monte_carlo_forecast":
                historical_df = pd.DataFrame(chart_data.get("historical_data", []))
                simulation_dfs = [pd.DataFrame(sim) for sim in chart_data.get("simulation_results", [])]
                
                fig = visualizer.create_monte_carlo_forecast_chart(
                    historical_data=historical_df,
                    simulation_results=simulation_dfs,
                    forecast_periods=chart_data.get("forecast_periods", 12),
                    title=chart_title
                )
                charts.append((chart_title, fig))
                
            elif chart_type == "scenario_comparison":
                fig = visualizer.create_scenario_comparison_chart(
                    scenarios=chart_data.get("scenarios", []),
                    title=chart_title
                )
                charts.append((chart_title, fig))
                
            elif chart_type == "risk_assessment":
                risk_df = pd.DataFrame(chart_data.get("risk_data", []))
                
                fig = visualizer.create_risk_heatmap(
                    risk_data=risk_df,
                    title=chart_title
                )
                charts.append((chart_title, fig))
        
        # Create comprehensive dashboard
        dashboard_fig = visualizer.create_interactive_dashboard(
            charts=charts,
            title=request.title,
            layout=request.options.get("layout", "grid")
        )
        
        # Save the dashboard
        output_dir = Path("Results/api_visualization")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        dashboard_path = output_dir / f"comprehensive_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        dashboard_fig.write_html(str(dashboard_path))
        
        return {
            "success": True,
            "dashboard_path": str(dashboard_path),
            "chart_type": "comprehensive_dashboard",
            "title": request.title,
            "charts_count": len(charts)
        }
        
    except Exception as e:
        logger.error(f"Error creating comprehensive dashboard: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating dashboard: {str(e)}")


@router.get("/charts/{chart_filename}")
async def get_chart(chart_filename: str):
    """Retrieve a generated chart by filename."""
    chart_path = Path("Results/api_visualization") / chart_filename
    
    if not chart_path.exists():
        raise HTTPException(status_code=404, detail="Chart not found")
    
    return FileResponse(
        path=str(chart_path),
        media_type="text/html",
        filename=chart_filename
    )


@router.get("/list-charts")
async def list_charts():
    """List all available charts."""
    output_dir = Path("Results/api_visualization")
    
    if not output_dir.exists():
        return {"charts": []}
    
    charts = []
    for chart_file in output_dir.glob("*.html"):
        charts.append({
            "filename": chart_file.name,
            "path": str(chart_file),
            "size": chart_file.stat().st_size,
            "created": datetime.fromtimestamp(chart_file.stat().st_ctime).isoformat()
        })
    
    return {
        "charts": charts,
        "total_count": len(charts)
    }


@router.delete("/charts/{chart_filename}")
async def delete_chart(chart_filename: str):
    """Delete a generated chart."""
    chart_path = Path("Results/api_visualization") / chart_filename
    
    if not chart_path.exists():
        raise HTTPException(status_code=404, detail="Chart not found")
    
    try:
        chart_path.unlink()
        return {"success": True, "message": f"Chart {chart_filename} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting chart {chart_filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting chart: {str(e)}")


@router.post("/generate-sample-data")
async def generate_sample_data():
    """Generate sample data for testing visualization endpoints."""
    if not VISUALIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Visualization system not available")
    
    try:
        # Generate sample historical data
        dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
        np.random.seed(42)
        
        trend = np.linspace(100, 150, len(dates))
        seasonality = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        noise = np.random.normal(0, 5, len(dates))
        historical_values = trend + seasonality + noise
        
        historical_data = [
            {"timestamp": date.isoformat(), "value": value}
            for date, value in zip(dates, historical_values)
        ]
        
        # Generate sample forecast data
        forecast_dates = pd.date_range(start='2024-01-02', end='2024-12-31', freq='D')
        forecast_trend = np.linspace(150, 200, len(forecast_dates))
        forecast_seasonality = 10 * np.sin(2 * np.pi * np.arange(len(forecast_dates)) / 365.25)
        forecast_noise = np.random.normal(0, 8, len(forecast_dates))
        forecast_values = forecast_trend + forecast_seasonality + forecast_noise
        
        # Add confidence intervals
        confidence_width = 15 + np.random.normal(0, 3, len(forecast_dates))
        lower_bound = forecast_values - confidence_width
        upper_bound = forecast_values + confidence_width
        
        forecast_data = [
            {
                "timestamp": date.isoformat(),
                "value": value,
                "lower_bound": lower,
                "upper_bound": upper
            }
            for date, value, lower, upper in zip(forecast_dates, forecast_values, lower_bound, upper_bound)
        ]
        
        # Generate sample simulation data
        simulation_results = []
        for i in range(5):
            np.random.seed(42 + i)
            sim_values = forecast_values + np.random.normal(0, 10, len(forecast_dates))
            sim_data = [
                {"timestamp": date.isoformat(), "value": value}
                for date, value in zip(forecast_dates, sim_values)
            ]
            simulation_results.append(sim_data)
        
        # Generate sample scenarios
        scenarios = [
            {
                "name": "Baseline",
                "type": "forecast",
                "timeline": [date.isoformat() for date in forecast_dates],
                "values": forecast_values.tolist()
            },
            {
                "name": "Optimistic",
                "type": "forecast",
                "timeline": [date.isoformat() for date in forecast_dates],
                "values": (forecast_values + 20).tolist()
            },
            {
                "name": "Pessimistic",
                "type": "forecast",
                "timeline": [date.isoformat() for date in forecast_dates],
                "values": (forecast_values - 20).tolist()
            },
            {
                "name": "Historical",
                "type": "historical",
                "timeline": [date.isoformat() for date in dates],
                "values": historical_values.tolist()
            }
        ]
        
        # Generate sample risk data
        risk_scenarios = ['Baseline', 'Optimistic', 'Pessimistic', 'Market Crash', 'Technology Breakthrough']
        time_periods = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025']
        
        np.random.seed(42)
        risk_data = []
        for i, period in enumerate(time_periods):
            for j, scenario in enumerate(risk_scenarios):
                risk_data.append({
                    "time_period": period,
                    "scenario": scenario,
                    "risk_score": np.random.uniform(10, 90)
                })
        
        return {
            "success": True,
            "sample_data": {
                "historical_data": historical_data,
                "forecast_data": forecast_data,
                "simulation_results": simulation_results,
                "scenarios": scenarios,
                "risk_data": risk_data
            },
            "data_info": {
                "historical_points": len(historical_data),
                "forecast_points": len(forecast_data),
                "simulation_paths": len(simulation_results),
                "scenarios": len(scenarios),
                "risk_data_points": len(risk_data)
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating sample data: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating sample data: {str(e)}")


@router.get("/color-scheme")
async def get_color_scheme():
    """Get the current color scheme configuration."""
    if not VISUALIZATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Visualization system not available")
    
    colors = ChartColors()
    
    return {
        "historical_colors": {
            "line": colors.historical_line,
            "marker": colors.historical_marker,
            "fill": colors.historical_fill
        },
        "future_colors": {
            "line": colors.future_line,
            "marker": colors.future_marker,
            "fill": colors.future_fill
        },
        "confidence_colors": {
            "upper": colors.confidence_upper,
            "lower": colors.confidence_lower,
            "fill": colors.confidence_fill
        },
        "scenario_colors": colors.scenario_colors
    }
