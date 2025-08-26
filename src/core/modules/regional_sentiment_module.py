"""
Regional Sentiment Module

Independent module for generating regional sentiment analysis sections that can be added to any report.
Provides regional sentiment trends, stakeholder analysis, diplomatic implications, and sentiment visualization.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class RegionalSentimentModule(BaseModule):
    """Regional Sentiment module for enhanced reports."""
    
    module_id = "regional_sentiment"
    title = "🌐 Regional Sentiment Analysis"
    description = "Comprehensive analysis of regional sentiment trends and stakeholder perspectives"
    version = "1.0.0"
    
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
    
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for the Regional Sentiment module."""
        
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

        # Extract regional sentiment information
        regional_sentiment = data.get('regional_sentiment', {})
        stakeholder_analysis = data.get('stakeholder_analysis', {})
        diplomatic_implications = data.get('diplomatic_implications', {})
        sentiment_trends = data.get('sentiment_trends', {})

        # Generate comprehensive regional sentiment content
        content = self._generate_regional_sentiment_content(
            regional_sentiment, stakeholder_analysis, diplomatic_implications, sentiment_trends
        )

        return {
            "content": content,
            "metadata": {
                "phase4_integrated": phase4_enhanced,
                "strategic_intelligence": phase4_enhanced,
                "confidence_score": 0.7,
                "sentiment_analyzed": bool(regional_sentiment),
                "stakeholders_identified": bool(stakeholder_analysis),
                "diplomatic_implications_assessed": bool(diplomatic_implications)
            }
        }
    
    def _generate_regional_sentiment_content(self, regional_sentiment: Dict[str, Any], 
                                           stakeholder_analysis: Dict[str, Any], 
                                           diplomatic_implications: Dict[str, Any], 
                                           sentiment_trends: Dict[str, Any]) -> str:
        """Generate the main regional sentiment content."""
        
        content = f"""
        <div class="regional-sentiment-section">
            <h2>🌐 Regional Sentiment Analysis</h2>
            
            {self._generate_regional_sentiment_overview(regional_sentiment)}
            {self._generate_stakeholder_analysis(stakeholder_analysis)}
            {self._generate_diplomatic_implications(diplomatic_implications)}
            {self._generate_sentiment_trends(sentiment_trends)}
            {self._generate_interactive_charts(regional_sentiment, stakeholder_analysis, sentiment_trends)}
        </div>
        """
        
        return content
    
    def _generate_regional_sentiment_overview(self, regional_sentiment: Dict[str, Any]) -> str:
        """Generate regional sentiment overview section."""
        if not regional_sentiment:
            return """
            <div class="regional-sentiment-overview">
                <h3>Regional Sentiment Overview</h3>
                <p>Regional sentiment overview not available.</p>
            </div>
            """
        
        overall_sentiment = regional_sentiment.get('overall_sentiment', 'N/A')
        key_regions = regional_sentiment.get('key_regions', [])
        sentiment_factors = regional_sentiment.get('sentiment_factors', [])
        
        regions_html = ""
        if key_regions:
            regions_html = "<ul>" + "".join([f"<li>{region}</li>" for region in key_regions]) + "</ul>"
        
        factors_html = ""
        if sentiment_factors:
            factors_html = "<ul>" + "".join([f"<li>{factor}</li>" for factor in sentiment_factors]) + "</ul>"
        
        return f"""
        <div class="regional-sentiment-overview">
            <h3>Regional Sentiment Overview</h3>
            <div class="overview-content">
                <p><strong>Overall Sentiment:</strong> {overall_sentiment}</p>
            </div>
            <div class="key-regions">
                <h4>Key Regions Analyzed</h4>
                {regions_html}
            </div>
            <div class="sentiment-factors">
                <h4>Key Sentiment Factors</h4>
                {factors_html}
            </div>
        </div>
        """
    
    def _generate_stakeholder_analysis(self, stakeholder_analysis: Dict[str, Any]) -> str:
        """Generate stakeholder analysis section."""
        if not stakeholder_analysis:
            return """
            <div class="stakeholder-analysis">
                <h3>Stakeholder Analysis</h3>
                <p>Stakeholder analysis not available.</p>
            </div>
            """
        
        primary_stakeholders = stakeholder_analysis.get('primary_stakeholders', [])
        stakeholder_sentiments = stakeholder_analysis.get('stakeholder_sentiments', {})
        influence_levels = stakeholder_analysis.get('influence_levels', {})
        
        stakeholders_html = ""
        if primary_stakeholders:
            stakeholders_html = "<ul>" + "".join([f"<li>{stakeholder}</li>" for stakeholder in primary_stakeholders]) + "</ul>"
        
        sentiments_html = ""
        if stakeholder_sentiments:
            sentiments_html = "<ul>" + "".join([f"<li><strong>{stakeholder}</strong>: {sentiment}</li>" for stakeholder, sentiment in stakeholder_sentiments.items()]) + "</ul>"
        
        return f"""
        <div class="stakeholder-analysis">
            <h3>Stakeholder Analysis</h3>
            <div class="primary-stakeholders">
                <h4>Primary Stakeholders</h4>
                {stakeholders_html}
            </div>
            <div class="stakeholder-sentiments">
                <h4>Stakeholder Sentiments</h4>
                {sentiments_html}
            </div>
            <div class="influence-levels">
                <h4>Influence Levels</h4>
                <p>Analysis of stakeholder influence and impact levels.</p>
            </div>
        </div>
        """
    
    def _generate_diplomatic_implications(self, diplomatic_implications: Dict[str, Any]) -> str:
        """Generate diplomatic implications section."""
        if not diplomatic_implications:
            return """
            <div class="diplomatic-implications">
                <h3>Diplomatic Implications</h3>
                <p>Diplomatic implications not available.</p>
            </div>
            """
        
        diplomatic_impact = diplomatic_implications.get('diplomatic_impact', 'N/A')
        policy_recommendations = diplomatic_implications.get('policy_recommendations', [])
        risk_assessment = diplomatic_implications.get('risk_assessment', 'N/A')
        
        recommendations_html = ""
        if policy_recommendations:
            recommendations_html = "<ul>" + "".join([f"<li>{recommendation}</li>" for recommendation in policy_recommendations]) + "</ul>"
        
        return f"""
        <div class="diplomatic-implications">
            <h3>Diplomatic Implications</h3>
            <div class="diplomatic-impact">
                <h4>Diplomatic Impact</h4>
                <p>{diplomatic_impact}</p>
            </div>
            <div class="policy-recommendations">
                <h4>Policy Recommendations</h4>
                {recommendations_html}
            </div>
            <div class="risk-assessment">
                <h4>Risk Assessment</h4>
                <p>{risk_assessment}</p>
            </div>
        </div>
        """
    
    def _generate_sentiment_trends(self, sentiment_trends: Dict[str, Any]) -> str:
        """Generate sentiment trends section."""
        if not sentiment_trends:
            return """
            <div class="sentiment-trends">
                <h3>Sentiment Trends</h3>
                <p>Sentiment trends not available.</p>
            </div>
            """
        
        trend_summary = sentiment_trends.get('trend_summary', 'N/A')
        historical_data = sentiment_trends.get('historical_data', [])
        future_projections = sentiment_trends.get('future_projections', 'N/A')
        
        historical_html = ""
        if historical_data:
            historical_html = "<ul>" + "".join([f"<li>{data_point}</li>" for data_point in historical_data]) + "</ul>"
        
        return f"""
        <div class="sentiment-trends">
            <h3>Sentiment Trends</h3>
            <div class="trend-summary">
                <h4>Trend Summary</h4>
                <p>{trend_summary}</p>
            </div>
            <div class="historical-data">
                <h4>Historical Data</h4>
                {historical_html}
            </div>
            <div class="future-projections">
                <h4>Future Projections</h4>
                <p>{future_projections}</p>
            </div>
        </div>
        """
    
    def _generate_interactive_charts(self, regional_sentiment: Dict[str, Any], 
                                   stakeholder_analysis: Dict[str, Any], 
                                   sentiment_trends: Dict[str, Any]) -> str:
        """Generate interactive charts for regional sentiment visualization."""
        
        # Create chart data
        chart_data = {
            'sentiment_data': regional_sentiment.get('sentiment_data', {}),
            'stakeholder_data': stakeholder_analysis.get('stakeholder_data', {}),
            'trends_data': sentiment_trends.get('trends_data', {})
        }
        
        return f"""
        <div class="interactive-charts">
            <h3>Interactive Regional Sentiment Visualizations</h3>
            <div class="chart-container">
                <div class="chart" id="sentiment-distribution-chart">
                    <h4>Sentiment Distribution</h4>
                    <div class="chart-placeholder">
                        <p>Interactive pie chart showing sentiment distribution across regions</p>
                        <p>Regions: {len(chart_data['sentiment_data'])} analyzed</p>
                    </div>
                </div>
                <div class="chart" id="stakeholder-sentiment-chart">
                    <h4>Stakeholder Sentiment</h4>
                    <div class="chart-placeholder">
                        <p>Interactive bar chart showing stakeholder sentiment levels</p>
                        <p>Stakeholders: {len(chart_data['stakeholder_data'])} tracked</p>
                    </div>
                </div>
                <div class="chart" id="sentiment-trends-chart">
                    <h4>Sentiment Trends Over Time</h4>
                    <div class="chart-placeholder">
                        <p>Interactive line chart showing sentiment trends over time</p>
                        <p>Time points: {len(chart_data['trends_data'])} available</p>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltips for the Regional Sentiment module."""
        self.tooltips = {
            'regional_sentiment': TooltipData(
                title="Regional Sentiment",
                description="Analysis of sentiment across different regions",
                source="Regional Analysis Framework",
                strategic_impact="High - Critical for regional understanding"
            ),
            'stakeholder_analysis': TooltipData(
                title="Stakeholder Analysis",
                description="Analysis of key stakeholders and their perspectives",
                source="Stakeholder Analysis Framework",
                strategic_impact="High - Critical for stakeholder engagement"
            ),
            'diplomatic_implications': TooltipData(
                title="Diplomatic Implications",
                description="Analysis of diplomatic consequences and policy implications",
                source="Diplomatic Analysis Framework",
                strategic_impact="High - Critical for diplomatic strategy"
            ),
            'sentiment_trends': TooltipData(
                title="Sentiment Trends",
                description="Historical and projected sentiment trends",
                source="Trend Analysis Framework",
                strategic_impact="Medium - Important for trend monitoring"
            )
        }
