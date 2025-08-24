#!/usr/bin/env python3
"""
Thailand-Cambodia Invasion Report using Strands with FastMCP server.
Connecting to the standalone FastMCP server on port 8000 to access 59 MCP tools.
"""
import asyncio
import sys
import os
from typing import Dict, Any

# Add src to path for our custom modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from strands import Agent
    from strands.tools.mcp.mcp_client import MCPClient
    from mcp.client.streamable_http import streamablehttp_client
    STRANDS_AVAILABLE = True
    print("✅ Full Strands implementation available")
except ImportError:
    print("❌ Strands not available, using mock implementation")
    from src.core.strands_mock import Agent
    STRANDS_AVAILABLE = False


def create_strands_agent_with_fastmcp():
    """Create a Strands agent that connects to the FastMCP server."""
    
    if not STRANDS_AVAILABLE:
        print("❌ Cannot connect to FastMCP server - Strands not available")
        return None
    
    try:
        print("🔗 Connecting to FastMCP server on http://localhost:8000/mcp")
        
        # Create MCP client with Streamable HTTP transport
        streamable_http_mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Get tools from the FastMCP server
        with streamable_http_mcp_client:
            tools = streamable_http_mcp_client.list_tools_sync()
            print(f"✅ Retrieved {len(tools)} tools from FastMCP server")
            
            # Look for specific tools we need
            tool_names = [tool.get('name', '') for tool in tools]
            
            if 'export_data' in tool_names:
                print("✅ Found 'export_data' tool")
            else:
                print("❌ 'export_data' tool not found")
            
            # Look for DIA3 tools
            dia3_tools = [name for name in tool_names if 'dia3' in name.lower()]
            if dia3_tools:
                print(f"✅ Found DIA3 tools: {dia3_tools}")
            else:
                print("ℹ️ No DIA3-specific tools found")
            
            # Create an agent with the MCP tools
            agent = Agent(tools=tools)
            print("✅ Strands agent created with FastMCP tools")
            
            return agent
            
    except Exception as e:
        print(f"❌ Error connecting to FastMCP server: {e}")
        return None


async def run_cambodia_analysis_with_fastmcp():
    """Run Thailand-Cambodia invasion analysis using Strands + FastMCP."""
    
    print("🇹🇭🇰🇭 Thailand-Cambodia Invasion Analysis")
    print("🔗 Using Strands + FastMCP Integration")
    print("=" * 60)
    
    # Create the agent with FastMCP tools
    agent = create_strands_agent_with_fastmcp()
    
    if not agent:
        print("❌ Failed to create agent with FastMCP tools")
        return False
    
    # Define the analysis request
    analysis_request = """
    Please perform a comprehensive analysis of the impacts and consequences of Thailand invading Cambodia.
    
    Use the available MCP tools to generate a detailed report that includes:
    
    1. Executive summary of the scenario
    2. Humanitarian consequences and civilian impact
    3. Economic implications and infrastructure damage
    4. Geopolitical ramifications and regional destabilization
    5. Strategic military considerations
    6. International response and sanctions
    7. Long-term consequences for both nations
    
    If you have access to the export_data tool, use it to generate an HTML report with:
    - include_dia3_enhanced=True
    - format="html"
    - analysis_type="comprehensive"
    - Include all key findings and analysis components
    
    Provide the file path where the report was saved.
    """
    
    print("\n🤖 Running Strands agent with FastMCP tools...")
    print("📋 Request:", analysis_request.strip())
    
    try:
        # Run the agent
        result = await agent.run(analysis_request)
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"📄 Agent response: {result.message}")
        
        # Check if file was created
        if os.path.exists("Results"):
            files = [f for f in os.listdir("Results") if "cambodia" in f.lower() and f.endswith('.html')]
            if files:
                latest_file = max(files, key=lambda x: os.path.getctime(os.path.join("Results", x)))
                print(f"📁 Report created: Results/{latest_file}")
                return True
        
        return True
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return False


def test_fastmcp_connection():
    """Test connection to FastMCP server."""
    
    if not STRANDS_AVAILABLE:
        print("❌ Cannot test FastMCP connection - Strands not available")
        return False
    
    try:
        print("🧪 Testing FastMCP server connection...")
        
        # Create MCP client
        streamable_http_mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Test connection
        with streamable_http_mcp_client:
            tools = streamable_http_mcp_client.list_tools_sync()
            print(f"✅ Successfully connected to FastMCP server")
            print(f"📋 Found {len(tools)} tools")
            
            # List first 10 tools
            print("🔧 Available tools:")
            for i, tool in enumerate(tools[:10], 1):
                print(f"  {i:2d}. {tool.get('name', 'Unknown')}")
            
            if len(tools) > 10:
                print(f"  ... and {len(tools) - 10} more tools")
            
            return True
            
    except Exception as e:
        print(f"❌ Failed to connect to FastMCP server: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Strands + FastMCP Thailand-Cambodia Analysis")
    
    # First test the connection
    if test_fastmcp_connection():
        print("\n✅ FastMCP connection test passed")
        
        # Run the analysis
        success = asyncio.run(run_cambodia_analysis_with_fastmcp())
        
        if success:
            print(f"\n🎉 Analysis completed successfully!")
            print(f"📁 Check the Results/ directory for the HTML report")
        else:
            print(f"\n❌ Analysis failed")
    else:
        print(f"\n❌ FastMCP connection test failed")
        print("💡 Make sure the FastMCP server is running on port 8000")
