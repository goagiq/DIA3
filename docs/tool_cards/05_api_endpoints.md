# Tool Card: API Endpoints

## General Info

- **Name**: API Endpoints (Multiple)
- **Title**: FastAPI REST Endpoints
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: REST API endpoints for content analysis, business intelligence, export functionality, and system management

## Required Libraries

### Core Python Libraries
```python
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import tempfile
import os
from pathlib import Path
```

### FastAPI and Web Framework
```python
from fastapi>=0.104.1
from fastapi.middleware.cors import CORSMiddleware
from pydantic>=2.5.0
import uvicorn[standard]>=0.24.0
```

### Data Processing and Analysis
```python
import pandas>=2.1.4
import numpy>=1.24.3
import scikit-learn>=1.3.2
import transformers>=4.35.0
import torch>=2.1.0
```

### Export and Document Generation
```python
import reportlab>=4.0.7
import python-docx>=1.1.0
import jinja2>=3.1.2
import weasyprint>=60.2
import markdown>=3.5.0
```

### Database and Storage
```python
import chromadb>=0.4.18
import redis>=5.0.1
import psycopg2-binary>=2.9.9
import pymongo>=4.6.0
```

### Additional Dependencies
```python
from loguru>=0.7.2
import requests>=2.31.0
import aiohttp>=3.9.1
import httpx>=0.25.2
import python-multipart>=0.0.6
```

## Available API Endpoints

### Content Analysis Endpoints

#### 1. POST /analyze/text
- **Description**: Analyze text content for sentiment, entities, and insights
- **Use Case**: Text sentiment analysis and entity extraction

#### 2. POST /analyze/image
- **Description**: Analyze image content for sentiment and objects
- **Use Case**: Image analysis and computer vision

#### 3. POST /analyze/audio
- **Description**: Analyze audio content for sentiment and transcription
- **Use Case**: Audio processing and speech analysis

#### 4. POST /analyze/video
- **Description**: Analyze video content for sentiment and objects
- **Use Case**: Video analysis and multimedia processing

#### 5. POST /analyze/webpage
- **Description**: Analyze webpage content for sentiment and insights
- **Use Case**: Web content analysis and scraping

#### 6. POST /analyze/pdf
- **Description**: Analyze PDF documents for sentiment and content
- **Use Case**: Document analysis and text extraction

### Business Intelligence Endpoints

#### 7. POST /business/dashboard
- **Description**: Generate business intelligence dashboard
- **Use Case**: Business analytics and reporting

#### 8. POST /business/executive-summary
- **Description**: Generate executive summary reports
- **Use Case**: Executive reporting and decision support

#### 9. POST /business/visualizations
- **Description**: Generate business visualizations and charts
- **Use Case**: Data visualization and analytics

#### 10. POST /business/intelligence-report
- **Description**: Generate comprehensive business intelligence reports
- **Use Case**: Strategic business analysis

### Export and Document Endpoints

#### 11. POST /export/markdown-to-pdf
- **Description**: Convert markdown content to PDF
- **Use Case**: Document generation and export

#### 12. POST /export/markdown-to-word
- **Description**: Convert markdown content to Word document
- **Use Case**: Document generation and export

#### 13. POST /export/markdown-to-both
- **Description**: Convert markdown to both PDF and Word
- **Use Case**: Multi-format document export

#### 14. GET /export/status/{operation_id}
- **Description**: Check export operation status
- **Use Case**: Export progress monitoring

### Search and Analytics Endpoints

#### 15. POST /semantic/search
- **Description**: Perform semantic search across content
- **Use Case**: Content discovery and retrieval

#### 16. POST /search/knowledge-graph
- **Description**: Query knowledge graph for insights
- **Use Case**: Knowledge discovery and relationship analysis

#### 17. POST /search/combined
- **Description**: Combined semantic and knowledge graph search
- **Use Case**: Comprehensive content search

#### 18. POST /analytics/predictive
- **Description**: Perform predictive analytics
- **Use Case**: Forecasting and trend analysis

### System Management Endpoints

#### 19. GET /health
- **Description**: System health check
- **Use Case**: System monitoring and status

#### 20. GET /models
- **Description**: List available analysis models
- **Use Case**: Model management and selection

#### 21. GET /agents/status
- **Description**: Check agent system status
- **Use Case**: Agent monitoring and management

## Input/Output Schemas

### Content Analysis Request Schema
```json
{
  "type": "object",
  "properties": {
    "content": {
      "type": "string",
      "description": "Content to analyze"
    },
    "content_type": {
      "type": "string",
      "enum": ["text", "image", "audio", "video", "webpage", "pdf"],
      "description": "Type of content"
    },
    "analysis_options": {
      "type": "object",
      "properties": {
        "sentiment": {"type": "boolean", "default": true},
        "entities": {"type": "boolean", "default": true},
        "keywords": {"type": "boolean", "default": true},
        "summary": {"type": "boolean", "default": false}
      }
    },
    "language": {
      "type": "string",
      "default": "auto",
      "description": "Language code or auto-detection"
    }
  },
  "required": ["content", "content_type"]
}
```

