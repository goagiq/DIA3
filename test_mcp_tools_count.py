#!/usr/bin/env python3
"""
Simple MCP Tools Count Test
"""

import requests
import json

def count_mcp_tools():
    """Count available MCP tools."""
    print("🔍 Counting MCP Tools...")
    
    # Try to get tools list
    try:
        tools_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        # Try port 8000 (standalone MCP server)
        response = requests.post(
            "http://localhost:8000/mcp",
            json=tools_request,
            headers=headers,
            timeout=10
        )
        
        print(f"✅ Response from port 8000: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if 'result' in result and 'tools' in result['result']:
                    tools = result['result']['tools']
                    print(f"   📊 Found {len(tools)} tools on port 8000")
                    return len(tools)
                else:
                    print("   ❌ No tools found in response")
            except json.JSONDecodeError:
                print("   ❌ Invalid JSON response")
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing port 8000: {e}")
    
    # Try port 8003 (integrated server)
    try:
        response = requests.post(
            "http://localhost:8003/mcp",
            json=tools_request,
            headers=headers,
            timeout=10
        )
        
        print(f"✅ Response from port 8003: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if 'result' in result and 'tools' in result['result']:
                    tools = result['result']['tools']
                    print(f"   📊 Found {len(tools)} tools on port 8003")
                    return len(tools)
                else:
                    print("   ❌ No tools found in response")
            except json.JSONDecodeError:
                print("   ❌ Invalid JSON response")
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing port 8003: {e}")
    
    return 0

if __name__ == "__main__":
    tool_count = count_mcp_tools()
    if tool_count >= 32:
        print(f"\n✅ Success! Found {tool_count} MCP tools")
    else:
        print(f"\n❌ Only found {tool_count} tools (expected 32+)")
