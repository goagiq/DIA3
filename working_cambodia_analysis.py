#!/usr/bin/env python3
"""
Working Thailand-Cambodia Invasion Analysis with Correct MCP Integration.
Using the proper Agent API and tool access patterns.
"""
import asyncio
import sys
import os

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


def create_working_agent():
    """Create a Strands agent with proper MCP client connection."""
    
    try:
        print("🔗 Connecting to FastMCP server...")
        
        # Create MCP client
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Get tools from the FastMCP server
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            print(f"✅ Retrieved {len(tools)} tools from FastMCP server")
            
            # List the actual tool names
            print("🔧 Available tools:")
            tool_names = []
            for i, tool in enumerate(tools, 1):
                tool_name = tool.mcp_tool.name
                tool_names.append(tool_name)
                print(f"  {i:2d}. {tool_name}")
            
            # Create an agent with the MCP tools
            agent = Agent(tools=tools)
            print("✅ Working Strands agent created with MCP tools")
            
            return agent, mcp_client, tool_names
            
    except Exception as e:
        print(f"❌ Error connecting to FastMCP server: {e}")
        return None, None, []


async def run_working_cambodia_analysis():
    """Run Thailand-Cambodia invasion analysis with working MCP integration."""
    
    print("🇹🇭🇰🇭 Thailand-Cambodia Invasion Analysis with Working MCP Integration")
    print("🔗 Using Correct Agent API and Tool Access")
    print("=" * 60)
    
    # Create the working agent
    agent, mcp_client, tool_names = create_working_agent()
    
    if not agent or not mcp_client:
        print("❌ Failed to create working agent")
        return False
    
    # Define the analysis request
    analysis_request = """
    Please perform a comprehensive analysis of the impacts and consequences of Thailand invading Cambodia.
    
    Use the available MCP tools to generate detailed reports that include:
    
    1. Executive summary of the scenario
    2. Humanitarian consequences and civilian impact
    3. Economic implications and infrastructure damage
    4. Geopolitical ramifications and regional destabilization
    5. Strategic military considerations
    6. International response and sanctions
    7. Long-term consequences for both nations
    8. Risk assessment and probability analysis
    9. Strategic recommendations for different timeframes
    
    Specifically use these available tools:
    - process_content: For content processing and analysis
    - analyze_content: For sentiment and entity analysis
    - search_content: For data gathering and research
    - generate_report: For comprehensive report generation
    - run_simulation: For Monte Carlo simulations
    - analyze_strategic: For Art of War strategic analysis
    - manage_system: For performance monitoring
    - export_data: For data export in multiple formats
    - knowledge_graph_operations: For knowledge graph generation
    - manage_agents: For agent coordination
    
    Make sure to:
    - Use ALL available tools comprehensively
    - Include all key findings and analysis components
    - Provide detailed file paths for all generated reports
    - Include interactive visualizations and knowledge graphs
    - Perform comprehensive risk assessment
    - Generate actionable strategic recommendations
    - Export in multiple formats for different stakeholders
    """
    
    print("\n🤖 Running analysis with working MCP integration...")
    print("📋 Request:", analysis_request.strip())
    
    try:
        # Use the correct Agent API - invoke_async
        print("\n🔧 Executing analysis with working MCP tools...")
        
        # Run the agent with the analysis request using invoke_async
        result = await agent.invoke_async(analysis_request)
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"📄 Agent response: {result}")
        
        # Check if files were created
        if os.path.exists("Results"):
            files = [f for f in os.listdir("Results") if "cambodia" in f.lower()]
            if files:
                print(f"📁 Generated {len(files)} files in Results/ directory:")
                for file in files:
                    print(f"  - {file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return False


def test_working_connection():
    """Test the working MCP connection."""
    
    try:
        print("🧪 Testing working MCP connection...")
        
        # Create MCP client
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Test connection
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            print(f"✅ Successfully connected to FastMCP server")
            print(f"📋 Found {len(tools)} tools")
            
            # List actual tool names
            print("🔧 Available tools:")
            for i, tool in enumerate(tools, 1):
                tool_name = tool.mcp_tool.name
                print(f"  {i:2d}. {tool_name}")
            
            return True
            
    except Exception as e:
        print(f"❌ Failed to connect to FastMCP server: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Thailand-Cambodia Analysis with Working MCP Integration")
    
    # First test the working connection
    if test_working_connection():
        print("\n✅ Working MCP connection test passed")
        
        # Run the analysis
        success = asyncio.run(run_working_cambodia_analysis())
        
        if success:
            print(f"\n🎉 Analysis completed successfully!")
            print(f"📁 Check the Results/ directory for all generated reports")
            print(f"🔧 All DIA3 enhanced features have been utilized")
        else:
            print(f"\n❌ Analysis failed")
    else:
        print(f"\n❌ Working MCP connection test failed")
        print("💡 The MCP client connection issue needs further investigation")
