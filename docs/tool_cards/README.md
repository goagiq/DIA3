# DIA3 MCP Tools and API Endpoints Documentation

## 📚 Complete Documentation Suite

This directory contains comprehensive documentation for all MCP tools and API endpoints in the DIA3 system. Each tool and endpoint is documented with detailed specifications, examples, and runbooks.

## 📋 Documentation Structure

```
docs/tool_cards/
├── README.md                           # This file - Overview and navigation
├── 00_index.md                         # Complete index of all tools and endpoints
├── 01_process_content.md               # Enhanced content processing tool
├── 02_analyze_sentiment.md             # Sentiment analysis tool
├── 03_generate_enhanced_report.md      # Enhanced report generation tool
├── 04_monte_carlo_simulation.md        # Monte Carlo simulation tools
└── 05_api_endpoints.md                 # REST API endpoints documentation
```

## 🚀 Quick Start

### 1. System Overview
- **MCP Server**: `http://localhost:8000/mcp` (streamable HTTP protocol)
- **REST API**: `http://localhost:8000` (FastAPI framework)
- **Documentation**: `http://localhost:8000/docs` (interactive API docs)

### 2. Installation
```bash
# Install dependencies
pip install -r requirements-phase5.txt

# Start the server
python main.py
```

### 3. Basic Usage

#### MCP Tools
```python
from mcp.client.streamable_http import streamablehttp_client

async def use_mcp():
    client = streamablehttp_client("http://localhost:8000/mcp")
    async with client:
        # List available tools
        tools = await client.list_tools()
        
        # Use process_content tool
        result = await client.call_tool(
            "process_content",
            {"content": "Sample text", "content_type": "text"}
        )
```

#### REST API
```bash
# Analyze text content
curl -X POST "http://localhost:8000/analyze/text" \
  -H "Content-Type: application/json" \
  -d '{"content": "Sample text", "content_type": "text"}'

# Generate enhanced report
curl -X POST "http://localhost:8000/export/markdown-to-pdf" \
  -H "Content-Type: application/json" \
  -d '{"content": "# Report", "format": "pdf"}'
```

## 🔧 Available Tools and Endpoints

### MCP Tools (55+ Available)

#### Core Processing Tools
- **process_content** - Enhanced unified content processing
- **analyze_sentiment** - Multilingual sentiment analysis
- **generate_enhanced_report** - Interactive report generation
- **extract_entities** - Entity extraction and mapping
- **knowledge_graph** - Knowledge graph management

#### Analysis and Intelligence Tools
- **business_intelligence** - Business analytics
- **classical_chinese_humint** - HUMINT analysis
- **comprehensive_threat_assessment** - Threat assessment
- **art_of_war_deception** - Deception analysis
- **strategic_assessment** - Strategic analysis

#### Simulation and Modeling Tools
- **run_monte_carlo_simulation** - Risk assessment
- **run_custom_monte_carlo_simulation** - Custom modeling
- **run_time_series_monte_carlo_simulation** - Time series analysis
- **model_optimization** - ML model optimization
- **deep_learning_training** - Neural network training

#### Search and Discovery Tools
- **semantic_search** - Content discovery
- **multi_language_search** - Multilingual search
- **conceptual_search** - Concept-based search
- **combined_search** - Integrated search
- **query_knowledge_graph** - Knowledge queries

#### System Management Tools
- **get_all_agents_status** - Agent monitoring
- **start_agent_swarm** - Agent orchestration
- **system_health** - System monitoring
- **performance_monitoring** - Performance tracking
- **configuration_management** - System configuration

### REST API Endpoints (21 Available)

#### Content Analysis
- `POST /analyze/text` - Text analysis
- `POST /analyze/image` - Image analysis
- `POST /analyze/audio` - Audio analysis
- `POST /analyze/video` - Video analysis
- `POST /analyze/webpage` - Web content analysis
- `POST /analyze/pdf` - Document analysis

#### Business Intelligence
- `POST /business/dashboard` - Business dashboards
- `POST /business/executive-summary` - Executive reports
- `POST /business/visualizations` - Data visualizations
- `POST /business/intelligence-report` - Intelligence reports

#### Export and Documents
- `POST /export/markdown-to-pdf` - PDF generation
- `POST /export/markdown-to-word` - Word document generation
- `POST /export/markdown-to-both` - Multi-format export
- `GET /export/status/{operation_id}` - Export monitoring

#### Search and Analytics
- `POST /semantic/search` - Semantic search
- `POST /search/knowledge-graph` - Knowledge graph queries
- `POST /search/combined` - Combined search
- `POST /analytics/predictive` - Predictive analytics

#### System Management
- `GET /health` - Health checks
- `GET /models` - Model management
- `GET /agents/status` - Agent status

## 📖 Documentation Details

Each tool card includes:

### Standard Sections
- **General Info** - Name, version, author, description
- **Required Libraries** - All dependencies with versions
- **Imports and Decorators** - Code setup examples
- **Intended Use** - Purpose and use cases
- **Out-of-Scope/Limitations** - Constraints and limitations
- **Input Schema** - JSON schema for inputs
- **Output Schema** - JSON schema for outputs
- **Example** - Complete input/output examples
- **Safety & Reliability** - Security and error handling
- **Runbook** - Setup, usage, error handling, monitoring

