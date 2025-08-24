#!/usr/bin/env python3
"""
Demo: Generate Enhanced Report with Selected Modules

This script demonstrates how to generate targeted enhanced reports
using specific modules for Pakistan Submarine Acquisition Analysis.
Shows different combinations for different analysis purposes.
"""

import asyncio
from loguru import logger
from pathlib import Path

from src.core.modular_report_generator import ModularReportGenerator


async def generate_strategic_focus_report():
    """Generate a strategic-focused report with key strategic modules."""
    logger.info("🎯 Generating Strategic Focus Report")
    
    # Initialize the modular report generator
    generator = ModularReportGenerator()
    
    # Topic for the analysis
    topic = "Pakistan Submarine Acquisition - Strategic Analysis Focus"
    
    # Strategic-focused data
    strategic_data = {
        # Executive Summary Module
        "executive_summary": {
            "key_findings": [
                "Pakistan's submarine acquisition significantly enhances regional deterrence capabilities",
                "Strategic implications extend beyond regional balance to global maritime security",
                "Technology transfer agreements provide long-term capability development"
            ],
            "strategic_implications": [
                "Enhanced second-strike capability",
                "Improved maritime domain awareness",
                "Strengthened deterrence posture"
            ],
            "recommendations": [
                "Monitor technological capabilities development",
                "Assess regional response patterns",
                "Evaluate alliance implications"
            ]
        },
        
        # Geopolitical Impact Module
        "geopolitical_impact": {
            "regional_dynamics": {
                "india_pakistan_relations": "Increased tension due to enhanced deterrence capability",
                "china_involvement": "Strategic partnership through technology transfer and financing",
                "us_interests": "Concerns about regional stability and alliance implications"
            },
            "alliance_implications": {
                "china_pakistan": "Strengthened through submarine program",
                "india_us": "Enhanced cooperation in response to regional changes"
            }
        },
        
        # Balance of Power Module
        "balance_of_power": {
            "military_capabilities": {
                "submarine_fleet_size": {"before": 5, "after": 13, "percentage_increase": 160},
                "deterrence_capability": {"nuclear": "Enhanced", "conventional": "Significantly improved"}
            },
            "regional_responses": {
                "india_response": "Accelerated submarine acquisition program",
                "china_support": "Continued technology transfer and financing"
            }
        },
        
        # Strategic Analysis Module
        "strategic_analysis": {
            "doctrine_implications": {
                "naval_doctrine": "Shift from coastal defense to extended deterrence",
                "nuclear_doctrine": "Enhanced credible minimum deterrence"
            },
            "capability_gaps": [
                "Advanced sonar systems",
                "Long-range cruise missiles"
            ]
        },
        
        # Strategic Recommendations Module
        "strategic_recommendations": {
            "intelligence_summary": {
                "total_insights": 15,
                "average_confidence": 85.5,
                "high_impact_insights": 8
            },
            "recommendations": {
                "immediate": [
                    {
                        "title": "Enhanced Maritime Surveillance",
                        "confidence": 0.92,
                        "impact": "High",
                        "timeline": "1-3 months"
                    }
                ],
                "short_term": [
                    {
                        "title": "Technology Assessment Program",
                        "confidence": 0.78,
                        "impact": "High",
                        "timeline": "6-12 months"
                    }
                ]
            }
        }
    }
    
    # Selected modules for strategic focus
    strategic_modules = [
        "executivesummarymodule",
        "geopoliticalimpactmodule", 
        "balanceofpowermodule",
        "strategicanalysismodule",
        "strategicrecommendationsmodule"
    ]
    
    logger.info(f"📊 Using {len(strategic_modules)} strategic modules")
    
    result = await generator.generate_modular_report(
        topic=topic,
        data=strategic_data,
        enabled_modules=strategic_modules
    )
    
    return result, "Strategic Focus"


