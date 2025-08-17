# Dynamic MCP Tool Management System

## 🎯 **Overview**

The Dynamic MCP Tool Management System allows you to enable/disable MCP tools on the fly to optimize system resources. This is especially important for resource-intensive operations like Monte Carlo simulations, deep learning, and reinforcement learning.

## 🚀 **Key Features**

### **Dynamic Tool Management**
- ✅ Enable/disable tools at runtime
- ✅ Pause/resume tools temporarily
- ✅ Bulk operations for multiple tools
- ✅ Priority-based resource allocation

### **Resource Monitoring**
- ✅ Real-time CPU, memory, and GPU monitoring
- ✅ Resource usage history tracking
- ✅ Automatic resource level detection
- ✅ Health monitoring and auto-recovery

### **Auto-Scaling**
- ✅ Automatic tool scaling based on resource levels
- ✅ Priority-based tool management
- ✅ Configurable scaling thresholds
- ✅ Graceful resource cleanup

### **Configuration Management**
- ✅ JSON-based configuration files
- ✅ Runtime configuration updates
- ✅ Tool-specific resource limits
- ✅ Dependency management

## 📋 **Supported Tools**

| Tool | Priority | CPU Limit | Memory Limit | Status |
|------|----------|-----------|--------------|--------|
| **Monte Carlo** | 8 | 80% | 4GB | ✅ Enabled |
| **Deception Analysis** | 9 | 85% | 5GB | ✅ Enabled |
| **Language Processing** | 7 | 70% | 3GB | ✅ Enabled |
| **Sentiment Analysis** | 6 | 60% | 2GB | ✅ Enabled |
| **Business Intelligence** | 5 | 50% | 1.5GB | ✅ Enabled |
| **Audio Processing** | 6 | 65% | 2.5GB | ✅ Enabled |
| **Data Ingestion** | 7 | 55% | 2GB | ✅ Enabled |
| **Deep Learning** | 4 | 90% | 8GB | ❌ Disabled |
| **Reinforcement Learning** | 3 | 85% | 6GB | ❌ Disabled |
| **Video Processing** | 2 | 95% | 10GB | ❌ Disabled |

## 🛠️ **Installation & Setup**

### **1. Install Dependencies**
```bash
pip install psutil fastapi pydantic
```

### **2. Configuration File**
The system uses `config/mcp_tool_config.json` for tool configuration:

```json
{
  "auto_scaling_enabled": true,
  "tools": {
    "monte_carlo": {
      "enabled": true,
      "priority": 8,
      "max_cpu_percent": 80.0,
      "max_memory_mb": 4096.0,
      "auto_scale": true
    }
  }
}
```

### **3. Start the System**
```bash
# Start monitoring
python scripts/mcp_tool_manager.py start-monitoring

# Or via API
curl -X POST http://localhost:8000/mcp/tools/monitoring/start
```

## 📖 **Usage Guide**

### **Command Line Interface (CLI)**

#### **List All Tools**
```bash
python scripts/mcp_tool_manager.py list
python scripts/mcp_tool_manager.py list --show-resources
```

#### **Enable/Disable Tools**
```bash
# Enable a single tool
python scripts/mcp_tool_manager.py enable --tool monte_carlo

# Disable a tool
python scripts/mcp_tool_manager.py disable --tool deep_learning

# Enable multiple tools
python scripts/mcp_tool_manager.py enable-multiple --tools monte_carlo sentiment_analysis

# Disable multiple tools
python scripts/mcp_tool_manager.py disable-multiple --tools deep_learning reinforcement_learning
```

#### **Pause/Resume Tools**
```bash
# Pause a tool (temporarily disable)
python scripts/mcp_tool_manager.py pause --tool monte_carlo

# Resume a paused tool
python scripts/mcp_tool_manager.py resume --tool monte_carlo
```

#### **Resource Monitoring**
```bash
# Show system resources
python scripts/mcp_tool_manager.py resources

# Show system health
python scripts/mcp_tool_manager.py health
```

#### **Auto-Scaling Control**
```bash
# Enable auto-scaling
python scripts/mcp_tool_manager.py auto-scale --enabled true

# Disable auto-scaling
python scripts/mcp_tool_manager.py auto-scale --enabled false
```

