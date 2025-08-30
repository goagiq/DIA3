# Tool Card: verify_ingestion

## General Info

- **Name**: verify_ingestion
- **Title**: Verify Ingestion and Search Functionality
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Verify that ingested content is properly stored and searchable across vector database, knowledge graph, and semantic search systems

## Required Libraries

### Core Python Libraries
```python
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from pathlib import Path
```

### Database and Storage Libraries
```python
import chromadb>=0.4.18
import redis>=5.0.1
import sqlalchemy>=2.0.0
import psycopg2-binary>=2.9.9
```

### Vector and Search Libraries
```python
import numpy>=1.24.3
import pandas>=2.1.4
import faiss>=1.7.4
import sentence-transformers>=2.2.2
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
import chromadb
from datetime import datetime

# MCP Tool Decorator
@self.mcp.tool(description="Verify ingestion and search functionality")
```

## Intended Use

- Verify that content has been properly ingested into vector database
- Test semantic search functionality across all content
- Validate knowledge graph search capabilities
- Check system health and data integrity
- Provide comprehensive verification reports
- Test search queries and result quality
- Monitor ingestion pipeline performance

## Out-of-Scope / Limitations

- Maximum verification time: 5 minutes per verification session
- Test queries limited to 20 per verification
- Requires pre-ingested content for testing
- Some verification features may require specific data formats
- Performance depends on database size and complexity

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "search_queries": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of search queries to test"
    },
    "test_knowledge_graph": {
      "type": "boolean",
      "default": true,
      "description": "Test knowledge graph functionality"
    },
    "test_semantic_search": {
      "type": "boolean",
      "default": true,
      "description": "Test semantic search functionality"
    },
    "test_vector_database": {
      "type": "boolean",
      "default": true,
      "description": "Test vector database functionality"
    },
    "include_performance_metrics": {
      "type": "boolean",
      "default": false,
      "description": "Include performance metrics in results"
    }
  }
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "vector_database": {
      "type": "object",
      "properties": {
        "status": {"type": "string"},
        "stats": {"type": "object"},
        "error": {"type": "string"}
      }
    },
    "knowledge_graph": {
      "type": "object",
      "properties": {
        "status": {"type": "string"},
        "query_results": {"type": "object"},
        "error": {"type": "string"}
      }
    },
    "semantic_search": {
      "type": "object",
      "properties": {
        "query_results": {"type": "object"},
        "performance_metrics": {"type": "object"}
      }
    },
    "knowledge_graph_search": {
      "type": "object",
      "properties": {
        "query_results": {"type": "object"},
        "performance_metrics": {"type": "object"}
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_queries_tested": {"type": "number"},
        "semantic_search_success_rate": {"type": "string"},
        "knowledge_graph_success_rate": {"type": "string"},
        "vector_database_status": {"type": "string"},
        "overall_status": {"type": "string"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "summary"]
}
```

## Example

### Input:
```json
{
  "search_queries": [
    "Sun Tzu Art of War",
    "Leo Tolstoy War and Peace",
    "military strategy",
    "Napoleonic Wars",
    "Russian aristocracy 19th century"
  ],
  "test_knowledge_graph": true,
  "test_semantic_search": true,
  "include_performance_metrics": true
}
```

### Output:
```json
{
  "success": true,
  "vector_database": {
    "status": "success",
    "stats": {
      "total_documents": 15000,
      "total_embeddings": 15000,
      "database_size_mb": 245.6,
      "collections": ["semantic_search", "knowledge_graph", "documents"]
    }
  },
  "knowledge_graph": {
    "status": "success",
    "query_results": {
      "Sun Tzu military strategy": {
        "status": "success",
        "results_count": 5,
        "has_results": true
      },
      "Leo Tolstoy War and Peace characters": {
        "status": "success",
        "results_count": 3,
        "has_results": true
      }
    }
  },
  "semantic_search": {
    "Sun Tzu Art of War": {
      "status": "success",
      "results_count": 8,
      "has_results": true
    },
    "Leo Tolstoy War and Peace": {
      "status": "success",
      "results_count": 12,
      "has_results": true
    },
    "military strategy": {
      "status": "success",
      "results_count": 15,
      "has_results": true
    }
  },
  "knowledge_graph_search": {
    "Sun Tzu military strategy": {
      "status": "success",
      "results_count": 5,
      "has_results": true
    },
    "Napoleonic Wars Russia": {
      "status": "success",
      "results_count": 7,
      "has_results": true
    }
  },
  "summary": {
    "total_queries_tested": 5,
    "semantic_search_success_rate": "5/5",
    "knowledge_graph_success_rate": "2/2",
    "vector_database_status": "success",
    "overall_status": "success"
  },
  "errors": [],
  "warnings": []
}
```

## Safety & Reliability

- Validates all search queries before execution
- Implements timeout protection for long-running queries
- Provides detailed error messages and diagnostics
- Includes fallback mechanisms for failed components
- Logs all verification activities for audit trail
- Supports partial success reporting
- Implements resource usage monitoring

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Configure vector database connections in `config/database_config.py`
3. Set up knowledge graph database
4. Configure semantic search indexes
5. Test with sample data before production use

### Usage Examples
```python
# Basic verification
result = await verify_ingestion(
    search_queries=["test query 1", "test query 2"],
    test_knowledge_graph=True,
    test_semantic_search=True
)

# Comprehensive verification with performance metrics
result = await verify_ingestion(
    search_queries=["Sun Tzu", "military strategy", "war tactics"],
    test_knowledge_graph=True,
    test_semantic_search=True,
    include_performance_metrics=True
)

# Quick health check
result = await verify_ingestion(
    search_queries=["health check"],
    test_vector_database=True
)
```

### Error Handling
- Database connection failure: Returns error with connection details
- Query timeout: Returns partial results with timeout warning
- Missing data: Returns warning with data availability status
- Component failure: Returns status for working components only

### Monitoring
- Database health metrics
- Search performance tracking
- Query success rates
- System resource usage
- Error rate monitoring
- Response time tracking
