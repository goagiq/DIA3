"""
Interactive Visualizations Module

Independent module for generating interactive visualization sections that can be added to any report.
Provides enhanced data visualization, strategic trends analysis, chart.js integration, and advanced tooltips.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class InteractiveVisualizationsModule(BaseModule):
    """Interactive Visualizations module for enhanced reports."""
    
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
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Interactive Visualizations module."""
        self.validate_data(data)
        
        visualization_overview = data.get('visualization_overview', {})
        strategic_trends = data.get('strategic_trends', {})
        data_metrics = data.get('data_metrics', {})
        interactive_charts = data.get('interactive_charts', {})
        
        # Generate visualization overview
        overview_html = self._generate_visualization_overview(visualization_overview)
        
        # Generate strategic trends analysis
        trends_html = self._generate_strategic_trends(strategic_trends)
        
        # Generate data metrics analysis
        metrics_html = self._generate_data_metrics(data_metrics)
        
        # Generate interactive charts analysis
        charts_html = self._generate_interactive_charts(interactive_charts)
        
        # Generate interactive visualizations
        visualizations_html = self._generate_interactive_visualizations(data)
        
        return f"""
        <div class="section" id="interactive-visualizations">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {trends_html}
            {metrics_html}
            {charts_html}
            {visualizations_html}
        </div>
        """
    
    def _generate_visualization_overview(self, overview_data: Dict[str, Any]) -> str:
        """Generate the interactive visualization overview section."""
        title = overview_data.get('title', 'Interactive Visualization Analysis')
        overview = overview_data.get('overview', 'No visualization overview available.')
        key_visualizations = overview_data.get('key_visualizations', [])
        overall_complexity = overview_data.get('overall_complexity', 'Medium')
        confidence_score = overview_data.get('confidence_score', 0.0)
        
        visualizations_html = ""
        if key_visualizations:
            visualizations_html = """
            <div class="key-visualizations">
                <h4>📈 Key Visualization Types</h4>
                <div class="visualizations-grid">
            """
            for i, viz in enumerate(key_visualizations):
                viz_id = f"visualization_{i}"
                visualizations_html += f"""
                <div class="visualization-card" data-tooltip-{self.module_id}="{viz_id}">
                    <h5>{viz.get('name', 'Unknown Visualization')}</h5>
                    <p class="visualization-type">{viz.get('type', 'No type specified')}</p>
                    <p class="visualization-complexity">Complexity: {viz.get('complexity', 'Medium')}</p>
                    <p class="visualization-interactivity">Interactivity: {viz.get('interactivity', 'Medium')}</p>
                </div>
                """
            visualizations_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="visualization-overview">
            <div class="overview-header" data-tooltip-{self.module_id}="visualization_overview">
                <h3>📊 Visualization Overview</h3>
                <h4>{title}</h4>
                <div class="complexity-indicator">
                    <span class="complexity-label">Overall Complexity:</span>
                    <span class="complexity-value {overall_complexity.lower()}">{overall_complexity}</span>
                </div>
                <div class="confidence-indicator">
                    <span class="confidence-label">Confidence:</span>
                    <span class="confidence-value">{confidence_score:.1f}%</span>
                </div>
            </div>
            <div class="overview-content">
                <p>{overview}</p>
            </div>
            {visualizations_html}
        </div>
        """
    
    def _generate_strategic_trends(self, trends_data: Dict[str, Any]) -> str:
        """Generate the strategic trends analysis section."""
        trend_categories = trends_data.get('trend_categories', [])
        trend_indicators = trends_data.get('trend_indicators', [])
        trend_analysis = trends_data.get('trend_analysis', {})
        
        categories_html = ""
        if trend_categories:
            categories_html = """
            <div class="trend-categories">
                <h4>📈 Trend Categories</h4>
                <div class="categories-container">
            """
            for i, category in enumerate(trend_categories):
                category_id = f"trend_category_{i}"
                categories_html += f"""
                <div class="category-card" data-tooltip-{self.module_id}="{category_id}">
                    <h5>{category.get('name', 'Unknown Category')}</h5>
                    <div class="category-metrics">
                        <div class="metric">
                            <span class="label">Trend Direction:</span>
                            <span class="value">{category.get('direction', 'Stable')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Strength:</span>
                            <span class="value">{category.get('strength', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Duration:</span>
                            <span class="value">{category.get('duration', 'Unknown')}</span>
                        </div>
                    </div>
                    <p class="category-description">{category.get('description', 'No description available.')}</p>
                </div>
                """
            categories_html += """
                </div>
            </div>
            """
        
        indicators_html = ""
        if trend_indicators:
            indicators_html = """
            <div class="trend-indicators">
                <h4>📊 Trend Indicators</h4>
                <div class="indicators-container">
            """
            for i, indicator in enumerate(trend_indicators):
                indicator_id = f"trend_indicator_{i}"
                indicators_html += f"""
                <div class="indicator-card" data-tooltip-{self.module_id}="{indicator_id}">
                    <h5>{indicator.get('name', 'Unknown Indicator')}</h5>
                    <div class="indicator-metrics">
                        <div class="metric">
                            <span class="label">Current Value:</span>
                            <span class="value">{indicator.get('current_value', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Trend:</span>
                            <span class="value">{indicator.get('trend', 'Stable')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Significance:</span>
                            <span class="value">{indicator.get('significance', 'Medium')}</span>
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
        <div class="strategic-trends-analysis">
            <h3>📈 Strategic Trends Analysis</h3>
            {categories_html}
            {indicators_html}
        </div>
        """
    
    def _generate_data_metrics(self, metrics_data: Dict[str, Any]) -> str:
        """Generate the data metrics analysis section."""
        performance_indicators = metrics_data.get('performance_indicators', [])
        statistical_analysis = metrics_data.get('statistical_analysis', [])
        data_quality = metrics_data.get('data_quality', {})
        
        indicators_html = ""
        if performance_indicators:
            indicators_html = """
            <div class="performance-indicators">
                <h4>📊 Performance Indicators</h4>
                <div class="indicators-container">
            """
            for i, indicator in enumerate(performance_indicators):
                indicator_id = f"performance_indicator_{i}"
                indicators_html += f"""
                <div class="indicator-card" data-tooltip-{self.module_id}="{indicator_id}">
                    <h5>{indicator.get('name', 'Unknown Indicator')}</h5>
                    <div class="indicator-metrics">
                        <div class="metric">
                            <span class="label">Value:</span>
                            <span class="value">{indicator.get('value', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Target:</span>
                            <span class="value">{indicator.get('target', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Status:</span>
                            <span class="value">{indicator.get('status', 'On Track')}</span>
                        </div>
                    </div>
                    <p class="indicator-description">{indicator.get('description', 'No description available.')}</p>
                </div>
                """
            indicators_html += """
                </div>
            </div>
            """
        
        analysis_html = ""
        if statistical_analysis:
            analysis_html = """
            <div class="statistical-analysis">
                <h4>📈 Statistical Analysis</h4>
                <div class="analysis-container">
            """
            for i, analysis in enumerate(statistical_analysis):
                analysis_id = f"statistical_analysis_{i}"
                analysis_html += f"""
                <div class="analysis-card" data-tooltip-{self.module_id}="{analysis_id}">
                    <h5>{analysis.get('name', 'Unknown Analysis')}</h5>
                    <div class="analysis-metrics">
                        <div class="metric">
                            <span class="label">Method:</span>
                            <span class="value">{analysis.get('method', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Result:</span>
                            <span class="value">{analysis.get('result', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Confidence:</span>
                            <span class="value">{analysis.get('confidence', 'Unknown')}%</span>
                        </div>
                    </div>
                    <p class="analysis-description">{analysis.get('description', 'No description available.')}</p>
                </div>
                """
            analysis_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="data-metrics-analysis">
            <h3>📊 Data Metrics Analysis</h3>
            {indicators_html}
            {analysis_html}
        </div>
        """
    
    def _generate_interactive_charts(self, charts_data: Dict[str, Any]) -> str:
        """Generate the interactive charts analysis section."""
        chart_types = charts_data.get('chart_types', [])
        chart_configurations = charts_data.get('chart_configurations', [])
        chart_interactions = charts_data.get('chart_interactions', {})
        
        types_html = ""
        if chart_types:
            types_html = """
            <div class="chart-types">
                <h4>📊 Chart Types</h4>
                <div class="types-container">
            """
            for i, chart_type in enumerate(chart_types):
                type_id = f"chart_type_{i}"
                types_html += f"""
                <div class="type-card" data-tooltip-{self.module_id}="{type_id}">
                    <h5>{chart_type.get('name', 'Unknown Type')}</h5>
                    <div class="type-metrics">
                        <div class="metric">
                            <span class="label">Type:</span>
                            <span class="value">{chart_type.get('type', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Interactivity:</span>
                            <span class="value">{chart_type.get('interactivity', 'Medium')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Complexity:</span>
                            <span class="value">{chart_type.get('complexity', 'Medium')}</span>
                        </div>
                    </div>
                    <p class="type-description">{chart_type.get('description', 'No description available.')}</p>
                </div>
                """
            types_html += """
                </div>
            </div>
            """
        
        configs_html = ""
        if chart_configurations:
            configs_html = """
            <div class="chart-configurations">
                <h4>⚙️ Chart Configurations</h4>
                <div class="configs-container">
            """
            for i, config in enumerate(chart_configurations):
                config_id = f"chart_config_{i}"
                configs_html += f"""
                <div class="config-card" data-tooltip-{self.module_id}="{config_id}">
                    <h5>{config.get('name', 'Unknown Configuration')}</h5>
                    <div class="config-metrics">
                        <div class="metric">
                            <span class="label">Chart Type:</span>
                            <span class="value">{config.get('chart_type', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Data Source:</span>
                            <span class="value">{config.get('data_source', 'Unknown')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Update Frequency:</span>
                            <span class="value">{config.get('update_frequency', 'Unknown')}</span>
                        </div>
                    </div>
                    <p class="config-description">{config.get('description', 'No description available.')}</p>
                </div>
                """
            configs_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="interactive-charts-analysis">
            <h3>📊 Interactive Charts Analysis</h3>
            {types_html}
            {configs_html}
        </div>
        """
    
    def _generate_interactive_visualizations(self, data: Dict[str, Any]) -> str:
        """Generate interactive visualizations for the module."""
        if not self.config.charts_enabled:
            return ""
        
        # Generate trend analysis chart
        trend_chart_html = self._generate_trend_analysis_chart(data)
        
        # Generate performance metrics chart
        performance_chart_html = self._generate_performance_metrics_chart(data)
        
        return f"""
        <div class="interactive-visualizations">
            <h3>📈 Interactive Visualizations</h3>
            {trend_chart_html}
            {performance_chart_html}
        </div>
        """
    
    def _generate_trend_analysis_chart(self, data: Dict[str, Any]) -> str:
        """Generate a line chart for trend analysis visualization."""
        strategic_trends = data.get('strategic_trends', {})
        trend_indicators = strategic_trends.get('trend_indicators', [])
        
        if not trend_indicators:
            return ""
        
        # Prepare chart data
        indicators = [indicator.get('name', 'Unknown') for indicator in trend_indicators]
        values = [self._convert_trend_to_number(indicator.get('trend', 'Stable')) for indicator in trend_indicators]
        
        chart_id = f"trend_analysis_{self.module_id}"
        
        # Add chart data to the module
        self.add_chart_data(chart_id, {
            'type': 'line',
            'data': {
                'labels': indicators,
                'datasets': [{
                    'label': 'Trend Strength',
                    'data': values,
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 2,
                    'fill': False
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
                        'text': 'Strategic Trends Analysis'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>📈 Trend Analysis Chart</h4>
            <canvas id="{chart_id}" width="400" height="300"></canvas>
        </div>
        """
    
    def _generate_performance_metrics_chart(self, data: Dict[str, Any]) -> str:
        """Generate a bar chart for performance metrics visualization."""
        data_metrics = data.get('data_metrics', {})
        performance_indicators = data_metrics.get('performance_indicators', [])
        
        if not performance_indicators:
            return ""
        
        # Prepare chart data
        indicators = [indicator.get('name', 'Unknown') for indicator in performance_indicators]
        values = [self._convert_performance_to_number(indicator.get('value', '0')) for indicator in performance_indicators]
        
        chart_id = f"performance_metrics_{self.module_id}"
        
        # Add chart data to the module
        self.add_chart_data(chart_id, {
            'type': 'bar',
            'data': {
                'labels': indicators,
                'datasets': [{
                    'label': 'Performance Value',
                    'data': values,
                    'backgroundColor': 'rgba(54, 162, 235, 0.8)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 1
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
                        'text': 'Performance Metrics Analysis'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>📊 Performance Metrics Chart</h4>
            <canvas id="{chart_id}" width="400" height="300"></canvas>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        # Visualization overview tooltips
        self.add_tooltip("visualization_overview", TooltipData(
            title="Visualization Overview",
            description="Comprehensive analysis of interactive visualization capabilities and strategic data presentation.",
            source="Interactive Visualization Framework",
            strategic_impact="High - Critical for data-driven decision making and strategic communication",
            recommendations="• Use appropriate chart types for data\n• Ensure interactive capabilities\n• Maintain visual clarity\n• Provide context and explanations",
            use_cases="Used in strategic reporting, data analysis, and decision support",
            confidence=92.0
        ))
        
        self.add_tooltip("strategic_trends", TooltipData(
            title="Strategic Trends",
            description="Analysis of key trends and patterns in strategic data with interactive visualization capabilities.",
            source="Strategic Trends Analysis Framework",
            strategic_impact="High - Essential for trend identification and strategic planning",
            recommendations="• Monitor trend indicators regularly\n• Analyze trend patterns\n• Track trend evolution\n• Plan trend responses",
            use_cases="Used in strategic planning and trend analysis",
            confidence=88.0
        ))
        
        self.add_tooltip("data_metrics", TooltipData(
            title="Data Metrics",
            description="Comprehensive analysis of performance indicators and statistical metrics with interactive visualization.",
            source="Data Metrics Analysis Framework",
            strategic_impact="High - Critical for performance measurement and data quality assessment",
            recommendations="• Track key performance indicators\n• Monitor data quality metrics\n• Analyze statistical trends\n• Plan metric improvements",
            use_cases="Used in performance measurement and data analysis",
            confidence=90.0
        ))
        
        self.add_tooltip("interactive_charts", TooltipData(
            title="Interactive Charts",
            description="Advanced interactive chart configurations and capabilities for enhanced data visualization.",
            source="Interactive Chart Framework",
            strategic_impact="High - Essential for effective data communication and user engagement",
            recommendations="• Configure appropriate chart types\n• Enable interactive features\n• Ensure responsive design\n• Provide user guidance",
            use_cases="Used in data visualization and user interface design",
            confidence=85.0
        ))
    
    def _convert_trend_to_number(self, trend: str) -> float:
        """Convert trend level to numerical value for charts."""
        trend_map = {
            'Very Low': 20,
            'Low': 40,
            'Stable': 60,
            'High': 80,
            'Very High': 100
        }
        return trend_map.get(trend, 50.0)
    
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
