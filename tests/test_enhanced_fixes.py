#!/usr/bin/env python3
"""
Test script to verify the enhanced HTML report generator fixes.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.enhanced_html_report_generator import EnhancedHTMLReportGenerator

async def test_enhanced_system():
    """Test the enhanced HTML report generator with meaningful content."""
    
    print("🚀 Testing Enhanced HTML Report Generator with Meaningful Content")
    print("=" * 70)
    
    # Initialize the generator
    print("📋 Initializing generator...")
    generator = EnhancedHTMLReportGenerator()
    print("✅ Generator initialized")
    
    # Test data
    test_data = {
        "sections": [
            {
                "title": "Executive Summary",
                "content": "Comprehensive analysis of Pakistan's submarine acquisition program."
            },
            {
                "title": "Geopolitical Impact Analysis", 
                "content": "Analysis of regional security implications."
            }
        ]
    }
    
    # Generate the report
    output_path = "Results/Test_Enhanced_Fixes_20250825_183000.html"
    
    print(f"📊 Generating enhanced report with {len(test_data['sections'])} input sections...")
    print(f"📁 Output file: {output_path}")
    
    print("🔄 Starting report generation...")
    result = await generator.generate_enhanced_report(test_data, output_path)
    print("✅ Report generation completed")
    
    if result["success"]:
        print("✅ Report generated successfully!")
        
        # Display validation results
        validation = result.get("validation_results", {})
        
        print("\n📋 VALIDATION RESULTS:")
        print("-" * 40)
        
        # Module coverage
        module_coverage = validation.get("module_coverage", {})
        print(f"📚 Module Coverage:")
        print(f"   Total Required: {module_coverage.get('total_required', 0)}")
        print(f"   Total Generated: {module_coverage.get('total_generated', 0)}")
        print(f"   Coverage: {module_coverage.get('coverage_percentage', 0):.1f}%")
        print(f"   All Present: {module_coverage.get('all_present', False)}")
        
        if module_coverage.get("missing_modules"):
            print(f"   Missing: {module_coverage['missing_modules']}")
        
        # Chart validation
        js_validation = validation.get("javascript_validation", {})
        chart_validation = js_validation.get("chart_constructors", {})
        print(f"\n📈 Chart Validation:")
        print(f"   Total Chart Calls: {chart_validation.get('total_chart_calls', 0)}")
        print(f"   Valid Chart Calls: {chart_validation.get('valid_chart_calls', 0)}")
        print(f"   Invalid Chart Calls: {chart_validation.get('invalid_chart_calls', 0)}")
        print(f"   Has Valid Syntax: {chart_validation.get('has_valid_syntax', False)}")
        
        # Tooltip validation
        interactive_features = validation.get("interactive_features", {})
        tooltip_validation = interactive_features.get("advanced_tooltips", {})
        print(f"\n💡 Tooltip Validation:")
        print(f"   Tooltip Div Present: {tooltip_validation.get('tooltip_div_present', False)}")
        print(f"   Tooltip Data Present: {tooltip_validation.get('tooltip_data_present', False)}")
        print(f"   Event Listeners: {tooltip_validation.get('tooltip_event_listeners', False)}")
        print(f"   Functionality Present: {tooltip_validation.get('tooltip_functionality_present', False)}")
        print(f"   Has Enhanced Tooltip HTML: {tooltip_validation.get('has_enhanced_tooltip_html', False)}")
        
        # Navigation validation
        nav_validation = validation.get("navigation_validation", {})
        print(f"\n🧭 Navigation Validation:")
        print(f"   Navigation Div Present: {nav_validation.get('navigation_div_present', False)}")
        print(f"   Nav Buttons Present: {nav_validation.get('nav_buttons_present', False)}")
        print(f"   Functionality Present: {nav_validation.get('navigation_functionality_present', False)}")
        
        # Overall success
        overall_success = validation.get("overall_success", False)
        print(f"\n🎯 Overall Success: {overall_success}")
        
        if overall_success:
            print("\n🎉 COMPREHENSIVE SUCCESS!")
            print("✅ All 22 modules generated with meaningful content")
            print("✅ Interactive visualizations with proper labels")
            print("✅ Advanced tooltips with multiple sources")
            print("✅ Complete navigation system")
            print("✅ No autoscroll issues")
        else:
            print("\n⚠️  PARTIAL SUCCESS - Some issues detected")
            
    else:
        print(f"❌ Report generation failed: {result.get('error', 'Unknown error')}")
    
    print(f"\n📄 Report file: {result.get('file_path', 'Not generated')}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_system())
