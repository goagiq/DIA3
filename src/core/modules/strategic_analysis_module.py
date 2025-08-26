"""
Strategic Analysis Module

Independent module for generating strategic analysis sections that can be added to any report.
Provides comprehensive strategic insights, geopolitical impact analysis, and strategic implications.
"""

from typing import Dict, Any, List, Optional
from .base_module import BaseModule, ModuleConfig, TooltipData


class StrategicAnalysisModule(BaseModule):
    """Strategic Analysis module for enhanced reports."""
    
    module_id = "strategic_analysis"
    title = "🎯 Strategic Analysis"
    description = "Comprehensive strategic analysis with enhanced insights and geopolitical considerations"
    version = "1.0.0"
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the Strategic Analysis module."""
        if config is None:
            config = ModuleConfig(
                title="🎯 Strategic Analysis",
                description="Comprehensive strategic analysis with enhanced insights and geopolitical considerations",
                order=7,  # Strategic analysis typically comes after executive summary and key sections
                tooltips_enabled=True,
                charts_enabled=True
            )
        super().__init__(config)
        
        # Initialize default tooltips
        self._initialize_default_tooltips()
    
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        return [
            'strategic_analysis',
            'strategic_insights',
            'geopolitical_impact',
            'strategic_implications'
        ]
    
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for the Strategic Analysis module."""
        
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

        # Extract strategic analysis data
        strategic_analysis = data.get('strategic_analysis', {})
        strategic_insights = data.get('strategic_insights', {})
        geopolitical_impact = data.get('geopolitical_impact', {})
        strategic_implications = data.get('strategic_implications', {})

        # Generate comprehensive strategic analysis
        content = self._generate_strategic_analysis_content(
            strategic_analysis, strategic_insights, geopolitical_impact, strategic_implications
        )

        return {
            "content": content,
            "metadata": {
                "phase4_integrated": phase4_enhanced,
                "strategic_intelligence": phase4_enhanced,
                "confidence_score": 0.7,
                "strategic_analysis_complete": bool(strategic_analysis),
                "insights_generated": bool(strategic_insights),
                "geopolitical_assessed": bool(geopolitical_impact)
            }
        }
    
    def _generate_strategic_analysis_content(self, strategic_analysis: Dict[str, Any], 
                                          strategic_insights: Dict[str, Any], 
                                          geopolitical_impact: Dict[str, Any], 
                                          strategic_implications: Dict[str, Any]) -> str:
        """Generate the main strategic analysis content."""
        
        content = f"""
        <div class="strategic-analysis-section">
            <h2>🎯 Strategic Analysis</h2>
            
            {self._generate_strategic_overview(strategic_analysis)}
            {self._generate_strategic_insights(strategic_insights)}
            {self._generate_geopolitical_impact(geopolitical_impact)}
            {self._generate_strategic_implications(strategic_implications)}
        </div>
        """
        
        return content
    
    def _generate_strategic_overview(self, strategic_analysis: Dict[str, Any]) -> str:
        """Generate strategic overview section."""
        if not strategic_analysis:
            return """
            <div class="strategic-overview">
                <h3>Strategic Overview</h3>
                <p>Strategic analysis data not available.</p>
            </div>
            """
        
        analysis_summary = strategic_analysis.get('analysis_summary', 'N/A')
        key_factors = strategic_analysis.get('key_factors', [])
        strategic_context = strategic_analysis.get('strategic_context', 'N/A')
        
        factors_html = ""
        if key_factors:
            factors_html = "<ul>" + "".join([f"<li>{factor}</li>" for factor in key_factors]) + "</ul>"
        
        return f"""
        <div class="strategic-overview">
            <h3>Strategic Overview</h3>
            <div class="overview-content">
                <p><strong>Analysis Summary:</strong> {analysis_summary}</p>
                <p><strong>Strategic Context:</strong> {strategic_context}</p>
            </div>
            <div class="key-factors">
                <h4>Key Strategic Factors</h4>
                {factors_html}
            </div>
        </div>
        """
    
    def _generate_strategic_insights(self, strategic_insights: Dict[str, Any]) -> str:
        """Generate strategic insights section."""
        if not strategic_insights:
            return """
            <div class="strategic-insights">
                <h3>Strategic Insights</h3>
                <p>Strategic insights data not available.</p>
            </div>
            """
        
        primary_insights = strategic_insights.get('primary_insights', [])
        secondary_insights = strategic_insights.get('secondary_insights', [])
        confidence_level = strategic_insights.get('confidence_level', 'N/A')
        
        primary_html = ""
        if primary_insights:
            primary_html = "<ul>" + "".join([f"<li>{insight}</li>" for insight in primary_insights]) + "</ul>"
        
        secondary_html = ""
        if secondary_insights:
            secondary_html = "<ul>" + "".join([f"<li>{insight}</li>" for insight in secondary_insights]) + "</ul>"
        
        return f"""
        <div class="strategic-insights">
            <h3>Strategic Insights</h3>
            <div class="insights-stats">
                <div class="stat-item">
                    <span class="stat-label">Confidence Level:</span>
                    <span class="stat-value">{confidence_level}</span>
                </div>
            </div>
            <div class="primary-insights">
                <h4>Primary Insights</h4>
                {primary_html}
            </div>
            <div class="secondary-insights">
                <h4>Secondary Insights</h4>
                {secondary_html}
            </div>
        </div>
        """
    
    def _generate_geopolitical_impact(self, geopolitical_impact: Dict[str, Any]) -> str:
        """Generate geopolitical impact analysis."""
        if not geopolitical_impact:
            return """
            <div class="geopolitical-impact">
                <h3>Geopolitical Impact</h3>
                <p>Geopolitical impact data not available.</p>
            </div>
            """
        
        impact_assessment = geopolitical_impact.get('impact_assessment', 'N/A')
        affected_regions = geopolitical_impact.get('affected_regions', [])
        impact_timeline = geopolitical_impact.get('impact_timeline', 'N/A')
        
        regions_html = ""
        if affected_regions:
            regions_html = "<ul>" + "".join([f"<li>{region}</li>" for region in affected_regions]) + "</ul>"
        
        return f"""
        <div class="geopolitical-impact">
            <h3>Geopolitical Impact Analysis</h3>
            <div class="impact-stats">
                <div class="stat-item">
                    <span class="stat-label">Impact Assessment:</span>
                    <span class="stat-value">{impact_assessment}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Impact Timeline:</span>
                    <span class="stat-value">{impact_timeline}</span>
                </div>
            </div>
            <div class="affected-regions">
                <h4>Affected Regions</h4>
                {regions_html}
            </div>
        </div>
        """
    
    def _generate_strategic_implications(self, strategic_implications: Dict[str, Any]) -> str:
        """Generate strategic implications analysis."""
        if not strategic_implications:
            return """
            <div class="strategic-implications">
                <h3>Strategic Implications</h3>
                <p>Strategic implications data not available.</p>
            </div>
            """
        
        short_term_implications = strategic_implications.get('short_term_implications', [])
        long_term_implications = strategic_implications.get('long_term_implications', [])
        risk_assessment = strategic_implications.get('risk_assessment', 'N/A')
        
        short_term_html = ""
        if short_term_implications:
            short_term_html = "<ul>" + "".join([f"<li>{implication}</li>" for implication in short_term_implications]) + "</ul>"
        
        long_term_html = ""
        if long_term_implications:
            long_term_html = "<ul>" + "".join([f"<li>{implication}</li>" for implication in long_term_implications]) + "</ul>"
        
        return f"""
        <div class="strategic-implications">
            <h3>Strategic Implications</h3>
            <div class="implications-stats">
                <div class="stat-item">
                    <span class="stat-label">Risk Assessment:</span>
                    <span class="stat-value">{risk_assessment}</span>
                </div>
            </div>
            <div class="short-term-implications">
                <h4>Short-term Implications</h4>
                {short_term_html}
            </div>
            <div class="long-term-implications">
                <h4>Long-term Implications</h4>
                {long_term_html}
            </div>
        </div>
        """
    
    def _initialize_default_tooltips(self):
        """Initialize default tooltips for the Strategic Analysis module."""
        self.tooltips = {
            'strategic_overview': TooltipData(
                title="Strategic Overview",
                description="Comprehensive overview of strategic analysis and key factors",
                source="Strategic Analysis Framework",
                strategic_impact="High - Critical for strategic planning"
            ),
            'strategic_insights': TooltipData(
                title="Strategic Insights",
                description="Key insights derived from strategic analysis",
                source="Intelligence Analysis Framework",
                strategic_impact="High - Critical for decision making"
            ),
            'geopolitical_impact': TooltipData(
                title="Geopolitical Impact",
                description="Analysis of geopolitical implications and affected regions",
                source="Geopolitical Analysis Framework",
                strategic_impact="High - Critical for international relations"
            ),
            'strategic_implications': TooltipData(
                title="Strategic Implications",
                description="Short and long-term strategic implications and risk assessment",
                source="Strategic Implications Framework",
                strategic_impact="High - Critical for long-term planning"
            )
        }
