# File Generation System

## Overview

The DIA3 system now includes a centralized file generation system that automatically prepends `file:///D:/AI/DIA3/` to all generated files. This ensures consistent file URLs across the entire system and provides standardized file management capabilities.

## Key Features

- **Automatic Protocol Prefix**: All generated files automatically get the `file:///D:/AI/DIA3/` prefix
- **Centralized Management**: Single point of control for all file generation operations
- **Metadata Tracking**: Comprehensive metadata for all generated files
- **Directory Management**: Automatic directory creation and organization
- **Multiple Formats**: Support for JSON, text, binary, reports, and visualizations
- **Backward Compatibility**: Existing code can be easily migrated

## Architecture

### Core Components

1. **FilePathUtils** (`src/core/utils/file_path_utils.py`)
   - Handles path manipulation and protocol prefix prepending
   - Provides utility functions for common directory operations
   - Ensures consistent file URL generation

2. **FileGenerator** (`src/core/utils/file_generator.py`)
   - Centralized file generation with automatic protocol prefix
   - Supports multiple file types and formats
   - Tracks all generated files with metadata

3. **Integration Points**
   - Report Manager: Updated to use new file generation system
   - Export Manager: Enhanced with protocol prefix support
   - Report Generator: Modified to return file URLs

## Usage Examples

### Basic File Generation

```python
from src.core.utils.file_generator import save_json, save_text

# Save JSON data
data = {"analysis": "results", "timestamp": "2025-01-17"}
result = save_json(data, "analysis_results.json", "Results/analysis")
print(f"File URL: {result['file_info']['file_url']}")
# Output: file:///D:/AI/DIA3/Results/analysis/analysis_results.json

# Save text content
content = "# Analysis Report\n\nThis is a report."
result = save_text(content, "report.md", "Results/reports")
print(f"File URL: {result['file_info']['file_url']}")
# Output: file:///D:/AI/DIA3/Results/reports/report.md
```

### Advanced File Generation

```python
from src.core.utils.file_generator import file_generator

# Save binary data
binary_data = b"binary content"
result = file_generator.save_binary(binary_data, "data.bin", "cache")

# Save report with metadata
report_content = "# Report\n\nContent here."
result = file_generator.save_report(
    content=report_content,
    filename="analysis_report.md",
    report_type="intelligence_analysis",
    metadata={"analyst": "AI", "confidence": 0.95}
)

# Save visualization
html_content = "<html><body><h1>Chart</h1></body></html>"
result = file_generator.save_visualization(
    html_content=html_content,
    title="Analysis Chart",
    visualization_type="interactive",
    metadata={"chart_type": "bar", "data_points": 100}
)
```

### File Path Utilities

```python
from src.core.utils.file_path_utils import FilePathUtils

# Prepend protocol to any path
path = "Results/analysis/data.json"
url = FilePathUtils.prepend_file_protocol(path)
# Output: file:///D:/AI/DIA3/Results/analysis/data.json

# Get directory-specific paths
results_url = FilePathUtils.get_results_path("analysis.json")
reports_url = FilePathUtils.get_reports_path("report.md")
docs_url = FilePathUtils.get_docs_path("document.pdf")
white_papers_url = FilePathUtils.get_white_papers_path("paper.docx")

# Check if path is within workspace
is_within = FilePathUtils.is_within_workspace("/some/external/path")
# Output: False

# Get relative path
relative = FilePathUtils.get_relative_path("D:/AI/DIA3/Results/data.json")
# Output: Results/data.json
```

## File Information Structure

All file generation operations return a standardized response structure:

```python
{
    "success": True,
    "file_info": {
        "filename": "analysis_results.json",
        "path": "D:/AI/DIA3/Results/analysis_results.json",
        "file_url": "file:///D:/AI/DIA3/Results/analysis_results.json",
        "relative_path": "Results/analysis_results.json",
        "file_type": "json",
        "size_bytes": 1024,
        "size_kb": 1.0,
        "created_at": "2025-01-17T10:00:00",
        "modified_at": "2025-01-17T10:00:00",
        # Additional metadata based on file type
        "report_type": "analysis",  # For reports
        "visualization_type": "interactive",  # For visualizations
        "metadata": {}  # Custom metadata
    },
    "message": "File saved successfully"
}
```

