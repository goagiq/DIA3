"""
Risk Assessment Module

Independent module for generating risk assessment analysis sections that can be added to any report.
Provides comprehensive risk matrix, escalation probability timeline, risk factor analysis, and mitigation strategies.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class RiskAssessmentModule(BaseModule):
    """Risk Assessment module for enhanced reports."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Risk Assessment module."""
        if config is None:
            config = ModuleConfig(
                title="⚠️ Risk Assessment Analysis",
                description="Comprehensive risk assessment with escalation probability timeline and mitigation strategies",
                order=35,  # Early order for risk importance
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'risk_overview',
            'risk_matrix',
            'escalation_timeline',
            'mitigation_strategies'
        ]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Risk Assessment module."""
        self.validate_data(data)
        
        risk_overview = data.get('risk_overview', {})
        risk_matrix = data.get('risk_matrix', {})
        escalation_timeline = data.get('escalation_timeline', {})
        mitigation_strategies = data.get('mitigation_strategies', {})
        
        # Generate risk overview
        overview_html = self._generate_risk_overview(risk_overview)
        
        # Generate risk matrix analysis
        matrix_html = self._generate_risk_matrix(risk_matrix)
        
        # Generate escalation timeline analysis
        timeline_html = self._generate_escalation_timeline(escalation_timeline)
        
        # Generate mitigation strategies analysis
        mitigation_html = self._generate_mitigation_strategies(mitigation_strategies)
        
        # Generate interactive visualizations
        visualizations_html = self._generate_interactive_visualizations(data)
        
        return f"""
        <div class="section" id="risk-assessment">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {matrix_html}
            {timeline_html}
            {mitigation_html}
            {visualizations_html}
        </div>
        """
    
    def _generate_risk_overview(self, overview_data: Dict[str, Any]) -> str:
        """Generate the risk assessment overview section."""
        title = overview_data.get('title', 'Risk Assessment Analysis')
        overview = overview_data.get('overview', 'No risk overview available.')
        key_risks = overview_data.get('key_risks', [])
        overall_risk_level = overview_data.get('overall_risk_level', 'Medium')
        confidence_score = overview_data.get('confidence_score', 0.0)
        
        risks_html = ""
        if key_risks:
            risks_html = """
            <div class="key-risks">
                <h4>🎯 Key Risk Factors</h4>
                <div class="risks-grid">
            """
            for i, risk in enumerate(key_risks):
                risk_id = f"risk_{i}"
                risks_html += f"""
                <div class="risk-card" data-tooltip-{self.module_id}="{risk_id}">
                    <h5>{risk.get('name', 'Unknown Risk')}</h5>
                    <p class="risk-category">{risk.get('category', 'No category specified')}</p>
                    <p class="risk-level">Risk Level: {risk.get('risk_level', 'Medium')}</p>
                    <p class="risk-probability">Probability: {risk.get('probability', 'Unknown')}%</p>
                </div>
                """
            risks_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="risk-overview">
            <div class="overview-header" data-tooltip-{self.module_id}="risk_overview">
                <h3>⚠️ Risk Overview</h3>
                <h4>{title}</h4>
                <div class="risk-indicator">
                    <span class="risk-label">Overall Risk Level:</span>
                    <span class="risk-value {overall_risk_level.lower()}">{overall_risk_level}</span>
                </div>
                <div class="confidence-indicator">
                    <span class="confidence-label">Confidence:</span>
                    <span class="confidence-value">{confidence_score:.1f}%</span>
                </div>
            </div>
            <div class="overview-content">
                <p>{overview}</p>
            </div>
            {risks_html}
        </div>
        """
    
    def _generate_risk_matrix(self, matrix_data: Dict[str, Any]) -> str:
        """Generate the comprehensive risk matrix section."""
        risk_categories = matrix_data.get('risk_categories', [])
        probability_levels = matrix_data.get('probability_levels', [])
        impact_levels = matrix_data.get('impact_levels', [])
        risk_assessments = matrix_data.get('risk_assessments', [])
        
        categories_html = ""
        if risk_categories:
            categories_html = """
            <div class="risk-categories">
                <h4>📊 Risk Categories</h4>
                <div class="categories-container">
            """
            for i, category in enumerate(risk_categories):
                category_id = f"risk_category_{i}"
                categories_html += f"""
                <div class="category-card" data-tooltip-{self.module_id}="{category_id}">
                    <h5>{category.get('name', 'Unknown Category')}</h5>
                    <div class="category-metrics">
                        <div class="metric">
                            <span class="label">Risk Level:</span>
                            <span class="value">{category.get('risk_level', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Probability:</span>
                            <span class="value">{category.get('probability', 'Unknown')}%</span>
                        </div>
                        <div class="metric">
                            <span class="label">Impact:</span>
                            <span class="value">{category.get('impact', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="category-description">{category.get('description', 'No description available.')}</p>
                </div>
                """
            categories_html += """
                </div>
            </div>
            """
        
        assessments_html = ""
        if risk_assessments:
            assessments_html = """
            <div class="risk-assessments">
                <h4>📈 Risk Assessments</h4>
                <div class="assessments-container">
            """
            for i, assessment in enumerate(risk_assessments):
                assessment_id = f"risk_assessment_{i}"
                assessments_html += f"""
                <div class="assessment-card" data-tooltip-{self.module_id}="{assessment_id}">
                    <h5>{assessment.get('name', 'Unknown Assessment')}</h5>
                    <div class="assessment-metrics">
                        <div class="metric">
                            <span class="label">Risk Score:</span>
                            <span class="value">{assessment.get('risk_score', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Trend:</span>
                            <span class="value">{assessment.get('trend', 'Stable')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Priority:</span>
                            <span class="value">{assessment.get('priority', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="assessment-description">{assessment.get('description', 'No description available.')}</p>
                </div>
                """
            assessments_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="risk-matrix-analysis">
            <h3>📊 Comprehensive Risk Matrix</h3>
            {categories_html}
            {assessments_html}
        </div>
        """
    
    def _generate_escalation_timeline(self, timeline_data: Dict[str, Any]) -> str:
        """Generate the escalation probability timeline section."""
        timeline_periods = timeline_data.get('timeline_periods', [])
        escalation_scenarios = timeline_data.get('escalation_scenarios', [])
        probability_curve = timeline_data.get('probability_curve', {})
        
        periods_html = ""
        if timeline_periods:
            periods_html = """
            <div class="timeline-periods">
                <h4>⏰ Timeline Periods</h4>
                <div class="periods-container">
            """
            for i, period in enumerate(timeline_periods):
                period_id = f"timeline_period_{i}"
                periods_html += f"""
                <div class="period-card" data-tooltip-{self.module_id}="{period_id}">
                    <h5>{period.get('name', 'Unknown Period')}</h5>
                    <div class="period-metrics">
                        <div class="metric">
                            <span class="label">Duration:</span>
                            <span class="value">{period.get('duration', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Risk Level:</span>
                            <span class="value">{period.get('risk_level', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Probability:</span>
                            <span class="value">{period.get('probability', 'Unknown')}%</span>
                        </div>
                    </div>
                    <p class="period-description">{period.get('description', 'No description available.')}</p>
                </div>
                """
            periods_html += """
                </div>
            </div>
            """
        
        scenarios_html = ""
        if escalation_scenarios:
            scenarios_html = """
            <div class="escalation-scenarios">
                <h4>🚨 Escalation Scenarios</h4>
                <div class="scenarios-container">
            """
            for i, scenario in enumerate(escalation_scenarios):
                scenario_id = f"escalation_scenario_{i}"
                scenarios_html += f"""
                <div class="scenario-card" data-tooltip-{self.module_id}="{scenario_id}">
                    <h5>{scenario.get('name', 'Unknown Scenario')}</h5>
                    <div class="scenario-metrics">
                        <div class="metric">
                            <span class="label">Trigger:</span>
                            <span class="value">{scenario.get('trigger', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Probability:</span>
                            <span class="value">{scenario.get('probability', 'Unknown')}%</span>
                        </div>
                        <div class="metric">
                            <span class="label">Impact:</span>
                            <span class="value">{scenario.get('impact', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="scenario-description">{scenario.get('description', 'No description available.')}</p>
                </div>
                """
            scenarios_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="escalation-timeline-analysis">
            <h3>⏰ Escalation Probability Timeline</h3>
            {periods_html}
            {scenarios_html}
        </div>
        """
    
    def _generate_mitigation_strategies(self, strategies_data: Dict[str, Any]) -> str:
        """Generate the mitigation strategies analysis section."""
        strategy_categories = strategies_data.get('strategy_categories', [])
        implementation_plans = strategies_data.get('implementation_plans', [])
        effectiveness_metrics = strategies_data.get('effectiveness_metrics', {})
        
        categories_html = ""
        if strategy_categories:
            categories_html = """
            <div class="strategy-categories">
                <h4>🛡️ Mitigation Strategy Categories</h4>
                <div class="categories-container">
            """
            for i, category in enumerate(strategy_categories):
                category_id = f"strategy_category_{i}"
                categories_html += f"""
                <div class="category-card" data-tooltip-{self.module_id}="{category_id}">
                    <h5>{category.get('name', 'Unknown Category')}</h5>
                    <div class="category-metrics">
                        <div class="metric">
                            <span class="label">Effectiveness:</span>
                            <span class="value">{category.get('effectiveness', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Cost:</span>
                            <span class="value">{category.get('cost', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Timeline:</span>
                            <span class="value">{category.get('timeline', 'Unknown')}</span>
                        </div>
                    </div>
                    <p class="category-description">{category.get('description', 'No description available.')}</p>
                </div>
                """
            categories_html += """
                </div>
            </div>
            """
        
        plans_html = ""
        if implementation_plans:
            plans_html = """
            <div class="implementation-plans">
                <h4>📋 Implementation Plans</h4>
                <div class="plans-container">
            """
            for i, plan in enumerate(implementation_plans):
                plan_id = f"implementation_plan_{i}"
                plans_html += f"""
                <div class="plan-card" data-tooltip-{self.module_id}="{plan_id}">
                    <h5>{plan.get('name', 'Unknown Plan')}</h5>
                    <div class="plan-metrics">
                        <div class="metric">
                            <span class="label">Priority:</span>
                            <span class="value">{plan.get('priority', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Timeline:</span>
                            <span class="value">{plan.get('timeline', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Resources:</span>
                            <span class="value">{plan.get('resources', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="plan-description">{plan.get('description', 'No description available.')}</p>
                </div>
                """
            plans_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="mitigation-strategies-analysis">
            <h3>🛡️ Mitigation Strategies</h3>
            {categories_html}
            {plans_html}
        </div>
        """
    
    def _generate_interactive_visualizations(self, data: Dict[str, Any]) -> str:
        """Generate interactive visualizations for risk assessment analysis."""
        if not self.config.charts_enabled:
            return ""
        
        # Generate risk matrix heatmap
        risk_chart_html = self._generate_risk_matrix_chart(data)
        
        # Generate escalation timeline chart
        timeline_chart_html = self._generate_escalation_timeline_chart(data)
        
        return f"""
        <div class="risk-visualizations">
            <h3>📈 Interactive Visualizations</h3>
            {risk_chart_html}
            {timeline_chart_html}
        </div>
        """
    
    def _generate_risk_matrix_chart(self, data: Dict[str, Any]) -> str:
        """Generate a heatmap chart for risk matrix visualization."""
        risk_matrix = data.get('risk_matrix', {})
        risk_categories = risk_matrix.get('risk_categories', [])
        
        if not risk_categories:
            return ""
        
        # Prepare chart data
        categories = [cat.get('name', 'Unknown') for cat in risk_categories]
        probabilities = [self._convert_risk_to_number(cat.get('probability', '50%')) for cat in risk_categories]
        impacts = [self._convert_impact_to_number(cat.get('impact', 'Medium')) for cat in risk_categories]
        
        chart_id = f"risk_matrix_{self.module_id}"
        
        # Add chart data to the module
        self.add_chart_data(chart_id, {
            'type': 'bar',
            'data': {
                'labels': categories,
                'datasets': [{
                    'label': 'Risk Probability (%)',
                    'data': probabilities,
                    'backgroundColor': 'rgba(255, 99, 132, 0.8)',
                    'borderColor': 'rgba(255, 99, 132, 1)',
                    'borderWidth': 1
                }, {
                    'label': 'Risk Impact Score',
                    'data': impacts,
                    'backgroundColor': 'rgba(54, 162, 235, 0.8)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'max': 100
                    }
                },
                'plugins': {
                    'legend': {
                        'position': 'top'
                    },
                    'title': {
                        'display': True,
                        'text': 'Risk Matrix Analysis'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>📊 Risk Matrix Heatmap</h4>
            <canvas id="{chart_id}" width="400" height="300"></canvas>
        </div>
        """
    
    def _generate_escalation_timeline_chart(self, data: Dict[str, Any]) -> str:
        """Generate a line chart for escalation timeline visualization."""
        escalation_timeline = data.get('escalation_timeline', {})
        timeline_periods = escalation_timeline.get('timeline_periods', [])
        
        if not timeline_periods:
            return ""
        
        # Prepare chart data
        periods = [period.get('name', 'Unknown') for period in timeline_periods]
        probabilities = [self._convert_risk_to_number(period.get('probability', '50%')) for period in timeline_periods]
        
        chart_id = f"escalation_timeline_{self.module_id}"
        
        # Add chart data to the module
        self.add_chart_data(chart_id, {
            'type': 'line',
            'data': {
                'labels': periods,
                'datasets': [{
                    'label': 'Escalation Probability (%)',
                    'data': probabilities,
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 2,
                    'fill': False
                }]
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'max': 100
                    }
                },
                'plugins': {
                    'legend': {
                        'position': 'top'
                    },
                    'title': {
                        'display': True,
                        'text': 'Escalation Timeline'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>⏰ Escalation Timeline</h4>
            <canvas id="{chart_id}" width="400" height="300"></canvas>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        # Risk overview tooltips
        self.add_tooltip("risk_overview", TooltipData(
            title="Risk Overview",
            description="Comprehensive analysis of the current risk landscape and its strategic implications.",
            source="Risk Assessment Framework",
            strategic_impact="High - Critical for risk management and strategic planning",
            recommendations="• Monitor risk indicators regularly\n• Assess risk trends\n• Track escalation factors\n• Plan mitigation strategies",
            use_cases="Used in risk management, strategic planning, and threat assessment",
            confidence=90.0
        ))
        
        self.add_tooltip("risk_matrix", TooltipData(
            title="Risk Matrix",
            description="Comprehensive risk matrix showing probability and impact assessments across different risk categories.",
            source="Risk Matrix Analysis Framework",
            strategic_impact="High - Essential for risk prioritization and resource allocation",
            recommendations="• Prioritize high-probability, high-impact risks\n• Monitor risk trends\n• Track risk evolution\n• Plan risk responses",
            use_cases="Used in risk prioritization and resource allocation",
            confidence=88.0
        ))
        
        self.add_tooltip("escalation_timeline", TooltipData(
            title="Escalation Timeline",
            description="Analysis of how risks may escalate over time and the probability of different escalation scenarios.",
            source="Escalation Analysis Framework",
            strategic_impact="High - Critical for proactive risk management and early warning",
            recommendations="• Monitor escalation indicators\n• Track timeline trends\n• Plan escalation responses\n• Develop early warning systems",
            use_cases="Used in proactive risk management and early warning systems",
            confidence=85.0
        ))
        
        self.add_tooltip("mitigation_strategies", TooltipData(
            title="Mitigation Strategies",
            description="Comprehensive analysis of mitigation strategies, their effectiveness, and implementation plans.",
            source="Mitigation Strategy Framework",
            strategic_impact="High - Essential for risk reduction and strategic planning",
            recommendations="• Implement high-effectiveness strategies\n• Monitor strategy effectiveness\n• Track implementation progress\n• Plan strategy adjustments",
            use_cases="Used in risk reduction and strategic planning",
            confidence=87.0
        ))
    
    def _convert_risk_to_number(self, risk: str) -> float:
        """Convert risk level to numerical value for charts."""
        # Extract percentage from string like "85%" or "High (85%)"
        import re
        numbers = re.findall(r'\d+', str(risk))
        if numbers:
            return float(numbers[0])
        
        # Convert text levels to numbers
        risk_map = {
            'Very Low': 20,
            'Low': 40,
            'Medium': 60,
            'High': 80,
            'Very High': 100
        }
        return risk_map.get(risk, 50.0)
    
    def _convert_impact_to_number(self, impact: str) -> float:
        """Convert impact level to numerical value for charts."""
        impact_map = {
            'Very Low': 20,
            'Low': 40,
            'Medium': 60,
            'High': 80,
            'Very High': 100
        }
        return impact_map.get(impact, 50.0)
