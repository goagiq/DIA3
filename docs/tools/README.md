# DIA3 MCP Tools Documentation

## Overview

This directory contains comprehensive documentation for all MCP (Model Context Protocol) tools available in the DIA3 system. Each tool is documented using a standardized template that includes detailed information about functionality, usage, and implementation.

## Tool Categories

### 1. Agent Management Tools
**File**: `01_agent_management_tools.md`

Tools for managing and monitoring the system's agent infrastructure:

- **get_all_agents_status** - Agent Status Monitor
- **start_all_agents** - Agent Swarm Starter  
- **stop_all_agents** - Agent Swarm Stopper

### 2. Content Processing Tools
**File**: `02_content_processing_tools.md`

Tools for processing and analyzing various types of content:

- **process_pdf_enhanced_multilingual** - Enhanced Multilingual PDF Processor
- **analyze_text_sentiment** - Text Sentiment Analyzer
- **extract_entities** - Entity Extraction Engine

### 3. Unified Content Processing Tools
**File**: `03_unified_content_processing_tools.md`

Advanced tools for unified content processing and management:

- **process_content** - Enhanced Unified Content Processor
- **verify_ingestion** - Content Ingestion Verifier
- **extract_text_from_content** - Multi-Format Text Extractor

### 4. Advanced Analytics Tools
**File**: `04_advanced_analytics_tools.md`

Sophisticated analytics and forecasting capabilities:

- **advanced_forecasting** - Advanced Multivariate Forecasting Engine
- **causal_analysis** - Causal Inference Analysis Engine
- **convert_content_format** - Content Format Converter

### 5. Report Generation & System Management Tools
**File**: `05_report_generation_tools.md`

Tools for generating reports and managing system operations:

- **generate_graph_report** - Knowledge Graph Report Generator
- **comprehensive_threat_assessment** - Comprehensive Threat Assessment Engine
- **system_health_check** - System Health and Status Monitor
- **configuration_management** - System Configuration Manager

## Tool Documentation Template

Each tool is documented using the following standardized format:

### General Info
- **Name**: Tool identifier
- **Title**: Human-readable title
- **Version**: Tool version
- **Author**: Development team
- **Description**: Comprehensive description of functionality

### Required Libraries
- Core Python libraries
- Specialized dependencies
- MCP and Strands integration requirements
- Additional dependencies

### Imports and Decorators
- Required import statements
- MCP tool decorator usage
- Function signature

### Intended Use
- Primary use cases
- Target scenarios
- Application domains

### Out-of-Scope / Limitations
- What the tool cannot do
- Performance limitations
- Input/output constraints
- Platform restrictions

### Input Schema
- JSON schema for input parameters
- Required vs optional fields
- Data types and constraints
- Default values

### Output Schema
- JSON schema for output structure
- Response format
- Error handling
- Success indicators

### Example
- Sample input with realistic data
- Expected output format
- Usage scenarios

### Safety & Reliability
- Error handling mechanisms
- Data validation
- Security considerations
- Performance characteristics

## Quick Reference

### Tool Count by Category
- **Agent Management**: 3 tools
- **Content Processing**: 3 tools
- **Unified Content Processing**: 3 tools
- **Advanced Analytics**: 3 tools
- **Report Generation & System Management**: 4 tools

**Total**: 16 documented MCP tools

### Common Patterns

#### Input Validation
All tools include comprehensive input validation:
```python
# Example validation pattern
if not content:
    return {"success": False, "error": "Content is required"}
```

#### Error Handling
Standardized error response format:
```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

#### Success Response
Standardized success response format:
```json
{
  "success": true,
  "result": {
    // Tool-specific result data
  },
  "processing_time": 1.23
}
```

## Usage Guidelines

### 1. Tool Selection
- Choose tools based on specific use case requirements
- Consider input/output format compatibility
- Evaluate performance requirements

### 2. Error Handling
- Always check the `success` field in responses
- Handle errors gracefully with appropriate fallbacks
- Log errors for debugging and monitoring

### 3. Performance Considerations
- Monitor `processing_time` for performance optimization
- Use appropriate input sizes for optimal performance
- Consider batch processing for large datasets

### 4. Security
- Validate all inputs before processing
- Handle sensitive data appropriately
- Follow security best practices for data handling

## Integration Examples

### Basic Tool Usage
```python
# Example: Using sentiment analysis tool
result = await analyze_text_sentiment(
    text="This is a sample text for analysis",
    language="en"
)

if result["success"]:
    sentiment = result["result"]["sentiment"]
    confidence = result["result"]["confidence"]
    print(f"Sentiment: {sentiment} (confidence: {confidence})")
else:
    print(f"Error: {result['error']}")
```

### Chaining Tools
```python
# Example: Processing PDF and extracting entities
pdf_result = await process_pdf_enhanced_multilingual(
    pdf_path="/path/to/document.pdf",
    language="en"
)

if pdf_result["success"]:
    extracted_text = pdf_result["result"]["extracted_text"]
    
    entity_result = await extract_entities(
        text=extracted_text,
        language="en"
    )
    
    if entity_result["success"]:
        entities = entity_result["result"]["entities"]
        print(f"Found {len(entities)} entities")
```

## Development Guidelines

### Adding New Tools
1. Follow the established documentation template
2. Include comprehensive input/output schemas
3. Provide realistic examples
4. Document limitations and constraints
5. Include safety and reliability information

### Tool Testing
- Test with various input types and sizes
- Validate error handling scenarios
- Performance testing with realistic workloads
- Integration testing with other tools

### Documentation Updates
- Keep documentation current with tool changes
- Update examples for new features
- Maintain consistency across all tool documentation
- Regular review and validation of accuracy

## Support and Maintenance

### Getting Help
- Check tool documentation for usage examples
- Review error messages for troubleshooting
- Consult system logs for detailed error information
- Contact development team for complex issues

### Reporting Issues
- Include tool name and version
- Provide input data and expected output
- Include error messages and stack traces
- Describe environment and configuration

### Contributing
- Follow established coding standards
- Include comprehensive tests
- Update documentation for new features
- Maintain backward compatibility

## Version History

### v1.0.0 (Current)
- Initial comprehensive documentation
- 16 documented MCP tools
- Standardized documentation template
- Complete examples and usage guidelines

### Future Enhancements
- Interactive tool documentation
- Performance benchmarks
- Integration tutorials
- Advanced usage patterns
- Tool comparison matrix

---

**Last Updated**: January 2024  
**Documentation Version**: 1.0.0  
**Total Tools Documented**: 16