### Advanced Features
- **Dependency Management** - Complete library requirements
- **Error Handling** - Comprehensive error scenarios
- **Monitoring** - Performance and health tracking
- **Security** - Input validation and safety measures
- **Examples** - Real-world usage scenarios

## 🛠️ Development and Customization

### Adding New Tools
1. Create tool function in `src/mcp_servers/unified_mcp_server.py`
2. Add `@self.mcp.tool()` decorator with description
3. Create documentation file following the template
4. Update the index in `00_index.md`

### Adding New API Endpoints
1. Add endpoint in appropriate route file
2. Define request/response models
3. Create documentation following API template
4. Update the index

### Template Usage
Use the existing tool cards as templates for new documentation:
- Copy an existing `.md` file
- Replace content with your tool's specifications
- Follow the established format and structure
- Include all required sections

## 🔍 Finding Information

### By Tool Type
- **Content Processing**: See `01_process_content.md`
- **Analysis**: See `02_analyze_sentiment.md`
- **Reports**: See `03_generate_enhanced_report.md`
- **Simulation**: See `04_monte_carlo_simulation.md`
- **APIs**: See `05_api_endpoints.md`

### By Functionality
- **Text Analysis**: `analyze_sentiment`, `process_content`
- **Report Generation**: `generate_enhanced_report`, export endpoints
- **Risk Assessment**: Monte Carlo simulation tools
- **Search**: Semantic search tools and endpoints
- **System Management**: Health and monitoring tools

### By Domain
- **Business Intelligence**: Business analysis tools and endpoints
- **Cybersecurity**: Threat assessment and security tools
- **Military/Defense**: HUMINT and strategic analysis tools
- **Data Science**: ML and statistical analysis tools

## 📊 System Capabilities

### Content Processing
- **Multimodal Analysis**: Text, images, audio, video, documents
- **Multilingual Support**: 7+ languages with auto-detection
- **Bulk Processing**: Handle large volumes of content
- **Quality Assessment**: Content validation and scoring

### Intelligence and Analysis
- **Sentiment Analysis**: Advanced emotion detection
- **Entity Extraction**: Named entity recognition and mapping
- **Knowledge Graphs**: Relationship mapping and queries
- **Threat Assessment**: Comprehensive security analysis
- **Strategic Analysis**: Art of War principles integration

### Reporting and Visualization
- **Interactive Reports**: HTML with advanced visualizations
- **Multiple Formats**: PDF, Word, HTML export
- **22 Analysis Modules**: Comprehensive coverage
- **Custom Styling**: Professional templates and themes
- **Source Tracking**: Tooltips and reference management

### Simulation and Modeling
- **Monte Carlo**: Risk assessment and scenario analysis
- **Time Series**: Forecasting and trend analysis
- **Machine Learning**: Model training and optimization
- **Predictive Analytics**: Future trend prediction

## 🔧 Technical Specifications

### System Requirements
- **Python**: 3.8+
- **Memory**: 8GB+ recommended
- **Storage**: 10GB+ for models and data
- **Network**: Internet access for external APIs

### Performance Characteristics
- **Response Time**: 1-30 seconds depending on complexity
- **Throughput**: 100+ requests/minute
- **Concurrency**: Async processing support
- **Scalability**: Horizontal scaling capabilities

### Security Features
- **Input Validation**: Comprehensive sanitization
- **Rate Limiting**: Request throttling
- **Error Handling**: Graceful failure management
- **Audit Logging**: Complete operation tracking
- **Content Filtering**: Inappropriate content detection

## 📞 Support and Resources

### Documentation
- **Interactive API Docs**: `http://localhost:8000/docs`
- **OpenAPI Spec**: `http://localhost:8000/openapi.json`
- **ReDoc**: `http://localhost:8000/redoc`

### Monitoring
- **Health Checks**: `http://localhost:8000/health`
- **MCP Status**: `http://localhost:8000/mcp-health`
- **Agent Status**: `http://localhost:8000/agents/status`

### Troubleshooting
- **Logs**: Check `logs/` directory
- **Debug Mode**: Set `LOG_LEVEL=DEBUG`
- **Common Issues**: See troubleshooting section in `00_index.md`

## 🤝 Contributing

### Documentation Standards
- Follow the established template format
- Include all required sections
- Provide complete examples
- Update the index when adding new tools
- Test all code examples

### Code Standards
- Follow PEP 8 style guidelines
- Include proper error handling
- Add comprehensive logging
- Implement input validation
- Provide clear documentation strings

---

## 📝 Quick Reference

### Essential Commands
```bash
# Start server
python main.py

# Check health
curl http://localhost:8000/health

# List MCP tools
python -c "
import asyncio
from mcp.client.streamable_http import streamablehttp_client

async def list_tools():
    client = streamablehttp_client('http://localhost:8000/mcp')
    async with client:
        tools = await client.list_tools()
        for tool in tools:
            print(f'{tool.name}: {tool.description}')

asyncio.run(list_tools())
"
```

### Key Files
- **Main Server**: `main.py`
- **MCP Server**: `src/mcp_servers/unified_mcp_server.py`
- **API Routes**: `src/api/main.py`
- **Configuration**: `config/config.py`
- **Requirements**: `requirements-phase5.txt`

---

*This documentation is maintained by the DIA3 Development Team. For questions, issues, or contributions, please refer to the project repository.*
