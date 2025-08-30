#!/usr/bin/env python3
"""
Test Executive Summary Module

Test script to verify the Executive Summary module functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modules.executive_summary_module import ExecutiveSummaryModule
from core.modular_report_generator import modular_report_generator


def test_executive_summary_module():
    """Test the Executive Summary module."""
    print("🧪 Testing Executive Summary Module")
    
    # Create module
    module = ExecutiveSummaryModule()
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
    
    # Test executive summary summary
    summary = module.get_executive_summary_summary()
    print(f"✅ Executive summary summary: {summary}")
    
    return True


async def test_executive_summary_report_generation():
    """Test report generation with Executive Summary module."""
    print("\n🧪 Testing Executive Summary Report Generation")
    
    # Sample data for Executive Summary module
    sample_data = {
        "executive_summary": {
            "title": "Pakistan Submarine Acquisition: Executive Summary",
            "overview": "This analysis examines the strategic implications of Pakistan's submarine acquisition program and its impact on regional security dynamics.",
            "key_findings": [
                "Pakistan's submarine program represents a significant strategic capability enhancement",
                "Regional security dynamics are likely to be affected by this acquisition",
                "Economic and technological implications extend beyond military considerations"
            ],
            "confidence_level": 87.5
        },
        "key_metrics": {
            "metrics": {
                "Strategic Impact Score": {
                    "value": "8.5/10",
                    "trend": "up",
                    "description": "High strategic impact on regional security"
                },
                "Economic Investment": {
                    "value": "$5.2B",
                    "trend": "stable",
                    "description": "Significant economic investment in defense"
                },
                "Technology Transfer": {
                    "value": "Advanced",
                    "trend": "up",
                    "description": "Advanced technology transfer involved"
                },
                "Regional Response": {
                    "value": "Moderate",
                    "trend": "neutral",
                    "description": "Moderate regional response expected"
                }
            }
        },
        "trend_analysis": {
            "trends": [
                {
                    "title": "Increasing Regional Tensions",
                    "description": "Submarine acquisition likely to increase regional security tensions.",
                    "direction": "up",
                    "impact": "high"
                },
                {
                    "title": "Technology Advancement",
                    "description": "Significant advancement in naval technology capabilities.",
                    "direction": "up",
                    "impact": "medium"
                },
                {
                    "title": "Economic Burden",
                    "description": "Economic burden on defense budget and national resources.",
                    "direction": "down",
                    "impact": "medium"
                }
            ]
        },
        "strategic_insights": [
            {
                "title": "Strategic Deterrence Enhancement",
                "description": "Submarine capability significantly enhances strategic deterrence posture.",
                "category": "Strategic",
                "priority": "high"
            },
            {
                "title": "Regional Power Balance",
                "description": "Shifts regional power balance and security dynamics.",
                "category": "Geopolitical",
                "priority": "high"
            },
            {
                "title": "Economic Implications",
                "description": "Long-term economic implications for defense spending and resource allocation.",
                "category": "Economic",
                "priority": "medium"
            }
        ],
        # Strategic recommendations data (for existing module)
        "strategic_recommendations": [
            {
                "title": "Monitor Regional Response",
                "description": "Closely monitor regional responses to submarine acquisition.",
                "rationale": "Critical for understanding security implications",
                "timeline": "0-6 months",
                "confidence": 85.0,
                "category": "Strategic",
                "priority": "immediate"
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
                        "title": "Monitor Regional Response",
                        "confidence": 85.0
                    }
                ]
            }
        }
    }
    
    try:
        # Generate report with both modules
        result = await modular_report_generator.generate_modular_report(
            topic="Pakistan Submarine Acquisition",
            data=sample_data,
            enabled_modules=["executivesummarymodule", "strategicrecommendationsmodule"],
            report_title="Pakistan Submarine Acquisition: Executive Summary Analysis"
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
    """Test Executive Summary module configuration."""
    print("\n🧪 Testing Executive Summary Module Configuration")
    
    generator = modular_report_generator
    
    # Test enabling/disabling modules
    generator.enable_module("executivesummarymodule", True)
    enabled_modules = [m.module_id for m in generator.get_enabled_modules()]
    print(f"✅ Enabled modules after configuration: {enabled_modules}")
    
    # Test module ordering
    generator.set_module_order("executivesummarymodule", 1)
    module = generator.get_module("executivesummarymodule")
    if module:
        print(f"✅ Module order set: {module.get_order()}")
    
    # Test custom configuration
    custom_config = {
        "enabled": True,
        "title": "📊 Custom Executive Summary",
        "description": "Custom executive summary for testing",
        "order": 1,
        "tooltips_enabled": True,
        "charts_enabled": True
    }
    
    generator.configure_module("executivesummarymodule", custom_config)
    module = generator.get_module("executivesummarymodule")
    if module:
        print(f"✅ Custom configuration applied: {module.get_title()}")
    
    return True


async def main():
    """Main test function."""
    print("🚀 Executive Summary Module Test Suite")
    print("=" * 50)
    
    # Test basic functionality
    test1_passed = test_executive_summary_module()
    
    # Test async functionality
    test2_passed = await test_executive_summary_report_generation()
    test3_passed = await test_module_configuration()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"✅ Executive Summary Module: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"✅ Report Generation: {'PASSED' if test2_passed else 'FAILED'}")
    print(f"✅ Module Configuration: {'PASSED' if test3_passed else 'FAILED'}")
    
    all_tests_passed = all([test1_passed, test2_passed, test3_passed])
    
    if all_tests_passed:
        print("\n🎉 All tests passed! Executive Summary module is working correctly.")
        return True
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
