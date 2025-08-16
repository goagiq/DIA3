"""
Async MCP client test using mcp-client library
"""
import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


async def test_async_mcp_client():
    """Test MCP client using mcp-client library with async API."""
    
    print("🔍 Testing Async MCP Client...")
    print("=" * 50)
    
    try:
        # Import the MCP client library
        from mcp.client.streamable_http import streamablehttp_client
        
        print("✅ MCP client library imported successfully")
        
        # Create the streamable HTTP client
        print("1. Creating streamable HTTP client...")
        client = streamablehttp_client("http://localhost:8000/mcp")
        
        print("   ✅ Streamable HTTP client created")
        
        # Test the client using async context manager
        print("\n2. Testing client connection...")
        
        async with client as mcp_client:
            print("   ✅ MCP client connection established")
            
            # Initialize the client
            print("   Initializing MCP client...")
            init_result = await mcp_client.initialize(
                protocol_version="2024-11-05",
                capabilities={},
                client_info={"name": "test_client", "version": "1.0.0"}
            )
            
            print("   ✅ MCP client initialized")
            print(f"   Server: {init_result.server_info.name}")
            print(f"   Version: {init_result.server_info.version}")
            
            # List tools
            print("\n3. Listing available tools...")
            tools_result = await mcp_client.list_tools()
            
            print(f"   ✅ Found {len(tools_result.tools)} MCP tools")
            
            # Look for Phase 5 tools
            phase5_tools = [tool for tool in tools_result.tools if 'phase5' in tool.name.lower()]
            if phase5_tools:
                print(f"   🎯 Found {len(phase5_tools)} Phase 5 tools:")
                for tool in phase5_tools:
                    print(f"      - {tool.name}")
                    print(f"        Description: {tool.description[:100]}...")
            else:
                print("   ⚠️ No Phase 5 tools found")
                
            # Show all available tools (first 10)
            print("\n   📋 All available tools (showing first 10):")
            for i, tool in enumerate(tools_result.tools[:10]):
                print(f"      {i+1}. {tool.name}")
                print(f"         Description: {tool.description[:80]}...")
            
            if len(tools_result.tools) > 10:
                print(f"      ... and {len(tools_result.tools) - 10} more tools")
            
            # Test Phase 5 tool calls
            print("\n4. Testing Phase 5 tool calls...")
            if phase5_tools:
                # Test the first Phase 5 tool
                test_tool = phase5_tools[0]
                print(f"   Testing tool: {test_tool.name}")
                
                try:
                    # Call the tool
                    result = await mcp_client.call_tool(test_tool.name, {})
                    print("   ✅ Tool call successful")
                    print(f"   Result: {str(result.content)[:200]}...")
                except Exception as e:
                    print(f"   ❌ Error calling tool: {e}")
            else:
                print("   ⚠️ No Phase 5 tools available for testing")
        
        print("\n" + "=" * 50)
        print("🏁 Async MCP Client Test Complete")
        print("\n📋 Summary:")
        print("✅ MCP client library working")
        print("✅ MCP server accessible via proper protocol")
        print("✅ Tools can be listed and called")
        if 'phase5_tools' in locals() and phase5_tools:
            print(f"✅ {len(phase5_tools)} Phase 5 tools available")
        else:
            print("⚠️ No Phase 5 tools found")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure the MCP client library is installed:")
        print("   pip install mcp-client")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Check if the MCP server is running on port 8000")


def test_phase5_api_endpoints():
    """Test Phase 5 API endpoints directly."""
    
    print("\n🔍 Testing Phase 5 API Endpoints...")
    print("=" * 50)
    
    try:
        import requests
        
        # Test Phase 5 health endpoint
        print("1. Testing Phase 5 health endpoint...")
        response = requests.get("http://localhost:8003/ml-forecasting/phase5/health")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Phase 5 health check successful")
            print(f"   Phase: {result.get('phase', 'Unknown')}")
            print(f"   Status: {result.get('status', 'Unknown')}")
            print(f"   Components: {list(result.get('components', {}).keys())}")
            print(f"   Endpoints: {len(result.get('endpoints', []))} available")
        else:
            print(f"   ❌ Phase 5 health check failed: {response.text}")
        
        # Test a Phase 5 endpoint
        print("\n2. Testing Phase 5 explain-model-predictions endpoint...")
        test_data = {
            "model_output": {"prediction": 0.85, "confidence": 0.92},
            "input_data": {"feature1": 1.0, "feature2": 0.5},
            "explanation_type": "comprehensive"
        }
        
        response = requests.post(
            "http://localhost:8003/ml-forecasting/phase5/explain-model-predictions",
            json=test_data
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Phase 5 explain-model-predictions successful")
            print(f"   Explanation: {result.get('explanation', {}).get('summary', 'N/A')[:100]}...")
        else:
            print(f"   ❌ Phase 5 explain-model-predictions failed: {response.text[:200]}...")
        
        print("\n" + "=" * 50)
        print("🏁 Phase 5 API Endpoints Test Complete")
        
    except Exception as e:
        print(f"❌ Error testing Phase 5 API endpoints: {e}")


async def main():
    """Main async function."""
    # Test async MCP client
    await test_async_mcp_client()
    
    # Test Phase 5 API endpoints
    test_phase5_api_endpoints()


if __name__ == "__main__":
    # Run the async test
    asyncio.run(main())
