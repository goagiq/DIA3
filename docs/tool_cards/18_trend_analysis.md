# Tool Card: trend_analysis

## General Info

- **Name**: trend_analysis
- **Title**: Advanced Trend Analysis and Forecasting Engine
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Perform comprehensive trend analysis, forecasting, and trend prediction using advanced statistical and machine learning methods

## Required Libraries

### Core Python Libraries
```python
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import numpy as np
import pandas as pd
```

### Statistical Libraries
```python
import scipy>=1.11.4
import statsmodels>=0.14.0
import scikit-learn>=1.3.2
import numpy>=1.24.3
import pandas>=2.1.4
```

### Time Series Libraries
```python
import statsmodels.tsa>=0.14.0
import statsmodels.tsa.seasonal>=0.14.0
import statsmodels.tsa.stattools>=0.14.0
import statsmodels.tsa.arima>=0.14.0
import statsmodels.tsa.statespace>=0.14.0
import pmdarima>=2.0.4
import prophet>=1.1.4
```

### Machine Learning Libraries
```python
import scikit-learn>=1.3.2
import xgboost>=2.0.0
import lightgbm>=4.1.0
import catboost>=1.2.0
import tensorflow>=2.15.0
import torch>=2.1.0
```

### Forecasting Libraries
```python
import neuralprophet>=0.6.0
import kats>=0.2.0
import darts>=0.25.0
import pyflux>=0.4.18
import arch>=6.2.0
```

### Visualization Libraries
```python
import plotly>=5.17.0
import matplotlib>=3.8.2
import seaborn>=0.13.0
import bokeh>=3.2.0
import altair>=5.1.0
```

### MCP and FastAPI Integration
```python
from mcp.server import FastMCP>=1.0.0
from fastapi>=0.104.1
from pydantic>=2.5.0
```

### Additional Dependencies
```python
from loguru>=0.7.2
import requests>=2.31.0
import aiohttp>=3.9.1
import warnings
import itertools
import warnings
```

## Imports and Decorators

```python
from mcp.server import FastMCP
from loguru import logger
from typing import Dict, Any, List, Optional, Union
import asyncio
import json
import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy import stats
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pmdarima as pm
from prophet import Prophet
import neuralprophet
from kats.consts import TimeSeriesData
from kats.detectors.trend_detector import TrendDetector
from kats.models.prophet import ProphetModel, ProphetParams
from darts import TimeSeries
from darts.models import Prophet as DartsProphet
from darts.models import ExponentialSmoothing as DartsExpSmoothing
from darts.models import ARIMA as DartsARIMA
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import itertools

# MCP Tool Decorator
@self.mcp.tool(description="Advanced trend analysis and forecasting")
```

## Intended Use

- Perform comprehensive trend analysis on time series data
- Generate short-term and long-term forecasts
- Identify trend patterns and seasonal components
- Analyze trend strength and direction
- Support multiple forecasting models and methods
- Provide trend-based insights and recommendations
- Generate trend visualizations and reports
- Support real-time trend monitoring

## Out-of-Scope / Limitations

