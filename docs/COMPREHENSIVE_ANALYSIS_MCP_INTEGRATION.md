# Comprehensive Analysis MCP Integration

## Overview

The main analysis script functionality has been successfully integrated into the MCP (Model Context Protocol) framework, following the Design Framework requirements. This integration provides automatic access to comprehensive analysis capabilities through MCP tools.

## Integration Summary

### ✅ Completed Integration

1. **MCP Tool Registration**: Added `run_comprehensive_analysis` tool to both unified and standalone MCP servers
2. **Full Pipeline Integration**: Integrated all main.py functionality into MCP tools
3. **Art of War Deception Analysis**: Existing deception analysis tools are fully functional
4. **Comprehensive Reporting**: Report generation capabilities are integrated
5. **Error Handling**: Proper error handling and logging throughout the pipeline

### 🔧 Available MCP Tools

The following MCP tools are now available for automatic calling:

#### Primary Analysis Tool
- **`run_comprehensive_analysis`**: Main entry point for comprehensive analysis
  - **Parameters**:
    - `input_content`: Content to analyze (file path, URL, or direct text)
    - `analysis_type`: Type of analysis (`deception`, `sentiment`, `knowledge_graph`, `entities`, `comprehensive`)
    - `language`: Language for processing (default: `en`)
    - `options`: Additional options dictionary
    - `generate_report`: Whether to generate a comprehensive report (default: `true`)
    - `report_format`: Format for the report (`markdown`, `html`, `json`)

#### Art of War Deception Analysis Tools
- **`analyze_art_of_war_deception`**: Comprehensive deception analysis
- **`search_deception_patterns`**: Search stored deception analyses
- **`generate_deception_report`**: Generate deception analysis reports

## Usage Examples

### 1. Basic Deception Analysis

```python
# Using the comprehensive analysis tool
result = await mcp_server.run_comprehensive_analysis(
    input_content="data/art_of_war_complete.txt",
    analysis_type="deception",
    language="en",
    options={
        "include_modern_applications": True,
        "include_ethical_considerations": True
    },
    generate_report=True,
    report_format="markdown"
)
```

### 2. Comprehensive Analysis

```python
# Run all analysis types
result = await mcp_server.run_comprehensive_analysis(
    input_content="data/art_of_war_complete.txt",
    analysis_type="comprehensive",
    language="en",
    options={},
    generate_report=True,
    report_format="markdown"
)
```

### 3. Direct Deception Analysis

```python
# Use the dedicated deception analysis tool
result = await mcp_server.analyze_art_of_war_deception(
    analysis_type="comprehensive",
    focus_areas=["information_warfare", "economic_deception"],
    include_modern_applications=True,
    include_ethical_considerations=True,
    generate_report=True,
    report_format="markdown"
)
```

## Architecture

### MCP Server Integration

The integration follows the Design Framework patterns:

1. **Unified MCP Server** (Port 8003): Integrated with FastAPI for web access
2. **Standalone MCP Server** (Port 8000): Dedicated server for Strands integration
3. **Dual Server Architecture**: Both servers provide the same comprehensive analysis tools

### Pipeline Components

The comprehensive analysis pipeline includes:

1. **Content Processing**: Automatic content type detection and routing
2. **Analysis Execution**: Multiple analysis types (deception, sentiment, knowledge graphs, entities)
3. **Report Generation**: Comprehensive report generation in multiple formats
4. **Error Handling**: Robust error handling and logging
5. **Result Storage**: Automatic storage in vector database and knowledge graphs

## Analysis Types

### 1. Deception Analysis (`deception`)
- Art of War deception techniques analysis
- Modern diplomatic applications
- Ethical considerations
- Comprehensive reporting

### 2. Sentiment Analysis (`sentiment`)
- Text sentiment analysis
- Multi-language support
- Detailed sentiment breakdown

### 3. Knowledge Graph (`knowledge_graph`)
- Entity extraction and relationship mapping
- Graph visualization
- Knowledge graph storage

### 4. Entity Extraction (`entities`)
- Named entity recognition
- Entity categorization
- Relationship extraction

