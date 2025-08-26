# Phase 4 Strategic Intelligence Integration Guide

## Overview

This guide shows how to integrate the Enhanced StrategicIntelligenceEngine from Phase 4 with your existing report generation system to create intelligence-driven strategic reports with advanced analytics and recommendations.

## 🎯 Integration Benefits

- **Intelligence-Driven Reports**: Base reports on accumulated knowledge graph intelligence
- **Strategic Recommendations**: Include AI-generated strategic recommendations
- **Risk Assessment**: Integrate risk analysis into reports
- **Predictive Analytics**: Add forecasting and trend analysis
- **Multi-Domain Analysis**: Cross-domain intelligence integration
- **Interactive Dashboards**: Strategic analytics dashboard integration

## 🔧 Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Report Generation System                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Modular Report  │  │ Enhanced HTML   │  │ Knowledge    │ │
│  │ Generator       │  │ Report Generator│  │ Graph Agent  │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────────┤
│              Phase 4 Strategic Intelligence                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Strategic       │  │ Enhanced        │  │ Strategic    │ │
│  │ Intelligence    │  │ Strategic       │  │ Analytics    │ │
│  │ Engine          │  │ Recommendations │  │ Dashboard    │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Integration Steps

### Step 1: Create Strategic Intelligence Module

Create a new module that integrates the StrategicIntelligenceEngine:

```python
# src/core/modules/strategic_intelligence_module.py

import asyncio
from typing import Dict, Any, List
from datetime import datetime
from .base_module import BaseModule, ModuleConfig

from src.core.strategic_intelligence_engine import StrategicIntelligenceEngine
from src.core.enhanced_strategic_recommendations import EnhancedStrategicRecommendations
from src.core.strategic_analytics_dashboard import StrategicAnalyticsDashboard


class StrategicIntelligenceModule(BaseModule):
    """Strategic Intelligence Module integrating Phase 4 capabilities."""
    
    module_id = "strategic_intelligence"
    title = "Strategic Intelligence Analysis"
    description = "Advanced strategic intelligence with knowledge graph integration"
    version = "1.0.0"
    
    def __init__(self):
        super().__init__()
        self.strategic_engine = StrategicIntelligenceEngine()
        self.recommendations_engine = EnhancedStrategicRecommendations()
        self.dashboard = StrategicAnalyticsDashboard()
    
    async def generate_content(self, data: Dict[str, Any], config: ModuleConfig) -> Dict[str, Any]:
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
                    "confidence_score": intelligence_results.get("confidence_score", 0.7)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating strategic intelligence: {e}")
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
        
        # Risk-adjusted recommendations
        if intel_recs:
            risk_adjusted = await self.recommendations_engine.adjust_recommendations_by_risk(
                intel_recs, {"risk_level": "medium"}
            )
            recommendations.extend(self._format_recommendations(risk_adjusted, "risk_adjusted"))
        
        # Confidence-weighted recommendations
        if intel_recs:
            confidence_weighted = await self.recommendations_engine.weight_recommendations_by_confidence(intel_recs)
            recommendations.extend(self._format_recommendations(confidence_weighted, "confidence_weighted"))
        
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
```

### Step 2: Update Modular Report Generator

Update the modular report generator to include the new strategic intelligence module:

```python
# Update src/core/modular_report_generator.py

# Add import for the new module
from .modules.strategic_intelligence_module import StrategicIntelligenceModule

class ModularReportGenerator:
    def _register_available_modules(self):
        """Register all available modules."""
        # ... existing modules ...
        
        # Add the new strategic intelligence module
        self.register_module(StrategicIntelligenceModule())
```

### Step 3: Create Integration Script

Create a script to demonstrate the integration:

