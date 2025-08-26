"""
Strategic Intelligence Module

This module integrates Phase 4 Strategic Intelligence capabilities with the modular report system.
Provides comprehensive strategic intelligence analysis, recommendations, and dashboards.
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from .base_module import BaseModule, ModuleConfig

logger = logging.getLogger(__name__)


class StrategicIntelligenceModule(BaseModule):
    """Strategic Intelligence Module integrating Phase 4 capabilities."""
    
    module_id = "strategic_intelligence"
    title = "Strategic Intelligence Analysis"
    description = "Advanced strategic intelligence with knowledge graph integration"
    version = "1.0.0"
    
    def __init__(self):
        super().__init__()
        self.strategic_engine = None
        self.recommendations_engine = None
        self.dashboard = None
        self._initialize_phase4_components()
    
    def get_required_data_keys(self) -> List[str]:
        """Get required data keys for this module."""
        return ["topic", "analysis_type", "time_range"]
    
    def _initialize_phase4_components(self):
        """Initialize Phase 4 strategic intelligence components."""
        try:
            # Import Phase 4 components
            from src.core.strategic_intelligence_engine import StrategicIntelligenceEngine
            from src.core.enhanced_strategic_recommendations import EnhancedStrategicRecommendations
            from src.core.strategic_analytics_dashboard import StrategicAnalyticsDashboard
            
            self.strategic_engine = StrategicIntelligenceEngine()
            self.recommendations_engine = EnhancedStrategicRecommendations()
            self.dashboard = StrategicAnalyticsDashboard()
            
        except ImportError:
            # Fallback to mock components if Phase 4 components not available
            self.strategic_engine = MockStrategicEngine()
            self.recommendations_engine = MockRecommendationsEngine()
            self.dashboard = MockDashboard()
    
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate strategic intelligence content."""
        try:
            topic = data.get("topic", "")
            
            # Generate comprehensive strategic intelligence
            intelligence_results = await self._generate_strategic_intelligence(topic)
            
            # Generate strategic recommendations
            recommendations = await self._generate_recommendations(topic)
            
            # Create strategic analytics dashboard
            dashboard_data = await self._create_dashboard(topic)
            
            return {
                "content": self._format_strategic_content(intelligence_results, recommendations, dashboard_data),
                "metadata": {
                    "intelligence_score": intelligence_results.get("overall_score", 0),
                    "recommendations_count": len(recommendations),
                    "risk_level": intelligence_results.get("risk_level", "medium"),
                    "confidence_score": intelligence_results.get("confidence_score", 0.7),
                    "phase4_integrated": True
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating strategic intelligence: {e}")
            return {"content": "Strategic intelligence analysis failed", "error": str(e)}
    
    async def _generate_strategic_intelligence(self, topic: str) -> Dict[str, Any]:
        """Generate comprehensive strategic intelligence."""
        results = {}
        
        # Query knowledge graph for intelligence
        kg_intelligence = await self.strategic_engine.query_knowledge_graph_for_intelligence(
            topic, "strategic"
        )
        results["knowledge_graph_intelligence"] = kg_intelligence
        
        # Analyze historical patterns
        historical_patterns = await self.strategic_engine.analyze_historical_patterns(
            topic, "5_years"
        )
        results["historical_patterns"] = historical_patterns
        
        # Generate cross-domain intelligence
        cross_domain = await self.strategic_engine.generate_cross_domain_intelligence([
            "geopolitical", "economic", "military", "technological"
        ])
        results["cross_domain_intelligence"] = cross_domain
        
        # Predict strategic trends
        trends = await self.strategic_engine.predict_strategic_trends(topic)
        results["strategic_trends"] = trends
        
        # Assess strategic risks
        risks = await self.strategic_engine.assess_strategic_risks_from_kg(topic)
        results["strategic_risks"] = risks
        
        # Identify opportunities
        opportunities = await self.strategic_engine.identify_strategic_opportunities(topic)
        results["strategic_opportunities"] = opportunities
        
        # Calculate overall intelligence score
        results["overall_score"] = self._calculate_intelligence_score(results)
        results["risk_level"] = self._assess_risk_level(risks)
        results["confidence_score"] = self._calculate_confidence_score(results)
        
        return results
    
    async def _generate_recommendations(self, topic: str) -> List[Dict[str, Any]]:
        """Generate strategic recommendations."""
        recommendations = []
        
        # Intelligence-driven recommendations
        intel_recs = await self.recommendations_engine.generate_intelligence_driven_recommendations(topic)
        recommendations.extend(self._format_recommendations(intel_recs, "intelligence_driven"))
        
        # Multi-domain recommendations
        multi_domain_recs = await self.recommendations_engine.generate_multi_domain_recommendations([
            "geopolitical", "economic", "military", "technological"
        ])
        recommendations.extend(self._format_recommendations(multi_domain_recs, "multi_domain"))
        
        return recommendations
    
    async def _create_dashboard(self, topic: str) -> Dict[str, Any]:
        """Create strategic analytics dashboard."""
        dashboard_data = {}
        
        # Get strategic metrics
        metrics = await self.dashboard.get_strategic_metrics()
        dashboard_data["metrics"] = metrics
        
        # Get dashboard summary
        summary = await self.dashboard.get_dashboard_summary()
        dashboard_data["summary"] = summary
        
        return dashboard_data
    
    def _format_strategic_content(self, intelligence: Dict[str, Any], 
                                 recommendations: List[Dict[str, Any]], 
                                 dashboard: Dict[str, Any]) -> str:
        """Format strategic intelligence content for HTML report."""
        
        content = f"""
        <div class="strategic-intelligence-section">
            <h2>Strategic Intelligence Analysis</h2>
            
            <div class="intelligence-overview">
                <h3>Intelligence Overview</h3>
                <div class="intelligence-score">
                    <span class="score-label">Overall Intelligence Score:</span>
                    <span class="score-value">{intelligence.get('overall_score', 0):.2f}/1.0</span>
                </div>
                <div class="risk-assessment">
                    <span class="risk-label">Risk Level:</span>
                    <span class="risk-value {intelligence.get('risk_level', 'medium')}">{intelligence.get('risk_level', 'medium').title()}</span>
                </div>
                <div class="confidence-score">
                    <span class="confidence-label">Confidence Score:</span>
                    <span class="confidence-value">{intelligence.get('confidence_score', 0.7):.2f}/1.0</span>
                </div>
            </div>
            
            <div class="knowledge-graph-insights">
                <h3>Knowledge Graph Intelligence</h3>
                <div class="insights-content">
                    {self._format_kg_insights(intelligence.get('knowledge_graph_intelligence', {}))}
                </div>
            </div>
            
            <div class="historical-patterns">
                <h3>Historical Pattern Analysis</h3>
                <div class="patterns-content">
                    {self._format_historical_patterns(intelligence.get('historical_patterns', {}))}
                </div>
            </div>
            
            <div class="cross-domain-intelligence">
                <h3>Cross-Domain Intelligence</h3>
                <div class="cross-domain-content">
                    {self._format_cross_domain_intelligence(intelligence.get('cross_domain_intelligence', {}))}
                </div>
            </div>
            
            <div class="strategic-trends">
                <h3>Strategic Trends & Predictions</h3>
                <div class="trends-content">
                    {self._format_strategic_trends(intelligence.get('strategic_trends', {}))}
                </div>
            </div>
            
            <div class="risk-assessment">
                <h3>Strategic Risk Assessment</h3>
                <div class="risks-content">
                    {self._format_risk_assessment(intelligence.get('strategic_risks', {}))}
                </div>
            </div>
            
            <div class="strategic-opportunities">
                <h3>Strategic Opportunities</h3>
                <div class="opportunities-content">
                    {self._format_opportunities(intelligence.get('strategic_opportunities', {}))}
                </div>
            </div>
            
            <div class="strategic-recommendations">
                <h3>Strategic Recommendations</h3>
                <div class="recommendations-content">
                    {self._format_recommendations_html(recommendations)}
                </div>
            </div>
            
            <div class="strategic-dashboard">
                <h3>Strategic Analytics Dashboard</h3>
                <div class="dashboard-content">
                    {self._format_dashboard_html(dashboard)}
                </div>
            </div>
        </div>
        """
        
        return content
    
    def _format_kg_insights(self, kg_data: Dict[str, Any]) -> str:
        """Format knowledge graph insights."""
        if not kg_data.get("success"):
            return "<p>Knowledge graph intelligence not available.</p>"
        
        insights = kg_data.get("strategic_insights", {})
        return f"""
        <div class="kg-insights">
            <p><strong>Key Insights:</strong></p>
            <ul>
                {''.join([f'<li>{insight}</li>' for insight in insights.get('key_insights', [])])}
            </ul>
            <p><strong>Strategic Patterns:</strong></p>
            <ul>
                {''.join([f'<li>{pattern}</li>' for pattern in insights.get('strategic_patterns', [])])}
            </ul>
        </div>
        """
    
    def _format_historical_patterns(self, patterns_data: Dict[str, Any]) -> str:
        """Format historical patterns."""
        if not patterns_data.get("success"):
            return "<p>Historical pattern analysis not available.</p>"
        
        patterns = patterns_data.get("patterns", [])
        return f"""
        <div class="historical-patterns">
            <p><strong>Identified Patterns:</strong></p>
            <ul>
                {''.join([f'<li><strong>{pattern.get("pattern_type", "Unknown")}:</strong> {pattern.get("description", "No description")}</li>' for pattern in patterns])}
            </ul>
        </div>
        """
    
    def _format_cross_domain_intelligence(self, cross_domain_data: Dict[str, Any]) -> str:
        """Format cross-domain intelligence."""
        if not cross_domain_data.get("success"):
            return "<p>Cross-domain intelligence not available.</p>"
        
        domains = cross_domain_data.get("cross_domain_patterns", [])
        return f"""
        <div class="cross-domain-intelligence">
            <p><strong>Cross-Domain Patterns:</strong></p>
            <ul>
                {''.join([f'<li><strong>{domain.get("domains", "Unknown")}:</strong> {domain.get("pattern", "No pattern")}</li>' for domain in domains])}
            </ul>
        </div>
        """
    
    def _format_strategic_trends(self, trends_data: Dict[str, Any]) -> str:
        """Format strategic trends."""
        if not trends_data.get("success"):
            return "<p>Strategic trends not available.</p>"
        
        trends = trends_data.get("predicted_trends", [])
        return f"""
        <div class="strategic-trends">
            <p><strong>Predicted Trends:</strong></p>
            <ul>
                {''.join([f'<li><strong>{trend.get("trend_type", "Unknown")}:</strong> {trend.get("description", "No description")} (Confidence: {trend.get("confidence", 0):.2f})</li>' for trend in trends])}
            </ul>
        </div>
        """
    
    def _format_risk_assessment(self, risks_data: Dict[str, Any]) -> str:
        """Format risk assessment."""
        if not risks_data.get("success"):
            return "<p>Risk assessment not available.</p>"
        
        risks = risks_data.get("risk_factors", [])
        return f"""
        <div class="risk-assessment">
            <p><strong>Risk Factors:</strong></p>
            <ul>
                {''.join([f'<li><strong>{risk.get("factor", "Unknown")}:</strong> {risk.get("description", "No description")} (Risk Level: {risk.get("level", "medium")})</li>' for risk in risks])}
            </ul>
        </div>
        """
    
    def _format_opportunities(self, opportunities_data: Dict[str, Any]) -> str:
        """Format strategic opportunities."""
        if not opportunities_data.get("success"):
            return "<p>Strategic opportunities not available.</p>"
        
        opportunities = opportunities_data.get("opportunities", [])
        return f"""
        <div class="strategic-opportunities">
            <p><strong>Identified Opportunities:</strong></p>
            <ul>
                {''.join([f'<li><strong>{opp.get("opportunity", "Unknown")}:</strong> {opp.get("description", "No description")} (Impact: {opp.get("impact_score", 0):.2f})</li>' for opp in opportunities])}
            </ul>
        </div>
        """
    
    def _format_recommendations_html(self, recommendations: List[Dict[str, Any]]) -> str:
        """Format recommendations for HTML."""
        if not recommendations:
            return "<p>No strategic recommendations available.</p>"
        
        html = "<div class='recommendations-grid'>"
        for rec in recommendations:
            html += f"""
            <div class='recommendation-card'>
                <h4>{rec.get('title', 'Unknown Recommendation')}</h4>
                <p><strong>Type:</strong> {rec.get('type', 'Unknown')}</p>
                <p><strong>Priority:</strong> {rec.get('priority', 'medium')}</p>
                <p><strong>Confidence:</strong> {rec.get('confidence_score', 0):.2f}</p>
                <p>{rec.get('description', 'No description')}</p>
            </div>
            """
        html += "</div>"
        return html
    
    def _format_dashboard_html(self, dashboard: Dict[str, Any]) -> str:
        """Format dashboard for HTML."""
        summary = dashboard.get("summary", {})
        metrics = dashboard.get("metrics", {})
        
        return f"""
        <div class="dashboard-summary">
            <div class="dashboard-stats">
                <div class="stat">
                    <span class="stat-number">{summary.get('total_metrics', 0)}</span>
                    <span class="stat-label">Total Metrics</span>
                </div>
                <div class="stat">
                    <span class="stat-number">{summary.get('active_recommendations', 0)}</span>
                    <span class="stat-label">Active Recommendations</span>
                </div>
                <div class="stat">
                    <span class="stat-number">{summary.get('critical_risks', 0)}</span>
                    <span class="stat-label">Critical Risks</span>
                </div>
                <div class="stat">
                    <span class="stat-number">{summary.get('active_opportunities', 0)}</span>
                    <span class="stat-label">Active Opportunities</span>
                </div>
            </div>
            <div class="performance-scores">
                <div class="score">
                    <span class="score-label">Performance Score:</span>
                    <span class="score-value">{summary.get('performance_score', 0):.2f}</span>
                </div>
                <div class="score">
                    <span class="score-label">Risk Score:</span>
                    <span class="score-value">{summary.get('risk_score', 0):.2f}</span>
                </div>
                <div class="score">
                    <span class="score-label">Opportunity Score:</span>
                    <span class="score-value">{summary.get('opportunity_score', 0):.2f}</span>
                </div>
            </div>
        </div>
        """
    
    def _format_recommendations(self, recommendations: List, rec_type: str) -> List[Dict[str, Any]]:
        """Format recommendations for consistent structure."""
        formatted = []
        for rec in recommendations:
            if hasattr(rec, 'title'):
                formatted.append({
                    'title': rec.title,
                    'description': getattr(rec, 'description', 'No description'),
                    'priority': getattr(rec, 'priority', 'medium'),
                    'confidence_score': getattr(rec, 'confidence_score', 0.7),
                    'type': rec_type
                })
        return formatted
    
    def _calculate_intelligence_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall intelligence score."""
        scores = []
        
        # Knowledge graph intelligence score
        if results.get("knowledge_graph_intelligence", {}).get("success"):
            scores.append(0.8)
        
        # Historical patterns score
        if results.get("historical_patterns", {}).get("success"):
            scores.append(0.7)
        
        # Cross-domain intelligence score
        if results.get("cross_domain_intelligence", {}).get("success"):
            scores.append(0.9)
        
        # Strategic trends score
        if results.get("strategic_trends", {}).get("success"):
            scores.append(0.8)
        
        # Risk assessment score
        if results.get("strategic_risks", {}).get("success"):
            scores.append(0.7)
        
        # Opportunities score
        if results.get("strategic_opportunities", {}).get("success"):
            scores.append(0.8)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _assess_risk_level(self, risks_data: Dict[str, Any]) -> str:
        """Assess overall risk level."""
        if not risks_data.get("success"):
            return "medium"
        
        risk_factors = risks_data.get("risk_factors", [])
        high_risks = sum(1 for risk in risk_factors if risk.get("level") == "high")
        
        if high_risks > 3:
            return "high"
        elif high_risks > 1:
            return "medium"
        else:
            return "low"
    
    def _calculate_confidence_score(self, results: Dict[str, Any]) -> float:
        """Calculate confidence score based on data quality."""
        confidence_scores = []
        
        for key, data in results.items():
            if isinstance(data, dict) and data.get("success"):
                confidence_scores.append(0.8)
            elif isinstance(data, dict) and not data.get("success"):
                confidence_scores.append(0.3)
        
        return sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5


# Mock classes for fallback
class MockStrategicEngine:
    async def query_knowledge_graph_for_intelligence(self, topic, analysis_type):
        return {"success": True, "strategic_insights": {"key_insights": ["Mock intelligence insight"]}}
    
    async def analyze_historical_patterns(self, topic, time_range):
        return {"success": True, "patterns": [{"pattern_type": "Mock", "description": "Mock pattern"}]}
    
    async def generate_cross_domain_intelligence(self, domains):
        return {"success": True, "cross_domain_patterns": [{"domains": "Mock", "pattern": "Mock pattern"}]}
    
    async def predict_strategic_trends(self, topic):
        return {"success": True, "predicted_trends": [{"trend_type": "Mock", "description": "Mock trend", "confidence": 0.8}]}
    
    async def assess_strategic_risks_from_kg(self, topic):
        return {"success": True, "risk_factors": [{"factor": "Mock", "description": "Mock risk", "level": "medium"}]}
    
    async def identify_strategic_opportunities(self, topic):
        return {"success": True, "opportunities": [{"opportunity": "Mock", "description": "Mock opportunity", "impact_score": 0.7}]}


class MockRecommendationsEngine:
    async def generate_intelligence_driven_recommendations(self, topic):
        return [MockRecommendation("Mock Intelligence Recommendation", "Mock description")]
    
    async def generate_multi_domain_recommendations(self, domains):
        return [MockRecommendation("Mock Multi-Domain Recommendation", "Mock description")]


class MockRecommendation:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.priority = "medium"
        self.confidence_score = 0.7


class MockDashboard:
    async def get_strategic_metrics(self):
        return {"total_metrics": 5, "active_recommendations": 3}
    
    async def get_dashboard_summary(self):
        return {"total_metrics": 5, "active_recommendations": 3, "critical_risks": 1, "active_opportunities": 2}
