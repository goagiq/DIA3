# Report Generation & System Management MCP Tools

## Tool Card: generate_graph_report

### General Info
- **Name**: generate_graph_report
- **Title**: Knowledge Graph Report Generator
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Generates comprehensive knowledge graph reports with multilingual support and visualization.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)
pathlib
datetime

# Report Generation
jinja2>=3.1.0
markdown>=3.4.0
weasyprint>=60.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.15.0

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
from datetime import datetime

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Generate knowledge graph report")
async def generate_graph_report(
    output_path: str = None,
    target_language: str = "en"
):
```

### Intended Use
- Knowledge graph analysis reporting
- Research documentation
- Intelligence briefings
- Academic research reports
- Business intelligence reports

### Out-of-Scope / Limitations
- Requires existing knowledge graph data
- Limited to supported languages
- Report format customization limited
- May take time for large graphs

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "output_path": {
      "type": "string",
      "description": "Optional output path for the report"
    },
    "target_language": {
      "type": "string",
      "description": "Language for report generation",
      "default": "en"
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
    "report_files": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "file_path": {"type": "string"},
          "format": {"type": "string"},
          "size": {"type": "integer"}
        }
      }
    },
    "output_path": {"type": "string"},
    "generation_time": {"type": "number"},
    "report_metadata": {
      "type": "object",
      "properties": {
        "node_count": {"type": "integer"},
        "edge_count": {"type": "integer"},
        "language": {"type": "string"}
      }
    }
  },
  "required": ["success", "report_files", "output_path"]
}
```

### Example
**Input:**
```json
{
  "output_path": "/reports/knowledge_graph_analysis",
  "target_language": "en"
}
```

**Output:**
```json
{
  "success": true,
  "report_files": [
    {
      "file_path": "/reports/knowledge_graph_analysis.html",
      "format": "html",
      "size": 245000
    },
    {
      "file_path": "/reports/knowledge_graph_analysis.pdf",
      "format": "pdf",
      "size": 180000
    }
  ],
  "output_path": "/reports/knowledge_graph_analysis",
  "generation_time": 45.2,
  "report_metadata": {
    "node_count": 3450,
    "edge_count": 12800,
    "language": "en"
  }
}
```

### Safety & Reliability
- Validates output directory permissions
- Handles large datasets efficiently
- Supports multiple output formats
- Comprehensive error handling
- Safe file operations

---

## Tool Card: comprehensive_threat_assessment

### General Info
- **Name**: comprehensive_threat_assessment
- **Title**: Comprehensive Threat Assessment Engine
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Performs comprehensive threat assessment with deception detection and warning indicators.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)
json

# Threat Analysis
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0

# NLP and Analysis
spacy>=3.5.0
transformers>=4.30.0
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
import json
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Comprehensive threat assessment with deception detection and warning indicators")
async def comprehensive_threat_assessment(
    content: str,
    assessment_type: str = "comprehensive",
    include_deception_detection: bool = True
) -> Dict[str, Any]:
```

### Intended Use
- Security threat analysis
- Risk assessment and management
- Intelligence analysis
- Deception detection
- Strategic planning support

### Out-of-Scope / Limitations
- Requires relevant content input
- Limited to supported threat types
- May not detect sophisticated deception
- Context-dependent accuracy

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "content": {
      "type": "string",
      "description": "Content to assess for threats"
    },
    "assessment_type": {
      "type": "string",
      "enum": ["comprehensive", "cyber", "physical", "social"],
      "description": "Type of threat assessment",
      "default": "comprehensive"
    },
    "include_deception_detection": {
      "type": "boolean",
      "description": "Whether to include deception detection",
      "default": true
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
    "threat_assessment": {
      "type": "object",
      "properties": {
        "overall_risk_level": {
          "type": "string",
          "enum": ["low", "medium", "high", "critical"]
        },
        "threat_indicators": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "indicator": {"type": "string"},
              "confidence": {"type": "number"},
              "severity": {"type": "string"}
            }
          }
        },
        "deception_detection": {
          "type": "object",
          "properties": {
            "deception_score": {"type": "number"},
            "deception_indicators": {"type": "array"},
            "confidence": {"type": "number"}
          }
        },
        "recommendations": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    },
    "processing_time": {"type": "number"}
  },
  "required": ["success", "threat_assessment"]
}
```

### Example
**Input:**
```json
{
  "content": "Analysis of recent cyber attacks and potential threats to critical infrastructure...",
  "assessment_type": "comprehensive",
  "include_deception_detection": true
}
```

**Output:**
```json
{
  "success": true,
  "threat_assessment": {
    "overall_risk_level": "high",
    "threat_indicators": [
      {
        "indicator": "cyber_attack_patterns",
        "confidence": 0.85,
        "severity": "high"
      },
      {
        "indicator": "infrastructure_targeting",
        "confidence": 0.78,
        "severity": "medium"
      }
    ],
    "deception_detection": {
      "deception_score": 0.65,
      "deception_indicators": [
        "inconsistent_timeline",
        "suspicious_source_patterns"
      ],
      "confidence": 0.72
    },
    "recommendations": [
      "Implement enhanced cybersecurity measures",
      "Conduct regular threat assessments",
      "Improve deception detection capabilities"
    ]
  },
  "processing_time": 12.5
}
```

