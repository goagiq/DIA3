# Advanced Analytics MCP Tools

## Tool Card: advanced_forecasting

### General Info
- **Name**: advanced_forecasting
- **Title**: Advanced Multivariate Forecasting Engine
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Performs advanced multivariate time series forecasting using ensemble models and multiple algorithms.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)
json

# Statistical Analysis
numpy>=1.24.0
pandas>=2.0.0
scipy>=1.10.0

# Machine Learning
scikit-learn>=1.3.0
prophet>=1.1.0
statsmodels>=0.14.0

# Deep Learning
tensorflow>=2.13.0
keras>=2.13.0

# MCP and Strands Integration
mcp>=1.13.0
strands-agents>=1.6.0
strands-agents-tools>=0.2.5

# Additional Dependencies
fastapi>=0.104.0
pydantic>=2.5.0
```

### Imports and Decorators
```python
import asyncio
import logging
import json
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Advanced multivariate forecasting")
async def advanced_forecasting(
    data: str,
    target_variables: str,
    forecast_horizon: int = 10,
    model_type: str = "ensemble"
) -> Dict[str, Any]:
```

### Intended Use
- Time series forecasting
- Business planning and strategy
- Market trend analysis
- Resource allocation planning
- Risk assessment and management

### Out-of-Scope / Limitations
- Requires time series data format
- Limited to supported model types
- Computational intensity for large datasets
- Requires sufficient historical data

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "string",
      "description": "JSON string of time series data"
    },
    "target_variables": {
      "type": "string",
      "description": "JSON string of target variable names"
    },
    "forecast_horizon": {
      "type": "integer",
      "description": "Number of periods to forecast",
      "default": 10
    },
    "model_type": {
      "type": "string",
      "enum": ["ensemble", "prophet", "arima", "lstm", "xgboost"],
      "description": "Type of forecasting model to use",
      "default": "ensemble"
    }
  },
  "required": ["data", "target_variables"]
}
```

### Output Schema
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "result": {
      "type": "object",
      "properties": {
        "forecasts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "variable": {"type": "string"},
              "predictions": {"type": "array"},
              "confidence_intervals": {"type": "object"},
              "model_performance": {"type": "object"}
            }
          }
        },
        "model_metrics": {
          "type": "object",
          "properties": {
            "mae": {"type": "number"},
            "rmse": {"type": "number"},
            "mape": {"type": "number"}
          }
        },
        "processing_time": {"type": "number"}
      }
    }
  },
  "required": ["success", "result"]
}
```

### Example
**Input:**
```json
{
  "data": "[{\"date\": \"2023-01-01\", \"sales\": 100, \"temperature\": 20}, {\"date\": \"2023-01-02\", \"sales\": 120, \"temperature\": 22}]",
  "target_variables": "[\"sales\", \"temperature\"]",
  "forecast_horizon": 7,
  "model_type": "ensemble"
}
```

**Output:**
```json
{
  "success": true,
  "result": {
    "forecasts": [
      {
        "variable": "sales",
        "predictions": [110, 115, 118, 122, 125, 128, 130],
        "confidence_intervals": {
          "lower": [105, 110, 113, 117, 120, 123, 125],
          "upper": [115, 120, 123, 127, 130, 133, 135]
        },
        "model_performance": {
          "mae": 2.3,
          "rmse": 3.1
        }
      }
    ],
    "model_metrics": {
      "mae": 2.3,
      "rmse": 3.1,
      "mape": 0.018
    },
    "processing_time": 15.2
  }
}
```

### Safety & Reliability
- Validates data format and completeness
- Handles missing values appropriately
- Provides confidence intervals
- Model performance validation
- Graceful error handling

---

## Tool Card: causal_analysis

### General Info
- **Name**: causal_analysis
- **Title**: Causal Inference Analysis Engine
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Performs causal inference analysis using various statistical methods including Granger causality.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)
json

# Statistical Analysis
numpy>=1.24.0
pandas>=2.0.0
scipy>=1.10.0
statsmodels>=0.14.0

# Causal Inference
causalnex>=0.12.0
dowhy>=0.8.0
networkx>=3.0

# MCP and Strands Integration
mcp>=1.13.0
strands-agents>=1.6.0
strands-agents-tools>=0.2.5

# Additional Dependencies
fastapi>=0.104.0
pydantic>=2.5.0
```

### Imports and Decorators
```python
import asyncio
import logging
import json
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Causal inference analysis")
async def causal_analysis(
    data: str,
    variables: str,
    analysis_type: str = "granger"
) -> Dict[str, Any]:
```

### Intended Use
- Causal relationship discovery
- Policy impact analysis
- Business decision support
- Research and hypothesis testing
- Risk factor identification

