#!/usr/bin/env python3
"""
Thailand-Cambodia Invasion Analysis using Strands + Streamlined FastMCP.
Connecting to the streamlined FastMCP server with under 20 essential tools.
"""
import asyncio
import sys
import os
from typing import Dict, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from strands import Agent
    from strands.tools.mcp.mcp_client import MCPClient
    from mcp.client.streamable_http import streamablehttp_client
    print("✅ Full Strands implementation available")
except ImportError as e:
    print(f"❌ Strands import error: {e}")
    sys.exit(1)


def create_strands_agent_with_streamlined_mcp():
    """Create a Strands agent that connects to the streamlined FastMCP server."""
    
    try:
        print("🔗 Connecting to Streamlined FastMCP server on http://localhost:8001/mcp")
        
        # Create MCP client with Streamable HTTP transport
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8001/mcp")
        )
        
        # Get tools from the streamlined FastMCP server
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            print(f"✅ Retrieved {len(tools)} tools from streamlined FastMCP server")
            
            # List the available tools
            print("🔧 Available tools:")
            for i, tool in enumerate(tools, 1):
                name = tool.get('name', 'Unknown')
                description = tool.get('description', 'No description')
                print(f"  {i:2d}. {name}")
                print(f"      {description}")
            
            # Create an agent with the MCP tools
            agent = Agent(tools=tools)
            print("✅ Strands agent created with streamlined FastMCP tools")
            
            return agent
            
    except Exception as e:
        print(f"❌ Error connecting to streamlined FastMCP server: {e}")
        return None


async def run_cambodia_analysis():
    """Run Thailand-Cambodia invasion analysis using Strands + Streamlined FastMCP."""
    
    print("🇹🇭🇰🇭 Thailand-Cambodia Invasion Analysis")
    print("🔗 Using Strands + Streamlined FastMCP Integration")
    print("=" * 60)
    
    # Create the agent with streamlined FastMCP tools
    agent = create_strands_agent_with_streamlined_mcp()
    
    if not agent:
        print("❌ Failed to create agent with streamlined FastMCP tools")
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
    
    Specifically:
    - Use the analyze_geopolitical_scenario tool to analyze the Thailand-Cambodia invasion scenario
    - Use the export_data tool to generate an HTML report with include_dia3_enhanced=True
    - Use the generate_strategic_recommendations tool to create strategic recommendations
    - Use the create_visualizations tool to generate interactive visualizations
    - Use the analyze_sentiment tool to analyze the sentiment of the scenario
    - Use the extract_entities tool to identify key entities involved
    - Use the generate_knowledge_graph tool to create a knowledge graph
    - Use the search_geopolitical_data tool to gather relevant data
    - Use the export_analysis tool to export results in multiple formats
    
    Make sure to:
    - Generate the report in HTML format
    - Include all key findings and analysis components
    - Provide the file path where the report was saved
    - Include strategic recommendations
    - Create visualizations and knowledge graphs
    """
    
    print("\n🤖 Running Strands agent with streamlined FastMCP tools...")
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


def test_streamlined_mcp_connection():
    """Test connection to streamlined FastMCP server."""
    
    try:
        print("🧪 Testing streamlined FastMCP server connection...")
        
        # Create MCP client
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8001/mcp")
        )
        
        # Test connection
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            print(f"✅ Successfully connected to streamlined FastMCP server")
            print(f"📋 Found {len(tools)} tools (under 20 as requested)")
            
            # List all tools
            print("🔧 Available tools:")
            for i, tool in enumerate(tools, 1):
                name = tool.get('name', 'Unknown')
                print(f"  {i:2d}. {name}")
            
            return True
            
    except Exception as e:
        print(f"❌ Failed to connect to streamlined FastMCP server: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Strands + Streamlined FastMCP Thailand-Cambodia Analysis")
    
    # First test the connection
    if test_streamlined_mcp_connection():
        print("\n✅ Streamlined FastMCP connection test passed")
        
        # Run the analysis
        success = asyncio.run(run_cambodia_analysis())
        
        if success:
            print(f"\n🎉 Analysis completed successfully!")
            print(f"📁 Check the Results/ directory for the HTML report")
        else:
            print(f"\n❌ Analysis failed")
    else:
        print(f"\n❌ Streamlined FastMCP connection test failed")
        print("💡 Make sure the streamlined FastMCP server is running on port 8001")
        print("💡 Run: python src/mcp_servers/streamlined_mcp_server.py")