```python
# integrate_phase4_strategic_intelligence.py

#!/usr/bin/env python3
"""
Phase 4 Strategic Intelligence Integration Script

Demonstrates how to integrate the Enhanced StrategicIntelligenceEngine
with the existing report generation system.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.modular_report_generator import ModularReportGenerator
from src.core.adaptive_data_adapter import adaptive_data_adapter


async def generate_strategic_intelligence_report():
    """Generate a report with integrated strategic intelligence."""
    
    # Topic for strategic analysis
    topic = ("Pakistan Submarine Acquisition: Strategic Intelligence Analysis "
             "of Geopolitical Impact, Economic Implications, and Regional "
             "Security Dynamics")
    
    print("🚀 Generating Strategic Intelligence Report...")
    print(f"📋 Topic: {topic}")
    
    try:
        # Initialize the modular report generator
        generator = ModularReportGenerator()
        
        # Generate adaptive data
        print("📊 Generating adaptive data...")
        universal_data = adaptive_data_adapter.generate_universal_data(topic, {})
        
        # Get available modules including the new strategic intelligence module
        modules_info = generator.get_available_modules()
        all_module_ids = list(modules_info.keys())
        
        print(f"✅ Found {len(all_module_ids)} modules including strategic intelligence")
        
        # Generate the enhanced HTML report with strategic intelligence
        print("📝 Generating strategic intelligence report...")
        result = await generator.generate_modular_report(
            query=topic,
            enabled_modules=all_module_ids,
            config={
                "enhanced_template": True,
                "advanced_tooltips": True,
                "multiple_sources": True,
                "interactive_charts": True,
                "strategic_intelligence": True  # Enable strategic intelligence
            },
            output_format="html",
            title=f"Strategic Intelligence Analysis: {topic}"
        )
        
        if result.get("success"):
            print("✅ Strategic intelligence report generated successfully!")
            print(f"📁 File: {result.get('file_path')}")
            print(f"📊 Modules used: {len(result.get('modules_used', []))}")
            print(f"📏 File size: {result.get('file_size', 0)} bytes")
            
            # Open the report in browser
            import webbrowser
            file_path = Path(result.get('file_path'))
            if file_path.exists():
                webbrowser.open(f"file://{file_path.absolute()}")
                print("🌐 Opened report in browser")
            
            return result
        else:
            print(f"❌ Error generating report: {result.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_strategic_intelligence_components():
    """Test individual strategic intelligence components."""
    
    print("\n🔧 Testing Strategic Intelligence Components...")
    
    try:
        from src.core.strategic_intelligence_engine import StrategicIntelligenceEngine
        from src.core.enhanced_strategic_recommendations import EnhancedStrategicRecommendations
        from src.core.strategic_analytics_dashboard import StrategicAnalyticsDashboard
        
        # Test Strategic Intelligence Engine
        print("📊 Testing Strategic Intelligence Engine...")
        strategic_engine = StrategicIntelligenceEngine()
        
        # Test knowledge graph query
        kg_result = await strategic_engine.query_knowledge_graph_for_intelligence(
            "Pakistan submarine acquisition", "strategic"
        )
        print(f"✅ Knowledge Graph Query: {'Success' if kg_result.get('success') else 'Failed'}")
        
        # Test historical patterns
        patterns_result = await strategic_engine.analyze_historical_patterns(
            "Pakistan submarine acquisition", "5_years"
        )
        print(f"✅ Historical Patterns: {'Success' if patterns_result.get('success') else 'Failed'}")
        
        # Test Enhanced Strategic Recommendations
        print("📋 Testing Enhanced Strategic Recommendations...")
        recommendations_engine = EnhancedStrategicRecommendations()
        
        recs_result = await recommendations_engine.generate_intelligence_driven_recommendations(
            "Pakistan submarine acquisition"
        )
        print(f"✅ Intelligence-Driven Recommendations: {len(recs_result)} generated")
        
        # Test Strategic Analytics Dashboard
        print("📈 Testing Strategic Analytics Dashboard...")
        dashboard = StrategicAnalyticsDashboard()
        
        metrics_result = await dashboard.get_strategic_metrics()
        print(f"✅ Strategic Metrics: {'Success' if metrics_result else 'Failed'}")
        
        summary_result = await dashboard.get_dashboard_summary()
        print(f"✅ Dashboard Summary: {'Success' if summary_result else 'Failed'}")
        
        print("✅ All strategic intelligence components tested successfully!")
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Test components first
    asyncio.run(test_strategic_intelligence_components())
    
    # Generate the integrated report
    result = asyncio.run(generate_strategic_intelligence_report())
    
    if result:
        print("\n🎉 Strategic Intelligence Integration completed successfully!")
        print("📊 The integrated report includes:")
        print("   • Enhanced Strategic Intelligence Engine")
        print("   • Intelligence-driven recommendations")
        print("   • Strategic analytics dashboard")
        print("   • Risk assessment and opportunity identification")
        print("   • Cross-domain intelligence analysis")
        print("   • Historical pattern analysis")
        print("   • Predictive strategic trends")
        print("   • Interactive visualizations")
        print("   • Professional styling and layout")
    else:
        print("\n❌ Strategic Intelligence Integration failed!")
        sys.exit(1)
```

