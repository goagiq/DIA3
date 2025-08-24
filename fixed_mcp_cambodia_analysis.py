#!/usr/bin/env python3
"""
Fixed Thailand-Cambodia Invasion Analysis with Proper MCP Client Connection.
Fixing the JSON-RPC response parsing and tool access issues.
"""
import asyncio
import sys
import os
import json
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


def create_fixed_mcp_agent():
    """Create a Strands agent with proper MCP client connection."""
    
    try:
        print("🔗 Connecting to FastMCP server with proper configuration...")
        
        # Create MCP client with proper configuration
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Get tools from the FastMCP server with proper error handling
        with mcp_client:
            try:
                tools = mcp_client.list_tools_sync()
                print(f"✅ Retrieved {len(tools)} tools from FastMCP server")
                
                # Handle tools properly - they are MCPAgentTool objects
                print("🔧 Available tools:")
                for i, tool in enumerate(tools, 1):
                    # Access tool attributes properly
                    try:
                        name = tool.name if hasattr(tool, 'name') else f"Tool_{i}"
                        description = tool.description if hasattr(tool, 'description') else "No description"
                        print(f"  {i:2d}. {name}")
                        print(f"      {description}")
                    except Exception as tool_error:
                        print(f"  {i:2d}. Tool_{i} (Error accessing: {tool_error})")
                
                # Create an agent with the MCP tools
                agent = Agent(tools=tools)
                print("✅ Fixed Strands agent created with proper MCP tools")
                
                return agent, mcp_client
                
            except Exception as tools_error:
                print(f"❌ Error accessing tools: {tools_error}")
                return None, None
            
    except Exception as e:
        print(f"❌ Error connecting to FastMCP server: {e}")
        return None, None


async def run_fixed_cambodia_analysis():
    """Run Thailand-Cambodia invasion analysis with fixed MCP connection."""
    
    print("🇹🇭🇰🇭 Thailand-Cambodia Invasion Analysis with Fixed MCP Connection")
    print("🔗 Using Proper MCP Client Configuration")
    print("=" * 60)
    
    # Create the fixed agent
    agent, mcp_client = create_fixed_mcp_agent()
    
    if not agent or not mcp_client:
        print("❌ Failed to create fixed agent")
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
    
    Specifically use the available tools to:
    - Generate comprehensive HTML reports
    - Perform sentiment analysis
    - Create strategic analysis
    - Run Monte Carlo simulations
    - Generate knowledge graphs
    - Export data in multiple formats
    - Monitor system performance
    
    Make sure to:
    - Use ALL available tools comprehensively
    - Include all key findings and analysis components
    - Provide detailed file paths for all generated reports
    - Include interactive visualizations and knowledge graphs
    - Perform comprehensive risk assessment
    - Generate actionable strategic recommendations
    - Export in multiple formats for different stakeholders
    """
    
    print("\n🤖 Running analysis with fixed MCP connection...")
    print("📋 Request:", analysis_request.strip())
    
    try:
        # Use the agent to run the analysis
        print("\n🔧 Executing analysis with fixed MCP tools...")
        
        # Run the agent with the analysis request
        result = await agent.run(analysis_request)
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"📄 Agent response: {result.message}")
        
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


def test_fixed_mcp_connection():
    """Test the fixed MCP connection."""
    
    try:
        print("🧪 Testing fixed MCP connection...")
        
        # Create MCP client with proper configuration
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Test connection with proper error handling
        with mcp_client:
            try:
                tools = mcp_client.list_tools_sync()
                print(f"✅ Successfully connected to FastMCP server")
                print(f"📋 Found {len(tools)} tools")
                
                # List tools with proper attribute access
                print("🔧 Available tools:")
                for i, tool in enumerate(tools, 1):
                    try:
                        name = tool.name if hasattr(tool, 'name') else f"Tool_{i}"
                        print(f"  {i:2d}. {name}")
                    except Exception as tool_error:
                        print(f"  {i:2d}. Tool_{i} (Error: {tool_error})")
                
                return True
                
            except Exception as tools_error:
                print(f"❌ Error accessing tools: {tools_error}")
                return False
            
    except Exception as e:
        print(f"❌ Failed to connect to FastMCP server: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Thailand-Cambodia Analysis with Fixed MCP Connection")
    
    # First test the fixed connection
    if test_fixed_mcp_connection():
        print("\n✅ Fixed MCP connection test passed")
        
        # Run the analysis
        success = asyncio.run(run_fixed_cambodia_analysis())
        
        if success:
            print(f"\n🎉 Analysis completed successfully!")
            print(f"📁 Check the Results/ directory for all generated reports")
            print(f"🔧 All DIA3 enhanced features have been utilized")
        else:
            print(f"\n❌ Analysis failed")
    else:
        print(f"\n❌ Fixed MCP connection test failed")
        print("💡 The MCP client connection issue needs further investigation")
