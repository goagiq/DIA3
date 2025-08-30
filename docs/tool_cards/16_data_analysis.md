# Tool Card: data_analysis

## General Info

- **Name**: data_analysis
- **Title**: Advanced Data Analysis and Statistics Engine
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Perform comprehensive data analysis and statistical modeling with advanced analytics, hypothesis testing, and data exploration capabilities

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

### Data Analysis Libraries
```python
import pingouin>=0.5.3
import seaborn>=0.13.0
import matplotlib>=3.8.2
import plotly>=5.17.0
import plotly.express as px
import plotly.graph_objects as go
```

### Machine Learning Libraries
```python
import scikit-learn>=1.3.2
import xgboost>=2.0.0
import lightgbm>=4.1.0
import catboost>=1.2.0
```

### Advanced Analytics Libraries
```python
import lifelines>=0.27.8
import scipy.stats>=1.11.4
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.diagnostic import acorr_ljungbox
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
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.diagnostic import acorr_ljungbox
import pingouin as pg
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from datetime import datetime
import warnings
import itertools

# MCP Tool Decorator
@self.mcp.tool(description="Advanced data analysis and statistical modeling")
```

## Intended Use

- Perform comprehensive data analysis and statistical modeling
- Conduct exploratory data analysis (EDA) and data profiling
- Perform hypothesis testing and statistical inference
- Generate descriptive statistics and data summaries
- Conduct correlation analysis and relationship mapping
- Perform outlier detection and anomaly analysis
- Generate data quality reports and validation
- Support time series analysis and forecasting
- Provide data visualization and reporting

## Out-of-Scope / Limitations