### Step 4: Add CSS Styling

Add CSS styling for the strategic intelligence components:

```css
/* Add to your existing CSS or create a new strategic-intelligence.css file */

.strategic-intelligence-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 15px;
    margin: 20px 0;
    color: white;
}

.intelligence-overview {
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}

.intelligence-score, .risk-assessment, .confidence-score {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 10px 0;
    padding: 10px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 5px;
}

.score-value, .confidence-value {
    font-weight: bold;
    font-size: 1.2em;
}

.risk-value {
    padding: 5px 10px;
    border-radius: 15px;
    font-weight: bold;
}

.risk-value.low { background: #27ae60; }
.risk-value.medium { background: #f39c12; }
.risk-value.high { background: #e74c3c; }

.kg-insights, .historical-patterns, .cross-domain-intelligence,
.strategic-trends, .risk-assessment, .strategic-opportunities {
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
}

.recommendations-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.recommendation-card {
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    border-left: 4px solid #3498db;
}

.dashboard-summary {
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
}

.dashboard-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
}

.stat {
    text-align: center;
    padding: 15px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
}

.stat-number {
    display: block;
    font-size: 2em;
    font-weight: bold;
    color: #3498db;
}

.stat-label {
    font-size: 0.9em;
    opacity: 0.8;
}

.performance-scores {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
}

.score {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 5px;
}

.score-value {
    font-weight: bold;
    color: #3498db;
}
```

### Step 5: API Integration

Add API endpoints for strategic intelligence:

```python
# Add to your existing API routes or create new strategic intelligence routes

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

router = APIRouter(prefix="/strategic-intelligence", tags=["Strategic Intelligence"])

class StrategicAnalysisRequest(BaseModel):
    topic: str
    analysis_depth: str = "comprehensive"
    include_recommendations: bool = True
    include_dashboard: bool = True

@router.post("/analyze")
async def analyze_strategic_intelligence(request: StrategicAnalysisRequest):
    """Generate comprehensive strategic intelligence analysis."""
    try:
        from src.core.strategic_intelligence_engine import StrategicIntelligenceEngine
        from src.core.enhanced_strategic_recommendations import EnhancedStrategicRecommendations
        from src.core.strategic_analytics_dashboard import StrategicAnalyticsDashboard
        
        # Initialize components
        strategic_engine = StrategicIntelligenceEngine()
        recommendations_engine = EnhancedStrategicRecommendations()
        dashboard = StrategicAnalyticsDashboard()
        
        # Generate comprehensive analysis
        results = {}
        
        # Strategic intelligence
        kg_intelligence = await strategic_engine.query_knowledge_graph_for_intelligence(
            request.topic, "strategic"
        )
        results["knowledge_graph_intelligence"] = kg_intelligence
        
        historical_patterns = await strategic_engine.analyze_historical_patterns(
            request.topic, "5_years"
        )
        results["historical_patterns"] = historical_patterns
        
        cross_domain = await strategic_engine.generate_cross_domain_intelligence([
            "geopolitical", "economic", "military", "technological"
        ])
        results["cross_domain_intelligence"] = cross_domain
        
        trends = await strategic_engine.predict_strategic_trends(request.topic)
        results["strategic_trends"] = trends
        
        risks = await strategic_engine.assess_strategic_risks_from_kg(request.topic)
        results["strategic_risks"] = risks
        
        opportunities = await strategic_engine.identify_strategic_opportunities(request.topic)
        results["strategic_opportunities"] = opportunities
        
        # Recommendations
        if request.include_recommendations:
            intel_recs = await recommendations_engine.generate_intelligence_driven_recommendations(request.topic)
            multi_domain_recs = await recommendations_engine.generate_multi_domain_recommendations([
                "geopolitical", "economic", "military", "technological"
            ])
            results["recommendations"] = {
                "intelligence_driven": intel_recs,
                "multi_domain": multi_domain_recs
            }
        
        # Dashboard
        if request.include_dashboard:
            metrics = await dashboard.get_strategic_metrics()
            summary = await dashboard.get_dashboard_summary()
            results["dashboard"] = {
                "metrics": metrics,
                "summary": summary
            }
        
        return {
            "success": True,
            "topic": request.topic,
            "analysis_depth": request.analysis_depth,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Strategic intelligence analysis failed: {str(e)}")

@router.post("/generate-report")
async def generate_strategic_intelligence_report(request: StrategicAnalysisRequest):
    """Generate a complete strategic intelligence report."""
    try:
        from src.core.modular_report_generator import ModularReportGenerator
        
        # Initialize generator
        generator = ModularReportGenerator()
        
        # Generate report with strategic intelligence
        result = await generator.generate_modular_report(
            query=request.topic,
            enabled_modules=["strategic_intelligence"],  # Focus on strategic intelligence
            config={
                "enhanced_template": True,
                "advanced_tooltips": True,
                "strategic_intelligence": True
            },
            output_format="html",
            title=f"Strategic Intelligence Report: {request.topic}"
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")
```

