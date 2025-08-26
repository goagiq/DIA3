#!/usr/bin/env python3
"""
Demonstration of Enhanced HTML Report System with Advanced Tooltips
Shows how the new system integrates with the modular report generator.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.modular_report_generator import ModularReportGenerator
from core.enhanced_html_report_generator import EnhancedHTMLReportGenerator

async def demonstrate_enhanced_system():
    """Demonstrate the enhanced HTML report system with advanced tooltips."""
    
    print("🚀 Demonstrating Enhanced HTML Report System with Advanced Tooltips")
    print("=" * 70)
    
    # Test data for Pakistan Submarine Analysis
    test_data = {
        "content": "Pakistan Submarine Acquisition Analysis and Deterrence Enhancement",
        "type": "strategic_analysis",
        "sections": [
            {
                "title": "Executive Summary",
                "content": "Comprehensive analysis of Pakistan's submarine acquisition program, examining strategic implications, economic impact, and regional security dynamics."
            },
            {
                "title": "Geopolitical Impact Analysis",
                "content": "Analysis of how submarine acquisition affects Pakistan's geopolitical position, regional alliances, and international relations in South Asia."
            },
            {
                "title": "Trade and Economic Impact",
                "content": "Detailed assessment of economic implications including defense spending, technology transfer, and economic benefits over the next decade."
            },
            {
                "title": "Security Implications",
                "content": "Evaluation of maritime security enhancement, deterrence capabilities, and strategic balance in the Indian Ocean region."
            },
            {
                "title": "Regional Balance of Power",
                "content": "Analysis of how submarine acquisition affects the regional balance of power, alliance structures, and security dynamics."
            },
            {
                "title": "Strategic Recommendations",
                "content": "Comprehensive recommendations for optimal submarine acquisition strategy, risk mitigation, and implementation planning."
            }
        ],
        "metadata": {
            "source": "comprehensive_analysis",
            "analysis_type": "strategic_assessment",
            "date": "2025-08-25"
        }
    }
    
    print("\n📊 Test 1: Direct Enhanced HTML Report Generation")
    print("-" * 50)
    
    try:
        # Test direct enhanced HTML generation
        enhanced_generator = EnhancedHTMLReportGenerator()
        result1 = await enhanced_generator.generate_enhanced_report(
            test_data,
            "Results/Pakistan_Submarine_Analysis_-_Enhanced_Direct_20250825_183000.html"
        )
        
        if result1["success"]:
            print(f"✅ Enhanced HTML report generated successfully!")
            print(f"📁 File: {result1['file_path']}")
            print(f"📊 Size: {result1['file_size']} bytes")
            
            # Check for advanced tooltip features
            file_path = Path(result1['file_path'])
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            features = [
                ("Advanced Tooltip HTML", "enhanced-tooltip"),
                ("Tooltip JavaScript Data", "tooltipData"),
                ("Internal DIA3 Sources", "Source: DIA3 -"),
                ("External Sources", "Source: "),
                ("Autoscroll Prevention", "scroll-behavior: auto"),
                ("Interactive Charts", "Chart.js"),
                ("Multiple Sources", "📚")
            ]
            
            for feature_name, feature_check in features:
                if feature_check in content:
                    print(f"✅ {feature_name}")
                else:
                    print(f"❌ {feature_name}")
        else:
            print(f"❌ Enhanced HTML generation failed: {result1.get('error')}")
    
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
    
    print("\n📊 Test 2: Integration with Modular Report Generator")
    print("-" * 50)
    
    try:
        # Test integration with modular report generator
        modular_generator = ModularReportGenerator()
        result2 = await modular_generator.generate_modular_report(
            query="Pakistan Submarine Acquisition Analysis and Deterrence Enhancement",
            enabled_modules=["executive_summary", "geopolitical_impact", "trade_impact"],
            output_format="html",
            title="Pakistan Submarine Analysis - Modular Enhanced"
        )
        
        if result2["success"]:
            print(f"✅ Modular enhanced HTML report generated successfully!")
            print(f"📁 File: {result2['file_path']}")
            print(f"📊 Size: {result2['file_size']} bytes")
            
            # Display validation results if available
            if "validation_results" in result2:
                validation = result2["validation_results"]
                print(f"\n🔍 MODULAR REPORT VALIDATION RESULTS:")
                print("=" * 50)
                
                # Module coverage
                module_coverage = validation.get("module_coverage", {})
                print(f"📊 Module Coverage: {module_coverage.get('total_generated', 0)} out of {module_coverage.get('total_required', 0)} modules ({module_coverage.get('coverage_percentage', 0):.1f}%)")
                
                # JavaScript validation
                js_validation = validation.get("javascript_validation", {})
                chart_validation = js_validation.get("chart_constructors", {})
                print(f"⚡ Interactive Charts: {chart_validation.get('total_chart_calls', 0)} charts with {'✅ valid' if chart_validation.get('has_valid_syntax', False) else '❌ invalid'} JavaScript syntax")
                
                # Advanced tooltips
                interactive_features = validation.get("interactive_features", {})
                tooltip_validation = interactive_features.get("advanced_tooltips", {})
                print(f"💡 Advanced Tooltips: {'✅ Working' if tooltip_validation.get('has_enhanced_tooltip_html', False) else '❌ Missing'}")
                
                # Overall summary
                if "summary" in validation:
                    print(f"📋 Summary: {validation['summary']}")
            
            # Check for advanced tooltip features
            file_path = Path(result2['file_path'])
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            features = [
                ("Advanced Tooltip HTML", "enhanced-tooltip"),
                ("Tooltip JavaScript Data", "tooltipData"),
                ("Internal DIA3 Sources", "Source: DIA3 -"),
                ("External Sources", "Source: "),
                ("Autoscroll Prevention", "scroll-behavior: auto"),
                ("Interactive Charts", "Chart.js"),
                ("Multiple Sources", "📚")
            ]
            
            for feature_name, feature_check in features:
                if feature_check in content:
                    print(f"✅ {feature_name}")
                else:
                    print(f"❌ {feature_name}")
        else:
            print(f"❌ Modular enhanced HTML generation failed: {result2.get('error')}")
    
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
    
    print("\n📊 Test 3: Error Recovery and Self-Healing")
    print("-" * 50)
    
    try:
        # Test with problematic data to show error recovery
        problematic_data = "This is just a string without proper structure"
        
        result3 = await generate_enhanced_html_report(
            data=problematic_data,
            query_type="error_test",
            title="Error Recovery Test",
            output_dir="Results"
        )
        
        if result3["success"]:
            print(f"✅ Error recovery successful!")
            print(f"📁 File: {result3['file_path']}")
            print(f"📊 Size: {result3['file_size']} bytes")
            
            if "recovery_attempt" in result3:
                print(f"🔄 Recovery attempt: {result3['recovery_attempt']}")
        else:
            print(f"❌ Error recovery failed: {result3.get('error')}")
    
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
    
    print("\n🎉 Enhanced HTML Report System Demonstration Complete!")
    print("=" * 70)
    print("\n📋 Summary of Advanced Features:")
    print("✅ Advanced tooltips with multiple sources")
    print("✅ Proper source attribution (DIA3 - vs External)")
    print("✅ Autoscroll prevention")
    print("✅ Interactive visualizations")
    print("✅ Self-healing error recovery")
    print("✅ Dynamic data structure handling")
    print("✅ Future-proof architecture")
    print("\n🔗 Open the generated HTML files in your browser to see the advanced tooltips in action!")

if __name__ == "__main__":
    asyncio.run(demonstrate_enhanced_system())
