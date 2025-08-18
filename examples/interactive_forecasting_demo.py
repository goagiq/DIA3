#!/usr/bin/env python3
"""
Interactive Forecasting Visualization Demo

Demonstrates the enhanced interactive visualization system for forecasting and prediction charts
with distinct color schemes for historical vs future values.
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from core.visualization.interactive_forecasting_charts import (
        InteractiveForecastingCharts, 
        MonteCarloVisualizationHelper,
        ChartColors
    )
    from core.monte_carlo.visualization_integration import MonteCarloVisualizationIntegration
    VISUALIZATION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Visualization system not available: {e}")
    VISUALIZATION_AVAILABLE = False


def generate_sample_data():
    """Generate sample data for demonstration."""
    
    # Generate historical data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    np.random.seed(42)
    
    # Create realistic time series with trend and seasonality
    trend = np.linspace(100, 150, len(dates))
    seasonality = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
    noise = np.random.normal(0, 5, len(dates))
    historical_values = trend + seasonality + noise
    
    historical_data = pd.DataFrame({
        'timestamp': dates,
        'value': historical_values
    })
    
    # Generate forecast data
    forecast_dates = pd.date_range(start='2024-01-02', end='2024-12-31', freq='D')
    forecast_trend = np.linspace(150, 200, len(forecast_dates))
    forecast_seasonality = 10 * np.sin(2 * np.pi * np.arange(len(forecast_dates)) / 365.25)
    forecast_noise = np.random.normal(0, 8, len(forecast_dates))  # Higher uncertainty for future
    forecast_values = forecast_trend + forecast_seasonality + forecast_noise
    
    # Add confidence intervals
    confidence_width = 15 + np.random.normal(0, 3, len(forecast_dates))
    lower_bound = forecast_values - confidence_width
    upper_bound = forecast_values + confidence_width
    
    forecast_data = pd.DataFrame({
        'timestamp': forecast_dates,
        'value': forecast_values,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    })
    
    return historical_data, forecast_data


def generate_monte_carlo_simulations(historical_data, num_simulations=50, forecast_periods=365):
    """Generate Monte Carlo simulation paths."""
    
    # Use the last value as starting point
    last_value = historical_data['value'].iloc[-1]
    last_date = historical_data['timestamp'].iloc[-1]
    
    simulation_paths = []
    
    for i in range(num_simulations):
        # Generate forecast dates
        forecast_dates = pd.date_range(start=last_date + timedelta(days=1), 
                                     periods=forecast_periods, freq='D')
        
        # Generate random walk with drift
        np.random.seed(42 + i)  # Different seed for each simulation
        drift = 0.1  # Daily growth rate
        volatility = 0.02  # Daily volatility
        
        # Generate random walk
        random_walks = np.random.normal(drift, volatility, forecast_periods)
        cumulative_returns = np.cumprod(1 + random_walks)
        
        # Apply to starting value
        forecast_values = last_value * cumulative_returns
        
        # Add some trend and seasonality
        trend = np.linspace(0, 50, forecast_periods)
        seasonality = 5 * np.sin(2 * np.pi * np.arange(forecast_periods) / 365.25)
        forecast_values += trend + seasonality
        
        sim_data = pd.DataFrame({
            'timestamp': forecast_dates,
            'value': forecast_values
        })
        
        simulation_paths.append(sim_data)
    
    return simulation_paths


def generate_scenarios():
    """Generate different scenario data."""
    
    base_dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='ME')
    
    scenarios = [
        {
            'name': 'Baseline',
            'type': 'forecast',
            'timeline': base_dates,
            'values': np.linspace(150, 180, len(base_dates)) + np.random.normal(0, 5, len(base_dates))
        },
        {
            'name': 'Optimistic',
            'type': 'forecast',
            'timeline': base_dates,
            'values': np.linspace(150, 220, len(base_dates)) + np.random.normal(0, 3, len(base_dates))
        },
        {
            'name': 'Pessimistic',
            'type': 'forecast',
            'timeline': base_dates,
            'values': np.linspace(150, 140, len(base_dates)) + np.random.normal(0, 7, len(base_dates))
        },
        {
            'name': 'Historical',
            'type': 'historical',
            'timeline': pd.date_range(start='2023-01-01', end='2023-12-31', freq='ME'),
            'values': np.linspace(100, 150, 12) + np.random.normal(0, 5, 12)
        }
    ]
    
    return scenarios


def generate_risk_data():
    """Generate sample risk assessment data."""
    
    scenarios = ['Baseline', 'Optimistic', 'Pessimistic', 'Market Crash', 'Technology Breakthrough']
    time_periods = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025']
    
    # Generate risk scores (0-100, where 0 is low risk, 100 is high risk)
    np.random.seed(42)
    risk_scores = np.random.uniform(10, 90, (len(time_periods), len(scenarios)))
    
    # Create DataFrame
    risk_data = []
    for i, period in enumerate(time_periods):
        for j, scenario in enumerate(scenarios):
            risk_data.append({
                'time_period': period,
                'scenario': scenario,
                'risk_score': risk_scores[i, j]
            })
    
    return pd.DataFrame(risk_data)


def demo_forecast_timeline():
    """Demonstrate forecast timeline chart."""
    print("🎯 Demo 1: Forecast Timeline Chart")
    print("=" * 50)
    
    if not VISUALIZATION_AVAILABLE:
        print("❌ Visualization system not available")
        return
    
    # Generate sample data
    historical_data, forecast_data = generate_sample_data()
    
    # Create custom colors
    colors = ChartColors(
        historical_line="#1f77b4",  # Blue for historical
        future_line="#ff7f0e",      # Orange for future
        confidence_fill="rgba(255, 127, 14, 0.2)"
    )
    
    # Create visualization
    visualizer = InteractiveForecastingCharts(colors)
    
    # Create the chart
    fig = visualizer.create_forecast_timeline_chart(
        historical_data=historical_data,
        forecast_data=forecast_data,
        confidence_cols=('lower_bound', 'upper_bound'),
        title="Interactive Forecast Timeline - Historical vs Future Values"
    )
    
    # Save the chart
    output_path = Path("Results/interactive_forecasting_demo")
    output_path.mkdir(parents=True, exist_ok=True)
    
    chart_path = output_path / "forecast_timeline_demo.html"
    fig.write_html(str(chart_path))
    
    print(f"✅ Forecast timeline chart created and saved to: {chart_path}")
    print(f"📊 Historical data points: {len(historical_data)}")
    print(f"🔮 Forecast data points: {len(forecast_data)}")
    print(f"🎨 Color scheme: Blue (historical) vs Orange (future)")
    print()


def demo_monte_carlo_forecast():
    """Demonstrate Monte Carlo forecast chart."""
    print("🎲 Demo 2: Monte Carlo Forecast Chart")
    print("=" * 50)
    
    if not VISUALIZATION_AVAILABLE:
        print("❌ Visualization system not available")
        return
    
    # Generate sample data
    historical_data, _ = generate_sample_data()
    simulation_paths = generate_monte_carlo_simulations(historical_data, num_simulations=30)
    
    # Create visualization
    visualizer = InteractiveForecastingCharts()
    
    # Create the chart
    fig = visualizer.create_monte_carlo_forecast_chart(
        historical_data=historical_data,
        simulation_results=simulation_paths,
        forecast_periods=365,
        title="Monte Carlo Simulation - Multiple Future Paths"
    )
    
    # Save the chart
    output_path = Path("Results/interactive_forecasting_demo")
    chart_path = output_path / "monte_carlo_forecast_demo.html"
    fig.write_html(str(chart_path))
    
    print(f"✅ Monte Carlo forecast chart created and saved to: {chart_path}")
    print(f"📊 Historical data points: {len(historical_data)}")
    print(f"🔄 Simulation paths: {len(simulation_paths)}")
    print(f"🎨 Multiple colors for different simulation paths")
    print()


def demo_scenario_comparison():
    """Demonstrate scenario comparison chart."""
    print("📈 Demo 3: Scenario Comparison Chart")
    print("=" * 50)
    
    if not VISUALIZATION_AVAILABLE:
        print("❌ Visualization system not available")
        return
    
    # Generate scenarios
    scenarios = generate_scenarios()
    
    # Create visualization
    visualizer = InteractiveForecastingCharts()
    
    # Create the chart
    fig = visualizer.create_scenario_comparison_chart(
        scenarios=scenarios,
        title="Scenario Comparison - Multiple Future Scenarios"
    )
    
    # Save the chart
    output_path = Path("Results/interactive_forecasting_demo")
    chart_path = output_path / "scenario_comparison_demo.html"
    fig.write_html(str(chart_path))
    
    print(f"✅ Scenario comparison chart created and saved to: {chart_path}")
    print(f"📊 Scenarios: {len(scenarios)}")
    print(f"🎨 Different colors for each scenario")
    print(f"📅 Historical scenario in solid line, forecasts in dashed lines")
    print()


def demo_risk_assessment():
    """Demonstrate risk assessment heatmap."""
    print("⚠️ Demo 4: Risk Assessment Heatmap")
    print("=" * 50)
    
    if not VISUALIZATION_AVAILABLE:
        print("❌ Visualization system not available")
        return
    
    # Generate risk data
    risk_data = generate_risk_data()
    
    # Create visualization
    visualizer = InteractiveForecastingCharts()
    
    # Create the chart
    fig = visualizer.create_risk_heatmap(
        risk_data=risk_data,
        title="Risk Assessment Heatmap - Future Risk Analysis"
    )
    
    # Save the chart
    output_path = Path("Results/interactive_forecasting_demo")
    chart_path = output_path / "risk_assessment_demo.html"
    fig.write_html(str(chart_path))
    
    print(f"✅ Risk assessment heatmap created and saved to: {chart_path}")
    print(f"📊 Risk scenarios: {risk_data['scenario'].nunique()}")
    print(f"📅 Time periods: {risk_data['time_period'].nunique()}")
    print(f"🎨 Color scale: Red (high risk) to Green (low risk)")
    print()


def demo_probability_distribution():
    """Demonstrate probability distribution chart."""
    print("📊 Demo 5: Probability Distribution Chart")
    print("=" * 50)
    
    if not VISUALIZATION_AVAILABLE:
        print("❌ Visualization system not available")
        return
    
    # Generate sample data
    historical_data, _ = generate_sample_data()
    
    # Generate probability distributions for different forecast periods
    forecast_periods = ['1 Month', '3 Months', '6 Months', '1 Year']
    forecast_distributions = []
    
    for i, period in enumerate(forecast_periods):
        # Generate different distributions for each period
        mean_value = 150 + i * 10
        std_value = 5 + i * 2
        distribution = np.random.normal(mean_value, std_value, 1000)
        forecast_distributions.append(distribution)
    
    # Create visualization
    visualizer = InteractiveForecastingCharts()
    
    # Create the chart
    fig = visualizer.create_probability_distribution_chart(
        historical_data=historical_data,
        forecast_distributions=forecast_distributions,
        forecast_periods=forecast_periods,
        title="Probability Distribution Forecast - Uncertainty Analysis"
    )
    
    # Save the chart
    output_path = Path("Results/interactive_forecasting_demo")
    chart_path = output_path / "probability_distribution_demo.html"
    fig.write_html(str(chart_path))
    
    print(f"✅ Probability distribution chart created and saved to: {chart_path}")
    print(f"📊 Historical data points: {len(historical_data)}")
    print(f"📈 Forecast periods: {len(forecast_periods)}")
    print(f"🎨 Different colors for each forecast period distribution")
    print()


def demo_comprehensive_dashboard():
    """Demonstrate comprehensive dashboard."""
    print("🏠 Demo 6: Comprehensive Dashboard")
    print("=" * 50)
    
    if not VISUALIZATION_AVAILABLE:
        print("❌ Visualization system not available")
        return
    
    # Generate all data
    historical_data, forecast_data = generate_sample_data()
    simulation_paths = generate_monte_carlo_simulations(historical_data, num_simulations=20)
    scenarios = generate_scenarios()
    risk_data = generate_risk_data()
    
    # Create visualizations
    visualizer = InteractiveForecastingCharts()
    
    # Create individual charts
    charts = []
    
    # 1. Forecast timeline
    forecast_fig = visualizer.create_forecast_timeline_chart(
        historical_data=historical_data,
        forecast_data=forecast_data,
        title="Forecast Timeline"
    )
    charts.append(("Forecast Timeline", forecast_fig))
    
    # 2. Monte Carlo simulation
    mc_fig = visualizer.create_monte_carlo_forecast_chart(
        historical_data=historical_data,
        simulation_results=simulation_paths,
        forecast_periods=365,
        title="Monte Carlo Simulation"
    )
    charts.append(("Monte Carlo Simulation", mc_fig))
    
    # 3. Scenario comparison
    scenario_fig = visualizer.create_scenario_comparison_chart(
        scenarios=scenarios,
        title="Scenario Comparison"
    )
    charts.append(("Scenario Comparison", scenario_fig))
    
    # 4. Risk assessment
    risk_fig = visualizer.create_risk_heatmap(
        risk_data=risk_data,
        title="Risk Assessment"
    )
    charts.append(("Risk Assessment", risk_fig))
    
    # Create comprehensive dashboard
    dashboard_fig = visualizer.create_interactive_dashboard(
        charts=charts,
        title="Interactive Forecasting Dashboard - Comprehensive View",
        layout="grid"
    )
    
    # Save the dashboard
    output_path = Path("Results/interactive_forecasting_demo")
    dashboard_path = output_path / "comprehensive_dashboard_demo.html"
    dashboard_fig.write_html(str(dashboard_path))
    
    print(f"✅ Comprehensive dashboard created and saved to: {dashboard_path}")
    print(f"📊 Total charts: {len(charts)}")
    print(f"🎨 Interactive features: Zoom, Pan, Hover, Range Slider")
    print(f"📱 Responsive layout with grid arrangement")
    print()


def demo_monte_carlo_integration():
    """Demonstrate Monte Carlo integration with visualization."""
    print("🔗 Demo 7: Monte Carlo Integration")
    print("=" * 50)
    
    if not VISUALIZATION_AVAILABLE:
        print("❌ Visualization system not available")
        return
    
    try:
        # Create integration instance
        integration = MonteCarloVisualizationIntegration()
        
        # Create sample simulation results
        historical_data, forecast_data = generate_sample_data()
        simulation_paths = generate_monte_carlo_simulations(historical_data, num_simulations=25)
        
        simulation_results = {
            'historical_data': historical_data,
            'forecast_data': forecast_data,
            'simulation_paths': simulation_paths,
            'forecast_periods': 365,
            'risk_metrics': {
                'var_95': 0.05,
                'cvar_95': 0.08,
                'probability_of_failure': 0.15
            }
        }
        
        # Create visualizations using integration
        output_path = Path("Results/interactive_forecasting_demo")
        
        # 1. Forecast visualization
        forecast_viz = integration.create_forecast_visualization(
            historical_data=historical_data,
            forecast_data=forecast_data,
            confidence_intervals=('lower_bound', 'upper_bound'),
            title="Integrated Forecast Analysis",
            save_path=str(output_path / "integrated_forecast.html")
        )
        
        # 2. Monte Carlo visualization
        mc_viz = integration.create_monte_carlo_visualization(
            simulation_results=simulation_results,
            title="Integrated Monte Carlo Analysis",
            save_path=str(output_path / "integrated_monte_carlo.html")
        )
        
        # 3. Risk assessment visualization
        risk_viz = integration.create_risk_assessment_visualization(
            risk_data=generate_risk_data(),
            title="Integrated Risk Assessment",
            save_path=str(output_path / "integrated_risk_assessment.html")
        )
        
        print("✅ Monte Carlo integration demo completed")
        print(f"📊 Forecast visualization: {forecast_viz.get('success', False)}")
        print(f"🎲 Monte Carlo visualization: {mc_viz.get('success', False)}")
        print(f"⚠️ Risk assessment visualization: {risk_viz.get('success', False)}")
        print()
        
    except Exception as e:
        print(f"❌ Monte Carlo integration demo failed: {e}")
        print()


def main():
    """Run all demos."""
    print("🚀 Interactive Forecasting Visualization Demo")
    print("=" * 60)
    print("This demo showcases the enhanced interactive visualization system")
    print("with distinct color schemes for historical vs future values.")
    print()
    
    # Create output directory
    output_path = Path("Results/interactive_forecasting_demo")
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Run all demos
    demos = [
        demo_forecast_timeline,
        demo_monte_carlo_forecast,
        demo_scenario_comparison,
        demo_risk_assessment,
        demo_probability_distribution,
        demo_comprehensive_dashboard,
        demo_monte_carlo_integration
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            print()
    
    print("🎉 Demo completed!")
    print(f"📁 All charts saved to: {output_path}")
    print()
    print("📋 Summary of Interactive Features:")
    print("• 🎨 Distinct colors: Blue (historical) vs Orange (future)")
    print("• 🔍 Zoom and pan capabilities")
    print("• 📊 Range slider for time navigation")
    print("• 🖱️ Interactive hover tooltips")
    print("• 📱 Responsive design")
    print("• 💾 HTML export for sharing")
    print()
    print("🔗 Open the HTML files in a web browser to view interactive charts!")


if __name__ == "__main__":
    main()
