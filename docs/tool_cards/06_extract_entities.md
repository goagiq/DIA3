# Tool Card: extract_entities

## General Info

- **Name**: extract_entities
- **Title**: Entity Extraction and Relationship Mapping
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Advanced entity extraction and relationship mapping with support for multiple languages and domains

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
```

### NLP and Text Processing Libraries
```python
import spacy>=3.7.0
import nltk>=3.8.1
import transformers>=4.35.0
import torch>=2.1.0
import stanza>=1.7.0
```

### Machine Learning Libraries
```python
import numpy>=1.24.3
import pandas>=2.1.4
import scikit-learn>=1.3.2
import tensorflow>=2.15.0
```

### Graph and Network Libraries
```python
import networkx>=3.2.1
import rdflib>=7.0.0
import py2neo>=2021.2.3
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
import spacy
import networkx as nx
import numpy as np
import pandas as pd
from transformers import pipeline
import torch

# MCP Tool Decorator
@self.mcp.tool(description="Entity extraction and relationship mapping")
```

## Intended Use

- Extract named entities from text content
- Identify relationships between entities
- Support multiple languages and domains
- Create knowledge graphs from extracted entities
- Provide entity linking and disambiguation
- Generate entity hierarchies and taxonomies
- Support custom entity types and patterns

## Out-of-Scope / Limitations

- Maximum text length: 50,000 characters per extraction
- Supported languages: English, Spanish, French, German, Chinese, Arabic, Russian
- Requires sufficient text for accurate extraction (minimum 50 words)
- Processing time scales with text length and complexity
- Some entity types may have reduced accuracy in certain languages

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "text": {
      "type": "string",
      "description": "Text content to extract entities from"
    },
    "language": {
      "type": "string",
      "default": "auto",
      "description": "Language code or 'auto' for detection"
    },
    "entity_types": {
      "type": "array",
      "items": {"type": "string"},
      "default": ["PERSON", "ORG", "LOC", "MISC"],
      "description": "Types of entities to extract"
    },
    "include_relationships": {
      "type": "boolean",
      "default": true,
      "description": "Extract relationships between entities"
    },
    "confidence_threshold": {
      "type": "number",
      "default": 0.7,
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Minimum confidence score for entities"
    },
    "custom_patterns": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "pattern": {"type": "string"},
          "description": {"type": "string"}
        }
      },
      "description": "Custom entity patterns to match"
    }
  },
  "required": ["text"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "extraction_id": {"type": "string"},
    "entities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "text": {"type": "string"},
          "type": {"type": "string"},
          "start": {"type": "number"},
          "end": {"type": "number"},
          "confidence": {"type": "number"},
          "normalized_form": {"type": "string"},
          "attributes": {"type": "object"}
        }
      }
    },
    "relationships": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "source": {"type": "string"},
          "target": {"type": "string"},
          "relation": {"type": "string"},
          "confidence": {"type": "number"},
          "context": {"type": "string"}
        }
      }
    },
    "knowledge_graph": {
      "type": "object",
      "properties": {
        "nodes": {"type": "array"},
        "edges": {"type": "array"},
        "graph_metrics": {"type": "object"}
      }
    },
    "statistics": {
      "type": "object",
      "properties": {
        "total_entities": {"type": "number"},
        "entity_types": {"type": "object"},
        "total_relationships": {"type": "number"},
        "processing_time": {"type": "number"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "language": {"type": "string"},
        "model_used": {"type": "string"},
        "extraction_method": {"type": "string"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "extraction_id", "entities"]
}
```

## Example

### Input:
```json
{
  "text": "Microsoft Corporation, headquartered in Redmond, Washington, was founded by Bill Gates and Paul Allen in 1975. The company is a leading technology firm.",
  "language": "en",
  "entity_types": ["PERSON", "ORG", "LOC", "DATE"],
  "include_relationships": true,
  "confidence_threshold": 0.8
}
```

