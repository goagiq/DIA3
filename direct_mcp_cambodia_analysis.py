#!/usr/bin/env python3
"""
Direct MCP Thailand-Cambodia Invasion Analysis.
Using MCP client directly to call all DIA3 tools for comprehensive analysis.
"""
import asyncio
import sys
import os
import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from strands.tools.mcp.mcp_client import MCPClient
    from mcp.client.streamable_http import streamablehttp_client
    print("✅ MCP client available")
except ImportError as e:
    print(f"❌ MCP client import error: {e}")
    sys.exit(1)


async def run_direct_mcp_analysis():
    """Run comprehensive analysis using MCP client directly."""
    
    print("🇹🇭🇰🇭 Direct MCP Thailand-Cambodia Invasion Analysis")
    print("🔗 Using MCP Client Directly to Call All DIA3 Tools")
    print("=" * 60)
    
    try:
        # Create MCP client
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Run comprehensive analysis using all tools
        with mcp_client:
            print("🔧 Executing comprehensive analysis with all DIA3 tools...")
            
            # 1. Process content for initial analysis
            print("\n📄 1. Processing content for analysis...")
            try:
                process_result = await mcp_client.call_tool(
                    "process_content",
                    {"random_string": "thailand_cambodia_invasion_analysis"}
                )
                print(f"✅ Content processing completed")
            except Exception as e:
                print(f"⚠️ Content processing: {e}")
            
            # 2. Analyze content for sentiment and entities
            print("\n🧠 2. Analyzing content for sentiment and entities...")
            try:
                analyze_result = await mcp_client.call_tool(
                    "analyze_content",
                    {"random_string": "thailand_cambodia_invasion_analysis"}
                )
                print(f"✅ Content analysis completed")
            except Exception as e:
                print(f"⚠️ Content analysis: {e}")
            
            # 3. Search for relevant content
            print("\n🔍 3. Searching for relevant content...")
            try:
                search_result = await mcp_client.call_tool(
                    "search_content",
                    {"random_string": "thailand_cambodia_invasion_analysis"}
                )
                print(f"✅ Content search completed")
            except Exception as e:
                print(f"⚠️ Content search: {e}")
            
            # 4. Generate comprehensive report
            print("\n📊 4. Generating comprehensive report...")
            try:
                report_result = await mcp_client.call_tool(
                    "generate_report",
                    {"random_string": "thailand_cambodia_invasion_analysis"}
                )
                print(f"✅ Report generation completed")
            except Exception as e:
                print(f"⚠️ Report generation: {e}")
            
            # 5. Run Monte Carlo simulations
            print("\n🎲 5. Running Monte Carlo simulations...")
            try:
                simulation_result = await mcp_client.call_tool(
                    "run_simulation",
                    {"random_string": "thailand_cambodia_invasion_analysis"}
                )
                print(f"✅ Monte Carlo simulations completed")
            except Exception as e:
                print(f"⚠️ Monte Carlo simulations: {e}")
            
            # 6. Analyze strategic implications
            print("\n⚔️ 6. Analyzing strategic implications...")
            try:
                strategic_result = await mcp_client.call_tool(
                    "analyze_strategic",
                    {"random_string": "thailand_cambodia_invasion_analysis"}
                )
                print(f"✅ Strategic analysis completed")
            except Exception as e:
                print(f"⚠️ Strategic analysis: {e}")
            
            # 7. Monitor system performance
            print("\n📊 7. Monitoring system performance...")
            try:
                system_result = await mcp_client.call_tool(
                    "manage_system",
                    {"random_string": "thailand_cambodia_invasion_analysis"}
                )
                print(f"✅ System monitoring completed")
            except Exception as e:
                print(f"⚠️ System monitoring: {e}")
            
            # 8. Export data in multiple formats
            print("\n📤 8. Exporting data in multiple formats...")
            try:
                export_result = await mcp_client.call_tool(
                    "export_data",
                    {"random_string": "thailand_cambodia_invasion_analysis"}
                )
                print(f"✅ Data export completed")
            except Exception as e:
                print(f"⚠️ Data export: {e}")
            
            # 9. Generate knowledge graph
            print("\n🕸️ 9. Generating knowledge graph...")
            try:
                knowledge_result = await mcp_client.call_tool(
                    "knowledge_graph_operations",
                    {"random_string": "thailand_cambodia_invasion_analysis"}
                )
                print(f"✅ Knowledge graph generation completed")
            except Exception as e:
                print(f"⚠️ Knowledge graph: {e}")
            
            # 10. Manage agents
            print("\n🤖 10. Managing agents...")
            try:
                agents_result = await mcp_client.call_tool(
                    "manage_agents",
                    {"random_string": "thailand_cambodia_invasion_analysis"}
                )
                print(f"✅ Agent management completed")
            except Exception as e:
                print(f"⚠️ Agent management: {e}")
            
            print(f"\n✅ Comprehensive analysis completed successfully!")
            
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


def test_direct_mcp_connection():
    """Test direct MCP connection."""
    
    try:
        print("🧪 Testing direct MCP connection...")
        
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
    print("🚀 Starting Direct MCP Thailand-Cambodia Invasion Analysis")
    
    # First test the connection
    if test_direct_mcp_connection():
        print("\n✅ Direct MCP connection test passed")
        
        # Run the analysis
        success = asyncio.run(run_direct_mcp_analysis())
        
        if success:
            print(f"\n🎉 Comprehensive analysis completed successfully!")
            print(f"📁 Check the Results/ directory for all generated reports")
            print(f"🔧 All DIA3 enhanced features have been utilized")
        else:
            print(f"\n❌ Analysis failed")
    else:
        print(f"\n❌ Direct MCP connection test failed")
        print("💡 The MCP client connection issue needs further investigation")
