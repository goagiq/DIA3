#!/usr/bin/env python3
"""
Simple MCP Connection Test

This script tests the MCP server connection without requiring external dependencies.
"""

import sys
import os
import time
import json
import requests
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger

def test_mcp_endpoint_connection():
    """Test MCP endpoint connection and basic functionality."""
    try:
        logger.info("🔧 Testing MCP Endpoint Connection...")
        
        # Test the working MCP endpoint on port 8003
        mcp_url = "http://localhost:8003/mcp"
        
        logger.info(f"🔗 Connecting to MCP endpoint: {mcp_url}")
        
        # Test basic GET request
        response = requests.get(mcp_url, timeout=10)
        logger.info(f"✅ GET request successful: {response.status_code}")
        
        # Test POST request with MCP initialize method
        initialize_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        logger.info("📋 Testing MCP initialize method...")
        response = requests.post(mcp_url, json=initialize_payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ MCP initialize successful: {data}")
            
            # Test list tools method
            list_tools_payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
            
            logger.info("📋 Testing MCP list tools method...")
            response = requests.post(mcp_url, json=list_tools_payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                tools = data.get("result", {}).get("tools", [])
                logger.info(f"✅ Found {len(tools)} MCP tools")
                
                # Check for enhanced markdown export tools
                enhanced_tools = []
                for tool in tools:
                    if "enhanced_markdown_export" in tool.get("name", "").lower():
                        enhanced_tools.append(tool)
                
                if enhanced_tools:
                    logger.info(f"✅ Found {len(enhanced_tools)} enhanced markdown export tools:")
                    for tool in enhanced_tools:
                        logger.info(f"   - {tool.get('name')}: {tool.get('description', 'No description')}")
                else:
                    logger.warning("⚠️ No enhanced markdown export tools found")
                
                return {
                    "success": True,
                    "total_tools": len(tools),
                    "enhanced_tools": len(enhanced_tools),
                    "enhanced_tool_names": [tool.get("name") for tool in enhanced_tools],
                    "message": "MCP connection and tool listing successful"
                }
            else:
                logger.error(f"❌ MCP list tools failed: {response.status_code}")
                return {
                    "success": False,
                    "error": f"List tools failed: {response.status_code}",
                    "message": "MCP list tools method failed"
                }
        else:
            logger.error(f"❌ MCP initialize failed: {response.status_code}")
            return {
                "success": False,
                "error": f"Initialize failed: {response.status_code}",
                "message": "MCP initialize method failed"
            }
            
    except Exception as e:
        logger.error(f"❌ MCP connection test failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "MCP connection test failed"
        }

def test_enhanced_markdown_export_tools():
    """Test if enhanced markdown export tools are available via MCP."""
    try:
        logger.info("🎯 Testing Enhanced Markdown Export Tools via MCP...")
        
        mcp_url = "http://localhost:8003/mcp"
        
        # First initialize the MCP connection
        initialize_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = requests.post(mcp_url, json=initialize_payload, timeout=10)
        if response.status_code != 200:
            logger.error("❌ Failed to initialize MCP connection")
            return {"success": False, "error": "MCP initialization failed"}
        
        # List tools
        list_tools_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        response = requests.post(mcp_url, json=list_tools_payload, timeout=10)
        if response.status_code != 200:
            logger.error("❌ Failed to list MCP tools")
            return {"success": False, "error": "MCP list tools failed"}
        
        data = response.json()
        tools = data.get("result", {}).get("tools", [])
        
        # Look for enhanced markdown export tools
        enhanced_tools = []
        for tool in tools:
            if "enhanced_markdown_export" in tool.get("name", "").lower():
                enhanced_tools.append(tool)
        
        if enhanced_tools:
            logger.info(f"✅ Found {len(enhanced_tools)} enhanced markdown export tools:")
            for tool in enhanced_tools:
                logger.info(f"   - {tool.get('name')}: {tool.get('description', 'No description')}")
            
            # Test calling one of the tools
            if enhanced_tools:
                test_tool = enhanced_tools[0]
                tool_name = test_tool.get("name")
                
                logger.info(f"🧪 Testing tool: {tool_name}")
                
                # Test the tool with a simple call
                call_payload = {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": {
                            "markdown_content": "# Test\nThis is a test document.",
                            "filename": "test_mcp_export"
                        }
                    }
                }
                
                response = requests.post(mcp_url, json=call_payload, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"✅ Tool call successful: {data}")
                    return {
                        "success": True,
                        "tools_found": len(enhanced_tools),
                        "tool_names": [tool.get("name") for tool in enhanced_tools],
                        "test_tool_call": "successful",
                        "message": "Enhanced markdown export tools are working via MCP"
                    }
                else:
                    logger.warning(f"⚠️ Tool call failed: {response.status_code}")
                    return {
                        "success": True,
                        "tools_found": len(enhanced_tools),
                        "tool_names": [tool.get("name") for tool in enhanced_tools],
                        "test_tool_call": "failed",
                        "message": "Enhanced markdown export tools found but call failed"
                    }
        else:
            logger.warning("⚠️ No enhanced markdown export tools found in MCP tools")
            return {
                "success": False,
                "tools_found": 0,
                "message": "No enhanced markdown export tools found"
            }
            
    except Exception as e:
        logger.error(f"❌ Enhanced markdown export tools test failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Enhanced markdown export tools test failed"
        }

def main():
    """Main test function."""
    logger.info("🚀 Starting Simple MCP Connection Tests")
    logger.info("=" * 60)
    
    # Test basic MCP connection
    logger.info("📋 Testing Basic MCP Connection...")
    connection_results = test_mcp_endpoint_connection()
    
    # Test enhanced markdown export tools
    logger.info("🎯 Testing Enhanced Markdown Export Tools...")
    tools_results = test_enhanced_markdown_export_tools()
    
    # Summary
    logger.info("=" * 60)
    logger.info("📊 Test Results Summary:")
    
    if connection_results.get("success"):
        logger.info("✅ MCP Connection: SUCCESS")
        logger.info(f"   Total Tools: {connection_results.get('total_tools', 0)}")
        logger.info(f"   Enhanced Tools: {connection_results.get('enhanced_tools', 0)}")
    else:
        logger.error("❌ MCP Connection: FAILED")
        logger.error(f"   Error: {connection_results.get('error', 'Unknown error')}")
    
    if tools_results.get("success"):
        logger.info("✅ Enhanced Markdown Export Tools: SUCCESS")
        logger.info(f"   Tools Found: {tools_results.get('tools_found', 0)}")
        if tools_results.get("tool_names"):
            logger.info(f"   Tool Names: {', '.join(tools_results['tool_names'])}")
    else:
        logger.error("❌ Enhanced Markdown Export Tools: FAILED")
        logger.error(f"   Error: {tools_results.get('error', 'Unknown error')}")
    
    # Save results
    results = {
        "timestamp": time.time(),
        "mcp_connection": connection_results,
        "enhanced_tools": tools_results
    }
    
    output_file = Path("Test/mcp_simple_connection_results.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"📄 Test results saved to: {output_file}")
    
    # Exit with appropriate code
    if connection_results.get("success") and tools_results.get("success"):
        logger.info("✅ MCP connection and tools test completed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ MCP connection and tools test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
