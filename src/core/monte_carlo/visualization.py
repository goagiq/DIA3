"""
Monte Carlo Simulation Visualization Module - Phase 6

This module provides interactive visualizations for Monte Carlo simulation results,
including real-time dashboards, distribution plots, correlation matrices, and
DoD/IC specific visualizations with security compliance.
"""

import asyncio
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
import asyncio
from dataclasses import dataclass
from enum import Enum
import logging

from .engine import MonteCarloEngine
from .analysis import ResultAnalyzer
from .config import MonteCarloConfig

logger = logging.getLogger(__name__)


class VisualizationType(Enum):
    """Types of visualizations available."""
    DISTRIBUTION_PLOT = "distribution_plot"
    CORRELATION_MATRIX = "correlation_matrix"
    SCENARIO_COMPARISON = "scenario_comparison"
    RISK_DASHBOARD = "risk_dashboard"
    TIME_SERIES = "time_series"
    HEATMAP = "heatmap"
    BOX_PLOT = "box_plot"
    HISTOGRAM = "histogram"
    SCATTER_PLOT = "scatter_plot"
    THREAT_ASSESSMENT = "threat_assessment"
    INTELLIGENCE_FUSION = "intelligence_fusion"
    MISSION_PLANNING = "mission_planning"


class SecurityLevel(Enum):
    """Security classification levels for DoD/IC visualizations."""
    UNCLASSIFIED = "UNCLASSIFIED"
    CONFIDENTIAL = "CONFIDENTIAL"
    SECRET = "SECRET"
    TOP_SECRET = "TOP_SECRET"


@dataclass
class VisualizationConfig:
    """Configuration for visualizations."""
    theme: str = "plotly_white"
    height: int = 600
    width: int = 800
    show_legend: bool = True
    enable_animations: bool = True
    security_level: SecurityLevel = SecurityLevel.UNCLASSIFIED
    include_metadata: bool = True
    real_time_updates: bool = False
    update_interval: float = 1.0  # seconds