### Out-of-Scope / Limitations
- Requires time series or observational data
- Limited to supported analysis types
- Assumes certain causal assumptions
- May not capture complex interactions

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "string",
      "description": "JSON string of data containing variables"
    },
    "variables": {
      "type": "string",
      "description": "JSON string of variable names to analyze"
    },
    "analysis_type": {
      "type": "string",
      "enum": ["granger", "structural", "instrumental", "propensity"],
      "description": "Type of causal analysis to perform",
      "default": "granger"
    }
  },
  "required": ["data", "variables"]
}
```

### Output Schema
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "result": {
      "type": "object",
      "properties": {
        "causal_relationships": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "cause": {"type": "string"},
              "effect": {"type": "string"},
              "strength": {"type": "number"},
              "p_value": {"type": "number"},
              "confidence": {"type": "number"}
            }
          }
        },
        "causal_graph": {
          "type": "object",
          "description": "Graph representation of causal relationships"
        },
        "model_performance": {
          "type": "object",
          "properties": {
            "r_squared": {"type": "number"},
            "aic": {"type": "number"},
            "bic": {"type": "number"}
          }
        },
        "processing_time": {"type": "number"}
      }
    }
  },
  "required": ["success", "result"]
}
```

### Example
**Input:**
```json
{
  "data": "[{\"advertising\": 100, \"sales\": 1000}, {\"advertising\": 150, \"sales\": 1200}]",
  "variables": "[\"advertising\", \"sales\"]",
  "analysis_type": "granger"
}
```

**Output:**
```json
{
  "success": true,
  "result": {
    "causal_relationships": [
      {
        "cause": "advertising",
        "effect": "sales",
        "strength": 0.85,
        "p_value": 0.001,
        "confidence": 0.95
      }
    ],
    "causal_graph": {
      "nodes": ["advertising", "sales"],
      "edges": [{"from": "advertising", "to": "sales", "weight": 0.85}]
    },
    "model_performance": {
      "r_squared": 0.72,
      "aic": 245.3,
      "bic": 248.1
    },
    "processing_time": 8.5
  }
}
```

### Safety & Reliability
- Validates data quality and completeness
- Provides statistical significance measures
- Handles multicollinearity
- Robust error handling
- Transparent methodology

---

## Tool Card: convert_content_format

### General Info
- **Name**: convert_content_format
- **Title**: Content Format Converter
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Converts content between different formats (text, JSON, XML, CSV, etc.).

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)
json
xml.etree.ElementTree
csv

# Format Conversion
pandas>=2.0.0
openpyxl>=3.1.0
python-docx>=0.8.11

# MCP and Strands Integration
mcp>=1.13.0
strands-agents>=1.6.0
strands-agents-tools>=0.2.5

# Additional Dependencies
fastapi>=0.104.0
pydantic>=2.5.0
```

### Imports and Decorators
```python
import asyncio
import logging
import json
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Format conversion between types")
async def convert_content_format(
    content: str,
    source_format: str,
    target_format: str,
    options: Dict[str, Any] = None
) -> Dict[str, Any]:
```

### Intended Use
- Data format standardization
- Interoperability between systems
- Report generation in different formats
- Data migration and transformation
- API integration support

### Out-of-Scope / Limitations
- Limited to supported format pairs
- May lose some formatting in conversion
- Large files may have performance impact
- Complex nested structures may be simplified

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "content": {
      "type": "string",
      "description": "Content to convert"
    },
    "source_format": {
      "type": "string",
      "enum": ["json", "xml", "csv", "text", "yaml"],
      "description": "Source format of the content"
    },
    "target_format": {
      "type": "string",
      "enum": ["json", "xml", "csv", "text", "yaml", "html"],
      "description": "Target format for conversion"
    },
    "options": {
      "type": "object",
      "description": "Additional conversion options"
    }
  },
  "required": ["content", "source_format", "target_format"]
}
```

### Output Schema
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "result": {
      "type": "object",
      "properties": {
        "converted_content": {"type": "string"},
        "format": {"type": "string"},
        "conversion_metadata": {
          "type": "object",
          "properties": {
            "original_size": {"type": "integer"},
            "converted_size": {"type": "integer"},
            "conversion_time": {"type": "number"}
          }
        }
      }
    }
  },
  "required": ["success", "result"]
}
```

### Example
**Input:**
```json
{
  "content": "{\"name\": \"John\", \"age\": 30, \"city\": \"New York\"}",
  "source_format": "json",
  "target_format": "xml"
}
```

**Output:**
```json
{
  "success": true,
  "result": {
    "converted_content": "<root><name>John</name><age>30</age><city>New York</city></root>",
    "format": "xml",
    "conversion_metadata": {
      "original_size": 45,
      "converted_size": 67,
      "conversion_time": 0.05
    }
  }
}
```

### Safety & Reliability
- Validates input format before conversion
- Preserves data integrity
- Handles encoding issues
- Comprehensive error reporting
- Safe for various content types
