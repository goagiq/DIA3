#!/usr/bin/env python3
"""
Template Configuration
Defines paths and configurations for report templates.
"""

from pathlib import Path


class TemplateConfig:
    """Configuration for report templates."""
    
    # Base directories
    RESULTS_DIR = Path("Results")
    TEMPLATES_DIR = RESULTS_DIR / "templates"
    
    # Template file paths
    ENHANCED_REPORT_TEMPLATE = (
        TEMPLATES_DIR / "Pakistan_Submarine_Analysis_Enhanced_Report.html"
    )
    LEADERSHIP_TEMPLATE = (
        TEMPLATES_DIR / "Pakistan_Submarine_Leadership_Report.html"
    )
    
    @classmethod
    def get_template_path(cls, template_name: str) -> Path:
        """Get the path to a specific template."""
        template_map = {
            "enhanced_report": cls.ENHANCED_REPORT_TEMPLATE,
            "leadership": cls.LEADERSHIP_TEMPLATE,
            "default": cls.ENHANCED_REPORT_TEMPLATE
        }
        
        return template_map.get(template_name, template_map["default"])
    
    @classmethod
    def template_exists(cls, template_name: str) -> bool:
        """Check if a template exists."""
        template_path = cls.get_template_path(template_name)
        return template_path.exists()
    
    @classmethod
    def list_available_templates(cls) -> list:
        """List all available templates."""
        available = []
        if cls.ENHANCED_REPORT_TEMPLATE.exists():
            available.append("enhanced_report")
        if cls.LEADERSHIP_TEMPLATE.exists():
            available.append("leadership")
        return available
    
    @classmethod
    def get_template_content(cls, template_name: str) -> str:
        """Get the content of a template file."""
        template_path = cls.get_template_path(template_name)
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
