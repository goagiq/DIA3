"""
Executive Summary Module

Independent module for generating executive summary sections that can be added to any report.
Provides configurable metrics display, trend indicators, and strategic impact assessment.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class ExecutiveSummaryModule(BaseModule):
    """Executive Summary module for enhanced reports."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Executive Summary module."""
        if config is None:
            config = ModuleConfig(
                title="📊 Executive Summary",
                description="Comprehensive executive summary with key metrics and strategic insights",
                order=1,  # First order to appear at the beginning
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'executive_summary',
            'key_metrics',
            'trend_analysis',
            'strategic_insights'
        ]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Executive Summary module."""
        self.validate_data(data)
        
        executive_summary = data.get('executive_summary', {})
        key_metrics = data.get('key_metrics', {})
        trend_analysis = data.get('trend_analysis', {})
        strategic_insights = data.get('strategic_insights', [])
        
        # Generate executive summary overview
        overview_html = self._generate_overview(executive_summary)
        
        # Generate key metrics section
        metrics_html = self._generate_key_metrics(key_metrics)
        
        # Generate trend analysis
        trends_html = self._generate_trend_analysis(trend_analysis)
        
        # Generate strategic insights
        insights_html = self._generate_strategic_insights(strategic_insights)
        
        return f"""
        <div class="section" id="executive-summary">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {metrics_html}
            {trends_html}
            {insights_html}
        </div>
        """
    
    def _generate_overview(self, summary_data: Dict[str, Any]) -> str:
        """Generate the executive summary overview section."""
        title = summary_data.get('title', 'Executive Summary')
        overview = summary_data.get('overview', 'No overview available.')
        key_findings = summary_data.get('key_findings', [])
        confidence_level = summary_data.get('confidence_level', 0.0)
        
        findings_html = ""
        if key_findings:
            findings_html = """
            <div class="key-findings">
                <h4>🔍 Key Findings</h4>
                <ul>
            """
            for i, finding in enumerate(key_findings):
                finding_id = f"finding_{i}"
                findings_html += f"""
                <li data-tooltip-{self.module_id}="{finding_id}">
                    {finding}
                </li>
                """
            findings_html += """
                </ul>
            </div>
            """
        
        return f"""
        <div class="executive-overview">
            <div class="overview-header" data-tooltip-{self.module_id}="executive_overview">
                <h3>{title}</h3>
                <div class="confidence-indicator">
                    <span class="confidence-label">Confidence Level:</span>
                    <span class="confidence-value">{confidence_level:.1f}%</span>
                </div>
            </div>
            <div class="overview-content">
                <p>{overview}</p>
            </div>
            {findings_html}
        </div>
        """
    
    def _generate_key_metrics(self, metrics_data: Dict[str, Any]) -> str:
        """Generate the key metrics section."""
        metrics = metrics_data.get('metrics', {})
        
        if not metrics:
            return "<p>No key metrics available.</p>"
        
        metrics_html = """
        <div class="key-metrics-section">
            <h3>📈 Key Metrics</h3>
            <div class="metrics-grid">
        """
        
        for metric_name, metric_data in metrics.items():
            if isinstance(metric_data, dict):
                value = metric_data.get('value', 'N/A')
                trend = metric_data.get('trend', 'neutral')
                description = metric_data.get('description', '')
                metric_id = f"metric_{metric_name.lower().replace(' ', '_')}"
                
                trend_icon = self._get_trend_icon(trend)
                trend_class = f"trend-{trend}"
                
                metrics_html += f"""
                <div class="metric-card" data-tooltip-{self.module_id}="{metric_id}">
                    <div class="metric-header">
                        <h4>{metric_name}</h4>
                        <span class="trend-indicator {trend_class}">{trend_icon}</span>
                    </div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-description">{description}</div>
                </div>
                """
        
        metrics_html += """
            </div>
        </div>
        """
        
        return metrics_html
    
    def _generate_trend_analysis(self, trend_data: Dict[str, Any]) -> str:
        """Generate the trend analysis section."""
        trends = trend_data.get('trends', [])
        
        if not trends:
            return "<p>No trend analysis available.</p>"
        
        trends_html = """
        <div class="trend-analysis-section">
            <h3>📊 Trend Analysis</h3>
            <div class="trends-container">
        """
        
        for i, trend in enumerate(trends):
            trend_id = f"trend_{i}"
            title = trend.get('title', 'Untitled Trend')
            description = trend.get('description', '')
            direction = trend.get('direction', 'neutral')
            impact = trend.get('impact', 'medium')
            
            direction_icon = self._get_trend_icon(direction)
            impact_class = f"impact-{impact}"
            
            trends_html += f"""
            <div class="trend-item {impact_class}" data-tooltip-{self.module_id}="{trend_id}">
                <div class="trend-header">
                    <h4>{title}</h4>
                    <span class="trend-direction">{direction_icon}</span>
                </div>
                <p>{description}</p>
            </div>
            """
        
        trends_html += """
            </div>
        </div>
        """
        
        return trends_html
    
    def _generate_strategic_insights(self, insights: List[Dict[str, Any]]) -> str:
        """Generate the strategic insights section."""
        if not insights:
            return "<p>No strategic insights available.</p>"
        
        insights_html = """
        <div class="strategic-insights-section">
            <h3>🎯 Strategic Insights</h3>
            <div class="insights-grid">
        """
        
        for i, insight in enumerate(insights):
            insight_id = f"insight_{i}"
            title = insight.get('title', 'Untitled Insight')
            description = insight.get('description', '')
            category = insight.get('category', 'General')
            priority = insight.get('priority', 'medium')
            
            priority_class = f"priority-{priority}"
            
            insights_html += f"""
            <div class="insight-card {priority_class}" data-tooltip-{self.module_id}="{insight_id}">
                <div class="insight-header">
                    <h4>{title}</h4>
                    <span class="insight-category">{category}</span>
                </div>
                <p>{description}</p>
            </div>
            """
        
        insights_html += """
            </div>
        </div>
        """
        
        return insights_html
    
    def _get_trend_icon(self, trend: str) -> str:
        """Get the appropriate icon for a trend direction."""
        trend_icons = {
            'up': '📈',
            'down': '📉',
            'stable': '➡️',
            'neutral': '➡️',
            'positive': '📈',
            'negative': '📉'
        }
        return trend_icons.get(trend.lower(), '➡️')
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        # Executive overview tooltip
        self.add_tooltip("executive_overview", TooltipData(
            title="Executive Summary Overview",
            description="High-level summary of the analysis with key findings and confidence assessment.",
            source="Source: Executive Analysis Framework",
            strategic_impact="Provides critical context for decision-making and strategic planning.",
            recommendations="• Review findings with stakeholders\n• Validate confidence levels\n• Update metrics regularly",
            use_cases="• Board presentations\n• Strategic planning\n• Executive briefings\n• Decision support",
            confidence=95.0
        ))
        
        # Key findings tooltips
        self.add_tooltip("finding_0", TooltipData(
            title="Key Finding Analysis",
            description="Critical insights derived from comprehensive analysis.",
            source="Source: Multi-source Intelligence Analysis",
            strategic_impact="Direct influence on strategic decision-making and resource allocation.",
            recommendations="• Prioritize findings by impact\n• Develop response strategies\n• Monitor implementation",
            use_cases="• Strategic planning\n• Risk assessment\n• Resource allocation\n• Policy development",
            confidence=90.0
        ))
        
        # Metrics tooltips
        self.add_tooltip("metric_performance", TooltipData(
            title="Performance Metrics",
            description="Quantitative measures of system or process performance.",
            source="Source: Performance Monitoring Systems",
            strategic_impact="Essential for performance evaluation and improvement initiatives.",
            recommendations="• Establish baseline metrics\n• Set performance targets\n• Monitor trends regularly",
            use_cases="• Performance management\n• Process improvement\n• Benchmarking\n• Goal setting",
            confidence=85.0
        ))
        
        # Trend analysis tooltips
        self.add_tooltip("trend_0", TooltipData(
            title="Trend Analysis",
            description="Analysis of patterns and directions in key indicators over time.",
            source="Source: Historical Data Analysis",
            strategic_impact="Critical for forecasting and strategic planning.",
            recommendations="• Monitor trend changes\n• Adjust strategies accordingly\n• Plan for contingencies",
            use_cases="• Forecasting\n• Strategic planning\n• Risk management\n• Market analysis",
            confidence=88.0
        ))
        
        # Strategic insights tooltips
        self.add_tooltip("insight_0", TooltipData(
            title="Strategic Insight",
            description="Strategic-level insights derived from comprehensive analysis.",
            source="Source: Strategic Analysis Framework",
            strategic_impact="Direct influence on strategic direction and decision-making.",
            recommendations="• Prioritize insights by impact\n• Develop action plans\n• Monitor implementation",
            use_cases="• Strategic planning\n• Executive decision-making\n• Policy development\n• Resource allocation",
            confidence=92.0
        ))
    
    def add_metric_tooltip(self, metric_id: str, tooltip_data: TooltipData):
        """Add tooltip data for a specific metric."""
        self.add_tooltip(metric_id, tooltip_data)
    
    def add_trend_tooltip(self, trend_id: str, tooltip_data: TooltipData):
        """Add tooltip data for a specific trend."""
        self.add_tooltip(trend_id, tooltip_data)
    
    def add_insight_tooltip(self, insight_id: str, tooltip_data: TooltipData):
        """Add tooltip data for a specific insight."""
        self.add_tooltip(insight_id, tooltip_data)
    
    def get_executive_summary_summary(self) -> Dict[str, Any]:
        """Get a summary of the executive summary module."""
        return {
            'module_type': 'executive_summary',
            'title': self.get_title(),
            'enabled': self.is_enabled(),
            'tooltips_count': len(self.tooltip_data),
            'features': [
                'Executive Summary Overview',
                'Key Metrics Display',
                'Trend Analysis',
                'Strategic Insights',
                'Advanced Tooltips with Source References'
            ]
        }
