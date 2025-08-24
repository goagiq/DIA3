"""
Balance of Power Module

Independent module for generating balance of power analysis sections that can be added to any report.
Provides naval capability comparison, strategic deterrence index, and interactive radar charts.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class BalanceOfPowerModule(BaseModule):
    """Balance of Power module for enhanced reports."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Balance of Power module."""
        if config is None:
            config = ModuleConfig(
                title="⚖️ Balance of Power Analysis",
                description="Comprehensive analysis of military capabilities, strategic deterrence, and power balance",
                order=30,  # Early order for strategic importance
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'balance_overview',
            'naval_capabilities',
            'strategic_deterrence',
            'power_comparison'
        ]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Balance of Power module."""
        self.validate_data(data)
        
        balance_overview = data.get('balance_overview', {})
        naval_capabilities = data.get('naval_capabilities', {})
        strategic_deterrence = data.get('strategic_deterrence', {})
        power_comparison = data.get('power_comparison', {})
        
        # Generate balance overview
        overview_html = self._generate_balance_overview(balance_overview)
        
        # Generate naval capabilities analysis
        naval_html = self._generate_naval_capabilities(naval_capabilities)
        
        # Generate strategic deterrence analysis
        deterrence_html = self._generate_strategic_deterrence(strategic_deterrence)
        
        # Generate power comparison analysis
        comparison_html = self._generate_power_comparison(power_comparison)
        
        # Generate interactive visualizations
        visualizations_html = self._generate_interactive_visualizations(data)
        
        return f"""
        <div class="section" id="balance-of-power">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {naval_html}
            {deterrence_html}
            {comparison_html}
            {visualizations_html}
        </div>
        """
    
    def _generate_balance_overview(self, overview_data: Dict[str, Any]) -> str:
        """Generate the balance of power overview section."""
        title = overview_data.get('title', 'Balance of Power Analysis')
        overview = overview_data.get('overview', 'No balance overview available.')
        key_actors = overview_data.get('key_actors', [])
        balance_assessment = overview_data.get('balance_assessment', 'Medium')
        confidence_score = overview_data.get('confidence_score', 0.0)
        
        actors_html = ""
        if key_actors:
            actors_html = """
            <div class="key-actors">
                <h4>🎯 Key Power Actors</h4>
                <div class="actors-grid">
            """
            for i, actor in enumerate(key_actors):
                actor_id = f"actor_{i}"
                actors_html += f"""
                <div class="actor-card" data-tooltip-{self.module_id}="{actor_id}">
                    <h5>{actor.get('name', 'Unknown Actor')}</h5>
                    <p class="actor-role">{actor.get('role', 'No role specified')}</p>
                    <p class="actor-power">Power Level: {actor.get('power_level', 'Medium')}</p>
                </div>
                """
            actors_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="balance-overview">
            <div class="overview-header" data-tooltip-{self.module_id}="balance_overview">
                <h3>⚖️ Balance Overview</h3>
                <h4>{title}</h4>
                <div class="balance-indicator">
                    <span class="balance-label">Balance Assessment:</span>
                    <span class="balance-value {balance_assessment.lower()}">{balance_assessment}</span>
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
    
    def _generate_naval_capabilities(self, naval_data: Dict[str, Any]) -> str:
        """Generate the naval capabilities comparison section."""
        surface_combatants = naval_data.get('surface_combatants', [])
        submarines = naval_data.get('submarines', [])
        naval_aviation = naval_data.get('naval_aviation', [])
        amphibious_forces = naval_data.get('amphibious_forces', [])
        
        surface_html = ""
        if surface_combatants:
            surface_html = """
            <div class="surface-combatants">
                <h4>🚢 Surface Combatants</h4>
                <div class="combatants-container">
            """
            for i, combatant in enumerate(surface_combatants):
                combatant_id = f"surface_combatant_{i}"
                surface_html += f"""
                <div class="combatant-card" data-tooltip-{self.module_id}="{combatant_id}">
                    <h5>{combatant.get('name', 'Unknown Combatant')}</h5>
                    <div class="combatant-metrics">
                        <div class="metric">
                            <span class="label">Quantity:</span>
                            <span class="value">{combatant.get('quantity', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Quality:</span>
                            <span class="value">{combatant.get('quality', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Readiness:</span>
                            <span class="value">{combatant.get('readiness', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="combatant-description">{combatant.get('description', 'No description available.')}</p>
                </div>
                """
            surface_html += """
                </div>
            </div>
            """
        
        submarine_html = ""
        if submarines:
            submarine_html = """
            <div class="submarines">
                <h4>🛥️ Submarine Forces</h4>
                <div class="submarines-container">
            """
            for i, submarine in enumerate(submarines):
                submarine_id = f"submarine_{i}"
                submarine_html += f"""
                <div class="submarine-card" data-tooltip-{self.module_id}="{submarine_id}">
                    <h5>{submarine.get('name', 'Unknown Submarine')}</h5>
                    <div class="submarine-metrics">
                        <div class="metric">
                            <span class="label">Quantity:</span>
                            <span class="value">{submarine.get('quantity', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Type:</span>
                            <span class="value">{submarine.get('type', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Capability:</span>
                            <span class="value">{submarine.get('capability', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="submarine-description">{submarine.get('description', 'No description available.')}</p>
                </div>
                """
            submarine_html += """
                </div>
            </div>
            """
        
        aviation_html = ""
        if naval_aviation:
            aviation_html = """
            <div class="naval-aviation">
                <h4>✈️ Naval Aviation</h4>
                <div class="aviation-container">
            """
            for i, aircraft in enumerate(naval_aviation):
                aircraft_id = f"naval_aircraft_{i}"
                aviation_html += f"""
                <div class="aircraft-card" data-tooltip-{self.module_id}="{aircraft_id}">
                    <h5>{aircraft.get('name', 'Unknown Aircraft')}</h5>
                    <div class="aircraft-metrics">
                        <div class="metric">
                            <span class="label">Quantity:</span>
                            <span class="value">{aircraft.get('quantity', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Role:</span>
                            <span class="value">{aircraft.get('role', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Effectiveness:</span>
                            <span class="value">{aircraft.get('effectiveness', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="aircraft-description">{aircraft.get('description', 'No description available.')}</p>
                </div>
                """
            aviation_html += """
                </div>
            </div>
            """
        
        amphibious_html = ""
        if amphibious_forces:
            amphibious_html = """
            <div class="amphibious-forces">
                <h4>🛳️ Amphibious Forces</h4>
                <div class="amphibious-container">
            """
            for i, force in enumerate(amphibious_forces):
                force_id = f"amphibious_force_{i}"
                amphibious_html += f"""
                <div class="amphibious-card" data-tooltip-{self.module_id}="{force_id}">
                    <h5>{force.get('name', 'Unknown Force')}</h5>
                    <div class="amphibious-metrics">
                        <div class="metric">
                            <span class="label">Quantity:</span>
                            <span class="value">{force.get('quantity', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Capability:</span>
                            <span class="value">{force.get('capability', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Readiness:</span>
                            <span class="value">{force.get('readiness', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="amphibious-description">{force.get('description', 'No description available.')}</p>
                </div>
                """
            amphibious_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="naval-capabilities-analysis">
            <h3>🚢 Naval Capabilities Comparison</h3>
            {surface_html}
            {submarine_html}
            {aviation_html}
            {amphibious_html}
        </div>
        """
    
    def _generate_strategic_deterrence(self, deterrence_data: Dict[str, Any]) -> str:
        """Generate the strategic deterrence analysis section."""
        nuclear_capabilities = deterrence_data.get('nuclear_capabilities', [])
        conventional_deterrence = deterrence_data.get('conventional_deterrence', {})
        deterrence_index = deterrence_data.get('deterrence_index', 0.0)
        
        nuclear_html = ""
        if nuclear_capabilities:
            nuclear_html = """
            <div class="nuclear-capabilities">
                <h4>☢️ Nuclear Deterrence</h4>
                <div class="nuclear-container">
            """
            for i, capability in enumerate(nuclear_capabilities):
                capability_id = f"nuclear_capability_{i}"
                nuclear_html += f"""
                <div class="nuclear-card" data-tooltip-{self.module_id}="{capability_id}">
                    <h5>{capability.get('name', 'Unknown Capability')}</h5>
                    <div class="nuclear-metrics">
                        <div class="metric">
                            <span class="label">Quantity:</span>
                            <span class="value">{capability.get('quantity', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Reliability:</span>
                            <span class="value">{capability.get('reliability', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Survivability:</span>
                            <span class="value">{capability.get('survivability', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="nuclear-description">{capability.get('description', 'No description available.')}</p>
                </div>
                """
            nuclear_html += """
                </div>
            </div>
            """
        
        conventional_html = ""
        if conventional_deterrence:
            conventional_html = """
            <div class="conventional-deterrence">
                <h4>🛡️ Conventional Deterrence</h4>
                <div class="conventional-metrics">
            """
            for factor, value in conventional_deterrence.items():
                conventional_html += f"""
                <div class="conventional-factor">
                    <h5>{factor.replace('_', ' ').title()}</h5>
                    <p class="factor-value">{value}</p>
                </div>
                """
            conventional_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="strategic-deterrence-analysis">
            <h3>🛡️ Strategic Deterrence Analysis</h3>
            <div class="deterrence-index">
                <h4>📊 Deterrence Index: {deterrence_index:.1f}</h4>
            </div>
            {nuclear_html}
            {conventional_html}
        </div>
        """
    
    def _generate_power_comparison(self, comparison_data: Dict[str, Any]) -> str:
        """Generate the power comparison analysis section."""
        military_balance = comparison_data.get('military_balance', {})
        economic_balance = comparison_data.get('economic_balance', {})
        technological_balance = comparison_data.get('technological_balance', {})
        overall_assessment = comparison_data.get('overall_assessment', 'No overall assessment available.')
        
        military_html = ""
        if military_balance:
            military_html = """
            <div class="military-balance">
                <h4>⚔️ Military Balance</h4>
                <div class="balance-metrics">
            """
            for country, metrics in military_balance.items():
                military_html += f"""
                <div class="country-military">
                    <h5>{country}</h5>
                    <div class="military-metrics">
            """
                for metric, value in metrics.items():
                    military_html += f"""
                        <div class="metric">
                            <span class="label">{metric.replace('_', ' ').title()}:</span>
                            <span class="value">{value}</span>
                        </div>
                    """
                military_html += """
                    </div>
                </div>
                """
            military_html += """
                </div>
            </div>
            """
        
        economic_html = ""
        if economic_balance:
            economic_html = """
            <div class="economic-balance">
                <h4>💰 Economic Balance</h4>
                <div class="balance-metrics">
            """
            for country, metrics in economic_balance.items():
                economic_html += f"""
                <div class="country-economic">
                    <h5>{country}</h5>
                    <div class="economic-metrics">
            """
                for metric, value in metrics.items():
                    economic_html += f"""
                        <div class="metric">
                            <span class="label">{metric.replace('_', ' ').title()}:</span>
                            <span class="value">{value}</span>
                        </div>
                    """
                economic_html += """
                    </div>
                </div>
                """
            economic_html += """
                </div>
            </div>
            """
        
        technological_html = ""
        if technological_balance:
            technological_html = """
            <div class="technological-balance">
                <h4>🔬 Technological Balance</h4>
                <div class="balance-metrics">
            """
            for country, metrics in technological_balance.items():
                technological_html += f"""
                <div class="country-technological">
                    <h5>{country}</h5>
                    <div class="technological-metrics">
            """
                for metric, value in metrics.items():
                    technological_html += f"""
                        <div class="metric">
                            <span class="label">{metric.replace('_', ' ').title()}:</span>
                            <span class="value">{value}</span>
                        </div>
                    """
                technological_html += """
                    </div>
                </div>
                """
            technological_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="power-comparison-analysis">
            <h3>📊 Power Comparison Analysis</h3>
            {military_html}
            {economic_html}
            {technological_html}
            <div class="overall-assessment">
                <h4>🎯 Overall Assessment</h4>
                <p>{overall_assessment}</p>
            </div>
        </div>
        """
    
    def _generate_interactive_visualizations(self, data: Dict[str, Any]) -> str:
        """Generate interactive visualizations for balance of power analysis."""
        if not self.config.charts_enabled:
            return ""
        
        # Generate naval capabilities radar chart
        naval_chart_html = self._generate_naval_capabilities_chart(data)
        
        # Generate power comparison bar chart
        power_chart_html = self._generate_power_comparison_chart(data)
        
        return f"""
        <div class="balance-visualizations">
            <h3>📈 Interactive Visualizations</h3>
            {naval_chart_html}
            {power_chart_html}
        </div>
        """
    
    def _generate_naval_capabilities_chart(self, data: Dict[str, Any]) -> str:
        """Generate a radar chart for naval capabilities comparison."""
        naval_capabilities = data.get('naval_capabilities', {})
        surface_combatants = naval_capabilities.get('surface_combatants', [])
        submarines = naval_capabilities.get('submarines', [])
        
        if not surface_combatants and not submarines:
            return ""
        
        # Prepare chart data
        labels = ['Surface Combatants', 'Submarines', 'Naval Aviation', 'Amphibious Forces', 'Anti-Submarine Warfare']
        datasets = []
        
        # Add surface combatants data
        if surface_combatants:
            surface_scores = [self._convert_capability_to_number(combatant.get('quality', 'Medium')) for combatant in surface_combatants]
            if surface_scores:
                datasets.append({
                    'label': 'Surface Combatants',
                    'data': [sum(surface_scores) / len(surface_scores)] + [0] * 4,
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 2
                })
        
        # Add submarines data
        if submarines:
            submarine_scores = [self._convert_capability_to_number(submarine.get('capability', 'Medium')) for submarine in submarines]
            if submarine_scores:
                datasets.append({
                    'label': 'Submarines',
                    'data': [0] + [sum(submarine_scores) / len(submarine_scores)] + [0] * 3,
                    'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                    'borderColor': 'rgba(255, 99, 132, 1)',
                    'borderWidth': 2
                })
        
        chart_id = f"naval_capabilities_{self.module_id}"
        
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
                        'max': 100
                    }
                },
                'plugins': {
                    'legend': {
                        'position': 'top'
                    },
                    'title': {
                        'display': True,
                        'text': 'Naval Capabilities Comparison'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>🚢 Naval Capabilities Radar Chart</h4>
            <canvas id="{chart_id}" width="400" height="400"></canvas>
        </div>
        """
    
    def _generate_power_comparison_chart(self, data: Dict[str, Any]) -> str:
        """Generate a bar chart for power comparison analysis."""
        power_comparison = data.get('power_comparison', {})
        military_balance = power_comparison.get('military_balance', {})
        
        if not military_balance:
            return ""
        
        # Prepare chart data
        countries = list(military_balance.keys())
        military_scores = []
        
        for country in countries:
            metrics = military_balance[country]
            # Calculate average military score
            scores = [self._convert_metric_to_number(value) for value in metrics.values()]
            military_scores.append(sum(scores) / len(scores) if scores else 0)
        
        chart_id = f"power_comparison_{self.module_id}"
        
        # Add chart data to the module
        self.add_chart_data(chart_id, {
            'type': 'bar',
            'data': {
                'labels': countries,
                'datasets': [{
                    'label': 'Military Power Score',
                    'data': military_scores,
                    'backgroundColor': 'rgba(75, 192, 192, 0.8)',
                    'borderColor': 'rgba(75, 192, 192, 1)',
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
                        'text': 'Military Power Comparison'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>⚔️ Military Power Comparison</h4>
            <canvas id="{chart_id}" width="400" height="300"></canvas>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        # Balance overview tooltips
        self.add_tooltip("balance_overview", TooltipData(
            title="Balance Overview",
            description="Comprehensive analysis of the current balance of power and its strategic implications.",
            source="Sources: Strategic Balance Analysis Framework, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="High - Critical for strategic planning and policy development",
            recommendations="• Monitor power shifts regularly\n• Assess capability developments\n• Track strategic trends\n• Plan for balance changes",
            use_cases="Used in strategic planning, policy development, and threat assessment",
            confidence=92.0
        ))
        
        self.add_tooltip("naval_capabilities", TooltipData(
            title="Naval Capabilities",
            description="Detailed comparison of naval forces, capabilities, and readiness across key actors.",
            source="Sources: Naval Analysis Framework, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="High - Essential for maritime strategy and naval planning",
            recommendations="• Assess naval modernization programs\n• Monitor capability developments\n• Track readiness levels\n• Plan naval responses",
            use_cases="Used in naval strategy and maritime security planning",
            confidence=88.0
        ))
        
        self.add_tooltip("strategic_deterrence", TooltipData(
            title="Strategic Deterrence",
            description="Analysis of nuclear and conventional deterrence capabilities and effectiveness.",
            source="Sources: Deterrence Analysis Framework, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="High - Critical for strategic stability and deterrence policy",
            recommendations="• Assess deterrence effectiveness\n• Monitor capability developments\n• Track strategic trends\n• Plan deterrence strategies",
            use_cases="Used in strategic policy and deterrence planning",
            confidence=90.0
        ))
        
        self.add_tooltip("power_comparison", TooltipData(
            title="Power Comparison",
            description="Comprehensive comparison of military, economic, and technological power across actors.",
            source="Sources: Power Analysis Framework, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
            strategic_impact="High - Essential for strategic assessment and planning",
            recommendations="• Monitor power shifts\n• Assess capability developments\n• Track strategic trends\n• Plan strategic responses",
            use_cases="Used in strategic assessment and policy planning",
            confidence=85.0
        ))
    
    def _convert_capability_to_number(self, capability: str) -> int:
        """Convert capability level to numerical value for charts."""
        capability_map = {
            'Very Low': 20,
            'Low': 40,
            'Medium': 60,
            'High': 80,
            'Very High': 100
        }
        return capability_map.get(capability, 60)
    
    def _convert_metric_to_number(self, metric: str) -> float:
        """Convert metric string to numerical value for charts."""
        # Extract percentage from string like "85%" or "High (85%)"
        import re
        numbers = re.findall(r'\d+', str(metric))
        if numbers:
            return float(numbers[0])
        return 50.0  # Default value
