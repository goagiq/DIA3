#!/usr/bin/env python3
"""
Simple Strands test following the official documentation.
Testing connection to FastMCP server.
"""
import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from strands import Agent, tool
    from strands_tools import calculator, current_time, python_repl
    print("✅ Full Strands implementation available")
except ImportError as e:
    print(f"❌ Strands import error: {e}")
    sys.exit(1)


@tool
def test_cambodia_analysis() -> str:
    """Test function for Cambodia analysis."""
    return "Thailand-Cambodia invasion analysis test completed successfully!"


def create_basic_agent():
    """Create a basic Strands agent following the documentation."""
    
    # Create an agent with basic tools
    agent = Agent(
        tools=[calculator, current_time, python_repl, test_cambodia_analysis],
        system_prompt="You are a helpful assistant that can perform calculations, get time, run Python code, and analyze geopolitical scenarios."
    )
    
    return agent


async def test_basic_functionality():
    """Test basic Strands functionality."""
    
    print("🧪 Testing basic Strands functionality...")
    
    agent = create_basic_agent()
    
    # Test basic functionality
    test_message = """
    I have 3 requests:
    
    1. What is the current time?
    2. Calculate 25 * 48
    3. Run a test for Cambodia analysis
    """
    
    try:
        result = await agent.run(test_message)
        print(f"✅ Basic test completed successfully!")
        print(f"📄 Result: {result.message}")
        return True
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False


async def test_mcp_connection():
    """Test MCP connection using Strands."""
    
    print("\n🔗 Testing MCP connection with Strands...")
    
    try:
        from strands.tools.mcp.mcp_client import MCPClient
        from mcp.client.streamable_http import streamablehttp_client
        
        # Create MCP client
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Test connection
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            print(f"✅ Successfully connected to FastMCP server")
            print(f"📋 Found {len(tools)} tools")
            
            # List first 5 tools
            print("🔧 First 5 tools:")
            for i, tool in enumerate(tools[:5], 1):
                print(f"  {i}. {tool.get('name', 'Unknown')}")
            
            return True
            
    except Exception as e:
        print(f"❌ MCP connection failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Strands Tests")
    print("=" * 40)
    
    # Test basic functionality
    basic_success = asyncio.run(test_basic_functionality())
    
    # Test MCP connection
    mcp_success = asyncio.run(test_mcp_connection())
    
    if basic_success and mcp_success:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed")
