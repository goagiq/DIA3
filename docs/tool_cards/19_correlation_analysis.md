# Tool Card: correlation_analysis

## General Info

- **Name**: correlation_analysis
- **Title**: Advanced Correlation and Relationship Analysis Engine
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Perform comprehensive correlation analysis, relationship mapping, and dependency detection using advanced statistical and machine learning methods

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

### Correlation Analysis Libraries
```python
import pingouin>=0.5.3
import scipy.stats>=1.11.4
import scipy.special>=1.11.4
import statsmodels.stats>=0.14.0
import statsmodels.stats.correlation_tools>=0.14.0
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

### Network Analysis Libraries
```python
import networkx>=3.2.1
import igraph>=0.10.0
import community>=0.15
import leidenalg>=0.10.0
import python-louvain>=0.16
```

### Visualization Libraries
```python
import plotly>=5.17.0
import matplotlib>=3.8.2
import seaborn>=0.13.0
import bokeh>=3.2.0
import altair>=5.1.0
import plotly.graph_objects as go
import plotly.express as px
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
from scipy.special import comb
import statsmodels.api as sm
from statsmodels.stats.correlation_tools import corr_nearest
import pingouin as pg
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import networkx as nx
import community
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import itertools

# MCP Tool Decorator
@self.mcp.tool(description="Advanced correlation and relationship analysis")
```

## Intended Use

- Perform comprehensive correlation analysis between variables
- Detect linear and non-linear relationships
- Analyze correlation networks and dependencies
- Identify correlation clusters and communities
- Support multiple correlation methods and metrics
- Provide correlation-based insights and recommendations
- Generate correlation visualizations and reports
- Support real-time correlation monitoring

## Out-of-Scope / Limitations

- Maximum data size: 1GB per analysis
- Maximum variables: 1000 per dataset
- Processing time: Up to 30 minutes for complex correlations
- Memory usage: Up to 8GB for large datasets
- Requires sufficient data for reliable correlation analysis
- Some advanced features may require specific data formats
- Real-time correlation analysis limited by processing capabilities

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "string",
      "description": "JSON string or array of data for correlation analysis"
    },
    "variables": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of variables to analyze for correlations"
    },
    "analysis_type": {
      "type": "string",
      "enum": ["comprehensive", "correlation_matrix", "network_analysis", "dependency_analysis", "feature_selection"],
      "default": "comprehensive",
      "description": "Type of correlation analysis to perform"
    },
    "correlation_methods": {
      "type": "array",
      "items": {"type": "string"},
      "default": ["pearson", "spearman", "kendall", "point_biserial", "phi"],
      "description": "Correlation methods to use"
    },
    "include_significance_tests": {
      "type": "boolean",
      "default": true,
      "description": "Include statistical significance tests"
    },
    "include_confidence_intervals": {
      "type": "boolean",
      "default": true,
      "description": "Include confidence intervals"
    },
    "include_network_analysis": {
      "type": "boolean",
      "default": true,
      "description": "Include correlation network analysis"
    },
    "include_feature_selection": {
      "type": "boolean",
      "default": true,
      "description": "Include feature selection analysis"
    },
    "include_visualizations": {
      "type": "boolean",
      "default": true,
      "description": "Include correlation visualizations"
    },
    "correlation_threshold": {
      "type": "number",
      "default": 0.3,
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Threshold for significant correlations"
    },
    "significance_level": {
      "type": "number",
      "default": 0.05,
      "minimum": 0.01,
      "maximum": 0.1,
      "description": "Significance level for statistical tests"
    },
    "confidence_level": {
      "type": "number",
      "default": 0.95,
      "minimum": 0.8,
      "maximum": 0.99,
      "description": "Confidence level for intervals"
    },
    "network_analysis_params": {
      "type": "object",
      "properties": {
        "community_detection": {
          "type": "boolean",
          "default": true
        },
        "centrality_measures": {
          "type": "boolean",
          "default": true
        },
        "clustering_coefficient": {
          "type": "boolean",
          "default": true
        }
      }
    }
  },
  "required": ["data", "variables"]
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
        "variables_analyzed": {"type": "number"},
        "data_points": {"type": "number"},
        "processing_time": {"type": "number"}
      }
    },
    "correlation_analysis": {
      "type": "object",
      "properties": {
        "correlation_methods_used": {"type": "array"},
        "correlation_matrix": {
          "type": "object",
          "properties": {
            "pearson": {"type": "object"},
            "spearman": {"type": "object"},
            "kendall": {"type": "object"}
          }
        },
        "correlation_summary": {
          "type": "object",
          "properties": {
            "total_correlations": {"type": "number"},
            "significant_correlations": {"type": "number"},
            "strong_correlations": {"type": "number"},
            "moderate_correlations": {"type": "number"},
            "weak_correlations": {"type": "number"}
          }
        },
        "correlation_details": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "variable1": {"type": "string"},
              "variable2": {"type": "string"},
              "correlation_method": {"type": "string"},
              "correlation_coefficient": {"type": "number"},
              "p_value": {"type": "number"},
              "significance": {"type": "boolean"},
              "confidence_interval": {"type": "object"},
              "effect_size": {"type": "string"}
            }
          }
        },
        "correlation_clusters": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "cluster_id": {"type": "integer"},
              "variables": {"type": "array"},
              "average_correlation": {"type": "number"},
              "cluster_strength": {"type": "number"}
            }
          }
        }
      }
    },
    "significance_analysis": {
      "type": "object",
      "properties": {
        "significance_tests": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "variable_pair": {"type": "array"},
              "test_statistic": {"type": "number"},
              "p_value": {"type": "number"},
              "significance": {"type": "boolean"},
              "effect_size": {"type": "number"}
            }
          }
        },
        "multiple_testing_correction": {
          "type": "object",
          "properties": {
            "method": {"type": "string"},
            "adjusted_p_values": {"type": "object"},
            "significant_after_correction": {"type": "number"}
          }
        }
      }
    },
    "network_analysis": {
      "type": "object",
      "properties": {
        "network_summary": {
          "type": "object",
          "properties": {
            "nodes": {"type": "number"},
            "edges": {"type": "number"},
            "density": {"type": "number"},
            "average_degree": {"type": "number"},
            "clustering_coefficient": {"type": "number"}
          }
        },
        "centrality_measures": {
          "type": "object",
          "properties": {
            "degree_centrality": {"type": "object"},
            "betweenness_centrality": {"type": "object"},
            "eigenvector_centrality": {"type": "object"},
            "closeness_centrality": {"type": "object"}
          }
        },
        "community_detection": {
          "type": "object",
          "properties": {
            "communities": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "community_id": {"type": "integer"},
                  "variables": {"type": "array"},
                  "size": {"type": "number"},
                  "modularity": {"type": "number"}
                }
              }
            },
            "modularity_score": {"type": "number"}
          }
        },
        "network_metrics": {
          "type": "object",
          "properties": {
            "diameter": {"type": "number"},
            "average_path_length": {"type": "number"},
            "connectivity": {"type": "number"},
            "assortativity": {"type": "number"}
          }
        }
      }
    },
    "dependency_analysis": {
      "type": "object",
      "properties": {
        "mutual_information": {
          "type": "object",
          "properties": {
            "mi_matrix": {"type": "object"},
            "top_dependencies": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "variable1": {"type": "string"},
                  "variable2": {"type": "string"},
                  "mutual_information": {"type": "number"}
                }
              }
            }
          }
        },
        "feature_importance": {
          "type": "object",
          "properties": {
            "random_forest_importance": {"type": "object"},
            "xgboost_importance": {"type": "object"},
            "lightgbm_importance": {"type": "object"}
          }
        },
        "causal_relationships": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "cause": {"type": "string"},
              "effect": {"type": "string"},
              "strength": {"type": "number"},
              "confidence": {"type": "number"}
            }
          }
        }
      }
    },
    "feature_selection": {
      "type": "object",
      "properties": {
        "correlation_based_selection": {
          "type": "object",
          "properties": {
            "selected_features": {"type": "array"},
            "removed_features": {"type": "array"},
            "selection_criteria": {"type": "string"}
          }
        },
        "mutual_information_selection": {
          "type": "object",
          "properties": {
            "selected_features": {"type": "array"},
            "feature_scores": {"type": "object"},
            "selection_threshold": {"type": "number"}
          }
        },
        "ensemble_selection": {
          "type": "object",
          "properties": {
            "selected_features": {"type": "array"},
            "ensemble_scores": {"type": "object"},
            "voting_method": {"type": "string"}
          }
        }
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "correlation_heatmap_path": {"type": "string"},
        "correlation_network_path": {"type": "string"},
        "scatter_plot_matrix_path": {"type": "string"},
        "correlation_distribution_path": {"type": "string"},
        "network_communities_path": {"type": "string"}
      }
    },
    "insights_and_recommendations": {
      "type": "object",
      "properties": {
        "correlation_insights": {"type": "array"},
        "network_insights": {"type": "array"},
        "dependency_insights": {"type": "array"},
        "feature_selection_insights": {"type": "array"},
        "recommendations": {"type": "array"},
        "monitoring_suggestions": {"type": "array"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "analysis_time": {"type": "string"},
        "analysis_type": {"type": "string"},
        "methods_used": {"type": "number"},
        "variables_analyzed": {"type": "number"},
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
  "data": "[{\"age\": 25, \"income\": 50000, \"education\": \"bachelor\", \"satisfaction\": 8.5}, {\"age\": 35, \"income\": 75000, \"education\": \"master\", \"satisfaction\": 7.8}, {\"age\": 28, \"income\": 60000, \"education\": \"bachelor\", \"satisfaction\": 8.2}, {\"age\": 42, \"income\": 90000, \"education\": \"phd\", \"satisfaction\": 9.1}, {\"age\": 31, \"income\": 65000, \"education\": \"master\", \"satisfaction\": 8.0}]",
  "variables": ["age", "income", "education", "satisfaction"],
  "analysis_type": "comprehensive",
  "correlation_methods": ["pearson", "spearman", "kendall"],
  "include_significance_tests": true,
  "include_confidence_intervals": true,
  "include_network_analysis": true,
  "include_feature_selection": true,
  "correlation_threshold": 0.3,
  "significance_level": 0.05,
  "confidence_level": 0.95,
  "network_analysis_params": {
    "community_detection": true,
    "centrality_measures": true,
    "clustering_coefficient": true
  }
}
```