## 🎯 Usage Examples

### Example 1: Generate Strategic Intelligence Report

```python
import asyncio
from src.core.modular_report_generator import ModularReportGenerator

async def generate_strategic_report():
    generator = ModularReportGenerator()
    
    result = await generator.generate_modular_report(
        query="Pakistan submarine acquisition strategic analysis",
        enabled_modules=["strategic_intelligence"],
        config={"strategic_intelligence": True},
        output_format="html"
    )
    
    print(f"Report generated: {result.get('file_path')}")

# Run the generation
asyncio.run(generate_strategic_report())
```

### Example 2: Use Strategic Intelligence API

```python
import requests

# Generate strategic intelligence analysis
response = requests.post("http://localhost:8000/strategic-intelligence/analyze", json={
    "topic": "Pakistan submarine acquisition",
    "analysis_depth": "comprehensive",
    "include_recommendations": True,
    "include_dashboard": True
})

if response.status_code == 200:
    analysis = response.json()
    print(f"Strategic Intelligence Score: {analysis['results'].get('overall_score', 0)}")
    print(f"Risk Level: {analysis['results'].get('risk_level', 'unknown')}")
```

### Example 3: Integrate with Existing Reports

```python
# Add strategic intelligence to existing report generation
from src.core.modular_report_generator import ModularReportGenerator

async def generate_enhanced_report():
    generator = ModularReportGenerator()
    
    # Include strategic intelligence with other modules
    result = await generator.generate_modular_report(
        query="Your analysis topic",
        enabled_modules=[
            "executive_summary",
            "strategic_intelligence",  # Add strategic intelligence
            "geopolitical_impact",
            "risk_assessment",
            "strategic_recommendations"
        ],
        config={
            "enhanced_template": True,
            "strategic_intelligence": True
        }
    )
    
    return result
```

## 🔍 Key Features

### 1. **Intelligence-Driven Analysis**
- Knowledge graph queries for strategic insights
- Historical pattern analysis
- Cross-domain intelligence generation
- Predictive trend analysis

### 2. **Strategic Recommendations**
- Intelligence-driven recommendations
- Multi-domain recommendations
- Risk-adjusted recommendations
- Confidence-weighted recommendations

### 3. **Strategic Analytics Dashboard**
- Key strategic metrics
- Recommendation tracking
- Risk monitoring
- Opportunity tracking

### 4. **Interactive Visualizations**
- Strategic intelligence charts
- Risk assessment visualizations
- Trend analysis graphs
- Dashboard widgets

## 🚀 Benefits

1. **Enhanced Intelligence**: Leverage accumulated knowledge graph data
2. **Strategic Insights**: AI-generated strategic recommendations
3. **Risk Awareness**: Comprehensive risk assessment and monitoring
4. **Predictive Capabilities**: Trend analysis and forecasting
5. **Cross-Domain Analysis**: Multi-domain intelligence integration
6. **Interactive Reporting**: Rich visualizations and dashboards

## 📊 Output

The integrated system produces:

- **Comprehensive HTML Reports** with strategic intelligence sections
- **Interactive Dashboards** showing key metrics and trends
- **Strategic Recommendations** with confidence scores and priorities
- **Risk Assessments** with mitigation strategies
- **Opportunity Analysis** with impact scores
- **Trend Predictions** with confidence intervals

This integration transforms your existing report generation system into a comprehensive strategic intelligence platform that provides actionable insights and recommendations based on accumulated knowledge and advanced analytics.

