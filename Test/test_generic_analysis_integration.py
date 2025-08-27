#!/usr/bin/env python3
"""
Test: Generic Comprehensive Analysis System Integration
Tests the integration of the generic analysis system into the main codebase and MCP tools.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from loguru import logger

# Import the integrated components
from core.generic_comprehensive_analysis import GenericComprehensiveAnalysisSystem
from mcp_servers.standalone_mcp_server import StandaloneMCPServer


async def test_generic_analysis_system():
    """Test the standalone generic comprehensive analysis system."""
    print("🧪 Testing Generic Comprehensive Analysis System")
    print("=" * 60)
    
    try:
        # Initialize the system
        analyzer = GenericComprehensiveAnalysisSystem()
        print("✅ Generic Comprehensive Analysis System initialized")
        
        # Test with a strategic topic
        topic = "China-Taiwan relations"
        print(f"\n📊 Testing analysis for: {topic}")
        
        result = await analyzer.analyze_topic(topic, "comprehensive")
        
        if result["success"]:
            print("✅ Analysis completed successfully!")
            print(f"📄 Reports generated:")
            for report_type, path in result["report_paths"].items():
                print(f"   - {report_type}: {path}")
            
            print(f"\n📋 Analysis Summary:")
            print(f"   - Topic: {result['topic']}")
            print(f"   - Analysis Type: {result['analysis_type']}")
            print(f"   - Categories Determined: {len(result['relevant_categories'])}")
            print(f"   - Research Areas: {len(result['research_results'])}")
            
            print(f"\n🎯 Sample Relevant Categories:")
            for i, category in enumerate(result['relevant_categories'][:5], 1):
                print(f"   {i}. {category}")
            
            return True
        else:
            print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


async def test_mcp_server_integration():
    """Test the MCP server integration with the generic analysis system."""
    print("\n🧪 Testing MCP Server Integration")
    print("=" * 60)
    
    try:
        # Initialize the MCP server
        server = StandaloneMCPServer()
        print("✅ MCP Server initialized with generic analysis system")
        
        # Test the generic analysis tool through MCP
        topic = "Russia-Ukraine conflict escalation"
        print(f"\n📊 Testing MCP tool for: {topic}")
        
        # Simulate the MCP tool call
        result = await server.generic_analysis_system.analyze_topic(topic, "comprehensive")
        
        if result["success"]:
            print("✅ MCP integration test completed successfully!")
            print(f"📄 Reports generated:")
            for report_type, path in result["report_paths"].items():
                print(f"   - {report_type}: {path}")
            
            return True
        else:
            print(f"❌ MCP integration test failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ MCP integration test failed with error: {e}")
        return False


async def test_multiple_topics():
    """Test the system with multiple strategic topics."""
    print("\n🧪 Testing Multiple Strategic Topics")
    print("=" * 60)
    
    topics = [
        "Iran nuclear program",
        "North Korea missile development",
        "Cyber warfare capabilities",
        "Space militarization"
    ]
    
    analyzer = GenericComprehensiveAnalysisSystem()
    success_count = 0
    
    for topic in topics:
        print(f"\n📊 Testing: {topic}")
        try:
            result = await analyzer.analyze_topic(topic, "comprehensive")
            if result["success"]:
                print(f"✅ Success: {len(result['relevant_categories'])} categories determined")
                success_count += 1
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n📊 Multiple Topics Test Results:")
    print(f"   - Total topics tested: {len(topics)}")
    print(f"   - Successful analyses: {success_count}")
    print(f"   - Success rate: {(success_count/len(topics)*100):.1f}%")
    
    return success_count == len(topics)


async def main():
    """Main test function."""
    print("🎯 Generic Comprehensive Analysis System Integration Test")
    print("=" * 80)
    print("This test verifies the integration of the generic analysis system")
    print("into the main codebase and MCP tools.")
    print()
    
    # Test 1: Standalone system
    test1_success = await test_generic_analysis_system()
    
    # Test 2: MCP server integration
    test2_success = await test_mcp_server_integration()
    
    # Test 3: Multiple topics
    test3_success = await test_multiple_topics()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 INTEGRATION TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Standalone System Test: {'PASSED' if test1_success else 'FAILED'}")
    print(f"✅ MCP Server Integration Test: {'PASSED' if test2_success else 'FAILED'}")
    print(f"✅ Multiple Topics Test: {'PASSED' if test3_success else 'FAILED'}")
    
    overall_success = test1_success and test2_success and test3_success
    print(f"\n🎯 Overall Integration Status: {'✅ SUCCESS' if overall_success else '❌ FAILED'}")
    
    if overall_success:
        print("\n🎉 All integration tests passed!")
        print("The generic comprehensive analysis system is successfully integrated")
        print("into the main codebase and MCP tools.")
    else:
        print("\n⚠️ Some integration tests failed.")
        print("Please check the error messages above for details.")
    
    return overall_success


if __name__ == "__main__":
    # Run the integration tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1)





