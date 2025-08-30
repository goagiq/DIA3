# Tool Card: causal_analysis

## General Info

- **Name**: causal_analysis
- **Title**: Causal Inference Analysis
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Perform causal inference analysis using advanced statistical methods and machine learning techniques

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

### Causal Inference Libraries
```python
import dowhy>=0.8
import causalinference>=0.1.3
import linearmodels>=4.27
import pingouin>=0.5.3
```

### Machine Learning Libraries
```python
import tensorflow>=2.15.0
import torch>=2.1.0
import xgboost>=2.0.0
import lightgbm>=4.1.0
```

### Visualization Libraries
```python
import plotly>=5.17.0
import matplotlib>=3.8.2
import seaborn>=0.13.0
import networkx>=3.2.1
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
from statsmodels.stats.outliers_influence import variance_inflation_factor
import dowhy
from dowhy import CausalModel
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# MCP Tool Decorator
@self.mcp.tool(description="Causal inference analysis")
```

## Intended Use

- Perform causal inference analysis on observational data
- Identify causal relationships between variables
- Estimate treatment effects and causal impacts
- Generate causal graphs and structural models
- Provide confidence intervals for causal estimates
- Support multiple causal inference methods
- Generate causal analysis visualizations

## Out-of-Scope / Limitations

- Maximum data size: 500MB per analysis
- Maximum variables: 100 per analysis
- Processing time: Up to 20 minutes for complex analyses
- Memory usage: Up to 8GB for large datasets
- Requires sufficient data for reliable causal inference
- Assumes no unmeasured confounding (unless specified)

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "string",
      "description": "JSON string or array of observational data"
    },
    "variables": {
      "type": "string",
      "description": "JSON string or array of variable names"
    },
    "analysis_type": {
      "type": "string",
      "enum": ["granger", "instrumental_variables", "propensity_score", "structural_equation", "difference_in_differences", "regression_discontinuity"],
      "default": "granger",
      "description": "Type of causal analysis to perform"
    },
    "treatment_variable": {
      "type": "string",
      "description": "Name of the treatment/exposure variable"
    },
    "outcome_variable": {
      "type": "string",
      "description": "Name of the outcome variable"
    },
    "confounders": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of confounding variables"
    },
    "instruments": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of instrumental variables (for IV analysis)"
    },
    "time_variable": {
      "type": "string",
      "description": "Name of the time variable (for time series analysis)"
    },
    "include_visualizations": {
      "type": "boolean",
      "default": true,
      "description": "Include causal analysis visualizations"
    },
    "confidence_level": {
      "type": "number",
      "default": 0.95,
      "minimum": 0.8,
      "maximum": 0.99,
      "description": "Confidence level for inference"
    }
  },
  "required": ["data", "variables", "treatment_variable", "outcome_variable"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "analysis_id": {"type": "string"},
    "causal_estimates": {
      "type": "object",
      "properties": {
        "treatment_effect": {"type": "number"},
        "standard_error": {"type": "number"},
        "confidence_interval": {
          "type": "object",
          "properties": {
            "lower": {"type": "number"},
            "upper": {"type": "number"}
          }
        },
        "p_value": {"type": "number"},
        "effect_size": {"type": "number"}
      }
    },
    "model_diagnostics": {
      "type": "object",
      "properties": {
        "r_squared": {"type": "number"},
        "f_statistic": {"type": "number"},
        "residual_analysis": {"type": "object"},
        "model_assumptions": {"type": "object"}
      }
    },
    "causal_graph": {
      "type": "object",
      "properties": {
        "nodes": {"type": "array"},
        "edges": {"type": "array"},
        "graph_metrics": {"type": "object"}
      }
    },
    "sensitivity_analysis": {
      "type": "object",
      "properties": {
        "robustness_checks": {"type": "array"},
        "bias_analysis": {"type": "object"},
        "confounding_assessment": {"type": "object"}
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "causal_graph_path": {"type": "string"},
        "effect_plot_path": {"type": "string"},
        "diagnostic_plots": {"type": "array"}
      }
    },
    "interpretation": {
      "type": "object",
      "properties": {
        "causal_interpretation": {"type": "string"},
        "limitations": {"type": "array"},
        "recommendations": {"type": "array"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "analysis_time": {"type": "string"},
        "method_used": {"type": "string"},
        "data_points": {"type": "number"},
        "variables_analyzed": {"type": "number"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "analysis_id", "causal_estimates"]
}
```

## Example

### Input:
```json
{
  "data": "[{\"treatment\": 1, \"outcome\": 85, \"age\": 30, \"education\": 16}, {\"treatment\": 0, \"outcome\": 72, \"age\": 28, \"education\": 14}]",
  "variables": "[\"treatment\", \"outcome\", \"age\", \"education\"]",
  "analysis_type": "propensity_score",
  "treatment_variable": "treatment",
  "outcome_variable": "outcome",
  "confounders": ["age", "education"],
  "include_visualizations": true,
  "confidence_level": 0.95
}
```

### Output:
```json
{
  "success": true,
  "analysis_id": "causal_20241201_001",
  "causal_estimates": {
    "treatment_effect": 8.5,
    "standard_error": 2.1,
    "confidence_interval": {
      "lower": 4.4,
      "upper": 12.6
    },
    "p_value": 0.001,
    "effect_size": 0.42
  },
  "model_diagnostics": {
    "r_squared": 0.78,
    "f_statistic": 45.2,
    "residual_analysis": {
      "normality_test": "passed",
      "homoscedasticity": "passed",
      "independence": "passed"
    },
    "model_assumptions": {
      "linearity": "satisfied",
      "multicollinearity": "low",
      "outliers": "none_detected"
    }
  },
  "causal_graph": {
    "nodes": [
      {"id": "treatment", "type": "exposure"},
      {"id": "outcome", "type": "outcome"},
      {"id": "age", "type": "confounder"},
      {"id": "education", "type": "confounder"}
    ],
    "edges": [
      {"source": "age", "target": "treatment"},
      {"source": "education", "target": "treatment"},
      {"source": "treatment", "target": "outcome"},
      {"source": "age", "target": "outcome"},
      {"source": "education", "target": "outcome"}
    ],
    "graph_metrics": {
      "node_count": 4,
      "edge_count": 5,
      "density": 0.83
    }
  },
  "sensitivity_analysis": {
    "robustness_checks": [
      "propensity_score_matching",
      "inverse_probability_weighting",
      "doubly_robust_estimation"
    ],
    "bias_analysis": {
      "selection_bias": "low",
      "measurement_bias": "low",
      "confounding_bias": "controlled"
    },
    "confounding_assessment": {
      "unmeasured_confounding": "minimal_risk",
      "sensitivity_parameter": 0.15
    }
  },
  "visualizations": {
    "causal_graph_path": "/Results/causal_graph_20241201_001.html",
    "effect_plot_path": "/Results/effect_plot_20241201_001.html",
    "diagnostic_plots": [
      "/Results/residual_plot_20241201_001.html",
      "/Results/propensity_score_plot_20241201_001.html"
    ]
  },
  "interpretation": {
    "causal_interpretation": "The treatment has a statistically significant positive effect on the outcome, with an estimated causal effect of 8.5 units (95% CI: 4.4, 12.6). This effect is robust across multiple estimation methods.",
    "limitations": [
      "Assumes no unmeasured confounding",
      "Limited to observed variables",
      "Requires strong ignorability assumption"
    ],
    "recommendations": [
      "Conduct sensitivity analysis for unmeasured confounding",
      "Validate results with experimental data if possible",
      "Consider alternative causal inference methods"
    ]
  },
  "metadata": {
    "analysis_time": "2024-12-01T10:30:00Z",
    "method_used": "propensity_score_matching",
    "data_points": 1000,
    "variables_analyzed": 4
  },
  "errors": [],
  "warnings": []
}
```

## Safety & Reliability

- Validates data quality and assumptions
- Implements multiple robustness checks
- Provides sensitivity analysis for key assumptions
- Includes diagnostic tests for model validity
- Handles missing data appropriately
- Supports multiple causal inference methods
- Implements proper statistical inference

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Configure causal inference libraries in `config/causal_config.py`
3. Set up visualization settings
4. Configure statistical analysis parameters
5. Test with sample data before production use

### Usage Examples
```python
# Basic causal analysis
result = await causal_analysis(
    data=observational_data_json,
    variables=["treatment", "outcome", "age", "education"],
    analysis_type="propensity_score",
    treatment_variable="treatment",
    outcome_variable="outcome",
    confounders=["age", "education"]
)

# Granger causality analysis
result = await causal_analysis(
    data=time_series_data,
    variables=["gdp", "unemployment", "inflation"],
    analysis_type="granger",
    treatment_variable="gdp",
    outcome_variable="unemployment",
    time_variable="date"
)

# Instrumental variables analysis
result = await causal_analysis(
    data=iv_data,
    variables=["education", "income", "ability"],
    analysis_type="instrumental_variables",
    treatment_variable="education",
    outcome_variable="income",
    instruments=["compulsory_schooling"]
)
```

### Error Handling
- Invalid data format: Returns error with format requirements
- Insufficient data: Returns warning with minimum data requirements
- Model convergence failure: Falls back to simpler methods
- Assumption violations: Returns detailed diagnostic information
- Missing variables: Returns error with required variable list

### Monitoring
- Model performance metrics
- Causal effect estimation accuracy
- Assumption validation results
- Sensitivity analysis outcomes
- Error rate monitoring
- Computational efficiency tracking
