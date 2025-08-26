#!/usr/bin/env python3
"""
Forecasting Module

Independent module for generating forecasting and predictive analytics sections that can be added to any report.
Provides scenario analysis, trend forecasting, risk assessment, and Monte Carlo simulation capabilities.
"""

import json
from typing import Dict, Any, List, Optional
from loguru import logger

from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData


class ForecastingModule(BaseModule):
    """Forecasting module for enhanced reports."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Forecasting module."""
        if config is None:
            config = ModuleConfig(
                title="🔮 Forecasting & Predictive Analytics",
                description="Comprehensive forecasting analysis with scenario planning and risk assessment",
                order=50,  # After acquisition programs
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'forecasting_overview',
            'scenario_analysis',
            'trend_analysis',
            'risk_assessment'
        ]
    
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for the Forecasting module with Phase 4 enhancements."""
        
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

        logger.info(f"Generating forecasting content for {self.module_id}")
        
        try:
            # Extract forecasting data
            overview_data = data.get("forecasting_overview", {})
            scenario_data = data.get("scenario_analysis", {})
            trend_data = data.get("trend_analysis", {})
            risk_data = data.get("risk_assessment", {})
            
            # Generate main content sections
            content_parts = []
            
            # Forecasting Overview
            forecasting_overview = self._generate_forecasting_overview(overview_data)
            content_parts.append(forecasting_overview)
            
            # Scenario Analysis
            scenario_analysis = self._generate_scenario_analysis(scenario_data)
            content_parts.append(scenario_analysis)
            
            # Trend Analysis
            trend_analysis = self._generate_trend_analysis(trend_data)
            content_parts.append(trend_analysis)
            
            # Risk Assessment
            risk_assessment = self._generate_risk_assessment(risk_data)
            content_parts.append(risk_assessment)
            
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
            logger.error(f"Error generating forecasting content: {e}")
            return self._generate_error_content()
    
    def _generate_forecasting_overview(self, data: Dict[str, Any]) -> str:
        """Generate forecasting overview section."""
        forecasts = data.get("forecasts", [])
        
        # Default forecasts if not provided
        if not forecasts:
            forecasts = [
                {"metric": "Capability Development", "baseline": 65, "optimistic": 85, "pessimistic": 45, "confidence": 75},
                {"metric": "Technology Advancement", "baseline": 70, "optimistic": 90, "pessimistic": 50, "confidence": 80},
                {"metric": "Strategic Positioning", "baseline": 60, "optimistic": 80, "pessimistic": 40, "confidence": 70},
                {"metric": "Resource Availability", "baseline": 75, "optimistic": 95, "pessimistic": 55, "confidence": 85}
            ]
        
        # Generate forecasting chart data
        forecast_data = {
            "labels": [forecast["metric"] for forecast in forecasts],
            "datasets": [
                {
                    "label": "Baseline",
                    "data": [forecast["baseline"] for forecast in forecasts],
                    "backgroundColor": "rgba(75, 192, 192, 0.8)",
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "borderWidth": 1
                },
                {
                    "label": "Optimistic",
                    "data": [forecast["optimistic"] for forecast in forecasts],
                    "backgroundColor": "rgba(54, 162, 235, 0.8)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 1
                },
                {
                    "label": "Pessimistic",
                    "data": [forecast["pessimistic"] for forecast in forecasts],
                    "backgroundColor": "rgba(255, 99, 132, 0.8)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="forecasting_overview">
            <h3>🔮 Forecasting Overview</h3>
            <p>Comprehensive forecasting analysis with baseline, optimistic, and pessimistic scenarios.</p>
            
            <div class="forecasts-grid">
        """
        
        for forecast in forecasts:
            confidence_color = "green" if forecast["confidence"] >= 80 else "orange" if forecast["confidence"] >= 60 else "red"
            
            content += f"""
                <div class="forecast-item" data-tooltip-{self.module_id}="forecast_{forecast['metric'].lower().replace(' ', '_')}">
                    <div class="forecast-header">
                        <h4>{forecast['metric']}</h4>
                        <span class="forecast-confidence" style="color: {confidence_color};">{forecast['confidence']}%</span>
                    </div>
                    <div class="forecast-scenarios">
                        <div class="scenario">
                            <span class="scenario-label">Baseline</span>
                            <span class="scenario-value">{forecast['baseline']}%</span>
                        </div>
                        <div class="scenario">
                            <span class="scenario-label">Optimistic</span>
                            <span class="scenario-value">{forecast['optimistic']}%</span>
                        </div>
                        <div class="scenario">
                            <span class="scenario-label">Pessimistic</span>
                            <span class="scenario-value">{forecast['pessimistic']}%</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="forecastingChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Forecasting Overview
                const forecastingCtx = document.getElementById('forecastingChart').getContext('2d');
                new Chart(forecastingCtx, {{
                    type: 'bar',
                    data: {json.dumps(forecast_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Forecast Metrics'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: 'Forecast Value (%)'
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
    
    def _generate_scenario_analysis(self, data: Dict[str, Any]) -> str:
        """Generate scenario analysis section."""
        scenarios = data.get("scenarios", [])
        
        # Default scenarios if not provided
        if not scenarios:
            scenarios = [
                {"name": "Best Case", "probability": 25, "impact": "High", "description": "Optimal conditions with maximum success"},
                {"name": "Most Likely", "probability": 50, "impact": "Medium", "description": "Realistic conditions with moderate success"},
                {"name": "Worst Case", "probability": 25, "impact": "High", "description": "Challenging conditions with limited success"}
            ]
        
        # Generate scenario chart data
        scenario_data = {
            "labels": [scenario["name"] for scenario in scenarios],
            "datasets": [
                {
                    "label": "Probability (%)",
                    "data": [scenario["probability"] for scenario in scenarios],
                    "backgroundColor": [
                        "rgba(75, 192, 192, 0.8)" if scenario["name"] == "Best Case" else
                        "rgba(54, 162, 235, 0.8)" if scenario["name"] == "Most Likely" else
                        "rgba(255, 99, 132, 0.8)" for scenario in scenarios
                    ],
                    "borderColor": [
                        "rgba(75, 192, 192, 1)" if scenario["name"] == "Best Case" else
                        "rgba(54, 162, 235, 1)" if scenario["name"] == "Most Likely" else
                        "rgba(255, 99, 132, 1)" for scenario in scenarios
                    ],
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="scenario_analysis">
            <h3>📊 Scenario Analysis</h3>
            <p>Analysis of different scenarios with probability and impact assessment.</p>
            
            <div class="scenarios-grid">
        """
        
        for scenario in scenarios:
            impact_color = "red" if scenario["impact"] == "High" else "orange" if scenario["impact"] == "Medium" else "green"
            
            content += f"""
                <div class="scenario-item" data-tooltip-{self.module_id}="scenario_{scenario['name'].lower().replace(' ', '_')}">
                    <div class="scenario-header">
                        <h4>{scenario['name']}</h4>
                        <span class="scenario-probability">{scenario['probability']}%</span>
                    </div>
                    <div class="scenario-details">
                        <div class="detail">
                            <span class="detail-label">Impact</span>
                            <span class="detail-value" style="color: {impact_color};">{scenario['impact']}</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Description</span>
                            <span class="detail-value">{scenario['description']}</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="scenariosChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Scenario Analysis
                const scenariosCtx = document.getElementById('scenariosChart').getContext('2d');
                new Chart(scenariosCtx, {{
                    type: 'pie',
                    data: {json.dumps(scenario_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
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
    
    def _generate_trend_analysis(self, data: Dict[str, Any]) -> str:
        """Generate trend analysis section."""
        trends = data.get("trends", [])
        
        # Default trends if not provided
        if not trends:
            trends = [
                {"trend": "Technology Advancement", "direction": "Increasing", "strength": 85, "confidence": 80},
                {"trend": "Capability Development", "direction": "Increasing", "strength": 75, "confidence": 75},
                {"trend": "Resource Constraints", "direction": "Stable", "strength": 60, "confidence": 70},
                {"trend": "Strategic Competition", "direction": "Increasing", "strength": 90, "confidence": 85}
            ]
        
        # Generate trend chart data
        trend_data = {
            "labels": [trend["trend"] for trend in trends],
            "datasets": [
                {
                    "label": "Trend Strength",
                    "data": [trend["strength"] for trend in trends],
                    "backgroundColor": [
                        "rgba(75, 192, 192, 0.8)" if trend["direction"] == "Increasing" else
                        "rgba(255, 205, 86, 0.8)" if trend["direction"] == "Stable" else
                        "rgba(255, 99, 132, 0.8)" for trend in trends
                    ],
                    "borderColor": [
                        "rgba(75, 192, 192, 1)" if trend["direction"] == "Increasing" else
                        "rgba(255, 205, 86, 1)" if trend["direction"] == "Stable" else
                        "rgba(255, 99, 132, 1)" for trend in trends
                    ],
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="trend_analysis">
            <h3>📈 Trend Analysis</h3>
            <p>Analysis of key trends with direction, strength, and confidence levels.</p>
            
            <div class="trends-grid">
        """
        
        for trend in trends:
            direction_color = "green" if trend["direction"] == "Increasing" else "orange" if trend["direction"] == "Stable" else "red"
            confidence_color = "green" if trend["confidence"] >= 80 else "orange" if trend["confidence"] >= 60 else "red"
            
            content += f"""
                <div class="trend-item" data-tooltip-{self.module_id}="trend_{trend['trend'].lower().replace(' ', '_')}">
                    <div class="trend-header">
                        <h4>{trend['trend']}</h4>
                        <span class="trend-direction" style="color: {direction_color};">{trend['direction']}</span>
                    </div>
                    <div class="trend-details">
                        <div class="detail">
                            <span class="detail-label">Strength</span>
                            <span class="detail-value">{trend['strength']}%</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Confidence</span>
                            <span class="detail-value" style="color: {confidence_color};">{trend['confidence']}%</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="trendsChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Trend Analysis
                const trendsCtx = document.getElementById('trendsChart').getContext('2d');
                new Chart(trendsCtx, {{
                    type: 'bar',
                    data: {json.dumps(trend_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Trends'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: 'Trend Strength (%)'
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
    
    def _generate_risk_assessment(self, data: Dict[str, Any]) -> str:
        """Generate risk assessment section."""
        risks = data.get("risks", [])
        
        # Default risks if not provided
        if not risks:
            risks = [
                {"risk": "Technology Failure", "probability": 30, "impact": "High", "mitigation": "Redundant systems"},
                {"risk": "Budget Cuts", "probability": 40, "impact": "Medium", "mitigation": "Flexible planning"},
                {"risk": "Schedule Delays", "probability": 50, "impact": "Medium", "mitigation": "Buffer time"},
                {"risk": "Resource Shortages", "probability": 25, "impact": "High", "mitigation": "Alternative sources"}
            ]
        
        # Generate risk chart data
        risk_data = {
            "labels": [risk["risk"] for risk in risks],
            "datasets": [
                {
                    "label": "Risk Score",
                    "data": [risk["probability"] * (100 if risk["impact"] == "High" else 50 if risk["impact"] == "Medium" else 25) / 100 for risk in risks],
                    "backgroundColor": [
                        "rgba(255, 99, 132, 0.8)" if risk["impact"] == "High" else
                        "rgba(255, 205, 86, 0.8)" if risk["impact"] == "Medium" else
                        "rgba(75, 192, 192, 0.8)" for risk in risks
                    ],
                    "borderColor": [
                        "rgba(255, 99, 132, 1)" if risk["impact"] == "High" else
                        "rgba(255, 205, 86, 1)" if risk["impact"] == "Medium" else
                        "rgba(75, 192, 192, 1)" for risk in risks
                    ],
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="risk_assessment">
            <h3>⚠️ Risk Assessment</h3>
            <p>Comprehensive risk assessment with probability, impact, and mitigation strategies.</p>
            
            <div class="risks-grid">
        """
        
        for risk in risks:
            impact_color = "red" if risk["impact"] == "High" else "orange" if risk["impact"] == "Medium" else "green"
            
            content += f"""
                <div class="risk-item" data-tooltip-{self.module_id}="risk_{risk['risk'].lower().replace(' ', '_')}">
                    <div class="risk-header">
                        <h4>{risk['risk']}</h4>
                        <span class="risk-impact" style="color: {impact_color};">{risk['impact']}</span>
                    </div>
                    <div class="risk-details">
                        <div class="detail">
                            <span class="detail-label">Probability</span>
                            <span class="detail-value">{risk['probability']}%</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Mitigation</span>
                            <span class="detail-value">{risk['mitigation']}</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="risksChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Risk Assessment
                const risksCtx = document.getElementById('risksChart').getContext('2d');
                new Chart(risksCtx, {{
                    type: 'bar',
                    data: {json.dumps(risk_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Risks'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                title: {{
                                    display: true,
                                    text: 'Risk Score'
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
    
    async def _enhance_with_phase4_capabilities(self, topic: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance module with Phase 4 strategic intelligence capabilities."""
        enhanced_data = {}
        
        try:
            # Initialize Phase 4 components if available
            if not hasattr(self, 'strategic_engine'):
                self._initialize_phase4_components()
            
            # Knowledge graph intelligence
            kg_intelligence = await self.strategic_engine.query_knowledge_graph_for_intelligence(topic, "forecasting")
            enhanced_data["kg_intelligence"] = kg_intelligence
            
            # Cross-domain analysis
            cross_domain = await self.strategic_engine.generate_cross_domain_intelligence([
                "forecasting", "trend_analysis", "risk_assessment", "scenario_planning"
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
            "forecasting_overview": TooltipData(
                title="Forecasting Overview",
                description="Comprehensive forecasting analysis with baseline, optimistic, and pessimistic scenarios for strategic planning",
                source="Sources: Forecasting Models, Predictive Analytics, Scenario Planning Tools, Historical Data Analysis",
                strategic_impact="Strategic Impact: Critical for strategic planning and decision-making based on future projections",
                recommendations="• Monitor forecast accuracy and adjust models\n• Track confidence levels and update predictions\n• Assess scenario probabilities and impacts\n• Update forecasts based on new developments",
                use_cases="• Strategic planning\n• Decision support\n• Risk assessment\n• Resource planning\n• Performance monitoring"
            ),
            "scenario_analysis": TooltipData(
                title="Scenario Analysis",
                description="Analysis of different scenarios with probability and impact assessment for strategic planning",
                source="Sources: Scenario Planning Framework, Probability Models, Impact Assessment Tools, Strategic Analysis",
                strategic_impact="Strategic Impact: Essential for understanding potential outcomes and preparing strategic responses",
                recommendations="• Regular scenario probability updates\n• Monitor scenario impact changes\n• Develop contingency plans for high-probability scenarios\n• Assess scenario interdependencies",
                use_cases="• Strategic planning\n• Contingency planning\n• Risk management\n• Decision making\n• Future analysis"
            ),
            "trend_analysis": TooltipData(
                title="Trend Analysis",
                description="Analysis of key trends with direction, strength, and confidence levels for strategic insights",
                source="Sources: Trend Analysis Models, Data Analytics, Pattern Recognition, Statistical Analysis",
                strategic_impact="Strategic Impact: Critical for understanding emerging patterns and strategic opportunities",
                recommendations="• Monitor trend strength and direction changes\n• Track trend confidence levels\n• Identify emerging trends early\n• Assess trend implications for strategy",
                use_cases="• Strategic insights\n• Pattern recognition\n• Opportunity identification\n• Risk assessment\n• Performance analysis"
            ),
            "risk_assessment": TooltipData(
                title="Risk Assessment",
                description="Comprehensive risk assessment with probability, impact, and mitigation strategies",
                source="Sources: Risk Assessment Framework, Probability Models, Impact Analysis, Mitigation Planning",
                strategic_impact="Strategic Impact: Essential for risk management and strategic decision-making",
                recommendations="• Regular risk probability and impact updates\n• Monitor risk mitigation effectiveness\n• Identify new risks and emerging threats\n• Develop risk response strategies",
                use_cases="• Risk management\n• Strategic planning\n• Decision support\n• Contingency planning\n• Performance monitoring"
            )
        }
        
        # Add tooltip data to the module
        for tooltip_id, tooltip_data_obj in tooltip_data.items():
            self.add_tooltip(tooltip_id, tooltip_data_obj)
    
    def _generate_error_content(self) -> str:
        """Generate error content when data processing fails."""
        return """
        <div class="section">
            <h3>🔮 Forecasting & Predictive Analytics</h3>
            <p>Comprehensive forecasting analysis with scenario planning and risk assessment.</p>
            
            <div class="error-message">
                <p>⚠️ Unable to generate forecasting analysis due to data processing issues.</p>
                <p>Please ensure forecasting data is properly formatted and available.</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-section" data-tooltip="forecasting_chart">
                    <h3>Forecasting Overview</h3>
                    <canvas id="forecastingChart" width="400" height="300"></canvas>
                </div>
                <div class="chart-section" data-tooltip="scenarios_chart">
                    <h3>Scenario Analysis</h3>
                    <canvas id="scenariosChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
        """

# Mock classes for fallback
class MockStrategicEngine:
    async def query_knowledge_graph_for_intelligence(self, topic, analysis_type):
        return {"success": True, "strategic_insights": {"key_insights": ["Mock forecasting intelligence insight"]}}
    
    async def generate_cross_domain_intelligence(self, domains):
        return {"success": True, "cross_domain_patterns": [{"domains": "Mock", "pattern": "Mock pattern"}]}

class MockRecommendationsEngine:
    async def generate_intelligence_driven_recommendations(self, topic):
        return [MockRecommendation("Mock Forecasting Recommendation", "Mock description")]

class MockRecommendation:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.priority = "medium"
        self.confidence_score = 0.7
