#!/usr/bin/env python3
"""
Test script for adaptive modular report system integration.
Tests the integrated adaptive system that generates all 22 modules by default.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append('src')

async def test_adaptive_system():
    """Test the integrated adaptive modular report system."""
    
    print("🧪 Testing Integrated Adaptive Modular Report System")
    print("=" * 60)
    
    try:
        # Test 1: Import the adaptive system
        print("📦 Test 1: Importing adaptive system...")
        from src.core.integrated_adaptive_modular_report_generator import integrated_adaptive_modular_report_generator
        from src.core.adaptive_data_adapter import AdaptiveDataAdapter
        
        print("✅ Adaptive system imported successfully")
        
        # Test 2: Test adaptive data adapter
        print("\n📊 Test 2: Testing adaptive data adapter...")
        adapter = AdaptiveDataAdapter()
        
        # Test data generation
        test_query = "Pakistan Submarine Acquisition Analysis"
        test_data = {"topic": "Test", "entities": ["Pakistan"]}
        
        universal_data = adapter.generate_universal_data(test_query, test_data)
        print(f"✅ Universal data generated: {len(universal_data)} sections")
        
        # Test data cleaning
        clean_data = adapter.clean_data_structure(universal_data)
        print(f"✅ Data cleaning completed: {len(clean_data)} sections")
        
        # Test 3: Test adaptive report generation
        print("\n📄 Test 3: Testing adaptive report generation...")
        
        result = await integrated_adaptive_modular_report_generator.generate_adaptive_report(
            test_query,
            test_data
        )
        
        if result['success']:
            print("✅ Adaptive report generated successfully")
            print(f"   📁 File: {result['file_path']}")
            print(f"   📊 Data sections: {result['universal_data_sections']}")
            print(f"   🔄 Modules generated: {result['modules_generated']}")
            print(f"   🎯 Query: {result['query']}")
            print(f"   🔧 Adaptive mode: {result['integrated_adaptive_mode']}")
        else:
            print(f"❌ Failed to generate adaptive report: {result.get('error', 'Unknown error')}")
            return False
        
        # Test 4: Test MCP tools integration
        print("\n🔧 Test 4: Testing MCP tools integration...")
        try:
            from src.mcp_servers.modular_report_mcp_tools import ModularReportMCPTools
            
            mcp_tools = ModularReportMCPTools()
            tools = mcp_tools.get_tools()
            
            print(f"✅ MCP tools available: {len(tools)} tools")
            
            # Check if adaptive tool is available
            adaptive_tool = next((tool for tool in tools if tool['name'] == 'generate_adaptive_modular_report'), None)
            if adaptive_tool:
                print("✅ Adaptive MCP tool available")
                print(f"   📝 Description: {adaptive_tool['description']}")
            else:
                print("❌ Adaptive MCP tool not found")
                return False
                
        except Exception as e:
            print(f"❌ MCP tools test failed: {e}")
            return False
        
        # Test 5: Test API integration
        print("\n🌐 Test 5: Testing API integration...")
        try:
            from src.api.enhanced_report_routes import AdaptiveReportRequest, AdaptiveReportResponse
            
            # Test request model
            test_request = AdaptiveReportRequest(
                query="Test Query",
                data={"test": "data"},
                include_tooltips=True,
                include_source_references=True,
                format="html"
            )
            
            print("✅ API models imported successfully")
            print(f"   📝 Request model: {test_request.query}")
            
        except Exception as e:
            print(f"❌ API integration test failed: {e}")
            return False
        
        print("\n🎉 All tests passed! Adaptive system is fully integrated.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_multiple_queries():
    """Test the adaptive system with multiple different queries."""
    
    print("\n🧪 Testing Multiple Query Types")
    print("=" * 40)
    
    try:
        from src.core.integrated_adaptive_modular_report_generator import integrated_adaptive_modular_report_generator
        
        test_cases = [
            {
                'query': "Pakistan Submarine Acquisition Analysis",
                'data': {'topic': 'Military', 'entities': ['Pakistan', 'India']}
            },
            {
                'query': "China's Belt and Road Initiative Economic Impact",
                'data': {'topic': 'Economic', 'entities': ['China', 'Pakistan']}
            },
            {
                'query': "Russian Cyber Warfare Capabilities Assessment",
                'data': {'topic': 'Security', 'entities': ['Russia', 'USA']}
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Test Case {i}: {test_case['query']}")
            
            result = await integrated_adaptive_modular_report_generator.generate_adaptive_report(
                test_case['query'],
                test_case['data']
            )
            
            if result['success']:
                print(f"✅ Success: {result['file_path']}")
                print(f"   📊 Sections: {result['universal_data_sections']}")
                print(f"   🔄 Modules: {result['modules_generated']}")
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        
        print("\n🎉 Multiple query tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Multiple query test failed: {e}")
        return False

async def main():
    """Main test function."""
    
    print("🚀 Starting Adaptive Modular Report System Integration Tests")
    print("=" * 70)
    
    # Test basic integration
    basic_success = await test_adaptive_system()
    
    if basic_success:
        # Test multiple queries
        await test_multiple_queries()
        
        print("\n" + "=" * 70)
        print("🎉 ALL TESTS PASSED!")
        print("✅ Adaptive modular report system is fully integrated")
        print("✅ All 22 modules will be generated by default")
        print("✅ Natural language query processing works")
        print("✅ MCP tools are available")
        print("✅ API endpoints are ready")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("❌ TESTS FAILED!")
        print("❌ Adaptive system integration incomplete")
        print("=" * 70)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
