#!/usr/bin/env python3
"""
Simple Working Demo - Pakistan Submarine Analysis

This script demonstrates the Modularized Enhanced Report System using
only the modules that work properly to avoid async/sync and data issues.
"""

import asyncio
from pathlib import Path
from loguru import logger

from src.core.modular_report_generator import ModularReportGenerator


async def generate_working_report():
    """Generate a report using only working modules."""
    logger.info("🚀 Generating Working Report Demo")
    
    # Initialize the report generator
    generator = ModularReportGenerator()
    
    # Topic for the analysis
    topic = "Pakistan Submarine Acquisition Analysis and Deterrence Enhancement"
    
    # Data for working modules only
    analysis_data = {
        # Strategic Recommendations Module (we know this works)
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
                        "rationale": "Monitor submarine deployment patterns"
                    },
                    {
                        "title": "Diplomatic Engagement Framework",
                        "confidence": 0.88,
                        "impact": "Medium", 
                        "timeline": "2-6 months",
                        "rationale": "Prevent escalation through dialogue"
                    }
                ],
                "short_term": [
                    {
                        "title": "Technology Assessment Initiative",
                        "confidence": 0.82,
                        "impact": "High",
                        "timeline": "6-12 months",
                        "rationale": "Evaluate capabilities and transfer"
                    }
                ],
                "long_term": [
                    {
                        "title": "Regional Balance Maintenance Strategy",
                        "confidence": 0.75,
                        "impact": "High",
                        "timeline": "2-5 years",
                        "rationale": "Maintain strategic stability"
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
    
    # Use only the working module
    working_modules = ["strategicrecommendationsmodule"]
    
    logger.info(f"📊 Using {len(working_modules)} working modules")
    
    # Generate the report
    result = await generator.generate_modular_report(
        topic=topic,
        data=analysis_data,
        enabled_modules=working_modules,
        report_title="Pakistan Submarine Acquisition - Working Demo"
    )
    
    if result["success"]:
        logger.info("✅ Working Report Generated Successfully!")
        logger.info(f"📄 File: {result['filename']}")
        logger.info(f"📊 Size: {result['file_size']:,} bytes")
        logger.info(f"🔧 Modules: {', '.join(result['modules_used'])}")
        return result
    else:
        logger.error(f"❌ Failed: {result.get('error', 'Unknown error')}")
        return None


async def show_available_modules():
    """Show what modules are available."""
    logger.info("📋 Available Modules in the System")
    
    generator = ModularReportGenerator()
    available_modules = generator.get_available_modules()
    
    logger.info(f"📊 Total Available Modules: {len(available_modules)}")
    logger.info("📝 Module List:")
    
    for i, module_id in enumerate(available_modules, 1):
        module = generator.get_module(module_id)
        title = module.get_title() if module else "Unknown"
        logger.info(f"  {i:2d}. {module_id} - {title}")
    
    return available_modules


async def main():
    """Main function demonstrating the working system."""
    logger.info("🌟 Pakistan Submarine Analysis - Working Demo")
    logger.info("🎯 Topic: Pakistan Submarine Acquisition Analysis and Deterrence Enhancement")
    logger.info("📊 Impact Analysis: Geopolitics, Trade, Balance of Power, Escalation")
    
    print("\n" + "="*80)
    print("🚀 WORKING DEMONSTRATION")
    print("="*80)
    
    # Show available modules
    print("\n📍 Available Modules:")
    print("-" * 50)
    available_modules = await show_available_modules()
    
    # Generate working report
    print("\n📍 Generating Working Report:")
    print("-" * 50)
    result = await generate_working_report()
    
    # Summary
    print("\n" + "="*80)
    print("📊 DEMONSTRATION SUMMARY")
    print("="*80)
    
    if result:
        logger.info("✅ Successfully generated working report!")
        logger.info(f"📄 File: {result['filename']}")
        logger.info(f"📊 Size: {result['file_size']:,} bytes")
        logger.info(f"🔧 Modules: {len(result['modules_used'])}")
        
        logger.info("\n🌐 How to View Report:")
        logger.info("  1. Navigate to the 'Results' folder")
        logger.info("  2. Open the HTML file in your web browser")
        logger.info("  3. Interact with charts and hover for tooltips")
        
        logger.info("\n💡 Next Steps:")
        logger.info("  • The system is working with the Strategic Recommendations module")
        logger.info("  • Other modules need data structure fixes")
        logger.info("  • Use this as a template for your own reports")
        
    else:
        logger.error("❌ Report generation failed")
    
    print("\n🎉 Working Demo Complete!")
    print("📁 Check the 'Results' folder for the generated HTML report")


if __name__ == "__main__":
    asyncio.run(main())
