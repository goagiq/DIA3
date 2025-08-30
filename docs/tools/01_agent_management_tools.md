# Agent Management MCP Tools

## Tool Card: get_all_agents_status

### General Info
- **Name**: get_all_agents_status
- **Title**: Agent Status Monitor
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Retrieves comprehensive status information for all available agents in the system.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)

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
from typing import Dict, Any

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Get status of all available agents")
async def get_all_agents_status():
```

### Intended Use
- For system administrators and monitoring systems
- Real-time agent health monitoring
- Debugging agent initialization issues
- Performance monitoring and optimization

### Out-of-Scope / Limitations
- Read-only access; no agent control
- Limited to status information only
- Requires active agent instances
- No historical status tracking

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
    "total_agents": {"type": "integer"},
    "agents": {
      "type": "object",
      "properties": {
        "text": {"type": "object"},
        "audio": {"type": "object"},
        "vision": {"type": "object"},
        "web": {"type": "object"},
        "ocr": {"type": "object"},
        "orchestrator": {"type": "object"},
        "knowledge_graph": {"type": "object"},
        "file_extraction": {"type": "object"}
      }
    },
    "services": {"type": "object"}
  },
  "required": ["success", "total_agents", "agents", "services"]
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
  "total_agents": 8,
  "agents": {
    "text": {
      "agent_id": "text_agent",
      "status": "active",
      "type": "TextProcessingAgent"
    },
    "audio": {
      "agent_id": "audio_agent", 
      "status": "active",
      "type": "AudioProcessingAgent"
    }
  },
  "services": {
    "vector_db": "initialized",
    "translation_service": "ready"
  }
}
```

### Safety & Reliability
- Validates agent existence before status check
- Graceful error handling for missing agents
- No side effects on agent operation
- Safe for concurrent access

---

## Tool Card: start_all_agents

### General Info
- **Name**: start_all_agents
- **Title**: Agent Swarm Starter
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Initializes and starts all available agents in the system.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)

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
from typing import Dict, Any

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Start all agents")
async def start_all_agents():
```

### Intended Use
- System initialization
- Recovery from agent failures
- Batch agent startup for processing
- Development and testing environments

### Out-of-Scope / Limitations
- Cannot start individual agents
- Requires proper agent configuration
- May fail if dependencies unavailable
- No rollback on partial failures

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
    "results": {
      "type": "object",
      "properties": {
        "text": {"type": "object"},
        "audio": {"type": "object"},
        "vision": {"type": "object"},
        "web": {"type": "object"},
        "ocr": {"type": "object"},
        "orchestrator": {"type": "object"},
        "knowledge_graph": {"type": "object"},
        "file_extraction": {"type": "object"}
      }
    }
  },
  "required": ["success", "results"]
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
  "results": {
    "text": {"success": true, "message": "Started"},
    "audio": {"success": true, "message": "Started"},
    "vision": {"success": true, "message": "Started"},
    "web": {"success": true, "message": "Started"},
    "ocr": {"success": true, "message": "Started"},
    "orchestrator": {"success": true, "message": "Started"},
    "knowledge_graph": {"success": true, "message": "Started"},
    "file_extraction": {"success": true, "message": "Started"}
  }
}
```

### Safety & Reliability
- Individual agent failure doesn't stop others
- Comprehensive error reporting
- Safe for repeated calls
- Validates agent availability before starting

---

## Tool Card: stop_all_agents

### General Info
- **Name**: stop_all_agents
- **Title**: Agent Swarm Stopper
- **Version**: 1.0.0
- **Author**: DIA3 Development Team
- **Description**: Gracefully stops all running agents in the system.

### Required Libraries
```python
# Core Python Libraries
asyncio
logging
typing (Dict, List, Any, Optional)

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
from typing import Dict, Any

logger = logging.getLogger(__name__)

@self.mcp.tool(description="Stop all agents")
async def stop_all_agents():
```

### Intended Use
- System shutdown procedures
- Resource cleanup
- Maintenance operations
- Development environment reset

### Out-of-Scope / Limitations
- Cannot stop individual agents
- May take time for graceful shutdown
- No forced termination
- Requires proper agent stop methods

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
    "results": {
      "type": "object",
      "properties": {
        "text": {"type": "object"},
        "audio": {"type": "object"},
        "vision": {"type": "object"},
        "web": {"type": "object"},
        "ocr": {"type": "object"},
        "orchestrator": {"type": "object"},
        "knowledge_graph": {"type": "object"},
        "file_extraction": {"type": "object"}
      }
    }
  },
  "required": ["success", "results"]
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
  "results": {
    "text": {"success": true, "message": "Stopped"},
    "audio": {"success": true, "message": "Stopped"},
    "vision": {"success": true, "message": "Stopped"},
    "web": {"success": true, "message": "Stopped"},
    "ocr": {"success": true, "message": "Stopped"},
    "orchestrator": {"success": true, "message": "Stopped"},
    "knowledge_graph": {"success": true, "message": "Stopped"},
    "file_extraction": {"success": true, "message": "Stopped"}
  }
}
```

### Safety & Reliability
- Graceful shutdown for each agent
- Individual agent failure doesn't affect others
- Comprehensive status reporting
- Safe for repeated calls
