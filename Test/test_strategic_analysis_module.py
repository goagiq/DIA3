#!/usr/bin/env python3
"""
Test Strategic Analysis Module

Test script to verify the Strategic Analysis Module functionality.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modules.strategic_analysis_module import StrategicAnalysisModule


def test_strategic_analysis_module():
    """Test the Strategic Analysis Module with sample data."""
    print("🧪 Testing Strategic Analysis Module")
    
    # Create module
    module = StrategicAnalysisModule()
    print(f"✅ Module created: {module.module_id}")
    
    # Sample data for testing
    sample_data = {
        "strategic_analysis": {
            "title": "Pakistan Submarine Acquisition Strategic Analysis",
            "overview": "Comprehensive strategic analysis of Pakistan's submarine acquisition program and its implications for regional security dynamics.",
            "key_components": [
                "Naval capability enhancement",
                "Regional power balance shift",
                "Strategic deterrence implications",
                "Economic and technological impact",
                "Diplomatic and political consequences"
            ],
            "confidence_level": 0.85
        },
        "strategic_insights": {
            "title": "Strategic Insights",
            "insights": [
                "Significant enhancement of Pakistan's naval capabilities",
                "Potential shift in regional maritime power dynamics",
                "Increased strategic deterrence capabilities",
                "Economic burden and resource allocation implications",
                "Diplomatic tensions with neighboring countries"
            ],
            "categories": {
                "military": "Naval and military implications",
                "economic": "Economic and resource implications",
                "political": "Political and diplomatic implications"
            }
        },
        "geopolitical_impact": {
            "title": "Geopolitical Impact Analysis",
            "regional_impact": {
                "South Asia": "Significant impact on regional maritime security",
                "Indian Ocean": "Enhanced presence in key maritime routes",
                "Middle East": "Potential influence on regional stability"
            },
            "global_implications": [
                "Impact on international maritime security",
                "Influence on global arms trade dynamics",
                "Implications for international relations"
            ],
            "power_dynamics": {
                "regional_balance": "Shift in regional power balance",
                "strategic_partnerships": "Impact on strategic partnerships"
            }
        },
        "strategic_implications": [
            "Long-term strategic positioning in the region",
            "Enhanced deterrence capabilities against potential threats",
            "Economic and technological development implications",
            "Diplomatic and political relationship impacts",
            "Regional security architecture changes"
        ]
    }
    
    try:
        # Generate content
        content = module.generate_content(sample_data)
        print(f"✅ Content generated successfully!")
        print(f"📄 Content length: {len(content)} characters")
        
        # Test tooltip data
        tooltip_data = module.get_tooltip_data()
        print(f"✅ Tooltip data: {len(tooltip_data)} tooltips")
        
        # Test chart data
        chart_data = module.get_chart_data()
        print(f"✅ Chart data: {len(chart_data)} charts")
        
        # Test module metadata
        metadata = module.get_module_metadata()
        print(f"✅ Module metadata: {metadata}")
        
        # Test configuration
        config = module.export_config()
        print(f"✅ Module configuration: {config}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False


def test_module_integration():
    """Test module integration with the generator."""
    print("\n🧪 Testing Module Integration")
    
    try:
        from core.modular_report_generator import modular_report_generator
        
        # Check if module is registered
        available_modules = modular_report_generator.get_available_modules()
        if "strategicanalysismodule" in available_modules:
            print("✅ Module is registered in generator")
        else:
            print("❌ Module is not registered in generator")
            return False
        
        # Check if module is enabled
        enabled_modules = [m.module_id for m in modular_report_generator.get_enabled_modules()]
        if "strategicanalysismodule" in enabled_modules:
            print("✅ Module is enabled in generator")
        else:
            print("❌ Module is not enabled in generator")
            return False
        
        # Test module retrieval
        module = modular_report_generator.get_module("strategicanalysismodule")
        if module:
            print("✅ Module can be retrieved from generator")
        else:
            print("❌ Module cannot be retrieved from generator")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error during integration testing: {e}")
        return False


def main():
    """Main test function."""
    print("🚀 Strategic Analysis Module Test Suite")
    print("=" * 50)
    
    # Test module functionality
    test1_passed = test_strategic_analysis_module()
    
    # Test module integration
    test2_passed = test_module_integration()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"✅ Strategic Analysis Module: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ Module Integration: {'PASSED' if test2_passed else 'FAILED'}")
    
    all_tests_passed = all([test1_passed, test2_passed])
    
    if all_tests_passed:
        print("\n🎉 All tests passed! Strategic Analysis Module is working correctly.")
        return True
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    # Run the test suite
    success = main()
    sys.exit(0 if success else 1)