class MonteCarloVisualization:
    """
    Interactive visualization engine for Monte Carlo simulation results.
    
    Features:
    - Real-time streaming dashboards
    - Interactive parameter controls
    - DoD/IC specific visualizations
    - Security-compliant data handling
    - Multi-format export capabilities
    """
    
    def __init__(self, engine: MonteCarloEngine, config: Optional[VisualizationConfig] = None):
        self.engine = engine
        self.analysis = ResultAnalyzer()
        self.config = config or VisualizationConfig()
        self.active_streams: Dict[str, asyncio.Task] = {}
        self.cache: Dict[str, Any] = {}
        
    async def create_distribution_plot(
        self, 
        data: Union[List[float], np.ndarray], 
        title: str = "Distribution Plot",
        x_label: str = "Value",
        y_label: str = "Frequency",
        show_stats: bool = True
    ) -> Dict[str, Any]:
        """
        Create an interactive distribution plot with statistical information.
        
        Args:
            data: Simulation results data
            title: Plot title
            x_label: X-axis label
            y_label: Y-axis label
            show_stats: Whether to show statistical information
            
        Returns:
            Dictionary containing plot data and metadata
        """
        try:
            # Convert to numpy array if needed
            if isinstance(data, list):
                data = np.array(data)
            
            # Create histogram
            fig = go.Figure()
            
            # Add histogram trace
            fig.add_trace(go.Histogram(
                x=data,
                nbinsx=50,
                name="Distribution",
                opacity=0.7,
                marker_color='rgb(55, 83, 109)'
            ))
            
            # Add statistical information if requested
            if show_stats:
                mean_val = np.mean(data)
                std_val = np.std(data)
                median_val = np.median(data)
                
                # Add vertical lines for statistics
                fig.add_vline(x=mean_val, line_dash="dash", line_color="red", 
                            annotation_text=f"Mean: {mean_val:.4f}")
                fig.add_vline(x=median_val, line_dash="dash", line_color="green", 
                            annotation_text=f"Median: {median_val:.4f}")
                
                # Add text annotation with statistics
                fig.add_annotation(
                    x=0.02, y=0.98,
                    xref="paper", yref="paper",
                    text=f"Mean: {mean_val:.4f}<br>Std: {std_val:.4f}<br>Median: {median_val:.4f}",
                    showarrow=False,
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="black",
                    borderwidth=1
                )
            
            # Update layout
            fig.update_layout(
                title=title,
                xaxis_title=x_label,
                yaxis_title=y_label,
                template=self.config.theme,
                height=self.config.height,
                width=self.config.width,
                showlegend=self.config.show_legend
            )
            
            return {
                "type": "distribution_plot",
                "data": fig.to_dict(),
                "metadata": {
                    "title": title,
                    "data_points": len(data),
                    "security_level": self.config.security_level.value,
                    "created_at": datetime.now().isoformat(),
                    "statistics": {
                        "mean": float(np.mean(data)),
                        "std": float(np.std(data)),
                        "median": float(np.median(data)),
                        "min": float(np.min(data)),
                        "max": float(np.max(data))
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating distribution plot: {e}")
            return {"error": str(e)}
    
    async def create_correlation_matrix(
        self, 
        correlation_matrix: Union[List[List[float]], np.ndarray],
        variable_names: Optional[List[str]] = None,
        title: str = "Correlation Matrix"
    ) -> Dict[str, Any]:
        """
        Create an interactive correlation matrix heatmap.
        
        Args:
            correlation_matrix: Correlation matrix data
            variable_names: Names of variables
            title: Plot title
            
        Returns:
            Dictionary containing plot data and metadata
        """
        try:
            # Convert to numpy array if needed
            if isinstance(correlation_matrix, list):
                correlation_matrix = np.array(correlation_matrix)
            
            # Create variable names if not provided
            if variable_names is None:
                variable_names = [f"Var_{i+1}" for i in range(correlation_matrix.shape[0])]
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=correlation_matrix,
                x=variable_names,
                y=variable_names,
                colorscale='RdBu',
                zmid=0,
                text=np.round(correlation_matrix, 3),
                texttemplate="%{text}",
                textfont={"size": 10},
                hoverongaps=False
            ))
            
            # Update layout
            fig.update_layout(
                title=title,
                template=self.config.theme,
                height=self.config.height,
                width=self.config.width,
                xaxis_title="Variables",
                yaxis_title="Variables"
            )
            
            return {
                "type": "correlation_matrix",
                "data": fig.to_dict(),
                "metadata": {
                    "title": title,
                    "matrix_size": correlation_matrix.shape[0],
                    "security_level": self.config.security_level.value,
                    "created_at": datetime.now().isoformat(),
                    "variable_names": variable_names
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating correlation matrix: {e}")
            return {"error": str(e)}
    
    async def create_scenario_comparison(
        self, 
        scenario_results: Dict[str, List[float]],
        title: str = "Scenario Comparison",
        metric_name: str = "Value"
    ) -> Dict[str, Any]:
        """
        Create a comparison chart for multiple scenarios.
        
        Args:
            scenario_results: Dictionary of scenario names to results
            title: Plot title
            metric_name: Name of the metric being compared
            
        Returns:
            Dictionary containing plot data and metadata
        """
        try:
            fig = go.Figure()
            
            # Add box plots for each scenario
            for scenario_name, results in scenario_results.items():
                fig.add_trace(go.Box(
                    y=results,
                    name=scenario_name,
                    boxpoints='outliers',
                    jitter=0.3,
                    pointpos=-1.8
                ))
            
            # Update layout
            fig.update_layout(
                title=title,
                yaxis_title=metric_name,
                template=self.config.theme,
                height=self.config.height,
                width=self.config.width,
                showlegend=self.config.show_legend
            )
            
            return {
                "type": "scenario_comparison",
                "data": fig.to_dict(),
                "metadata": {
                    "title": title,
                    "scenarios": list(scenario_results.keys()),
                    "security_level": self.config.security_level.value,
                    "created_at": datetime.now().isoformat(),
                    "total_scenarios": len(scenario_results)
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating scenario comparison: {e}")
            return {"error": str(e)}
    
    async def create_risk_dashboard(
        self, 
        risk_metrics: Dict[str, float],
        title: str = "Risk Assessment Dashboard"
    ) -> Dict[str, Any]:
        """
        Create a comprehensive risk assessment dashboard.
        
        Args:
            risk_metrics: Dictionary of risk metric names to values
            title: Dashboard title
            
        Returns:
            Dictionary containing dashboard data and metadata
        """
        try:
            # Create subplots for different risk components
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=list(risk_metrics.keys()),
                specs=[[{"type": "indicator"}, {"type": "indicator"}],
                       [{"type": "indicator"}, {"type": "indicator"}]]
            )
            
            # Add gauge charts for each risk metric
            positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
            for i, (metric_name, value) in enumerate(risk_metrics.items()):
                if i < len(positions):
                    row, col = positions[i]
                    fig.add_trace(
                        go.Indicator(
                            mode="gauge+number+delta",
                            value=value,
                            title={'text': metric_name},
                            gauge={
                                'axis': {'range': [None, 1]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 0.3], 'color': "lightgray"},
                                    {'range': [0.3, 0.7], 'color': "yellow"},
                                    {'range': [0.7, 1], 'color': "red"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 0.8
                                }
                            }
                        ),
                        row=row, col=col
                    )
            
            # Update layout
            fig.update_layout(
                title=title,
                template=self.config.theme,
                height=self.config.height,
                width=self.config.width
            )
            
            return {
                "type": "risk_dashboard",
                "data": fig.to_dict(),
                "metadata": {
                    "title": title,
                    "risk_metrics": risk_metrics,
                    "security_level": self.config.security_level.value,
                    "created_at": datetime.now().isoformat(),
                    "total_metrics": len(risk_metrics)
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating risk dashboard: {e}")
            return {"error": str(e)}
    
    async def create_threat_assessment_visualization(
        self, 
        threat_data: Dict[str, Any],
        title: str = "Threat Assessment Visualization"
    ) -> Dict[str, Any]:
        """
        Create DoD/IC specific threat assessment visualization.
        
        Args:
            threat_data: Threat assessment data
            title: Visualization title
            
        Returns:
            Dictionary containing visualization data and metadata
        """
        try:
            # Create radar chart for threat capabilities
            if "capabilities" in threat_data:
                categories = list(threat_data["capabilities"].keys())
                values = list(threat_data["capabilities"].values())
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name='Threat Capabilities'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 1]
                        )),
                    showlegend=True,
                    title=title,
                    template=self.config.theme,
                    height=self.config.height,
                    width=self.config.width
                )
                
                return {
                    "type": "threat_assessment",
                    "data": fig.to_dict(),
                    "metadata": {
                        "title": title,
                        "security_level": self.config.security_level.value,
                        "created_at": datetime.now().isoformat(),
                        "threat_level": threat_data.get("threat_level", "UNKNOWN"),
                        "confidence": threat_data.get("confidence", 0.0)
                    }
                }
            
            return {"error": "Invalid threat data format"}
            
        except Exception as e:
            logger.error(f"Error creating threat assessment visualization: {e}")
            return {"error": str(e)}
    
    async def create_real_time_dashboard(
        self, 
        simulation_id: str,
        update_interval: float = 1.0
    ) -> Dict[str, Any]:
        """
        Create a real-time streaming dashboard for live simulation monitoring.
        
        Args:
            simulation_id: ID of the simulation to monitor
            update_interval: Update interval in seconds
            
        Returns:
            Dictionary containing dashboard configuration
        """
        try:
            # Create streaming task
            if simulation_id in self.active_streams:
                self.active_streams[simulation_id].cancel()
            
            stream_task = asyncio.create_task(
                self._stream_simulation_updates(simulation_id, update_interval)
            )
            self.active_streams[simulation_id] = stream_task
            
            return {
                "type": "real_time_dashboard",
                "simulation_id": simulation_id,
                "update_interval": update_interval,
                "status": "active",
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "security_level": self.config.security_level.value,
                    "streaming": True
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating real-time dashboard: {e}")
            return {"error": str(e)}
    
    async def _stream_simulation_updates(
        self, 
        simulation_id: str, 
        update_interval: float
    ):
        """Internal method to stream simulation updates."""
        try:
            while True:
                # Get current simulation status
                status = await self.engine.get_simulation_status(simulation_id)
                
                if status and status.get("status") == "completed":
                    # Simulation completed, stop streaming
                    break
                
                # Emit update (in real implementation, this would use WebSocket)
                logger.info(f"Simulation {simulation_id} update: {status}")
                
                await asyncio.sleep(update_interval)
                
        except asyncio.CancelledError:
            logger.info(f"Streaming cancelled for simulation {simulation_id}")
        except Exception as e:
            logger.error(f"Error in simulation streaming: {e}")
    
    async def export_visualization(
        self, 
        visualization_data: Dict[str, Any], 
        format: str = "html",
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Export visualization to various formats.
        
        Args:
            visualization_data: Visualization data to export
            format: Export format (html, png, svg, json)
            filename: Optional filename for export
            
        Returns:
            Dictionary containing export information
        """
        try:
            if "error" in visualization_data:
                return {"error": "Cannot export visualization with errors"}
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"monte_carlo_viz_{timestamp}"
            
            # Create figure from data
            fig = go.Figure(visualization_data["data"])
            
            # Export based on format
            if format == "html":
                output_path = f"Results/visualizations/{filename}.html"
                fig.write_html(output_path)
            elif format == "png":
                output_path = f"Results/visualizations/{filename}.png"
                fig.write_image(output_path)
            elif format == "svg":
                output_path = f"Results/visualizations/{filename}.svg"
                fig.write_image(output_path)
            elif format == "json":
                output_path = f"Results/visualizations/{filename}.json"
                with open(output_path, 'w') as f:
                    json.dump(visualization_data, f, indent=2)
            else:
                return {"error": f"Unsupported format: {format}"}
            
            return {
                "export_success": True,
                "format": format,
                "filename": filename,
                "output_path": output_path,
                "metadata": visualization_data.get("metadata", {})
            }
            
        except Exception as e:
            logger.error(f"Error exporting visualization: {e}")
            return {"error": str(e)}
    
    async def stop_real_time_dashboard(self, simulation_id: str) -> Dict[str, Any]:
        """
        Stop a real-time dashboard stream.
        
        Args:
            simulation_id: ID of the simulation to stop streaming
            
        Returns:
            Dictionary containing stop status
        """
        try:
            if simulation_id in self.active_streams:
                self.active_streams[simulation_id].cancel()
                del self.active_streams[simulation_id]
                
                return {
                    "status": "stopped",
                    "simulation_id": simulation_id,
                    "message": "Real-time dashboard stopped successfully"
                }
            else:
                return {
                    "status": "not_found",
                    "simulation_id": simulation_id,
                    "message": "No active stream found for this simulation"
                }
                
        except Exception as e:
            logger.error(f"Error stopping real-time dashboard: {e}")
            return {"error": str(e)}
    
    async def get_visualization_status(self) -> Dict[str, Any]:
        """
        Get status of all active visualizations.
        
        Returns:
            Dictionary containing visualization status
        """
        try:
            return {
                "active_streams": len(self.active_streams),
                "cached_visualizations": len(self.cache),
                "config": {
                    "theme": self.config.theme,
                    "security_level": self.config.security_level.value,
                    "real_time_updates": self.config.real_time_updates
                },
                "status": "healthy"
            }
            
        except Exception as e:
            logger.error(f"Error getting visualization status: {e}")
            return {"error": str(e)}


# Factory function for creating visualizations
async def create_monte_carlo_visualization(
    engine: MonteCarloEngine,
    config: Optional[VisualizationConfig] = None
) -> MonteCarloVisualization:
    """
    Factory function to create a Monte Carlo visualization instance.
    
    Args:
        engine: Monte Carlo engine instance
        config: Optional visualization configuration
        
    Returns:
        MonteCarloVisualization instance
    """
    return MonteCarloVisualization(engine, config)
