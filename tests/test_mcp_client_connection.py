#!/usr/bin/env python3
"""
Test script for MCP Client Connection

This script tests the connection between the MCP client and MCP tools
using the streamable HTTP implementation.
"""

import sys
import os
import time
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger

def test_mcp_client_connection():
    """Test MCP client connection using streamable HTTP."""
    try:
        # Import the required modules
        from mcp.client.streamable_http import streamablehttp_client
        from strands import Agent
        from strands.tools.mcp.mcp_client import MCPClient
        
        logger.info("🔧 Testing MCP Client Connection...")
        
        # Create the streamable HTTP MCP client
        streamable_http_mcp_client = MCPClient(lambda: streamablehttp_client("http://localhost:8000/mcp"))
        
        logger.info("✅ MCP Client created successfully")
        
        # Test the connection
        with streamable_http_mcp_client:
            logger.info("🔗 Connected to MCP server")
            
            # Get the tools from the MCP server
            logger.info("📋 Listing available tools...")
            tools = streamable_http_mcp_client.list_tools_sync()
            
            logger.info(f"✅ Found {len(tools)} tools")
            
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
            
            # Create an agent with these tools
            logger.info("🤖 Creating agent with MCP tools...")
            agent = Agent(tools=tools)
            logger.info("✅ Agent created successfully")
            
            # Test basic MCP functionality
            logger.info("🧪 Testing basic MCP functionality...")
            
            # Try to get tool schemas
            try:
                schemas = streamable_http_mcp_client.list_tool_schemas_sync()
                logger.info(f"✅ Retrieved {len(schemas)} tool schemas")
            except Exception as e:
                logger.warning(f"⚠️ Could not retrieve tool schemas: {e}")
            
            return {
                "success": True,
                "total_tools": len(tools),
                "enhanced_tools": len(enhanced_tools),
                "enhanced_tool_names": [tool.get("name") for tool in enhanced_tools],
                "message": "MCP client connection successful"
            }
            
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return {
            "success": False,
            "error": f"Import error: {e}",
            "message": "Required MCP client libraries not available"
        }
    except Exception as e:
        logger.error(f"❌ MCP client connection failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "MCP client connection failed"
        }

def test_mcp_server_endpoints():
    """Test MCP server endpoints directly."""
    try:
        import requests
        
        logger.info("🌐 Testing MCP Server Endpoints...")
        
        # Test different MCP endpoints
        endpoints = [
            "http://localhost:8000/mcp",
            "http://localhost:8000/mcp/",
            "http://localhost:8003/mcp",
            "http://localhost:8003/mcp/",
            "http://localhost:8004/mcp",
            "http://localhost:8004/mcp/"
        ]
        
        results = {}
        
        for endpoint in endpoints:
            try:
                logger.info(f"🔍 Testing endpoint: {endpoint}")
                response = requests.get(endpoint, timeout=5)
                results[endpoint] = {
                    "status_code": response.status_code,
                    "content_type": response.headers.get("content-type", "unknown"),
                    "success": response.status_code == 200
                }
                logger.info(f"   Status: {response.status_code}, Content-Type: {response.headers.get('content-type', 'unknown')}")
            except Exception as e:
                results[endpoint] = {
                    "status_code": None,
                    "error": str(e),
                    "success": False
                }
                logger.warning(f"   Error: {e}")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Endpoint testing failed: {e}")
        return {"error": str(e)}

def main():
    """Main test function."""
    logger.info("🚀 Starting MCP Client Connection Tests")
    logger.info("=" * 60)
    
    # Test MCP server endpoints first
    logger.info("📋 Testing MCP Server Endpoints...")
    endpoint_results = test_mcp_server_endpoints()
    
    # Test MCP client connection
    logger.info("🔧 Testing MCP Client Connection...")
    client_results = test_mcp_client_connection()
    
    # Summary
    logger.info("=" * 60)
    logger.info("📊 Test Results Summary:")
    
    if client_results.get("success"):
        logger.info("✅ MCP Client Connection: SUCCESS")
        logger.info(f"   Total Tools: {client_results.get('total_tools', 0)}")
        logger.info(f"   Enhanced Tools: {client_results.get('enhanced_tools', 0)}")
        if client_results.get("enhanced_tool_names"):
            logger.info(f"   Enhanced Tool Names: {', '.join(client_results['enhanced_tool_names'])}")
    else:
        logger.error("❌ MCP Client Connection: FAILED")
        logger.error(f"   Error: {client_results.get('error', 'Unknown error')}")
    
    # Save results
    results = {
        "timestamp": time.time(),
        "client_connection": client_results,
        "endpoint_tests": endpoint_results
    }
    
    output_file = Path("Test/mcp_client_connection_results.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"📄 Test results saved to: {output_file}")
    
    # Exit with appropriate code
    if client_results.get("success"):
        logger.info("✅ MCP client connection test completed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ MCP client connection test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
