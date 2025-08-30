#!/usr/bin/env python3
"""
Simple test to check if the MCP server is working at the correct endpoint.
"""

import requests


def test_mcp_server():
    """Test the MCP server at the correct endpoint."""
    print("=== TESTING MCP SERVER ===")
    
    try:
        # Test if the MCP server is responding at the correct endpoint
        # The MCP server requires Accept header to include both application/json and text/event-stream
        response = requests.post(
            "http://localhost:8000/mcp",
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
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            timeout=5
        )
        print(f"✅ Initialize Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        if response.status_code == 200:
            print("✅ MCP server is responding to JSON-RPC calls at /mcp")
            
            # Test tools/list
            response = requests.post(
                "http://localhost:8000/mcp",
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {}
                },
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream"
                },
                timeout=5
            )
            print(f"✅ Tools/List Status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'tools' in data['result']:
                    tools = data['result']['tools']
                    print(f"✅ Retrieved {len(tools)} tools from MCP server")
                    
                    # Look for Monte Carlo tools
                    monte_carlo_tools = [
                        tool for tool in tools 
                        if 'monte_carlo' in tool.get('name', '').lower()
                    ]
                    print(f"✅ Found {len(monte_carlo_tools)} Monte Carlo tools")
                    
                    # Print tool names for verification
                    tool_names = [tool.get('name', 'unknown') for tool in tools]
                    print(f"✅ Available tools: {tool_names}")
                    
                    return True
                else:
                    print("❌ No tools found in response")
                    return False
            else:
                print(f"❌ Tools/List failed: {response.status_code}")
                return False
        else:
            print(f"❌ Initialize failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False


if __name__ == "__main__":
    success = test_mcp_server()
    if success:
        print("\n🎉 MCP Server Test PASSED!")
        print("The MCP server is working correctly at the /mcp endpoint.")
    else:
        print("\n❌ MCP Server Test FAILED!")
    exit(0 if success else 1)
