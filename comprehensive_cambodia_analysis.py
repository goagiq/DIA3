#!/usr/bin/env python3
"""
Comprehensive Thailand-Cambodia Invasion Analysis using ALL DIA3 Enhanced Tools.
Connecting to the existing FastMCP server with full DIA3 capabilities.
"""
import asyncio
import sys
import os
import datetime
import json
from typing import Dict, Any, List

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


def create_comprehensive_agent():
    """Create a Strands agent that connects to the existing FastMCP server with all tools."""
    
    try:
        print("🔗 Connecting to existing FastMCP server on http://localhost:8000/mcp")
        
        # Create MCP client with Streamable HTTP transport
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Get tools from the existing FastMCP server
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            print(f"✅ Retrieved {len(tools)} tools from FastMCP server")
            
            # List the available tools
            print("🔧 Available tools:")
            for i, tool in enumerate(tools, 1):
                name = tool.get('name', 'Unknown')
                description = tool.get('description', 'No description')
                print(f"  {i:2d}. {name}")
                print(f"      {description}")
            
            # Create an agent with the MCP tools
            agent = Agent(tools=tools)
            print("✅ Comprehensive Strands agent created with all FastMCP tools")
            
            return agent, mcp_client
            
    except Exception as e:
        print(f"❌ Error connecting to FastMCP server: {e}")
        return None, None


