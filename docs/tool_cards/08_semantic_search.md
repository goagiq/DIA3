# Tool Card: semantic_search

## General Info

- **Name**: semantic_search
- **Title**: Semantic Search Across All Content
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Advanced semantic search capabilities across all content types with vector embeddings and similarity matching

## Required Libraries

### Core Python Libraries
```python
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
import re
from datetime import datetime
from pathlib import Path
import tempfile
import os
```

### Vector and Embedding Libraries
```python
import numpy>=1.24.3
import pandas>=2.1.4
import scipy>=1.11.4
import faiss>=1.7.4
import sentence-transformers>=2.2.2
import transformers>=4.35.0
import torch>=2.1.0
```

### Database and Storage Libraries
```python
import chromadb>=0.4.18
import redis>=5.0.1
import elasticsearch>=8.0.0
import pinecone-client>=2.2.4
import weaviate-client>=3.25.3
```

### NLP and Text Processing Libraries
```python
import spacy>=3.7.0
import nltk>=3.8.1
import textblob>=0.17.1
import gensim>=4.3.2
```

### Machine Learning Libraries
```python
import scikit-learn>=1.3.2
import tensorflow>=2.15.0
import keras>=2.15.0
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
import tiktoken>=0.5.1
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
from sentence_transformers import SentenceTransformer
import chromadb
import faiss
import torch
from sklearn.metrics.pairwise import cosine_similarity

# MCP Tool Decorator
@self.mcp.tool(description="Semantic search across all content")
```

## Intended Use

- Perform semantic search across all content types (text, documents, images, etc.)
- Support multiple languages and content formats
- Provide similarity-based content discovery
- Enable fuzzy matching and concept-based search
- Support real-time search with vector databases
- Generate search analytics and insights
- Integrate with knowledge graphs for enhanced search

## Out-of-Scope / Limitations

