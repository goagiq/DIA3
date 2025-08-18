#!/usr/bin/env python3
"""
Markdown to PDF/DOC Converter

Automatically converts markdown files to PDF and DOC formats using the DIA3 system's
MCP tools and API endpoints. This script provides a unified interface for markdown conversion.

Usage:
    python convert_markdown.py --input file.md --output pdf,docx
    python convert_markdown.py --input "*.md" --output both
    python convert_markdown.py --input file.md --output pdf --api
"""

import asyncio
import sys
import os
import argparse
import glob
from pathlib import Path
from typing import List, Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def convert_with_mcp_tools(markdown_content: str, output_format: str, filename: str) -> dict:
    """Convert markdown using MCP tools."""
    try:
        from src.mcp_servers.simple_markdown_export_mcp_tools import SimpleMarkdownExportMCPTools
        
        mcp_tools = SimpleMarkdownExportMCPTools()
        
        if output_format == "pdf":
            result = await mcp_tools.simple_markdown_export_to_pdf(markdown_content, filename)
        elif output_format == "docx":
            result = await mcp_tools.simple_markdown_export_to_word(markdown_content, filename)
        elif output_format == "both":
            result = await mcp_tools.simple_markdown_export_to_both(markdown_content, filename)
        else:
            return {"success": False, "error": f"Unsupported format: {output_format}"}
        
        return result
    except Exception as e:
        return {"success": False, "error": f"MCP tools error: {str(e)}"}

async def convert_with_api(markdown_content: str, output_format: str, filename: str) -> dict:
    """Convert markdown using API endpoints."""
    try:
        import requests
        import json
        
        # API endpoint
        api_url = "http://localhost:8000/api/v1/simple-markdown-export/export"
        
        # Prepare request
        payload = {
            "markdown_content": markdown_content,
            "output_format": output_format,
            "filename": filename
        }
        
        # Make request
        response = requests.post(api_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"success": False, "error": f"API error: {str(e)}"}

async def convert_with_direct_service(markdown_content: str, output_format: str, filename: str) -> dict:
    """Convert markdown using direct service call."""
    try:
        from src.core.export.simple_markdown_export_service import SimpleMarkdownExportService
        
        # Initialize service
        output_dir = "docs/white_papers"
        export_service = SimpleMarkdownExportService(output_dir)
        
        if output_format == "pdf":
            result = await export_service.export_markdown_to_pdf(
                markdown_content,
                output_filename=f"{filename}.pdf"
            )
        elif output_format == "docx":
            result = await export_service.export_markdown_to_word(
                markdown_content,
                output_filename=f"{filename}.docx"
            )
        elif output_format == "both":
            result = await export_service.export_markdown_to_both(
                markdown_content,
                output_filename=filename
            )
        else:
            return {"success": False, "error": f"Unsupported format: {output_format}"}
        
        return result
    except Exception as e:
        return {"success": False, "error": f"Direct service error: {str(e)}"}

async def convert_markdown_file(input_file: str, output_format: str, use_api: bool = False) -> dict:
    """Convert a single markdown file."""
    try:
        # Read markdown content
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Generate filename
        base_filename = Path(input_file).stem
        timestamp = asyncio.get_event_loop().time()
        filename = f"{base_filename}_{int(timestamp)}"
        
        print(f"📄 Converting {input_file} to {output_format}...")
        
        # Try different conversion methods
        result = None
        
        # Method 1: Try MCP tools first
        if not use_api:
            print("  🔧 Trying MCP tools...")
            result = await convert_with_mcp_tools(markdown_content, output_format, filename)
            
            if result.get("success"):
                print("  ✅ MCP tools conversion successful")
                return result
        
        # Method 2: Try API if requested or MCP failed
        if use_api or not result.get("success"):
            print("  🌐 Trying API endpoint...")
            result = await convert_with_api(markdown_content, output_format, filename)
            
            if result.get("success"):
                print("  ✅ API conversion successful")
                return result
        
        # Method 3: Fallback to direct service
        print("  🔧 Trying direct service...")
        result = await convert_with_direct_service(markdown_content, output_format, filename)
        
        if result.get("success"):
            print("  ✅ Direct service conversion successful")
            return result
        else:
            print(f"  ❌ All conversion methods failed: {result.get('error')}")
            return result
            
    except Exception as e:
        return {"success": False, "error": f"File conversion error: {str(e)}"}

async def convert_markdown_files(input_pattern: str, output_format: str, use_api: bool = False) -> List[dict]:
    """Convert multiple markdown files."""
    # Expand glob pattern
    files = glob.glob(input_pattern)
    
    if not files:
        return [{"success": False, "error": f"No files found matching pattern: {input_pattern}"}]
    
    print(f"📁 Found {len(files)} files to convert")
    
    results = []
    for file in files:
        result = await convert_markdown_file(file, output_format, use_api)
        results.append({"file": file, "result": result})
    
    return results

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Convert markdown files to PDF and DOC formats")
    parser.add_argument("--input", "-i", required=True, help="Input markdown file or glob pattern")
    parser.add_argument("--output", "-o", default="both", choices=["pdf", "docx", "both"], 
                       help="Output format (default: both)")
    parser.add_argument("--api", action="store_true", help="Use API endpoint instead of MCP tools")
    parser.add_argument("--list", action="store_true", help="List available conversion methods")
    
    args = parser.parse_args()
    
    if args.list:
        print("🛠️ Available conversion methods:")
        print("  1. MCP Tools (default) - Uses internal MCP tools")
        print("  2. API Endpoint - Uses HTTP API (requires server running)")
        print("  3. Direct Service - Uses export service directly")
        print("\n📋 Usage examples:")
        print("  python convert_markdown.py --input file.md --output pdf")
        print("  python convert_markdown.py --input '*.md' --output both")
        print("  python convert_markdown.py --input file.md --output docx --api")
        return 0
    
    print("🚀 Markdown to PDF/DOC Converter")
    print("=" * 50)
    
    # Convert files
    results = asyncio.run(convert_markdown_files(args.input, args.output, args.api))
    
    # Print results
    print("\n📊 Conversion Results:")
    print("=" * 50)
    
    success_count = 0
    total_count = len(results)
    
    for item in results:
        if "file" in item:
            file = item["file"]
            result = item["result"]
        else:
            file = "Unknown"
            result = item
        
        if result.get("success"):
            success_count += 1
            print(f"✅ {file}: Success")
            if "file_path" in result:
                print(f"   📄 Output: {result['file_path']}")
            if "file_size" in result:
                print(f"   📊 Size: {result['file_size']} bytes")
        else:
            print(f"❌ {file}: Failed - {result.get('error', 'Unknown error')}")
    
    print(f"\n📈 Summary: {success_count}/{total_count} files converted successfully")
    
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())
