#!/usr/bin/env python3
"""
Regional Security Module

This module provides comprehensive regional security dynamics analysis,
including security assessment, dynamics evolution, and strategic implications.
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger

from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData


class RegionalSecurityModule(BaseModule):
    """Regional Security Dynamics Analysis Module."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Regional Security Module."""
        super().__init__(config or ModuleConfig())
        
        # Set module properties
        self.config.title = "Regional Security Dynamics"
        self.config.description = "Comprehensive analysis of regional security dynamics and implications"
        
        # Set default configuration for regional security analysis
        self.config.enabled = True
        self.config.tooltips_enabled = True
        self.config.charts_enabled = True
        self.config.order = 14  # Regional Security is typically module 14
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return ["regional_security"]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate regional security analysis content."""
        logger.info(f"Generating regional security content for {self.module_id}")
        
        try:
            # Extract regional security data
            regional_data = data.get("regional_security", {})
            
            # Generate main content sections
            content_parts = []
            
            # Regional Security Assessment
            security_assessment = self._generate_security_assessment(regional_data)
            content_parts.append(security_assessment)
            
            # Security Dynamics Evolution
            dynamics_evolution = self._generate_dynamics_evolution(regional_data)
            content_parts.append(dynamics_evolution)
            
            # Regional Analysis
            regional_analysis = self._generate_regional_analysis(regional_data)
            content_parts.append(regional_analysis)
            
            # Security Implications
            security_implications = self._generate_security_implications(regional_data)
            content_parts.append(security_implications)
            
            # Combine all content
            content = "\n".join(content_parts)
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating regional security content: {e}")
            return self._generate_error_content()
    
    def _generate_security_assessment(self, data: Dict[str, Any]) -> str:
        """Generate regional security assessment section."""
        assessment_data = data.get("security_assessment", {})
        
        # Extract key metrics
        threat_level = assessment_data.get("threat_level", "Moderate")
        stability_index = assessment_data.get("stability_index", 0.65)
        conflict_probability = assessment_data.get("conflict_probability", 0.25)
        regional_tensions = assessment_data.get("regional_tensions", "Medium")
        
        # Generate radar chart data
        radar_data = {
            "labels": ["Threat Level", "Stability", "Tensions", "Cooperation", "Deterrence"],
            "datasets": [{
                "label": "Current State",
                "data": [
                    self._normalize_threat_level(threat_level),
                    stability_index,
                    self._normalize_tensions(regional_tensions),
                    assessment_data.get("cooperation_level", 0.6),
                    assessment_data.get("deterrence_effectiveness", 0.7)
                ],
                "backgroundColor": "rgba(54, 162, 235, 0.2)",
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 2
            }]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="regional_security_assessment">
            <h3>🛡️ Regional Security Assessment</h3>
            <p>Comprehensive assessment of regional security dynamics and current threat environment.</p>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{threat_level}</div>
                    <div class="metric-label">Threat Level</div>
                    <div class="metric-description">Current regional threat assessment</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{stability_index:.1%}</div>
                    <div class="metric-label">Stability Index</div>
                    <div class="metric-description">Regional stability measurement</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{conflict_probability:.1%}</div>
                    <div class="metric-label">Conflict Probability</div>
                    <div class="metric-description">Probability of regional conflict</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{regional_tensions}</div>
                    <div class="metric-label">Regional Tensions</div>
                    <div class="metric-description">Current tension levels</div>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="regionalSecurityAssessmentChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                const regionalSecurityAssessmentCtx = document.getElementById('regionalSecurityAssessmentChart').getContext('2d');
                new Chart(regionalSecurityAssessmentCtx, {{
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
                                position: 'top'
                            }}
                        }}
                    }}
                }});
            </script>
        </div>
        """
        
        return content
    
    def _generate_dynamics_evolution(self, data: Dict[str, Any]) -> str:
        """Generate security dynamics evolution section."""
        dynamics_data = data.get("dynamics_evolution", {})
        
        # Extract timeline data
        timeline_data = dynamics_data.get("timeline", [])
        evolution_metrics = dynamics_data.get("evolution_metrics", {})
        
        # Generate line chart data
        line_data = {
            "labels": [item.get("period", f"Period {i+1}") for i, item in enumerate(timeline_data)],
            "datasets": [
                {
                    "label": "Security Stability",
                    "data": [item.get("stability", 0.6) for item in timeline_data],
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "tension": 0.4
                },
                {
                    "label": "Threat Level",
                    "data": [item.get("threat_level", 0.4) for item in timeline_data],
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "tension": 0.4
                },
                {
                    "label": "Cooperation Level",
                    "data": [item.get("cooperation", 0.5) for item in timeline_data],
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "tension": 0.4
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="security_dynamics_evolution">
            <h3>📈 Security Dynamics Evolution</h3>
            <p>Analysis of how regional security dynamics have evolved over time and projected trends.</p>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{evolution_metrics.get('trend_direction', 'Stable')}</div>
                    <div class="metric-label">Trend Direction</div>
                    <div class="metric-description">Overall security trend</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{evolution_metrics.get('change_rate', '0.05')}</div>
                    <div class="metric-label">Change Rate</div>
                    <div class="metric-description">Rate of security change</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{evolution_metrics.get('volatility', 'Medium')}</div>
                    <div class="metric-label">Volatility</div>
                    <div class="metric-description">Security volatility level</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{evolution_metrics.get('predictability', '0.7')}</div>
                    <div class="metric-label">Predictability</div>
                    <div class="metric-description">Trend predictability</div>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="securityDynamicsEvolutionChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                const securityDynamicsEvolutionCtx = document.getElementById('securityDynamicsEvolutionChart').getContext('2d');
                new Chart(securityDynamicsEvolutionCtx, {{
                    type: 'line',
                    data: {json.dumps(line_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
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
                                position: 'top'
                            }}
                        }}
                    }}
                }});
            </script>
        </div>
        """
        
        return content
    
    def _generate_regional_analysis(self, data: Dict[str, Any]) -> str:
        """Generate regional analysis section."""
        regional_data = data.get("regional_analysis", {})
        
        # Extract regional factors
        key_actors = regional_data.get("key_actors", [])
        power_balance = regional_data.get("power_balance", {})
        conflict_zones = regional_data.get("conflict_zones", [])
        
        # Generate bar chart data for power balance
        power_data = {
            "labels": list(power_balance.keys()),
            "datasets": [{
                "label": "Power Index",
                "data": list(power_balance.values()),
                "backgroundColor": [
                    "rgba(255, 99, 132, 0.8)",
                    "rgba(54, 162, 235, 0.8)",
                    "rgba(255, 205, 86, 0.8)",
                    "rgba(75, 192, 192, 0.8)",
                    "rgba(153, 102, 255, 0.8)"
                ],
                "borderColor": [
                    "rgba(255, 99, 132, 1)",
                    "rgba(54, 162, 235, 1)",
                    "rgba(255, 205, 86, 1)",
                    "rgba(75, 192, 192, 1)",
                    "rgba(153, 102, 255, 1)"
                ],
                "borderWidth": 1
            }]
        }
        
        # Generate key actors list
        actors_html = ""
        for actor in key_actors:
            actors_html += f"""
            <div class="actor-item">
                <strong>{actor.get('name', 'Unknown')}</strong>
                <span class="actor-role">{actor.get('role', 'Regional Actor')}</span>
                <span class="actor-influence">{actor.get('influence', 'Medium')}</span>
            </div>
            """
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="regional_analysis">
            <h3>🌍 Regional Analysis</h3>
            <p>Comprehensive analysis of regional actors, power dynamics, and conflict zones.</p>
            
            <div class="analysis-grid">
                <div class="analysis-column">
                    <h4>Key Regional Actors</h4>
                    <div class="actors-list">
                        {actors_html}
                    </div>
                </div>
                
                <div class="analysis-column">
                    <h4>Power Balance</h4>
                    <div class="chart-container">
                        <canvas id="regionalPowerBalanceChart" width="300" height="200"></canvas>
                    </div>
                </div>
            </div>
            
            <div class="conflict-zones">
                <h4>Conflict Zones</h4>
                <div class="zones-grid">
        """
        
        for zone in conflict_zones:
            content += f"""
                    <div class="zone-card">
                        <div class="zone-name">{zone.get('name', 'Unknown Zone')}</div>
                        <div class="zone-risk">{zone.get('risk_level', 'Medium')}</div>
                        <div class="zone-description">{zone.get('description', 'No description available')}</div>
                    </div>
            """
        
        content += f"""
                </div>
            </div>
            
            <script>
                const regionalPowerBalanceCtx = document.getElementById('regionalPowerBalanceChart').getContext('2d');
                new Chart(regionalPowerBalanceCtx, {{
                    type: 'bar',
                    data: {json.dumps(power_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                max: 1,
                                ticks: {{
                                    stepSize: 0.2
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: false
                            }}
                        }}
                    }}
                }});
            </script>
        </div>
        """
        
        return content
    
    def _generate_security_implications(self, data: Dict[str, Any]) -> str:
        """Generate security implications section."""
        implications_data = data.get("security_implications", {})
        
        # Extract implications
        strategic_implications = implications_data.get("strategic_implications", [])
        operational_implications = implications_data.get("operational_implications", [])
        policy_recommendations = implications_data.get("policy_recommendations", [])
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="security_implications">
            <h3>🎯 Security Implications</h3>
            <p>Strategic and operational implications of current regional security dynamics.</p>
            
            <div class="implications-grid">
                <div class="implication-column">
                    <h4>Strategic Implications</h4>
                    <ul class="implications-list">
        """
        
        for implication in strategic_implications:
            content += f"""
                        <li data-tooltip="strategic_implication">
                            <strong>{implication.get('title', 'Strategic Implication')}</strong>
                            <p>{implication.get('description', 'No description available')}</p>
                            <span class="impact-level">{implication.get('impact', 'Medium')}</span>
                        </li>
            """
        
        content += f"""
                    </ul>
                </div>
                
                <div class="implication-column">
                    <h4>Operational Implications</h4>
                    <ul class="implications-list">
        """
        
        for implication in operational_implications:
            content += f"""
                        <li data-tooltip="operational_implication">
                            <strong>{implication.get('title', 'Operational Implication')}</strong>
                            <p>{implication.get('description', 'No description available')}</p>
                            <span class="impact-level">{implication.get('impact', 'Medium')}</span>
                        </li>
            """
        
        content += f"""
                    </ul>
                </div>
            </div>
            
            <div class="policy-recommendations">
                <h4>Policy Recommendations</h4>
                <div class="recommendations-grid">
        """
        
        for recommendation in policy_recommendations:
            content += f"""
                    <div class="recommendation-card" data-tooltip="policy_recommendation">
                        <div class="recommendation-title">{recommendation.get('title', 'Policy Recommendation')}</div>
                        <div class="recommendation-description">{recommendation.get('description', 'No description available')}</div>
                        <div class="recommendation-priority">{recommendation.get('priority', 'Medium')}</div>
                        <div class="recommendation-timeline">{recommendation.get('timeline', 'Short-term')}</div>
                    </div>
            """
        
        content += """
                </div>
            </div>
        </div>
        """
        
        return content
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        tooltip_data = {
            "regional_security_assessment": TooltipData(
                title="Regional Security Assessment",
                description="Comprehensive assessment of regional security dynamics and current threat environment",
                source="Source: Regional Security Analysis Framework",
                strategic_impact="Strategic Impact: Critical for understanding regional context and threat assessment",
                recommendations="Recommendations: Regular monitoring and assessment updates required",
                use_cases="Use Cases: Strategic planning, threat assessment, regional analysis"
            ),
            "security_dynamics_evolution": TooltipData(
                title="Security Dynamics Evolution",
                description="Analysis of how regional security dynamics have evolved over time and projected trends",
                source="Source: Historical Security Analysis",
                strategic_impact="Strategic Impact: Essential for trend analysis and future planning",
                recommendations="Recommendations: Continuous monitoring and trend analysis",
                use_cases="Use Cases: Trend analysis, forecasting, strategic planning"
            ),
            "regional_analysis": TooltipData(
                title="Regional Analysis",
                description="Comprehensive analysis of regional actors, power dynamics, and conflict zones",
                source="Source: Regional Intelligence Analysis",
                strategic_impact="Strategic Impact: Critical for understanding regional power dynamics",
                recommendations="Recommendations: Regular actor analysis and power balance assessment",
                use_cases="Use Cases: Regional analysis, actor assessment, power dynamics"
            ),
            "security_implications": TooltipData(
                title="Security Implications",
                description="Strategic and operational implications of current regional security dynamics",
                source="Source: Strategic Analysis Framework",
                strategic_impact="Strategic Impact: Essential for strategic and operational planning",
                recommendations="Recommendations: Regular implications assessment and policy review",
                use_cases="Use Cases: Strategic planning, operational planning, policy development"
            )
        }
        
        # Add tooltip data to the module
        for tooltip_id, tooltip_data_obj in tooltip_data.items():
            self.add_tooltip(tooltip_id, tooltip_data_obj)
    
    def _normalize_threat_level(self, threat_level: str) -> float:
        """Normalize threat level string to float value."""
        threat_mapping = {
            "Low": 0.2,
            "Low-Moderate": 0.35,
            "Moderate": 0.5,
            "Moderate-High": 0.65,
            "High": 0.8,
            "Very High": 0.9,
            "Critical": 1.0
        }
        return threat_mapping.get(threat_level, 0.5)
    
    def _normalize_tensions(self, tensions: str) -> float:
        """Normalize tension level string to float value."""
        tension_mapping = {
            "Low": 0.2,
            "Medium": 0.5,
            "High": 0.8,
            "Very High": 0.9
        }
        return tension_mapping.get(tensions, 0.5)
    
    def _generate_error_content(self) -> str:
        """Generate error content when data processing fails."""
        return """
        <div class="section">
            <h3>🛡️ Regional Security Dynamics</h3>
            <p>Analysis of regional security dynamics and strategic implications.</p>
            
            <div class="error-message">
                <p>⚠️ Unable to generate regional security analysis due to data processing issues.</p>
                <p>Please ensure regional security data is properly formatted and available.</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-section" data-tooltip="regional_security_chart">
                    <h3>Regional Security Assessment</h3>
                    <canvas id="regionalSecurityChart" width="400" height="300"></canvas>
                </div>
                <div class="chart-section" data-tooltip="security_dynamics_chart">
                    <h3>Security Dynamics Evolution</h3>
                    <canvas id="securityDynamicsChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
        """
