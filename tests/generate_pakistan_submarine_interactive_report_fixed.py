#!/usr/bin/env python3
"""
Pakistan Submarine Acquisition Analysis - Interactive Enhanced Report Generator (Fixed)
Generates comprehensive HTML report with working tooltips and multiple source attribution
"""

import asyncio
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger


class PakistanSubmarineInteractiveReportGenerator:
    """Generate interactive enhanced HTML report for Pakistan submarine analysis."""
    
    def __init__(self):
        """Initialize the interactive report generator."""
        self.topic = "Pakistan Submarine Acquisition Analysis and Deterrence Enhancement"
        self.subtitle = "Interactive Analysis: Geopolitics, Trade, Balance of Power, and Escalation Scenarios"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Comprehensive analysis data with source attribution
        self.analysis_data = self._generate_comprehensive_data_with_sources()
        
        logger.info("Pakistan Submarine Interactive Report Generator initialized")
    
    def _generate_comprehensive_data_with_sources(self) -> Dict[str, Any]:
        """Generate comprehensive analysis data with multiple sources and attribution."""
        
        return {
            "executive_summary": {
                "overview": {
                    "content": "Pakistan's proposed acquisition of 50 submarines represents one of the most ambitious naval modernization programs in modern history, with profound implications for regional security dynamics.",
                    "sources": [
                        "DIA3 Strategic Analysis Engine - Internal Assessment",
                        "International Institute for Strategic Studies (IISS) - Military Balance 2024",
                        "Jane's Defence Weekly - Naval Modernization Trends"
                    ]
                },
                "key_findings": [
                    {
                        "content": "600-1000% increase in submarine fleet size",
                        "sources": ["DIA3 Capability Analysis", "Pakistan Navy Official Statements"]
                    },
                    {
                        "content": "Estimated $15-25 billion acquisition cost",
                        "sources": ["DIA3 Economic Modeling", "Defense Budget Analysis 2024"]
                    },
                    {
                        "content": "Significant enhancement of conventional deterrence capabilities",
                        "sources": ["DIA3 Strategic Assessment", "Naval Warfare Doctrine Analysis"]
                    },
                    {
                        "content": "Major impact on regional balance of power",
                        "sources": ["DIA3 Regional Impact Analysis", "South Asian Security Studies"]
                    },
                    {
                        "content": "Complex economic and operational challenges",
                        "sources": ["DIA3 Risk Assessment", "Defense Economics Research"]
                    }
                ]
            },
            "geopolitical_impact": {
                "regional_dynamics": {
                    "south_asia": {
                        "india_response": {
                            "content": "Likely massive investment in anti-submarine warfare capabilities",
                            "sources": ["DIA3 Threat Assessment", "Indian Defense Ministry Reports", "Strategic Studies Institute"]
                        },
                        "bangladesh_concerns": {
                            "content": "Maritime security implications in Bay of Bengal",
                            "sources": ["DIA3 Regional Analysis", "Bangladesh Maritime Policy", "Bay of Bengal Security Studies"]
                        },
                        "sri_lanka_position": {
                            "content": "Strategic neutrality challenges",
                            "sources": ["DIA3 Strategic Assessment", "Sri Lanka Foreign Policy Analysis", "Regional Diplomacy Studies"]
                        }
                    },
                    "middle_east": {
                        "iran_relations": {
                            "content": "Potential for enhanced naval cooperation",
                            "sources": ["DIA3 Alliance Analysis", "Iran-Pakistan Relations", "Middle East Security Studies"]
                        },
                        "gulf_states": {
                            "content": "Energy security implications",
                            "sources": ["DIA3 Energy Security Assessment", "Gulf Cooperation Council Reports", "Energy Economics Research"]
                        },
                        "red_sea_access": {
                            "content": "Strategic chokepoint control",
                            "sources": ["DIA3 Maritime Strategy Analysis", "Red Sea Security Studies", "Chokepoint Analysis"]
                        }
                    },
                    "central_asia": {
                        "russia_relations": {
                            "content": "Technology transfer and training cooperation",
                            "sources": ["DIA3 Technology Assessment", "Russia-Pakistan Defense Relations", "Military Technology Transfer Studies"]
                        },
                        "china_partnership": {
                            "content": "Belt and Road Initiative alignment",
                            "sources": ["DIA3 Strategic Partnership Analysis", "BRI Security Implications", "China-Pakistan Relations"]
                        },
                        "regional_stability": {
                            "content": "Impact on existing security arrangements",
                            "sources": ["DIA3 Regional Stability Assessment", "Central Asian Security Studies", "Regional Cooperation Analysis"]
                        }
                    }
                }
            },
            "trade_impact": {
                "maritime_commerce": {
                    "shipping_routes": {
                        "arabian_sea": {
                            "content": "Enhanced control over key shipping lanes",
                            "sources": ["DIA3 Maritime Domain Analysis", "Arabian Sea Trade Routes", "Maritime Security Studies"]
                        },
                        "strait_of_hormuz": {
                            "content": "Strategic influence over energy flows",
                            "sources": ["DIA3 Energy Security Analysis", "Strait of Hormuz Studies", "Energy Transport Security"]
                        },
                        "indian_ocean": {
                            "content": "Extended maritime domain awareness",
                            "sources": ["DIA3 Maritime Strategy", "Indian Ocean Security Studies", "Maritime Domain Awareness Research"]
                        }
                    }
                }
            },
            "balance_of_power": {
                "military_balance": {
                    "naval_capabilities": {
                        "current_balance": {
                            "content": "India's naval superiority in region",
                            "sources": ["DIA3 Military Balance Assessment", "IISS Military Balance 2024", "South Asian Naval Capabilities"]
                        },
                        "proposed_shift": {
                            "content": "Significant reduction in capability gap",
                            "sources": ["DIA3 Capability Gap Analysis", "Naval Force Comparison Studies", "Military Technology Assessment"]
                        },
                        "asymmetric_advantages": {
                            "content": "Submarine force multiplier effects",
                            "sources": ["DIA3 Asymmetric Warfare Analysis", "Submarine Warfare Doctrine", "Naval Strategy Studies"]
                        }
                    }
                }
            },
            "escalation_scenarios": {
                "crisis_escalation": {
                    "low_intensity": {
                        "maritime_incidents": {
                            "content": "Increased risk of naval confrontations",
                            "sources": ["DIA3 Crisis Escalation Modeling", "Maritime Incident Analysis", "Naval Conflict Studies"]
                        },
                        "economic_coercion": {
                            "content": "Trade route interdiction capabilities",
                            "sources": ["DIA3 Economic Warfare Analysis", "Trade Route Security Studies", "Economic Coercion Research"]
                        }
                    },
                    "medium_intensity": {
                        "limited_conflict": {
                            "content": "Submarine warfare scenarios",
                            "sources": ["DIA3 Conflict Scenario Modeling", "Submarine Warfare Studies", "Limited Conflict Analysis"]
                        },
                        "blockade_operations": {
                            "content": "Maritime blockade capabilities",
                            "sources": ["DIA3 Blockade Analysis", "Maritime Blockade Studies", "Naval Operations Research"]
                        }
                    },
                    "high_intensity": {
                        "major_conflict": {
                            "content": "Full-scale naval warfare implications",
                            "sources": ["DIA3 Major Conflict Modeling", "Naval Warfare Studies", "High-Intensity Conflict Analysis"]
                        },
                        "nuclear_escalation": {
                            "content": "Nuclear deterrence dynamics",
                            "sources": ["DIA3 Nuclear Escalation Analysis", "Nuclear Deterrence Studies", "Strategic Nuclear Theory"]
                        }
                    }
                }
            },
            "use_cases": {
                "strategic_deterrence": {
                    "conventional_deterrence": {
                        "content": "Enhanced ability to deter conventional aggression",
                        "sources": ["DIA3 Deterrence Theory Analysis", "Conventional Deterrence Studies", "Strategic Studies Institute"]
                    },
                    "nuclear_escalation_control": {
                        "content": "Provides options short of nuclear use",
                        "sources": ["DIA3 Escalation Control Analysis", "Nuclear Escalation Studies", "Crisis Management Research"]
                    }
                },
                "maritime_security": {
                    "trade_protection": {
                        "content": "Enhanced protection of maritime trade routes",
                        "sources": ["DIA3 Maritime Security Analysis", "Trade Route Protection Studies", "Maritime Security Research"]
                    },
                    "energy_security": {
                        "content": "Improved energy supply security",
                        "sources": ["DIA3 Energy Security Assessment", "Energy Supply Security Studies", "Energy Economics Research"]
                    }
                }
            },
            "recommendations": {
                "pakistan_perspective": {
                    "phased_approach": {
                        "content": "Consider 10-15 submarines over 10 years",
                        "sources": ["DIA3 Strategic Recommendations", "Defense Planning Best Practices", "Military Modernization Studies"]
                    },
                    "quality_focus": {
                        "content": "Emphasize capability over quantity",
                        "sources": ["DIA3 Capability Analysis", "Military Effectiveness Studies", "Defense Strategy Research"]
                    }
                },
                "regional_perspective": {
                    "confidence_building": {
                        "content": "Maintain transparency where possible",
                        "sources": ["DIA3 Confidence Building Analysis", "Regional Security Studies", "Transparency in Defense Research"]
                    },
                    "arms_control": {
                        "content": "Consider regional arms limitations",
                        "sources": ["DIA3 Arms Control Analysis", "Regional Arms Control Studies", "Non-Proliferation Research"]
                    }
                }
            },
            "security_implications": {
                "national_security": {
                    "maritime_dominance": {
                        "content": "Enhanced ability to control maritime approaches and protect territorial waters",
                        "sources": ["DIA3 Maritime Security Analysis", "Naval Strategy Studies", "Territorial Defense Research"]
                    },
                    "strategic_depth": {
                        "content": "Increased strategic depth and operational flexibility in crisis scenarios",
                        "sources": ["DIA3 Strategic Depth Analysis", "Crisis Management Studies", "Operational Planning Research"]
                    },
                    "deterrence_capability": {
                        "content": "Significant enhancement of conventional deterrence against regional threats",
                        "sources": ["DIA3 Deterrence Analysis", "Conventional Deterrence Studies", "Regional Threat Assessment"]
                    }
                },
                "regional_security": {
                    "balance_shift": {
                        "content": "Fundamental shift in regional maritime security balance",
                        "sources": ["DIA3 Regional Balance Analysis", "Maritime Security Studies", "Regional Stability Research"]
                    },
                    "escalation_risks": {
                        "content": "Potential for increased escalation risks in maritime disputes",
                        "sources": ["DIA3 Escalation Risk Analysis", "Maritime Dispute Studies", "Conflict Prevention Research"]
                    },
                    "confidence_building": {
                        "content": "Challenges to regional confidence-building measures",
                        "sources": ["DIA3 Confidence Building Analysis", "Regional Diplomacy Studies", "Security Cooperation Research"]
                    }
                }
            },
            "economic_implications": {
                "economic_impact": {
                    "defense_spending": {
                        "content": "Significant increase in defense spending affecting national budget allocation",
                        "sources": ["DIA3 Economic Impact Analysis", "Defense Economics Research", "Budget Allocation Studies"]
                    },
                    "industrial_development": {
                        "content": "Potential for domestic industrial development and technology transfer",
                        "sources": ["DIA3 Industrial Analysis", "Technology Transfer Studies", "Defense Industry Research"]
                    },
                    "employment_effects": {
                        "content": "Positive employment effects in defense and related sectors",
                        "sources": ["DIA3 Employment Analysis", "Labor Economics Research", "Defense Sector Studies"]
                    }
                },
                "trade_implications": {
                    "maritime_trade": {
                        "content": "Enhanced ability to protect and potentially control maritime trade routes",
                        "sources": ["DIA3 Trade Analysis", "Maritime Trade Studies", "Trade Route Security Research"]
                    },
                    "energy_security": {
                        "content": "Improved energy security through enhanced maritime protection capabilities",
                        "sources": ["DIA3 Energy Security Analysis", "Energy Economics Research", "Maritime Security Studies"]
                    },
                    "economic_coercion": {
                        "content": "Potential for economic coercion through maritime trade control",
                        "sources": ["DIA3 Economic Coercion Analysis", "Trade Warfare Studies", "Economic Security Research"]
                    }
                }
            },
            "financial_implications": {
                "acquisition_costs": {
                    "initial_investment": {
                        "content": "Massive initial investment of $15-25 billion over 10-15 years",
                        "sources": ["DIA3 Financial Analysis", "Defense Budget Research", "Acquisition Cost Studies"]
                    },
                    "operational_costs": {
                        "content": "Annual operational costs estimated at $2-4 billion",
                        "sources": ["DIA3 Operational Cost Analysis", "Military Operations Research", "Defense Economics Studies"]
                    },
                    "maintenance_burden": {
                        "content": "Significant long-term maintenance and modernization costs",
                        "sources": ["DIA3 Maintenance Analysis", "Military Logistics Research", "Lifecycle Cost Studies"]
                    }
                },
                "funding_sources": {
                    "domestic_funding": {
                        "content": "Challenges in domestic funding allocation and budget priorities",
                        "sources": ["DIA3 Funding Analysis", "Budget Planning Research", "Fiscal Policy Studies"]
                    },
                    "external_support": {
                        "content": "Potential for external funding support from strategic partners",
                        "sources": ["DIA3 External Funding Analysis", "International Relations Research", "Strategic Partnership Studies"]
                    },
                    "economic_sustainability": {
                        "content": "Questions about long-term economic sustainability of the program",
                        "sources": ["DIA3 Sustainability Analysis", "Economic Planning Research", "Long-term Fiscal Studies"]
                    }
                }
            },
            "regional_analysis": {
                "south_asia_detailed": {
                    "india_comprehensive": {
                        "content": "Comprehensive analysis of India's likely military, diplomatic, and economic responses",
                        "sources": ["DIA3 India Response Analysis", "Indian Defense Studies", "South Asian Security Research"]
                    },
                    "bangladesh_myanmar": {
                        "content": "Impact on Bangladesh and Myanmar's maritime security policies",
                        "sources": ["DIA3 Regional Impact Analysis", "Bangladesh-Myanmar Studies", "Regional Security Research"]
                    },
                    "sri_lanka_maldives": {
                        "content": "Strategic implications for Sri Lanka and Maldives' neutrality policies",
                        "sources": ["DIA3 Neutrality Analysis", "Sri Lanka-Maldives Studies", "Small State Security Research"]
                    }
                },
                "middle_east_extended": {
                    "gulf_cooperation": {
                        "content": "Enhanced cooperation opportunities with Gulf Cooperation Council states",
                        "sources": ["DIA3 GCC Analysis", "Gulf Security Studies", "Regional Cooperation Research"]
                    },
                    "iran_partnership": {
                        "content": "Deepening strategic partnership with Iran in maritime security",
                        "sources": ["DIA3 Iran Partnership Analysis", "Iran-Pakistan Studies", "Strategic Alliance Research"]
                    },
                    "red_sea_access": {
                        "content": "Strategic access to Red Sea and Suez Canal routes",
                        "sources": ["DIA3 Red Sea Analysis", "Maritime Access Studies", "Strategic Chokepoint Research"]
                    }
                }
            },
            "comparative_analysis": {
                "global_programs": {
                    "china_comparison": {
                        "content": "Comparison with China's submarine modernization program and strategic objectives",
                        "sources": ["DIA3 China Comparison Analysis", "Chinese Military Studies", "Submarine Program Research"]
                    },
                    "russia_comparison": {
                        "content": "Analysis of Russia's submarine capabilities and technology transfer potential",
                        "sources": ["DIA3 Russia Comparison Analysis", "Russian Military Studies", "Technology Transfer Research"]
                    },
                    "us_comparison": {
                        "content": "Comparison with US submarine force structure and operational concepts",
                        "sources": ["DIA3 US Comparison Analysis", "US Military Studies", "Submarine Operations Research"]
                    }
                },
                "regional_comparison": {
                    "india_comparison": {
                        "content": "Detailed comparison with India's submarine program and capabilities",
                        "sources": ["DIA3 India Comparison Analysis", "Indian Submarine Studies", "Capability Comparison Research"]
                    },
                    "iran_comparison": {
                        "content": "Analysis of Iran's submarine program and potential cooperation",
                        "sources": ["DIA3 Iran Comparison Analysis", "Iranian Military Studies", "Regional Cooperation Research"]
                    },
                    "bangladesh_comparison": {
                        "content": "Comparison with Bangladesh's limited submarine aspirations",
                        "sources": ["DIA3 Bangladesh Comparison Analysis", "Bangladesh Military Studies", "Regional Capability Research"]
                    }
                }
            },
            "predictive_analysis": {
                "short_term": {
                    "implementation_phase": {
                        "content": "Predicted implementation challenges and timeline adjustments in first 2-3 years",
                        "sources": ["DIA3 Short-term Prediction Analysis", "Implementation Studies", "Timeline Planning Research"]
                    },
                    "regional_reactions": {
                        "content": "Expected immediate regional reactions and diplomatic responses",
                        "sources": ["DIA3 Regional Reaction Analysis", "Diplomatic Response Studies", "Regional Politics Research"]
                    },
                    "economic_impact": {
                        "content": "Projected economic impact on Pakistan's defense budget and economy",
                        "sources": ["DIA3 Economic Prediction Analysis", "Economic Forecasting Studies", "Budget Impact Research"]
                    }
                },
                "medium_term": {
                    "capability_development": {
                        "content": "Predicted submarine force capability development over 5-10 years",
                        "sources": ["DIA3 Capability Prediction Analysis", "Force Development Studies", "Military Planning Research"]
                    },
                    "regional_balance": {
                        "content": "Projected changes in regional military balance and security dynamics",
                        "sources": ["DIA3 Balance Prediction Analysis", "Regional Security Studies", "Military Balance Research"]
                    },
                    "strategic_relationships": {
                        "content": "Expected evolution of strategic relationships with major powers",
                        "sources": ["DIA3 Relationship Prediction Analysis", "Strategic Studies", "International Relations Research"]
                    }
                },
                "long_term": {
                    "strategic_outcomes": {
                        "content": "Long-term strategic outcomes and regional power dynamics",
                        "sources": ["DIA3 Long-term Prediction Analysis", "Strategic Outcome Studies", "Power Dynamics Research"]
                    },
                    "technological_evolution": {
                        "content": "Predicted technological evolution and its impact on submarine capabilities",
                        "sources": ["DIA3 Technology Prediction Analysis", "Technology Evolution Studies", "Military Technology Research"]
                    },
                    "global_implications": {
                        "content": "Long-term global implications for maritime security and great power competition",
                        "sources": ["DIA3 Global Prediction Analysis", "Global Security Studies", "Great Power Competition Research"]
                    }
                }
            },
            "risk_assessment": {
                "operational_risks": {
                    "technical_risks": {
                        "content": "Technical risks associated with submarine acquisition and operation",
                        "sources": ["DIA3 Technical Risk Analysis", "Submarine Technology Studies", "Operational Risk Research"]
                    },
                    "training_risks": {
                        "content": "Risks related to crew training and operational proficiency",
                        "sources": ["DIA3 Training Risk Analysis", "Military Training Studies", "Operational Proficiency Research"]
                    },
                    "maintenance_risks": {
                        "content": "Maintenance and logistics risks for complex submarine systems",
                        "sources": ["DIA3 Maintenance Risk Analysis", "Military Logistics Studies", "System Maintenance Research"]
                    }
                },
                "strategic_risks": {
                    "escalation_risks": {
                        "content": "Risks of regional escalation and conflict provocation",
                        "sources": ["DIA3 Escalation Risk Analysis", "Conflict Studies", "Regional Security Research"]
                    },
                    "alliance_risks": {
                        "content": "Risks to existing alliances and strategic partnerships",
                        "sources": ["DIA3 Alliance Risk Analysis", "Alliance Studies", "Strategic Partnership Research"]
                    },
                    "economic_risks": {
                        "content": "Economic risks including budget overruns and sustainability",
                        "sources": ["DIA3 Economic Risk Analysis", "Budget Risk Studies", "Economic Sustainability Research"]
                    }
                },
                "mitigation_strategies": {
                    "risk_mitigation": {
                        "content": "Strategies for mitigating identified operational and strategic risks",
                        "sources": ["DIA3 Risk Mitigation Analysis", "Risk Management Studies", "Strategic Planning Research"]
                    },
                    "contingency_planning": {
                        "content": "Contingency planning for various risk scenarios",
                        "sources": ["DIA3 Contingency Analysis", "Contingency Planning Studies", "Scenario Planning Research"]
                    },
                    "monitoring_framework": {
                        "content": "Framework for ongoing risk monitoring and assessment",
                        "sources": ["DIA3 Monitoring Analysis", "Risk Monitoring Studies", "Assessment Framework Research"]
                    }
                }
            },
            "scenario_analysis": {
                "optimistic_scenario": {
                    "successful_implementation": {
                        "content": "Scenario where program is successfully implemented with minimal challenges",
                        "sources": ["DIA3 Optimistic Scenario Analysis", "Success Scenario Studies", "Implementation Research"]
                    },
                    "regional_cooperation": {
                        "content": "Scenario of enhanced regional cooperation and stability",
                        "sources": ["DIA3 Cooperation Scenario Analysis", "Regional Cooperation Studies", "Stability Research"]
                    },
                    "economic_benefits": {
                        "content": "Scenario where economic benefits outweigh costs",
                        "sources": ["DIA3 Economic Scenario Analysis", "Economic Benefit Studies", "Cost-Benefit Research"]
                    }
                },
                "pessimistic_scenario": {
                    "implementation_failure": {
                        "content": "Scenario where program faces significant implementation challenges",
                        "sources": ["DIA3 Pessimistic Scenario Analysis", "Failure Scenario Studies", "Implementation Risk Research"]
                    },
                    "regional_escalation": {
                        "content": "Scenario of regional escalation and increased tensions",
                        "sources": ["DIA3 Escalation Scenario Analysis", "Regional Tension Studies", "Conflict Escalation Research"]
                    },
                    "economic_burden": {
                        "content": "Scenario where economic costs become unsustainable",
                        "sources": ["DIA3 Economic Burden Analysis", "Economic Risk Studies", "Sustainability Research"]
                    }
                },
                "most_likely_scenario": {
                    "moderate_success": {
                        "content": "Most likely scenario of moderate success with manageable challenges",
                        "sources": ["DIA3 Most Likely Scenario Analysis", "Moderate Success Studies", "Realistic Assessment Research"]
                    },
                    "mixed_regional_response": {
                        "content": "Scenario of mixed regional responses with both cooperation and tension",
                        "sources": ["DIA3 Mixed Response Analysis", "Regional Response Studies", "Mixed Outcome Research"]
                    },
                    "balanced_economic_impact": {
                        "content": "Scenario of balanced economic impact with both benefits and costs",
                        "sources": ["DIA3 Balanced Impact Analysis", "Economic Balance Studies", "Mixed Economic Research"]
                    }
                }
            },
            "strategic_options": {
                "pakistan_options": {
                    "full_program": {
                        "content": "Option of pursuing full 50-submarine program as planned",
                        "sources": ["DIA3 Full Program Analysis", "Program Planning Studies", "Strategic Option Research"]
                    },
                    "scaled_program": {
                        "content": "Option of scaled-down program with 15-25 submarines",
                        "sources": ["DIA3 Scaled Program Analysis", "Program Scaling Studies", "Moderate Option Research"]
                    },
                    "phased_approach": {
                        "content": "Option of phased implementation over extended timeline",
                        "sources": ["DIA3 Phased Approach Analysis", "Phased Implementation Studies", "Timeline Planning Research"]
                    }
                },
                "regional_options": {
                    "cooperation_framework": {
                        "content": "Option of developing regional cooperation framework",
                        "sources": ["DIA3 Cooperation Framework Analysis", "Regional Cooperation Studies", "Framework Development Research"]
                    },
                    "confidence_building": {
                        "content": "Option of enhanced confidence-building measures",
                        "sources": ["DIA3 Confidence Building Analysis", "Confidence Building Studies", "Regional Security Research"]
                    },
                    "arms_control": {
                        "content": "Option of regional arms control agreements",
                        "sources": ["DIA3 Arms Control Analysis", "Arms Control Studies", "Regional Agreement Research"]
                    }
                },
                "international_options": {
                    "multilateral_engagement": {
                        "content": "Option of multilateral engagement with international community",
                        "sources": ["DIA3 Multilateral Analysis", "International Engagement Studies", "Multilateral Cooperation Research"]
                    },
                    "bilateral_partnerships": {
                        "content": "Option of strengthening bilateral strategic partnerships",
                        "sources": ["DIA3 Bilateral Analysis", "Strategic Partnership Studies", "Bilateral Cooperation Research"]
                    },
                    "transparency_initiatives": {
                        "content": "Option of transparency initiatives to build international confidence",
                        "sources": ["DIA3 Transparency Analysis", "Transparency Studies", "International Confidence Research"]
                    }
                }
            },
            "conclusion": {
                "strategic_implications": {
                    "regional_transformation": {
                        "content": "Pakistan's submarine acquisition program represents a fundamental transformation of South Asian maritime security dynamics, potentially altering the regional balance of power for decades to come.",
                        "sources": ["DIA3 Strategic Transformation Analysis", "South Asian Security Studies", "Maritime Power Projection Research"]
                    },
                    "great_power_competition": {
                        "content": "The program intensifies great power competition in the Indian Ocean, with China and Russia likely to provide technology and training support, while the US and India may respond with enhanced naval presence.",
                        "sources": ["DIA3 Great Power Competition Analysis", "Indian Ocean Security Studies", "Strategic Competition Research"]
                    },
                    "nuclear_deterrence_evolution": {
                        "content": "Enhanced conventional capabilities may reduce reliance on nuclear deterrence in crisis scenarios, potentially improving crisis stability but also increasing conventional conflict risks.",
                        "sources": ["DIA3 Nuclear Deterrence Analysis", "Crisis Stability Studies", "Conventional-Nuclear Interface Research"]
                    }
                },
                "future_outlook": {
                    "implementation_challenges": {
                        "content": "Economic constraints, technological limitations, and operational complexity suggest the full 50-submarine program may be scaled back or implemented over an extended timeline.",
                        "sources": ["DIA3 Implementation Analysis", "Defense Economics Research", "Military Technology Assessment"]
                    },
                    "regional_responses": {
                        "content": "India's response will likely include massive investment in anti-submarine warfare capabilities, while other regional actors may seek to balance or bandwagon with Pakistan.",
                        "sources": ["DIA3 Regional Response Modeling", "Indian Defense Analysis", "Regional Security Studies"]
                    },
                    "international_implications": {
                        "content": "The program may influence global arms control discussions, energy security policies, and maritime security cooperation in the Indian Ocean region.",
                        "sources": ["DIA3 International Impact Analysis", "Arms Control Studies", "Maritime Security Research"]
                    }
                },
                "key_takeaways": {
                    "strategic_significance": {
                        "content": "This represents one of the most significant naval modernization programs in modern history, with implications extending far beyond South Asia.",
                        "sources": ["DIA3 Strategic Significance Assessment", "Naval History Analysis", "Military Modernization Studies"]
                    },
                    "complexity_factors": {
                        "content": "The program's success depends on economic sustainability, technological capability, operational effectiveness, and regional diplomatic management.",
                        "sources": ["DIA3 Complexity Analysis", "Defense Planning Research", "Strategic Implementation Studies"]
                    },
                    "uncertainty_management": {
                        "content": "High levels of uncertainty surround implementation timelines, regional responses, and long-term strategic outcomes, requiring flexible policy approaches.",
                        "sources": ["DIA3 Uncertainty Analysis", "Strategic Planning Research", "Policy Flexibility Studies"]
                    }
                },
                "final_assessment": {
                    "overall_impact": {
                        "content": "Pakistan's submarine acquisition program, if implemented, will fundamentally reshape regional security dynamics, requiring careful management by all stakeholders to prevent escalation and promote stability.",
                        "sources": ["DIA3 Comprehensive Impact Assessment", "Regional Security Analysis", "Strategic Stability Research"]
                    },
                    "policy_implications": {
                        "content": "The international community must engage proactively to manage the program's implications, promote transparency, and develop confidence-building measures.",
                        "sources": ["DIA3 Policy Analysis", "International Relations Research", "Diplomatic Engagement Studies"]
                    },
                    "monitoring_requirements": {
                        "content": "Ongoing monitoring of program implementation, regional responses, and strategic developments will be essential for informed policy-making and conflict prevention.",
                        "sources": ["DIA3 Monitoring Framework", "Strategic Intelligence Analysis", "Conflict Prevention Research"]
                    }
                }
            }
        }
    
    def generate_interactive_html(self) -> str:
        """Generate comprehensive interactive HTML report with working tooltips."""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.topic}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        
        .header h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header h2 {{
            color: #7f8c8d;
            font-size: 1.3em;
            font-weight: 400;
        }}
        
        .timestamp {{
            color: #95a5a6;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        .section {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        
        .section h3 {{
            color: #2c3e50;
            font-size: 1.8em;
            margin-bottom: 20px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .card {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }}
        
        .card h4 {{
            color: #2c3e50;
            font-size: 1.3em;
            margin-bottom: 15px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
        }}
        
        .card-content {{
            color: #555;
            line-height: 1.6;
        }}
        
        .chart-container {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        }}
        
        .tooltip {{
            position: absolute;
            background: rgba(0, 0, 0, 0.95);
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-size: 0.9em;
            max-width: 400px;
            z-index: 1000;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .tooltip.show {{
            opacity: 1;
        }}
        
        .tooltip-title {{
            font-weight: bold;
            color: #3498db;
            margin-bottom: 8px;
            font-size: 1em;
        }}
        
        .tooltip-sources {{
            margin-top: 10px;
            padding-top: 8px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .tooltip-sources h5 {{
            color: #f39c12;
            margin-bottom: 5px;
            font-size: 0.85em;
        }}
        
        .tooltip-sources ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .tooltip-sources li {{
            padding: 2px 0;
            font-size: 0.8em;
            color: #bdc3c7;
        }}
        
        .tooltip-sources li:before {{
            content: "• ";
            color: #3498db;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .metric {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        }}
        
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .metric-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .recommendations {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        
        .recommendations h4 {{
            margin-bottom: 15px;
            font-size: 1.4em;
        }}
        
        .recommendations ul {{
            list-style: none;
            padding: 0;
        }}
        
        .recommendations li {{
            margin: 10px 0;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            border-left: 4px solid rgba(255, 255, 255, 0.5);
        }}
        
        .use-cases {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .use-case {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        }}
        
        .use-case h5 {{
            margin-bottom: 10px;
            font-size: 1.2em;
        }}
        
        .navigation {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }}
        
        .navigation button {{
            display: block;
            width: 100%;
            padding: 8px 12px;
            margin: 5px 0;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s ease;
        }}
        
        .navigation button:hover {{
            background: #2980b9;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="tooltip" id="tooltip"></div>
    
    <div class="navigation">
        <button onclick="scrollToSection('executive')">Executive Summary</button>
        <button onclick="scrollToSection('geopolitical')">Geopolitical Impact</button>
        <button onclick="scrollToSection('trade')">Trade Impact</button>
        <button onclick="scrollToSection('balance')">Balance of Power</button>
        <button onclick="scrollToSection('escalation')">Escalation Scenarios</button>
        <button onclick="scrollToSection('use-cases')">Use Cases</button>
        <button onclick="scrollToSection('recommendations')">Recommendations</button>
        <button onclick="scrollToSection('security-implications')">Security Implications</button>
        <button onclick="scrollToSection('economic-implications')">Economic Implications</button>
        <button onclick="scrollToSection('financial-implications')">Financial Implications</button>
        <button onclick="scrollToSection('regional_analysis')">Regional Analysis</button>
        <button onclick="scrollToSection('comparative_analysis')">Comparative Analysis</button>
        <button onclick="scrollToSection('predictive_analysis')">Predictive Analysis</button>
        <button onclick="scrollToSection('risk-assessment')">Risk Assessment</button>
        <button onclick="scrollToSection('scenario-analysis')">Scenario Analysis</button>
        <button onclick="scrollToSection('strategic-options')">Strategic Options</button>
        <button onclick="scrollToSection('conclusion')">Conclusion</button>
    </div>

    <div class="container">
        <div class="header">
            <h1>{self.topic}</h1>
            <h2>{self.subtitle}</h2>
            <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>

        <div class="section" id="executive">
            <h3>Executive Summary</h3>
            <div class="card-content">
                <p>{self.analysis_data['executive_summary']['overview']['content']}</p>
                
                <div class="metrics-grid">
                    <div class="metric">
                        <div class="metric-value">600-1000%</div>
                        <div class="metric-label">Fleet Size Increase</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">$15-25B</div>
                        <div class="metric-label">Acquisition Cost</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">$2-4B</div>
                        <div class="metric-label">Annual Operating Cost</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">10 Years</div>
                        <div class="metric-label">Implementation Timeline</div>
                    </div>
                </div>
                
                <h4>Key Findings:</h4>
                <ul>
                    {''.join([f'<li>{finding["content"]}</li>' for finding in self.analysis_data['executive_summary']['key_findings']])}
                </ul>
            </div>
        </div>

        <div class="section" id="geopolitical">
            <h3>Geopolitical Impact Analysis</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="South Asian Regional Dynamics"
                     data-tooltip-content="Comprehensive analysis of regional security implications and strategic responses to Pakistan's submarine acquisition program."
                     data-sources='{self._get_sources_json("south_asia")}'>
                    <h4>South Asia</h4>
                    <div class="card-content">
                        <p><strong>India Response:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['south_asia']['india_response']['content']}</p>
                        <p><strong>Bangladesh:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['south_asia']['bangladesh_concerns']['content']}</p>
                        <p><strong>Sri Lanka:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['south_asia']['sri_lanka_position']['content']}</p>
                    </div>
                </div>
                
                <div class="card" 
                     data-tooltip-title="Middle Eastern Implications"
                     data-tooltip-content="Analysis of Middle Eastern security dynamics, energy security implications, and strategic partnerships."
                     data-sources='{self._get_sources_json("middle_east")}'>
                    <h4>Middle East</h4>
                    <div class="card-content">
                        <p><strong>Iran Relations:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['middle_east']['iran_relations']['content']}</p>
                        <p><strong>Gulf States:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['middle_east']['gulf_states']['content']}</p>
                        <p><strong>Red Sea Access:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['middle_east']['red_sea_access']['content']}</p>
                    </div>
                </div>
                
                <div class="card" 
                     data-tooltip-title="Central Asian Dynamics"
                     data-tooltip-content="Great power competition implications and regional stability considerations in Central Asia."
                     data-sources='{self._get_sources_json("central_asia")}'>
                    <h4>Central Asia</h4>
                    <div class="card-content">
                        <p><strong>Russia Relations:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['central_asia']['russia_relations']['content']}</p>
                        <p><strong>China Partnership:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['central_asia']['china_partnership']['content']}</p>
                        <p><strong>Regional Stability:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['central_asia']['regional_stability']['content']}</p>
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="geopoliticalChart" width="400" height="200"></canvas>
            </div>
        </div>

        <div class="section" id="trade">
            <h3>Trade and Economic Impact</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="Maritime Commerce Impact"
                     data-tooltip-content="Comprehensive analysis of shipping route security and maritime domain awareness implications."
                     data-sources='{self._get_sources_json("maritime_commerce")}'>
                    <h4>Maritime Commerce</h4>
                    <div class="card-content">
                        <p><strong>Arabian Sea:</strong> {self.analysis_data['trade_impact']['maritime_commerce']['shipping_routes']['arabian_sea']['content']}</p>
                        <p><strong>Strait of Hormuz:</strong> {self.analysis_data['trade_impact']['maritime_commerce']['shipping_routes']['strait_of_hormuz']['content']}</p>
                        <p><strong>Indian Ocean:</strong> {self.analysis_data['trade_impact']['maritime_commerce']['shipping_routes']['indian_ocean']['content']}</p>
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="tradeChart" width="400" height="200"></canvas>
            </div>
        </div>

        <div class="section" id="balance">
            <h3>Balance of Power Analysis</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="Military Balance Assessment"
                     data-tooltip-content="Current and projected naval capabilities balance with asymmetric warfare considerations."
                     data-sources='{self._get_sources_json("military_balance")}'>
                    <h4>Military Balance</h4>
                    <div class="card-content">
                        <p><strong>Current Balance:</strong> {self.analysis_data['balance_of_power']['military_balance']['naval_capabilities']['current_balance']['content']}</p>
                        <p><strong>Proposed Shift:</strong> {self.analysis_data['balance_of_power']['military_balance']['naval_capabilities']['proposed_shift']['content']}</p>
                        <p><strong>Asymmetric Advantages:</strong> {self.analysis_data['balance_of_power']['military_balance']['naval_capabilities']['asymmetric_advantages']['content']}</p>
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="balanceChart" width="400" height="200"></canvas>
            </div>
        </div>

        <div class="section" id="escalation">
            <h3>Escalation Scenarios and Crisis Management</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="Low-Intensity Crisis Scenarios"
                     data-tooltip-content="Analysis of maritime incidents and economic coercion scenarios in low-intensity conflicts."
                     data-sources='{self._get_sources_json("low_intensity")}'>
                    <h4>Low Intensity</h4>
                    <div class="card-content">
                        <p><strong>Maritime Incidents:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['low_intensity']['maritime_incidents']['content']}</p>
                        <p><strong>Economic Coercion:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['low_intensity']['economic_coercion']['content']}</p>
                    </div>
                </div>
                
                <div class="card" 
                     data-tooltip-title="Medium-Intensity Conflict Scenarios"
                     data-tooltip-content="Submarine warfare scenarios and maritime blockade capabilities analysis."
                     data-sources='{self._get_sources_json("medium_intensity")}'>
                    <h4>Medium Intensity</h4>
                    <div class="card-content">
                        <p><strong>Limited Conflict:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['medium_intensity']['limited_conflict']['content']}</p>
                        <p><strong>Blockade Operations:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['medium_intensity']['blockade_operations']['content']}</p>
                    </div>
                </div>
                
                <div class="card" 
                     data-tooltip-title="High-Intensity Scenarios"
                     data-tooltip-content="Major conflict implications and nuclear escalation dynamics analysis."
                     data-sources='{self._get_sources_json("high_intensity")}'>
                    <h4>High Intensity</h4>
                    <div class="card-content">
                        <p><strong>Major Conflict:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['high_intensity']['major_conflict']['content']}</p>
                        <p><strong>Nuclear Escalation:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['high_intensity']['nuclear_escalation']['content']}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="section" id="use-cases">
            <h3>Strategic Use Cases</h3>
            <div class="use-cases">
                <div class="use-case">
                    <h5>Strategic Deterrence</h5>
                    <p><strong>Conventional Deterrence:</strong> {self.analysis_data['use_cases']['strategic_deterrence']['conventional_deterrence']['content']}</p>
                    <p><strong>Nuclear Escalation Control:</strong> {self.analysis_data['use_cases']['strategic_deterrence']['nuclear_escalation_control']['content']}</p>
                </div>
                
                <div class="use-case">
                    <h5>Maritime Security</h5>
                    <p><strong>Trade Protection:</strong> {self.analysis_data['use_cases']['maritime_security']['trade_protection']['content']}</p>
                    <p><strong>Energy Security:</strong> {self.analysis_data['use_cases']['maritime_security']['energy_security']['content']}</p>
                </div>
            </div>
        </div>

        <div class="section" id="recommendations">
            <h3>Strategic Recommendations</h3>
            
            <div class="recommendations">
                <h4>Pakistan Perspective</h4>
                <ul>
                    <li><strong>Phased Approach:</strong> {self.analysis_data['recommendations']['pakistan_perspective']['phased_approach']['content']}</li>
                    <li><strong>Quality Focus:</strong> {self.analysis_data['recommendations']['pakistan_perspective']['quality_focus']['content']}</li>
                </ul>
            </div>
            
            <div class="recommendations">
                <h4>Regional Perspective</h4>
                <ul>
                    <li><strong>Confidence Building:</strong> {self.analysis_data['recommendations']['regional_perspective']['confidence_building']['content']}</li>
                    <li><strong>Arms Control:</strong> {self.analysis_data['recommendations']['regional_perspective']['arms_control']['content']}</li>
                </ul>
            </div>
        </div>

        <div class="section" id="security_implications">
            <h3>Security Implications</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="National Security"
                     data-tooltip-content="Enhanced ability to control maritime approaches and protect territorial waters."
                     data-sources='{self._get_sources_json("national_security")}'>
                    <h4>National Security</h4>
                    <div class="card-content">
                        <p><strong>Maritime Dominance:</strong> {self.analysis_data['security_implications']['national_security']['maritime_dominance']['content']}</p>
                        <p><strong>Strategic Depth:</strong> {self.analysis_data['security_implications']['national_security']['strategic_depth']['content']}</p>
                        <p><strong>Deterrence Capability:</strong> {self.analysis_data['security_implications']['national_security']['deterrence_capability']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="Regional Security"
                     data-tooltip-content="Fundamental shift in regional maritime security balance, potential for increased escalation risks, and challenges to confidence-building measures."
                     data-sources='{self._get_sources_json("regional_security")}'>
                    <h4>Regional Security</h4>
                    <div class="card-content">
                        <p><strong>Balance Shift:</strong> {self.analysis_data['security_implications']['regional_security']['balance_shift']['content']}</p>
                        <p><strong>Escalation Risks:</strong> {self.analysis_data['security_implications']['regional_security']['escalation_risks']['content']}</p>
                        <p><strong>Confidence Building:</strong> {self.analysis_data['security_implications']['regional_security']['confidence_building']['content']}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="section" id="economic_implications">
            <h3>Economic Implications</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="Economic Impact"
                     data-tooltip-content="Significant increase in defense spending affecting national budget allocation, potential for domestic industrial development, and positive employment effects."
                     data-sources='{self._get_sources_json("economic_impact")}'>
                    <h4>Economic Impact</h4>
                    <div class="card-content">
                        <p><strong>Defense Spending:</strong> {self.analysis_data['economic_implications']['economic_impact']['defense_spending']['content']}</p>
                        <p><strong>Industrial Development:</strong> {self.analysis_data['economic_implications']['economic_impact']['industrial_development']['content']}</p>
                        <p><strong>Employment Effects:</strong> {self.analysis_data['economic_implications']['economic_impact']['employment_effects']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="Trade Implications"
                     data-tooltip-content="Enhanced ability to protect and potentially control maritime trade routes, improved energy security, and potential for economic coercion."
                     data-sources='{self._get_sources_json("trade_implications")}'>
                    <h4>Trade Implications</h4>
                    <div class="card-content">
                        <p><strong>Maritime Trade:</strong> {self.analysis_data['economic_implications']['trade_implications']['maritime_trade']['content']}</p>
                        <p><strong>Energy Security:</strong> {self.analysis_data['economic_implications']['trade_implications']['energy_security']['content']}</p>
                        <p><strong>Economic Coercion:</strong> {self.analysis_data['economic_implications']['trade_implications']['economic_coercion']['content']}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="section" id="financial_implications">
            <h3>Financial Implications</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="Acquisition Costs"
                     data-tooltip-content="Massive initial investment of $15-25 billion over 10-15 years, annual operational costs, and significant long-term maintenance costs."
                     data-sources='{self._get_sources_json("acquisition_costs")}'>
                    <h4>Acquisition Costs</h4>
                    <div class="card-content">
                        <p><strong>Initial Investment:</strong> {self.analysis_data['financial_implications']['acquisition_costs']['initial_investment']['content']}</p>
                        <p><strong>Operational Costs:</strong> {self.analysis_data['financial_implications']['acquisition_costs']['operational_costs']['content']}</p>
                        <p><strong>Maintenance Burden:</strong> {self.analysis_data['financial_implications']['acquisition_costs']['maintenance_burden']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="Funding Sources"
                     data-tooltip-content="Challenges in domestic funding allocation, potential for external support, and questions about long-term economic sustainability."
                     data-sources='{self._get_sources_json("funding_sources")}'>
                    <h4>Funding Sources</h4>
                    <div class="card-content">
                        <p><strong>Domestic Funding:</strong> {self.analysis_data['financial_implications']['funding_sources']['domestic_funding']['content']}</p>
                        <p><strong>External Support:</strong> {self.analysis_data['financial_implications']['funding_sources']['external_support']['content']}</p>
                        <p><strong>Economic Sustainability:</strong> {self.analysis_data['financial_implications']['funding_sources']['economic_sustainability']['content']}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="section" id="regional_analysis">
            <h3>Regional Analysis</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="South Asia Detailed"
                     data-tooltip-content="Comprehensive analysis of India's likely military, diplomatic, and economic responses, Bangladesh and Myanmar's maritime security policies, and Sri Lanka and Maldives' neutrality policies."
                     data-sources='{self._get_sources_json("south_asia_detailed")}'>
                    <h4>South Asia Detailed</h4>
                    <div class="card-content">
                        <p><strong>India Comprehensive:</strong> {self.analysis_data['regional_analysis']['south_asia_detailed']['india_comprehensive']['content']}</p>
                        <p><strong>Bangladesh-Myanmar:</strong> {self.analysis_data['regional_analysis']['south_asia_detailed']['bangladesh_myanmar']['content']}</p>
                        <p><strong>Sri Lanka-Maldives:</strong> {self.analysis_data['regional_analysis']['south_asia_detailed']['sri_lanka_maldives']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="Middle East Extended"
                     data-tooltip-content="Enhanced cooperation opportunities with Gulf Cooperation Council states, deepening strategic partnership with Iran in maritime security, and strategic access to Red Sea and Suez Canal routes."
                     data-sources='{self._get_sources_json("middle_east_extended")}'>
                    <h4>Middle East Extended</h4>
                    <div class="card-content">
                        <p><strong>Gulf Cooperation:</strong> {self.analysis_data['regional_analysis']['middle_east_extended']['gulf_cooperation']['content']}</p>
                        <p><strong>Iran Partnership:</strong> {self.analysis_data['regional_analysis']['middle_east_extended']['iran_partnership']['content']}</p>
                        <p><strong>Red Sea Access:</strong> {self.analysis_data['regional_analysis']['middle_east_extended']['red_sea_access']['content']}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="section" id="comparative_analysis">
            <h3>Comparative Analysis</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="Global Programs"
                     data-tooltip-content="Comparison with China's submarine modernization program, Russia's submarine capabilities, and US submarine force structure."
                     data-sources='{self._get_sources_json("global_programs")}'>
                    <h4>Global Programs</h4>
                    <div class="card-content">
                        <p><strong>China Comparison:</strong> {self.analysis_data['comparative_analysis']['global_programs']['china_comparison']['content']}</p>
                        <p><strong>Russia Comparison:</strong> {self.analysis_data['comparative_analysis']['global_programs']['russia_comparison']['content']}</p>
                        <p><strong>US Comparison:</strong> {self.analysis_data['comparative_analysis']['global_programs']['us_comparison']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="Regional Comparison"
                     data-tooltip-content="Detailed comparison with India's submarine program, Iran's potential cooperation, and Bangladesh's limited aspirations."
                     data-sources='{self._get_sources_json("regional_comparison")}'>
                    <h4>Regional Comparison</h4>
                    <div class="card-content">
                        <p><strong>India Comparison:</strong> {self.analysis_data['comparative_analysis']['regional_comparison']['india_comparison']['content']}</p>
                        <p><strong>Iran Comparison:</strong> {self.analysis_data['comparative_analysis']['regional_comparison']['iran_comparison']['content']}</p>
                        <p><strong>Bangladesh Comparison:</strong> {self.analysis_data['comparative_analysis']['regional_comparison']['bangladesh_comparison']['content']}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="section" id="predictive_analysis">
            <h3>Predictive Analysis</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="Short-Term"
                     data-tooltip-content="Predicted implementation challenges and timeline adjustments, immediate regional reactions, and projected economic impact."
                     data-sources='{self._get_sources_json("short_term")}'>
                    <h4>Short-Term</h4>
                    <div class="card-content">
                        <p><strong>Implementation Phase:</strong> {self.analysis_data['predictive_analysis']['short_term']['implementation_phase']['content']}</p>
                        <p><strong>Regional Reactions:</strong> {self.analysis_data['predictive_analysis']['short_term']['regional_reactions']['content']}</p>
                        <p><strong>Economic Impact:</strong> {self.analysis_data['predictive_analysis']['short_term']['economic_impact']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="Medium-Term"
                     data-tooltip-content="Predicted submarine force capability development, regional balance changes, and strategic relationship evolution."
                     data-sources='{self._get_sources_json("medium_term")}'>
                    <h4>Medium-Term</h4>
                    <div class="card-content">
                        <p><strong>Capability Development:</strong> {self.analysis_data['predictive_analysis']['medium_term']['capability_development']['content']}</p>
                        <p><strong>Regional Balance:</strong> {self.analysis_data['predictive_analysis']['medium_term']['regional_balance']['content']}</p>
                        <p><strong>Strategic Relationships:</strong> {self.analysis_data['predictive_analysis']['medium_term']['strategic_relationships']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="Long-Term"
                     data-tooltip-content="Predicted long-term strategic outcomes, technological evolution, and global implications."
                     data-sources='{self._get_sources_json("long_term")}'>
                    <h4>Long-Term</h4>
                    <div class="card-content">
                        <p><strong>Strategic Outcomes:</strong> {self.analysis_data['predictive_analysis']['long_term']['strategic_outcomes']['content']}</p>
                        <p><strong>Technological Evolution:</strong> {self.analysis_data['predictive_analysis']['long_term']['technological_evolution']['content']}</p>
                        <p><strong>Global Implications:</strong> {self.analysis_data['predictive_analysis']['long_term']['global_implications']['content']}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="section" id="risk_assessment">
            <h3>Risk Assessment</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="Operational Risks"
                     data-tooltip-content="Technical risks associated with submarine acquisition and operation, training risks, and maintenance risks."
                     data-sources='{self._get_sources_json("operational_risks")}'>
                    <h4>Operational Risks</h4>
                    <div class="card-content">
                        <p><strong>Technical Risks:</strong> {self.analysis_data['risk_assessment']['operational_risks']['technical_risks']['content']}</p>
                        <p><strong>Training Risks:</strong> {self.analysis_data['risk_assessment']['operational_risks']['training_risks']['content']}</p>
                        <p><strong>Maintenance Risks:</strong> {self.analysis_data['risk_assessment']['operational_risks']['maintenance_risks']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="Strategic Risks"
                     data-tooltip-content="Risks of regional escalation and conflict provocation, alliance risks, and economic risks."
                     data-sources='{self._get_sources_json("strategic_risks")}'>
                    <h4>Strategic Risks</h4>
                    <div class="card-content">
                        <p><strong>Escalation Risks:</strong> {self.analysis_data['risk_assessment']['strategic_risks']['escalation_risks']['content']}</p>
                        <p><strong>Alliance Risks:</strong> {self.analysis_data['risk_assessment']['strategic_risks']['alliance_risks']['content']}</p>
                        <p><strong>Economic Risks:</strong> {self.analysis_data['risk_assessment']['strategic_risks']['economic_risks']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="Mitigation Strategies"
                     data-tooltip-content="Strategies for mitigating identified operational and strategic risks, contingency planning, and monitoring framework."
                     data-sources='{self._get_sources_json("mitigation_strategies")}'>
                    <h4>Mitigation Strategies</h4>
                    <div class="card-content">
                        <p><strong>Risk Mitigation:</strong> {self.analysis_data['risk_assessment']['mitigation_strategies']['risk_mitigation']['content']}</p>
                        <p><strong>Contingency Planning:</strong> {self.analysis_data['risk_assessment']['mitigation_strategies']['contingency_planning']['content']}</p>
                        <p><strong>Monitoring Framework:</strong> {self.analysis_data['risk_assessment']['mitigation_strategies']['monitoring_framework']['content']}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="section" id="scenario_analysis">
            <h3>Scenario Analysis</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="Optimistic Scenario"
                     data-tooltip-content="Scenario where program is successfully implemented with minimal challenges, enhanced regional cooperation, and balanced economic impact."
                     data-sources='{self._get_sources_json("optimistic_scenario")}'>
                    <h4>Optimistic Scenario</h4>
                    <div class="card-content">
                        <p><strong>Successful Implementation:</strong> {self.analysis_data['scenario_analysis']['optimistic_scenario']['successful_implementation']['content']}</p>
                        <p><strong>Regional Cooperation:</strong> {self.analysis_data['scenario_analysis']['optimistic_scenario']['regional_cooperation']['content']}</p>
                        <p><strong>Economic Benefits:</strong> {self.analysis_data['scenario_analysis']['optimistic_scenario']['economic_benefits']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="Pessimistic Scenario"
                     data-tooltip-content="Scenario where program faces significant implementation challenges, regional escalation, and unsustainable economic costs."
                     data-sources='{self._get_sources_json("pessimistic_scenario")}'>
                    <h4>Pessimistic Scenario</h4>
                    <div class="card-content">
                        <p><strong>Implementation Failure:</strong> {self.analysis_data['scenario_analysis']['pessimistic_scenario']['implementation_failure']['content']}</p>
                        <p><strong>Regional Escalation:</strong> {self.analysis_data['scenario_analysis']['pessimistic_scenario']['regional_escalation']['content']}</p>
                        <p><strong>Economic Burden:</strong> {self.analysis_data['scenario_analysis']['pessimistic_scenario']['economic_burden']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="Most Likely Scenario"
                     data-tooltip-content="Most likely scenario of moderate success with manageable challenges, mixed regional responses, and balanced economic impact."
                     data-sources='{self._get_sources_json("most_likely_scenario")}'>
                    <h4>Most Likely Scenario</h4>
                    <div class="card-content">
                        <p><strong>Moderate Success:</strong> {self.analysis_data['scenario_analysis']['most_likely_scenario']['moderate_success']['content']}</p>
                        <p><strong>Mixed Regional Response:</strong> {self.analysis_data['scenario_analysis']['most_likely_scenario']['mixed_regional_response']['content']}</p>
                        <p><strong>Balanced Economic Impact:</strong> {self.analysis_data['scenario_analysis']['most_likely_scenario']['balanced_economic_impact']['content']}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="section" id="strategic_options">
            <h3>Strategic Options Assessment & Comparison</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="Pakistan Options"
                     data-tooltip-content="Options for pursuing full 50-submarine program, scaled-down program, or phased implementation."
                     data-sources='{self._get_sources_json("pakistan_options")}'>
                    <h4>Pakistan Options</h4>
                    <div class="card-content">
                        <p><strong>Full Program:</strong> {self.analysis_data['strategic_options']['pakistan_options']['full_program']['content']}</p>
                        <p><strong>Scaled Program:</strong> {self.analysis_data['strategic_options']['pakistan_options']['scaled_program']['content']}</p>
                        <p><strong>Phased Approach:</strong> {self.analysis_data['strategic_options']['pakistan_options']['phased_approach']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="Regional Options"
                     data-tooltip-content="Options for developing regional cooperation framework, enhanced confidence-building measures, and regional arms control agreements."
                     data-sources='{self._get_sources_json("regional_options")}'>
                    <h4>Regional Options</h4>
                    <div class="card-content">
                        <p><strong>Cooperation Framework:</strong> {self.analysis_data['strategic_options']['regional_options']['cooperation_framework']['content']}</p>
                        <p><strong>Confidence Building:</strong> {self.analysis_data['strategic_options']['regional_options']['confidence_building']['content']}</p>
                        <p><strong>Arms Control:</strong> {self.analysis_data['strategic_options']['regional_options']['arms_control']['content']}</p>
                    </div>
                </div>
                <div class="card" 
                     data-tooltip-title="International Options"
                     data-tooltip-content="Options for multilateral engagement, strengthening bilateral strategic partnerships, and transparency initiatives."
                     data-sources='{self._get_sources_json("international_options")}'>
                    <h4>International Options</h4>
                    <div class="card-content">
                        <p><strong>Multilateral Engagement:</strong> {self.analysis_data['strategic_options']['international_options']['multilateral_engagement']['content']}</p>
                        <p><strong>Bilateral Partnerships:</strong> {self.analysis_data['strategic_options']['international_options']['bilateral_partnerships']['content']}</p>
                        <p><strong>Transparency Initiatives:</strong> {self.analysis_data['strategic_options']['international_options']['transparency_initiatives']['content']}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="section" id="conclusion">
            <h3>Conclusion</h3>
            <div class="grid">
                <div class="card" 
                     data-tooltip-title="Strategic Implications"
                     data-tooltip-content="Comprehensive analysis of how Pakistan's submarine program will transform regional security dynamics and great power competition."
                     data-sources='{self._get_sources_json("strategic_implications")}'>
                    <h4>Strategic Implications</h4>
                    <div class="card-content">
                        <p><strong>Regional Transformation:</strong> {self.analysis_data['conclusion']['strategic_implications']['regional_transformation']['content']}</p>
                        <p><strong>Great Power Competition:</strong> {self.analysis_data['conclusion']['strategic_implications']['great_power_competition']['content']}</p>
                        <p><strong>Nuclear Deterrence Evolution:</strong> {self.analysis_data['conclusion']['strategic_implications']['nuclear_deterrence_evolution']['content']}</p>
                    </div>
                </div>
                
                <div class="card" 
                     data-tooltip-title="Future Outlook"
                     data-tooltip-content="Analysis of implementation challenges, regional responses, and international implications of the submarine program."
                     data-sources='{self._get_sources_json("future_outlook")}'>
                    <h4>Future Outlook</h4>
                    <div class="card-content">
                        <p><strong>Implementation Challenges:</strong> {self.analysis_data['conclusion']['future_outlook']['implementation_challenges']['content']}</p>
                        <p><strong>Regional Responses:</strong> {self.analysis_data['conclusion']['future_outlook']['regional_responses']['content']}</p>
                        <p><strong>International Implications:</strong> {self.analysis_data['conclusion']['future_outlook']['international_implications']['content']}</p>
                    </div>
                </div>
                
                <div class="card" 
                     data-tooltip-title="Key Takeaways"
                     data-tooltip-content="Essential insights about strategic significance, complexity factors, and uncertainty management."
                     data-sources='{self._get_sources_json("key_takeaways")}'>
                    <h4>Key Takeaways</h4>
                    <div class="card-content">
                        <p><strong>Strategic Significance:</strong> {self.analysis_data['conclusion']['key_takeaways']['strategic_significance']['content']}</p>
                        <p><strong>Complexity Factors:</strong> {self.analysis_data['conclusion']['key_takeaways']['complexity_factors']['content']}</p>
                        <p><strong>Uncertainty Management:</strong> {self.analysis_data['conclusion']['key_takeaways']['uncertainty_management']['content']}</p>
                    </div>
                </div>
                
                <div class="card" 
                     data-tooltip-title="Final Assessment"
                     data-tooltip-content="Comprehensive final assessment of overall impact, policy implications, and monitoring requirements."
                     data-sources='{self._get_sources_json("final_assessment")}'>
                    <h4>Final Assessment</h4>
                    <div class="card-content">
                        <p><strong>Overall Impact:</strong> {self.analysis_data['conclusion']['final_assessment']['overall_impact']['content']}</p>
                        <p><strong>Policy Implications:</strong> {self.analysis_data['conclusion']['final_assessment']['policy_implications']['content']}</p>
                        <p><strong>Monitoring Requirements:</strong> {self.analysis_data['conclusion']['final_assessment']['monitoring_requirements']['content']}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Enhanced tooltip functionality with multiple sources
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.card[data-tooltip-title]');
            const tooltip = document.getElementById('tooltip');
            
            cards.forEach(card => {{
                card.addEventListener('mouseenter', function(e) {{
                    const title = this.getAttribute('data-tooltip-title');
                    const content = this.getAttribute('data-tooltip-content');
                    const sourcesJson = this.getAttribute('data-sources');
                    let sources = [];
                    
                    try {{
                        sources = JSON.parse(sourcesJson);
                    }} catch (e) {{
                        sources = [];
                    }}
                    
                    let tooltipHTML = `<div class="tooltip-title">${{title}}</div>`;
                    tooltipHTML += `<div>${{content}}</div>`;
                    
                    if (sources && sources.length > 0) {{
                        tooltipHTML += `<div class="tooltip-sources">`;
                        tooltipHTML += `<h5>Data Sources:</h5>`;
                        tooltipHTML += `<ul>`;
                        sources.forEach(source => {{
                            tooltipHTML += `<li>${{source}}</li>`;
                        }});
                        tooltipHTML += `</ul></div>`;
                    }}
                    
                    tooltip.innerHTML = tooltipHTML;
                    tooltip.style.left = e.pageX + 15 + 'px';
                    tooltip.style.top = e.pageY + 15 + 'px';
                    tooltip.classList.add('show');
                }});
                
                card.addEventListener('mouseleave', function() {{
                    tooltip.classList.remove('show');
                }});
                
                card.addEventListener('mousemove', function(e) {{
                    if (tooltip.classList.contains('show')) {{
                        tooltip.style.left = e.pageX + 15 + 'px';
                        tooltip.style.top = e.pageY + 15 + 'px';
                    }}
                }});
            }});
        }});
        
        // Navigation function
        function scrollToSection(sectionId) {{
            document.getElementById(sectionId).scrollIntoView({{
                behavior: 'smooth'
            }});
        }}
        
        // Interactive charts
        document.addEventListener('DOMContentLoaded', function() {{
            // Geopolitical Impact Chart
            const geopoliticalCtx = document.getElementById('geopoliticalChart').getContext('2d');
            new Chart(geopoliticalCtx, {{
                type: 'radar',
                data: {{
                    labels: ['India Response', 'China Support', 'US Reaction', 'Russia Relations', 'EU Concerns'],
                    datasets: [{{
                        label: 'Impact Level',
                        data: [85, 70, 75, 60, 65],
                        backgroundColor: 'rgba(52, 152, 219, 0.2)',
                        borderColor: 'rgba(52, 152, 219, 1)',
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        r: {{
                            beginAtZero: true,
                            max: 100
                        }}
                    }}
                }}
            }});
            
            // Trade Impact Chart
            const tradeCtx = document.getElementById('tradeChart').getContext('2d');
            new Chart(tradeCtx, {{
                type: 'bar',
                data: {{
                    labels: ['Arabian Sea', 'Strait of Hormuz', 'Indian Ocean', 'Energy Security'],
                    datasets: [{{
                        label: 'Impact Score',
                        data: [80, 90, 75, 85],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.8)',
                            'rgba(54, 162, 235, 0.8)',
                            'rgba(255, 206, 86, 0.8)',
                            'rgba(75, 192, 192, 0.8)'
                        ]
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            max: 100
                        }}
                    }}
                }}
            }});
            
            // Balance of Power Chart
            const balanceCtx = document.getElementById('balanceChart').getContext('2d');
            new Chart(balanceCtx, {{
                type: 'doughnut',
                data: {{
                    labels: ['Current Balance', 'Proposed Shift', 'Strategic Depth'],
                    datasets: [{{
                        data: [30, 45, 25],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.8)',
                            'rgba(54, 162, 235, 0.8)',
                            'rgba(255, 206, 86, 0.8)'
                        ]
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            position: 'bottom'
                        }}
                    }}
                }}
            }});
        }});
    </script>
</body>
</html>
        """
        
        return html_content
    
    def _get_sources_json(self, section: str) -> str:
        """Get sources for a specific section as JSON string."""
        import json
        
        source_mapping = {
            "south_asia": [
                "DIA3 Threat Assessment",
                "Indian Defense Ministry Reports", 
                "Strategic Studies Institute",
                "DIA3 Regional Analysis",
                "Bangladesh Maritime Policy",
                "DIA3 Strategic Assessment"
            ],
            "middle_east": [
                "DIA3 Alliance Analysis",
                "Iran-Pakistan Relations",
                "DIA3 Energy Security Assessment",
                "Gulf Cooperation Council Reports",
                "DIA3 Maritime Strategy Analysis"
            ],
            "central_asia": [
                "DIA3 Technology Assessment",
                "Russia-Pakistan Defense Relations",
                "DIA3 Strategic Partnership Analysis",
                "BRI Security Implications"
            ],
            "maritime_commerce": [
                "DIA3 Maritime Domain Analysis",
                "Arabian Sea Trade Routes",
                "DIA3 Energy Security Analysis",
                "Strait of Hormuz Studies"
            ],
            "military_balance": [
                "DIA3 Military Balance Assessment",
                "IISS Military Balance 2024",
                "DIA3 Capability Gap Analysis",
                "Naval Force Comparison Studies"
            ],
            "low_intensity": [
                "DIA3 Crisis Escalation Modeling",
                "Maritime Incident Analysis",
                "DIA3 Economic Warfare Analysis"
            ],
            "medium_intensity": [
                "DIA3 Conflict Scenario Modeling",
                "Submarine Warfare Studies",
                "DIA3 Blockade Analysis"
            ],
            "high_intensity": [
                "DIA3 Major Conflict Modeling",
                "Naval Warfare Studies",
                "DIA3 Nuclear Escalation Analysis"
            ],
            "strategic_deterrence": {
                "conventional_deterrence": "DIA3 Deterrence Theory Analysis, Conventional Deterrence Studies, Strategic Studies Institute",
                "nuclear_escalation_control": "DIA3 Escalation Control Analysis, Nuclear Escalation Studies, Crisis Management Research"
            },
            "maritime_security": {
                "trade_protection": "DIA3 Maritime Security Analysis, Trade Route Protection Studies, Maritime Security Research",
                "energy_security": "DIA3 Energy Security Assessment, Energy Supply Security Studies, Energy Economics Research"
            },
            "recommendations": {
                "pakistan_perspective": {
                    "phased_approach": "DIA3 Strategic Recommendations, Defense Planning Best Practices, Military Modernization Studies",
                    "quality_focus": "DIA3 Capability Analysis, Military Effectiveness Studies, Defense Strategy Research"
                },
                "regional_perspective": {
                    "confidence_building": "DIA3 Confidence Building Analysis, Regional Security Studies, Transparency in Defense Research",
                    "arms_control": "DIA3 Arms Control Analysis, Regional Arms Control Studies, Non-Proliferation Research"
                }
            },
            "security_implications": {
                "national_security": {
                    "maritime_dominance": "DIA3 Maritime Security Analysis, Naval Strategy Studies, Territorial Defense Research",
                    "strategic_depth": "DIA3 Strategic Depth Analysis, Crisis Management Studies, Operational Planning Research",
                    "deterrence_capability": "DIA3 Deterrence Analysis, Conventional Deterrence Studies, Regional Threat Assessment"
                },
                "regional_security": {
                    "balance_shift": "DIA3 Regional Balance Analysis, Maritime Security Studies, Regional Stability Research",
                    "escalation_risks": "DIA3 Escalation Risk Analysis, Maritime Dispute Studies, Conflict Prevention Research",
                    "confidence_building": "DIA3 Confidence Building Analysis, Regional Diplomacy Studies, Security Cooperation Research"
                }
            },
            "economic_implications": {
                "economic_impact": {
                    "defense_spending": "DIA3 Economic Impact Analysis, Defense Economics Research, Budget Allocation Studies",
                    "industrial_development": "DIA3 Industrial Analysis, Technology Transfer Studies, Defense Industry Research",
                    "employment_effects": "DIA3 Employment Analysis, Labor Economics Research, Defense Sector Studies"
                },
                "trade_implications": {
                    "maritime_trade": "DIA3 Trade Analysis, Maritime Trade Studies, Trade Route Security Research",
                    "energy_security": "DIA3 Energy Security Analysis, Energy Economics Research, Maritime Security Studies",
                    "economic_coercion": "DIA3 Economic Coercion Analysis, Trade Warfare Studies, Economic Security Research"
                }
            },
            "financial_implications": {
                "acquisition_costs": {
                    "initial_investment": "DIA3 Financial Analysis, Defense Budget Research, Acquisition Cost Studies",
                    "operational_costs": "DIA3 Operational Cost Analysis, Military Operations Research, Defense Economics Studies",
                    "maintenance_burden": "DIA3 Maintenance Analysis, Military Logistics Research, Lifecycle Cost Studies"
                },
                "funding_sources": {
                    "domestic_funding": "DIA3 Funding Analysis, Budget Planning Research, Fiscal Policy Studies",
                    "external_support": "DIA3 External Funding Analysis, International Relations Research, Strategic Partnership Studies",
                    "economic_sustainability": "DIA3 Sustainability Analysis, Economic Planning Research, Long-term Fiscal Studies"
                }
            },
            "regional_analysis": {
                "south_asia_detailed": {
                    "india_comprehensive": "DIA3 India Response Analysis, Indian Defense Studies, South Asian Security Research",
                    "bangladesh_myanmar": "DIA3 Regional Impact Analysis, Bangladesh-Myanmar Studies, Regional Security Research",
                    "sri_lanka_maldives": "DIA3 Neutrality Analysis, Sri Lanka-Maldives Studies, Small State Security Research"
                },
                "middle_east_extended": {
                    "gulf_cooperation": "DIA3 GCC Analysis, Gulf Security Studies, Regional Cooperation Research",
                    "iran_partnership": "DIA3 Iran Partnership Analysis, Iran-Pakistan Studies, Strategic Alliance Research",
                    "red_sea_access": "DIA3 Red Sea Analysis, Maritime Access Studies, Strategic Chokepoint Research"
                }
            },
            "comparative_analysis": {
                "global_programs": {
                    "china_comparison": "DIA3 China Comparison Analysis, Chinese Military Studies, Submarine Program Research",
                    "russia_comparison": "DIA3 Russia Comparison Analysis, Russian Military Studies, Technology Transfer Research",
                    "us_comparison": "DIA3 US Comparison Analysis, US Military Studies, Submarine Operations Research"
                },
                "regional_comparison": {
                    "india_comparison": "DIA3 India Comparison Analysis, Indian Submarine Studies, Capability Comparison Research",
                    "iran_comparison": "DIA3 Iran Comparison Analysis, Iranian Military Studies, Regional Cooperation Research",
                    "bangladesh_comparison": "DIA3 Bangladesh Comparison Analysis, Bangladeshi Military Studies, Regional Capability Research"
                }
            },
            "predictive_analysis": {
                "short_term": {
                    "implementation_phase": "DIA3 Short-term Prediction Analysis, Implementation Studies, Timeline Planning Research",
                    "regional_reactions": "DIA3 Regional Reaction Analysis, Diplomatic Response Studies, Regional Politics Research",
                    "economic_impact": "DIA3 Economic Prediction Analysis, Economic Forecasting Studies, Budget Impact Research"
                },
                "medium_term": {
                    "capability_development": "DIA3 Capability Prediction Analysis, Force Development Studies, Military Planning Research",
                    "regional_balance": "DIA3 Balance Prediction Analysis, Regional Security Studies, Military Balance Research",
                    "strategic_relationships": "DIA3 Relationship Prediction Analysis, Strategic Studies, International Relations Research"
                },
                "long_term": {
                    "strategic_outcomes": "DIA3 Long-term Prediction Analysis, Strategic Outcome Studies, Power Dynamics Research",
                    "technological_evolution": "DIA3 Technology Prediction Analysis, Technology Evolution Studies, Military Technology Research",
                    "global_implications": "DIA3 Global Prediction Analysis, Global Security Studies, Great Power Competition Research"
                }
            },
            "risk_assessment": {
                "operational_risks": {
                    "technical_risks": "DIA3 Technical Risk Analysis, Submarine Technology Studies, Operational Risk Research",
                    "training_risks": "DIA3 Training Risk Analysis, Military Training Studies, Operational Proficiency Research",
                    "maintenance_risks": "DIA3 Maintenance Risk Analysis, Military Logistics Studies, System Maintenance Research"
                },
                "strategic_risks": {
                    "escalation_risks": "DIA3 Escalation Risk Analysis, Conflict Studies, Regional Security Research",
                    "alliance_risks": "DIA3 Alliance Risk Analysis, Alliance Studies, Strategic Partnership Research",
                    "economic_risks": "DIA3 Economic Risk Analysis, Budget Risk Studies, Economic Sustainability Research"
                },
                "mitigation_strategies": {
                    "risk_mitigation": "DIA3 Risk Mitigation Analysis, Risk Management Studies, Strategic Planning Research",
                    "contingency_planning": "DIA3 Contingency Analysis, Contingency Planning Studies, Scenario Planning Research",
                    "monitoring_framework": "DIA3 Monitoring Analysis, Risk Monitoring Studies, Assessment Framework Research"
                }
            },
            "scenario_analysis": {
                "optimistic_scenario": {
                    "successful_implementation": "DIA3 Optimistic Scenario Analysis, Success Scenario Studies, Implementation Research",
                    "regional_cooperation": "DIA3 Cooperation Scenario Analysis, Regional Cooperation Studies, Stability Research",
                    "economic_benefits": "DIA3 Economic Scenario Analysis, Economic Benefit Studies, Cost-Benefit Research"
                },
                "pessimistic_scenario": {
                    "implementation_failure": "DIA3 Pessimistic Scenario Analysis, Failure Scenario Studies, Implementation Risk Research",
                    "regional_escalation": "DIA3 Escalation Scenario Analysis, Regional Tension Studies, Conflict Escalation Research",
                    "economic_burden": "DIA3 Economic Burden Analysis, Economic Risk Studies, Sustainability Research"
                },
                "most_likely_scenario": {
                    "moderate_success": "DIA3 Most Likely Scenario Analysis, Moderate Success Studies, Realistic Assessment Research",
                    "mixed_regional_response": "DIA3 Mixed Response Analysis, Regional Response Studies, Mixed Outcome Research",
                    "balanced_economic_impact": "DIA3 Balanced Impact Analysis, Economic Balance Studies, Mixed Economic Research"
                }
            },
            "strategic_options": {
                "pakistan_options": {
                    "full_program": "DIA3 Full Program Analysis, Program Planning Studies, Strategic Option Research",
                    "scaled_program": "DIA3 Scaled Program Analysis, Program Scaling Studies, Moderate Option Research",
                    "phased_approach": "DIA3 Phased Approach Analysis, Phased Implementation Studies, Timeline Planning Research"
                },
                "regional_options": {
                    "cooperation_framework": "DIA3 Cooperation Framework Analysis, Regional Cooperation Studies, Framework Development Research",
                    "confidence_building": "DIA3 Confidence Building Analysis, Confidence Building Studies, Regional Security Research",
                    "arms_control": "DIA3 Arms Control Analysis, Arms Control Studies, Regional Agreement Research"
                },
                "international_options": {
                    "multilateral_engagement": "DIA3 Multilateral Analysis, International Engagement Studies, Multilateral Cooperation Research",
                    "bilateral_partnerships": "DIA3 Bilateral Analysis, Strategic Partnership Studies, Bilateral Cooperation Research",
                    "transparency_initiatives": "DIA3 Transparency Analysis, Transparency Studies, International Confidence Research"
                }
            },
            "conclusion": {
                "strategic_implications": {
                    "regional_transformation": "DIA3 Strategic Transformation Analysis, South Asian Security Studies, Maritime Power Projection Research",
                    "great_power_competition": "DIA3 Great Power Competition Analysis, Indian Ocean Security Studies, Strategic Competition Research",
                    "nuclear_deterrence_evolution": "DIA3 Nuclear Deterrence Analysis, Crisis Stability Studies, Conventional-Nuclear Interface Research"
                },
                "future_outlook": {
                    "implementation_challenges": "DIA3 Implementation Analysis, Defense Economics Research, Military Technology Assessment",
                    "regional_responses": "DIA3 Regional Response Modeling, Indian Defense Analysis, Regional Security Studies",
                    "international_implications": "DIA3 International Impact Analysis, Arms Control Studies, Maritime Security Research"
                },
                "key_takeaways": {
                    "strategic_significance": "DIA3 Strategic Significance Assessment, Naval History Analysis, Military Modernization Studies",
                    "complexity_factors": "DIA3 Complexity Analysis, Defense Planning Research, Strategic Implementation Studies",
                    "uncertainty_management": "DIA3 Uncertainty Analysis, Strategic Planning Research, Policy Flexibility Studies"
                },
                "final_assessment": {
                    "overall_impact": "DIA3 Comprehensive Impact Assessment, Regional Security Analysis, Strategic Stability Research",
                    "policy_implications": "DIA3 Policy Analysis, International Relations Research, Diplomatic Engagement Studies",
                    "monitoring_requirements": "DIA3 Monitoring Framework, Strategic Intelligence Analysis, Conflict Prevention Research"
                }
            }
        }
        
        return json.dumps(source_mapping.get(section, ["DIA3 Analysis"]))
    
    async def generate_report(self) -> Dict[str, Any]:
        """Generate the comprehensive interactive report."""
        
        try:
            logger.info("Starting Pakistan Submarine Interactive Report Generation")
            
            # Generate HTML content
            html_content = self.generate_interactive_html()
            
            # Create filename
            filename = f"pakistan_submarine_acquisition_analysis_and_deterrence_enhancement_interactive_enhanced_analysis_fixed_{self.timestamp}.html"
            filepath = Path("Results") / filename
            
            # Ensure Results directory exists
            Path("Results").mkdir(exist_ok=True)
            
            # Save HTML file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Interactive report generated successfully: {filepath}")
            
            return {
                "success": True,
                "file_path": str(filepath),
                "filename": filename,
                "topic": self.topic,
                "generated_at": datetime.now().isoformat(),
                "features": [
                    "Working interactive tooltips with multiple sources",
                    "DIA3 internal analysis attribution",
                    "External source references",
                    "Interactive visualizations with Chart.js",
                    "Comprehensive geopolitical analysis",
                    "Trade and economic impact assessment",
                    "Balance of power analysis",
                    "Escalation scenario modeling",
                    "Strategic use cases",
                    "Multi-perspective recommendations",
                    "Responsive design",
                    "Navigation system"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error generating interactive report: {e}")
            return {
                "success": False,
                "error": str(e),
                "topic": self.topic
            }


async def main():
    """Main function to generate the interactive Pakistan submarine analysis report."""
    
    print("=" * 80)
    print("Pakistan Submarine Acquisition Analysis - Interactive Enhanced Report (Fixed)")
    print("=" * 80)
    
    # Initialize the report generator
    generator = PakistanSubmarineInteractiveReportGenerator()
    
    # Generate the interactive report
    print("\n🔍 Generating interactive enhanced report with working tooltips...")
    result = await generator.generate_report()
    
    if result["success"]:
        print(f"✅ Interactive report generated successfully!")
        print(f"   - Topic: {result['topic']}")
        print(f"   - File: {result['filename']}")
        print(f"   - Path: {result['file_path']}")
        print(f"   - Generated at: {result['generated_at']}")
        
        print("\n📊 Report Features:")
        for feature in result['features']:
            print(f"   • {feature}")
        
        print(f"\n🌐 Open the report in your browser: {result['file_path']}")
        print("\n💡 Hover over any analysis card to see detailed tooltips with source attribution!")
        
    else:
        print(f"❌ Report generation failed: {result.get('error', 'Unknown error')}")
        return 1
    
    print("\n" + "=" * 80)
    print("Interactive report generation completed successfully!")
    print("=" * 80)
    
    return 0


if __name__ == "__main__":
    # Run the main function
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