async def generate_economic_focus_report():
    """Generate an economic-focused report with financial and trade modules."""
    logger.info("💰 Generating Economic Focus Report")
    
    # Initialize the modular report generator
    generator = ModularReportGenerator()
    
    # Topic for the analysis
    topic = "Pakistan Submarine Acquisition - Economic Impact Analysis"
    
    # Economic-focused data
    economic_data = {
        # Executive Summary Module
        "executive_summary": {
            "key_findings": [
                "Economic implications total approximately $4-6 billion over 15 years",
                "Significant impact on Pakistani defense industry development",
                "Technology transfer creates long-term economic benefits"
            ]
        },
        
        # Trade Impact Module
        "trade_impact": {
            "economic_implications": {
                "total_investment": "$4.5 billion",
                "annual_maintenance": "$150 million",
                "technology_transfer_value": "$800 million"
            },
            "trade_relationships": {
                "china_pakistan_trade": "Expected 15% increase in defense trade",
                "technology_sectors": "Significant boost to Pakistani shipbuilding industry"
            }
        },
        
        # Economic Analysis Module
        "economic_analysis": {
            "cost_breakdown": {
                "acquisition_cost": "$3.5 billion",
                "technology_transfer": "$800 million",
                "infrastructure": "$200 million"
            },
            "economic_impact": {
                "defense_industry_growth": "25% increase in shipbuilding sector",
                "employment_generation": "5,000 direct and indirect jobs"
            }
        },
        
        # Acquisition Programs Module
        "acquisition_programs": {
            "program_details": {
                "program_name": "Pakistan Navy Submarine Acquisition Program",
                "total_cost": "$4.5 billion",
                "timeline": "2015-2025"
            },
            "supplier_information": {
                "primary_supplier": "China Shipbuilding Industry Corporation",
                "financing": "Chinese loans and Pakistani budget"
            }
        },
        
        # Risk Assessment Module
        "risk_assessment": {
            "economic_risks": [
                {"risk": "Cost overruns", "probability": 0.4, "impact": "Medium"},
                {"risk": "Financing challenges", "probability": 0.3, "impact": "High"}
            ],
            "mitigation_strategies": [
                "Diversified financing mechanisms",
                "Enhanced cost control measures"
            ]
        }
    }
    
    # Selected modules for economic focus
    economic_modules = [
        "executivesummarymodule",
        "tradeimpactmodule",
        "economicanalysismodule",
        "acquisitionprogramsmodule",
        "riskassessmentmodule"
    ]
    
    logger.info(f"📊 Using {len(economic_modules)} economic modules")
    
    result = await generator.generate_modular_report(
        topic=topic,
        data=economic_data,
        enabled_modules=economic_modules
    )
    
    return result, "Economic Focus"


async def generate_security_focus_report():
    """Generate a security-focused report with risk and regional security modules."""
    logger.info("🛡️ Generating Security Focus Report")
    
    # Initialize the modular report generator
    generator = ModularReportGenerator()
    
    # Topic for the analysis
    topic = "Pakistan Submarine Acquisition - Security Impact Analysis"
    
    # Security-focused data
    security_data = {
        # Executive Summary Module
        "executive_summary": {
            "key_findings": [
                "Enhanced deterrence capability affects regional security dynamics",
                "Potential for escalation requires careful monitoring",
                "Regional response patterns indicate mixed reactions"
            ]
        },
        
        # Risk Assessment Module
        "risk_assessment": {
            "security_risks": [
                {"risk": "Technology proliferation", "probability": 0.3, "impact": "High"},
                {"risk": "Regional arms race", "probability": 0.7, "impact": "Medium"},
                {"risk": "Operational accidents", "probability": 0.2, "impact": "High"}
            ],
            "mitigation_strategies": [
                "Enhanced safety protocols and training programs",
                "Regional confidence-building measures"
            ]
        },
        
        # Regional Security Module
        "regional_security": {
            "security_dynamics": {
                "threat_assessment": "Moderate to high regional threat level",
                "deterrence_effectiveness": "Significantly enhanced"
            },
            "security_implications": [
                "Enhanced Pakistan Navy deterrence capability",
                "Potential for regional arms competition"
            ]
        },
        
        # Regional Sentiment Module
        "regional_sentiment": {
            "public_opinion": {
                "pakistan": {"support": 0.78, "concern": 0.22},
                "india": {"support": 0.15, "concern": 0.85},
                "china": {"support": 0.85, "concern": 0.15}
            },
            "expert_opinions": [
                {"expert": "Regional Security Analysts", "sentiment": "Cautiously optimistic"}
            ]
        },
        
        # Scenario Analysis Module
        "scenario_analysis": {
            "scenario_overview": {
                "scenarios": [
                    {"scenario": "Optimistic", "probability": 0.30, "impact": "High"},
                    {"scenario": "Baseline", "probability": 0.50, "impact": "Medium"},
                    {"scenario": "Pessimistic", "probability": 0.20, "impact": "Low"}
                ]
            }
        }
    }
    
    # Selected modules for security focus
    security_modules = [
        "executivesummarymodule",
        "riskassessmentmodule",
        "regionalsecuritymodule",
        "regionalsentimentmodule",
        "scenarioanalysismodule"
    ]
    
    logger.info(f"📊 Using {len(security_modules)} security modules")
    
    result = await generator.generate_modular_report(
        topic=topic,
        data=security_data,
        enabled_modules=security_modules
    )
    
    return result, "Security Focus"


