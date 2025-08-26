"""
Dynamic Report Generator
Part of Phase 3: Dynamic Report Generation implementation.

Provides dynamic report generation capabilities that:
- Analyze data structure to determine optimal report format
- Generate dynamic templates based on query results
- Integrate knowledge graph intelligence into reports
- Create adaptive visualizations based on data types
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass
import pandas as pd

from .knowledge_graph_intelligence_service import KnowledgeGraphIntelligenceService, StrategicIntelligence

logger = logging.getLogger(__name__)


@dataclass
class ReportTemplate:
    """Dynamic report template structure."""
    template_id: str
    sections: List[str]
    data_types: List[str]
    visualization_types: List[str]
    max_length: int
    include_metrics: bool
    include_visualizations: bool
    include_methodology: bool
    knowledge_graph_integration: bool


@dataclass
class Report:
    """Generated report structure."""
    report_id: str
    template_used: ReportTemplate
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    knowledge_graph_insights: Optional[StrategicIntelligence]
    generated_at: str
    confidence_score: float


class DynamicReportGenerator:
    """Dynamic report generation system with knowledge graph intelligence integration."""
    
    def __init__(self, knowledge_graph_service: Optional[KnowledgeGraphIntelligenceService] = None):
        """Initialize the dynamic report generator.
        
        Args:
            knowledge_graph_service: Optional knowledge graph intelligence service
        """
        self.kg_service = knowledge_graph_service
        self.template_cache = {}
        self.data_analyzer = DataStructureAnalyzer()
        self.visualization_generator = DynamicVisualizationGenerator()
        
        logger.info("Dynamic Report Generator initialized")
    
    async def generate_report(
        self, 
        data_structure: Dict[str, Any], 
        query_results: Dict[str, Any],
        topic: Optional[str] = None,
        domain: str = "general"
    ) -> Report:
        """Generate a dynamic report based on data structure analysis and query results.
        
        Args:
            data_structure: Structure of the data to be reported
            query_results: Results from the analysis query
            topic: Optional topic for the report
            domain: Domain context for the report
            
        Returns:
            Generated report with dynamic template and knowledge graph insights
        """
        try:
            logger.info(f"Generating dynamic report for domain: {domain}")
            
            # Step 1: Analyze data structure
            data_analysis = self.data_analyzer.analyze_data_structure(data_structure, query_results)
            
            # Step 2: Determine optimal report format
            optimal_template = await self._determine_optimal_template(data_analysis, domain)
            
            # Step 3: Extract knowledge graph intelligence if available
            kg_insights = None
            if self.kg_service:
                kg_insights = await self._extract_knowledge_graph_intelligence(
                    data_analysis, domain, topic
                )
            
            # Step 4: Generate dynamic template
            dynamic_template = await self._generate_dynamic_template(
                optimal_template, data_analysis, kg_insights
            )
            
            # Step 5: Generate report content
            report_content = await self._generate_report_content(
                data_structure, query_results, dynamic_template, kg_insights
            )
            
            # Step 6: Create report metadata
            metadata = self._create_report_metadata(data_analysis, dynamic_template, kg_insights)
            
            # Step 7: Calculate confidence score
            confidence_score = self._calculate_report_confidence(
                data_analysis, kg_insights, report_content
            )
            
            # Create and return report
            report = Report(
                report_id=f"dynamic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                template_used=dynamic_template,
                content=report_content,
                metadata=metadata,
                knowledge_graph_insights=kg_insights,
                generated_at=datetime.now().isoformat(),
                confidence_score=confidence_score
            )
            
            logger.info(f"Dynamic report generated successfully with confidence: {confidence_score:.2f}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating dynamic report: {e}")
            return self._create_error_report(str(e))
    
    async def generate_intelligent_report(
        self, 
        topic: str, 
        analysis_data: Dict[str, Any],
        domain: str = "general"
    ) -> Report:
        """Generate an intelligent report with knowledge graph integration.
        
        Args:
            topic: Topic for the report
            analysis_data: Analysis data to include in the report
            domain: Domain context for the report
            
        Returns:
            Intelligent report with knowledge graph insights
        """
        try:
            logger.info(f"Generating intelligent report for topic: {topic}")
            
            # Step 1: Query knowledge graph for related insights
            kg_insights = None
            if self.kg_service:
                query_context = {
                    "domain": domain,
                    "entities": [topic],
                    "timeframe": "1y",
                    "geographic_scope": "global",
                    "strategic_objectives": ["analysis", "insights"],
                    "constraints": []
                }
                kg_insights = await self.kg_service.extract_strategic_intelligence(query_context)
            
            # Step 2: Generate cross-domain analysis
            cross_domain_analysis = await self._generate_cross_domain_analysis(topic, domain)
            
            # Step 3: Include predictive intelligence
            predictive_intelligence = await self._generate_predictive_intelligence(topic, domain)
            
            # Step 4: Create dynamic visualizations
            visualizations = await self._create_dynamic_visualizations(
                analysis_data, kg_insights, cross_domain_analysis
            )
            
            # Step 5: Generate comprehensive report content
            report_content = {
                "topic_analysis": {
                    "topic": topic,
                    "domain": domain,
                    "analysis_summary": analysis_data.get("summary", ""),
                    "key_findings": analysis_data.get("findings", [])
                },
                "knowledge_graph_insights": self.kg_service.export_intelligence_report(kg_insights) if kg_insights and self.kg_service else {},
                "cross_domain_analysis": cross_domain_analysis,
                "predictive_intelligence": predictive_intelligence,
                "visualizations": visualizations,
                "recommendations": await self._generate_intelligent_recommendations(
                    topic, analysis_data, kg_insights
                )
            }
            
            # Step 6: Create intelligent template
            intelligent_template = ReportTemplate(
                template_id="intelligent_report",
                sections=["topic_analysis", "knowledge_graph_insights", "cross_domain_analysis", 
                         "predictive_intelligence", "visualizations", "recommendations"],
                data_types=["text", "structured", "visual"],
                visualization_types=["charts", "graphs", "maps"],
                max_length=5000,
                include_metrics=True,
                include_visualizations=True,
                include_methodology=True,
                knowledge_graph_integration=True
            )
            
            # Create and return intelligent report
            report = Report(
                report_id=f"intelligent_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                template_used=intelligent_template,
                content=report_content,
                metadata=self._create_intelligent_report_metadata(topic, domain, kg_insights),
                knowledge_graph_insights=kg_insights,
                generated_at=datetime.now().isoformat(),
                confidence_score=kg_insights.confidence_score if kg_insights else 0.5
            )
            
            logger.info(f"Intelligent report generated successfully for topic: {topic}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating intelligent report: {e}")
            return self._create_error_report(str(e))
    
    async def _determine_optimal_template(
        self, 
        data_analysis: Dict[str, Any], 
        domain: str
    ) -> ReportTemplate:
        """Determine the optimal template based on data analysis."""
        try:
            # Analyze data characteristics
            data_types = data_analysis.get("data_types", [])
            complexity = data_analysis.get("complexity", "medium")
            volume = data_analysis.get("volume", "medium")
            
            # Determine template based on characteristics
            if "time_series" in data_types:
                template_id = "trend_analysis"
                sections = ["executive_summary", "trend_analysis", "forecasting", "recommendations"]
                visualization_types = ["line_charts", "heatmaps"]
            elif "categorical" in data_types:
                template_id = "comparative_analysis"
                sections = ["executive_summary", "comparative_analysis", "benchmarking", "recommendations"]
                visualization_types = ["bar_charts", "pie_charts"]
            elif "geospatial" in data_types:
                template_id = "geospatial_analysis"
                sections = ["executive_summary", "geospatial_analysis", "regional_insights", "recommendations"]
                visualization_types = ["maps", "choropleth"]
            elif complexity == "high":
                template_id = "comprehensive_analysis"
                sections = ["executive_summary", "detailed_analysis", "methodology", "findings", "recommendations"]
                visualization_types = ["multi_charts", "interactive"]
            else:
                template_id = "standard_analysis"
                sections = ["executive_summary", "analysis", "recommendations"]
                visualization_types = ["basic_charts"]
            
            return ReportTemplate(
                template_id=template_id,
                sections=sections,
                data_types=data_types,
                visualization_types=visualization_types,
                max_length=self._calculate_max_length(complexity, volume),
                include_metrics=True,
                include_visualizations=True,
                include_methodology=complexity == "high",
                knowledge_graph_integration=True
            )
            
        except Exception as e:
            logger.error(f"Error determining optimal template: {e}")
            return self._get_default_template()
    
    async def _extract_knowledge_graph_intelligence(
        self, 
        data_analysis: Dict[str, Any], 
        domain: str, 
        topic: Optional[str]
    ) -> Optional[StrategicIntelligence]:
        """Extract knowledge graph intelligence for the report."""
        try:
            if not self.kg_service:
                return None
            
            # Create query context based on data analysis
            entities = data_analysis.get("key_entities", [])
            if topic:
                entities.append(topic)
            
            query_context = {
                "domain": domain,
                "entities": entities,
                "timeframe": "1y",
                "geographic_scope": "global",
                "strategic_objectives": ["analysis", "insights", "recommendations"],
                "constraints": []
            }
            
            return await self.kg_service.extract_strategic_intelligence(query_context)
            
        except Exception as e:
            logger.error(f"Error extracting knowledge graph intelligence: {e}")
            return None
    
    async def _generate_dynamic_template(
        self, 
        base_template: ReportTemplate, 
        data_analysis: Dict[str, Any],
        kg_insights: Optional[StrategicIntelligence]
    ) -> ReportTemplate:
        """Generate a dynamic template based on data analysis and knowledge graph insights."""
        try:
            # Enhance template based on knowledge graph insights
            enhanced_sections = base_template.sections.copy()
            
            if kg_insights:
                if kg_insights.strategic_patterns:
                    enhanced_sections.append("strategic_patterns")
                if kg_insights.risk_indicators:
                    enhanced_sections.append("risk_analysis")
                if kg_insights.opportunities:
                    enhanced_sections.append("opportunity_analysis")
                if kg_insights.historical_insights:
                    enhanced_sections.append("historical_context")
                if kg_insights.predictive_trends:
                    enhanced_sections.append("predictive_insights")
                if kg_insights.cross_domain_connections:
                    enhanced_sections.append("cross_domain_analysis")
            
            # Enhance visualization types based on data analysis
            enhanced_visualizations = base_template.visualization_types.copy()
            if data_analysis.get("has_relationships", False):
                enhanced_visualizations.append("network_graphs")
            if data_analysis.get("has_temporal_data", False):
                enhanced_visualizations.append("timeline_charts")
            
            return ReportTemplate(
                template_id=f"{base_template.template_id}_enhanced",
                sections=enhanced_sections,
                data_types=base_template.data_types,
                visualization_types=enhanced_visualizations,
                max_length=base_template.max_length,
                include_metrics=base_template.include_metrics,
                include_visualizations=base_template.include_visualizations,
                include_methodology=base_template.include_methodology,
                knowledge_graph_integration=True
            )
            
        except Exception as e:
            logger.error(f"Error generating dynamic template: {e}")
            return base_template
    
    async def _generate_report_content(
        self, 
        data_structure: Dict[str, Any], 
        query_results: Dict[str, Any],
        template: ReportTemplate,
        kg_insights: Optional[StrategicIntelligence]
    ) -> Dict[str, Any]:
        """Generate report content based on template and data."""
        try:
            content = {}
            
            # Generate content for each section
            for section in template.sections:
                if section == "executive_summary":
                    content[section] = await self._generate_executive_summary(
                        data_structure, query_results, kg_insights
                    )
                elif section == "strategic_patterns" and kg_insights:
                    content[section] = kg_insights.strategic_patterns
                elif section == "risk_analysis" and kg_insights:
                    content[section] = kg_insights.risk_indicators
                elif section == "opportunity_analysis" and kg_insights:
                    content[section] = kg_insights.opportunities
                elif section == "historical_context" and kg_insights:
                    content[section] = kg_insights.historical_insights
                elif section == "predictive_insights" and kg_insights:
                    content[section] = kg_insights.predictive_trends
                elif section == "cross_domain_analysis" and kg_insights:
                    content[section] = kg_insights.cross_domain_connections
                else:
                    content[section] = await self._generate_section_content(
                        section, data_structure, query_results
                    )
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating report content: {e}")
            return {"error": str(e)}
    
    async def _generate_cross_domain_analysis(self, topic: str, domain: str) -> Dict[str, Any]:
        """Generate cross-domain analysis for the topic."""
        try:
            # This would integrate with cross-domain analysis capabilities
            return {
                "cross_domain_connections": [],
                "domain_interactions": [],
                "synergy_opportunities": [],
                "conflict_areas": []
            }
        except Exception as e:
            logger.error(f"Error generating cross-domain analysis: {e}")
            return {}
    
    async def _generate_predictive_intelligence(self, topic: str, domain: str) -> Dict[str, Any]:
        """Generate predictive intelligence for the topic."""
        try:
            # This would integrate with predictive analytics capabilities
            return {
                "trend_predictions": [],
                "scenario_analysis": [],
                "risk_forecasts": [],
                "opportunity_projections": []
            }
        except Exception as e:
            logger.error(f"Error generating predictive intelligence: {e}")
            return {}
    
    async def _create_dynamic_visualizations(
        self, 
        analysis_data: Dict[str, Any],
        kg_insights: Optional[StrategicIntelligence],
        cross_domain_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create dynamic visualizations based on data and insights."""
        try:
            visualizations = {}
            
            # Generate entity relationship visualization if knowledge graph insights available
            if kg_insights and kg_insights.relationships:
                visualizations["entity_relationships"] = {
                    "type": "network_graph",
                    "data": kg_insights.relationships,
                    "title": "Entity Relationship Network"
                }
            
            # Generate strategic patterns visualization
            if kg_insights and kg_insights.strategic_patterns:
                visualizations["strategic_patterns"] = {
                    "type": "bar_chart",
                    "data": kg_insights.strategic_patterns,
                    "title": "Strategic Patterns Analysis"
                }
            
            # Generate risk vs opportunity matrix
            if kg_insights:
                visualizations["risk_opportunity_matrix"] = {
                    "type": "scatter_plot",
                    "data": {
                        "risks": kg_insights.risk_indicators,
                        "opportunities": kg_insights.opportunities
                    },
                    "title": "Risk vs Opportunity Matrix"
                }
            
            return visualizations
            
        except Exception as e:
            logger.error(f"Error creating dynamic visualizations: {e}")
            return {}
    
    async def _generate_intelligent_recommendations(
        self, 
        topic: str, 
        analysis_data: Dict[str, Any],
        kg_insights: Optional[StrategicIntelligence]
    ) -> List[Dict[str, Any]]:
        """Generate intelligent recommendations based on analysis and knowledge graph insights."""
        try:
            recommendations = []
            
            # Generate recommendations based on analysis data
            if analysis_data.get("findings"):
                for finding in analysis_data["findings"]:
                    recommendations.append({
                        "type": "analysis_based",
                        "recommendation": f"Address finding: {finding}",
                        "priority": "medium",
                        "confidence": 0.7
                    })
            
            # Generate recommendations based on knowledge graph insights
            if kg_insights:
                if kg_insights.risk_indicators:
                    recommendations.append({
                        "type": "risk_mitigation",
                        "recommendation": f"Mitigate identified risks: {', '.join(kg_insights.risk_indicators[:3])}",
                        "priority": "high",
                        "confidence": kg_insights.confidence_score
                    })
                
                if kg_insights.opportunities:
                    recommendations.append({
                        "type": "opportunity_capture",
                        "recommendation": f"Pursue opportunities: {', '.join(kg_insights.opportunities[:3])}",
                        "priority": "medium",
                        "confidence": kg_insights.confidence_score
                    })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating intelligent recommendations: {e}")
            return []
    
    def _calculate_max_length(self, complexity: str, volume: str) -> int:
        """Calculate maximum report length based on complexity and volume."""
        base_length = 2000
        
        if complexity == "high":
            base_length *= 1.5
        elif complexity == "low":
            base_length *= 0.7
        
        if volume == "high":
            base_length *= 1.3
        elif volume == "low":
            base_length *= 0.8
        
        return int(base_length)
    
    def _create_report_metadata(
        self, 
        data_analysis: Dict[str, Any], 
        template: ReportTemplate,
        kg_insights: Optional[StrategicIntelligence]
    ) -> Dict[str, Any]:
        """Create metadata for the generated report."""
        return {
            "generated_at": datetime.now().isoformat(),
            "template_used": template.template_id,
            "data_analysis": data_analysis,
            "knowledge_graph_integration": kg_insights is not None,
            "confidence_score": kg_insights.confidence_score if kg_insights else 0.5,
            "sections_count": len(template.sections),
            "visualization_count": len(template.visualization_types)
        }
    
    def _create_intelligent_report_metadata(
        self, 
        topic: str, 
        domain: str, 
        kg_insights: Optional[StrategicIntelligence]
    ) -> Dict[str, Any]:
        """Create metadata for intelligent reports."""
        return {
            "generated_at": datetime.now().isoformat(),
            "report_type": "intelligent_report",
            "topic": topic,
            "domain": domain,
            "knowledge_graph_integration": kg_insights is not None,
            "confidence_score": kg_insights.confidence_score if kg_insights else 0.5,
            "strategic_intelligence_available": kg_insights is not None
        }
    
    def _calculate_report_confidence(
        self, 
        data_analysis: Dict[str, Any],
        kg_insights: Optional[StrategicIntelligence],
        report_content: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for the generated report."""
        try:
            confidence = 0.5  # Base confidence
            
            # Adjust based on data analysis quality
            if data_analysis.get("quality", "medium") == "high":
                confidence += 0.2
            elif data_analysis.get("quality", "medium") == "low":
                confidence -= 0.1
            
            # Adjust based on knowledge graph insights
            if kg_insights:
                confidence += kg_insights.confidence_score * 0.3
            
            # Adjust based on report content completeness
            if len(report_content) > 5:
                confidence += 0.1
            
            return min(1.0, max(0.0, confidence))
            
        except Exception as e:
            logger.error(f"Error calculating report confidence: {e}")
            return 0.5
    
    def _get_default_template(self) -> ReportTemplate:
        """Get default template when optimal template determination fails."""
        return ReportTemplate(
            template_id="default",
            sections=["executive_summary", "analysis", "recommendations"],
            data_types=["text"],
            visualization_types=["basic_charts"],
            max_length=2000,
            include_metrics=True,
            include_visualizations=True,
            include_methodology=False,
            knowledge_graph_integration=False
        )
    
    def _create_error_report(self, error_message: str) -> Report:
        """Create an error report when generation fails."""
        return Report(
            report_id=f"error_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            template_used=self._get_default_template(),
            content={"error": error_message},
            metadata={"error": True, "error_message": error_message},
            knowledge_graph_insights=None,
            generated_at=datetime.now().isoformat(),
            confidence_score=0.0
        )


class DataStructureAnalyzer:
    """Analyzes data structure to determine optimal report format."""
    
    def analyze_data_structure(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data structure to determine characteristics."""
        try:
            analysis = {
                "data_types": self._identify_data_types(data_structure, query_results),
                "complexity": self._assess_complexity(data_structure, query_results),
                "volume": self._assess_volume(data_structure, query_results),
                "quality": self._assess_quality(data_structure, query_results),
                "key_entities": self._extract_key_entities(data_structure, query_results),
                "has_relationships": self._has_relationships(data_structure, query_results),
                "has_temporal_data": self._has_temporal_data(data_structure, query_results)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing data structure: {e}")
            return self._get_default_analysis()
    
    def _identify_data_types(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> List[str]:
        """Identify data types present in the data."""
        data_types = []
        
        # Analyze data structure for different types
        if self._contains_time_series(data_structure, query_results):
            data_types.append("time_series")
        if self._contains_categorical(data_structure, query_results):
            data_types.append("categorical")
        if self._contains_geospatial(data_structure, query_results):
            data_types.append("geospatial")
        if self._contains_numerical(data_structure, query_results):
            data_types.append("numerical")
        if self._contains_textual(data_structure, query_results):
            data_types.append("textual")
        
        return data_types if data_types else ["textual"]
    
    def _assess_complexity(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> str:
        """Assess the complexity of the data."""
        # Simple heuristic for complexity assessment
        if len(str(data_structure)) > 10000 or len(str(query_results)) > 10000:
            return "high"
        elif len(str(data_structure)) > 5000 or len(str(query_results)) > 5000:
            return "medium"
        else:
            return "low"
    
    def _assess_volume(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> str:
        """Assess the volume of the data."""
        # Simple heuristic for volume assessment
        total_size = len(str(data_structure)) + len(str(query_results))
        if total_size > 50000:
            return "high"
        elif total_size > 10000:
            return "medium"
        else:
            return "low"
    
    def _assess_quality(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> str:
        """Assess the quality of the data."""
        # Simple heuristic for quality assessment
        if data_structure and query_results:
            return "high"
        elif data_structure or query_results:
            return "medium"
        else:
            return "low"
    
    def _extract_key_entities(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> List[str]:
        """Extract key entities from the data."""
        entities = []
        
        # Extract entities from data structure keys
        if isinstance(data_structure, dict):
            entities.extend(list(data_structure.keys()))
        
        # Extract entities from query results
        if isinstance(query_results, dict):
            entities.extend(list(query_results.keys()))
        
        return list(set(entities))[:10]  # Limit to top 10 entities
    
    def _has_relationships(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> bool:
        """Check if data contains relationships."""
        # Simple check for relationship indicators
        data_str = str(data_structure) + str(query_results)
        relationship_indicators = ["relationship", "connection", "link", "correlation", "association"]
        return any(indicator in data_str.lower() for indicator in relationship_indicators)
    
    def _has_temporal_data(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> bool:
        """Check if data contains temporal information."""
        # Simple check for temporal indicators
        data_str = str(data_structure) + str(query_results)
        temporal_indicators = ["date", "time", "year", "month", "day", "timestamp", "period"]
        return any(indicator in data_str.lower() for indicator in temporal_indicators)
    
    def _contains_time_series(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> bool:
        """Check if data contains time series information."""
        return self._has_temporal_data(data_structure, query_results)
    
    def _contains_categorical(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> bool:
        """Check if data contains categorical information."""
        # Simple check for categorical indicators
        data_str = str(data_structure) + str(query_results)
        categorical_indicators = ["category", "type", "class", "group", "classification"]
        return any(indicator in data_str.lower() for indicator in categorical_indicators)
    
    def _contains_geospatial(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> bool:
        """Check if data contains geospatial information."""
        # Simple check for geospatial indicators
        data_str = str(data_structure) + str(query_results)
        geospatial_indicators = ["location", "geography", "region", "country", "city", "coordinates"]
        return any(indicator in data_str.lower() for indicator in geospatial_indicators)
    
    def _contains_numerical(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> bool:
        """Check if data contains numerical information."""
        # Simple check for numerical indicators
        data_str = str(data_structure) + str(query_results)
        numerical_indicators = ["count", "number", "amount", "quantity", "percentage", "ratio"]
        return any(indicator in data_str.lower() for indicator in numerical_indicators)
    
    def _contains_textual(self, data_structure: Dict[str, Any], query_results: Dict[str, Any]) -> bool:
        """Check if data contains textual information."""
        # Default to True as most data contains some text
        return True
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Get default analysis when analysis fails."""
        return {
            "data_types": ["textual"],
            "complexity": "medium",
            "volume": "medium",
            "quality": "medium",
            "key_entities": [],
            "has_relationships": False,
            "has_temporal_data": False
        }


class DynamicVisualizationGenerator:
    """Generates dynamic visualizations based on data types and content."""
    
    async def generate_visualizations(self, data: Dict[str, Any], template: ReportTemplate) -> Dict[str, Any]:
        """Generate visualizations based on data and template."""
        try:
            visualizations = {}
            
            for viz_type in template.visualization_types:
                if viz_type == "line_charts":
                    visualizations["trends"] = await self._generate_line_chart(data)
                elif viz_type == "bar_charts":
                    visualizations["comparisons"] = await self._generate_bar_chart(data)
                elif viz_type == "pie_charts":
                    visualizations["distributions"] = await self._generate_pie_chart(data)
                elif viz_type == "network_graphs":
                    visualizations["relationships"] = await self._generate_network_graph(data)
                elif viz_type == "maps":
                    visualizations["geospatial"] = await self._generate_map(data)
            
            return visualizations
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
            return {}
    
    async def _generate_line_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate line chart visualization."""
        return {
            "type": "line_chart",
            "title": "Trend Analysis",
            "data": [],
            "config": {"responsive": True}
        }
    
    async def _generate_bar_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate bar chart visualization."""
        return {
            "type": "bar_chart",
            "title": "Comparative Analysis",
            "data": [],
            "config": {"responsive": True}
        }
    
    async def _generate_pie_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate pie chart visualization."""
        return {
            "type": "pie_chart",
            "title": "Distribution Analysis",
            "data": [],
            "config": {"responsive": True}
        }
    
    async def _generate_network_graph(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate network graph visualization."""
        return {
            "type": "network_graph",
            "title": "Relationship Network",
            "data": {"nodes": [], "edges": []},
            "config": {"responsive": True}
        }
    
    async def _generate_map(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate map visualization."""
        return {
            "type": "map",
            "title": "Geospatial Analysis",
            "data": [],
            "config": {"responsive": True}
        }
    
    async def _generate_executive_summary(
        self, 
        data_structure: Dict[str, Any], 
        query_results: Dict[str, Any],
        kg_insights: Optional[StrategicIntelligence]
    ) -> Dict[str, Any]:
        """Generate executive summary for the report."""
        try:
            summary = {
                "overview": "Comprehensive analysis report with strategic insights",
                "key_findings": query_results.get("findings", [])[:3],
                "strategic_implications": [],
                "recommendations_summary": []
            }
            
            if kg_insights:
                summary["strategic_implications"] = kg_insights.strategic_patterns[:2]
                summary["recommendations_summary"] = kg_insights.opportunities[:2]
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return {"error": str(e)}
    
    async def _generate_section_content(
        self, 
        section: str, 
        data_structure: Dict[str, Any], 
        query_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate content for a specific section."""
        try:
            # Generate content based on section type
            if section == "executive_summary":
                return await self._generate_executive_summary(
                    data_structure, query_results, None
                )
            elif section == "analysis":
                return {
                    "analysis_type": "comprehensive",
                    "findings": query_results.get("findings", []),
                    "insights": query_results.get("insights", [])
                }
            elif section == "recommendations":
                return {
                    "recommendations": query_results.get("recommendations", []),
                    "priority_levels": ["high", "medium", "low"]
                }
            else:
                return {
                    "content": f"Content for {section} section",
                    "data": query_results.get(section, {})
                }
                
        except Exception as e:
            logger.error(f"Error generating section content: {e}")
            return {"error": str(e)}
    
    async def _generate_executive_summary(
        self, 
        data_structure: Dict[str, Any], 
        query_results: Dict[str, Any],
        kg_insights: Optional[StrategicIntelligence]
    ) -> Dict[str, Any]:
        """Generate executive summary for the report."""
        try:
            summary = {
                "overview": "Comprehensive analysis report with strategic insights",
                "key_findings": query_results.get("findings", [])[:3],
                "strategic_implications": [],
                "recommendations_summary": []
            }
            
            if kg_insights:
                summary["strategic_implications"] = kg_insights.strategic_patterns[:2]
                summary["recommendations_summary"] = kg_insights.opportunities[:2]
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return {"error": str(e)}
