#!/usr/bin/env python3
"""
Test MCP Server with All Tools
"""

import requests
import json

def test_mcp_all_tools():
    """Test that all MCP tools are available."""
    print("🧪 Testing MCP Server with All Tools...")
    
    # Test 1: Health check
    try:
        response = requests.get("http://localhost:8000/mcp-health", timeout=5)
        print(f"✅ MCP health check: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   Health data: {health_data}")
            if health_data.get("tools_available") == 29:
                print("   ✅ All 29 tools reported as available")
            else:
                print(f"   ⚠️ Expected 29 tools, got {health_data.get('tools_available', 'unknown')}")
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
            "http://localhost:8000/mcp",
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
    
    # Test 3: List all available tools
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
            "http://localhost:8000/mcp",
            json=tools_request,
            headers=headers,
            timeout=10
        )
        
        print(f"✅ MCP tools/list: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            
            # Check if tools are available
            if 'result' in result and 'tools' in result['result']:
                tools = result['result']['tools']
                print(f"   Available tools: {len(tools)}")
                
                # List all tool names
                tool_names = [tool.get('name', 'Unknown') for tool in tools]
                print("   Tool names:")
                for i, name in enumerate(tool_names, 1):
                    print(f"     {i:2d}. {name}")
                
                # Check for specific important tools
                important_tools = [
                    'generate_enhanced_report',
                    'process_content',
                    'analyze_sentiment',
                    'extract_entities',
                    'generate_knowledge_graph',
                    'analyze_art_of_war_deception'
                ]
                
                print("\n   Checking for important tools:")
                for tool in important_tools:
                    if tool in tool_names:
                        print(f"     ✅ Found: {tool}")
                    else:
                        print(f"     ❌ Missing: {tool}")
                
                if len(tools) >= 29:
                    print(f"\n   ✅ Success! All {len(tools)} tools are available")
                    return True
                else:
                    print(f"\n   ⚠️ Expected 29+ tools, got {len(tools)}")
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
    success = test_mcp_all_tools()
    if success:
        print("\n✅ MCP server is working with all tools!")
    else:
        print("\n❌ MCP server has issues with tools!")
