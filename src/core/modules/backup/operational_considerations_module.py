"""
Operational Considerations Module

Independent module for generating operational considerations and readiness assessment sections that can be added to any report.
Provides operational planning, readiness analysis, implementation considerations, and risk assessment capabilities.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


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
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Operational Considerations module."""
        self.validate_data(data)
        
        operational_overview = data.get('operational_overview', {})
        readiness_analysis = data.get('readiness_analysis', {})
        implementation_planning = data.get('implementation_planning', {})
        operational_risk_assessment = data.get('operational_risk_assessment', {})
        
        # Generate operational overview
        overview_html = self._generate_operational_overview(operational_overview)
        
        # Generate readiness analysis
        readiness_html = self._generate_readiness_analysis(readiness_analysis)
        
        # Generate implementation planning
        implementation_html = self._generate_implementation_planning(implementation_planning)
        
        # Generate operational risk assessment
        risk_html = self._generate_operational_risk_assessment(operational_risk_assessment)
        
        # Generate interactive visualizations
        visualizations_html = self._generate_interactive_visualizations(data)
        
        return f"""
        <div class="section" id="operational-considerations">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {readiness_html}
            {implementation_html}
            {risk_html}
            {visualizations_html}
        </div>
        """
    
    def _generate_operational_overview(self, overview_data: Dict[str, Any]) -> str:
        """Generate the operational overview section."""
        title = overview_data.get('title', 'Operational Overview')
        overview = overview_data.get('overview', 'No operational overview available.')
        operational_factors = overview_data.get('operational_factors', [])
        readiness_summary = overview_data.get('readiness_summary', {})
        implementation_considerations = overview_data.get('implementation_considerations', [])
        
        factors_html = ""
        if operational_factors:
            factors_html = """
            <div class="operational-factors">
                <h4>🎯 Key Operational Factors</h4>
                <div class="factors-grid">
            """
            for i, factor in enumerate(operational_factors):
                factor_id = f"factor_{i}"
                factors_html += f"""
                <div class="factor-card" data-tooltip-{self.module_id}="{factor_id}">
                    <h5>{factor.get('name', 'Unknown Factor')}</h5>
                    <p class="factor-description">{factor.get('description', 'No description available.')}</p>
                    <p class="factor-impact">Impact: {factor.get('impact', 'Unknown')}</p>
                    <p class="factor-priority">Priority: {factor.get('priority', 'Unknown')}</p>
                </div>
                """
            factors_html += """
                </div>
            </div>
            """
        
        readiness_html = ""
        if readiness_summary:
            readiness_html = f"""
            <div class="readiness-summary">
                <h4>📊 Overall Readiness Assessment</h4>
                <div class="readiness-metrics">
                    <div class="readiness-metric">
                        <h5>Personnel Readiness</h5>
                        <p class="metric-value">{readiness_summary.get('personnel_readiness', 'Unknown')}</p>
                    </div>
                    <div class="readiness-metric">
                        <h5>Equipment Readiness</h5>
                        <p class="metric-value">{readiness_summary.get('equipment_readiness', 'Unknown')}</p>
                    </div>
                    <div class="readiness-metric">
                        <h5>Training Readiness</h5>
                        <p class="metric-value">{readiness_summary.get('training_readiness', 'Unknown')}</p>
                    </div>
                    <div class="readiness-metric">
                        <h5>Overall Readiness</h5>
                        <p class="metric-value">{readiness_summary.get('overall_readiness', 'Unknown')}</p>
                    </div>
                </div>
            </div>
            """
        
        considerations_html = ""
        if implementation_considerations:
            considerations_html = """
            <div class="implementation-considerations">
                <h4>⚙️ Implementation Considerations</h4>
                <ul class="considerations-list">
            """
            for consideration in implementation_considerations:
                considerations_html += f"<li>{consideration}</li>"
            considerations_html += """
                </ul>
            </div>
            """
        
        return f"""
        <div class="operational-overview-section">
            <h3>⚡ {title}</h3>
            <div class="overview-content">
                <p>{overview}</p>
                {factors_html}
                {readiness_html}
                {considerations_html}
            </div>
        </div>
        """
    
    def _generate_readiness_analysis(self, readiness_data: Dict[str, Any]) -> str:
        """Generate the readiness analysis section."""
        title = readiness_data.get('title', 'Readiness Analysis')
        overview = readiness_data.get('overview', 'No readiness analysis overview available.')
        personnel_readiness = readiness_data.get('personnel_readiness', {})
        equipment_readiness = readiness_data.get('equipment_readiness', {})
        training_readiness = readiness_data.get('training_readiness', {})
        
        personnel_html = ""
        if personnel_readiness:
            personnel_html = f"""
            <div class="personnel-readiness">
                <h4>👥 Personnel Readiness</h4>
                <div class="readiness-details">
                    <p><strong>Total Personnel:</strong> {personnel_readiness.get('total_personnel', 'Unknown')}</p>
                    <p><strong>Available Personnel:</strong> {personnel_readiness.get('available_personnel', 'Unknown')}</p>
                    <p><strong>Qualified Personnel:</strong> {personnel_readiness.get('qualified_personnel', 'Unknown')}</p>
                    <p><strong>Readiness Rate:</strong> {personnel_readiness.get('readiness_rate', 'Unknown')}</p>
                    <p><strong>Key Gaps:</strong> {personnel_readiness.get('key_gaps', 'None identified')}</p>
                </div>
            </div>
            """
        
        equipment_html = ""
        if equipment_readiness:
            equipment_html = f"""
            <div class="equipment-readiness">
                <h4>🔧 Equipment Readiness</h4>
                <div class="readiness-details">
                    <p><strong>Total Equipment:</strong> {equipment_readiness.get('total_equipment', 'Unknown')}</p>
                    <p><strong>Operational Equipment:</strong> {equipment_readiness.get('operational_equipment', 'Unknown')}</p>
                    <p><strong>Maintenance Status:</strong> {equipment_readiness.get('maintenance_status', 'Unknown')}</p>
                    <p><strong>Readiness Rate:</strong> {equipment_readiness.get('readiness_rate', 'Unknown')}</p>
                    <p><strong>Critical Shortages:</strong> {equipment_readiness.get('critical_shortages', 'None identified')}</p>
                </div>
            </div>
            """
        
        training_html = ""
        if training_readiness:
            training_html = f"""
            <div class="training-readiness">
                <h4>🎓 Training Readiness</h4>
                <div class="readiness-details">
                    <p><strong>Training Completion:</strong> {training_readiness.get('training_completion', 'Unknown')}</p>
                    <p><strong>Certification Status:</strong> {training_readiness.get('certification_status', 'Unknown')}</p>
                    <p><strong>Recent Training:</strong> {training_readiness.get('recent_training', 'Unknown')}</p>
                    <p><strong>Readiness Rate:</strong> {training_readiness.get('readiness_rate', 'Unknown')}</p>
                    <p><strong>Training Gaps:</strong> {training_readiness.get('training_gaps', 'None identified')}</p>
                </div>
            </div>
            """
        
        return f"""
        <div class="readiness-analysis-section">
            <h3>📊 {title}</h3>
            <div class="readiness-content">
                <p>{overview}</p>
                {personnel_html}
                {equipment_html}
                {training_html}
            </div>
        </div>
        """
    
    def _generate_implementation_planning(self, planning_data: Dict[str, Any]) -> str:
        """Generate the implementation planning section."""
        title = planning_data.get('title', 'Implementation Planning')
        overview = planning_data.get('overview', 'No implementation planning overview available.')
        operational_phases = planning_data.get('operational_phases', [])
        resource_requirements = planning_data.get('resource_requirements', {})
        timeline_considerations = planning_data.get('timeline_considerations', [])
        
        phases_html = ""
        if operational_phases:
            phases_html = """
            <div class="operational-phases">
                <h4>📅 Operational Phases</h4>
                <div class="phases-timeline">
            """
            for i, phase in enumerate(operational_phases):
                phase_id = f"phase_{i}"
                phases_html += f"""
                <div class="phase-item" data-tooltip-{self.module_id}="{phase_id}">
                    <div class="phase-header">
                        <h5>Phase {i + 1}: {phase.get('name', 'Unknown Phase')}</h5>
                        <span class="phase-duration">{phase.get('duration', 'Unknown')}</span>
                    </div>
                    <p class="phase-description">{phase.get('description', 'No description available.')}</p>
                    <div class="phase-objectives">
                        <h6>Objectives:</h6>
                        <ul>
                        """
                objectives = phase.get('objectives', [])
                for objective in objectives:
                    phases_html += f"<li>{objective}</li>"
                phases_html += """
                        </ul>
                    </div>
                    <div class="phase-resources">
                        <h6>Resources Required:</h6>
                        <ul>
                        """
                resources = phase.get('resources', [])
                for resource in resources:
                    phases_html += f"<li>{resource}</li>"
                phases_html += """
                        </ul>
                    </div>
                </div>
                """
            phases_html += """
                </div>
            </div>
            """
        
        resources_html = ""
        if resource_requirements:
            resources_html = f"""
            <div class="resource-requirements">
                <h4>💰 Resource Requirements</h4>
                <div class="resources-grid">
                    <div class="resource-category">
                        <h5>Personnel</h5>
                        <p class="resource-value">{resource_requirements.get('personnel', 'Unknown')}</p>
                    </div>
                    <div class="resource-category">
                        <h5>Equipment</h5>
                        <p class="resource-value">{resource_requirements.get('equipment', 'Unknown')}</p>
                    </div>
                    <div class="resource-category">
                        <h5>Budget</h5>
                        <p class="resource-value">{resource_requirements.get('budget', 'Unknown')}</p>
                    </div>
                    <div class="resource-category">
                        <h5>Time</h5>
                        <p class="resource-value">{resource_requirements.get('time', 'Unknown')}</p>
                    </div>
                </div>
            </div>
            """
        
        timeline_html = ""
        if timeline_considerations:
            timeline_html = """
            <div class="timeline-considerations">
                <h4>⏰ Timeline Considerations</h4>
                <ul class="timeline-list">
            """
            for consideration in timeline_considerations:
                timeline_html += f"<li>{consideration}</li>"
            timeline_html += """
                </ul>
            </div>
            """
        
        return f"""
        <div class="implementation-planning-section">
            <h3>📋 {title}</h3>
            <div class="planning-content">
                <p>{overview}</p>
                {phases_html}
                {resources_html}
                {timeline_html}
            </div>
        </div>
        """
    
    def _generate_operational_risk_assessment(self, risk_data: Dict[str, Any]) -> str:
        """Generate the operational risk assessment section."""
        title = risk_data.get('title', 'Operational Risk Assessment')
        overview = risk_data.get('overview', 'No operational risk assessment overview available.')
        operational_risks = risk_data.get('operational_risks', [])
        mitigation_strategies = risk_data.get('mitigation_strategies', [])
        contingency_plans = risk_data.get('contingency_plans', [])
        
        risks_html = ""
        if operational_risks:
            risks_html = """
            <div class="operational-risks">
                <h4>⚠️ Operational Risks</h4>
                <div class="risks-grid">
            """
            for i, risk in enumerate(operational_risks):
                risk_id = f"risk_{i}"
                risk_level_color = self._get_risk_level_color(risk.get('level', 'Unknown'))
                risks_html += f"""
                <div class="risk-card {risk_level_color}" data-tooltip-{self.module_id}="{risk_id}">
                    <h5>{risk.get('name', 'Unknown Risk')}</h5>
                    <p class="risk-level">Level: {risk.get('level', 'Unknown')}</p>
                    <p class="risk-probability">Probability: {risk.get('probability', 'Unknown')}</p>
                    <p class="risk-impact">Impact: {risk.get('impact', 'Unknown')}</p>
                    <p class="risk-description">{risk.get('description', 'No description available.')}</p>
                </div>
                """
            risks_html += """
                </div>
            </div>
            """
        
        mitigation_html = ""
        if mitigation_strategies:
            mitigation_html = """
            <div class="mitigation-strategies">
                <h4>🛡️ Mitigation Strategies</h4>
                <div class="strategies-list">
            """
            for i, strategy in enumerate(mitigation_strategies):
                strategy_id = f"strategy_{i}"
                mitigation_html += f"""
                <div class="strategy-item" data-tooltip-{self.module_id}="{strategy_id}">
                    <h5>{strategy.get('name', 'Unknown Strategy')}</h5>
                    <p class="strategy-description">{strategy.get('description', 'No description available.')}</p>
                    <p class="strategy-effectiveness">Effectiveness: {strategy.get('effectiveness', 'Unknown')}</p>
                    <p class="strategy-cost">Cost: {strategy.get('cost', 'Unknown')}</p>
                </div>
                """
            mitigation_html += """
                </div>
            </div>
            """
        
        contingency_html = ""
        if contingency_plans:
            contingency_html = """
            <div class="contingency-plans">
                <h4>🔄 Contingency Plans</h4>
                <div class="plans-list">
            """
            for i, plan in enumerate(contingency_plans):
                plan_id = f"plan_{i}"
                contingency_html += f"""
                <div class="plan-item" data-tooltip-{self.module_id}="{plan_id}">
                    <h5>{plan.get('name', 'Unknown Plan')}</h5>
                    <p class="plan-description">{plan.get('description', 'No description available.')}</p>
                    <p class="plan-trigger">Trigger: {plan.get('trigger', 'Unknown')}</p>
                    <p class="plan-resources">Resources: {plan.get('resources', 'Unknown')}</p>
                </div>
                """
            contingency_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="operational-risk-assessment-section">
            <h3>⚠️ {title}</h3>
            <div class="risk-content">
                <p>{overview}</p>
                {risks_html}
                {mitigation_html}
                {contingency_html}
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
                    <h4>Readiness Assessment</h4>
                    {self._generate_readiness_assessment_chart(data)}
                </div>
                <div class="chart-container">
                    <h4>Implementation Timeline</h4>
                    {self._generate_implementation_timeline_chart(data)}
                </div>
                <div class="chart-container">
                    <h4>Operational Risk Matrix</h4>
                    {self._generate_operational_risk_matrix_chart(data)}
                </div>
            </div>
        </div>
        """
    
    def _generate_readiness_assessment_chart(self, data: Dict[str, Any]) -> str:
        """Generate readiness assessment chart."""
        # Generate sample data for demonstration
        chart_data = {
            'labels': ['Personnel', 'Equipment', 'Training', 'Overall'],
            'datasets': [{
                'label': 'Current Readiness',
                'data': [85, 78, 92, 82],
                'backgroundColor': 'rgba(54, 162, 235, 0.6)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 2
            }, {
                'label': 'Target Readiness',
                'data': [95, 90, 95, 93],
                'backgroundColor': 'rgba(75, 192, 192, 0.6)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 2
            }]
        }
        
        # Add chart data to module
        chart_id = f"readinessAssessmentChart_{self.module_id}"
        self.chart_data[chart_id] = {
            'type': 'bar',
            'data': chart_data,
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'max': 100,
                        'title': {
                            'display': True,
                            'text': 'Readiness Percentage'
                        }
                    }
                }
            }
        }
        
        return f'<canvas id="{chart_id}"></canvas>'
    
    def _generate_implementation_timeline_chart(self, data: Dict[str, Any]) -> str:
        """Generate implementation timeline chart."""
        # Generate sample data for demonstration
        chart_data = {
            'labels': ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4', 'Phase 5'],
            'datasets': [{
                'label': 'Planned Duration',
                'data': [30, 45, 60, 30, 15],
                'backgroundColor': 'rgba(255, 159, 64, 0.6)',
                'borderColor': 'rgba(255, 159, 64, 1)',
                'borderWidth': 2
            }, {
                'label': 'Actual Duration',
                'data': [28, 42, 58, 32, 12],
                'backgroundColor': 'rgba(255, 99, 132, 0.6)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 2
            }]
        }
        
        # Add chart data to module
        chart_id = f"implementationTimelineChart_{self.module_id}"
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
                            'text': 'Duration (Days)'
                        }
                    }
                }
            }
        }
        
        return f'<canvas id="{chart_id}"></canvas>'
    
    def _generate_operational_risk_matrix_chart(self, data: Dict[str, Any]) -> str:
        """Generate operational risk matrix chart."""
        # Generate sample data for demonstration
        chart_data = {
            'labels': ['Low Impact', 'Medium Impact', 'High Impact', 'Critical Impact'],
            'datasets': [{
                'label': 'Low Probability',
                'data': [3, 5, 8, 12],
                'backgroundColor': 'rgba(75, 192, 192, 0.8)'
            }, {
                'label': 'Medium Probability',
                'data': [8, 12, 18, 25],
                'backgroundColor': 'rgba(255, 205, 86, 0.8)'
            }, {
                'label': 'High Probability',
                'data': [15, 22, 30, 40],
                'backgroundColor': 'rgba(255, 99, 132, 0.8)'
            }]
        }
        
        # Add chart data to module
        chart_id = f"operationalRiskMatrixChart_{self.module_id}"
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
            'factor_0': TooltipData(
                title="Operational Factors Analysis",
                description="Comprehensive analysis of key operational factors affecting mission success and readiness.",
                source="Operational planning and readiness assessment data",
                strategic_impact="High - Direct impact on operational success and mission effectiveness",
                recommendations=[
                    "Prioritize critical operational factors",
                    "Address readiness gaps systematically",
                    "Develop contingency plans for high-impact factors"
                ],
                use_cases=[
                    "Operational planning",
                    "Readiness assessment",
                    "Resource allocation"
                ]
            ),
            'phase_0': TooltipData(
                title="Implementation Phase Analysis",
                description="Detailed analysis of operational implementation phases and their requirements.",
                source="Implementation planning and timeline analysis",
                strategic_impact="Critical - Implementation phases determine operational success",
                recommendations=[
                    "Ensure adequate resources for each phase",
                    "Develop phase-specific contingency plans",
                    "Monitor phase progress continuously"
                ],
                use_cases=[
                    "Implementation planning",
                    "Timeline management",
                    "Resource planning"
                ]
            ),
            'risk_0': TooltipData(
                title="Operational Risk Assessment",
                description="Comprehensive assessment of operational risks and their potential impact on mission success.",
                source="Risk analysis and operational assessment",
                strategic_impact="High - Risk assessment is critical for operational planning",
                recommendations=[
                    "Develop comprehensive mitigation strategies",
                    "Establish early warning indicators",
                    "Create contingency plans for high-risk scenarios"
                ],
                use_cases=[
                    "Risk management",
                    "Contingency planning",
                    "Operational resilience"
                ]
            ),
            'strategy_0': TooltipData(
                title="Mitigation Strategy Analysis",
                description="Analysis of mitigation strategies and their effectiveness in reducing operational risks.",
                source="Risk mitigation planning and strategy development",
                strategic_impact="Medium-High - Mitigation strategies improve operational resilience",
                recommendations=[
                    "Prioritize high-effectiveness strategies",
                    "Balance cost and effectiveness",
                    "Monitor strategy implementation"
                ],
                use_cases=[
                    "Risk mitigation",
                    "Strategy development",
                    "Resource optimization"
                ]
            )
        }
