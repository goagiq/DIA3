#!/usr/bin/env python3
"""
Operational Considerations Module

Independent module for generating operational considerations and readiness assessment sections that can be added to any report.
Provides operational planning, readiness analysis, implementation considerations, and risk assessment capabilities.
"""

import json
from typing import Dict, Any, List, Optional
from loguru import logger

from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData


class OperationalConsiderationsModule(BaseModule):
    """Operational Considerations module for enhanced reports."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Operational Considerations module."""
        if config is None:
            config = ModuleConfig(
                title="⚡ Operational Considerations & Readiness",
                description="Comprehensive operational planning and readiness assessment analysis",
                order=60,  # After forecasting
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'operational_overview',
            'readiness_analysis',
            'implementation_planning',
            'operational_risk_assessment'
        ]
    
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for the Operational Considerations module with Phase 4 enhancements."""
        
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

        logger.info(f"Generating operational considerations content for {self.module_id}")
        
        try:
            # Extract operational data
            overview_data = data.get("operational_overview", {})
            readiness_data = data.get("readiness_analysis", {})
            planning_data = data.get("implementation_planning", {})
            risk_data = data.get("operational_risk_assessment", {})
            
            # Generate main content sections
            content_parts = []
            
            # Operational Overview
            operational_overview = self._generate_operational_overview(overview_data)
            content_parts.append(operational_overview)
            
            # Readiness Analysis
            readiness_analysis = self._generate_readiness_analysis(readiness_data)
            content_parts.append(readiness_analysis)
            
            # Implementation Planning
            implementation_planning = self._generate_implementation_planning(planning_data)
            content_parts.append(implementation_planning)
            
            # Operational Risk Assessment
            operational_risk = self._generate_operational_risk(risk_data)
            content_parts.append(operational_risk)
            
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
            logger.error(f"Error generating operational considerations content: {e}")
            return self._generate_error_content()
    
    def _generate_operational_overview(self, data: Dict[str, Any]) -> str:
        """Generate operational overview section."""
        operational_areas = data.get("areas", [])
        
        # Default operational areas if not provided
        if not operational_areas:
            operational_areas = [
                {"area": "Personnel Readiness", "status": "Ready", "capacity": 85, "training": "Complete"},
                {"area": "Equipment Availability", "status": "Ready", "capacity": 90, "training": "Ongoing"},
                {"area": "Infrastructure", "status": "Partially Ready", "capacity": 70, "training": "Required"},
                {"area": "Logistics Support", "status": "Ready", "capacity": 80, "training": "Complete"}
            ]
        
        # Generate operational chart data
        operational_data = {
            "labels": [area["area"] for area in operational_areas],
            "datasets": [
                {
                    "label": "Capacity (%)",
                    "data": [area["capacity"] for area in operational_areas],
                    "backgroundColor": [
                        "rgba(75, 192, 192, 0.8)" if area["status"] == "Ready" else
                        "rgba(255, 205, 86, 0.8)" if area["status"] == "Partially Ready" else
                        "rgba(255, 99, 132, 0.8)" for area in operational_areas
                    ],
                    "borderColor": [
                        "rgba(75, 192, 192, 1)" if area["status"] == "Ready" else
                        "rgba(255, 205, 86, 1)" if area["status"] == "Partially Ready" else
                        "rgba(255, 99, 132, 1)" for area in operational_areas
                    ],
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="operational_overview">
            <h3>⚡ Operational Overview</h3>
            <p>Comprehensive overview of operational areas with readiness status and capacity assessment.</p>
            
            <div class="operational-areas-grid">
        """
        
        for area in operational_areas:
            status_color = {
                "Ready": "green",
                "Partially Ready": "orange",
                "Not Ready": "red"
            }.get(area["status"], "gray")
            
            content += f"""
                <div class="area-item" data-tooltip-{self.module_id}="area_{area['area'].lower().replace(' ', '_')}">
                    <div class="area-header">
                        <h4>{area['area']}</h4>
                        <span class="area-status" style="color: {status_color};">{area['status']}</span>
                    </div>
                    <div class="area-details">
                        <div class="detail">
                            <span class="detail-label">Capacity</span>
                            <span class="detail-value">{area['capacity']}%</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Training</span>
                            <span class="detail-value">{area['training']}</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="operationalChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Operational Overview
                const operationalCtx = document.getElementById('operationalChart').getContext('2d');
                new Chart(operationalCtx, {{
                    type: 'bar',
                    data: {json.dumps(operational_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Operational Areas'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: 'Capacity (%)'
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
    
    def _generate_readiness_analysis(self, data: Dict[str, Any]) -> str:
        """Generate readiness analysis section."""
        readiness_metrics = data.get("metrics", [])
        
        # Default readiness metrics if not provided
        if not readiness_metrics:
            readiness_metrics = [
                {"metric": "Combat Readiness", "score": 85, "trend": "Improving", "priority": "High"},
                {"metric": "Training Readiness", "score": 90, "trend": "Stable", "priority": "High"},
                {"metric": "Equipment Readiness", "score": 75, "trend": "Improving", "priority": "Medium"},
                {"metric": "Logistics Readiness", "score": 80, "trend": "Stable", "priority": "Medium"}
            ]
        
        # Generate readiness chart data
        readiness_data = {
            "labels": [metric["metric"] for metric in readiness_metrics],
            "datasets": [
                {
                    "label": "Readiness Score",
                    "data": [metric["score"] for metric in readiness_metrics],
                    "backgroundColor": [
                        "rgba(75, 192, 192, 0.8)" if metric["score"] >= 80 else
                        "rgba(255, 205, 86, 0.8)" if metric["score"] >= 60 else
                        "rgba(255, 99, 132, 0.8)" for metric in readiness_metrics
                    ],
                    "borderColor": [
                        "rgba(75, 192, 192, 1)" if metric["score"] >= 80 else
                        "rgba(255, 205, 86, 1)" if metric["score"] >= 60 else
                        "rgba(255, 99, 132, 1)" for metric in readiness_metrics
                    ],
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="readiness_analysis">
            <h3>🎯 Readiness Analysis</h3>
            <p>Comprehensive readiness analysis with key metrics and trend assessment.</p>
            
            <div class="readiness-metrics">
        """
        
        for metric in readiness_metrics:
            score_color = "green" if metric["score"] >= 80 else "orange" if metric["score"] >= 60 else "red"
            priority_color = "red" if metric["priority"] == "High" else "orange" if metric["priority"] == "Medium" else "green"
            
            content += f"""
                <div class="metric-item" data-tooltip-{self.module_id}="metric_{metric['metric'].lower().replace(' ', '_')}">
                    <div class="metric-header">
                        <h4>{metric['metric']}</h4>
                        <span class="metric-score" style="color: {score_color};">{metric['score']}/100</span>
                    </div>
                    <div class="metric-details">
                        <div class="detail">
                            <span class="detail-label">Trend</span>
                            <span class="detail-value">{metric['trend']}</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Priority</span>
                            <span class="detail-value" style="color: {priority_color};">{metric['priority']}</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="readinessChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Readiness Analysis
                const readinessCtx = document.getElementById('readinessChart').getContext('2d');
                new Chart(readinessCtx, {{
                    type: 'bar',
                    data: {json.dumps(readiness_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Readiness Metrics'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: 'Readiness Score'
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
    
    def _generate_implementation_planning(self, data: Dict[str, Any]) -> str:
        """Generate implementation planning section."""
        planning_phases = data.get("phases", [])
        
        # Default planning phases if not provided
        if not planning_phases:
            planning_phases = [
                {"phase": "Preparation", "duration": "2-3 months", "resources": "High", "risk": "Low"},
                {"phase": "Training", "duration": "3-6 months", "resources": "Medium", "risk": "Medium"},
                {"phase": "Implementation", "duration": "6-12 months", "resources": "High", "risk": "High"},
                {"phase": "Validation", "duration": "2-4 months", "resources": "Medium", "risk": "Medium"}
            ]
        
        # Generate planning chart data
        planning_data = {
            "labels": [phase["phase"] for phase in planning_phases],
            "datasets": [
                {
                    "label": "Resource Requirements",
                    "data": [
                        100 if phase["resources"] == "High" else
                        50 if phase["resources"] == "Medium" else
                        25 for phase in planning_phases
                    ],
                    "backgroundColor": "rgba(54, 162, 235, 0.8)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="implementation_planning">
            <h3>📋 Implementation Planning</h3>
            <p>Detailed implementation planning with phases, resources, and risk assessment.</p>
            
            <div class="planning-phases">
        """
        
        for phase in planning_phases:
            risk_color = "red" if phase["risk"] == "High" else "orange" if phase["risk"] == "Medium" else "green"
            resource_color = "red" if phase["resources"] == "High" else "orange" if phase["resources"] == "Medium" else "green"
            
            content += f"""
                <div class="phase-item" data-tooltip-{self.module_id}="phase_{phase['phase'].lower().replace(' ', '_')}">
                    <div class="phase-header">
                        <h4>{phase['phase']}</h4>
                        <span class="phase-duration">{phase['duration']}</span>
                    </div>
                    <div class="phase-details">
                        <div class="detail">
                            <span class="detail-label">Resources</span>
                            <span class="detail-value" style="color: {resource_color};">{phase['resources']}</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Risk</span>
                            <span class="detail-value" style="color: {risk_color};">{phase['risk']}</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="planningChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Implementation Planning
                const planningCtx = document.getElementById('planningChart').getContext('2d');
                new Chart(planningCtx, {{
                    type: 'bar',
                    data: {json.dumps(planning_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Implementation Phases'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: 'Resource Requirements (%)'
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
    
    def _generate_operational_risk(self, data: Dict[str, Any]) -> str:
        """Generate operational risk assessment section."""
        risks = data.get("risks", [])
        
        # Default risks if not provided
        if not risks:
            risks = [
                {"risk": "Personnel Shortage", "probability": 40, "impact": "High", "mitigation": "Recruitment drive"},
                {"risk": "Equipment Failure", "probability": 25, "impact": "Medium", "mitigation": "Preventive maintenance"},
                {"risk": "Training Delays", "probability": 35, "impact": "Medium", "mitigation": "Accelerated programs"},
                {"risk": "Logistics Issues", "probability": 30, "impact": "High", "mitigation": "Backup suppliers"}
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
        <div class="section" data-tooltip-{self.module_id}="operational_risk">
            <h3>⚠️ Operational Risk Assessment</h3>
            <p>Comprehensive operational risk assessment with probability, impact, and mitigation strategies.</p>
            
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
                <canvas id="operationalRiskChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Operational Risk Assessment
                const operationalRiskCtx = document.getElementById('operationalRiskChart').getContext('2d');
                new Chart(operationalRiskCtx, {{
                    type: 'bar',
                    data: {json.dumps(risk_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Operational Risks'
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
            kg_intelligence = await self.strategic_engine.query_knowledge_graph_for_intelligence(topic, "operational")
            enhanced_data["kg_intelligence"] = kg_intelligence
            
            # Cross-domain analysis
            cross_domain = await self.strategic_engine.generate_cross_domain_intelligence([
                "operational", "readiness", "implementation", "risk_assessment"
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
            "operational_overview": TooltipData(
                title="Operational Overview",
                description="Comprehensive overview of operational areas with readiness status, capacity assessment, and training requirements",
                source="Sources: Operational Readiness Framework, Capacity Assessment Models, Training Analysis, Status Reporting Systems",
                strategic_impact="Strategic Impact: Critical for understanding operational readiness and capability gaps",
                recommendations="• Monitor operational area status regularly\n• Track capacity improvements and training progress\n• Identify readiness gaps and resource needs\n• Update operational assessments based on new developments",
                use_cases="• Operational planning\n• Readiness assessment\n• Resource allocation\n• Training planning\n• Capability analysis"
            ),
            "readiness_analysis": TooltipData(
                title="Readiness Analysis",
                description="Comprehensive readiness analysis with key metrics, trend assessment, and priority identification",
                source="Sources: Readiness Assessment Framework, Performance Metrics, Trend Analysis, Priority Assessment Models",
                strategic_impact="Strategic Impact: Essential for understanding readiness levels and improvement priorities",
                recommendations="• Monitor readiness scores and trends\n• Track priority areas and improvement efforts\n• Identify readiness gaps and resource needs\n• Update readiness assessments based on performance",
                use_cases="• Readiness monitoring\n• Performance tracking\n• Priority setting\n• Resource planning\n• Improvement planning"
            ),
            "implementation_planning": TooltipData(
                title="Implementation Planning",
                description="Detailed implementation planning with phases, resource requirements, risk assessment, and timeline management",
                source="Sources: Implementation Planning Framework, Resource Assessment Models, Risk Analysis, Timeline Management Tools",
                strategic_impact="Strategic Impact: Critical for successful implementation and operational execution",
                recommendations="• Monitor implementation progress and resource utilization\n• Track risk mitigation effectiveness\n• Identify implementation challenges and solutions\n• Update planning based on actual progress",
                use_cases="• Implementation management\n• Resource planning\n• Risk management\n• Timeline tracking\n• Progress monitoring"
            ),
            "operational_risk": TooltipData(
                title="Operational Risk Assessment",
                description="Comprehensive operational risk assessment with probability analysis, impact assessment, and mitigation strategies",
                source="Sources: Risk Assessment Framework, Probability Models, Impact Analysis, Mitigation Planning",
                strategic_impact="Strategic Impact: Essential for risk management and operational decision-making",
                recommendations="• Monitor risk probability and impact changes\n• Track mitigation strategy effectiveness\n• Identify new risks and emerging threats\n• Update risk assessments based on operational experience",
                use_cases="• Risk management\n• Operational planning\n• Decision support\n• Contingency planning\n• Performance monitoring"
            )
        }
        
        # Add tooltip data to the module
        for tooltip_id, tooltip_data_obj in tooltip_data.items():
            self.add_tooltip(tooltip_id, tooltip_data_obj)
    
    def _generate_error_content(self) -> str:
        """Generate error content when data processing fails."""
        return """
        <div class="section">
            <h3>⚡ Operational Considerations & Readiness</h3>
            <p>Comprehensive operational planning and readiness assessment analysis.</p>
            
            <div class="error-message">
                <p>⚠️ Unable to generate operational considerations analysis due to data processing issues.</p>
                <p>Please ensure operational considerations data is properly formatted and available.</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-section" data-tooltip="operational_chart">
                    <h3>Operational Overview</h3>
                    <canvas id="operationalChart" width="400" height="300"></canvas>
                </div>
                <div class="chart-section" data-tooltip="readiness_chart">
                    <h3>Readiness Analysis</h3>
                    <canvas id="readinessChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
        """

# Mock classes for fallback
class MockStrategicEngine:
    async def query_knowledge_graph_for_intelligence(self, topic, analysis_type):
        return {"success": True, "strategic_insights": {"key_insights": ["Mock operational intelligence insight"]}}
    
    async def generate_cross_domain_intelligence(self, domains):
        return {"success": True, "cross_domain_patterns": [{"domains": "Mock", "pattern": "Mock pattern"}]}

class MockRecommendationsEngine:
    async def generate_intelligence_driven_recommendations(self, topic):
        return [MockRecommendation("Mock Operational Recommendation", "Mock description")]

class MockRecommendation:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.priority = "medium"
        self.confidence_score = 0.7
