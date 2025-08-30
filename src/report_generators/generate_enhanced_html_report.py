#!/usr/bin/env python3
"""
Enhanced HTML Report Generator

This script generates a comprehensive HTML report using the enhanced template
with advanced tooltips and multiple sources for all 22 modules.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.modular_report_generator import modular_report_generator
from src.core.adaptive_data_adapter import adaptive_data_adapter


async def generate_enhanced_html_report():
    """Generate an enhanced HTML report with all 22 modules."""
    
    # Topic for analysis
    topic = ("Pakistan Submarine Acquisition Analysis and Deterrence "
             "enhancement Impact on geopolitic, trade, balance of power, "
             "escalation")
    
    print("🚀 Generating Enhanced HTML Report...")
    print(f"📋 Topic: {topic}")
    
    try:
        # Generate adaptive data
        print("📊 Generating adaptive data...")
        universal_data = adaptive_data_adapter.generate_universal_data(topic, {})
        
        # Get all available modules
        print("🔧 Loading all 22 modules...")
        modules_info = modular_report_generator.get_available_modules()
        all_module_ids = list(modules_info.keys())
        
        print(f"✅ Found {len(all_module_ids)} modules: {', '.join(all_module_ids)}")
        
        # Generate the enhanced HTML report
        print("📝 Generating enhanced HTML report...")
        result = await modular_report_generator.generate_modular_report(
            topic=topic,
            data=universal_data,
            enabled_modules=all_module_ids,
            report_title=f"Enhanced Analysis: {topic}",
            custom_config={
                "enhanced_template": True,
                "advanced_tooltips": True,
                "multiple_sources": True,
                "interactive_charts": True
            }
        )
        
        if result.get("success"):
            print("✅ Enhanced HTML report generated successfully!")
            print(f"📁 File: {result.get('file_path')}")
            print(f"📊 Modules used: {len(result.get('modules_used', []))}")
            print(f"📏 File size: {result.get('file_size', 0)} bytes")
            
            # Open the report in browser
            import webbrowser
            file_path = Path(result.get('file_path'))
            if file_path.exists():
                webbrowser.open(f"file://{file_path.absolute()}")
                print("🌐 Opened report in browser")
            
            return result
        else:
            print(f"❌ Error generating report: {result.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Run the report generation
    result = asyncio.run(generate_enhanced_html_report())
    
    if result:
        print("\n🎉 Enhanced HTML report generation completed successfully!")
        print("📊 The report includes:")
        print("   • All 22 analysis modules")
        print("   • Advanced tooltips with multiple sources")
        print("   • Interactive visualizations")
        print("   • Professional styling and layout")
        print("   • Responsive design")
    else:
        print("\n❌ Report generation failed!")
        sys.exit(1)
