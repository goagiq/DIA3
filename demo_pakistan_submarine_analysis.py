#!/usr/bin/env python3
"""
Pakistan Submarine Acquisition Analysis - Interactive Demo

This script demonstrates how to generate enhanced reports using the 
Modularized Enhanced Report System for your specific topic:
"Pakistan Submarine Acquisition Analysis and Deterrence Enhancement - 
Impact on geopolitics, trade, balance of power, escalation"

Usage Examples:
1. Full comprehensive report with all available modules
2. Strategic focus report (5 key strategic modules)
3. Custom module selection

Run this script to see the system in action!
"""

import asyncio
from pathlib import Path
from loguru import logger

# Import the modular report generator
from src.core.modular_report_generator import ModularReportGenerator


async def generate_strategic_focus_report():
    """
    Example 1: Generate a strategic-focused report
    Using only the most important strategic modules
    """
    logger.info("🎯 Generating Strategic Focus Report")
    
    # Initialize the report generator
    generator = ModularReportGenerator()
    
    # Your analysis topic
    topic = "Pakistan Submarine Acquisition Analysis and Deterrence Enhancement"
    
    # Prepare analysis data (this would come from your analysis)
    analysis_data = {
        "strategic_recommendations": {
            "intelligence_summary": {
                "total_insights": 18,
                "average_confidence": 87.5,
                "high_impact_insights": 9,
                "critical_findings": 4
            },
            "recommendations": {
                "immediate": [
                    {
                        "title": "Enhanced Maritime Domain Awareness",
                        "confidence": 0.95,
                        "impact": "High",
                        "timeline": "1-3 months",
                        "rationale": "Monitor submarine deployment patterns and regional response"
                    },
                    {
                        "title": "Diplomatic Engagement Framework",
                        "confidence": 0.88,
                        "impact": "Medium", 
                        "timeline": "2-6 months",
                        "rationale": "Prevent escalation through proactive dialogue"
                    }
                ],
                "short_term": [
                    {
                        "title": "Technology Assessment Initiative",
                        "confidence": 0.82,
                        "impact": "High",
                        "timeline": "6-12 months",
                        "rationale": "Evaluate Pakistani submarine capabilities and technology transfer"
                    }
                ],
                "long_term": [
                    {
                        "title": "Regional Balance Maintenance Strategy",
                        "confidence": 0.75,
                        "impact": "High",
                        "timeline": "2-5 years",
                        "rationale": "Maintain strategic stability while adapting to new capabilities"
                    }
                ]
            },
            "implementation_roadmap": {
                "phases": [
                    {
                        "phase": "Phase 1: Assessment",
                        "duration": "0-6 months",
                        "milestones": ["Intelligence gathering", "Capability assessment"],
                        "confidence": 0.92
                    },
                    {
                        "phase": "Phase 2: Response Planning", 
                        "duration": "6-18 months",
                        "milestones": ["Strategy development", "Alliance coordination"],
                        "confidence": 0.85
                    },
                    {
                        "phase": "Phase 3: Implementation",
                        "duration": "18-36 months", 
                        "milestones": ["Program execution", "Monitoring systems"],
                        "confidence": 0.78
                    }
                ]
            },
            "monitoring_plan": {
                "kpis": [
                    {"metric": "Intelligence Coverage", "target": "95%", "current": "78%", "status": "Improving"},
                    {"metric": "Response Readiness", "target": "90%", "current": "85%", "status": "Good"},
                    {"metric": "Regional Stability", "target": "80%", "current": "75%", "status": "Monitoring"},
                    {"metric": "Alliance Coordination", "target": "85%", "current": "82%", "status": "Good"}
                ],
                "evaluation_criteria": [
                    "Strategic objective achievement",
                    "Regional stability maintenance", 
                    "Intelligence collection effectiveness",
                    "Diplomatic engagement success"
                ]
            }
        }
    }
    
    # Select strategic modules (focused analysis)
    strategic_modules = [
        "strategicrecommendationsmodule"  # This module works and has comprehensive features
    ]
    
    logger.info(f"📊 Using {len(strategic_modules)} strategic modules")
    
    # Generate the report
    result = await generator.generate_modular_report(
        topic=topic,
        data=analysis_data,
        enabled_modules=strategic_modules,
        report_title="Pakistan Submarine Acquisition - Strategic Analysis"
    )
    
    if result["success"]:
        logger.info("✅ Strategic Focus Report Generated!")
        logger.info(f"📄 File: {result['filename']}")
        logger.info(f"📊 Size: {result['file_size']:,} bytes")
        logger.info(f"🔧 Modules: {', '.join(result['modules_used'])}")
        return result
    else:
        logger.error(f"❌ Failed: {result.get('error', 'Unknown error')}")
        return None


