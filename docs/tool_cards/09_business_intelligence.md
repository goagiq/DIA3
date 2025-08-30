# Tool Card: business_intelligence

## General Info

- **Name**: business_intelligence
- **Title**: Business Intelligence Analysis
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Advanced business intelligence analysis with data visualization, trend analysis, and predictive insights

## Required Libraries

### Core Python Libraries
```python
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
import re
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import os
```

### Data Analysis and Statistics Libraries
```python
import numpy>=1.24.3
import pandas>=2.1.4
import scipy>=1.11.4
import statsmodels>=0.14.0
import scikit-learn>=1.3.2
```

### Visualization Libraries
```python
import plotly>=5.17.0
import matplotlib>=3.8.2
import seaborn>=0.13.0
import plotly.graph_objects as go
import plotly.express as px
import dash>=2.14.0
import dash-bootstrap-components>=1.5.0
```

### Machine Learning Libraries
```python
import torch>=2.1.0
import transformers>=4.35.0
import tensorflow>=2.15.0
import keras>=2.15.0
import xgboost>=2.0.0
import lightgbm>=4.1.0
```

### Database and Storage Libraries
```python
import sqlalchemy>=2.0.0
import psycopg2-binary>=2.9.9
import pymongo>=4.6.0
import redis>=5.0.1
import chromadb>=0.4.18
```

### Financial and Business Libraries
```python
import yfinance>=0.2.18
import quandl>=3.7.0
import alpha-vantage>=2.3.1
import pandas-datareader>=0.10.0
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
import jinja2>=3.1.2
import weasyprint>=60.2
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
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import yfinance as yf
from datetime import datetime, timedelta

# MCP Tool Decorator
@self.mcp.tool(description="Business intelligence analysis")
```

## Intended Use

- Perform comprehensive business intelligence analysis
- Generate interactive dashboards and visualizations
- Conduct trend analysis and forecasting
- Provide competitive intelligence insights
- Support strategic decision-making
- Generate executive reports and summaries
- Perform market analysis and segmentation

## Out-of-Scope / Limitations

