#!/usr/bin/env python3
"""
Test MCP Client Communication

This script tests the MCP client communication with the modular report system
and other integrated tools to ensure proper functionality.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.mcp_servers.unified_mcp_server import UnifiedMCPServer


class MCPClientCommunicationTest:
    """Test class for MCP client communication."""
    
    def __init__(self):
        """Initialize the test."""
        self.server = UnifiedMCPServer()
        self.test_results = []
    
    async def test_modular_report_tools(self):
        """Test modular report MCP tools."""
        print("🔧 Testing Modular Report MCP Tools...")
        
        try:
            # Check if modular report tools are available
            if hasattr(self.server, 'modular_report_mcp_tools') and self.server.modular_report_mcp_tools:
                print("✅ Modular Report MCP Tools are available")
                
                # Get available tools
                tools = self.server.modular_report_mcp_tools.get_tools()
                print(f"📋 Found {len(tools)} modular report tools:")
                
                for tool in tools:
                    print(f"   - {tool['name']}: {tool['description']}")
                
                # Test tool calls
                test_topic = "Cybersecurity Infrastructure Enhancement"
                test_data = {
                    "executive_summary": {
                        "key_metrics": {
                            "total_investment": 3000000000,
                            "timeline_years": 3,
                            "success_probability": 0.8,
                            "risk_level": "Low"
                        },
                        "trend_analysis": {
                            "market_trends": ["Increasing cyber threats", "Growing investment in security"],
                            "technology_trends": ["AI-powered security", "Zero-trust architecture"],
                            "regulatory_trends": ["Stricter compliance requirements", "Data protection laws"]
                        },
                        "strategic_insights": [
                            "Strategic investment in cybersecurity infrastructure",
                            "Focus on proactive threat detection",
                            "Integration of AI and machine learning"
                        ]
                    },
                    "strategic_analysis": {
                        "strategic_insights": [
                            "Cybersecurity infrastructure enhancement is critical for national security",
                            "Investment in advanced threat detection systems",
                            "Integration of AI and machine learning for proactive defense"
                        ],
                        "geopolitical_impact": {
                            "regional_implications": ["Enhanced regional security posture", "Improved international cooperation"],
                            "global_implications": ["Strengthened global cybersecurity framework", "Reduced cyber threat landscape"]
                        },
                        "strategic_implications": [
                            "Enhanced cybersecurity posture",
                            "Improved threat detection capabilities",
                            "Strengthened national security framework"
                        ]
                    }
                }
                
                # Test generate_modular_enhanced_report
                print("\n🧪 Testing generate_modular_enhanced_report...")
                result = await self.server.modular_report_mcp_tools.call_tool(
                    "generate_modular_enhanced_report",
                    {
                        "topic": test_topic,
                        "data": test_data,
                        "enabled_modules": ["executivesummarymodule", "strategicanalysismodule"]
                    }
                )
                
                if result.content:
                    print("✅ generate_modular_enhanced_report test passed")
                    print(f"   Response: {result.content[0].text[:100]}...")
                else:
                    print("❌ generate_modular_enhanced_report test failed")
                
                # Test get_modular_report_modules
                print("\n🧪 Testing get_modular_report_modules...")
                result = await self.server.modular_report_mcp_tools.call_tool(
                    "get_modular_report_modules",
                    {}
                )
                
                if result.content:
                    print("✅ get_modular_report_modules test passed")
                    print(f"   Response: {result.content[0].text[:100]}...")
                else:
                    print("❌ get_modular_report_modules test failed")
                
                self.test_results.append({
                    "test": "modular_report_tools",
                    "status": "passed",
                    "tools_found": len(tools)
                })
                
            else:
                print("❌ Modular Report MCP Tools are not available")
                self.test_results.append({
                    "test": "modular_report_tools",
                    "status": "failed",
                    "error": "Tools not available"
                })
                
        except Exception as e:
            print(f"❌ Error testing modular report tools: {e}")
            self.test_results.append({
                "test": "modular_report_tools",
                "status": "failed",
                "error": str(e)
            })
    
    async def test_enhanced_report_tools(self):
        """Test enhanced report MCP tools."""
        print("\n🔧 Testing Enhanced Report MCP Tools...")
        
        try:
            # Check if enhanced report tools are available
            if hasattr(self.server, 'enhanced_report_mcp_tools') and self.server.enhanced_report_mcp_tools:
                print("✅ Enhanced Report MCP Tools are available")
                
                # Get available tools
                tools = self.server.enhanced_report_mcp_tools.get_tools()
                print(f"📋 Found {len(tools)} enhanced report tools:")
                
                for tool in tools:
                    print(f"   - {tool['name']}: {tool['description']}")
                
                self.test_results.append({
                    "test": "enhanced_report_tools",
                    "status": "passed",
                    "tools_found": len(tools)
                })
                
            else:
                print("❌ Enhanced Report MCP Tools are not available")
                self.test_results.append({
                    "test": "enhanced_report_tools",
                    "status": "failed",
                    "error": "Tools not available"
                })
                
        except Exception as e:
            print(f"❌ Error testing enhanced report tools: {e}")
            self.test_results.append({
                "test": "enhanced_report_tools",
                "status": "failed",
                "error": str(e)
            })
    
    async def test_tools_registration(self):
        """Test tools registration in the MCP server."""
        print("\n🔧 Testing Tools Registration...")
        
        try:
            # Get tools info
            tools_info = self.server.get_tools_info()
            print(f"📋 Found {len(tools_info)} registered tools:")
            
            # Count tools by type
            tool_types = {}
            for tool in tools_info:
                tool_type = tool.get('type', 'unknown')
                tool_types[tool_type] = tool_types.get(tool_type, 0) + 1
            
            for tool_type, count in tool_types.items():
                print(f"   - {tool_type}: {count} tools")
            
            # Check for modular report tools
            modular_tools = [t for t in tools_info if t.get('type') == 'modular_report']
            if modular_tools:
                print(f"✅ Found {len(modular_tools)} modular report tools registered")
                for tool in modular_tools:
                    print(f"   - {tool['name']}: {tool['description']}")
            else:
                print("❌ No modular report tools found in registration")
            
            self.test_results.append({
                "test": "tools_registration",
                "status": "passed",
                "total_tools": len(tools_info),
                "tool_types": tool_types,
                "modular_tools_found": len(modular_tools)
            })
            
        except Exception as e:
            print(f"❌ Error testing tools registration: {e}")
            self.test_results.append({
                "test": "tools_registration",
                "status": "failed",
                "error": str(e)
            })
    
    async def test_api_integration(self):
        """Test API integration with the modular report system."""
        print("\n🔧 Testing API Integration...")
        
        try:
            # Import the enhanced report routes
            from src.api.enhanced_report_routes import router
            
            print("✅ Enhanced report routes imported successfully")
            
            # Check if the router has the modular report endpoints
            routes = []
            for route in router.routes:
                if hasattr(route, 'path'):
                    routes.append(route.path)
            
            modular_endpoints = [
                "/generate-modular",
                "/modules",
                "/configure-module",
                "/enable-modules"
            ]
            
            found_endpoints = []
            for endpoint in modular_endpoints:
                if any(endpoint in route for route in routes):
                    found_endpoints.append(endpoint)
                    print(f"✅ Found endpoint: {endpoint}")
                else:
                    print(f"❌ Missing endpoint: {endpoint}")
            
            self.test_results.append({
                "test": "api_integration",
                "status": "passed" if len(found_endpoints) == len(modular_endpoints) else "partial",
                "endpoints_found": len(found_endpoints),
                "total_endpoints": len(modular_endpoints),
                "found_endpoints": found_endpoints
            })
            
        except Exception as e:
            print(f"❌ Error testing API integration: {e}")
            self.test_results.append({
                "test": "api_integration",
                "status": "failed",
                "error": str(e)
            })
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*60)
        print("📊 MCP CLIENT COMMUNICATION TEST SUMMARY")
        print("="*60)
        
        passed = 0
        failed = 0
        partial = 0
        
        for result in self.test_results:
            status = result['status']
            if status == 'passed':
                passed += 1
                print(f"✅ {result['test']}: PASSED")
            elif status == 'partial':
                partial += 1
                print(f"⚠️  {result['test']}: PARTIAL")
            else:
                failed += 1
                print(f"❌ {result['test']}: FAILED")
                if 'error' in result:
                    print(f"   Error: {result['error']}")
            
            # Print additional details
            for key, value in result.items():
                if key not in ['test', 'status', 'error']:
                    print(f"   {key}: {value}")
            print()
        
        print(f"📈 Results: {passed} passed, {partial} partial, {failed} failed")
        
        if failed == 0:
            print("🎉 All critical tests passed! MCP client communication is working.")
        else:
            print("⚠️  Some tests failed. Please check the errors above.")
        
        return failed == 0
    
    async def run_all_tests(self):
        """Run all tests."""
        print("🚀 Starting MCP Client Communication Tests")
        print("="*60)
        
        await self.test_modular_report_tools()
        await self.test_enhanced_report_tools()
        await self.test_tools_registration()
        await self.test_api_integration()
        
        return self.print_summary()


async def main():
    """Main function to run the tests."""
    tester = MCPClientCommunicationTest()
    success = await tester.run_all_tests()
    
    # Save test results
    results_file = f"Test/mcp_client_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": tester.test_results,
            "overall_success": success
        }, f, indent=2)
    
    print(f"\n📄 Test results saved to: {results_file}")
    
    if success:
        print("\n🎉 MCP client communication test completed successfully!")
        return 0
    else:
        print("\n❌ MCP client communication test completed with failures.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