async def generate_multi_module_report():
    """
    Example 2: Generate a report with multiple working modules
    Using modules that we know work well together
    """
    logger.info("🔄 Generating Multi-Module Report")
    
    # Initialize the report generator
    generator = ModularReportGenerator()
    
    # Your analysis topic
    topic = "Pakistan Submarine Impact on Regional Balance and Escalation"
    
    # Extended analysis data for multiple modules
    analysis_data = {
        # Strategic Recommendations Module (we know this works)
        "strategic_recommendations": {
            "intelligence_summary": {
                "total_insights": 22,
                "average_confidence": 89.2,
                "high_impact_insights": 11,
                "critical_findings": 5
            },
            "recommendations": {
                "immediate": [
                    {
                        "title": "Enhanced Submarine Tracking",
                        "confidence": 0.93,
                        "impact": "High",
                        "timeline": "1-2 months",
                        "rationale": "Critical for understanding operational patterns"
                    }
                ],
                "short_term": [
                    {
                        "title": "Regional Alliance Coordination",
                        "confidence": 0.85,
                        "impact": "High", 
                        "timeline": "6-12 months",
                        "rationale": "Coordinate response with regional partners"
                    }
                ]
            }
        },
        
        # Regional Security Module
        "regional_security": {
            "security_dynamics": {
                "threat_assessment": "Moderate to high regional threat level",
                "deterrence_effectiveness": "Significantly enhanced Pakistani deterrence",
                "alliance_stability": "Mixed impact on existing security arrangements"
            },
            "security_implications": [
                "Enhanced Pakistan Navy second-strike capability",
                "Potential shift in India-Pakistan strategic balance",
                "Impact on broader regional security architecture",
                "Implications for maritime domain awareness"
            ],
            "mitigation_measures": [
                "Enhanced maritime confidence-building measures",
                "Technology proliferation monitoring",
                "Regional dialogue mechanisms",
                "Maritime security cooperation frameworks"
            ]
        },
        
        # Economic Analysis Module  
        "economic_analysis": {
            "cost_breakdown": {
                "acquisition_cost": "$3.8 billion",
                "technology_transfer": "$850 million", 
                "infrastructure_development": "$220 million",
                "training_and_support": "$180 million"
            },
            "economic_impact": {
                "defense_industry_growth": "28% increase in naval shipbuilding sector",
                "employment_generation": "6,200 direct and indirect jobs",
                "technology_spillovers": "Advanced manufacturing and metallurgy capabilities"
            },
            "financing_structure": {
                "chinese_loans": "72%",
                "pakistani_budget": "18%", 
                "other_financing": "10%"
            }
        }
    }
    
    # Select multiple working modules
    selected_modules = [
        "strategicrecommendationsmodule",
        "regionalsecuritymodule", 
        "economicanalysismodule"
    ]
    
    logger.info(f"📊 Using {len(selected_modules)} modules: {selected_modules}")
    
    # Generate the report
    result = await generator.generate_modular_report(
        topic=topic,
        data=analysis_data,
        enabled_modules=selected_modules,
        report_title="Pakistan Submarine Acquisition - Multi-Dimensional Analysis"
    )
    
    if result["success"]:
        logger.info("✅ Multi-Module Report Generated!")
        logger.info(f"📄 File: {result['filename']}")
        logger.info(f"📊 Size: {result['file_size']:,} bytes")
        logger.info(f"🔧 Modules: {', '.join(result['modules_used'])}")
        return result
    else:
        logger.error(f"❌ Failed: {result.get('error', 'Unknown error')}")
        return None


async def show_available_modules():
    """
    Example 3: Show what modules are available for use
    """
    logger.info("📋 Available Modules in the System")
    
    generator = ModularReportGenerator()
    available_modules = generator.get_available_modules()
    
    logger.info(f"📊 Total Available Modules: {len(available_modules)}")
    logger.info("📝 Module List:")
    
    for i, module_id in enumerate(available_modules, 1):
        # Get module details
        module = generator.get_module(module_id)
        title = module.get_title() if module else "Unknown"
        logger.info(f"  {i:2d}. {module_id} - {title}")
    
    return available_modules


