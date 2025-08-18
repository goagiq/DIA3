"""
Interactive Forecasting Charts

Advanced interactive visualization system for forecasting and prediction charts
with distinct color schemes for historical vs future values.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ChartColors:
    """Color scheme configuration for forecasting charts."""
    # Historical data colors
    historical_line: str = "#1f77b4"  # Blue
    historical_marker: str = "#1f77b4"
    historical_fill: str = "rgba(31, 119, 180, 0.1)"
    
    # Future/forecast colors
    future_line: str = "#ff7f0e"  # Orange
    future_marker: str = "#ff7f0e"
    future_fill: str = "rgba(255, 127, 14, 0.1)"
    
    # Confidence interval colors
    confidence_upper: str = "#ff7f0e"  # Orange
    confidence_lower: str = "#ff7f0e"
    confidence_fill: str = "rgba(255, 127, 14, 0.2)"
    
    # Alternative future scenarios
    scenario_colors: List[str] = None
    
    def __post_init__(self):
        if self.scenario_colors is None:
            self.scenario_colors = [
                "#2ca02c",  # Green
                "#d62728",  # Red
                "#9467bd",  # Purple
                "#8c564b",  # Brown
                "#e377c2",  # Pink
                "#7f7f7f",  # Gray
                "#bcbd22",  # Olive
                "#17becf"   # Cyan
            ]


class InteractiveForecastingCharts:
    """
    Interactive forecasting chart generator with enhanced features for
    Monte Carlo simulations and predictive analytics.
    """
    
    def __init__(self, colors: Optional[ChartColors] = None):
        """Initialize the interactive forecasting charts."""
        self.colors = colors or ChartColors()
        self.interactive_features = {
            'zoom': True,
            'pan': True,
            'hover': True,
            'selection': True,
            'range_slider': True
        }
    
    def create_forecast_timeline_chart(
        self,
        historical_data: pd.DataFrame,
        forecast_data: pd.DataFrame,
        title: str = "Forecast Timeline",
        x_col: str = "timestamp",
        y_col: str = "value",
        confidence_cols: Optional[Tuple[str, str]] = None,
        **kwargs
    ) -> go.Figure:
        """
        Create an interactive forecast timeline chart with distinct colors for historical vs future data.
        
        Args:
            historical_data: DataFrame with historical data
            forecast_data: DataFrame with forecast data
            title: Chart title
            x_col: Column name for x-axis (time)
            y_col: Column name for y-axis (values)
            confidence_cols: Tuple of (lower_bound_col, upper_bound_col) for confidence intervals
        """
        fig = go.Figure()
        
        # Add historical data
        if not historical_data.empty:
            fig.add_trace(go.Scatter(
                x=historical_data[x_col],
                y=historical_data[y_col],
                mode='lines+markers',
                name='Historical',
                line=dict(
                    color=self.colors.historical_line,
                    width=3
                ),
                marker=dict(
                    size=6,
                    color=self.colors.historical_marker
                ),
                hovertemplate='<b>Historical</b><br>' +
                            f'{x_col}: %{{x}}<br>' +
                            f'{y_col}: %{{y:.2f}}<br>' +
                            '<extra></extra>'
            ))
        
        # Add forecast data
        if not forecast_data.empty:
            fig.add_trace(go.Scatter(
                x=forecast_data[x_col],
                y=forecast_data[y_col],
                mode='lines+markers',
                name='Forecast',
                line=dict(
                    color=self.colors.future_line,
                    width=3,
                    dash='dash'
                ),
                marker=dict(
                    size=6,
                    color=self.colors.future_marker
                ),
                hovertemplate='<b>Forecast</b><br>' +
                            f'{x_col}: %{{x}}<br>' +
                            f'{y_col}: %{{y:.2f}}<br>' +
                            '<extra></extra>'
            ))
            
            # Add confidence intervals if available
            if confidence_cols and all(col in forecast_data.columns for col in confidence_cols):
                lower_col, upper_col = confidence_cols
                
                # Upper bound
                fig.add_trace(go.Scatter(
                    x=forecast_data[x_col],
                    y=forecast_data[upper_col],
                    mode='lines',
                    name='Upper Bound',
                    line=dict(
                        color=self.colors.confidence_upper,
                        width=1,
                        dash='dot'
                    ),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                # Lower bound with fill
                fig.add_trace(go.Scatter(
                    x=forecast_data[x_col],
                    y=forecast_data[lower_col],
                    mode='lines',
                    fill='tonexty',
                    name='Confidence Interval',
                    line=dict(
                        color=self.colors.confidence_lower,
                        width=1,
                        dash='dot'
                    ),
                    fillcolor=self.colors.confidence_fill,
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        # Update layout with interactive features
        fig.update_layout(
            title=title,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title(),
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            **kwargs
        )
        
        # Add interactive features
        if self.interactive_features['range_slider']:
            fig.update_xaxes(rangeslider_visible=True)
        
        if self.interactive_features['zoom']:
            fig.update_layout(
                dragmode='zoom',
                selectdirection='any'
            )
        
        return fig
    
    def create_monte_carlo_forecast_chart(
        self,
        historical_data: pd.DataFrame,
        simulation_results: List[pd.DataFrame],
        forecast_periods: int,
        title: str = "Monte Carlo Forecast",
        x_col: str = "timestamp",
        y_col: str = "value",
        **kwargs
    ) -> go.Figure:
        """
        Create an interactive Monte Carlo forecast chart showing multiple simulation paths.
        
        Args:
            historical_data: DataFrame with historical data
            simulation_results: List of DataFrames with simulation results
            forecast_periods: Number of forecast periods
            title: Chart title
            x_col: Column name for x-axis (time)
            y_col: Column name for y-axis (values)
        """
        fig = go.Figure()
        
        # Add historical data
        if not historical_data.empty:
            fig.add_trace(go.Scatter(
                x=historical_data[x_col],
                y=historical_data[y_col],
                mode='lines+markers',
                name='Historical',
                line=dict(
                    color=self.colors.historical_line,
                    width=4
                ),
                marker=dict(
                    size=8,
                    color=self.colors.historical_marker
                ),
                hovertemplate='<b>Historical</b><br>' +
                            f'{x_col}: %{{x}}<br>' +
                            f'{y_col}: %{{y:.2f}}<br>' +
                            '<extra></extra>'
            ))
        
        # Add simulation paths
        for i, sim_data in enumerate(simulation_results):
            if not sim_data.empty:
                # Use different colors for future scenarios
                color = self.colors.scenario_colors[i % len(self.colors.scenario_colors)]
                
                fig.add_trace(go.Scatter(
                    x=sim_data[x_col],
                    y=sim_data[y_col],
                    mode='lines',
                    name=f'Simulation {i+1}',
                    line=dict(
                        color=color,
                        width=1
                    ),
                    opacity=0.6,
                    showlegend=False,
                    hovertemplate='<b>Simulation</b><br>' +
                                f'{x_col}: %{{x}}<br>' +
                                f'{y_col}: %{{y:.2f}}<br>' +
                                '<extra></extra>'
                ))
        
        # Calculate and add confidence bands
        if simulation_results:
            all_forecasts = []
            for sim_data in simulation_results:
                if not sim_data.empty:
                    all_forecasts.append(sim_data[y_col].values)
            
            if all_forecasts:
                forecast_array = np.array(all_forecasts)
                mean_forecast = np.mean(forecast_array, axis=0)
                std_forecast = np.std(forecast_array, axis=0)
                
                # Use the first simulation data for x-axis
                forecast_x = simulation_results[0][x_col]
                
                # Add mean forecast line
                fig.add_trace(go.Scatter(
                    x=forecast_x,
                    y=mean_forecast,
                    mode='lines',
                    name='Mean Forecast',
                    line=dict(
                        color=self.colors.future_line,
                        width=3,
                        dash='solid'
                    ),
                    hovertemplate='<b>Mean Forecast</b><br>' +
                                f'{x_col}: %{{x}}<br>' +
                                f'{y_col}: %{{y:.2f}}<br>' +
                                '<extra></extra>'
                ))
                
                # Add confidence bands
                for confidence_level in [0.68, 0.95]:  # 1σ and 2σ
                    z_score = 1.0 if confidence_level == 0.68 else 2.0
                    upper_bound = mean_forecast + z_score * std_forecast
                    lower_bound = mean_forecast - z_score * std_forecast
                    
                    fig.add_trace(go.Scatter(
                        x=forecast_x,
                        y=upper_bound,
                        mode='lines',
                        name=f'{int(confidence_level*100)}% Confidence',
                        line=dict(
                            color=self.colors.confidence_upper,
                            width=1,
                            dash='dot'
                        ),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=forecast_x,
                        y=lower_bound,
                        mode='lines',
                        fill='tonexty',
                        name=f'{int(confidence_level*100)}% Confidence',
                        line=dict(
                            color=self.colors.confidence_lower,
                            width=1,
                            dash='dot'
                        ),
                        fillcolor=f'rgba(255, 127, 14, {0.1 if confidence_level == 0.68 else 0.05})',
                        showlegend=False,
                        hoverinfo='skip'
                    ))
        
        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title(),
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            **kwargs
        )
        
        # Add interactive features
        if self.interactive_features['range_slider']:
            fig.update_xaxes(rangeslider_visible=True)
        
        return fig
    
    def create_scenario_comparison_chart(
        self,
        scenarios: List[Dict[str, Any]],
        title: str = "Scenario Comparison",
        **kwargs
    ) -> go.Figure:
        """
        Create an interactive scenario comparison chart.
        
        Args:
            scenarios: List of scenario dictionaries with 'name', 'timeline', 'values', 'type'
            title: Chart title
        """
        fig = go.Figure()
        
        for i, scenario in enumerate(scenarios):
            scenario_type = scenario.get('type', 'forecast')
            color = self.colors.scenario_colors[i % len(self.colors.scenario_colors)]
            
            # Determine line style based on scenario type
            line_style = 'solid' if scenario_type == 'historical' else 'dash'
            line_color = self.colors.historical_line if scenario_type == 'historical' else color
            
            fig.add_trace(go.Scatter(
                x=scenario['timeline'],
                y=scenario['values'],
                mode='lines+markers',
                name=scenario['name'],
                line=dict(
                    color=line_color,
                    width=3,
                    dash=line_style
                ),
                marker=dict(size=6),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                            'Time: %{x}<br>' +
                            'Value: %{y:.2f}<br>' +
                            '<extra></extra>'
            ))
            
            # Add confidence intervals if available
            if 'lower_bound' in scenario and 'upper_bound' in scenario:
                fig.add_trace(go.Scatter(
                    x=scenario['timeline'],
                    y=scenario['upper_bound'],
                    mode='lines',
                    name=f"{scenario['name']} Upper",
                    line=dict(
                        color=color,
                        width=1,
                        dash='dot'
                    ),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                fig.add_trace(go.Scatter(
                    x=scenario['timeline'],
                    y=scenario['lower_bound'],
                    mode='lines',
                    fill='tonexty',
                    name=f"{scenario['name']} CI",
                    line=dict(
                        color=color,
                        width=1,
                        dash='dot'
                    ),
                    fillcolor=f'rgba({color},0.1)',
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title="Time Period",
            yaxis_title="Value",
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            **kwargs
        )
        
        # Add interactive features
        if self.interactive_features['range_slider']:
            fig.update_xaxes(rangeslider_visible=True)
        
        return fig
    
    def create_risk_heatmap(
        self,
        risk_data: pd.DataFrame,
        x_col: str = "scenario",
        y_col: str = "time_period",
        value_col: str = "risk_score",
        title: str = "Risk Assessment Heatmap",
        **kwargs
    ) -> go.Figure:
        """
        Create an interactive risk assessment heatmap.
        
        Args:
            risk_data: DataFrame with risk assessment data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            value_col: Column name for risk values
            title: Chart title
        """
        # Pivot data for heatmap
        pivot_data = risk_data.pivot(index=y_col, columns=x_col, values=value_col)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='RdYlGn_r',  # Red (high risk) to Green (low risk)
            colorbar=dict(
                title=dict(text="Risk Score", side="right")
            ),
            hovertemplate='<b>%{y}</b><br>' +
                         '<b>%{x}</b><br>' +
                         'Risk Score: %{z:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title(),
            **kwargs
        )
        
        return fig
    
    def create_probability_distribution_chart(
        self,
        historical_data: pd.DataFrame,
        forecast_distributions: List[np.ndarray],
        forecast_periods: List[str],
        title: str = "Probability Distribution Forecast",
        x_col: str = "timestamp",
        y_col: str = "value",
        **kwargs
    ) -> go.Figure:
        """
        Create an interactive probability distribution chart showing forecast uncertainty.
        
        Args:
            historical_data: DataFrame with historical data
            forecast_distributions: List of probability distributions for each forecast period
            forecast_periods: List of forecast period labels
            title: Chart title
            x_col: Column name for x-axis (time)
            y_col: Column name for y-axis (values)
        """
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Historical and Forecast", "Forecast Distributions"),
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )
        
        # Add historical data to first subplot
        if not historical_data.empty:
            fig.add_trace(go.Scatter(
                x=historical_data[x_col],
                y=historical_data[y_col],
                mode='lines+markers',
                name='Historical',
                line=dict(
                    color=self.colors.historical_line,
                    width=3
                ),
                marker=dict(
                    size=6,
                    color=self.colors.historical_marker
                ),
                hovertemplate='<b>Historical</b><br>' +
                            f'{x_col}: %{{x}}<br>' +
                            f'{y_col}: %{{y:.2f}}<br>' +
                            '<extra></extra>'
            ), row=1, col=1)
        
        # Add forecast distributions to second subplot
        for i, (distribution, period) in enumerate(zip(forecast_distributions, forecast_periods)):
            color = self.colors.scenario_colors[i % len(self.colors.scenario_colors)]
            
            # Create histogram for distribution
            fig.add_trace(go.Histogram(
                x=distribution,
                name=f'{period} Distribution',
                nbinsx=30,
                opacity=0.7,
                marker_color=color,
                hovertemplate='<b>%{fullData.name}</b><br>' +
                            'Value: %{x:.2f}<br>' +
                            'Count: %{y}<br>' +
                            '<extra></extra>'
            ), row=2, col=1)
        
        # Update layout
        fig.update_layout(
            title=title,
            showlegend=True,
            height=800,
            **kwargs
        )
        
        # Update axes labels
        fig.update_xaxes(title_text=x_col.replace('_', ' ').title(), row=1, col=1)
        fig.update_yaxes(title_text=y_col.replace('_', ' ').title(), row=1, col=1)
        fig.update_xaxes(title_text="Value", row=2, col=1)
        fig.update_yaxes(title_text="Frequency", row=2, col=1)
        
        return fig
    
    def create_interactive_dashboard(
        self,
        charts: List[Tuple[str, go.Figure]],
        title: str = "Interactive Forecasting Dashboard",
        layout: str = "grid"
    ) -> go.Figure:
        """
        Create an interactive dashboard combining multiple charts.
        
        Args:
            charts: List of (chart_name, figure) tuples
            title: Dashboard title
            layout: Layout type ('grid', 'vertical', 'horizontal')
        """
        if layout == "grid":
            n_charts = len(charts)
            cols = min(2, n_charts)
            rows = (n_charts + cols - 1) // cols
            
            fig = make_subplots(
                rows=rows, cols=cols,
                subplot_titles=[name for name, _ in charts],
                specs=[[{"type": "scatter"} for _ in range(cols)] for _ in range(rows)]
            )
            
            for i, (chart_name, chart_fig) in enumerate(charts):
                row = i // cols + 1
                col = i % cols + 1
                
                # Add traces from chart to subplot
                for trace in chart_fig.data:
                    fig.add_trace(trace, row=row, col=col)
        
        else:  # vertical or horizontal
            fig = make_subplots(
                rows=len(charts), cols=1,
                subplot_titles=[name for name, _ in charts],
                vertical_spacing=0.1
            )
            
            for i, (chart_name, chart_fig) in enumerate(charts):
                # Add traces from chart to subplot
                for trace in chart_fig.data:
                    fig.add_trace(trace, row=i+1, col=1)
        
        # Update layout
        fig.update_layout(
            title=title,
            showlegend=True,
            height=300 * len(charts)
        )
        
        return fig
    
    def export_chart_config(self, chart_id: str, config: Dict[str, Any]) -> None:
        """Export chart configuration for reuse."""
        # Implementation for chart configuration export
        pass
    
    def get_chart_config(self, chart_id: str) -> Optional[Dict[str, Any]]:
        """Get chart configuration."""
        # Implementation for chart configuration retrieval
        pass


class MonteCarloVisualizationHelper:
    """
    Helper class for creating Monte Carlo specific visualizations.
    """
    
    def __init__(self, colors: Optional[ChartColors] = None):
        self.charts = InteractiveForecastingCharts(colors)
    
    def create_simulation_results_chart(
        self,
        simulation_data: Dict[str, Any],
        title: str = "Monte Carlo Simulation Results"
    ) -> go.Figure:
        """
        Create a comprehensive Monte Carlo simulation results chart.
        
        Args:
            simulation_data: Dictionary containing simulation results
            title: Chart title
        """
        # Extract data from simulation results
        historical_data = simulation_data.get('historical_data', pd.DataFrame())
        simulation_paths = simulation_data.get('simulation_paths', [])
        forecast_periods = simulation_data.get('forecast_periods', 12)
        
        return self.charts.create_monte_carlo_forecast_chart(
            historical_data=historical_data,
            simulation_results=simulation_paths,
            forecast_periods=forecast_periods,
            title=title
        )
    
    def create_risk_metrics_chart(
        self,
        risk_metrics: Dict[str, Any],
        title: str = "Risk Metrics Analysis"
    ) -> go.Figure:
        """
        Create a risk metrics visualization chart.
        
        Args:
            risk_metrics: Dictionary containing risk metrics
            title: Chart title
        """
        # Convert risk metrics to DataFrame for visualization
        risk_df = pd.DataFrame(risk_metrics)
        
        return self.charts.create_risk_heatmap(
            risk_data=risk_df,
            title=title
        )
    
    def create_confidence_interval_chart(
        self,
        confidence_data: Dict[str, Any],
        title: str = "Confidence Interval Analysis"
    ) -> go.Figure:
        """
        Create a confidence interval visualization chart.
        
        Args:
            confidence_data: Dictionary containing confidence interval data
            title: Chart title
        """
        # Implementation for confidence interval chart
        pass
