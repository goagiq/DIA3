#!/usr/bin/env python3
"""
Configuration for Comprehensive Enhanced Report Generator
Manages default settings and preferences for report generation.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ComprehensiveReportConfig:
    """Configuration for comprehensive enhanced report generation."""
    
    # Default output settings
    default_output_dir: str = "Results"
    default_template_dir: str = "templates"
    default_format: str = "html"
    
    # Default report settings
    default_title: str = "Comprehensive Analysis Report"
    default_subtitle: str = "Enhanced Analysis with Interactive Visualizations"
    
    # Tooltip settings
    include_tooltips: bool = True
    include_visualizations: bool = True
    
    # Category detection settings
    min_relevance_score: float = 0.1
    max_categories: int = 24
    always_include_categories: List[str] = None
    
    # Source tracking settings
    internal_source_prefix: str = "DIA3-"
    external_source_prefix: str = "External-"
    
    # Data source settings
    enable_data_source_integration: bool = True
    intelligence_synthesis_enabled: bool = True
    external_data_sources_enabled: bool = True
    
    # Intelligence settings
    intelligence_categories: List[str] = None
    intelligence_confidence_threshold: float = 0.8
    intelligence_synthesis_method: str = "DIA3 Intelligence Integration"
    
    # Template settings
    template_name: str = "comprehensive_enhanced_report_template.html"
    
    # Export settings
    export_formats: List[str] = None
    include_metadata: bool = True
    include_timestamps: bool = True
    
    def __post_init__(self):
        """Initialize default values."""
        if self.always_include_categories is None:
            self.always_include_categories = ["executive_summary", "conclusion"]
        
        if self.export_formats is None:
            self.export_formats = ["html", "markdown", "json"]
        
        if self.intelligence_categories is None:
            self.intelligence_categories = [
                "strategic_recommendations",
                "geopolitical_impact_analysis",
                "security_implications",
                "trade_economic_impact"
            ]
    
    def get_output_path(self, filename: str) -> str:
        """Get full output path for a file."""
        return str(Path(self.default_output_dir) / filename)
    
    def get_template_path(self) -> str:
        """Get full template path."""
        return str(Path(self.default_template_dir) / self.template_name)
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate configuration and return any issues."""
        issues = {}
        
        # Check if output directory exists
        output_path = Path(self.default_output_dir)
        if not output_path.exists():
            issues["output_dir"] = f"Output directory does not exist: {self.default_output_dir}"
        
        # Check if template directory exists
        template_path = Path(self.default_template_dir)
        if not template_path.exists():
            issues["template_dir"] = f"Template directory does not exist: {self.default_template_dir}"
        
        # Check if template file exists
        template_file = template_path / self.template_name
        if not template_file.exists():
            issues["template_file"] = f"Template file does not exist: {template_file}"
        
        # Validate relevance score
        if not 0.0 <= self.min_relevance_score <= 1.0:
            issues["min_relevance_score"] = "Min relevance score must be between 0.0 and 1.0"
        
        # Validate max categories
        if self.max_categories < 1:
            issues["max_categories"] = "Max categories must be at least 1"
        
        return issues


# Default configuration instance
default_config = ComprehensiveReportConfig()


