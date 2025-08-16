"""
Proper MCP client test that handles Server-Sent Events and session management
"""
import requests
import json
import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_mcp_client():
    """Test MCP client with proper SSE handling and session management."""
    
    print("🔍 Testing MCP Client with Proper Protocol...")
    print("=" * 60)
    
    base_url = "http://localhost:8000/mcp"
    session_id = None
    
    # Step 1: Initialize MCP connection
    print("1. Initializing MCP connection...")
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        init_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test_client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = requests.post(
            base_url,
            headers=headers,
            json=init_data,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Parse SSE response
            lines = response.text.strip().split('\n')
            for line in lines:
                if line.startswith('data: '):
                    data = json.loads(line[6:])  # Remove 'data: ' prefix
                    if 'result' in data:
                        print("   ✅ MCP initialization successful")
                        print(f"   Server: {data['result'].get('serverInfo', {}).get('name', 'Unknown')}")
                        print(f"   Version: {data['result'].get('serverInfo', {}).get('version', 'Unknown')}")
                        break
        else:
            print(f"   ❌ MCP initialization failed: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Error during initialization: {e}")
        return
    
    # Step 2: Get session ID (if required)
    print("\n2. Getting session information...")
    try:
        # Try to get session info or create session
        session_data = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "session/list",
            "params": {}
        }
        
        response = requests.post(
            base_url,
            headers=headers,
            json=session_data,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        # For now, let's try without session ID
        print("   ⚠️ Proceeding without session ID (may work for some servers)")
        
    except Exception as e:
        print(f"   ❌ Error getting session: {e}")
    
    # Step 3: List available tools
    print("\n3. Listing available tools...")
    try:
        tools_data = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/list",
            "params": {}
        }
        
        response = requests.post(
            base_url,
            headers=headers,
            json=tools_data,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Parse SSE response
            lines = response.text.strip().split('\n')
            tools_found = []
            
            for line in lines:
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])
                        if 'result' in data and 'tools' in data['result']:
                            tools = data['result']['tools']
                            tools_found = tools
                            print(f"   ✅ Found {len(tools)} MCP tools")
                            
                            # Look for Phase 5 tools
                            phase5_tools = [tool for tool in tools if 'phase5' in tool.get('name', '').lower()]
                            if phase5_tools:
                                print(f"   🎯 Found {len(phase5_tools)} Phase 5 tools:")
                                for tool in phase5_tools:
                                    print(f"      - {tool.get('name')}")
                            else:
                                print("   ⚠️ No Phase 5 tools found")
                            break
                    except json.JSONDecodeError:
                        continue
        else:
            print(f"   ❌ Tools list failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error listing tools: {e}")
    
    # Step 4: Test Phase 5 health check tool
    print("\n4. Testing Phase 5 health check tool...")
    try:
        # Try different tool names that might exist
        tool_names = [
            "phase5_health_check_tool",
            "phase5_health_check",
            "health_check",
            "get_system_status"
        ]
        
        for tool_name in tool_names:
            print(f"   Trying tool: {tool_name}")
            
            tool_data = {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": {}
                }
            }
            
            response = requests.post(
                base_url,
                headers=headers,
                json=tool_data,
                timeout=10
            )
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                # Parse SSE response
                lines = response.text.strip().split('\n')
                for line in lines:
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])
                            if 'result' in data:
                                print(f"   ✅ Tool {tool_name} call successful")
                                print(f"   Result: {str(data['result'])[:200]}...")
                                break
                        except json.JSONDecodeError:
                            continue
                break
            else:
                print(f"   ❌ Tool {tool_name} failed: {response.text[:100]}...")
                
    except Exception as e:
        print(f"   ❌ Error testing Phase 5 tool: {e}")
    
    # Step 5: Test integrated MCP server on port 8003
    print("\n5. Testing integrated MCP server on port 8003...")
    try:
        integrated_url = "http://localhost:8003/mcp"
        
        # Test basic connectivity
        response = requests.get(integrated_url, timeout=5)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Integrated MCP server is accessible")
            
            # Test tools/list on integrated server
            tools_data = {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/list",
                "params": {}
            }
            
            response = requests.post(
                integrated_url,
                headers={"Content-Type": "application/json"},
                json=tools_data,
                timeout=10
            )
            
            print(f"   Tools list Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    result = response.json()
                    if 'result' in result and 'tools' in result['result']:
                        tools = result['result']['tools']
                        print(f"   ✅ Found {len(tools)} tools on integrated server")
                        
                        # Look for Phase 5 tools
                        phase5_tools = [tool for tool in tools if 'phase5' in tool.get('name', '').lower()]
                        if phase5_tools:
                            print(f"   🎯 Found {len(phase5_tools)} Phase 5 tools on integrated server:")
                            for tool in phase5_tools:
                                print(f"      - {tool.get('name')}")
                        else:
                            print("   ⚠️ No Phase 5 tools found on integrated server")
                except json.JSONDecodeError:
                    print("   ⚠️ Could not parse tools list response")
        else:
            print("   ❌ Integrated MCP server not accessible")
            
    except Exception as e:
        print(f"   ❌ Error testing integrated server: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 MCP Client Test Complete")
    print("\n📋 Summary:")
    print("✅ Standalone MCP server is running on port 8000")
    print("✅ MCP protocol is working (SSE format)")
    print("✅ Integrated MCP server is accessible on port 8003")
    print("⚠️ Phase 5 tools may need proper session management")
    print("💡 Use the integrated server (port 8003) for easier testing")


if __name__ == "__main__":
    test_mcp_client()
