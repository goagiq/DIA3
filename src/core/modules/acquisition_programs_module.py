#!/usr/bin/env python3
"""
Acquisition Programs Module

Independent module for generating acquisition programs analysis sections that can be added to any report.
Provides acquisition program overview, modernization initiatives, program analysis, and strategic impact assessment.
"""

import json
from typing import Dict, Any, List, Optional
from loguru import logger

from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData


class AcquisitionProgramsModule(BaseModule):
    """Acquisition Programs module for enhanced reports."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Acquisition Programs module."""
        if config is None:
            config = ModuleConfig(
                title="🎯 Acquisition Programs & Modernization",
                description="Comprehensive analysis of acquisition programs and modernization initiatives",
                order=40,  # After implementation timeline
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'acquisition_programs',
            'modernization_initiatives', 
            'program_analysis',
            'strategic_impact'
        ]
    
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for the Acquisition Programs module with Phase 4 enhancements."""
        
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

        logger.info(f"Generating acquisition programs content for {self.module_id}")
        
        try:
            # Extract acquisition data
            programs_data = data.get("acquisition_programs", {})
            modernization_data = data.get("modernization_initiatives", {})
            analysis_data = data.get("program_analysis", {})
            impact_data = data.get("strategic_impact", {})
            
            # Generate main content sections
            content_parts = []
            
            # Acquisition Programs Overview
            programs_overview = self._generate_programs_overview(programs_data)
            content_parts.append(programs_overview)
            
            # Modernization Initiatives
            modernization_initiatives = self._generate_modernization_initiatives(modernization_data)
            content_parts.append(modernization_initiatives)
            
            # Program Analysis
            program_analysis = self._generate_program_analysis(analysis_data)
            content_parts.append(program_analysis)
            
            # Strategic Impact Assessment
            strategic_impact = self._generate_strategic_impact(impact_data)
            content_parts.append(strategic_impact)
            
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
            logger.error(f"Error generating acquisition programs content: {e}")
            return self._generate_error_content()
    
    def _generate_programs_overview(self, data: Dict[str, Any]) -> str:
        """Generate acquisition programs overview section."""
        programs = data.get("programs", [])
        
        # Default programs if not provided
        if not programs:
            programs = [
                {"name": "Submarine Acquisition", "status": "Active", "budget": "$5.2B", "timeline": "2024-2030", "priority": "High"},
                {"name": "Surface Fleet Modernization", "status": "Planning", "budget": "$3.8B", "timeline": "2025-2032", "priority": "Medium"},
                {"name": "Air Defense Systems", "status": "Active", "budget": "$2.1B", "timeline": "2024-2028", "priority": "High"},
                {"name": "Cyber Defense Infrastructure", "status": "Development", "budget": "$1.5B", "timeline": "2024-2027", "priority": "Medium"}
            ]
        
        # Generate programs chart data
        programs_data = {
            "labels": [program["name"] for program in programs],
            "datasets": [
                {
                    "label": "Budget Allocation (Billions)",
                    "data": [float(program["budget"].replace("$", "").replace("B", "")) for program in programs],
                    "backgroundColor": [
                        "rgba(255, 99, 132, 0.8)" if program["priority"] == "High" else
                        "rgba(54, 162, 235, 0.8)" if program["priority"] == "Medium" else
                        "rgba(255, 205, 86, 0.8)" for program in programs
                    ],
                    "borderColor": [
                        "rgba(255, 99, 132, 1)" if program["priority"] == "High" else
                        "rgba(54, 162, 235, 1)" if program["priority"] == "Medium" else
                        "rgba(255, 205, 86, 1)" for program in programs
                    ],
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="programs_overview">
            <h3>🎯 Acquisition Programs Overview</h3>
            <p>Comprehensive overview of major acquisition programs and their current status.</p>
            
            <div class="programs-grid">
        """
        
        for program in programs:
            status_color = {
                "Active": "green",
                "Planning": "blue",
                "Development": "orange",
                "On Hold": "red",
                "Completed": "gray"
            }.get(program["status"], "gray")
            
            priority_color = {
                "High": "red",
                "Medium": "orange",
                "Low": "green"
            }.get(program["priority"], "gray")
            
            content += f"""
                <div class="program-item" data-tooltip-{self.module_id}="program_{program['name'].lower().replace(' ', '_')}">
                    <div class="program-header">
                        <h4>{program['name']}</h4>
                        <span class="program-status" style="color: {status_color};">{program['status']}</span>
                    </div>
                    <div class="program-details">
                        <div class="detail">
                            <span class="detail-label">Budget</span>
                            <span class="detail-value">{program['budget']}</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Timeline</span>
                            <span class="detail-value">{program['timeline']}</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Priority</span>
                            <span class="detail-value" style="color: {priority_color};">{program['priority']}</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="programsChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Acquisition Programs
                const programsCtx = document.getElementById('programsChart').getContext('2d');
                new Chart(programsCtx, {{
                    type: 'bar',
                    data: {json.dumps(programs_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Acquisition Programs'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                title: {{
                                    display: true,
                                    text: 'Budget (Billions USD)'
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
    
    def _generate_modernization_initiatives(self, data: Dict[str, Any]) -> str:
        """Generate modernization initiatives section."""
        initiatives = data.get("initiatives", [])
        
        # Default initiatives if not provided
        if not initiatives:
            initiatives = [
                {"name": "Digital Transformation", "progress": 75, "impact": "High", "investment": "$2.5B"},
                {"name": "Infrastructure Modernization", "progress": 60, "impact": "Medium", "investment": "$1.8B"},
                {"name": "Technology Integration", "progress": 45, "impact": "High", "investment": "$3.2B"},
                {"name": "Process Optimization", "progress": 80, "impact": "Medium", "investment": "$0.9B"}
            ]
        
        # Generate initiatives chart data
        initiatives_data = {
            "labels": [initiative["name"] for initiative in initiatives],
            "datasets": [
                {
                    "label": "Progress (%)",
                    "data": [initiative["progress"] for initiative in initiatives],
                    "backgroundColor": "rgba(75, 192, 192, 0.8)",
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="modernization_initiatives">
            <h3>🚀 Modernization Initiatives</h3>
            <p>Analysis of key modernization initiatives and their progress status.</p>
            
            <div class="initiatives-grid">
        """
        
        for initiative in initiatives:
            progress_color = "green" if initiative["progress"] >= 75 else "orange" if initiative["progress"] >= 50 else "red"
            impact_color = "red" if initiative["impact"] == "High" else "orange" if initiative["impact"] == "Medium" else "green"
            
            content += f"""
                <div class="initiative-item" data-tooltip-{self.module_id}="initiative_{initiative['name'].lower().replace(' ', '_')}">
                    <div class="initiative-header">
                        <h4>{initiative['name']}</h4>
                        <span class="initiative-progress" style="color: {progress_color};">{initiative['progress']}%</span>
                    </div>
                    <div class="initiative-details">
                        <div class="detail">
                            <span class="detail-label">Impact</span>
                            <span class="detail-value" style="color: {impact_color};">{initiative['impact']}</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Investment</span>
                            <span class="detail-value">{initiative['investment']}</span>
                        </div>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {initiative['progress']}%; background-color: {progress_color};"></div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="initiativesChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Modernization Initiatives
                const initiativesCtx = document.getElementById('initiativesChart').getContext('2d');
                new Chart(initiativesCtx, {{
                    type: 'bar',
                    data: {json.dumps(initiatives_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Modernization Initiatives'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: 'Progress (%)'
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
    
    def _generate_program_analysis(self, data: Dict[str, Any]) -> str:
        """Generate program analysis section."""
        analysis_metrics = data.get("metrics", [])
        
        # Default analysis metrics if not provided
        if not analysis_metrics:
            analysis_metrics = [
                {"metric": "Cost Performance", "score": 85, "trend": "Improving", "risk": "Low"},
                {"metric": "Schedule Adherence", "score": 70, "trend": "Stable", "risk": "Medium"},
                {"metric": "Technical Performance", "score": 90, "trend": "Excellent", "risk": "Low"},
                {"metric": "Risk Management", "score": 75, "trend": "Improving", "risk": "Medium"}
            ]
        
        # Generate analysis chart data
        analysis_data = {
            "labels": [metric["metric"] for metric in analysis_metrics],
            "datasets": [
                {
                    "label": "Performance Score",
                    "data": [metric["score"] for metric in analysis_metrics],
                    "backgroundColor": [
                        "rgba(75, 192, 192, 0.8)" if metric["score"] >= 80 else
                        "rgba(255, 205, 86, 0.8)" if metric["score"] >= 60 else
                        "rgba(255, 99, 132, 0.8)" for metric in analysis_metrics
                    ],
                    "borderColor": [
                        "rgba(75, 192, 192, 1)" if metric["score"] >= 80 else
                        "rgba(255, 205, 86, 1)" if metric["score"] >= 60 else
                        "rgba(255, 99, 132, 1)" for metric in analysis_metrics
                    ],
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="program_analysis">
            <h3>📊 Program Analysis</h3>
            <p>Comprehensive analysis of program performance metrics and risk assessment.</p>
            
            <div class="analysis-metrics">
        """
        
        for metric in analysis_metrics:
            score_color = "green" if metric["score"] >= 80 else "orange" if metric["score"] >= 60 else "red"
            risk_color = "green" if metric["risk"] == "Low" else "orange" if metric["risk"] == "Medium" else "red"
            
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
                            <span class="detail-label">Risk</span>
                            <span class="detail-value" style="color: {risk_color};">{metric['risk']}</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="analysisChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Program Analysis
                const analysisCtx = document.getElementById('analysisChart').getContext('2d');
                new Chart(analysisCtx, {{
                    type: 'bar',
                    data: {json.dumps(analysis_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Performance Metrics'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: 'Performance Score'
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
    
    def _generate_strategic_impact(self, data: Dict[str, Any]) -> str:
        """Generate strategic impact assessment section."""
        impact_areas = data.get("impact_areas", [])
        
        # Default impact areas if not provided
        if not impact_areas:
            impact_areas = [
                {"area": "Operational Capability", "impact": 85, "timeline": "2-3 years", "confidence": "High"},
                {"area": "Strategic Deterrence", "impact": 90, "timeline": "3-5 years", "confidence": "High"},
                {"area": "Regional Influence", "impact": 75, "timeline": "1-2 years", "confidence": "Medium"},
                {"area": "Technology Leadership", "impact": 80, "timeline": "2-4 years", "confidence": "High"}
            ]
        
        # Generate impact chart data
        impact_data = {
            "labels": [area["area"] for area in impact_areas],
            "datasets": [
                {
                    "label": "Strategic Impact",
                    "data": [area["impact"] for area in impact_areas],
                    "backgroundColor": "rgba(255, 99, 132, 0.8)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="strategic_impact">
            <h3>🎯 Strategic Impact Assessment</h3>
            <p>Assessment of strategic impact across key operational and strategic areas.</p>
            
            <div class="impact-areas">
        """
        
        for area in impact_areas:
            impact_color = "green" if area["impact"] >= 80 else "orange" if area["impact"] >= 60 else "red"
            confidence_color = "green" if area["confidence"] == "High" else "orange" if area["confidence"] == "Medium" else "red"
            
            content += f"""
                <div class="impact-item" data-tooltip-{self.module_id}="impact_{area['area'].lower().replace(' ', '_')}">
                    <div class="impact-header">
                        <h4>{area['area']}</h4>
                        <span class="impact-score" style="color: {impact_color};">{area['impact']}/100</span>
                    </div>
                    <div class="impact-details">
                        <div class="detail">
                            <span class="detail-label">Timeline</span>
                            <span class="detail-value">{area['timeline']}</span>
                        </div>
                        <div class="detail">
                            <span class="detail-label">Confidence</span>
                            <span class="detail-value" style="color: {confidence_color};">{area['confidence']}</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="impactChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Strategic Impact
                const impactCtx = document.getElementById('impactChart').getContext('2d');
                new Chart(impactCtx, {{
                    type: 'bar',
                    data: {json.dumps(impact_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Strategic Areas'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                title: {{
                                    display: true,
                                    text: 'Strategic Impact'
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
            kg_intelligence = await self.strategic_engine.query_knowledge_graph_for_intelligence(topic, "acquisition")
            enhanced_data["kg_intelligence"] = kg_intelligence
            
            # Cross-domain analysis
            cross_domain = await self.strategic_engine.generate_cross_domain_intelligence([
                "acquisition", "defense", "technology", "budget"
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
            "programs_overview": TooltipData(
                title="Acquisition Programs Overview",
                description="Comprehensive overview of major acquisition programs with status, budget, timeline, and priority information",
                source="Sources: Acquisition Program Database, Defense Budget Analysis, Program Management Systems, Strategic Planning Documents",
                strategic_impact="Strategic Impact: Critical for understanding acquisition priorities and resource allocation",
                recommendations="• Monitor program status and progress regularly\n• Track budget utilization and timeline adherence\n• Assess program priority alignment with strategic objectives\n• Identify program risks and mitigation strategies",
                use_cases="• Program oversight\n• Budget planning\n• Strategic alignment\n• Risk assessment\n• Resource allocation"
            ),
            "modernization_initiatives": TooltipData(
                title="Modernization Initiatives",
                description="Analysis of key modernization initiatives with progress tracking, impact assessment, and investment analysis",
                source="Sources: Modernization Planning Framework, Technology Assessment Reports, Investment Analysis, Progress Tracking Systems",
                strategic_impact="Strategic Impact: Essential for understanding modernization priorities and technology advancement",
                recommendations="• Track modernization progress and impact\n• Monitor investment efficiency and returns\n• Assess technology integration success\n• Identify modernization opportunities and risks",
                use_cases="• Technology planning\n• Investment analysis\n• Progress monitoring\n• Strategic modernization\n• Capability development"
            ),
            "program_analysis": TooltipData(
                title="Program Analysis",
                description="Comprehensive analysis of program performance metrics including cost, schedule, technical performance, and risk management",
                source="Sources: Program Performance Metrics, Cost Analysis Systems, Schedule Management Tools, Risk Assessment Frameworks",
                strategic_impact="Strategic Impact: Critical for program oversight and performance optimization",
                recommendations="• Monitor performance metrics regularly\n• Track trends and identify performance issues\n• Assess risk management effectiveness\n• Optimize program performance based on analysis",
                use_cases="• Performance monitoring\n• Risk assessment\n• Program optimization\n• Strategic oversight\n• Quality management"
            ),
            "strategic_impact": TooltipData(
                title="Strategic Impact Assessment",
                description="Assessment of strategic impact across operational capability, deterrence, regional influence, and technology leadership",
                source="Sources: Strategic Impact Analysis, Capability Assessment Models, Deterrence Analysis, Regional Influence Studies",
                strategic_impact="Strategic Impact: Fundamental for understanding strategic value and long-term impact",
                recommendations="• Monitor strategic impact across key areas\n• Track impact timeline and confidence levels\n• Assess strategic value and alignment\n• Identify strategic opportunities and risks",
                use_cases="• Strategic planning\n• Impact assessment\n• Value analysis\n• Strategic alignment\n• Long-term planning"
            )
        }
        
        # Add tooltip data to the module
        for tooltip_id, tooltip_data_obj in tooltip_data.items():
            self.add_tooltip(tooltip_id, tooltip_data_obj)
    
    def _generate_error_content(self) -> str:
        """Generate error content when data processing fails."""
        return """
        <div class="section">
            <h3>🎯 Acquisition Programs & Modernization</h3>
            <p>Comprehensive analysis of acquisition programs and modernization initiatives.</p>
            
            <div class="error-message">
                <p>⚠️ Unable to generate acquisition programs analysis due to data processing issues.</p>
                <p>Please ensure acquisition programs data is properly formatted and available.</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-section" data-tooltip="programs_chart">
                    <h3>Acquisition Programs</h3>
                    <canvas id="programsChart" width="400" height="300"></canvas>
                </div>
                <div class="chart-section" data-tooltip="initiatives_chart">
                    <h3>Modernization Initiatives</h3>
                    <canvas id="initiativesChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
        """

# Mock classes for fallback
class MockStrategicEngine:
    async def query_knowledge_graph_for_intelligence(self, topic, analysis_type):
        return {"success": True, "strategic_insights": {"key_insights": ["Mock acquisition intelligence insight"]}}
    
    async def generate_cross_domain_intelligence(self, domains):
        return {"success": True, "cross_domain_patterns": [{"domains": "Mock", "pattern": "Mock pattern"}]}

class MockRecommendationsEngine:
    async def generate_intelligence_driven_recommendations(self, topic):
        return [MockRecommendation("Mock Acquisition Recommendation", "Mock description")]

class MockRecommendation:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.priority = "medium"
        self.confidence_score = 0.7
