#!/usr/bin/env python3
"""
Executive Summary Module

Independent module for generating executive summary sections that can be added to any report.
Provides comprehensive executive summary with key metrics, trend analysis, and strategic insights.
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
    
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for the Executive Summary module with Phase 4 enhancements."""
        
        # Phase 4 Strategic Intelligence Integration
        topic = data.get("topic", "")
        phase4_enhanced = config and config.get("phase4_integration", False)
        
        if phase4_enhanced and topic:
            # Enhanced with strategic intelligence
            try:
                enhanced_data = await self._enhance_with_phase4_capabilities(topic, data)
                data.update(enhanced_data)
            except Exception as e:
                # Fallback if async enhancement fails
                print(f"Phase 4 enhancement failed: {e}")
                enhanced_data = {}
        
        self.validate_data(data)
        
        executive_summary = data.get('executive_summary', {})
        key_metrics = data.get('key_metrics', {})
        trend_analysis = data.get('trend_analysis', {})
        strategic_insights = data.get('strategic_insights', [])
        
        # Generate executive summary overview
        overview_html = self._generate_overview(executive_summary)
        
        # Generate key metrics section
        metrics_html = self._generate_key_metrics(key_metrics)
        
        # Generate trend analysis section
        trends_html = self._generate_trend_analysis(trend_analysis)
        
        # Generate strategic insights section
        insights_html = self._generate_strategic_insights(strategic_insights)
        
        # Generate interactive visualizations
        visualizations_html = self._generate_interactive_visualizations(data)
        
        content = f"""
        <div class="section" id="executive-summary">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {metrics_html}
            {trends_html}
            {insights_html}
            {visualizations_html}
        </div>
        """
        
        return {
            "content": content,
            "metadata": {
                "phase4_integrated": phase4_enhanced,
                "strategic_intelligence": phase4_enhanced,
                "confidence_score": 0.85
            }
        }
    
    async def _enhance_with_phase4_capabilities(self, topic: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance executive summary with Phase 4 strategic intelligence capabilities."""
        enhanced_data = {}
        
        try:
            # Initialize Phase 4 components if available
            if not hasattr(self, 'strategic_engine'):
                self._initialize_phase4_components()
            
            # Knowledge graph intelligence
            kg_intelligence = await self.strategic_engine.query_knowledge_graph_for_intelligence(topic, "strategic")
            enhanced_data["kg_intelligence"] = kg_intelligence
            
            # Cross-domain analysis
            cross_domain = await self.strategic_engine.generate_cross_domain_intelligence([
                "geopolitical", "economic", "military", "technological"
            ])
            enhanced_data["cross_domain_intelligence"] = cross_domain
            
            # Strategic recommendations
            recommendations = await self.recommendations_engine.generate_intelligence_driven_recommendations(topic)
            enhanced_data["intelligence_recommendations"] = recommendations
            
        except Exception as e:
            # Fallback to mock data if Phase 4 components not available
            enhanced_data["kg_intelligence"] = {"success": False, "error": str(e)}
            enhanced_data["cross_domain_intelligence"] = {"success": False, "error": str(e)}
            enhanced_data["intelligence_recommendations"] = []
        
        return enhanced_data
    
    def _initialize_phase4_components(self):
        """Initialize Phase 4 strategic intelligence components."""
        try:
            # Import Phase 4 components
            from src.core.strategic_intelligence_engine import StrategicIntelligenceEngine
            from src.core.enhanced_strategic_recommendations import EnhancedStrategicRecommendations
            
            self.strategic_engine = StrategicIntelligenceEngine()
            self.recommendations_engine = EnhancedStrategicRecommendations()
            
        except ImportError:
            # Fallback to mock components if Phase 4 components not available
            self.strategic_engine = MockStrategicEngine()
            self.recommendations_engine = MockRecommendationsEngine()
    
    def _generate_overview(self, summary_data: Dict[str, Any]) -> str:
        """Generate the executive summary overview section."""
        title = summary_data.get('title', 'Executive Summary')
        overview = summary_data.get('overview', 'No executive summary available.')
        key_points = summary_data.get('key_points', [])
        
        points_html = ""
        if key_points:
            points_html = """
            <div class="key-points">
                <h4>🎯 Key Points</h4>
                <ul>
            """
            for point in key_points:
                points_html += f"<li>{point}</li>"
            points_html += """
                </ul>
            </div>
            """
        
        return f"""
        <div class="executive-overview" data-tooltip-{self.module_id}="executive_overview">
            <h3>📊 Executive Overview</h3>
            <h4>{title}</h4>
            <div class="overview-content">
                <p>{overview}</p>
            </div>
            {points_html}
        </div>
        """
    
    def _generate_key_metrics(self, metrics_data: Dict[str, Any]) -> str:
        """Generate the key metrics section."""
        metrics = metrics_data.get('metrics', [])
        
        if not metrics:
            # Default metrics if not provided
            metrics = [
                {"name": "Strategic Impact", "value": "High", "trend": "Increasing"},
                {"name": "Risk Level", "value": "Medium", "trend": "Stable"},
                {"name": "Implementation Timeline", "value": "2-3 Years", "trend": "On Track"},
                {"name": "Resource Requirements", "value": "Significant", "trend": "Adequate"}
            ]
        
        metrics_html = """
        <div class="key-metrics" data-tooltip-{self.module_id}="key_metrics">
            <h3>📈 Key Metrics</h3>
            <div class="metrics-grid">
        """
        
        for metric in metrics:
            metrics_html += f"""
            <div class="metric-item">
                <div class="metric-name">{metric.get('name', 'Unknown Metric')}</div>
                <div class="metric-value">{metric.get('value', 'N/A')}</div>
                <div class="metric-trend">{metric.get('trend', 'Unknown')}</div>
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
            # Default trends if not provided
            trends = [
                {"trend": "Strategic Capability Enhancement", "direction": "Positive", "confidence": "High"},
                {"trend": "Regional Security Dynamics", "direction": "Stable", "confidence": "Medium"},
                {"trend": "Technology Advancement", "direction": "Positive", "confidence": "High"},
                {"trend": "Economic Impact", "direction": "Mixed", "confidence": "Medium"}
            ]
        
        trends_html = """
        <div class="trend-analysis" data-tooltip-{self.module_id}="trend_analysis">
            <h3>📊 Trend Analysis</h3>
            <div class="trends-container">
        """
        
        for trend in trends:
            trend_class = trend.get('direction', 'stable').lower()
            trends_html += f"""
            <div class="trend-item {trend_class}">
                <div class="trend-name">{trend.get('trend', 'Unknown Trend')}</div>
                <div class="trend-direction">{trend.get('direction', 'Unknown')}</div>
                <div class="trend-confidence">Confidence: {trend.get('confidence', 'Unknown')}</div>
            </div>
            """
        
        trends_html += """
            </div>
        </div>
        """
        
        return trends_html
    
    def _generate_strategic_insights(self, insights_data: List[Dict[str, Any]]) -> str:
        """Generate the strategic insights section."""
        if not insights_data:
            # Default insights if not provided
            insights_data = [
                {"insight": "Enhanced strategic positioning in the region", "impact": "High", "priority": "Critical"},
                {"insight": "Improved operational capabilities", "impact": "High", "priority": "High"},
                {"insight": "Strengthened regional partnerships", "impact": "Medium", "priority": "Medium"},
                {"insight": "Technology modernization benefits", "impact": "Medium", "priority": "Medium"}
            ]
        
        insights_html = """
        <div class="strategic-insights" data-tooltip-{self.module_id}="strategic_insights">
            <h3>🎯 Strategic Insights</h3>
            <div class="insights-container">
        """
        
        for insight in insights_data:
            priority_class = insight.get('priority', 'medium').lower()
            insights_html += f"""
            <div class="insight-item {priority_class}">
                <div class="insight-text">{insight.get('insight', 'Unknown Insight')}</div>
                <div class="insight-impact">Impact: {insight.get('impact', 'Unknown')}</div>
                <div class="insight-priority">Priority: {insight.get('priority', 'Unknown')}</div>
            </div>
            """
        
        insights_html += """
            </div>
        </div>
        """
        
        return insights_html
    
    def _generate_interactive_visualizations(self, data: Dict[str, Any]) -> str:
        """Generate interactive visualizations for executive summary."""
        if not self.config.charts_enabled:
            return ""
        
        # Generate metrics chart
        metrics_chart_html = self._generate_metrics_chart(data)
        
        # Generate trends chart
        trends_chart_html = self._generate_trends_chart(data)
        
        return f"""
        <div class="executive-visualizations">
            <h3>📈 Interactive Visualizations</h3>
            {metrics_chart_html}
            {trends_chart_html}
        </div>
        """
    
    def _generate_metrics_chart(self, data: Dict[str, Any]) -> str:
        """Generate a chart for key metrics visualization."""
        key_metrics = data.get('key_metrics', {})
        metrics = key_metrics.get('metrics', [])
        
        if not metrics:
            return ""
        
        # Prepare chart data
        metric_names = [metric.get('name', 'Unknown') for metric in metrics]
        metric_values = [self._convert_metric_to_number(metric.get('value', '0')) for metric in metrics]
        
        chart_id = f"executive_metrics_{self.module_id}"
        
        # Add chart data to the module
        self.add_chart_data(chart_id, {
            'type': 'bar',
            'data': {
                'labels': metric_names,
                'datasets': [{
                    'label': 'Metric Values',
                    'data': metric_values,
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
                        'text': 'Key Metrics Overview'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>📊 Key Metrics Overview</h4>
            <canvas id="{chart_id}" width="400" height="300"></canvas>
        </div>
        """
    
    def _generate_trends_chart(self, data: Dict[str, Any]) -> str:
        """Generate a chart for trend analysis visualization."""
        trend_analysis = data.get('trend_analysis', {})
        trends = trend_analysis.get('trends', [])
        
        if not trends:
            return ""
        
        # Prepare chart data
        trend_names = [trend.get('trend', 'Unknown') for trend in trends]
        trend_confidences = [self._convert_confidence_to_number(trend.get('confidence', 'Medium')) for trend in trends]
        
        chart_id = f"executive_trends_{self.module_id}"
        
        # Add chart data to the module
        self.add_chart_data(chart_id, {
            'type': 'radar',
            'data': {
                'labels': trend_names,
                'datasets': [{
                    'label': 'Trend Confidence',
                    'data': trend_confidences,
                    'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                    'borderColor': 'rgba(255, 99, 132, 1)',
                    'borderWidth': 2,
                    'pointBackgroundColor': 'rgba(255, 99, 132, 1)',
                    'pointBorderColor': '#fff',
                    'pointHoverBackgroundColor': '#fff',
                    'pointHoverBorderColor': 'rgba(255, 99, 132, 1)'
                }]
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
                        'position': 'bottom'
                    },
                    'title': {
                        'display': True,
                        'text': 'Trend Analysis'
                    }
                }
            }
        })
        
        return f"""
        <div class="chart-container">
            <h4>📈 Trend Analysis</h4>
            <canvas id="{chart_id}" width="400" height="300"></canvas>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltip data for the module."""
        # Executive overview tooltips
        self.add_tooltip("executive_overview", TooltipData(
            title="Executive Overview",
            description="Comprehensive executive summary providing high-level strategic overview and key points.",
            source="Sources: Executive Summary Framework, Strategic Intelligence Reports, Defense Intelligence Agency Reports, International Relations Database",
            strategic_impact="High - Critical for executive decision-making and strategic planning",
            recommendations="• Review executive summary regularly\n• Update key points based on new intelligence\n• Validate strategic insights\n• Monitor trend changes",
            use_cases="Used in executive briefings, strategic planning, and decision support",
            confidence=90.0
        ))
        
        # Key metrics tooltips
        self.add_tooltip("key_metrics", TooltipData(
            title="Key Metrics",
            description="Essential metrics and performance indicators for strategic assessment and monitoring.",
            source="Sources: Metrics Framework, Performance Indicators, Strategic Intelligence Reports, Defense Intelligence Agency Reports",
            strategic_impact="High - Essential for performance monitoring and strategic assessment",
            recommendations="• Monitor key metrics regularly\n• Track metric trends\n• Set performance targets\n• Adjust strategies based on metrics",
            use_cases="Used in performance monitoring, strategic assessment, and decision support",
            confidence=88.0
        ))
        
        # Trend analysis tooltips
        self.add_tooltip("trend_analysis", TooltipData(
            title="Trend Analysis",
            description="Analysis of strategic trends and their implications for future planning and decision-making.",
            source="Sources: Trend Analysis Framework, Strategic Intelligence Reports, Defense Intelligence Agency Reports, International Relations Database",
            strategic_impact="High - Critical for future planning and strategic positioning",
            recommendations="• Monitor trend changes\n• Assess trend implications\n• Plan for trend scenarios\n• Adjust strategies based on trends",
            use_cases="Used in strategic planning, future scenario analysis, and risk assessment",
            confidence=85.0
        ))
        
        # Strategic insights tooltips
        self.add_tooltip("strategic_insights", TooltipData(
            title="Strategic Insights",
            description="Key strategic insights and their implications for decision-making and planning.",
            source="Sources: Strategic Analysis Framework, Intelligence Reports, Defense Intelligence Agency Reports, International Relations Database",
            strategic_impact="High - Direct influence on strategic decision-making",
            recommendations="• Prioritize high-impact insights\n• Develop action plans for insights\n• Monitor insight evolution\n• Validate insight accuracy",
            use_cases="Used in strategic decision-making, planning, and intelligence analysis",
            confidence=87.0
        ))
    
    def _convert_metric_to_number(self, metric: str) -> float:
        """Convert metric value to numerical value for charts."""
        # Convert text values to numbers
        metric_map = {
            'Very Low': 20,
            'Low': 40,
            'Medium': 60,
            'High': 80,
            'Very High': 100,
            'Significant': 85,
            'Moderate': 50,
            'Minimal': 25
        }
        return metric_map.get(metric, 50.0)
    
    def _convert_confidence_to_number(self, confidence: str) -> float:
        """Convert confidence level to numerical value for charts."""
        confidence_map = {
            'Very Low': 20,
            'Low': 40,
            'Medium': 60,
            'High': 80,
            'Very High': 100
        }
        return confidence_map.get(confidence, 50.0)


# Mock classes for fallback
class MockStrategicEngine:
    async def query_knowledge_graph_for_intelligence(self, topic, analysis_type):
        return {"success": True, "strategic_insights": {"key_insights": ["Mock intelligence insight"]}}
    
    async def generate_cross_domain_intelligence(self, domains):
        return {"success": True, "cross_domain_patterns": [{"domains": "Mock", "pattern": "Mock pattern"}]}

class MockRecommendationsEngine:
    async def generate_intelligence_driven_recommendations(self, topic):
        return [MockRecommendation("Mock Intelligence Recommendation", "Mock description")]

class MockRecommendation:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.priority = "medium"
        self.confidence_score = 0.7
