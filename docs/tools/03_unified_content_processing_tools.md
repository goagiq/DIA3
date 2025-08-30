# Unified Content Processing MCP Tools

## Tool Card: process_content

### General Info
- **Name**: process_content
- **Title**: Enhanced Unified Content Processor
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Processes any type of content with unified interface, including bulk import requests, Open Library support, and intelligent MCP tool detection.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)
pathlib
urllib.parse

# Content Processing
requests>=2.25.0
beautifulsoup4>=4.12.0
PyPDF2>=3.0.0
pdfplumber>=0.9.0

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
from typing import Dict, Any, Optional, List
from pathlib import Path
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Enhanced unified content processing with bulk import, Open Library support, and intelligent MCP tool detection")
async def process_content(
    content: str,
    content_type: str = "auto",
    language: str = "en",
    options: Dict[str, Any] = None
) -> Dict[str, Any]:
```

### Intended Use
- Bulk content processing and import
- Multi-format content analysis
- Open Library and ctext.org integration
- Intelligent content type detection
- Research and intelligence gathering

### Out-of-Scope / Limitations
- Requires valid content input
- Limited to supported content types
- Bulk processing may have rate limits
- External service dependencies

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "content": {
      "type": "string",
      "description": "Content to process (text, URL, file path, or bulk import request)"
    },
    "content_type": {
      "type": "string",
      "description": "Type of content (auto, text, pdf, audio, video, image, vision)",
      "default": "auto"
    },
    "language": {
      "type": "string",
      "description": "Language code for processing",
      "default": "en"
    },
    "options": {
      "type": "object",
      "description": "Additional processing options"
    }
  },
  "required": ["content"]
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
        "content_type": {"type": "string"},
        "language_detected": {"type": "string"},
        "processing_time": {"type": "number"},
        "extracted_text": {"type": "string"},
        "metadata": {"type": "object"},
        "entities": {"type": "array"},
        "sentiment": {"type": "object"}
      }
    },
    "bulk_results": {
      "type": "array",
      "description": "Results for bulk processing"
    }
  },
  "required": ["success"]
}
```

### Example
**Input:**
```json
{
  "content": "https://openlibrary.org/works/OL45804W/The_Art_of_War",
  "content_type": "auto",
  "language": "en"
}
```

**Output:**
```json
{
  "success": true,
  "result": {
    "content_type": "web",
    "language_detected": "en",
    "processing_time": 5.2,
    "extracted_text": "The Art of War is an ancient Chinese military treatise...",
    "metadata": {
      "title": "The Art of War",
      "author": "Sun Tzu",
      "source": "openlibrary.org"
    },
    "entities": [
      {"text": "Sun Tzu", "type": "PERSON"},
      {"text": "China", "type": "GPE"}
    ],
    "sentiment": {
      "overall": "neutral",
      "confidence": 0.75
    }
  }
}
```

### Safety & Reliability
- Validates URLs and file paths
- Handles various content encodings
- Rate limiting for external services
- Comprehensive error handling
- No sensitive data persistence

---

## Tool Card: verify_ingestion

### General Info
- **Name**: verify_ingestion
- **Title**: Content Ingestion Verifier
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Verifies that ingested content is properly stored and searchable across vector database and knowledge graph.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)

# Database and Search
chromadb>=0.4.0
networkx>=3.0
sqlite3

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
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Verify ingestion and search functionality")
async def verify_ingestion(
    search_queries: List[str] = None,
    test_knowledge_graph: bool = True,
    test_semantic_search: bool = True
) -> Dict[str, Any]:
```

### Intended Use
- System health monitoring
- Data integrity verification
- Search functionality testing
- Quality assurance
- Debugging ingestion issues

### Out-of-Scope / Limitations
- Requires pre-ingested content
- Limited to available search queries
- Database-dependent operations
- May take time for large datasets

### Input Schema
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
      "description": "Whether to test knowledge graph functionality",
      "default": true
    },
    "test_semantic_search": {
      "type": "boolean",
      "description": "Whether to test semantic search functionality",
      "default": true
    }
  },
  "required": []
}
```

