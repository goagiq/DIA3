"""
Interactive Visualization MCP Tools
Provides MCP tools for interactive forecasting and prediction charts
with distinct color schemes for historical vs future values.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np
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

# Initialize visualization components
if VISUALIZATION_AVAILABLE:
    visualizer = InteractiveForecastingCharts()
    mc_helper = MonteCarloVisualizationHelper()
    mc_integration = MonteCarloVisualizationIntegration()


class InteractiveVisualizationMCPTools:
    """MCP tools for interactive visualization system."""
    
    def __init__(self):
        self.visualizer = visualizer if VISUALIZATION_AVAILABLE else None
        self.mc_helper = mc_helper if VISUALIZATION_AVAILABLE else None
        self.mc_integration = mc_integration if VISUALIZATION_AVAILABLE else None
        self.output_dir = Path("Results/mcp_visualization")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools."""
        if not VISUALIZATION_AVAILABLE:
            return []
        
        return [
            {
                "name": "create_forecast_timeline_chart",
                "description": "Create an interactive forecast timeline chart with distinct colors for historical vs future data",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "historical_data": {
                            "type": "array",
                            "description": "Historical data points with timestamp and value",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "timestamp": {"type": "string", "format": "date-time"},
                                    "value": {"type": "number"}
                                }
                            }
                        },
                        "forecast_data": {
                            "type": "array",
                            "description": "Forecast data points with timestamp, value, and optional confidence intervals",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "timestamp": {"type": "string", "format": "date-time"},
                                    "value": {"type": "number"},
                                    "lower_bound": {"type": "number"},
                                    "upper_bound": {"type": "number"}
                                }
                            }
                        },
                        "title": {"type": "string", "description": "Chart title"},
                        "x_col": {"type": "string", "default": "timestamp", "description": "X-axis column name"},
                        "y_col": {"type": "string", "default": "value", "description": "Y-axis column name"}
                    },
                    "required": ["historical_data", "forecast_data"]
                }
            },
            {
                "name": "create_monte_carlo_forecast_chart",
                "description": "Create an interactive Monte Carlo forecast chart showing multiple simulation paths",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "historical_data": {
                            "type": "array",
                            "description": "Historical data points",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "timestamp": {"type": "string", "format": "date-time"},
                                    "value": {"type": "number"}
                                }
                            }
                        },
                        "simulation_results": {
                            "type": "array",
                            "description": "List of simulation result arrays",
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "timestamp": {"type": "string", "format": "date-time"},
                                        "value": {"type": "number"}
                                    }
                                }
                            }
                        },
                        "forecast_periods": {"type": "integer", "description": "Number of forecast periods"},
                        "title": {"type": "string", "description": "Chart title"}
                    },
                    "required": ["historical_data", "simulation_results", "forecast_periods"]
                }
            },
            {
                "name": "create_scenario_comparison_chart",
                "description": "Create an interactive scenario comparison chart with multiple future scenarios",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "scenarios": {
                            "type": "array",
                            "description": "List of scenario data",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "type": {"type": "string", "enum": ["historical", "forecast"]},
                                    "timeline": {
                                        "type": "array",
                                        "items": {"type": "string", "format": "date-time"}
                                    },
                                    "values": {
                                        "type": "array",
                                        "items": {"type": "number"}
                                    },
                                    "lower_bound": {
                                        "type": "array",
                                        "items": {"type": "number"}
                                    },
                                    "upper_bound": {
                                        "type": "array",
                                        "items": {"type": "number"}
                                    }
                                },
                                "required": ["name", "type", "timeline", "values"]
                            }
                        },
                        "title": {"type": "string", "description": "Chart title"}
                    },
                    "required": ["scenarios"]
                }
            },
            {
                "name": "create_risk_assessment_heatmap",
                "description": "Create an interactive risk assessment heatmap",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "risk_data": {
                            "type": "array",
                            "description": "Risk assessment data",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "time_period": {"type": "string"},
                                    "scenario": {"type": "string"},
                                    "risk_score": {"type": "number"}
                                }
                            }
                        },
                        "title": {"type": "string", "description": "Chart title"},
                        "x_col": {"type": "string", "default": "scenario", "description": "X-axis column name"},
                        "y_col": {"type": "string", "default": "time_period", "description": "Y-axis column name"},
                        "value_col": {"type": "string", "default": "risk_score", "description": "Value column name"}
                    },
                    "required": ["risk_data"]
                }
            },
            {
                "name": "create_comprehensive_dashboard",
                "description": "Create a comprehensive dashboard with multiple charts",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "charts": {
                            "type": "array",
                            "description": "List of chart configurations",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {"type": "string", "enum": ["forecast_timeline", "monte_carlo_forecast", "scenario_comparison", "risk_assessment"]},
                                    "title": {"type": "string"},
                                    "data": {"type": "object"}
                                }
                            }
                        },
                        "title": {"type": "string", "description": "Dashboard title"},
                        "layout": {"type": "string", "default": "grid", "enum": ["grid", "vertical", "horizontal"]}
                    },
                    "required": ["charts", "title"]
                }
            },
            {
                "name": "generate_sample_visualization_data",
                "description": "Generate sample data for testing visualization tools",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "data_type": {
                            "type": "string",
                            "enum": ["forecast_timeline", "monte_carlo", "scenarios", "risk_assessment", "all"],
                            "default": "all",
                            "description": "Type of sample data to generate"
                        }
                    }
                }
            },
            {
                "name": "get_visualization_color_scheme",
                "description": "Get the current color scheme configuration for visualization charts",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
    
    async def create_forecast_timeline_chart(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create an interactive forecast timeline chart."""
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            # Extract parameters
            historical_data = args.get("historical_data", [])
            forecast_data = args.get("forecast_data", [])
            title = args.get("title", "Forecast Timeline")
            x_col = args.get("x_col", "timestamp")
            y_col = args.get("y_col", "value")
            
            # Convert data to DataFrames
            historical_df = pd.DataFrame(historical_data)
            forecast_df = pd.DataFrame(forecast_data)
            
            # Check for confidence intervals
            confidence_cols = None
            if "lower_bound" in forecast_df.columns and "upper_bound" in forecast_df.columns:
                confidence_cols = ("lower_bound", "upper_bound")
            
            # Create the chart
            fig = self.visualizer.create_forecast_timeline_chart(
                historical_data=historical_df,
                forecast_data=forecast_df,
                title=title,
                x_col=x_col,
                y_col=y_col,
                confidence_cols=confidence_cols
            )
            
            # Save the chart
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            chart_path = self.output_dir / f"forecast_timeline_{timestamp}.html"
            fig.write_html(str(chart_path))
            
            return {
                "success": True,
                "chart_path": str(chart_path),
                "chart_type": "forecast_timeline",
                "title": title,
                "historical_points": len(historical_df),
                "forecast_points": len(forecast_df),
                "has_confidence_intervals": confidence_cols is not None
            }
            
        except Exception as e:
            logger.error(f"Error creating forecast timeline chart: {e}")
            return {"error": f"Error creating chart: {str(e)}"}
    
    async def create_monte_carlo_forecast_chart(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create an interactive Monte Carlo forecast chart."""
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            # Extract parameters
            historical_data = args.get("historical_data", [])
            simulation_results = args.get("simulation_results", [])
            forecast_periods = args.get("forecast_periods", 12)
            title = args.get("title", "Monte Carlo Forecast")
            
            # Convert data to DataFrames
            historical_df = pd.DataFrame(historical_data)
            simulation_dfs = [pd.DataFrame(sim_data) for sim_data in simulation_results]
            
            # Create the chart
            fig = self.visualizer.create_monte_carlo_forecast_chart(
                historical_data=historical_df,
                simulation_results=simulation_dfs,
                forecast_periods=forecast_periods,
                title=title
            )
            
            # Save the chart
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            chart_path = self.output_dir / f"monte_carlo_forecast_{timestamp}.html"
            fig.write_html(str(chart_path))
            
            return {
                "success": True,
                "chart_path": str(chart_path),
                "chart_type": "monte_carlo_forecast",
                "title": title,
                "historical_points": len(historical_df),
                "simulation_paths": len(simulation_dfs),
                "forecast_periods": forecast_periods
            }
            
        except Exception as e:
            logger.error(f"Error creating Monte Carlo forecast chart: {e}")
            return {"error": f"Error creating chart: {str(e)}"}
    
    async def create_scenario_comparison_chart(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create an interactive scenario comparison chart."""
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            # Extract parameters
            scenarios = args.get("scenarios", [])
            title = args.get("title", "Scenario Comparison")
            
            # Create the chart
            fig = self.visualizer.create_scenario_comparison_chart(
                scenarios=scenarios,
                title=title
            )
            
            # Save the chart
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            chart_path = self.output_dir / f"scenario_comparison_{timestamp}.html"
            fig.write_html(str(chart_path))
            
            return {
                "success": True,
                "chart_path": str(chart_path),
                "chart_type": "scenario_comparison",
                "title": title,
                "scenarios": len(scenarios)
            }
            
        except Exception as e:
            logger.error(f"Error creating scenario comparison chart: {e}")
            return {"error": f"Error creating chart: {str(e)}"}
    
    async def create_risk_assessment_heatmap(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create an interactive risk assessment heatmap."""
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            # Extract parameters
            risk_data = args.get("risk_data", [])
            title = args.get("title", "Risk Assessment")
            x_col = args.get("x_col", "scenario")
            y_col = args.get("y_col", "time_period")
            value_col = args.get("value_col", "risk_score")
            
            # Convert data to DataFrame
            risk_df = pd.DataFrame(risk_data)
            
            # Create the chart
            fig = self.visualizer.create_risk_heatmap(
                risk_data=risk_df,
                x_col=x_col,
                y_col=y_col,
                value_col=value_col,
                title=title
            )
            
            # Save the chart
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            chart_path = self.output_dir / f"risk_assessment_{timestamp}.html"
            fig.write_html(str(chart_path))
            
            return {
                "success": True,
                "chart_path": str(chart_path),
                "chart_type": "risk_assessment",
                "title": title,
                "data_points": len(risk_df)
            }
            
        except Exception as e:
            logger.error(f"Error creating risk assessment chart: {e}")
            return {"error": f"Error creating chart: {str(e)}"}
    
    async def create_comprehensive_dashboard(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive dashboard with multiple charts."""
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            # Extract parameters
            charts_data = args.get("charts", [])
            title = args.get("title", "Comprehensive Dashboard")
            layout = args.get("layout", "grid")
            
            if not charts_data:
                return {"error": "No charts provided for dashboard"}
            
            # Create individual charts
            charts = []
            for chart_info in charts_data:
                chart_type = chart_info.get("type")
                chart_title = chart_info.get("title", "Chart")
                chart_data = chart_info.get("data", {})
                
                if chart_type == "forecast_timeline":
                    historical_df = pd.DataFrame(chart_data.get("historical_data", []))
                    forecast_df = pd.DataFrame(chart_data.get("forecast_data", []))
                    
                    fig = self.visualizer.create_forecast_timeline_chart(
                        historical_data=historical_df,
                        forecast_data=forecast_df,
                        title=chart_title
                    )
                    charts.append((chart_title, fig))
                    
                elif chart_type == "monte_carlo_forecast":
                    historical_df = pd.DataFrame(chart_data.get("historical_data", []))
                    simulation_dfs = [pd.DataFrame(sim) for sim in chart_data.get("simulation_results", [])]
                    
                    fig = self.visualizer.create_monte_carlo_forecast_chart(
                        historical_data=historical_df,
                        simulation_results=simulation_dfs,
                        forecast_periods=chart_data.get("forecast_periods", 12),
                        title=chart_title
                    )
                    charts.append((chart_title, fig))
                    
                elif chart_type == "scenario_comparison":
                    fig = self.visualizer.create_scenario_comparison_chart(
                        scenarios=chart_data.get("scenarios", []),
                        title=chart_title
                    )
                    charts.append((chart_title, fig))
                    
                elif chart_type == "risk_assessment":
                    risk_df = pd.DataFrame(chart_data.get("risk_data", []))
                    
                    fig = self.visualizer.create_risk_heatmap(
                        risk_data=risk_df,
                        title=chart_title
                    )
                    charts.append((chart_title, fig))
            
            # Create comprehensive dashboard
            dashboard_fig = self.visualizer.create_interactive_dashboard(
                charts=charts,
                title=title,
                layout=layout
            )
            
            # Save the dashboard
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dashboard_path = self.output_dir / f"comprehensive_dashboard_{timestamp}.html"
            dashboard_fig.write_html(str(dashboard_path))
            
            return {
                "success": True,
                "dashboard_path": str(dashboard_path),
                "chart_type": "comprehensive_dashboard",
                "title": title,
                "charts_count": len(charts),
                "layout": layout
            }
            
        except Exception as e:
            logger.error(f"Error creating comprehensive dashboard: {e}")
            return {"error": f"Error creating dashboard: {str(e)}"}
    
    async def generate_sample_visualization_data(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate sample data for testing visualization tools."""
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            data_type = args.get("data_type", "all")
            
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
            
            # Return requested data
            if data_type == "forecast_timeline":
                return {
                    "success": True,
                    "data": {
                        "historical_data": historical_data,
                        "forecast_data": forecast_data
                    }
                }
            elif data_type == "monte_carlo":
                return {
                    "success": True,
                    "data": {
                        "historical_data": historical_data,
                        "simulation_results": simulation_results,
                        "forecast_periods": len(forecast_dates)
                    }
                }
            elif data_type == "scenarios":
                return {
                    "success": True,
                    "data": {
                        "scenarios": scenarios
                    }
                }
            elif data_type == "risk_assessment":
                return {
                    "success": True,
                    "data": {
                        "risk_data": risk_data
                    }
                }
            else:  # all
                return {
                    "success": True,
                    "data": {
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
            return {"error": f"Error generating sample data: {str(e)}"}
    
    async def get_visualization_color_scheme(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get the current color scheme configuration."""
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            colors = ChartColors()
            
            return {
                "success": True,
                "color_scheme": {
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
            }
            
        except Exception as e:
            logger.error(f"Error getting color scheme: {e}")
            return {"error": f"Error getting color scheme: {str(e)}"}


# Create global instance
interactive_visualization_mcp_tools = InteractiveVisualizationMCPTools()
