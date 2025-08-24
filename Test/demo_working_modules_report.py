#!/usr/bin/env python3
"""
Demo: Generate Enhanced Report with Working Modules

This script demonstrates how to generate a comprehensive enhanced report
using working modules for Pakistan Submarine Acquisition Analysis.
"""

import asyncio
from loguru import logger

from src.core.modular_report_generator import ModularReportGenerator


async def generate_working_report():
    """Generate a report with working modules."""
    logger.info("🚀 Starting Working Modules Report Generation")
    
    # Initialize the modular report generator
    generator = ModularReportGenerator()
    
    # Topic for the analysis
    topic = "Pakistan Submarine Acquisition Analysis and Deterrence Enhancement"
    
    # Working data structure for modules that are known to work
    working_data = {
        # Strategic Recommendations Module - This one works perfectly
        "strategic_recommendations": {
            "intelligence_summary": {
                "total_insights": 25,
                "average_confidence": 85.5,
                "high_impact_insights": 12,
                "critical_findings": 5
            },
            "recommendations": {
                "immediate": [
                    {
                        "title": "Enhanced Maritime Surveillance",
                        "confidence": 0.92,
                        "impact": "High",
                        "timeline": "1-3 months",
                        "rationale": "Monitor submarine deployment patterns and operational readiness"
                    },
                    {
                        "title": "Regional Dialogue Initiation",
                        "confidence": 0.85,
                        "impact": "Medium",
                        "timeline": "2-6 months",
                        "rationale": "Prevent escalation through diplomatic engagement"
                    }
                ],
                "short_term": [
                    {
                        "title": "Technology Assessment Program",
                        "confidence": 0.78,
                        "impact": "High",
                        "timeline": "6-12 months",
                        "rationale": "Evaluate technological capabilities and gaps"
                    },
                    {
                        "title": "Alliance Coordination Framework",
                        "confidence": 0.82,
                        "impact": "Medium",
                        "timeline": "8-15 months",
                        "rationale": "Coordinate response with regional partners"
                    }
                ],
                "long_term": [
                    {
                        "title": "Strategic Balance Maintenance",
                        "confidence": 0.70,
                        "impact": "High",
                        "timeline": "2-5 years",
                        "rationale": "Maintain regional strategic stability"
                    }
                ]
            },
            "implementation_roadmap": {
                "phases": [
                    {"phase": "Phase 1: Assessment", "duration": "0-6 months", "milestones": ["Intelligence gathering", "Capability assessment"], "confidence": 0.92},
                    {"phase": "Phase 2: Response Planning", "duration": "6-18 months", "milestones": ["Strategy development", "Alliance coordination"], "confidence": 0.85},
                    {"phase": "Phase 3: Implementation", "duration": "18-36 months", "milestones": ["Program execution", "Monitoring systems"], "confidence": 0.78}
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
        },
        
        # Enhanced Data Analysis Module - This one works
        "data_analysis_overview": {
            "title": "Enhanced Data Analysis Overview",
            "overview": "Comprehensive data analysis of Pakistan's submarine acquisition program performance and metrics.",
            "key_findings": [
                "160% increase in submarine fleet capability",
                "85% technology transfer success rate",
                "Significant improvement in maritime domain awareness",
                "Enhanced regional deterrence effectiveness"
            ],
            "data_quality_score": 88.5,
            "analysis_confidence": 85.0
        },
        "key_data_metrics": {
            "metrics": [
                {"name": "Fleet Size", "value": 13, "unit": "submarines", "category": "Capability"},
                {"name": "Technology Transfer", "value": 85, "unit": "percent", "category": "Development"},
                {"name": "Operational Readiness", "value": 78, "unit": "percent", "category": "Readiness"},
                {"name": "Regional Impact", "value": "High", "unit": "level", "category": "Strategic"}
            ],
            "categories": {
                "Capability": {"count": 5, "average": 82.5},
                "Development": {"count": 4, "average": 78.0},
                "Readiness": {"count": 3, "average": 75.0},
                "Strategic": {"count": 4, "average": 85.0}
            }
        },
        "performance_indicators": {
            "kpis": [
                {"indicator": "Submarine Availability", "target": 90, "current": 85, "status": "Good"},
                {"indicator": "Training Completion", "target": 100, "current": 95, "status": "Excellent"},
                {"indicator": "Technology Integration", "target": 80, "current": 75, "status": "Good"},
                {"indicator": "Operational Effectiveness", "target": 85, "current": 80, "status": "Good"}
            ]
        },
        "statistical_analysis": {
            "correlation_factors": [
                {"factor": "Regional tension", "correlation": 0.75},
                {"factor": "Economic development", "correlation": 0.45},
                {"factor": "Technology advancement", "correlation": 0.85}
            ],
            "trend_analysis": "Upward trajectory in capability enhancement",
            "confidence_intervals": {"lower": 0.65, "upper": 0.95}
        },
        
        # Geopolitical Impact Module - Fixed data structure
        "geopolitical_analysis": {
            "title": "Geopolitical Impact Analysis",
            "overview": "Analysis of Pakistan's submarine acquisition impact on regional and global geopolitics.",
            "key_actors": [
                {"name": "Pakistan", "role": "Acquiring nation", "influence_level": "High"},
                {"name": "China", "role": "Technology provider", "influence_level": "High"},
                {"name": "India", "role": "Regional competitor", "influence_level": "High"},
                {"name": "United States", "role": "Global power", "influence_level": "Medium"}
            ],
            "impact_level": "High",
            "confidence_score": 85.0
        },
        "regional_dynamics": {
            "regions": [
                {"region": "South Asia", "impact": "High", "dynamics": "Increased strategic competition"},
                {"region": "Indian Ocean", "impact": "High", "dynamics": "Enhanced maritime security"},
                {"region": "Asia-Pacific", "impact": "Medium", "dynamics": "Regional power shift"}
            ]
        },
        "strategic_partnerships": [
            {"partner": "China", "impact": "High", "nature": "Technology and financing provider"},
            {"partner": "Turkey", "impact": "Medium", "nature": "Defense cooperation expansion"},
            {"partner": "Saudi Arabia", "impact": "Medium", "nature": "Potential financing support"}
        ],
        "power_balance": {
            "regional_shift": "Significant enhancement of Pakistan's maritime capabilities",
            "global_implications": "Impact on Indo-Pacific strategic balance",
            "alliance_dynamics": "Strengthening of China-Pakistan partnership"
        },
        
        # Advanced Forecasting Module - This one works
        "advanced_forecasting": {
            "predictive_models": {
                "capability_enhancement": "85% probability of successful integration",
                "regional_response": "70% probability of counter-measures",
                "technology_development": "90% probability of continued advancement"
            },
            "scenario_forecasting": [
                {"timeframe": "2025", "scenario": "Full operational capability", "confidence": 0.85},
                {"timeframe": "2030", "scenario": "Enhanced regional deterrence", "confidence": 0.75},
                {"timeframe": "2035", "scenario": "Technology indigenization", "confidence": 0.65}
            ]
        },
        
        # Model Performance Module - This one works
        "model_performance": {
            "accuracy_metrics": {
                "prediction_accuracy": 0.82,
                "confidence_interval": 0.15,
                "model_reliability": 0.88
            },
            "validation_results": {
                "historical_validation": "85% accuracy on similar programs",
                "cross_validation": "Strong performance across scenarios",
                "expert_validation": "High agreement with expert assessments"
            }
        },
        
        # Strategic Capability Module - This one works
        "strategic_capability": {
            "capability_development": {
                "current_capabilities": "Coastal defense focus",
                "enhanced_capabilities": "Extended deterrence and domain control",
                "future_projections": "Regional maritime power status"
            },
            "strategic_planning": {
                "5_year_horizon": "Full submarine fleet integration",
                "10_year_horizon": "Advanced indigenous capabilities",
                "15_year_horizon": "Regional maritime leadership"
            }
        },
        
        # Predictive Analytics Module - This one works
        "predictive_analytics": {
            "feature_importance": {
                "technology_transfer": 0.35,
                "financing_stability": 0.25,
                "regional_response": 0.20,
                "operational_readiness": 0.20
            },
            "prediction_insights": [
                "High probability of successful program completion",
                "Moderate risk of regional escalation",
                "Strong potential for technology indigenization"
            ]
        }
    }
    
    # Use only the working modules
    working_modules = [
        "strategicrecommendationsmodule",
        "enhanceddataanalysismodule", 
        "geopoliticalimpactmodule",
        "advancedforecastingmodule",
        "modelperformancemodule",
        "strategiccapabilitymodule",
        "predictiveanalyticsmodule"
    ]
    
    logger.info(f"📊 Generating report with {len(working_modules)} working modules...")
    logger.info(f"📋 Working modules: {working_modules}")
    
    result = await generator.generate_modular_report(
        topic=topic,
        data=working_data,
        enabled_modules=working_modules
    )
    
    if result["success"]:
        logger.info("✅ Working Modules Report Generated Successfully!")
        logger.info(f"📄 File: {result['filename']}")
        logger.info(f"📊 File Size: {result['file_size']:,} bytes")
        logger.info(f"🔧 Modules Used: {len(result['modules_used'])}/{len(working_modules)}")
        logger.info(f"📋 Modules List: {', '.join(result['modules_used'])}")
        
        return result
    else:
        logger.error(f"❌ Report Generation Failed: {result.get('error', 'Unknown error')}")
        return None


async def show_available_modules():
    """Show all available modules and their status."""
    logger.info("🔍 Checking all available modules...")
    
    generator = ModularReportGenerator()
    all_modules = generator.get_available_modules()
    
    logger.info(f"📋 Total available modules: {len(all_modules)}")
    
    # Test each module to see if it works
    working_modules = []
    problematic_modules = []
    
    for module_id in all_modules:
        try:
            module = generator.get_module(module_id)
            required_keys = module.get_required_data_keys()
            logger.info(f"✅ {module_id}: Requires {len(required_keys)} data keys")
            working_modules.append(module_id)
        except Exception as e:
            logger.error(f"❌ {module_id}: Error - {e}")
            problematic_modules.append(module_id)
    
    logger.info(f"✅ Working modules: {len(working_modules)}")
    logger.info(f"❌ Problematic modules: {len(problematic_modules)}")
    
    return working_modules, problematic_modules


async def main():
    """Main function to run the working modules demo."""
    logger.info("🌟 Pakistan Submarine Acquisition - Working Modules Demo")
    logger.info("📝 This demo generates a report using modules that are known to work")
    
    # First, show available modules
    working_modules, problematic_modules = await show_available_modules()
    
    # Generate report with working modules
    result = await generate_working_report()
    
    if result:
        logger.info("🎉 Demo completed successfully!")
        logger.info(f"📁 Report saved to: {result['filename']}")
        logger.info("💡 Open the HTML file in your browser to view the interactive report")
        
        # Provide guidance on fixing problematic modules
        if problematic_modules:
            logger.info("🔧 To fix problematic modules, you need to:")
            logger.info("   1. Check the required data keys for each module")
            logger.info("   2. Provide properly formatted data")
            logger.info("   3. Fix any code issues in the module files")
    else:
        logger.error("💥 Demo failed to complete")


if __name__ == "__main__":
    asyncio.run(main())
