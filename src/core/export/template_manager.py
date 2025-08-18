"""
Template Manager

Provides both pre-defined and customizable templates for PDF and Word document generation.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class TemplateConfig:
    """Template configuration."""
    name: str
    description: str
    category: str
    pdf_styles: Dict[str, Any]
    word_styles: Dict[str, Any]
    metadata: Dict[str, Any]


class TemplateManager:
    """Manages document templates for PDF and Word generation."""
    
    def __init__(self, templates_dir: str = "templates"):
        """Initialize template manager.
        
        Args:
            templates_dir: Directory containing template files
        """
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self._load_predefined_templates()
    
    def _load_predefined_templates(self):
        """Load pre-defined templates."""
        self.predefined_templates = {
            "executive_summary": self._create_executive_summary_template(),
            "technical_report": self._create_technical_report_template(),
            "business_report": self._create_business_report_template(),
            "academic_paper": self._create_academic_paper_template(),
            "whitepaper": self._create_whitepaper_template()
        }
    
    def _create_executive_summary_template(self) -> TemplateConfig:
        """Create executive summary template."""
        return TemplateConfig(
            name="Executive Summary",
            description="Professional template for executive summaries",
            category="business",
            pdf_styles={
                "page_size": "A4",
                "margins": {"top": 1, "bottom": 1, "left": 1, "right": 1},
                "header": {
                    "font": "Helvetica-Bold",
                    "font_size": 12,
                    "color": "#2c3e50",
                    "alignment": "center"
                },
                "title": {
                    "font": "Helvetica-Bold",
                    "font_size": 18,
                    "color": "#2c3e50",
                    "alignment": "center",
                    "spacing": 20
                },
                "heading1": {
                    "font": "Helvetica-Bold",
                    "font_size": 16,
                    "color": "#34495e",
                    "spacing": 15
                },
                "heading2": {
                    "font": "Helvetica-Bold",
                    "font_size": 14,
                    "color": "#34495e",
                    "spacing": 12
                },
                "body": {
                    "font": "Helvetica",
                    "font_size": 11,
                    "color": "#2c3e50",
                    "line_spacing": 1.2
                }
            },
            word_styles={
                "title_style": "Title",
                "heading1_style": "Heading 1",
                "heading2_style": "Heading 2",
                "body_style": "Normal",
                "font_family": "Calibri",
                "font_size": 11
            },
            metadata={
                "author": "DIA3 System",
                "subject": "Executive Summary",
                "keywords": ["executive", "summary", "business"]
            }
        )
    
    def _create_technical_report_template(self) -> TemplateConfig:
        """Create technical report template."""
        return TemplateConfig(
            name="Technical Report",
            description="Comprehensive template for technical documentation",
            category="technical",
            pdf_styles={
                "page_size": "A4",
                "margins": {"top": 1, "bottom": 1, "left": 1, "right": 1},
                "header": {
                    "font": "Courier-Bold",
                    "font_size": 10,
                    "color": "#2c3e50",
                    "alignment": "right"
                },
                "title": {
                    "font": "Helvetica-Bold",
                    "font_size": 20,
                    "color": "#2c3e50",
                    "alignment": "center",
                    "spacing": 25
                },
                "heading1": {
                    "font": "Helvetica-Bold",
                    "font_size": 16,
                    "color": "#34495e",
                    "spacing": 18
                },
                "heading2": {
                    "font": "Helvetica-Bold",
                    "font_size": 14,
                    "color": "#34495e",
                    "spacing": 15
                },
                "body": {
                    "font": "Helvetica",
                    "font_size": 10,
                    "color": "#2c3e50",
                    "line_spacing": 1.3
                },
                "code": {
                    "font": "Courier",
                    "font_size": 9,
                    "color": "#2c3e50",
                    "background": "#f8f9fa"
                }
            },
            word_styles={
                "title_style": "Title",
                "heading1_style": "Heading 1",
                "heading2_style": "Heading 2",
                "body_style": "Normal",
                "code_style": "Code",
                "font_family": "Consolas",
                "font_size": 10
            },
            metadata={
                "author": "DIA3 System",
                "subject": "Technical Report",
                "keywords": ["technical", "documentation", "report"]
            }
        )
    
    def _create_business_report_template(self) -> TemplateConfig:
        """Create business report template."""
        return TemplateConfig(
            name="Business Report",
            description="Professional template for business reports",
            category="business",
            pdf_styles={
                "page_size": "A4",
                "margins": {"top": 1, "bottom": 1, "left": 1, "right": 1},
                "header": {
                    "font": "Helvetica-Bold",
                    "font_size": 11,
                    "color": "#2c3e50",
                    "alignment": "center"
                },
                "title": {
                    "font": "Helvetica-Bold",
                    "font_size": 18,
                    "color": "#2c3e50",
                    "alignment": "center",
                    "spacing": 20
                },
                "heading1": {
                    "font": "Helvetica-Bold",
                    "font_size": 16,
                    "color": "#34495e",
                    "spacing": 15
                },
                "heading2": {
                    "font": "Helvetica-Bold",
                    "font_size": 14,
                    "color": "#34495e",
                    "spacing": 12
                },
                "body": {
                    "font": "Helvetica",
                    "font_size": 11,
                    "color": "#2c3e50",
                    "line_spacing": 1.4
                },
                "table": {
                    "header_font": "Helvetica-Bold",
                    "header_font_size": 10,
                    "cell_font": "Helvetica",
                    "cell_font_size": 9,
                    "border_color": "#bdc3c7"
                }
            },
            word_styles={
                "title_style": "Title",
                "heading1_style": "Heading 1",
                "heading2_style": "Heading 2",
                "body_style": "Normal",
                "table_style": "Table Grid",
                "font_family": "Calibri",
                "font_size": 11
            },
            metadata={
                "author": "DIA3 System",
                "subject": "Business Report",
                "keywords": ["business", "report", "analysis"]
            }
        )
    
    def _create_academic_paper_template(self) -> TemplateConfig:
        """Create academic paper template."""
        return TemplateConfig(
            name="Academic Paper",
            description="Formal template for academic papers",
            category="academic",
            pdf_styles={
                "page_size": "A4",
                "margins": {"top": 1, "bottom": 1, "left": 1.5, "right": 1},
                "header": {
                    "font": "Times-Bold",
                    "font_size": 10,
                    "color": "#2c3e50",
                    "alignment": "center"
                },
                "title": {
                    "font": "Times-Bold",
                    "font_size": 16,
                    "color": "#2c3e50",
                    "alignment": "center",
                    "spacing": 20
                },
                "heading1": {
                    "font": "Times-Bold",
                    "font_size": 14,
                    "color": "#2c3e50",
                    "spacing": 15
                },
                "heading2": {
                    "font": "Times-Bold",
                    "font_size": 12,
                    "color": "#2c3e50",
                    "spacing": 12
                },
                "body": {
                    "font": "Times-Roman",
                    "font_size": 11,
                    "color": "#2c3e50",
                    "line_spacing": 2.0
                },
                "abstract": {
                    "font": "Times-Italic",
                    "font_size": 10,
                    "color": "#2c3e50",
                    "indent": 0.5
                }
            },
            word_styles={
                "title_style": "Title",
                "heading1_style": "Heading 1",
                "heading2_style": "Heading 2",
                "body_style": "Normal",
                "abstract_style": "Quote",
                "font_family": "Times New Roman",
                "font_size": 11
            },
            metadata={
                "author": "DIA3 System",
                "subject": "Academic Paper",
                "keywords": ["academic", "research", "paper"]
            }
        )
    
    def _create_whitepaper_template(self) -> TemplateConfig:
        """Create whitepaper template."""
        return TemplateConfig(
            name="Whitepaper",
            description="Professional template for whitepapers",
            category="business",
            pdf_styles={
                "page_size": "A4",
                "margins": {"top": 1, "bottom": 1, "left": 1, "right": 1},
                "header": {
                    "font": "Helvetica-Bold",
                    "font_size": 10,
                    "color": "#666",
                    "alignment": "center"
                },
                "title": {
                    "font": "Helvetica-Bold",
                    "font_size": 24,
                    "color": "#2c3e50",
                    "alignment": "center",
                    "spacing": 30
                },
                "heading1": {
                    "font": "Helvetica-Bold",
                    "font_size": 18,
                    "color": "#34495e",
                    "spacing": 20
                },
                "heading2": {
                    "font": "Helvetica-Bold",
                    "font_size": 14,
                    "color": "#34495e",
                    "spacing": 15
                },
                "body": {
                    "font": "Helvetica",
                    "font_size": 12,
                    "color": "#333",
                    "line_spacing": 1.6
                },
                "blockquote": {
                    "font": "Helvetica-Oblique",
                    "font_size": 11,
                    "color": "#555",
                    "indent": 1,
                    "border_left": "#3498db"
                }
            },
            word_styles={
                "title_style": "Title",
                "heading1_style": "Heading 1",
                "heading2_style": "Heading 2",
                "body_style": "Normal",
                "quote_style": "Quote",
                "font_family": "Calibri",
                "font_size": 12
            },
            metadata={
                "author": "DIA3 System",
                "subject": "Whitepaper",
                "keywords": ["whitepaper", "technical", "documentation"]
            }
        )
    
    def get_template(self, template_name: str) -> Optional[TemplateConfig]:
        """Get a template by name.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template configuration or None if not found
        """
        # Check predefined templates first
        if template_name in self.predefined_templates:
            return self.predefined_templates[template_name]
        
        # Check custom templates
        custom_template_path = self.templates_dir / f"{template_name}.json"
        if custom_template_path.exists():
            try:
                with open(custom_template_path, 'r') as f:
                    data = json.load(f)
                return TemplateConfig(**data)
            except Exception as e:
                logger.error(f"Error loading custom template {template_name}: {e}")
                return None
        
        return None
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates.
        
        Returns:
            List of template information
        """
        templates = []
        
        # Add predefined templates
        for name, template in self.predefined_templates.items():
            templates.append({
                "name": name,
                "display_name": template.name,
                "description": template.description,
                "category": template.category,
                "type": "predefined"
            })
        
        # Add custom templates
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r') as f:
                    data = json.load(f)
                templates.append({
                    "name": template_file.stem,
                    "display_name": data.get("name", template_file.stem),
                    "description": data.get("description", ""),
                    "category": data.get("category", "custom"),
                    "type": "custom"
                })
            except Exception as e:
                logger.error(f"Error reading template file {template_file}: {e}")
        
        return templates
    
    def create_custom_template(self, 
                             template_name: str,
                             template_config: TemplateConfig) -> bool:
        """Create a custom template.
        
        Args:
            template_name: Name for the template
            template_config: Template configuration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            template_path = self.templates_dir / f"{template_name}.json"
            
            # Convert to dictionary
            template_dict = {
                "name": template_config.name,
                "description": template_config.description,
                "category": template_config.category,
                "pdf_styles": template_config.pdf_styles,
                "word_styles": template_config.word_styles,
                "metadata": template_config.metadata
            }
            
            with open(template_path, 'w') as f:
                json.dump(template_dict, f, indent=2)
            
            logger.info(f"Created custom template: {template_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating custom template {template_name}: {e}")
            return False
    
    def delete_custom_template(self, template_name: str) -> bool:
        """Delete a custom template.
        
        Args:
            template_name: Name of the template to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            template_path = self.templates_dir / f"{template_name}.json"
            if template_path.exists():
                template_path.unlink()
                logger.info(f"Deleted custom template: {template_name}")
                return True
            else:
                logger.warning(f"Template not found: {template_name}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting custom template {template_name}: {e}")
            return False
