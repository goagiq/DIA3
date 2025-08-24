"""
Geopolitical Impact Module

Independent module for generating geopolitical impact analysis sections that can be added to any report.
Provides regional power dynamics analysis, strategic partnerships visualization, and interactive radar charts.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class GeopoliticalImpactModule(BaseModule):
    """Geopolitical Impact module for enhanced reports."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Geopolitical Impact module."""
        if config is None:
            config = ModuleConfig(
                title="🌍 Geopolitical Impact Analysis",
                description="Comprehensive analysis of regional power dynamics and strategic partnerships",
                order=20,  # Early order for strategic importance
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'geopolitical_analysis',
            'regional_dynamics',
            'strategic_partnerships',
            'power_balance'
        ]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Geopolitical Impact module."""
        self.validate_data(data)
        
        geopolitical_analysis = data.get('geopolitical_analysis', {})
        regional_dynamics = data.get('regional_dynamics', {})
        strategic_partnerships = data.get('strategic_partnerships', [])
        power_balance = data.get('power_balance', {})
        
        # Generate geopolitical overview
        overview_html = self._generate_geopolitical_overview(geopolitical_analysis)
        
        # Generate regional dynamics analysis
        dynamics_html = self._generate_regional_dynamics(regional_dynamics)
        
        # Generate strategic partnerships visualization
        partnerships_html = self._generate_strategic_partnerships(strategic_partnerships)
        
        # Generate power balance analysis
        power_html = self._generate_power_balance(power_balance)
        
        # Generate interactive visualizations
        visualizations_html = self._generate_interactive_visualizations(data)
        
        return f"""
        <div class="section" id="geopolitical-impact">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {dynamics_html}
            {partnerships_html}
            {power_html}
            {visualizations_html}
        </div>
        """
    
    def _generate_geopolitical_overview(self, analysis_data: Dict[str, Any]) -> str:
        """Generate the geopolitical analysis overview section."""
        title = analysis_data.get('title', 'Geopolitical Impact Analysis')
        overview = analysis_data.get('overview', 'No geopolitical overview available.')
        key_actors = analysis_data.get('key_actors', [])
        impact_level = analysis_data.get('impact_level', 'Medium')
        confidence_score = analysis_data.get('confidence_score', 0.0)
        
        actors_html = ""
        if key_actors:
            actors_html = """
            <div class="key-actors">
                <h4>🎭 Key Geopolitical Actors</h4>
                <div class="actors-grid">
            """
            for i, actor in enumerate(key_actors):
                actor_id = f"actor_{i}"
                actors_html += f"""
                <div class="actor-card" data-tooltip-{self.module_id}="{actor_id}">
                    <h5>{actor.get('name', 'Unknown Actor')}</h5>
                    <p class="actor-role">{actor.get('role', 'No role specified')}</p>
                    <p class="actor-influence">Influence: {actor.get('influence_level', 'Medium')}</p>
                </div>
                """
            actors_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="geopolitical-overview">
            <div class="overview-header" data-tooltip-{self.module_id}="geopolitical_overview">
                <h3>🌍 Geopolitical Overview</h3>
                <h4>{title}</h4>
                <div class="impact-indicator">
                    <span class="impact-label">Impact Level:</span>
                    <span class="impact-value {impact_level.lower()}">{impact_level}</span>
                </div>
                <div class="confidence-indicator">
                    <span class="confidence-label">Confidence:</span>
                    <span class="confidence-value">{confidence_score:.1f}%</span>
                </div>
            </div>
            <div class="overview-content">
                <p>{overview}</p>
            </div>
            {actors_html}
        </div>
        """
    
    def _generate_regional_dynamics(self, dynamics_data: Dict[str, Any]) -> str:
        """Generate the regional dynamics analysis section."""
        regions = dynamics_data.get('regions', [])
        power_shifts = dynamics_data.get('power_shifts', [])
        conflict_areas = dynamics_data.get('conflict_areas', [])
        
        regions_html = ""
        if regions:
            regions_html = """
            <div class="regional-analysis">
                <h4>🗺️ Regional Power Dynamics</h4>
                <div class="regions-container">
            """
            for i, region in enumerate(regions):
                region_id = f"region_{i}"
                regions_html += f"""
                <div class="region-card" data-tooltip-{self.module_id}="{region_id}">
                    <h5>{region.get('name', 'Unknown Region')}</h5>
                    <div class="region-metrics">
                        <div class="metric">
                            <span class="label">Power Level:</span>
                            <span class="value">{region.get('power_level', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Stability:</span>
                            <span class="value">{region.get('stability', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Strategic Value:</span>
                            <span class="value">{region.get('strategic_value', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="region-description">{region.get('description', 'No description available.')}</p>
                </div>
                """
            regions_html += """
                </div>
            </div>
            """
        
        shifts_html = ""
        if power_shifts:
            shifts_html = """
            <div class="power-shifts">
                <h4>⚖️ Power Shifts</h4>
                <ul>
            """
            for i, shift in enumerate(power_shifts):
                shift_id = f"shift_{i}"
                shifts_html += f"""
                <li data-tooltip-{self.module_id}="{shift_id}">
                    <strong>{shift.get('actor', 'Unknown')}</strong>: {shift.get('description', 'No description')}
                    <span class="shift-magnitude">({shift.get('magnitude', 'Medium')})</span>
                </li>
                """
            shifts_html += """
                </ul>
            </div>
            """
        
        conflicts_html = ""
        if conflict_areas:
            conflicts_html = """
            <div class="conflict-areas">
                <h4>⚠️ Conflict Areas</h4>
                <div class="conflicts-grid">
            """
            for i, conflict in enumerate(conflict_areas):
                conflict_id = f"conflict_{i}"
                conflicts_html += f"""
                <div class="conflict-card" data-tooltip-{self.module_id}="{conflict_id}">
                    <h5>{conflict.get('name', 'Unknown Conflict')}</h5>
                    <p class="conflict-intensity">Intensity: {conflict.get('intensity', 'Medium')}</p>
                    <p class="conflict-description">{conflict.get('description', 'No description available.')}</p>
                </div>
                """
            conflicts_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="regional-dynamics">
            <h3>🗺️ Regional Dynamics Analysis</h3>
            {regions_html}
            {shifts_html}
            {conflicts_html}
        </div>
        """
    
    def _generate_strategic_partnerships(self, partnerships_data: List[Dict[str, Any]]) -> str:
        """Generate the strategic partnerships visualization section."""
        partnerships_html = """
        <div class="strategic-partnerships">
            <h3>🤝 Strategic Partnerships</h3>
        """
        
        if not partnerships_data:
            partnerships_html += """
            <div class="partnerships-container">
                <p>No strategic partnerships data available.</p>
            </div>
            """
        else:
            partnerships_html += """
            <div class="partnerships-container">
            """
        
        for i, partnership in enumerate(partnerships_data):
            partnership_id = f"partnership_{i}"
            strength = partnership.get('strength', 'Medium')
            type_partnership = partnership.get('type', 'Strategic')
            
            partnerships_html += f"""
            <div class="partnership-card" data-tooltip-{self.module_id}="{partnership_id}">
                <div class="partnership-header">
                    <h4>{partnership.get('name', 'Unknown Partnership')}</h4>
                    <span class="partnership-type">{type_partnership}</span>
                </div>
                <div class="partnership-details">
                    <div class="partners">
                        <strong>Partners:</strong> {partnership.get('partners', 'Unknown')}
                    </div>
                    <div class="strength-indicator">
                        <span class="label">Strength:</span>
                        <span class="strength-value {strength.lower()}">{strength}</span>
                    </div>
                    <div class="objectives">
                        <strong>Objectives:</strong> {partnership.get('objectives', 'No objectives specified')}
                    </div>
                    <div class="impact">
                        <strong>Geopolitical Impact:</strong> {partnership.get('impact', 'Medium')}
                    </div>
                </div>
                <p class="partnership-description">{partnership.get('description', 'No description available.')}</p>
            </div>
            """
        
        partnerships_html += """
            </div>
        </div>
        """
        
        return partnerships_html
    
    def _generate_power_balance(self, power_data: Dict[str, Any]) -> str:
        """Generate the power balance analysis section."""
        major_powers = power_data.get('major_powers', [])
        power_indicators = power_data.get('power_indicators', {})
        balance_assessment = power_data.get('balance_assessment', 'No assessment available.')
        
        powers_html = ""
        if major_powers:
            powers_html = """
            <div class="major-powers">
                <h4>🏛️ Major Powers Analysis</h4>
                <div class="powers-grid">
            """
            for i, power in enumerate(major_powers):
                power_id = f"power_{i}"
                powers_html += f"""
                <div class="power-card" data-tooltip-{self.module_id}="{power_id}">
                    <h5>{power.get('name', 'Unknown Power')}</h5>
                    <div class="power-metrics">
                        <div class="metric">
                            <span class="label">Military:</span>
                            <span class="value">{power.get('military_strength', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Economic:</span>
                            <span class="value">{power.get('economic_strength', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Political:</span>
                            <span class="value">{power.get('political_influence', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Strategic:</span>
                            <span class="value">{power.get('strategic_position', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="power-description">{power.get('description', 'No description available.')}</p>
                </div>
                """
            powers_html += """
                </div>
            </div>
            """
        
        indicators_html = ""
        if power_indicators:
            indicators_html = """
            <div class="power-indicators">
                <h4>📊 Power Balance Indicators</h4>
                <div class="indicators-grid">
            """
            for indicator, value in power_indicators.items():
                indicators_html += f"""
                <div class="indicator-card">
                    <h5>{indicator.replace('_', ' ').title()}</h5>
                    <p class="indicator-value">{value}</p>
                </div>
                """
            indicators_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="power-balance">
            <h3>⚖️ Power Balance Analysis</h3>
            {powers_html}
            {indicators_html}
            <div class="balance-assessment">
                <h4>📋 Balance Assessment</h4>
                <p>{balance_assessment}</p>
            </div>
        </div>
        """
    
    def _generate_interactive_visualizations(self, data: Dict[str, Any]) -> str:
        """Generate interactive visualizations for geopolitical analysis."""
        if not self.config.charts_enabled:
            return ""
        
        # Generate radar chart for power comparison
        radar_chart_html = self._generate_power_radar_chart(data)
        
        # Generate network diagram for partnerships
        network_chart_html = self._generate_partnership_network(data)
        
        return f"""
        <div class="geopolitical-visualizations">
            <h3>📈 Interactive Visualizations</h3>
            {radar_chart_html}
            {network_chart_html}
        </div>
        """
    
    def _generate_power_radar_chart(self, data: Dict[str, Any]) -> str:
        """Generate a radar chart comparing power metrics."""
        major_powers = data.get('power_balance', {}).get('major_powers', [])
        
        if not major_powers:
            return ""
        
        # Prepare chart data
        labels = ['Military', 'Economic', 'Political', 'Strategic', 'Technological']
        datasets = []
        
        for power in major_powers[:5]:  # Limit to 5 powers for readability
            power_name = power.get('name', 'Unknown')
            values = [
                self._convert_strength_to_number(power.get('military_strength', 'Medium')),
                self._convert_strength_to_number(power.get('economic_strength', 'Medium')),
                self._convert_strength_to_number(power.get('political_influence', 'Medium')),
                self._convert_strength_to_number(power.get('strategic_position', 'Medium')),
                self._convert_strength_to_number(power.get('technological_capability', 'Medium'))
            ]
            
            datasets.append({
                'label': power_name,
                'data': values,
                'borderColor': self._get_power_color(power_name),
                'backgroundColor': self._get_power_color(power_name, alpha=0.2),
                'pointBackgroundColor': self._get_power_color(power_name)
            })
        
        chart_id = f"power_radar_{self.module_id}"
        
        # Add chart data to the module
        self.add_chart_data(chart_id, {
            'type': 'radar',
            'data': {
                'labels': labels,
                'datasets': datasets
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'scales': {
                    'r': {
                        'beginAtZero': True,
                        'max': 100,
                        'ticks': {
                            'stepSize': 20
                        }
                    }
                },
                'plugins': {
                    'legend': {
                        'position': 'top'
                    },
                    'title': {
                        'display': True,
                        'text': 'Power Metrics Comparison'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>🎯 Power Comparison Radar Chart</h4>
            <canvas id="{chart_id}" width="400" height="400"></canvas>
        </div>
        """
    
    def _generate_partnership_network(self, data: Dict[str, Any]) -> str:
        """Generate a network diagram for strategic partnerships."""
        partnerships = data.get('strategic_partnerships', [])
        
        if not partnerships:
            return ""
        
        # Prepare network data
        nodes = []
        edges = []
        
        # Add nodes for each partner
        partner_ids = {}
        for i, partnership in enumerate(partnerships):
            partners = partnership.get('partners', '').split(' & ')
            for partner in partners:
                partner = partner.strip()
                if partner not in partner_ids:
                    partner_ids[partner] = len(nodes)
                    nodes.append({
                        'id': partner_ids[partner],
                        'label': partner,
                        'group': partnership.get('type', 'Strategic')
                    })
        
        # Add edges for partnerships
        for partnership in partnerships:
            partners = partnership.get('partners', '').split(' & ')
            if len(partners) >= 2:
                source = partner_ids.get(partners[0].strip(), 0)
                target = partner_ids.get(partners[1].strip(), 1)
                edges.append({
                    'from': source,
                    'to': target,
                    'label': partnership.get('name', 'Partnership'),
                    'width': self._convert_strength_to_width(partnership.get('strength', 'Medium'))
                })
        
        chart_id = f"partnership_network_{self.module_id}"
        
        return f"""
        <div class="chart-container">
            <h4>🕸️ Strategic Partnerships Network</h4>
            <div id="{chart_id}" style="width: 100%; height: 400px;"></div>
            <script>
                const container_{chart_id} = document.getElementById('{chart_id}');
                const data_{chart_id} = {{
                    nodes: new vis.DataSet({nodes}),
                    edges: new vis.DataSet({edges})
                }};
                const options_{chart_id} = {{
                    nodes: {{
                        shape: 'dot',
                        size: 20,
                        font: {{
                            size: 12
                        }}
                    }},
                    edges: {{
                        font: {{
                            size: 10
                        }}
                    }},
                    groups: {{
                        'Strategic': {{color: {{background: '#ff7675', border: '#d63031'}}}},
                        'Economic': {{color: {{background: '#74b9ff', border: '#0984e3'}}}},
                        'Military': {{color: {{background: '#55a3ff', border: '#2d3436'}}}},
                        'Diplomatic': {{color: {{background: '#a29bfe', border: '#6c5ce7'}}}}
                    }}
                }};
                new vis.Network(container_{chart_id}, data_{chart_id}, options_{chart_id});
            </script>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        # Geopolitical overview tooltips
        self.add_tooltip("geopolitical_overview", TooltipData(
            title="Geopolitical Overview",
            description="Comprehensive analysis of the geopolitical landscape and its implications for the subject matter.",
            source="Sources: Strategic Intelligence Analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="High - Provides foundation for all geopolitical assessments",
            recommendations="• Monitor geopolitical developments regularly\n• Assess impact on strategic objectives\n• Update analysis based on new developments",
            use_cases="Used in strategic planning and policy development",
            confidence=90.0
        ))
        
        self.add_tooltip("intelligence_summary", TooltipData(
            title="Intelligence Summary",
            description="Summary of key intelligence insights related to geopolitical dynamics.",
            source="Sources: Intelligence Analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="Medium - Supports decision-making processes",
            recommendations="• Validate intelligence sources\n• Cross-reference with multiple sources\n• Update assessments regularly",
            use_cases="Used in intelligence briefings and strategic assessments",
            confidence=85.0
        ))
        
        self.add_tooltip("confidence_metrics", TooltipData(
            title="Confidence Metrics",
            description="Quantified confidence levels for geopolitical assessments and predictions.",
            source="Sources: Analytical Assessment, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="Medium - Indicates reliability of analysis",
            recommendations="• Establish confidence thresholds\n• Track confidence trends\n• Reassess confidence regularly",
            use_cases="Used in risk assessment and decision-making",
            confidence=80.0
        ))
        
        self.add_tooltip("high_impact_insights", TooltipData(
            title="High Impact Insights",
            description="Geopolitical insights with significant strategic implications.",
            source="Sources: Strategic Analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="High - Critical for strategic planning",
            recommendations="• Prioritize high-impact insights\n• Develop response strategies\n• Monitor impact evolution",
            use_cases="Used in policy development and strategic planning",
            confidence=92.0
        ))
    
    def _convert_strength_to_number(self, strength: str) -> int:
        """Convert strength level to numerical value for charts."""
        strength_map = {
            'Very Low': 20,
            'Low': 40,
            'Medium': 60,
            'High': 80,
            'Very High': 100
        }
        return strength_map.get(strength, 60)
    
    def _convert_strength_to_width(self, strength: str) -> int:
        """Convert strength level to edge width for network diagrams."""
        strength_map = {
            'Very Low': 1,
            'Low': 2,
            'Medium': 3,
            'High': 4,
            'Very High': 5
        }
        return strength_map.get(strength, 3)
    
    def _get_power_color(self, power_name: str, alpha: float = 1.0) -> str:
        """Get color for power visualization."""
        colors = {
            'United States': f'rgba(0, 123, 255, {alpha})',
            'China': f'rgba(220, 53, 69, {alpha})',
            'Russia': f'rgba(255, 193, 7, {alpha})',
            'European Union': f'rgba(40, 167, 69, {alpha})',
            'India': f'rgba(255, 69, 0, {alpha})',
            'Japan': f'rgba(108, 117, 125, {alpha})',
            'United Kingdom': f'rgba(23, 162, 184, {alpha})',
            'France': f'rgba(102, 16, 242, {alpha})',
            'Germany': f'rgba(255, 165, 0, {alpha})',
            'Canada': f'rgba(220, 53, 69, {alpha})'
        }
        return colors.get(power_name, f'rgba(108, 117, 125, {alpha})')
