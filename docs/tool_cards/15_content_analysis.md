# Tool Card: content_analysis

## General Info

- **Name**: content_analysis
- **Title**: Comprehensive Content Analysis Engine
- **Version**: 2.0.0
- **Author**: DIA3 Development Team
- **Description**: Perform comprehensive content analysis across multiple domains with advanced text processing, semantic understanding, and contextual insights

## Required Libraries

### Core Python Libraries
```python
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import numpy as np
import pandas as pd
```

### NLP and Text Processing Libraries
```python
import spacy>=3.7.0
import nltk>=3.8.1
import textblob>=0.17.1
import vaderSentiment>=3.3.2
import gensim>=4.3.2
import transformers>=4.35.0
import sentence-transformers>=2.2.2
```

### Machine Learning Libraries
```python
import scikit-learn>=1.3.2
import tensorflow>=2.15.0
import torch>=2.1.0
import numpy>=1.24.3
import pandas>=2.1.4
```

### Text Analysis Libraries
```python
import textstat>=0.7.3
import readability>=0.3.1
import textacy>=0.15.0
import pytextrank>=3.2.4
```

### Visualization Libraries
```python
import plotly>=5.17.0
import matplotlib>=3.8.2
import seaborn>=0.13.0
import wordcloud>=1.9.2
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
import re
import hashlib
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
import spacy
import nltk
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import transformers
from transformers import pipeline
import textstat
import readability
import textacy
import pytextrank
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
from datetime import datetime
import re
import hashlib

# MCP Tool Decorator
@self.mcp.tool(description="Comprehensive content analysis across multiple domains")
```

## Intended Use

- Perform comprehensive content analysis on text, documents, and multimedia content
- Extract key insights, themes, and patterns from content
- Analyze readability, complexity, and linguistic features
- Identify topics, entities, and relationships
- Generate content summaries and key points
- Support multiple content types and languages
- Provide contextual analysis and recommendations

## Out-of-Scope / Limitations

