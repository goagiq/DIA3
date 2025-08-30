# Content Processing MCP Tools

## Tool Card: process_pdf_enhanced_multilingual

### General Info
- **Name**: process_pdf_enhanced_multilingual
- **Title**: Enhanced Multilingual PDF Processor
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Processes PDF documents with enhanced multilingual support, text extraction, and knowledge graph integration.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)
pathlib

# PDF Processing
PyPDF2>=3.0.0
pdfplumber>=0.9.0
pdf2image>=1.16.0

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

@self.mcp.tool(description="Process PDF with enhanced multilingual support")
async def process_pdf_enhanced_multilingual(
    pdf_path: str,
    language: str = "auto",
    generate_report: bool = True,
    output_path: str = None
):
```

### Intended Use
- Document analysis and processing
- Multilingual content extraction
- Knowledge graph generation from documents
- Automated report generation from PDFs
- Research and intelligence gathering

### Out-of-Scope / Limitations
- Requires valid PDF file path
- Limited to text-based PDFs (not scanned images)
- Language detection may not be 100% accurate
- Large PDFs may take significant processing time

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "pdf_path": {
      "type": "string",
      "description": "Path to the PDF file to process"
    },
    "language": {
      "type": "string",
      "description": "Language code for processing (default: auto-detect)",
      "default": "auto"
    },
    "generate_report": {
      "type": "boolean",
      "description": "Whether to generate a comprehensive report",
      "default": true
    },
    "output_path": {
      "type": "string",
      "description": "Optional output path for results"
    }
  },
  "required": ["pdf_path"]
}
```

### Output Schema
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "extraction_result": {
      "type": "object",
      "properties": {
        "pages_processed": {"type": "integer"},
        "text_length": {"type": "integer"},
        "language_detected": {"type": "string"},
        "metadata": {"type": "object"}
      }
    },
    "knowledge_graph_result": {
      "type": "object",
      "properties": {
        "entities_found": {"type": "integer"},
        "relationships": {"type": "array"},
        "confidence_score": {"type": "number"}
      }
    },
    "processing_time": {"type": "number"}
  },
  "required": ["success"]
}
```

### Example
**Input:**
```json
{
  "pdf_path": "/path/to/document.pdf",
  "language": "en",
  "generate_report": true
}
```

**Output:**
```json
{
  "success": true,
  "extraction_result": {
    "pages_processed": 15,
    "text_length": 12500,
    "language_detected": "en",
    "metadata": {
      "title": "Strategic Analysis Report",
      "author": "DIA3 Team"
    }
  },
  "knowledge_graph_result": {
    "entities_found": 45,
    "relationships": [
      {"source": "entity1", "target": "entity2", "type": "relates_to"}
    ],
    "confidence_score": 0.87
  },
  "processing_time": 12.5
}
```

### Safety & Reliability
- Validates PDF file existence and format
- Handles corrupted or invalid PDFs gracefully
- Supports multiple languages and encodings
- Memory-efficient processing for large files
- Comprehensive error reporting

---

## Tool Card: analyze_text_sentiment

### General Info
- **Name**: analyze_text_sentiment
- **Title**: Text Sentiment Analyzer
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Analyzes sentiment of text content with confidence scoring and language detection.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)

# NLP and Sentiment Analysis
transformers>=4.30.0
torch>=2.0.0
nltk>=3.8.0
textblob>=0.17.0

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

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Analyze text sentiment")
async def analyze_text_sentiment(
    text: str,
    language: str = "auto"
):
```

### Intended Use
- Social media monitoring
- Customer feedback analysis
- Content moderation
- Market sentiment analysis
- Research and intelligence gathering

### Out-of-Scope / Limitations
- Requires text input (not binary data)
- Language detection accuracy varies
- Sentiment analysis may not capture context nuances
- Limited to supported languages

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "text": {
      "type": "string",
      "description": "Text content to analyze"
    },
    "language": {
      "type": "string",
      "description": "Language code for analysis (default: auto-detect)",
      "default": "auto"
    }
  },
  "required": ["text"]
}
```

### Output Schema
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "sentiment": {
      "type": "string",
      "enum": ["positive", "negative", "neutral", "mixed"]
    },
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "processing_time": {"type": "number"},
    "language_detected": {"type": "string"},
    "sentiment_scores": {
      "type": "object",
      "properties": {
        "positive": {"type": "number"},
        "negative": {"type": "number"},
        "neutral": {"type": "number"}
      }
    }
  },
  "required": ["success", "sentiment", "confidence"]
}
```

