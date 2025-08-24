#!/usr/bin/env python3
"""
Comparison Analysis Module

This module provides comprehensive comparison analysis of strategic options,
including options comparison, assessment, and evaluation capabilities.
"""

import json
from typing import Dict, List, Any, Optional
from loguru import logger

from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData


class ComparisonAnalysisModule(BaseModule):
    """Comparison Analysis Module for strategic options comparison and assessment."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Comparison Analysis Module."""
        super().__init__(config or ModuleConfig())
        
        # Set module properties
        self.config.title = "Comparison Analysis & Strategic Options"
        self.config.description = "Comprehensive comparison analysis of strategic options and alternatives"
        self.config.enabled = True
        self.config.tooltips_enabled = True
        self.config.charts_enabled = True
        self.config.order = 16  # Comparison Analysis is typically module 16
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return ["comparison_analysis"]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate comparison analysis content."""
        logger.info(f"Generating comparison analysis content for {self.module_id}")
        
        try:
            # Extract comparison analysis data
            comparison_data = data.get("comparison_analysis", {})
            
            # Generate main content sections
            content_parts = []
            
            # Strategic Options Comparison
            options_comparison = self._generate_options_comparison(comparison_data)
            content_parts.append(options_comparison)
            
            # Strategic Options Assessment
            options_assessment = self._generate_options_assessment(comparison_data)
            content_parts.append(options_assessment)
            
            # Comparative Analysis
            comparative_analysis = self._generate_comparative_analysis(comparison_data)
            content_parts.append(comparative_analysis)
            
            # Option Evaluation
            option_evaluation = self._generate_option_evaluation(comparison_data)
            content_parts.append(option_evaluation)
            
            # Combine all content
            content = "\n".join(content_parts)
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating comparison analysis content: {e}")
            return self._generate_error_content()
    
    def _generate_options_comparison(self, data: Dict[str, Any]) -> str:
        """Generate strategic options comparison section."""
        options_data = data.get("strategic_options", {})
        
        # Extract strategic options
        options = options_data.get("options", [])
        
        # Default options if not provided
        if not options:
            options = [
                {
                    "name": "Option A: Full Acquisition",
                    "cost": 5000000000,
                    "timeline": 5,
                    "risk": 0.3,
                    "benefit": 0.8,
                    "feasibility": 0.7
                },
                {
                    "name": "Option B: Phased Implementation",
                    "cost": 3500000000,
                    "timeline": 7,
                    "risk": 0.2,
                    "benefit": 0.6,
                    "feasibility": 0.9
                },
                {
                    "name": "Option C: Joint Development",
                    "cost": 2500000000,
                    "timeline": 8,
                    "risk": 0.4,
                    "benefit": 0.7,
                    "feasibility": 0.6
                },
                {
                    "name": "Option D: Technology Transfer",
                    "cost": 1500000000,
                    "timeline": 3,
                    "risk": 0.1,
                    "benefit": 0.4,
                    "feasibility": 0.95
                }
            ]
        
        # Generate radar chart data for options comparison
        radar_data = {
            "labels": ["Cost Efficiency", "Timeline", "Risk Management", "Benefit", "Feasibility"],
            "datasets": []
        }
        
        colors = [
            "rgba(255, 99, 132, 0.8)",
            "rgba(54, 162, 235, 0.8)",
            "rgba(255, 205, 86, 0.8)",
            "rgba(75, 192, 192, 0.8)"
        ]
        
        for i, option in enumerate(options):
            # Normalize values for radar chart (0-1 scale)
            cost_efficiency = 1 - (option["cost"] / 5000000000)  # Inverse of cost
            timeline_score = 1 - (option["timeline"] / 10)  # Shorter timeline is better
            risk_score = 1 - option["risk"]  # Lower risk is better
            benefit_score = option["benefit"]
            feasibility_score = option["feasibility"]
            
            radar_data["datasets"].append({
                "label": option["name"],
                "data": [cost_efficiency, timeline_score, risk_score, benefit_score, feasibility_score],
                "backgroundColor": colors[i % len(colors)],
                "borderColor": colors[i % len(colors)].replace("0.8", "1"),
                "borderWidth": 2,
                "pointBackgroundColor": colors[i % len(colors)],
                "pointBorderColor": "#fff",
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": colors[i % len(colors)]
            })
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="strategic_options_comparison">
            <h3>⚖️ Strategic Options Comparison</h3>
            <p>Comprehensive comparison of strategic options across multiple dimensions.</p>
            
            <div class="options-grid">
        """
        
        for option in options:
            content += f"""
                <div class="option-card">
                    <h4>{option['name']}</h4>
                    <div class="option-metrics">
                        <div class="metric">
                            <span class="metric-label">Cost:</span>
                            <span class="metric-value">${option['cost']:,.0f}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Timeline:</span>
                            <span class="metric-value">{option['timeline']} years</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Risk:</span>
                            <span class="metric-value">{option['risk']:.1%}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Benefit:</span>
                            <span class="metric-value">{option['benefit']:.1%}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Feasibility:</span>
                            <span class="metric-value">{option['feasibility']:.1%}</span>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="strategicOptionsComparisonChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Strategic Options Comparison
                const strategicOptionsComparisonCtx = document.getElementById('strategicOptionsComparisonChart').getContext('2d');
                new Chart(strategicOptionsComparisonCtx, {{
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
    
    def _generate_options_assessment(self, data: Dict[str, Any]) -> str:
        """Generate strategic options assessment section."""
        assessment_data = data.get("options_assessment", {})
        
        # Extract assessment criteria
        criteria = assessment_data.get("criteria", [])
        
        # Default assessment criteria if not provided
        if not criteria:
            criteria = [
                {"criterion": "Strategic Alignment", "weight": 0.25},
                {"criterion": "Cost Effectiveness", "weight": 0.20},
                {"criterion": "Risk Management", "weight": 0.20},
                {"criterion": "Implementation Feasibility", "weight": 0.15},
                {"criterion": "Long-term Sustainability", "weight": 0.10},
                {"criterion": "Technology Readiness", "weight": 0.10}
            ]
        
        # Extract option scores
        option_scores = assessment_data.get("option_scores", {})
        
        # Default scores if not provided
        if not option_scores:
            option_scores = {
                "Option A": [0.8, 0.6, 0.7, 0.7, 0.8, 0.9],
                "Option B": [0.7, 0.8, 0.8, 0.9, 0.7, 0.6],
                "Option C": [0.6, 0.9, 0.6, 0.6, 0.6, 0.7],
                "Option D": [0.5, 0.9, 0.9, 0.9, 0.5, 0.5]
            }
        
        # Generate bar chart data for assessment
        bar_data = {
            "labels": [criterion["criterion"] for criterion in criteria],
            "datasets": []
        }
        
        colors = [
            "rgba(255, 99, 132, 0.8)",
            "rgba(54, 162, 235, 0.8)",
            "rgba(255, 205, 86, 0.8)",
            "rgba(75, 192, 192, 0.8)"
        ]
        
        for i, (option_name, scores) in enumerate(option_scores.items()):
            bar_data["datasets"].append({
                "label": option_name,
                "data": scores,
                "backgroundColor": colors[i % len(colors)],
                "borderColor": colors[i % len(colors)].replace("0.8", "1"),
                "borderWidth": 1
            })
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="strategic_options_assessment">
            <h3>📊 Strategic Options Assessment</h3>
            <p>Detailed assessment of strategic options against key criteria.</p>
            
            <div class="assessment-criteria">
                <h4>Assessment Criteria</h4>
                <div class="criteria-grid">
        """
        
        for criterion in criteria:
            content += f"""
                    <div class="criterion-item">
                        <div class="criterion-name">{criterion['criterion']}</div>
                        <div class="criterion-weight">{criterion['weight']:.1%}</div>
                    </div>
            """
        
        content += f"""
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="strategicOptionsAssessmentChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Strategic Options Assessment
                const strategicOptionsAssessmentCtx = document.getElementById('strategicOptionsAssessmentChart').getContext('2d');
                new Chart(strategicOptionsAssessmentCtx, {{
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
                                    text: 'Assessment Criteria'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 1,
                                title: {{
                                    display: true,
                                    text: 'Score'
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
    
    def _generate_comparative_analysis(self, data: Dict[str, Any]) -> str:
        """Generate comparative analysis section."""
        comparative_data = data.get("comparative_analysis", {})
        
        # Extract comparison metrics
        metrics = comparative_data.get("metrics", [])
        
        # Default metrics if not provided
        if not metrics:
            metrics = [
                {"metric": "Total Cost", "unit": "USD", "options": {"A": 5000000000, "B": 3500000000, "C": 2500000000, "D": 1500000000}},
                {"metric": "Implementation Time", "unit": "Years", "options": {"A": 5, "B": 7, "C": 8, "D": 3}},
                {"metric": "Risk Level", "unit": "Score", "options": {"A": 0.3, "B": 0.2, "C": 0.4, "D": 0.1}},
                {"metric": "Strategic Value", "unit": "Score", "options": {"A": 0.8, "B": 0.6, "C": 0.7, "D": 0.4}},
                {"metric": "Technology Maturity", "unit": "Score", "options": {"A": 0.9, "B": 0.6, "C": 0.7, "D": 0.5}}
            ]
        
        # Generate comparison table data
        table_data = {
            "labels": [metric["metric"] for metric in metrics],
            "datasets": []
        }
        
        colors = [
            "rgba(255, 99, 132, 0.8)",
            "rgba(54, 162, 235, 0.8)",
            "rgba(255, 205, 86, 0.8)",
            "rgba(75, 192, 192, 0.8)"
        ]
        
        for i, option in enumerate(["A", "B", "C", "D"]):
            values = []
            for metric in metrics:
                value = metric["options"][option]
                # Normalize values for better visualization
                if metric["metric"] == "Total Cost":
                    normalized_value = value / 5000000000  # Normalize to 0-1
                elif metric["metric"] == "Implementation Time":
                    normalized_value = 1 - (value / 10)  # Shorter time is better
                elif metric["metric"] == "Risk Level":
                    normalized_value = 1 - value  # Lower risk is better
                else:
                    normalized_value = value  # Already 0-1 scale
                
                values.append(normalized_value)
            
            table_data["datasets"].append({
                "label": f"Option {option}",
                "data": values,
                "backgroundColor": colors[i % len(colors)],
                "borderColor": colors[i % len(colors)].replace("0.8", "1"),
                "borderWidth": 1
            })
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="comparative_analysis">
            <h3>📈 Comparative Analysis</h3>
            <p>Detailed comparative analysis of strategic options across key metrics.</p>
            
            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Option A</th>
                            <th>Option B</th>
                            <th>Option C</th>
                            <th>Option D</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for metric in metrics:
            content += f"""
                        <tr>
                            <td>{metric['metric']}</td>
                            <td>{metric['options']['A']:,.0f} {metric['unit']}</td>
                            <td>{metric['options']['B']:,.0f} {metric['unit']}</td>
                            <td>{metric['options']['C']:,.0f} {metric['unit']}</td>
                            <td>{metric['options']['D']:,.0f} {metric['unit']}</td>
                        </tr>
            """
        
        content += f"""
                    </tbody>
                </table>
            </div>
            
            <div class="chart-container">
                <canvas id="comparativeAnalysisChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Comparative Analysis
                const comparativeAnalysisCtx = document.getElementById('comparativeAnalysisChart').getContext('2d');
                new Chart(comparativeAnalysisCtx, {{
                    type: 'bar',
                    data: {json.dumps(table_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                stacked: false,
                                title: {{
                                    display: true,
                                    text: 'Metrics'
                                }}
                            }},
                            y: {{
                                beginAtZero: true,
                                max: 1,
                                title: {{
                                    display: true,
                                    text: 'Normalized Score'
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
    
    def _generate_option_evaluation(self, data: Dict[str, Any]) -> str:
        """Generate option evaluation section."""
        evaluation_data = data.get("option_evaluation", {})
        
        # Extract evaluation results
        evaluations = evaluation_data.get("evaluations", [])
        
        # Default evaluations if not provided
        if not evaluations:
            evaluations = [
                {
                    "option": "Option A: Full Acquisition",
                    "overall_score": 0.75,
                    "strengths": ["High strategic value", "Advanced technology", "Complete control"],
                    "weaknesses": ["High cost", "Long timeline", "High risk"],
                    "recommendation": "Consider for high-priority strategic needs"
                },
                {
                    "option": "Option B: Phased Implementation",
                    "overall_score": 0.82,
                    "strengths": ["Manageable cost", "Reduced risk", "Flexible timeline"],
                    "weaknesses": ["Longer total timeline", "Complex coordination"],
                    "recommendation": "Recommended for balanced approach"
                },
                {
                    "option": "Option C: Joint Development",
                    "overall_score": 0.68,
                    "strengths": ["Cost sharing", "International cooperation", "Technology transfer"],
                    "weaknesses": ["Complex partnerships", "Shared control", "Coordination challenges"],
                    "recommendation": "Consider for international collaboration"
                },
                {
                    "option": "Option D: Technology Transfer",
                    "overall_score": 0.58,
                    "strengths": ["Lowest cost", "Quick implementation", "Low risk"],
                    "weaknesses": ["Limited strategic value", "Dependency on others", "Limited control"],
                    "recommendation": "Consider for immediate needs with limited resources"
                }
            ]
        
        # Generate evaluation chart data
        evaluation_chart_data = {
            "labels": [eval_item["option"] for eval_item in evaluations],
            "datasets": [{
                "label": "Overall Score",
                "data": [eval_item["overall_score"] for eval_item in evaluations],
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
            }]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="option_evaluation">
            <h3>🎯 Option Evaluation</h3>
            <p>Comprehensive evaluation of strategic options with strengths, weaknesses, and recommendations.</p>
            
            <div class="evaluation-results">
        """
        
        for evaluation in evaluations:
            content += f"""
                <div class="evaluation-card">
                    <h4>{evaluation['option']}</h4>
                    <div class="evaluation-score">
                        <span class="score-label">Overall Score:</span>
                        <span class="score-value">{evaluation['overall_score']:.1%}</span>
                    </div>
                    <div class="evaluation-details">
                        <div class="strengths">
                            <h5>Strengths:</h5>
                            <ul>
            """
            
            for strength in evaluation["strengths"]:
                content += f"<li>{strength}</li>"
            
            content += f"""
                            </ul>
                        </div>
                        <div class="weaknesses">
                            <h5>Weaknesses:</h5>
                            <ul>
            """
            
            for weakness in evaluation["weaknesses"]:
                content += f"<li>{weakness}</li>"
            
            content += f"""
                            </ul>
                        </div>
                        <div class="recommendation">
                            <h5>Recommendation:</h5>
                            <p>{evaluation['recommendation']}</p>
                        </div>
                    </div>
                </div>
            """
        
        content += f"""
            </div>
            
            <div class="chart-container">
                <canvas id="optionEvaluationChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Option Evaluation
                const optionEvaluationCtx = document.getElementById('optionEvaluationChart').getContext('2d');
                new Chart(optionEvaluationCtx, {{
                    type: 'bar',
                    data: {json.dumps(evaluation_chart_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                max: 1,
                                title: {{
                                    display: true,
                                    text: 'Overall Score'
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: false
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        return 'Score: ' + (context.raw * 100).toFixed(1) + '%';
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
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        tooltip_data = {
            "strategic_options_comparison": TooltipData(
                title="Strategic Options Comparison",
                description="Comprehensive comparison of strategic options across cost, timeline, risk, benefit, and feasibility dimensions",
                source="Source: Strategic Analysis Framework",
                strategic_impact="Strategic Impact: Critical for informed decision-making and resource allocation",
                recommendations="Recommendations: Use radar chart analysis to identify optimal option balance",
                use_cases="Use Cases: Strategic planning, option evaluation, decision support"
            ),
            "strategic_options_assessment": TooltipData(
                title="Strategic Options Assessment",
                description="Detailed assessment of strategic options against key criteria including strategic alignment, cost effectiveness, and risk management",
                source="Source: Multi-Criteria Decision Analysis",
                strategic_impact="Strategic Impact: Essential for systematic option evaluation and prioritization",
                recommendations="Recommendations: Weight criteria based on strategic priorities and organizational goals",
                use_cases="Use Cases: Option prioritization, criteria-based evaluation, strategic alignment"
            ),
            "comparative_analysis": TooltipData(
                title="Comparative Analysis",
                description="Detailed comparative analysis of strategic options across multiple metrics and performance indicators",
                source="Source: Comparative Analysis Framework",
                strategic_impact="Strategic Impact: Important for understanding option trade-offs and relative performance",
                recommendations="Recommendations: Consider normalized scores for fair comparison across different metrics",
                use_cases="Use Cases: Performance comparison, trade-off analysis, metric evaluation"
            ),
            "option_evaluation": TooltipData(
                title="Option Evaluation",
                description="Comprehensive evaluation of strategic options with strengths, weaknesses, and recommendations",
                source="Source: Strategic Evaluation Framework",
                strategic_impact="Strategic Impact: Critical for final option selection and implementation planning",
                recommendations="Recommendations: Consider overall scores alongside specific strengths and weaknesses",
                use_cases="Use Cases: Final option selection, implementation planning, strategic guidance"
            )
        }
        
        # Add tooltip data to the module
        for tooltip_id, tooltip_data_obj in tooltip_data.items():
            self.add_tooltip(tooltip_id, tooltip_data_obj)
    
    def _generate_error_content(self) -> str:
        """Generate error content when data processing fails."""
        return """
        <div class="section">
            <h3>⚖️ Comparison Analysis & Strategic Options</h3>
            <p>Comparative analysis of strategic options and alternatives.</p>
            
            <div class="error-message">
                <p>⚠️ Unable to generate comparison analysis due to data processing issues.</p>
                <p>Please ensure comparison analysis data is properly formatted and available.</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-section" data-tooltip="comparison_analysis_chart">
                    <h3>Strategic Options Comparison</h3>
                    <canvas id="comparisonAnalysisChart" width="400" height="300"></canvas>
                </div>
                <div class="chart-section" data-tooltip="strategic_options_chart">
                    <h3>Strategic Options Assessment</h3>
                    <canvas id="strategicOptionsChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
        """
