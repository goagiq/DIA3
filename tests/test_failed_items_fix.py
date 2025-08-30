#!/usr/bin/env python3
"""
Comprehensive test to fix the failed items from Phase 7 integration test.
Addresses:
1. MCP Tools - Session management issue (400 Bad Request: Missing session ID)
2. Dynamic Tool Management - API not exposed externally
"""

import sys
import os
import requests
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_dynamic_tool_management_api():
    """Test the Dynamic Tool Management API."""
    print("=== TESTING DYNAMIC TOOL MANAGEMENT API ===")
    
    try:
        # Test the API endpoint
        response = requests.get(
            'http://localhost:8003/api/v1/mcp/tools/status', 
            timeout=5
        )
        print(f"✅ API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response: {len(data)} tool statuses retrieved")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Dynamic Tool Management API: {e}")
        return False


def test_mcp_server_direct():
    """Test MCP server with direct JSON-RPC calls."""
    print("\n=== TESTING MCP SERVER DIRECT JSON-RPC ===")
    
    try:
        # Test initialize
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
        print(f"✅ Initialize Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ MCP server is responding to JSON-RPC calls")
            
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
            print(f"✅ Tools/List Status: {response.status_code}")
            
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
                    
                    return True
                else:
                    print("❌ No tools found in response")
                    return False
            else:
                print(f"❌ Tools/List failed: {response.status_code}")
                return False
        else:
            print(f"❌ Initialize failed: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False


def test_mcp_server_health():
    """Test MCP server health endpoints."""
    print("\n=== TESTING MCP SERVER HEALTH ===")
    
    # Test various health endpoints
    endpoints = [
        "http://localhost:8000/health",
        "http://localhost:8000/mcp/health",
        "http://localhost:8003/mcp-health",
        "http://localhost:8003/mcp"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=5)
            print(f"✅ {endpoint}: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.text[:100]}")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")


def main():
    """Main test function."""
    print("🚀 Starting Failed Items Fix Test")
    print("=" * 60)
    
    # Test results
    results = {}
    
    # Test 1: Dynamic Tool Management API
    results['dynamic_tool_management'] = test_dynamic_tool_management_api()
    
    # Test 2: MCP Server Direct JSON-RPC
    results['mcp_server_direct'] = test_mcp_server_direct()
    
    # Test 3: MCP Server Health (informational)
    test_mcp_server_health()
    
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
        print("\n🎉 ALL TESTS PASSED - Failed Items Fixed!")
        print("Both MCP Tools session management and Dynamic Tool Management API are working.")
    else:
        print("\n⚠️ Some tests failed. Please check the output above for details.")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
