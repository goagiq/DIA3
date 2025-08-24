"""
Adaptive Executive Summary Module

Enhanced executive summary module that can adapt to any data structure.
Provides intelligent content generation, dynamic metrics display, and flexible analysis.
"""

from typing import Dict, Any, List, Optional
from .adaptive_base_module import AdaptiveBaseModule, AdaptiveModuleConfig, AdaptiveTooltipData


class AdaptiveExecutiveSummaryModule(AdaptiveBaseModule):
    """Adaptive Executive Summary module for enhanced reports."""
    
    def __init__(self, config: Optional[AdaptiveModuleConfig] = None):
        """Initialize the Adaptive Executive Summary module."""
        if config is None:
            config = AdaptiveModuleConfig(
                title="📊 Adaptive Executive Summary",
                description="Intelligent executive summary that adapts to any data structure",
                order=1,  # First order to appear at the beginning
                tooltips_enabled=True,
                charts_enabled=True,
                adaptive_mode=True,
                fallback_content=True,
                data_patterns={
                    'summary': ['executive_summary', 'summary', 'overview', 'key_findings'],
                    'metrics': ['key_metrics', 'metrics', 'indicators', 'performance_indicators'],
                    'trends': ['trend_analysis', 'trends', 'patterns', 'current_trends'],
                    'insights': ['strategic_insights', 'insights', 'findings', 'analysis'],
                    'recommendations': ['recommendations', 'suggestions', 'actions', 'next_steps']
                }
            )
        super().__init__(config)
        
        # Initialize adaptive tooltips
        self._initialize_adaptive_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module (adaptive - no specific requirements)."""
        return []  # Adaptive modules don't require specific keys
    
    def _initialize_adaptive_tooltips(self):
        """Initialize adaptive tooltips for the executive summary module."""
        tooltip_data = [
            AdaptiveTooltipData(
                title="Executive Summary",
                description="Comprehensive overview of key findings and strategic insights",
                source="Adaptive Analysis System",
                strategic_impact="Provides high-level strategic context for decision making",
                recommendations="Use as a starting point for detailed analysis",
                data_type="summary"
            ),
            AdaptiveTooltipData(
                title="Key Metrics",
                description="Quantitative indicators and performance measures",
                source="Adaptive Analysis System",
                strategic_impact="Enables data-driven decision making and progress tracking",
                recommendations="Monitor trends and set benchmarks based on these metrics",
                data_type="metrics"
            ),
            AdaptiveTooltipData(
                title="Trend Analysis",
                description="Patterns and trends identified in the data",
                source="Adaptive Analysis System",
                strategic_impact="Helps predict future developments and plan accordingly",
                recommendations="Use trends to inform strategic planning and risk assessment",
                data_type="trends"
            ),
            AdaptiveTooltipData(
                title="Strategic Insights",
                description="Key insights and implications for strategic decision making",
                source="Adaptive Analysis System",
                strategic_impact="Guides strategic direction and resource allocation",
                recommendations="Incorporate insights into strategic planning processes",
                data_type="insights"
            )
        ]
        
        for tooltip in tooltip_data:
            self.add_tooltip(tooltip.data_type, tooltip)
    
    def _generate_main_content(self, relevant_data: Dict[str, Any]) -> str:
        """Generate enhanced main content with executive summary focus."""
        if not relevant_data:
            return self._generate_empty_content()
        
        content_sections = []
        
        # Generate executive overview
        overview_html = self._generate_executive_overview(relevant_data)
        if overview_html:
            content_sections.append(overview_html)
        
        # Generate key metrics dashboard
        metrics_html = self._generate_metrics_dashboard(relevant_data)
        if metrics_html:
            content_sections.append(metrics_html)
        
        # Generate trend analysis
        trends_html = self._generate_trend_analysis(relevant_data)
        if trends_html:
            content_sections.append(trends_html)
        
        # Generate strategic insights
        insights_html = self._generate_strategic_insights(relevant_data)
        if insights_html:
            content_sections.append(insights_html)
        
        # Generate recommendations
        recommendations_html = self._generate_recommendations(relevant_data)
        if recommendations_html:
            content_sections.append(recommendations_html)
        
        if not content_sections:
            return self._generate_empty_content()
        
        return '\n'.join(content_sections)
    
    def _generate_executive_overview(self, relevant_data: Dict[str, Any]) -> str:
        """Generate executive overview section."""
        summary_data = relevant_data.get('summary', {})
        
        if isinstance(summary_data, dict):
            title = summary_data.get('title', 'Executive Summary')
            overview = summary_data.get('overview', summary_data.get('summary', 'No overview available.'))
            key_findings = summary_data.get('key_findings', [])
            confidence_level = summary_data.get('confidence_level', 0.0)
        elif isinstance(summary_data, str):
            title = 'Executive Summary'
            overview = summary_data
            key_findings = []
            confidence_level = 0.0
        else:
            return ""
        
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
                <li data-tooltip-{self.module_id}="summary">
                    {finding}
                </li>
                """
            findings_html += """
                </ul>
            </div>
            """
        
        confidence_bar = self._generate_confidence_bar(confidence_level)
        
        return f"""
        <div class="executive-overview">
            <div class="overview-header" data-tooltip-{self.module_id}="summary">
                <h3>{title}</h3>
                {confidence_bar}
            </div>
            <div class="overview-content">
                <p>{overview}</p>
                {findings_html}
            </div>
        </div>
        """
    
    def _generate_metrics_dashboard(self, relevant_data: Dict[str, Any]) -> str:
        """Generate key metrics dashboard."""
        metrics_data = relevant_data.get('metrics', {})
        
        if not metrics_data:
            return ""
        
        metrics_html = """
        <div class="metrics-dashboard">
            <h3>📈 Key Metrics Dashboard</h3>
            <div class="metrics-grid">
        """
        
        if isinstance(metrics_data, dict):
            for key, value in metrics_data.items():
                if isinstance(value, (int, float)):
                    metrics_html += f"""
                    <div class="metric-card" data-tooltip-{self.module_id}="metrics">
                        <div class="metric-value">{value}</div>
                        <div class="metric-label">{self._format_key(key)}</div>
                    </div>
                    """
                elif isinstance(value, str):
                    metrics_html += f"""
                    <div class="metric-card" data-tooltip-{self.module_id}="metrics">
                        <div class="metric-value">{value}</div>
                        <div class="metric-label">{self._format_key(key)}</div>
                    </div>
                    """
        
        metrics_html += """
            </div>
        </div>
        """
        
        return metrics_html
    
    def _generate_trend_analysis(self, relevant_data: Dict[str, Any]) -> str:
        """Generate trend analysis section."""
        trends_data = relevant_data.get('trends', {})
        
        if not trends_data:
            return ""
        
        trends_html = """
        <div class="trend-analysis">
            <h3>📊 Trend Analysis</h3>
        """
        
        if isinstance(trends_data, dict):
            for key, value in trends_data.items():
                if isinstance(value, str):
                    trends_html += f"""
                    <div class="trend-item" data-tooltip-{self.module_id}="trends">
                        <h4>{self._format_key(key)}</h4>
                        <p>{value}</p>
                    </div>
                    """
                elif isinstance(value, list):
                    trends_html += f"""
                    <div class="trend-item" data-tooltip-{self.module_id}="trends">
                        <h4>{self._format_key(key)}</h4>
                        <ul>
                            {''.join(f'<li>{item}</li>' for item in value[:5])}
                        </ul>
                    </div>
                    """
        
        trends_html += """
        </div>
        """
        
        return trends_html
    
    def _generate_strategic_insights(self, relevant_data: Dict[str, Any]) -> str:
        """Generate strategic insights section."""
        insights_data = relevant_data.get('insights', {})
        
        if not insights_data:
            return ""
        
        insights_html = """
        <div class="strategic-insights">
            <h3>💡 Strategic Insights</h3>
        """
        
        if isinstance(insights_data, dict):
            for key, value in insights_data.items():
                if isinstance(value, str):
                    insights_html += f"""
                    <div class="insight-item" data-tooltip-{self.module_id}="insights">
                        <h4>{self._format_key(key)}</h4>
                        <p>{value}</p>
                    </div>
                    """
                elif isinstance(value, list):
                    insights_html += f"""
                    <div class="insight-item" data-tooltip-{self.module_id}="insights">
                        <h4>{self._format_key(key)}</h4>
                        <ul>
                            {''.join(f'<li>{item}</li>' for item in value[:5])}
                        </ul>
                    </div>
                    """
        
        insights_html += """
        </div>
        """
        
        return insights_html
    
    def _generate_recommendations(self, relevant_data: Dict[str, Any]) -> str:
        """Generate recommendations section."""
        recommendations_data = relevant_data.get('recommendations', {})
        
        if not recommendations_data:
            return ""
        
        recommendations_html = """
        <div class="recommendations">
            <h3>🎯 Strategic Recommendations</h3>
        """
        
        if isinstance(recommendations_data, dict):
            for key, value in recommendations_data.items():
                if isinstance(value, list):
                    recommendations_html += f"""
                    <div class="recommendation-category">
                        <h4>{self._format_key(key)}</h4>
                        <ul>
                            {''.join(f'<li>{item}</li>' for item in value[:5])}
                        </ul>
                    </div>
                    """
                elif isinstance(value, str):
                    recommendations_html += f"""
                    <div class="recommendation-category">
                        <h4>{self._format_key(key)}</h4>
                        <p>{value}</p>
                    </div>
                    """
        
        recommendations_html += """
        </div>
        """
        
        return recommendations_html
    
    def _generate_confidence_bar(self, confidence_level: float) -> str:
        """Generate confidence level visualization."""
        confidence_percentage = min(max(confidence_level * 100, 0), 100)
        confidence_color = self._get_confidence_color(confidence_percentage)
        
        return f"""
        <div class="confidence-indicator">
            <span class="confidence-label">Confidence Level:</span>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: {confidence_percentage}%; background-color: {confidence_color};"></div>
            </div>
            <span class="confidence-value">{confidence_percentage:.1f}%</span>
        </div>
        """
    
    def _get_confidence_color(self, confidence_percentage: float) -> str:
        """Get color for confidence level."""
        if confidence_percentage >= 80:
            return "#28a745"  # Green
        elif confidence_percentage >= 60:
            return "#ffc107"  # Yellow
        elif confidence_percentage >= 40:
            return "#fd7e14"  # Orange
        else:
            return "#dc3545"  # Red
    
    def _generate_empty_content(self) -> str:
        """Generate content when no relevant data is found."""
        return f"""
        <div class="empty-content">
            <h3>📊 Adaptive Executive Summary</h3>
            <p>This executive summary module is operating in adaptive mode.</p>
            <p>No specific executive summary data was found in the provided dataset.</p>
            <div class="adaptive-info">
                <p><strong>Adaptive Mode:</strong> This module automatically adapts to any data structure.</p>
                <p><strong>Available Data:</strong> The module will display content when relevant information is provided.</p>
                <p><strong>Fallback Content:</strong> Generated when specific data patterns are not found.</p>
            </div>
        </div>
        """
    
    def _generate_adaptive_visualizations(self, relevant_data: Dict[str, Any]) -> str:
        """Generate enhanced adaptive visualizations for executive summary."""
        if not self.config.charts_enabled:
            return ""
        
        visualizations_html = []
        
        # Generate metrics chart if metrics data is available
        metrics_data = relevant_data.get('metrics', {})
        if metrics_data and isinstance(metrics_data, dict):
            metrics_chart = self._generate_metrics_chart(metrics_data)
            if metrics_chart:
                visualizations_html.append(metrics_chart)
        
        # Generate trends chart if trends data is available
        trends_data = relevant_data.get('trends', {})
        if trends_data and isinstance(trends_data, dict):
            trends_chart = self._generate_trends_chart(trends_data)
            if trends_chart:
                visualizations_html.append(trends_chart)
        
        if not visualizations_html:
            return ""
        
        return f"""
        <div class="executive-visualizations">
            <h3>📊 Executive Visualizations</h3>
            {''.join(visualizations_html)}
        </div>
        """
    
    def _generate_metrics_chart(self, metrics_data: Dict[str, Any]) -> str:
        """Generate a chart for metrics data."""
        numeric_data = {k: v for k, v in metrics_data.items() if isinstance(v, (int, float))}
        
        if not numeric_data:
            return ""
        
        chart_id = f"executive_metrics_chart"
        
        return f"""
        <div class="chart-container">
            <h4>Key Metrics Overview</h4>
            <canvas id="{chart_id}" width="400" height="200"></canvas>
            <script>
                // Executive metrics chart configuration
                const {chart_id}Data = {numeric_data};
                // Chart rendering logic would go here
            </script>
        </div>
        """
    
    def _generate_trends_chart(self, trends_data: Dict[str, Any]) -> str:
        """Generate a chart for trends data."""
        chart_id = f"executive_trends_chart"
        
        return f"""
        <div class="chart-container">
            <h4>Trend Analysis Overview</h4>
            <div class="trends-summary">
                <p><strong>Trend Categories:</strong> {len(trends_data)}</p>
                <p><strong>Data Type:</strong> Trend Analysis</p>
            </div>
        </div>
        """
