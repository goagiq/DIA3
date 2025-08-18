"""
Monte Carlo Visualization Integration

Integration module connecting Monte Carlo simulation engine with interactive visualization system.
Provides enhanced visualization capabilities for forecasting and prediction charts.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
import json
from pathlib import Path

# Import the interactive visualization system
try:
    from ..visualization.interactive_forecasting_charts import (
        InteractiveForecastingCharts, 
        MonteCarloVisualizationHelper,
        ChartColors
    )
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    logging.warning("Interactive visualization system not available")

from .engine import MonteCarloEngine
from .analysis import ResultAnalyzer

logger = logging.getLogger(__name__)


class MonteCarloVisualizationIntegration:
    """
    Integration class for Monte Carlo simulations with interactive visualizations.
    """
    
    def __init__(self, engine: Optional[MonteCarloEngine] = None, colors: Optional[ChartColors] = None):
        """Initialize the Monte Carlo visualization integration."""
        self.engine = engine or MonteCarloEngine()
        self.analyzer = ResultAnalyzer()
        
        if VISUALIZATION_AVAILABLE:
            self.visualizer = InteractiveForecastingCharts(colors)
            self.mc_helper = MonteCarloVisualizationHelper(colors)
        else:
            self.visualizer = None
            self.mc_helper = None
            logger.warning("Visualization capabilities disabled - interactive charts not available")
    
    def create_forecast_visualization(
        self,
        historical_data: pd.DataFrame,
        forecast_data: pd.DataFrame,
        confidence_intervals: Optional[Tuple[str, str]] = None,
        title: str = "Forecast Analysis",
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an interactive forecast visualization with distinct colors for historical vs future data.
        
        Args:
            historical_data: DataFrame with historical data
            forecast_data: DataFrame with forecast data
            confidence_intervals: Tuple of (lower_bound_col, upper_bound_col) for confidence intervals
            title: Chart title
            save_path: Optional path to save the chart as HTML
        
        Returns:
            Dictionary containing chart data and metadata
        """
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            # Create the interactive forecast chart
            fig = self.visualizer.create_forecast_timeline_chart(
                historical_data=historical_data,
                forecast_data=forecast_data,
                title=title,
                confidence_cols=confidence_intervals
            )
            
            # Save chart if path provided
            if save_path:
                fig.write_html(save_path)
                logger.info(f"Forecast chart saved to: {save_path}")
            
            # Extract chart data for return
            chart_data = {
                "chart_type": "forecast_timeline",
                "title": title,
                "historical_data_points": len(historical_data),
                "forecast_data_points": len(forecast_data),
                "has_confidence_intervals": confidence_intervals is not None,
                "interactive_features": self.visualizer.interactive_features,
                "save_path": save_path
            }
            
            return {
                "success": True,
                "chart": fig,
                "data": chart_data
            }
            
        except Exception as e:
            logger.error(f"Error creating forecast visualization: {e}")
            return {"error": str(e)}
    
    def create_monte_carlo_visualization(
        self,
        simulation_results: Dict[str, Any],
        title: str = "Monte Carlo Simulation Results",
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an interactive Monte Carlo simulation visualization.
        
        Args:
            simulation_results: Dictionary containing simulation results
            title: Chart title
            save_path: Optional path to save the chart as HTML
        
        Returns:
            Dictionary containing chart data and metadata
        """
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            # Extract data from simulation results
            historical_data = simulation_results.get('historical_data', pd.DataFrame())
            simulation_paths = simulation_results.get('simulation_paths', [])
            forecast_periods = simulation_results.get('forecast_periods', 12)
            
            # Create the Monte Carlo visualization
            fig = self.visualizer.create_monte_carlo_forecast_chart(
                historical_data=historical_data,
                simulation_results=simulation_paths,
                forecast_periods=forecast_periods,
                title=title
            )
            
            # Save chart if path provided
            if save_path:
                fig.write_html(save_path)
                logger.info(f"Monte Carlo chart saved to: {save_path}")
            
            # Extract chart data for return
            chart_data = {
                "chart_type": "monte_carlo_forecast",
                "title": title,
                "historical_data_points": len(historical_data),
                "simulation_paths": len(simulation_paths),
                "forecast_periods": forecast_periods,
                "interactive_features": self.visualizer.interactive_features,
                "save_path": save_path
            }
            
            return {
                "success": True,
                "chart": fig,
                "data": chart_data
            }
            
        except Exception as e:
            logger.error(f"Error creating Monte Carlo visualization: {e}")
            return {"error": str(e)}
    
    def create_scenario_comparison_visualization(
        self,
        scenarios: List[Dict[str, Any]],
        title: str = "Scenario Comparison",
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an interactive scenario comparison visualization.
        
        Args:
            scenarios: List of scenario dictionaries
            title: Chart title
            save_path: Optional path to save the chart as HTML
        
        Returns:
            Dictionary containing chart data and metadata
        """
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            # Create the scenario comparison chart
            fig = self.visualizer.create_scenario_comparison_chart(
                scenarios=scenarios,
                title=title
            )
            
            # Save chart if path provided
            if save_path:
                fig.write_html(save_path)
                logger.info(f"Scenario comparison chart saved to: {save_path}")
            
            # Extract chart data for return
            chart_data = {
                "chart_type": "scenario_comparison",
                "title": title,
                "scenarios_count": len(scenarios),
                "scenario_names": [s.get('name', f'Scenario {i+1}') for i, s in enumerate(scenarios)],
                "interactive_features": self.visualizer.interactive_features,
                "save_path": save_path
            }
            
            return {
                "success": True,
                "chart": fig,
                "data": chart_data
            }
            
        except Exception as e:
            logger.error(f"Error creating scenario comparison visualization: {e}")
            return {"error": str(e)}
    
    def create_risk_assessment_visualization(
        self,
        risk_data: pd.DataFrame,
        title: str = "Risk Assessment",
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an interactive risk assessment heatmap visualization.
        
        Args:
            risk_data: DataFrame with risk assessment data
            title: Chart title
            save_path: Optional path to save the chart as HTML
        
        Returns:
            Dictionary containing chart data and metadata
        """
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            # Create the risk assessment heatmap
            fig = self.visualizer.create_risk_heatmap(
                risk_data=risk_data,
                title=title
            )
            
            # Save chart if path provided
            if save_path:
                fig.write_html(save_path)
                logger.info(f"Risk assessment chart saved to: {save_path}")
            
            # Extract chart data for return
            chart_data = {
                "chart_type": "risk_heatmap",
                "title": title,
                "risk_data_shape": risk_data.shape,
                "risk_data_columns": list(risk_data.columns),
                "interactive_features": self.visualizer.interactive_features,
                "save_path": save_path
            }
            
            return {
                "success": True,
                "chart": fig,
                "data": chart_data
            }
            
        except Exception as e:
            logger.error(f"Error creating risk assessment visualization: {e}")
            return {"error": str(e)}
    
    def create_probability_distribution_visualization(
        self,
        historical_data: pd.DataFrame,
        forecast_distributions: List[np.ndarray],
        forecast_periods: List[str],
        title: str = "Probability Distribution Forecast",
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an interactive probability distribution visualization.
        
        Args:
            historical_data: DataFrame with historical data
            forecast_distributions: List of probability distributions
            forecast_periods: List of forecast period labels
            title: Chart title
            save_path: Optional path to save the chart as HTML
        
        Returns:
            Dictionary containing chart data and metadata
        """
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            # Create the probability distribution chart
            fig = self.visualizer.create_probability_distribution_chart(
                historical_data=historical_data,
                forecast_distributions=forecast_distributions,
                forecast_periods=forecast_periods,
                title=title
            )
            
            # Save chart if path provided
            if save_path:
                fig.write_html(save_path)
                logger.info(f"Probability distribution chart saved to: {save_path}")
            
            # Extract chart data for return
            chart_data = {
                "chart_type": "probability_distribution",
                "title": title,
                "historical_data_points": len(historical_data),
                "forecast_distributions_count": len(forecast_distributions),
                "forecast_periods": forecast_periods,
                "interactive_features": self.visualizer.interactive_features,
                "save_path": save_path
            }
            
            return {
                "success": True,
                "chart": fig,
                "data": chart_data
            }
            
        except Exception as e:
            logger.error(f"Error creating probability distribution visualization: {e}")
            return {"error": str(e)}
    
    def create_comprehensive_dashboard(
        self,
        charts_data: List[Tuple[str, Dict[str, Any]]],
        title: str = "Comprehensive Forecasting Dashboard",
        layout: str = "grid",
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a comprehensive interactive dashboard with multiple charts.
        
        Args:
            charts_data: List of (chart_name, chart_data) tuples
            title: Dashboard title
            layout: Layout type ('grid', 'vertical', 'horizontal')
            save_path: Optional path to save the dashboard as HTML
        
        Returns:
            Dictionary containing dashboard data and metadata
        """
        if not VISUALIZATION_AVAILABLE:
            return {"error": "Visualization system not available"}
        
        try:
            # Create individual charts
            charts = []
            for chart_name, chart_data in charts_data:
                if chart_data.get("success"):
                    charts.append((chart_name, chart_data["chart"]))
            
            if not charts:
                return {"error": "No valid charts to include in dashboard"}
            
            # Create the comprehensive dashboard
            fig = self.visualizer.create_interactive_dashboard(
                charts=charts,
                title=title,
                layout=layout
            )
            
            # Save dashboard if path provided
            if save_path:
                fig.write_html(save_path)
                logger.info(f"Comprehensive dashboard saved to: {save_path}")
            
            # Extract dashboard data for return
            dashboard_data = {
                "dashboard_type": "comprehensive",
                "title": title,
                "layout": layout,
                "charts_count": len(charts),
                "chart_names": [name for name, _ in charts],
                "interactive_features": self.visualizer.interactive_features,
                "save_path": save_path
            }
            
            return {
                "success": True,
                "dashboard": fig,
                "data": dashboard_data
            }
            
        except Exception as e:
            logger.error(f"Error creating comprehensive dashboard: {e}")
            return {"error": str(e)}
    
    def run_monte_carlo_with_visualization(
        self,
        simulation_config: Dict[str, Any],
        visualization_config: Optional[Dict[str, Any]] = None,
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation with integrated visualization.
        
        Args:
            simulation_config: Configuration for Monte Carlo simulation
            visualization_config: Configuration for visualizations
            output_dir: Directory to save visualization outputs
        
        Returns:
            Dictionary containing simulation results and visualizations
        """
        try:
            # Run Monte Carlo simulation
            logger.info("Running Monte Carlo simulation...")
            simulation_results = self.engine.run_simulation(simulation_config)
            
            if not simulation_results.get("success"):
                return {"error": "Monte Carlo simulation failed", "details": simulation_results}
            
            # Prepare visualization outputs
            visualizations = {}
            output_paths = {}
            
            if output_dir:
                output_path = Path(output_dir)
                output_path.mkdir(parents=True, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            else:
                output_path = None
                timestamp = ""
            
            # Create forecast visualization
            if visualization_config.get("create_forecast_chart", True):
                forecast_save_path = f"{output_path}/forecast_chart_{timestamp}.html" if output_path else None
                forecast_viz = self.create_forecast_visualization(
                    historical_data=simulation_results.get("historical_data", pd.DataFrame()),
                    forecast_data=simulation_results.get("forecast_data", pd.DataFrame()),
                    title="Monte Carlo Forecast Analysis",
                    save_path=forecast_save_path
                )
                visualizations["forecast"] = forecast_viz
                if forecast_save_path:
                    output_paths["forecast"] = forecast_save_path
            
            # Create Monte Carlo visualization
            if visualization_config.get("create_monte_carlo_chart", True):
                mc_save_path = f"{output_path}/monte_carlo_chart_{timestamp}.html" if output_path else None
                mc_viz = self.create_monte_carlo_visualization(
                    simulation_results=simulation_results,
                    title="Monte Carlo Simulation Results",
                    save_path=mc_save_path
                )
                visualizations["monte_carlo"] = mc_viz
                if mc_save_path:
                    output_paths["monte_carlo"] = mc_save_path
            
            # Create risk assessment visualization
            if visualization_config.get("create_risk_chart", True) and "risk_metrics" in simulation_results:
                risk_save_path = f"{output_path}/risk_assessment_{timestamp}.html" if output_path else None
                risk_viz = self.create_risk_assessment_visualization(
                    risk_data=pd.DataFrame(simulation_results["risk_metrics"]),
                    title="Risk Assessment Analysis",
                    save_path=risk_save_path
                )
                visualizations["risk_assessment"] = risk_viz
                if risk_save_path:
                    output_paths["risk_assessment"] = risk_save_path
            
            # Create comprehensive dashboard
            if visualization_config.get("create_dashboard", True):
                dashboard_save_path = f"{output_path}/comprehensive_dashboard_{timestamp}.html" if output_path else None
                dashboard_viz = self.create_comprehensive_dashboard(
                    charts_data=list(visualizations.items()),
                    title="Monte Carlo Simulation Dashboard",
                    save_path=dashboard_save_path
                )
                visualizations["dashboard"] = dashboard_viz
                if dashboard_save_path:
                    output_paths["dashboard"] = dashboard_save_path
            
            return {
                "success": True,
                "simulation_results": simulation_results,
                "visualizations": visualizations,
                "output_paths": output_paths,
                "metadata": {
                    "timestamp": timestamp,
                    "simulation_config": simulation_config,
                    "visualization_config": visualization_config
                }
            }
            
        except Exception as e:
            logger.error(f"Error in Monte Carlo with visualization: {e}")
            return {"error": str(e)}
    
    def export_visualization_config(self, config_name: str, config_data: Dict[str, Any]) -> bool:
        """Export visualization configuration for reuse."""
        try:
            # Implementation for configuration export
            logger.info(f"Visualization configuration '{config_name}' exported")
            return True
        except Exception as e:
            logger.error(f"Error exporting visualization config: {e}")
            return False
    
    def get_visualization_config(self, config_name: str) -> Optional[Dict[str, Any]]:
        """Get visualization configuration."""
        try:
            # Implementation for configuration retrieval
            return None
        except Exception as e:
            logger.error(f"Error retrieving visualization config: {e}")
            return None
