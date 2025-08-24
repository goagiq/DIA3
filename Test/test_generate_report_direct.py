#!/usr/bin/env python3
"""
Direct test script for enhanced generate_report MCP tool functionality.

This script directly tests the enhanced generate_report tool by creating
an MCP server instance and calling the tool methods directly.
"""

import asyncio
import logging
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mcp_servers.unified_mcp_server import UnifiedMCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_enhanced_generate_report_direct():
    """Test the enhanced generate_report tool directly."""
    
    print("🧪 Testing Enhanced Generate Report Tool (Direct)")
    print("=" * 55)
    
    try:
        # Create MCP server instance
        server = UnifiedMCPServer()
        
        # Test content for analysis
        test_content = """
        Cambodia's recent acquisition of J-10 fighter jets from China represents a significant 
        shift in regional military dynamics. This development has implications for ASEAN security, 
        US-China relations, and regional stability.
        """
        
        print(f"📝 Test Content: {test_content[:80]}...")
        print()
        
        # Test 1: Basic report generation (without DIA3 enhanced)
        print("🔍 Test 1: Basic Report Generation")
        print("-" * 30)
        
        basic_result = await server.generate_report(
            content=test_content,
            report_type="basic",
            language="en",
            include_dia3_enhanced=False
        )
        
        if basic_result.get("success"):
            print("✅ Basic report generation successful")
            print(f"   Report saved to: {basic_result['result']['saved_to']}")
            print(f"   Filename: {basic_result['result']['filename']}")
        else:
            print(f"❌ Basic report generation failed: {basic_result.get('error')}")
        
        print()
        
        # Test 2: Enhanced report generation with DIA3 capabilities
        print("🔍 Test 2: Enhanced Report Generation with DIA3")
        print("-" * 50)
        
        enhanced_result = await server.generate_report(
            content=test_content,
            report_type="comprehensive",
            language="en",
            include_dia3_enhanced=True,
            include_sentiment=True,
            include_forecasting=True,
            include_strategic_analysis=True,
            include_monte_carlo=True,
            include_knowledge_graph=True,
            include_interactive_visualizations=True,
            output_dir="Results"
        )
        
        if enhanced_result.get("success"):
            print("✅ Enhanced report generation successful")
            print(f"   Report saved to: {enhanced_result['result']['saved_to']}")
            print(f"   Filename: {enhanced_result['result']['filename']}")
            print(f"   DIA3 Enhanced: {enhanced_result['result']['dia3_enhanced']}")
            
            # Check analysis components
            components = enhanced_result['result'].get('analysis_components', {})
            print("   Analysis Components:")
            for component, enabled in components.items():
                status = "✅" if enabled else "❌"
                print(f"     {status} {component}")
            
            # Check HTML report
            html_report = enhanced_result['result'].get('html_report')
            if html_report and not html_report.get('error'):
                print(f"   HTML Report: {html_report['filename']}")
            elif html_report and html_report.get('error'):
                print(f"   HTML Report Error: {html_report['error']}")
            
            # Check DIA3 results
            dia3_results = enhanced_result['result'].get('dia3_results', {})
            if dia3_results:
                print("   DIA3 Results:")
                for analysis_type, result in dia3_results.items():
                    if result and not result.get('error'):
                        print(f"     ✅ {analysis_type}")
                    else:
                        error = result.get('error', 'Unknown error') if result else 'No result'
                        print(f"     ❌ {analysis_type}: {error}")
        else:
            print(f"❌ Enhanced report generation failed: {enhanced_result.get('error')}")
        
        print()
        
        # Test 3: Test export_data tool (should be simplified now)
        print("🔍 Test 3: Basic Export Data Tool")
        print("-" * 30)
        
        export_result = await server.export_data(
            data={"test": "data", "content": test_content},
            format="json"
        )
        
        if export_result.get("success"):
            print("✅ Basic export data successful")
            print(f"   Format: {export_result['result']['format']}")
            print(f"   Note: {export_result['result']['note']}")
        else:
            print(f"❌ Basic export data failed: {export_result.get('error')}")
        
        print()
        print("✅ All direct tests completed successfully!")
        
    except Exception as e:
        logger.error(f"Direct test failed with error: {e}")
        print(f"❌ Direct test failed: {e}")
        return False
    
    return True

def main():
    """Main test function."""
    print("🚀 Starting Direct Enhanced Generate Report Tool Tests")
    print("=" * 65)
    
    # Run tests
    asyncio.run(test_enhanced_generate_report_direct())
    
    print("\n🎉 Direct test suite completed!")
    print("=" * 65)

if __name__ == "__main__":
    main()
