#!/usr/bin/env python3
"""
Test Modular Report System

Test script to verify the modular report system functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modular_report_generator import modular_report_generator
from core.modules.strategic_recommendations_module import StrategicRecommendationsModule
from core.modules.strategic_analysis_module import StrategicAnalysisModule


def test_modular_report_generator():
    """Test the modular report generator."""
    print("🧪 Testing Modular Report Generator")
    
    # Test generator initialization
    generator = modular_report_generator
    print(f"✅ Generator initialized: {generator is not None}")
    
    # Test available modules
    available_modules = generator.get_available_modules()
    print(f"✅ Available modules: {available_modules}")
    
    # Test enabled modules
    enabled_modules = [m.module_id for m in generator.get_enabled_modules()]
    print(f"✅ Enabled modules: {enabled_modules}")
    
    # Test generator summary
    summary = generator.get_generator_summary()
    print(f"✅ Generator summary: {summary}")
    
    return True


def test_strategic_recommendations_module():
    """Test the strategic recommendations module."""
    print("\n🧪 Testing Strategic Recommendations Module")
    
    # Create module
    module = StrategicRecommendationsModule()
    print(f"✅ Module created: {module.module_id}")
    
    # Test module metadata
    metadata = module.get_module_metadata()
    print(f"✅ Module metadata: {metadata}")
    
    # Test required data keys
    required_keys = module.get_required_data_keys()
    print(f"✅ Required data keys: {required_keys}")
    
    # Test module configuration
    config = module.export_config()
    print(f"✅ Module config: {config}")
    
    # Test recommendations summary
    summary = module.get_recommendations_summary()
    print(f"✅ Recommendations summary: {summary}")
    
    return True


def test_strategic_analysis_module():
    """Test the strategic analysis module."""
    print("\n🧪 Testing Strategic Analysis Module")
    
    # Create module
    module = StrategicAnalysisModule()
    print(f"✅ Module created: {module.module_id}")
    
    # Test module metadata
    metadata = module.get_module_metadata()
    print(f"✅ Module metadata: {metadata}")
    
    # Test required data keys
    required_keys = module.get_required_data_keys()
    print(f"✅ Required data keys: {required_keys}")
    
    # Test module configuration
    config = module.export_config()
    print(f"✅ Module config: {config}")
    
    # Test tooltip data
    tooltip_data = module.get_tooltip_data()
    print(f"✅ Tooltip data count: {len(tooltip_data)}")
    
    # Test chart data
    chart_data = module.get_chart_data()
    print(f"✅ Chart data count: {len(chart_data)}")
    
    return True


async def test_report_generation():
    """Test report generation with sample data."""
    print("\n🧪 Testing Report Generation")
    
    # Sample data for testing
    sample_data = {
        "strategic_recommendations": [
            {
                "title": "Implement Enhanced Monitoring Systems",
                "description": "Deploy advanced monitoring systems for strategic oversight.",
                "rationale": "Critical for operational effectiveness and safety",
                "timeline": "0-6 months",
                "confidence": 90.0,
                "category": "Operations",
                "priority": "immediate"
            },
            {
                "title": "Develop Strategic Partnerships",
                "description": "Establish formal partnerships with key regional allies.",
                "rationale": "Strengthens regional security architecture",
                "timeline": "3-12 months",
                "confidence": 75.0,
                "category": "Strategic",
                "priority": "short_term"
            },
            {
                "title": "Implement AI-Enhanced Defense Systems",
                "description": "Integrate artificial intelligence into defense systems.",
                "rationale": "Maintains technological edge and operational superiority",
                "timeline": "5-10 years",
                "confidence": 80.0,
                "category": "Technology",
                "priority": "long_term"
            }
        ],
        "intelligence_summary": {
            "total_insights": 15,
            "average_confidence": 85.5,
            "high_impact_insights": 8
        },
        "implementation_roadmap": {
            "timeline_sections": {
                "Immediate": [
                    {
                        "title": "Implement Enhanced Monitoring Systems",
                        "confidence": 90.0
                    },
                    {
                        "title": "Establish Crisis Communication Channels",
                        "confidence": 80.0
                    }
                ],
                "Short Term": [
                    {
                        "title": "Develop Strategic Partnerships",
                        "confidence": 75.0
                    },
                    {
                        "title": "Enhance Cybersecurity Infrastructure",
                        "confidence": 85.0
                    }
                ],
                "Long Term": [
                    {
                        "title": "Implement AI-Enhanced Defense Systems",
                        "confidence": 80.0
                    },
                    {
                        "title": "Develop Indigenous Defense Industry",
                        "confidence": 75.0
                    }
                ]
            }
        },
        "monitoring_plan": {
            "Performance Metrics": [
                "System uptime and reliability",
                "Response time to incidents",
                "Accuracy of threat detection"
            ],
            "Strategic Metrics": [
                "Regional security index",
                "Partnership effectiveness",
                "Technology advancement rate"
            ]
        }
    }
    
    try:
        # Generate report
        result = await modular_report_generator.generate_modular_report(
            topic="Test Strategic Analysis",
            data=sample_data,
            report_title="Test Modular Enhanced Report"
        )
        
        if result.get("success"):
            print(f"✅ Report generated successfully!")
            print(f"📄 File: {result.get('filename')}")
            print(f"📁 Path: {result.get('file_path')}")
            print(f"📊 Size: {result.get('file_size')} bytes")
            print(f"🔧 Modules Used: {result.get('modules_used')}")
            return True
        else:
            print(f"❌ Report generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error during report generation: {e}")
        return False


async def test_module_configuration():
    """Test module configuration capabilities."""
    print("\n🧪 Testing Module Configuration")
    
    generator = modular_report_generator
    
    # Test enabling/disabling modules
    generator.enable_module("strategicrecommendationsmodule", True)
    enabled_modules = [m.module_id for m in generator.get_enabled_modules()]
    print(f"✅ Enabled modules after configuration: {enabled_modules}")
    
    # Test module ordering
    generator.set_module_order("strategicrecommendationsmodule", 50)
    module = generator.get_module("strategicrecommendationsmodule")
    if module:
        print(f"✅ Module order set: {module.get_order()}")
    
    # Test custom configuration
    custom_config = {
        "enabled": True,
        "title": "Custom Strategic Recommendations",
        "description": "Custom description for testing",
        "order": 25,
        "tooltips_enabled": True,
        "charts_enabled": False
    }
    
    generator.configure_module("strategicrecommendationsmodule", custom_config)
    module = generator.get_module("strategicrecommendationsmodule")
    if module:
        print(f"✅ Custom configuration applied: {module.get_title()}")
    
    return True


async def main():
    """Main test function."""
    print("🚀 Modular Report System Test Suite")
    print("=" * 50)
    
    # Test basic functionality
    test1_passed = test_modular_report_generator()
    test2_passed = test_strategic_recommendations_module()
    test3_passed = test_strategic_analysis_module()
    
    # Test async functionality
    test4_passed = await test_report_generation()
    test5_passed = await test_module_configuration()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"✅ Modular Report Generator: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ Strategic Recommendations Module: {'PASSED' if test2_passed else 'FAILED'}")
    print(f"✅ Strategic Analysis Module: {'PASSED' if test3_passed else 'FAILED'}")
    print(f"✅ Report Generation: {'PASSED' if test4_passed else 'FAILED'}")
    print(f"✅ Module Configuration: {'PASSED' if test5_passed else 'FAILED'}")
    
    all_tests_passed = all([test1_passed, test2_passed, test3_passed, test4_passed, test5_passed])
    
    if all_tests_passed:
        print("\n🎉 All tests passed! Modular report system is working correctly.")
        return True
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
