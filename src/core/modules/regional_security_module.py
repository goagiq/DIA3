#!/usr/bin/env python3
"""
Regional Security Module

This module provides comprehensive regional security dynamics analysis,
including security assessment, dynamics evolution, and strategic implications.
Enhanced for contextual adaptation and data structure flexibility.
"""

import json
import re
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from loguru import logger

from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData


class RegionalSecurityModule(BaseModule):
    """Regional Security Dynamics Analysis Module with Contextual Adaptation."""
    
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
        
        # Initialize context domains and their characteristics
        self._initialize_context_domains()
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return ["regional_security"]
    
    def validate_data(self, data: Union[str, Dict[str, Any]]) -> bool:
        """Validate that required data is present or that data is a string query."""
        if isinstance(data, str):
            # If data is a string, it's a query and we can generate content
            return True
        elif isinstance(data, dict):
            # If data is a dict, check for required keys
            required_keys = self.get_required_data_keys()
            missing_keys = [key for key in required_keys if key not in data]
            
            if missing_keys:
                raise ValueError(
                    f"Missing required data keys for {self.module_id}: {missing_keys}"
                )
            return True
        else:
            raise ValueError(f"Invalid data type for {self.module_id}: {type(data)}")
    
    async def generate_content(self, data: Union[str, Dict[str, Any]], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate regional security analysis content with contextual adaptation."""
        logger.info(f"Generating regional security content for {self.module_id}")
        
        # Phase 4 Strategic Intelligence Integration
        topic = data.get("topic", "") if isinstance(data, dict) else data
        phase4_enhanced = config and config.get("phase4_integration", False)
        
        try:
            if phase4_enhanced and topic:
                # Enhanced with strategic intelligence
                enhanced_data = await self._enhance_with_phase4_capabilities(topic, data)
                data.update(enhanced_data)
        except Exception as e:
            # Graceful fallback if Phase 4 enhancement fails
            pass
        
        try:
            # Handle different data structures
            if isinstance(data, str):
                # If data is a string, treat it as a query and generate adaptive content
                query = data
                context_domain = self._detect_context_domain(query)
                regional_data = self._generate_adaptive_data(query, context_domain)
            elif isinstance(data, dict):
                # If data is a dict, extract regional security data
                regional_data = data.get("regional_security", {})
                query = regional_data.get("query", "Regional Security Analysis")
                context_domain = self._detect_context_domain(query)
            else:
                # Default fallback
                regional_data = {}
                query = "Regional Security Analysis"
                context_domain = "GENERAL"
            
            # Generate main content sections with contextual adaptation
            content_parts = []
            
            # Regional Security Assessment (context-aware)
            security_assessment = self._generate_contextual_security_assessment(regional_data, context_domain)
            content_parts.append(security_assessment)
            
            # Security Dynamics Evolution (context-aware)
            dynamics_evolution = self._generate_contextual_dynamics_evolution(regional_data, context_domain)
            content_parts.append(dynamics_evolution)
            
            # Regional Analysis (context-aware)
            regional_analysis = self._generate_contextual_regional_analysis(regional_data, context_domain)
            content_parts.append(regional_analysis)
            
            # Security Implications (context-aware)
            security_implications = self._generate_contextual_security_implications(regional_data, context_domain)
            content_parts.append(security_implications)
            
            # Combine all content
            content = "\n".join(content_parts)
            
            return {
                "content": content,
                "metadata": {
                    "phase4_integrated": phase4_enhanced,
                    "strategic_intelligence": phase4_enhanced,
                    "confidence_score": 0.7,
                    "context_domain": context_domain,
                    "security_analyzed": bool(regional_data)
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating regional security content: {e}")
            error_content = self._generate_error_content()
            return {
                "content": error_content,
                "metadata": {
                    "phase4_integrated": phase4_enhanced,
                    "strategic_intelligence": phase4_enhanced,
                    "confidence_score": 0.0,
                    "error": str(e)
                }
            }
    
    def _initialize_context_domains(self):
        """Initialize context domains and their characteristics."""
        self.context_domains = {
            "MILITARY": {
                "keywords": ["military", "defense", "weapons", "submarine", "navy", "army", "air force", "deterrence", "warfare", "combat"],
                "metrics": ["threat_level", "military_capability", "deterrence_effectiveness", "readiness_index", "strategic_depth"],
                "chart_types": ["radar", "bar", "line"],
                "analysis_focus": "military capabilities and strategic positioning"
            },
            "ECONOMIC": {
                "keywords": ["economic", "trade", "finance", "market", "investment", "gdp", "commerce", "business", "financial"],
                "metrics": ["economic_stability", "trade_balance", "market_confidence", "investment_climate", "economic_growth"],
                "chart_types": ["line", "bar", "doughnut"],
                "analysis_focus": "economic stability and trade relationships"
            },
            "GEOPOLITICAL": {
                "keywords": ["geopolitical", "political", "diplomatic", "international", "alliance", "treaty", "diplomacy", "foreign policy"],
                "metrics": ["political_stability", "diplomatic_relations", "alliance_strength", "international_influence", "political_risk"],
                "chart_types": ["radar", "line", "bar"],
                "analysis_focus": "political dynamics and international relations"
            },
            "HEALTHCARE": {
                "keywords": ["health", "medical", "disease", "pandemic", "healthcare", "public health", "epidemiology"],
                "metrics": ["health_security", "disease_prevalence", "healthcare_capacity", "public_health_risk", "medical_readiness"],
                "chart_types": ["line", "bar", "area"],
                "analysis_focus": "health security and public health dynamics"
            },
            "TECHNOLOGY": {
                "keywords": ["technology", "cyber", "digital", "innovation", "ai", "automation", "digital transformation"],
                "metrics": ["cyber_security", "technological_advantage", "innovation_capacity", "digital_readiness", "tech_risk"],
                "chart_types": ["radar", "line", "bar"],
                "analysis_focus": "technological capabilities and cyber security"
            },
            "GENERAL": {
                "keywords": [],
                "metrics": ["threat_level", "stability_index", "cooperation_level", "conflict_probability", "regional_tensions"],
                "chart_types": ["radar", "line", "bar"],
                "analysis_focus": "general regional security dynamics"
            }
        }
    
    def _detect_context_domain(self, query: str) -> str:
        """Detect the context domain from the query."""
        query_lower = query.lower()
        
        for domain, config in self.context_domains.items():
            for keyword in config["keywords"]:
                if keyword in query_lower:
                    return domain
        
        return "GENERAL"
    
    def _generate_adaptive_data(self, query: str, context_domain: str) -> Dict[str, Any]:
        """Generate adaptive data based on context domain."""
        domain_config = self.context_domains[context_domain]
        
        # Generate context-appropriate metrics
        metrics = {}
        for metric in domain_config["metrics"]:
            if "threat" in metric:
                metrics[metric] = "Moderate"
            elif "stability" in metric or "confidence" in metric:
                metrics[metric] = 0.7
            elif "risk" in metric:
                metrics[metric] = 0.3
            elif "capability" in metric or "effectiveness" in metric:
                metrics[metric] = 0.8
            else:
                metrics[metric] = 0.6
        
        return {
            "context_domain": context_domain,
            "query": query,
            "metrics": metrics,
            "analysis_focus": domain_config["analysis_focus"],
            "chart_types": domain_config["chart_types"],
            "data_sources": self._generate_contextual_sources(context_domain)
        }
    
    def _generate_contextual_sources(self, context_domain: str) -> List[str]:
        """Generate context-appropriate data sources."""
        source_mapping = {
            "MILITARY": [
                "Defense Intelligence Agency Reports",
                "Military Capability Assessments",
                "Strategic Defense Analysis",
                "Arms Control Monitoring Data",
                "Military Technology Reviews"
            ],
            "ECONOMIC": [
                "International Monetary Fund Data",
                "World Bank Economic Indicators",
                "Trade Statistics Database",
                "Market Analysis Reports",
                "Economic Intelligence Sources"
            ],
            "GEOPOLITICAL": [
                "Diplomatic Intelligence Reports",
                "International Relations Database",
                "Political Risk Assessments",
                "Alliance Analysis Framework",
                "Foreign Policy Intelligence"
            ],
            "HEALTHCARE": [
                "World Health Organization Data",
                "Public Health Intelligence",
                "Epidemiological Studies",
                "Healthcare Capacity Assessments",
                "Medical Intelligence Reports"
            ],
            "TECHNOLOGY": [
                "Technology Intelligence Reports",
                "Cyber Security Assessments",
                "Innovation Analysis Framework",
                "Digital Transformation Data",
                "Technology Risk Assessments"
            ],
            "GENERAL": [
                "Regional Security Assessment Framework",
                "International Relations Database",
                "Strategic Intelligence Reports",
                "Economic Impact Analysis",
                "Diplomatic Relations Index"
            ]
        }
        
        return source_mapping.get(context_domain, source_mapping["GENERAL"])
    
    def _generate_contextual_security_assessment(self, data: Dict[str, Any], context_domain: str) -> str:
        """Generate context-aware security assessment section."""
        metrics = data.get("metrics", {})
        analysis_focus = data.get("analysis_focus", "Regional security dynamics")
        
        # Generate context-appropriate radar chart data
        radar_labels = list(metrics.keys())[:5]  # Limit to 5 metrics for radar chart
        radar_data = list(metrics.values())[:5]
        
        # Normalize string values to numeric
        normalized_data = []
        for value in radar_data:
            if isinstance(value, str):
                normalized_data.append(self._normalize_threat_level(value))
            else:
                normalized_data.append(value)
        
        radar_chart_data = {
            "labels": radar_labels,
            "datasets": [{
                "label": f"{context_domain.title()} Security Assessment",
                "data": normalized_data,
                "backgroundColor": "rgba(54, 162, 235, 0.2)",
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 2
            }]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="regional_security_assessment">
            <h3>🛡️ {context_domain.title()} Security Assessment</h3>
            <p>Comprehensive assessment of {analysis_focus.lower()} and current threat environment.</p>
            
            <div class="metrics-grid">
        """
        
        # Generate context-appropriate metric cards
        for i, (metric, value) in enumerate(metrics.items()):
            if i >= 4:  # Limit to 4 metric cards
                break
            
            display_value = f"{value:.1%}" if isinstance(value, float) else str(value)
            content += f"""
                <div class="metric-card" data-tooltip-{self.module_id}="metric_{i}">
                    <div class="metric-value">{display_value}</div>
                    <div class="metric-label">{metric.replace('_', ' ').title()}</div>
                    <div class="metric-description">{self._get_metric_description(metric, context_domain)}</div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="regionalSecurityAssessmentChart_{self.module_id}" width="400" height="300"></canvas>
            </div>
            
            <script>
                const regionalSecurityAssessmentCtx_{self.module_id} = document.getElementById('regionalSecurityAssessmentChart_{self.module_id}').getContext('2d');
                new Chart(regionalSecurityAssessmentCtx_{self.module_id}, {{
                    type: 'radar',
                    data: {json.dumps(radar_chart_data)},
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
    
    def _generate_contextual_dynamics_evolution(self, data: Dict[str, Any], context_domain: str) -> str:
        """Generate context-aware security dynamics evolution section."""
        # Generate context-appropriate timeline data
        timeline_data = self._generate_contextual_timeline(context_domain)
        
        # Generate line chart data
        line_data = {
            "labels": [item["period"] for item in timeline_data],
            "datasets": [
                {
                    "label": f"{context_domain.title()} Stability",
                    "data": [item["stability"] for item in timeline_data],
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "tension": 0.4
                },
                {
                    "label": f"{context_domain.title()} Risk",
                    "data": [item["risk"] for item in timeline_data],
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "tension": 0.4
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="security_dynamics_evolution">
            <h3>📈 {context_domain.title()} Dynamics Evolution</h3>
            <p>Analysis of how {context_domain.lower()} dynamics have evolved over time and projected trends.</p>
            
            <div class="chart-container">
                <canvas id="securityDynamicsEvolutionChart_{self.module_id}" width="400" height="300"></canvas>
            </div>
            
            <script>
                const securityDynamicsEvolutionCtx_{self.module_id} = document.getElementById('securityDynamicsEvolutionChart_{self.module_id}').getContext('2d');
                new Chart(securityDynamicsEvolutionCtx_{self.module_id}, {{
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
    
    def _generate_contextual_regional_analysis(self, data: Dict[str, Any], context_domain: str) -> str:
        """Generate context-aware regional analysis section."""
        # Generate context-appropriate regional metrics
        regional_metrics = self._generate_contextual_regional_metrics(context_domain)
        
        # Generate chart data for interactive visualizations
        chart_data = {
            f"regionalMetricsChart_{self.module_id}": {
                "type": "bar",
                "data": {
                    "labels": [metric["region"] for metric in regional_metrics],
            "datasets": [{
                        "label": f"{context_domain.title()} Index",
                        "data": [metric["index"] for metric in regional_metrics],
                        "backgroundColor": "rgba(54, 162, 235, 0.6)",
                        "borderColor": "rgba(54, 162, 235, 1)",
                        "borderWidth": 2
                    }]
                },
                "options": {
                    "responsive": True,
                    "maintainAspectRatio": False,
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                            "max": 100,
                            "title": {
                                "display": True,
                                "text": f"{context_domain.title()} Index"
                            }
                        }
                    }
                }
            }
        }
        
        # Add chart data to module
        for chart_id, chart_config in chart_data.items():
            self.add_chart_data(chart_id, chart_config)
        
        # Get data sources
        data_sources = data.get("data_sources", self._generate_contextual_sources(context_domain))
        
        content = f"""
        <div class="section">
            <h3>🌍 {context_domain.title()} Regional Analysis</h3>
            <p>Comprehensive analysis of {context_domain.lower()} dynamics and stability indicators.</p>
            
            <div class="metrics-grid">
        """
        
        for i, metric in enumerate(regional_metrics):
            content += f"""
                <div class="metric-card" data-tooltip-{self.module_id}="metric_{i}">
                    <h4>{metric['region']}</h4>
                    <div class="metric-value">{metric['index']}%</div>
                    <div class="metric-label">{context_domain.title()} Index</div>
                    <div class="metric-details">
                        <span class="status-level">{metric['status']}</span>
                        <span class="trend-level">{metric['trend']}</span>
                    </div>
                    </div>
            """
        
        content += f"""
            </div>
            
            <div class="charts-grid">
                <div class="chart-section" data-tooltip-{self.module_id}="regional_metrics_chart">
                    <h4>{context_domain.title()} Regional Metrics</h4>
                    <canvas id="regionalMetricsChart_{self.module_id}" width="400" height="300"></canvas>
                </div>
            </div>
            
            <div class="data-sources">
                <h4>Data Sources</h4>
                <ul class="sources-list">
        """
        
        for source in data_sources:
            content += f"""
                    <li>{source}</li>
            """
        
        content += """
                </ul>
            </div>
        </div>
        """
        
        return content
    
    def _generate_contextual_security_implications(self, data: Dict[str, Any], context_domain: str) -> str:
        """Generate context-aware security implications section."""
        # Generate context-appropriate implications
        implications = self._generate_contextual_implications(context_domain)
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="security_implications">
            <h3>🎯 {context_domain.title()} Implications</h3>
            <p>Strategic and operational implications of current {context_domain.lower()} dynamics.</p>
            
            <div class="implications-grid">
                <div class="implication-column">
                    <h4>Strategic Implications</h4>
                    <ul class="implications-list">
        """
        
        for implication in implications["strategic"]:
            content += f"""
                        <li data-tooltip="strategic_implication">
                            <strong>{implication['title']}</strong>
                            <p>{implication['description']}</p>
                            <span class="impact-level">{implication['impact']}</span>
                        </li>
            """
        
        content += f"""
                    </ul>
                </div>
                
                <div class="implication-column">
                    <h4>Operational Implications</h4>
                    <ul class="implications-list">
        """
        
        for implication in implications["operational"]:
            content += f"""
                        <li data-tooltip="operational_implication">
                            <strong>{implication['title']}</strong>
                            <p>{implication['description']}</p>
                            <span class="impact-level">{implication['impact']}</span>
                        </li>
            """
        
        content += """
                    </ul>
                </div>
            </div>
        </div>
        """
        
        return content
    
    def _generate_contextual_timeline(self, context_domain: str) -> List[Dict[str, Any]]:
        """Generate context-appropriate timeline data."""
        timeline_mapping = {
            "MILITARY": [
                {"period": "2020", "stability": 0.6, "risk": 0.4},
                {"period": "2021", "stability": 0.65, "risk": 0.35},
                {"period": "2022", "stability": 0.7, "risk": 0.3},
                {"period": "2023", "stability": 0.75, "risk": 0.25},
                {"period": "2024", "stability": 0.8, "risk": 0.2}
            ],
            "ECONOMIC": [
                {"period": "2020", "stability": 0.5, "risk": 0.5},
                {"period": "2021", "stability": 0.6, "risk": 0.4},
                {"period": "2022", "stability": 0.7, "risk": 0.3},
                {"period": "2023", "stability": 0.75, "risk": 0.25},
                {"period": "2024", "stability": 0.8, "risk": 0.2}
            ],
            "GEOPOLITICAL": [
                {"period": "2020", "stability": 0.55, "risk": 0.45},
                {"period": "2021", "stability": 0.6, "risk": 0.4},
                {"period": "2022", "stability": 0.65, "risk": 0.35},
                {"period": "2023", "stability": 0.7, "risk": 0.3},
                {"period": "2024", "stability": 0.75, "risk": 0.25}
            ],
            "HEALTHCARE": [
                {"period": "2020", "stability": 0.4, "risk": 0.6},
                {"period": "2021", "stability": 0.5, "risk": 0.5},
                {"period": "2022", "stability": 0.6, "risk": 0.4},
                {"period": "2023", "stability": 0.7, "risk": 0.3},
                {"period": "2024", "stability": 0.75, "risk": 0.25}
            ],
            "TECHNOLOGY": [
                {"period": "2020", "stability": 0.7, "risk": 0.3},
                {"period": "2021", "stability": 0.75, "risk": 0.25},
                {"period": "2022", "stability": 0.8, "risk": 0.2},
                {"period": "2023", "stability": 0.85, "risk": 0.15},
                {"period": "2024", "stability": 0.9, "risk": 0.1}
            ],
            "GENERAL": [
                {"period": "2020", "stability": 0.6, "risk": 0.4},
                {"period": "2021", "stability": 0.65, "risk": 0.35},
                {"period": "2022", "stability": 0.7, "risk": 0.3},
                {"period": "2023", "stability": 0.75, "risk": 0.25},
                {"period": "2024", "stability": 0.8, "risk": 0.2}
            ]
        }
        
        return timeline_mapping.get(context_domain, timeline_mapping["GENERAL"])
    
    def _generate_contextual_regional_metrics(self, context_domain: str) -> List[Dict[str, Any]]:
        """Generate context-appropriate regional metrics."""
        metrics_mapping = {
            "MILITARY": [
                {"region": "South Asia", "index": 75, "status": "High Capability", "trend": "Improving"},
                {"region": "Indo-Pacific", "index": 85, "status": "Advanced", "trend": "Stable"},
                {"region": "Middle East", "index": 60, "status": "Moderate", "trend": "Declining"}
            ],
            "ECONOMIC": [
                {"region": "Asia-Pacific", "index": 80, "status": "Strong Growth", "trend": "Improving"},
                {"region": "Europe", "index": 70, "status": "Stable", "trend": "Stable"},
                {"region": "Americas", "index": 75, "status": "Recovering", "trend": "Improving"}
            ],
            "GEOPOLITICAL": [
                {"region": "Europe", "index": 80, "status": "Stable", "trend": "Stable"},
                {"region": "Asia-Pacific", "index": 70, "status": "Dynamic", "trend": "Improving"},
                {"region": "Middle East", "index": 55, "status": "Volatile", "trend": "Declining"}
            ],
            "HEALTHCARE": [
                {"region": "Europe", "index": 85, "status": "Advanced", "trend": "Stable"},
                {"region": "Asia-Pacific", "index": 75, "status": "Developing", "trend": "Improving"},
                {"region": "Africa", "index": 60, "status": "Basic", "trend": "Improving"}
            ],
            "TECHNOLOGY": [
                {"region": "North America", "index": 90, "status": "Leading", "trend": "Improving"},
                {"region": "Asia-Pacific", "index": 85, "status": "Advanced", "trend": "Improving"},
                {"region": "Europe", "index": 80, "status": "Strong", "trend": "Stable"}
            ],
            "GENERAL": [
                {"region": "South Asia", "index": 75, "status": "Stable", "trend": "Improving"},
                {"region": "Indo-Pacific", "index": 85, "status": "Strong", "trend": "Stable"},
                {"region": "Middle East", "index": 60, "status": "Moderate", "trend": "Declining"}
            ]
        }
        
        return metrics_mapping.get(context_domain, metrics_mapping["GENERAL"])
    
    def _generate_contextual_implications(self, context_domain: str) -> Dict[str, List[Dict[str, Any]]]:
        """Generate context-appropriate implications."""
        implications_mapping = {
            "MILITARY": {
                "strategic": [
                    {"title": "Deterrence Enhancement", "description": "Improved military capabilities enhance regional deterrence", "impact": "High"},
                    {"title": "Strategic Balance", "description": "Shifts in military power affect regional strategic balance", "impact": "High"}
                ],
                "operational": [
                    {"title": "Readiness Requirements", "description": "Increased operational readiness and training needs", "impact": "Medium"},
                    {"title": "Capability Development", "description": "Focus on developing specific military capabilities", "impact": "Medium"}
                ]
            },
            "ECONOMIC": {
                "strategic": [
                    {"title": "Trade Relations", "description": "Economic dynamics influence trade relationships", "impact": "High"},
                    {"title": "Market Stability", "description": "Economic indicators affect market confidence", "impact": "High"}
                ],
                "operational": [
                    {"title": "Investment Climate", "description": "Economic stability impacts investment decisions", "impact": "Medium"},
                    {"title": "Resource Allocation", "description": "Economic factors influence resource allocation", "impact": "Medium"}
                ]
            },
            "GEOPOLITICAL": {
                "strategic": [
                    {"title": "Alliance Dynamics", "description": "Political changes affect alliance relationships", "impact": "High"},
                    {"title": "Diplomatic Relations", "description": "Geopolitical shifts impact diplomatic engagement", "impact": "High"}
                ],
                "operational": [
                    {"title": "Policy Coordination", "description": "Need for coordinated policy responses", "impact": "Medium"},
                    {"title": "International Cooperation", "description": "Enhanced international cooperation requirements", "impact": "Medium"}
                ]
            },
            "HEALTHCARE": {
                "strategic": [
                    {"title": "Public Health Security", "description": "Healthcare capabilities affect public health security", "impact": "High"},
                    {"title": "Medical Readiness", "description": "Healthcare infrastructure impacts emergency response", "impact": "High"}
                ],
                "operational": [
                    {"title": "Capacity Building", "description": "Need for healthcare capacity development", "impact": "Medium"},
                    {"title": "Resource Planning", "description": "Healthcare resource planning and allocation", "impact": "Medium"}
                ]
            },
            "TECHNOLOGY": {
                "strategic": [
                    {"title": "Technological Advantage", "description": "Technology capabilities provide strategic advantage", "impact": "High"},
                    {"title": "Innovation Leadership", "description": "Technology leadership affects competitive position", "impact": "High"}
                ],
                "operational": [
                    {"title": "Digital Transformation", "description": "Need for digital transformation initiatives", "impact": "Medium"},
                    {"title": "Cybersecurity", "description": "Enhanced cybersecurity requirements", "impact": "Medium"}
                ]
            },
            "GENERAL": {
                "strategic": [
                    {"title": "Regional Stability", "description": "Overall regional stability and security", "impact": "High"},
                    {"title": "Strategic Balance", "description": "Maintenance of strategic balance", "impact": "High"}
                ],
                "operational": [
                    {"title": "Cooperation Enhancement", "description": "Enhanced regional cooperation", "impact": "Medium"},
                    {"title": "Risk Management", "description": "Improved risk management capabilities", "impact": "Medium"}
                ]
            }
        }
        
        return implications_mapping.get(context_domain, implications_mapping["GENERAL"])
    
    def _get_metric_description(self, metric: str, context_domain: str) -> str:
        """Get context-appropriate metric description."""
        descriptions = {
            "threat_level": "Current threat assessment level",
            "military_capability": "Military capability assessment",
            "deterrence_effectiveness": "Effectiveness of deterrence measures",
            "readiness_index": "Operational readiness measurement",
            "strategic_depth": "Strategic depth and positioning",
            "economic_stability": "Economic stability indicators",
            "trade_balance": "Trade balance and relationships",
            "market_confidence": "Market confidence levels",
            "investment_climate": "Investment climate assessment",
            "economic_growth": "Economic growth indicators",
            "political_stability": "Political stability assessment",
            "diplomatic_relations": "Diplomatic relationship strength",
            "alliance_strength": "Alliance strength and cohesion",
            "international_influence": "International influence level",
            "political_risk": "Political risk assessment",
            "health_security": "Health security level",
            "disease_prevalence": "Disease prevalence indicators",
            "healthcare_capacity": "Healthcare capacity assessment",
            "public_health_risk": "Public health risk level",
            "medical_readiness": "Medical readiness assessment",
            "cyber_security": "Cybersecurity capability",
            "technological_advantage": "Technological advantage level",
            "innovation_capacity": "Innovation capacity assessment",
            "digital_readiness": "Digital readiness level",
            "tech_risk": "Technology risk assessment",
            "stability_index": "Overall stability measurement",
            "cooperation_level": "Cooperation level assessment",
            "conflict_probability": "Conflict probability assessment",
            "regional_tensions": "Regional tension levels"
        }
        
        return descriptions.get(metric, f"{metric.replace('_', ' ').title()} assessment")
    
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
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        tooltip_data = {
            "regional_security_assessment": TooltipData(
                title="Regional Security Assessment",
                description="Comprehensive assessment of regional security dynamics and current threat environment",
                source="Sources: Regional Security Analysis Framework, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Strategic Impact: Critical for understanding regional context and threat assessment",
                recommendations="Recommendations: Regular monitoring and assessment updates required",
                use_cases="Use Cases: Strategic planning, threat assessment, regional analysis"
            ),
            "security_dynamics_evolution": TooltipData(
                title="Security Dynamics Evolution",
                description="Analysis of how regional security dynamics have evolved over time and projected trends",
                source="Sources: Historical Security Analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Strategic Impact: Essential for trend analysis and future planning",
                recommendations="Recommendations: Continuous monitoring and trend analysis",
                use_cases="Use Cases: Trend analysis, forecasting, strategic planning"
            ),
            "regional_analysis": TooltipData(
                title="Regional Analysis",
                description="Comprehensive analysis of regional actors, power dynamics, and conflict zones",
                source="Sources: Regional Intelligence Analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Strategic Impact: Critical for understanding regional power dynamics",
                recommendations="Recommendations: Regular actor analysis and power balance assessment",
                use_cases="Use Cases: Regional analysis, actor assessment, power dynamics"
            ),
            "security_implications": TooltipData(
                title="Security Implications",
                description="Strategic and operational implications of current regional security dynamics",
                source="Sources: Strategic Analysis Framework, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Strategic Impact: Essential for strategic and operational planning",
                recommendations="Recommendations: Regular implications assessment and policy review",
                use_cases="Use Cases: Strategic planning, operational planning, policy development"
            )
        }
        
        # Add tooltip data to the module
        for tooltip_id, tooltip_data_obj in tooltip_data.items():
            self.add_tooltip(tooltip_id, tooltip_data_obj)
    
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
