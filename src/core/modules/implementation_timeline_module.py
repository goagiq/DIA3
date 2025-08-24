"""
Implementation Timeline Module

Independent module for generating implementation timeline analysis sections that can be added to any report.
Provides implementation timeline, key milestones, progress tracking, and timeline visualization.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class ImplementationTimelineModule(BaseModule):
    """Implementation Timeline module for enhanced reports."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Implementation Timeline module."""
        if config is None:
            config = ModuleConfig(
                title="📅 Implementation Timeline Analysis",
                description="Comprehensive analysis of implementation timelines and key milestones",
                order=30,  # After regional sentiment
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'implementation_timeline',
            'key_milestones',
            'progress_tracking',
            'timeline_analysis'
        ]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Implementation Timeline module."""
        self.validate_data(data)
        
        implementation_timeline = data.get('implementation_timeline', {})
        key_milestones = data.get('key_milestones', {})
        progress_tracking = data.get('progress_tracking', {})
        timeline_analysis = data.get('timeline_analysis', {})
        
        # Generate timeline overview
        overview_html = self._generate_timeline_overview(implementation_timeline)
        
        # Generate key milestones analysis
        milestones_html = self._generate_key_milestones(key_milestones)
        
        # Generate progress tracking
        progress_html = self._generate_progress_tracking(progress_tracking)
        
        # Generate timeline analysis
        analysis_html = self._generate_timeline_analysis(timeline_analysis)
        
        # Generate interactive visualizations
        visualizations_html = self._generate_interactive_visualizations(data)
        
        return f"""
        <div class="section" id="implementation-timeline">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {milestones_html}
            {progress_html}
            {analysis_html}
            {visualizations_html}
        </div>
        """
    
    def _generate_timeline_overview(self, timeline_data: Dict[str, Any]) -> str:
        """Generate the implementation timeline overview section."""
        title = timeline_data.get('title', 'Implementation Timeline Overview')
        overview = timeline_data.get('overview', 'No implementation timeline overview available.')
        total_duration = timeline_data.get('total_duration', 'Unknown')
        start_date = timeline_data.get('start_date', 'Unknown')
        end_date = timeline_data.get('end_date', 'Unknown')
        phases = timeline_data.get('phases', [])
        
        phases_html = ""
        if phases:
            phases_html = """
            <div class="timeline-phases">
                <h4>📋 Implementation Phases</h4>
                <div class="phases-grid">
            """
            for i, phase in enumerate(phases):
                phase_id = f"phase_{i}"
                phases_html += f"""
                <div class="phase-card" data-tooltip-{self.module_id}="{phase_id}">
                    <h5>{phase.get('name', 'Unknown Phase')}</h5>
                    <p class="phase-duration">Duration: {phase.get('duration', 'Unknown')}</p>
                    <p class="phase-status">Status: {phase.get('status', 'Unknown')}</p>
                    <p class="phase-progress">Progress: {phase.get('progress', 0):.1%}</p>
                </div>
                """
            phases_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="timeline-overview">
            <h3>📊 {title}</h3>
            <p>{overview}</p>
            
            <div class="timeline-metrics">
                <div class="metric-card">
                    <div class="metric-label">Total Duration</div>
                    <div class="metric-value">{total_duration}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Start Date</div>
                    <div class="metric-value">{start_date}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">End Date</div>
                    <div class="metric-value">{end_date}</div>
                </div>
            </div>
            
            {phases_html}
        </div>
        """
    
    def _generate_key_milestones(self, milestones_data: Dict[str, Any]) -> str:
        """Generate the key milestones section."""
        title = milestones_data.get('title', 'Key Milestones')
        overview = milestones_data.get('overview', 'No key milestones overview available.')
        milestones = milestones_data.get('milestones', [])
        critical_path = milestones_data.get('critical_path', [])
        
        milestones_html = ""
        if milestones:
            milestones_html = """
            <div class="milestones-list">
                <h4>🎯 Key Milestones</h4>
                <div class="milestones-timeline">
            """
            for i, milestone in enumerate(milestones):
                milestone_id = f"milestone_{i}"
                is_critical = milestone.get('name', '') in critical_path
                critical_class = "critical-milestone" if is_critical else ""
                critical_icon = "🚨" if is_critical else "✅"
                
                milestones_html += f"""
                <div class="milestone-item {critical_class}" data-tooltip-{self.module_id}="{milestone_id}">
                    <div class="milestone-icon">{critical_icon}</div>
                    <div class="milestone-content">
                        <h5>{milestone.get('name', 'Unknown Milestone')}</h5>
                        <p class="milestone-date">Date: {milestone.get('date', 'Unknown')}</p>
                        <p class="milestone-description">{milestone.get('description', 'No description available.')}</p>
                        <div class="milestone-metrics">
                            <span class="metric">Status: {milestone.get('status', 'Unknown')}</span>
                            <span class="metric">Priority: {milestone.get('priority', 'Medium')}</span>
                            <span class="metric">Dependencies: {len(milestone.get('dependencies', []))}</span>
                        </div>
                    </div>
                </div>
                """
            milestones_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="key-milestones">
            <h3>🎯 {title}</h3>
            <p>{overview}</p>
            
            {milestones_html}
        </div>
        """
    
    def _generate_progress_tracking(self, progress_data: Dict[str, Any]) -> str:
        """Generate the progress tracking section."""
        title = progress_data.get('title', 'Progress Tracking')
        overview = progress_data.get('overview', 'No progress tracking overview available.')
        current_progress = progress_data.get('current_progress', 0.0)
        progress_metrics = progress_data.get('progress_metrics', {})
        progress_trends = progress_data.get('progress_trends', [])
        
        metrics_html = ""
        if progress_metrics:
            metrics_html = """
            <div class="progress-metrics">
                <h4>📈 Progress Metrics</h4>
                <div class="metrics-grid">
            """
            for key, value in progress_metrics.items():
                metrics_html += f"""
                <div class="metric-card">
                    <div class="metric-label">{key.replace('_', ' ').title()}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """
            metrics_html += """
                </div>
            </div>
            """
        
        trends_html = ""
        if progress_trends:
            trends_html = """
            <div class="progress-trends">
                <h4>📊 Progress Trends</h4>
                <div class="trends-list">
            """
            for trend in progress_trends:
                trends_html += f"""
                <div class="trend-item">
                    <h5>{trend.get('period', 'Unknown Period')}</h5>
                    <p>Progress: {trend.get('progress', 0):.1%}</p>
                    <p>Status: {trend.get('status', 'Unknown')}</p>
                    <p>Notes: {trend.get('notes', 'No notes available.')}</p>
                </div>
                """
            trends_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="progress-tracking">
            <h3>📈 {title}</h3>
            <p>{overview}</p>
            
            <div class="overall-progress">
                <h4>🎯 Overall Progress</h4>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {current_progress:.1%}"></div>
                </div>
                <p class="progress-text">{current_progress:.1%} Complete</p>
            </div>
            
            {metrics_html}
            {trends_html}
        </div>
        """
    
    def _generate_timeline_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """Generate the timeline analysis section."""
        title = analysis_data.get('title', 'Timeline Analysis')
        overview = analysis_data.get('overview', 'No timeline analysis overview available.')
        risk_factors = analysis_data.get('risk_factors', [])
        optimization_opportunities = analysis_data.get('optimization_opportunities', [])
        recommendations = analysis_data.get('recommendations', [])
        
        risks_html = ""
        if risk_factors:
            risks_html = """
            <div class="risk-factors">
                <h4>⚠️ Risk Factors</h4>
                <div class="risks-list">
            """
            for i, risk in enumerate(risk_factors):
                risk_id = f"risk_{i}"
                risks_html += f"""
                <div class="risk-item" data-tooltip-{self.module_id}="{risk_id}">
                    <h5>{risk.get('factor', 'Unknown Risk')}</h5>
                    <p class="risk-impact">Impact: {risk.get('impact', 'Unknown')}</p>
                    <p class="risk-probability">Probability: {risk.get('probability', 'Unknown')}</p>
                    <p class="risk-mitigation">{risk.get('mitigation', 'No mitigation strategy available.')}</p>
                </div>
                """
            risks_html += """
                </div>
            </div>
            """
        
        optimization_html = ""
        if optimization_opportunities:
            optimization_html = """
            <div class="optimization-opportunities">
                <h4>🚀 Optimization Opportunities</h4>
                <div class="opportunities-list">
            """
            for opportunity in optimization_opportunities:
                optimization_html += f"""
                <div class="opportunity-item">
                    <h5>{opportunity.get('opportunity', 'Unknown Opportunity')}</h5>
                    <p class="opportunity-impact">Potential Impact: {opportunity.get('impact', 'Unknown')}</p>
                    <p class="opportunity-effort">Effort Required: {opportunity.get('effort', 'Unknown')}</p>
                    <p class="opportunity-description">{opportunity.get('description', 'No description available.')}</p>
                </div>
                """
            optimization_html += """
                </div>
            </div>
            """
        
        recommendations_html = ""
        if recommendations:
            recommendations_html = """
            <div class="timeline-recommendations">
                <h4>💡 Recommendations</h4>
                <div class="recommendations-list">
            """
            for recommendation in recommendations:
                recommendations_html += f"""
                <div class="recommendation-item">
                    <h5>{recommendation.get('title', 'Unknown Recommendation')}</h5>
                    <p class="recommendation-description">{recommendation.get('description', 'No description available.')}</p>
                    <p class="recommendation-priority">Priority: {recommendation.get('priority', 'Medium')}</p>
                    <p class="recommendation-timeline">Timeline: {recommendation.get('timeline', 'Unknown')}</p>
                </div>
                """
            recommendations_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="timeline-analysis">
            <h3>📊 {title}</h3>
            <p>{overview}</p>
            
            {risks_html}
            {optimization_html}
            {recommendations_html}
        </div>
        """
    
    def _generate_interactive_visualizations(self, data: Dict[str, Any]) -> str:
        """Generate interactive visualizations for the module."""
        if not self.config.charts_enabled:
            return ""
        
        # Generate timeline Gantt chart
        gantt_chart = self._generate_timeline_gantt_chart(data)
        
        # Generate progress tracking chart
        progress_chart = self._generate_progress_tracking_chart(data)
        
        return f"""
        <div class="interactive-visualizations">
            <h3>📊 Interactive Visualizations</h3>
            
            <div class="charts-grid">
                <div class="chart-section">
                    <h4>📅 Implementation Timeline Gantt</h4>
                    {gantt_chart}
                </div>
                
                <div class="chart-section">
                    <h4>📈 Progress Tracking Analysis</h4>
                    {progress_chart}
                </div>
            </div>
        </div>
        """
    
    def _generate_timeline_gantt_chart(self, data: Dict[str, Any]) -> str:
        """Generate timeline Gantt chart."""
        implementation_timeline = data.get('implementation_timeline', {})
        phases = implementation_timeline.get('phases', [])
        
        if not phases:
            # Default data
            chart_data = {
                'labels': ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'],
                'datasets': [{
                    'label': 'Duration (weeks)',
                    'data': [4, 6, 8, 4],
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)'
                    ],
                    'borderColor': [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    'borderWidth': 2
                }]
            }
        else:
            # Process actual data
            labels = [phase.get('name', 'Unknown') for phase in phases]
            durations = [phase.get('duration_weeks', 4) for phase in phases]
            
            chart_data = {
                'labels': labels,
                'datasets': [{
                    'label': 'Duration (weeks)',
                    'data': durations,
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
        
        # Add chart data to module
        chart_id = f"timelineGanttChart_{self.module_id}"
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
                            'text': 'Duration (weeks)'
                        }
                    }
                }
            }
        }
        
        return f'<canvas id="{chart_id}"></canvas>'
    
    def _generate_progress_tracking_chart(self, data: Dict[str, Any]) -> str:
        """Generate progress tracking chart."""
        progress_tracking = data.get('progress_tracking', {})
        progress_trends = progress_tracking.get('progress_trends', [])
        
        if not progress_trends:
            # Default data
            chart_data = {
                'labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
                'datasets': [{
                    'label': 'Progress (%)',
                    'data': [10, 25, 40, 55, 70, 85],
                    'borderColor': '#2ecc71',
                    'backgroundColor': 'rgba(46, 204, 113, 0.1)',
                    'tension': 0.4,
                    'fill': True
                }]
            }
        else:
            # Process actual data
            labels = [trend.get('period', 'Unknown') for trend in progress_trends]
            progress_values = [trend.get('progress', 0) * 100 for trend in progress_trends]
            
            chart_data = {
                'labels': labels,
                'datasets': [{
                    'label': 'Progress (%)',
                    'data': progress_values,
                    'borderColor': '#2ecc71',
                    'backgroundColor': 'rgba(46, 204, 113, 0.1)',
                    'tension': 0.4,
                    'fill': True
                }]
            }
        
        # Add chart data to module
        chart_id = f"progressTrackingChart_{self.module_id}"
        self.chart_data[chart_id] = {
            'type': 'line',
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
                            'text': 'Progress (%)'
                        }
                    }
                }
            }
        }
        
        return f'<canvas id="{chart_id}"></canvas>'
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltips for the module."""
        self.tooltip_data = {
            'phase_0': TooltipData(
                title="Implementation Phase Analysis",
                description="Comprehensive analysis of implementation phases, including timeline, milestones, and progress tracking.",
                source="Sources: Implementation timeline data analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="High - Critical for project success and resource planning",
                recommendations=[
                    "Monitor phase progress regularly",
                    "Identify critical path dependencies",
                    "Optimize resource allocation"
                ],
                use_cases=[
                    "Project management",
                    "Resource planning",
                    "Risk assessment"
                ]
            ),
            'milestone_0': TooltipData(
                title="Key Milestone Analysis",
                description="Analysis of critical milestones and their impact on overall project timeline.",
                source="Sources: Milestone tracking and analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="High - Milestones drive project success",
                recommendations=[
                    "Track milestone dependencies",
                    "Monitor critical path",
                    "Prepare contingency plans"
                ],
                use_cases=[
                    "Project planning",
                    "Milestone tracking",
                    "Risk management"
                ]
            ),
            'risk_0': TooltipData(
                title="Timeline Risk Analysis",
                description="Analysis of risk factors that could impact implementation timeline and project success.",
                source="Sources: Risk assessment and analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="High - Risk mitigation is critical for timeline adherence",
                recommendations=[
                    "Identify risk factors early",
                    "Develop mitigation strategies",
                    "Monitor risk indicators"
                ],
                use_cases=[
                    "Risk management",
                    "Contingency planning",
                    "Project monitoring"
                ]
            )
        }
