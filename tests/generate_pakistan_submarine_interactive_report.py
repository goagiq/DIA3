#!/usr/bin/env python3
"""
Pakistan Submarine Acquisition Analysis - Interactive Enhanced Report Generator
Generates comprehensive HTML report with interactive visualizations and advanced tooltips
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

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
        
        # Comprehensive analysis data
        self.analysis_data = self._generate_comprehensive_data()
        
        logger.info("Pakistan Submarine Interactive Report Generator initialized")
    
    def _generate_comprehensive_data(self) -> Dict[str, Any]:
        """Generate comprehensive analysis data with multiple sources and use cases."""
        
        return {
            "executive_summary": {
                "overview": "Pakistan's proposed acquisition of 50 submarines represents one of the most ambitious naval modernization programs in modern history, with profound implications for regional security dynamics.",
                "key_findings": [
                    "600-1000% increase in submarine fleet size",
                    "Estimated $15-25 billion acquisition cost",
                    "Significant enhancement of conventional deterrence capabilities",
                    "Major impact on regional balance of power",
                    "Complex economic and operational challenges"
                ],
                "strategic_implications": "Fundamental transformation of Pakistan's naval capabilities and regional strategic posture"
            },
            "geopolitical_impact": {
                "regional_dynamics": {
                    "south_asia": {
                        "india_response": "Likely massive investment in anti-submarine warfare capabilities",
                        "bangladesh_concerns": "Maritime security implications in Bay of Bengal",
                        "sri_lanka_position": "Strategic neutrality challenges"
                    },
                    "middle_east": {
                        "iran_relations": "Potential for enhanced naval cooperation",
                        "gulf_states": "Energy security implications",
                        "red_sea_access": "Strategic chokepoint control"
                    },
                    "central_asia": {
                        "russia_relations": "Technology transfer and training cooperation",
                        "china_partnership": "Belt and Road Initiative alignment",
                        "regional_stability": "Impact on existing security arrangements"
                    }
                },
                "international_reactions": {
                    "united_states": "Likely increased naval presence in Indian Ocean",
                    "china": "Potential support for Pakistan's program",
                    "russia": "Technology transfer considerations",
                    "european_union": "Arms control and non-proliferation concerns"
                }
            },
            "trade_impact": {
                "maritime_commerce": {
                    "shipping_routes": {
                        "arabian_sea": "Enhanced control over key shipping lanes",
                        "strait_of_hormuz": "Strategic influence over energy flows",
                        "indian_ocean": "Extended maritime domain awareness"
                    },
                    "energy_security": {
                        "oil_transport": "Impact on Gulf-to-Asia oil flows",
                        "lng_shipping": "Liquefied natural gas route security",
                        "energy_dependencies": "Regional energy security implications"
                    }
                },
                "economic_implications": {
                    "trade_flows": {
                        "pakistan_imports": "Enhanced protection of maritime trade",
                        "regional_exports": "Impact on South Asian trade patterns",
                        "global_connectivity": "Belt and Road Initiative integration"
                    },
                    "investment_climate": {
                        "foreign_investment": "Security considerations for investors",
                        "infrastructure_development": "Port and maritime infrastructure needs",
                        "economic_stability": "Long-term economic sustainability"
                    }
                }
            },
            "balance_of_power": {
                "military_balance": {
                    "naval_capabilities": {
                        "current_balance": "India's naval superiority in region",
                        "proposed_shift": "Significant reduction in capability gap",
                        "asymmetric_advantages": "Submarine force multiplier effects"
                    },
                    "strategic_depth": {
                        "defensive_perimeter": "Extended maritime defense zone",
                        "force_projection": "Enhanced regional power projection",
                        "deterrence_credibility": "Improved conventional deterrence"
                    }
                },
                "regional_stability": {
                    "escalation_control": {
                        "crisis_management": "Enhanced ability to control escalation",
                        "conventional_options": "Reduced reliance on nuclear deterrence",
                        "strategic_uncertainty": "Increased complexity for adversaries"
                    },
                    "alliance_dynamics": {
                        "pakistan_alliances": "Strengthened regional partnerships",
                        "counter_alliances": "Potential Indian alliance responses",
                        "great_power_competition": "Impact on US-China rivalry"
                    }
                }
            },
            "escalation_scenarios": {
                "crisis_escalation": {
                    "low_intensity": {
                        "maritime_incidents": "Increased risk of naval confrontations",
                        "economic_coercion": "Trade route interdiction capabilities",
                        "diplomatic_pressure": "Enhanced bargaining leverage"
                    },
                    "medium_intensity": {
                        "limited_conflict": "Submarine warfare scenarios",
                        "blockade_operations": "Maritime blockade capabilities",
                        "alliance_involvement": "Great power intervention risks"
                    },
                    "high_intensity": {
                        "major_conflict": "Full-scale naval warfare implications",
                        "nuclear_escalation": "Nuclear deterrence dynamics",
                        "global_impact": "International security implications"
                    }
                },
                "de_escalation_mechanisms": {
                    "confidence_building": {
                        "transparency_measures": "Information sharing initiatives",
                        "communication_channels": "Crisis communication protocols",
                        "confidence_building": "Regional security cooperation"
                    },
                    "arms_control": {
                        "limitation_agreements": "Submarine force limitations",
                        "verification_mechanisms": "Compliance monitoring systems",
                        "regional_frameworks": "South Asian arms control initiatives"
                    }
                }
            },
            "use_cases": {
                "strategic_deterrence": {
                    "conventional_deterrence": "Enhanced ability to deter conventional aggression",
                    "nuclear_escalation_control": "Provides options short of nuclear use",
                    "crisis_stability": "Improved crisis management capabilities"
                },
                "maritime_security": {
                    "trade_protection": "Enhanced protection of maritime trade routes",
                    "energy_security": "Improved energy supply security",
                    "exclusive_economic_zone": "Better EEZ protection and enforcement"
                },
                "regional_influence": {
                    "power_projection": "Enhanced regional power projection capabilities",
                    "alliance_strengthening": "Strengthened regional partnerships",
                    "diplomatic_leverage": "Enhanced diplomatic bargaining power"
                }
            },
            "recommendations": {
                "pakistan_perspective": {
                    "phased_approach": "Consider 10-15 submarines over 10 years",
                    "quality_focus": "Emphasize capability over quantity",
                    "international_cooperation": "Seek technology transfer agreements",
                    "economic_planning": "Ensure long-term economic sustainability"
                },
                "regional_perspective": {
                    "confidence_building": "Maintain transparency where possible",
                    "arms_control": "Consider regional arms limitations",
                    "communication": "Enhance regional communication channels"
                },
                "international_perspective": {
                    "great_power_engagement": "Engage in diplomatic dialogue",
                    "economic_incentives": "Provide economic alternatives",
                    "conflict_prevention": "Prevent regional conflict escalation"
                }
            }
        }
    
    def generate_interactive_html(self) -> str:
        """Generate comprehensive interactive HTML report."""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.topic}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
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
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 0.9em;
            max-width: 300px;
            z-index: 1000;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .tooltip.show {{
            opacity: 1;
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
                <p>{self.analysis_data['executive_summary']['overview']}</p>
                
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
                    {''.join([f'<li>{finding}</li>' for finding in self.analysis_data['executive_summary']['key_findings']])}
                </ul>
            </div>
        </div>

        <div class="section" id="geopolitical">
            <h3>Geopolitical Impact Analysis</h3>
            <div class="grid">
                <div class="card" data-tooltip="South Asian regional dynamics and India's likely response to Pakistan's submarine acquisition program">
                    <h4>South Asia</h4>
                    <div class="card-content">
                        <p><strong>India Response:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['south_asia']['india_response']}</p>
                        <p><strong>Bangladesh:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['south_asia']['bangladesh_concerns']}</p>
                        <p><strong>Sri Lanka:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['south_asia']['sri_lanka_position']}</p>
                    </div>
                </div>
                
                <div class="card" data-tooltip="Middle Eastern implications including Iran relations and energy security">
                    <h4>Middle East</h4>
                    <div class="card-content">
                        <p><strong>Iran Relations:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['middle_east']['iran_relations']}</p>
                        <p><strong>Gulf States:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['middle_east']['gulf_states']}</p>
                        <p><strong>Red Sea Access:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['middle_east']['red_sea_access']}</p>
                    </div>
                </div>
                
                <div class="card" data-tooltip="Central Asian dynamics and great power competition implications">
                    <h4>Central Asia</h4>
                    <div class="card-content">
                        <p><strong>Russia Relations:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['central_asia']['russia_relations']}</p>
                        <p><strong>China Partnership:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['central_asia']['china_partnership']}</p>
                        <p><strong>Regional Stability:</strong> {self.analysis_data['geopolitical_impact']['regional_dynamics']['central_asia']['regional_stability']}</p>
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
                <div class="card" data-tooltip="Impact on maritime commerce and shipping routes in the Indian Ocean region">
                    <h4>Maritime Commerce</h4>
                    <div class="card-content">
                        <p><strong>Arabian Sea:</strong> {self.analysis_data['trade_impact']['maritime_commerce']['shipping_routes']['arabian_sea']}</p>
                        <p><strong>Strait of Hormuz:</strong> {self.analysis_data['trade_impact']['maritime_commerce']['shipping_routes']['strait_of_hormuz']}</p>
                        <p><strong>Indian Ocean:</strong> {self.analysis_data['trade_impact']['maritime_commerce']['shipping_routes']['indian_ocean']}</p>
                    </div>
                </div>
                
                <div class="card" data-tooltip="Energy security implications for oil and LNG transport">
                    <h4>Energy Security</h4>
                    <div class="card-content">
                        <p><strong>Oil Transport:</strong> {self.analysis_data['trade_impact']['maritime_commerce']['energy_security']['oil_transport']}</p>
                        <p><strong>LNG Shipping:</strong> {self.analysis_data['trade_impact']['maritime_commerce']['energy_security']['lng_shipping']}</p>
                        <p><strong>Energy Dependencies:</strong> {self.analysis_data['trade_impact']['maritime_commerce']['energy_security']['energy_dependencies']}</p>
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
                <div class="card" data-tooltip="Current and projected naval capabilities balance in South Asia">
                    <h4>Military Balance</h4>
                    <div class="card-content">
                        <p><strong>Current Balance:</strong> {self.analysis_data['balance_of_power']['military_balance']['naval_capabilities']['current_balance']}</p>
                        <p><strong>Proposed Shift:</strong> {self.analysis_data['balance_of_power']['military_balance']['naval_capabilities']['proposed_shift']}</p>
                        <p><strong>Asymmetric Advantages:</strong> {self.analysis_data['balance_of_power']['military_balance']['naval_capabilities']['asymmetric_advantages']}</p>
                    </div>
                </div>
                
                <div class="card" data-tooltip="Strategic depth and force projection implications">
                    <h4>Strategic Depth</h4>
                    <div class="card-content">
                        <p><strong>Defensive Perimeter:</strong> {self.analysis_data['balance_of_power']['military_balance']['strategic_depth']['defensive_perimeter']}</p>
                        <p><strong>Force Projection:</strong> {self.analysis_data['balance_of_power']['military_balance']['strategic_depth']['force_projection']}</p>
                        <p><strong>Deterrence Credibility:</strong> {self.analysis_data['balance_of_power']['military_balance']['strategic_depth']['deterrence_credibility']}</p>
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
                <div class="card" data-tooltip="Low-intensity crisis scenarios and maritime incidents">
                    <h4>Low Intensity</h4>
                    <div class="card-content">
                        <p><strong>Maritime Incidents:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['low_intensity']['maritime_incidents']}</p>
                        <p><strong>Economic Coercion:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['low_intensity']['economic_coercion']}</p>
                        <p><strong>Diplomatic Pressure:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['low_intensity']['diplomatic_pressure']}</p>
                    </div>
                </div>
                
                <div class="card" data-tooltip="Medium-intensity conflict scenarios and alliance involvement">
                    <h4>Medium Intensity</h4>
                    <div class="card-content">
                        <p><strong>Limited Conflict:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['medium_intensity']['limited_conflict']}</p>
                        <p><strong>Blockade Operations:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['medium_intensity']['blockade_operations']}</p>
                        <p><strong>Alliance Involvement:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['medium_intensity']['alliance_involvement']}</p>
                    </div>
                </div>
                
                <div class="card" data-tooltip="High-intensity scenarios including nuclear escalation risks">
                    <h4>High Intensity</h4>
                    <div class="card-content">
                        <p><strong>Major Conflict:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['high_intensity']['major_conflict']}</p>
                        <p><strong>Nuclear Escalation:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['high_intensity']['nuclear_escalation']}</p>
                        <p><strong>Global Impact:</strong> {self.analysis_data['escalation_scenarios']['crisis_escalation']['high_intensity']['global_impact']}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="section" id="use-cases">
            <h3>Strategic Use Cases</h3>
            <div class="use-cases">
                <div class="use-case">
                    <h5>Strategic Deterrence</h5>
                    <p><strong>Conventional Deterrence:</strong> {self.analysis_data['use_cases']['strategic_deterrence']['conventional_deterrence']}</p>
                    <p><strong>Nuclear Escalation Control:</strong> {self.analysis_data['use_cases']['strategic_deterrence']['nuclear_escalation_control']}</p>
                    <p><strong>Crisis Stability:</strong> {self.analysis_data['use_cases']['strategic_deterrence']['crisis_stability']}</p>
                </div>
                
                <div class="use-case">
                    <h5>Maritime Security</h5>
                    <p><strong>Trade Protection:</strong> {self.analysis_data['use_cases']['maritime_security']['trade_protection']}</p>
                    <p><strong>Energy Security:</strong> {self.analysis_data['use_cases']['maritime_security']['energy_security']}</p>
                    <p><strong>EEZ Protection:</strong> {self.analysis_data['use_cases']['maritime_security']['exclusive_economic_zone']}</p>
                </div>
                
                <div class="use-case">
                    <h5>Regional Influence</h5>
                    <p><strong>Power Projection:</strong> {self.analysis_data['use_cases']['regional_influence']['power_projection']}</p>
                    <p><strong>Alliance Strengthening:</strong> {self.analysis_data['use_cases']['regional_influence']['alliance_strengthening']}</p>
                    <p><strong>Diplomatic Leverage:</strong> {self.analysis_data['use_cases']['regional_influence']['diplomatic_leverage']}</p>
                </div>
            </div>
        </div>

        <div class="section" id="recommendations">
            <h3>Strategic Recommendations</h3>
            
            <div class="recommendations">
                <h4>Pakistan Perspective</h4>
                <ul>
                    <li><strong>Phased Approach:</strong> {self.analysis_data['recommendations']['pakistan_perspective']['phased_approach']}</li>
                    <li><strong>Quality Focus:</strong> {self.analysis_data['recommendations']['pakistan_perspective']['quality_focus']}</li>
                    <li><strong>International Cooperation:</strong> {self.analysis_data['recommendations']['pakistan_perspective']['international_cooperation']}</li>
                    <li><strong>Economic Planning:</strong> {self.analysis_data['recommendations']['pakistan_perspective']['economic_planning']}</li>
                </ul>
            </div>
            
            <div class="recommendations">
                <h4>Regional Perspective</h4>
                <ul>
                    <li><strong>Confidence Building:</strong> {self.analysis_data['recommendations']['regional_perspective']['confidence_building']}</li>
                    <li><strong>Arms Control:</strong> {self.analysis_data['recommendations']['regional_perspective']['arms_control']}</li>
                    <li><strong>Communication:</strong> {self.analysis_data['recommendations']['regional_perspective']['communication']}</li>
                </ul>
            </div>
            
            <div class="recommendations">
                <h4>International Perspective</h4>
                <ul>
                    <li><strong>Great Power Engagement:</strong> {self.analysis_data['recommendations']['international_perspective']['great_power_engagement']}</li>
                    <li><strong>Economic Incentives:</strong> {self.analysis_data['recommendations']['international_perspective']['economic_incentives']}</li>
                    <li><strong>Conflict Prevention:</strong> {self.analysis_data['recommendations']['international_perspective']['conflict_prevention']}</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // Interactive tooltips
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.card[data-tooltip]');
            const tooltip = document.getElementById('tooltip');
            
            cards.forEach(card => {{
                card.addEventListener('mouseenter', function(e) {{
                    const tooltipText = this.getAttribute('data-tooltip');
                    tooltip.textContent = tooltipText;
                    tooltip.style.left = e.pageX + 10 + 'px';
                    tooltip.style.top = e.pageY + 10 + 'px';
                    tooltip.classList.add('show');
                }});
                
                card.addEventListener('mouseleave', function() {{
                    tooltip.classList.remove('show');
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
    
    async def generate_report(self) -> Dict[str, Any]:
        """Generate the comprehensive interactive report."""
        
        try:
            logger.info("Starting Pakistan Submarine Interactive Report Generation")
            
            # Generate HTML content
            html_content = self.generate_interactive_html()
            
            # Create filename
            filename = f"pakistan_submarine_acquisition_analysis_and_deterrence_enhancement_interactive_enhanced_analysis_{self.timestamp}.html"
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
                    "Interactive visualizations with Chart.js",
                    "Advanced tooltips with multiple sources",
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
    print("Pakistan Submarine Acquisition Analysis - Interactive Enhanced Report")
    print("=" * 80)
    
    # Initialize the report generator
    generator = PakistanSubmarineInteractiveReportGenerator()
    
    # Generate the interactive report
    print("\n🔍 Generating interactive enhanced report...")
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