#### **Configuration Updates**
```bash
# Update tool priority
python scripts/mcp_tool_manager.py config --tool monte_carlo --priority 9

# Update resource limits
python scripts/mcp_tool_manager.py config --tool monte_carlo --max-cpu 85 --max-memory 5120
```

### **API Endpoints**

#### **Tool Status**
```bash
# Get all tool statuses
curl http://localhost:8000/mcp/tools/status

# Get specific tool status
curl http://localhost:8000/mcp/tools/status/monte_carlo
```

#### **Tool Control**
```bash
# Enable tool
curl -X POST http://localhost:8000/mcp/tools/monte_carlo/enable

# Disable tool
curl -X POST http://localhost:8000/mcp/tools/deep_learning/disable

# Pause tool
curl -X POST http://localhost:8000/mcp/tools/monte_carlo/pause

# Resume tool
curl -X POST http://localhost:8000/mcp/tools/monte_carlo/resume
```

#### **Bulk Operations**
```bash
# Enable multiple tools
curl -X POST http://localhost:8000/mcp/tools/bulk/enable \
  -H "Content-Type: application/json" \
  -d '["monte_carlo", "sentiment_analysis"]'

# Disable multiple tools
curl -X POST http://localhost:8000/mcp/tools/bulk/disable \
  -H "Content-Type: application/json" \
  -d '["deep_learning", "reinforcement_learning"]'
```

#### **System Resources**
```bash
# Get system resources
curl http://localhost:8000/mcp/tools/resources

# Get health status
curl http://localhost:8000/mcp/tools/health
```

#### **Auto-Scaling Control**
```bash
# Enable auto-scaling
curl -X POST http://localhost:8000/mcp/tools/auto-scale \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'

# Get auto-scaling status
curl http://localhost:8000/mcp/tools/auto-scale
```

#### **Configuration Management**
```bash
# Update tool configuration
curl -X PUT http://localhost:8000/mcp/tools/monte_carlo/config \
  -H "Content-Type: application/json" \
  -d '{"priority": 9, "max_cpu_percent": 85.0}'
```

## 🔧 **Resource Management Strategies**

### **Resource Levels**

| Level | CPU % | Memory % | Action |
|-------|-------|----------|--------|
| **Low** | < 50% | < 50% | Resume paused tools |
| **Medium** | 50-70% | 50-70% | Normal operation |
| **High** | 70-90% | 70-90% | Pause non-essential tools |
| **Critical** | > 90% | > 90% | Disable low-priority tools |

### **Priority System**

| Priority | Description | Auto-Scaling Behavior |
|----------|-------------|----------------------|
| **9-10** | Critical tools | Never auto-disabled |
| **7-8** | High-priority tools | Disabled only in critical conditions |
| **5-6** | Standard tools | Paused in high resource conditions |
| **3-4** | Low-priority tools | Disabled in high resource conditions |
| **1-2** | Background tools | Disabled in medium+ resource conditions |

### **Auto-Scaling Rules**

```python
# Critical resource level (>90% CPU/Memory)
if resource_level == "critical":
    disable_tools(priority <= 3)  # Disable low-priority tools

# High resource level (>70% CPU/Memory)  
if resource_level == "high":
    pause_tools(priority <= 5)    # Pause non-essential tools

# Low resource level (<30% CPU/Memory)
if resource_level == "low":
    resume_paused_tools()         # Resume paused tools
```

## 📊 **Monitoring & Alerts**

### **Health Metrics**
- **Health Score**: Overall system health (0-100%)
- **Active Tools**: Number of currently active tools
- **Error Tools**: Number of tools in error state
- **Resource Usage**: CPU and memory utilization

### **Monitoring Dashboard**
```bash
# Get comprehensive health status
curl http://localhost:8000/mcp/tools/health

# Response example:
{
  "status": "healthy",
  "health_score": 95.2,
  "total_tools": 10,
  "active_tools": 7,
  "error_tools": 0,
  "system_resources": {
    "cpu_percent": 45.2,
    "memory_percent": 62.8,
    "resource_level": "medium"
  },
  "monitoring_active": true,
  "auto_scaling_enabled": true
}
```

## 🎯 **Use Cases**