async def generate_technical_focus_report():
    """Generate a technical-focused report with operational and capability modules."""
    logger.info("⚙️ Generating Technical Focus Report")
    
    # Initialize the modular report generator
    generator = ModularReportGenerator()
    
    # Topic for the analysis
    topic = "Pakistan Submarine Acquisition - Technical Capabilities Analysis"
    
    # Technical-focused data
    technical_data = {
        # Executive Summary Module
        "executive_summary": {
            "key_findings": [
                "Significant technological advancement in submarine capabilities",
                "Technology transfer enables long-term indigenous development",
                "Operational readiness projected for 2025"
            ]
        },
        
        # Operational Considerations Module
        "operational_considerations": {
            "deployment_strategy": {
                "primary_areas": ["Arabian Sea", "Indian Ocean"],
                "patrol_patterns": "Extended deterrence missions"
            },
            "maintenance_requirements": {
                "shore_facilities": "Karachi Naval Dockyard expansion",
                "technical_support": "Chinese technical assistance"
            }
        },
        
        # Strategic Capability Module
        "strategic_capability": {
            "capability_development": {
                "current_capabilities": "Coastal defense focus",
                "enhanced_capabilities": "Extended deterrence and domain control"
            }
        },
        
        # Advanced Forecasting Module
        "advanced_forecasting": {
            "predictive_models": {
                "capability_enhancement": "85% probability of successful integration",
                "technology_development": "90% probability of continued advancement"
            }
        },
        
        # Model Performance Module
        "model_performance": {
            "accuracy_metrics": {
                "prediction_accuracy": 0.82,
                "model_reliability": 0.88
            }
        }
    }
    
    # Selected modules for technical focus
    technical_modules = [
        "executivesummarymodule",
        "operationalconsiderationsmodule",
        "strategiccapabilitymodule",
        "advancedforecastingmodule",
        "modelperformancemodule"
    ]
    
    logger.info(f"📊 Using {len(technical_modules)} technical modules")
    
    result = await generator.generate_modular_report(
        topic=topic,
        data=technical_data,
        enabled_modules=technical_modules
    )
    
    return result, "Technical Focus"


async def main():
    """Main function to run all targeted report demos."""
    logger.info("🌟 Pakistan Submarine Acquisition - Targeted Analysis Demos")
    logger.info("📝 This demo generates multiple reports using different module combinations")
    
    # Store results
    results = []
    
    # Generate different focused reports
    demos = [
        generate_strategic_focus_report,
        generate_economic_focus_report,
        generate_security_focus_report,
        generate_technical_focus_report
    ]
    
    for demo_func in demos:
        try:
            result, focus_type = await demo_func()
            if result and result["success"]:
                results.append((result, focus_type))
                logger.info(f"✅ {focus_type} Report: {result['filename']}")
                logger.info(f"📊 Modules: {len(result['modules_used'])}, Size: {result['file_size']:,} bytes")
            else:
                logger.error(f"❌ {focus_type} Report failed")
        except Exception as e:
            logger.error(f"💥 Error generating report: {e}")
    
    # Summary
    logger.info("\n🎉 Demo Summary:")
    logger.info(f"📋 Generated {len(results)} targeted reports:")
    
    for result, focus_type in results:
        logger.info(f"  📄 {focus_type}: {result['filename']}")
        logger.info(f"      📊 {len(result['modules_used'])} modules, {result['file_size']:,} bytes")
    
    logger.info("\n💡 Usage Guide:")
    logger.info("  • Strategic Focus: Use for high-level policy analysis")
    logger.info("  • Economic Focus: Use for financial impact assessment")
    logger.info("  • Security Focus: Use for threat and risk analysis")
    logger.info("  • Technical Focus: Use for capability assessment")
    logger.info("\n📁 All reports saved to Results/ directory")
    logger.info("🌐 Open the HTML files in your browser to view interactive reports")


if __name__ == "__main__":
    asyncio.run(main())
