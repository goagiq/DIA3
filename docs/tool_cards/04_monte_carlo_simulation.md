# Tool Card: Monte Carlo Simulation Tools

## General Info

- **Name**: monte_carlo_simulation (Multiple Tools)
- **Title**: Monte Carlo Simulation Engine
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Advanced Monte Carlo simulation tools for risk assessment, scenario analysis, and predictive modeling across multiple domains

## Required Libraries

### Core Python Libraries
```python
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
import random
import math
from datetime import datetime, timedelta
```

### Statistical and Mathematical Libraries
```python
import numpy>=1.24.3
import pandas>=2.1.4
import scipy>=1.11.4
import statsmodels>=0.14.0
import monte-carlo>=0.1.0
```

### Machine Learning Libraries
```python
import scikit-learn>=1.3.2
import torch>=2.1.0
import transformers>=4.35.0
```

### Visualization Libraries
```python
import plotly>=5.17.0
import matplotlib>=3.8.2
import seaborn>=0.13.0
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
```

## Available Monte Carlo Tools

### 1. run_monte_carlo_simulation
- **Description**: Run Monte Carlo simulation with predefined scenarios
- **Use Case**: Standard risk assessment and scenario analysis

### 2. run_custom_monte_carlo_simulation
- **Description**: Run Monte Carlo simulation with custom scenario
- **Use Case**: Custom risk modeling and analysis

### 3. run_time_series_monte_carlo_simulation
- **Description**: Run time series Monte Carlo simulation
- **Use Case**: Temporal risk analysis and forecasting

### 4. run_domain_monte_carlo_simulation
- **Description**: Run domain-specific Monte Carlo simulations
- **Use Case**: Defense, business, financial, cybersecurity domain analysis

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
from datetime import datetime, timedelta
import random

