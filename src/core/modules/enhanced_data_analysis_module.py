"""
Enhanced Data Analysis Module

Independent module for generating enhanced data analysis sections that can be added to any report.
Provides comprehensive data analysis, performance indicators, statistical analysis, and data visualization.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class EnhancedDataAnalysisModule(BaseModule):
    """Enhanced Data Analysis module for enhanced reports."""
    
    module_id = "enhanced_data_analysis"
    title = "📊 Enhanced Data Analysis"
    description = "Comprehensive data analysis with performance indicators and statistical insights"
    version = "1.0.0"
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Enhanced Data Analysis module."""
        if config is None:
            config = ModuleConfig(
                title="📊 Enhanced Data Analysis",
                description="Comprehensive data analysis with performance indicators and statistical insights",
                order=8,  # After strategic analysis
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'data_analysis_overview',
            'key_data_metrics',
            'performance_indicators',
            'statistical_analysis'
        ]
    
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for the Enhanced Data Analysis module."""
        
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

        # Extract data analysis information
        data_analysis_overview = data.get('data_analysis_overview', {})
        key_data_metrics = data.get('key_data_metrics', {})
        performance_indicators = data.get('performance_indicators', {})
        statistical_analysis = data.get('statistical_analysis', {})

        # Generate comprehensive data analysis content
        content = self._generate_enhanced_data_analysis_content(
            data_analysis_overview, key_data_metrics, performance_indicators, statistical_analysis
        )

        return {
            "content": content,
            "metadata": {
                "phase4_integrated": phase4_enhanced,
                "strategic_intelligence": phase4_enhanced,
                "confidence_score": 0.7,
                "data_analysis_complete": bool(data_analysis_overview),
                "metrics_analyzed": bool(key_data_metrics),
                "performance_assessed": bool(performance_indicators)
            }
        }
    
    def _generate_enhanced_data_analysis_content(self, data_analysis_overview: Dict[str, Any], 
                                               key_data_metrics: Dict[str, Any], 
                                               performance_indicators: Dict[str, Any], 
                                               statistical_analysis: Dict[str, Any]) -> str:
        """Generate the main enhanced data analysis content."""
        
        content = f"""
        <div class="enhanced-data-analysis-section">
            <h2>📊 Enhanced Data Analysis</h2>
            
            {self._generate_data_analysis_overview(data_analysis_overview)}
            {self._generate_key_data_metrics(key_data_metrics)}
            {self._generate_performance_indicators(performance_indicators)}
            {self._generate_statistical_analysis(statistical_analysis)}
            {self._generate_interactive_charts(data_analysis_overview, key_data_metrics, performance_indicators)}
        </div>
        """
        
        return content
    
    def _generate_data_analysis_overview(self, data_analysis_overview: Dict[str, Any]) -> str:
        """Generate data analysis overview section."""
        if not data_analysis_overview:
            return """
            <div class="data-analysis-overview">
                <h3>Data Analysis Overview</h3>
                <p>Data analysis overview not available.</p>
            </div>
            """
        
        analysis_summary = data_analysis_overview.get('analysis_summary', 'N/A')
        data_sources = data_analysis_overview.get('data_sources', [])
        analysis_methodology = data_analysis_overview.get('analysis_methodology', 'N/A')
        
        sources_html = ""
        if data_sources:
            sources_html = "<ul>" + "".join([f"<li>{source}</li>" for source in data_sources]) + "</ul>"
        
        return f"""
        <div class="data-analysis-overview">
            <h3>Data Analysis Overview</h3>
            <div class="overview-content">
                <p><strong>Analysis Summary:</strong> {analysis_summary}</p>
                <p><strong>Analysis Methodology:</strong> {analysis_methodology}</p>
            </div>
            <div class="data-sources">
                <h4>Data Sources</h4>
                {sources_html}
            </div>
        </div>
        """
    
    def _generate_key_data_metrics(self, key_data_metrics: Dict[str, Any]) -> str:
        """Generate key data metrics section."""
        if not key_data_metrics:
            return """
            <div class="key-data-metrics">
                <h3>Key Data Metrics</h3>
                <p>Key data metrics not available.</p>
            </div>
            """
        
        metrics_summary = key_data_metrics.get('metrics_summary', {})
        trend_analysis = key_data_metrics.get('trend_analysis', 'N/A')
        data_quality_score = key_data_metrics.get('data_quality_score', 'N/A')
        
        summary_html = ""
        if metrics_summary:
            summary_html = "<ul>" + "".join([f"<li><strong>{metric}</strong>: {value}</li>" for metric, value in metrics_summary.items()]) + "</ul>"
        
        return f"""
        <div class="key-data-metrics">
            <h3>Key Data Metrics</h3>
            <div class="metrics-stats">
                <div class="stat-item">
                    <span class="stat-label">Data Quality Score:</span>
                    <span class="stat-value">{data_quality_score}</span>
                </div>
            </div>
            <div class="metrics-summary">
                <h4>Metrics Summary</h4>
                {summary_html}
            </div>
            <div class="trend-analysis">
                <h4>Trend Analysis</h4>
                <p>{trend_analysis}</p>
            </div>
        </div>
        """
    
    def _generate_performance_indicators(self, performance_indicators: Dict[str, Any]) -> str:
        """Generate performance indicators section."""
        if not performance_indicators:
            return """
            <div class="performance-indicators">
                <h3>Performance Indicators</h3>
                <p>Performance indicators not available.</p>
            </div>
            """
        
        kpi_summary = performance_indicators.get('kpi_summary', {})
        performance_trends = performance_indicators.get('performance_trends', [])
        benchmark_comparison = performance_indicators.get('benchmark_comparison', 'N/A')
        
        kpi_html = ""
        if kpi_summary:
            kpi_html = "<ul>" + "".join([f"<li><strong>{kpi}</strong>: {value}</li>" for kpi, value in kpi_summary.items()]) + "</ul>"
        
        trends_html = ""
        if performance_trends:
            trends_html = "<ul>" + "".join([f"<li>{trend}</li>" for trend in performance_trends]) + "</ul>"
        
        return f"""
        <div class="performance-indicators">
            <h3>Performance Indicators</h3>
            <div class="kpi-summary">
                <h4>KPI Summary</h4>
                {kpi_html}
            </div>
            <div class="performance-trends">
                <h4>Performance Trends</h4>
                {trends_html}
            </div>
            <div class="benchmark-comparison">
                <h4>Benchmark Comparison</h4>
                <p>{benchmark_comparison}</p>
            </div>
        </div>
        """
    
    def _generate_statistical_analysis(self, statistical_analysis: Dict[str, Any]) -> str:
        """Generate statistical analysis section."""
        if not statistical_analysis:
            return """
            <div class="statistical-analysis">
                <h3>Statistical Analysis</h3>
                <p>Statistical analysis not available.</p>
            </div>
            """
        
        statistical_summary = statistical_analysis.get('statistical_summary', {})
        correlation_analysis = statistical_analysis.get('correlation_analysis', 'N/A')
        significance_tests = statistical_analysis.get('significance_tests', [])
        
        summary_html = ""
        if statistical_summary:
            summary_html = "<ul>" + "".join([f"<li><strong>{stat}</strong>: {value}</li>" for stat, value in statistical_summary.items()]) + "</ul>"
        
        tests_html = ""
        if significance_tests:
            tests_html = "<ul>" + "".join([f"<li>{test}</li>" for test in significance_tests]) + "</ul>"
        
        return f"""
        <div class="statistical-analysis">
            <h3>Statistical Analysis</h3>
            <div class="statistical-summary">
                <h4>Statistical Summary</h4>
                {summary_html}
            </div>
            <div class="correlation-analysis">
                <h4>Correlation Analysis</h4>
                <p>{correlation_analysis}</p>
            </div>
            <div class="significance-tests">
                <h4>Significance Tests</h4>
                {tests_html}
            </div>
        </div>
        """
    
    def _generate_interactive_charts(self, data_analysis_overview: Dict[str, Any], 
                                   key_data_metrics: Dict[str, Any], 
                                   performance_indicators: Dict[str, Any]) -> str:
        """Generate interactive charts for data analysis visualization."""
        
        # Create chart data
        chart_data = {
            'metrics_trends': key_data_metrics.get('trends_data', {}),
            'performance_data': performance_indicators.get('performance_data', {}),
            'statistical_data': data_analysis_overview.get('statistical_data', {})
        }
        
        return f"""
        <div class="interactive-charts">
            <h3>Interactive Data Analysis Visualizations</h3>
            <div class="chart-container">
                <div class="chart" id="metrics-trends-chart">
                    <h4>Metrics Trends</h4>
                    <div class="chart-placeholder">
                        <p>Interactive line chart showing key metrics trends over time</p>
                        <p>Data points: {len(chart_data['metrics_trends'])} available</p>
                    </div>
                </div>
                <div class="chart" id="performance-dashboard-chart">
                    <h4>Performance Dashboard</h4>
                    <div class="chart-placeholder">
                        <p>Interactive dashboard showing performance indicators</p>
                        <p>Indicators: {len(chart_data['performance_data'])} tracked</p>
                    </div>
                </div>
                <div class="chart" id="statistical-distribution-chart">
                    <h4>Statistical Distribution</h4>
                    <div class="chart-placeholder">
                        <p>Histogram showing statistical distribution of key variables</p>
                        <p>Variables: {len(chart_data['statistical_data'])} analyzed</p>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltips for the Enhanced Data Analysis module."""
        self.tooltips = {
            'data_analysis': TooltipData(
                title="Data Analysis",
                description="Comprehensive analysis of data patterns and trends",
                source="Data Analysis Framework",
                strategic_impact="High - Critical for data-driven decisions"
            ),
            'performance_metrics': TooltipData(
                title="Performance Metrics",
                description="Key performance indicators and measurement criteria",
                source="Performance Analysis Framework",
                strategic_impact="High - Critical for performance assessment"
            ),
            'statistical_insights': TooltipData(
                title="Statistical Insights",
                description="Statistical analysis and significance testing results",
                source="Statistical Analysis Framework",
                strategic_impact="Medium - Important for data validation"
            ),
            'data_visualization': TooltipData(
                title="Data Visualization",
                description="Interactive charts and visual data representations",
                source="Visualization Framework",
                strategic_impact="Medium - Important for data presentation"
            )
        }
