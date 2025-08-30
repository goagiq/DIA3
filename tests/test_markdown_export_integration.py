#!/usr/bin/env python3
"""
Test script for Markdown Export Integration

Tests the markdown export functionality through both API endpoints and MCP tools.
"""

import asyncio
import sys
import os
from pathlib import Path
import requests
import json
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_markdown_export_api():
    """Test markdown export API endpoints."""
    print("🧪 Testing Markdown Export API Endpoints...")
    
    base_url = "http://localhost:8000"
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/api/v1/markdown-export/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test markdown export
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
    
    try:
        # Test PDF export
        pdf_data = {
            "markdown_content": test_markdown,
            "output_format": "pdf",
            "filename": f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
        
        response = requests.post(
            f"{base_url}/api/v1/markdown-export/export",
            json=pdf_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ PDF export successful: {result}")
            
            # Test file download
            if result.get("file_path"):
                filename = Path(result["file_path"]).name
                download_response = requests.get(f"{base_url}/api/v1/markdown-export/download/{filename}")
                if download_response.status_code == 200:
                    print(f"✅ File download successful: {len(download_response.content)} bytes")
                else:
                    print(f"❌ File download failed: {download_response.status_code}")
        else:
            print(f"❌ PDF export failed: {response.status_code} - {response.text}")
            return False
        
        # Test Word export
        word_data = {
            "markdown_content": test_markdown,
            "output_format": "word",
            "filename": f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
        
        response = requests.post(
            f"{base_url}/api/v1/markdown-export/export",
            json=word_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Word export successful: {result}")
        else:
            print(f"❌ Word export failed: {response.status_code} - {response.text}")
            return False
        
        # Test file listing
        response = requests.get(f"{base_url}/api/v1/markdown-export/files")
        if response.status_code == 200:
            files_data = response.json()
            print(f"✅ File listing successful: {files_data}")
        else:
            print(f"❌ File listing failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

async def test_markdown_export_mcp():
    """Test markdown export MCP tools."""
    print("🧪 Testing Markdown Export MCP Tools...")
    
    try:
        from src.mcp_servers.markdown_export_mcp_tools import MarkdownExportMCPTools, MARKDOWN_EXPORT_AVAILABLE
        
        if not MARKDOWN_EXPORT_AVAILABLE:
            print("❌ Markdown export MCP tools not available")
            return False
        
        # Initialize MCP tools
        mcp_tools = MarkdownExportMCPTools()
        
        # Test tool availability
        tools = mcp_tools.get_tools()
        if tools:
            print(f"✅ Found {len(tools)} markdown export MCP tools")
            for tool in tools:
                print(f"   - {tool['function']['name']}: {tool['function']['description']}")
        else:
            print("❌ No markdown export MCP tools found")
            return False
        
        # Test PDF export
        test_markdown = """
# MCP Test Document

This is a test document for **MCP tools**.

## Features Tested
- **Bold formatting**
- *Italic formatting*
- `Code formatting`
- ~~Strikethrough~~

## List Example
1. **First item**
2. *Second item*
3. `Third item`

> This is a blockquote test.

---
*End of MCP test*
"""
        
        result = await mcp_tools.markdown_export_to_pdf(
            markdown_content=test_markdown,
            filename=f"mcp_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        if result.get("success"):
            print(f"✅ MCP PDF export successful: {result}")
        else:
            print(f"❌ MCP PDF export failed: {result}")
            return False
        
        # Test Word export
        result = await mcp_tools.markdown_export_to_word(
            markdown_content=test_markdown,
            filename=f"mcp_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        if result.get("success"):
            print(f"✅ MCP Word export successful: {result}")
        else:
            print(f"❌ MCP Word export failed: {result}")
            return False
        
        # Test file listing
        result = await mcp_tools.markdown_export_list_files()
        if result.get("success"):
            print(f"✅ MCP file listing successful: {result}")
        else:
            print(f"❌ MCP file listing failed: {result}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ MCP test error: {e}")
        return False

def test_markdown_export_file_upload():
    """Test markdown file upload and export."""
    print("🧪 Testing Markdown File Upload and Export...")
    
    base_url = "http://localhost:8000"
    
    # Create a test markdown file
    test_file_content = """
# File Upload Test

This is a test of **file upload** functionality.

## Upload Features
- **File upload** support
- **Automatic filename** generation
- **Multiple format** export
- **Template configuration**

## Code Example
```python
def upload_and_export():
    with open('test.md', 'rb') as f:
        files = {'file': f}
        data = {'output_format': 'pdf'}
        response = requests.post('/api/v1/markdown-export/export-file', 
                               files=files, data=data)
    return response
```

> This demonstrates file upload capabilities.

---
*End of upload test*
"""
    
    # Create temporary test file
    test_file_path = Path("temp_test_file.md")
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_file_content)
    
    try:
        # Test file upload and export
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_file.md", f, "text/markdown")}
            data = {"output_format": "pdf"}
            
            response = requests.post(
                f"{base_url}/api/v1/markdown-export/export-file",
                files=files,
                data=data
            )
        
        if response.status_code == 200:
            print(f"✅ File upload and export successful: {len(response.content)} bytes")
            
            # Save the exported file
            output_path = Path("temp_output/test_upload_export.pdf")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Exported file saved to: {output_path}")
        else:
            print(f"❌ File upload and export failed: {response.status_code} - {response.text}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ File upload test error: {e}")
        return False
    finally:
        # Clean up test file
        if test_file_path.exists():
            test_file_path.unlink()

async def test_markdown_export_batch():
    """Test batch markdown export functionality."""
    print("🧪 Testing Batch Markdown Export...")
    
    try:
        from src.mcp_servers.markdown_export_mcp_tools import MarkdownExportMCPTools, MARKDOWN_EXPORT_AVAILABLE
        
        if not MARKDOWN_EXPORT_AVAILABLE:
            print("❌ Markdown export MCP tools not available")
            return False
        
        mcp_tools = MarkdownExportMCPTools()
        
        # Create multiple test documents
        test_exports = [
            {
                "markdown_content": "# Document 1\n\nThis is **document 1**.",
                "filename": f"batch_test_1_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "formats": ["pdf", "word"]
            },
            {
                "markdown_content": "# Document 2\n\nThis is *document 2*.",
                "filename": f"batch_test_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "formats": ["pdf"]
            },
            {
                "markdown_content": "# Document 3\n\nThis is `document 3`.",
                "filename": f"batch_test_3_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "formats": ["word"]
            }
        ]
        
        result = await mcp_tools.markdown_export_batch(test_exports)
        
        if result.get("success"):
            print(f"✅ Batch export successful: {result}")
            for export_result in result.get("results", []):
                print(f"   - {export_result['filename']}: {export_result['formats']}")
        else:
            print(f"❌ Batch export failed: {result}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Batch export test error: {e}")
        return False

async def main():
    """Run all markdown export tests."""
    print("🚀 Starting Markdown Export Integration Tests...")
    print("=" * 60)
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    await asyncio.sleep(5)
    
    test_results = []
    
    # Test API endpoints
    print("\n" + "=" * 60)
    api_result = test_markdown_export_api()
    test_results.append(("API Endpoints", api_result))
    
    # Test MCP tools
    print("\n" + "=" * 60)
    mcp_result = await test_markdown_export_mcp()
    test_results.append(("MCP Tools", mcp_result))
    
    # Test file upload
    print("\n" + "=" * 60)
    upload_result = test_markdown_export_file_upload()
    test_results.append(("File Upload", upload_result))
    
    # Test batch export
    print("\n" + "=" * 60)
    batch_result = await test_markdown_export_batch()
    test_results.append(("Batch Export", batch_result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20} {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("🎉 All tests passed! Markdown export integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    """Run the test suite."""
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        sys.exit(1)