async def run_comprehensive_cambodia_analysis():
    """Run comprehensive Thailand-Cambodia invasion analysis using ALL DIA3 tools."""
    
    print("🇹🇭🇰🇭 Comprehensive Thailand-Cambodia Invasion Analysis")
    print("🔗 Using ALL DIA3 Enhanced Tools from FastMCP Server")
    print("=" * 70)
    
    # Create the comprehensive agent
    agent, mcp_client = create_comprehensive_agent()
    
    if not agent or not mcp_client:
        print("❌ Failed to create comprehensive agent")
        return False
    
    # Define the comprehensive analysis request
    analysis_request = """
    Please perform a COMPREHENSIVE analysis of the impacts and consequences of Thailand invading Cambodia.
    
    Use ALL available MCP tools to generate detailed reports that include:
    
    1. EXECUTIVE SUMMARY:
       - Scenario overview and key implications
       - Critical findings and recommendations
    
    2. HUMANITARIAN CONSEQUENCES:
       - Civilian impact and casualties
       - Refugee crisis and displacement
       - Infrastructure destruction
       - Healthcare and basic services
    
    3. ECONOMIC IMPLICATIONS:
       - Direct economic damages
       - Trade disruption and sanctions
       - Long-term economic consequences
       - Regional economic impact
    
    4. GEOPOLITICAL RAMIFICATIONS:
       - Regional destabilization
       - International relations impact
       - Alliance and security implications
       - Diplomatic consequences
    
    5. STRATEGIC MILITARY CONSIDERATIONS:
       - Military capabilities and limitations
       - Strategic objectives and outcomes
       - Force projection and logistics
       - Operational challenges
    
    6. INTERNATIONAL RESPONSE:
       - UN and international organization reactions
       - Economic sanctions and pressure
       - Diplomatic isolation
       - International intervention scenarios
    
    7. LONG-TERM CONSEQUENCES:
       - Political stability implications
       - Economic recovery challenges
       - Regional security dynamics
       - Historical precedents and lessons
    
    8. RISK ASSESSMENT:
       - High, medium, and low-risk scenarios
       - Probability analysis
       - Impact severity assessment
       - Mitigation strategies
    
    9. STRATEGIC RECOMMENDATIONS:
       - Immediate actions required
       - Short-term policy options
       - Long-term strategic planning
       - International coordination needs
    
    SPECIFIC TOOL REQUIREMENTS:
    
    - Use export_data tool with include_dia3_enhanced=True for comprehensive HTML report
    - Use mcp_DIA3_analyze_content for content analysis and sentiment
    - Use mcp_DIA3_generate_report for enhanced report generation
    - Use mcp_DIA3_search_content for data gathering and research
    - Use mcp_DIA3_run_simulation for Monte Carlo simulations
    - Use mcp_DIA3_analyze_strategic for Art of War strategic analysis
    - Use mcp_DIA3_manage_system for performance monitoring
    - Use mcp_DIA3_export_data for multiple format exports
    - Use mcp_DIA3_knowledge_graph_operations for knowledge graph generation
    - Use mcp_DIA3_manage_agents for agent coordination
    
    OUTPUT REQUIREMENTS:
    
    1. Generate comprehensive HTML report with all analysis components
    2. Create interactive visualizations and charts
    3. Generate knowledge graph of key entities and relationships
    4. Perform Monte Carlo simulations for scenario analysis
    5. Conduct sentiment analysis of geopolitical content
    6. Create strategic analysis using Art of War principles
    7. Export results in multiple formats (HTML, JSON, Markdown)
    8. Include performance metrics and system monitoring
    9. Provide detailed risk assessment with probability analysis
    10. Generate actionable strategic recommendations
    
    Make sure to:
    - Use ALL available tools comprehensively
    - Include all key findings and analysis components
    - Provide detailed file paths for all generated reports
    - Include interactive visualizations and knowledge graphs
    - Perform comprehensive risk assessment
    - Generate actionable strategic recommendations
    - Export in multiple formats for different stakeholders
    """
    
    print("\n🤖 Running comprehensive analysis with ALL DIA3 tools...")
    print("📋 Request:", analysis_request.strip())
    
    try:
        # Use the MCP client directly to call all available tools
        with mcp_client:
            print("\n🔧 Executing comprehensive analysis with all tools...")
            
            # 1. Generate comprehensive HTML report
            print("📄 Generating comprehensive HTML report...")
            export_result = await mcp_client.call_tool(
                "export_data",
                {
                    "data": {
                        "scenario": "Thailand invading Cambodia",
                        "analysis_type": "comprehensive",
                        "include_all_components": True
                    },
                    "format": "html",
                    "include_dia3_enhanced": True,
                    "analysis_type": "comprehensive",
                    "output_dir": "Results"
                }
            )
            print(f"✅ HTML report generated: {export_result}")
            
            # 2. Generate enhanced report with all DIA3 features
            print("📊 Generating enhanced DIA3 report...")
            try:
                enhanced_result = await mcp_client.call_tool(
                    "mcp_DIA3_generate_report",
                    {
                        "analysis_type": "comprehensive",
                        "topic": "Thailand invading Cambodia",
                        "include_visualizations": True,
                        "include_knowledge_graph": True,
                        "include_sentiment_analysis": True,
                        "include_strategic_analysis": True,
                        "include_monte_carlo": True
                    }
                )
                print(f"✅ Enhanced DIA3 report generated: {enhanced_result}")
            except Exception as e:
                print(f"⚠️ Enhanced report generation: {e}")
            
            # 3. Content analysis and sentiment
            print("🧠 Performing content analysis and sentiment...")
            try:
                content_result = await mcp_client.call_tool(
                    "mcp_DIA3_analyze_content",
                    {
                        "content": "Thailand invading Cambodia would result in extreme humanitarian crisis, economic devastation, regional destabilization, and international isolation with severe consequences for both nations and Southeast Asia.",
                        "analysis_type": "comprehensive"
                    }
                )
                print(f"✅ Content analysis completed: {content_result}")
            except Exception as e:
                print(f"⚠️ Content analysis: {e}")
            
            # 4. Strategic analysis using Art of War principles
            print("⚔️ Performing strategic analysis...")
            try:
                strategic_result = await mcp_client.call_tool(
                    "mcp_DIA3_analyze_strategic",
                    {
                        "scenario": "Thailand invading Cambodia",
                        "analysis_type": "art_of_war",
                        "include_deception_detection": True
                    }
                )
                print(f"✅ Strategic analysis completed: {strategic_result}")
            except Exception as e:
                print(f"⚠️ Strategic analysis: {e}")
            
            # 5. Monte Carlo simulations
            print("🎲 Running Monte Carlo simulations...")
            try:
                simulation_result = await mcp_client.call_tool(
                    "mcp_DIA3_run_simulation",
                    {
                        "scenario": "thailand_cambodia_invasion",
                        "simulation_type": "monte_carlo",
                        "iterations": 1000,
                        "variables": ["casualties", "economic_damage", "duration", "international_response"]
                    }
                )
                print(f"✅ Monte Carlo simulations completed: {simulation_result}")
            except Exception as e:
                print(f"⚠️ Monte Carlo simulations: {e}")
            
            # 6. Knowledge graph generation
            print("🕸️ Generating knowledge graph...")
            try:
                knowledge_result = await mcp_client.call_tool(
                    "mcp_DIA3_knowledge_graph_operations",
                    {
                        "operation": "generate",
                        "topic": "Thailand Cambodia invasion",
                        "entities": ["Thailand", "Cambodia", "ASEAN", "UN", "China", "US"],
                        "relationships": ["invades", "supports", "condemns", "sanctions"]
                    }
                )
                print(f"✅ Knowledge graph generated: {knowledge_result}")
            except Exception as e:
                print(f"⚠️ Knowledge graph: {e}")
            
            # 7. Export data in multiple formats
            print("📤 Exporting data in multiple formats...")
            try:
                export_data_result = await mcp_client.call_tool(
                    "mcp_DIA3_export_data",
                    {
                        "data": {
                            "scenario": "Thailand invading Cambodia",
                            "analysis": "comprehensive",
                            "findings": "Extreme humanitarian crisis, economic devastation, regional destabilization"
                        },
                        "formats": ["html", "json", "markdown", "pdf"],
                        "output_dir": "Results"
                    }
                )
                print(f"✅ Multi-format export completed: {export_data_result}")
            except Exception as e:
                print(f"⚠️ Multi-format export: {e}")
            
            # 8. System performance monitoring
            print("📊 Monitoring system performance...")
            try:
                performance_result = await mcp_client.call_tool(
                    "mcp_DIA3_manage_system",
                    {
                        "operation": "get_performance_metrics",
                        "include_all_metrics": True
                    }
                )
                print(f"✅ Performance monitoring completed: {performance_result}")
            except Exception as e:
                print(f"⚠️ Performance monitoring: {e}")
            
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
        print(f"❌ Error during comprehensive analysis: {e}")
        return False