### Safety & Reliability
- Validates input content quality
- Provides confidence scores
- Handles various content types
- Comprehensive threat coverage
- Ethical analysis guidelines

---

## Tool Card: system_health_check

### General Info
- **Name**: system_health_check
- **Title**: System Health and Status Monitor
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Comprehensive system health check and status monitoring for all components.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)
psutil
platform

# System Monitoring
psutil>=5.9.0
GPUtil>=1.4.0

# Database Monitoring
sqlite3
redis>=4.5.0

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
import psutil
import platform
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

@self.mcp.tool(description="System health and status")
async def system_health_check() -> Dict[str, Any]:
```

### Intended Use
- System monitoring and health checks
- Performance monitoring
- Resource utilization tracking
- Troubleshooting support
- Capacity planning

### Out-of-Scope / Limitations
- Limited to system-level metrics
- May not detect application-specific issues
- Requires appropriate permissions
- Platform-specific limitations

### Input Schema
```json
{
  "type": "object",
  "properties": {},
  "required": []
}
```

### Output Schema
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "system_status": {
      "type": "object",
      "properties": {
        "overall_health": {
          "type": "string",
          "enum": ["healthy", "warning", "critical"]
        },
        "cpu_usage": {"type": "number"},
        "memory_usage": {"type": "number"},
        "disk_usage": {"type": "number"},
        "network_status": {"type": "object"},
        "services": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "service_name": {"type": "string"},
              "status": {"type": "string"},
              "uptime": {"type": "number"}
            }
          }
        }
      }
    },
    "performance_metrics": {
      "type": "object",
      "properties": {
        "response_time": {"type": "number"},
        "throughput": {"type": "number"},
        "error_rate": {"type": "number"}
      }
    },
    "timestamp": {"type": "string"}
  },
  "required": ["success", "system_status"]
}
```

### Example
**Input:**
```json
{}
```

**Output:**
```json
{
  "success": true,
  "system_status": {
    "overall_health": "healthy",
    "cpu_usage": 45.2,
    "memory_usage": 67.8,
    "disk_usage": 23.4,
    "network_status": {
      "connections": 125,
      "bandwidth_usage": 12.5
    },
    "services": [
      {
        "service_name": "mcp_server",
        "status": "running",
        "uptime": 3600
      },
      {
        "service_name": "vector_db",
        "status": "running",
        "uptime": 7200
      }
    ]
  },
  "performance_metrics": {
    "response_time": 0.15,
    "throughput": 1250,
    "error_rate": 0.001
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Safety & Reliability
- Non-intrusive monitoring
- Safe system metrics collection
- Comprehensive health indicators
- Real-time status updates
- Performance impact minimization

---

## Tool Card: configuration_management

### General Info
- **Name**: configuration_management
- **Title**: System Configuration Manager
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Manages system configuration settings, updates, and validation.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)
json
pathlib

# Configuration Management
pyyaml>=6.0
configparser>=5.3.0
jsonschema>=4.17.0

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
import json
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Configuration management")
async def configuration_management(
    action: str,
    config_data: Dict[str, Any] = None,
    config_path: str = None
) -> Dict[str, Any]:
```

### Intended Use
- System configuration management
- Settings validation and updates
- Configuration backup and restore
- Environment-specific configurations
- Configuration version control

### Out-of-Scope / Limitations
- Limited to supported configuration formats
- Requires appropriate permissions
- May require system restart for some changes
- Configuration validation rules apply

### Input Schema
```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": ["get", "set", "validate", "backup", "restore"],
      "description": "Configuration action to perform"
    },
    "config_data": {
      "type": "object",
      "description": "Configuration data for set action"
    },
    "config_path": {
      "type": "string",
      "description": "Path to configuration file"
    }
  },
  "required": ["action"]
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
        "current_config": {"type": "object"},
        "validation_results": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "field": {"type": "string"},
              "status": {"type": "string"},
              "message": {"type": "string"}
            }
          }
        },
        "backup_path": {"type": "string"},
        "restore_status": {"type": "string"}
      }
    },
    "timestamp": {"type": "string"}
  },
  "required": ["success", "result"]
}
```

### Example
**Input:**
```json
{
  "action": "get",
  "config_path": "/config/system.json"
}
```

**Output:**
```json
{
  "success": true,
  "result": {
    "current_config": {
      "server": {
        "host": "localhost",
        "port": 8000,
        "debug": false
      },
      "database": {
        "type": "sqlite",
        "path": "/data/app.db"
      },
      "logging": {
        "level": "INFO",
        "file": "/logs/app.log"
      }
    },
    "validation_results": [
      {
        "field": "server.port",
        "status": "valid",
        "message": "Port number is within valid range"
      }
    ]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Safety & Reliability
- Configuration validation before application
- Backup creation before changes
- Rollback capabilities
- Comprehensive error handling
- Audit trail for changes
