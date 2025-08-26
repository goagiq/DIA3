#!/usr/bin/env python3
"""
Test script for the Enhanced HTML Report Generator with Advanced Tooltips
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.enhanced_html_report_generator import generate_enhanced_html_report

async def test_enhanced_html_generator():
    """Test the enhanced HTML report generator with advanced tooltips."""
    
    # Test data with multiple sections
    test_data = {
        "content": "Pakistan Submarine Acquisition Analysis",
        "type": "strategic_analysis",
        "sections": [
            {
                "title": "Strategic Impact Analysis",
                "content": "Comprehensive analysis of Pakistan's submarine acquisition impact on regional strategic balance, deterrence capabilities, and power dynamics."
            },
            {
                "title": "Economic Impact Timeline",
                "content": "Detailed timeline of economic implications including investment phases, cost projections, and economic benefits over the next decade."
            },
            {
                "title": "Regional Balance of Power",
                "content": "Analysis of how submarine acquisition affects the regional balance of power, alliance structures, and security dynamics in South Asia."
            }
        ],
        "metadata": {
            "source": "test_data",
            "analysis_type": "comprehensive"
        }
    }
    
    print("🚀 Testing Enhanced HTML Report Generator with Advanced Tooltips...")
    
    try:
        # Generate the enhanced report
        result = await generate_enhanced_html_report(
            data=test_data,
            query_type="strategic_analysis",
            title="Pakistan Submarine Acquisition Analysis",
            output_dir="Results"
        )
        
        if result["success"]:
            print(f"✅ Enhanced HTML report generated successfully!")
            print(f"📁 File: {result['file_path']}")
            print(f"📊 File size: {result['file_size']} bytes")
            print(f"🕒 Generated at: {result['generated_at']}")
            print(f"📋 Data type: {result['data_type']}")
            print(f"🔍 Query type: {result['query_type']}")
            
            # Display comprehensive validation results
            if "validation_results" in result:
                validation = result["validation_results"]
                print("\n🔍 COMPREHENSIVE VALIDATION RESULTS:")
                print("=" * 60)
                
                # Module coverage
                module_coverage = validation.get("module_coverage", {})
                print(f"📊 Module Coverage: {module_coverage.get('total_generated', 0)} out of {module_coverage.get('total_required', 0)} modules ({module_coverage.get('coverage_percentage', 0):.1f}%)")
                
                if module_coverage.get("missing_modules"):
                    print(f"⚠️ Missing modules: {len(module_coverage['missing_modules'])}")
                    for module in module_coverage["missing_modules"][:5]:  # Show first 5
                        print(f"   - {module}")
                
                # JavaScript validation
                js_validation = validation.get("javascript_validation", {})
                chart_validation = js_validation.get("chart_constructors", {})
                print(f"\n⚡ JavaScript Validation:")
                print(f"  📊 Chart constructor calls: {chart_validation.get('total_chart_calls', 0)}")
                print(f"  ✅ Valid variable names: {chart_validation.get('valid_variable_names', 0)}")
                print(f"  ❌ Invalid variable names: {chart_validation.get('invalid_variable_names', 0)}")
                print(f"  🔧 Valid syntax: {chart_validation.get('has_valid_syntax', False)}")
                
                # Interactive features
                interactive_features = validation.get("interactive_features", {})
                viz_validation = interactive_features.get("visualizations", {})
                print(f"\n🎨 Interactive Visualizations:")
                print(f"  📊 Canvas elements: {viz_validation.get('has_canvas_elements', 0)}")
                print(f"  📦 Chart containers: {viz_validation.get('has_chart_containers', 0)}")
                print(f"  📈 Chart data: {viz_validation.get('has_chart_data', False)}")
                print(f"  🏷️ Chart labels: {viz_validation.get('has_chart_labels', False)}")
                
                # Advanced tooltips
                tooltip_validation = interactive_features.get("advanced_tooltips", {})
                print(f"\n💡 Advanced Tooltips:")
                print(f"  🎯 Enhanced tooltip HTML: {tooltip_validation.get('has_enhanced_tooltip_html', False)}")
                print(f"  📚 Source formatting: {tooltip_validation.get('has_source_formatting', False)}")
                print(f"  🏢 Internal sources: {tooltip_validation.get('has_internal_source_format', False)}")
                print(f"  🌐 External sources: {tooltip_validation.get('has_external_source_format', False)}")
                
                # Overall summary
                if "summary" in validation:
                    print(f"\n📋 VALIDATION SUMMARY:")
                    print(f"  {validation['summary']}")
            
            # Check if the file exists and has content
            file_path = Path(result['file_path'])
            if file_path.exists():
                file_size = file_path.stat().st_size
                print(f"\n✅ File exists and has {file_size} bytes of content")
                
                # Check for advanced tooltip features
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if 'enhanced-tooltip' in content:
                    print("✅ Advanced tooltip HTML structure found")
                else:
                    print("❌ Advanced tooltip HTML structure not found")
                    
                if 'tooltipData' in content:
                    print("✅ Advanced tooltip JavaScript data found")
                else:
                    print("❌ Advanced tooltip JavaScript data not found")
                    
                if 'Source: DIA3 -' in content:
                    print("✅ Internal DIA3 sources found")
                else:
                    print("❌ Internal DIA3 sources not found")
                    
                if 'Source: ' in content and ' - ' in content:
                    print("✅ External sources found")
                else:
                    print("❌ External sources not found")
                    
                if 'scroll-behavior: auto' in content:
                    print("✅ Autoscroll prevention CSS found")
                else:
                    print("❌ Autoscroll prevention CSS not found")
                    
                print(f"\n🎉 Test completed successfully! Open {result['file_path']} in your browser to see the enhanced report with advanced tooltips.")
            else:
                print(f"❌ Generated file not found at {result['file_path']}")
        else:
            print(f"❌ Report generation failed: {result.get('error', 'Unknown error')}")
            if 'error_count' in result:
                print(f"🔄 Error count: {result['error_count']}")
    
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_enhanced_html_generator())
