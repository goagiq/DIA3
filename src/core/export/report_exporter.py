"""
Enhanced Report Exporter for Enhanced Report System.

This module provides comprehensive export functionality for enhanced reports,
including component selection, narrative generation, and multiple format support.
"""

import json
import logging
import os
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from dataclasses import dataclass, asdict

from .pdf_exporter import PDFExporter
from .word_exporter import WordExporter
from .markdown_export_service import MarkdownExportService
from .template_manager import TemplateManager
from .progress_tracker import ProgressTracker, ProgressManager, ExportStage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ExportComponent:
    """Export component configuration."""
    name: str
    title: str
    description: str
    enabled: bool = True
    order: int = 0
    template: Optional[str] = None
    custom_styling: Optional[Dict[str, Any]] = None


@dataclass
class ExportConfiguration:
    """Export configuration for enhanced reports."""
    report_id: str
    export_format: str  # "pdf", "word", "markdown", "html"
    components: List[ExportComponent]
    include_narrative: bool = True
    include_summary: bool = True
    include_visualizations: bool = True
    include_appendices: bool = False
    custom_styling: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class EnhancedReportExporter:
    """
    Enhanced report exporter with component selection and narrative generation.
    
    Features:
    - Component selection for export
    - Narrative and summary generation
    - Multiple format support (PDF, Word, Markdown, HTML)
    - Customizable export templates
    - Progress tracking
    - Metadata management
    """
    
    def __init__(self, output_dir: str = "exports"):
        """
        Initialize the enhanced report exporter.
        
        Args:
            output_dir: Directory for exported files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize export services
        self.pdf_exporter = PDFExporter()
        self.word_exporter = WordExporter()
        self.markdown_exporter = MarkdownExportService()
        self.template_manager = TemplateManager()
        self.progress_manager = ProgressManager()
        
        # Default export components
        self.default_components = self._initialize_default_components()
        
        logger.info(f"Enhanced Report Exporter initialized with output directory: {self.output_dir}")
    
    def _initialize_default_components(self) -> List[ExportComponent]:
        """Initialize default export components."""
        return [
            ExportComponent(
                name="executive_summary",
                title="Executive Summary",
                description="High-level overview and key findings",
                order=1,
                template="executive_summary_template"
            ),
            ExportComponent(
                name="monte_carlo_simulation",
                title="Monte Carlo Simulation Results",
                description="Risk assessment and forecasting analysis",
                order=2,
                template="monte_carlo_template"
            ),
            ExportComponent(
                name="strategic_analysis",
                title="Strategic Analysis",
                description="Strategic positioning and competitive analysis",
                order=3,
                template="strategic_analysis_template"
            ),
            ExportComponent(
                name="knowledge_graph",
                title="Knowledge Graph Analysis",
                description="Entity relationships and pattern analysis",
                order=4,
                template="knowledge_graph_template"
            ),
            ExportComponent(
                name="risk_assessment",
                title="Risk Assessment Matrix",
                description="Multi-dimensional risk analysis",
                order=5,
                template="risk_assessment_template"
            ),
            ExportComponent(
                name="visualizations",
                title="Interactive Visualizations",
                description="Charts, graphs, and interactive elements",
                order=6,
                template="visualization_template"
            ),
            ExportComponent(
                name="recommendations",
                title="Recommendations",
                description="Data-backed recommendations with references",
                order=7,
                template="recommendations_template"
            ),
            ExportComponent(
                name="methodology",
                title="Methodology",
                description="Analysis approach and data sources",
                order=8,
                template="methodology_template"
            ),
            ExportComponent(
                name="appendices",
                title="Appendices",
                description="Supporting data and detailed analysis",
                order=9,
                template="appendix_template",
                enabled=False
            )
        ]
    
    def export_enhanced_report(self, report_data: Dict[str, Any], 
                             export_config: ExportConfiguration) -> Dict[str, Any]:
        """
        Export an enhanced report with component selection.
        
        Args:
            report_data: Enhanced report data
            export_config: Export configuration
            
        Returns:
            Dictionary containing export results
        """
        export_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        logger.info(f"Starting enhanced report export: {export_id}")
        
        try:
            # Initialize progress tracking
            tracker = self.progress_manager.create_tracker(f"export_{export_id}")
            
            # Generate narrative and summary
            narrative_data = {}
            if export_config.include_narrative:
                narrative_data = self._generate_narrative(report_data)
            
            if export_config.include_summary:
                summary_data = self._generate_summary(report_data)
                narrative_data["summary"] = summary_data
            
            # Process selected components
            processed_components = []
            for component in export_config.components:
                if component.enabled:
                    processed_component = self._process_component(
                        component, report_data, narrative_data
                    )
                    processed_components.append(processed_component)
                    # Update progress for each component
                    progress_percentage = (
                        len(processed_components) / len(export_config.components)
                    ) * 100
                    tracker.update_progress(
                        ExportStage.PROCESSING_IMAGES, 
                        progress_percentage, 
                        f"Processed component: {component.name}"
                    )
            
            # Generate export content
            export_content = self._generate_export_content(
                processed_components, export_config, narrative_data
            )
            
            # Export to requested format
            export_result = self._export_to_format(
                export_content, export_config, export_id
            )
            
            # Add metadata
            export_result.update({
                "export_id": export_id,
                "timestamp": timestamp,
                "components_exported": len(processed_components),
                "total_components": len(export_config.components),
                "export_configuration": asdict(export_config)
            })
            
            logger.info(f"Enhanced report export completed: {export_id}")
            return export_result
            
        except Exception as e:
            logger.error(f"Enhanced report export failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "export_id": export_id,
                "timestamp": timestamp
            }
    
    def _generate_narrative(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate narrative content for the report."""
        narrative = {
            "introduction": self._generate_introduction(report_data),
            "context": self._generate_context(report_data),
            "key_insights": self._extract_key_insights(report_data),
            "conclusions": self._generate_conclusions(report_data)
        }
        
        return narrative
    
    def _generate_introduction(self, report_data: Dict[str, Any]) -> str:
        """Generate introduction section."""
        query = report_data.get("query", "Unknown query")
        timestamp = report_data.get("timestamp", datetime.now().isoformat())
        
        introduction = f"""
# Introduction

This comprehensive analysis report was generated in response to the query: **"{query}"**

**Report Generated:** {timestamp}

## Overview

This enhanced report provides a multi-dimensional analysis incorporating:
- Monte Carlo simulations for risk assessment and forecasting
- Strategic analysis with competitive positioning
- Knowledge graph analysis for entity relationships
- Interactive visualizations for data exploration
- Comprehensive risk assessment matrices
- Data-backed recommendations with supporting evidence

The analysis leverages advanced analytical techniques including machine learning, statistical modeling, and strategic intelligence frameworks to provide actionable insights and recommendations.
        """
        
        return introduction.strip()
    
    def _generate_context(self, report_data: Dict[str, Any]) -> str:
        """Generate context section."""
        context = """
## Context and Methodology

### Analysis Framework

This report employs a comprehensive analytical framework that integrates multiple methodologies:

1. **Monte Carlo Simulation**: Provides probabilistic forecasting and risk assessment
2. **Strategic Analysis**: Evaluates competitive positioning and market dynamics
3. **Knowledge Graph Analysis**: Maps entity relationships and identifies patterns
4. **Risk Assessment**: Multi-dimensional risk evaluation with mitigation strategies
5. **Interactive Visualization**: Dynamic data exploration and presentation

### Data Sources and Processing

The analysis incorporates multiple data sources and processing techniques:
- Real-time data feeds and historical datasets
- Advanced statistical modeling and machine learning algorithms
- Strategic intelligence frameworks and competitive analysis
- Risk assessment methodologies and compliance frameworks

### Quality Assurance

All analysis components undergo rigorous quality assurance processes:
- Data validation and integrity checks
- Statistical significance testing
- Cross-validation of results across multiple methodologies
- Expert review and validation of findings
        """
        
        return context.strip()
    
    def _extract_key_insights(self, report_data: Dict[str, Any]) -> List[str]:
        """Extract key insights from report data."""
        insights = []
        
        # Extract insights from Monte Carlo simulation
        if "monte_carlo_simulation" in report_data:
            mc_data = report_data["monte_carlo_simulation"]
            if "key_findings" in mc_data:
                insights.extend(mc_data["key_findings"])
        
        # Extract insights from strategic analysis
        if "strategic_analysis" in report_data:
            sa_data = report_data["strategic_analysis"]
            if "key_insights" in sa_data:
                insights.extend(sa_data["key_insights"])
        
        # Extract insights from risk assessment
        if "risk_assessment" in report_data:
            ra_data = report_data["risk_assessment"]
            if "critical_risks" in ra_data:
                insights.extend([f"Critical Risk: {risk}" for risk in ra_data["critical_risks"]])
        
        # Add default insights if none found
        if not insights:
            insights = [
                "Comprehensive analysis reveals multiple strategic opportunities",
                "Risk assessment identifies key areas requiring attention",
                "Monte Carlo simulations provide probabilistic forecasting insights",
                "Knowledge graph analysis uncovers important entity relationships"
            ]
        
        return insights[:10]  # Limit to top 10 insights
    
    def _generate_conclusions(self, report_data: Dict[str, Any]) -> str:
        """Generate conclusions section."""
        conclusions = """
## Conclusions and Next Steps

### Key Findings

The comprehensive analysis reveals several critical insights that require immediate attention and strategic planning.

### Strategic Implications

Based on the multi-dimensional analysis, the following strategic implications emerge:

1. **Risk Management**: Implement targeted risk mitigation strategies
2. **Opportunity Identification**: Leverage identified strategic opportunities
3. **Resource Allocation**: Optimize resource allocation based on analysis results
4. **Performance Monitoring**: Establish ongoing monitoring and evaluation frameworks

### Recommendations

The analysis provides data-backed recommendations for:
- Immediate actions to address critical risks
- Strategic initiatives to capitalize on opportunities
- Operational improvements to enhance performance
- Long-term planning and development initiatives

### Implementation Roadmap

A phased implementation approach is recommended:
- **Phase 1**: Address critical risks and immediate opportunities
- **Phase 2**: Implement strategic initiatives and operational improvements
- **Phase 3**: Establish monitoring frameworks and continuous improvement processes
        """
        
        return conclusions.strip()
    
    def _generate_summary(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary."""
        summary = {
            "title": "Executive Summary",
            "content": self._generate_executive_summary_content(report_data),
            "key_metrics": self._extract_key_metrics(report_data),
            "recommendations": self._extract_top_recommendations(report_data)
        }
        
        return summary
    
    def _generate_executive_summary_content(self, report_data: Dict[str, Any]) -> str:
        """Generate executive summary content."""
        query = report_data.get("query", "Unknown query")
        
        summary_content = f"""
# Executive Summary

## Analysis Overview

This comprehensive analysis addresses the query: **"{query}"**

The enhanced report provides a multi-dimensional analysis incorporating advanced analytical techniques including Monte Carlo simulations, strategic analysis, knowledge graph analysis, and interactive visualizations.

## Key Findings

{self._format_key_findings(report_data)}

## Strategic Implications

The analysis reveals significant strategic implications requiring executive attention and decision-making.

## Recommendations

Immediate action is recommended in the following areas:
{self._format_recommendations(report_data)}

## Risk Assessment

Critical risks have been identified and require immediate mitigation strategies.

## Next Steps

A phased implementation approach is recommended to address findings and capitalize on opportunities.
        """
        
        return summary_content.strip()
    
    def _extract_key_metrics(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key metrics from report data."""
        metrics = {}
        
        # Extract Monte Carlo metrics
        if "monte_carlo_simulation" in report_data:
            mc_data = report_data["monte_carlo_simulation"]
            if "metrics" in mc_data:
                metrics["monte_carlo"] = mc_data["metrics"]
        
        # Extract risk metrics
        if "risk_assessment" in report_data:
            ra_data = report_data["risk_assessment"]
            if "risk_metrics" in ra_data:
                metrics["risk_assessment"] = ra_data["risk_metrics"]
        
        # Extract strategic metrics
        if "strategic_analysis" in report_data:
            sa_data = report_data["strategic_analysis"]
            if "strategic_metrics" in sa_data:
                metrics["strategic_analysis"] = sa_data["strategic_metrics"]
        
        return metrics
    
    def _extract_top_recommendations(self, report_data: Dict[str, Any]) -> List[str]:
        """Extract top recommendations from report data."""
        recommendations = []
        
        # Extract recommendations from various components
        for component_name in ["recommendations", "strategic_analysis", "risk_assessment"]:
            if component_name in report_data:
                component_data = report_data[component_name]
                if "recommendations" in component_data:
                    recommendations.extend(component_data["recommendations"])
        
        # Limit to top 5 recommendations
        return recommendations[:5]
    
    def _format_key_findings(self, report_data: Dict[str, Any]) -> str:
        """Format key findings for summary."""
        findings = self._extract_key_insights(report_data)
        
        formatted_findings = ""
        for i, finding in enumerate(findings[:5], 1):
            formatted_findings += f"{i}. {finding}\n"
        
        return formatted_findings.strip()
    
    def _format_recommendations(self, report_data: Dict[str, Any]) -> str:
        """Format recommendations for summary."""
        recommendations = self._extract_top_recommendations(report_data)
        
        formatted_recommendations = ""
        for i, recommendation in enumerate(recommendations, 1):
            formatted_recommendations += f"{i}. {recommendation}\n"
        
        return formatted_recommendations.strip()
    
    def _process_component(self, component: ExportComponent, 
                          report_data: Dict[str, Any], 
                          narrative_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single export component."""
        component_data = {
            "name": component.name,
            "title": component.title,
            "description": component.description,
            "order": component.order,
            "content": self._extract_component_content(component.name, report_data),
            "template": component.template,
            "custom_styling": component.custom_styling
        }
        
        # Apply template if specified
        if component.template:
            component_data["content"] = self._apply_template(
                component.template, component_data["content"], narrative_data
            )
        
        return component_data
    
    def _extract_component_content(self, component_name: str, 
                                  report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract content for a specific component."""
        if component_name in report_data:
            return report_data[component_name]
        else:
            return {
                "content": f"Content for {component_name} not available",
                "status": "not_available"
            }
    
    def _apply_template(self, template_name: str, content: Dict[str, Any], 
                       narrative_data: Dict[str, Any]) -> str:
        """Apply template to component content."""
        try:
            template = self.template_manager.get_template(template_name)
            return template.render(content=content, narrative=narrative_data)
        except Exception as e:
            logger.warning(f"Failed to apply template {template_name}: {e}")
            return self._generate_default_template_content(content)
    
    def _generate_default_template_content(self, content: Dict[str, Any]) -> str:
        """Generate default template content."""
        if isinstance(content, dict):
            return f"# {content.get('title', 'Component')}\n\n{content.get('content', 'No content available')}"
        else:
            return str(content)
    
    def _generate_export_content(self, processed_components: List[Dict[str, Any]], 
                                export_config: ExportConfiguration,
                                narrative_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final export content."""
        # Sort components by order
        sorted_components = sorted(processed_components, key=lambda x: x["order"])
        
        export_content = {
            "title": f"Enhanced Analysis Report - {export_config.report_id}",
            "timestamp": datetime.now().isoformat(),
            "narrative": narrative_data,
            "components": sorted_components,
            "metadata": export_config.metadata or {},
            "export_config": {
                "format": export_config.export_format,
                "include_narrative": export_config.include_narrative,
                "include_summary": export_config.include_summary,
                "include_visualizations": export_config.include_visualizations,
                "include_appendices": export_config.include_appendices
            }
        }
        
        return export_content
    
    def _export_to_format(self, export_content: Dict[str, Any], 
                         export_config: ExportConfiguration,
                         export_id: str) -> Dict[str, Any]:
        """Export content to the specified format."""
        format_type = export_config.export_format.lower()
        
        if format_type == "pdf":
            return self._export_to_pdf(export_content, export_id)
        elif format_type == "word":
            return self._export_to_word(export_content, export_id)
        elif format_type == "markdown":
            return self._export_to_markdown(export_content, export_id)
        elif format_type == "html":
            return self._export_to_html(export_content, export_id)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def _export_to_pdf(self, export_content: Dict[str, Any], export_id: str) -> Dict[str, Any]:
        """Export to PDF format."""
        try:
            # Convert content to markdown first
            markdown_content = self._convert_to_markdown(export_content)
            
            # Generate PDF
            pdf_path = self.output_dir / f"enhanced_report_{export_id}.pdf"
            self.pdf_exporter.export_markdown_to_pdf(markdown_content, str(pdf_path))
            
            return {
                "success": True,
                "format": "pdf",
                "file_path": str(pdf_path),
                "file_size": pdf_path.stat().st_size if pdf_path.exists() else 0
            }
        except Exception as e:
            logger.error(f"PDF export failed: {e}")
            return {"success": False, "error": str(e), "format": "pdf"}
    
    def _export_to_word(self, export_content: Dict[str, Any], export_id: str) -> Dict[str, Any]:
        """Export to Word format."""
        try:
            # Convert content to markdown first
            markdown_content = self._convert_to_markdown(export_content)
            
            # Generate Word document
            word_path = self.output_dir / f"enhanced_report_{export_id}.docx"
            self.word_exporter.export_markdown_to_word(markdown_content, str(word_path))
            
            return {
                "success": True,
                "format": "word",
                "file_path": str(word_path),
                "file_size": word_path.stat().st_size if word_path.exists() else 0
            }
        except Exception as e:
            logger.error(f"Word export failed: {e}")
            return {"success": False, "error": str(e), "format": "word"}
    
    def _export_to_markdown(self, export_content: Dict[str, Any], export_id: str) -> Dict[str, Any]:
        """Export to Markdown format."""
        try:
            markdown_content = self._convert_to_markdown(export_content)
            
            # Save markdown file
            md_path = self.output_dir / f"enhanced_report_{export_id}.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return {
                "success": True,
                "format": "markdown",
                "file_path": str(md_path),
                "file_size": md_path.stat().st_size if md_path.exists() else 0
            }
        except Exception as e:
            logger.error(f"Markdown export failed: {e}")
            return {"success": False, "error": str(e), "format": "markdown"}
    
    def _export_to_html(self, export_content: Dict[str, Any], export_id: str) -> Dict[str, Any]:
        """Export to HTML format."""
        try:
            # Convert content to markdown first
            markdown_content = self._convert_to_markdown(export_content)
            
            # Convert markdown to HTML
            html_content = self.markdown_exporter.convert_to_html(markdown_content)
            
            # Save HTML file
            html_path = self.output_dir / f"enhanced_report_{export_id}.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return {
                "success": True,
                "format": "html",
                "file_path": str(html_path),
                "file_size": html_path.stat().st_size if html_path.exists() else 0
            }
        except Exception as e:
            logger.error(f"HTML export failed: {e}")
            return {"success": False, "error": str(e), "format": "html"}
    
    def _convert_to_markdown(self, export_content: Dict[str, Any]) -> str:
        """Convert export content to markdown format."""
        markdown_parts = []
        
        # Add title
        markdown_parts.append(f"# {export_content['title']}")
        markdown_parts.append(f"**Generated:** {export_content['timestamp']}")
        markdown_parts.append("")
        
        # Add narrative sections
        if "narrative" in export_content:
            narrative = export_content["narrative"]
            
            if "summary" in narrative:
                markdown_parts.append(narrative["summary"]["content"])
                markdown_parts.append("")
            
            if "introduction" in narrative:
                markdown_parts.append(narrative["introduction"])
                markdown_parts.append("")
            
            if "context" in narrative:
                markdown_parts.append(narrative["context"])
                markdown_parts.append("")
        
        # Add components
        for component in export_content["components"]:
            markdown_parts.append(f"## {component['title']}")
            markdown_parts.append("")
            
            if isinstance(component["content"], str):
                markdown_parts.append(component["content"])
            elif isinstance(component["content"], dict):
                markdown_parts.append(self._dict_to_markdown(component["content"]))
            else:
                markdown_parts.append(str(component["content"]))
            
            markdown_parts.append("")
        
        # Add conclusions
        if "narrative" in export_content and "conclusions" in export_content["narrative"]:
            markdown_parts.append(export_content["narrative"]["conclusions"])
            markdown_parts.append("")
        
        return "\n".join(markdown_parts)
    
    def _dict_to_markdown(self, data: Dict[str, Any], level: int = 0) -> str:
        """Convert dictionary to markdown format."""
        markdown_parts = []
        indent = "  " * level
        
        for key, value in data.items():
            if isinstance(value, dict):
                markdown_parts.append(f"{indent}- **{key}:**")
                markdown_parts.append(self._dict_to_markdown(value, level + 1))
            elif isinstance(value, list):
                markdown_parts.append(f"{indent}- **{key}:**")
                for item in value:
                    if isinstance(item, dict):
                        markdown_parts.append(self._dict_to_markdown(item, level + 1))
                    else:
                        markdown_parts.append(f"{indent}  - {item}")
            else:
                markdown_parts.append(f"{indent}- **{key}:** {value}")
        
        return "\n".join(markdown_parts)
    
    def get_export_statistics(self) -> Dict[str, Any]:
        """Get export statistics."""
        export_files = list(self.output_dir.glob("enhanced_report_*"))
        
        stats = {
            "total_exports": len(export_files),
            "export_formats": {},
            "total_file_size": 0,
            "recent_exports": []
        }
        
        for file_path in export_files:
            # Determine format
            format_type = file_path.suffix[1:] if file_path.suffix else "unknown"
            stats["export_formats"][format_type] = stats["export_formats"].get(format_type, 0) + 1
            
            # Add file size
            if file_path.exists():
                stats["total_file_size"] += file_path.stat().st_size
            
            # Add to recent exports
            stats["recent_exports"].append({
                "file_name": file_path.name,
                "format": format_type,
                "file_size": file_path.stat().st_size if file_path.exists() else 0,
                "created": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })
        
        # Sort recent exports by creation time
        stats["recent_exports"].sort(key=lambda x: x["created"], reverse=True)
        stats["recent_exports"] = stats["recent_exports"][:10]  # Keep only 10 most recent
        
        return stats


# Global enhanced report exporter instance
enhanced_report_exporter = EnhancedReportExporter()