- Maximum data size: 1GB per analysis
- Maximum variables: 500 per dataset
- Processing time: Up to 30 minutes for complex analyses
- Memory usage: Up to 8GB for large datasets
- Requires sufficient data for reliable statistical analysis
- Some advanced features may require specific data formats
- Real-time analysis limited by processing capabilities

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "string",
      "description": "JSON string or array of data to analyze"
    },
    "analysis_type": {
      "type": "string",
      "enum": ["comprehensive", "descriptive", "inferential", "correlation", "outlier", "quality", "time_series"],
      "default": "comprehensive",
      "description": "Type of data analysis to perform"
    },
    "variables": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of variables to analyze"
    },
    "target_variable": {
      "type": "string",
      "description": "Target variable for predictive analysis"
    },
    "categorical_variables": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of categorical variables"
    },
    "numerical_variables": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of numerical variables"
    },
    "include_descriptive_stats": {
      "type": "boolean",
      "default": true,
      "description": "Include descriptive statistics"
    },
    "include_correlation_analysis": {
      "type": "boolean",
      "default": true,
      "description": "Include correlation analysis"
    },
    "include_hypothesis_testing": {
      "type": "boolean",
      "default": true,
      "description": "Include hypothesis testing"
    },
    "include_outlier_detection": {
      "type": "boolean",
      "default": true,
      "description": "Include outlier detection"
    },
    "include_data_quality": {
      "type": "boolean",
      "default": true,
      "description": "Include data quality assessment"
    },
    "include_visualizations": {
      "type": "boolean",
      "default": true,
      "description": "Include data analysis visualizations"
    },
    "confidence_level": {
      "type": "number",
      "default": 0.95,
      "minimum": 0.8,
      "maximum": 0.99,
      "description": "Confidence level for statistical tests"
    },
    "missing_data_strategy": {
      "type": "string",
      "enum": ["drop", "impute", "ignore"],
      "default": "impute",
      "description": "Strategy for handling missing data"
    }
  },
  "required": ["data"]
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
        "data_types": {"type": "object"},
        "memory_usage": {"type": "number"},
        "processing_time": {"type": "number"}
      }
    },
    "descriptive_statistics": {
      "type": "object",
      "properties": {
        "numerical_summary": {
          "type": "object",
          "properties": {
            "count": {"type": "object"},
            "mean": {"type": "object"},
            "std": {"type": "object"},
            "min": {"type": "object"},
            "q25": {"type": "object"},
            "q50": {"type": "object"},
            "q75": {"type": "object"},
            "max": {"type": "object"},
            "skewness": {"type": "object"},
            "kurtosis": {"type": "object"}
          }
        },
        "categorical_summary": {
          "type": "object",
          "properties": {
            "value_counts": {"type": "object"},
            "unique_counts": {"type": "object"},
            "mode": {"type": "object"},
            "entropy": {"type": "object"}
          }
        },
        "missing_data_summary": {
          "type": "object",
          "properties": {
            "missing_counts": {"type": "object"},
            "missing_percentages": {"type": "object"},
            "missing_patterns": {"type": "object"}
          }
        }
      }
    },
    "correlation_analysis": {
      "type": "object",
      "properties": {
        "correlation_matrix": {"type": "object"},
        "correlation_significance": {"type": "object"},
        "strong_correlations": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "variable1": {"type": "string"},
              "variable2": {"type": "string"},
              "correlation": {"type": "number"},
              "p_value": {"type": "number"},
              "significance": {"type": "string"}
            }
          }
        },
        "correlation_heatmap_path": {"type": "string"}
      }
    },
    "hypothesis_testing": {
      "type": "object",
      "properties": {
        "normality_tests": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "variable": {"type": "string"},
              "test_statistic": {"type": "number"},
              "p_value": {"type": "number"},
              "is_normal": {"type": "boolean"}
            }
          }
        },
        "t_tests": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "test_type": {"type": "string"},
              "variables": {"type": "array"},
              "test_statistic": {"type": "number"},
              "p_value": {"type": "number"},
              "effect_size": {"type": "number"},
              "confidence_interval": {"type": "object"}
            }
          }
        },
        "anova_tests": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "dependent_variable": {"type": "string"},
              "independent_variables": {"type": "array"},
              "f_statistic": {"type": "number"},
              "p_value": {"type": "number"},
              "effect_size": {"type": "number"}
            }
          }
        },
        "chi_square_tests": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "variables": {"type": "array"},
              "chi_square": {"type": "number"},
              "p_value": {"type": "number"},
              "degrees_of_freedom": {"type": "number"}
            }
          }
        }
      }
    },
    "outlier_detection": {
      "type": "object",
      "properties": {
        "outlier_methods": {
          "type": "array",
          "items": {"type": "string"}
        },
        "outlier_summary": {
          "type": "object",
          "properties": {
            "iqr_outliers": {"type": "object"},
            "zscore_outliers": {"type": "object"},
            "isolation_forest_outliers": {"type": "object"},
            "dbscan_outliers": {"type": "object"}
          }
        },
        "outlier_details": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "variable": {"type": "string"},
              "outlier_indices": {"type": "array"},
              "outlier_values": {"type": "array"},
              "detection_method": {"type": "string"}
            }
          }
        }
      }
    },
    "data_quality_assessment": {
      "type": "object",
      "properties": {
        "data_quality_score": {"type": "number"},
        "quality_metrics": {
          "type": "object",
          "properties": {
            "completeness": {"type": "number"},
            "consistency": {"type": "number"},
            "accuracy": {"type": "number"},
            "timeliness": {"type": "number"},
            "validity": {"type": "number"}
          }
        },
        "data_issues": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "issue_type": {"type": "string"},
              "variable": {"type": "string"},
              "description": {"type": "string"},
              "severity": {"type": "string"},
              "recommendation": {"type": "string"}
            }
          }
        },
        "data_cleaning_suggestions": {"type": "array"}
      }
    },
    "distribution_analysis": {
      "type": "object",
      "properties": {
        "numerical_distributions": {
          "type": "object",
          "properties": {
            "histograms": {"type": "object"},
            "box_plots": {"type": "object"},
            "qq_plots": {"type": "object"}
          }
        },
        "categorical_distributions": {
          "type": "object",
          "properties": {
            "bar_charts": {"type": "object"},
            "pie_charts": {"type": "object"}
          }
        }
      }
    },
    "time_series_analysis": {
      "type": "object",
      "properties": {
        "time_series_components": {
          "type": "object",
          "properties": {
            "trend": {"type": "object"},
            "seasonality": {"type": "object"},
            "residuals": {"type": "object"}
          }
        },
        "stationarity_tests": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "variable": {"type": "string"},
              "adf_statistic": {"type": "number"},
              "adf_p_value": {"type": "number"},
              "kpss_statistic": {"type": "number"},
              "kpss_p_value": {"type": "number"},
              "is_stationary": {"type": "boolean"}
            }
          }
        },
        "autocorrelation_analysis": {"type": "object"}
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "distribution_plots_path": {"type": "string"},
        "correlation_heatmap_path": {"type": "string"},
        "outlier_plots_path": {"type": "string"},
        "quality_dashboard_path": {"type": "string"},
        "time_series_plots_path": {"type": "string"}
      }
    },
    "insights_and_recommendations": {
      "type": "object",
      "properties": {
        "key_insights": {"type": "array"},
        "statistical_insights": {"type": "array"},
        "data_quality_insights": {"type": "array"},
        "recommendations": {"type": "array"},
        "next_steps": {"type": "array"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "analysis_time": {"type": "string"},
        "analysis_type": {"type": "string"},
        "variables_analyzed": {"type": "number"},
        "statistical_tests_performed": {"type": "number"},
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
  "data": "[{\"age\": 25, \"income\": 50000, \"education\": \"bachelor\", \"satisfaction\": 8.5}, {\"age\": 35, \"income\": 75000, \"education\": \"master\", \"satisfaction\": 7.8}, {\"age\": 28, \"income\": 60000, \"education\": \"bachelor\", \"satisfaction\": 8.2}]",
  "analysis_type": "comprehensive",
  "variables": ["age", "income", "education", "satisfaction"],
  "target_variable": "satisfaction",
  "categorical_variables": ["education"],
  "numerical_variables": ["age", "income", "satisfaction"],
  "include_descriptive_stats": true,
  "include_correlation_analysis": true,
  "include_hypothesis_testing": true,
  "include_outlier_detection": true,
  "include_data_quality": true,
  "confidence_level": 0.95,
  "missing_data_strategy": "impute"
}
```

### Output:
```json
{
  "success": true,
  "analysis_id": "data_20241201_001",
  "data_overview": {
    "data_shape": {
      "rows": 3,
      "columns": 4
    },
    "data_types": {
      "age": "int64",
      "income": "int64",
      "education": "object",
      "satisfaction": "float64"
    },
    "memory_usage": 0.0002,
    "processing_time": 2.5
  },
  "descriptive_statistics": {
    "numerical_summary": {
      "count": {
        "age": 3,
        "income": 3,
        "satisfaction": 3
      },
      "mean": {
        "age": 29.33,
        "income": 61666.67,
        "satisfaction": 8.17
      },
      "std": {
        "age": 5.03,
        "income": 12583.06,
        "satisfaction": 0.36
      },
      "min": {
        "age": 25,
        "income": 50000,
        "satisfaction": 7.8
      },
      "q25": {
        "age": 26.5,
        "income": 55000,
        "satisfaction": 8.0
      },
      "q50": {
        "age": 28,
        "income": 60000,
        "satisfaction": 8.2
      },
      "q75": {
        "age": 31.5,
        "income": 67500,
        "satisfaction": 8.35
      },
      "max": {
        "age": 35,
        "income": 75000,
        "satisfaction": 8.5
      },
      "skewness": {
        "age": 0.85,
        "income": 0.85,
        "satisfaction": -0.85
      },
      "kurtosis": {
        "age": -1.5,
        "income": -1.5,
        "satisfaction": -1.5
      }
    },
    "categorical_summary": {
      "value_counts": {
        "education": {
          "bachelor": 2,
          "master": 1
        }
      },
      "unique_counts": {
        "education": 2
      },
      "mode": {
        "education": "bachelor"
      },
      "entropy": {
        "education": 0.92
      }
    },
    "missing_data_summary": {
      "missing_counts": {
        "age": 0,
        "income": 0,
        "education": 0,
        "satisfaction": 0
      },
      "missing_percentages": {
        "age": 0.0,
        "income": 0.0,
        "education": 0.0,
        "satisfaction": 0.0
      },
      "missing_patterns": {}
    }
  },
  "correlation_analysis": {
    "correlation_matrix": {
      "age": {
        "age": 1.0,
        "income": 0.85,
        "satisfaction": -0.85
      },
      "income": {
        "age": 0.85,
        "income": 1.0,
        "satisfaction": -0.85
      },
      "satisfaction": {
        "age": -0.85,
        "income": -0.85,
        "satisfaction": 1.0
      }
    },
    "correlation_significance": {
      "age_income": {
        "correlation": 0.85,
        "p_value": 0.35,
        "significant": false
      },
      "age_satisfaction": {
        "correlation": -0.85,
        "p_value": 0.35,
        "significant": false
      },
      "income_satisfaction": {
        "correlation": -0.85,
        "p_value": 0.35,
        "significant": false
      }
    },
    "strong_correlations": [
      {
        "variable1": "age",
        "variable2": "income",
        "correlation": 0.85,
        "p_value": 0.35,
        "significance": "not_significant"
      },
      {
        "variable1": "age",
        "variable2": "satisfaction",
        "correlation": -0.85,
        "p_value": 0.35,
        "significance": "not_significant"
      },
      {
        "variable1": "income",
        "variable2": "satisfaction",
        "correlation": -0.85,
        "p_value": 0.35,
        "significance": "not_significant"
      }
    ],
    "correlation_heatmap_path": "/Results/correlation_heatmap_20241201_001.html"
  },
  "hypothesis_testing": {
    "normality_tests": [
      {
        "variable": "age",
        "test_statistic": 0.92,
        "p_value": 0.45,
        "is_normal": true
      },
      {
        "variable": "income",
        "test_statistic": 0.92,
        "p_value": 0.45,
        "is_normal": true
      },
      {
        "variable": "satisfaction",
        "test_statistic": 0.92,
        "p_value": 0.45,
        "is_normal": true
      }
    ],
    "t_tests": [
      {
        "test_type": "paired_t_test",
        "variables": ["age", "income"],
        "test_statistic": -2.45,
        "p_value": 0.12,
        "effect_size": 0.85,
        "confidence_interval": {
          "lower": -0.15,
          "upper": 0.15
        }
      }
    ],
    "anova_tests": [
      {
        "dependent_variable": "satisfaction",
        "independent_variables": ["education"],
        "f_statistic": 0.25,
        "p_value": 0.65,
        "effect_size": 0.15
      }
    ],
    "chi_square_tests": []
  },
  "outlier_detection": {
    "outlier_methods": ["iqr", "zscore", "isolation_forest"],
    "outlier_summary": {
      "iqr_outliers": {
        "age": 0,
        "income": 0,
        "satisfaction": 0
      },
      "zscore_outliers": {
        "age": 0,
        "income": 0,
        "satisfaction": 0
      },
      "isolation_forest_outliers": {
        "age": 0,
        "income": 0,
        "satisfaction": 0
      },
      "dbscan_outliers": {
        "age": 0,
        "income": 0,
        "satisfaction": 0
      }
    },
    "outlier_details": []
  },
  "data_quality_assessment": {
    "data_quality_score": 0.95,
    "quality_metrics": {
      "completeness": 1.0,
      "consistency": 0.95,
      "accuracy": 0.90,
      "timeliness": 1.0,
      "validity": 0.95
    },
    "data_issues": [
      {
        "issue_type": "small_sample_size",
        "variable": "all",
        "description": "Sample size is too small for reliable statistical inference",
        "severity": "medium",
        "recommendation": "Collect more data for robust analysis"
      }
    ],
    "data_cleaning_suggestions": [
      "No data cleaning required - data is clean and complete",
      "Consider collecting more samples for better statistical power"
    ]
  },
  "distribution_analysis": {
    "numerical_distributions": {
      "histograms": {
        "age": "/Results/age_histogram_20241201_001.html",
        "income": "/Results/income_histogram_20241201_001.html",
        "satisfaction": "/Results/satisfaction_histogram_20241201_001.html"
      },
      "box_plots": {
        "age": "/Results/age_boxplot_20241201_001.html",
        "income": "/Results/income_boxplot_20241201_001.html",
        "satisfaction": "/Results/satisfaction_boxplot_20241201_001.html"
      },
      "qq_plots": {
        "age": "/Results/age_qqplot_20241201_001.html",
        "income": "/Results/income_qqplot_20241201_001.html",
        "satisfaction": "/Results/satisfaction_qqplot_20241201_001.html"
      }
    },
    "categorical_distributions": {
      "bar_charts": {
        "education": "/Results/education_barchart_20241201_001.html"
      },
      "pie_charts": {
        "education": "/Results/education_piechart_20241201_001.html"
      }
    }
  },
  "time_series_analysis": {
    "time_series_components": {
      "trend": {},
      "seasonality": {},
      "residuals": {}
    },
    "stationarity_tests": [],
    "autocorrelation_analysis": {}
  },
  "visualizations": {
    "distribution_plots_path": "/Results/distributions_20241201_001.html",
    "correlation_heatmap_path": "/Results/correlation_heatmap_20241201_001.html",
    "outlier_plots_path": "/Results/outliers_20241201_001.html",
    "quality_dashboard_path": "/Results/quality_dashboard_20241201_001.html",
    "time_series_plots_path": "/Results/timeseries_20241201_001.html"
  },
  "insights_and_recommendations": {
    "key_insights": [
      "Data shows no missing values and high data quality (95% score)",
      "Sample size is small (3 observations) limiting statistical power",
      "No outliers detected across all variables",
      "All numerical variables show normal distribution patterns"
    ],
    "statistical_insights": [
      "Correlations between variables are not statistically significant due to small sample size",
      "Normality tests indicate normal distribution for all numerical variables",
      "No significant differences found in satisfaction by education level",
      "Paired t-test between age and income shows no significant relationship"
    ],
    "data_quality_insights": [
      "Data completeness is 100% with no missing values",
      "Data consistency is high (95%) with logical value ranges",
      "Data validity is good (95%) with appropriate data types",
      "Small sample size is the primary data quality concern"
    ],
    "recommendations": [
      "Collect larger sample size for more reliable statistical inference",
      "Consider stratified sampling to ensure representation across education levels",
      "Implement data validation rules for future data collection",
      "Use non-parametric tests given the small sample size"
    ],
    "next_steps": [
      "Expand dataset to at least 30 observations per group",
      "Conduct power analysis to determine optimal sample size",
      "Implement automated data quality monitoring",
      "Consider multivariate analysis techniques for larger datasets"
    ]
  },
  "metadata": {
    "analysis_time": "2024-12-01T10:30:00Z",
    "analysis_type": "comprehensive",
    "variables_analyzed": 4,
    "statistical_tests_performed": 5,
    "processing_time": 2.5
  },
  "errors": [],
  "warnings": [
    "Small sample size (3 observations) limits statistical power",
    "Correlation analysis may not be reliable with current sample size"
  ]
}
```

## Safety & Reliability

- Validates data format and variable specifications
- Implements multiple statistical tests for robustness
- Provides confidence intervals and significance levels
- Includes data quality validation and assessment
- Handles various data types and formats
- Supports missing data handling strategies
- Implements proper statistical inference methods
- Provides comprehensive error handling and warnings

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Configure statistical analysis parameters in `config/stats_config.py`
3. Set up data quality assessment rules
4. Configure visualization settings
5. Test with sample data before production use

### Usage Examples
```python
# Comprehensive data analysis
result = await data_analysis(
    data=dataset_json,
    analysis_type="comprehensive",
    variables=["age", "income", "education", "satisfaction"],
    include_descriptive_stats=True,
    include_correlation_analysis=True
)

# Descriptive statistics only
result = await data_analysis(
    data=dataset_json,
    analysis_type="descriptive",
    include_descriptive_stats=True,
    include_visualizations=True
)

# Correlation analysis
result = await data_analysis(
    data=dataset_json,
    analysis_type="correlation",
    include_correlation_analysis=True,
    confidence_level=0.99
)

# Outlier detection
result = await data_analysis(
    data=dataset_json,
    analysis_type="outlier",
    include_outlier_detection=True,
    include_visualizations=True
)
```

### Error Handling
- Invalid data format: Returns error with format requirements
- Insufficient data: Returns warning with minimum data requirements
- Statistical test failures: Falls back to alternative methods
- Memory overflow: Returns error with data size limits
- Missing variables: Returns error with required variable list

### Monitoring
- Statistical test performance metrics
- Data quality assessment accuracy
- Processing time monitoring
- Error rate tracking
- Outlier detection effectiveness
- Correlation analysis reliability