- Maximum data size: 1GB per analysis
- Maximum time series length: 10,000 data points
- Processing time: Up to 30 minutes for complex trends
- Memory usage: Up to 8GB for large datasets
- Requires sufficient historical data for reliable forecasting
- Some advanced features may require specific data formats
- Real-time trend analysis limited by processing capabilities

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "string",
      "description": "JSON string or array of time series data"
    },
    "time_column": {
      "type": "string",
      "description": "Column name containing timestamps"
    },
    "value_column": {
      "type": "string",
      "description": "Column name containing values to analyze"
    },
    "analysis_type": {
      "type": "string",
      "enum": ["comprehensive", "trend_detection", "forecasting", "seasonal_analysis", "trend_prediction"],
      "default": "comprehensive",
      "description": "Type of trend analysis to perform"
    },
    "forecast_horizon": {
      "type": "integer",
      "default": 12,
      "minimum": 1,
      "maximum": 1000,
      "description": "Number of periods to forecast"
    },
    "forecast_models": {
      "type": "array",
      "items": {"type": "string"},
      "default": ["arima", "prophet", "exponential_smoothing", "neural_prophet"],
      "description": "Forecasting models to use"
    },
    "trend_detection_methods": {
      "type": "array",
      "items": {"type": "string"},
      "default": ["linear_regression", "moving_average", "exponential_smoothing", "mann_kendall"],
      "description": "Methods for trend detection"
    },
    "seasonal_periods": {
      "type": "array",
      "items": {"type": "integer"},
      "default": [7, 30, 365],
      "description": "Seasonal periods to analyze"
    },
    "confidence_level": {
      "type": "number",
      "default": 0.95,
      "minimum": 0.8,
      "maximum": 0.99,
      "description": "Confidence level for forecasts"
    },
    "include_visualizations": {
      "type": "boolean",
      "default": true,
      "description": "Include trend analysis visualizations"
    },
    "include_decomposition": {
      "type": "boolean",
      "default": true,
      "description": "Include seasonal decomposition"
    },
    "include_stationarity_tests": {
      "type": "boolean",
      "default": true,
      "description": "Include stationarity tests"
    },
    "trend_threshold": {
      "type": "number",
      "default": 0.05,
      "minimum": 0.01,
      "maximum": 0.1,
      "description": "Significance threshold for trend detection"
    }
  },
  "required": ["data", "time_column", "value_column"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "analysis_id": {"type": "string"},
    "data_overview": {
      "type": "object",
      "properties": {
        "data_shape": {"type": "object"},
        "time_range": {"type": "object"},
        "data_points": {"type": "number"},
        "processing_time": {"type": "number"}
      }
    },
    "trend_analysis": {
      "type": "object",
      "properties": {
        "trend_detection_methods": {"type": "array"},
        "trend_summary": {
          "type": "object",
          "properties": {
            "trend_direction": {"type": "string"},
            "trend_strength": {"type": "number"},
            "trend_significance": {"type": "boolean"},
            "trend_slope": {"type": "number"},
            "trend_intercept": {"type": "number"}
          }
        },
        "trend_details": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "method": {"type": "string"},
              "trend_direction": {"type": "string"},
              "trend_strength": {"type": "number"},
              "p_value": {"type": "number"},
              "confidence_interval": {"type": "object"},
              "trend_equation": {"type": "string"}
            }
          }
        },
        "trend_breakpoints": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "breakpoint_date": {"type": "string"},
              "breakpoint_index": {"type": "number"},
              "trend_change": {"type": "string"},
              "significance": {"type": "number"}
            }
          }
        }
      }
    },
    "seasonal_analysis": {
      "type": "object",
      "properties": {
        "seasonal_periods_detected": {"type": "array"},
        "seasonal_strength": {"type": "number"},
        "seasonal_patterns": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "period": {"type": "number"},
              "amplitude": {"type": "number"},
              "phase": {"type": "number"},
              "strength": {"type": "number"}
            }
          }
        },
        "decomposition_results": {
          "type": "object",
          "properties": {
            "trend": {"type": "object"},
            "seasonal": {"type": "object"},
            "residual": {"type": "object"}
          }
        }
      }
    },
    "stationarity_tests": {
      "type": "object",
      "properties": {
        "adf_test": {
          "type": "object",
          "properties": {
            "test_statistic": {"type": "number"},
            "p_value": {"type": "number"},
            "critical_values": {"type": "object"},
            "is_stationary": {"type": "boolean"}
          }
        },
        "kpss_test": {
          "type": "object",
          "properties": {
            "test_statistic": {"type": "number"},
            "p_value": {"type": "number"},
            "critical_values": {"type": "object"},
            "is_stationary": {"type": "boolean"}
          }
        }
      }
    },
    "forecasting_results": {
      "type": "object",
      "properties": {
        "forecast_models_used": {"type": "array"},
        "forecast_summary": {
          "type": "object",
          "properties": {
            "forecast_horizon": {"type": "number"},
            "forecast_dates": {"type": "array"},
            "ensemble_forecast": {"type": "array"},
            "confidence_intervals": {"type": "object"}
          }
        },
        "model_performance": {
          "type": "object",
          "properties": {
            "mae": {"type": "object"},
            "rmse": {"type": "object"},
            "mape": {"type": "object"},
            "aic": {"type": "object"},
            "bic": {"type": "object"}
          }
        },
        "individual_forecasts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "model_name": {"type": "string"},
              "forecast_values": {"type": "array"},
              "confidence_intervals": {"type": "object"},
              "model_parameters": {"type": "object"},
              "performance_metrics": {"type": "object"}
            }
          }
        }
      }
    },
    "trend_predictions": {
      "type": "object",
      "properties": {
        "short_term_trend": {
          "type": "object",
          "properties": {
            "direction": {"type": "string"},
            "magnitude": {"type": "number"},
            "confidence": {"type": "number"},
            "timeframe": {"type": "string"}
          }
        },
        "long_term_trend": {
          "type": "object",
          "properties": {
            "direction": {"type": "string"},
            "magnitude": {"type": "number"},
            "confidence": {"type": "number"},
            "timeframe": {"type": "string"}
          }
        },
        "trend_scenarios": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "scenario_name": {"type": "string"},
              "probability": {"type": "number"},
              "trend_direction": {"type": "string"},
              "magnitude": {"type": "number"},
              "timeframe": {"type": "string"}
            }
          }
        }
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "trend_plot_path": {"type": "string"},
        "forecast_plot_path": {"type": "string"},
        "decomposition_plot_path": {"type": "string"},
        "seasonal_plot_path": {"type": "string"},
        "trend_breakpoints_plot_path": {"type": "string"}
      }
    },
    "insights_and_recommendations": {
      "type": "object",
      "properties": {
        "trend_insights": {"type": "array"},
        "forecast_insights": {"type": "array"},
        "seasonal_insights": {"type": "array"},
        "recommendations": {"type": "array"},
        "monitoring_suggestions": {"type": "array"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "analysis_time": {"type": "string"},
        "analysis_type": {"type": "string"},
        "models_used": {"type": "number"},
        "forecast_horizon": {"type": "number"},
        "processing_time": {"type": "number"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "analysis_id", "data_overview"]
}
```

## Example

### Input:
```json
{
  "data": "[{\"date\": \"2024-01-01\", \"sales\": 100}, {\"date\": \"2024-01-02\", \"sales\": 105}, {\"date\": \"2024-01-03\", \"sales\": 110}, {\"date\": \"2024-01-04\", \"sales\": 108}, {\"date\": \"2024-01-05\", \"sales\": 115}]",
  "time_column": "date",
  "value_column": "sales",
  "analysis_type": "comprehensive",
  "forecast_horizon": 7,
  "forecast_models": ["arima", "prophet", "exponential_smoothing"],
  "trend_detection_methods": ["linear_regression", "moving_average"],
  "seasonal_periods": [7, 30],
  "confidence_level": 0.95,
  "include_visualizations": true,
  "include_decomposition": true,
  "include_stationarity_tests": true,
  "trend_threshold": 0.05
}
```

### Output:
```json
{
  "success": true,
  "analysis_id": "trend_20241201_001",
  "data_overview": {
    "data_shape": {
      "rows": 5,
      "columns": 2
    },
    "time_range": {
      "start": "2024-01-01",
      "end": "2024-01-05"
    },
    "data_points": 5,
    "processing_time": 12.5
  },
  "trend_analysis": {
    "trend_detection_methods": ["linear_regression", "moving_average"],
    "trend_summary": {
      "trend_direction": "increasing",
      "trend_strength": 0.85,
      "trend_significance": true,
      "trend_slope": 3.5,
      "trend_intercept": 96.5
    },
    "trend_details": [
      {
        "method": "linear_regression",
        "trend_direction": "increasing",
        "trend_strength": 0.85,
        "p_value": 0.02,
        "confidence_interval": {
          "lower": 1.2,
          "upper": 5.8
        },
        "trend_equation": "sales = 3.5 * time + 96.5"
      },
      {
        "method": "moving_average",
        "trend_direction": "increasing",
        "trend_strength": 0.78,
        "p_value": 0.03,
        "confidence_interval": {
          "lower": 0.8,
          "upper": 4.2
        },
        "trend_equation": "trend = 2.5 * time + 102.5"
      }
    ],
    "trend_breakpoints": []
  },
  "seasonal_analysis": {
    "seasonal_periods_detected": [7],
    "seasonal_strength": 0.45,
    "seasonal_patterns": [
      {
        "period": 7,
        "amplitude": 8.5,
        "phase": 0.3,
        "strength": 0.45
      }
    ],
    "decomposition_results": {
      "trend": {
        "direction": "increasing",
        "slope": 3.5,
        "strength": 0.85
      },
      "seasonal": {
        "period": 7,
        "amplitude": 8.5,
        "strength": 0.45
      },
      "residual": {
        "variance": 4.2,
        "autocorrelation": 0.15
      }
    }
  },
  "stationarity_tests": {
    "adf_test": {
      "test_statistic": -2.45,
      "p_value": 0.12,
      "critical_values": {
        "1%": -3.5,
        "5%": -2.9,
        "10%": -2.6
      },
      "is_stationary": false
    },
    "kpss_test": {
      "test_statistic": 0.85,
      "p_value": 0.01,
      "critical_values": {
        "1%": 0.74,
        "5%": 0.46,
        "10%": 0.35
      },
      "is_stationary": false
    }
  },
  "forecasting_results": {
    "forecast_models_used": ["arima", "prophet", "exponential_smoothing"],
    "forecast_summary": {
      "forecast_horizon": 7,
      "forecast_dates": ["2024-01-06", "2024-01-07", "2024-01-08", "2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12"],
      "ensemble_forecast": [118.5, 122.0, 125.5, 129.0, 132.5, 136.0, 139.5],
      "confidence_intervals": {
        "lower": [115.2, 118.8, 122.4, 126.0, 129.6, 133.2, 136.8],
        "upper": [121.8, 125.2, 128.6, 132.0, 135.4, 138.8, 142.2]
      }
    },
    "model_performance": {
      "mae": {
        "arima": 2.1,
        "prophet": 2.3,
        "exponential_smoothing": 2.0
      },
      "rmse": {
        "arima": 2.8,
        "prophet": 3.1,
        "exponential_smoothing": 2.6
      },
      "mape": {
        "arima": 0.021,
        "prophet": 0.023,
        "exponential_smoothing": 0.020
      },
      "aic": {
        "arima": 15.2,
        "prophet": 16.8,
        "exponential_smoothing": 14.9
      },
      "bic": {
        "arima": 17.5,
        "prophet": 19.1,
        "exponential_smoothing": 17.2
      }
    },
    "individual_forecasts": [
      {
        "model_name": "arima",
        "forecast_values": [118.0, 121.5, 125.0, 128.5, 132.0, 135.5, 139.0],
        "confidence_intervals": {
          "lower": [114.5, 117.8, 121.2, 124.6, 128.0, 131.4, 134.8],
          "upper": [121.5, 125.2, 128.8, 132.4, 136.0, 139.6, 143.2]
        },
        "model_parameters": {
          "order": [1, 1, 1],
          "seasonal_order": [0, 0, 0, 0]
        },
        "performance_metrics": {
          "mae": 2.1,
          "rmse": 2.8,
          "mape": 0.021
        }
      },
      {
        "model_name": "prophet",
        "forecast_values": [119.0, 122.5, 126.0, 129.5, 133.0, 136.5, 140.0],
        "confidence_intervals": {
          "lower": [115.8, 119.2, 122.6, 126.0, 129.4, 132.8, 136.2],
          "upper": [122.2, 125.8, 129.4, 133.0, 136.6, 140.2, 143.8]
        },
        "model_parameters": {
          "changepoint_prior_scale": 0.05,
          "seasonality_prior_scale": 10.0
        },
        "performance_metrics": {
          "mae": 2.3,
          "rmse": 3.1,
          "mape": 0.023
        }
      },
      {
        "model_name": "exponential_smoothing",
        "forecast_values": [118.2, 121.8, 125.4, 129.0, 132.6, 136.2, 139.8],
        "confidence_intervals": {
          "lower": [115.0, 118.5, 122.0, 125.5, 129.0, 132.5, 136.0],
          "upper": [121.4, 125.1, 128.8, 132.5, 136.2, 139.9, 143.6]
        },
        "model_parameters": {
          "trend": "add",
          "seasonal": "add",
          "seasonal_periods": 7
        },
        "performance_metrics": {
          "mae": 2.0,
          "rmse": 2.6,
          "mape": 0.020
        }
      }
    ]
  },
  "trend_predictions": {
    "short_term_trend": {
      "direction": "increasing",
      "magnitude": 3.5,
      "confidence": 0.85,
      "timeframe": "next_7_days"
    },
    "long_term_trend": {
      "direction": "increasing",
      "magnitude": 2.8,
      "confidence": 0.72,
      "timeframe": "next_30_days"
    },
    "trend_scenarios": [
      {
        "scenario_name": "optimistic",
        "probability": 0.25,
        "trend_direction": "increasing",
        "magnitude": 4.2,
        "timeframe": "next_30_days"
      },
      {
        "scenario_name": "baseline",
        "probability": 0.50,
        "trend_direction": "increasing",
        "magnitude": 2.8,
        "timeframe": "next_30_days"
      },
      {
        "scenario_name": "pessimistic",
        "probability": 0.25,
        "trend_direction": "increasing",
        "magnitude": 1.4,
        "timeframe": "next_30_days"
      }
    ]
  },
  "visualizations": {
    "trend_plot_path": "/Results/trend_plot_20241201_001.html",
    "forecast_plot_path": "/Results/forecast_plot_20241201_001.html",
    "decomposition_plot_path": "/Results/decomposition_plot_20241201_001.html",
    "seasonal_plot_path": "/Results/seasonal_plot_20241201_001.html",
    "trend_breakpoints_plot_path": "/Results/breakpoints_plot_20241201_001.html"
  },
  "insights_and_recommendations": {
    "trend_insights": [
      "Strong increasing trend detected with 85% confidence",
      "Trend slope indicates 3.5 unit increase per time period",
      "No significant trend breakpoints detected in the data"
    ],
    "forecast_insights": [
      "Exponential smoothing model performs best (MAE: 2.0)",
      "All models predict continued upward trend",
      "Forecast confidence intervals show moderate uncertainty"
    ],
    "seasonal_insights": [
      "Weekly seasonal pattern detected with moderate strength (45%)",
      "Seasonal amplitude of 8.5 units indicates significant weekly variation",
      "Seasonal component contributes to overall trend stability"
    ],
    "recommendations": [
      "Continue monitoring trend direction and strength",
      "Use exponential smoothing model for short-term forecasts",
      "Consider seasonal adjustments for weekly planning"
    ],
    "monitoring_suggestions": [
      "Track actual vs forecasted values weekly",
      "Monitor for trend breakpoints or changes in direction",
      "Update forecasts monthly with new data"
    ]
  },
  "metadata": {
    "analysis_time": "2024-12-01T10:30:00Z",
    "analysis_type": "comprehensive",
    "models_used": 3,
    "forecast_horizon": 7,
    "processing_time": 12.5
  },
  "errors": [],
  "warnings": [
    "Limited data points (5) may affect forecast reliability",
    "Short time series may not capture long-term seasonal patterns"
  ]
}
```

## Safety & Reliability

- Validates time series data format and requirements
- Implements multiple forecasting models for robustness
- Provides confidence intervals for all forecasts
- Includes trend validation and verification
- Handles various time series formats and frequencies
- Supports missing data handling and interpolation
- Implements proper statistical validation methods
- Provides comprehensive error handling and warnings

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Configure trend analysis parameters in `config/trend_config.py`
3. Set up forecasting model configurations
4. Configure seasonal analysis settings
5. Test with sample time series data before production use

### Usage Examples
```python
# Comprehensive trend analysis
result = await trend_analysis(
    data=time_series_data_json,
    time_column="date",
    value_column="sales",
    analysis_type="comprehensive",
    forecast_horizon=12
)

# Trend detection only
result = await trend_analysis(
    data=time_series_data_json,
    time_column="date",
    value_column="sales",
    analysis_type="trend_detection",
    trend_detection_methods=["linear_regression", "mann_kendall"]
)

# Forecasting only
result = await trend_analysis(
    data=time_series_data_json,
    time_column="date",
    value_column="sales",
    analysis_type="forecasting",
    forecast_models=["arima", "prophet"],
    forecast_horizon=30
)

# Seasonal analysis
result = await trend_analysis(
    data=time_series_data_json,
    time_column="date",
    value_column="sales",
    analysis_type="seasonal_analysis",
    seasonal_periods=[7, 30, 365],
    include_decomposition=True
)
```

### Error Handling
- Invalid time series format: Returns error with format requirements
- Insufficient data: Returns warning with minimum data requirements
- Model fitting failures: Falls back to simpler models
- Memory overflow: Returns error with data size limits
- Missing time column: Returns error with required column list

### Monitoring
- Forecast accuracy metrics tracking
- Trend detection performance monitoring
- Model performance comparison
- Processing time monitoring
- Error rate tracking
- Trend evolution tracking
