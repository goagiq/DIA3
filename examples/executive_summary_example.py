#!/usr/bin/env python3
"""
Executive Summary Module Example

Example application demonstrating the Executive Summary module functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modular_report_generator import modular_report_generator
from core.modules.executive_summary_module import ExecutiveSummaryModule


async def example_executive_summary_analysis():
    """Example: Executive Summary analysis for Pakistan submarine acquisition."""
    print("🚀 Example: Executive Summary Analysis")
    print("=" * 60)
    
    # Executive Summary specific data
    analysis_data = {
        "executive_summary": {
            "title": "Pakistan Submarine Acquisition: Executive Summary",
            "overview": "This comprehensive analysis examines the strategic implications of Pakistan's submarine acquisition program and its impact on regional security dynamics, economic considerations, and technological advancement.",
            "key_findings": [
                "Pakistan's submarine program represents a significant strategic capability enhancement with regional security implications",
                "The acquisition involves advanced technology transfer and substantial economic investment",
                "Regional security dynamics are likely to be affected by this strategic capability enhancement",
                "Economic and technological implications extend beyond immediate military considerations",
                "The program demonstrates Pakistan's commitment to naval modernization and strategic deterrence"
            ],
            "confidence_level": 87.5
        },
        "key_metrics": {
            "metrics": {
                "Strategic Impact Score": {
                    "value": "8.5/10",
                    "trend": "up",
                    "description": "High strategic impact on regional security dynamics"
                },
                "Economic Investment": {
                    "value": "$5.2B",
                    "trend": "stable",
                    "description": "Significant economic investment in defense modernization"
                },
                "Technology Transfer Level": {
                    "value": "Advanced",
                    "trend": "up",
                    "description": "Advanced technology transfer and capability enhancement"
                },
                "Regional Response Index": {
                    "value": "Moderate",
                    "trend": "neutral",
                    "description": "Moderate regional response and security implications"
                },
                "Operational Readiness": {
                    "value": "75%",
                    "trend": "up",
                    "description": "Improving operational readiness and capability"
                },
                "Strategic Deterrence": {
                    "value": "Enhanced",
                    "trend": "up",
                    "description": "Significantly enhanced strategic deterrence capability"
                }
            }
        },
        "trend_analysis": {
            "trends": [
                {
                    "title": "Increasing Regional Security Tensions",
                    "description": "Submarine acquisition likely to increase regional security tensions and strategic competition.",
                    "direction": "up",
                    "impact": "high"
                },
                {
                    "title": "Technology Advancement and Modernization",
                    "description": "Significant advancement in naval technology capabilities and modernization efforts.",
                    "direction": "up",
                    "impact": "medium"
                },
                {
                    "title": "Economic Burden and Resource Allocation",
                    "description": "Economic burden on defense budget and national resource allocation priorities.",
                    "direction": "down",
                    "impact": "medium"
                },
                {
                    "title": "Strategic Deterrence Enhancement",
                    "description": "Enhanced strategic deterrence capability and regional power projection.",
                    "direction": "up",
                    "impact": "high"
                },
                {
                    "title": "Regional Power Balance Shift",
                    "description": "Shifts in regional power balance and security dynamics.",
                    "direction": "neutral",
                    "impact": "high"
                }
            ]
        },
        "strategic_insights": [
            {
                "title": "Strategic Deterrence Enhancement",
                "description": "Submarine capability significantly enhances strategic deterrence posture and regional power projection capabilities.",
                "category": "Strategic",
                "priority": "high"
            },
            {
                "title": "Regional Power Balance Dynamics",
                "description": "Shifts regional power balance and security dynamics, requiring strategic response from regional actors.",
                "category": "Geopolitical",
                "priority": "high"
            },
            {
                "title": "Economic and Resource Implications",
                "description": "Long-term economic implications for defense spending and resource allocation priorities.",
                "category": "Economic",
                "priority": "medium"
            },
            {
                "title": "Technology Transfer and Capability Building",
                "description": "Advanced technology transfer contributes to indigenous capability building and modernization.",
                "category": "Technology",
                "priority": "medium"
            },
            {
                "title": "Regional Security Architecture",
                "description": "Implications for regional security architecture and multilateral cooperation frameworks.",
                "category": "Strategic",
                "priority": "high"
            }
        ],
        # Strategic recommendations data (for existing module)
        "strategic_recommendations": [
            {
                "title": "Monitor Regional Response and Reactions",
                "description": "Closely monitor regional responses and reactions to submarine acquisition program.",
                "rationale": "Critical for understanding security implications and strategic responses",
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
    
    # Configure modules
    custom_config = {
        "executivesummarymodule": {
            "enabled": True,
            "title": "📊 Pakistan Submarine Acquisition: Executive Summary",
            "description": "Comprehensive executive summary analysis of Pakistan's submarine acquisition program",
            "order": 1,
            "tooltips_enabled": True,
            "charts_enabled": True
        },
        "strategicrecommendationsmodule": {
            "enabled": True,
            "title": "🎯 Strategic Recommendations",
            "description": "Strategic recommendations based on executive summary analysis",
            "order": 100,
            "tooltips_enabled": True,
            "charts_enabled": False
        }
    }
    
    # Generate report
    result = await modular_report_generator.generate_modular_report(
        topic="Pakistan Submarine Acquisition",
        data=analysis_data,
        enabled_modules=["executivesummarymodule", "strategicrecommendationsmodule"],
        report_title="Pakistan Submarine Acquisition: Executive Summary Analysis",
        custom_config=custom_config
    )
    
    if result.get("success"):
        print("✅ Executive Summary analysis report generated successfully!")
        print(f"📄 File: {result.get('filename')}")
        print(f"📁 Path: {result.get('file_path')}")
        print(f"📊 Size: {result.get('file_size')} bytes")
        print(f"🔧 Modules Used: {', '.join(result.get('modules_used', []))}")
        return True
    else:
        print(f"❌ Failed to generate report: {result.get('error')}")
        return False


async def example_custom_executive_summary():
    """Example: Custom Executive Summary configuration."""
    print("\n🚀 Example: Custom Executive Summary Configuration")
    print("=" * 60)
    
    # Sample data for custom executive summary
    sample_data = {
        "executive_summary": {
            "title": "Custom Strategic Analysis: Executive Summary",
            "overview": "This is a custom executive summary demonstrating the flexibility and configurability of the Executive Summary module.",
            "key_findings": [
                "Custom analysis demonstrates module flexibility",
                "Configurable metrics and insights",
                "Advanced tooltip system integration"
            ],
            "confidence_level": 92.0
        },
        "key_metrics": {
            "metrics": {
                "Custom Metric 1": {
                    "value": "95%",
                    "trend": "up",
                    "description": "Custom metric for demonstration"
                },
                "Custom Metric 2": {
                    "value": "Excellent",
                    "trend": "stable",
                    "description": "Another custom metric"
                }
            }
        },
        "trend_analysis": {
            "trends": [
                {
                    "title": "Custom Trend Analysis",
                    "description": "Custom trend analysis for demonstration purposes.",
                    "direction": "up",
                    "impact": "medium"
                }
            ]
        },
        "strategic_insights": [
            {
                "title": "Custom Strategic Insight",
                "description": "Custom strategic insight demonstrating module capabilities.",
                "category": "Custom",
                "priority": "high"
            }
        ],
        # Minimal strategic recommendations data
        "strategic_recommendations": [
            {
                "title": "Custom Recommendation",
                "description": "Custom strategic recommendation.",
                "rationale": "Demonstrates custom configuration",
                "timeline": "1-2 years",
                "confidence": 90.0,
                "category": "Custom",
                "priority": "short_term"
            }
        ],
        "intelligence_summary": {
            "total_insights": 5,
            "average_confidence": 90.0,
            "high_impact_insights": 2
        },
        "implementation_roadmap": {
            "timeline_sections": {
                "Custom": [
                    {
                        "title": "Custom Recommendation",
                        "confidence": 90.0
                    }
                ]
            }
        }
    }
    
    # Custom configuration
    custom_config = {
        "executivesummarymodule": {
            "enabled": True,
            "title": "🔧 Custom Executive Summary",
            "description": "Demonstration of custom executive summary configuration",
            "order": 1,
            "tooltips_enabled": True,
            "charts_enabled": True,
            "custom_styles": {
                "background_color": "#2c3e50",
                "text_color": "#ecf0f1"
            }
        }
    }
    
    # Generate report with custom configuration
    result = await modular_report_generator.generate_modular_report(
        topic="Custom Executive Summary Demo",
        data=sample_data,
        enabled_modules=["executivesummarymodule", "strategicrecommendationsmodule"],
        report_title="Custom Executive Summary Demonstration",
        custom_config=custom_config
    )
    
    if result.get("success"):
        print("✅ Custom executive summary report generated successfully!")
        print(f"📄 File: {result.get('filename')}")
        print(f"📁 Path: {result.get('file_path')}")
        print(f"📊 Size: {result.get('file_size')} bytes")
        return True
    else:
        print(f"❌ Failed to generate custom report: {result.get('error')}")
        return False


async def example_module_management():
    """Example: Executive Summary module management."""
    print("\n🚀 Example: Executive Summary Module Management")
    print("=" * 60)
    
    generator = modular_report_generator
    
    # Show available modules
    available_modules = generator.get_available_modules()
    print(f"📊 Available modules: {available_modules}")
    
    # Show enabled modules
    enabled_modules = [m.module_id for m in generator.get_enabled_modules()]
    print(f"✅ Enabled modules: {enabled_modules}")
    
    # Configure Executive Summary module
    generator.configure_module("executivesummarymodule", {
        "title": "📊 Executive Summary (Configured)",
        "description": "This module has been configured for demonstration",
        "order": 1
    })
    
    # Get module metadata
    module = generator.get_module("executivesummarymodule")
    if module:
        metadata = module.get_module_metadata()
        print(f"🔧 Executive Summary module metadata: {metadata}")
    
    # Show generator summary
    summary = generator.get_generator_summary()
    print(f"📋 Generator summary: {summary}")
    
    return True


async def main():
    """Main example function."""
    print("🎯 Executive Summary Module Examples")
    print("=" * 60)
    
    # Run examples
    example1_passed = await example_executive_summary_analysis()
    example2_passed = await example_custom_executive_summary()
    example3_passed = await example_module_management()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Example Results Summary")
    print("=" * 60)
    print(f"✅ Executive Summary Analysis: {'PASSED' if example1_passed else 'FAILED'}")
    print(f"✅ Custom Configuration: {'PASSED' if example2_passed else 'FAILED'}")
    print(f"✅ Module Management: {'PASSED' if example3_passed else 'FAILED'}")
    
    all_examples_passed = all([example1_passed, example2_passed, example3_passed])
    
    if all_examples_passed:
        print("\n🎉 All examples completed successfully!")
        print("\n📁 Generated reports are available in the 'Results' directory.")
        print("🔧 The Executive Summary module is ready for use.")
        return True
    else:
        print("\n❌ Some examples failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    # Run the examples
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
