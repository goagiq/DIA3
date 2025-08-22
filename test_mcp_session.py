#!/usr/bin/env python3
"""
Test MCP Server with Proper Session Handling
"""

import requests
import json
import time

def test_mcp_session():
    """Test MCP server with proper session handling."""
    print("🧪 Testing MCP Server with Session Handling...")
    
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    })
    
    # Step 1: Initialize the session
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
        
        response = session.post(
            "http://localhost:8000/mcp",
            json=init_request,
            timeout=10
        )
        
        print(f"✅ Initialize response: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Initialize failed: {e}")
        return False
    
    # Step 2: List tools
    try:
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        response = session.post(
            "http://localhost:8000/mcp",
            json=tools_request,
            timeout=10
        )
        
        print(f"✅ Tools list response: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:500]}...")
            
            try:
                result = response.json()
                if 'result' in result and 'tools' in result['result']:
                    tools = result['result']['tools']
                    print(f"   Available tools: {len(tools)}")
                    if len(tools) >= 29:
                        print("   ✅ At least 29 tools are available")
                        return True
                    else:
                        print(f"   ❌ Expected at least 29 tools, but found {len(tools)}")
                        return False
                else:
                    print("   ❌ No tools found in response")
                    return False
            except json.JSONDecodeError:
                print("   ❌ Invalid JSON response")
                return False
        else:
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Tools list failed: {e}")
        return False

if __name__ == "__main__":
    success = test_mcp_session()
    if success:
        print("\n✅ MCP server is working with all tools!")
    else:
        print("\n❌ MCP server has issues!")
