# Tool Card: generate_enhanced_report

## General Info

- **Name**: generate_enhanced_report
- **Title**: Enhanced Report Generation with Interactive Visualizations
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Generate enhanced reports for any topic with interactive visualizations, advanced tooltips, and comprehensive analysis

## Required Libraries

### Core Python Libraries
```python
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import tempfile
import os
from datetime import datetime
```

### Web and HTML Generation
```python
import jinja2>=3.1.2
import weasyprint>=60.2
import markdown>=3.5.0
import html5lib>=1.1
```

### Data Visualization
```python
import plotly>=5.17.0
import matplotlib>=3.8.2
import seaborn>=0.13.0
import mermaid-cli>=10.6.1
```

### Data Processing
```python
import pandas>=2.1.4
import numpy>=1.24.3
import scikit-learn>=1.3.2
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
import chromadb>=0.4.18
```

## Imports and Decorators

```python
from mcp.server import FastMCP
from loguru import logger
from typing import Dict, Any, List, Optional, Union
import asyncio
import json
import jinja2
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import tempfile
import os

# MCP Tool Decorator
@self.mcp.tool(description="Enhanced report generation with 22 modules and advanced tooltips")
```

## Intended Use

- Generate comprehensive reports for any topic or domain
- Create interactive HTML reports with advanced visualizations
- Include 22 modular analysis components
- Provide source tracking and tooltips
- Support multiple output formats (HTML, PDF, Word)
- Generate executive summaries and detailed analysis

## Out-of-Scope / Limitations

- Maximum report size: 50MB
- Processing time: Up to 5 minutes for complex reports
- Requires sufficient content for analysis
- Some visualizations require specific data formats
- External data sources may have rate limits

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "topic": {
      "type": "string",
      "description": "Main topic or subject for the report"
    },
    "content": {
      "type": "string",
      "description": "Content to analyze and include in report"
    },
    "report_type": {
      "type": "string",
      "enum": ["comprehensive", "executive", "technical", "strategic"],
      "default": "comprehensive",
      "description": "Type of report to generate"
    },
    "modules": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Specific modules to include (optional, uses all 22 if not specified)"
    },
    "output_format": {
      "type": "string",
      "enum": ["html", "pdf", "word", "all"],
      "default": "html",
      "description": "Output format for the report"
    },
    "include_visualizations": {
      "type": "boolean",
      "default": true,
      "description": "Include interactive visualizations"
    },
    "include_tooltips": {
      "type": "boolean",
      "default": true,
      "description": "Include source tooltips and references"
    },
    "custom_styling": {
      "type": "object",
      "description": "Custom styling options"
    }
  },
  "required": ["topic", "content"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "report_id": {"type": "string"},
    "report_info": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "generated_at": {"type": "string"},
        "processing_time": {"type": "number"},
        "modules_included": {"type": "array"},
        "word_count": {"type": "number"},
        "page_count": {"type": "number"}
      }
    },
    "output_files": {
      "type": "object",
      "properties": {
        "html_path": {"type": "string"},
        "pdf_path": {"type": "string"},
        "word_path": {"type": "string"}
      }
    },
    "analysis_summary": {
      "type": "object",
      "properties": {
        "key_findings": {"type": "array"},
        "recommendations": {"type": "array"},
        "risk_assessment": {"type": "object"},
        "confidence_score": {"type": "number"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "sources_used": {"type": "array"},
        "tools_used": {"type": "array"},
        "data_sources": {"type": "array"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "report_id", "report_info"]
}
```

## Example

### Input:
```json
{
  "topic": "Cybersecurity Threats in Modern Warfare",
  "content": "Analysis of emerging cybersecurity threats and their impact on modern military operations...",
  "report_type": "comprehensive",
  "modules": ["threat_analysis", "risk_assessment", "strategic_recommendations"],
  "output_format": "html",
  "include_visualizations": true,
  "include_tooltips": true,
  "custom_styling": {
    "theme": "professional",
    "color_scheme": "blue"
  }
}
```

### Output:
```json
{
  "success": true,
  "report_id": "report_20241201_001",
  "report_info": {
    "title": "Cybersecurity Threats in Modern Warfare - Comprehensive Analysis",
    "generated_at": "2024-12-01T10:30:00Z",
    "processing_time": 180.5,
    "modules_included": [
      "threat_analysis",
      "risk_assessment", 
      "strategic_recommendations",
      "sentiment_analysis",
      "entity_extraction",
      "knowledge_graph",
      "forecasting",
      "deception_detection"
    ],
    "word_count": 15420,
    "page_count": 45
  },
  "output_files": {
    "html_path": "/Results/cybersecurity_threats_analysis_20241201_001.html",
    "pdf_path": "/Results/cybersecurity_threats_analysis_20241201_001.pdf",
    "word_path": "/Results/cybersecurity_threats_analysis_20241201_001.docx"
  },
  "analysis_summary": {
    "key_findings": [
      "Critical vulnerabilities identified in military communication systems",
      "Emerging AI-powered cyber threats pose significant risks",
      "Supply chain attacks targeting defense contractors increasing"
    ],
    "recommendations": [
      "Implement zero-trust architecture across all military networks",
      "Enhance AI-based threat detection capabilities",
      "Strengthen supply chain security protocols"
    ],
    "risk_assessment": {
      "overall_risk": "high",
      "confidence": 0.87,
      "risk_factors": ["technology", "human", "process"]
    },
    "confidence_score": 0.92
  },
  "metadata": {
    "sources_used": ["military_reports", "cybersecurity_database", "threat_intelligence"],
    "tools_used": ["sentiment_analysis", "entity_extraction", "knowledge_graph"],
    "data_sources": ["defense_contractors", "military_networks", "threat_feeds"]
  },
  "errors": [],
  "warnings": ["Some external data sources had rate limiting"]
}
```

## Safety & Reliability

- Validates all inputs and content
- Implements content sanitization for security
- Provides detailed error messages and warnings
- Includes processing timeouts and retry logic
- Logs all report generation activities
- Supports content encryption for sensitive reports
- Implements rate limiting for high-volume requests

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Configure template paths in `config/report_config.py`
3. Set up output directories: `mkdir -p Results`
4. Configure visualization settings
5. Set up database connections for content storage

### Usage Examples
```python
# Basic comprehensive report
result = await generate_enhanced_report(
    topic="AI in Military Applications",
    content="Analysis of artificial intelligence applications...",
    report_type="comprehensive"
)

# Executive summary report
result = await generate_enhanced_report(
    topic="Cybersecurity Strategy",
    content="Strategic cybersecurity analysis...",
    report_type="executive",
    output_format="pdf"
)

# Custom module report
result = await generate_enhanced_report(
    topic="Threat Assessment",
    content="Threat analysis content...",
    modules=["threat_analysis", "risk_assessment"],
    include_visualizations=True
)
```

### Error Handling
- Invalid topic: Returns error with topic suggestions
- Content too short: Returns warning with minimum content requirement
- Module not found: Falls back to available modules
- Processing timeout: Returns partial report with timeout warning
- File generation failure: Provides detailed error information

### Monitoring
- Report generation time tracking
- Success/failure rates by report type
- Module usage statistics
- Output format preferences
- Error frequency tracking
- Resource usage monitoring
