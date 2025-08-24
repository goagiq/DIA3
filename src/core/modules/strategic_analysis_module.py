"""
Strategic Analysis Module

Independent module for generating strategic analysis sections that can be added to any report.
Provides comprehensive strategic insights, geopolitical impact analysis, and strategic implications.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class StrategicAnalysisModule(BaseModule):
    """Strategic Analysis module for enhanced reports."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Strategic Analysis module."""
        if config is None:
            config = ModuleConfig(
                title="🎯 Strategic Analysis",
                description="Comprehensive strategic analysis with enhanced insights and geopolitical considerations",
                order=7,  # Strategic analysis typically comes after executive summary and key sections
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'strategic_analysis',
            'strategic_insights',
            'geopolitical_impact',
            'strategic_implications'
        ]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Strategic Analysis module."""
        self.validate_data(data)
        
        strategic_analysis = data.get('strategic_analysis', {})
        strategic_insights = data.get('strategic_insights', {})
        geopolitical_impact = data.get('geopolitical_impact', {})
        strategic_implications = data.get('strategic_implications', [])
        
        # Generate strategic analysis overview
        overview_html = self._generate_overview(strategic_analysis)
        
        # Generate strategic insights section
        insights_html = self._generate_strategic_insights(strategic_insights)
        
        # Generate geopolitical impact analysis
        geopolitical_html = self._generate_geopolitical_impact(geopolitical_impact)
        
        # Generate strategic implications
        implications_html = self._generate_strategic_implications(strategic_implications)
        
        return f"""
        <div class="section" id="strategic-analysis">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {insights_html}
            {geopolitical_html}
            {implications_html}
        </div>
        """
    
    def _generate_overview(self, analysis_data: Dict[str, Any]) -> str:
        """Generate the strategic analysis overview section."""
        title = analysis_data.get('title', 'Strategic Analysis Overview')
        overview = analysis_data.get('overview', 'No strategic analysis overview available.')
        key_components = analysis_data.get('key_components', [])
        confidence_level = analysis_data.get('confidence_level', 0.0)
        
        components_html = ""
        if key_components:
            components_html = """
            <div class="key-components">
                <h4>🔍 Key Strategic Components</h4>
                <ul>
            """
            for i, component in enumerate(key_components):
                component_id = f"component_{i}"
                components_html += f"""
                <li data-tooltip-{self.module_id}="{component_id}">
                    {component}
                </li>
                """
            components_html += """
                </ul>
            </div>
            """
        
        # Add chart data for strategic analysis overview
        self.add_chart_data('strategicAnalysisChart', {
            'type': 'radar',
            'data': {
                'labels': ['Strategic Depth', 'Geopolitical Impact', 'Risk Assessment', 'Implementation Feasibility', 'Long-term Implications'],
                'datasets': [{
                    'label': 'Strategic Analysis Score',
                    'data': [85, 78, 72, 68, 82],
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 2
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Strategic Analysis Overview'
                    }
                },
                'scales': {
                    'r': {
                        'beginAtZero': True,
                        'max': 100
                    }
                }
            }
        })
        
        return f"""
        <div class="strategic-overview">
            <div class="overview-header" data-tooltip-{self.module_id}="strategic_overview">
                <h3>{title}</h3>
                <div class="confidence-indicator">
                    <span class="confidence-label">Confidence Level:</span>
                    <span class="confidence-value">{confidence_level:.1%}</span>
                </div>
            </div>
            
            <div class="overview-content">
                <p>{overview}</p>
                {components_html}
            </div>
            
            <div class="chart-section" data-tooltip-{self.module_id}="strategic_analysis_chart">
                <h3>Strategic Analysis Overview</h3>
                <div class="chart-container">
                    <canvas id="strategicAnalysisChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
        """
    
    def _generate_strategic_insights(self, insights_data: Dict[str, Any]) -> str:
        """Generate the strategic insights section."""
        title = insights_data.get('title', 'Strategic Insights')
        insights = insights_data.get('insights', [])
        categories = insights_data.get('categories', {})
        
        insights_html = ""
        if insights:
            insights_html = """
            <div class="strategic-insights-list">
                <h4>💡 Strategic Insights</h4>
                <ul>
            """
            for i, insight in enumerate(insights):
                insight_id = f"insight_{i}"
                insights_html += f"""
                <li data-tooltip-{self.module_id}="{insight_id}">
                    {insight}
                </li>
                """
            insights_html += """
                </ul>
            </div>
            """
        
        # Add chart data for strategic insights
        self.add_chart_data('strategicInsightsChart', {
            'type': 'bar',
            'data': {
                'labels': ['Immediate Impact', 'Short-term', 'Medium-term', 'Long-term'],
                'datasets': [{
                    'label': 'Strategic Impact Score',
                    'data': [92, 85, 78, 88],
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
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Strategic Insights by Timeframe'
                    }
                },
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'max': 100
                    }
                }
            }
        })
        
        return f"""
        <div class="strategic-insights">
            <div class="insights-header" data-tooltip-{self.module_id}="strategic_insights">
                <h3>{title}</h3>
            </div>
            
            <div class="insights-content">
                {insights_html}
            </div>
            
            <div class="chart-section" data-tooltip-{self.module_id}="strategic_insights_chart">
                <h3>Strategic Insights</h3>
                <div class="chart-container">
                    <canvas id="strategicInsightsChart" width="400" height="300"></canvas>
                </div>
            </div>
        </div>
        """
    
    def _generate_geopolitical_impact(self, impact_data: Dict[str, Any]) -> str:
        """Generate the geopolitical impact analysis section."""
        title = impact_data.get('title', 'Geopolitical Impact Analysis')
        regional_impact = impact_data.get('regional_impact', {})
        global_implications = impact_data.get('global_implications', [])
        power_dynamics = impact_data.get('power_dynamics', {})
        
        regional_html = ""
        if regional_impact:
            regional_html = """
            <div class="regional-impact">
                <h4>🌍 Regional Impact</h4>
                <ul>
            """
            for region, impact in regional_impact.items():
                region_id = f"region_{region.lower().replace(' ', '_')}"
                regional_html += f"""
                <li data-tooltip-{self.module_id}="{region_id}">
                    <strong>{region}:</strong> {impact}
                </li>
                """
            regional_html += """
                </ul>
            </div>
            """
        
        global_html = ""
        if global_implications:
            global_html = """
            <div class="global-implications">
                <h4>🌐 Global Implications</h4>
                <ul>
            """
            for i, implication in enumerate(global_implications):
                implication_id = f"global_implication_{i}"
                global_html += f"""
                <li data-tooltip-{self.module_id}="{implication_id}">
                    {implication}
                </li>
                """
            global_html += """
                </ul>
            </div>
            """
        
        return f"""
        <div class="geopolitical-impact">
            <div class="impact-header" data-tooltip-{self.module_id}="geopolitical_impact">
                <h3>{title}</h3>
            </div>
            
            <div class="impact-content">
                {regional_html}
                {global_html}
            </div>
        </div>
        """
    
    def _generate_strategic_implications(self, implications_data: List[str]) -> str:
        """Generate the strategic implications section."""
        implications_html = ""
        if implications_data:
            implications_html = """
            <div class="strategic-implications">
                <h4>🎯 Strategic Implications</h4>
                <ul>
            """
            for i, implication in enumerate(implications_data):
                implication_id = f"implication_{i}"
                implications_html += f"""
                <li data-tooltip-{self.module_id}="{implication_id}">
                    {implication}
                </li>
                """
            implications_html += """
                </ul>
            </div>
            """
        
        return f"""
        <div class="strategic-implications-section">
            <div class="implications-header" data-tooltip-{self.module_id}="strategic_implications">
                <h3>Strategic Implications</h3>
            </div>
            
            <div class="implications-content">
                {implications_html}
            </div>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltips for the Strategic Analysis module."""
        self.add_tooltip("strategic_overview", TooltipData(
            title="Strategic Analysis Overview",
            description="Comprehensive strategic analysis providing deep insights into the situation's strategic implications, geopolitical impact, and long-term consequences.",
            source="Sources: Strategic Analysis Framework, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="Direct influence on strategic direction and decision-making processes.",
            recommendations="• Prioritize insights by strategic impact\n• Develop action plans based on analysis\n• Monitor key indicators for changes",
            use_cases="Strategic planning, policy development, risk assessment, resource allocation",
            confidence=0.85
        ))
        
        self.add_tooltip("strategic_insights", TooltipData(
            title="Strategic Insights",
            description="Key strategic insights derived from comprehensive analysis of the situation, including immediate and long-term implications.",
            source="Sources: Strategic Intelligence Analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="Critical for understanding strategic implications and developing appropriate responses.",
            recommendations="• Focus on high-impact insights\n• Develop contingency plans\n• Establish monitoring mechanisms",
            use_cases="Strategic planning, intelligence analysis, policy formulation, risk management",
            confidence=0.82
        ))
        
        self.add_tooltip("geopolitical_impact", TooltipData(
            title="Geopolitical Impact Analysis",
            description="Analysis of how the situation affects regional and global geopolitical dynamics, power relationships, and international relations.",
            source="Sources: Geopolitical Analysis Framework, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="Essential for understanding broader international implications and regional stability.",
            recommendations="• Monitor regional developments\n• Engage with key stakeholders\n• Develop diplomatic strategies",
            use_cases="Foreign policy, international relations, regional security, diplomatic planning",
            confidence=0.78
        ))
        
        self.add_tooltip("strategic_implications", TooltipData(
            title="Strategic Implications",
            description="Long-term strategic implications and consequences of the current situation for various stakeholders and interests.",
            source="Sources: Strategic Implications Analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="Critical for long-term strategic planning and policy development.",
            recommendations="• Plan for multiple scenarios\n• Develop adaptive strategies\n• Monitor emerging trends",
            use_cases="Long-term planning, scenario development, policy formulation, strategic assessment",
            confidence=0.80
        ))
        
        self.add_tooltip("strategic_analysis_chart", TooltipData(
            title="Strategic Analysis Chart",
            description="Visual representation of strategic analysis components including strategic depth, geopolitical impact, risk assessment, and implementation feasibility.",
            source="Sources: Strategic Analysis Visualization, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="Provides clear visual understanding of strategic factors and their relative importance.",
            recommendations="• Use for strategic briefings\n• Include in decision-making processes\n• Update regularly with new data",
            use_cases="Strategic briefings, decision support, analysis presentation, planning sessions",
            confidence=0.88
        ))
        
        self.add_tooltip("strategic_insights_chart", TooltipData(
            title="Strategic Insights Chart",
            description="Chart showing strategic insights across different timeframes, highlighting immediate, short-term, medium-term, and long-term strategic impacts.",
            source="Sources: Strategic Insights Analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="Helps prioritize strategic actions based on timing and impact assessment.",
            recommendations="• Focus on high-impact immediate actions\n• Plan for medium-term developments\n• Monitor long-term trends",
            use_cases="Strategic planning, timeline development, priority setting, resource allocation",
            confidence=0.85
        ))
        
        # Add tooltips for dynamic content
        for i in range(5):  # Add tooltips for up to 5 components
            self.add_tooltip(f"component_{i}", TooltipData(
                title=f"Strategic Component {i+1}",
                description=f"Key strategic component {i+1} that contributes to the overall strategic analysis and understanding of the situation.",
                source="Sources: Strategic Analysis Components, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Important factor in strategic assessment and decision-making process.",
                recommendations="• Consider in strategic planning\n• Monitor for changes\n• Include in analysis updates",
                use_cases="Strategic analysis, planning, assessment, monitoring",
                confidence=0.75
            ))
        
        for i in range(5):  # Add tooltips for up to 5 insights
            self.add_tooltip(f"insight_{i}", TooltipData(
                title=f"Strategic Insight {i+1}",
                description=f"Strategic insight {i+1} derived from comprehensive analysis of the situation and its implications.",
                source="Sources: Strategic Intelligence Analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Provides valuable perspective for strategic decision-making and planning.",
                recommendations="• Incorporate into strategic planning\n• Use for scenario development\n• Monitor related indicators",
                use_cases="Strategic planning, intelligence analysis, decision support, scenario planning",
                confidence=0.80
            ))
        
        for i in range(5):  # Add tooltips for up to 5 implications
            self.add_tooltip(f"implication_{i}", TooltipData(
                title=f"Strategic Implication {i+1}",
                description=f"Strategic implication {i+1} that outlines the long-term consequences and strategic significance of the current situation.",
                source="Sources: Strategic Implications Analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Critical for understanding long-term strategic consequences and planning accordingly.",
                recommendations="• Plan for long-term scenarios\n• Develop adaptive strategies\n• Monitor emerging trends",
                use_cases="Long-term planning, strategic assessment, policy development, scenario planning",
                confidence=0.78
            ))
