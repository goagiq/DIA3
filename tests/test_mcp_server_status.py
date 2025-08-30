"""
Test script to check MCP server status and connectivity
"""
import requests
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_mcp_server():
    """Test MCP server connectivity and basic functionality."""
    
    print("🔍 Testing MCP Server Status...")
    print("=" * 50)
    
    # Test 1: Check if server is responding
    print("1. Testing basic connectivity...")
    try:
        response = requests.get("http://localhost:8000/mcp", timeout=5)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Test MCP initialize
    print("\n2. Testing MCP initialize...")
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test",
                    "version": "1.0.0"
                }
            }
        }
        
        response = requests.post(
            "http://localhost:8000/mcp",
            headers=headers,
            json=data,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                print("   ✅ MCP initialize successful")
            else:
                print("   ⚠️ MCP initialize returned error")
        else:
            print("   ❌ MCP initialize failed")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Test tools/list
    print("\n3. Testing tools/list...")
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        data = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        response = requests.post(
            "http://localhost:8000/mcp",
            headers=headers,
            json=data,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result and "tools" in result["result"]:
                tools = result["result"]["tools"]
                print(f"   ✅ Found {len(tools)} MCP tools")
                for tool in tools[:5]:  # Show first 5 tools
                    print(f"      - {tool.get('name', 'Unknown')}")
                if len(tools) > 5:
                    print(f"      ... and {len(tools) - 5} more")
            else:
                print("   ⚠️ No tools found or error in response")
        else:
            print("   ❌ tools/list failed")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Check Phase 5 tools specifically
    print("\n4. Testing Phase 5 tools availability...")
    try:
        # Test a simple Phase 5 tool call
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        data = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "phase5_health_check_tool",
                "arguments": {}
            }
        }
        
        response = requests.post(
            "http://localhost:8000/mcp",
            headers=headers,
            json=data,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                print("   ✅ Phase 5 tool call successful")
            else:
                print("   ⚠️ Phase 5 tool call returned error")
        else:
            print("   ❌ Phase 5 tool call failed")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 MCP Server Status Test Complete")

if __name__ == "__main__":
    test_mcp_server()
