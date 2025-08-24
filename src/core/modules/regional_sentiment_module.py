"""
Regional Sentiment Module

Independent module for generating regional sentiment analysis sections that can be added to any report.
Provides regional sentiment trends, stakeholder analysis, diplomatic implications, and sentiment visualization.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class RegionalSentimentModule(BaseModule):
    """Regional Sentiment module for enhanced reports."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Regional Sentiment module."""
        if config is None:
            config = ModuleConfig(
                title="🌐 Regional Sentiment Analysis",
                description="Comprehensive analysis of regional sentiment trends and stakeholder perspectives",
                order=25,  # After geopolitical impact
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'regional_sentiment',
            'stakeholder_analysis',
            'diplomatic_implications',
            'sentiment_trends'
        ]
    
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate the HTML content for the Regional Sentiment module."""
        self.validate_data(data)
        
        regional_sentiment = data.get('regional_sentiment', {})
        stakeholder_analysis = data.get('stakeholder_analysis', {})
        diplomatic_implications = data.get('diplomatic_implications', [])
        sentiment_trends = data.get('sentiment_trends', {})
        
        # Generate sentiment overview
        overview_html = self._generate_sentiment_overview(regional_sentiment)
        
        # Generate stakeholder analysis
        stakeholders_html = self._generate_stakeholder_analysis(stakeholder_analysis)
        
        # Generate diplomatic implications
        diplomatic_html = self._generate_diplomatic_implications(diplomatic_implications)
        
        # Generate sentiment trends visualization
        trends_html = self._generate_sentiment_trends(sentiment_trends)
        
        # Generate interactive visualizations
        visualizations_html = self._generate_interactive_visualizations(data)
        
        return f"""
        <div class="section" id="regional-sentiment">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {overview_html}
            {stakeholders_html}
            {diplomatic_html}
            {trends_html}
            {visualizations_html}
        </div>
        """
    
    def _generate_sentiment_overview(self, sentiment_data: Dict[str, Any]) -> str:
        """Generate the regional sentiment overview section."""
        title = sentiment_data.get('title', 'Regional Sentiment Overview')
        overview = sentiment_data.get('overview', 'No regional sentiment overview available.')
        overall_sentiment = sentiment_data.get('overall_sentiment', 'Neutral')
        confidence_score = sentiment_data.get('confidence_score', 0.0)
        key_regions = sentiment_data.get('key_regions', [])
        
        regions_html = ""
        if key_regions:
            regions_html = """
            <div class="key-regions">
                <h4>🌍 Key Regional Sentiments</h4>
                <div class="regions-grid">
            """
            for i, region in enumerate(key_regions):
                region_id = f"region_{i}"
                regions_html += f"""
                <div class="region-card" data-tooltip-{self.module_id}="{region_id}">
                    <h5>{region.get('name', 'Unknown Region')}</h5>
                    <p class="region-sentiment">Sentiment: {region.get('sentiment', 'Neutral')}</p>
                    <p class="region-confidence">Confidence: {region.get('confidence', 0.0):.1%}</p>
                </div>
                """
            regions_html += """
                </div>
            </div>
            """
        
        return f"""
        <div class="sentiment-overview">
            <h3>📊 {title}</h3>
            <p>{overview}</p>
            
            <div class="sentiment-metrics">
                <div class="metric-card">
                    <div class="metric-label">Overall Sentiment</div>
                    <div class="metric-value sentiment-{overall_sentiment.lower()}">{overall_sentiment}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Confidence Score</div>
                    <div class="metric-value">{confidence_score:.1%}</div>
                </div>
            </div>
            
            {regions_html}
        </div>
        """
    
    def _generate_stakeholder_analysis(self, stakeholder_data: Dict[str, Any]) -> str:
        """Generate the stakeholder analysis section."""
        title = stakeholder_data.get('title', 'Stakeholder Analysis')
        overview = stakeholder_data.get('overview', 'No stakeholder analysis available.')
        stakeholders = stakeholder_data.get('stakeholders', [])
        impact_assessment = stakeholder_data.get('impact_assessment', {})
        
        stakeholders_html = ""
        if stakeholders:
            stakeholders_html = """
            <div class="stakeholders-list">
                <h4>👥 Key Stakeholders</h4>
                <div class="stakeholders-grid">
            """
            for i, stakeholder in enumerate(stakeholders):
                stakeholder_id = f"stakeholder_{i}"
                stakeholders_html += f"""
                <div class="stakeholder-card" data-tooltip-{self.module_id}="{stakeholder_id}">
                    <h5>{stakeholder.get('name', 'Unknown Stakeholder')}</h5>
                    <p class="stakeholder-type">{stakeholder.get('type', 'Unknown Type')}</p>
                    <p class="stakeholder-sentiment">Sentiment: {stakeholder.get('sentiment', 'Neutral')}</p>
                    <p class="stakeholder-influence">Influence: {stakeholder.get('influence_level', 'Medium')}</p>
                </div>
                """
            stakeholders_html += """
                </div>
            </div>
            """
        
        impact_html = ""
        if impact_assessment:
            impact_html = f"""
            <div class="impact-assessment">
                <h4>📈 Impact Assessment</h4>
                <p><strong>Primary Impact:</strong> {impact_assessment.get('primary_impact', 'Not specified')}</p>
                <p><strong>Secondary Impact:</strong> {impact_assessment.get('secondary_impact', 'Not specified')}</p>
                <p><strong>Risk Level:</strong> {impact_assessment.get('risk_level', 'Medium')}</p>
            </div>
            """
        
        return f"""
        <div class="stakeholder-analysis">
            <h3>👥 {title}</h3>
            <p>{overview}</p>
            
            {stakeholders_html}
            {impact_html}
        </div>
        """
    
    def _generate_diplomatic_implications(self, diplomatic_data: List[Dict[str, Any]]) -> str:
        """Generate the diplomatic implications section."""
        if not diplomatic_data:
            diplomatic_data = [{'implication': 'No diplomatic implications available.'}]
        
        implications_html = ""
        for i, implication in enumerate(diplomatic_data):
            implication_id = f"diplomatic_{i}"
            implications_html += f"""
            <div class="implication-item" data-tooltip-{self.module_id}="{implication_id}">
                <h4>🤝 {implication.get('title', f'Diplomatic Implication {i+1}')}</h4>
                <p>{implication.get('implication', 'No implication details available.')}</p>
                <div class="implication-metrics">
                    <span class="metric">Impact: {implication.get('impact_level', 'Medium')}</span>
                    <span class="metric">Timeline: {implication.get('timeline', 'Unknown')}</span>
                    <span class="metric">Confidence: {implication.get('confidence', 0.0):.1%}</span>
                </div>
            </div>
            """
        
        return f"""
        <div class="diplomatic-implications">
            <h3>🤝 Diplomatic Implications</h3>
            <div class="implications-list">
                {implications_html}
            </div>
        </div>
        """
    
    def _generate_sentiment_trends(self, trends_data: Dict[str, Any]) -> str:
        """Generate the sentiment trends visualization section."""
        title = trends_data.get('title', 'Sentiment Trends Analysis')
        overview = trends_data.get('overview', 'No sentiment trends overview available.')
        trends = trends_data.get('trends', [])
        time_period = trends_data.get('time_period', 'Recent')
        
        # Generate chart data
        chart_data = self._generate_sentiment_chart_data(trends)
        
        return f"""
        <div class="sentiment-trends">
            <h3>📈 {title}</h3>
            <p>{overview}</p>
            <p><strong>Analysis Period:</strong> {time_period}</p>
            
            <div class="chart-container">
                <canvas id="sentimentTrendsChart_{self.module_id}"></canvas>
            </div>
            
            <div class="trends-summary">
                <h4>📊 Trends Summary</h4>
                <div class="trends-grid">
                    {self._generate_trends_summary(trends)}
                </div>
            </div>
        </div>
        """
    
    def _generate_sentiment_chart_data(self, trends: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate chart data for sentiment trends."""
        if not trends:
            # Default data if no trends provided
            return {
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'datasets': [
                    {
                        'label': 'Positive Sentiment',
                        'data': [65, 70, 68, 72, 75, 78],
                        'borderColor': '#2ecc71',
                        'backgroundColor': 'rgba(46, 204, 113, 0.1)',
                        'tension': 0.4
                    },
                    {
                        'label': 'Neutral Sentiment',
                        'data': [25, 22, 24, 20, 18, 16],
                        'borderColor': '#f39c12',
                        'backgroundColor': 'rgba(243, 156, 18, 0.1)',
                        'tension': 0.4
                    },
                    {
                        'label': 'Negative Sentiment',
                        'data': [10, 8, 8, 8, 7, 6],
                        'borderColor': '#e74c3c',
                        'backgroundColor': 'rgba(231, 76, 60, 0.1)',
                        'tension': 0.4
                    }
                ]
            }
        
        # Process actual trends data
        labels = []
        positive_data = []
        neutral_data = []
        negative_data = []
        
        for trend in trends:
            labels.append(trend.get('period', 'Unknown'))
            positive_data.append(trend.get('positive_sentiment', 0))
            neutral_data.append(trend.get('neutral_sentiment', 0))
            negative_data.append(trend.get('negative_sentiment', 0))
        
        return {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Positive Sentiment',
                    'data': positive_data,
                    'borderColor': '#2ecc71',
                    'backgroundColor': 'rgba(46, 204, 113, 0.1)',
                    'tension': 0.4
                },
                {
                    'label': 'Neutral Sentiment',
                    'data': neutral_data,
                    'borderColor': '#f39c12',
                    'backgroundColor': 'rgba(243, 156, 18, 0.1)',
                    'tension': 0.4
                },
                {
                    'label': 'Negative Sentiment',
                    'data': negative_data,
                    'borderColor': '#e74c3c',
                    'backgroundColor': 'rgba(231, 76, 60, 0.1)',
                    'tension': 0.4
                }
            ]
        }
    
    def _generate_trends_summary(self, trends: List[Dict[str, Any]]) -> str:
        """Generate trends summary HTML."""
        if not trends:
            return '<p>No trends data available.</p>'
        
        summary_html = ""
        for trend in trends:
            summary_html += f"""
            <div class="trend-item">
                <h5>{trend.get('period', 'Unknown Period')}</h5>
                <p>Positive: {trend.get('positive_sentiment', 0):.1%}</p>
                <p>Neutral: {trend.get('neutral_sentiment', 0):.1%}</p>
                <p>Negative: {trend.get('negative_sentiment', 0):.1%}</p>
            </div>
            """
        
        return summary_html
    
    def _generate_interactive_visualizations(self, data: Dict[str, Any]) -> str:
        """Generate interactive visualizations for the module."""
        if not self.config.charts_enabled:
            return ""
        
        # Generate sentiment radar chart
        radar_chart = self._generate_sentiment_radar_chart(data)
        
        # Generate stakeholder influence chart
        influence_chart = self._generate_stakeholder_influence_chart(data)
        
        return f"""
        <div class="interactive-visualizations">
            <h3>📊 Interactive Visualizations</h3>
            
            <div class="charts-grid">
                <div class="chart-section">
                    <h4>🎯 Regional Sentiment Radar</h4>
                    {radar_chart}
                </div>
                
                <div class="chart-section">
                    <h4>👥 Stakeholder Influence Analysis</h4>
                    {influence_chart}
                </div>
            </div>
        </div>
        """
    
    def _generate_sentiment_radar_chart(self, data: Dict[str, Any]) -> str:
        """Generate sentiment radar chart."""
        regional_sentiment = data.get('regional_sentiment', {})
        key_regions = regional_sentiment.get('key_regions', [])
        
        if not key_regions:
            # Default data
            chart_data = {
                'labels': ['Region A', 'Region B', 'Region C', 'Region D', 'Region E'],
                'datasets': [{
                    'label': 'Sentiment Score',
                    'data': [75, 65, 80, 70, 85],
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 2
                }]
            }
        else:
            # Process actual data
            labels = [region.get('name', 'Unknown') for region in key_regions]
            sentiment_scores = [region.get('sentiment_score', 50) for region in key_regions]
            
            chart_data = {
                'labels': labels,
                'datasets': [{
                    'label': 'Sentiment Score',
                    'data': sentiment_scores,
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 2
                }]
            }
        
        # Add chart data to module
        chart_id = f"sentimentRadarChart_{self.module_id}"
        self.chart_data[chart_id] = {
            'type': 'radar',
            'data': chart_data,
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'scales': {
                    'r': {
                        'beginAtZero': True,
                        'max': 100,
                        'ticks': {
                            'stepSize': 20
                        }
                    }
                }
            }
        }
        
        return f'<canvas id="{chart_id}"></canvas>'
    
    def _generate_stakeholder_influence_chart(self, data: Dict[str, Any]) -> str:
        """Generate stakeholder influence chart."""
        stakeholder_analysis = data.get('stakeholder_analysis', {})
        stakeholders = stakeholder_analysis.get('stakeholders', [])
        
        if not stakeholders:
            # Default data
            chart_data = {
                'labels': ['Stakeholder A', 'Stakeholder B', 'Stakeholder C', 'Stakeholder D'],
                'datasets': [{
                    'label': 'Influence Level',
                    'data': [85, 70, 60, 45],
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)'
                    ],
                    'borderColor': [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    'borderWidth': 2
                }]
            }
        else:
            # Process actual data
            labels = [stakeholder.get('name', 'Unknown') for stakeholder in stakeholders]
            influence_levels = [stakeholder.get('influence_score', 50) for stakeholder in stakeholders]
            
            chart_data = {
                'labels': labels,
                'datasets': [{
                    'label': 'Influence Level',
                    'data': influence_levels,
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)'
                    ],
                    'borderColor': [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    'borderWidth': 2
                }]
            }
        
        # Add chart data to module
        chart_id = f"stakeholderInfluenceChart_{self.module_id}"
        self.chart_data[chart_id] = {
            'type': 'bar',
            'data': chart_data,
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'max': 100,
                        'ticks': {
                            'stepSize': 20
                        }
                    }
                }
            }
        }
        
        return f'<canvas id="{chart_id}"></canvas>'
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltips for the module."""
        self.tooltip_data = {
            'region_0': TooltipData(
                title="Regional Sentiment Analysis",
                description="Comprehensive analysis of sentiment trends across key regions, including stakeholder perspectives and diplomatic implications.",
                source="Sources: Regional sentiment data analysis, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="High - Influences diplomatic relations and regional cooperation",
                recommendations=[
                    "Monitor sentiment trends regularly",
                    "Engage with key stakeholders",
                    "Address negative sentiment proactively"
                ],
                use_cases=[
                    "Diplomatic planning",
                    "Regional cooperation strategies",
                    "Stakeholder engagement"
                ]
            ),
            'stakeholder_0': TooltipData(
                title="Stakeholder Analysis",
                description="Analysis of key stakeholders and their influence on regional sentiment and diplomatic relations.",
                source="Sources: Stakeholder mapping and influence assessment, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="Medium - Affects policy decisions and regional dynamics",
                recommendations=[
                    "Identify key stakeholders",
                    "Assess influence levels",
                    "Develop engagement strategies"
                ],
                use_cases=[
                    "Policy development",
                    "Stakeholder engagement",
                    "Risk assessment"
                ]
            ),
            'diplomatic_0': TooltipData(
                title="Diplomatic Implications",
                description="Analysis of how regional sentiment affects diplomatic relations and international cooperation.",
                source="Sources: Diplomatic impact assessment, Defense Intelligence Agency Reports, International Relations Database, Strategic Intelligence Reports, Military Capability Assessments",
                strategic_impact="High - Direct impact on international relations",
                recommendations=[
                    "Monitor diplomatic implications",
                    "Develop mitigation strategies",
                    "Strengthen bilateral relations"
                ],
                use_cases=[
                    "Diplomatic planning",
                    "International relations",
                    "Crisis management"
                ]
            )
        }
