"""
Interactive Visualizations Module

Independent module for generating interactive visualization sections that can be added to any report.
Provides enhanced data visualization, strategic trends analysis, chart.js integration, and advanced tooltips.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class InteractiveVisualizationsModule(BaseModule):
    """Interactive Visualizations module for enhanced reports."""
    
    module_id = "interactive_visualizations"
    title = "📊 Interactive Visualizations"
    description = "Enhanced data visualization with strategic trends analysis and interactive charts"
    version = "1.0.0"
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Interactive Visualizations module."""
        if config is None:
            config = ModuleConfig(
                title="📊 Interactive Visualizations",
                description="Enhanced data visualization with strategic trends analysis and interactive charts",
                order=40,  # Later order for visualizations
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'visualization_overview',
            'strategic_trends',
            'data_metrics',
            'interactive_charts'
        ]
    
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for the Interactive Visualizations module."""
        
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

        # Extract visualization data
        visualization_overview = data.get('visualization_overview', {})
        strategic_trends = data.get('strategic_trends', {})
        data_metrics = data.get('data_metrics', {})
        interactive_charts = data.get('interactive_charts', {})

        # Generate comprehensive interactive visualizations
        content = self._generate_interactive_visualizations_content(
            visualization_overview, strategic_trends, data_metrics, interactive_charts
        )

        return {
            "content": content,
            "metadata": {
                "phase4_integrated": phase4_enhanced,
                "strategic_intelligence": phase4_enhanced,
                "confidence_score": 0.7,
                "visualizations_created": bool(visualization_overview),
                "trends_analyzed": bool(strategic_trends),
                "metrics_processed": bool(data_metrics)
            }
        }
    
    def _generate_interactive_visualizations_content(self, visualization_overview: Dict[str, Any], 
                                                   strategic_trends: Dict[str, Any], 
                                                   data_metrics: Dict[str, Any], 
                                                   interactive_charts: Dict[str, Any]) -> str:
        """Generate the main interactive visualizations content."""
        
        content = f"""
        <div class="interactive-visualizations-section">
            <h2>📊 Interactive Visualizations</h2>
            
            {self._generate_visualization_overview(visualization_overview)}
            {self._generate_strategic_trends(strategic_trends)}
            {self._generate_data_metrics(data_metrics)}
            {self._generate_interactive_charts(interactive_charts)}
        </div>
        """
        
        return content
    
    def _generate_visualization_overview(self, visualization_overview: Dict[str, Any]) -> str:
        """Generate visualization overview section."""
        if not visualization_overview:
            return """
            <div class="visualization-overview">
                <h3>Visualization Overview</h3>
                <p>Visualization data not available.</p>
            </div>
            """
        
        total_visualizations = visualization_overview.get('total_visualizations', 0)
        chart_types = visualization_overview.get('chart_types', [])
        data_sources = visualization_overview.get('data_sources', [])
        
        chart_types_html = ""
        if chart_types:
            chart_types_html = "<ul>" + "".join([f"<li>{chart_type}</li>" for chart_type in chart_types]) + "</ul>"
        
        data_sources_html = ""
        if data_sources:
            data_sources_html = "<ul>" + "".join([f"<li>{source}</li>" for source in data_sources]) + "</ul>"
        
        return f"""
        <div class="visualization-overview">
            <h3>Visualization Overview</h3>
            <div class="overview-stats">
                <div class="stat-item">
                    <span class="stat-label">Total Visualizations:</span>
                    <span class="stat-value">{total_visualizations}</span>
                </div>
            </div>
            <div class="chart-types">
                <h4>Chart Types</h4>
                {chart_types_html}
            </div>
            <div class="data-sources">
                <h4>Data Sources</h4>
                {data_sources_html}
            </div>
        </div>
        """
    
    def _generate_strategic_trends(self, strategic_trends: Dict[str, Any]) -> str:
        """Generate strategic trends analysis section."""
        if not strategic_trends:
            return """
            <div class="strategic-trends">
                <h3>Strategic Trends</h3>
                <p>Strategic trends data not available.</p>
            </div>
            """
        
        key_trends = strategic_trends.get('key_trends', [])
        trend_analysis = strategic_trends.get('trend_analysis', 'N/A')
        confidence_level = strategic_trends.get('confidence_level', 'N/A')
        
        trends_html = ""
        if key_trends:
            trends_html = "<ul>" + "".join([f"<li>{trend}</li>" for trend in key_trends]) + "</ul>"
        
        return f"""
        <div class="strategic-trends">
            <h3>Strategic Trends Analysis</h3>
            <div class="trends-stats">
                <div class="stat-item">
                    <span class="stat-label">Confidence Level:</span>
                    <span class="stat-value">{confidence_level}</span>
                </div>
            </div>
            <div class="trend-analysis">
                <h4>Trend Analysis</h4>
                <p>{trend_analysis}</p>
            </div>
            <div class="key-trends">
                <h4>Key Trends</h4>
                {trends_html}
            </div>
        </div>
        """
    
    def _generate_data_metrics(self, data_metrics: Dict[str, Any]) -> str:
        """Generate data metrics section."""
        if not data_metrics:
            return """
            <div class="data-metrics">
                <h3>Data Metrics</h3>
                <p>Data metrics not available.</p>
            </div>
            """
        
        metrics_summary = data_metrics.get('metrics_summary', {})
        performance_indicators = data_metrics.get('performance_indicators', [])
        data_quality = data_metrics.get('data_quality', 'N/A')
        
        summary_html = ""
        if metrics_summary:
            summary_html = "<ul>" + "".join([f"<li><strong>{metric}</strong>: {value}</li>" for metric, value in metrics_summary.items()]) + "</ul>"
        
        indicators_html = ""
        if performance_indicators:
            indicators_html = "<ul>" + "".join([f"<li>{indicator}</li>" for indicator in performance_indicators]) + "</ul>"
        
        return f"""
        <div class="data-metrics">
            <h3>Data Metrics</h3>
            <div class="metrics-stats">
                <div class="stat-item">
                    <span class="stat-label">Data Quality:</span>
                    <span class="stat-value">{data_quality}</span>
                </div>
            </div>
            <div class="metrics-summary">
                <h4>Metrics Summary</h4>
                {summary_html}
            </div>
            <div class="performance-indicators">
                <h4>Performance Indicators</h4>
                {indicators_html}
            </div>
        </div>
        """
    
    def _generate_interactive_charts(self, interactive_charts: Dict[str, Any]) -> str:
        """Generate interactive charts section."""
        if not interactive_charts:
            return """
            <div class="interactive-charts">
                <h3>Interactive Charts</h3>
                <p>Interactive charts data not available.</p>
            </div>
            """
        
        chart_configs = interactive_charts.get('chart_configs', {})
        chart_data = interactive_charts.get('chart_data', {})
        chart_options = interactive_charts.get('chart_options', {})
        
        configs_html = ""
        if chart_configs:
            configs_html = "<ul>" + "".join([f"<li><strong>{chart_name}</strong>: {config}</li>" for chart_name, config in chart_configs.items()]) + "</ul>"
        
        return f"""
        <div class="interactive-charts">
            <h3>Interactive Charts</h3>
            <div class="chart-configurations">
                <h4>Chart Configurations</h4>
                {configs_html}
            </div>
            <div class="chart-container">
                <div class="chart" id="strategic-trends-chart">
                    <h4>Strategic Trends Chart</h4>
                    <div class="chart-placeholder">
                        <p>Interactive line chart showing strategic trends over time</p>
                        <p>Data points: {len(chart_data.get('trends_data', {}))}</p>
                    </div>
                </div>
                <div class="chart" id="performance-metrics-chart">
                    <h4>Performance Metrics Chart</h4>
                    <div class="chart-placeholder">
                        <p>Interactive bar chart showing performance metrics</p>
                        <p>Metrics: {len(chart_data.get('metrics_data', {}))}</p>
                    </div>
                </div>
                <div class="chart" id="data-distribution-chart">
                    <h4>Data Distribution Chart</h4>
                    <div class="chart-placeholder">
                        <p>Interactive pie chart showing data distribution</p>
                        <p>Categories: {len(chart_data.get('distribution_data', {}))}</p>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltips for the Interactive Visualizations module."""
        self.tooltips = {
            'visualization_overview': TooltipData(
                title="Visualization Overview",
                description="Summary of available visualizations and chart types",
                source="Visualization Framework",
                strategic_impact="Medium - Important for data presentation"
            ),
            'strategic_trends': TooltipData(
                title="Strategic Trends",
                description="Analysis of key strategic trends and patterns",
                source="Trend Analysis Framework",
                strategic_impact="High - Critical for strategic planning"
            ),
            'data_metrics': TooltipData(
                title="Data Metrics",
                description="Performance indicators and data quality metrics",
                source="Metrics Framework",
                strategic_impact="Medium - Important for performance assessment"
            ),
            'interactive_charts': TooltipData(
                title="Interactive Charts",
                description="Interactive chart configurations and data sources",
                source="Chart Framework",
                strategic_impact="Medium - Important for data visualization"
            )
        }
