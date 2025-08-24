"""
Trade Impact Module

Independent module for generating trade impact analysis sections that can be added to any report.
Provides trade disruption risk assessment, energy trade impact analysis, and interactive bar and line charts.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class TradeImpactModule(BaseModule):
    """Trade Impact module for enhanced reports."""
    
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
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Trade Impact module."""
        self.validate_data(data)
        
        trade_analysis = data.get('trade_analysis', {})
        trade_disruptions = data.get('trade_disruptions', {})
        energy_trade = data.get('energy_trade', {})
        economic_implications = data.get('economic_implications', {})
        
        # Generate trade overview
        overview_html = self._generate_trade_overview(trade_analysis)
        
        # Generate trade disruption analysis
        disruptions_html = self._generate_trade_disruptions(trade_disruptions)
        
        # Generate energy trade analysis
        energy_html = self._generate_energy_trade_analysis(energy_trade)
        
        # Generate economic implications
        economic_html = self._generate_economic_implications(economic_implications)
        
        # Generate interactive visualizations
        visualizations_html = self._generate_interactive_visualizations(data)
        
        return f"""
        <div class="section" id="trade-impact">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {disruptions_html}
            {energy_html}
            {economic_html}
            {visualizations_html}
        </div>
        """
    
    def _generate_trade_overview(self, analysis_data: Dict[str, Any]) -> str:
        """Generate the trade analysis overview section."""
        title = analysis_data.get('title', 'Trade Impact Analysis')
        overview = analysis_data.get('overview', 'No trade overview available.')
        key_sectors = analysis_data.get('key_sectors', [])
        impact_level = analysis_data.get('impact_level', 'Medium')
        confidence_score = analysis_data.get('confidence_score', 0.0)
        
        sectors_html = ""
        if key_sectors:
            sectors_html = """
            <div class="key-sectors">
                <h4>🏭 Key Trade Sectors</h4>
                <div class="sectors-grid">
            """
            for i, sector in enumerate(key_sectors):
                sector_id = f"sector_{i}"
                sectors_html += f"""
                <div class="sector-card" data-tooltip-{self.module_id}="{sector_id}">
                    <h5>{sector.get('name', 'Unknown Sector')}</h5>
                    <p class="sector-role">{sector.get('role', 'No role specified')}</p>
                    <p class="sector-impact">Impact: {sector.get('impact_level', 'Medium')}</p>
                </div>
                """
            sectors_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="trade-overview">
            <div class="overview-header" data-tooltip-{self.module_id}="trade_overview">
                <h3>📊 Trade Overview</h3>
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
            {sectors_html}
        </div>
        """
    
    def _generate_trade_disruptions(self, disruptions_data: Dict[str, Any]) -> str:
        """Generate the trade disruption analysis section."""
        disruptions = disruptions_data.get('disruptions', [])
        risk_factors = disruptions_data.get('risk_factors', [])
        mitigation_strategies = disruptions_data.get('mitigation_strategies', [])
        
        disruptions_html = ""
        if disruptions:
            disruptions_html = """
            <div class="trade-disruptions">
                <h4>⚠️ Trade Disruptions</h4>
                <div class="disruptions-container">
            """
            for i, disruption in enumerate(disruptions):
                disruption_id = f"disruption_{i}"
                disruptions_html += f"""
                <div class="disruption-card" data-tooltip-{self.module_id}="{disruption_id}">
                    <h5>{disruption.get('name', 'Unknown Disruption')}</h5>
                    <div class="disruption-metrics">
                        <div class="metric">
                            <span class="label">Severity:</span>
                            <span class="value">{disruption.get('severity', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Duration:</span>
                            <span class="value">{disruption.get('duration', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Probability:</span>
                            <span class="value">{disruption.get('probability', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="disruption-description">{disruption.get('description', 'No description available.')}</p>
                </div>
                """
            disruptions_html += """
                </div>
            </div>
            """
        
        risks_html = ""
        if risk_factors:
            risks_html = """
            <div class="risk-factors">
                <h4>🎯 Risk Factors</h4>
                <ul>
            """
            for i, risk in enumerate(risk_factors):
                risk_id = f"risk_{i}"
                risks_html += f"""
                <li data-tooltip-{self.module_id}="{risk_id}">
                    <strong>{risk.get('factor', 'Unknown')}</strong>: {risk.get('description', 'No description')}
                    <span class="risk-level">({risk.get('level', 'Medium')})</span>
                </li>
                """
            risks_html += """
                </ul>
            </div>
            """
        
        mitigation_html = ""
        if mitigation_strategies:
            mitigation_html = """
            <div class="mitigation-strategies">
                <h4>🛡️ Mitigation Strategies</h4>
                <div class="strategies-grid">
            """
            for i, strategy in enumerate(mitigation_strategies):
                strategy_id = f"strategy_{i}"
                mitigation_html += f"""
                <div class="strategy-card" data-tooltip-{self.module_id}="{strategy_id}">
                    <h5>{strategy.get('name', 'Unknown Strategy')}</h5>
                    <p class="strategy-effectiveness">Effectiveness: {strategy.get('effectiveness', 'Medium')}</p>
                    <p class="strategy-description">{strategy.get('description', 'No description available.')}</p>
                </div>
                """
            mitigation_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="trade-disruptions-analysis">
            <h3>⚠️ Trade Disruption Analysis</h3>
            {disruptions_html}
            {risks_html}
            {mitigation_html}
        </div>
        """
    
    def _generate_energy_trade_analysis(self, energy_data: Dict[str, Any]) -> str:
        """Generate the energy trade impact analysis section."""
        energy_sectors = energy_data.get('energy_sectors', [])
        price_impacts = energy_data.get('price_impacts', {})
        supply_chains = energy_data.get('supply_chains', [])
        
        sectors_html = ""
        if energy_sectors:
            sectors_html = """
            <div class="energy-sectors">
                <h4>⚡ Energy Trade Sectors</h4>
                <div class="sectors-container">
            """
            for i, sector in enumerate(energy_sectors):
                sector_id = f"energy_sector_{i}"
                sectors_html += f"""
                <div class="energy-sector-card" data-tooltip-{self.module_id}="{sector_id}">
                    <h5>{sector.get('name', 'Unknown Energy Sector')}</h5>
                    <div class="sector-metrics">
                        <div class="metric">
                            <span class="label">Trade Volume:</span>
                            <span class="value">{sector.get('trade_volume', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Impact Level:</span>
                            <span class="value">{sector.get('impact_level', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Price Sensitivity:</span>
                            <span class="value">{sector.get('price_sensitivity', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="sector-description">{sector.get('description', 'No description available.')}</p>
                </div>
                """
            sectors_html += """
                </div>
            </div>
            """
        
        prices_html = ""
        if price_impacts:
            prices_html = """
            <div class="price-impacts">
                <h4>💰 Price Impact Analysis</h4>
                <div class="price-metrics">
            """
            for commodity, impact in price_impacts.items():
                prices_html += f"""
                <div class="price-metric">
                    <h5>{commodity.replace('_', ' ').title()}</h5>
                    <p class="price-change">{impact}</p>
                </div>
                """
            prices_html += """
                </div>
            </div>
            """
        
        supply_html = ""
        if supply_chains:
            supply_html = """
            <div class="supply-chains">
                <h4>🔗 Supply Chain Analysis</h4>
                <div class="chains-grid">
            """
            for i, chain in enumerate(supply_chains):
                chain_id = f"supply_chain_{i}"
                supply_html += f"""
                <div class="supply-chain-card" data-tooltip-{self.module_id}="{chain_id}">
                    <h5>{chain.get('name', 'Unknown Supply Chain')}</h5>
                    <p class="chain-vulnerability">Vulnerability: {chain.get('vulnerability', 'Medium')}</p>
                    <p class="chain-description">{chain.get('description', 'No description available.')}</p>
                </div>
                """
            supply_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="energy-trade-analysis">
            <h3>⚡ Energy Trade Impact Analysis</h3>
            {sectors_html}
            {prices_html}
            {supply_html}
        </div>
        """
    
    def _generate_economic_implications(self, economic_data: Dict[str, Any]) -> str:
        """Generate the economic implications analysis section."""
        gdp_impacts = economic_data.get('gdp_impacts', {})
        employment_effects = economic_data.get('employment_effects', {})
        currency_effects = economic_data.get('currency_effects', {})
        long_term_implications = economic_data.get('long_term_implications', 'No long-term implications available.')
        
        gdp_html = ""
        if gdp_impacts:
            gdp_html = """
            <div class="gdp-impacts">
                <h4>📈 GDP Impact Analysis</h4>
                <div class="gdp-metrics">
            """
            for country, impact in gdp_impacts.items():
                gdp_html += f"""
                <div class="gdp-metric">
                    <h5>{country}</h5>
                    <p class="gdp-change">{impact}</p>
                </div>
                """
            gdp_html += """
                </div>
            </div>
            """
        
        employment_html = ""
        if employment_effects:
            employment_html = """
            <div class="employment-effects">
                <h4>👥 Employment Effects</h4>
                <div class="employment-metrics">
            """
            for sector, effect in employment_effects.items():
                employment_html += f"""
                <div class="employment-metric">
                    <h5>{sector.replace('_', ' ').title()}</h5>
                    <p class="employment-change">{effect}</p>
                </div>
                """
            employment_html += """
                </div>
            </div>
            """
        
        currency_html = ""
        if currency_effects:
            currency_html = """
            <div class="currency-effects">
                <h4>💱 Currency Effects</h4>
                <div class="currency-metrics">
            """
            for currency, effect in currency_effects.items():
                currency_html += f"""
                <div class="currency-metric">
                    <h5>{currency}</h5>
                    <p class="currency-change">{effect}</p>
                </div>
                """
            currency_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="economic-implications">
            <h3>💰 Economic Implications</h3>
            {gdp_html}
            {employment_html}
            {currency_html}
            <div class="long-term-implications">
                <h4>🔮 Long-term Implications</h4>
                <p>{long_term_implications}</p>
            </div>
        </div>
        """
    
    def _generate_interactive_visualizations(self, data: Dict[str, Any]) -> str:
        """Generate interactive visualizations for trade analysis."""
        if not self.config.charts_enabled:
            return ""
        
        # Generate trade volume chart
        volume_chart_html = self._generate_trade_volume_chart(data)
        
        # Generate price impact chart
        price_chart_html = self._generate_price_impact_chart(data)
        
        return f"""
        <div class="trade-visualizations">
            <h3>📈 Interactive Visualizations</h3>
            {volume_chart_html}
            {price_chart_html}
        </div>
        """
    
    def _generate_trade_volume_chart(self, data: Dict[str, Any]) -> str:
        """Generate a bar chart for trade volume analysis."""
        trade_analysis = data.get('trade_analysis', {})
        sectors = trade_analysis.get('key_sectors', [])
        
        if not sectors:
            return ""
        
        # Prepare chart data
        labels = [sector.get('name', 'Unknown') for sector in sectors]
        volumes = [self._convert_volume_to_number(sector.get('trade_volume', 'Medium')) for sector in sectors]
        impacts = [self._convert_impact_to_number(sector.get('impact_level', 'Medium')) for sector in sectors]
        
        chart_id = f"trade_volume_{self.module_id}"
        
        # Add chart data to the module
        self.add_chart_data(chart_id, {
            'type': 'bar',
            'data': {
                'labels': labels,
                'datasets': [
                    {
                        'label': 'Trade Volume',
                        'data': volumes,
                        'backgroundColor': 'rgba(54, 162, 235, 0.8)',
                        'borderColor': 'rgba(54, 162, 235, 1)',
                        'borderWidth': 1
                    },
                    {
                        'label': 'Impact Level',
                        'data': impacts,
                        'backgroundColor': 'rgba(255, 99, 132, 0.8)',
                        'borderColor': 'rgba(255, 99, 132, 1)',
                        'borderWidth': 1
                    }
                ]
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
                        'text': 'Trade Volume and Impact Analysis'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>📊 Trade Volume by Sector</h4>
            <canvas id="{chart_id}" width="400" height="300"></canvas>
        </div>
        """
    
    def _generate_price_impact_chart(self, data: Dict[str, Any]) -> str:
        """Generate a line chart for price impact analysis."""
        energy_trade = data.get('energy_trade', {})
        price_impacts = energy_trade.get('price_impacts', {})
        
        if not price_impacts:
            return ""
        
        # Prepare chart data
        labels = list(price_impacts.keys())
        values = [self._convert_price_impact_to_number(impact) for impact in price_impacts.values()]
        
        chart_id = f"price_impact_{self.module_id}"
        
        # Add chart data to the module
        self.add_chart_data(chart_id, {
            'type': 'line',
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': 'Price Impact (%)',
                    'data': values,
                    'borderColor': 'rgba(255, 159, 64, 1)',
                    'backgroundColor': 'rgba(255, 159, 64, 0.2)',
                    'tension': 0.1,
                    'fill': True
                }]
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'scales': {
                    'y': {
                        'beginAtZero': True
                    }
                },
                'plugins': {
                    'legend': {
                        'position': 'top'
                    },
                    'title': {
                        'display': True,
                        'text': 'Commodity Price Impact Analysis'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>💰 Price Impact Analysis</h4>
            <canvas id="{chart_id}" width="400" height="300"></canvas>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        # Trade overview tooltips
        self.add_tooltip("trade_overview", TooltipData(
            title="Trade Overview",
            description="Comprehensive analysis of trade patterns, disruptions, and economic implications.",
            source="Trade Analysis Framework",
            strategic_impact="High - Critical for economic planning and policy development",
            recommendations="• Monitor trade flows regularly\n• Assess disruption risks\n• Develop mitigation strategies\n• Track economic impacts",
            use_cases="Used in economic planning, policy development, and risk assessment",
            confidence=90.0
        ))
        
        self.add_tooltip("trade_disruptions", TooltipData(
            title="Trade Disruptions",
            description="Analysis of potential trade disruptions and their impact on economic stability.",
            source="Risk Assessment Framework",
            strategic_impact="High - Essential for contingency planning",
            recommendations="• Identify high-risk trade routes\n• Develop alternative supply chains\n• Establish early warning systems\n• Plan mitigation strategies",
            use_cases="Used in supply chain management and risk assessment",
            confidence=85.0
        ))
        
        self.add_tooltip("energy_trade", TooltipData(
            title="Energy Trade Analysis",
            description="Comprehensive analysis of energy trade patterns and their economic implications.",
            source="Energy Analysis Framework",
            strategic_impact="High - Critical for energy security planning",
            recommendations="• Diversify energy sources\n• Monitor price volatility\n• Assess supply chain risks\n• Plan for energy transitions",
            use_cases="Used in energy policy and security planning",
            confidence=88.0
        ))
        
        self.add_tooltip("economic_implications", TooltipData(
            title="Economic Implications",
            description="Analysis of trade impacts on GDP, employment, and currency stability.",
            source="Economic Analysis Framework",
            strategic_impact="High - Critical for economic policy development",
            recommendations="• Monitor economic indicators\n• Assess employment impacts\n• Track currency effects\n• Plan economic responses",
            use_cases="Used in economic policy and planning",
            confidence=92.0
        ))
    
    def _convert_volume_to_number(self, volume: str) -> int:
        """Convert volume level to numerical value for charts."""
        volume_map = {
            'Very Low': 20,
            'Low': 40,
            'Medium': 60,
            'High': 80,
            'Very High': 100
        }
        return volume_map.get(volume, 60)
    
    def _convert_impact_to_number(self, impact: str) -> int:
        """Convert impact level to numerical value for charts."""
        impact_map = {
            'Very Low': 20,
            'Low': 40,
            'Medium': 60,
            'High': 80,
            'Very High': 100
        }
        return impact_map.get(impact, 60)
    
    def _convert_price_impact_to_number(self, impact: str) -> float:
        """Convert price impact string to numerical value for charts."""
        # Extract percentage from string like "15-20% increase" or "-10% decrease"
        import re
        numbers = re.findall(r'-?\d+', impact)
        if numbers:
            # Take the average if range is given
            values = [int(n) for n in numbers]
            return sum(values) / len(values)
        return 0.0