### Output:
```json
{
  "success": true,
  "extraction_id": "ent_20241201_001",
  "entities": [
    {
      "text": "Microsoft Corporation",
      "type": "ORG",
      "start": 0,
      "end": 20,
      "confidence": 0.95,
      "normalized_form": "Microsoft Corporation",
      "attributes": {
        "industry": "technology",
        "size": "large"
      }
    },
    {
      "text": "Redmond",
      "type": "LOC",
      "start": 35,
      "end": 42,
      "confidence": 0.92,
      "normalized_form": "Redmond, Washington",
      "attributes": {
        "country": "USA",
        "state": "Washington"
      }
    },
    {
      "text": "Washington",
      "type": "LOC",
      "start": 44,
      "end": 54,
      "confidence": 0.89,
      "normalized_form": "Washington",
      "attributes": {
        "type": "state"
      }
    },
    {
      "text": "Bill Gates",
      "type": "PERSON",
      "start": 75,
      "end": 85,
      "confidence": 0.98,
      "normalized_form": "Bill Gates",
      "attributes": {
        "role": "co-founder"
      }
    },
    {
      "text": "Paul Allen",
      "type": "PERSON",
      "start": 90,
      "end": 100,
      "confidence": 0.96,
      "normalized_form": "Paul Allen",
      "attributes": {
        "role": "co-founder"
      }
    },
    {
      "text": "1975",
      "type": "DATE",
      "start": 104,
      "end": 108,
      "confidence": 0.99,
      "normalized_form": "1975",
      "attributes": {
        "year": 1975
      }
    }
  ],
  "relationships": [
    {
      "source": "Microsoft Corporation",
      "target": "Redmond",
      "relation": "headquartered_in",
      "confidence": 0.94,
      "context": "headquartered in Redmond"
    },
    {
      "source": "Bill Gates",
      "target": "Microsoft Corporation",
      "relation": "founded",
      "confidence": 0.91,
      "context": "founded by Bill Gates"
    },
    {
      "source": "Paul Allen",
      "target": "Microsoft Corporation",
      "relation": "founded",
      "confidence": 0.91,
      "context": "founded by Paul Allen"
    }
  ],
  "knowledge_graph": {
    "nodes": [
      {"id": "Microsoft Corporation", "type": "ORG", "properties": {"industry": "technology"}},
      {"id": "Redmond", "type": "LOC", "properties": {"state": "Washington"}},
      {"id": "Bill Gates", "type": "PERSON", "properties": {"role": "co-founder"}},
      {"id": "Paul Allen", "type": "PERSON", "properties": {"role": "co-founder"}}
    ],
    "edges": [
      {"source": "Microsoft Corporation", "target": "Redmond", "relation": "headquartered_in"},
      {"source": "Bill Gates", "target": "Microsoft Corporation", "relation": "founded"},
      {"source": "Paul Allen", "target": "Microsoft Corporation", "relation": "founded"}
    ],
    "graph_metrics": {
      "node_count": 4,
      "edge_count": 3,
      "density": 0.5
    }
  },
  "statistics": {
    "total_entities": 6,
    "entity_types": {
      "ORG": 1,
      "LOC": 2,
      "PERSON": 2,
      "DATE": 1
    },
    "total_relationships": 3,
    "processing_time": 0.85
  },
  "metadata": {
    "language": "en",
    "model_used": "spacy-en_core_web_trf",
    "extraction_method": "hybrid"
  },
  "errors": [],
  "warnings": []
}
```

## Safety & Reliability

- Validates text input and language codes
- Implements entity disambiguation for ambiguous mentions
- Provides confidence scores for all extractions
- Handles edge cases and malformed input gracefully
- Logs extraction requests for audit trail
- Supports rate limiting for high-volume requests
- Implements fallback models for reliability

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Download language models: `python -m spacy download en_core_web_trf`
3. Download NLTK data: `python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"`
4. Configure entity extraction models in `config/entity_config.py`
5. Set up knowledge graph database connections

### Usage Examples
```python
# Basic entity extraction
result = await extract_entities(
    text="Apple Inc. is headquartered in Cupertino, California.",
    language="en"
)

# Custom entity types
result = await extract_entities(
    text="Sample text with custom entities",
    entity_types=["CUSTOM_TYPE", "PERSON", "ORG"],
    custom_patterns=[
        {"name": "CUSTOM_TYPE", "pattern": r"\\b[A-Z]{3,}\\b", "description": "Custom pattern"}
    ]
)

# Relationship extraction
result = await extract_entities(
    text="John works at Google in Mountain View.",
    include_relationships=True,
    confidence_threshold=0.8
)
```

### Error Handling
- Invalid language code: Returns error with supported languages
- Text too short: Returns warning with minimum length requirement
- Model loading failure: Falls back to basic extraction
- Processing timeout: Returns partial results with timeout warning

### Monitoring
- Entity extraction accuracy metrics
- Processing time tracking
- Model performance monitoring
- Language detection accuracy
- Error rate tracking
- Resource usage monitoring