### Output:
```json
{
  "success": true,
  "analysis_id": "correlation_20241201_001",
  "data_overview": {
    "data_shape": {
      "rows": 5,
      "columns": 4
    },
    "variables_analyzed": 4,
    "data_points": 5,
    "processing_time": 8.5
  },
  "correlation_analysis": {
    "correlation_methods_used": ["pearson", "spearman", "kendall"],
    "correlation_matrix": {
      "pearson": {
        "age": {
          "age": 1.0,
          "income": 0.85,
          "education": 0.72,
          "satisfaction": 0.65
        },
        "income": {
          "age": 0.85,
          "income": 1.0,
          "education": 0.78,
          "satisfaction": 0.82
        },
        "education": {
          "age": 0.72,
          "income": 0.78,
          "education": 1.0,
          "satisfaction": 0.68
        },
        "satisfaction": {
          "age": 0.65,
          "income": 0.82,
          "education": 0.68,
          "satisfaction": 1.0
        }
      },
      "spearman": {
        "age": {
          "age": 1.0,
          "income": 0.82,
          "education": 0.68,
          "satisfaction": 0.58
        },
        "income": {
          "age": 0.82,
          "income": 1.0,
          "education": 0.75,
          "satisfaction": 0.78
        },
        "education": {
          "age": 0.68,
          "income": 0.75,
          "education": 1.0,
          "satisfaction": 0.65
        },
        "satisfaction": {
          "age": 0.58,
          "income": 0.78,
          "education": 0.65,
          "satisfaction": 1.0
        }
      },
      "kendall": {
        "age": {
          "age": 1.0,
          "income": 0.78,
          "education": 0.65,
          "satisfaction": 0.52
        },
        "income": {
          "age": 0.78,
          "income": 1.0,
          "education": 0.72,
          "satisfaction": 0.75
        },
        "education": {
          "age": 0.65,
          "income": 0.72,
          "education": 1.0,
          "satisfaction": 0.62
        },
        "satisfaction": {
          "age": 0.52,
          "income": 0.75,
          "education": 0.62,
          "satisfaction": 1.0
        }
      }
    },
    "correlation_summary": {
      "total_correlations": 6,
      "significant_correlations": 5,
      "strong_correlations": 3,
      "moderate_correlations": 2,
      "weak_correlations": 1
    },
    "correlation_details": [
      {
        "variable1": "age",
        "variable2": "income",
        "correlation_method": "pearson",
        "correlation_coefficient": 0.85,
        "p_value": 0.03,
        "significance": true,
        "confidence_interval": {
          "lower": 0.45,
          "upper": 0.98
        },
        "effect_size": "large"
      },
      {
        "variable1": "age",
        "variable2": "income",
        "correlation_method": "spearman",
        "correlation_coefficient": 0.82,
        "p_value": 0.04,
        "significance": true,
        "confidence_interval": {
          "lower": 0.38,
          "upper": 0.96
        },
        "effect_size": "large"
      },
      {
        "variable1": "income",
        "variable2": "satisfaction",
        "correlation_method": "pearson",
        "correlation_coefficient": 0.82,
        "p_value": 0.04,
        "significance": true,
        "confidence_interval": {
          "lower": 0.38,
          "upper": 0.96
        },
        "effect_size": "large"
      }
    ],
    "correlation_clusters": [
      {
        "cluster_id": 0,
        "variables": ["age", "income", "education"],
        "average_correlation": 0.78,
        "cluster_strength": 0.85
      },
      {
        "cluster_id": 1,
        "variables": ["satisfaction"],
        "average_correlation": 0.72,
        "cluster_strength": 0.78
      }
    ]
  },
  "significance_analysis": {
    "significance_tests": [
      {
        "variable_pair": ["age", "income"],
        "test_statistic": 2.85,
        "p_value": 0.03,
        "significance": true,
        "effect_size": 0.85
      },
      {
        "variable_pair": ["income", "satisfaction"],
        "test_statistic": 2.78,
        "p_value": 0.04,
        "significance": true,
        "effect_size": 0.82
      },
      {
        "variable_pair": ["age", "education"],
        "test_statistic": 2.45,
        "p_value": 0.08,
        "significance": false,
        "effect_size": 0.72
      }
    ],
    "multiple_testing_correction": {
      "method": "bonferroni",
      "adjusted_p_values": {
        "age_income": 0.18,
        "income_satisfaction": 0.24,
        "age_education": 0.48
      },
      "significant_after_correction": 0
    }
  },
  "network_analysis": {
    "network_summary": {
      "nodes": 4,
      "edges": 6,
      "density": 1.0,
      "average_degree": 3.0,
      "clustering_coefficient": 0.85
    },
    "centrality_measures": {
      "degree_centrality": {
        "age": 0.75,
        "income": 1.0,
        "education": 0.75,
        "satisfaction": 0.75
      },
      "betweenness_centrality": {
        "age": 0.33,
        "income": 0.67,
        "education": 0.33,
        "satisfaction": 0.33
      },
      "eigenvector_centrality": {
        "age": 0.85,
        "income": 1.0,
        "education": 0.78,
        "satisfaction": 0.82
      },
      "closeness_centrality": {
        "age": 0.75,
        "income": 1.0,
        "education": 0.75,
        "satisfaction": 0.75
      }
    },
    "community_detection": {
      "communities": [
        {
          "community_id": 0,
          "variables": ["age", "income", "education"],
          "size": 3,
          "modularity": 0.25
        },
        {
          "community_id": 1,
          "variables": ["satisfaction"],
          "size": 1,
          "modularity": 0.15
        }
      ],
      "modularity_score": 0.40
    },
    "network_metrics": {
      "diameter": 2,
      "average_path_length": 1.5,
      "connectivity": 1.0,
      "assortativity": 0.45
    }
  },
  "dependency_analysis": {
    "mutual_information": {
      "mi_matrix": {
        "age": {
          "age": 0.0,
          "income": 0.85,
          "education": 0.72,
          "satisfaction": 0.65
        },
        "income": {
          "age": 0.85,
          "income": 0.0,
          "education": 0.78,
          "satisfaction": 0.82
        },
        "education": {
          "age": 0.72,
          "income": 0.78,
          "education": 0.0,
          "satisfaction": 0.68
        },
        "satisfaction": {
          "age": 0.65,
          "income": 0.82,
          "education": 0.68,
          "satisfaction": 0.0
        }
      },
      "top_dependencies": [
        {
          "variable1": "income",
          "variable2": "satisfaction",
          "mutual_information": 0.82
        },
        {
          "variable1": "age",
          "variable2": "income",
          "mutual_information": 0.85
        },
        {
          "variable1": "income",
          "variable2": "education",
          "mutual_information": 0.78
        }
      ]
    },
    "feature_importance": {
      "random_forest_importance": {
        "age": 0.25,
        "income": 0.45,
        "education": 0.20,
        "satisfaction": 0.10
      },
      "xgboost_importance": {
        "age": 0.28,
        "income": 0.42,
        "education": 0.22,
        "satisfaction": 0.08
      },
      "lightgbm_importance": {
        "age": 0.26,
        "income": 0.44,
        "education": 0.21,
        "satisfaction": 0.09
      }
    },
    "causal_relationships": [
      {
        "cause": "age",
        "effect": "income",
        "strength": 0.85,
        "confidence": 0.75
      },
      {
        "cause": "income",
        "effect": "satisfaction",
        "strength": 0.82,
        "confidence": 0.78
      },
      {
        "cause": "education",
        "effect": "income",
        "strength": 0.78,
        "confidence": 0.72
      }
    ]
  },
  "feature_selection": {
    "correlation_based_selection": {
      "selected_features": ["age", "income", "satisfaction"],
      "removed_features": ["education"],
      "selection_criteria": "correlation_threshold_0.3"
    },
    "mutual_information_selection": {
      "selected_features": ["income", "age", "satisfaction"],
      "feature_scores": {
        "income": 0.85,
        "age": 0.82,
        "satisfaction": 0.78,
        "education": 0.72
      },
      "selection_threshold": 0.75
    },
    "ensemble_selection": {
      "selected_features": ["income", "age", "satisfaction"],
      "ensemble_scores": {
        "income": 0.44,
        "age": 0.26,
        "satisfaction": 0.09,
        "education": 0.21
      },
      "voting_method": "majority"
    }
  },
  "visualizations": {
    "correlation_heatmap_path": "/Results/correlation_heatmap_20241201_001.html",
    "correlation_network_path": "/Results/correlation_network_20241201_001.html",
    "scatter_plot_matrix_path": "/Results/scatter_matrix_20241201_001.html",
    "correlation_distribution_path": "/Results/correlation_dist_20241201_001.html",
    "network_communities_path": "/Results/network_communities_20241201_001.html"
  },
  "insights_and_recommendations": {
    "correlation_insights": [
      "Strong positive correlation between age and income (r=0.85)",
      "Income shows highest correlation with satisfaction (r=0.82)",
      "Education has moderate correlations with other variables"
    ],
    "network_insights": [
      "Income is the most central variable in the correlation network",
      "Two distinct communities detected: demographic and satisfaction",
      "Network shows high connectivity with clustering coefficient of 0.85"
    ],
    "dependency_analysis": [
      "Income has highest mutual information with other variables",
      "Age and income show strongest causal relationship",
      "Education has moderate dependency with income"
    ],
    "feature_selection_insights": [
      "Income is consistently ranked as most important feature",
      "Education shows lower importance across all methods",
      "Age and satisfaction are consistently selected features"
    ],
    "recommendations": [
      "Focus on income as primary predictor variable",
      "Consider age-income relationship for targeted interventions",
      "Monitor satisfaction-income correlation for business insights"
    ],
    "monitoring_suggestions": [
      "Track correlation changes over time",
      "Monitor network centrality shifts",
      "Update feature importance rankings regularly"
    ]
  },
  "metadata": {
    "analysis_time": "2024-12-01T10:30:00Z",
    "analysis_type": "comprehensive",
    "methods_used": 3,
    "variables_analyzed": 4,
    "processing_time": 8.5
  },
  "errors": [],
  "warnings": [
    "Limited data points (5) may affect correlation reliability",
    "Multiple testing correction reduced significant correlations to 0"
  ]
}
```

