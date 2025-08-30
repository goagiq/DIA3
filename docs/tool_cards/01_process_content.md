# Tool Card: process_content

## General Info

- **Name**: process_content
- **Title**: Enhanced Unified Content Processing
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Enhanced unified content processing with bulk import, Open Library support, and intelligent MCP tool detection

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
```

### HTTP and API Libraries
```python
import requests>=2.31.0
import aiohttp>=3.9.1
import httpx>=0.25.2
```

### MCP and FastAPI Integration
```python
from mcp.server import FastMCP>=1.0.0
from fastapi>=0.104.1
from pydantic>=2.5.0
```

### Data Processing Libraries
```python
import pandas>=2.1.4
import numpy>=1.24.3
from PIL>=10.0.0  # For image processing
import fitz>=1.23.0  # PyMuPDF for PDF processing
```

### Database and Storage
```python
import chromadb>=0.4.18
import redis>=5.0.1
import psycopg2-binary>=2.9.9
```

### Additional Dependencies
```python
from loguru>=0.7.2
import python-multipart>=0.0.6
import python-jose[cryptography]>=3.3.0
```

## Imports and Decorators

```python
from mcp.server import FastMCP
from loguru import logger
from typing import Dict, Any, List, Optional, Union
import asyncio
import json
import tempfile
import os
from pathlib import Path

# MCP Tool Decorator
@self.mcp.tool(description="Enhanced unified content processing with bulk import, Open Library support, and intelligent MCP tool detection")
```

## Intended Use

- For processing various content types (text, images, PDFs, audio, video)
- Supports bulk import operations
- Integrates with Open Library for enhanced content enrichment
- Provides intelligent MCP tool detection and routing
- Handles multilingual content processing
- Supports content validation and quality assessment

## Out-of-Scope / Limitations

- Maximum file size: 100MB per file
- Supported formats: PDF, DOCX, TXT, JPG, PNG, MP3, MP4, WAV
- Requires valid content input
- Processing time scales with content size
- Some features require external API keys

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "content": {
      "type": "string",
      "description": "Content to process (text, file path, or URL)"
    },
    "content_type": {
      "type": "string",
      "enum": ["text", "file", "url", "bulk"],
      "description": "Type of content input"
    },
    "processing_options": {
      "type": "object",
      "properties": {
        "extract_text": {"type": "boolean", "default": true},
        "extract_entities": {"type": "boolean", "default": true},
        "analyze_sentiment": {"type": "boolean", "default": true},
        "translate": {"type": "boolean", "default": false},
        "target_language": {"type": "string", "default": "en"},
        "enhance_with_open_library": {"type": "boolean", "default": true}
      }
    },
    "output_format": {
      "type": "string",
      "enum": ["json", "structured", "summary"],
      "default": "json"
    }
  },
  "required": ["content"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "content_id": {"type": "string"},
    "processed_content": {
      "type": "object",
      "properties": {
        "text": {"type": "string"},
        "entities": {"type": "array"},
        "sentiment": {"type": "object"},
        "metadata": {"type": "object"},
        "enhanced_data": {"type": "object"}
      }
    },
    "processing_stats": {
      "type": "object",
      "properties": {
        "processing_time": {"type": "number"},
        "content_size": {"type": "number"},
        "quality_score": {"type": "number"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "content_id"]
}
```

## Example

### Input:
```json
{
  "content": "The strategic importance of cybersecurity in modern warfare cannot be overstated.",
  "content_type": "text",
  "processing_options": {
    "extract_text": true,
    "extract_entities": true,
    "analyze_sentiment": true,
    "enhance_with_open_library": true
  },
  "output_format": "json"
}
```

### Output:
```json
{
  "success": true,
  "content_id": "proc_20241201_001",
  "processed_content": {
    "text": "The strategic importance of cybersecurity in modern warfare cannot be overstated.",
    "entities": [
      {"type": "CONCEPT", "text": "cybersecurity", "confidence": 0.95},
      {"type": "DOMAIN", "text": "modern warfare", "confidence": 0.92}
    ],
    "sentiment": {
      "overall": "neutral",
      "confidence": 0.87,
      "scores": {"positive": 0.3, "neutral": 0.6, "negative": 0.1}
    },
    "metadata": {
      "language": "en",
      "word_count": 12,
      "complexity_score": 0.75
    },
    "enhanced_data": {
      "related_concepts": ["information warfare", "digital defense"],
      "context": "military strategy"
    }
  },
  "processing_stats": {
    "processing_time": 1.23,
    "content_size": 89,
    "quality_score": 0.92
  },
  "errors": [],
  "warnings": []
}
```

## Safety & Reliability

- Validates all inputs against schema
- Implements content sanitization
- Provides detailed error messages
- Includes processing timeouts
- Logs all operations for audit trail
- Supports content encryption for sensitive data
- Implements rate limiting for bulk operations

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Configure database connections in `config/config.py`
3. Set up Redis for caching
4. Configure Open Library API credentials
5. Initialize ChromaDB for vector storage

### Usage Examples
```python
# Basic text processing
result = await process_content(
    content="Sample text content",
    content_type="text"
)

# File processing
result = await process_content(
    content="/path/to/document.pdf",
    content_type="file",
    processing_options={"extract_text": True, "analyze_sentiment": True}
)

# Bulk processing
result = await process_content(
    content=["file1.pdf", "file2.docx", "file3.txt"],
    content_type="bulk"
)
```

### Error Handling
- Invalid content format: Returns error with format suggestions
- File not found: Returns specific file path error
- Processing timeout: Returns partial results with timeout warning
- API rate limit: Implements exponential backoff

### Monitoring
- Processing time metrics
- Success/failure rates
- Content quality scores
- Error frequency tracking
- Resource usage monitoring
