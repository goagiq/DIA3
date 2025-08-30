#!/usr/bin/env python3
"""
Simple test to check MCP client connection and identify specific errors.
"""

import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


async def test_mcp_connection():
    """Test basic MCP connection."""
    print("=== TESTING MCP CONNECTION ===")
    
    try:
        # Import the required modules for streamable HTTP client
        from mcp.client.streamable_http import streamablehttp_client
        
        print("✅ Successfully imported streamable HTTP client module")
        
        # Test direct connection to see if the server is responding
        import requests
        
        # Test if the MCP server is responding to basic HTTP requests
        try:
            response = requests.post(
                "http://localhost:8000",
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {"name": "test", "version": "1.0.0"}
                    }
                },
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            print(f"✅ MCP server responded to initialize: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
            # Test tools/list
            response = requests.post(
                "http://localhost:8000",
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {}
                },
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            print(f"✅ MCP server responded to tools/list: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing MCP server directly: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing MCP connection: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    print("🚀 Starting Simple MCP Connection Test")
    print("=" * 60)
    
    success = await test_mcp_connection()
    
    if success:
        print("\n🎉 MCP Connection Test PASSED!")
    else:
        print("\n❌ MCP Connection Test FAILED!")
    
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
