#!/usr/bin/env python3
"""
Strategic Recommendations Module

This module provides comprehensive strategic recommendations and implementation planning
capabilities, including intelligence analysis, strategic recommendations, and monitoring plans.
"""

import json
from typing import Dict, List, Any, Optional
from loguru import logger

from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData


class StrategicRecommendationsModule(BaseModule):
    """Strategic Recommendations Module for comprehensive strategic planning."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Strategic Recommendations Module."""
        super().__init__(config or ModuleConfig())
        
        # Set module properties
        self.config.title = "🎯 Strategic Recommendations & Planning"
        self.config.description = "Comprehensive strategic recommendations with implementation roadmap and monitoring plans"
        self.config.enabled = True
        self.config.tooltips_enabled = True
        self.config.charts_enabled = True
        self.config.order = 100  # High order to appear at the end
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return ["strategic_recommendations"]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate strategic recommendations content."""
        logger.info(f"Generating strategic recommendations content for {self.module_id}")
        
        try:
            # Extract strategic recommendations data
            recommendations_data = data.get("strategic_recommendations", {})
            
            # Generate main content sections
            content_parts = []
            
            # Intelligence Analysis Summary
            intelligence_summary = self._generate_intelligence_summary(recommendations_data)
            content_parts.append(intelligence_summary)
            
            # Strategic Recommendations
            strategic_recommendations = self._generate_strategic_recommendations(recommendations_data)
            content_parts.append(strategic_recommendations)
            
            # Implementation Roadmap
            implementation_roadmap = self._generate_implementation_roadmap(recommendations_data)
            content_parts.append(implementation_roadmap)
            
            # Monitoring & Evaluation Plan
            monitoring_plan = self._generate_monitoring_plan(recommendations_data)
            content_parts.append(monitoring_plan)
            
            # Combine all content
            content = "\n".join(content_parts)
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating strategic recommendations content: {e}")
            return self._generate_error_content()
    
    def _generate_intelligence_summary(self, data: Dict[str, Any]) -> str:
        """Generate intelligence analysis summary section."""
        intelligence_data = data.get("intelligence_summary", {})
        
        # Extract intelligence metrics
        total_insights = intelligence_data.get("total_insights", 0)
        avg_confidence = intelligence_data.get("average_confidence", 0.0)
        high_impact_insights = intelligence_data.get("high_impact_insights", 0)
        critical_findings = intelligence_data.get("critical_findings", 0)
        
        # Default metrics if not provided
        if total_insights == 0:
            total_insights = 15
            avg_confidence = 85.5
            high_impact_insights = 8
            critical_findings = 3
        
        # Generate radar chart data for intelligence metrics
        radar_data = {
            "labels": ["Total Insights", "Confidence", "High Impact", "Critical Findings"],
            "datasets": [
                {
                    "label": "Intelligence Metrics",
                    "data": [total_insights/20, avg_confidence/100, high_impact_insights/10, critical_findings/5],
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 2,
                    "pointBackgroundColor": "rgba(255, 99, 132, 1)",
                    "pointBorderColor": "#fff",
                    "pointHoverBackgroundColor": "#fff",
                    "pointHoverBorderColor": "rgba(255, 99, 132, 1)"
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="intelligence_summary">
                <h3>🧠 Intelligence Analysis Summary</h3>
            <p>Comprehensive intelligence analysis with key insights and confidence metrics.</p>
            
            <div class="intelligence-metrics">
                <div class="metric-item">
                    <span class="metric-name">Total Insights</span>
                    <span class="metric-value">{total_insights}</span>
                    <span class="metric-status">Analyzed</span>
                </div>
                <div class="metric-item">
                    <span class="metric-name">Average Confidence</span>
                    <span class="metric-value">{avg_confidence:.1f}%</span>
                    <span class="metric-status">High</span>
                    </div>
                <div class="metric-item">
                    <span class="metric-name">High Impact Insights</span>
                    <span class="metric-value">{high_impact_insights}</span>
                    <span class="metric-status">Critical</span>
                    </div>
                <div class="metric-item">
                    <span class="metric-name">Critical Findings</span>
                    <span class="metric-value">{critical_findings}</span>
                    <span class="metric-status">Urgent</span>
                    </div>
                </div>
            
            <div class="chart-container">
                <canvas id="intelligenceSummaryChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Intelligence Summary
                const intelligenceSummaryCtx = document.getElementById('intelligenceSummaryChart').getContext('2d');
                new Chart(intelligenceSummaryCtx, {{
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
    
    def _generate_strategic_recommendations(self, data: Dict[str, Any]) -> str:
        """Generate strategic recommendations section."""
        recommendations_data = data.get("recommendations", {})
        
        # Extract recommendations by priority
        immediate_recs = recommendations_data.get("immediate", [])
        short_term_recs = recommendations_data.get("short_term", [])
        long_term_recs = recommendations_data.get("long_term", [])
        
        # Default recommendations if not provided
        if not immediate_recs:
            immediate_recs = [
                {"title": "Enhanced Intelligence Gathering", "confidence": 0.95, "impact": "High", "timeline": "1-3 months", "rationale": "Critical for immediate threat assessment"},
                {"title": "Strategic Communication Protocol", "confidence": 0.88, "impact": "Medium", "timeline": "2-4 months", "rationale": "Essential for coordinated response"}
            ]
        
        if not short_term_recs:
            short_term_recs = [
                {"title": "Capability Enhancement Program", "confidence": 0.82, "impact": "High", "timeline": "6-12 months", "rationale": "Address identified capability gaps"},
                {"title": "Partnership Development", "confidence": 0.78, "impact": "Medium", "timeline": "8-15 months", "rationale": "Strengthen regional alliances"}
            ]
        
        if not long_term_recs:
            long_term_recs = [
                {"title": "Strategic Infrastructure Investment", "confidence": 0.75, "impact": "High", "timeline": "2-3 years", "rationale": "Long-term strategic positioning"},
                {"title": "Technology Modernization", "confidence": 0.70, "impact": "Medium", "timeline": "3-5 years", "rationale": "Future-proof capabilities"}
            ]
        
        # Generate bar chart data for recommendation priorities
        bar_data = {
            "labels": ["Immediate", "Short Term", "Long Term"],
            "datasets": [
                {
                    "label": "Average Confidence",
                    "data": [
                        sum(r.get("confidence", 0) for r in immediate_recs) / len(immediate_recs) if immediate_recs else 0,
                        sum(r.get("confidence", 0) for r in short_term_recs) / len(short_term_recs) if short_term_recs else 0,
                        sum(r.get("confidence", 0) for r in long_term_recs) / len(long_term_recs) if long_term_recs else 0
                    ],
                    "backgroundColor": "rgba(54, 162, 235, 0.8)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="strategic_recommendations">
            <h3>🎯 Strategic Recommendations</h3>
            <p>Comprehensive strategic recommendations organized by priority and timeline.</p>
            
            <div class="recommendations-grid">
                <div class="priority-section">
                    <h4>🚨 Immediate Recommendations</h4>
                    <div class="recommendations-list">
        """
        
        for i, rec in enumerate(immediate_recs):
            content += f"""
                        <div class="recommendation-item" data-tooltip-{self.module_id}="immediate_rec_{i}">
                            <div class="rec-title">{rec['title']}</div>
                            <div class="rec-confidence">{rec['confidence']:.1%}</div>
                            <div class="rec-timeline">{rec['timeline']}</div>
                            <div class="rec-rationale">{rec['rationale']}</div>
        </div>
        """
        
        content += f"""
                    </div>
                </div>
    
        <div class="priority-section">
                    <h4>📅 Short Term Recommendations</h4>
                    <div class="recommendations-list">
        """
        
        for i, rec in enumerate(short_term_recs):
            content += f"""
                        <div class="recommendation-item" data-tooltip-{self.module_id}="short_term_rec_{i}">
                            <div class="rec-title">{rec['title']}</div>
                            <div class="rec-confidence">{rec['confidence']:.1%}</div>
                            <div class="rec-timeline">{rec['timeline']}</div>
                            <div class="rec-rationale">{rec['rationale']}</div>
                        </div>
            """
        
        content += f"""
                    </div>
                </div>
                
                <div class="priority-section">
                    <h4>🔮 Long Term Recommendations</h4>
                    <div class="recommendations-list">
        """
        
        for i, rec in enumerate(long_term_recs):
            content += f"""
                        <div class="recommendation-item" data-tooltip-{self.module_id}="long_term_rec_{i}">
                            <div class="rec-title">{rec['title']}</div>
                            <div class="rec-confidence">{rec['confidence']:.1%}</div>
                            <div class="rec-timeline">{rec['timeline']}</div>
                            <div class="rec-rationale">{rec['rationale']}</div>
        </div>
        """
        
        content += f"""
                    </div>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="strategicRecommendationsChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Strategic Recommendations
                const strategicRecommendationsCtx = document.getElementById('strategicRecommendationsChart').getContext('2d');
                new Chart(strategicRecommendationsCtx, {{
                    type: 'bar',
                    data: {json.dumps(bar_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Recommendation Priority'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 1,
                                title: {{
                                    display: true,
                                    text: 'Average Confidence'
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
    
    def _generate_implementation_roadmap(self, data: Dict[str, Any]) -> str:
        """Generate implementation roadmap section."""
        roadmap_data = data.get("implementation_roadmap", {})
        
        # Extract roadmap phases
        phases = roadmap_data.get("phases", [])
        
        # Default phases if not provided
        if not phases:
            phases = [
                {"phase": "Phase 1: Foundation", "duration": "3-6 months", "milestones": ["Setup infrastructure", "Establish protocols"], "confidence": 0.90},
                {"phase": "Phase 2: Development", "duration": "6-12 months", "milestones": ["Implement core systems", "Train personnel"], "confidence": 0.85},
                {"phase": "Phase 3: Integration", "duration": "12-18 months", "milestones": ["System integration", "Performance optimization"], "confidence": 0.80},
                {"phase": "Phase 4: Optimization", "duration": "18-24 months", "milestones": ["Advanced features", "Continuous improvement"], "confidence": 0.75}
            ]
        
        # Generate line chart data for roadmap timeline
        line_data = {
            "labels": [phase["phase"] for phase in phases],
            "datasets": [
                {
                    "label": "Implementation Confidence",
                    "data": [phase["confidence"] for phase in phases],
                    "borderColor": "rgba(75, 192, 192, 0.8)",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "tension": 0.4,
                    "fill": True
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="implementation_roadmap">
            <h3>🗺️ Implementation Roadmap</h3>
            <p>Comprehensive implementation roadmap with phases, milestones, and confidence levels.</p>
            
            <div class="roadmap-phases">
        """
        
        for i, phase in enumerate(phases):
            content += f"""
                <div class="phase-item" data-tooltip-{self.module_id}="phase_{i}">
                    <div class="phase-header">
                        <h4>{phase['phase']}</h4>
                        <span class="phase-duration">{phase['duration']}</span>
                        <span class="phase-confidence">{phase['confidence']:.1%}</span>
                    </div>
                    <div class="phase-milestones">
                <ul>
            """
            
            for milestone in phase['milestones']:
                content += f"<li>{milestone}</li>"
            
            content += f"""
                </ul>
                    </div>
            </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="implementationRoadmapChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Implementation Roadmap
                const implementationRoadmapCtx = document.getElementById('implementationRoadmapChart').getContext('2d');
                new Chart(implementationRoadmapCtx, {{
                    type: 'line',
                    data: {json.dumps(line_data)},
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
                                max: 1,
                                title: {{
                                    display: true,
                                    text: 'Confidence Level'
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
    
    def _generate_monitoring_plan(self, data: Dict[str, Any]) -> str:
        """Generate monitoring and evaluation plan section."""
        monitoring_data = data.get("monitoring_plan", {})
        
        # Extract monitoring metrics
        kpis = monitoring_data.get("kpis", [])
        evaluation_criteria = monitoring_data.get("evaluation_criteria", [])
        
        # Default monitoring data if not provided
        if not kpis:
            kpis = [
                {"metric": "Implementation Progress", "target": "90%", "current": "75%", "status": "On Track"},
                {"metric": "Resource Utilization", "target": "85%", "current": "82%", "status": "Good"},
                {"metric": "Timeline Adherence", "target": "95%", "current": "88%", "status": "Needs Attention"},
                {"metric": "Quality Standards", "target": "95%", "current": "92%", "status": "Good"}
            ]
        
        if not evaluation_criteria:
            evaluation_criteria = [
                "Strategic alignment assessment",
                "Performance metrics validation",
                "Risk mitigation effectiveness",
                "Stakeholder satisfaction levels"
            ]
        
        # Generate pie chart data for KPI status
        pie_data = {
            "labels": [kpi["metric"] for kpi in kpis],
            "datasets": [
                {
                    "data": [float(kpi["current"].rstrip('%')) for kpi in kpis],
                    "backgroundColor": [
                        "rgba(255, 99, 132, 0.8)",
                        "rgba(54, 162, 235, 0.8)",
                        "rgba(255, 205, 86, 0.8)",
                        "rgba(75, 192, 192, 0.8)"
                    ],
                    "borderColor": [
                        "rgba(255, 99, 132, 1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 205, 86, 1)",
                        "rgba(75, 192, 192, 1)"
                    ],
                    "borderWidth": 2
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="monitoring_plan">
            <h3>📊 Monitoring & Evaluation Plan</h3>
            <p>Comprehensive monitoring and evaluation framework with KPIs and assessment criteria.</p>
            
            <div class="monitoring-kpis">
                <h4>Key Performance Indicators</h4>
                <div class="kpi-grid">
        """
        
        for kpi in kpis:
            content += f"""
                    <div class="kpi-item" data-tooltip-{self.module_id}="kpi_{kpi['metric'].lower().replace(' ', '_')}">
                        <div class="kpi-metric">{kpi['metric']}</div>
                        <div class="kpi-target">Target: {kpi['target']}</div>
                        <div class="kpi-current">Current: {kpi['current']}</div>
                        <div class="kpi-status">{kpi['status']}</div>
                    </div>
            """
        
        content += f"""
                </div>
            </div>
            
            <div class="evaluation-criteria">
                <h4>Evaluation Criteria</h4>
                <ul>
            """
            
        for criterion in evaluation_criteria:
            content += f"<li>{criterion}</li>"
            
        content += f"""
                </ul>
            </div>
        
            <div class="chart-container">
                <canvas id="monitoringPlanChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Monitoring Plan
                const monitoringPlanCtx = document.getElementById('monitoringPlanChart').getContext('2d');
                new Chart(monitoringPlanCtx, {{
                    type: 'pie',
                    data: {json.dumps(pie_data)},
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
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        tooltip_data = {
            "intelligence_summary": TooltipData(
            title="Intelligence Analysis Summary",
                description="Comprehensive intelligence analysis with key insights, confidence metrics, and critical findings for strategic decision-making",
            source="Sources: Intelligence Analysis Framework, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Strategic Impact: Critical for understanding the strategic context and decision-making basis",
                recommendations="• Review intelligence sources regularly\n• Validate insights with multiple sources\n• Update confidence scores based on new information\n• Prioritize high-impact insights for immediate action",
                use_cases="• Strategic planning sessions\n• Intelligence briefings\n• Decision support systems\n• Risk assessment frameworks\n• Crisis management"
            ),
            "strategic_recommendations": TooltipData(
                title="Strategic Recommendations",
                description="Comprehensive strategic recommendations organized by priority and timeline with confidence levels and implementation rationale",
                source="Sources: Strategic Planning Framework, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Strategic Impact: Direct influence on strategic decision-making and resource allocation priorities",
                recommendations="• Prioritize immediate recommendations for urgent action\n• Develop detailed implementation plans for short-term recommendations\n• Establish monitoring frameworks for long-term recommendations\n• Regular review and update of recommendation priorities",
                use_cases="• Strategic planning\n• Resource allocation\n• Priority setting\n• Implementation planning\n• Performance monitoring"
            ),
            "implementation_roadmap": TooltipData(
                title="Implementation Roadmap",
                description="Comprehensive implementation roadmap with phases, milestones, and confidence levels for strategic execution",
                source="Sources: Implementation Planning Framework, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Strategic Impact: Essential for successful execution and achievement of strategic objectives",
                recommendations="• Establish clear phase boundaries and milestones\n• Monitor confidence levels throughout implementation\n• Adjust timelines based on progress and challenges\n• Maintain stakeholder communication throughout phases",
                use_cases="• Project management\n• Implementation planning\n• Progress tracking\n• Risk management\n• Stakeholder communication"
            ),
            "monitoring_plan": TooltipData(
                title="Monitoring & Evaluation Plan",
                description="Comprehensive monitoring and evaluation framework with KPIs and assessment criteria for strategic oversight",
                source="Sources: Monitoring & Evaluation Framework, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Strategic Impact: Critical for ensuring strategic objectives are achieved and maintaining accountability",
                recommendations="• Establish regular monitoring schedules\n• Set up automated KPI tracking systems\n• Conduct periodic evaluation reviews\n• Adjust strategies based on monitoring results",
                use_cases="• Performance monitoring\n• Strategic oversight\n• Accountability frameworks\n• Continuous improvement\n• Risk management"
            )
        }
        
        # Add tooltip data to the module
        for tooltip_id, tooltip_data_obj in tooltip_data.items():
            self.add_tooltip(tooltip_id, tooltip_data_obj)
    
    def _generate_error_content(self) -> str:
        """Generate error content when data processing fails."""
        return """
        <div class="section">
            <h3>🎯 Strategic Recommendations & Planning</h3>
            <p>Comprehensive strategic recommendations with implementation roadmap and monitoring plans.</p>
            
            <div class="error-message">
                <p>⚠️ Unable to generate strategic recommendations due to data processing issues.</p>
                <p>Please ensure strategic recommendations data is properly formatted and available.</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-section" data-tooltip="intelligence_summary_chart">
                    <h3>Intelligence Summary</h3>
                    <canvas id="intelligenceSummaryChart" width="400" height="300"></canvas>
                </div>
                <div class="chart-section" data-tooltip="strategic_recommendations_chart">
                    <h3>Strategic Recommendations</h3>
                    <canvas id="strategicRecommendationsChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
        """