### **1. Monte Carlo Simulations**
```bash
# Enable Monte Carlo for intensive simulations
python scripts/mcp_tool_manager.py enable --tool monte_carlo

# Disable other tools to free resources
python scripts/mcp_tool_manager.py disable-multiple --tools deep_learning reinforcement_learning video_processing

# Monitor resource usage
python scripts/mcp_tool_manager.py resources
```

### **2. Deep Learning Training**
```bash
# Enable deep learning tools
python scripts/mcp_tool_manager.py enable --tool deep_learning

# Set high priority for deep learning
python scripts/mcp_tool_manager.py config --tool deep_learning --priority 9

# Disable non-essential tools
python scripts/mcp_tool_manager.py disable-multiple --tools sentiment_analysis business_intelligence
```

### **3. Resource Optimization**
```bash
# Enable auto-scaling for automatic resource management
python scripts/mcp_tool_manager.py auto-scale --enabled true

# Start monitoring
python scripts/mcp_tool_manager.py start-monitoring

# Check health periodically
python scripts/mcp_tool_manager.py health
```

### **4. Development vs Production**
```bash
# Development mode - enable all tools
python scripts/mcp_tool_manager.py enable-multiple --tools monte_carlo sentiment_analysis language_processing business_intelligence audio_processing data_ingestion

# Production mode - enable only essential tools
python scripts/mcp_tool_manager.py disable-multiple --tools deep_learning reinforcement_learning video_processing
python scripts/mcp_tool_manager.py enable-multiple --tools monte_carlo language_processing data_ingestion
```

## 🔍 **Troubleshooting**

### **Common Issues**

#### **1. Tool Won't Start**
```bash
# Check tool status
python scripts/mcp_tool_manager.py list

# Check system resources
python scripts/mcp_tool_manager.py resources

# Check dependencies
# Ensure all required dependencies are installed
```

#### **2. High Resource Usage**
```bash
# Check which tools are consuming resources
python scripts/mcp_tool_manager.py list --show-resources

# Disable resource-intensive tools
python scripts/mcp_tool_manager.py disable --tool deep_learning

# Enable auto-scaling
python scripts/mcp_tool_manager.py auto-scale --enabled true
```

#### **3. Auto-Scaling Not Working**
```bash
# Check auto-scaling status
curl http://localhost:8000/mcp/tools/auto-scale

# Restart monitoring
python scripts/mcp_tool_manager.py stop-monitoring
python scripts/mcp_tool_manager.py start-monitoring
```

### **Logs and Debugging**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Check system logs
tail -f logs/mcp_tool_manager.log

# Monitor resource usage in real-time
watch -n 5 'python scripts/mcp_tool_manager.py resources'
```

## 📈 **Performance Optimization**

### **Best Practices**

1. **Monitor Resource Usage**: Regularly check system resources
2. **Use Auto-Scaling**: Enable automatic resource management
3. **Set Appropriate Priorities**: Configure tool priorities based on importance
4. **Disable Unused Tools**: Turn off tools you don't need
5. **Monitor Health**: Check system health regularly

### **Resource Optimization Tips**

- **Monte Carlo**: High priority (8-9), requires significant CPU
- **Deep Learning**: Very high resource usage, disable when not needed
- **Language Processing**: Moderate resources, good for background tasks
- **Sentiment Analysis**: Lightweight, can run alongside other tools

## 🔐 **Security Considerations**

- Configuration files contain sensitive resource information
- API endpoints should be secured in production
- Monitor tool access and usage patterns
- Implement proper authentication for API access

## 📚 **API Reference**

### **Complete API Documentation**
```bash
# Start the API server
uvicorn src.api.main:app --reload

# Access interactive API docs
# http://localhost:8000/docs
```

### **Response Formats**
All API responses follow a consistent format:
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {...}
}
```

## 🚀 **Future Enhancements**

- **GPU Monitoring**: Enhanced GPU resource tracking
- **Container Support**: Docker/Kubernetes integration
- **Web Dashboard**: Interactive web interface
- **Alert System**: Email/SMS notifications
- **Machine Learning**: Predictive resource management
- **Load Balancing**: Distributed tool management

---

**For more information, see the API documentation at `/docs` when the server is running.**
