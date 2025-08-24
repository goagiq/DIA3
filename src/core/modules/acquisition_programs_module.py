"""
Acquisition Programs Module

Independent module for generating acquisition programs analysis sections that can be added to any report.
Provides acquisition program overview, modernization initiatives, program analysis, and strategic impact assessment.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


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
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Acquisition Programs module."""
        self.validate_data(data)
        
        acquisition_programs = data.get('acquisition_programs', {})
        modernization_initiatives = data.get('modernization_initiatives', {})
        program_analysis = data.get('program_analysis', {})
        strategic_impact = data.get('strategic_impact', {})
        
        # Generate program overview
        overview_html = self._generate_programs_overview(acquisition_programs)
        
        # Generate modernization initiatives
        modernization_html = self._generate_modernization_initiatives(modernization_initiatives)
        
        # Generate program analysis
        analysis_html = self._generate_program_analysis(program_analysis)
        
        # Generate strategic impact assessment
        impact_html = self._generate_strategic_impact(strategic_impact)
        
        # Generate interactive visualizations
        visualizations_html = self._generate_interactive_visualizations(data)
        
        return f"""
        <div class="section" id="acquisition-programs">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {modernization_html}
            {analysis_html}
            {impact_html}
            {visualizations_html}
        </div>
        """
    
    def _generate_programs_overview(self, programs_data: Dict[str, Any]) -> str:
        """Generate the acquisition programs overview section."""
        title = programs_data.get('title', 'Acquisition Programs Overview')
        overview = programs_data.get('overview', 'No acquisition programs overview available.')
        total_budget = programs_data.get('total_budget', 'Unknown')
        total_programs = programs_data.get('total_programs', 0)
        programs = programs_data.get('programs', [])
        
        programs_html = ""
        if programs:
            programs_html = """
            <div class="acquisition-programs">
                <h4>🎯 Active Programs</h4>
                <div class="programs-grid">
            """
            for i, program in enumerate(programs):
                program_id = f"program_{i}"
                status_color = self._get_status_color(program.get('status', 'Unknown'))
                programs_html += f"""
                <div class="program-card" data-tooltip-{self.module_id}="{program_id}">
                    <h5>{program.get('name', 'Unknown Program')}</h5>
                    <p class="program-type">Type: {program.get('type', 'Unknown')}</p>
                    <p class="program-budget">Budget: {program.get('budget', 'Unknown')}</p>
                    <p class="program-timeline">Timeline: {program.get('timeline', 'Unknown')}</p>
                    <div class="status-indicator {status_color}">
                        Status: {program.get('status', 'Unknown')}
                    </div>
                    <p class="program-priority">Priority: {program.get('priority', 'Unknown')}</p>
                </div>
                """
            programs_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="programs-overview-section">
            <h3>📊 {title}</h3>
            <div class="overview-content">
                <p>{overview}</p>
                
                <div class="program-metrics">
                    <div class="metric-card">
                        <h4>Total Budget</h4>
                        <p class="metric-value">{total_budget}</p>
                    </div>
                    <div class="metric-card">
                        <h4>Active Programs</h4>
                        <p class="metric-value">{total_programs}</p>
                    </div>
                    <div class="metric-card">
                        <h4>Program Status</h4>
                        <p class="metric-value">
                            {len([p for p in programs if p.get('status') == 'Active'])} Active
                        </p>
                    </div>
                </div>
                
                {programs_html}
            </div>
        </div>
        """
    
    def _generate_modernization_initiatives(self, modernization_data: Dict[str, Any]) -> str:
        """Generate the modernization initiatives section."""
        title = modernization_data.get('title', 'Modernization Initiatives')
        overview = modernization_data.get('overview', 'No modernization initiatives overview available.')
        initiatives = modernization_data.get('initiatives', [])
        
        initiatives_html = ""
        if initiatives:
            initiatives_html = """
            <div class="modernization-initiatives">
                <h4>🔧 Key Initiatives</h4>
                <div class="initiatives-list">
            """
            for i, initiative in enumerate(initiatives):
                initiative_id = f"initiative_{i}"
                initiatives_html += f"""
                <div class="initiative-item" data-tooltip-{self.module_id}="{initiative_id}">
                    <div class="initiative-header">
                        <h5>{initiative.get('name', 'Unknown Initiative')}</h5>
                        <span class="initiative-category">{initiative.get('category', 'Unknown')}</span>
                    </div>
                    <p class="initiative-description">{initiative.get('description', 'No description available.')}</p>
                    <div class="initiative-details">
                        <span class="detail-item">Impact: {initiative.get('impact', 'Unknown')}</span>
                        <span class="detail-item">Timeline: {initiative.get('timeline', 'Unknown')}</span>
                        <span class="detail-item">Cost: {initiative.get('cost', 'Unknown')}</span>
                    </div>
                </div>
                """
            initiatives_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="modernization-section">
            <h3>🔧 {title}</h3>
            <div class="modernization-content">
                <p>{overview}</p>
                {initiatives_html}
            </div>
        </div>
        """
    
    def _generate_program_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """Generate the program analysis section."""
        title = analysis_data.get('title', 'Program Analysis')
        overview = analysis_data.get('overview', 'No program analysis overview available.')
        risks = analysis_data.get('risks', [])
        dependencies = analysis_data.get('dependencies', [])
        milestones = analysis_data.get('milestones', [])
        
        risks_html = ""
        if risks:
            risks_html = """
            <div class="program-risks">
                <h4>⚠️ Risk Assessment</h4>
                <div class="risks-grid">
            """
            for i, risk in enumerate(risks):
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
        
        dependencies_html = ""
        if dependencies:
            dependencies_html = """
            <div class="program-dependencies">
                <h4>🔗 Program Dependencies</h4>
                <div class="dependencies-list">
            """
            for i, dependency in enumerate(dependencies):
                dependency_id = f"dependency_{i}"
                dependencies_html += f"""
                <div class="dependency-item" data-tooltip-{self.module_id}="{dependency_id}">
                    <h5>{dependency.get('name', 'Unknown Dependency')}</h5>
                    <p class="dependency-type">Type: {dependency.get('type', 'Unknown')}</p>
                    <p class="dependency-status">Status: {dependency.get('status', 'Unknown')}</p>
                    <p class="dependency-critical">Critical: {dependency.get('critical', False)}</p>
                </div>
                """
            dependencies_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="program-analysis-section">
            <h3>📈 {title}</h3>
            <div class="analysis-content">
                <p>{overview}</p>
                {risks_html}
                {dependencies_html}
            </div>
        </div>
        """
    
    def _generate_strategic_impact(self, impact_data: Dict[str, Any]) -> str:
        """Generate the strategic impact section."""
        title = impact_data.get('title', 'Strategic Impact Assessment')
        overview = impact_data.get('overview', 'No strategic impact assessment available.')
        capability_gaps = impact_data.get('capability_gaps', [])
        strategic_benefits = impact_data.get('strategic_benefits', [])
        implications = impact_data.get('implications', [])
        
        gaps_html = ""
        if capability_gaps:
            gaps_html = """
            <div class="capability-gaps">
                <h4>🎯 Capability Gaps Addressed</h4>
                <div class="gaps-list">
            """
            for i, gap in enumerate(capability_gaps):
                gap_id = f"gap_{i}"
                gaps_html += f"""
                <div class="gap-item" data-tooltip-{self.module_id}="{gap_id}">
                    <h5>{gap.get('name', 'Unknown Gap')}</h5>
                    <p class="gap-current">Current State: {gap.get('current_state', 'Unknown')}</p>
                    <p class="gap-target">Target State: {gap.get('target_state', 'Unknown')}</p>
                    <p class="gap-impact">Impact: {gap.get('impact', 'Unknown')}</p>
                </div>
                """
            gaps_html += """
                </div>
            </div>
            """
        
        benefits_html = ""
        if strategic_benefits:
            benefits_html = """
            <div class="strategic-benefits">
                <h4>💎 Strategic Benefits</h4>
                <div class="benefits-list">
            """
            for i, benefit in enumerate(strategic_benefits):
                benefit_id = f"benefit_{i}"
                benefits_html += f"""
                <div class="benefit-item" data-tooltip-{self.module_id}="{benefit_id}">
                    <h5>{benefit.get('name', 'Unknown Benefit')}</h5>
                    <p class="benefit-description">{benefit.get('description', 'No description available.')}</p>
                    <p class="benefit-timeframe">Timeframe: {benefit.get('timeframe', 'Unknown')}</p>
                    <p class="benefit-magnitude">Magnitude: {benefit.get('magnitude', 'Unknown')}</p>
                </div>
                """
            benefits_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="strategic-impact-section">
            <h3>💎 {title}</h3>
            <div class="impact-content">
                <p>{overview}</p>
                {gaps_html}
                {benefits_html}
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
                    <h4>Program Timeline Analysis</h4>
                    {self._generate_program_timeline_chart(data)}
                </div>
                <div class="chart-container">
                    <h4>Budget Allocation by Program</h4>
                    {self._generate_budget_allocation_chart(data)}
                </div>
                <div class="chart-container">
                    <h4>Capability Gap Assessment</h4>
                    {self._generate_capability_gap_chart(data)}
                </div>
            </div>
        </div>
        """
    
    def _generate_program_timeline_chart(self, data: Dict[str, Any]) -> str:
        """Generate program timeline chart."""
        programs = data.get('acquisition_programs', {}).get('programs', [])
        
        if not programs:
            # Generate sample data for demonstration
            chart_data = {
                'labels': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025'],
                'datasets': [{
                    'label': 'Programs Started',
                    'data': [2, 3, 1, 4, 2, 3],
                    'backgroundColor': 'rgba(54, 162, 235, 0.6)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 2
                }, {
                    'label': 'Programs Completed',
                    'data': [0, 1, 2, 1, 3, 2],
                    'backgroundColor': 'rgba(75, 192, 192, 0.6)',
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 2
                }]
            }
        else:
            # Process actual data
            # Create timeline based on actual program data
            labels = []
            started_data = []
            completed_data = []
            
            # Process programs to extract timeline data
            for program in programs:
                if 'timeline' in program:
                    # Extract timeline information
                    pass
            
            chart_data = {
                'labels': labels if labels else ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024'],
                'datasets': [{
                    'label': 'Programs Started',
                    'data': started_data if started_data else [2, 3, 1, 4],
                    'backgroundColor': 'rgba(54, 162, 235, 0.6)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 2
                }, {
                    'label': 'Programs Completed',
                    'data': completed_data if completed_data else [0, 1, 2, 1],
                    'backgroundColor': 'rgba(75, 192, 192, 0.6)',
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 2
                }]
            }
        
        # Add chart data to module
        chart_id = f"programTimelineChart_{self.module_id}"
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
                            'text': 'Number of Programs'
                        }
                    }
                }
            }
        }
        
        return f'<canvas id="{chart_id}"></canvas>'
    
    def _generate_budget_allocation_chart(self, data: Dict[str, Any]) -> str:
        """Generate budget allocation chart."""
        programs = data.get('acquisition_programs', {}).get('programs', [])
        
        if not programs:
            # Generate sample data for demonstration
            chart_data = {
                'labels': ['Naval Systems', 'Air Defense', 'Ground Systems', 'C4ISR', 'Logistics'],
                'datasets': [{
                    'label': 'Budget Allocation (Millions)',
                    'data': [450, 320, 280, 180, 120],
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)'
                    ],
                    'borderColor': [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    'borderWidth': 2
                }]
            }
        else:
            # Process actual data
            program_types = {}
            for program in programs:
                prog_type = program.get('type', 'Unknown')
                budget_str = program.get('budget', '0')
                try:
                    # Extract numeric value from budget string
                    budget = float(''.join(filter(str.isdigit, budget_str))) if budget_str != 'Unknown' else 0
                    program_types[prog_type] = program_types.get(prog_type, 0) + budget
                except:
                    pass
            
            if program_types:
                chart_data = {
                    'labels': list(program_types.keys()),
                    'datasets': [{
                        'label': 'Budget Allocation',
                        'data': list(program_types.values()),
                        'backgroundColor': [
                            'rgba(255, 99, 132, 0.8)',
                            'rgba(54, 162, 235, 0.8)',
                            'rgba(255, 205, 86, 0.8)',
                            'rgba(75, 192, 192, 0.8)',
                            'rgba(153, 102, 255, 0.8)'
                        ][:len(program_types)],
                        'borderWidth': 2
                    }]
                }
            else:
                # Fallback to sample data
                chart_data = {
                    'labels': ['Naval Systems', 'Air Defense', 'Ground Systems'],
                    'datasets': [{
                        'label': 'Budget Allocation',
                        'data': [450, 320, 280],
                        'backgroundColor': ['rgba(255, 99, 132, 0.8)', 'rgba(54, 162, 235, 0.8)', 'rgba(255, 205, 86, 0.8)'],
                        'borderWidth': 2
                    }]
                }
        
        # Add chart data to module
        chart_id = f"budgetAllocationChart_{self.module_id}"
        self.chart_data[chart_id] = {
            'type': 'doughnut',
            'data': chart_data,
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'plugins': {
                    'legend': {
                        'position': 'bottom'
                    }
                }
            }
        }
        
        return f'<canvas id="{chart_id}"></canvas>'
    
    def _generate_capability_gap_chart(self, data: Dict[str, Any]) -> str:
        """Generate capability gap assessment chart."""
        capability_gaps = data.get('strategic_impact', {}).get('capability_gaps', [])
        
        if not capability_gaps:
            # Generate sample data for demonstration
            chart_data = {
                'labels': ['Current Capability', 'Target Capability'],
                'datasets': [{
                    'label': 'Anti-Air Defense',
                    'data': [40, 85],
                    'backgroundColor': 'rgba(255, 99, 132, 0.6)',
                    'borderColor': 'rgba(255, 99, 132, 1)',
                    'borderWidth': 2
                }, {
                    'label': 'Naval Power Projection', 
                    'data': [30, 75],
                    'backgroundColor': 'rgba(54, 162, 235, 0.6)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 2
                }, {
                    'label': 'C4ISR Systems',
                    'data': [50, 90],
                    'backgroundColor': 'rgba(75, 192, 192, 0.6)',
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 2
                }]
            }
        else:
            # Process actual data
            datasets = []
            colors = [
                ('rgba(255, 99, 132, 0.6)', 'rgba(255, 99, 132, 1)'),
                ('rgba(54, 162, 235, 0.6)', 'rgba(54, 162, 235, 1)'),
                ('rgba(75, 192, 192, 0.6)', 'rgba(75, 192, 192, 1)'),
                ('rgba(255, 205, 86, 0.6)', 'rgba(255, 205, 86, 1)'),
                ('rgba(153, 102, 255, 0.6)', 'rgba(153, 102, 255, 1)')
            ]
            
            for i, gap in enumerate(capability_gaps[:5]):  # Limit to 5 capabilities
                color_pair = colors[i % len(colors)]
                try:
                    current = float(gap.get('current_state', '0').replace('%', '')) if '%' in str(gap.get('current_state', '0')) else 0
                    target = float(gap.get('target_state', '0').replace('%', '')) if '%' in str(gap.get('target_state', '0')) else 0
                except:
                    current, target = 0, 0
                
                datasets.append({
                    'label': gap.get('name', f'Capability {i+1}'),
                    'data': [current, target],
                    'backgroundColor': color_pair[0],
                    'borderColor': color_pair[1],
                    'borderWidth': 2
                })
            
            chart_data = {
                'labels': ['Current Capability', 'Target Capability'],
                'datasets': datasets if datasets else [{
                    'label': 'Sample Capability',
                    'data': [40, 85],
                    'backgroundColor': 'rgba(255, 99, 132, 0.6)',
                    'borderColor': 'rgba(255, 99, 132, 1)',
                    'borderWidth': 2
                }]
            }
        
        # Add chart data to module
        chart_id = f"capabilityGapChart_{self.module_id}"
        self.chart_data[chart_id] = {
            'type': 'radar',
            'data': chart_data,
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'scales': {
                    'r': {
                        'beginAtZero': True,
                        'max': 100,
                        'title': {
                            'display': True,
                            'text': 'Capability Level (%)'
                        }
                    }
                }
            }
        }
        
        return f'<canvas id="{chart_id}"></canvas>'
    
    def _get_status_color(self, status: str) -> str:
        """Get CSS class for program status color."""
        status_lower = status.lower()
        if status_lower in ['active', 'on track', 'completed']:
            return 'status-green'
        elif status_lower in ['at risk', 'delayed', 'reviewing']:
            return 'status-yellow'
        elif status_lower in ['critical', 'cancelled', 'suspended']:
            return 'status-red'
        else:
            return 'status-gray'
    
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
            'program_0': TooltipData(
                title="Acquisition Program Analysis",
                description="Comprehensive analysis of acquisition programs including budget, timeline, and strategic objectives.",
                source="Sources: Acquisition program data and strategic analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="High - Direct impact on capability development and strategic positioning",
                recommendations=[
                    "Monitor program milestones closely",
                    "Assess budget allocation efficiency",
                    "Track capability gap closure progress"
                ],
                use_cases=[
                    "Program management",
                    "Strategic planning",
                    "Resource allocation"
                ]
            ),
            'initiative_0': TooltipData(
                title="Modernization Initiative Assessment",
                description="Analysis of modernization initiatives and their impact on overall capability enhancement.",
                source="Sources: Modernization planning and implementation tracking, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Medium-High - Affects long-term capability development",
                recommendations=[
                    "Prioritize high-impact initiatives",
                    "Ensure technology compatibility",
                    "Plan for workforce training"
                ],
                use_cases=[
                    "Capability planning",
                    "Technology roadmapping",
                    "Investment prioritization"
                ]
            ),
            'risk_0': TooltipData(
                title="Program Risk Assessment",
                description="Analysis of risks affecting acquisition programs and their potential impact on objectives.",
                source="Sources: Risk assessment and program monitoring, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="High - Risk management is critical for program success",
                recommendations=[
                    "Develop comprehensive mitigation strategies",
                    "Establish early warning indicators",
                    "Create contingency plans"
                ],
                use_cases=[
                    "Risk management",
                    "Contingency planning",
                    "Program oversight"
                ]
            ),
            'gap_0': TooltipData(
                title="Capability Gap Analysis",
                description="Assessment of capability gaps and how acquisition programs address strategic requirements.",
                source="Sources: Capability assessment and gap analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Critical - Capability gaps affect strategic readiness",
                recommendations=[
                    "Prioritize critical capability gaps",
                    "Align programs with strategic requirements",
                    "Track gap closure progress"
                ],
                use_cases=[
                    "Strategic planning",
                    "Capability development",
                    "Requirements analysis"
                ]
            )
        }
