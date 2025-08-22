#!/usr/bin/env python3
"""
Test MCP Server with 32 Tools
"""

import requests
import json

def test_mcp_32_tools():
    """Test that all 32 MCP tools are available."""
    print("🧪 Testing MCP Server with 32 Tools...")

    # Test 1: Health check
    try:
        response = requests.get("http://localhost:8003/mcp-health", timeout=5)
        print(f"✅ MCP health check: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   Health data: {health_data}")
    except Exception as e:
        print(f"❌ MCP health check failed: {e}")
        return False

    # Test 2: Initialize MCP connection
    try:
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }

        response = requests.post(
            "http://localhost:8003/mcp",
            json=init_request,
            headers=headers,
            timeout=10
        )

        print(f"✅ MCP initialize: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Initialize result: {json.dumps(result, indent=2)}")
        else:
            print(f"   Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ MCP initialize failed: {e}")
        return False

    # Test 3: List available tools
    try:
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }

        response = requests.post(
            "http://localhost:8003/mcp",
            json=tools_request,
            headers=headers,
            timeout=10
        )

        print(f"✅ MCP tools/list: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Tools list result: {json.dumps(result, indent=2)}")

            if 'result' in result and 'tools' in result['result']:
                tools = result['result']['tools']
                print(f"   Available tools: {len(tools)}")
                if len(tools) >= 32:
                    print("   ✅ At least 32 tools are available")
                    print("   📋 Tool names:")
                    for i, tool in enumerate(tools[:10], 1):
                        print(f"      {i}. {tool.get('name', 'Unknown')}")
                    if len(tools) > 10:
                        print(f"      ... and {len(tools) - 10} more tools")
                    return True
                else:
                    print(f"   ❌ Expected at least 32 tools, but found {len(tools)}")
                    return False
            else:
                print("   ❌ No tools found in response")
                return False
        else:
            print(f"   Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ MCP tools/list failed: {e}")
        return False

if __name__ == "__main__":
    success = test_mcp_32_tools()
    if success:
        print("\n✅ MCP server has all 32 tools available!")
    else:
        print("\n❌ MCP server has issues with tools!")
