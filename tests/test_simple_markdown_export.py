#!/usr/bin/env python3
"""
Test script for Simple Markdown Export

Tests the simplified markdown export functionality that doesn't require WeasyPrint.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_simple_markdown_export():
    """Test the simple markdown export functionality."""
    print("🧪 Testing Simple Markdown Export...")
    
    try:
        from src.core.export.simple_markdown_export_service import SimpleMarkdownExportService
        
        # Initialize service
        output_dir = "temp_output/test_exports"
        export_service = SimpleMarkdownExportService(output_dir)
        
        # Test markdown content
        test_markdown = """
# Test Document

This is a **test document** with *markdown formatting*.

## Features
- **Bold text**
- *Italic text*
- `Inline code`
- ~~Strikethrough~~

## Table Example
| Feature | Description |
|---------|-------------|
| **PDF Export** | Export to PDF format |
| **Word Export** | Export to Word format |
| **Images** | Support for embedded images |
| **Tables** | Support for markdown tables |

## Code Block
```python
def hello_world():
    print("Hello, World!")
```

> This is a blockquote example.

---
*End of test document*
"""
        
        print("📄 Testing PDF export...")
        pdf_result = await export_service.export_markdown_to_pdf(
            test_markdown,
            output_filename="test_export.pdf"
        )
        
        if pdf_result["success"]:
            print(f"✅ PDF export successful: {pdf_result['output_path']}")
            print(f"📊 File size: {pdf_result['file_size']} bytes")
        else:
            print(f"❌ PDF export failed: {pdf_result['error']}")
            return False
        
        print("\n📄 Testing Word export...")
        word_result = await export_service.export_markdown_to_word(
            test_markdown,
            output_filename="test_export.docx"
        )
        
        if word_result["success"]:
            print(f"✅ Word export successful: {word_result['output_path']}")
            print(f"📊 File size: {word_result['file_size']} bytes")
        else:
            print(f"❌ Word export failed: {word_result['error']}")
            return False
        
        print("\n📄 Testing dual export...")
        both_result = await export_service.export_markdown_to_both(
            test_markdown,
            output_filename="test_export_both"
        )
        
        if both_result["success"]:
            print(f"✅ Dual export successful")
            print(f"📊 PDF: {both_result['pdf_result']['output_path']}")
            print(f"📊 Word: {both_result['word_result']['output_path']}")
        else:
            print(f"❌ Dual export failed: {both_result['error']}")
            return False
        
        print("\n🎉 All tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

async def test_mcp_tools():
    """Test the MCP tools."""
    print("\n🧪 Testing MCP Tools...")
    
    try:
        from src.mcp_servers.simple_markdown_export_mcp_tools import SimpleMarkdownExportMCPTools
        
        mcp_tools = SimpleMarkdownExportMCPTools()
        tools = mcp_tools.get_tools()
        
        print(f"✅ MCP tools initialized successfully")
        print(f"📋 Available tools: {len(tools)}")
        
        for tool in tools:
            tool_name = tool["function"]["name"]
            print(f"  - {tool_name}")
        
        # Test a simple export
        test_markdown = "# Test\n\nThis is a test document."
        
        print("\n📄 Testing MCP PDF export...")
        pdf_result = await mcp_tools.simple_markdown_export_to_pdf(test_markdown, "mcp_test")
        
        if pdf_result["success"]:
            print(f"✅ MCP PDF export successful: {pdf_result['file_path']}")
        else:
            print(f"❌ MCP PDF export failed: {pdf_result['error']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        return False

async def test_api_routes():
    """Test the API routes."""
    print("\n🧪 Testing API Routes...")
    
    try:
        from src.api.simple_markdown_export_routes import router
        
        print(f"✅ API routes initialized successfully")
        print(f"📋 Router prefix: {router.prefix}")
        
        # Check available endpoints
        routes = []
        for route in router.routes:
            if hasattr(route, 'path'):
                routes.append(f"{route.methods} {route.path}")
        
        print(f"📋 Available endpoints:")
        for route in routes:
            print(f"  - {route}")
        
        return True
        
    except Exception as e:
        print(f"❌ API routes test failed: {e}")
        return False

async def main():
    """Run all tests."""
    print("🚀 Simple Markdown Export Test Suite")
    print("=" * 50)
    
    # Test simple export service
    export_ok = await test_simple_markdown_export()
    
    if not export_ok:
        print("\n❌ Export service test failed.")
        return False
    
    # Test MCP tools
    mcp_ok = await test_mcp_tools()
    
    # Test API routes
    api_ok = await test_api_routes()
    
    print("\n" + "=" * 50)
    print("📊 Final Test Results:")
    print(f"✅ Export Service: {'PASS' if export_ok else 'FAIL'}")
    print(f"✅ MCP Tools: {'PASS' if mcp_ok else 'FAIL'}")
    print(f"✅ API Routes: {'PASS' if api_ok else 'FAIL'}")
    
    if all([export_ok, mcp_ok, api_ok]):
        print("\n🎉 All tests passed! Simple markdown export functionality is working.")
        return True
    else:
        print("\n❌ Some tests failed. Please check the issues.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
