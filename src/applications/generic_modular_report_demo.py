#!/usr/bin/env python3
"""
Generic Modular Report Demo

This script demonstrates how to use the modular report system with any topic.
It provides a flexible interface for generating comprehensive reports with
configurable modules and data structures.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.modular_report_generator import modular_report_generator


class GenericModularReportDemo:
    """Generic demo for modular report generation with any topic."""
    
    def __init__(self):
        """Initialize the demo."""
        self.generator = modular_report_generator
        self.results_dir = Path("Results")
        self.results_dir.mkdir(exist_ok=True)
    
    def get_sample_data_structure(self, topic: str) -> Dict[str, Any]:
        """Generate a sample data structure for any topic."""
        return {
            # Executive Summary Module
            "executive_summary": {
                "key_metrics": {
                    "total_investment": 5000000000,
                    "timeline_years": 5,
                    "success_probability": 0.75,
                    "risk_level": "Medium"
                },
                "trend_analysis": {
                    "capability_trend": f"Significant enhancement in {topic.lower()} capabilities",
                    "regional_trend": "Increased strategic competition",
                    "economic_trend": "Defense sector growth and technology development",
                    "technology_trend": "Accelerated indigenous capability development"
                },
                "executive_strategic_insights": [
                    f"Enhanced {topic.lower()} capability establishment",
                    "Regional domain control improvement",
                    "Technology indigenization advancement",
                    "Strategic partnership strengthening"
                ]
            },
            
            # Strategic Analysis Module
            "strategic_analysis": {
                "strategic_objectives": [
                    f"Enhance {topic.lower()} capabilities",
                    "Improve regional deterrence",
                    "Strengthen strategic partnerships",
                    "Develop indigenous technology"
                ],
                "strategic_insights": {
                    "primary_drivers": f"{topic} acquisition and modernization",
                    "secondary_factors": "Regional security dynamics",
                    "long_term_implications": "Strategic balance shift",
                    "immediate_actions": "Capability development and training"
                },
                "competitive_analysis": {
                    "strengths": ["Advanced technology", "Strategic partnerships", "Regional expertise"],
                    "weaknesses": ["Resource constraints", "Technology gaps", "Operational challenges"],
                    "opportunities": ["Technology transfer", "Regional cooperation", "Capability enhancement"],
                    "threats": ["Regional tensions", "Resource competition", "Technology proliferation"]
                }
            },
            
            # Enhanced Data Analysis Module
            "enhanced_data_analysis": {
                "data_sources": [
                    "Government reports",
                    "Industry analysis",
                    "Academic research",
                    "Expert interviews"
                ],
                "analytical_methods": [
                    "Statistical analysis",
                    "Trend analysis",
                    "Comparative analysis",
                    "Predictive modeling"
                ],
                "key_findings": [
                    f"{topic} shows significant growth potential",
                    "Technology advancement is accelerating",
                    "Regional dynamics are evolving",
                    "Strategic partnerships are critical"
                ]
            },
            
            # Geopolitical Impact Module
            "geopolitical_impact": {
                "regional_dynamics": {
                    "power_balance": "Shifting towards multipolarity",
                    "alliance_structures": "Evolving partnerships",
                    "conflict_probability": 0.3,
                    "cooperation_opportunities": 0.7
                },
                "global_implications": {
                    "international_order": "Gradual transformation",
                    "norms_evolution": "Technology-driven changes",
                    "institutional_adaptation": "Required for stability"
                },
                "strategic_recommendations": [
                    "Enhance diplomatic engagement",
                    "Strengthen multilateral cooperation",
                    "Develop confidence-building measures",
                    "Promote technology sharing"
                ]
            },
            
            # Trade Impact Module
            "trade_impact": {
                "trade_flows": {
                    "imports": {
                        "technology": 2000000000,
                        "equipment": 1500000000,
                        "services": 500000000
                    },
                    "exports": {
                        "manufactured_goods": 1000000000,
                        "services": 800000000,
                        "raw_materials": 200000000
                    }
                },
                "economic_effects": {
                    "gdp_impact": "2.5% increase",
                    "employment_creation": "15,000 jobs",
                    "technology_transfer": "Significant advancement",
                    "industrial_development": "Comprehensive growth"
                }
            },
            
            # Balance of Power Module
            "balance_of_power": {
                "power_metrics": {
                    "military_capability": 0.75,
                    "economic_strength": 0.65,
                    "technological_advantage": 0.70,
                    "strategic_influence": 0.60
                },
                "regional_assessment": {
                    "current_balance": "Evolving multipolarity",
                    "trend_direction": "Towards equilibrium",
                    "stability_factors": ["Economic interdependence", "Diplomatic engagement"],
                    "destabilizing_factors": ["Resource competition", "Technology gaps"]
                }
            },
            
            # Regional Sentiment Module
            "regional_sentiment": {
                "sentiment_analysis": {
                    "overall_sentiment": "Cautiously optimistic",
                    "confidence_level": 0.65,
                    "concern_level": 0.35,
                    "support_level": 0.70
                },
                "stakeholder_perceptions": {
                    "government": "Strongly supportive",
                    "business": "Moderately supportive",
                    "public": "Cautiously supportive",
                    "international": "Mixed reactions"
                }
            },
            
            # Implementation Timeline Module
            "implementation_timeline": {
                "phases": [
                    {
                        "phase": "Phase 1: Planning",
                        "duration": "6 months",
                        "key_activities": ["Feasibility study", "Stakeholder consultation"],
                        "milestones": ["Study completion", "Approval obtained"]
                    },
                    {
                        "phase": "Phase 2: Development",
                        "duration": "18 months",
                        "key_activities": ["Technology development", "Infrastructure setup"],
                        "milestones": ["Prototype ready", "Infrastructure operational"]
                    },
                    {
                        "phase": "Phase 3: Deployment",
                        "duration": "12 months",
                        "key_activities": ["Full deployment", "Training completion"],
                        "milestones": ["System operational", "Training completed"]
                    }
                ]
            },
            
            # Risk Assessment Module
            "risk_assessment": {
                "risk_categories": {
                    "technical_risks": {
                        "probability": 0.25,
                        "impact": "Medium",
                        "mitigation": "Technology partnerships"
                    },
                    "financial_risks": {
                        "probability": 0.30,
                        "impact": "High",
                        "mitigation": "Diversified funding"
                    },
                    "operational_risks": {
                        "probability": 0.20,
                        "impact": "Medium",
                        "mitigation": "Comprehensive training"
                    },
                    "strategic_risks": {
                        "probability": 0.15,
                        "impact": "High",
                        "mitigation": "Diplomatic engagement"
                    }
                }
            },
            
            # Interactive Visualizations Module
            "interactive_visualizations": {
                "chart_data": {
                    "timeline": [2024, 2025, 2026, 2027, 2028],
                    "capability": [0.3, 0.5, 0.7, 0.85, 1.0],
                    "investment": [1000, 2000, 3000, 4000, 5000],
                    "risk_level": [0.8, 0.6, 0.4, 0.3, 0.2]
                }
            },
            
            # Acquisition Programs Module
            "acquisition_programs": {
                "programs": [
                    {
                        "name": f"{topic} Enhancement Program",
                        "budget": 2000000000,
                        "timeline": "3 years",
                        "status": "Planning"
                    },
                    {
                        "name": "Technology Development Initiative",
                        "budget": 1500000000,
                        "timeline": "4 years",
                        "status": "Development"
                    }
                ]
            },
            
            # Forecasting Module
            "forecasting": {
                "predictions": {
                    "short_term": {
                        "capability_improvement": "25%",
                        "technology_advancement": "Significant",
                        "regional_impact": "Moderate"
                    },
                    "medium_term": {
                        "capability_improvement": "50%",
                        "technology_advancement": "Major",
                        "regional_impact": "Substantial"
                    },
                    "long_term": {
                        "capability_improvement": "75%",
                        "technology_advancement": "Transformative",
                        "regional_impact": "Significant"
                    }
                }
            },
            
            # Operational Considerations Module
            "operational_considerations": {
                "operational_requirements": {
                    "personnel": "5000 trained personnel",
                    "infrastructure": "Advanced facilities",
                    "logistics": "Comprehensive supply chain",
                    "maintenance": "Regular maintenance schedule"
                },
                "operational_challenges": [
                    "Technology integration",
                    "Personnel training",
                    "Infrastructure development",
                    "Logistics coordination"
                ]
            },
            
            # Regional Security Module
            "regional_security": {
                "security_assessment": {
                    "threat_level": "Moderate to High",
                    "stability_index": 0.65,
                    "conflict_probability": 0.25,
                    "regional_tensions": "Medium",
                    "cooperation_level": 0.6,
                    "deterrence_effectiveness": 0.7
                },
                "security_dynamics": {
                    "threat_assessment": "Moderate to high regional threat level",
                    "deterrence_effectiveness": "Significantly enhanced",
                    "alliance_stability": "Mixed impact on existing alliances"
                },
                "security_implications": {
                    "strategic_implications": [
                        {
                            "title": f"Enhanced {topic} Deterrence",
                            "description": f"Significant enhancement of {topic.lower()} deterrence capabilities",
                            "impact": "High"
                        },
                        {
                            "title": "Regional Arms Competition",
                            "description": "Potential escalation of regional arms competition",
                            "impact": "Medium"
                        }
                    ],
                    "operational_implications": [
                        "Enhanced operational capabilities",
                        "Improved strategic positioning",
                        "Increased regional influence"
                    ]
                },
                "dynamics_evolution": {
                    "timeline": [
                        {"period": "2024-2025", "stability": 0.6, "threat_level": 0.4, "cooperation": 0.5},
                        {"period": "2026-2027", "stability": 0.65, "threat_level": 0.35, "cooperation": 0.6},
                        {"period": "2028-2029", "stability": 0.7, "threat_level": 0.3, "cooperation": 0.7}
                    ]
                },
                "regional_analysis": {
                    "neighbor_relations": "Mixed but improving",
                    "alliance_dynamics": "Evolving partnerships",
                    "security_cooperation": "Increasing engagement"
                }
            },
            
            # Economic Analysis Module
            "economic_analysis": {
                "cost_breakdown": {
                    "acquisition_cost": 3500000000,
                    "operational_cost": 500000000,
                    "maintenance_cost": 750000000,
                    "training_cost": 150000000,
                    "infrastructure_cost": 200000000,
                    "technology_transfer": 800000000,
                    "training_and_support": 150000000
                },
                "economic_impact": {
                    "defense_industry_growth": "25% increase in defense sector",
                    "employment_generation": "5,000 direct and indirect jobs",
                    "technology_spillovers": "Advanced manufacturing capabilities"
                },
                "financing_structure": {
                    "government_budget": "60%",
                    "private_investment": "25%",
                    "international_partnerships": "15%"
                }
            },
            
            # Comparison Analysis Module
            "comparison_analysis": {
                "benchmarking": {
                    "international_standards": "Meeting advanced standards",
                    "regional_comparison": "Leading in region",
                    "technology_gaps": "Minimal gaps identified"
                },
                "competitive_advantage": {
                    "strengths": ["Strategic location", "Technology partnerships", "Operational experience"],
                    "weaknesses": ["Resource constraints", "Technology dependence", "Operational challenges"],
                    "opportunities": ["Regional leadership", "Technology development", "Partnership expansion"]
                }
            },
            
            # Advanced Forecasting Module
            "advanced_forecasting": {
                "scenarios": [
                    {
                        "scenario": "Optimistic",
                        "probability": 0.3,
                        "capability_growth": "80%",
                        "regional_influence": "High",
                        "economic_benefits": "Significant"
                    },
                    {
                        "scenario": "Baseline",
                        "probability": 0.5,
                        "capability_growth": "60%",
                        "regional_influence": "Medium",
                        "economic_benefits": "Moderate"
                    },
                    {
                        "scenario": "Pessimistic",
                        "probability": 0.2,
                        "capability_growth": "40%",
                        "regional_influence": "Low",
                        "economic_benefits": "Limited"
                    }
                ]
            },
            
            # Model Performance Module
            "model_performance": {
                "performance_metrics": {
                    "accuracy": 0.85,
                    "precision": 0.82,
                    "recall": 0.88,
                    "f1_score": 0.85
                },
                "validation_results": {
                    "cross_validation": "Passed",
                    "backtesting": "Successful",
                    "sensitivity_analysis": "Robust"
                }
            },
            
            # Strategic Capability Module
            "strategic_capability": {
                "capability_assessment": {
                    "current_capability": 0.6,
                    "target_capability": 0.9,
                    "capability_gap": 0.3,
                    "readiness_level": 0.7
                },
                "capability_development": {
                    "short_term_goals": ["Technology integration", "Personnel training"],
                    "medium_term_goals": ["Operational deployment", "Capability enhancement"],
                    "long_term_goals": ["Strategic leadership", "Regional influence"]
                }
            },
            
            # Predictive Analytics Module
            "predictive_analytics": {
                "predictions": {
                    "capability_trend": "Steady improvement",
                    "technology_evolution": "Rapid advancement",
                    "regional_dynamics": "Increasing complexity",
                    "strategic_environment": "Evolving multipolarity"
                },
                "confidence_intervals": {
                    "capability_prediction": [0.7, 0.9],
                    "technology_prediction": [0.8, 0.95],
                    "regional_prediction": [0.6, 0.8]
                }
            },
            
            # Scenario Analysis Module
            "scenario_analysis": {
                "scenario_overview": {
                    "scenarios": [
                        {
                            "scenario": "Optimistic",
                            "probability": 0.30,
                            "impact": "High",
                            "timeline": "2-3 years",
                            "key_factors": ["Technology success", "Political support", "Economic growth"]
                        },
                        {
                            "scenario": "Baseline",
                            "probability": 0.50,
                            "impact": "Medium",
                            "timeline": "3-4 years",
                            "key_factors": ["Steady progress", "Moderate challenges", "Balanced outcomes"]
                        },
                        {
                            "scenario": "Pessimistic",
                            "probability": 0.20,
                            "impact": "Low",
                            "timeline": "4-5 years",
                            "key_factors": ["Technology delays", "Resource constraints", "Political challenges"]
                        }
                    ]
                },
                "risk_scenarios": [
                    "Technology transfer delays",
                    "Financing challenges",
                    "Regional escalation",
                    "Operational complications"
                ]
            }
        }
    
    async def generate_comprehensive_report(self, topic: str, enabled_modules: Optional[List[str]] = None) -> Dict[str, Any]:
        """Generate a comprehensive modular report for any topic."""
        try:
            print(f"🎯 Generating comprehensive modular report for: {topic}")
            
            # Generate sample data for the topic
            data = self.get_sample_data_structure(topic)
            
            # Generate the report
            result = await self.generator.generate_modular_report(
                topic=topic,
                data=data,
                enabled_modules=enabled_modules,
                report_title=f"{topic} - Comprehensive Analysis Report"
            )
            
            if result.get("success"):
                print(f"✅ Report generated successfully!")
                print(f"📄 File: {result.get('filename')}")
                print(f"📁 Path: {result.get('file_path')}")
                print(f"📊 Size: {result.get('file_size')} bytes")
                print(f"🔧 Modules Used: {', '.join(result.get('modules_used', []))}")
                print(f"⏰ Generated: {result.get('generated_at')}")
            else:
                print(f"❌ Failed to generate report: {result.get('error')}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_targeted_report(self, topic: str, module_ids: List[str]) -> Dict[str, Any]:
        """Generate a targeted report with specific modules."""
        try:
            print(f"🎯 Generating targeted report for: {topic}")
            print(f"🔧 Using modules: {', '.join(module_ids)}")
            
            # Generate sample data for the topic
            data = self.get_sample_data_structure(topic)
            
            # Generate the report with specific modules
            result = await self.generator.generate_modular_report(
                topic=topic,
                data=data,
                enabled_modules=module_ids,
                report_title=f"{topic} - Targeted Analysis Report"
            )
            
            if result.get("success"):
                print(f"✅ Targeted report generated successfully!")
                print(f"📄 File: {result.get('filename')}")
                print(f"📊 Size: {result.get('file_size')} bytes")
            else:
                print(f"❌ Failed to generate targeted report: {result.get('error')}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error generating targeted report: {e}")
            return {"success": False, "error": str(e)}
    
    def show_available_modules(self):
        """Display all available modules."""
        try:
            available_modules = self.generator.get_available_modules()
            enabled_modules = [m.module_id for m in self.generator.get_enabled_modules()]
            
            print("📋 Available Modules:")
            print("=" * 50)
            
            for i, module_id in enumerate(available_modules, 1):
                module = self.generator.get_module(module_id)
                if module:
                    metadata = module.get_module_metadata()
                    status = "✅ Enabled" if module_id in enabled_modules else "❌ Disabled"
                    print(f"{i:2d}. {module_id:<30} {status}")
                    print(f"    Description: {metadata.get('description', 'No description')}")
                    print()
            
            print(f"Total Modules: {len(available_modules)}")
            print(f"Enabled Modules: {len(enabled_modules)}")
            
        except Exception as e:
            print(f"❌ Error showing modules: {e}")
    
    async def interactive_demo(self):
        """Run an interactive demo."""
        print("🚀 Generic Modular Report System Demo")
        print("=" * 50)
        
        while True:
            print("\nOptions:")
            print("1. Generate comprehensive report")
            print("2. Generate targeted report")
            print("3. Show available modules")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                topic = input("Enter analysis topic: ").strip()
                if topic:
                    await self.generate_comprehensive_report(topic)
                else:
                    print("❌ Topic cannot be empty")
            
            elif choice == "2":
                topic = input("Enter analysis topic: ").strip()
                if topic:
                    self.show_available_modules()
                    modules_input = input("Enter module IDs (comma-separated): ").strip()
                    if modules_input:
                        module_ids = [m.strip() for m in modules_input.split(",")]
                        await self.generate_targeted_report(topic, module_ids)
                    else:
                        print("❌ No modules specified")
                else:
                    print("❌ Topic cannot be empty")
            
            elif choice == "3":
                self.show_available_modules()
            
            elif choice == "4":
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-4.")


async def main():
    """Main function to run the demo."""
    demo = GenericModularReportDemo()
    
    if len(sys.argv) > 1:
        # Command line usage
        topic = sys.argv[1]
        if len(sys.argv) > 2:
            # Specific modules
            modules = sys.argv[2:]
            await demo.generate_targeted_report(topic, modules)
        else:
            # All modules
            await demo.generate_comprehensive_report(topic)
    else:
        # Interactive mode
        await demo.interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())
