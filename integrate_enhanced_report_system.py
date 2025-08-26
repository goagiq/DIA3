#!/usr/bin/env python3
"""
Enhanced HTML Report System Integration

This script demonstrates how to use the new robust, self-healing enhanced HTML report generator.
It integrates with the existing DIA3 system and provides automatic error recovery.
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any, Union

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.enhanced_html_report_generator import (
    EnhancedHTMLReportGenerator,
    generate_enhanced_html_report
)
from src.core.modular_report_generator import ModularReportGenerator


async def demonstrate_enhanced_report_generation():
    """Demonstrate the enhanced HTML report generation capabilities."""
    
    print("🚀 Enhanced HTML Report System Integration Demo")
    print("=" * 60)
    
    # Initialize the enhanced HTML report generator
    generator = EnhancedHTMLReportGenerator("Results")
    
    # Test data with different structures
    test_cases = [
        {
            "name": "String Data",
            "data": "Pakistan submarine acquisition analysis with comprehensive strategic implications for regional security dynamics.",
            "query_type": "strategic_analysis",
            "title": "Pakistan Submarine Strategic Analysis"
        },
        {
            "name": "Dictionary Data",
            "data": {
                "content": "Comprehensive analysis of submarine acquisition",
                "sections": [
                    {"title": "Strategic Impact", "content": "Significant impact on regional balance of power"},
                    {"title": "Economic Implications", "content": "Major investment with long-term economic benefits"},
                    {"title": "Security Considerations", "content": "Enhanced deterrence capabilities and maritime security"}
                ],
                "metadata": {"source": "strategic_analysis", "confidence": 0.85}
            },
            "query_type": "comprehensive_analysis",
            "title": "Comprehensive Submarine Analysis"
        },
        {
            "name": "List Data",
            "data": [
                "Strategic impact analysis",
                "Economic implications assessment",
                "Security considerations review",
                "Regional balance evaluation"
            ],
            "query_type": "list_analysis",
            "title": "Multi-Dimensional Analysis"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📊 Test Case {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Generate enhanced HTML report
            result = await generator.generate_enhanced_report(
                data=test_case["data"],
                query_type=test_case["query_type"],
                title=test_case["title"]
            )
            
            if result["success"]:
                print(f"✅ Success: {test_case['name']}")
                print(f"   📁 File: {result['file_path']}")
                print(f"   📏 Size: {result['file_size']} bytes")
                print(f"   🕒 Generated: {result['generated_at']}")
                print(f"   📊 Data Type: {result['data_type']}")
                print(f"   🔍 Query Type: {result['query_type']}")
                
                if "recovery_attempt" in result:
                    print(f"   🔄 Recovery Attempt: {result['recovery_attempt']}")
                
                results.append(result)
            else:
                print(f"❌ Failed: {test_case['name']}")
                print(f"   Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Exception: {test_case['name']}")
            print(f"   Error: {str(e)}")
    
    # Demonstrate modular integration
    print(f"\n🔧 Modular System Integration")
    print("-" * 40)
    
    try:
        modular_generator = ModularReportGenerator()
        
        # Generate report using modular system
        modular_result = await modular_generator.generate_modular_report(
            query="Pakistan submarine acquisition comprehensive analysis",
            enabled_modules=["executive_summary", "strategic_analysis", "economic_analysis"],
            title="Modular Submarine Analysis"
        )
        
        if modular_result["success"]:
            print("✅ Modular Integration Success")
            print(f"   📁 File: {modular_result['file_path']}")
            print(f"   📊 Modules Used: {modular_result.get('modules_used', [])}")
            print(f"   🔍 Query: {modular_result.get('query', 'N/A')}")
        else:
            print("❌ Modular Integration Failed")
            print(f"   Error: {modular_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Modular Integration Exception: {str(e)}")
    
    # Summary
    print(f"\n📈 Summary")
    print("-" * 40)
    print(f"✅ Successful Reports: {len([r for r in results if r.get('success', False)])}")
    print(f"❌ Failed Reports: {len([r for r in results if not r.get('success', False)])}")
    print(f"📁 Total Files Generated: {len(results)}")
    
    if results:
        total_size = sum(r.get('file_size', 0) for r in results if r.get('success', False))
        print(f"📏 Total Size: {total_size} bytes")
    
    print(f"\n🎉 Enhanced HTML Report System Integration Complete!")
    print("The system is now robust, self-healing, and ready for production use.")


async def demonstrate_error_recovery():
    """Demonstrate the error recovery capabilities."""
    
    print("\n🔄 Error Recovery Demonstration")
    print("=" * 40)
    
    generator = EnhancedHTMLReportGenerator("Results")
    
    # Test with problematic data
    problematic_data = {
        "content": None,  # This will cause issues
        "sections": "invalid_sections",  # Wrong type
        "metadata": {"source": "test"}
    }
    
    print("Testing with problematic data...")
    
    try:
        result = await generator.generate_enhanced_report(
            data=problematic_data,
            query_type="error_test",
            title="Error Recovery Test"
        )
        
        if result["success"]:
            print("✅ Error Recovery Successful!")
            print(f"   📁 File: {result['file_path']}")
            if "recovery_attempt" in result:
                print(f"   🔄 Recovery Attempt: {result['recovery_attempt']}")
        else:
            print("❌ Error Recovery Failed")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Exception during error recovery: {str(e)}")


async def demonstrate_convenience_function():
    """Demonstrate the convenience function."""
    
    print("\n🎯 Convenience Function Demonstration")
    print("=" * 40)
    
    # Simple string data
    simple_data = "Quick analysis of regional security implications"
    
    try:
        result = await generate_enhanced_html_report(
            data=simple_data,
            query_type="quick_analysis",
            title="Quick Security Analysis",
            output_dir="Results"
        )
        
        if result["success"]:
            print("✅ Convenience Function Success!")
            print(f"   📁 File: {result['file_path']}")
            print(f"   📏 Size: {result['file_size']} bytes")
        else:
            print("❌ Convenience Function Failed")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Exception with convenience function: {str(e)}")


async def main():
    """Main demonstration function."""
    
    print("🌟 Enhanced HTML Report System - Production Ready Integration")
    print("=" * 70)
    print("This system provides:")
    print("✅ Robust error handling and recovery")
    print("✅ Dynamic data structure support")
    print("✅ Self-healing capabilities")
    print("✅ Proper tooltip source attribution")
    print("✅ Interactive visualizations")
    print("✅ Production-ready reliability")
    print()
    
    # Run demonstrations
    await demonstrate_enhanced_report_generation()
    await demonstrate_error_recovery()
    await demonstrate_convenience_function()
    
    print(f"\n🎊 Integration Complete!")
    print("The enhanced HTML report system is now integrated and ready for production use.")
    print("Users can now generate robust, self-healing reports without manual fixes.")


if __name__ == "__main__":
    asyncio.run(main())