## Directory Structure

The system organizes files into logical directories:

```
D:/AI/DIA3/
├── Results/
│   ├── reports/          # Analysis reports
│   ├── visualizations/   # Charts and graphs
│   └── exports/          # Data exports
├── docs/
│   ├── white_papers/     # White papers
│   └── generated_pdfs/   # Generated PDFs
├── cache/                # Temporary files
├── temp/                 # Temporary files
└── logs/                 # Log files
```

## Migration Guide

### For Existing Code

1. **Replace direct file operations**:
   ```python
   # Old way
   with open("Results/data.json", 'w') as f:
       json.dump(data, f)
   
   # New way
   from src.core.utils.file_generator import save_json
   result = save_json(data, "data.json", "Results")
   ```

2. **Update path references**:
   ```python
   # Old way
   file_path = "Results/report.md"
   
   # New way
   from src.core.utils.file_path_utils import FilePathUtils
   file_url = FilePathUtils.get_reports_path("report.md")
   ```

3. **Use file URLs in responses**:
   ```python
   # Old way
   return {"file_path": "Results/data.json"}
   
   # New way
   return {"file_url": "file:///D:/AI/DIA3/Results/data.json"}
   ```

### For New Code

1. **Import utilities**:
   ```python
   from src.core.utils.file_generator import file_generator
   from src.core.utils.file_path_utils import FilePathUtils
   ```

2. **Use centralized generation**:
   ```python
   # Always use the file generator for new files
   result = file_generator.save_json(data, filename, directory)
   ```

3. **Return file URLs**:
   ```python
   # Always return file URLs in API responses
   return {"file_url": result["file_info"]["file_url"]}
   ```

## API Integration

### REST API Endpoints

All API endpoints that generate files now return file URLs:

```python
# Example API response
{
    "success": True,
    "data": {...},
    "files": [
        {
            "filename": "analysis_report.pdf",
            "file_url": "file:///D:/AI/DIA3/Results/reports/analysis_report.pdf",
            "size_kb": 245.6
        }
    ]
}
```

### MCP Server Integration

MCP server responses include file URLs:

```python
# MCP tool response
{
    "success": True,
    "result": {
        "analysis": {...},
        "generated_files": [
            "file:///D:/AI/DIA3/Results/reports/report_20250117_100000.md"
        ]
    }
}
```

## Benefits

1. **Consistency**: All files have standardized URLs
2. **Accessibility**: Easy file access and sharing
3. **Tracking**: Comprehensive metadata for all files
4. **Organization**: Logical directory structure
5. **Scalability**: Centralized management for large file volumes
6. **Integration**: Seamless integration with existing systems

## Testing

Run the demo to test the file generation system:

```bash
python examples/file_generation_demo.py
```

This will generate sample files and demonstrate all capabilities.

## Configuration

The system uses the following configuration:

- **Workspace Base**: `D:/AI/DIA3`
- **Protocol Prefix**: `file:///D:/AI/DIA3/`
- **Default Directory**: `Results`
- **Encoding**: UTF-8 (configurable)

## Future Enhancements

1. **Cloud Storage Integration**: Support for cloud file storage
2. **File Versioning**: Automatic version control for files
3. **Compression**: Automatic file compression for large files
4. **Encryption**: Optional file encryption
5. **Backup**: Automatic backup to secondary storage

## Support

For questions or issues with the file generation system:

1. Check the demo script for usage examples
2. Review the utility function documentation
3. Examine the integration points in existing code
4. Test with the provided demo script

## Status

✅ **IMPLEMENTED**: Core file generation system
✅ **IMPLEMENTED**: Protocol prefix prepending
✅ **IMPLEMENTED**: Metadata tracking
✅ **IMPLEMENTED**: Directory management
✅ **IMPLEMENTED**: Integration with existing systems
✅ **IMPLEMENTED**: Demo and documentation

The file generation system is now fully operational and ready for use across the entire DIA3 codebase.
