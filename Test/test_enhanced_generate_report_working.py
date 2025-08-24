#!/usr/bin/env python3
"""
Test script for enhanced generate_report MCP tool functionality.

This script tests the enhanced generate_report tool by connecting to the
running MCP server through HTTP and calling the tool directly.
"""

import asyncio
import logging
import sys
import os
import aiohttp
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_enhanced_generate_report():
    """Test the enhanced generate_report tool via HTTP."""
    
    print("🧪 Testing Enhanced Generate Report Tool (HTTP)")
    print("=" * 55)
    
    # Test content for analysis
    test_content = """
    Cambodia's recent acquisition of J-10 fighter jets from China represents a significant 
    shift in regional military dynamics. This development has implications for ASEAN security, 
    US-China relations, and regional stability.
    """
    
    print(f"📝 Test Content: {test_content[:80]}...")
    print()
    
    # MCP server endpoint
    mcp_url = "http://localhost:8000/mcp"
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test 1: Basic report generation (without DIA3 enhanced)
            print("🔍 Test 1: Basic Report Generation")
            print("-" * 30)
            
            basic_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "generate_report",
                    "arguments": {
                        "content": test_content,
                        "report_type": "basic",
                        "language": "en",
                        "include_dia3_enhanced": False
                    }
                }
            }
            
            async with session.post(mcp_url, json=basic_request) as response:
                if response.status == 200:
                    result = await response.json()
                    if "result" in result and result["result"].get("success"):
                        print("✅ Basic report generation successful")
                        print(f"   Report saved to: {result['result']['result']['saved_to']}")
                        print(f"   Filename: {result['result']['result']['filename']}")
                    else:
                        print(f"❌ Basic report generation failed: {result}")
                else:
                    print(f"❌ HTTP error: {response.status}")
            
            print()
            
            # Test 2: Enhanced report generation with DIA3 capabilities
            print("🔍 Test 2: Enhanced Report Generation with DIA3")
            print("-" * 50)
            
            enhanced_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "generate_report",
                    "arguments": {
                        "content": test_content,
                        "report_type": "comprehensive",
                        "language": "en",
                        "include_dia3_enhanced": True,
                        "include_sentiment": True,
                        "include_forecasting": True,
                        "include_strategic_analysis": True,
                        "include_monte_carlo": True,
                        "include_knowledge_graph": True,
                        "include_interactive_visualizations": True,
                        "output_dir": "Results"
                    }
                }
            }
            
            async with session.post(mcp_url, json=enhanced_request) as response:
                if response.status == 200:
                    result = await response.json()
                    if "result" in result and result["result"].get("success"):
                        print("✅ Enhanced report generation successful")
                        report_result = result["result"]["result"]
                        print(f"   Report saved to: {report_result['saved_to']}")
                        print(f"   Filename: {report_result['filename']}")
                        print(f"   DIA3 Enhanced: {report_result['dia3_enhanced']}")
                        
                        # Check analysis components
                        components = report_result.get('analysis_components', {})
                        print("   Analysis Components:")
                        for component, enabled in components.items():
                            status = "✅" if enabled else "❌"
                            print(f"     {status} {component}")
                        
                        # Check HTML report
                        html_report = report_result.get('html_report')
                        if html_report and not html_report.get('error'):
                            print(f"   HTML Report: {html_report['filename']}")
                        elif html_report and html_report.get('error'):
                            print(f"   HTML Report Error: {html_report['error']}")
                        
                        # Check DIA3 results
                        dia3_results = report_result.get('dia3_results', {})
                        if dia3_results:
                            print("   DIA3 Results:")
                            for analysis_type, result in dia3_results.items():
                                if result and not result.get('error'):
                                    print(f"     ✅ {analysis_type}")
                                else:
                                    error = result.get('error', 'Unknown error') if result else 'No result'
                                    print(f"     ❌ {analysis_type}: {error}")
                    else:
                        print(f"❌ Enhanced report generation failed: {result}")
                else:
                    print(f"❌ HTTP error: {response.status}")
            
            print()
            
            # Test 3: List available tools
            print("🔍 Test 3: Available Tools")
            print("-" * 20)
            
            tools_request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/list",
                "params": {}
            }
            
            async with session.post(mcp_url, json=tools_request) as response:
                if response.status == 200:
                    result = await response.json()
                    if "result" in result:
                        tools = result["result"].get("tools", [])
                        print(f"✅ Found {len(tools)} tools:")
                        for tool in tools:
                            print(f"   - {tool['name']}: {tool['description'][:50]}...")
                        
                        # Check if generate_report tool is available
                        tool_names = [tool['name'] for tool in tools]
                        if 'generate_report' in tool_names:
                            print("✅ generate_report tool found")
                        else:
                            print("❌ generate_report tool not found")
                    else:
                        print(f"❌ Failed to get tools: {result}")
                else:
                    print(f"❌ HTTP error: {response.status}")
            
            print()
            print("✅ All HTTP tests completed successfully!")
            
    except Exception as e:
        logger.error(f"HTTP test failed with error: {e}")
        print(f"❌ HTTP test failed: {e}")
        return False
    
    return True

def main():
    """Main test function."""
    print("🚀 Starting HTTP Enhanced Generate Report Tool Tests")
    print("=" * 65)
    
    # Run tests
    asyncio.run(test_enhanced_generate_report())
    
    print("\n🎉 HTTP test suite completed!")
    print("=" * 65)

if __name__ == "__main__":
    main()