### Example
**Input:**
```json
{
  "text": "This product exceeded my expectations. The quality is outstanding!",
  "language": "en"
}
```

**Output:**
```json
{
  "success": true,
  "sentiment": "positive",
  "confidence": 0.92,
  "processing_time": 0.15,
  "language_detected": "en",
  "sentiment_scores": {
    "positive": 0.92,
    "negative": 0.03,
    "neutral": 0.05
  }
}
```

### Safety & Reliability
- Handles various text encodings
- Robust against malformed input
- Provides confidence scores for reliability
- Supports multiple languages
- No data persistence or logging of sensitive content

---

## Tool Card: extract_entities

### General Info
- **Name**: extract_entities
- **Title**: Entity Extraction Engine
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Extracts named entities, relationships, and key information from text content.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)

# NLP and Entity Extraction
spacy>=3.5.0
transformers>=4.30.0
torch>=2.0.0
nltk>=3.8.0

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

@self.mcp.tool(description="Extract entities from text")
async def extract_entities(
    text: str,
    language: str = "auto"
):
```

### Intended Use
- Information extraction from documents
- Knowledge graph construction
- Intelligence gathering
- Research and analysis
- Data mining and pattern recognition

### Out-of-Scope / Limitations
- Requires text input
- Entity recognition accuracy varies by domain
- Limited to supported entity types
- May miss context-dependent entities

### Input Schema
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
      "description": "Language code for extraction (default: auto-detect)",
      "default": "auto"
    }
  },
  "required": ["text"]
}
```

### Output Schema
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "entities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "text": {"type": "string"},
          "type": {"type": "string"},
          "confidence": {"type": "number"},
          "position": {
            "type": "object",
            "properties": {
              "start": {"type": "integer"},
              "end": {"type": "integer"}
            }
          }
        }
      }
    },
    "entity_count": {"type": "integer"},
    "processing_time": {"type": "number"},
    "entity_types": {
      "type": "object",
      "properties": {
        "PERSON": {"type": "integer"},
        "ORG": {"type": "integer"},
        "GPE": {"type": "integer"},
        "DATE": {"type": "integer"},
        "MONEY": {"type": "integer"}
      }
    }
  },
  "required": ["success", "entities", "entity_count"]
}
```

### Example
**Input:**
```json
{
  "text": "John Smith works at Microsoft Corporation in Seattle, Washington. He started on January 15, 2023.",
  "language": "en"
}
```

**Output:**
```json
{
  "success": true,
  "entities": [
    {
      "text": "John Smith",
      "type": "PERSON",
      "confidence": 0.95,
      "position": {"start": 0, "end": 10}
    },
    {
      "text": "Microsoft Corporation",
      "type": "ORG",
      "confidence": 0.98,
      "position": {"start": 20, "end": 42}
    },
    {
      "text": "Seattle",
      "type": "GPE",
      "confidence": 0.92,
      "position": {"start": 46, "end": 53}
    },
    {
      "text": "Washington",
      "type": "GPE",
      "confidence": 0.94,
      "position": {"start": 55, "end": 65}
    },
    {
      "text": "January 15, 2023",
      "type": "DATE",
      "confidence": 0.89,
      "position": {"start": 85, "end": 101}
    }
  ],
  "entity_count": 5,
  "processing_time": 0.25,
  "entity_types": {
    "PERSON": 1,
    "ORG": 1,
    "GPE": 2,
    "DATE": 1,
    "MONEY": 0
  }
}
```

### Safety & Reliability
- Handles various text formats and encodings
- Provides confidence scores for each entity
- Supports multiple languages and entity types
- Robust error handling for malformed input
- No sensitive data persistence
