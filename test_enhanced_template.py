#!/usr/bin/env python3
"""
Test Enhanced HTML Template

This script tests the enhanced HTML template with a sample topic.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.modular_report_generator import modular_report_generator
from src.core.adaptive_data_adapter import adaptive_data_adapter

async def test_enhanced_template():
    """Test the enhanced HTML template."""
    
    topic = "Test Topic: Enhanced Template Analysis"
    
    print("🧪 Testing Enhanced HTML Template...")
    print(f"📋 Topic: {topic}")
    
    try:
        # Generate adaptive data
        universal_data = adaptive_data_adapter.generate_universal_data(topic, {})
        
        # Get all available modules
        modules_info = modular_report_generator.get_available_modules()
        all_module_ids = list(modules_info.keys())
        
        # Generate the enhanced HTML report
        result = await modular_report_generator.generate_modular_report(
            topic=topic,
            data=universal_data,
            enabled_modules=all_module_ids,
            report_title=f"Enhanced Test: {topic}",
            custom_config={
                "enhanced_template": True,
                "advanced_tooltips": True,
                "multiple_sources": True,
                "interactive_charts": True
            }
        )
        
        if result.get("success"):
            print("✅ Enhanced template test successful!")
            print(f"📁 File: {result.get('file_path')}")
            return True
        else:
            print(f"❌ Test failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_enhanced_template())
    if success:
        print("\n🎉 Enhanced template is working correctly!")
    else:
        print("\n❌ Enhanced template test failed!")
        sys.exit(1)
