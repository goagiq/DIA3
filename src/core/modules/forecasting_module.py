"""
Forecasting Module

Independent module for generating forecasting and predictive analytics sections that can be added to any report.
Provides scenario analysis, trend forecasting, risk assessment, and Monte Carlo simulation capabilities.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


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
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Forecasting module."""
        self.validate_data(data)
        
        forecasting_overview = data.get('forecasting_overview', {})
        scenario_analysis = data.get('scenario_analysis', {})
        trend_analysis = data.get('trend_analysis', {})
        risk_assessment = data.get('risk_assessment', {})
        
        # Generate forecasting overview
        overview_html = self._generate_forecasting_overview(forecasting_overview)
        
        # Generate scenario analysis
        scenarios_html = self._generate_scenario_analysis(scenario_analysis)
        
        # Generate trend analysis
        trends_html = self._generate_trend_analysis(trend_analysis)
        
        # Generate risk assessment
        risk_html = self._generate_risk_assessment(risk_assessment)
        
        # Generate interactive visualizations
        visualizations_html = self._generate_interactive_visualizations(data)
        
        return f"""
        <div class="section" id="forecasting">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {scenarios_html}
            {trends_html}
            {risk_html}
            {visualizations_html}
        </div>
        """
    
    def _generate_forecasting_overview(self, overview_data: Dict[str, Any]) -> str:
        """Generate the forecasting overview section."""
        title = overview_data.get('title', 'Forecasting Overview')
        overview = overview_data.get('overview', 'No forecasting overview available.')
        time_horizon = overview_data.get('time_horizon', 'Unknown')
        confidence_level = overview_data.get('confidence_level', 'Unknown')
        methodology = overview_data.get('methodology', 'No methodology specified.')
        key_metrics = overview_data.get('key_metrics', [])
        
        metrics_html = ""
        if key_metrics:
            metrics_html = """
            <div class="forecasting-metrics">
                <h4>📊 Key Forecasting Metrics</h4>
                <div class="metrics-grid">
            """
            for i, metric in enumerate(key_metrics):
                metric_id = f"metric_{i}"
                metrics_html += f"""
                <div class="metric-card" data-tooltip-{self.module_id}="{metric_id}">
                    <h5>{metric.get('name', 'Unknown Metric')}</h5>
                    <p class="metric-value">{metric.get('value', 'Unknown')}</p>
                    <p class="metric-description">{metric.get('description', 'No description available.')}</p>
                    <p class="metric-trend">Trend: {metric.get('trend', 'Unknown')}</p>
                </div>
                """
            metrics_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="forecasting-overview-section">
            <h3>🔮 {title}</h3>
            <div class="overview-content">
                <p>{overview}</p>
                
                <div class="forecasting-parameters">
                    <div class="parameter-card">
                        <h4>Time Horizon</h4>
                        <p class="parameter-value">{time_horizon}</p>
                    </div>
                    <div class="parameter-card">
                        <h4>Confidence Level</h4>
                        <p class="parameter-value">{confidence_level}</p>
                    </div>
                    <div class="parameter-card">
                        <h4>Methodology</h4>
                        <p class="parameter-value">{methodology}</p>
                    </div>
                </div>
                
                {metrics_html}
            </div>
        </div>
        """
    
    def _generate_scenario_analysis(self, scenario_data: Dict[str, Any]) -> str:
        """Generate the scenario analysis section."""
        title = scenario_data.get('title', 'Scenario Analysis')
        overview = scenario_data.get('overview', 'No scenario analysis overview available.')
        scenarios = scenario_data.get('scenarios', [])
        
        scenarios_html = ""
        if scenarios:
            scenarios_html = """
            <div class="scenario-analysis">
                <h4>🎯 Future Scenarios</h4>
                <div class="scenarios-grid">
            """
            for i, scenario in enumerate(scenarios):
                scenario_id = f"scenario_{i}"
                probability_color = self._get_probability_color(scenario.get('probability', 0))
                scenarios_html += f"""
                <div class="scenario-card {probability_color}" data-tooltip-{self.module_id}="{scenario_id}">
                    <div class="scenario-header">
                        <h5>{scenario.get('name', 'Unknown Scenario')}</h5>
                        <span class="scenario-probability">{scenario.get('probability', 0)}%</span>
                    </div>
                    <p class="scenario-description">{scenario.get('description', 'No description available.')}</p>
                    <div class="scenario-details">
                        <span class="detail-item">Impact: {scenario.get('impact', 'Unknown')}</span>
                        <span class="detail-item">Timeline: {scenario.get('timeline', 'Unknown')}</span>
                        <span class="detail-item">Confidence: {scenario.get('confidence', 'Unknown')}</span>
                    </div>
                    <div class="scenario-conditions">
                        <h6>Key Conditions:</h6>
                        <ul>
                        """
                conditions = scenario.get('conditions', [])
                for condition in conditions:
                    scenarios_html += f"<li>{condition}</li>"
                scenarios_html += """
                        </ul>
                    </div>
                </div>
                """
            scenarios_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="scenario-section">
            <h3>🎯 {title}</h3>
            <div class="scenario-content">
                <p>{overview}</p>
                {scenarios_html}
            </div>
        </div>
        """
    
    def _generate_trend_analysis(self, trend_data: Dict[str, Any]) -> str:
        """Generate the trend analysis section."""
        title = trend_data.get('title', 'Trend Analysis')
        overview = trend_data.get('overview', 'No trend analysis overview available.')
        trends = trend_data.get('trends', [])
        historical_data = trend_data.get('historical_data', {})
        
        trends_html = ""
        if trends:
            trends_html = """
            <div class="trend-analysis">
                <h4>📈 Key Trends</h4>
                <div class="trends-list">
            """
            for i, trend in enumerate(trends):
                trend_id = f"trend_{i}"
                trend_direction = self._get_trend_direction(trend.get('direction', 'Unknown'))
                trends_html += f"""
                <div class="trend-item {trend_direction}" data-tooltip-{self.module_id}="{trend_id}">
                    <div class="trend-header">
                        <h5>{trend.get('name', 'Unknown Trend')}</h5>
                        <span class="trend-direction">{trend.get('direction', 'Unknown')}</span>
                    </div>
                    <p class="trend-description">{trend.get('description', 'No description available.')}</p>
                    <div class="trend-metrics">
                        <span class="metric-item">Strength: {trend.get('strength', 'Unknown')}</span>
                        <span class="metric-item">Duration: {trend.get('duration', 'Unknown')}</span>
                        <span class="metric-item">Confidence: {trend.get('confidence', 'Unknown')}</span>
                    </div>
                    <div class="trend-factors">
                        <h6>Driving Factors:</h6>
                        <ul>
                        """
                factors = trend.get('factors', [])
                for factor in factors:
                    trends_html += f"<li>{factor}</li>"
                trends_html += """
                        </ul>
                    </div>
                </div>
                """
            trends_html += """
                </div>
            </div>
            """
        
        historical_html = ""
        if historical_data:
            historical_html = f"""
            <div class="historical-data">
                <h4>📊 Historical Context</h4>
                <div class="historical-summary">
                    <p><strong>Data Period:</strong> {historical_data.get('period', 'Unknown')}</p>
                    <p><strong>Data Points:</strong> {historical_data.get('data_points', 'Unknown')}</p>
                    <p><strong>Data Quality:</strong> {historical_data.get('quality', 'Unknown')}</p>
                </div>
            </div>
            """
        
        return f"""
        <div class="trend-analysis-section">
            <h3>📈 {title}</h3>
            <div class="trend-content">
                <p>{overview}</p>
                {historical_html}
                {trends_html}
            </div>
        </div>
        """
    
    def _generate_risk_assessment(self, risk_data: Dict[str, Any]) -> str:
        """Generate the risk assessment section."""
        title = risk_data.get('title', 'Risk Assessment')
        overview = risk_data.get('overview', 'No risk assessment overview available.')
        risk_factors = risk_data.get('risk_factors', [])
        uncertainty_analysis = risk_data.get('uncertainty_analysis', {})
        
        risks_html = ""
        if risk_factors:
            risks_html = """
            <div class="risk-assessment">
                <h4>⚠️ Risk Factors</h4>
                <div class="risks-grid">
            """
            for i, risk in enumerate(risk_factors):
                risk_id = f"risk_{i}"
                risk_level_color = self._get_risk_level_color(risk.get('level', 'Unknown'))
                risks_html += f"""
                <div class="risk-card {risk_level_color}" data-tooltip-{self.module_id}="{risk_id}">
                    <h5>{risk.get('name', 'Unknown Risk')}</h5>
                    <p class="risk-level">Level: {risk.get('level', 'Unknown')}</p>
                    <p class="risk-probability">Probability: {risk.get('probability', 'Unknown')}</p>
                    <p class="risk-impact">Impact: {risk.get('impact', 'Unknown')}</p>
                    <p class="risk-mitigation">Mitigation: {risk.get('mitigation', 'No mitigation plan.')}</p>
                </div>
                """
            risks_html += """
                </div>
            </div>
            """
        
        uncertainty_html = ""
        if uncertainty_analysis:
            uncertainty_html = f"""
            <div class="uncertainty-analysis">
                <h4>🎲 Uncertainty Analysis</h4>
                <div class="uncertainty-metrics">
                    <div class="uncertainty-card">
                        <h5>Model Uncertainty</h5>
                        <p class="uncertainty-value">{uncertainty_analysis.get('model_uncertainty', 'Unknown')}</p>
                    </div>
                    <div class="uncertainty-card">
                        <h5>Data Uncertainty</h5>
                        <p class="uncertainty-value">{uncertainty_analysis.get('data_uncertainty', 'Unknown')}</p>
                    </div>
                    <div class="uncertainty-card">
                        <h5>Scenario Uncertainty</h5>
                        <p class="uncertainty-value">{uncertainty_analysis.get('scenario_uncertainty', 'Unknown')}</p>
                    </div>
                </div>
            </div>
            """
        
        return f"""
        <div class="risk-assessment-section">
            <h3>⚠️ {title}</h3>
            <div class="risk-content">
                <p>{overview}</p>
                {risks_html}
                {uncertainty_html}
            </div>
        </div>
        """
    
    def _generate_interactive_visualizations(self, data: Dict[str, Any]) -> str:
        """Generate interactive visualizations section."""
        return f"""
        <div class="visualizations-section">
            <h3>📊 Interactive Visualizations</h3>
            <div class="charts-container">
                <div class="chart-container">
                    <h4>Forecast Timeline</h4>
                    {self._generate_forecast_timeline_chart(data)}
                </div>
                <div class="chart-container">
                    <h4>Scenario Comparison</h4>
                    {self._generate_scenario_comparison_chart(data)}
                </div>
                <div class="chart-container">
                    <h4>Risk Assessment Matrix</h4>
                    {self._generate_risk_matrix_chart(data)}
                </div>
            </div>
        </div>
        """
    
    def _generate_forecast_timeline_chart(self, data: Dict[str, Any]) -> str:
        """Generate forecast timeline chart."""
        # Generate sample data for demonstration
        chart_data = {
            'labels': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025'],
            'datasets': [{
                'label': 'Historical Data',
                'data': [65, 68, 72, 70, 75, 78, 82, 85],
                'backgroundColor': 'rgba(54, 162, 235, 0.6)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 2
            }, {
                'label': 'Forecast',
                'data': [None, None, None, None, 80, 85, 90, 95],
                'backgroundColor': 'rgba(255, 159, 64, 0.6)',
                'borderColor': 'rgba(255, 159, 64, 1)',
                'borderWidth': 2,
                'borderDash': [5, 5]
            }]
        }
        
        # Add chart data to module
        chart_id = f"forecastTimelineChart_{self.module_id}"
        self.chart_data[chart_id] = {
            'type': 'line',
            'data': chart_data,
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'title': {
                            'display': True,
                            'text': 'Forecast Value'
                        }
                    }
                }
            }
        }
        
        return f'<canvas id="{chart_id}"></canvas>'
    
    def _generate_scenario_comparison_chart(self, data: Dict[str, Any]) -> str:
        """Generate scenario comparison chart."""
        # Generate sample data for demonstration
        chart_data = {
            'labels': ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025'],
            'datasets': [{
                'label': 'Optimistic Scenario',
                'data': [85, 90, 95, 100],
                'backgroundColor': 'rgba(75, 192, 192, 0.6)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 2
            }, {
                'label': 'Baseline Scenario',
                'data': [80, 85, 90, 95],
                'backgroundColor': 'rgba(255, 205, 86, 0.6)',
                'borderColor': 'rgba(255, 205, 86, 1)',
                'borderWidth': 2
            }, {
                'label': 'Pessimistic Scenario',
                'data': [75, 80, 85, 90],
                'backgroundColor': 'rgba(255, 99, 132, 0.6)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 2
            }]
        }
        
        # Add chart data to module
        chart_id = f"scenarioComparisonChart_{self.module_id}"
        self.chart_data[chart_id] = {
            'type': 'line',
            'data': chart_data,
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'title': {
                            'display': True,
                            'text': 'Scenario Value'
                        }
                    }
                }
            }
        }
        
        return f'<canvas id="{chart_id}"></canvas>'
    
    def _generate_risk_matrix_chart(self, data: Dict[str, Any]) -> str:
        """Generate risk assessment matrix chart."""
        # Generate sample data for demonstration
        chart_data = {
            'labels': ['Low Impact', 'Medium Impact', 'High Impact', 'Critical Impact'],
            'datasets': [{
                'label': 'Low Probability',
                'data': [5, 8, 12, 15],
                'backgroundColor': 'rgba(75, 192, 192, 0.8)'
            }, {
                'label': 'Medium Probability',
                'data': [10, 15, 20, 25],
                'backgroundColor': 'rgba(255, 205, 86, 0.8)'
            }, {
                'label': 'High Probability',
                'data': [15, 22, 28, 35],
                'backgroundColor': 'rgba(255, 99, 132, 0.8)'
            }]
        }
        
        # Add chart data to module
        chart_id = f"riskMatrixChart_{self.module_id}"
        self.chart_data[chart_id] = {
            'type': 'bar',
            'data': chart_data,
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'title': {
                            'display': True,
                            'text': 'Risk Score'
                        }
                    }
                }
            }
        }
        
        return f'<canvas id="{chart_id}"></canvas>'
    
    def _get_probability_color(self, probability: float) -> str:
        """Get CSS class for probability color."""
        if probability >= 70:
            return 'probability-high'
        elif probability >= 40:
            return 'probability-medium'
        else:
            return 'probability-low'
    
    def _get_trend_direction(self, direction: str) -> str:
        """Get CSS class for trend direction."""
        direction_lower = direction.lower()
        if direction_lower in ['up', 'increasing', 'positive']:
            return 'trend-up'
        elif direction_lower in ['down', 'decreasing', 'negative']:
            return 'trend-down'
        else:
            return 'trend-stable'
    
    def _get_risk_level_color(self, level: str) -> str:
        """Get CSS class for risk level color."""
        level_lower = level.lower()
        if level_lower == 'low':
            return 'risk-low'
        elif level_lower == 'medium':
            return 'risk-medium'
        elif level_lower == 'high':
            return 'risk-high'
        elif level_lower == 'critical':
            return 'risk-critical'
        else:
            return 'risk-unknown'
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltips for the module."""
        self.tooltip_data = {
            'metric_0': TooltipData(
                title="Forecasting Metrics Analysis",
                description="Comprehensive analysis of key forecasting metrics and their implications for strategic planning.",
                source="Forecasting data and trend analysis",
                strategic_impact="High - Direct impact on strategic decision-making and resource allocation",
                recommendations=[
                    "Monitor key metrics continuously",
                    "Update forecasts based on new data",
                    "Adjust strategies based on trend changes"
                ],
                use_cases=[
                    "Strategic planning",
                    "Resource allocation",
                    "Risk management"
                ]
            ),
            'scenario_0': TooltipData(
                title="Scenario Analysis Assessment",
                description="Analysis of multiple future scenarios and their probability of occurrence.",
                source="Scenario planning and probability modeling",
                strategic_impact="Critical - Scenario analysis drives strategic preparedness",
                recommendations=[
                    "Develop contingency plans for each scenario",
                    "Monitor scenario indicators",
                    "Prepare for multiple outcomes"
                ],
                use_cases=[
                    "Contingency planning",
                    "Strategic preparedness",
                    "Risk mitigation"
                ]
            ),
            'trend_0': TooltipData(
                title="Trend Analysis Assessment",
                description="Analysis of historical trends and their implications for future developments.",
                source="Historical data analysis and pattern recognition",
                strategic_impact="Medium-High - Trend analysis informs strategic direction",
                recommendations=[
                    "Identify emerging trends early",
                    "Assess trend sustainability",
                    "Plan for trend continuation or reversal"
                ],
                use_cases=[
                    "Strategic direction",
                    "Market analysis",
                    "Competitive intelligence"
                ]
            ),
            'risk_0': TooltipData(
                title="Risk Assessment Analysis",
                description="Comprehensive assessment of risks and uncertainties affecting forecasts.",
                source="Risk analysis and uncertainty quantification",
                strategic_impact="High - Risk assessment is critical for robust planning",
                recommendations=[
                    "Develop comprehensive mitigation strategies",
                    "Establish early warning indicators",
                    "Create contingency plans"
                ],
                use_cases=[
                    "Risk management",
                    "Contingency planning",
                    "Strategic resilience"
                ]
            )
        }
