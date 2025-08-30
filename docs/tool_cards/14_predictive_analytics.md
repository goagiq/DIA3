# Tool Card: predictive_analytics

## General Info

- **Name**: predictive_analytics
- **Title**: Advanced Predictive Analytics with Machine Learning
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Perform advanced predictive analytics using ensemble machine learning models with comprehensive feature engineering and model selection

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

### Machine Learning Libraries
```python
import scikit-learn>=1.3.2
import tensorflow>=2.15.0
import torch>=2.1.0
import xgboost>=2.0.0
import lightgbm>=4.1.0
import catboost>=1.2.0
```

### Statistical Libraries
```python
import scipy>=1.11.4
import statsmodels>=0.14.0
import numpy>=1.24.3
import pandas>=2.1.4
```

### Feature Engineering Libraries
```python
import feature-engine>=1.6.0
import category_encoders>=2.6.0
import imbalanced-learn>=0.11.0
import optuna>=3.4.0
```

### Visualization Libraries
```python
import plotly>=5.17.0
import matplotlib>=3.8.2
import seaborn>=0.13.0
import shap>=0.44.0
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
import joblib>=1.3.2
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
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
import tensorflow as tf
import torch
import shap
import optuna
from datetime import datetime
import joblib

# MCP Tool Decorator
@self.mcp.tool(description="Advanced predictive analytics with ensemble machine learning")
```

## Intended Use

- Perform predictive analytics on structured and unstructured data
- Build ensemble machine learning models for classification and regression
- Conduct comprehensive feature engineering and selection
- Generate predictive insights and forecasts
- Provide model interpretability and explainability
- Support automated model selection and hyperparameter tuning
- Generate predictive analytics reports and visualizations

## Out-of-Scope / Limitations

