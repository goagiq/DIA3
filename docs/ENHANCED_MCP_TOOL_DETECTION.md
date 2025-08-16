# Enhanced MCP Tool Detection

## Overview

The `process_content` tool has been enhanced with intelligent detection capabilities to better identify when users want to process content using MCP tools. This enhancement improves the user experience by automatically detecting various request patterns and routing them appropriately.

## Enhanced Detection Patterns

### Core Request Phrases

The system now detects the following key phrases that indicate MCP tool usage:

- **"add the following"** - Indicates content should be added to databases
- **"process these"** - Indicates content should be processed
- **"include the following"** - Indicates content should be included in processing

### URL Processing Patterns

Enhanced detection for URL-based requests:

- `@https://example.com` - Direct URL references
- `process @url` - Explicit processing requests
- `add @url` - Addition requests
- `include @url` - Inclusion requests

### Database Storage Patterns

Detection for database storage requests:

- `to vector db` - Vector database storage
- `to knowledge graph` - Knowledge graph storage
- `to both databases` - Dual storage
- `store in vector` - Vector storage
- `store in knowledge graph` - Knowledge graph storage
- `store in both` - Dual storage

### MCP Tool Specific Patterns

Recognition of MCP-related terminology:

- `mcp tool` - MCP tool usage
- `mcp server` - MCP server operations
- `process content` - Content processing
- `unified processing` - Unified processing requests
- `content processing` - General content processing

### Library and Content Source Patterns

Detection for specific content sources:

- `openlibrary` - Open Library content
- `ctext.org` - Chinese Text Project content
- `library content` - Library content
- `book content` - Book content
- `document processing` - Document processing

### Batch Processing Patterns

Recognition of batch operations:

- `batch process` - Batch processing
- `bulk import` - Bulk import operations
- `multiple urls` - Multiple URL processing
- `several urls` - Several URL processing
- `list of urls` - URL list processing

### Content Analysis Patterns

Detection for analysis requests:

- `analyze content` - Content analysis
- `extract entities` - Entity extraction
- `generate knowledge graph` - Knowledge graph generation
- `create vector embeddings` - Vector embedding creation
- `semantic analysis` - Semantic analysis

### Multi-step Processing Patterns

Recognition of multi-step operations:

- `process and store` - Process then store
- `analyze and save` - Analyze then save
- `extract and store` - Extract then store
- `process then store` - Sequential processing
- `analyze then save` - Sequential analysis

## Detection Logic

The enhanced detection uses a multi-layered approach:

1. **URL Pattern Detection**: Checks for `@https://` patterns first
2. **Bulk Pattern Matching**: Matches against comprehensive regex patterns
3. **Keyword Context Analysis**: Analyzes processing-related keywords
4. **Combined Decision Logic**: Returns true if URLs + keywords OR bulk patterns match

## Implementation Details

### Files Updated

- `src/mcp_servers/unified_mcp_server.py`
- `src/mcp_servers/enhanced_unified_mcp_server.py`
- `src/agents/enhanced_process_content_agent.py`

### Key Methods

- `_detect_bulk_import_request()` - Main detection method
- `_extract_urls_from_request()` - URL extraction
- `_process_bulk_import_request()` - Bulk processing handler

## Usage Examples

### Basic URL Processing
```
process @https://example.com
add @https://example.com to vector db
include @https://example.com in knowledge graph
```

### Multiple URL Processing
```
add @https://url1.com and @https://url2.com to both vector and knowledge graph db
process these URLs: @https://url1.com @https://url2.com
add the following URLs to both databases: @https://url1.com @https://url2.com
```

### Content Source Processing
```
process these Open Library books: @https://openlibrary.org/book1 @https://openlibrary.org/book2
add the following ctext.org content to vector db: @https://ctext.org/art-of-war
include these library resources in knowledge graph: @https://example.com/book1 @https://example.com/book2
```

### Analysis Requests
```
analyze and store @https://example.com in both databases
extract entities from @https://example.com and save to vector db
generate knowledge graph for @https://example.com and store results
```

## Benefits

1. **Improved User Experience**: Automatic detection reduces manual configuration
2. **Flexible Input**: Supports various natural language patterns
3. **Comprehensive Coverage**: Handles multiple content types and sources
4. **Intelligent Routing**: Automatically routes to appropriate processing agents
5. **Batch Processing**: Efficiently handles multiple URLs and content sources

## Future Enhancements

- Machine learning-based pattern recognition
- User preference learning
- Custom pattern definition
- Advanced context analysis
- Multi-language support for detection patterns

## Testing

The enhanced detection can be tested with various input patterns:

```python
# Test detection patterns
test_inputs = [
    "add the following URLs to vector db: @https://example.com",
    "process these documents: @https://doc1.com @https://doc2.com",
    "include the following content in knowledge graph: @https://content.com",
    "analyze and store @https://example.com in both databases",
    "extract entities from @https://example.com and save to vector db"
]

for test_input in test_inputs:
    result = detect_bulk_import_request(test_input)
    print(f"Input: {test_input}")
    print(f"Detected: {result}\n")
```

This enhancement significantly improves the system's ability to understand and process user requests for content processing using MCP tools.