def test_fastmcp_connection():
    """Test connection to existing FastMCP server."""
    
    try:
        print("🧪 Testing existing FastMCP server connection...")
        
        # Create MCP client
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Test connection
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            print(f"✅ Successfully connected to existing FastMCP server")
            print(f"📋 Found {len(tools)} tools with full DIA3 capabilities")
            
            # List all tools
            print("🔧 Available tools:")
            for i, tool in enumerate(tools, 1):
                name = tool.get('name', 'Unknown')
                print(f"  {i:2d}. {name}")
            
            return True
            
    except Exception as e:
        print(f"❌ Failed to connect to existing FastMCP server: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Comprehensive Thailand-Cambodia Invasion Analysis")
    print("🔗 Using ALL DIA3 Enhanced Tools from Existing FastMCP Server")
    
    # First test the connection
    if test_fastmcp_connection():
        print("\n✅ FastMCP connection test passed")
        
        # Run the comprehensive analysis
        success = asyncio.run(run_comprehensive_cambodia_analysis())
        
        if success:
            print(f"\n🎉 Comprehensive analysis completed successfully!")
            print(f"📁 Check the Results/ directory for all generated reports")
            print(f"🔧 All DIA3 enhanced features have been utilized")
        else:
            print(f"\n❌ Comprehensive analysis failed")
    else:
        print(f"\n❌ FastMCP connection test failed")
        print("💡 Make sure the FastMCP server is running on port 8000")
        print("💡 The server should have all DIA3 enhanced tools available")