async def generate_custom_report():
    """
    Example 4: How to create a custom report with your own module selection
    """
    logger.info("🎨 Custom Report Generation Example")
    
    # Show available modules
    generator = ModularReportGenerator()
    available_modules = generator.get_available_modules()
    
    logger.info("📋 You can select any combination of these modules:")
    for module_id in available_modules[:10]:  # Show first 10
        module = generator.get_module(module_id)
        title = module.get_title() if module else "Unknown"
        logger.info(f"  • {module_id} - {title}")
    
    # Example custom selection
    custom_modules = [
        "strategicrecommendationsmodule",
        "regionalsecuritymodule"
    ]
    
    # Basic data that works
    basic_data = {
        "strategic_recommendations": {
            "intelligence_summary": {
                "total_insights": 15,
                "average_confidence": 85.0,
                "high_impact_insights": 7
            }
        },
        "regional_security": {
            "security_dynamics": {
                "threat_assessment": "Regional security implications of submarine acquisition",
                "deterrence_effectiveness": "Enhanced deterrence capability"
            }
        }
    }
    
    logger.info(f"🎯 Generating custom report with: {custom_modules}")
    
    result = await generator.generate_modular_report(
        topic="Pakistan Submarine Acquisition - Custom Analysis",
        data=basic_data,
        enabled_modules=custom_modules,
        report_title="Custom Module Selection Example"
    )
    
    if result["success"]:
        logger.info("✅ Custom Report Generated!")
        logger.info(f"📄 File: {result['filename']}")
        return result
    else:
        logger.error(f"❌ Failed: {result.get('error', 'Unknown error')}")
        return None


async def main():
    """
    Main function demonstrating the Modularized Enhanced Report System
    """
    logger.info("🌟 Pakistan Submarine Acquisition Analysis - Interactive Demo")
    logger.info("🎯 Topic: Pakistan Submarine Acquisition Analysis and Deterrence Enhancement")
    logger.info("📊 Impact Analysis: Geopolitics, Trade, Balance of Power, Escalation")
    
    print("\n" + "="*80)
    print("🚀 MODULARIZED ENHANCED REPORT SYSTEM DEMONSTRATION")
    print("="*80)
    
    results = []
    
    # Example 1: Strategic Focus Report
    print("\n📍 EXAMPLE 1: Strategic Focus Report")
    print("-" * 50)
    result1 = await generate_strategic_focus_report()
    if result1:
        results.append(("Strategic Focus", result1))
    
    # Example 2: Multi-Module Report
    print("\n📍 EXAMPLE 2: Multi-Module Report") 
    print("-" * 50)
    result2 = await generate_multi_module_report()
    if result2:
        results.append(("Multi-Module", result2))
    
    # Example 3: Show Available Modules
    print("\n📍 EXAMPLE 3: Available Modules")
    print("-" * 50)
    available_modules = await show_available_modules()
    
    # Example 4: Custom Report
    print("\n📍 EXAMPLE 4: Custom Module Selection")
    print("-" * 50)
    result3 = await generate_custom_report()
    if result3:
        results.append(("Custom Selection", result3))
    
    # Summary
    print("\n" + "="*80)
    print("📊 DEMONSTRATION SUMMARY")
    print("="*80)
    
    if results:
        logger.info(f"✅ Successfully generated {len(results)} reports:")
        
        for report_type, result in results:
            logger.info(f"  📄 {report_type}: {result['filename']}")
            logger.info(f"      Size: {result['file_size']:,} bytes | Modules: {len(result['modules_used'])}")
        
        logger.info("\n🌐 How to View Reports:")
        logger.info("  1. Navigate to the 'Results' folder")
        logger.info("  2. Open any .html file in your web browser")
        logger.info("  3. Interact with charts and hover over elements for tooltips")
        
        logger.info("\n💡 How to Create Your Own Reports:")
        logger.info("  1. Import: from src.core.modular_report_generator import ModularReportGenerator")
        logger.info("  2. Initialize: generator = ModularReportGenerator()")
        logger.info("  3. Select modules: enabled_modules = ['module1', 'module2', ...]")
        logger.info("  4. Prepare data: analysis_data = {'key': 'value', ...}")
        logger.info("  5. Generate: await generator.generate_modular_report(topic, data, enabled_modules)")
        
        logger.info("\n🎯 Available Module Categories:")
        logger.info("  • Strategic: Strategic recommendations, strategic analysis")
        logger.info("  • Security: Regional security, risk assessment")  
        logger.info("  • Economic: Economic analysis, trade impact")
        logger.info("  • Operational: Implementation timeline, operational considerations")
        logger.info("  • Analytical: Forecasting, predictive analytics, scenario analysis")
        
    else:
        logger.warning("⚠️ No reports were generated successfully")
    
    print("\n🎉 Demonstration Complete!")
    print("📁 Check the 'Results' folder for generated HTML reports")


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())
