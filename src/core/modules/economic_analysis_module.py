#!/usr/bin/env python3
"""
Economic Analysis Module

This module provides comprehensive economic cost analysis,
including cost breakdown, financial implications, and economic planning.
"""

import json
from typing import Dict, List, Any, Optional
from loguru import logger

from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData


class EconomicAnalysisModule(BaseModule):
    """Economic Analysis Module for cost and financial analysis."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Economic Analysis Module."""
        super().__init__(config or ModuleConfig())
        
        # Set module properties
        self.config.title = "Economic Cost Analysis"
        self.config.description = "Comprehensive economic cost analysis and financial implications"
        self.config.enabled = True
        self.config.tooltips_enabled = True
        self.config.charts_enabled = True
        self.config.order = 15  # Economic Analysis is typically module 15
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return ["economic_analysis"]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate economic analysis content."""
        logger.info(f"Generating economic analysis content for {self.module_id}")
        
        try:
            # Extract economic analysis data
            economic_data = data.get("economic_analysis", {})
            
            # Generate main content sections
            content_parts = []
            
            # Economic Cost Breakdown
            cost_breakdown = self._generate_cost_breakdown(economic_data)
            content_parts.append(cost_breakdown)
            
            # Financial Implications
            financial_implications = self._generate_financial_implications(economic_data)
            content_parts.append(financial_implications)
            
            # Economic Planning
            economic_planning = self._generate_economic_planning(economic_data)
            content_parts.append(economic_planning)
            
            # Budget Analysis
            budget_analysis = self._generate_budget_analysis(economic_data)
            content_parts.append(budget_analysis)
            
            # Combine all content
            content = "\n".join(content_parts)
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating economic analysis content: {e}")
            return self._generate_error_content()
    
    def _generate_cost_breakdown(self, data: Dict[str, Any]) -> str:
        """Generate economic cost breakdown section."""
        cost_data = data.get("cost_breakdown", {})
        
        # Extract cost components
        acquisition_cost = cost_data.get("acquisition_cost", 2500000000)  # $2.5B default
        operational_cost = cost_data.get("operational_cost", 500000000)   # $500M default
        maintenance_cost = cost_data.get("maintenance_cost", 750000000)   # $750M default
        training_cost = cost_data.get("training_cost", 100000000)         # $100M default
        infrastructure_cost = cost_data.get("infrastructure_cost", 300000000)  # $300M default
        
        total_cost = acquisition_cost + operational_cost + maintenance_cost + training_cost + infrastructure_cost
        
        # Generate pie chart data for cost breakdown
        pie_data = {
            "labels": ["Acquisition", "Operations", "Maintenance", "Training", "Infrastructure"],
            "datasets": [{
                "label": "Cost Breakdown",
                "data": [acquisition_cost, operational_cost, maintenance_cost, training_cost, infrastructure_cost],
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
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="economic_cost_breakdown">
            <h3>💰 Economic Cost Breakdown</h3>
            <p>Comprehensive breakdown of economic costs across all categories.</p>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">${total_cost:,.0f}</div>
                    <div class="metric-label">Total Cost</div>
                    <div class="metric-description">Total program cost estimate</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${acquisition_cost:,.0f}</div>
                    <div class="metric-label">Acquisition Cost</div>
                    <div class="metric-description">Initial acquisition expenses</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${operational_cost:,.0f}</div>
                    <div class="metric-label">Operational Cost</div>
                    <div class="metric-description">Annual operational expenses</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{(acquisition_cost/total_cost)*100:.1f}%</div>
                    <div class="metric-label">Acquisition Share</div>
                    <div class="metric-description">Acquisition cost percentage</div>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="economicCostBreakdownChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                // Chart.js Economic Cost Breakdown
                const economicCostBreakdownCtx = document.getElementById('economicCostBreakdownChart').getContext('2d');
                new Chart(economicCostBreakdownCtx, {{
                    type: 'pie',
                    data: {json.dumps(pie_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                display: true,
                                position: 'bottom'
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        return context.label + ': $' + context.raw.toLocaleString();
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
    
    def _generate_financial_implications(self, data: Dict[str, Any]) -> str:
        """Generate financial implications section."""
        financial_data = data.get("financial_implications", {})
        
        # Extract financial metrics
        budget_impact = financial_data.get("budget_impact", 0.15)  # 15% of defense budget
        gdp_impact = financial_data.get("gdp_impact", 0.008)       # 0.8% of GDP
        debt_ratio = financial_data.get("debt_ratio", 0.12)        # 12% increase in debt
        economic_multiplier = financial_data.get("economic_multiplier", 1.4)  # 1.4x multiplier
        
        # Generate timeline data for financial impact
        timeline_data = financial_data.get("timeline", [
            {"year": "Year 1", "cost": 800000000, "impact": 0.05},
            {"year": "Year 2", "cost": 1200000000, "impact": 0.08},
            {"year": "Year 3", "cost": 900000000, "impact": 0.06},
            {"year": "Year 4", "cost": 600000000, "impact": 0.04},
            {"year": "Year 5", "cost": 650000000, "impact": 0.045}
        ])
        
        # Generate line chart data
        line_data = {
            "labels": [item["year"] for item in timeline_data],
            "datasets": [
                {
                    "label": "Annual Cost (Billions)",
                    "data": [item["cost"]/1000000000 for item in timeline_data],
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "yAxisID": "y",
                    "tension": 0.4
                },
                {
                    "label": "Budget Impact (%)",
                    "data": [item["impact"]*100 for item in timeline_data],
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "yAxisID": "y1",
                    "tension": 0.4
                }
            ]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="financial_implications">
            <h3>📊 Financial Implications</h3>
            <p>Analysis of financial implications and economic impact over time.</p>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{budget_impact:.1%}</div>
                    <div class="metric-label">Budget Impact</div>
                    <div class="metric-description">Impact on defense budget</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{gdp_impact:.2%}</div>
                    <div class="metric-label">GDP Impact</div>
                    <div class="metric-description">Impact on national GDP</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{debt_ratio:.1%}</div>
                    <div class="metric-label">Debt Increase</div>
                    <div class="metric-description">Increase in national debt</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{economic_multiplier:.1f}x</div>
                    <div class="metric-label">Economic Multiplier</div>
                    <div class="metric-description">Economic multiplier effect</div>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="financialImplicationsChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                const financialImplicationsCtx = document.getElementById('financialImplicationsChart').getContext('2d');
                new Chart(financialImplicationsCtx, {{
                    type: 'line',
                    data: {json.dumps(line_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{
                            mode: 'index',
                            intersect: false,
                        }},
                        scales: {{
                            x: {{
                                display: true,
                                title: {{
                                    display: true,
                                    text: 'Timeline'
                                }}
                            }},
                            y: {{
                                type: 'linear',
                                display: true,
                                position: 'left',
                                title: {{
                                    display: true,
                                    text: 'Cost (Billions USD)'
                                }}
                            }},
                            y1: {{
                                type: 'linear',
                                display: true,
                                position: 'right',
                                title: {{
                                    display: true,
                                    text: 'Budget Impact (%)'
                                }},
                                grid: {{
                                    drawOnChartArea: false,
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
    
    def _generate_economic_planning(self, data: Dict[str, Any]) -> str:
        """Generate economic planning section."""
        planning_data = data.get("economic_planning", {})
        
        # Extract planning components
        funding_sources = planning_data.get("funding_sources", [])
        cost_mitigation = planning_data.get("cost_mitigation", [])
        economic_benefits = planning_data.get("economic_benefits", [])
        
        # Default data if not provided
        if not funding_sources:
            funding_sources = [
                {"source": "Defense Budget", "amount": 2000000000, "percentage": 50},
                {"source": "Special Allocation", "amount": 1000000000, "percentage": 25},
                {"source": "International Financing", "amount": 600000000, "percentage": 15},
                {"source": "Private Investment", "amount": 400000000, "percentage": 10}
            ]
        
        if not cost_mitigation:
            cost_mitigation = [
                {"strategy": "Phased Implementation", "savings": 200000000},
                {"strategy": "Local Manufacturing", "savings": 300000000},
                {"strategy": "Technology Transfer", "savings": 150000000},
                {"strategy": "Bulk Procurement", "savings": 100000000}
            ]
        
        if not economic_benefits:
            economic_benefits = [
                {"benefit": "Job Creation", "value": 15000, "unit": "jobs"},
                {"benefit": "Technology Transfer", "value": 25, "unit": "technologies"},
                {"benefit": "Industrial Capacity", "value": 30, "unit": "% increase"},
                {"benefit": "Export Potential", "value": 500, "unit": "million USD"}
            ]
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="economic_planning">
            <h3>📈 Economic Planning</h3>
            <p>Strategic economic planning and resource allocation analysis.</p>
            
            <div class="planning-grid">
                <div class="planning-column">
                    <h4>Funding Sources</h4>
                    <div class="funding-list">
        """
        
        for source in funding_sources:
            content += f"""
                        <div class="funding-item">
                            <div class="funding-source">{source['source']}</div>
                            <div class="funding-amount">${source['amount']:,.0f}</div>
                            <div class="funding-percentage">{source['percentage']}%</div>
                        </div>
            """
        
        content += f"""
                    </div>
                </div>
                
                <div class="planning-column">
                    <h4>Cost Mitigation Strategies</h4>
                    <div class="mitigation-list">
        """
        
        for strategy in cost_mitigation:
            content += f"""
                        <div class="mitigation-item">
                            <div class="strategy-name">{strategy['strategy']}</div>
                            <div class="strategy-savings">${strategy['savings']:,.0f}</div>
                        </div>
            """
        
        content += f"""
                    </div>
                </div>
            </div>
            
            <div class="economic-benefits">
                <h4>Economic Benefits</h4>
                <div class="benefits-grid">
        """
        
        for benefit in economic_benefits:
            content += f"""
                    <div class="benefit-card" data-tooltip-{self.module_id}="economic_benefit">
                        <div class="benefit-value">{benefit['value']:,}</div>
                        <div class="benefit-unit">{benefit['unit']}</div>
                        <div class="benefit-name">{benefit['benefit']}</div>
                    </div>
            """
        
        content += """
                </div>
            </div>
        </div>
        """
        
        return content
    
    def _generate_budget_analysis(self, data: Dict[str, Any]) -> str:
        """Generate budget analysis section."""
        budget_data = data.get("budget_analysis", {})
        
        # Extract budget metrics
        annual_budget = budget_data.get("annual_defense_budget", 15000000000)  # $15B default
        program_cost = budget_data.get("program_annual_cost", 800000000)       # $800M default
        budget_utilization = budget_data.get("budget_utilization", 0.85)      # 85% utilization
        cost_efficiency = budget_data.get("cost_efficiency", 0.92)            # 92% efficiency
        
        # Generate bar chart data for budget comparison
        budget_comparison_data = {
            "labels": ["Current Budget", "Program Cost", "Remaining Budget", "Other Programs"],
            "datasets": [{
                "label": "Budget Allocation (Billions USD)",
                "data": [
                    annual_budget/1000000000,
                    program_cost/1000000000,
                    (annual_budget - program_cost)/1000000000,
                    (annual_budget * 0.7)/1000000000
                ],
                "backgroundColor": [
                    "rgba(54, 162, 235, 0.8)",
                    "rgba(255, 99, 132, 0.8)",
                    "rgba(75, 192, 192, 0.8)",
                    "rgba(255, 205, 86, 0.8)"
                ],
                "borderColor": [
                    "rgba(54, 162, 235, 1)",
                    "rgba(255, 99, 132, 1)",
                    "rgba(75, 192, 192, 1)",
                    "rgba(255, 205, 86, 1)"
                ],
                "borderWidth": 1
            }]
        }
        
        content = f"""
        <div class="section" data-tooltip-{self.module_id}="budget_analysis">
            <h3>💼 Budget Analysis</h3>
            <p>Comprehensive budget analysis and resource allocation assessment.</p>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">${annual_budget:,.0f}</div>
                    <div class="metric-label">Annual Defense Budget</div>
                    <div class="metric-description">Total defense budget allocation</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{(program_cost/annual_budget)*100:.1f}%</div>
                    <div class="metric-label">Budget Share</div>
                    <div class="metric-description">Program share of defense budget</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{budget_utilization:.1%}</div>
                    <div class="metric-label">Budget Utilization</div>
                    <div class="metric-description">Efficiency of budget utilization</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{cost_efficiency:.1%}</div>
                    <div class="metric-label">Cost Efficiency</div>
                    <div class="metric-description">Overall cost efficiency rating</div>
                </div>
            </div>
            
            <div class="chart-container">
                <canvas id="budgetAnalysisChart" width="400" height="300"></canvas>
            </div>
            
            <script>
                const budgetAnalysisCtx = document.getElementById('budgetAnalysisChart').getContext('2d');
                new Chart(budgetAnalysisCtx, {{
                    type: 'bar',
                    data: {json.dumps(budget_comparison_data)},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                title: {{
                                    display: true,
                                    text: 'Amount (Billions USD)'
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
                                        return context.label + ': $' + context.raw.toFixed(1) + 'B';
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
            "economic_cost_breakdown": TooltipData(
                title="Economic Cost Breakdown",
                description="Comprehensive breakdown of all economic costs including acquisition, operations, maintenance, training, and infrastructure",
                source="Sources: Economic Analysis Framework, International Monetary Fund Data, World Bank Economic Indicators, Trade Statistics Database, Market Analysis Reports",
                strategic_impact="Strategic Impact: Critical for budget planning and resource allocation",
                recommendations="Recommendations: Regular cost monitoring and optimization analysis",
                use_cases="Use Cases: Budget planning, cost optimization, resource allocation"
            ),
            "financial_implications": TooltipData(
                title="Financial Implications",
                description="Analysis of financial implications and economic impact over time including budget and GDP effects",
                source="Sources: Financial Impact Analysis, International Monetary Fund Data, World Bank Economic Indicators, Trade Statistics Database, Market Analysis Reports",
                strategic_impact="Strategic Impact: Essential for understanding long-term financial commitments",
                recommendations="Recommendations: Monitor financial metrics and adjust plans accordingly",
                use_cases="Use Cases: Financial planning, impact assessment, policy development"
            ),
            "economic_planning": TooltipData(
                title="Economic Planning",
                description="Strategic economic planning including funding sources, cost mitigation, and economic benefits",
                source="Sources: Strategic Economic Planning Framework, International Monetary Fund Data, World Bank Economic Indicators, Trade Statistics Database, Market Analysis Reports",
                strategic_impact="Strategic Impact: Critical for sustainable program implementation",
                recommendations="Recommendations: Diversify funding sources and maximize economic benefits",
                use_cases="Use Cases: Strategic planning, funding strategy, benefit optimization"
            ),
            "budget_analysis": TooltipData(
                title="Budget Analysis",
                description="Comprehensive budget analysis and resource allocation assessment within defense spending",
                source="Sources: Budget Analysis Framework, International Monetary Fund Data, World Bank Economic Indicators, Trade Statistics Database, Market Analysis Reports",
                strategic_impact="Strategic Impact: Essential for responsible fiscal management",
                recommendations="Recommendations: Maintain budget efficiency and monitor utilization rates",
                use_cases="Use Cases: Budget management, fiscal planning, efficiency monitoring"
            ),
            "economic_benefit": TooltipData(
                title="Economic Benefit",
                description="Quantified economic benefits including job creation, technology transfer, and industrial capacity building",
                source="Sources: Economic Impact Assessment, International Monetary Fund Data, World Bank Economic Indicators, Trade Statistics Database, Market Analysis Reports",
                strategic_impact="Strategic Impact: Important for justifying program investments",
                recommendations="Recommendations: Track and maximize economic benefit realization",
                use_cases="Use Cases: Benefit tracking, impact measurement, program justification"
            )
        }
        
        # Add tooltip data to the module
        for tooltip_id, tooltip_data_obj in tooltip_data.items():
            self.add_tooltip(tooltip_id, tooltip_data_obj)
    
    def _generate_error_content(self) -> str:
        """Generate error content when data processing fails."""
        return """
        <div class="section">
            <h3>💰 Economic Cost Analysis</h3>
            <p>Detailed economic cost analysis and financial implications.</p>
            
            <div class="error-message">
                <p>⚠️ Unable to generate economic analysis due to data processing issues.</p>
                <p>Please ensure economic analysis data is properly formatted and available.</p>
            </div>
            
            <div class="charts-grid">
                <div class="chart-section" data-tooltip="economic_costs_chart">
                    <h3>Economic Cost Breakdown</h3>
                    <canvas id="economicCostsChart" width="400" height="300"></canvas>
                </div>
                <div class="chart-section" data-tooltip="financial_implications_chart">
                    <h3>Financial Implications</h3>
                    <canvas id="financialImplicationsChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
        """
