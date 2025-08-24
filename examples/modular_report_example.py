#!/usr/bin/env python3
"""
Modular Report System Example

Example application demonstrating the modular enhanced report system.
Shows how to generate reports with configurable components.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.modular_report_generator import modular_report_generator
from core.modules.strategic_recommendations_module import StrategicRecommendationsModule


async def example_pakistan_submarine_analysis():
    """Example: Pakistan submarine acquisition analysis."""
    print("🚀 Example: Pakistan Submarine Acquisition Analysis")
    print("=" * 60)
    
    # Pakistan submarine specific data
    analysis_data = {
        "strategic_recommendations": [
            {
                "title": "Accelerate Submarine Crew Training",
                "description": "Implement intensive training programs for submarine crews to ensure operational readiness.",
                "rationale": "Critical for operational effectiveness and safety",
                "timeline": "0-6 months",
                "confidence": 90.0,
                "category": "Operations",
                "priority": "immediate"
            },
            {
                "title": "Implement Enhanced Maritime Surveillance",
                "description": "Deploy advanced maritime surveillance systems to monitor regional naval activities.",
                "rationale": "Critical for maritime security and threat detection",
                "timeline": "0-3 months",
                "confidence": 85.0,
                "category": "Security",
                "priority": "immediate"
            },
            {
                "title": "Establish Crisis Communication Channels",
                "description": "Create dedicated communication channels with key regional partners for rapid crisis response.",
                "rationale": "Essential for crisis management and escalation prevention",
                "timeline": "0-2 months",
                "confidence": 80.0,
                "category": "Diplomacy",
                "priority": "immediate"
            },
            {
                "title": "Enhance Cybersecurity Infrastructure",
                "description": "Strengthen cybersecurity capabilities to protect critical defense systems.",
                "rationale": "Protects against cyber threats and espionage",
                "timeline": "6-12 months",
                "confidence": 85.0,
                "category": "Technology",
                "priority": "short_term"
            },
            {
                "title": "Diversify Defense Supply Chains",
                "description": "Reduce dependency on single suppliers by developing multiple defense partnerships.",
                "rationale": "Reduces supply chain vulnerabilities and dependencies",
                "timeline": "6-18 months",
                "confidence": 80.0,
                "category": "Economic",
                "priority": "short_term"
            },
            {
                "title": "Develop Regional Security Partnerships",
                "description": "Establish formal security partnerships with key regional allies.",
                "rationale": "Strengthens regional security architecture and collective defense",
                "timeline": "3-12 months",
                "confidence": 75.0,
                "category": "Strategic",
                "priority": "short_term"
            },
            {
                "title": "Implement AI-Enhanced Defense Systems",
                "description": "Integrate artificial intelligence into defense systems for enhanced decision-making.",
                "rationale": "Maintains technological edge and operational superiority",
                "timeline": "5-10 years",
                "confidence": 80.0,
                "category": "Technology",
                "priority": "long_term"
            },
            {
                "title": "Develop Indigenous Defense Industry",
                "description": "Build domestic defense manufacturing capabilities to reduce external dependencies.",
                "rationale": "Ensures strategic autonomy and economic benefits",
                "timeline": "3-7 years",
                "confidence": 75.0,
                "category": "Economic",
                "priority": "long_term"
            },
            {
                "title": "Establish Regional Security Architecture",
                "description": "Develop comprehensive regional security framework with multilateral cooperation.",
                "rationale": "Creates sustainable regional security environment",
                "timeline": "2-5 years",
                "confidence": 70.0,
                "category": "Strategic",
                "priority": "long_term"
            }
        ],
        "intelligence_summary": {
            "total_insights": 25,
            "average_confidence": 82.5,
            "high_impact_insights": 12
        },
        "implementation_roadmap": {
            "timeline_sections": {
                "Immediate": [
                    {
                        "title": "Accelerate Submarine Crew Training",
                        "confidence": 90.0
                    },
                    {
                        "title": "Implement Enhanced Maritime Surveillance",
                        "confidence": 85.0
                    },
                    {
                        "title": "Establish Crisis Communication Channels",
                        "confidence": 80.0
                    }
                ],
                "Short Term": [
                    {
                        "title": "Enhance Cybersecurity Infrastructure",
                        "confidence": 85.0
                    },
                    {
                        "title": "Diversify Defense Supply Chains",
                        "confidence": 80.0
                    },
                    {
                        "title": "Develop Regional Security Partnerships",
                        "confidence": 75.0
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
                    },
                    {
                        "title": "Establish Regional Security Architecture",
                        "confidence": 70.0
                    }
                ]
            }
        },
        "monitoring_plan": {
            "Performance Metrics": [
                "Submarine operational readiness",
                "Maritime surveillance coverage",
                "Crisis response time",
                "Cybersecurity incident rate"
            ],
            "Strategic Metrics": [
                "Regional security index",
                "Partnership effectiveness",
                "Technology advancement rate",
                "Supply chain resilience"
            ],
            "Economic Metrics": [
                "Defense industry growth",
                "Cost efficiency improvements",
                "Economic impact assessment",
                "Resource allocation optimization"
            ]
        }
    }
    
    # Configure modules
    custom_config = {
        "strategicrecommendationsmodule": {
            "enabled": True,
            "title": "🎯 Pakistan Submarine Acquisition: Strategic Recommendations",
            "description": "Comprehensive strategic recommendations for Pakistan's submarine acquisition program",
            "order": 100,
            "tooltips_enabled": True,
            "charts_enabled": False
        }
    }
    
    # Generate report
    result = await modular_report_generator.generate_modular_report(
        topic="Pakistan Submarine Acquisition",
        data=analysis_data,
        report_title="Pakistan Submarine Acquisition: Modular Enhanced Analysis",
        custom_config=custom_config
    )
    
    if result.get("success"):
        print("✅ Pakistan submarine analysis report generated successfully!")
        print(f"📄 File: {result.get('filename')}")
        print(f"📁 Path: {result.get('file_path')}")
        print(f"📊 Size: {result.get('file_size')} bytes")
        print(f"🔧 Modules Used: {', '.join(result.get('modules_used', []))}")
        return True
    else:
        print(f"❌ Failed to generate report: {result.get('error')}")
        return False


async def example_custom_configuration():
    """Example: Custom module configuration."""
    print("\n🚀 Example: Custom Module Configuration")
    print("=" * 60)
    
    # Sample data
    sample_data = {
        "strategic_recommendations": [
            {
                "title": "Custom Strategic Initiative",
                "description": "A custom strategic initiative for demonstration purposes.",
                "rationale": "Demonstrates custom configuration capabilities",
                "timeline": "1-2 years",
                "confidence": 85.0,
                "category": "Demonstration",
                "priority": "short_term"
            }
        ],
        "intelligence_summary": {
            "total_insights": 5,
            "average_confidence": 85.0,
            "high_impact_insights": 2
        },
        "implementation_roadmap": {
            "timeline_sections": {
                "Custom Timeline": [
                    {
                        "title": "Custom Strategic Initiative",
                        "confidence": 85.0
                    }
                ]
            }
        }
    }
    
    # Custom configuration
    custom_config = {
        "strategicrecommendationsmodule": {
            "enabled": True,
            "title": "🔧 Custom Strategic Analysis",
            "description": "Demonstration of custom module configuration",
            "order": 50,
            "tooltips_enabled": True,
            "charts_enabled": False,
            "custom_styles": {
                "background_color": "#2c3e50",
                "text_color": "#ecf0f1"
            }
        }
    }
    
    # Generate report with custom configuration
    result = await modular_report_generator.generate_modular_report(
        topic="Custom Configuration Demo",
        data=sample_data,
        report_title="Custom Configuration Demonstration",
        custom_config=custom_config
    )
    
    if result.get("success"):
        print("✅ Custom configuration report generated successfully!")
        print(f"📄 File: {result.get('filename')}")
        print(f"📁 Path: {result.get('file_path')}")
        print(f"📊 Size: {result.get('file_size')} bytes")
        return True
    else:
        print(f"❌ Failed to generate custom report: {result.get('error')}")
        return False


async def example_module_management():
    """Example: Module management and configuration."""
    print("\n🚀 Example: Module Management")
    print("=" * 60)
    
    generator = modular_report_generator
    
    # Show available modules
    available_modules = generator.get_available_modules()
    print(f"📊 Available modules: {available_modules}")
    
    # Show enabled modules
    enabled_modules = [m.module_id for m in generator.get_enabled_modules()]
    print(f"✅ Enabled modules: {enabled_modules}")
    
    # Configure module
    generator.configure_module("strategicrecommendationsmodule", {
        "title": "🎯 Strategic Recommendations (Configured)",
        "description": "This module has been configured for demonstration",
        "order": 25
    })
    
    # Get module metadata
    module = generator.get_module("strategicrecommendationsmodule")
    if module:
        metadata = module.get_module_metadata()
        print(f"🔧 Module metadata: {metadata}")
    
    # Show generator summary
    summary = generator.get_generator_summary()
    print(f"📋 Generator summary: {summary}")
    
    return True


async def main():
    """Main example function."""
    print("🎯 Modular Report System Examples")
    print("=" * 60)
    
    # Run examples
    example1_passed = await example_pakistan_submarine_analysis()
    example2_passed = await example_custom_configuration()
    example3_passed = await example_module_management()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Example Results Summary")
    print("=" * 60)
    print(f"✅ Pakistan Submarine Analysis: {'PASSED' if example1_passed else 'FAILED'}")
    print(f"✅ Custom Configuration: {'PASSED' if example2_passed else 'FAILED'}")
    print(f"✅ Module Management: {'PASSED' if example3_passed else 'FAILED'}")
    
    all_examples_passed = all([example1_passed, example2_passed, example3_passed])
    
    if all_examples_passed:
        print("\n🎉 All examples completed successfully!")
        print("\n📁 Generated reports are available in the 'Results' directory.")
        print("🔧 The modular report system is ready for use.")
        return True
    else:
        print("\n❌ Some examples failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    # Run the examples
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
