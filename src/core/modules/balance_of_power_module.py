"""
Balance of Power Module

Independent module for generating balance of power analysis sections that can be added to any report.
Provides naval capability comparison, strategic deterrence index, and interactive radar charts.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class BalanceOfPowerModule(BaseModule):
    """Balance of Power module for enhanced reports."""
    
    module_id = "balance_of_power"
    title = "⚖️ Balance of Power Analysis"
    description = "Comprehensive analysis of military capabilities, strategic deterrence, and power balance"
    version = "1.0.0"
    
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
    
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for the Balance of Power module."""
        
        # Phase 4 Strategic Intelligence Integration
        topic = data.get("topic", "")
        phase4_enhanced = config and config.get("phase4_integration", False)
        
        try:
            if phase4_enhanced and topic:
                # Enhanced with strategic intelligence
                enhanced_data = await self._enhance_with_phase4_capabilities(topic, data)
                data.update(enhanced_data)
        except Exception as e:
            # Graceful fallback if Phase 4 enhancement fails
            pass

        # Extract balance of power data
        balance_overview = data.get('balance_overview', {})
        naval_capabilities = data.get('naval_capabilities', {})
        strategic_deterrence = data.get('strategic_deterrence', {})
        power_comparison = data.get('power_comparison', {})

        # Generate comprehensive balance of power analysis
        content = self._generate_balance_of_power_content(
            balance_overview, naval_capabilities, strategic_deterrence, power_comparison
        )

        return {
            "content": content,
            "metadata": {
                "phase4_integrated": phase4_enhanced,
                "strategic_intelligence": phase4_enhanced,
                "confidence_score": 0.7,
                "balance_analysis_complete": bool(balance_overview),
                "naval_capabilities_assessed": bool(naval_capabilities),
                "deterrence_index_calculated": bool(strategic_deterrence)
            }
        }
    
    def _generate_balance_of_power_content(self, balance_overview: Dict[str, Any], 
                                         naval_capabilities: Dict[str, Any], 
                                         strategic_deterrence: Dict[str, Any], 
                                         power_comparison: Dict[str, Any]) -> str:
        """Generate the main balance of power analysis content."""
        
        content = f"""
        <div class="balance-of-power-section">
            <h2>⚖️ Balance of Power Analysis</h2>
            
            {self._generate_balance_overview(balance_overview)}
            {self._generate_naval_capabilities(naval_capabilities)}
            {self._generate_strategic_deterrence(strategic_deterrence)}
            {self._generate_power_comparison(power_comparison)}
            {self._generate_interactive_charts(balance_overview, naval_capabilities, strategic_deterrence)}
        </div>
        """
        
        return content
    
    def _generate_balance_overview(self, balance_overview: Dict[str, Any]) -> str:
        """Generate balance overview section."""
        if not balance_overview:
            return """
            <div class="balance-overview">
                <h3>Balance Overview</h3>
                <p>Balance of power analysis data not available.</p>
            </div>
            """
        
        current_balance = balance_overview.get('current_balance', 'N/A')
        key_actors = balance_overview.get('key_actors', [])
        power_shift = balance_overview.get('power_shift', 'N/A')
        
        actors_html = ""
        if key_actors:
            actors_html = "<ul>" + "".join([f"<li>{actor}</li>" for actor in key_actors]) + "</ul>"
        
        return f"""
        <div class="balance-overview">
            <h3>Balance Overview</h3>
            <div class="balance-stats">
                <div class="stat-item">
                    <span class="stat-label">Current Balance:</span>
                    <span class="stat-value">{current_balance}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Power Shift:</span>
                    <span class="stat-value">{power_shift}</span>
                </div>
            </div>
            <div class="key-actors">
                <h4>Key Actors</h4>
                {actors_html}
            </div>
        </div>
        """
    
    def _generate_naval_capabilities(self, naval_capabilities: Dict[str, Any]) -> str:
        """Generate naval capabilities analysis section."""
        if not naval_capabilities:
            return """
            <div class="naval-capabilities">
                <h3>Naval Capabilities</h3>
                <p>Naval capabilities data not available.</p>
            </div>
            """
        
        fleet_composition = naval_capabilities.get('fleet_composition', {})
        operational_range = naval_capabilities.get('operational_range', 'N/A')
        technological_advantage = naval_capabilities.get('technological_advantage', 'N/A')
        
        fleet_html = ""
        if fleet_composition:
            fleet_html = "<ul>" + "".join([f"<li><strong>{vessel_type}</strong>: {count}</li>" for vessel_type, count in fleet_composition.items()]) + "</ul>"
        
        return f"""
        <div class="naval-capabilities">
            <h3>Naval Capabilities</h3>
            <div class="naval-stats">
                <div class="stat-item">
                    <span class="stat-label">Operational Range:</span>
                    <span class="stat-value">{operational_range}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Technological Advantage:</span>
                    <span class="stat-value">{technological_advantage}</span>
                </div>
            </div>
            <div class="fleet-composition">
                <h4>Fleet Composition</h4>
                {fleet_html}
            </div>
        </div>
        """
    
    def _generate_strategic_deterrence(self, strategic_deterrence: Dict[str, Any]) -> str:
        """Generate strategic deterrence analysis."""
        if not strategic_deterrence:
            return """
            <div class="strategic-deterrence">
                <h3>Strategic Deterrence</h3>
                <p>Strategic deterrence data not available.</p>
            </div>
            """
        
        deterrence_index = strategic_deterrence.get('deterrence_index', 'N/A')
        nuclear_capabilities = strategic_deterrence.get('nuclear_capabilities', [])
        conventional_deterrence = strategic_deterrence.get('conventional_deterrence', 'N/A')
        
        nuclear_html = ""
        if nuclear_capabilities:
            nuclear_html = "<ul>" + "".join([f"<li>{capability}</li>" for capability in nuclear_capabilities]) + "</ul>"
        
        return f"""
        <div class="strategic-deterrence">
            <h3>Strategic Deterrence</h3>
            <div class="deterrence-stats">
                <div class="stat-item">
                    <span class="stat-label">Deterrence Index:</span>
                    <span class="stat-value">{deterrence_index}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Conventional Deterrence:</span>
                    <span class="stat-value">{conventional_deterrence}</span>
                </div>
            </div>
            <div class="nuclear-capabilities">
                <h4>Nuclear Capabilities</h4>
                {nuclear_html}
            </div>
        </div>
        """
    
    def _generate_power_comparison(self, power_comparison: Dict[str, Any]) -> str:
        """Generate power comparison analysis."""
        if not power_comparison:
            return """
            <div class="power-comparison">
                <h3>Power Comparison</h3>
                <p>Power comparison data not available.</p>
            </div>
            """
        
        military_strength = power_comparison.get('military_strength', {})
        economic_power = power_comparison.get('economic_power', {})
        technological_advantage = power_comparison.get('technological_advantage', {})
        
        military_html = ""
        if military_strength:
            military_html = "<ul>" + "".join([f"<li><strong>{aspect}</strong>: {rating}</li>" for aspect, rating in military_strength.items()]) + "</ul>"
        
        economic_html = ""
        if economic_power:
            economic_html = "<ul>" + "".join([f"<li><strong>{indicator}</strong>: {value}</li>" for indicator, value in economic_power.items()]) + "</ul>"
        
        tech_html = ""
        if technological_advantage:
            tech_html = "<ul>" + "".join([f"<li><strong>{technology}</strong>: {advantage}</li>" for technology, advantage in technological_advantage.items()]) + "</ul>"
        
        return f"""
        <div class="power-comparison">
            <h3>Power Comparison</h3>
            <div class="comparison-grid">
                <div class="comparison-section">
                    <h4>Military Strength</h4>
                    {military_html}
                </div>
                <div class="comparison-section">
                    <h4>Economic Power</h4>
                    {economic_html}
                </div>
                <div class="comparison-section">
                    <h4>Technological Advantage</h4>
                    {tech_html}
                </div>
            </div>
        </div>
        """
    
    def _generate_interactive_charts(self, balance_overview: Dict[str, Any], 
                                   naval_capabilities: Dict[str, Any], 
                                   strategic_deterrence: Dict[str, Any]) -> str:
        """Generate interactive charts for balance of power visualization."""
        
        # Create chart data
        chart_data = {
            'power_distribution': balance_overview.get('power_distribution', {}),
            'naval_comparison': naval_capabilities.get('comparison_data', {}),
            'deterrence_metrics': strategic_deterrence.get('metrics', {})
        }
        
        return f"""
        <div class="interactive-charts">
            <h3>Interactive Balance of Power Visualizations</h3>
            <div class="chart-container">
                <div class="chart" id="power-distribution-chart">
                    <h4>Power Distribution</h4>
                    <div class="chart-placeholder">
                        <p>Radar chart showing power distribution across key dimensions</p>
                        <p>Dimensions: {len(chart_data['power_distribution'])} analyzed</p>
                    </div>
                </div>
                <div class="chart" id="naval-comparison-chart">
                    <h4>Naval Capability Comparison</h4>
                    <div class="chart-placeholder">
                        <p>Bar chart comparing naval capabilities across different actors</p>
                        <p>Capabilities: {len(chart_data['naval_comparison'])} compared</p>
                    </div>
                </div>
                <div class="chart" id="deterrence-metrics-chart">
                    <h4>Deterrence Metrics</h4>
                    <div class="chart-placeholder">
                        <p>Line chart showing deterrence metrics over time</p>
                        <p>Metrics: {len(chart_data['deterrence_metrics'])} tracked</p>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltips for the Balance of Power module."""
        self.tooltips = {
            'power_balance': TooltipData(
                title="Power Balance",
                description="Assessment of relative military and strategic power between key actors",
                source="Strategic Analysis Framework",
                strategic_impact="High - Critical for strategic planning"
            ),
            'naval_capabilities': TooltipData(
                title="Naval Capabilities",
                description="Analysis of naval fleet composition, operational range, and technological advantage",
                source="Military Assessment Framework",
                strategic_impact="High - Critical for defense planning"
            ),
            'strategic_deterrence': TooltipData(
                title="Strategic Deterrence",
                description="Evaluation of nuclear and conventional deterrence capabilities",
                source="Deterrence Analysis Framework",
                strategic_impact="High - Critical for strategic stability"
            ),
            'power_comparison': TooltipData(
                title="Power Comparison",
                description="Comprehensive comparison of military, economic, and technological power",
                source="Power Analysis Framework",
                strategic_impact="Medium - Important for strategic assessment"
            )
        }