- Maximum data size: 100MB per analysis
- Processing time: Up to 15 minutes for complex analyses
- Memory usage: Up to 8GB for large datasets
- Requires structured data for optimal analysis
- Some financial data may require API keys
- Real-time data updates limited by source availability

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "analysis_type": {
      "type": "string",
      "enum": ["dashboard", "trend_analysis", "forecasting", "competitive", "market", "financial", "executive_summary"],
      "description": "Type of business intelligence analysis"
    },
    "data_source": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["csv", "json", "database", "api", "excel"],
          "description": "Type of data source"
        },
        "path": {"type": "string"},
        "connection_string": {"type": "string"},
        "api_key": {"type": "string"},
        "query": {"type": "string"}
      },
      "description": "Data source configuration"
    },
    "business_context": {
      "type": "object",
      "properties": {
        "industry": {"type": "string"},
        "company_size": {"type": "string"},
        "region": {"type": "string"},
        "timeframe": {"type": "string"},
        "key_metrics": {"type": "array"}
      },
      "description": "Business context for analysis"
    },
    "analysis_parameters": {
      "type": "object",
      "properties": {
        "forecast_periods": {"type": "integer", "default": 12},
        "confidence_level": {"type": "number", "default": 0.95},
        "segmentation_criteria": {"type": "array"},
        "comparison_metrics": {"type": "array"},
        "visualization_types": {"type": "array"}
      },
      "description": "Analysis-specific parameters"
    },
    "output_format": {
      "type": "string",
      "enum": ["html", "pdf", "json", "excel", "dashboard"],
      "default": "html",
      "description": "Output format for results"
    },
    "include_insights": {
      "type": "boolean",
      "default": true,
      "description": "Include AI-generated insights"
    }
  },
  "required": ["analysis_type", "data_source"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "analysis_id": {"type": "string"},
    "analysis_summary": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "executive_summary": {"type": "string"},
        "key_findings": {"type": "array"},
        "recommendations": {"type": "array"},
        "risk_factors": {"type": "array"}
      }
    },
    "data_analysis": {
      "type": "object",
      "properties": {
        "descriptive_stats": {"type": "object"},
        "trend_analysis": {"type": "object"},
        "correlation_analysis": {"type": "object"},
        "segmentation_results": {"type": "object"},
        "forecast_results": {"type": "object"}
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "charts": {"type": "array"},
        "dashboards": {"type": "array"},
        "interactive_urls": {"type": "array"},
        "export_paths": {"type": "object"}
      }
    },
    "competitive_analysis": {
      "type": "object",
      "properties": {
        "market_position": {"type": "object"},
        "competitor_comparison": {"type": "array"},
        "swot_analysis": {"type": "object"},
        "market_share": {"type": "object"}
      }
    },
    "financial_insights": {
      "type": "object",
      "properties": {
        "financial_metrics": {"type": "object"},
        "ratio_analysis": {"type": "object"},
        "cash_flow_analysis": {"type": "object"},
        "valuation_metrics": {"type": "object"}
      }
    },
    "predictive_models": {
      "type": "object",
      "properties": {
        "forecast_accuracy": {"type": "number"},
        "model_performance": {"type": "object"},
        "scenario_analysis": {"type": "array"},
        "confidence_intervals": {"type": "object"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "analysis_time": {"type": "string"},
        "data_sources_used": {"type": "array"},
        "processing_time": {"type": "number"},
        "model_versions": {"type": "object"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "analysis_id", "analysis_summary"]
}
```

## Example

### Input:
```json
{
  "analysis_type": "dashboard",
  "data_source": {
    "type": "csv",
    "path": "/data/sales_data.csv"
  },
  "business_context": {
    "industry": "technology",
    "company_size": "medium",
    "region": "global",
    "timeframe": "2023-2024",
    "key_metrics": ["revenue", "growth_rate", "customer_satisfaction"]
  },
  "analysis_parameters": {
    "forecast_periods": 6,
    "confidence_level": 0.95,
    "segmentation_criteria": ["region", "product_category"],
    "visualization_types": ["line_chart", "bar_chart", "heatmap", "scatter_plot"]
  },
  "output_format": "html",
  "include_insights": true
}
```

### Output:
```json
{
  "success": true,
  "analysis_id": "bi_20241201_001",
  "analysis_summary": {
    "title": "Technology Company Business Intelligence Dashboard",
    "executive_summary": "The analysis reveals strong revenue growth of 23% YoY, with emerging markets showing the highest potential. Customer satisfaction scores have improved by 15% over the last quarter.",
    "key_findings": [
      "Revenue growth of 23% year-over-year",
      "Emerging markets showing 35% growth rate",
      "Customer satisfaction improved by 15%",
      "Product A is the top performer with 40% market share"
    ],
    "recommendations": [
      "Increase investment in emerging markets",
      "Expand Product A distribution channels",
      "Implement customer feedback loop improvements",
      "Consider strategic partnerships in Asia-Pacific region"
    ],
    "risk_factors": [
      "Supply chain disruptions in Q3",
      "Competitive pressure in mature markets",
      "Regulatory changes in EU region"
    ]
  },
  "data_analysis": {
    "descriptive_stats": {
      "total_revenue": 125000000,
      "average_growth_rate": 0.23,
      "customer_satisfaction_score": 4.2,
      "market_share": 0.18
    },
    "trend_analysis": {
      "revenue_trend": "increasing",
      "growth_acceleration": 0.05,
      "seasonal_patterns": ["Q4 peak", "Q1 dip"],
      "forecast_accuracy": 0.92
    },
    "correlation_analysis": {
      "revenue_customer_satisfaction": 0.78,
      "growth_marketing_spend": 0.65,
      "satisfaction_support_quality": 0.82
    },
    "segmentation_results": {
      "by_region": {
        "North_America": {"revenue": 45000000, "growth": 0.15},
        "Europe": {"revenue": 38000000, "growth": 0.20},
        "Asia_Pacific": {"revenue": 42000000, "growth": 0.35}
      },
      "by_product": {
        "Product_A": {"revenue": 50000000, "market_share": 0.40},
        "Product_B": {"revenue": 35000000, "market_share": 0.28},
        "Product_C": {"revenue": 40000000, "market_share": 0.32}
      }
    },
    "forecast_results": {
      "next_6_months": [130000000, 135000000, 140000000, 145000000, 150000000, 155000000],
      "confidence_intervals": {
        "lower": [125000000, 130000000, 135000000, 140000000, 145000000, 150000000],
        "upper": [135000000, 140000000, 145000000, 150000000, 155000000, 160000000]
      }
    }
  },
  "visualizations": {
    "charts": [
      {
        "type": "line_chart",
        "title": "Revenue Trend Analysis",
        "data": {"x": ["2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4", "2024-Q1"], "y": [100, 110, 115, 120, 125]},
        "insights": "Steady upward trend with seasonal variations"
      },
      {
        "type": "bar_chart",
        "title": "Regional Performance Comparison",
        "data": {"regions": ["NA", "EU", "APAC"], "revenue": [45, 38, 42]},
        "insights": "Asia-Pacific showing strongest growth potential"
      }
    ],
    "dashboards": [
      {
        "name": "Executive Dashboard",
        "url": "http://localhost:8000/dashboard/exec_20241201_001",
        "components": ["revenue_chart", "growth_metrics", "regional_map", "forecast_chart"]
      }
    ],
    "interactive_urls": [
      "http://localhost:8000/dashboard/interactive_20241201_001"
    ],
    "export_paths": {
      "html": "/Results/bi_dashboard_20241201_001.html",
      "pdf": "/Results/bi_report_20241201_001.pdf",
      "excel": "/Results/bi_data_20241201_001.xlsx"
    }
  },
  "competitive_analysis": {
    "market_position": {
      "market_rank": 3,
      "market_share": 0.18,
      "competitive_advantage": "product_innovation",
      "threat_level": "medium"
    },
    "competitor_comparison": [
      {
        "competitor": "Competitor A",
        "market_share": 0.25,
        "strengths": ["brand_recognition", "distribution_network"],
        "weaknesses": ["innovation_speed", "customer_service"]
      }
    ],
    "swot_analysis": {
      "strengths": ["innovative_products", "strong_customer_base", "global_presence"],
      "weaknesses": ["limited_market_share", "high_operating_costs"],
      "opportunities": ["emerging_markets", "digital_transformation", "partnerships"],
      "threats": ["intense_competition", "regulatory_changes", "economic_uncertainty"]
    }
  },
  "financial_insights": {
    "financial_metrics": {
      "gross_margin": 0.65,
      "operating_margin": 0.15,
      "net_margin": 0.12,
      "roi": 0.18
    },
    "ratio_analysis": {
      "current_ratio": 2.1,
      "debt_to_equity": 0.4,
      "asset_turnover": 1.2,
      "inventory_turnover": 8.5
    },
    "cash_flow_analysis": {
      "operating_cash_flow": 18000000,
      "investing_cash_flow": -8000000,
      "financing_cash_flow": -5000000,
      "free_cash_flow": 10000000
    }
  },
  "predictive_models": {
    "forecast_accuracy": 0.92,
    "model_performance": {
      "mape": 0.08,
      "rmse": 2500000,
      "r_squared": 0.89
    },
    "scenario_analysis": [
      {
        "scenario": "optimistic",
        "revenue_forecast": 170000000,
        "probability": 0.25
      },
      {
        "scenario": "baseline",
        "revenue_forecast": 155000000,
        "probability": 0.50
      },
      {
        "scenario": "pessimistic",
        "revenue_forecast": 140000000,
        "probability": 0.25
      }
    ]
  },
  "metadata": {
    "analysis_time": "2024-12-01T10:30:00Z",
    "data_sources_used": ["sales_data.csv", "market_data_api", "customer_surveys"],
    "processing_time": 45.2,
    "model_versions": {
      "forecasting_model": "v2.1.0",
      "segmentation_model": "v1.8.0",
      "insight_generator": "v3.0.0"
    }
  },
  "errors": [],
  "warnings": ["Some data points were missing and interpolated"]
}
```

## Safety & Reliability

- Validates all input data and parameters
- Implements data quality checks and cleaning
- Provides detailed error messages and warnings
- Includes processing timeouts and resource limits
- Logs all analysis activities for audit trail
- Supports data encryption for sensitive information
- Implements access control and security measures

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Configure database connections in `config/database_config.py`
3. Set up API keys for financial data sources
4. Configure visualization server for dashboards
5. Set up data backup and recovery procedures

### Usage Examples
```python
# Create business dashboard
result = await business_intelligence(
    analysis_type="dashboard",
    data_source={"type": "csv", "path": "sales_data.csv"},
    business_context={"industry": "technology", "timeframe": "2023-2024"},
    output_format="html"
)

# Perform trend analysis
result = await business_intelligence(
    analysis_type="trend_analysis",
    data_source={"type": "database", "connection_string": "postgresql://..."},
    analysis_parameters={"forecast_periods": 12, "confidence_level": 0.95}
)

# Generate competitive analysis
result = await business_intelligence(
    analysis_type="competitive",
    data_source={"type": "api", "api_key": "your_api_key"},
    business_context={"industry": "retail", "region": "global"}
)
```

### Error Handling
- Invalid data format: Returns error with format requirements
- Missing data: Returns warning with data quality assessment
- API rate limits: Implements exponential backoff
- Processing timeout: Returns partial results with timeout warning
- Model convergence issues: Falls back to simpler models

### Monitoring
- Analysis performance metrics
- Data quality monitoring
- Model accuracy tracking
- User activity monitoring
- Resource utilization tracking
- Error rate monitoring
