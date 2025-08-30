# Tool Card: knowledge_graph

## General Info

- **Name**: knowledge_graph
- **Title**: Knowledge Graph Creation and Management
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Advanced knowledge graph creation, management, and querying with support for complex relationships and reasoning

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

### Graph and Network Libraries
```python
import networkx>=3.2.1
import rdflib>=7.0.0
import py2neo>=2021.2.3
import igraph>=0.10.0
import graphviz>=0.20.1
```

### Database and Storage Libraries
```python
import neo4j>=5.0.0
import arangodb>=7.0.0
import chromadb>=0.4.18
import redis>=5.0.1
```

### Machine Learning Libraries
```python
import numpy>=1.24.3
import pandas>=2.1.4
import scikit-learn>=1.3.2
import torch>=2.1.0
import transformers>=4.35.0
```

### Visualization Libraries
```python
import plotly>=5.17.0
import matplotlib>=3.8.2
import seaborn>=0.13.0
import plotly.graph_objects as go
import plotly.express as px
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
import sqlalchemy>=2.0.0
```

## Imports and Decorators

```python
from mcp.server import FastMCP
from loguru import logger
from typing import Dict, Any, List, Optional, Union
import asyncio
import json
import networkx as nx
import numpy as np
import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
import plotly.graph_objects as go
import plotly.express as px

# MCP Tool Decorator
@self.mcp.tool(description="Knowledge graph creation and management")
```

## Intended Use

- Create and manage knowledge graphs from structured and unstructured data
- Perform complex graph queries and reasoning
- Support multiple graph databases and formats
- Generate graph visualizations and analytics
- Implement graph-based recommendation systems
- Support semantic search and knowledge discovery
- Enable graph-based machine learning workflows

## Out-of-Scope / Limitations

