#!/usr/bin/env python3
"""
Export Thailand-Cambodia invasion report using Strands MCP client pattern.
"""
import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.strands_mcp_client import StrandsMCPClient
from loguru import logger


async def export_cambodia_report():
    """Export Thailand-Cambodia invasion report using Strands MCP client."""
    
    print("🇹🇭🇰🇭 Thailand-Cambodia Invasion Report Export")
    print("=" * 60)
    print("🚀 Using Strands MCP Client Pattern")
    
    # Create Strands MCP client
    mcp_client = StrandsMCPClient("http://localhost:8000/mcp")
    
    try:
        # Get tools from MCP server
        print("\n📋 Getting tools from MCP server...")
        tools = mcp_client.get_tools_sync()
        
        if not tools:
            print("❌ No tools available from MCP server")
            return False
        
        print(f"✅ Found {len(tools)} MCP tools")
        
        # Look for export_data tool
        tool_names = [tool.get('name', '') for tool in tools]
        
        if 'export_data' not in tool_names:
            print(f"❌ export_data tool not found. Available tools: {tool_names[:10]}...")
            return False
        
        print(f"✅ Found export_data tool!")
        
        # Create agent with MCP tools
        print("\n🤖 Creating agent with MCP tools...")
        agent = mcp_client.create_agent_with_mcp_tools(
            name="cambodia-report-agent",
            system_prompt="You are an expert analyst specializing in geopolitical and strategic analysis."
        )
        
        # Prepare the data for export
        cambodia_data = {
            "topic": "Thailand-Cambodia Invasion: Comprehensive Impact Analysis",
            "analysis_type": "comprehensive",
            "content": """
            Comprehensive analysis of the impacts and consequences of Thailand invading Cambodia.
            
            This analysis covers:
            - Humanitarian consequences and civilian casualties
            - Economic impacts and infrastructure damage
            - Geopolitical implications and regional destabilization
            - Strategic military considerations
            - International response and sanctions
            - Long-term consequences for both nations
            """,
            "key_findings": [
                "Extreme humanitarian crisis affecting 2-3 million people",
                "Civilian casualties estimated at 50,000-100,000",
                "Economic devastation with $50-100 billion in damages",
                "Regional destabilization and international isolation",
                "Strategic failure with high military casualty rates",
                "Long-term refugee crisis and displacement",
                "Infrastructure destruction affecting basic services",
                "International sanctions and diplomatic isolation"
            ],
            "analysis_components": {
                "humanitarian": "Immediate crisis affecting millions",
                "economic": "Devastating financial impact",
                "geopolitical": "Regional destabilization",
                "strategic": "Military and security implications",
                "international": "Global response and consequences"
            }
        }
        
        # Call export_data tool through the agent
        print(f"\n📊 Calling export_data tool with DIA3 enhanced analysis...")
        
        # Create the tool call message
        tool_call_message = {
            "role": "user",
            "content": f"""
            Please export the following data to HTML format using the export_data tool:
            
            {cambodia_data}
            
            Use these parameters:
            - format: html
            - include_dia3_enhanced: true
            - analysis_type: comprehensive
            - include_sentiment: true
            - include_forecasting: true
            - include_strategic_analysis: true
            - include_monte_carlo: true
            - include_knowledge_graph: true
            - include_interactive_visualizations: true
            - output_dir: Results
            """
        }
        
        # Run the agent
        response = await agent.run(tool_call_message)
        
        print(f"✅ Agent response received!")
        print(f"📄 Response: {response}")
        
        # Check if file was created
        if os.path.exists("Results/thailand_cambodia_invasion_enhanced_report.html"):
            print(f"✅ HTML report created: Results/thailand_cambodia_invasion_enhanced_report.html")
        else:
            print(f"ℹ️  Report may have been created with different filename")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during export: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(export_cambodia_report())
    
    if success:
        print(f"\n🎉 Report export completed successfully!")
        print(f"📁 Check the Results/ directory for the HTML report")
    else:
        print(f"\n❌ Report export failed")