## Safety & Reliability

- Validates data format and variable specifications
- Implements multiple correlation methods for robustness
- Provides confidence intervals and significance tests
- Includes multiple testing corrections
- Handles various data types and formats
- Supports missing data handling
- Implements proper statistical validation methods
- Provides comprehensive error handling and warnings

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Configure correlation analysis parameters in `config/correlation_config.py`
3. Set up network analysis configurations
4. Configure feature selection settings
5. Test with sample data before production use

### Usage Examples
```python
# Comprehensive correlation analysis
result = await correlation_analysis(
    data=dataset_json,
    variables=["age", "income", "education", "satisfaction"],
    analysis_type="comprehensive"
)

# Correlation matrix only
result = await correlation_analysis(
    data=dataset_json,
    variables=["var1", "var2", "var3"],
    analysis_type="correlation_matrix",
    correlation_methods=["pearson", "spearman"]
)

# Network analysis
result = await correlation_analysis(
    data=dataset_json,
    variables=["var1", "var2", "var3", "var4"],
    analysis_type="network_analysis",
    include_network_analysis=True
)

# Feature selection
result = await correlation_analysis(
    data=dataset_json,
    variables=["feature1", "feature2", "feature3"],
    analysis_type="feature_selection",
    include_feature_selection=True
)
```

### Error Handling
- Invalid data format: Returns error with format requirements
- Insufficient data: Returns warning with minimum data requirements
- Correlation calculation failures: Falls back to simpler methods
- Memory overflow: Returns error with data size limits
- Missing variables: Returns error with required variable list

### Monitoring
- Correlation stability monitoring
- Network evolution tracking
- Feature importance changes
- Processing time monitoring
- Error rate tracking
- Correlation drift detection