### Output Schema
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
        "test_results": {"type": "array"}
      }
    },
    "knowledge_graph": {
      "type": "object",
      "properties": {
        "status": {"type": "string"},
        "node_count": {"type": "integer"},
        "edge_count": {"type": "integer"},
        "test_results": {"type": "array"}
      }
    },
    "semantic_search": {
      "type": "object",
      "properties": {
        "status": {"type": "string"},
        "query_results": {"type": "array"}
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "overall_status": {"type": "string"},
        "total_tests": {"type": "integer"},
        "passed_tests": {"type": "integer"},
        "failed_tests": {"type": "integer"}
      }
    }
  },
  "required": ["success", "summary"]
}
```

### Example
**Input:**
```json
{
  "search_queries": ["Sun Tzu", "military strategy", "The Art of War"],
  "test_knowledge_graph": true,
  "test_semantic_search": true
}
```

**Output:**
```json
{
  "success": true,
  "vector_database": {
    "status": "success",
    "stats": {
      "total_documents": 1250,
      "total_embeddings": 1250,
      "collection_size": "45.2 MB"
    },
    "test_results": [
      {"query": "Sun Tzu", "results": 5, "status": "passed"},
      {"query": "military strategy", "results": 12, "status": "passed"}
    ]
  },
  "knowledge_graph": {
    "status": "success",
    "node_count": 3450,
    "edge_count": 12800,
    "test_results": [
      {"query": "Sun Tzu", "entities_found": 3, "status": "passed"}
    ]
  },
  "semantic_search": {
    "status": "success",
    "query_results": [
      {"query": "The Art of War", "relevance_score": 0.95, "status": "passed"}
    ]
  },
  "summary": {
    "overall_status": "healthy",
    "total_tests": 6,
    "passed_tests": 6,
    "failed_tests": 0
  }
}
```

### Safety & Reliability
- Non-destructive testing only
- Comprehensive error reporting
- Graceful handling of missing data
- Performance monitoring
- Safe for concurrent access

---

## Tool Card: extract_text_from_content

### General Info
- **Name**: extract_text_from_content
- **Title**: Multi-Format Text Extractor
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Extracts text from any content type including PDFs, audio, video, and images.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)
pathlib

# Text Extraction
PyPDF2>=3.0.0
pdfplumber>=0.9.0
pytesseract>=0.3.10
speech_recognition>=3.10.0

# Audio/Video Processing
moviepy>=1.0.3
pydub>=0.25.1

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
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Extract text from any content type")
async def extract_text_from_content(
    content: str,
    content_type: str = "auto",
    language: str = "en"
) -> Dict[str, Any]:
```

### Intended Use
- Document text extraction
- Audio transcription
- Video subtitle extraction
- Image OCR processing
- Multi-format content analysis

### Out-of-Scope / Limitations
- Requires valid content input
- Audio/video quality affects transcription
- OCR accuracy depends on image quality
- Limited to supported formats

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "content": {
      "type": "string",
      "description": "Content to extract text from (file path, URL, or raw text)"
    },
    "content_type": {
      "type": "string",
      "description": "Type of content (auto, pdf, audio, video, image, vision)",
      "default": "auto"
    },
    "language": {
      "type": "string",
      "description": "Language for processing",
      "default": "en"
    }
  },
  "required": ["content"]
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
        "text": {"type": "string"},
        "language": {"type": "string"},
        "confidence": {"type": "number"},
        "processing_time": {"type": "number"},
        "metadata": {"type": "object"}
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
  "content": "/path/to/document.pdf",
  "content_type": "pdf",
  "language": "en"
}
```

**Output:**
```json
{
  "success": true,
  "result": {
    "text": "This is the extracted text from the PDF document...",
    "language": "en",
    "confidence": 0.95,
    "processing_time": 2.3,
    "metadata": {
      "pages": 5,
      "characters": 2500,
      "format": "pdf"
    }
  }
}
```

### Safety & Reliability
- Validates file existence and format
- Handles corrupted files gracefully
- Supports multiple languages
- Memory-efficient processing
- Comprehensive error reporting
