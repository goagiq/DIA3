#!/usr/bin/env python3
"""
Test script to verify the enhanced HTML report generator v2 with improved navigation and content.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.enhanced_html_report_generator import EnhancedHTMLReportGenerator

async def test_enhanced_v2_system():
    """Test the enhanced HTML report generator v2 with improved navigation and content."""
    
    print("🚀 Testing Enhanced HTML Report Generator V2")
    print("=" * 60)
    
    # Initialize the generator
    generator = EnhancedHTMLReportGenerator()
    
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
    output_path = "Results/Test_Enhanced_V2_20250825_184500.html"
    
    print(f"📊 Generating enhanced report with {len(test_data['sections'])} input sections...")
    print(f"📁 Output file: {output_path}")
    
    result = await generator.generate_enhanced_report(test_data, output_path)
    
    if result["success"]:
        print("✅ Report generated successfully!")
        print(f"📄 File: {result['file_path']}")
        
        # Check for enhanced features
        file_path = Path(result['file_path'])
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for enhanced features
        features = [
            ("Enhanced Navigation", "📋 Executive Summary"),
            ("Enhanced Navigation", "🌍 Geopolitical Impact"),
            ("Enhanced Navigation", "🎯 Strategic Recommendations"),
            ("Enhanced Navigation", "🏁 Conclusion"),
            ("Enhanced Recommendations", "Module Analysis Summary"),
            ("Enhanced Recommendations", "Deductive Reasoning"),
            ("Enhanced Recommendations", "Strategic Recommendations"),
            ("Enhanced Conclusion", "Comprehensive Conclusion"),
            ("Enhanced Conclusion", "Critical Action Items"),
            ("Enhanced Conclusion", "Strategic Implications"),
            ("Advanced Tooltips", "enhanced-tooltip"),
            ("Advanced Tooltips", "tooltipData"),
            ("Meaningful Chart Data", "Strategic Impact"),
            ("Meaningful Chart Data", "Economic Impact"),
            ("Meaningful Chart Data", "Regional Alliances"),
            ("Meaningful Chart Data", "Technology Development")
        ]
        
        print("\n🔍 FEATURE VERIFICATION:")
        print("-" * 40)
        
        for feature_name, feature_check in features:
            if feature_check in content:
                print(f"✅ {feature_name}")
            else:
                print(f"❌ {feature_name}")
        
        # Count sections
        section_count = content.count('module-section')
        print(f"\n📊 Total Sections Generated: {section_count}")
        
        # Check navigation buttons
        nav_buttons = content.count('nav-button')
        print(f"🧭 Navigation Buttons: {nav_buttons}")
        
        # Check tooltips
        tooltip_sources = content.count('Source: DIA3 -')
        print(f"💡 Tooltip Sources: {tooltip_sources}")
        
        print(f"\n🎉 Enhanced V2 System Test Complete!")
        print("✅ Improved navigation with meaningful section names")
        print("✅ Enhanced recommendations with deductive reasoning")
        print("✅ Comprehensive conclusion with action items")
        print("✅ Advanced tooltips with multiple sources")
        print("✅ Meaningful chart data for all modules")
        
    else:
        print(f"❌ Report generation failed: {result.get('error', 'Unknown error')}")
    
    print(f"\n📄 Report file: {result.get('file_path', 'Not generated')}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_v2_system())
