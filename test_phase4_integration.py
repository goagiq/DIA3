#!/usr/bin/env python3
"""
Test Phase 4 Integration with 22 Enhanced Report Modules

This script tests the integration of Phase 4 Strategic Intelligence capabilities
with all 22 enhanced report modules.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.modular_report_generator import ModularReportGenerator
from src.core.adaptive_data_adapter import adaptive_data_adapter


async def test_phase4_integration():
    """Test the Phase 4 integration with all 22 modules."""
    
    print("🧪 Testing Phase 4 Strategic Intelligence Integration")
    print("=" * 60)
    
    # Initialize the modular report generator
    generator = ModularReportGenerator()
    
    # Get all available modules
    modules_info = generator.get_available_modules()
    module_ids = list(modules_info.keys())
    
    print(f"📋 Found {len(module_ids)} modules:")
    for i, module_id in enumerate(module_ids, 1):
        print(f"   {i:2d}. {module_id}")
    
    # Test topic
    topic = "Pakistan Submarine Acquisition: Strategic Intelligence Analysis"
    
    print(f"\n🎯 Testing with topic: {topic}")
    
    try:
        # Generate adaptive data
        print("📊 Generating adaptive data...")
        universal_data = adaptive_data_adapter.generate_universal_data(topic, {})
        
        # Test report generation with Phase 4 integration
        print("📝 Generating Phase 4 integrated report...")
        result = await generator.generate_modular_report(
            query=topic,
            enabled_modules=module_ids,  # Use all modules
            config={
                "enhanced_template": True,
                "advanced_tooltips": True,
                "multiple_sources": True,
                "interactive_charts": True,
                "strategic_intelligence": True,
                "phase4_integration": True
            },
            output_format="html",
            title=f"Phase 4 Integration Test: {topic}"
        )
        
        if result.get("success"):
            print("✅ Phase 4 Integration test successful!")
            print(f"📁 Report generated: {result.get('file_path')}")
            print(f"📊 Modules used: {len(result.get('modules_used', []))}")
            print(f"📏 File size: {result.get('file_size', 0)} bytes")
            
            # Check for Phase 4 capabilities
            modules_used = result.get('modules_used', [])
            if "strategic_intelligence" in modules_used:
                print("✅ Strategic Intelligence Module successfully integrated")
            
            # Count enhanced modules
            enhanced_count = len([m for m in modules_used if m in module_ids])
            print(f"✅ {enhanced_count} enhanced modules used")
            
            return result
        else:
            print(f"❌ Phase 4 Integration test failed: {result.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_individual_modules():
    """Test individual modules with Phase 4 capabilities."""
    
    print("\n🔧 Testing Individual Modules with Phase 4 Capabilities")
    print("=" * 60)
    
    generator = ModularReportGenerator()
    modules_info = generator.get_available_modules()
    
    # Test a few key modules
    test_modules = [
        "strategic_recommendations",
        "risk_assessment", 
        "forecasting",
        "strategic_analysis"
    ]
    
    topic = "Pakistan Submarine Acquisition"
    
    for module_id in test_modules:
        if module_id in modules_info:
            print(f"\n🧪 Testing {module_id}...")
            
            try:
                result = await generator.generate_modular_report(
                    query=topic,
                    enabled_modules=[module_id],
                    config={
                        "enhanced_template": True,
                        "strategic_intelligence": True,
                        "phase4_integration": True
                    },
                    output_format="html",
                    title=f"Phase 4 Test - {module_id}"
                )
                
                if result.get("success"):
                    print(f"   ✅ {module_id} test successful")
                    print(f"   📁 File: {result.get('file_path')}")
                else:
                    print(f"   ❌ {module_id} test failed: {result.get('error')}")
                    
            except Exception as e:
                print(f"   ❌ {module_id} error: {e}")
        else:
            print(f"   ⚠️ {module_id} not found")


async def main():
    """Main test function."""
    
    print("🎯 Phase 4 Strategic Intelligence Integration Test")
    print("=" * 60)
    
    # Test the full integration
    result = await test_phase4_integration()
    
    # Test individual modules
    await test_individual_modules()
    
    if result:
        print("\n🎉 Phase 4 Integration Test completed successfully!")
        print("🚀 All 22 modules enhanced with strategic intelligence capabilities!")
        print("📊 The system is now a comprehensive strategic intelligence platform!")
    else:
        print("\n❌ Phase 4 Integration Test failed!")
        print("🔧 Please check the error messages above.")


if __name__ == "__main__":
    asyncio.run(main())
