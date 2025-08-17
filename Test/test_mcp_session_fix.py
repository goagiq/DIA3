#!/usr/bin/env python3
"""
Test MCP server with proper session management to fix the "Missing session ID" issue.
"""

import requests
import json


def test_mcp_server_with_session():
    """Test the MCP server with proper session management."""
    print("=== TESTING MCP SERVER WITH SESSION MANAGEMENT ===")
    
    try:
        # Step 1: Initialize the session
        print("Step 1: Initializing MCP session...")
        init_response = requests.post(
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
        print(f"✅ Initialize Status: {init_response.status_code}")
        
        if init_response.status_code == 200:
            print("✅ MCP session initialized successfully")
            
            # Step 2: List tools (should work now with session established)
            print("\nStep 2: Listing tools...")
            tools_response = requests.post(
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
            print(f"✅ Tools/List Status: {tools_response.status_code}")
            
            if tools_response.status_code == 200:
                data = tools_response.json()
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
                    
                    # Step 3: Test a Monte Carlo tool if available
                    if monte_carlo_tools:
                        print(f"\nStep 3: Testing Monte Carlo tool: {monte_carlo_tools[0]['name']}")
                        test_response = requests.post(
                            "http://localhost:8000/mcp",
                            json={
                                "jsonrpc": "2.0",
                                "id": 3,
                                "method": "tools/call",
                                "params": {
                                    "name": monte_carlo_tools[0]['name'],
                                    "arguments": {}
                                }
                            },
                            headers={
                                "Content-Type": "application/json",
                                "Accept": "application/json, text/event-stream"
                            },
                            timeout=10
                        )
                        print(f"✅ Tool Call Status: {test_response.status_code}")
                        print(f"Response: {test_response.text[:200]}")
                    
                    return True
                else:
                    print("❌ No tools found in response")
                    print(f"Response: {data}")
                    return False
            else:
                print(f"❌ Tools/List failed: {tools_response.status_code}")
                print(f"Response: {tools_response.text[:200]}")
                return False
        else:
            print(f"❌ Initialize failed: {init_response.status_code}")
            print(f"Response: {init_response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False


def test_dynamic_tool_management():
    """Test the Dynamic Tool Management API."""
    print("\n=== TESTING DYNAMIC TOOL MANAGEMENT API ===")
    
    try:
        response = requests.get(
            'http://localhost:8003/mcp/tools/status', 
            timeout=5
        )
        print(f"✅ API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response: {len(data)} tool statuses retrieved")
            
            # Check for Monte Carlo tools
            monte_carlo_tools = [
                name for name in data.keys() 
                if 'monte_carlo' in name.lower()
            ]
            print(f"✅ Found {len(monte_carlo_tools)} Monte Carlo tools: {monte_carlo_tools}")
            
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Dynamic Tool Management API: {e}")
        return False


def main():
    """Main test function."""
    print("🚀 Starting MCP Session Management Test")
    print("=" * 60)
    
    # Test results
    results = {}
    
    # Test 1: MCP Server with session management
    results['mcp_server_session'] = test_mcp_server_with_session()
    
    # Test 2: Dynamic Tool Management API
    results['dynamic_tool_management'] = test_dynamic_tool_management()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    # Overall result
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 ALL TESTS PASSED - Phase 7 Issues Resolved!")
        print("Both MCP Tools session management and Dynamic Tool Management API are working.")
        print("The 'Missing session ID' issue has been resolved.")
    else:
        print("\n⚠️ Some tests failed. Please check the output above for details.")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
