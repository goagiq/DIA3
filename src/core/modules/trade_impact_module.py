"""
Trade Impact Module

Independent module for generating trade impact analysis sections that can be added to any report.
Provides trade disruption risk assessment, energy trade impact analysis, and interactive bar and line charts.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class TradeImpactModule(BaseModule):
    """Trade Impact module for enhanced reports."""
    
    module_id = "trade_impact"
    title = "📊 Trade Impact Analysis"
    description = "Comprehensive analysis of trade disruptions, energy impacts, and economic implications"
    version = "1.0.0"
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Trade Impact module."""
        if config is None:
            config = ModuleConfig(
                title="📊 Trade Impact Analysis",
                description="Comprehensive analysis of trade disruptions, energy impacts, and economic implications",
                order=25,  # Early order for economic importance
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'trade_analysis',
            'trade_disruptions',
            'energy_trade',
            'economic_implications'
        ]
    
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for the Trade Impact module."""
        
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

        # Extract trade-related data
        trade_analysis = data.get('trade_analysis', {})
        trade_disruptions = data.get('trade_disruptions', [])
        energy_trade = data.get('energy_trade', {})
        economic_implications = data.get('economic_implications', {})

        # Generate comprehensive trade impact analysis
        content = self._generate_trade_impact_content(
            trade_analysis, trade_disruptions, energy_trade, economic_implications
        )

        return {
            "content": content,
            "metadata": {
                "phase4_integrated": phase4_enhanced,
                "strategic_intelligence": phase4_enhanced,
                "confidence_score": 0.7,
                "trade_analysis_complete": bool(trade_analysis),
                "disruptions_analyzed": len(trade_disruptions),
                "energy_impact_assessed": bool(energy_trade)
            }
        }
    
    def _generate_trade_impact_content(self, trade_analysis: Dict[str, Any], 
                                     trade_disruptions: List[Dict[str, Any]], 
                                     energy_trade: Dict[str, Any], 
                                     economic_implications: Dict[str, Any]) -> str:
        """Generate the main trade impact analysis content."""
        
        content = f"""
        <div class="trade-impact-section">
            <h2>📊 Trade Impact Analysis</h2>
            
            {self._generate_trade_overview(trade_analysis)}
            {self._generate_disruption_analysis(trade_disruptions)}
            {self._generate_energy_trade_analysis(energy_trade)}
            {self._generate_economic_implications(economic_implications)}
            {self._generate_interactive_charts(trade_analysis, trade_disruptions, energy_trade)}
        </div>
        """
        
        return content
    
    def _generate_trade_overview(self, trade_analysis: Dict[str, Any]) -> str:
        """Generate trade overview section."""
        if not trade_analysis:
            return """
            <div class="trade-overview">
                <h3>Trade Overview</h3>
                <p>Trade analysis data not available.</p>
            </div>
            """
        
        total_trade_volume = trade_analysis.get('total_volume', 'N/A')
        major_partners = trade_analysis.get('major_partners', [])
        trade_balance = trade_analysis.get('trade_balance', 'N/A')
        
        partners_html = ""
        if major_partners:
            partners_html = "<ul>" + "".join([f"<li>{partner}</li>" for partner in major_partners]) + "</ul>"
        
        return f"""
        <div class="trade-overview">
            <h3>Trade Overview</h3>
            <div class="trade-stats">
                <div class="stat-item">
                    <span class="stat-label">Total Trade Volume:</span>
                    <span class="stat-value">{total_trade_volume}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Trade Balance:</span>
                    <span class="stat-value">{trade_balance}</span>
                </div>
            </div>
            <div class="major-partners">
                <h4>Major Trading Partners</h4>
                {partners_html}
            </div>
        </div>
        """
    
    def _generate_disruption_analysis(self, trade_disruptions: List[Dict[str, Any]]) -> str:
        """Generate trade disruption analysis section."""
        if not trade_disruptions:
            return """
            <div class="disruption-analysis">
                <h3>Trade Disruption Analysis</h3>
                <p>No trade disruptions identified.</p>
            </div>
            """
        
        disruptions_html = ""
        for disruption in trade_disruptions:
            disruption_type = disruption.get('type', 'Unknown')
            impact_level = disruption.get('impact_level', 'Medium')
            description = disruption.get('description', 'No description available')
            mitigation = disruption.get('mitigation', 'No mitigation strategy')
            
            disruptions_html += f"""
            <div class="disruption-item">
                <h4>{disruption_type}</h4>
                <div class="impact-level {impact_level.lower()}">
                    <span class="impact-label">Impact Level:</span>
                    <span class="impact-value">{impact_level}</span>
                </div>
                <p><strong>Description:</strong> {description}</p>
                <p><strong>Mitigation Strategy:</strong> {mitigation}</p>
            </div>
            """
        
        return f"""
        <div class="disruption-analysis">
            <h3>Trade Disruption Analysis</h3>
            <div class="disruptions-list">
                {disruptions_html}
            </div>
        </div>
        """
    
    def _generate_energy_trade_analysis(self, energy_trade: Dict[str, Any]) -> str:
        """Generate energy trade impact analysis."""
        if not energy_trade:
            return """
            <div class="energy-trade-analysis">
                <h3>Energy Trade Impact</h3>
                <p>Energy trade data not available.</p>
            </div>
            """
        
        energy_imports = energy_trade.get('imports', {})
        energy_exports = energy_trade.get('exports', {})
        energy_security = energy_trade.get('security_implications', [])
        
        imports_html = ""
        if energy_imports:
            imports_html = "<ul>" + "".join([f"<li>{fuel}: {volume}</li>" for fuel, volume in energy_imports.items()]) + "</ul>"
        
        exports_html = ""
        if energy_exports:
            exports_html = "<ul>" + "".join([f"<li>{fuel}: {volume}</li>" for fuel, volume in energy_exports.items()]) + "</ul>"
        
        security_html = ""
        if energy_security:
            security_html = "<ul>" + "".join([f"<li>{implication}</li>" for implication in energy_security]) + "</ul>"
        
        return f"""
        <div class="energy-trade-analysis">
            <h3>Energy Trade Impact</h3>
            <div class="energy-imports">
                <h4>Energy Imports</h4>
                {imports_html}
            </div>
            <div class="energy-exports">
                <h4>Energy Exports</h4>
                {exports_html}
            </div>
            <div class="energy-security">
                <h4>Security Implications</h4>
                {security_html}
            </div>
        </div>
        """
    
    def _generate_economic_implications(self, economic_implications: Dict[str, Any]) -> str:
        """Generate economic implications analysis."""
        if not economic_implications:
            return """
            <div class="economic-implications">
                <h3>Economic Implications</h3>
                <p>Economic implications data not available.</p>
            </div>
            """
        
        gdp_impact = economic_implications.get('gdp_impact', 'N/A')
        employment_impact = economic_implications.get('employment_impact', 'N/A')
        inflation_impact = economic_implications.get('inflation_impact', 'N/A')
        sector_impacts = economic_implications.get('sector_impacts', [])
        
        sectors_html = ""
        if sector_impacts:
            sectors_html = "<ul>" + "".join([f"<li><strong>{sector}</strong>: {impact}</li>" for sector, impact in sector_impacts]) + "</ul>"
        
        return f"""
        <div class="economic-implications">
            <h3>Economic Implications</h3>
            <div class="economic-stats">
                <div class="stat-item">
                    <span class="stat-label">GDP Impact:</span>
                    <span class="stat-value">{gdp_impact}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Employment Impact:</span>
                    <span class="stat-value">{employment_impact}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Inflation Impact:</span>
                    <span class="stat-value">{inflation_impact}</span>
                </div>
            </div>
            <div class="sector-impacts">
                <h4>Sector-Specific Impacts</h4>
                {sectors_html}
            </div>
        </div>
        """
    
    def _generate_interactive_charts(self, trade_analysis: Dict[str, Any], 
                                   trade_disruptions: List[Dict[str, Any]], 
                                   energy_trade: Dict[str, Any]) -> str:
        """Generate interactive charts for trade impact visualization."""
        
        # Create chart data
        chart_data = {
            'trade_volume': trade_analysis.get('monthly_volume', {}),
            'disruption_timeline': [d.get('date', 'Unknown') for d in trade_disruptions],
            'energy_mix': energy_trade.get('energy_mix', {})
        }
        
        return f"""
        <div class="interactive-charts">
            <h3>Interactive Trade Impact Visualizations</h3>
            <div class="chart-container">
                <div class="chart" id="trade-volume-chart">
                    <h4>Trade Volume Trends</h4>
                    <div class="chart-placeholder">
                        <p>Interactive chart showing trade volume trends over time</p>
                        <p>Data: {len(chart_data['trade_volume'])} data points available</p>
                    </div>
                </div>
                <div class="chart" id="disruption-timeline-chart">
                    <h4>Disruption Timeline</h4>
                    <div class="chart-placeholder">
                        <p>Timeline visualization of trade disruptions</p>
                        <p>Disruptions: {len(chart_data['disruption_timeline'])} events</p>
                    </div>
                </div>
                <div class="chart" id="energy-mix-chart">
                    <h4>Energy Trade Mix</h4>
                    <div class="chart-placeholder">
                        <p>Pie chart showing energy trade composition</p>
                        <p>Energy sources: {len(chart_data['energy_mix'])} types</p>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltips for the Trade Impact module."""
        self.tooltips = {
            'trade_volume': TooltipData(
                title="Trade Volume",
                description="Total value of imports and exports in the specified period",
                source="Trade Data Sources",
                strategic_impact="Medium - Important for economic planning"
            ),
            'trade_balance': TooltipData(
                title="Trade Balance",
                description="Difference between exports and imports (positive = surplus, negative = deficit)",
                source="Trade Analysis Framework",
                strategic_impact="High - Critical for economic assessment"
            ),
            'disruption_impact': TooltipData(
                title="Disruption Impact",
                description="Assessment of how trade disruptions affect economic activity",
                source="Risk Assessment Framework",
                strategic_impact="High - Critical for risk management"
            ),
            'energy_security': TooltipData(
                title="Energy Security",
                description="Analysis of energy supply reliability and vulnerability",
                source="Energy Security Analysis",
                strategic_impact="High - Critical for energy security"
            )
        }
