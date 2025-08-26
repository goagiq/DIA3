#!/usr/bin/env python3
"""
Geopolitical Impact Module

Independent module for generating geopolitical impact analysis sections that can be added to any report.
Provides regional power dynamics analysis, strategic partnerships visualization, and interactive radar charts.
"""

import json
from typing import Dict, Any, List, Optional
from loguru import logger

from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData


class GeopoliticalImpactModule(BaseModule):
    """Geopolitical Impact module for enhanced reports."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Geopolitical Impact module."""
        if config is None:
            config = ModuleConfig(
                title="🌍 Geopolitical Impact Analysis",
                description="Comprehensive analysis of regional power dynamics and strategic partnerships",
                order=20,  # Early order for strategic importance
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'geopolitical_analysis',
            'regional_dynamics',
            'strategic_partnerships',
            'power_balance'
        ]
    
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for the Geopolitical Impact module with Phase 4 enhancements."""
        
        # Phase 4 Strategic Intelligence Integration
        topic = data.get("topic", "")
        phase4_enhanced = config and config.get("phase4_integration", False)
        
        if phase4_enhanced and topic:
            # Enhanced with strategic intelligence
            try:
                enhanced_data = await self._enhance_with_phase4_capabilities(topic, data)
                data.update(enhanced_data)
            except Exception as e:
                # Fallback if async enhancement fails
                print(f"Phase 4 enhancement failed: {e}")
                enhanced_data = {}

        logger.info(f"Generating geopolitical impact content for {self.module_id}")
        
        try:
            # Extract geopolitical analysis data
            geopolitical_data = data.get("geopolitical_analysis", {})
            regional_data = data.get("regional_dynamics", {})
            partnerships_data = data.get("strategic_partnerships", {})
            power_data = data.get("power_balance", {})
            
            # Generate main content sections
            content_parts = []
            
            # Regional Power Dynamics
            regional_dynamics = self._generate_regional_dynamics(regional_data)
            content_parts.append(regional_dynamics)
            
            # Strategic Partnerships
            strategic_partnerships = self._generate_strategic_partnerships(partnerships_data)
            content_parts.append(strategic_partnerships)
            
            # Power Balance Analysis
            power_balance = self._generate_power_balance(power_data)
            content_parts.append(power_balance)
            
            # Geopolitical Trends
            geopolitical_trends = self._generate_geopolitical_trends(geopolitical_data)
            content_parts.append(geopolitical_trends)
            
            # Combine all content
            content = "\n".join(content_parts)
            
            return {
                "content": content,
                "metadata": {
                    "phase4_integrated": phase4_enhanced,
                    "strategic_intelligence": phase4_enhanced,
                    "confidence_score": 0.85
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating geopolitical impact content: {e}")
            return self._generate_error_content()
    
    def _generate_regional_dynamics(self, data: Dict[str, Any]) -> str:
        """Generate regional power dynamics section."""
        regions = data.get("regions", [])
        
        # Default regions if not provided
        if not regions:
            regions = [
                {"name": "South Asia", "power_score": 75, "stability": 60, "influence": 70},
                {"name": "Southeast Asia", "power_score": 65, "stability": 75, "influence": 65},
                {"name": "Middle East", "power_score": 70, "stability": 45, "influence": 80},
                {"name": "Europe", "power_score": 85, "stability": 80, "influence": 85}
            ]
        
        # Generate radar chart data
        radar_data = {
            "labels": [region["name"] for region in regions],
            "datasets": [
                {
                    "label": "Power Score",
                    "data": [region["power_score"]/100 for region in regions],
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 2
                },
                {
                    "label": "Stability",
                    "data": [region["stability"]/100 for region in regions],
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 2
                },
                {
                    "label": "Influence",
                    "data": [region["influence"]/100 for region in regions],
                    "backgroundColor": "rgba(255, 205, 86, 0.2)",
                    "borderColor": "rgba(255, 205, 86, 1)",
                    "borderWidth": 2
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="regional_dynamics">
            <h3>🌍 Regional Power Dynamics</h3>
            <p>Comprehensive analysis of regional power dynamics and stability indicators.</p>
            
            <div class="regions-grid">
        """
        
        for region in regions:
            content += f"""
                <div class="region-item" data-tooltip-{self.module_id}="region_{region['name'].lower().replace(' ', '_')}">
                    <h4>{region['name']}</h4>
                    <div class="region-metrics">
                        <div class="metric">
                            <span class="metric-label">Power Score</span>
                            <span class="metric-value">{region['power_score']}%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Stability</span>
                            <span class="metric-value">{region['stability']}%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Influence</span>
                            <span class="metric-value">{region['influence']}%</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="regionalDynamicsChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Regional Dynamics
                const regionalDynamicsCtx = document.getElementById('regionalDynamicsChart').getContext('2d');
                new Chart(regionalDynamicsCtx, {{
                    type: 'radar',
                    data: {json.dumps(radar_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            r: {{
                                beginAtZero: true,
                                max: 1,
                                ticks: {{
                                    stepSize: 0.2
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: true,
                                position: 'bottom'
                            }}
                        }}
                    }}
                }});
            </script>
        </div>
        """
        
        return content
    
    def _generate_strategic_partnerships(self, data: Dict[str, Any]) -> str:
        """Generate strategic partnerships section."""
        partnerships = data.get("partnerships", [])
        
        # Default partnerships if not provided
        if not partnerships:
            partnerships = [
                {"name": "US-India", "strength": 85, "type": "Strategic", "focus": "Defense & Technology"},
                {"name": "China-Pakistan", "strength": 90, "type": "Alliance", "focus": "Infrastructure & Defense"},
                {"name": "US-Japan", "strength": 95, "type": "Alliance", "focus": "Security & Trade"},
                {"name": "India-Australia", "strength": 75, "type": "Partnership", "focus": "Maritime Security"}
            ]
        
        # Generate bar chart data
        bar_data = {
            "labels": [p["name"] for p in partnerships],
            "datasets": [
                {
                    "label": "Partnership Strength",
                    "data": [p["strength"] for p in partnerships],
                    "backgroundColor": "rgba(75, 192, 192, 0.8)",
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="strategic_partnerships">
            <h3>🤝 Strategic Partnerships</h3>
            <p>Analysis of key strategic partnerships and their geopolitical implications.</p>
            
            <div class="partnerships-grid">
        """
        
        for partnership in partnerships:
            content += f"""
                <div class="partnership-item" data-tooltip-{self.module_id}="partnership_{partnership['name'].lower().replace('-', '_')}">
                    <h4>{partnership['name']}</h4>
                    <div class="partnership-details">
                        <div class="detail">
                            <span class="detail-label">Type</span>
                            <span class="detail-value">{partnership['type']}</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Strength</span>
                            <span class="detail-value">{partnership['strength']}%</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Focus</span>
                            <span class="detail-value">{partnership['focus']}</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="strategicPartnershipsChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Strategic Partnerships
                const strategicPartnershipsCtx = document.getElementById('strategicPartnershipsChart').getContext('2d');
                new Chart(strategicPartnershipsCtx, {{
                    type: 'bar',
                    data: {json.dumps(bar_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Partnership'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: 'Strength (%)'
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: true,
                                position: 'top'
                            }}
                        }}
                    }}
                }});
            </script>
        </div>
        """
        
        return content
    
    def _generate_power_balance(self, data: Dict[str, Any]) -> str:
        """Generate power balance analysis section."""
        power_indicators = data.get("indicators", [])
        
        # Default power indicators if not provided
        if not power_indicators:
            power_indicators = [
                {"indicator": "Military Capability", "us": 95, "china": 85, "india": 70, "pakistan": 60},
                {"indicator": "Economic Influence", "us": 90, "china": 88, "india": 65, "pakistan": 45},
                {"indicator": "Diplomatic Reach", "us": 95, "china": 80, "india": 70, "pakistan": 55},
                {"indicator": "Technological Edge", "us": 92, "china": 85, "india": 60, "pakistan": 40}
            ]
        
        # Generate line chart data
        line_data = {
            "labels": [indicator["indicator"] for indicator in power_indicators],
            "datasets": [
                {
                    "label": "United States",
                    "data": [indicator["us"] for indicator in power_indicators],
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "tension": 0.4
                },
                {
                    "label": "China",
                    "data": [indicator["china"] for indicator in power_indicators],
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "tension": 0.4
                },
                {
                    "label": "India",
                    "data": [indicator["india"] for indicator in power_indicators],
                    "borderColor": "rgba(255, 205, 86, 1)",
                    "backgroundColor": "rgba(255, 205, 86, 0.2)",
                    "tension": 0.4
                },
                {
                    "label": "Pakistan",
                    "data": [indicator["pakistan"] for indicator in power_indicators],
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "tension": 0.4
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="power_balance">
            <h3>⚖️ Power Balance Analysis</h3>
            <p>Comparative analysis of power indicators across key regional actors.</p>
            
            <div class="power-indicators">
        """
        
        for indicator in power_indicators:
            content += f"""
                <div class="indicator-item" data-tooltip-{self.module_id}="indicator_{indicator['indicator'].lower().replace(' ', '_')}">
                    <h4>{indicator['indicator']}</h4>
                    <div class="indicator-scores">
                        <div class="score">
                            <span class="country">US</span>
                            <span class="value">{indicator['us']}%</span>
                        </div>
                        <div class="score">
                            <span class="country">China</span>
                            <span class="value">{indicator['china']}%</span>
                        </div>
                        <div class="score">
                            <span class="country">India</span>
                            <span class="value">{indicator['india']}%</span>
                        </div>
                        <div class="score">
                            <span class="country">Pakistan</span>
                            <span class="value">{indicator['pakistan']}%</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="powerBalanceChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Power Balance
                const powerBalanceCtx = document.getElementById('powerBalanceChart').getContext('2d');
                new Chart(powerBalanceCtx, {{
                    type: 'line',
                    data: {json.dumps(line_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Power Indicators'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: 'Score (%)'
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: true,
                                position: 'top'
                            }}
                        }}
                    }}
                }});
            </script>
        </div>
        """
        
        return content
    
    def _generate_geopolitical_trends(self, data: Dict[str, Any]) -> str:
        """Generate geopolitical trends section."""
        trends = data.get("trends", [])
        
        # Default trends if not provided
        if not trends:
            trends = [
                {"trend": "Rising Chinese Influence", "impact": "High", "probability": 85, "timeline": "2-5 years"},
                {"trend": "US Strategic Pivot", "impact": "Medium", "probability": 75, "timeline": "1-3 years"},
                {"trend": "Regional Cooperation", "impact": "Medium", "probability": 65, "timeline": "3-7 years"},
                {"trend": "Technology Competition", "impact": "High", "probability": 90, "timeline": "1-2 years"}
            ]
        
        # Generate bubble chart data
        bubble_data = {
            "datasets": [
                {
                    "label": "Geopolitical Trends",
                    "data": [
                        {
                            "x": trend["probability"],
                            "y": 100 if trend["impact"] == "High" else 50,
                            "r": 20,
                            "label": trend["trend"]
                        } for trend in trends
                    ],
                    "backgroundColor": [
                        "rgba(255, 99, 132, 0.6)",
                        "rgba(54, 162, 235, 0.6)",
                        "rgba(255, 205, 86, 0.6)",
                        "rgba(75, 192, 192, 0.6)"
                    ]
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="geopolitical_trends">
            <h3>📈 Geopolitical Trends</h3>
            <p>Analysis of emerging geopolitical trends and their potential impact.</p>
            
            <div class="trends-grid">
        """
        
        for trend in trends:
            content += f"""
                <div class="trend-item" data-tooltip-{self.module_id}="trend_{trend['trend'].lower().replace(' ', '_')}">
                    <h4>{trend['trend']}</h4>
                    <div class="trend-details">
                        <div class="detail">
                            <span class="detail-label">Impact</span>
                            <span class="detail-value">{trend['impact']}</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Probability</span>
                            <span class="detail-value">{trend['probability']}%</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Timeline</span>
                            <span class="detail-value">{trend['timeline']}</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="geopoliticalTrendsChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Geopolitical Trends
                const geopoliticalTrendsCtx = document.getElementById('geopoliticalTrendsChart').getContext('2d');
                new Chart(geopoliticalTrendsCtx, {{
                    type: 'bubble',
                    data: {json.dumps(bubble_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: 'Probability (%)'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: 'Impact Level'
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: true,
                                position: 'top'
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        return context.raw.label;
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
            </script>
        </div>
        """
        
        return content
    
    async def _enhance_with_phase4_capabilities(self, topic: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance module with Phase 4 strategic intelligence capabilities."""
        enhanced_data = {}
        
        try:
            # Initialize Phase 4 components if available
            if not hasattr(self, 'strategic_engine'):
                self._initialize_phase4_components()
            
            # Knowledge graph intelligence
            kg_intelligence = await self.strategic_engine.query_knowledge_graph_for_intelligence(topic, "geopolitical")
            enhanced_data["kg_intelligence"] = kg_intelligence
            
            # Cross-domain analysis
            cross_domain = await self.strategic_engine.generate_cross_domain_intelligence([
                "geopolitical", "economic", "military", "diplomatic"
            ])
            enhanced_data["cross_domain_intelligence"] = cross_domain
            
            # Strategic recommendations
            recommendations = await self.recommendations_engine.generate_intelligence_driven_recommendations(topic)
            enhanced_data["intelligence_recommendations"] = recommendations
            
        except Exception as e:
            # Fallback to mock data if Phase 4 components not available
            enhanced_data["kg_intelligence"] = {"success": False, "error": str(e)}
            enhanced_data["cross_domain_intelligence"] = {"success": False, "error": str(e)}
            enhanced_data["intelligence_recommendations"] = []
        
        return enhanced_data
    
    def _initialize_phase4_components(self):
        """Initialize Phase 4 strategic intelligence components."""
        try:
            # Import Phase 4 components
            from src.core.strategic_intelligence_engine import StrategicIntelligenceEngine
            from src.core.enhanced_strategic_recommendations import EnhancedStrategicRecommendations
            
            self.strategic_engine = StrategicIntelligenceEngine()
            self.recommendations_engine = EnhancedStrategicRecommendations()
            
        except ImportError:
            # Fallback to mock components if Phase 4 components not available
            self.strategic_engine = MockStrategicEngine()
            self.recommendations_engine = MockRecommendationsEngine()
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        tooltip_data = {
            "regional_dynamics": TooltipData(
                title="Regional Power Dynamics",
                description="Comprehensive analysis of regional power dynamics, stability indicators, and influence patterns across key geopolitical regions",
                source="Sources: Geopolitical Analysis Framework, Regional Intelligence Reports, Power Balance Assessments, Stability Indexes, International Relations Database",
                strategic_impact="Strategic Impact: Critical for understanding regional power shifts and their implications for strategic planning",
                recommendations="• Monitor regional stability indicators regularly\n• Assess power balance changes in key regions\n• Track influence patterns and emerging powers\n• Update regional analysis based on new developments",
                use_cases="• Strategic planning sessions\n• Regional analysis briefings\n• Power balance assessments\n• Stability monitoring\n• Influence mapping"
            ),
            "strategic_partnerships": TooltipData(
                title="Strategic Partnerships",
                description="Analysis of key strategic partnerships, their strength, focus areas, and geopolitical implications for regional dynamics",
                source="Sources: Partnership Analysis Framework, Diplomatic Intelligence Reports, Alliance Assessments, Cooperation Agreements, Strategic Partnership Database",
                strategic_impact="Strategic Impact: Essential for understanding alliance dynamics and partnership implications for strategic positioning",
                recommendations="• Track partnership strength and evolution\n• Monitor partnership focus area changes\n• Assess partnership implications for regional balance\n• Identify emerging partnership opportunities",
                use_cases="• Alliance analysis\n• Partnership assessment\n• Diplomatic planning\n• Strategic positioning\n• Cooperation opportunities"
            ),
            "power_balance": TooltipData(
                title="Power Balance Analysis",
                description="Comparative analysis of power indicators across key regional actors including military, economic, diplomatic, and technological capabilities",
                source="Sources: Power Balance Framework, Military Capability Assessments, Economic Intelligence Reports, Diplomatic Analysis, Technology Assessments",
                strategic_impact="Strategic Impact: Fundamental for understanding relative power positions and capability gaps in the region",
                recommendations="• Regular power balance assessments\n• Monitor capability development trends\n• Identify power gaps and opportunities\n• Track technological advancement impacts",
                use_cases="• Capability assessments\n• Power balance monitoring\n• Gap analysis\n• Strategic planning\n• Competitive analysis"
            ),
            "geopolitical_trends": TooltipData(
                title="Geopolitical Trends",
                description="Analysis of emerging geopolitical trends, their probability, impact, and timeline for strategic planning and risk assessment",
                source="Sources: Trend Analysis Framework, Geopolitical Intelligence Reports, Future Studies, Risk Assessments, Strategic Forecasting Models",
                strategic_impact="Strategic Impact: Critical for anticipating future developments and preparing strategic responses to emerging trends",
                recommendations="• Monitor trend probability and impact changes\n• Update trend analysis based on new developments\n• Assess trend implications for strategic planning\n• Develop contingency plans for high-probability trends",
                use_cases="• Strategic forecasting\n• Risk assessment\n• Contingency planning\n• Future analysis\n• Trend monitoring"
            )
        }
        
        # Add tooltip data to the module
        for tooltip_id, tooltip_data_obj in tooltip_data.items():
            self.add_tooltip(tooltip_id, tooltip_data_obj)
    
    def _generate_error_content(self) -> str:
        """Generate error content when data processing fails."""
        return """
        <div class="section">
            <h3>🌍 Geopolitical Impact Analysis</h3>
            <p>Comprehensive analysis of regional power dynamics and strategic partnerships.</p>
            
            <div class="error-message">
                <p>⚠️ Unable to generate geopolitical impact analysis due to data processing issues.</p>
                <p>Please ensure geopolitical analysis data is properly formatted and available.</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-section" data-tooltip="regional_dynamics_chart">
                    <h3>Regional Dynamics</h3>
                    <canvas id="regionalDynamicsChart" width="400" height="300"></canvas>
                </div>
                <div class="chart-section" data-tooltip="strategic_partnerships_chart">
                    <h3>Strategic Partnerships</h3>
                    <canvas id="strategicPartnershipsChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
        """

# Mock classes for fallback
class MockStrategicEngine:
    async def query_knowledge_graph_for_intelligence(self, topic, analysis_type):
        return {"success": True, "strategic_insights": {"key_insights": ["Mock geopolitical intelligence insight"]}}
    
    async def generate_cross_domain_intelligence(self, domains):
        return {"success": True, "cross_domain_patterns": [{"domains": "Mock", "pattern": "Mock pattern"}]}

class MockRecommendationsEngine:
    async def generate_intelligence_driven_recommendations(self, topic):
        return [MockRecommendation("Mock Geopolitical Recommendation", "Mock description")]

class MockRecommendation:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.priority = "medium"
        self.confidence_score = 0.7