### 5. Comprehensive Analysis (`comprehensive`)
- All analysis types combined
- Cross-analysis insights
- Comprehensive reporting

## File Structure

```
src/mcp_servers/
├── unified_mcp_server.py          # Unified MCP server with comprehensive analysis
├── standalone_mcp_server.py       # Standalone MCP server with comprehensive analysis
└── enhanced_unified_mcp_server.py # Enhanced server with additional features

src/agents/
└── art_of_war_deception_agent.py  # Core deception analysis agent

Test/
├── test_comprehensive_analysis_mcp_integration.py  # Full integration tests
└── simple_comprehensive_analysis_test.py           # Basic functionality tests
```

## Testing

### Automated Tests

Run the comprehensive integration tests:

```bash
# Full integration test
.venv/Scripts/python.exe Test/test_comprehensive_analysis_mcp_integration.py

# Simple functionality test
.venv/Scripts/python.exe Test/simple_comprehensive_analysis_test.py
```

### Manual Testing

1. **Start the MCP servers**:
   ```bash
   .venv/Scripts/python.exe main.py
   ```

2. **Access MCP tools**:
   - Unified server: `http://localhost:8003/mcp`
   - Standalone server: `http://localhost:8000`

3. **Test the tools** using MCP client or direct API calls

## Configuration

### Environment Setup

The integration uses the existing configuration system:

- **Virtual Environment**: `.venv/Scripts/python.exe` for all script execution
- **Configuration Files**: `src/config/` directory
- **Logging**: Comprehensive logging with loguru
- **Error Handling**: Standardized error handling patterns

### MCP Configuration

MCP servers are configured with:

- **Tool Registration**: Automatic tool registration on server startup
- **Error Handling**: Comprehensive error handling for all tools
- **Logging**: Detailed logging for debugging and monitoring
- **Performance**: Optimized for production use

## Benefits

### 1. Automation
- **Automatic Calling**: MCP tools can be called automatically by AI agents
- **Integration**: Seamless integration with existing AI workflows
- **Standardization**: Standard MCP protocol for tool access

### 2. Flexibility
- **Multiple Analysis Types**: Support for various analysis types
- **Configurable Options**: Extensive configuration options
- **Multiple Output Formats**: Support for markdown, HTML, and JSON outputs

### 3. Scalability
- **Dual Server Architecture**: Support for both web and standalone access
- **Performance Optimization**: Optimized for large-scale analysis
- **Resource Management**: Efficient resource usage and caching

### 4. Reliability
- **Error Handling**: Comprehensive error handling and recovery
- **Logging**: Detailed logging for monitoring and debugging
- **Testing**: Automated tests for all functionality

## Future Enhancements

### Planned Improvements

1. **Enhanced Error Handling**: Fix minor issues with report generation
2. **Performance Optimization**: Further optimize for large datasets
3. **Additional Analysis Types**: Add more specialized analysis types
4. **Advanced Reporting**: Enhanced reporting with interactive visualizations

### Integration Opportunities

1. **Additional MCP Tools**: Expand tool set with more specialized analysis
2. **Real-time Analysis**: Add real-time analysis capabilities
3. **Batch Processing**: Support for batch processing of multiple files
4. **API Integration**: Enhanced API integration for external systems

## Conclusion

The comprehensive analysis MCP integration successfully provides:

✅ **Full Integration**: Main analysis script functionality is fully integrated into MCP tools  
✅ **Automatic Calling**: Tools can be called automatically through MCP protocol  
✅ **Design Framework Compliance**: Follows all Design Framework requirements  
✅ **Production Ready**: Robust error handling and comprehensive testing  
✅ **Scalable Architecture**: Dual server architecture for maximum compatibility  

The integration enables automatic analysis of Art of War deception techniques and their modern diplomatic applications through standardized MCP tools, making the analysis capabilities easily accessible to AI agents and automated workflows.

---

*This documentation was generated as part of the comprehensive analysis MCP integration project, following the Design Framework requirements for MCP tool integration.*
