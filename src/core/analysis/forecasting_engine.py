#!/usr/bin/env python3
"""
Forecasting Engine for Enhanced Reports
Provides time series forecasting and trend prediction capabilities.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class ForecastingEngine:
    """Advanced forecasting engine for strategic analysis."""
    
    def __init__(self):
        """Initialize the forecasting engine."""
        self.results = {}
        self.models = {}
        
    def create_sample_time_series(self, periods: int = 100, trend: float = 0.1, 
                                 seasonality: bool = True, noise: float = 0.1) -> pd.Series:
        """Create sample time series data for demonstration."""
        dates = pd.date_range('2020-01-01', periods=periods, freq='D')
        
        # Generate trend
        trend_component = np.linspace(0, trend * periods, periods)
        
        # Generate seasonality (weekly pattern)
        if seasonality:
            seasonal_component = 2 * np.sin(2 * np.pi * np.arange(periods) / 7)
        else:
            seasonal_component = np.zeros(periods)
        
        # Generate noise
        noise_component = np.random.normal(0, noise, periods)
        
        # Combine components
        values = trend_component + seasonal_component + noise_component
        
        return pd.Series(values, index=dates)
    
    def perform_time_series_forecast(self, data: pd.Series, forecast_periods: int = 30,
                                   title: str = "Time Series Forecast") -> Dict[str, Any]:
        """Perform time series forecasting using multiple methods."""
        try:
            # Simple moving average forecast
            ma_forecast = data.rolling(window=7).mean().iloc[-1]
            ma_forecast_series = [ma_forecast] * forecast_periods
            
            # Linear trend forecast
            x = np.arange(len(data))
            y = data.values
            slope, intercept = np.polyfit(x, y, 1)
            
            future_x = np.arange(len(data), len(data) + forecast_periods)
            linear_forecast = slope * future_x + intercept
            
            # Exponential smoothing forecast
            alpha = 0.3
            exp_smooth = [data.iloc[-1]]
            for _ in range(forecast_periods - 1):
                next_val = alpha * data.iloc[-1] + (1 - alpha) * exp_smooth[-1]
                exp_smooth.append(next_val)
            
            # Generate forecast dates
            last_date = data.index[-1]
            forecast_dates = pd.date_range(last_date + timedelta(days=1), 
                                         periods=forecast_periods, freq='D')
            
            # Calculate forecast metrics
            forecast_metrics = {
                "ma_forecast": {
                    "values": ma_forecast_series,
                    "mean": np.mean(ma_forecast_series),
                    "std": np.std(ma_forecast_series)
                },
                "linear_forecast": {
                    "values": linear_forecast.tolist(),
                    "mean": np.mean(linear_forecast),
                    "std": np.std(linear_forecast),
                    "trend": slope
                },
                "exp_smooth_forecast": {
                    "values": exp_smooth,
                    "mean": np.mean(exp_smooth),
                    "std": np.std(exp_smooth)
                }
            }
            
            # Confidence intervals
            confidence_intervals = {
                "ma_forecast": {
                    "lower": [v - 1.96 * forecast_metrics["ma_forecast"]["std"] for v in ma_forecast_series],
                    "upper": [v + 1.96 * forecast_metrics["ma_forecast"]["std"] for v in ma_forecast_series]
                },
                "linear_forecast": {
                    "lower": [v - 1.96 * forecast_metrics["linear_forecast"]["std"] for v in linear_forecast],
                    "upper": [v + 1.96 * forecast_metrics["linear_forecast"]["std"] for v in linear_forecast]
                },
                "exp_smooth_forecast": {
                    "lower": [v - 1.96 * forecast_metrics["exp_smooth_forecast"]["std"] for v in exp_smooth],
                    "upper": [v + 1.96 * forecast_metrics["exp_smooth_forecast"]["std"] for v in exp_smooth]
                }
            }
            
            return {
                "title": title,
                "original_data": {
                    "dates": data.index.strftime('%Y-%m-%d').tolist(),
                    "values": data.values.tolist(),
                    "length": len(data)
                },
                "forecast_periods": forecast_periods,
                "forecast_dates": forecast_dates.strftime('%Y-%m-%d').tolist(),
                "forecast_metrics": forecast_metrics,
                "confidence_intervals": confidence_intervals,
                "model_comparison": {
                    "ma_forecast_mean": forecast_metrics["ma_forecast"]["mean"],
                    "linear_forecast_mean": forecast_metrics["linear_forecast"]["mean"],
                    "exp_smooth_forecast_mean": forecast_metrics["exp_smooth_forecast"]["mean"],
                    "trend_direction": "increasing" if slope > 0 else "decreasing",
                    "trend_strength": abs(slope)
                }
            }
            
        except Exception as e:
            return {
                "error": f"Forecasting failed: {str(e)}",
                "title": title
            }
    
    def analyze_trends(self, data: pd.Series, window_sizes: List[int] = [7, 14, 30]) -> Dict[str, Any]:
        """Analyze trends in time series data."""
        try:
            trends = {}
            
            for window in window_sizes:
                if len(data) >= window:
                    # Calculate moving averages
                    ma = data.rolling(window=window).mean()
                    
                    # Calculate trend direction
                    if len(ma.dropna()) > 1:
                        trend_slope = np.polyfit(range(len(ma.dropna())), ma.dropna(), 1)[0]
                        trend_direction = "increasing" if trend_slope > 0 else "decreasing"
                        trend_strength = abs(trend_slope)
                    else:
                        trend_slope = 0
                        trend_direction = "stable"
                        trend_strength = 0
                    
                    trends[f"window_{window}"] = {
                        "moving_average": ma.tolist(),
                        "trend_slope": trend_slope,
                        "trend_direction": trend_direction,
                        "trend_strength": trend_strength
                    }
            
            # Overall trend analysis
            overall_slope = np.polyfit(range(len(data)), data.values, 1)[0]
            
            return {
                "window_trends": trends,
                "overall_trend": {
                    "slope": overall_slope,
                    "direction": "increasing" if overall_slope > 0 else "decreasing",
                    "strength": abs(overall_slope)
                },
                "data_summary": {
                    "mean": data.mean(),
                    "std": data.std(),
                    "min": data.min(),
                    "max": data.max(),
                    "range": data.max() - data.min()
                }
            }
            
        except Exception as e:
            return {
                "error": f"Trend analysis failed: {str(e)}"
            }
    
    def generate_forecast_report(self, forecast_results: Dict[str, Any], output_path: str = None) -> str:
        """Generate comprehensive forecasting report."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if output_path is None:
                output_path = f"Results/forecast_report_{timestamp}.html"
            
            # Create HTML report
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Forecasting Report</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; }}
                    .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 20px; border-radius: 10px; }}
                    .section {{ margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 10px; }}
                    .metric {{ display: inline-block; margin: 10px; padding: 15px; background: white; border-radius: 8px; text-align: center; }}
                    .metric-value {{ font-size: 2em; font-weight: bold; }}
                    .chart-container {{ width: 100%; max-width: 800px; margin: 20px auto; }}
                    .forecast-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                    .forecast-table th, .forecast-table td {{ padding: 10px; border: 1px solid #ddd; text-align: center; }}
                    .forecast-table th {{ background: #1e3c72; color: white; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Forecasting Report</h1>
                    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
                
                <div class="section">
                    <h2>Forecast Summary</h2>
                    <div class="metric">
                        <div class="metric-value">
                            {forecast_results.get('forecast_periods', 0)}
                        </div>
                        <div>Forecast Periods</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">
                            {forecast_results.get('model_comparison', {}).get('trend_direction', 'Unknown')}
                        </div>
                        <div>Trend Direction</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">
                            {forecast_results.get('model_comparison', {}).get('trend_strength', 0):.3f}
                        </div>
                        <div>Trend Strength</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Forecast Comparison</h2>
                    <div class="chart-container">
                        <canvas id="forecastChart"></canvas>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Model Performance Comparison</h2>
                    <table class="forecast-table">
                        <thead>
                            <tr>
                                <th>Model</th>
                                <th>Mean Forecast</th>
                                <th>Standard Deviation</th>
                                <th>Trend</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Moving Average</td>
                                <td>{forecast_results.get('forecast_metrics', {}).get('ma_forecast', {}).get('mean', 0):.2f}</td>
                                <td>{forecast_results.get('forecast_metrics', {}).get('ma_forecast', {}).get('std', 0):.2f}</td>
                                <td>Stable</td>
                            </tr>
                            <tr>
                                <td>Linear Trend</td>
                                <td>{forecast_results.get('forecast_metrics', {}).get('linear_forecast', {}).get('mean', 0):.2f}</td>
                                <td>{forecast_results.get('forecast_metrics', {}).get('linear_forecast', {}).get('std', 0):.2f}</td>
                                <td>{forecast_results.get('model_comparison', {}).get('trend_direction', 'Unknown')}</td>
                            </tr>
                            <tr>
                                <td>Exponential Smoothing</td>
                                <td>{forecast_results.get('forecast_metrics', {}).get('exp_smooth_forecast', {}).get('mean', 0):.2f}</td>
                                <td>{forecast_results.get('forecast_metrics', {}).get('exp_smooth_forecast', {}).get('std', 0):.2f}</td>
                                <td>Adaptive</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <script>
                    // Forecast Chart
                    const ctx = document.getElementById('forecastChart').getContext('2d');
                    new Chart(ctx, {{
                        type: 'line',
                        data: {{
                            labels: {forecast_results.get('original_data', {}).get('dates', []) + forecast_results.get('forecast_dates', [])},
                            datasets: [
                                {{
                                    label: 'Original Data',
                                    data: {forecast_results.get('original_data', {}).get('values', [])},
                                    borderColor: '#1e3c72',
                                    backgroundColor: 'rgba(30, 60, 114, 0.1)',
                                    fill: false
                                }},
                                {{
                                    label: 'Moving Average Forecast',
                                    data: [null, ...{forecast_results.get('forecast_metrics', {}).get('ma_forecast', {}).get('values', [])}],
                                    borderColor: '#28a745',
                                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                                    fill: false,
                                    borderDash: [5, 5]
                                }},
                                {{
                                    label: 'Linear Trend Forecast',
                                    data: [null, ...{forecast_results.get('forecast_metrics', {}).get('linear_forecast', {}).get('values', [])}],
                                    borderColor: '#dc3545',
                                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                                    fill: false,
                                    borderDash: [10, 5]
                                }},
                                {{
                                    label: 'Exponential Smoothing',
                                    data: [null, ...{forecast_results.get('forecast_metrics', {}).get('exp_smooth_forecast', {}).get('values', [])}],
                                    borderColor: '#ffc107',
                                    backgroundColor: 'rgba(255, 193, 7, 0.1)',
                                    fill: false,
                                    borderDash: [2, 2]
                                }}
                            ]
                        }},
                        options: {{
                            responsive: true,
                            plugins: {{
                                title: {{
                                    display: true,
                                    text: 'Time Series Forecast Comparison'
                                }}
                            }},
                            scales: {{
                                x: {{
                                    title: {{
                                        display: true,
                                        text: 'Date'
                                    }}
                                }},
                                y: {{
                                    title: {{
                                        display: true,
                                        text: 'Value'
                                    }}
                                }}
                            }}
                        }}
                    }});
                </script>
            </body>
            </html>
            """
            
            # Save report
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return output_path
            
        except Exception as e:
            return f"Report generation failed: {str(e)}"

# Create global instance
forecasting_engine = ForecastingEngine()


