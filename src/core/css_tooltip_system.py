"""
CSS Tooltip System

Pure CSS tooltip implementation with no JavaScript dependencies.
Replaces JavaScript tooltips with CSS :hover pseudo-classes for offline compatibility.

Features:
- CSS-only tooltips using :hover
- Multiple tooltip styles and positions
- Responsive design
- Offline viewing capability
- Fast performance
"""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class TooltipStyle:
    """Configuration for tooltip styling."""
    position: str = "top"  # top, bottom, left, right
    background_color: str = "#333"
    text_color: str = "#fff"
    border_radius: str = "4px"
    padding: str = "8px 12px"
    font_size: str = "14px"
    max_width: str = "300px"
    box_shadow: str = "0 2px 8px rgba(0,0,0,0.3)"
    z_index: str = "1000"
    opacity: str = "0"
    transition: str = "opacity 0.3s ease"


@dataclass
class TooltipData:
    """Data structure for tooltip content."""
    title: str
    description: str
    source: str = ""
    strategic_impact: str = ""
    recommendations: str = ""
    use_cases: str = ""
    confidence: str = ""
    style: Optional[TooltipStyle] = None


class CSSTooltipSystem:
    """CSS-only tooltip system with no JavaScript dependencies."""
    
    def __init__(self):
        """Initialize the CSS tooltip system."""
        self.tooltip_counter = 0
        self.generated_css = ""
        self.tooltip_styles = {
            'default': TooltipStyle(),
            'info': TooltipStyle(
                background_color="#3498db",
                text_color="#fff"
            ),
            'warning': TooltipStyle(
                background_color="#f39c12",
                text_color="#fff"
            ),
            'success': TooltipStyle(
                background_color="#27ae60",
                text_color="#fff"
            ),
            'error': TooltipStyle(
                background_color="#e74c3c",
                text_color="#fff"
            ),
            'dark': TooltipStyle(
                background_color="#2c3e50",
                text_color="#ecf0f1"
            )
        }
        
        logger.info("✅ CSS Tooltip System initialized successfully")
    
    def add_tooltip_style(self, name: str, style: TooltipStyle):
        """Add a custom tooltip style."""
        self.tooltip_styles[name] = style
        logger.info(f"✅ Added custom tooltip style: {name}")
    
    def generate_css(self, modules_data: List[Dict[str, Any]]) -> str:
        """Generate CSS for all tooltips in the modules.
        
        Args:
            modules_data: List of processed module data
            
        Returns:
            CSS string for all tooltips
        """
        css_parts = []
        
        # Base tooltip styles
        css_parts.append(self.generate_base_css())
        
        # Generate CSS for each module's tooltips
        for module in modules_data:
            if module.get('tooltip_data'):
                module_css = self.generate_module_tooltip_css(module)
                css_parts.append(module_css)
        
        # Combine all CSS
        self.generated_css = "\n".join(css_parts)
        logger.info(f"✅ Generated CSS for {len(modules_data)} modules")
        
        return self.generated_css
    
    def generate_base_css(self) -> str:
        """Generate base CSS for tooltip functionality."""
        return """
        /* CSS Tooltip System - Pure CSS Implementation */
        
        /* Tooltip container */
        .tooltip-container {
            position: relative;
            display: inline-block;
            cursor: help;
        }
        
        /* Tooltip content */
        .tooltip-content {
            position: absolute;
            visibility: hidden;
            opacity: 0;
            background-color: #333;
            color: #fff;
            text-align: left;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 14px;
            line-height: 1.4;
            max-width: 300px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            z-index: 1000;
            transition: opacity 0.3s ease, visibility 0.3s ease;
            white-space: normal;
            word-wrap: break-word;
        }
        
        /* Tooltip arrow */
        .tooltip-content::after {
            content: "";
            position: absolute;
            border: 5px solid transparent;
        }
        
        /* Show tooltip on hover */
        .tooltip-container:hover .tooltip-content {
            visibility: visible;
            opacity: 1;
        }
        
        /* Position variants */
        .tooltip-top .tooltip-content {
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
        }
        
        .tooltip-top .tooltip-content::after {
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border-top-color: #333;
        }
        
        .tooltip-bottom .tooltip-content {
            top: 125%;
            left: 50%;
            transform: translateX(-50%);
        }
        
        .tooltip-bottom .tooltip-content::after {
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            border-bottom-color: #333;
        }
        
        .tooltip-left .tooltip-content {
            right: 125%;
            top: 50%;
            transform: translateY(-50%);
        }
        
        .tooltip-left .tooltip-content::after {
            left: 100%;
            top: 50%;
            transform: translateY(-50%);
            border-left-color: #333;
        }
        
        .tooltip-right .tooltip-content {
            left: 125%;
            top: 50%;
            transform: translateY(-50%);
        }
        
        .tooltip-right .tooltip-content::after {
            right: 100%;
            top: 50%;
            transform: translateY(-50%);
            border-right-color: #333;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .tooltip-content {
                max-width: 250px;
                font-size: 13px;
                padding: 6px 10px;
            }
            
            .tooltip-left .tooltip-content,
            .tooltip-right .tooltip-content {
                display: none;
            }
        }
        
        /* Tooltip content styling */
        .tooltip-title {
            font-weight: bold;
            margin-bottom: 5px;
            color: #fff;
        }
        
        .tooltip-description {
            margin-bottom: 8px;
        }
        
        .tooltip-source {
            font-size: 12px;
            color: #ccc;
            font-style: italic;
            margin-bottom: 5px;
        }
        
        .tooltip-strategic {
            font-size: 12px;
            color: #ffd700;
            margin-bottom: 5px;
        }
        
        .tooltip-recommendations {
            font-size: 12px;
            color: #90ee90;
            margin-bottom: 5px;
        }
        
        .tooltip-use-cases {
            font-size: 12px;
            color: #87ceeb;
            margin-bottom: 5px;
        }
        
        .tooltip-confidence {
            font-size: 11px;
            color: #ffa500;
            text-align: right;
        }
        """
    
    def generate_module_tooltip_css(self, module_id: str, tooltips: List[Dict[str, Any]]) -> str:
        """Generate CSS for a specific module's tooltips."""
        if not tooltips:
            return ""
        
        css_parts = []
        css_parts.append(f"/* CSS for {module_id} module tooltips */")
        
        for i, tooltip in enumerate(tooltips):
            tooltip_id = tooltip.get('id', f"{module_id}_tooltip_{i}")
            css_parts.append(self._generate_tooltip_css(tooltip_id, tooltip))
        
        return "\n".join(css_parts)
    
    def _generate_tooltip_css(self, tooltip_id: str, tooltip: Dict[str, Any]) -> str:
        """Generate CSS for a single tooltip."""
        css_class = f"tooltip-{tooltip_id.replace('_', '-')}"
        return f"""
        /* Tooltip: {tooltip_id} */
        .{css_class} {{
            position: relative;
            display: inline-block;
        }}
        
        .{css_class} .tooltip-content {{
            visibility: hidden;
            background-color: #333;
            color: #fff;
            text-align: center;
            border-radius: 4px;
            padding: 8px 12px;
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            margin-left: -60px;
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .{css_class}:hover .tooltip-content {{
            visibility: visible;
            opacity: 1;
        }}
        """
    
    def _generate_single_tooltip_css(self, css_class: str, tooltip_info: Dict[str, Any], style: TooltipStyle) -> str:
        """Generate CSS for a single tooltip."""
        # Determine position
        position = tooltip_info.get('position', style.position)
        
        # Generate CSS
        css = f"""
        /* Tooltip: {css_class} */
        .{css_class} .tooltip-content {{
            background-color: {style.background_color};
            color: {style.text_color};
            border-radius: {style.border_radius};
            padding: {style.padding};
            font-size: {style.font_size};
            max-width: {style.max_width};
            box-shadow: {style.box_shadow};
            z-index: {style.z_index};
            opacity: {style.opacity};
            transition: {style.transition};
        }}
        
        .{css_class}.tooltip-{position} .tooltip-content::after {{
            border-{position}-color: {style.background_color};
        }}
        """
        
        return css
    
    def create_tooltip_html(self, tooltip_id: str, tooltip_data: TooltipData, trigger_text: str) -> str:
        """Create HTML for a tooltip element.
        
        Args:
            tooltip_id: Unique identifier for the tooltip
            tooltip_data: Tooltip content data
            trigger_text: Text that triggers the tooltip
            
        Returns:
            HTML string for the tooltip
        """
        # Determine position
        position = tooltip_data.style.position if tooltip_data.style else "top"
        
        # Build tooltip content
        content_parts = []
        
        if tooltip_data.title:
            content_parts.append(f'<div class="tooltip-title">{tooltip_data.title}</div>')
        
        if tooltip_data.description:
            content_parts.append(f'<div class="tooltip-description">{tooltip_data.description}</div>')
        
        if tooltip_data.source:
            content_parts.append(f'<div class="tooltip-source">Source: {tooltip_data.source}</div>')
        
        if tooltip_data.strategic_impact:
            content_parts.append(f'<div class="tooltip-strategic">Strategic Impact: {tooltip_data.strategic_impact}</div>')
        
        if tooltip_data.recommendations:
            content_parts.append(f'<div class="tooltip-recommendations">Recommendations: {tooltip_data.recommendations}</div>')
        
        if tooltip_data.use_cases:
            content_parts.append(f'<div class="tooltip-use-cases">Use Cases: {tooltip_data.use_cases}</div>')
        
        if tooltip_data.confidence:
            content_parts.append(f'<div class="tooltip-confidence">Confidence: {tooltip_data.confidence}</div>')
        
        tooltip_content = "".join(content_parts)
        
        # Generate HTML
        html = f"""
        <span class="tooltip-container tooltip-{position}" id="{tooltip_id}">
            {trigger_text}
            <div class="tooltip-content">
                {tooltip_content}
            </div>
        </span>
        """
        
        return html
    
    def create_simple_tooltip_html(self, text: str, tooltip_text: str, position: str = "top") -> str:
        """Create a simple tooltip HTML element.
        
        Args:
            text: Text that triggers the tooltip
            tooltip_text: Tooltip content
            position: Tooltip position (top, bottom, left, right)
            
        Returns:
            HTML string for the simple tooltip
        """
        return f"""
        <span class="tooltip-container tooltip-{position}">
            {text}
            <div class="tooltip-content">
                {tooltip_text}
            </div>
        </span>
        """
    
    def get_tooltip_styles_info(self) -> Dict[str, Any]:
        """Get information about available tooltip styles."""
        return {
            'available_styles': list(self.tooltip_styles.keys()),
            'default_style': 'default',
            'features': [
                'CSS-only implementation',
                'No JavaScript required',
                'Responsive design',
                'Multiple positions',
                'Customizable styles',
                'Offline compatible'
            ]
        }
    
    def validate_tooltip_data(self, tooltip_data: Dict[str, Any]) -> bool:
        """Validate tooltip data structure."""
        required_fields = ['title', 'description']
        
        for field in required_fields:
            if field not in tooltip_data:
                logger.warning(f"Missing required tooltip field: {field}")
                return False
        
        return True
    
    def sanitize_tooltip_content(self, content: str) -> str:
        """Sanitize tooltip content for safe HTML rendering."""
        # Remove potentially dangerous HTML
        content = re.sub(r'<script.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
        content = re.sub(r'<.*?>', '', content)  # Remove all HTML tags
        
        # Escape special characters
        content = content.replace('&', '&amp;')
        content = content.replace('<', '&lt;')
        content = content.replace('>', '&gt;')
        content = content.replace('"', '&quot;')
        content = content.replace("'", '&#39;')
        
        return content


# Convenience functions for quick tooltip creation
def create_info_tooltip(text: str, info: str) -> str:
    """Create an info tooltip."""
    tooltip_system = CSSTooltipSystem()
    return tooltip_system.create_simple_tooltip_html(text, info, "top")


def create_warning_tooltip(text: str, warning: str) -> str:
    """Create a warning tooltip."""
    tooltip_system = CSSTooltipSystem()
    return tooltip_system.create_simple_tooltip_html(text, warning, "top")


def create_help_tooltip(text: str, help_text: str) -> str:
    """Create a help tooltip."""
    tooltip_system = CSSTooltipSystem()
    return tooltip_system.create_simple_tooltip_html(text, help_text, "top")


if __name__ == "__main__":
    # Example usage
    tooltip_system = CSSTooltipSystem()
    
    # Create sample tooltip data
    sample_tooltip = TooltipData(
        title="Strategic Analysis",
        description="This analysis provides insights into strategic positioning.",
        source="DIA3 Analysis Engine",
        strategic_impact="High impact on decision making",
        recommendations="Consider implementing recommended actions",
        confidence="85%"
    )
    
    # Generate tooltip HTML
    html = tooltip_system.create_tooltip_html("sample-tooltip", sample_tooltip, "Strategic Analysis")
    print("Generated tooltip HTML:")
    print(html)
    
    # Generate CSS
    modules_data = [{
        'id': 'sample_module',
        'tooltip_data': {
            'sample_tooltip': {
                'title': 'Strategic Analysis',
                'description': 'This analysis provides insights into strategic positioning.',
                'position': 'top'
            }
        }
    }]
    
    css = tooltip_system.generate_css(modules_data)
    print("\nGenerated CSS:")
    print(css)
