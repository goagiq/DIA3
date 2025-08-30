# Tool Card: analyze_sentiment

## General Info

- **Name**: analyze_sentiment
- **Title**: Sentiment Analysis with Multilingual Support
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Advanced sentiment analysis with multilingual support, emotion detection, and context-aware analysis

## Required Libraries

### Core Python Libraries
```python
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
import re
from datetime import datetime
```

### Machine Learning Libraries
```python
import numpy>=1.24.3
import pandas>=2.1.4
import scikit-learn>=1.3.2
import transformers>=4.35.0
import torch>=2.1.0
```

### NLP and Text Processing
```python
import nltk>=3.8.1
import spacy>=3.7.0
import textblob>=0.17.1
import vaderSentiment>=3.3.2
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
from transformers import pipeline
import torch

# MCP Tool Decorator
@self.mcp.tool(description="Sentiment analysis with multilingual support")
```

## Intended Use

- Analyze sentiment of text content in multiple languages
- Detect emotions and emotional intensity
- Provide context-aware sentiment analysis
- Support batch processing of multiple texts
- Generate sentiment trends and patterns
- Integrate with content processing pipeline

## Out-of-Scope / Limitations

- Maximum text length: 10,000 characters per analysis
- Supported languages: English, Spanish, French, German, Chinese, Arabic, Russian
- Requires sufficient text for accurate analysis (minimum 10 words)
- Processing time scales with text length
- Some languages may have reduced accuracy

## Input Schema

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
      "default": "auto",
      "description": "Language code or 'auto' for detection"
    },
    "analysis_type": {
      "type": "string",
      "enum": ["basic", "detailed", "emotion", "contextual"],
      "default": "detailed",
      "description": "Type of sentiment analysis"
    },
    "include_confidence": {
      "type": "boolean",
      "default": true,
      "description": "Include confidence scores"
    },
    "context": {
      "type": "object",
      "description": "Additional context for analysis"
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
    "analysis_id": {"type": "string"},
    "sentiment_results": {
      "type": "object",
      "properties": {
        "overall_sentiment": {
          "type": "string",
          "enum": ["positive", "negative", "neutral", "mixed"]
        },
        "sentiment_score": {"type": "number"},
        "confidence": {"type": "number"},
        "emotions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "emotion": {"type": "string"},
              "intensity": {"type": "number"},
              "confidence": {"type": "number"}
            }
          }
        },
        "aspects": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "aspect": {"type": "string"},
              "sentiment": {"type": "string"},
              "score": {"type": "number"}
            }
          }
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "language": {"type": "string"},
        "word_count": {"type": "number"},
        "processing_time": {"type": "number"},
        "model_used": {"type": "string"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "analysis_id", "sentiment_results"]
}
```

## Example

### Input:
```json
{
  "text": "The new cybersecurity measures are excellent and provide much better protection than before.",
  "language": "en",
  "analysis_type": "detailed",
  "include_confidence": true,
  "context": {
    "domain": "technology",
    "topic": "cybersecurity"
  }
}
```

### Output:
```json
{
  "success": true,
  "analysis_id": "sent_20241201_001",
  "sentiment_results": {
    "overall_sentiment": "positive",
    "sentiment_score": 0.85,
    "confidence": 0.92,
    "emotions": [
      {
        "emotion": "satisfaction",
        "intensity": 0.78,
        "confidence": 0.89
      },
      {
        "emotion": "approval",
        "intensity": 0.82,
        "confidence": 0.91
      }
    ],
    "aspects": [
      {
        "aspect": "cybersecurity measures",
        "sentiment": "positive",
        "score": 0.88
      },
      {
        "aspect": "protection",
        "sentiment": "positive",
        "score": 0.82
      }
    ]
  },
  "metadata": {
    "language": "en",
    "word_count": 15,
    "processing_time": 0.45,
    "model_used": "transformers-sentiment-v2"
  },
  "errors": [],
  "warnings": []
}
```

## Safety & Reliability

- Validates text input and language codes
- Implements content filtering for inappropriate content
- Provides confidence scores for all predictions
- Handles edge cases and malformed input gracefully
- Logs analysis requests for audit trail
- Supports rate limiting for high-volume requests
- Implements fallback models for reliability

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Download language models: `python -m spacy download en_core_web_sm`
3. Download NLTK data: `python -c "import nltk; nltk.download('vader_lexicon')"`
4. Configure model paths in `config/sentiment_config.py`
5. Set up GPU acceleration if available

### Usage Examples
```python
# Basic sentiment analysis
result = await analyze_sentiment(
    text="This is a positive statement.",
    language="en"
)

# Detailed emotion analysis
result = await analyze_sentiment(
    text="I'm very happy with the results!",
    analysis_type="emotion",
    include_confidence=True
)

# Contextual analysis
result = await analyze_sentiment(
    text="The security breach was concerning.",
    analysis_type="contextual",
    context={"domain": "cybersecurity"}
)
```

### Error Handling
- Invalid language code: Returns error with supported languages
- Text too short: Returns warning with minimum length requirement
- Model loading failure: Falls back to basic sentiment analysis
- Processing timeout: Returns partial results with timeout warning

### Monitoring
- Sentiment distribution metrics
- Processing time tracking
- Model accuracy monitoring
- Language detection accuracy
- Error rate tracking
- Resource usage monitoring
