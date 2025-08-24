#!/usr/bin/env python3
"""
Strategic Capability Module

This module provides comprehensive strategic capability forecasting and planning
capabilities, including 5-year strategic horizon analysis and capability development.
"""

import json
from typing import Dict, List, Any, Optional
from loguru import logger

from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData


class StrategicCapabilityModule(BaseModule):
    """Strategic Capability Module for capability forecasting and planning."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Strategic Capability Module."""
        super().__init__(config or ModuleConfig())
        
        # Set module properties
        self.config.title = "Strategic Capability Forecasts"
        self.config.description = "Long-term strategic capability forecasting and planning"
        self.config.enabled = True
        self.config.tooltips_enabled = True
        self.config.charts_enabled = True
        self.config.order = 19  # Strategic Capability is typically module 19
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return ["strategic_capability"]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate strategic capability content."""
        logger.info(f"Generating strategic capability content for {self.module_id}")
        
        try:
            # Extract strategic capability data
            capability_data = data.get("strategic_capability", {})
            
            # Generate main content sections
            content_parts = []
            
            # Capability Forecasts
            capability_forecasts = self._generate_capability_forecasts(capability_data)
            content_parts.append(capability_forecasts)
            
            # 5-Year Strategic Horizon
            five_year_horizon = self._generate_five_year_horizon(capability_data)
            content_parts.append(five_year_horizon)
            
            # Capability Planning
            capability_planning = self._generate_capability_planning(capability_data)
            content_parts.append(capability_planning)
            
            # Strategic Development
            strategic_development = self._generate_strategic_development(capability_data)
            content_parts.append(strategic_development)
            
            # Combine all content
            content = "\n".join(content_parts)
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating strategic capability content: {e}")
            return self._generate_error_content()
    
    def _generate_capability_forecasts(self, data: Dict[str, Any]) -> str:
        """Generate capability forecasts section."""
        forecasts_data = data.get("capability_forecasts", {})
        
        # Extract forecast metrics
        forecasts = forecasts_data.get("forecasts", [])
        
        # Default forecasts if not provided
        if not forecasts:
            forecasts = [
                {"capability": "Naval Power Projection", "current": 0.65, "year_1": 0.70, "year_2": 0.75, "year_3": 0.80, "year_4": 0.85, "year_5": 0.90},
                {"capability": "Strategic Deterrence", "current": 0.75, "year_1": 0.78, "year_2": 0.82, "year_3": 0.85, "year_4": 0.88, "year_5": 0.92},
                {"capability": "Operational Readiness", "current": 0.70, "year_1": 0.73, "year_2": 0.76, "year_3": 0.79, "year_4": 0.82, "year_5": 0.85},
                {"capability": "Technological Superiority", "current": 0.60, "year_1": 0.65, "year_2": 0.70, "year_3": 0.75, "year_4": 0.80, "year_5": 0.85},
                {"capability": "Strategic Mobility", "current": 0.55, "year_1": 0.60, "year_2": 0.65, "year_3": 0.70, "year_4": 0.75, "year_5": 0.80}
            ]
        
        # Generate line chart data for capability forecasts
        line_data = {
            "labels": ["Current", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
            "datasets": []
        }
        
        colors = [
            "rgba(255, 99, 132, 0.8)",
            "rgba(54, 162, 235, 0.8)",
            "rgba(255, 205, 86, 0.8)",
            "rgba(75, 192, 192, 0.8)",
            "rgba(153, 102, 255, 0.8)"
        ]
        
        for i, forecast in enumerate(forecasts):
            line_data["datasets"].append({
                "label": forecast["capability"],
                "data": [forecast["current"], forecast["year_1"], forecast["year_2"], 
                        forecast["year_3"], forecast["year_4"], forecast["year_5"]],
                "borderColor": colors[i % len(colors)],
                "backgroundColor": colors[i % len(colors)].replace("0.8", "0.2"),
                "tension": 0.4,
                "fill": False
            })
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="capability_forecasts">
            <h3>🎯 Capability Forecasts</h3>
            <p>Long-term strategic capability forecasting and development planning.</p>
            
            <div class="forecasts-table">
                <table>
                    <thead>
                        <tr>
                            <th>Capability</th>
                            <th>Current</th>
                            <th>Year 1</th>
                            <th>Year 2</th>
                            <th>Year 3</th>
                            <th>Year 4</th>
                            <th>Year 5</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for forecast in forecasts:
            content += f"""
                        <tr>
                            <td>{forecast['capability']}</td>
                            <td>{forecast['current']:.1%}</td>
                            <td>{forecast['year_1']:.1%}</td>
                            <td>{forecast['year_2']:.1%}</td>
                            <td>{forecast['year_3']:.1%}</td>
                            <td>{forecast['year_4']:.1%}</td>
                            <td>{forecast['year_5']:.1%}</td>
                        </tr>
            """
        
        content += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="chart-container">
                <canvas id="capabilityForecastsChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Capability Forecasts
                const capabilityForecastsCtx = document.getElementById('capabilityForecastsChart').getContext('2d');
                new Chart(capabilityForecastsCtx, {{
                    type: 'line',
                    data: {json.dumps(line_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Timeline'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 1,
                                title: {{
                                    display: true,
                                    text: 'Capability Level'
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
    
    def _generate_five_year_horizon(self, data: Dict[str, Any]) -> str:
        """Generate 5-year strategic horizon section."""
        horizon_data = data.get("five_year_horizon", {})
        
        # Extract horizon metrics
        horizon_metrics = horizon_data.get("horizon_metrics", [])
        
        # Default horizon metrics if not provided
        if not horizon_metrics:
            horizon_metrics = [
                {"dimension": "Strategic Reach", "baseline": 0.60, "target": 0.85, "confidence": 0.80},
                {"dimension": "Operational Flexibility", "baseline": 0.65, "target": 0.90, "confidence": 0.85},
                {"dimension": "Technological Edge", "baseline": 0.55, "target": 0.80, "confidence": 0.75},
                {"dimension": "Strategic Deterrence", "baseline": 0.75, "target": 0.95, "confidence": 0.90},
                {"dimension": "Regional Influence", "baseline": 0.70, "target": 0.88, "confidence": 0.82}
            ]
        
        # Generate radar chart data for horizon analysis
        radar_data = {
            "labels": [metric["dimension"] for metric in horizon_metrics],
            "datasets": [
                {
                    "label": "Baseline (Current)",
                    "data": [metric["baseline"] for metric in horizon_metrics],
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 2,
                    "pointBackgroundColor": "rgba(255, 99, 132, 1)",
                    "pointBorderColor": "#fff",
                    "pointHoverBackgroundColor": "#fff",
                    "pointHoverBorderColor": "rgba(255, 99, 132, 1)"
                },
                {
                    "label": "5-Year Target",
                    "data": [metric["target"] for metric in horizon_metrics],
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 2,
                    "pointBackgroundColor": "rgba(54, 162, 235, 1)",
                    "pointBorderColor": "#fff",
                    "pointHoverBackgroundColor": "#fff",
                    "pointHoverBorderColor": "rgba(54, 162, 235, 1)"
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="five_year_horizon">
            <h3>📅 5-Year Strategic Horizon</h3>
            <p>Strategic planning horizon analysis and long-term capability development.</p>
            
            <div class="horizon-table">
                <table>
                    <thead>
                        <tr>
                            <th>Strategic Dimension</th>
                            <th>Baseline (Current)</th>
                            <th>5-Year Target</th>
                            <th>Confidence Level</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for metric in horizon_metrics:
            content += f"""
                        <tr>
                            <td>{metric['dimension']}</td>
                            <td>{metric['baseline']:.1%}</td>
                            <td>{metric['target']:.1%}</td>
                            <td>{metric['confidence']:.1%}</td>
                        </tr>
            """
        
        content += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="chart-container">
                <canvas id="fiveYearHorizonChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js 5-Year Strategic Horizon
                const fiveYearHorizonCtx = document.getElementById('fiveYearHorizonChart').getContext('2d');
                new Chart(fiveYearHorizonCtx, {{
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
    
    def _generate_capability_planning(self, data: Dict[str, Any]) -> str:
        """Generate capability planning section."""
        planning_data = data.get("capability_planning", {})
        
        # Extract planning phases
        planning_phases = planning_data.get("planning_phases", [])
        
        # Default planning phases if not provided
        if not planning_phases:
            planning_phases = [
                {"phase": "Phase 1: Foundation (Years 1-2)", "focus": "Infrastructure Development", "priority": "High", "resources": "40%", "success_metrics": "Infrastructure readiness, basic capabilities"},
                {"phase": "Phase 2: Enhancement (Years 2-3)", "focus": "Capability Enhancement", "priority": "High", "resources": "35%", "success_metrics": "Enhanced capabilities, operational readiness"},
                {"phase": "Phase 3: Optimization (Years 3-4)", "focus": "Advanced Capabilities", "priority": "Medium", "resources": "20%", "success_metrics": "Advanced capabilities, technological edge"},
                {"phase": "Phase 4: Excellence (Years 4-5)", "focus": "Strategic Excellence", "priority": "Medium", "resources": "5%", "success_metrics": "Strategic superiority, regional leadership"}
            ]
        
        # Generate planning summary
        planning_summary = planning_data.get("summary", {
            "total_phases": 4,
            "total_duration": "5 years",
            "total_investment": "$15.2B",
            "expected_outcome": "Strategic superiority"
        })
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="capability_planning">
            <h3>📋 Capability Planning</h3>
            <p>Comprehensive capability planning and development roadmap.</p>
            
            <div class="planning-summary">
                <h4>Planning Summary</h4>
                <div class="summary-grid">
                    <div class="summary-item">
                        <div class="summary-value">{planning_summary['total_phases']}</div>
                        <div class="summary-label">Total Phases</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{planning_summary['total_duration']}</div>
                        <div class="summary-label">Duration</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{planning_summary['total_investment']}</div>
                        <div class="summary-label">Total Investment</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">{planning_summary['expected_outcome']}</div>
                        <div class="summary-label">Expected Outcome</div>
                    </div>
                </div>
            </div>
            
            <div class="planning-phases">
                <h4>Development Phases</h4>
                <div class="phases-grid">
        """
        
        for phase in planning_phases:
            content += f"""
                    <div class="phase-card">
                        <h5>{phase['phase']}</h5>
                        <div class="phase-details">
                            <div class="phase-detail">
                                <span class="detail-label">Focus:</span>
                                <span class="detail-value">{phase['focus']}</span>
                            </div>
                            <div class="phase-detail">
                                <span class="detail-label">Priority:</span>
                                <span class="detail-value">{phase['priority']}</span>
                            </div>
                            <div class="phase-detail">
                                <span class="detail-label">Resources:</span>
                                <span class="detail-value">{phase['resources']}</span>
                            </div>
                            <div class="phase-detail">
                                <span class="detail-label">Success Metrics:</span>
                                <span class="detail-value">{phase['success_metrics']}</span>
                            </div>
                        </div>
                    </div>
            """
        
        content += """
                </div>
            </div>
        </div>
        """
        
        return content
    
    def _generate_strategic_development(self, data: Dict[str, Any]) -> str:
        """Generate strategic development section."""
        development_data = data.get("strategic_development", {})
        
        # Extract development areas
        development_areas = development_data.get("development_areas", [])
        
        # Default development areas if not provided
        if not development_areas:
            development_areas = [
                {"area": "Technological Innovation", "current_level": 0.65, "target_level": 0.90, "investment": "$4.2B", "timeline": "3-5 years"},
                {"area": "Operational Excellence", "current_level": 0.75, "target_level": 0.95, "investment": "$3.8B", "timeline": "2-4 years"},
                {"area": "Strategic Partnerships", "current_level": 0.60, "target_level": 0.85, "investment": "$2.1B", "timeline": "1-3 years"},
                {"area": "Human Capital Development", "current_level": 0.70, "target_level": 0.88, "investment": "$1.5B", "timeline": "2-3 years"},
                {"area": "Infrastructure Modernization", "current_level": 0.55, "target_level": 0.80, "investment": "$3.6B", "timeline": "3-4 years"}
            ]
        
        # Generate bar chart data for development areas
        bar_data = {
            "labels": [area["area"] for area in development_areas],
            "datasets": [
                {
                    "label": "Current Level",
                    "data": [area["current_level"] for area in development_areas],
                    "backgroundColor": "rgba(255, 99, 132, 0.8)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1
                },
                {
                    "label": "Target Level",
                    "data": [area["target_level"] for area in development_areas],
                    "backgroundColor": "rgba(54, 162, 235, 0.8)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 1
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="strategic_development">
            <h3>🚀 Strategic Development</h3>
            <p>Strategic development areas and investment planning for capability enhancement.</p>
            
            <div class="development-table">
                <table>
                    <thead>
                        <tr>
                            <th>Development Area</th>
                            <th>Current Level</th>
                            <th>Target Level</th>
                            <th>Investment</th>
                            <th>Timeline</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for area in development_areas:
            content += f"""
                        <tr>
                            <td>{area['area']}</td>
                            <td>{area['current_level']:.1%}</td>
                            <td>{area['target_level']:.1%}</td>
                            <td>{area['investment']}</td>
                            <td>{area['timeline']}</td>
                        </tr>
            """
        
        content += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="chart-container">
                <canvas id="strategicDevelopmentChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Strategic Development
                const strategicDevelopmentCtx = document.getElementById('strategicDevelopmentChart').getContext('2d');
                new Chart(strategicDevelopmentCtx, {{
                    type: 'bar',
                    data: {json.dumps(bar_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                stacked: false,
                                title: {{
                                    display: true,
                                    text: 'Development Areas'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 1,
                                title: {{
                                    display: true,
                                    text: 'Development Level'
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
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        tooltip_data = {
            "capability_forecasts": TooltipData(
                title="Capability Forecasts",
                description="Long-term strategic capability forecasting and development planning with 5-year projections across multiple capability dimensions",
                source="Source: Capability Forecasting Model",
                strategic_impact="Strategic Impact: Critical for long-term strategic planning and capability development",
                recommendations="Recommendations: Focus on high-impact capabilities, maintain technological edge, and ensure balanced development across all dimensions",
                use_cases="Use Cases: Strategic planning, resource allocation, capability development, long-term investment planning"
            ),
            "five_year_horizon": TooltipData(
                title="5-Year Strategic Horizon",
                description="Strategic planning horizon analysis and long-term capability development with baseline and target metrics",
                source="Source: Strategic Horizon Analysis",
                strategic_impact="Strategic Impact: Essential for long-term strategic vision and planning",
                recommendations="Recommendations: Set realistic targets, maintain strategic focus, and ensure continuous monitoring and adjustment",
                use_cases="Use Cases: Strategic planning, goal setting, performance monitoring, strategic alignment"
            ),
            "capability_planning": TooltipData(
                title="Capability Planning",
                description="Comprehensive capability planning and development roadmap with phased approach and resource allocation",
                source="Source: Capability Planning Framework",
                strategic_impact="Strategic Impact: Critical for successful capability development and strategic execution",
                recommendations="Recommendations: Prioritize phases based on strategic importance, ensure adequate resource allocation, and maintain flexibility for adjustments",
                use_cases="Use Cases: Project planning, resource allocation, strategic execution, performance management"
            ),
            "strategic_development": TooltipData(
                title="Strategic Development",
                description="Strategic development areas and investment planning for capability enhancement with current and target levels",
                source="Source: Strategic Development Model",
                strategic_impact="Strategic Impact: Fundamental for maintaining competitive advantage and strategic positioning",
                recommendations="Recommendations: Focus on high-impact areas, ensure balanced investment, and maintain strategic alignment",
                use_cases="Use Cases: Investment planning, strategic development, capability enhancement, competitive positioning"
            )
        }
        
        # Add tooltip data to the module
        for tooltip_id, tooltip_data_obj in tooltip_data.items():
            self.add_tooltip(tooltip_id, tooltip_data_obj)
    
    def _generate_error_content(self) -> str:
        """Generate error content when data processing fails."""
        return """
        <div class="section">
            <h3>🎯 Strategic Capability Forecasts</h3>
            <p>Long-term strategic capability forecasting and planning.</p>
            
            <div class="error-message">
                <p>⚠️ Unable to generate strategic capability analysis due to data processing issues.</p>
                <p>Please ensure strategic capability data is properly formatted and available.</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-section" data-tooltip="capability_forecasts_chart">
                    <h3>Capability Forecasts</h3>
                    <canvas id="capabilityForecastsChart" width="400" height="300"></canvas>
                </div>
                <div class="chart-section" data-tooltip="five_year_horizon_chart">
                    <h3>5-Year Strategic Horizon</h3>
                    <canvas id="fiveYearHorizonChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
        """
