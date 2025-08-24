"""
Enhanced Data Analysis Module

Independent module for generating enhanced data analysis sections that can be added to any report.
Provides comprehensive data analysis, performance indicators, statistical analysis, and data visualization.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class EnhancedDataAnalysisModule(BaseModule):
    """Enhanced Data Analysis module for enhanced reports."""
    
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
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Enhanced Data Analysis module."""
        self.validate_data(data)
        
        data_analysis_overview = data.get('data_analysis_overview', {})
        key_data_metrics = data.get('key_data_metrics', {})
        performance_indicators = data.get('performance_indicators', {})
        statistical_analysis = data.get('statistical_analysis', {})
        
        # Generate data analysis overview
        overview_html = self._generate_data_analysis_overview(data_analysis_overview)
        
        # Generate key data metrics section
        metrics_html = self._generate_key_data_metrics(key_data_metrics)
        
        # Generate performance indicators section
        indicators_html = self._generate_performance_indicators(performance_indicators)
        
        # Generate statistical analysis section
        statistical_html = self._generate_statistical_analysis(statistical_analysis)
        
        # Generate interactive visualizations
        visualizations_html = self._generate_interactive_visualizations(data)
        
        return f"""
        <div class="section" id="enhanced-data-analysis">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {metrics_html}
            {indicators_html}
            {statistical_html}
            {visualizations_html}
        </div>
        """
    
    def _generate_data_analysis_overview(self, overview_data: Dict[str, Any]) -> str:
        """Generate the data analysis overview section."""
        title = overview_data.get('title', 'Enhanced Data Analysis Overview')
        overview = overview_data.get('overview', 'No data analysis overview available.')
        key_findings = overview_data.get('key_findings', [])
        data_quality_score = overview_data.get('data_quality_score', 0.0)
        analysis_confidence = overview_data.get('analysis_confidence', 0.0)
        
        findings_html = ""
        if key_findings:
            findings_html = """
            <div class="key-findings">
                <h4>🔍 Key Data Findings</h4>
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
        <div class="data-analysis-overview">
            <div class="overview-header" data-tooltip-{self.module_id}="data_analysis_overview">
                <h3>📊 Data Analysis Overview</h3>
                <h4>{title}</h4>
                <div class="quality-indicator">
                    <span class="quality-label">Data Quality Score:</span>
                    <span class="quality-value">{data_quality_score:.1f}%</span>
                </div>
                <div class="confidence-indicator">
                    <span class="confidence-label">Analysis Confidence:</span>
                    <span class="confidence-value">{analysis_confidence:.1f}%</span>
                </div>
            </div>
            <div class="overview-content">
                <p>{overview}</p>
                {findings_html}
            </div>
        </div>
        """
    
    def _generate_key_data_metrics(self, metrics_data: Dict[str, Any]) -> str:
        """Generate the key data metrics section."""
        metrics = metrics_data.get('metrics', [])
        categories = metrics_data.get('categories', {})
        
        metrics_html = ""
        if metrics:
            metrics_html = """
            <div class="key-metrics">
                <h4>📈 Key Data Metrics</h4>
                <div class="metrics-grid">
            """
            for i, metric in enumerate(metrics):
                metric_id = f"metric_{i}"
                metrics_html += f"""
                <div class="metric-card" data-tooltip-{self.module_id}="{metric_id}">
                    <h5>{metric.get('name', 'Unknown Metric')}</h5>
                    <div class="metric-value">{metric.get('value', 'N/A')}</div>
                    <div class="metric-trend">
                        <span class="trend-label">Trend:</span>
                        <span class="trend-value {metric.get('trend', 'stable').lower()}">{metric.get('trend', 'Stable')}</span>
                    </div>
                    <p class="metric-description">{metric.get('description', 'No description available.')}</p>
                </div>
                """
            metrics_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="key-data-metrics">
            <div class="metrics-header" data-tooltip-{self.module_id}="key_data_metrics">
                <h3>📈 Key Data Metrics</h3>
            </div>
            <div class="metrics-content">
                {metrics_html}
            </div>
        </div>
        """
    
    def _generate_performance_indicators(self, indicators_data: Dict[str, Any]) -> str:
        """Generate the performance indicators section."""
        indicators = indicators_data.get('indicators', [])
        performance_categories = indicators_data.get('performance_categories', {})
        
        indicators_html = ""
        if indicators:
            indicators_html = """
            <div class="performance-indicators">
                <h4>🎯 Performance Indicators</h4>
                <div class="indicators-container">
            """
            for i, indicator in enumerate(indicators):
                indicator_id = f"performance_indicator_{i}"
                indicators_html += f"""
                <div class="indicator-card" data-tooltip-{self.module_id}="{indicator_id}">
                    <h5>{indicator.get('name', 'Unknown Indicator')}</h5>
                    <div class="indicator-metrics">
                        <div class="metric">
                            <span class="label">Current Value:</span>
                            <span class="value">{indicator.get('current_value', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Target:</span>
                            <span class="value">{indicator.get('target', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Status:</span>
                            <span class="value {indicator.get('status', 'on_track').lower()}">{indicator.get('status', 'On Track')}</span>
                        </div>
                    </div>
                    <p class="indicator-description">{indicator.get('description', 'No description available.')}</p>
                </div>
                """
            indicators_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="performance-indicators-section">
            <div class="indicators-header" data-tooltip-{self.module_id}="performance_indicators">
                <h3>🎯 Performance Indicators</h3>
            </div>
            <div class="indicators-content">
                {indicators_html}
            </div>
        </div>
        """
    
    def _generate_statistical_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """Generate the statistical analysis section."""
        statistical_measures = analysis_data.get('statistical_measures', [])
        correlation_analysis = analysis_data.get('correlation_analysis', {})
        trend_analysis = analysis_data.get('trend_analysis', {})
        
        measures_html = ""
        if statistical_measures:
            measures_html = """
            <div class="statistical-measures">
                <h4>📊 Statistical Measures</h4>
                <div class="measures-container">
            """
            for i, measure in enumerate(statistical_measures):
                measure_id = f"statistical_measure_{i}"
                measures_html += f"""
                <div class="measure-card" data-tooltip-{self.module_id}="{measure_id}">
                    <h5>{measure.get('name', 'Unknown Measure')}</h5>
                    <div class="measure-metrics">
                        <div class="metric">
                            <span class="label">Value:</span>
                            <span class="value">{measure.get('value', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Significance:</span>
                            <span class="value">{measure.get('significance', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Confidence:</span>
                            <span class="value">{measure.get('confidence', 'Unknown')}%</span>
                        </div>
                    </div>
                    <p class="measure-description">{measure.get('description', 'No description available.')}</p>
                </div>
                """
            measures_html += """
                </div>
            </div>
            """
        
        correlation_html = ""
        if correlation_analysis:
            correlations = correlation_analysis.get('correlations', [])
            if correlations:
                correlation_html = """
                <div class="correlation-analysis">
                    <h4>🔗 Correlation Analysis</h4>
                    <ul>
                """
                for i, correlation in enumerate(correlations):
                    correlation_id = f"correlation_{i}"
                    correlation_html += f"""
                    <li data-tooltip-{self.module_id}="{correlation_id}">
                        <strong>{correlation.get('variable1', 'Unknown')}</strong> vs 
                        <strong>{correlation.get('variable2', 'Unknown')}</strong>: 
                        {correlation.get('correlation_coefficient', 'Unknown')} 
                        ({correlation.get('strength', 'Unknown')})
                    </li>
                    """
                correlation_html += """
                    </ul>
                </div>
                """
        
        return f"""
        <div class="statistical-analysis-section">
            <div class="analysis-header" data-tooltip-{self.module_id}="statistical_analysis">
                <h3>📊 Statistical Analysis</h3>
            </div>
            <div class="analysis-content">
                {measures_html}
                {correlation_html}
            </div>
        </div>
        """
    
    def _generate_interactive_visualizations(self, data: Dict[str, Any]) -> str:
        """Generate interactive visualizations for the module."""
        if not self.config.charts_enabled:
            return ""
        
        # Generate performance metrics chart
        performance_chart_html = self._generate_performance_metrics_chart(data)
        
        # Generate statistical analysis chart
        statistical_chart_html = self._generate_statistical_analysis_chart(data)
        
        return f"""
        <div class="interactive-visualizations">
            <h3>📈 Interactive Visualizations</h3>
            {performance_chart_html}
            {statistical_chart_html}
        </div>
        """
    
    def _generate_performance_metrics_chart(self, data: Dict[str, Any]) -> str:
        """Generate a bar chart for performance metrics visualization."""
        performance_indicators = data.get('performance_indicators', {})
        indicators = performance_indicators.get('indicators', [])
        
        if not indicators:
            return ""
        
        # Prepare chart data
        indicator_names = [indicator.get('name', 'Unknown') for indicator in indicators]
        current_values = [self._convert_performance_to_number(indicator.get('current_value', '0')) for indicator in indicators]
        targets = [self._convert_performance_to_number(indicator.get('target', '0')) for indicator in indicators]
        
        chart_id = f"performance_metrics_{self.module_id}"
        
        # Add chart data to the module
        self.add_chart_data(chart_id, {
            'type': 'bar',
            'data': {
                'labels': indicator_names,
                'datasets': [
                    {
                        'label': 'Current Value',
                        'data': current_values,
                        'backgroundColor': 'rgba(54, 162, 235, 0.8)',
                        'borderColor': 'rgba(54, 162, 235, 1)',
                        'borderWidth': 1
                    },
                    {
                        'label': 'Target',
                        'data': targets,
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
                        'text': 'Performance Metrics Analysis'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>🎯 Performance Metrics Chart</h4>
            <canvas id="{chart_id}" width="400" height="300"></canvas>
        </div>
        """
    
    def _generate_statistical_analysis_chart(self, data: Dict[str, Any]) -> str:
        """Generate a line chart for statistical analysis visualization."""
        statistical_analysis = data.get('statistical_analysis', {})
        statistical_measures = statistical_analysis.get('statistical_measures', [])
        
        if not statistical_measures:
            return ""
        
        # Prepare chart data
        measure_names = [measure.get('name', 'Unknown') for measure in statistical_measures]
        values = [self._convert_statistical_to_number(measure.get('value', '0')) for measure in statistical_measures]
        confidences = [self._convert_confidence_to_number(measure.get('confidence', '0')) for measure in statistical_measures]
        
        chart_id = f"statistical_analysis_{self.module_id}"
        
        # Add chart data to the module
        self.add_chart_data(chart_id, {
            'type': 'line',
            'data': {
                'labels': measure_names,
                'datasets': [
                    {
                        'label': 'Statistical Value',
                        'data': values,
                        'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                        'borderColor': 'rgba(75, 192, 192, 1)',
                        'borderWidth': 2,
                        'fill': False
                    },
                    {
                        'label': 'Confidence Level',
                        'data': confidences,
                        'backgroundColor': 'rgba(255, 159, 64, 0.2)',
                        'borderColor': 'rgba(255, 159, 64, 1)',
                        'borderWidth': 2,
                        'fill': False
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
                        'text': 'Statistical Analysis Overview'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>📊 Statistical Analysis Chart</h4>
            <canvas id="{chart_id}" width="400" height="300"></canvas>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        # Data analysis overview tooltips
        self.add_tooltip("data_analysis_overview", TooltipData(
            title="Data Analysis Overview",
            description="Comprehensive overview of enhanced data analysis capabilities and key findings from the analysis.",
            source="Enhanced Data Analysis Framework",
            strategic_impact="High - Critical for data-driven decision making and strategic insights",
            recommendations="• Focus on high-quality data sources\n• Ensure statistical significance\n• Monitor data quality metrics\n• Validate analysis results",
            use_cases="Used in strategic planning, performance measurement, and data-driven decision making",
            confidence=90.0
        ))
        
        self.add_tooltip("key_data_metrics", TooltipData(
            title="Key Data Metrics",
            description="Essential data metrics and key performance indicators that provide insights into the current situation.",
            source="Data Metrics Analysis Framework",
            strategic_impact="High - Essential for performance measurement and trend analysis",
            recommendations="• Track key metrics regularly\n• Set appropriate targets\n• Monitor trend changes\n• Analyze metric correlations",
            use_cases="Used in performance monitoring, trend analysis, and strategic assessment",
            confidence=88.0
        ))
        
        self.add_tooltip("performance_indicators", TooltipData(
            title="Performance Indicators",
            description="Comprehensive performance indicators and metrics that measure effectiveness and progress.",
            source="Performance Measurement Framework",
            strategic_impact="High - Critical for performance evaluation and strategic planning",
            recommendations="• Establish clear performance targets\n• Monitor indicator trends\n• Analyze performance gaps\n• Develop improvement strategies",
            use_cases="Used in performance evaluation, strategic planning, and operational assessment",
            confidence=92.0
        ))
        
        self.add_tooltip("statistical_analysis", TooltipData(
            title="Statistical Analysis",
            description="Advanced statistical analysis and correlation studies that provide deeper insights into data relationships.",
            source="Statistical Analysis Framework",
            strategic_impact="High - Essential for understanding data relationships and making informed decisions",
            recommendations="• Ensure statistical significance\n• Validate correlation findings\n• Consider multiple variables\n• Monitor confidence levels",
            use_cases="Used in research analysis, correlation studies, and statistical modeling",
            confidence=85.0
        ))
        
        # Add tooltips for dynamic content
        for i in range(10):  # Add tooltips for up to 10 findings
            self.add_tooltip(f"finding_{i}", TooltipData(
                title=f"Data Finding {i+1}",
                description=f"Key data finding {i+1} derived from comprehensive analysis of the available data and metrics.",
                source="Enhanced Data Analysis",
                strategic_impact="Important insight for strategic decision-making and planning.",
                recommendations="• Consider in strategic planning\n• Validate with additional data\n• Monitor for changes\n• Include in analysis updates",
                use_cases="Data analysis, strategic planning, performance assessment, trend monitoring",
                confidence=0.80
            ))
        
        for i in range(10):  # Add tooltips for up to 10 metrics
            self.add_tooltip(f"metric_{i}", TooltipData(
                title=f"Data Metric {i+1}",
                description=f"Key data metric {i+1} that provides important insights into the current situation and trends.",
                source="Data Metrics Analysis",
                strategic_impact="Valuable metric for understanding performance and trends.",
                recommendations="• Monitor regularly for changes\n• Compare with historical data\n• Analyze trends and patterns\n• Use for strategic planning",
                use_cases="Performance monitoring, trend analysis, strategic assessment, decision support",
                confidence=0.85
            ))
        
        for i in range(10):  # Add tooltips for up to 10 performance indicators
            self.add_tooltip(f"performance_indicator_{i}", TooltipData(
                title=f"Performance Indicator {i+1}",
                description=f"Performance indicator {i+1} that measures effectiveness and progress in key areas.",
                source="Performance Measurement Framework",
                strategic_impact="Critical indicator for performance evaluation and strategic planning.",
                recommendations="• Track against targets\n• Monitor trends and changes\n• Analyze performance gaps\n• Develop improvement plans",
                use_cases="Performance evaluation, strategic planning, operational assessment, goal setting",
                confidence=0.90
            ))
        
        for i in range(10):  # Add tooltips for up to 10 statistical measures
            self.add_tooltip(f"statistical_measure_{i}", TooltipData(
                title=f"Statistical Measure {i+1}",
                description=f"Statistical measure {i+1} that provides quantitative insights into data relationships and patterns.",
                source="Statistical Analysis Framework",
                strategic_impact="Important statistical insight for data-driven decision making.",
                recommendations="• Validate statistical significance\n• Consider confidence levels\n• Analyze with other measures\n• Use for modeling",
                use_cases="Statistical analysis, research studies, data modeling, correlation analysis",
                confidence=0.85
            ))
        
        for i in range(10):  # Add tooltips for up to 10 correlations
            self.add_tooltip(f"correlation_{i}", TooltipData(
                title=f"Correlation Analysis {i+1}",
                description=f"Correlation analysis {i+1} showing relationships between different variables and factors.",
                source="Correlation Analysis Framework",
                strategic_impact="Valuable insight into variable relationships and dependencies.",
                recommendations="• Validate correlation strength\n• Consider causation vs correlation\n• Analyze with other factors\n• Monitor for changes",
                use_cases="Correlation studies, relationship analysis, dependency mapping, statistical modeling",
                confidence=0.80
            ))
    
    def _convert_performance_to_number(self, performance: str) -> float:
        """Convert performance value to numerical value for charts."""
        # Extract percentage from string like "85%" or "High (85%)"
        import re
        numbers = re.findall(r'\d+', str(performance))
        if numbers:
            return float(numbers[0])
        
        # Convert text levels to numbers
        performance_map = {
            'Very Low': 20,
            'Low': 40,
            'Medium': 60,
            'High': 80,
            'Very High': 100
        }
        return performance_map.get(performance, 50.0)
    
    def _convert_statistical_to_number(self, statistical: str) -> float:
        """Convert statistical value to numerical value for charts."""
        # Extract percentage from string like "85%" or "High (85%)"
        import re
        numbers = re.findall(r'\d+', str(statistical))
        if numbers:
            return float(numbers[0])
        
        # Convert text levels to numbers
        statistical_map = {
            'Very Low': 20,
            'Low': 40,
            'Medium': 60,
            'High': 80,
            'Very High': 100
        }
        return statistical_map.get(statistical, 50.0)
    
    def _convert_confidence_to_number(self, confidence: str) -> float:
        """Convert confidence value to numerical value for charts."""
        # Extract percentage from string like "85%" or "High (85%)"
        import re
        numbers = re.findall(r'\d+', str(confidence))
        if numbers:
            return float(numbers[0])
        
        # Convert text levels to numbers
        confidence_map = {
            'Very Low': 20,
            'Low': 40,
            'Medium': 60,
            'High': 80,
            'Very High': 100
        }
        return confidence_map.get(confidence, 50.0)
