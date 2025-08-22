#!/usr/bin/env python3
"""
Test Enhanced Report Tooltip Integration
Tests the integration of tooltip functionality with enhanced reports.
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_tooltip_report_generator():
    """Test the tooltip report generator directly."""
    print("🧪 Testing Tooltip Report Generator")
    print("=" * 50)
    
    try:
        from src.core.enhanced_report_with_tooltips import EnhancedReportWithTooltips
        
        # Create generator
        generator = EnhancedReportWithTooltips()
        print("✅ Tooltip report generator created successfully")
        
        # Test HTML generation
        html_content = generator._generate_beautiful_html_report_with_tooltips(None, 2.5)
        
        # Check for tooltip elements
        if "tooltip-modal" in html_content:
            print("✅ Tooltip modal found in HTML")
        else:
            print("❌ Tooltip modal not found in HTML")
            return False
        
        if "showTooltip" in html_content:
            print("✅ Tooltip JavaScript functions found")
        else:
            print("❌ Tooltip JavaScript functions not found")
            return False
        
        if "clickable" in html_content:
            print("✅ Clickable elements found")
        else:
            print("❌ Clickable elements not found")
            return False
        
        # Save test report
        test_file = generator.save_enhanced_report(html_content, "test_tooltip_report")
        print(f"✅ Test report saved: {test_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing tooltip report generator: {e}")
        return False

def test_mcp_tool_integration():
    """Test MCP tool integration."""
    print("\n🧪 Testing MCP Tool Integration")
    print("=" * 50)
    
    try:
        from src.mcp_servers.enhanced_report_mcp_tools import EnhancedReportMCPTools
        
        # Create MCP tools
        mcp_tools = EnhancedReportMCPTools()
        print("✅ MCP tools created successfully")
        
        # Check if tooltip generator is available
        if hasattr(mcp_tools, 'tooltip_generator') and mcp_tools.tooltip_generator:
            print("✅ Tooltip generator available in MCP tools")
        else:
            print("❌ Tooltip generator not available in MCP tools")
            return False
        
        # Get tools list
        tools = mcp_tools.get_tools()
        tool_names = [tool["name"] for tool in tools]
        
        if "generate_enhanced_report_with_tooltips" in tool_names:
            print("✅ Tooltip tool found in MCP tools list")
        else:
            print("❌ Tooltip tool not found in MCP tools list")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP tool integration: {e}")
        return False

async def test_api_integration():
    """Test API integration."""
    print("\n🧪 Testing API Integration")
    print("=" * 50)
    
    try:
        import httpx
        
        # Test the new API endpoint
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/api/v1/enhanced-reports/generate-with-tooltips",
                json={
                    "query": "Test tooltip integration",
                    "components": ["executive_summary", "predictive_analysis"]
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ API endpoint responded successfully")
                print(f"   Report ID: {result.get('report_id')}")
                print(f"   HTML File: {result.get('html_file')}")
                print(f"   Message: {result.get('message')}")
                return True
            else:
                print(f"❌ API endpoint failed with status {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing API integration: {e}")
        return False

def test_html_file_validation():
    """Test that generated HTML files contain tooltip functionality."""
    print("\n🧪 Testing HTML File Validation")
    print("=" * 50)
    
    try:
        results_dir = Path("Results")
        if not results_dir.exists():
            print("❌ Results directory not found")
            return False
        
        # Find tooltip reports
        tooltip_files = list(results_dir.glob("*tooltip*.html"))
        
        if not tooltip_files:
            print("❌ No tooltip report files found")
            return False
        
        # Test the most recent tooltip file
        latest_file = max(tooltip_files, key=lambda f: f.stat().st_mtime)
        print(f"✅ Testing file: {latest_file.name}")
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required tooltip elements
        required_elements = [
            "tooltip-modal",
            "showTooltip",
            "closeTooltip",
            "clickable",
            "feature-score",
            "table-value"
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Missing elements: {missing_elements}")
            return False
        else:
            print("✅ All required tooltip elements found")
        
        # Check for tooltip data
        if "tooltipData" in content:
            print("✅ Tooltip data found")
        else:
            print("❌ Tooltip data not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating HTML file: {e}")
        return False

async def main():
    """Run all tests."""
    print("🚀 Enhanced Report Tooltip Integration Test Suite")
    print("=" * 60)
    
    tests = [
        ("Tooltip Report Generator", test_tooltip_report_generator),
        ("MCP Tool Integration", test_mcp_tool_integration),
        ("HTML File Validation", test_html_file_validation),
    ]
    
    results = []
    
    # Run synchronous tests
    for test_name, test_func in tests[:2]:
        print(f"\n📋 Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    # Run HTML validation test
    print(f"\n📋 Running HTML File Validation...")
    result = test_html_file_validation()
    results.append(("HTML File Validation", result))
    
    # Run API test if server is available
    try:
        print(f"\n📋 Running API Integration...")
        result = await test_api_integration()
        results.append(("API Integration", result))
    except Exception as e:
        print(f"⚠️ API test skipped (server may not be running): {e}")
        results.append(("API Integration", False))
    
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
        print("🎉 All tests passed! Tooltip integration is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    asyncio.run(main())