### Business Intelligence Request Schema
```json
{
  "type": "object",
  "properties": {
    "business_data": {
      "type": "object",
      "description": "Business data for analysis"
    },
    "report_type": {
      "type": "string",
      "enum": ["dashboard", "executive_summary", "intelligence_report"],
      "description": "Type of business report"
    },
    "timeframe": {
      "type": "string",
      "description": "Analysis timeframe"
    },
    "metrics": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Specific metrics to include"
    }
  },
  "required": ["business_data", "report_type"]
}
```

### Export Request Schema
```json
{
  "type": "object",
  "properties": {
    "content": {
      "type": "string",
      "description": "Content to export"
    },
    "format": {
      "type": "string",
      "enum": ["pdf", "word", "both"],
      "description": "Export format"
    },
    "template": {
      "type": "string",
      "description": "Template to use for export"
    },
    "options": {
      "type": "object",
      "properties": {
        "include_toc": {"type": "boolean", "default": true},
        "page_numbers": {"type": "boolean", "default": true},
        "header_footer": {"type": "boolean", "default": true}
      }
    }
  },
  "required": ["content", "format"]
}
```

## Response Schemas

### Analysis Response Schema
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "analysis_id": {"type": "string"},
    "results": {
      "type": "object",
      "properties": {
        "sentiment": {
          "type": "object",
          "properties": {
            "overall": {"type": "string"},
            "score": {"type": "number"},
            "confidence": {"type": "number"}
          }
        },
        "entities": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "text": {"type": "string"},
              "type": {"type": "string"},
              "confidence": {"type": "number"}
            }
          }
        },
        "keywords": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "keyword": {"type": "string"},
              "relevance": {"type": "number"}
            }
          }
        },
        "summary": {"type": "string"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "processing_time": {"type": "number"},
        "model_used": {"type": "string"},
        "language": {"type": "string"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "analysis_id", "results"]
}
```

### Export Response Schema
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "operation_id": {"type": "string"},
    "status": {
      "type": "string",
      "enum": ["pending", "processing", "completed", "failed"]
    },
    "files": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "format": {"type": "string"},
          "filename": {"type": "string"},
          "size": {"type": "number"},
          "download_url": {"type": "string"}
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "processing_time": {"type": "number"},
        "template_used": {"type": "string"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "operation_id", "status"]
}
```

## Example Usage

### Content Analysis Example
```bash
curl -X POST "http://localhost:8000/analyze/text" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "The new cybersecurity measures are excellent and provide much better protection.",
    "content_type": "text",
    "analysis_options": {
      "sentiment": true,
      "entities": true,
      "keywords": true
    },
    "language": "en"
  }'
```

### Business Intelligence Example
```bash
curl -X POST "http://localhost:8000/business/dashboard" \
  -H "Content-Type: application/json" \
  -d '{
    "business_data": {
      "revenue": [1000000, 1200000, 1100000],
      "expenses": [800000, 900000, 850000],
      "periods": ["Q1", "Q2", "Q3"]
    },
    "report_type": "dashboard",
    "timeframe": "quarterly",
    "metrics": ["revenue", "expenses", "profit_margin"]
  }'
```

### Export Example
```bash
curl -X POST "http://localhost:8000/export/markdown-to-pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Analysis Report\n\nThis is a comprehensive analysis...",
    "format": "pdf",
    "template": "professional",
    "options": {
      "include_toc": true,
      "page_numbers": true
    }
  }'
```

## Safety & Reliability

- Input validation and sanitization
- Rate limiting and request throttling
- Authentication and authorization (where applicable)
- Error handling and detailed error messages
- Request logging and audit trails
- Content filtering and security measures
- Timeout handling and resource management

## Runbook

### Setup Instructions
1. Install dependencies: `pip install -r requirements-phase5.txt`
2. Configure database connections in `config/config.py`
3. Set up Redis for caching and session management
4. Configure export templates and paths
5. Set up authentication and security settings

### API Documentation
- Interactive API docs available at: `http://localhost:8000/docs`
- OpenAPI specification at: `http://localhost:8000/openapi.json`
- ReDoc documentation at: `http://localhost:8000/redoc`

### Error Handling
- HTTP status codes: 200 (success), 400 (bad request), 500 (server error)
- Detailed error messages with error codes
- Validation errors with field-specific messages
- Rate limit exceeded responses
- Timeout and resource limit handling

### Monitoring
- Request/response logging
- Performance metrics tracking
- Error rate monitoring
- API usage statistics
- Response time monitoring
- Resource utilization tracking
