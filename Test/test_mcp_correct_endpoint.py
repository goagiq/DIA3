#!/usr/bin/env python3
"""
Test MCP server at the correct endpoint based on the working Phase 1-4 implementation.
"""

import sys
import os
import requests

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_mcp_server_correct_endpoint():
    """Test the MCP server at the correct endpoint (/mcp)."""
    print("=== TESTING MCP SERVER AT CORRECT ENDPOINT ===")
    
    try:
        # Test if the MCP server is responding at the correct endpoint
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
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        print(f"✅ Initialize Status: {response.status_code}")
        
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
                    
                    # Print tool names for verification
                    tool_names = [tool.get('name', 'unknown') for tool in tools]
                    print(f"✅ Available tools: {tool_names}")
                    
                    return True
                else:
                    print("❌ No tools found in response")
                    print(f"Response: {data}")
                    return False
            else:
                print(f"❌ Tools/List failed: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False
        else:
            print(f"❌ Initialize failed: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False


def test_mcp_client_sample():
    """Test using the MCP client sample code provided by the user."""
    print("\n=== TESTING MCP CLIENT SAMPLE CODE ===")
    
    try:
        # Import the required modules
        from mcp.client.streamable_http import streamablehttp_client
        
        print("✅ Successfully imported streamable HTTP client")
        
        # Test the client connection
        try:
            with streamablehttp_client("http://localhost:8000/mcp") as client:
                print("✅ Successfully connected to MCP server")
                
                # Test initialize
                result = client.initialize({
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "1.0.0"}
                })
                print(f"✅ Initialize result: {result}")
                
                # Test list tools
                tools_result = client.list_tools()
                print(f"✅ List tools result: {tools_result}")
                
                if 'tools' in tools_result:
                    tools = tools_result['tools']
                    print(f"✅ Retrieved {len(tools)} tools via streamable HTTP client")
                    
                    # Look for Monte Carlo tools
                    monte_carlo_tools = [
                        tool for tool in tools 
                        if 'monte_carlo' in tool.get('name', '').lower()
                    ]
                    print(f"✅ Found {len(monte_carlo_tools)} Monte Carlo tools via client")
                    
                    return True
                else:
                    print("❌ No tools found in client response")
                    return False
                    
        except Exception as e:
            print(f"❌ Error with streamable HTTP client: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing MCP client: {e}")
        return False


def main():
    """Main test function."""
    print("🚀 Starting MCP Server Correct Endpoint Test")
    print("=" * 60)
    
    # Test results
    results = {}
    
    # Test 1: MCP Server at correct endpoint
    results['mcp_server_correct_endpoint'] = test_mcp_server_correct_endpoint()
    
    # Test 2: MCP Client sample code
    results['mcp_client_sample'] = test_mcp_client_sample()
    
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
        print("\n🎉 ALL TESTS PASSED - MCP Server Issue Resolved!")
        print("The MCP server is working correctly at the /mcp endpoint.")
        print("Both JSON-RPC calls and streamable HTTP client are working.")
    else:
        print("\n⚠️ Some tests failed. Please check the output above for details.")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