- Maximum query length: 10,000 characters
- Maximum results: 1,000 per search
- Processing time: Up to 30 seconds for complex queries
- Memory usage: Up to 8GB for large vector databases
- Requires pre-indexed content for optimal performance
- Some languages may have reduced accuracy

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search query text"
    },
    "content_types": {
      "type": "array",
      "items": {"type": "string"},
      "default": ["text", "document", "image", "audio", "video"],
      "description": "Types of content to search"
    },
    "language": {
      "type": "string",
      "default": "auto",
      "description": "Language code or 'auto' for detection"
    },
    "search_type": {
      "type": "string",
      "enum": ["semantic", "hybrid", "vector", "keyword"],
      "default": "semantic",
      "description": "Type of search to perform"
    },
    "filters": {
      "type": "object",
      "properties": {
        "date_range": {
          "type": "object",
          "properties": {
            "start": {"type": "string"},
            "end": {"type": "string"}
          }
        },
        "content_sources": {"type": "array"},
        "tags": {"type": "array"},
        "categories": {"type": "array"}
      },
      "description": "Search filters to apply"
    },
    "similarity_threshold": {
      "type": "number",
      "default": 0.7,
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Minimum similarity score for results"
    },
    "max_results": {
      "type": "integer",
      "default": 50,
      "minimum": 1,
      "maximum": 1000,
      "description": "Maximum number of results to return"
    },
    "include_metadata": {
      "type": "boolean",
      "default": true,
      "description": "Include metadata in search results"
    },
    "include_embeddings": {
      "type": "boolean",
      "default": false,
      "description": "Include vector embeddings in results"
    }
  },
  "required": ["query"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "search_id": {"type": "string"},
    "query_info": {
      "type": "object",
      "properties": {
        "original_query": {"type": "string"},
        "processed_query": {"type": "string"},
        "language": {"type": "string"},
        "search_type": {"type": "string"},
        "filters_applied": {"type": "object"}
      }
    },
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "content_id": {"type": "string"},
          "content_type": {"type": "string"},
          "title": {"type": "string"},
          "content": {"type": "string"},
          "similarity_score": {"type": "number"},
          "relevance_score": {"type": "number"},
          "metadata": {"type": "object"},
          "highlights": {"type": "array"},
          "source_url": {"type": "string"},
          "created_at": {"type": "string"},
          "updated_at": {"type": "string"}
        }
      }
    },
    "search_analytics": {
      "type": "object",
      "properties": {
        "total_results": {"type": "number"},
        "processing_time": {"type": "number"},
        "query_complexity": {"type": "string"},
        "result_distribution": {"type": "object"},
        "performance_metrics": {"type": "object"}
      }
    },
    "suggestions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "suggestion": {"type": "string"},
          "type": {"type": "string"},
          "confidence": {"type": "number"}
        }
      }
    },
    "facets": {
      "type": "object",
      "properties": {
        "content_types": {"type": "object"},
        "sources": {"type": "object"},
        "tags": {"type": "object"},
        "categories": {"type": "object"},
        "date_ranges": {"type": "object"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "search_time": {"type": "string"},
        "model_used": {"type": "string"},
        "database_used": {"type": "string"},
        "index_size": {"type": "number"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "search_id", "results"]
}
```

## Example

### Input:
```json
{
  "query": "cybersecurity threats in modern warfare",
  "content_types": ["text", "document", "report"],
  "language": "en",
  "search_type": "semantic",
  "filters": {
    "date_range": {
      "start": "2020-01-01",
      "end": "2024-12-01"
    },
    "categories": ["military", "technology", "security"]
  },
  "similarity_threshold": 0.8,
  "max_results": 20,
  "include_metadata": true
}
```

### Output:
```json
{
  "success": true,
  "search_id": "search_20241201_001",
  "query_info": {
    "original_query": "cybersecurity threats in modern warfare",
    "processed_query": "cybersecurity threats modern warfare",
    "language": "en",
    "search_type": "semantic",
    "filters_applied": {
      "date_range": {"start": "2020-01-01", "end": "2024-12-01"},
      "categories": ["military", "technology", "security"]
    }
  },
  "results": [
    {
      "content_id": "doc_001",
      "content_type": "document",
      "title": "Emerging Cybersecurity Threats in Military Operations",
      "content": "Modern warfare increasingly relies on digital infrastructure, making cybersecurity a critical component of military strategy...",
      "similarity_score": 0.95,
      "relevance_score": 0.92,
      "metadata": {
        "author": "Military Research Institute",
        "publication_date": "2024-06-15",
        "category": "military",
        "tags": ["cybersecurity", "warfare", "military", "technology"],
        "word_count": 2500
      },
      "highlights": [
        "cybersecurity threats in modern warfare",
        "digital infrastructure in military operations",
        "cybersecurity as critical component"
      ],
      "source_url": "https://example.com/doc_001",
      "created_at": "2024-06-15T10:00:00Z",
      "updated_at": "2024-06-15T10:00:00Z"
    },
    {
      "content_id": "report_002",
      "content_type": "report",
      "title": "Cyber Warfare: The New Battlefield",
      "content": "The landscape of modern warfare has evolved significantly with the rise of cyber threats...",
      "similarity_score": 0.88,
      "relevance_score": 0.85,
      "metadata": {
        "author": "Defense Analysis Center",
        "publication_date": "2024-03-20",
        "category": "security",
        "tags": ["cyber warfare", "threats", "defense"],
        "word_count": 1800
      },
      "highlights": [
        "cyber threats in modern warfare",
        "new battlefield of cyber warfare",
        "evolving landscape of warfare"
      ],
      "source_url": "https://example.com/report_002",
      "created_at": "2024-03-20T14:30:00Z",
      "updated_at": "2024-03-20T14:30:00Z"
    }
  ],
  "search_analytics": {
    "total_results": 15,
    "processing_time": 1.25,
    "query_complexity": "medium",
    "result_distribution": {
      "document": 8,
      "report": 5,
      "text": 2
    },
    "performance_metrics": {
      "query_processing_time": 0.15,
      "vector_search_time": 0.85,
      "result_ranking_time": 0.25
    }
  },
  "suggestions": [
    {
      "suggestion": "cyber warfare threats",
      "type": "related_query",
      "confidence": 0.85
    },
    {
      "suggestion": "military cybersecurity",
      "type": "related_query",
      "confidence": 0.78
    }
  ],
  "facets": {
    "content_types": {
      "document": 8,
      "report": 5,
      "text": 2
    },
    "sources": {
      "Military Research Institute": 3,
      "Defense Analysis Center": 4,
      "Security Journal": 2
    },
    "tags": {
      "cybersecurity": 12,
      "warfare": 10,
      "military": 8,
      "threats": 7
    },
    "categories": {
      "military": 8,
      "security": 5,
      "technology": 2
    },
    "date_ranges": {
      "2024": 10,
      "2023": 3,
      "2022": 2
    }
  },
  "metadata": {
    "search_time": "2024-12-01T10:30:00Z",
    "model_used": "sentence-transformers/all-MiniLM-L6-v2",
    "database_used": "chromadb",
    "index_size": 15000
  },
  "errors": [],
  "warnings": []
}
```

## Safety & Reliability

- Validates all search queries and parameters
- Implements query sanitization and security measures
- Provides detailed error messages and warnings
- Includes processing timeouts and resource limits
- Logs all search activities for audit trail
- Supports rate limiting for high-volume searches
- Implements fallback search methods for reliability

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Download embedding models: `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"`
3. Set up vector databases (ChromaDB, Pinecone, etc.)
4. Configure search indexes in `config/search_config.py`
5. Set up content indexing pipeline

### Usage Examples
```python
# Basic semantic search
result = await semantic_search(
    query="artificial intelligence applications",
    content_types=["text", "document"],
    max_results=20
)

# Filtered search
result = await semantic_search(
    query="machine learning algorithms",
    filters={
        "date_range": {"start": "2023-01-01", "end": "2024-12-01"},
        "categories": ["technology", "research"]
    },
    similarity_threshold=0.8
)

# Multi-language search
result = await semantic_search(
    query="intelligence artificielle",
    language="fr",
    search_type="hybrid"
)
```

### Error Handling
- Invalid query: Returns error with query suggestions
- No results found: Returns empty results with suggestions
- Database connection failure: Falls back to local search
- Processing timeout: Returns partial results with timeout warning
- Model loading failure: Falls back to keyword search

### Monitoring
- Search performance metrics
- Query complexity analysis
- Result quality assessment
- User search patterns
- Database performance monitoring
- Error rate tracking