- Maximum data size: 2GB per analysis
- Maximum features: 1000 per model
- Processing time: Up to 45 minutes for complex models
- Memory usage: Up to 16GB for large datasets
- Requires sufficient training data for reliable predictions
- Some advanced models may require GPU acceleration

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "string",
      "description": "JSON string or array of training data"
    },
    "target_variable": {
      "type": "string",
      "description": "Name of the target variable to predict"
    },
    "problem_type": {
      "type": "string",
      "enum": ["classification", "regression", "time_series", "anomaly_detection"],
      "default": "classification",
      "description": "Type of predictive problem"
    },
    "model_types": {
      "type": "array",
      "items": {"type": "string"},
      "default": ["random_forest", "xgboost", "lightgbm", "neural_network"],
      "description": "Types of models to include in ensemble"
    },
    "feature_engineering": {
      "type": "object",
      "properties": {
        "include_feature_selection": {"type": "boolean", "default": true},
        "include_feature_scaling": {"type": "boolean", "default": true},
        "include_categorical_encoding": {"type": "boolean", "default": true},
        "include_polynomial_features": {"type": "boolean", "default": false}
      },
      "description": "Feature engineering options"
    },
    "hyperparameter_tuning": {
      "type": "object",
      "properties": {
        "enable_tuning": {"type": "boolean", "default": true},
        "optimization_method": {"type": "string", "enum": ["optuna", "grid_search", "random_search"], "default": "optuna"},
        "n_trials": {"type": "integer", "default": 100, "minimum": 10, "maximum": 1000}
      },
      "description": "Hyperparameter tuning configuration"
    },
    "validation_strategy": {
      "type": "string",
      "enum": ["train_test_split", "cross_validation", "time_series_split"],
      "default": "train_test_split",
      "description": "Validation strategy for model evaluation"
    },
    "include_interpretability": {
      "type": "boolean",
      "default": true,
      "description": "Include model interpretability analysis"
    },
    "include_visualizations": {
      "type": "boolean",
      "default": true,
      "description": "Include predictive analytics visualizations"
    },
    "test_size": {
      "type": "number",
      "default": 0.2,
      "minimum": 0.1,
      "maximum": 0.5,
      "description": "Fraction of data to use for testing"
    }
  },
  "required": ["data", "target_variable"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "analysis_id": {"type": "string"},
    "model_performance": {
      "type": "object",
      "properties": {
        "best_model": {"type": "string"},
        "overall_accuracy": {"type": "number"},
        "precision": {"type": "number"},
        "recall": {"type": "number"},
        "f1_score": {"type": "number"},
        "roc_auc": {"type": "number"},
        "model_comparison": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "model_name": {"type": "string"},
              "accuracy": {"type": "number"},
              "training_time": {"type": "number"},
              "prediction_time": {"type": "number"}
            }
          }
        }
      }
    },
    "feature_importance": {
      "type": "object",
      "properties": {
        "top_features": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "feature_name": {"type": "string"},
              "importance_score": {"type": "number"},
              "feature_type": {"type": "string"}
            }
          }
        },
        "feature_correlation_matrix": {"type": "object"},
        "feature_selection_results": {"type": "object"}
      }
    },
    "predictions": {
      "type": "object",
      "properties": {
        "test_predictions": {"type": "array"},
        "prediction_probabilities": {"type": "array"},
        "confidence_intervals": {"type": "object"},
        "prediction_metadata": {"type": "object"}
      }
    },
    "model_interpretability": {
      "type": "object",
      "properties": {
        "shap_values": {"type": "object"},
        "feature_contributions": {"type": "array"},
        "decision_paths": {"type": "array"},
        "model_explanations": {"type": "object"}
      }
    },
    "hyperparameter_optimization": {
      "type": "object",
      "properties": {
        "best_parameters": {"type": "object"},
        "optimization_history": {"type": "array"},
        "parameter_importance": {"type": "object"},
        "optimization_metrics": {"type": "object"}
      }
    },
    "data_quality_report": {
      "type": "object",
      "properties": {
        "missing_values": {"type": "object"},
        "data_types": {"type": "object"},
        "outliers": {"type": "object"},
        "data_distribution": {"type": "object"}
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "performance_plots_path": {"type": "string"},
        "feature_importance_plot_path": {"type": "string"},
        "prediction_plots_path": {"type": "string"},
        "model_comparison_plot_path": {"type": "string"},
        "shap_summary_plot_path": {"type": "string"}
      }
    },
    "model_artifacts": {
      "type": "object",
      "properties": {
        "model_file_path": {"type": "string"},
        "preprocessor_file_path": {"type": "string"},
        "feature_names": {"type": "array"},
        "model_metadata": {"type": "object"}
      }
    },
    "insights_and_recommendations": {
      "type": "object",
      "properties": {
        "key_insights": {"type": "array"},
        "model_recommendations": {"type": "array"},
        "feature_recommendations": {"type": "array"},
        "deployment_considerations": {"type": "array"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "analysis_time": {"type": "string"},
        "problem_type": {"type": "string"},
        "data_shape": {"type": "object"},
        "processing_time": {"type": "number"},
        "models_trained": {"type": "number"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "analysis_id", "model_performance"]
}
```

## Example

### Input:
```json
{
  "data": "[{\"age\": 25, \"income\": 50000, \"education\": \"bachelor\", \"target\": 1}, {\"age\": 35, \"income\": 75000, \"education\": \"master\", \"target\": 0}]",
  "target_variable": "target",
  "problem_type": "classification",
  "model_types": ["random_forest", "xgboost", "lightgbm"],
  "feature_engineering": {
    "include_feature_selection": true,
    "include_feature_scaling": true,
    "include_categorical_encoding": true
  },
  "hyperparameter_tuning": {
    "enable_tuning": true,
    "optimization_method": "optuna",
    "n_trials": 50
  },
  "include_interpretability": true,
  "test_size": 0.2
}
```

### Output:
```json
{
  "success": true,
  "analysis_id": "predictive_20241201_001",
  "model_performance": {
    "best_model": "xgboost",
    "overall_accuracy": 0.92,
    "precision": 0.89,
    "recall": 0.94,
    "f1_score": 0.91,
    "roc_auc": 0.95,
    "model_comparison": [
      {
        "model_name": "xgboost",
        "accuracy": 0.92,
        "training_time": 15.2,
        "prediction_time": 0.05
      },
      {
        "model_name": "random_forest",
        "accuracy": 0.89,
        "training_time": 8.5,
        "prediction_time": 0.12
      },
      {
        "model_name": "lightgbm",
        "accuracy": 0.91,
        "training_time": 12.8,
        "prediction_time": 0.03
      }
    ]
  },
  "feature_importance": {
    "top_features": [
      {
        "feature_name": "income",
        "importance_score": 0.45,
        "feature_type": "numerical"
      },
      {
        "feature_name": "age",
        "importance_score": 0.32,
        "feature_type": "numerical"
      },
      {
        "feature_name": "education",
        "importance_score": 0.23,
        "feature_type": "categorical"
      }
    ],
    "feature_correlation_matrix": {
      "income_age": 0.65,
      "income_education": 0.42,
      "age_education": 0.28
    },
    "feature_selection_results": {
      "selected_features": ["income", "age", "education"],
      "feature_selection_method": "recursive_feature_elimination"
    }
  },
  "predictions": {
    "test_predictions": [1, 0, 1, 0, 1],
    "prediction_probabilities": [0.85, 0.12, 0.78, 0.23, 0.91],
    "confidence_intervals": {
      "lower": [0.72, 0.08, 0.65, 0.15, 0.82],
      "upper": [0.98, 0.16, 0.91, 0.31, 1.00]
    },
    "prediction_metadata": {
      "prediction_count": 100,
      "average_confidence": 0.82,
      "prediction_distribution": {"0": 45, "1": 55}
    }
  },
  "model_interpretability": {
    "shap_values": {
      "income": 0.45,
      "age": 0.32,
      "education": 0.23
    },
    "feature_contributions": [
      {
        "feature": "income",
        "contribution": 0.45,
        "direction": "positive"
      },
      {
        "feature": "age",
        "contribution": 0.32,
        "direction": "positive"
      }
    ],
    "decision_paths": [
      "income > 60000 AND age > 30 -> target = 1",
      "income <= 60000 OR age <= 30 -> target = 0"
    ],
    "model_explanations": {
      "global_explanation": "Income and age are the most important predictors",
      "local_explanations": ["High income individuals are more likely to be in target class"]
    }
  },
  "hyperparameter_optimization": {
    "best_parameters": {
      "n_estimators": 200,
      "max_depth": 6,
      "learning_rate": 0.1,
      "subsample": 0.8
    },
    "optimization_history": [
      {"trial": 1, "accuracy": 0.85},
      {"trial": 2, "accuracy": 0.88},
      {"trial": 50, "accuracy": 0.92}
    ],
    "parameter_importance": {
      "max_depth": 0.35,
      "learning_rate": 0.28,
      "n_estimators": 0.22,
      "subsample": 0.15
    },
    "optimization_metrics": {
      "best_score": 0.92,
      "optimization_time": 45.2,
      "trials_completed": 50
    }
  },
  "data_quality_report": {
    "missing_values": {
      "age": 0,
      "income": 0,
      "education": 0,
      "target": 0
    },
    "data_types": {
      "age": "int64",
      "income": "int64",
      "education": "object",
      "target": "int64"
    },
    "outliers": {
      "income": 5,
      "age": 2
    },
    "data_distribution": {
      "target": {"0": 45, "1": 55},
      "education": {"bachelor": 60, "master": 40}
    }
  },
  "visualizations": {
    "performance_plots_path": "/Results/performance_plots_20241201_001.html",
    "feature_importance_plot_path": "/Results/feature_importance_20241201_001.html",
    "prediction_plots_path": "/Results/prediction_plots_20241201_001.html",
    "model_comparison_plot_path": "/Results/model_comparison_20241201_001.html",
    "shap_summary_plot_path": "/Results/shap_summary_20241201_001.html"
  },
  "model_artifacts": {
    "model_file_path": "/models/xgboost_model_20241201_001.pkl",
    "preprocessor_file_path": "/models/preprocessor_20241201_001.pkl",
    "feature_names": ["income", "age", "education"],
    "model_metadata": {
      "model_type": "xgboost",
      "version": "2.0.0",
      "training_date": "2024-12-01T10:30:00Z"
    }
  },
  "insights_and_recommendations": {
    "key_insights": [
      "Income is the most important predictor with 45% importance",
      "XGBoost model achieved the best performance with 92% accuracy",
      "Feature engineering improved model performance by 8%"
    ],
    "model_recommendations": [
      "Use XGBoost for production deployment",
      "Consider ensemble methods for improved robustness",
      "Monitor model performance over time"
    ],
    "feature_recommendations": [
      "Collect additional income-related features",
      "Consider feature interactions for improved performance",
      "Regularize features to prevent overfitting"
    ],
    "deployment_considerations": [
      "Implement model versioning and monitoring",
      "Set up automated retraining pipelines",
      "Establish model performance thresholds"
    ]
  },
  "metadata": {
    "analysis_time": "2024-12-01T10:30:00Z",
    "problem_type": "classification",
    "data_shape": {"rows": 1000, "columns": 4},
    "processing_time": 67.8,
    "models_trained": 3
  },
  "errors": [],
  "warnings": []
}
```

## Safety & Reliability

- Validates data quality and format requirements
- Implements cross-validation for robust model evaluation
- Provides confidence intervals for predictions
- Includes model interpretability and explainability
- Handles missing data and outliers appropriately
- Supports automated hyperparameter optimization
- Implements proper model validation and testing

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Configure machine learning models in `config/ml_config.py`
3. Set up feature engineering pipelines
4. Configure hyperparameter optimization settings
5. Test with sample data before production use

### Usage Examples
```python
# Basic classification
result = await predictive_analytics(
    data=classification_data_json,
    target_variable="target",
    problem_type="classification",
    model_types=["random_forest", "xgboost"]
)

# Regression with feature engineering
result = await predictive_analytics(
    data=regression_data_json,
    target_variable="price",
    problem_type="regression",
    feature_engineering={
        "include_feature_selection": True,
        "include_polynomial_features": True
    }
)

# Time series forecasting
result = await predictive_analytics(
    data=time_series_data_json,
    target_variable="sales",
    problem_type="time_series",
    validation_strategy="time_series_split"
)
```

### Error Handling
- Invalid data format: Returns error with format requirements
- Insufficient data: Returns warning with minimum data requirements
- Model convergence failure: Falls back to simpler models
- Memory overflow: Returns error with data size limits
- Feature engineering failure: Returns error with feature requirements

### Monitoring
- Model performance metrics tracking
- Prediction accuracy monitoring
- Feature importance stability
- Model drift detection
- Hyperparameter optimization progress
- Computational resource usage