- Maximum graph size: 1 million nodes and 10 million edges
- Processing time: Up to 30 minutes for large graphs
- Memory usage: Up to 16GB for complex operations
- Requires sufficient data for meaningful graph construction
- Some advanced reasoning features require specific graph formats

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "operation": {
      "type": "string",
      "enum": ["create", "query", "update", "analyze", "visualize", "export"],
      "description": "Type of knowledge graph operation"
    },
    "data_source": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["entities", "relationships", "text", "structured", "api"],
          "description": "Type of data source"
        },
        "content": {
          "type": "string",
          "description": "Data content or source path"
        },
        "format": {
          "type": "string",
          "enum": ["json", "csv", "rdf", "graphml", "neo4j"],
          "description": "Data format"
        }
      },
      "description": "Source data for graph operations"
    },
    "graph_config": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "node_types": {"type": "array"},
        "edge_types": {"type": "array"},
        "properties": {"type": "object"}
      },
      "description": "Graph configuration parameters"
    },
    "query": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["cypher", "sparql", "gremlin", "natural"],
          "description": "Query language"
        },
        "query_string": {"type": "string"},
        "parameters": {"type": "object"}
      },
      "description": "Graph query specification"
    },
    "visualization_options": {
      "type": "object",
      "properties": {
        "layout": {
          "type": "string",
          "enum": ["force", "circular", "hierarchical", "kamada_kawai"],
          "default": "force"
        },
        "node_size": {"type": "number", "default": 10},
        "edge_width": {"type": "number", "default": 1},
        "color_scheme": {"type": "string", "default": "viridis"}
      },
      "description": "Visualization configuration"
    }
  },
  "required": ["operation"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "operation_id": {"type": "string"},
    "graph_info": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "node_count": {"type": "number"},
        "edge_count": {"type": "number"},
        "density": {"type": "number"},
        "diameter": {"type": "number"},
        "average_clustering": {"type": "number"},
        "connected_components": {"type": "number"}
      }
    },
    "query_results": {
      "type": "object",
      "properties": {
        "nodes": {"type": "array"},
        "edges": {"type": "array"},
        "paths": {"type": "array"},
        "metrics": {"type": "object"}
      }
    },
    "analytics": {
      "type": "object",
      "properties": {
        "centrality_measures": {"type": "object"},
        "community_detection": {"type": "object"},
        "path_analysis": {"type": "object"},
        "similarity_scores": {"type": "object"}
      }
    },
    "visualization": {
      "type": "object",
      "properties": {
        "html_path": {"type": "string"},
        "image_path": {"type": "string"},
        "interactive_url": {"type": "string"}
      }
    },
    "export_data": {
      "type": "object",
      "properties": {
        "format": {"type": "string"},
        "file_path": {"type": "string"},
        "size": {"type": "number"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "creation_time": {"type": "string"},
        "processing_time": {"type": "number"},
        "database_used": {"type": "string"},
        "version": {"type": "string"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "operation_id"]
}
```

## Example

### Input (Create Graph):
```json
{
  "operation": "create",
  "data_source": {
    "type": "entities",
    "content": "{\"entities\": [{\"id\": \"person1\", \"type\": \"Person\", \"name\": \"John Doe\", \"attributes\": {\"age\": 30, \"occupation\": \"Engineer\"}}, {\"id\": \"company1\", \"type\": \"Company\", \"name\": \"Tech Corp\", \"attributes\": {\"industry\": \"Technology\"}}], \"relationships\": [{\"source\": \"person1\", \"target\": \"company1\", \"type\": \"WORKS_FOR\", \"attributes\": {\"start_date\": \"2020-01-01\"}}]}",
    "format": "json"
  },
  "graph_config": {
    "name": "employment_network",
    "description": "Employment relationships network",
    "node_types": ["Person", "Company", "Location"],
    "edge_types": ["WORKS_FOR", "FOUNDED", "LOCATED_IN"]
  }
}
```

### Output:
```json
{
  "success": true,
  "operation_id": "kg_20241201_001",
  "graph_info": {
    "name": "employment_network",
    "node_count": 2,
    "edge_count": 1,
    "density": 1.0,
    "diameter": 1,
    "average_clustering": 0.0,
    "connected_components": 1
  },
  "query_results": null,
  "analytics": {
    "centrality_measures": {
      "degree_centrality": {
        "person1": 1.0,
        "company1": 1.0
      },
      "betweenness_centrality": {
        "person1": 0.0,
        "company1": 0.0
      },
      "eigenvector_centrality": {
        "person1": 0.707,
        "company1": 0.707
      }
    },
    "community_detection": {
      "communities": [["person1", "company1"]],
      "modularity": 0.0
    },
    "path_analysis": {
      "shortest_paths": {
        "person1_to_company1": 1
      },
      "average_path_length": 1.0
    },
    "similarity_scores": {
      "jaccard_similarity": 0.0,
      "cosine_similarity": 0.0
    }
  },
  "visualization": {
    "html_path": "/Results/employment_network_20241201_001.html",
    "image_path": "/Results/employment_network_20241201_001.png",
    "interactive_url": "http://localhost:8000/graph/employment_network_20241201_001"
  },
  "export_data": null,
  "metadata": {
    "creation_time": "2024-12-01T10:30:00Z",
    "processing_time": 2.5,
    "database_used": "neo4j",
    "version": "2.0.0"
  },
  "errors": [],
  "warnings": []
}
```

### Input (Query Graph):
```json
{
  "operation": "query",
  "query": {
    "type": "cypher",
    "query_string": "MATCH (p:Person)-[r:WORKS_FOR]->(c:Company) RETURN p.name, c.name, r.start_date",
    "parameters": {}
  }
}
```

### Output:
```json
{
  "success": true,
  "operation_id": "kg_query_20241201_001",
  "graph_info": null,
  "query_results": {
    "nodes": [],
    "edges": [],
    "paths": [],
    "metrics": {
      "execution_time": 0.15,
      "result_count": 1
    },
    "data": [
      {
        "p.name": "John Doe",
        "c.name": "Tech Corp",
        "r.start_date": "2020-01-01"
      }
    ]
  },
  "analytics": null,
  "visualization": null,
  "export_data": null,
  "metadata": {
    "query_time": "2024-12-01T10:35:00Z",
    "processing_time": 0.15,
    "database_used": "neo4j",
    "version": "2.0.0"
  },
  "errors": [],
  "warnings": []
}
```

## Safety & Reliability

- Validates all input data and graph configurations
- Implements graph size limits and resource management
- Provides detailed error messages and warnings
- Includes processing timeouts and retry logic
- Logs all graph operations for audit trail
- Supports graph backup and recovery
- Implements access control and security measures

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Set up graph databases (Neo4j, ArangoDB, etc.)
3. Configure graph storage paths in `config/graph_config.py`
4. Set up visualization server for interactive graphs
5. Configure backup and recovery procedures

### Usage Examples
```python
# Create knowledge graph from entities
result = await knowledge_graph(
    operation="create",
    data_source={
        "type": "entities",
        "content": entity_data,
        "format": "json"
    },
    graph_config={
        "name": "my_knowledge_graph",
        "description": "Custom knowledge graph"
    }
)

# Query knowledge graph
result = await knowledge_graph(
    operation="query",
    query={
        "type": "cypher",
        "query_string": "MATCH (n) RETURN n LIMIT 10"
    }
)

# Analyze graph metrics
result = await knowledge_graph(
    operation="analyze",
    graph_config={"name": "my_knowledge_graph"}
)
```

### Error Handling
- Invalid graph format: Returns error with supported formats
- Graph too large: Returns warning with size limits
- Database connection failure: Falls back to in-memory graph
- Processing timeout: Returns partial results with timeout warning
- Query syntax error: Returns detailed syntax error information

### Monitoring
- Graph size and growth metrics
- Query performance tracking
- Database connection monitoring
- Memory usage tracking
- Error rate monitoring
- User activity tracking