# MCP Tool Decorators
@self.mcp.tool(description="Run Monte Carlo simulation with predefined scenarios")
@self.mcp.tool(description="Run Monte Carlo simulation with custom scenario")
@self.mcp.tool(description="Run time series Monte Carlo simulation")
@self.mcp.tool(description="Run domain-specific Monte Carlo simulation")
```

## Intended Use

- Risk assessment and quantification
- Scenario analysis and planning
- Predictive modeling and forecasting
- Decision support under uncertainty
- Portfolio optimization and management
- Threat assessment and mitigation planning
- Financial modeling and stress testing

## Out-of-Scope / Limitations

- Maximum simulation iterations: 1,000,000
- Processing time: Up to 10 minutes for complex simulations
- Memory usage: Up to 8GB for large simulations
- Requires sufficient historical data for accurate modeling
- Some probability distributions may not be available

## Input Schema

### Standard Monte Carlo Simulation
```json
{
  "type": "object",
  "properties": {
    "scenario_name": {
      "type": "string",
      "description": "Name of predefined scenario to run"
    },
    "iterations": {
      "type": "integer",
      "default": 10000,
      "description": "Number of simulation iterations"
    },
    "time_horizon": {
      "type": "integer",
      "default": 365,
      "description": "Time horizon in days"
    },
    "parameters": {
      "type": "object",
      "description": "Scenario-specific parameters"
    }
  },
  "required": ["scenario_name"]
}
```

### Custom Monte Carlo Simulation
```json
{
  "type": "object",
  "properties": {
    "variables": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "distribution": {"type": "string"},
          "parameters": {"type": "object"}
        }
      },
      "description": "Custom variables and their distributions"
    },
    "model_function": {
      "type": "string",
      "description": "Mathematical model or function to evaluate"
    },
    "iterations": {
      "type": "integer",
      "default": 10000
    },
    "output_metrics": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Metrics to calculate from simulation results"
    }
  },
  "required": ["variables", "model_function"]
}
```

### Time Series Monte Carlo Simulation
```json
{
  "type": "object",
  "properties": {
    "time_series_data": {
      "type": "array",
      "description": "Historical time series data"
    },
    "forecast_periods": {
      "type": "integer",
      "description": "Number of periods to forecast"
    },
    "model_type": {
      "type": "string",
      "enum": ["arima", "garch", "monte_carlo"],
      "default": "monte_carlo"
    },
    "confidence_levels": {
      "type": "array",
      "items": {"type": "number"},
      "default": [0.95, 0.99]
    }
  },
  "required": ["time_series_data", "forecast_periods"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "simulation_id": {"type": "string"},
    "simulation_results": {
      "type": "object",
      "properties": {
        "summary_statistics": {
          "type": "object",
          "properties": {
            "mean": {"type": "number"},
            "median": {"type": "number"},
            "std_dev": {"type": "number"},
            "min": {"type": "number"},
            "max": {"type": "number"},
            "percentiles": {"type": "object"}
          }
        },
        "risk_metrics": {
          "type": "object",
          "properties": {
            "var_95": {"type": "number"},
            "var_99": {"type": "number"},
            "cvar_95": {"type": "number"},
            "cvar_99": {"type": "number"}
          }
        },
        "scenario_analysis": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "scenario": {"type": "string"},
              "probability": {"type": "number"},
              "impact": {"type": "number"}
            }
          }
        },
        "confidence_intervals": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "level": {"type": "number"},
              "lower_bound": {"type": "number"},
              "upper_bound": {"type": "number"}
            }
          }
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "iterations": {"type": "number"},
        "processing_time": {"type": "number"},
        "model_used": {"type": "string"},
        "convergence_status": {"type": "string"}
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "histogram": {"type": "string"},
        "time_series": {"type": "string"},
        "scatter_plot": {"type": "string"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "simulation_id", "simulation_results"]
}
```

## Example

### Input (Standard Simulation):
```json
{
  "scenario_name": "cybersecurity_breach_risk",
  "iterations": 50000,
  "time_horizon": 365,
  "parameters": {
    "attack_probability": 0.1,
    "impact_severity": "high",
    "mitigation_effectiveness": 0.7
  }
}
```

### Output:
```json
{
  "success": true,
  "simulation_id": "mc_20241201_001",
  "simulation_results": {
    "summary_statistics": {
      "mean": 0.15,
      "median": 0.12,
      "std_dev": 0.08,
      "min": 0.01,
      "max": 0.45,
      "percentiles": {
        "5": 0.03,
        "25": 0.08,
        "75": 0.22,
        "95": 0.32
      }
    },
    "risk_metrics": {
      "var_95": 0.28,
      "var_99": 0.38,
      "cvar_95": 0.35,
      "cvar_99": 0.42
    },
    "scenario_analysis": [
      {
        "scenario": "low_impact_breach",
        "probability": 0.65,
        "impact": 0.05
      },
      {
        "scenario": "high_impact_breach",
        "probability": 0.25,
        "impact": 0.25
      },
      {
        "scenario": "critical_breach",
        "probability": 0.10,
        "impact": 0.45
      }
    ],
    "confidence_intervals": [
      {
        "level": 0.95,
        "lower_bound": 0.03,
        "upper_bound": 0.32
      },
      {
        "level": 0.99,
        "lower_bound": 0.01,
        "upper_bound": 0.38
      }
    ]
  },
  "metadata": {
    "iterations": 50000,
    "processing_time": 45.2,
    "model_used": "monte_carlo_risk_model_v2",
    "convergence_status": "converged"
  },
  "visualizations": {
    "histogram": "/Results/mc_histogram_20241201_001.png",
    "time_series": "/Results/mc_timeseries_20241201_001.png",
    "scatter_plot": "/Results/mc_scatter_20241201_001.png"
  },
  "errors": [],
  "warnings": ["Simulation converged after 45,000 iterations"]
}
```

## Safety & Reliability

- Validates all input parameters and distributions
- Implements convergence checking for simulation accuracy
- Provides detailed error messages and warnings
- Includes processing timeouts and resource limits
- Logs all simulation activities for audit trail
- Supports parallel processing for large simulations
- Implements memory management for resource efficiency

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Configure simulation parameters in `config/monte_carlo_config.py`
3. Set up output directories: `mkdir -p Results`
4. Configure parallel processing settings
5. Set up database connections for result storage

### Usage Examples
```python
# Standard scenario simulation
result = await run_monte_carlo_simulation(
    scenario_name="market_risk_assessment",
    iterations=100000,
    time_horizon=252
)

# Custom simulation
result = await run_custom_monte_carlo_simulation(
    variables=[
        {"name": "market_return", "distribution": "normal", "parameters": {"mean": 0.08, "std": 0.15}},
        {"name": "volatility", "distribution": "lognormal", "parameters": {"mean": 0.20, "std": 0.05}}
    ],
    model_function="portfolio_value = initial_value * (1 + market_return) * (1 - volatility)",
    iterations=50000
)

# Time series simulation
result = await run_time_series_monte_carlo_simulation(
    time_series_data=historical_data,
    forecast_periods=30,
    model_type="arima"
)
```

### Error Handling
- Invalid distribution: Returns error with supported distributions
- Insufficient iterations: Returns warning with convergence status
- Memory limit exceeded: Returns partial results with memory warning
- Processing timeout: Returns partial results with timeout warning
- Invalid parameters: Returns detailed parameter validation errors

### Monitoring
- Simulation convergence tracking
- Processing time monitoring
- Memory usage tracking
- Error rate monitoring
- Result accuracy validation
- Resource utilization monitoring