- Maximum content size: 50MB per analysis
- Processing time: Up to 10 minutes for complex content
- Memory usage: Up to 4GB for large documents
- Requires sufficient content for meaningful analysis
- Some advanced features may require specific content formats
- Real-time analysis limited by processing capabilities

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "content": {
      "type": "string",
      "description": "Content to analyze (text, document, or content URL)"
    },
    "content_type": {
      "type": "string",
      "enum": ["text", "document", "url", "file"],
      "default": "text",
      "description": "Type of content to analyze"
    },
    "language": {
      "type": "string",
      "default": "en",
      "description": "Language of the content"
    },
    "analysis_type": {
      "type": "string",
      "enum": ["comprehensive", "semantic", "linguistic", "thematic", "entity", "summary"],
      "default": "comprehensive",
      "description": "Type of content analysis to perform"
    },
    "include_readability_analysis": {
      "type": "boolean",
      "default": true,
      "description": "Include readability and complexity analysis"
    },
    "include_sentiment_analysis": {
      "type": "boolean",
      "default": true,
      "description": "Include sentiment and emotion analysis"
    },
    "include_topic_modeling": {
      "type": "boolean",
      "default": true,
      "description": "Include topic modeling and theme extraction"
    },
    "include_entity_extraction": {
      "type": "boolean",
      "default": true,
      "description": "Include named entity recognition"
    },
    "include_keyword_extraction": {
      "type": "boolean",
      "default": true,
      "description": "Include keyword and key phrase extraction"
    },
    "include_visualizations": {
      "type": "boolean",
      "default": true,
      "description": "Include content analysis visualizations"
    },
    "max_topics": {
      "type": "integer",
      "default": 10,
      "minimum": 1,
      "maximum": 50,
      "description": "Maximum number of topics to extract"
    },
    "max_keywords": {
      "type": "integer",
      "default": 20,
      "minimum": 5,
      "maximum": 100,
      "description": "Maximum number of keywords to extract"
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
    "analysis_id": {"type": "string"},
    "content_overview": {
      "type": "object",
      "properties": {
        "content_length": {"type": "number"},
        "word_count": {"type": "number"},
        "sentence_count": {"type": "number"},
        "paragraph_count": {"type": "number"},
        "language_detected": {"type": "string"},
        "content_type": {"type": "string"}
      }
    },
    "readability_analysis": {
      "type": "object",
      "properties": {
        "flesch_reading_ease": {"type": "number"},
        "flesch_kincaid_grade": {"type": "number"},
        "gunning_fog_index": {"type": "number"},
        "smog_index": {"type": "number"},
        "automated_readability_index": {"type": "number"},
        "coleman_liau_index": {"type": "number"},
        "linsear_write_formula": {"type": "number"},
        "dale_chall_readability": {"type": "number"},
        "readability_level": {"type": "string"},
        "complexity_score": {"type": "number"}
      }
    },
    "linguistic_analysis": {
      "type": "object",
      "properties": {
        "pos_distribution": {"type": "object"},
        "sentence_length_stats": {"type": "object"},
        "word_length_stats": {"type": "object"},
        "vocabulary_diversity": {"type": "number"},
        "lexical_density": {"type": "number"},
        "grammar_quality": {"type": "object"},
        "writing_style": {"type": "object"}
      }
    },
    "sentiment_analysis": {
      "type": "object",
      "properties": {
        "overall_sentiment": {"type": "string"},
        "sentiment_scores": {"type": "object"},
        "emotion_analysis": {"type": "object"},
        "tone_analysis": {"type": "object"},
        "sentiment_by_section": {"type": "array"}
      }
    },
    "topic_modeling": {
      "type": "object",
      "properties": {
        "topics": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "topic_id": {"type": "integer"},
              "topic_words": {"type": "array"},
              "topic_weight": {"type": "number"},
              "topic_coherence": {"type": "number"}
            }
          }
        },
        "topic_distribution": {"type": "object"},
        "topic_evolution": {"type": "array"}
      }
    },
    "entity_extraction": {
      "type": "object",
      "properties": {
        "entities": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "text": {"type": "string"},
              "type": {"type": "string"},
              "confidence": {"type": "number"},
              "frequency": {"type": "number"}
            }
          }
        },
        "entity_types": {"type": "object"},
        "entity_relationships": {"type": "array"}
      }
    },
    "keyword_extraction": {
      "type": "object",
      "properties": {
        "keywords": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "keyword": {"type": "string"},
              "score": {"type": "number"},
              "frequency": {"type": "number"},
              "position": {"type": "array"}
            }
          }
        },
        "key_phrases": {"type": "array"},
        "keyword_categories": {"type": "object"}
      }
    },
    "semantic_analysis": {
      "type": "object",
      "properties": {
        "semantic_similarity": {"type": "object"},
        "concept_extraction": {"type": "array"},
        "semantic_clusters": {"type": "array"},
        "contextual_meaning": {"type": "object"}
      }
    },
    "content_summary": {
      "type": "object",
      "properties": {
        "executive_summary": {"type": "string"},
        "key_points": {"type": "array"},
        "main_themes": {"type": "array"},
        "summary_statistics": {"type": "object"}
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "wordcloud_path": {"type": "string"},
        "topic_visualization_path": {"type": "string"},
        "sentiment_timeline_path": {"type": "string"},
        "entity_network_path": {"type": "string"},
        "readability_chart_path": {"type": "string"}
      }
    },
    "insights_and_recommendations": {
      "type": "object",
      "properties": {
        "content_insights": {"type": "array"},
        "improvement_suggestions": {"type": "array"},
        "target_audience_analysis": {"type": "object"},
        "content_optimization": {"type": "array"}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "analysis_time": {"type": "string"},
        "analysis_type": {"type": "string"},
        "processing_time": {"type": "number"},
        "models_used": {"type": "array"}
      }
    },
    "errors": {"type": "array"},
    "warnings": {"type": "array"}
  },
  "required": ["success", "analysis_id", "content_overview"]
}
```

## Example

### Input:
```json
{
  "content": "The rapid advancement of artificial intelligence and machine learning technologies has transformed various industries, from healthcare to finance. These technologies enable organizations to process vast amounts of data, identify patterns, and make informed decisions. However, the implementation of AI systems also raises important ethical considerations regarding privacy, bias, and accountability. Organizations must carefully balance innovation with responsible AI development to ensure these technologies benefit society while minimizing potential risks.",
  "content_type": "text",
  "language": "en",
  "analysis_type": "comprehensive",
  "include_readability_analysis": true,
  "include_sentiment_analysis": true,
  "include_topic_modeling": true,
  "include_entity_extraction": true,
  "include_keyword_extraction": true,
  "max_topics": 5,
  "max_keywords": 15
}
```

### Output:
```json
{
  "success": true,
  "analysis_id": "content_20241201_001",
  "content_overview": {
    "content_length": 456,
    "word_count": 89,
    "sentence_count": 4,
    "paragraph_count": 1,
    "language_detected": "en",
    "content_type": "text"
  },
  "readability_analysis": {
    "flesch_reading_ease": 45.2,
    "flesch_kincaid_grade": 12.8,
    "gunning_fog_index": 15.3,
    "smog_index": 12.1,
    "automated_readability_index": 12.5,
    "coleman_liau_index": 13.2,
    "linsear_write_formula": 12.8,
    "dale_chall_readability": 8.7,
    "readability_level": "college",
    "complexity_score": 0.72
  },
  "linguistic_analysis": {
    "pos_distribution": {
      "nouns": 0.28,
      "verbs": 0.18,
      "adjectives": 0.12,
      "adverbs": 0.08,
      "pronouns": 0.06,
      "prepositions": 0.15,
      "conjunctions": 0.08,
      "articles": 0.05
    },
    "sentence_length_stats": {
      "average": 22.25,
      "median": 21.5,
      "std_dev": 3.2,
      "min": 19,
      "max": 26
    },
    "word_length_stats": {
      "average": 5.1,
      "median": 5.0,
      "std_dev": 2.3,
      "min": 2,
      "max": 12
    },
    "vocabulary_diversity": 0.85,
    "lexical_density": 0.68,
    "grammar_quality": {
      "grammar_score": 0.92,
      "spelling_errors": 0,
      "punctuation_errors": 0
    },
    "writing_style": {
      "formality": "formal",
      "tone": "academic",
      "complexity": "high"
    }
  },
  "sentiment_analysis": {
    "overall_sentiment": "neutral",
    "sentiment_scores": {
      "positive": 0.35,
      "neutral": 0.45,
      "negative": 0.20
    },
    "emotion_analysis": {
      "concern": 0.25,
      "optimism": 0.30,
      "neutrality": 0.45
    },
    "tone_analysis": {
      "tone": "analytical",
      "formality": "high",
      "objectivity": "high"
    },
    "sentiment_by_section": [
      {
        "section": "introduction",
        "sentiment": "positive",
        "score": 0.65
      },
      {
        "section": "main_content",
        "sentiment": "neutral",
        "score": 0.45
      },
      {
        "section": "conclusion",
        "sentiment": "neutral",
        "score": 0.40
      }
    ]
  },
  "topic_modeling": {
    "topics": [
      {
        "topic_id": 1,
        "topic_words": ["artificial", "intelligence", "machine", "learning", "technologies"],
        "topic_weight": 0.35,
        "topic_coherence": 0.78
      },
      {
        "topic_id": 2,
        "topic_words": ["industries", "healthcare", "finance", "organizations", "data"],
        "topic_weight": 0.28,
        "topic_coherence": 0.72
      },
      {
        "topic_id": 3,
        "topic_words": ["ethical", "considerations", "privacy", "bias", "accountability"],
        "topic_weight": 0.22,
        "topic_coherence": 0.75
      },
      {
        "topic_id": 4,
        "topic_words": ["innovation", "responsible", "development", "society", "risks"],
        "topic_weight": 0.15,
        "topic_coherence": 0.68
      }
    ],
    "topic_distribution": {
      "AI_technologies": 0.35,
      "industry_applications": 0.28,
      "ethical_concerns": 0.22,
      "responsible_development": 0.15
    },
    "topic_evolution": [
      {
        "position": "beginning",
        "dominant_topic": "AI_technologies"
      },
      {
        "position": "middle",
        "dominant_topic": "industry_applications"
      },
      {
        "position": "end",
        "dominant_topic": "ethical_concerns"
      }
    ]
  },
  "entity_extraction": {
    "entities": [
      {
        "text": "artificial intelligence",
        "type": "TECHNOLOGY",
        "confidence": 0.95,
        "frequency": 1
      },
      {
        "text": "machine learning",
        "type": "TECHNOLOGY",
        "confidence": 0.92,
        "frequency": 1
      },
      {
        "text": "healthcare",
        "type": "INDUSTRY",
        "confidence": 0.88,
        "frequency": 1
      },
      {
        "text": "finance",
        "type": "INDUSTRY",
        "confidence": 0.88,
        "frequency": 1
      },
      {
        "text": "organizations",
        "type": "ORGANIZATION",
        "confidence": 0.85,
        "frequency": 2
      }
    ],
    "entity_types": {
      "TECHNOLOGY": 2,
      "INDUSTRY": 2,
      "ORGANIZATION": 1
    },
    "entity_relationships": [
      {
        "source": "artificial intelligence",
        "target": "healthcare",
        "relationship": "applied_in"
      },
      {
        "source": "machine learning",
        "target": "finance",
        "relationship": "applied_in"
      }
    ]
  },
  "keyword_extraction": {
    "keywords": [
      {
        "keyword": "artificial intelligence",
        "score": 0.95,
        "frequency": 1,
        "position": [0, 25]
      },
      {
        "keyword": "machine learning",
        "score": 0.92,
        "frequency": 1,
        "position": [26, 42]
      },
      {
        "keyword": "technologies",
        "score": 0.88,
        "frequency": 1,
        "position": [43, 55]
      },
      {
        "keyword": "industries",
        "score": 0.85,
        "frequency": 1,
        "position": [56, 66]
      },
      {
        "keyword": "healthcare",
        "score": 0.82,
        "frequency": 1,
        "position": [67, 77]
      },
      {
        "keyword": "finance",
        "score": 0.82,
        "frequency": 1,
        "position": [78, 86]
      },
      {
        "keyword": "data",
        "score": 0.78,
        "frequency": 1,
        "position": [87, 91]
      },
      {
        "keyword": "ethical considerations",
        "score": 0.75,
        "frequency": 1,
        "position": [92, 113]
      },
      {
        "keyword": "privacy",
        "score": 0.72,
        "frequency": 1,
        "position": [114, 121]
      },
      {
        "keyword": "bias",
        "score": 0.70,
        "frequency": 1,
        "position": [122, 126]
      },
      {
        "keyword": "accountability",
        "score": 0.68,
        "frequency": 1,
        "position": [127, 139]
      },
      {
        "keyword": "innovation",
        "score": 0.65,
        "frequency": 1,
        "position": [140, 150]
      },
      {
        "keyword": "responsible development",
        "score": 0.62,
        "frequency": 1,
        "position": [151, 170]
      },
      {
        "keyword": "society",
        "score": 0.60,
        "frequency": 1,
        "position": [171, 178]
      },
      {
        "keyword": "risks",
        "score": 0.58,
        "frequency": 1,
        "position": [179, 184]
      }
    ],
    "key_phrases": [
      "artificial intelligence and machine learning",
      "various industries",
      "ethical considerations",
      "responsible AI development"
    ],
    "keyword_categories": {
      "technology": ["artificial intelligence", "machine learning", "technologies"],
      "industry": ["industries", "healthcare", "finance"],
      "ethics": ["ethical considerations", "privacy", "bias", "accountability"],
      "development": ["innovation", "responsible development", "society", "risks"]
    }
  },
  "semantic_analysis": {
    "semantic_similarity": {
      "ai_ml_similarity": 0.85,
      "healthcare_finance_similarity": 0.72,
      "ethics_risk_similarity": 0.68
    },
    "concept_extraction": [
      "technological advancement",
      "industry transformation",
      "data processing",
      "decision making",
      "ethical responsibility"
    ],
    "semantic_clusters": [
      {
        "cluster": "technology",
        "concepts": ["artificial intelligence", "machine learning", "technologies"]
      },
      {
        "cluster": "application",
        "concepts": ["industries", "healthcare", "finance", "data processing"]
      },
      {
        "cluster": "ethics",
        "concepts": ["ethical considerations", "privacy", "bias", "accountability"]
      }
    ],
    "contextual_meaning": {
      "primary_context": "technology_ethics",
      "secondary_contexts": ["industry_applications", "responsible_development"]
    }
  },
  "content_summary": {
    "executive_summary": "This text discusses the transformative impact of AI and machine learning technologies across industries, while emphasizing the importance of ethical considerations in their development and implementation.",
    "key_points": [
      "AI and ML technologies are transforming various industries",
      "These technologies enable data processing and informed decision-making",
      "Ethical considerations include privacy, bias, and accountability",
      "Organizations must balance innovation with responsible development"
    ],
    "main_themes": [
      "Technological advancement and innovation",
      "Industry transformation and applications",
      "Ethical considerations and responsibility",
      "Balanced development approach"
    ],
    "summary_statistics": {
      "main_topics": 4,
      "key_entities": 5,
      "sentiment_balance": "neutral",
      "complexity_level": "college"
    }
  },
  "visualizations": {
    "wordcloud_path": "/Results/wordcloud_20241201_001.html",
    "topic_visualization_path": "/Results/topics_20241201_001.html",
    "sentiment_timeline_path": "/Results/sentiment_20241201_001.html",
    "entity_network_path": "/Results/entities_20241201_001.html",
    "readability_chart_path": "/Results/readability_20241201_001.html"
  },
  "insights_and_recommendations": {
    "content_insights": [
      "Content demonstrates high academic complexity suitable for college-level readers",
      "Balanced discussion of both benefits and challenges of AI technologies",
      "Strong emphasis on ethical considerations and responsible development",
      "Clear structure with logical flow from technology to applications to ethics"
    ],
    "improvement_suggestions": [
      "Consider adding specific examples of AI applications in healthcare and finance",
      "Include more concrete recommendations for responsible AI development",
      "Provide statistical data to support claims about industry transformation",
      "Add citations or references to strengthen credibility"
    ],
    "target_audience_analysis": {
      "primary_audience": "academic_professionals",
      "secondary_audience": "industry_decision_makers",
      "suitable_for": ["research_papers", "policy_documents", "educational_materials"],
      "reading_level": "college_graduate"
    },
    "content_optimization": [
      "Maintain formal tone for academic audience",
      "Include more specific examples and case studies",
      "Add visual elements to support complex concepts",
      "Consider breaking into shorter paragraphs for better readability"
    ]
  },
  "metadata": {
    "analysis_time": "2024-12-01T10:30:00Z",
    "analysis_type": "comprehensive",
    "processing_time": 8.5,
    "models_used": ["spacy", "transformers", "textstat", "gensim", "vaderSentiment"]
  },
  "errors": [],
  "warnings": []
}
```

## Safety & Reliability

- Validates content format and language specifications
- Implements multiple analysis algorithms for robustness
- Provides confidence scores for all extracted information
- Includes content quality validation
- Handles various content formats and languages
- Supports incremental analysis for large documents
- Implements proper content privacy and security measures

## Runbook

### Setup Instructions
1. Install required dependencies: `pip install -r requirements-phase5.txt`
2. Configure NLP models in `config/nlp_config.py`
3. Set up content analysis pipelines
4. Configure visualization settings
5. Test with sample content before production use

### Usage Examples
```python
# Basic content analysis
result = await content_analysis(
    content="Sample text content for analysis...",
    content_type="text",
    analysis_type="comprehensive"
)

# Semantic-focused analysis
result = await content_analysis(
    content="Document content for semantic analysis...",
    content_type="document",
    analysis_type="semantic",
    include_topic_modeling=True
)

# Linguistic analysis
result = await content_analysis(
    content="Text for linguistic analysis...",
    analysis_type="linguistic",
    include_readability_analysis=True
)
```

### Error Handling
- Invalid content format: Returns error with format requirements
- Unsupported language: Returns error with supported languages
- Insufficient content: Returns warning with minimum content requirements
- Model loading failure: Falls back to basic text analysis
- Processing timeout: Returns partial results with timeout warning

### Monitoring
- Content analysis accuracy metrics
- Processing time monitoring
- Model performance tracking
- Error rate monitoring
- Content quality assessment
- Analysis coverage tracking