# Configuration presets for different use cases
PRESET_CONFIGS = {
    "executive": ComprehensiveReportConfig(
        default_title="Executive Summary Report",
        default_subtitle="High-Level Strategic Analysis",
        max_categories=8,
        always_include_categories=["executive_summary", "strategic_recommendations", "conclusion"],
        include_visualizations=False
    ),
    
    "detailed": ComprehensiveReportConfig(
        default_title="Detailed Analysis Report",
        default_subtitle="Comprehensive Strategic Analysis",
        max_categories=24,
        include_tooltips=True,
        include_visualizations=True
    ),
    
    "technical": ComprehensiveReportConfig(
        default_title="Technical Analysis Report",
        default_subtitle="In-Depth Technical Assessment",
        max_categories=20,
        include_tooltips=True,
        include_visualizations=True,
        export_formats=["html", "json"]
    ),
    
    "strategic": ComprehensiveReportConfig(
        default_title="Strategic Intelligence Report",
        default_subtitle="Strategic Intelligence Analysis",
        max_categories=16,
        always_include_categories=[
            "executive_summary", 
            "geopolitical_impact_analysis",
            "security_implications",
            "strategic_recommendations",
            "conclusion"
        ]
    ),
    
    "economic": ComprehensiveReportConfig(
        default_title="Economic Impact Analysis",
        default_subtitle="Comprehensive Economic Assessment",
        max_categories=12,
        always_include_categories=[
            "executive_summary",
            "trade_economic_impact",
            "economic_implications",
            "financial_implications",
            "strategic_recommendations",
            "conclusion"
        ]
    )
}


def get_config(preset: str = None) -> ComprehensiveReportConfig:
    """Get configuration for a specific preset or default."""
    if preset and preset in PRESET_CONFIGS:
        return PRESET_CONFIGS[preset]
    return default_config


def validate_preset_configs() -> Dict[str, Dict[str, Any]]:
    """Validate all preset configurations."""
    validation_results = {}
    
    for preset_name, config in PRESET_CONFIGS.items():
        validation_results[preset_name] = config.validate_config()
    
    return validation_results


# Category priority mapping for different report types
CATEGORY_PRIORITIES = {
    "executive": {
        "executive_summary": 1,
        "strategic_recommendations": 2,
        "conclusion": 3,
        "geopolitical_impact_analysis": 4,
        "security_implications": 5,
        "economic_implications": 6,
        "risk_assessment": 7,
        "strategic_options_assessment": 8
    },
    
    "strategic": {
        "executive_summary": 1,
        "geopolitical_impact_analysis": 2,
        "security_implications": 3,
        "strategic_options_assessment": 4,
        "strategic_recommendations": 5,
        "risk_assessment": 6,
        "predictive_analysis_insights": 7,
        "advanced_forecasting": 8,
        "conclusion": 9
    },
    
    "economic": {
        "executive_summary": 1,
        "trade_economic_impact": 2,
        "economic_implications": 3,
        "financial_implications": 4,
        "regional_analysis": 5,
        "comparative_analysis": 6,
        "strategic_recommendations": 7,
        "conclusion": 8
    },
    
    "technical": {
        "executive_summary": 1,
        "feature_importance_analysis": 2,
        "capability_forecasts": 3,
        "capability_planning": 4,
        "strategic_use_cases": 5,
        "strategic_development": 6,
        "option_evaluation": 7,
        "conclusion": 8
    }
}


def get_category_priorities(report_type: str) -> Dict[str, int]:
    """Get category priorities for a specific report type."""
    return CATEGORY_PRIORITIES.get(report_type, {})


# Default tooltip settings
DEFAULT_TOOLTIP_SETTINGS = {
    "max_width": "400px",
    "background_color": "rgba(255, 255, 255, 0.98)",
    "border_color": "#3498db",
    "text_color": "#2c3e50",
    "font_size": "14px",
    "line_height": "1.4",
    "padding": "15px",
    "border_radius": "8px",
    "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.15)"
}


# Default visualization settings
DEFAULT_VISUALIZATION_SETTINGS = {
    "chart_colors": ["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6"],
    "chart_height": "400px",
    "chart_width": "100%",
    "animation_duration": "1000ms",
    "responsive": True,
    "interactive": True
}


# Export format configurations
EXPORT_FORMAT_CONFIGS = {
    "html": {
        "include_css": True,
        "include_js": True,
        "minify": False,
        "embed_images": True
    },
    "markdown": {
        "include_metadata": True,
        "include_sources": True,
        "format_sections": True
    },
    "json": {
        "pretty_print": True,
        "include_metadata": True,
        "include_tooltips": True
    },
    "pdf": {
        "page_size": "A4",
        "margins": "1in",
        "include_header": True,
        "include_footer": True
    }
}
