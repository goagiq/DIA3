#!/usr/bin/env python3
"""
Test MCP server using the proper async MCP client approach with streamable HTTP.
Based on the working Phase 1-5 implementation.
"""

import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


async def test_mcp_async_client():
    """Test MCP server using the proper async client approach."""
    print("=== TESTING MCP SERVER WITH ASYNC CLIENT ===")
    
    try:
        # Import the required modules
        from mcp.client.streamable_http import streamablehttp_client
        
        print("✅ Successfully imported streamable HTTP client")
        
        # Test the client connection using the proper async approach
        try:
            # Create the MCP client using the proper async approach
            async with streamablehttp_client("http://localhost:8000/mcp") as client:
                print("✅ Successfully connected to MCP server")
                
                # Test initialize
                result = await client.initialize({
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "1.0.0"}
                })
                print(f"✅ Initialize result: {result}")
                
                # Test list tools
                tools_result = await client.list_tools()
                print(f"✅ List tools result: {tools_result}")
                
                if 'tools' in tools_result:
                    tools = tools_result['tools']
                    print(f"✅ Retrieved {len(tools)} tools via streamable HTTP client")
                    
                    # Look for Monte Carlo tools
                    monte_carlo_tools = [
                        tool for tool in tools 
                        if 'monte_carlo' in tool.get('name', '').lower()
                    ]
                    print(f"✅ Found {len(monte_carlo_tools)} Monte Carlo tools")
                    
                    # Print tool names for verification
                    tool_names = [tool.get('name', 'unknown') for tool in tools]
                    print(f"✅ Available tools: {tool_names}")
                    
                    # Test calling a Monte Carlo tool if available
                    if monte_carlo_tools:
                        tool_name = monte_carlo_tools[0]['name']
                        print(f"\nTesting Monte Carlo tool: {tool_name}")
                        
                        # Test tool call
                        call_result = await client.call_tool(tool_name, {})
                        print(f"✅ Tool call result: {call_result}")
                    
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


def test_dynamic_tool_management():
    """Test the Dynamic Tool Management API."""
    print("\n=== TESTING DYNAMIC TOOL MANAGEMENT API ===")
    
    try:
        import requests
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


async def main():
    """Main test function."""
    print("🚀 Starting MCP Async Client Test")
    print("=" * 60)
    
    # Test results
    results = {}
    
    # Test 1: MCP Server with async client
    results['mcp_async_client'] = await test_mcp_async_client()
    
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
        print("The 'Missing session ID' issue has been resolved using proper async MCP client.")
    else:
        print("\n⚠️ Some tests failed. Please check the output above for details.")
    
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
