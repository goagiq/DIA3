#!/usr/bin/env python3
"""
Complete Thailand-Cambodia Invasion Analysis - Full DIA3 Enhanced Checklist.
Systematically going through ALL DIA3 enhanced features using proper MCP connection.
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
    from strands.tools.mcp.mcp_client import MCPClient
    from mcp.client.streamable_http import streamablehttp_client
    print("✅ MCP client available")
except ImportError as e:
    print(f"❌ MCP client import error: {e}")
    sys.exit(1)


async def execute_complete_checklist():
    """Execute the complete DIA3 enhanced analysis checklist."""
    
    print("🇹🇭🇰🇭 COMPLETE THAILAND-CAMBODIA INVASION ANALYSIS")
    print("📋 GOING THROUGH FULL DIA3 ENHANCED CHECKLIST")
    print("=" * 70)
    
    # Initialize results tracking
    results = {
        "timestamp": datetime.datetime.now().isoformat(),
        "scenario": "Thailand invading Cambodia",
        "components": {},
        "files_generated": [],
        "success": True
    }
    
    try:
        # Create MCP client with proper connection
        print("🔗 Connecting to FastMCP server...")
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            print(f"✅ Connected to FastMCP server with {len(tools)} tools")
            
            # Get tool names for proper calling
            tool_names = []
            for tool in tools:
                tool_name = tool.mcp_tool.name
                tool_names.append(tool_name)
                print(f"  📋 {tool_name}")
            
            print(f"\n🚀 Starting Complete DIA3 Enhanced Analysis...")
            print("=" * 50)
            
            # 1. CONTENT PROCESSING
            print("\n📄 1. CONTENT PROCESSING")
            print("-" * 30)
            try:
                # Use the correct tool calling method
                process_result = await mcp_client.call_tool_async(
                    "process_content",
                    {"random_string": "thailand_cambodia_invasion_comprehensive_analysis"}
                )
                results["components"]["content_processing"] = {
                    "status": "completed",
                    "result": str(process_result)
                }
                print("✅ Content processing completed")
            except Exception as e:
                results["components"]["content_processing"] = {
                    "status": "failed",
                    "error": str(e)
                }
                print(f"❌ Content processing failed: {e}")
            
            # 2. CONTENT ANALYSIS (Sentiment, Entities, Patterns)
            print("\n🧠 2. CONTENT ANALYSIS (Sentiment, Entities, Patterns)")
            print("-" * 50)
            try:
                analyze_result = await mcp_client.call_tool_async(
                    "analyze_content",
                    {"random_string": "thailand_cambodia_invasion_sentiment_analysis"}
                )
                results["components"]["content_analysis"] = {
                    "status": "completed",
                    "result": str(analyze_result)
                }
                print("✅ Content analysis (sentiment, entities, patterns) completed")
            except Exception as e:
                results["components"]["content_analysis"] = {
                    "status": "failed",
                    "error": str(e)
                }
                print(f"❌ Content analysis failed: {e}")
            
            # 3. CONTENT SEARCH (Semantic and Knowledge Graph)
            print("\n🔍 3. CONTENT SEARCH (Semantic and Knowledge Graph)")
            print("-" * 45)
            try:
                search_result = await mcp_client.call_tool_async(
                    "search_content",
                    {"random_string": "thailand_cambodia_invasion_semantic_search"}
                )
                results["components"]["content_search"] = {
                    "status": "completed",
                    "result": str(search_result)
                }
                print("✅ Content search (semantic and knowledge graph) completed")
            except Exception as e:
                results["components"]["content_search"] = {
                    "status": "failed",
                    "error": str(e)
                }
                print(f"❌ Content search failed: {e}")
            
            # 4. COMPREHENSIVE REPORT GENERATION
            print("\n📊 4. COMPREHENSIVE REPORT GENERATION")
            print("-" * 35)
            try:
                report_result = await mcp_client.call_tool_async(
                    "generate_report",
                    {"random_string": "thailand_cambodia_invasion_comprehensive_report"}
                )
                results["components"]["report_generation"] = {
                    "status": "completed",
                    "result": str(report_result)
                }
                print("✅ Comprehensive report generation completed")
            except Exception as e:
                results["components"]["report_generation"] = {
                    "status": "failed",
                    "error": str(e)
                }
                print(f"❌ Report generation failed: {e}")
            
            # 5. MONTE CARLO SIMULATIONS (Forecasting & Prediction)
            print("\n🎲 5. MONTE CARLO SIMULATIONS (Forecasting & Prediction)")
            print("-" * 45)
            try:
                simulation_result = await mcp_client.call_tool_async(
                    "run_simulation",
                    {"random_string": "thailand_cambodia_invasion_monte_carlo"}
                )
                results["components"]["monte_carlo_simulations"] = {
                    "status": "completed",
                    "result": str(simulation_result)
                }
                print("✅ Monte Carlo simulations (forecasting & prediction) completed")
            except Exception as e:
                results["components"]["monte_carlo_simulations"] = {
                    "status": "failed",
                    "error": str(e)
                }
                print(f"❌ Monte Carlo simulations failed: {e}")
            
            # 6. STRATEGIC ANALYSIS (Art of War Principles)
            print("\n⚔️ 6. STRATEGIC ANALYSIS (Art of War Principles)")
            print("-" * 40)
            try:
                strategic_result = await mcp_client.call_tool_async(
                    "analyze_strategic",
                    {"random_string": "thailand_cambodia_invasion_art_of_war"}
                )
                results["components"]["strategic_analysis"] = {
                    "status": "completed",
                    "result": str(strategic_result)
                }
                print("✅ Strategic analysis (Art of War principles) completed")
            except Exception as e:
                results["components"]["strategic_analysis"] = {
                    "status": "failed",
                    "error": str(e)
                }
                print(f"❌ Strategic analysis failed: {e}")
            
            # 7. SYSTEM PERFORMANCE MONITORING
            print("\n📊 7. SYSTEM PERFORMANCE MONITORING")
            print("-" * 35)
            try:
                system_result = await mcp_client.call_tool_async(
                    "manage_system",
                    {"random_string": "thailand_cambodia_invasion_performance_monitoring"}
                )
                results["components"]["system_monitoring"] = {
                    "status": "completed",
                    "result": str(system_result)
                }
                print("✅ System performance monitoring completed")
            except Exception as e:
                results["components"]["system_monitoring"] = {
                    "status": "failed",
                    "error": str(e)
                }
                print(f"❌ System monitoring failed: {e}")
            
            # 8. DATA EXPORT (Multiple Formats)
            print("\n📤 8. DATA EXPORT (Multiple Formats)")
            print("-" * 30)
            try:
                export_result = await mcp_client.call_tool_async(
                    "export_data",
                    {"random_string": "thailand_cambodia_invasion_data_export"}
                )
                results["components"]["data_export"] = {
                    "status": "completed",
                    "result": str(export_result)
                }
                print("✅ Data export (multiple formats) completed")
            except Exception as e:
                results["components"]["data_export"] = {
                    "status": "failed",
                    "error": str(e)
                }
                print(f"❌ Data export failed: {e}")
            
            # 9. KNOWLEDGE GRAPH OPERATIONS
            print("\n🕸️ 9. KNOWLEDGE GRAPH OPERATIONS")
            print("-" * 25)
            try:
                knowledge_result = await mcp_client.call_tool_async(
                    "knowledge_graph_operations",
                    {"random_string": "thailand_cambodia_invasion_knowledge_graph"}
                )
                results["components"]["knowledge_graph"] = {
                    "status": "completed",
                    "result": str(knowledge_result)
                }
                print("✅ Knowledge graph operations completed")
            except Exception as e:
                results["components"]["knowledge_graph"] = {
                    "status": "failed",
                    "error": str(e)
                }
                print(f"❌ Knowledge graph operations failed: {e}")
            
            # 10. AGENT MANAGEMENT
            print("\n🤖 10. AGENT MANAGEMENT")
            print("-" * 20)
            try:
                agents_result = await mcp_client.call_tool_async(
                    "manage_agents",
                    {"random_string": "thailand_cambodia_invasion_agent_coordination"}
                )
                results["components"]["agent_management"] = {
                    "status": "completed",
                    "result": str(agents_result)
                }
                print("✅ Agent management completed")
            except Exception as e:
                results["components"]["agent_management"] = {
                    "status": "failed",
                    "error": str(e)
                }
                print(f"❌ Agent management failed: {e}")
            
            # Check for generated files
            print(f"\n📁 Checking for generated files...")
            if os.path.exists("Results"):
                files = [f for f in os.listdir("Results") if "cambodia" in f.lower()]
                results["files_generated"] = files
                if files:
                    print(f"✅ Found {len(files)} generated files:")
                    for file in files:
                        filepath = os.path.join("Results", file)
                        size = os.path.getsize(filepath)
                        print(f"  📄 {file} ({size:,} bytes)")
                else:
                    print("⚠️ No Cambodia-related files found in Results/")
            else:
                print("⚠️ Results/ directory not found")
            
            # Generate summary report
            print(f"\n📋 ANALYSIS SUMMARY")
            print("=" * 30)
            completed = sum(1 for comp in results["components"].values() if comp["status"] == "completed")
            failed = sum(1 for comp in results["components"].values() if comp["status"] == "failed")
            total = len(results["components"])
            
            print(f"✅ Completed: {completed}/{total} components")
            print(f"❌ Failed: {failed}/{total} components")
            print(f"📁 Files generated: {len(results['files_generated'])}")
            
            # Save results summary
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_file = f"Results/complete_checklist_summary_{timestamp}.json"
            os.makedirs("Results", exist_ok=True)
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"📄 Summary saved to: {summary_file}")
            
            return results
            
    except Exception as e:
        print(f"❌ Error during complete checklist analysis: {e}")
        results["success"] = False
        results["error"] = str(e)
        return results


def test_mcp_connection():
    """Test MCP connection before running analysis."""
    
    try:
        print("🧪 Testing MCP connection...")
        
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            print(f"✅ Successfully connected to FastMCP server")
            print(f"📋 Found {len(tools)} tools")
            
            # List all available tools
            print("🔧 Available DIA3 tools:")
            for i, tool in enumerate(tools, 1):
                tool_name = tool.mcp_tool.name
                print(f"  {i:2d}. {tool_name}")
            
            return True
            
    except Exception as e:
        print(f"❌ Failed to connect to FastMCP server: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Complete DIA3 Enhanced Checklist Analysis")
    print("📋 Thailand-Cambodia Invasion Scenario")
    print("=" * 60)
    
    # Test connection first
    if test_mcp_connection():
        print("\n✅ MCP connection test passed")
        print("🚀 Proceeding with complete checklist analysis...")
        
        # Run the complete analysis
        results = asyncio.run(execute_complete_checklist())
        
        if results["success"]:
            print(f"\n🎉 Complete checklist analysis finished!")
            print(f"📁 Check Results/ directory for all generated reports")
            print(f"📄 Summary: {results['files_generated']}")
        else:
            print(f"\n❌ Analysis failed: {results.get('error', 'Unknown error')}")
    else:
        print(f"\n❌ MCP connection test failed")
        print("💡 Please ensure the FastMCP server is running on port 8000")
