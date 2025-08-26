#!/usr/bin/env python3
"""
Advanced Tooltip System with Source Tracking
Provides comprehensive tooltips with multiple sources and DIA3- prefix tracking.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class TooltipSource:
    """Information about a tooltip source."""
    name: str
    description: str
    source_type: str  # "internal", "external", "analysis", "intelligence"
    confidence_score: float  # 0.0 to 1.0
    timestamp: str
    metadata: Dict[str, Any]
    data_category: str = ""  # Category of data (e.g., "geopolitical", "economic", "security")
    intelligence_level: str = ""  # Level of intelligence analysis required


@dataclass
class AdvancedTooltip:
    """Advanced tooltip with comprehensive information."""
    id: str
    title: str
    description: str
    detailed_explanation: str
    sources: List[TooltipSource]
    category: str
    priority: int
    created_at: str
    updated_at: str


class AdvancedTooltipSystem:
    """Advanced tooltip system with comprehensive source tracking."""
    
    def __init__(self):
        self.tooltips = {}
        self.source_registry = {}
        self.internal_sources = set()
        
    def create_tooltip(
        self,
        title: str,
        description: str,
        detailed_explanation: str,
        category: str,
        sources: List[Dict[str, Any]],
        priority: int = 3
    ) -> AdvancedTooltip:
        """
        Create an advanced tooltip with comprehensive information.
        
        Args:
            title: Tooltip title
            description: Brief description
            detailed_explanation: Comprehensive explanation
            category: Tooltip category
            sources: List of source dictionaries
            priority: Priority level (1-5)
            
        Returns:
            AdvancedTooltip object
        """
        try:
            tooltip_id = self._generate_tooltip_id(title, category)
            
            # Process sources
            processed_sources = []
            for source_data in sources:
                source = self._create_source_from_dict(source_data)
                processed_sources.append(source)
                
                # Track internal sources
                if source.source_type == "internal":
                    self.internal_sources.add(source.name)
            
            # Create tooltip
            tooltip = AdvancedTooltip(
                id=tooltip_id,
                title=title,
                description=description,
                detailed_explanation=detailed_explanation,
                sources=processed_sources,
                category=category,
                priority=priority,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            
            self.tooltips[tooltip_id] = tooltip
            return tooltip
            
        except Exception as e:
            logger.error(f"Error creating tooltip: {e}")
            raise
    
    def _create_source_from_dict(self, source_data: Dict[str, Any]) -> TooltipSource:
        """Create a TooltipSource from a dictionary."""
        # Add DIA3- prefix for internal sources
        name = source_data.get("name", "")
        source_type = source_data.get("source_type", "external")
        
        if source_type == "internal" and not name.startswith("DIA3-"):
            name = f"DIA3-{name}"
        
        return TooltipSource(
            name=name,
            description=source_data.get("description", ""),
            source_type=source_type,
            confidence_score=source_data.get("confidence_score", 0.5),
            timestamp=source_data.get("timestamp", datetime.now().isoformat()),
            metadata=source_data.get("metadata", {})
        )
    
    def _generate_tooltip_id(self, title: str, category: str) -> str:
        """Generate a unique tooltip ID."""
        import hashlib
        combined = f"{title}_{category}_{datetime.now().isoformat()}"
        return hashlib.md5(combined.encode()).hexdigest()[:12]
    
    def get_tooltip(self, tooltip_id: str) -> Optional[AdvancedTooltip]:
        """Get a tooltip by ID."""
        return self.tooltips.get(tooltip_id)
    
    def get_tooltips_by_category(self, category: str) -> List[AdvancedTooltip]:
        """Get all tooltips for a specific category."""
        return [
            tooltip for tooltip in self.tooltips.values()
            if tooltip.category == category
        ]
    
    def create_category_tooltip(
        self,
        category_name: str,
        category_description: str,
        analysis_methods: List[str],
        data_sources: List[str],
        confidence_level: str
    ) -> AdvancedTooltip:
        """Create a tooltip for a report category."""
        
        # Create comprehensive explanation
        detailed_explanation = f"""
        <strong>Category Analysis:</strong> {category_name}
        
        <strong>Description:</strong> {category_description}
        
        <strong>Analysis Methods:</strong>
        <ul>
        {''.join([f'<li>{method}</li>' for method in analysis_methods])}
        </ul>
        
        <strong>Data Sources:</strong>
        <ul>
        {''.join([f'<li>{source}</li>' for source in data_sources])}
        </ul>
        
        <strong>Confidence Level:</strong> {confidence_level}
        
        <strong>Last Updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        # Create sources
        sources = [
            {
                "name": "DIA3-CategoryDetector",
                "description": "Automated category detection and analysis",
                "source_type": "internal",
                "confidence_score": 0.8,
                "metadata": {
                    "detection_method": "keyword_analysis",
                    "analysis_timestamp": datetime.now().isoformat()
                }
            },
            {
                "name": "DIA3-ContentAnalyzer",
                "description": "Content analysis and relevance scoring",
                "source_type": "internal",
                "confidence_score": 0.7,
                "metadata": {
                    "analysis_type": "semantic_analysis",
                    "processing_timestamp": datetime.now().isoformat()
                }
            }
        ]
        
        return self.create_tooltip(
            title=f"{category_name} Analysis",
            description=category_description,
            detailed_explanation=detailed_explanation,
            category="category_analysis",
            sources=sources,
            priority=2
        )
    
    def create_analysis_tooltip(
        self,
        analysis_type: str,
        analysis_description: str,
        methodology: str,
        results_summary: str,
        confidence_score: float,
        data_sources: List[str]
    ) -> AdvancedTooltip:
        """Create a tooltip for analysis results."""
        
        detailed_explanation = f"""
        <strong>Analysis Type:</strong> {analysis_type}
        
        <strong>Description:</strong> {analysis_description}
        
        <strong>Methodology:</strong>
        {methodology}
        
        <strong>Results Summary:</strong>
        {results_summary}
        
        <strong>Confidence Score:</strong> {confidence_score:.2f}
        
        <strong>Data Sources:</strong>
        <ul>
        {''.join([f'<li>{source}</li>' for source in data_sources])}
        </ul>
        
        <strong>Analysis Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        sources = [
            {
                "name": f"DIA3-{analysis_type.replace('_', '').title()}Analyzer",
                "description": f"Automated {analysis_type} analysis",
                "source_type": "internal",
                "confidence_score": confidence_score,
                "metadata": {
                    "analysis_type": analysis_type,
                    "methodology": methodology,
                    "timestamp": datetime.now().isoformat()
                }
            }
        ]
        
        return self.create_tooltip(
            title=f"{analysis_type.replace('_', ' ').title()} Analysis",
            description=analysis_description,
            detailed_explanation=detailed_explanation,
            category="analysis_results",
            sources=sources,
            priority=2
        )
    
    def generate_html_tooltip(self, tooltip: AdvancedTooltip) -> str:
        """Generate HTML for a tooltip."""
        sources_html = ""
        for source in tooltip.sources:
            source_class = "source-internal" if source.source_type == "internal" else "source-external"
            sources_html += f"""
            <div class="tooltip-source {source_class}">
                <strong>{source.name}</strong>
                <p>{source.description}</p>
                <small>Confidence: {source.confidence_score:.2f}</small>
            </div>
            """
        
        return f"""
        <div class="advanced-tooltip" data-tooltip-id="{tooltip.id}">
            <div class="tooltip-header">
                <h4>{tooltip.title}</h4>
                <span class="tooltip-category">{tooltip.category}</span>
            </div>
            <div class="tooltip-content">
                <p class="tooltip-description">{tooltip.description}</p>
                <div class="tooltip-detailed">
                    {tooltip.detailed_explanation}
                </div>
            </div>
            <div class="tooltip-sources">
                <h5>Sources:</h5>
                {sources_html}
            </div>
            <div class="tooltip-footer">
                <small>Updated: {tooltip.updated_at}</small>
            </div>
        </div>
        """
    
    def generate_css_styles(self) -> str:
        """Generate CSS styles for tooltips."""
        return """
        .advanced-tooltip {
            background: rgba(255, 255, 255, 0.98);
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            max-width: 400px;
            font-size: 14px;
            line-height: 1.4;
        }
        
        .tooltip-header {
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }
        
        .tooltip-header h4 {
            margin: 0;
            color: #2c3e50;
            font-size: 16px;
        }
        
        .tooltip-category {
            background: #3498db;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            text-transform: uppercase;
        }
        
        .tooltip-description {
            font-weight: 500;
            color: #34495e;
            margin-bottom: 10px;
        }
        
        .tooltip-detailed {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        
        .tooltip-detailed ul {
            margin: 5px 0;
            padding-left: 20px;
        }
        
        .tooltip-sources {
            border-top: 1px solid #eee;
            padding-top: 10px;
        }
        
        .tooltip-sources h5 {
            margin: 0 0 8px 0;
            color: #2c3e50;
            font-size: 13px;
        }
        
        .tooltip-source {
            margin-bottom: 8px;
            padding: 8px;
            border-radius: 4px;
            border-left: 3px solid;
        }
        
        .tooltip-source.source-internal {
            background: #e8f5e8;
            border-left-color: #27ae60;
        }
        
        .tooltip-source.source-external {
            background: #fff3cd;
            border-left-color: #f39c12;
        }
        
        .tooltip-source strong {
            color: #2c3e50;
            font-size: 12px;
        }
        
        .tooltip-source p {
            margin: 4px 0;
            font-size: 11px;
            color: #555;
        }
        
        .tooltip-source small {
            color: #7f8c8d;
            font-size: 10px;
        }
        
        .tooltip-footer {
            text-align: right;
            margin-top: 10px;
            padding-top: 8px;
            border-top: 1px solid #eee;
        }
        
        .tooltip-footer small {
            color: #95a5a6;
            font-size: 10px;
        }
        """
    
    def export_tooltips(self, output_path: str) -> Dict[str, Any]:
        """Export all tooltips to a file."""
        try:
            export_data = {
                "tooltips": {},
                "metadata": {
                    "export_timestamp": datetime.now().isoformat(),
                    "total_tooltips": len(self.tooltips),
                    "internal_sources": list(self.internal_sources)
                }
            }
            
            for tooltip_id, tooltip in self.tooltips.items():
                export_data["tooltips"][tooltip_id] = asdict(tooltip)
            
            # Save to file
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return {
                "success": True,
                "output_path": str(output_file),
                "total_tooltips": len(self.tooltips)
            }
            
        except Exception as e:
            logger.error(f"Error exporting tooltips: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_intelligence_tooltip(
        self,
        title: str,
        description: str,
        detailed_explanation: str,
        category: str,
        intelligence_sources: List[str],
        external_sources: List[str] = None,
        priority: int = 1
    ) -> AdvancedTooltip:
        """
        Create a tooltip specifically for DIA3 intelligence synthesis.
        
        Args:
            title: Tooltip title
            description: Brief description
            detailed_explanation: Comprehensive intelligence analysis
            category: Intelligence category
            intelligence_sources: List of DIA3 intelligence sources
            external_sources: List of external sources
            priority: Priority level (1-5)
            
        Returns:
            AdvancedTooltip object with intelligence sources
        """
        try:
            # Create intelligence sources
            sources = []
            
            # Add DIA3 intelligence sources
            for source_name in intelligence_sources:
                if not source_name.startswith("DIA3 - "):
                    source_name = f"DIA3 - {source_name}"
                
                source = TooltipSource(
                    name=source_name,
                    description=f"Intelligence analysis from {source_name}",
                    source_type="intelligence",
                    confidence_score=0.95,
                    timestamp=datetime.now().isoformat(),
                    metadata={
                        "intelligence_level": "strategic",
                        "analysis_type": "synthesis",
                        "source_category": category
                    },
                    data_category=category,
                    intelligence_level="strategic"
                )
                sources.append(source)
            
            # Add external sources if provided
            if external_sources:
                for source_name in external_sources:
                    source = TooltipSource(
                        name=source_name,
                        description=f"External source: {source_name}",
                        source_type="external",
                        confidence_score=0.8,
                        timestamp=datetime.now().isoformat(),
                        metadata={
                            "source_type": "external",
                            "verification_status": "verified"
                        },
                        data_category=category,
                        intelligence_level="supporting"
                    )
                    sources.append(source)
            
            return self.create_tooltip(
                title=title,
                description=description,
                detailed_explanation=detailed_explanation,
                category=category,
                sources=sources,
                priority=priority
            )
            
        except Exception as e:
            logger.error(f"Error creating intelligence tooltip: {e}")
            return None
    
    def get_intelligence_sources(self) -> List[str]:
        """Get all DIA3 intelligence sources used in tooltips."""
        intelligence_sources = set()
        
        for tooltip in self.tooltips.values():
            for source in tooltip.sources:
                if source.source_type == "intelligence" and source.name.startswith("DIA3 - "):
                    intelligence_sources.add(source.name)
        
        return list(intelligence_sources)
    
    def get_category_data_sources(self, category: str) -> Dict[str, List[str]]:
        """Get data sources for a specific category."""
        internal_sources = set()
        external_sources = set()
        intelligence_sources = set()
        
        for tooltip in self.tooltips.values():
            if tooltip.category == category:
                for source in tooltip.sources:
                    if source.source_type == "internal":
                        internal_sources.add(source.name)
                    elif source.source_type == "external":
                        external_sources.add(source.name)
                    elif source.source_type == "intelligence":
                        intelligence_sources.add(source.name)
        
        return {
            "internal": list(internal_sources),
            "external": list(external_sources),
            "intelligence": list(intelligence_sources)
        }
