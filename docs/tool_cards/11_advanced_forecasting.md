# Tool Card: advanced_forecasting

## General Info

- **Name**: advanced_forecasting
- **Title**: Advanced Multivariate Forecasting
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Perform advanced multivariate time series forecasting using ensemble models and Monte Carlo simulations

## Required Libraries

### Core Python Libraries
```python
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
```

### Machine Learning Libraries
```python
import scikit-learn>=1.3.2
import tensorflow>=2.15.0
import torch>=2.1.0
import xgboost>=2.0.0
import lightgbm>=4.1.0
import statsmodels>=0.14.0
```

### Time Series Libraries
```python
import prophet>=1.1.4
import pmdarima>=2.0.4
import arch>=6.2.0
import pyflux>=0.4.18
```

### Statistical Libraries
```python
import scipy>=1.11.4
import numpy>=1.24.3
import pandas>=2.1.4
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
import plotly>=5.17.0
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
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import torch
import xgboost as xgb
from datetime import datetime, timedelta

# MCP Tool Decorator
@self.mcp.tool(description="Advanced multivariate forecasting")
```

## Intended Use

- Perform multivariate time series forecasting
- Use ensemble models for improved accuracy
- Generate confidence intervals and uncertainty estimates
- Support multiple forecasting horizons
- Handle seasonal and trend components
- Provide model performance metrics
- Generate forecasting visualizations

## Out-of-Scope / Limitations

- Maximum data size: 1GB per forecasting task
- Maximum forecast horizon: 100 periods
- Processing time: Up to 30 minutes for complex models
- Memory usage: Up to 16GB for large datasets
- Requires sufficient historical data for accurate forecasting
- Some models may not handle all data types

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "string",
      "description": "JSON string or array of time series data"
    },
    "target_variables": {
      "type": "string",
      "description": "JSON string or array of target variable names"
    },
    "forecast_horizon": {
      "type": "integer",
      "default": 10,
      "minimum": 1,
      "maximum": 100,
      "description": "Number of periods to forecast"
    },
    "model_type": {
      "type": "string",
      "enum": ["ensemble", "lstm", "prophet", "arima", "xgboost", "random_forest"],
      "default": "ensemble",
      "description": "Type of forecasting model to use"
    },
    "include_confidence_intervals": {
      "type": "boolean",
      "default": true,
      "description": "Include confidence intervals in output"
    },
    "seasonality": {
      "type": "object",
      "properties": {
        "period": {"type": "integer"},
        "type": {"type": "string", "enum": ["additive", "multiplicative"]}
      },
      "description": "Seasonality configuration"
    },
    "validation_split": {
      "type": "number",
      "default": 0.2,
      "minimum": 0.1,
      "maximum": 0.5,
      "description": "Fraction of data to use for validation"
    }
  },
  "required": ["data", "target_variables"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "forecast_id": {"type": "string"},
    "forecasts": {
      "type": "object",
      "properties": {
        "predictions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "timestamp": {"type": "string"},
              "values": {"type": "object"}
            }
          }
        },
        "confidence_intervals": {
          "type": "object",
          "properties": {
            "lower": {"type": "array"},
            "upper": {"type": "array"}
          }
        }
      }
    },
    "model_performance": {
      "type": "object",
      "properties": {
        "mape": {"type": "number"},
        "rmse": {"type": "number"},
        "mae": {"type": "number"},
        "r_squared": {"type": "number"}
      }
    },
    "model_info": {
      "type": "object",
      "properties": {
        "model_type": {"type": "string"},
        "training_time": {"type": "number"},
        "forecasting_time": {"type": "number"},
        "data_points": {"type": "number"},
        "variables": {"type": "array"}
      }
    },
    "visualization": {
      "type": "object",
      "properties": {
        "html_path": {"type": "string"},
        "image_path": {"type": "string"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "forecast_time": {"type": "string"},
        "model_version": {"type": "string"},
        "data_sources": {"type": "array"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "forecast_id", "forecasts"]
}
```

## Example

### Input:
```json
{
  "data": "[{\"date\": \"2023-01-01\", \"sales\": 100, \"marketing\": 50}, {\"date\": \"2023-01-02\", \"sales\": 120, \"marketing\": 60}]",
  "target_variables": "[\"sales\", \"marketing\"]",
  "forecast_horizon": 12,
  "model_type": "ensemble",
  "include_confidence_intervals": true,
  "seasonality": {
    "period": 7,
    "type": "additive"
  }
}
```

### Output:
```json
{
  "success": true,
  "forecast_id": "forecast_20241201_001",
  "forecasts": {
    "predictions": [
      {
        "timestamp": "2024-01-01",
        "values": {
          "sales": 150.5,
          "marketing": 75.2
        }
      },
      {
        "timestamp": "2024-01-02",
        "values": {
          "sales": 165.3,
          "marketing": 82.1
        }
      }
    ],
    "confidence_intervals": {
      "lower": {
        "sales": [140.2, 155.1],
        "marketing": [70.1, 77.8]
      },
      "upper": {
        "sales": [160.8, 175.5],
        "marketing": [80.3, 86.4]
      }
    }
  },
  "model_performance": {
    "mape": 0.08,
    "rmse": 12.5,
    "mae": 8.3,
    "r_squared": 0.92
  },
  "model_info": {
    "model_type": "ensemble",
    "training_time": 45.2,
    "forecasting_time": 2.1,
    "data_points": 365,
    "variables": ["sales", "marketing"]
  },
  "visualization": {
    "html_path": "/Results/forecast_20241201_001.html",
    "image_path": "/Results/forecast_20241201_001.png"
  },
  "metadata": {
    "forecast_time": "2024-12-01T10:30:00Z",
    "model_version": "2.0.0",
    "data_sources": ["sales_data.csv"]
  },
  "errors": [],
  "warnings": []
}
```

## Safety & Reliability

- Validates input data format and quality
- Implements data preprocessing and cleaning
- Provides model performance validation
- Includes confidence interval calculations
- Handles missing data and outliers
- Supports model ensemble for robustness
- Implements cross-validation for model selection

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Configure forecasting models in `config/forecasting_config.py`
3. Set up data preprocessing pipelines
4. Configure visualization settings
5. Test with sample time series data

### Usage Examples
```python
# Basic multivariate forecasting
result = await advanced_forecasting(
    data=sales_data_json,
    target_variables=["sales", "revenue"],
    forecast_horizon=12,
    model_type="ensemble"
)

# LSTM-based forecasting
result = await advanced_forecasting(
    data=time_series_data,
    target_variables=["demand"],
    forecast_horizon=24,
    model_type="lstm",
    include_confidence_intervals=True
)

# Seasonal forecasting
result = await advanced_forecasting(
    data=seasonal_data,
    target_variables=["temperature"],
    forecast_horizon=52,
    model_type="prophet",
    seasonality={"period": 12, "type": "additive"}
)
```

### Error Handling
- Invalid data format: Returns error with format requirements
- Insufficient data: Returns warning with minimum data requirements
- Model convergence failure: Falls back to simpler models
- Memory overflow: Returns error with data size limits
- Timeout: Returns partial results with timeout warning

### Monitoring
- Model performance metrics
- Forecasting accuracy tracking
- Training time monitoring
- Memory usage tracking
- Error rate monitoring
- Model selection analytics
