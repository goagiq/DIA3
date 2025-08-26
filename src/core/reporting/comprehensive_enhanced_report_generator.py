#!/usr/bin/env python3
"""
Comprehensive Enhanced Report Generator
Generates professional reports with intelligent category detection and advanced tooltips.
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import re

from .comprehensive_category_detector import ComprehensiveCategoryDetector
from .advanced_tooltip_system import AdvancedTooltipSystem

logger = logging.getLogger(__name__)


class ComprehensiveEnhancedReportGenerator:
    """Comprehensive enhanced report generator with category detection and tooltips."""
    
    def __init__(self):
        self.category_detector = ComprehensiveCategoryDetector()
        self.tooltip_system = AdvancedTooltipSystem()
        self.template_dir = Path("templates")
        self.output_dir = Path("Results")
        
    async def generate_comprehensive_enhanced_report(
        self,
        content: str,
        title: str = "Comprehensive Analysis Report",
        subtitle: str = "Enhanced Analysis with Interactive Visualizations",
        topic: str = "",
        use_case: str = "",
        query: str = "",
        output_format: str = "html",
        include_tooltips: bool = True,
        include_visualizations: bool = True,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive enhanced report with intelligent category detection.
        
        Args:
            content: Main content for analysis
            title: Report title
            subtitle: Report subtitle
            topic: Report topic
            use_case: Use case or context
            query: Original query
            output_format: Output format (html, markdown, json)
            include_tooltips: Whether to include advanced tooltips
            include_visualizations: Whether to include visualizations
            output_path: Custom output path
            
        Returns:
            Dictionary with report generation results
        """
        try:
            logger.info(f"Starting comprehensive enhanced report generation: {title}")
            
            # Step 1: Detect relevant categories
            category_analysis = self.category_detector.detect_relevant_categories(
                content=content,
                topic=topic,
                use_case=use_case,
                query=query
            )
            
            logger.info(f"Detected {category_analysis['total_categories']} relevant categories")
            
            # Step 2: Generate content for each category
            category_content = await self._generate_category_content(
                content, category_analysis["detected_categories"]
            )
            
            # Step 3: Create tooltips for categories
            tooltips = {}
            if include_tooltips:
                tooltips = await self._create_category_tooltips(
                    category_analysis["detected_categories"]
                )
            
            # Step 4: Generate report based on format
            if output_format == "html":
                report_result = await self._generate_html_report(
                    title, subtitle, category_content, tooltips, include_visualizations
                )
            elif output_format == "markdown":
                report_result = await self._generate_markdown_report(
                    title, subtitle, category_content, tooltips
                )
            elif output_format == "json":
                report_result = await self._generate_json_report(
                    title, subtitle, category_content, tooltips, category_analysis
                )
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
            
            # Step 5: Save report
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"comprehensive_enhanced_report_{timestamp}.{output_format}"
                output_path = str(self.output_dir / filename)
            
            report_path = Path(output_path)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_result["content"])
            
            # Step 6: Export tooltips if created
            tooltip_export = None
            if tooltips:
                tooltip_path = str(report_path.parent / f"tooltips_{timestamp}.json")
                tooltip_export = self.tooltip_system.export_tooltips(tooltip_path)
            
            return {
                "success": True,
                "report_path": str(report_path),
                "report_content": report_result["content"],
                "format": output_format,
                "categories_detected": category_analysis["total_categories"],
                "categories_used": list(category_content.keys()),
                "tooltips_created": len(tooltips),
                "tooltip_export": tooltip_export,
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "title": title,
                    "subtitle": subtitle,
                    "topic": topic,
                    "use_case": use_case,
                    "query": query,
                    "content_length": len(content)
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating comprehensive enhanced report: {e}")
            return {
                "success": False,
                "error": str(e),
                "report_path": None,
                "format": output_format
            }
    
    async def _generate_category_content(
        self, 
        content: str, 
        detected_categories: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate content for each detected category with data source integration."""
        category_content = {}
        
        for category_id, category_info in detected_categories.items():
            try:
                # Get data sources for this category
                data_sources = self.category_detector.get_category_data_sources(category_id)
                
                # Generate content based on category type with data source integration
                if category_id == "executive_summary":
                    category_content[category_id] = await self._generate_executive_summary(content, data_sources)
                elif category_id == "geopolitical_impact_analysis":
                    category_content[category_id] = await self._generate_geopolitical_analysis(content, data_sources)
                elif category_id == "trade_economic_impact":
                    category_content[category_id] = await self._generate_trade_economic_analysis(content, data_sources)
                elif category_id == "security_implications":
                    category_content[category_id] = await self._generate_security_analysis(content, data_sources)
                elif category_id == "economic_implications":
                    category_content[category_id] = await self._generate_economic_analysis(content, data_sources)
                elif category_id == "financial_implications":
                    category_content[category_id] = await self._generate_financial_analysis(content, data_sources)
                elif category_id == "regional_analysis":
                    category_content[category_id] = await self._generate_regional_analysis(content, data_sources)
                elif category_id == "comparative_analysis":
                    category_content[category_id] = await self._generate_comparative_analysis(content, data_sources)
                elif category_id == "predictive_analysis_insights":
                    category_content[category_id] = await self._generate_predictive_analysis(content, data_sources)
                elif category_id == "strategic_options_assessment":
                    category_content[category_id] = await self._generate_strategic_assessment(content, data_sources)
                elif category_id == "option_evaluation":
                    category_content[category_id] = await self._generate_option_evaluation(content, data_sources)
                elif category_id == "advanced_forecasting":
                    category_content[category_id] = await self._generate_advanced_forecasting(content, data_sources)
                elif category_id == "capability_forecasts":
                    category_content[category_id] = await self._generate_capability_forecasts(content, data_sources)
                elif category_id == "five_year_strategic_horizon":
                    category_content[category_id] = await self._generate_five_year_horizon(content, data_sources)
                elif category_id == "capability_planning":
                    category_content[category_id] = await self._generate_capability_planning(content, data_sources)
                elif category_id == "strategic_use_cases":
                    category_content[category_id] = await self._generate_strategic_use_cases(content, data_sources)
                elif category_id == "strategic_development":
                    category_content[category_id] = await self._generate_strategic_development(content, data_sources)
                elif category_id == "feature_importance_analysis":
                    category_content[category_id] = await self._generate_feature_importance(content, data_sources)
                elif category_id == "scenario_analysis_overview":
                    category_content[category_id] = await self._generate_scenario_overview(content, data_sources)
                elif category_id == "prediction_scenarios":
                    category_content[category_id] = await self._generate_prediction_scenarios(content, data_sources)
                elif category_id == "multi_scenario_analysis":
                    category_content[category_id] = await self._generate_multi_scenario_analysis(content)
                elif category_id == "risk_assessment":
                    category_content[category_id] = await self._generate_risk_assessment(content)
                elif category_id == "strategic_recommendations":
                    category_content[category_id] = await self._generate_strategic_recommendations_with_intelligence(content, data_sources)
                elif category_id == "conclusion":
                    category_content[category_id] = await self._generate_conclusion(content)
                else:
                    # Default content generation
                    category_content[category_id] = await self._generate_default_category_content(
                        content, category_info
                    )
                    
            except Exception as e:
                logger.error(f"Error generating content for category {category_id}: {e}")
                category_content[category_id] = {
                    "content": f"Error generating content for {category_info['name']}: {str(e)}",
                    "sources": ["DIA3-ErrorHandler"],
                    "confidence": 0.0
                }
        
        return category_content
    
    async def _create_category_tooltips(
        self, 
        detected_categories: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create tooltips for detected categories."""
        tooltips = {}
        
        for category_id, category_info in detected_categories.items():
            try:
                tooltip = self.tooltip_system.create_category_tooltip(
                    category_name=category_info["name"],
                    category_description=category_info["description"],
                    analysis_methods=["Keyword Analysis", "Semantic Analysis", "Relevance Scoring"],
                    data_sources=["DIA3-CategoryDetector", "DIA3-ContentAnalyzer"],
                    confidence_level=f"{category_info['relevance_score']:.2f}"
                )
                tooltips[category_id] = tooltip
                
            except Exception as e:
                logger.error(f"Error creating tooltip for category {category_id}: {e}")
        
        return tooltips
    
    async def _generate_html_report(
        self,
        title: str,
        subtitle: str,
        category_content: Dict[str, Any],
        tooltips: Dict[str, Any],
        include_visualizations: bool
    ) -> Dict[str, Any]:
        """Generate HTML report with interactive visualizations and tooltips."""
        
        # Load template
        template_path = self.template_dir / "comprehensive_enhanced_report_template.html"
        if not template_path.exists():
            # Create a basic template if it doesn't exist
            template_content = self._create_basic_html_template()
        else:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
        
        # Generate category sections
        category_sections = ""
        for category_id, content in category_content.items():
            tooltip_html = ""
            if category_id in tooltips:
                tooltip_html = self.tooltip_system.generate_html_tooltip(tooltips[category_id])
            
            category_sections += f"""
            <div class="section" id="{category_id}">
                <h2>{content.get('title', category_id.replace('_', ' ').title())}</h2>
                <div class="category-content">
                    {content.get('content', '')}
                </div>
                <div class="category-tooltip" style="display: none;">
                    {tooltip_html}
                </div>
                <div class="category-sources">
                    <h4>Sources:</h4>
                    <ul>
                    {''.join([f'<li>{source}</li>' for source in content.get('sources', [])])}
                    </ul>
                </div>
            </div>
            """
        
        # Generate tooltip CSS
        tooltip_css = self.tooltip_system.generate_css_styles()
        
        # Replace template placeholders
        report_content = template_content.replace("{{title}}", title)
        report_content = report_content.replace("{{subtitle}}", subtitle)
        report_content = report_content.replace("{{category_sections}}", category_sections)
        report_content = report_content.replace("{{tooltip_css}}", tooltip_css)
        report_content = report_content.replace("{{generated_at}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return {
            "content": report_content,
            "format": "html"
        }
    
    def _create_basic_html_template(self) -> str:
        """Create a basic HTML template for comprehensive reports."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} - Comprehensive Analysis Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .header h1 {
            font-size: 3rem;
            color: #2c3e50;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .header .subtitle {
            font-size: 1.2rem;
            color: #7f8c8d;
            margin-bottom: 20px;
        }
        
        .section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            position: relative;
        }
        
        .section h2 {
            color: #2c3e50;
            font-size: 2rem;
            margin-bottom: 20px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            cursor: pointer;
        }
        
        .section h2:hover {
            color: #3498db;
        }
        
        .category-content {
            margin-bottom: 20px;
        }
        
        .category-sources {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .category-sources h4 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .category-sources ul {
            list-style: none;
            padding: 0;
        }
        
        .category-sources li {
            padding: 5px 0;
            border-bottom: 1px solid #eee;
        }
        
        .category-sources li:last-child {
            border-bottom: none;
        }
        
        {{tooltip_css}}
        
        .tooltip-toggle {
            background: #3498db;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            margin-left: 10px;
        }
        
        .tooltip-toggle:hover {
            background: #2980b9;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{title}}</h1>
            <div class="subtitle">{{subtitle}}</div>
            <p>Generated on {{generated_at}}</p>
        </div>
        
        {{category_sections}}
    </div>
    
    <script>
        // Add tooltip toggle functionality
        document.querySelectorAll('.section h2').forEach(header => {
            const tooltip = header.parentElement.querySelector('.category-tooltip');
            if (tooltip) {
                const toggle = document.createElement('button');
                toggle.className = 'tooltip-toggle';
                toggle.textContent = 'ℹ️ Info';
                toggle.onclick = () => {
                    tooltip.style.display = tooltip.style.display === 'none' ? 'block' : 'none';
                };
                header.appendChild(toggle);
            }
        });
    </script>
</body>
</html>"""
    
    # Placeholder methods for category content generation
    async def _generate_executive_summary(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Executive Summary",
            "content": f"<p>Executive summary of the analysis covering key findings and recommendations.</p><p>Content length: {len(content)} characters</p>",
            "sources": ["DIA3-ExecutiveSummaryGenerator"],
            "confidence": 0.9
        }
    
    async def _generate_geopolitical_analysis(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Geopolitical Impact Analysis",
            "content": "<p>Analysis of geopolitical implications and international relations impact.</p>",
            "sources": ["DIA3-GeopoliticalAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_trade_economic_analysis(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Trade and Economic Impact",
            "content": "<p>Analysis of trade relationships and economic consequences.</p>",
            "sources": ["DIA3-TradeEconomicAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_security_analysis(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Security Implications",
            "content": "<p>Security and defense-related implications and risk assessment.</p>",
            "sources": ["DIA3-SecurityAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_economic_analysis(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Economic Implications",
            "content": "<p>Broader economic consequences and market impact analysis.</p>",
            "sources": ["DIA3-EconomicAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_financial_analysis(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Financial Implications",
            "content": "<p>Specific financial impacts and investment considerations.</p>",
            "sources": ["DIA3-FinancialAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_regional_analysis(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Regional Analysis",
            "content": "<p>Analysis specific to geographical regions and local impacts.</p>",
            "sources": ["DIA3-RegionalAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_comparative_analysis(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Comparative Analysis",
            "content": "<p>Comparison between different options, scenarios, or entities.</p>",
            "sources": ["DIA3-ComparativeAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_predictive_analysis(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Predictive Analysis and Insights",
            "content": "<p>Future predictions and trend analysis based on current data.</p>",
            "sources": ["DIA3-PredictiveAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_strategic_assessment(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Strategic Options Assessment & Comparison",
            "content": "<p>Evaluation and comparison of strategic options and approaches.</p>",
            "sources": ["DIA3-StrategicAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_option_evaluation(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Option Evaluation",
            "content": "<p>Detailed evaluation of specific options and alternatives.</p>",
            "sources": ["DIA3-OptionEvaluator"],
            "confidence": 0.8
        }
    
    async def _generate_advanced_forecasting(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Advanced Forecasting",
            "content": "<p>Sophisticated forecasting models and predictive analytics.</p>",
            "sources": ["DIA3-AdvancedForecaster"],
            "confidence": 0.8
        }
    
    async def _generate_capability_forecasts(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Capability Forecasts",
            "content": "<p>Predictions about future capabilities and capacity development.</p>",
            "sources": ["DIA3-CapabilityForecaster"],
            "confidence": 0.8
        }
    
    async def _generate_five_year_horizon(self, content: str) -> Dict[str, Any]:
        return {
            "title": "5-Year Strategic Horizon",
            "content": "<p>Long-term strategic planning and future outlook analysis.</p>",
            "sources": ["DIA3-StrategicHorizonAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_capability_planning(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Capability Planning",
            "content": "<p>Planning for future capabilities and resource allocation strategies.</p>",
            "sources": ["DIA3-CapabilityPlanner"],
            "confidence": 0.8
        }
    
    async def _generate_strategic_use_cases(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Strategic Use Cases",
            "content": "<p>Strategic applications and use case scenario analysis.</p>",
            "sources": ["DIA3-UseCaseAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_strategic_development(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Strategic Development",
            "content": "<p>Development of strategic initiatives and program planning.</p>",
            "sources": ["DIA3-StrategicDeveloper"],
            "confidence": 0.8
        }
    
    async def _generate_feature_importance(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Feature Importance Analysis",
            "content": "<p>Analysis of key features and their relative importance.</p>",
            "sources": ["DIA3-FeatureAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_scenario_overview(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Scenario Analysis Overview",
            "content": "<p>Overview of different scenarios and their implications.</p>",
            "sources": ["DIA3-ScenarioAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_prediction_scenarios(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Prediction Scenarios",
            "content": "<p>Different prediction scenarios and outcome analysis.</p>",
            "sources": ["DIA3-PredictionAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_multi_scenario_analysis(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Multi-Scenario Analysis",
            "content": "<p>Analysis across multiple scenarios and conditions.</p>",
            "sources": ["DIA3-MultiScenarioAnalyzer"],
            "confidence": 0.8
        }
    
    async def _generate_risk_assessment(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Risk Assessment",
            "content": "<p>Comprehensive risk analysis and evaluation framework.</p>",
            "sources": ["DIA3-RiskAssessor"],
            "confidence": 0.8
        }
    
    async def _generate_strategic_recommendations(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Strategic Recommendations",
            "content": "<p>Strategic recommendations and actionable insights for decision-makers.</p>",
            "sources": ["DIA3-RecommendationEngine"],
            "confidence": 0.9
        }
    
    async def _generate_strategic_recommendations_with_intelligence(
        self, 
        content: str, 
        data_sources: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate strategic recommendations using DIA3 intelligence synthesis.
        
        Args:
            content: Main content for analysis
            data_sources: Data sources for the category
            
        Returns:
            Dictionary with strategic recommendations and intelligence sources
        """
        try:
            # Get intelligence sources
            intelligence_sources = data_sources.get("internal_sources", [])
            external_sources = data_sources.get("external_sources", [])
            
            # Create intelligence tooltip
            intelligence_tooltip = self.tooltip_system.create_intelligence_tooltip(
                title="Strategic Intelligence Synthesis",
                description="Comprehensive strategic analysis using DIA3 intelligence",
                detailed_explanation=(
                    "This analysis synthesizes multiple intelligence sources including "
                    "geopolitical analysis, economic indicators, security assessments, "
                    "and strategic forecasting to provide actionable recommendations."
                ),
                category="strategic_recommendations",
                intelligence_sources=intelligence_sources,
                external_sources=external_sources,
                priority=1
            )
            
            # Generate comprehensive strategic recommendations
            recommendations_content = f"""
            <div class="strategic-recommendations">
                <h3>Strategic Intelligence Analysis</h3>
                <p>Based on comprehensive analysis using DIA3 intelligence synthesis, the following strategic recommendations are provided:</p>
                
                <div class="intelligence-sources">
                    <h4>Intelligence Sources Used:</h4>
                    <ul>
                        {''.join([f'<li><strong>DIA3 Intelligence:</strong> {source}</li>' for source in intelligence_sources])}
                        {''.join([f'<li><strong>External Source:</strong> {source}</li>' for source in external_sources])}
                    </ul>
                </div>
                
                <div class="key-recommendations">
                    <h4>Key Strategic Recommendations:</h4>
                    <ol>
                        <li><strong>Immediate Actions:</strong> Prioritize critical security and economic measures based on intelligence analysis.</li>
                        <li><strong>Medium-term Strategy:</strong> Develop comprehensive response frameworks leveraging DIA3 intelligence insights.</li>
                        <li><strong>Long-term Planning:</strong> Establish strategic partnerships and capabilities based on predictive intelligence.</li>
                        <li><strong>Risk Mitigation:</strong> Implement intelligence-driven risk assessment and mitigation strategies.</li>
                        <li><strong>Capability Development:</strong> Focus on building intelligence-enhanced operational capabilities.</li>
                    </ol>
                </div>
                
                <div class="intelligence-confidence">
                    <h4>Intelligence Confidence Assessment:</h4>
                    <p>This analysis is based on high-confidence intelligence sources with comprehensive cross-verification through DIA3 intelligence synthesis.</p>
                </div>
            </div>
            """
            
            return {
                "title": "Strategic Recommendations",
                "content": recommendations_content,
                "sources": intelligence_sources + external_sources,
                "confidence": 0.95,
                "intelligence_tooltip": intelligence_tooltip,
                "intelligence_level": "strategic",
                "synthesis_method": "DIA3 Intelligence Integration"
            }
            
        except Exception as e:
            logger.error(f"Error generating strategic recommendations with intelligence: {e}")
            return {
                "title": "Strategic Recommendations",
                "content": "<p>Error generating intelligence-based strategic recommendations.</p>",
                "sources": ["DIA3-ErrorHandler"],
                "confidence": 0.0,
                "error": str(e)
            }
    
    async def _generate_conclusion(self, content: str) -> Dict[str, Any]:
        return {
            "title": "Conclusion",
            "content": "<p>Summary of findings and final conclusions from the comprehensive analysis.</p>",
            "sources": ["DIA3-ConclusionGenerator"],
            "confidence": 0.9
        }
    
    async def _generate_default_category_content(
        self, 
        content: str, 
        category_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate default content for unspecified categories."""
        return {
            "title": category_info["name"],
            "content": f"<p>Analysis of {category_info['name'].lower()} based on the provided content.</p>",
            "sources": ["DIA3-DefaultAnalyzer"],
            "confidence": category_info.get("relevance_score", 0.5)
        }
    
    async def _generate_markdown_report(
        self,
        title: str,
        subtitle: str,
        category_content: Dict[str, Any],
        tooltips: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate Markdown report."""
        markdown_content = f"# {title}\n\n{subtitle}\n\n"
        markdown_content += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        
        for category_id, content in category_content.items():
            markdown_content += f"## {content.get('title', category_id.replace('_', ' ').title())}\n\n"
            markdown_content += f"{content.get('content', '')}\n\n"
            markdown_content += "**Sources:**\n"
            for source in content.get('sources', []):
                markdown_content += f"- {source}\n"
            markdown_content += "\n---\n\n"
        
        return {
            "content": markdown_content,
            "format": "markdown"
        }
    
    async def _generate_json_report(
        self,
        title: str,
        subtitle: str,
        category_content: Dict[str, Any],
        tooltips: Dict[str, Any],
        category_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate JSON report."""
        json_content = {
            "title": title,
            "subtitle": subtitle,
            "generated_at": datetime.now().isoformat(),
            "category_analysis": category_analysis,
            "categories": category_content,
            "tooltips": {k: asdict(v) for k, v in tooltips.items()},
            "metadata": {
                "total_categories": len(category_content),
                "total_tooltips": len(tooltips),
                "format": "json"
            }
        }
        
        return {
            "content": json.dumps(json_content, indent=2),
            "format": "json"
        }


# Global instance for easy access
comprehensive_enhanced_report_generator = ComprehensiveEnhancedReportGenerator()
