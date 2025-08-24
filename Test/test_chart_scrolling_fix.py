#!/usr/bin/env python3
"""
Test Chart Scrolling Fix

Test script to verify that chart scrolling issues have been fixed.
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modular_report_generator import modular_report_generator


async def test_chart_scrolling_fix():
    """Test that chart scrolling issues have been fixed."""
    print("🧪 Testing Chart Scrolling Fix")
    
    # Sample data for testing with charts
    sample_data = {
        "strategic_analysis": {
            "title": "Test Strategic Analysis",
            "overview": "Test strategic analysis overview.",
            "key_components": [
                "Component 1",
                "Component 2",
                "Component 3"
            ],
            "confidence_level": 0.85
        },
        "strategic_insights": {
            "title": "Test Strategic Insights",
            "insights": [
                "Insight 1",
                "Insight 2",
                "Insight 3"
            ],
            "categories": {
                "category1": "Category 1",
                "category2": "Category 2"
            }
        },
        "geopolitical_impact": {
            "title": "Test Geopolitical Impact",
            "regional_impact": {
                "Region 1": "Impact 1",
                "Region 2": "Impact 2"
            },
            "global_implications": [
                "Implication 1",
                "Implication 2"
            ]
        },
        "strategic_implications": [
            "Implication 1",
            "Implication 2",
            "Implication 3"
        ]
    }
    
    try:
        # Generate report with Strategic Analysis Module (which has charts)
        result = await modular_report_generator.generate_modular_report(
            topic="Chart Scrolling Test",
            data=sample_data,
            enabled_modules=["strategicanalysismodule"],
            report_title="Chart Scrolling Fix Test"
        )
        
        if result.get("success"):
            print(f"✅ Report generated successfully!")
            print(f"📄 File: {result.get('filename')}")
            print(f"📁 Path: {result.get('file_path')}")
            print(f"📊 Size: {result.get('file_size')} bytes")
            
            # Check the generated file for chart container fixes
            file_path = Path(result.get('file_path'))
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for proper chart container CSS
                if '.chart-container {' in content:
                    print("✅ Chart container CSS found")
                else:
                    print("❌ Chart container CSS missing")
                    return False
                
                # Check for proper chart container HTML structure
                if '<div class="chart-container">' in content:
                    print("✅ Chart container HTML structure found")
                else:
                    print("❌ Chart container HTML structure missing")
                    return False
                
                # Check for proper responsive chart settings
                if '"responsive": true' in content and 'config.options.responsive = true' in content:
                    print("✅ Responsive chart settings found")
                else:
                    print("❌ Responsive chart settings missing")
                    return False
                
                # Check for proper container sizing
                if 'container.style.height' in content and 'container.style.position' in content:
                    print("✅ Container sizing JavaScript found")
                else:
                    print("❌ Container sizing JavaScript missing")
                    return False
                
                return True
            else:
                print("❌ Generated file not found")
                return False
        else:
            print(f"❌ Report generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False


async def main():
    """Main test function."""
    print("🚀 Chart Scrolling Fix Test Suite")
    print("=" * 50)
    
    # Test chart scrolling fix
    test_passed = await test_chart_scrolling_fix()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"✅ Chart Scrolling Fix: {'PASSED' if test_passed else 'FAILED'}")
    
    if test_passed:
        print("\n🎉 Chart scrolling fix is working correctly!")
        return True
    else:
        print("\n❌ Chart scrolling fix needs attention.")
        return False


if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
