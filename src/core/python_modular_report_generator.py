"""
Python Modular Report Generator

Pure Python implementation of the modular report generator that replaces
JavaScript-dependent components with Python-based solutions.
Part of Phase 2.1: Core Modules Migration
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from datetime import datetime
import logging
from dataclasses import dataclass, field

from .python_report_generator import PythonReportGenerator, ReportConfig
from .css_tooltip_system import CSSTooltipSystem
from .python_chart_generator import PythonChartGenerator

logger = logging.getLogger(__name__)


@dataclass
class ModuleData:
    """Data structure for module content."""
    module_id: str
    title: str
    content: str
    data_type: str = "text"
    metadata: Dict[str, Any] = field(default_factory=dict)
    tooltip_data: Dict[str, Any] = field(default_factory=dict)
    chart_data: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CoreModuleConfig:
    """Configuration for core modules."""
    module_id: str
    title: str
    description: str
    enabled: bool = True
    priority: int = 1
    data_structures: List[str] = field(default_factory=lambda: ["string", "dict"])
    interactive_features: bool = True
    tooltips_enabled: bool = True
    charts_enabled: bool = True
    custom_styles: Dict[str, str] = field(default_factory=dict)


class PythonModularReportGenerator:
    """Python-based modular report generator for Phase 2.1 migration."""
    
    def __init__(self):
        """Initialize the Python modular report generator."""
        self.report_generator = PythonReportGenerator()
        self.tooltip_system = CSSTooltipSystem()
        self.chart_generator = PythonChartGenerator()
        
        # Core modules configuration for Phase 2.1
        self.core_modules = self._initialize_core_modules()
        
        # Output directory
        self.output_dir = Path("Results")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Python Modular Report Generator initialized for Phase 2.1")
    
    def _initialize_core_modules(self) -> Dict[str, CoreModuleConfig]:
        """Initialize core modules configuration for Phase 2.1."""
        return {
            "executive_summary": CoreModuleConfig(
                module_id="executive_summary",
                title="Executive Summary",
                description="High-level summary of key findings and recommendations",
                priority=1,
                interactive_features=False,
                tooltips_enabled=False,
                custom_styles={"background": "#ffffff", "border": "1px solid #dee2e6"}
            ),
            
            "strategic_recommendations": CoreModuleConfig(
                module_id="strategic_recommendations",
                title="Strategic Recommendations",
                description="Strategic-level recommendations and action items",
                priority=2,
                interactive_features=True,
                tooltips_enabled=True,
                custom_styles={"background": "#f8f9fa", "border": "2px solid #007bff"}
            ),
            
            "strategic_analysis": CoreModuleConfig(
                module_id="strategic_analysis",
                title="Strategic Analysis",
                description="Comprehensive strategic analysis and assessment",
                priority=3,
                interactive_features=True,
                tooltips_enabled=True,
                custom_styles={"background": "#d4edda", "border": "2px solid #28a745"}
            ),
            
            "risk_assessment": CoreModuleConfig(
                module_id="risk_assessment",
                title="Risk Assessment",
                description="Comprehensive risk analysis and mitigation strategies",
                priority=4,
                interactive_features=True,
                tooltips_enabled=True,
                custom_styles={"background": "#fff3cd", "border": "2px solid #ffc107"}
            )
        }
    
    async def generate_core_modules_report(self, 
                                         data: Dict[str, Any],
                                         topic: str = "Analysis Report",
                                         include_modules: Optional[List[str]] = None) -> str:
        """Generate a report using the core modules (Phase 2.1)."""
        try:
            logger.info(f"Generating core modules report for topic: {topic}")
            
            # Determine which modules to include
            if include_modules is None:
                include_modules = list(self.core_modules.keys())
            
            # Validate modules
            valid_modules = [m for m in include_modules if m in self.core_modules]
            if not valid_modules:
                raise ValueError("No valid modules specified")
            
            # Sort modules by priority
            valid_modules.sort(key=lambda m: self.core_modules[m].priority)
            
            # Generate module content
            modules_data = []
            all_tooltips = []
            all_charts = []
            
            for module_id in valid_modules:
                module_config = self.core_modules[module_id]
                logger.info(f"Processing module: {module_id}")
                
                # Generate module content
                module_content = await self._generate_module_content(module_id, data, topic)
                
                # Generate tooltips if enabled
                module_tooltips = []
                if module_config.tooltips_enabled:
                    module_tooltips = await self._generate_module_tooltips(module_id, module_content)
                    all_tooltips.extend(module_tooltips)
                
                # Generate charts if enabled
                module_charts = []
                if module_config.charts_enabled:
                    module_charts = await self._generate_module_charts(module_id, module_content)
                    all_charts.extend(module_charts)
                
                # Create module data
                module_data = ModuleData(
                    module_id=module_id,
                    title=module_config.title,
                    content=module_content,
                    metadata={
                        "priority": module_config.priority,
                        "interactive_features": module_config.interactive_features
                    },
                    tooltip_data={tooltip["id"]: tooltip for tooltip in module_tooltips},
                    chart_data=module_charts
                )
                
                modules_data.append(module_data)
            
            # Generate the complete report
            report_config = {
                "title": f"{topic} - Core Analysis",
                "subtitle": f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "topic": topic,
                "modules_count": len(modules_data),
                "interactive_features": any(m.metadata.get("interactive_features", False) for m in modules_data)
            }
            
            # Generate tooltip CSS
            tooltip_css = self.tooltip_system.generate_base_css()
            if all_tooltips:
                tooltip_css += self.tooltip_system.generate_module_tooltip_css("core_modules", all_tooltips)
            
            # Generate charts HTML
            charts_html = ""
            if all_charts:
                # Convert charts to module format for the chart generator
                modules_with_charts = [{"charts": all_charts}]
                charts_html = await self.chart_generator.generate_charts_html(modules_with_charts)
            
            # Generate the final report
            report_result = await self.report_generator.generate_report(
                modules_data=modules_data,
                config=ReportConfig(
                    title=report_config["title"],
                    description=report_config["subtitle"],
                    include_tooltips=True,
                    include_charts=True
                )
            )
            
            if report_result['success']:
                logger.info(f"Core modules report generated successfully: {report_result['output_path']}")
                return report_result['output_path']
            else:
                raise Exception(f"Report generation failed: {report_result['error']}")
            
        except Exception as e:
            logger.error(f"Error generating core modules report: {e}")
            raise
    
    async def _generate_module_content(self, module_id: str, data: Dict[str, Any], topic: str) -> str:
        """Generate content for a specific module."""
        try:
            if module_id == "executive_summary":
                return await self._generate_executive_summary_content(data, topic)
            elif module_id == "strategic_recommendations":
                return await self._generate_strategic_recommendations_content(data, topic)
            elif module_id == "strategic_analysis":
                return await self._generate_strategic_analysis_content(data, topic)
            elif module_id == "risk_assessment":
                return await self._generate_risk_assessment_content(data, topic)
            else:
                return f"<p>Content for {module_id} module will be implemented in Phase 2.2.</p>"
                
        except Exception as e:
            logger.error(f"Error generating content for module {module_id}: {e}")
            return f"<p>Error generating content for {module_id} module.</p>"
    
    async def _generate_executive_summary_content(self, data: Dict[str, Any], topic: str) -> str:
        """Generate executive summary content."""
        content = f"""
        <div class="executive-summary">
            <h2>Executive Summary</h2>
            <p>This report provides a comprehensive analysis of <strong>{topic}</strong> based on the latest available data and strategic assessments.</p>
            
            <h3>Key Findings</h3>
            <ul>
                <li>Strategic implications of {topic.lower()} require careful consideration</li>
                <li>Multiple stakeholders are affected by the current situation</li>
                <li>Timely action is recommended to address identified challenges</li>
            </ul>
            
            <h3>Critical Insights</h3>
            <p>The analysis reveals several critical factors that decision-makers should consider:</p>
            <ul>
                <li><strong>Strategic Impact:</strong> Significant implications for long-term planning</li>
                <li><strong>Operational Considerations:</strong> Immediate operational adjustments may be required</li>
                <li><strong>Risk Factors:</strong> Several risk factors have been identified and assessed</li>
            </ul>
            
            <h3>Recommendations</h3>
            <p>Based on this analysis, the following high-level recommendations are provided:</p>
            <ol>
                <li>Conduct detailed strategic planning sessions</li>
                <li>Implement risk mitigation strategies</li>
                <li>Establish monitoring and evaluation frameworks</li>
            </ol>
        </div>
        """
        return content
    
    async def _generate_strategic_recommendations_content(self, data: Dict[str, Any], topic: str) -> str:
        """Generate strategic recommendations content."""
        content = f"""
        <div class="strategic-recommendations">
            <h2>Strategic Recommendations</h2>
            <p>Based on comprehensive analysis of <strong>{topic}</strong>, the following strategic recommendations are provided:</p>
            
            <h3>Immediate Actions (0-3 months)</h3>
            <div class="recommendation-category">
                <h4>1. Strategic Assessment</h4>
                <p>Conduct immediate strategic assessment to evaluate current position and capabilities.</p>
                <ul>
                    <li>Review current strategic objectives</li>
                    <li>Assess resource allocation and capabilities</li>
                    <li>Identify immediate gaps and opportunities</li>
                </ul>
            </div>
            
            <h3>Short-term Initiatives (3-12 months)</h3>
            <div class="recommendation-category">
                <h4>2. Capability Enhancement</h4>
                <p>Implement capability enhancement programs to address identified gaps.</p>
                <ul>
                    <li>Develop new capabilities where needed</li>
                    <li>Strengthen existing capabilities</li>
                    <li>Establish partnerships and alliances</li>
                </ul>
            </div>
            
            <h3>Long-term Strategic Planning (1-5 years)</h3>
            <div class="recommendation-category">
                <h4>3. Strategic Transformation</h4>
                <p>Plan and implement strategic transformation initiatives for long-term success.</p>
                <ul>
                    <li>Develop comprehensive strategic roadmap</li>
                    <li>Implement organizational changes as needed</li>
                    <li>Establish continuous improvement processes</li>
                </ul>
            </div>
        </div>
        """
        return content
    
    async def _generate_strategic_analysis_content(self, data: Dict[str, Any], topic: str) -> str:
        """Generate strategic analysis content."""
        content = f"""
        <div class="strategic-analysis">
            <h2>Strategic Analysis</h2>
            <p>Comprehensive strategic analysis of <strong>{topic}</strong> reveals the following key insights:</p>
            
            <h3>Strategic Environment Assessment</h3>
            <div class="analysis-section">
                <h4>External Environment</h4>
                <p>The external environment presents both opportunities and challenges:</p>
                <ul>
                    <li><strong>Political Factors:</strong> Current political climate influences strategic options</li>
                    <li><strong>Economic Conditions:</strong> Economic factors impact resource availability</li>
                    <li><strong>Technological Trends:</strong> Rapid technological change creates both opportunities and threats</li>
                    <li><strong>Social Dynamics:</strong> Social factors affect stakeholder relationships</li>
                </ul>
            </div>
            
            <h3>Internal Capability Analysis</h3>
            <div class="analysis-section">
                <h4>Core Competencies</h4>
                <p>Assessment of internal capabilities reveals:</p>
                <ul>
                    <li><strong>Strengths:</strong> Strong foundation in key areas</li>
                    <li><strong>Weaknesses:</strong> Areas requiring improvement identified</li>
                    <li><strong>Opportunities:</strong> Potential areas for growth and development</li>
                    <li><strong>Threats:</strong> External factors that may impact success</li>
                </ul>
            </div>
            
            <h3>Strategic Positioning</h3>
            <div class="analysis-section">
                <h4>Competitive Landscape</h4>
                <p>Analysis of competitive positioning indicates:</p>
                <ul>
                    <li>Current market position and competitive advantages</li>
                    <li>Areas where competitive differentiation is needed</li>
                    <li>Potential strategic partnerships and alliances</li>
                    <li>Long-term competitive sustainability factors</li>
                </ul>
            </div>
        </div>
        """
        return content
    
    async def _generate_risk_assessment_content(self, data: Dict[str, Any], topic: str) -> str:
        """Generate risk assessment content."""
        content = f"""
        <div class="risk-assessment">
            <h2>Risk Assessment</h2>
            <p>Comprehensive risk assessment for <strong>{topic}</strong> identifies the following key risk factors:</p>
            
            <h3>Strategic Risks</h3>
            <div class="risk-category high-risk">
                <h4>High Priority Risks</h4>
                <ul>
                    <li><strong>Strategic Misalignment:</strong> Risk of strategic objectives not aligning with capabilities</li>
                    <li><strong>Resource Constraints:</strong> Limited resources may impact strategic initiatives</li>
                    <li><strong>External Threats:</strong> External factors may threaten strategic success</li>
                </ul>
            </div>
            
            <h3>Operational Risks</h3>
            <div class="risk-category medium-risk">
                <h4>Medium Priority Risks</h4>
                <ul>
                    <li><strong>Process Inefficiencies:</strong> Operational processes may not be optimized</li>
                    <li><strong>Technology Gaps:</strong> Technology capabilities may be insufficient</li>
                    <li><strong>Human Resource Issues:</strong> Personnel challenges may impact operations</li>
                </ul>
            </div>
            
            <h3>Financial Risks</h3>
            <div class="risk-category low-risk">
                <h4>Low Priority Risks</h4>
                <ul>
                    <li><strong>Budget Constraints:</strong> Financial limitations may impact initiatives</li>
                    <li><strong>Cost Overruns:</strong> Projects may exceed budget expectations</li>
                    <li><strong>Revenue Uncertainty:</strong> Revenue projections may not be met</li>
                </ul>
            </div>
            
            <h3>Risk Mitigation Strategies</h3>
            <div class="mitigation-strategies">
                <h4>Recommended Mitigation Approaches</h4>
                <ul>
                    <li><strong>Risk Monitoring:</strong> Implement continuous risk monitoring systems</li>
                    <li><strong>Contingency Planning:</strong> Develop contingency plans for high-priority risks</li>
                    <li><strong>Resource Allocation:</strong> Allocate resources to address critical risk factors</li>
                    <li><strong>Stakeholder Communication:</strong> Maintain open communication with stakeholders</li>
                </ul>
            </div>
        </div>
        """
        return content
    
    async def _generate_module_tooltips(self, module_id: str, content: str) -> List[Dict[str, Any]]:
        """Generate tooltips for a module."""
        tooltips = []
        
        if module_id == "strategic_recommendations":
            tooltips = [
                {
                    "id": "rec_immediate",
                    "content": "Immediate actions should be taken within 0-3 months to address urgent strategic needs.",
                    "trigger": "Immediate Actions"
                },
                {
                    "id": "rec_short_term",
                    "content": "Short-term initiatives span 3-12 months and focus on capability enhancement.",
                    "trigger": "Short-term Initiatives"
                },
                {
                    "id": "rec_long_term",
                    "content": "Long-term planning covers 1-5 years and involves strategic transformation.",
                    "trigger": "Long-term Strategic Planning"
                }
            ]
        elif module_id == "strategic_analysis":
            tooltips = [
                {
                    "id": "analysis_external",
                    "content": "External environment factors include political, economic, technological, and social influences.",
                    "trigger": "External Environment"
                },
                {
                    "id": "analysis_internal",
                    "content": "Internal capabilities assessment evaluates strengths, weaknesses, opportunities, and threats.",
                    "trigger": "Internal Capability Analysis"
                },
                {
                    "id": "analysis_positioning",
                    "content": "Strategic positioning analysis examines competitive landscape and market position.",
                    "trigger": "Strategic Positioning"
                }
            ]
        elif module_id == "risk_assessment":
            tooltips = [
                {
                    "id": "risk_strategic",
                    "content": "Strategic risks impact long-term objectives and organizational success.",
                    "trigger": "Strategic Risks"
                },
                {
                    "id": "risk_operational",
                    "content": "Operational risks affect day-to-day operations and process efficiency.",
                    "trigger": "Operational Risks"
                },
                {
                    "id": "risk_financial",
                    "content": "Financial risks relate to budget, costs, and revenue projections.",
                    "trigger": "Financial Risks"
                }
            ]
        
        return tooltips
    
    async def _generate_module_charts(self, module_id: str, content: str) -> List[Dict[str, Any]]:
        """Generate charts for a module."""
        charts = []
        
        if module_id == "strategic_recommendations":
            charts = [
                {
                    "id": "rec_timeline",
                    "type": "timeline",
                    "title": "Recommendation Timeline",
                    "data": {
                        "categories": ["Immediate", "Short-term", "Long-term"],
                        "values": [3, 12, 60],
                        "labels": ["0-3 months", "3-12 months", "1-5 years"]
                    }
                }
            ]
        elif module_id == "risk_assessment":
            charts = [
                {
                    "id": "risk_matrix",
                    "type": "heatmap",
                    "title": "Risk Assessment Matrix",
                    "data": {
                        "x_labels": ["Low", "Medium", "High"],
                        "y_labels": ["Financial", "Operational", "Strategic"],
                        "values": [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
                    }
                }
            ]
        
        return charts
    
    def get_core_modules_info(self) -> Dict[str, Any]:
        """Get information about available core modules."""
        return {
            "phase": "2.1",
            "modules": {
                module_id: {
                    "title": config.title,
                    "description": config.description,
                    "enabled": config.enabled,
                    "priority": config.priority,
                    "interactive_features": config.interactive_features,
                    "tooltips_enabled": config.tooltips_enabled,
                    "charts_enabled": config.charts_enabled
                }
                for module_id, config in self.core_modules.items()
            },
            "total_modules": len(self.core_modules)
        }


# Global instance for easy access
python_modular_report_generator = PythonModularReportGenerator()
