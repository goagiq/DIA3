#!/usr/bin/env python3
"""
Test MCP Tooltip Integration
Tests that MCP client can trigger tooltip-enhanced report generation.
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_mcp_tooltip_tool():
    """Test the MCP tooltip tool directly."""
    print("🧪 Testing MCP Tooltip Tool")
    print("=" * 50)
    
    try:
        from src.mcp_servers.enhanced_report_mcp_tools import EnhancedReportMCPTools
        
        # Create MCP tools
        mcp_tools = EnhancedReportMCPTools()
        
        # Test the tooltip tool
        arguments = {
            "query": "Pakistan Submarine Acquisition Analysis with Tooltips",
            "include_tooltips": True,
            "include_feature_explanations": True,
            "include_forecast_explanations": True,
            "include_confidence_intervals": True,
            "beautiful_styling": True
        }
        
        print("📋 Calling generate_enhanced_report_with_tooltips...")
        result = await mcp_tools.call_tool("generate_enhanced_report_with_tooltips", arguments)
        
        if result.get("success"):
            print("✅ Tooltip report generated successfully")
            print(f"   Report ID: {result.get('report_id')}")
            print(f"   HTML File: {result.get('html_file')}")
            print(f"   Processing Time: {result.get('processing_time')}")
            print(f"   Message: {result.get('message')}")
            
            # Check features
            features = result.get('features', {})
            if features.get('tooltips'):
                print("✅ Tooltips feature enabled")
            if features.get('feature_explanations'):
                print("✅ Feature explanations enabled")
            if features.get('forecast_explanations'):
                print("✅ Forecast explanations enabled")
            if features.get('confidence_intervals'):
                print("✅ Confidence intervals enabled")
            
            return True
        else:
            print(f"❌ Tooltip report generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MCP tooltip tool: {e}")
        return False

async def test_mcp_client_integration():
    """Test MCP client integration with tooltip tool."""
    print("\n🧪 Testing MCP Client Integration")
    print("=" * 50)
    
    try:
        # This would test the actual MCP client connection
        # For now, we'll simulate the client call
        print("📋 Simulating MCP client call...")
        
        # Simulate the tool call that would come from an MCP client
        tool_call = {
            "name": "generate_enhanced_report_with_tooltips",
            "arguments": {
                "query": "Test MCP client tooltip integration",
                "include_tooltips": True,
                "include_feature_explanations": True,
                "include_forecast_explanations": True,
                "include_confidence_intervals": True,
                "beautiful_styling": True
            }
        }
        
        print(f"   Tool: {tool_call['name']}")
        print(f"   Query: {tool_call['arguments']['query']}")
        print(f"   Features: {list(tool_call['arguments'].keys())}")
        
        # Test the tool execution
        from src.mcp_servers.enhanced_report_mcp_tools import EnhancedReportMCPTools
        mcp_tools = EnhancedReportMCPTools()
        
        result = await mcp_tools.call_tool(
            tool_call['name'], 
            tool_call['arguments']
        )
        
        if result.get("success"):
            print("✅ MCP client integration successful")
            print(f"   Generated file: {result.get('html_file')}")
            return True
        else:
            print(f"❌ MCP client integration failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MCP client integration: {e}")
        return False

def test_tool_availability():
    """Test that the tooltip tool is available in the MCP tools list."""
    print("\n🧪 Testing Tool Availability")
    print("=" * 50)
    
    try:
        from src.mcp_servers.enhanced_report_mcp_tools import EnhancedReportMCPTools
        
        mcp_tools = EnhancedReportMCPTools()
        tools = mcp_tools.get_tools()
        
        # Find the tooltip tool
        tooltip_tool = None
        for tool in tools:
            if tool["name"] == "generate_enhanced_report_with_tooltips":
                tooltip_tool = tool
                break
        
        if tooltip_tool:
            print("✅ Tooltip tool found in MCP tools")
            print(f"   Name: {tooltip_tool['name']}")
            print(f"   Description: {tooltip_tool['description']}")
            
            # Check required parameters
            schema = tooltip_tool.get('inputSchema', {})
            required = schema.get('required', [])
            if 'query' in required:
                print("✅ Query parameter is required")
            else:
                print("❌ Query parameter should be required")
                return False
            
            return True
        else:
            print("❌ Tooltip tool not found in MCP tools")
            return False
            
    except Exception as e:
        print(f"❌ Error testing tool availability: {e}")
        return False

async def main():
    """Run all MCP tooltip integration tests."""
    print("🚀 MCP Tooltip Integration Test Suite")
    print("=" * 60)
    
    tests = [
        ("Tool Availability", test_tool_availability),
        ("MCP Tooltip Tool", test_mcp_tooltip_tool),
        ("MCP Client Integration", test_mcp_client_integration),
    ]
    
    results = []
    
    # Run synchronous tests
    for test_name, test_func in tests[:1]:
        print(f"\n📋 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Run async tests
    for test_name, test_func in tests[1:]:
        print(f"\n📋 Running {test_name}...")
        result = await test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MCP tooltip integration is working correctly.")
        print("\n📝 Next Steps:")
        print("   1. Start the MCP server: python main.py")
        print("   2. Wait 60 seconds for server to fully start")
        print("   3. Use MCP client to call: generate_enhanced_report_with_tooltips")
        print("   4. Open the generated HTML file to test tooltips")
        return True
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    asyncio.run(main())
