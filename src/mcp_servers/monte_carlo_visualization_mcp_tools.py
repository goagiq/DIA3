"""
Monte Carlo Visualization MCP Tools - Phase 6

This module provides MCP tools for Monte Carlo simulation visualizations,
including real-time dashboards, interactive controls, and DoD/IC specific visualizations.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from src.core.monte_carlo.visualization import (
    MonteCarloVisualization,
    VisualizationConfig,
    SecurityLevel,
    create_monte_carlo_visualization
)
from src.core.monte_carlo.engine import MonteCarloEngine


# Global visualization instance
visualization_instance: Optional[MonteCarloVisualization] = None


async def get_visualization_instance() -> MonteCarloVisualization:
    """Get or create visualization instance."""
    global visualization_instance
    
    if visualization_instance is None:
        engine = MonteCarloEngine()
        config = VisualizationConfig()
        visualization_instance = await create_monte_carlo_visualization(engine, config)
    
    return visualization_instance


def get_monte_carlo_visualization_mcp_tools():
    """Get Monte Carlo visualization MCP tools."""
    
    async def monte_carlo_visualization_health_check_tool() -> Dict[str, Any]:
        """Health check for Monte Carlo visualization service."""
        try:
            viz = await get_visualization_instance()
            status = await viz.get_visualization_status()
            
            return {
                "status": "healthy",
                "service": "monte_carlo_visualization",
                "timestamp": datetime.now().isoformat(),
                "active_streams": status.get("active_streams", 0),
                "cached_visualizations": status.get("cached_visualizations", 0)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def monte_carlo_create_distribution_plot_tool(
        data: List[float],
        title: str = "Distribution Plot",
        x_label: str = "Value",
        y_label: str = "Frequency",
        show_stats: bool = True,
        theme: str = "plotly_white",
        height: int = 600,
        width: int = 800,
        security_level: str = "UNCLASSIFIED"
    ) -> Dict[str, Any]:
        """Create an interactive distribution plot."""
        try:
            viz = await get_visualization_instance()
            
            # Update config
            viz.config.theme = theme
            viz.config.height = height
            viz.config.width = width
            viz.config.security_level = SecurityLevel(security_level)
            
            result = await viz.create_distribution_plot(
                data=data,
                title=title,
                x_label=x_label,
                y_label=y_label,
                show_stats=show_stats
            )
            
            if "error" in result:
                return {"error": result["error"]}
            
            return {
                "success": True,
                "visualization_type": "distribution_plot",
                "data": result["data"],
                "metadata": result["metadata"]
            }
            
        except Exception as e:
            return {"error": f"Error creating distribution plot: {str(e)}"}
    
    async def monte_carlo_create_correlation_matrix_tool(
        correlation_matrix: List[List[float]],
        variable_names: Optional[List[str]] = None,
        title: str = "Correlation Matrix",
        theme: str = "plotly_white",
        height: int = 600,
        width: int = 800,
        security_level: str = "UNCLASSIFIED"
    ) -> Dict[str, Any]:
        """Create an interactive correlation matrix heatmap."""
        try:
            viz = await get_visualization_instance()
            
            # Update config
            viz.config.theme = theme
            viz.config.height = height
            viz.config.width = width
            viz.config.security_level = SecurityLevel(security_level)
            
            result = await viz.create_correlation_matrix(
                correlation_matrix=correlation_matrix,
                variable_names=variable_names,
                title=title
            )
            
            if "error" in result:
                return {"error": result["error"]}
            
            return {
                "success": True,
                "visualization_type": "correlation_matrix",
                "data": result["data"],
                "metadata": result["metadata"]
            }
            
        except Exception as e:
            return {"error": f"Error creating correlation matrix: {str(e)}"}
    
    async def monte_carlo_create_scenario_comparison_tool(
        scenario_results: Dict[str, List[float]],
        title: str = "Scenario Comparison",
        metric_name: str = "Value",
        theme: str = "plotly_white",
        height: int = 600,
        width: int = 800,
        security_level: str = "UNCLASSIFIED"
    ) -> Dict[str, Any]:
        """Create a scenario comparison chart."""
        try:
            viz = await get_visualization_instance()
            
            # Update config
            viz.config.theme = theme
            viz.config.height = height
            viz.config.width = width
            viz.config.security_level = SecurityLevel(security_level)
            
            result = await viz.create_scenario_comparison(
                scenario_results=scenario_results,
                title=title,
                metric_name=metric_name
            )
            
            if "error" in result:
                return {"error": result["error"]}
            
            return {
                "success": True,
                "visualization_type": "scenario_comparison",
                "data": result["data"],
                "metadata": result["metadata"]
            }
            
        except Exception as e:
            return {"error": f"Error creating scenario comparison: {str(e)}"}
    
    async def monte_carlo_create_risk_dashboard_tool(
        risk_metrics: Dict[str, float],
        title: str = "Risk Assessment Dashboard",
        theme: str = "plotly_white",
        height: int = 600,
        width: int = 800,
        security_level: str = "UNCLASSIFIED"
    ) -> Dict[str, Any]:
        """Create a comprehensive risk assessment dashboard."""
        try:
            viz = await get_visualization_instance()
            
            # Update config
            viz.config.theme = theme
            viz.config.height = height
            viz.config.width = width
            viz.config.security_level = SecurityLevel(security_level)
            
            result = await viz.create_risk_dashboard(
                risk_metrics=risk_metrics,
                title=title
            )
            
            if "error" in result:
                return {"error": result["error"]}
            
            return {
                "success": True,
                "visualization_type": "risk_dashboard",
                "data": result["data"],
                "metadata": result["metadata"]
            }
            
        except Exception as e:
            return {"error": f"Error creating risk dashboard: {str(e)}"}
    
    async def monte_carlo_create_threat_assessment_tool(
        threat_data: Dict[str, Any],
        title: str = "Threat Assessment Visualization",
        theme: str = "plotly_white",
        height: int = 600,
        width: int = 800,
        security_level: str = "UNCLASSIFIED"
    ) -> Dict[str, Any]:
        """Create DoD/IC specific threat assessment visualization."""
        try:
            viz = await get_visualization_instance()
            
            # Update config
            viz.config.theme = theme
            viz.config.height = height
            viz.config.width = width
            viz.config.security_level = SecurityLevel(security_level)
            
            result = await viz.create_threat_assessment_visualization(
                threat_data=threat_data,
                title=title
            )
            
            if "error" in result:
                return {"error": result["error"]}
            
            return {
                "success": True,
                "visualization_type": "threat_assessment",
                "data": result["data"],
                "metadata": result["metadata"]
            }
            
        except Exception as e:
            return {"error": f"Error creating threat assessment: {str(e)}"}
    
    async def monte_carlo_create_real_time_dashboard_tool(
        simulation_id: str,
        update_interval: float = 1.0,
        theme: str = "plotly_white",
        height: int = 600,
        width: int = 800,
        security_level: str = "UNCLASSIFIED"
    ) -> Dict[str, Any]:
        """Create a real-time streaming dashboard."""
        try:
            viz = await get_visualization_instance()
            
            # Update config
            viz.config.theme = theme
            viz.config.height = height
            viz.config.width = width
            viz.config.security_level = SecurityLevel(security_level)
            
            result = await viz.create_real_time_dashboard(
                simulation_id=simulation_id,
                update_interval=update_interval
            )
            
            if "error" in result:
                return {"error": result["error"]}
            
            return {
                "success": True,
                "visualization_type": "real_time_dashboard",
                "data": result,
                "metadata": result.get("metadata", {})
            }
            
        except Exception as e:
            return {"error": f"Error creating real-time dashboard: {str(e)}"}
    
    async def monte_carlo_export_visualization_tool(
        visualization_data: Dict[str, Any],
        format: str = "html",
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Export visualization to various formats."""
        try:
            viz = await get_visualization_instance()
            
            result = await viz.export_visualization(
                visualization_data=visualization_data,
                format=format,
                filename=filename
            )
            
            if "error" in result:
                return {"error": result["error"]}
            
            return {
                "success": True,
                "export_info": result,
                "format": format,
                "filename": result.get("filename")
            }
            
        except Exception as e:
            return {"error": f"Error exporting visualization: {str(e)}"}
    
    async def monte_carlo_stop_real_time_dashboard_tool(simulation_id: str) -> Dict[str, Any]:
        """Stop a real-time dashboard stream."""
        try:
            viz = await get_visualization_instance()
            
            result = await viz.stop_real_time_dashboard(simulation_id)
            
            if "error" in result:
                return {"error": result["error"]}
            
            return {
                "success": True,
                "status": result.get("status"),
                "message": result.get("message")
            }
            
        except Exception as e:
            return {"error": f"Error stopping real-time dashboard: {str(e)}"}
    
    async def monte_carlo_get_visualization_status_tool() -> Dict[str, Any]:
        """Get status of all active visualizations."""
        try:
            viz = await get_visualization_instance()
            
            result = await viz.get_visualization_status()
            
            if "error" in result:
                return {"error": result["error"]}
            
            return {
                "success": True,
                "status": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Error getting visualization status: {str(e)}"}
    
    async def monte_carlo_list_visualization_types_tool() -> Dict[str, Any]:
        """Get list of available visualization types."""
        try:
            from src.core.monte_carlo.visualization import VisualizationType
            
            return {
                "success": True,
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
            
        except Exception as e:
            return {"error": f"Error listing visualization types: {str(e)}"}
    
    return {
        "monte_carlo_visualization_health_check": {
            "name": "monte_carlo_visualization_health_check",
            "description": "Health check for Monte Carlo visualization service",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        "monte_carlo_create_distribution_plot": {
            "name": "monte_carlo_create_distribution_plot",
            "description": "Create an interactive distribution plot with statistical information",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Simulation results data"
                    },
                    "title": {
                        "type": "string",
                        "description": "Plot title",
                        "default": "Distribution Plot"
                    },
                    "x_label": {
                        "type": "string",
                        "description": "X-axis label",
                        "default": "Value"
                    },
                    "y_label": {
                        "type": "string",
                        "description": "Y-axis label",
                        "default": "Frequency"
                    },
                    "show_stats": {
                        "type": "boolean",
                        "description": "Show statistical information",
                        "default": True
                    },
                    "theme": {
                        "type": "string",
                        "description": "Visualization theme",
                        "default": "plotly_white"
                    },
                    "height": {
                        "type": "integer",
                        "description": "Visualization height",
                        "default": 600
                    },
                    "width": {
                        "type": "integer",
                        "description": "Visualization width",
                        "default": 800
                    },
                    "security_level": {
                        "type": "string",
                        "description": "Security classification level",
                        "default": "UNCLASSIFIED"
                    }
                },
                "required": ["data"]
            }
        },
        "monte_carlo_create_correlation_matrix": {
            "name": "monte_carlo_create_correlation_matrix",
            "description": "Create an interactive correlation matrix heatmap",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "correlation_matrix": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "number"}
                        },
                        "description": "Correlation matrix data"
                    },
                    "variable_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Variable names"
                    },
                    "title": {
                        "type": "string",
                        "description": "Plot title",
                        "default": "Correlation Matrix"
                    },
                    "theme": {
                        "type": "string",
                        "description": "Visualization theme",
                        "default": "plotly_white"
                    },
                    "height": {
                        "type": "integer",
                        "description": "Visualization height",
                        "default": 600
                    },
                    "width": {
                        "type": "integer",
                        "description": "Visualization width",
                        "default": 800
                    },
                    "security_level": {
                        "type": "string",
                        "description": "Security classification level",
                        "default": "UNCLASSIFIED"
                    }
                },
                "required": ["correlation_matrix"]
            }
        },
        "monte_carlo_create_scenario_comparison": {
            "name": "monte_carlo_create_scenario_comparison",
            "description": "Create a scenario comparison chart",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "scenario_results": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "array",
                            "items": {"type": "number"}
                        },
                        "description": "Scenario results data"
                    },
                    "title": {
                        "type": "string",
                        "description": "Plot title",
                        "default": "Scenario Comparison"
                    },
                    "metric_name": {
                        "type": "string",
                        "description": "Metric name for comparison",
                        "default": "Value"
                    },
                    "theme": {
                        "type": "string",
                        "description": "Visualization theme",
                        "default": "plotly_white"
                    },
                    "height": {
                        "type": "integer",
                        "description": "Visualization height",
                        "default": 600
                    },
                    "width": {
                        "type": "integer",
                        "description": "Visualization width",
                        "default": 800
                    },
                    "security_level": {
                        "type": "string",
                        "description": "Security classification level",
                        "default": "UNCLASSIFIED"
                    }
                },
                "required": ["scenario_results"]
            }
        },
        "monte_carlo_create_risk_dashboard": {
            "name": "monte_carlo_create_risk_dashboard",
            "description": "Create a comprehensive risk assessment dashboard",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "risk_metrics": {
                        "type": "object",
                        "additionalProperties": {"type": "number"},
                        "description": "Risk metrics data"
                    },
                    "title": {
                        "type": "string",
                        "description": "Dashboard title",
                        "default": "Risk Assessment Dashboard"
                    },
                    "theme": {
                        "type": "string",
                        "description": "Visualization theme",
                        "default": "plotly_white"
                    },
                    "height": {
                        "type": "integer",
                        "description": "Visualization height",
                        "default": 600
                    },
                    "width": {
                        "type": "integer",
                        "description": "Visualization width",
                        "default": 800
                    },
                    "security_level": {
                        "type": "string",
                        "description": "Security classification level",
                        "default": "UNCLASSIFIED"
                    }
                },
                "required": ["risk_metrics"]
            }
        },
        "monte_carlo_create_threat_assessment": {
            "name": "monte_carlo_create_threat_assessment",
            "description": "Create DoD/IC specific threat assessment visualization",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "threat_data": {
                        "type": "object",
                        "description": "Threat assessment data"
                    },
                    "title": {
                        "type": "string",
                        "description": "Visualization title",
                        "default": "Threat Assessment Visualization"
                    },
                    "theme": {
                        "type": "string",
                        "description": "Visualization theme",
                        "default": "plotly_white"
                    },
                    "height": {
                        "type": "integer",
                        "description": "Visualization height",
                        "default": 600
                    },
                    "width": {
                        "type": "integer",
                        "description": "Visualization width",
                        "default": 800
                    },
                    "security_level": {
                        "type": "string",
                        "description": "Security classification level",
                        "default": "UNCLASSIFIED"
                    }
                },
                "required": ["threat_data"]
            }
        },
        "monte_carlo_create_real_time_dashboard": {
            "name": "monte_carlo_create_real_time_dashboard",
            "description": "Create a real-time streaming dashboard for live simulation monitoring",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "simulation_id": {
                        "type": "string",
                        "description": "Simulation ID to monitor"
                    },
                    "update_interval": {
                        "type": "number",
                        "description": "Update interval in seconds",
                        "default": 1.0
                    },
                    "theme": {
                        "type": "string",
                        "description": "Visualization theme",
                        "default": "plotly_white"
                    },
                    "height": {
                        "type": "integer",
                        "description": "Visualization height",
                        "default": 600
                    },
                    "width": {
                        "type": "integer",
                        "description": "Visualization width",
                        "default": 800
                    },
                    "security_level": {
                        "type": "string",
                        "description": "Security classification level",
                        "default": "UNCLASSIFIED"
                    }
                },
                "required": ["simulation_id"]
            }
        },
        "monte_carlo_export_visualization": {
            "name": "monte_carlo_export_visualization",
            "description": "Export visualization to various formats (html, png, svg, json)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "visualization_data": {
                        "type": "object",
                        "description": "Visualization data to export"
                    },
                    "format": {
                        "type": "string",
                        "description": "Export format (html, png, svg, json)",
                        "default": "html"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Optional filename for export"
                    }
                },
                "required": ["visualization_data"]
            }
        },
        "monte_carlo_stop_real_time_dashboard": {
            "name": "monte_carlo_stop_real_time_dashboard",
            "description": "Stop a real-time dashboard stream",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "simulation_id": {
                        "type": "string",
                        "description": "ID of the simulation to stop streaming"
                    }
                },
                "required": ["simulation_id"]
            }
        },
        "monte_carlo_get_visualization_status": {
            "name": "monte_carlo_get_visualization_status",
            "description": "Get status of all active visualizations",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        "monte_carlo_list_visualization_types": {
            "name": "monte_carlo_list_visualization_types",
            "description": "Get list of available visualization types",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }, {
        "monte_carlo_visualization_health_check": monte_carlo_visualization_health_check_tool,
        "monte_carlo_create_distribution_plot": monte_carlo_create_distribution_plot_tool,
        "monte_carlo_create_correlation_matrix": monte_carlo_create_correlation_matrix_tool,
        "monte_carlo_create_scenario_comparison": monte_carlo_create_scenario_comparison_tool,
        "monte_carlo_create_risk_dashboard": monte_carlo_create_risk_dashboard_tool,
        "monte_carlo_create_threat_assessment": monte_carlo_create_threat_assessment_tool,
        "monte_carlo_create_real_time_dashboard": monte_carlo_create_real_time_dashboard_tool,
        "monte_carlo_export_visualization": monte_carlo_export_visualization_tool,
        "monte_carlo_stop_real_time_dashboard": monte_carlo_stop_real_time_dashboard_tool,
        "monte_carlo_get_visualization_status": monte_carlo_get_visualization_status_tool,
        "monte_carlo_list_visualization_types": monte_carlo_list_visualization_types_tool
    }
