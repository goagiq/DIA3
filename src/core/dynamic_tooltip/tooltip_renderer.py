"""
Tooltip Renderer for Dynamic Tooltips

Handles the visual presentation, positioning, and styling of tooltips
with responsive design and accessibility features.
"""

import re
from typing import Dict, Any, Optional

class TooltipRenderer:
    """Renders tooltip content with styling and positioning."""
    
    def __init__(self, style_config: Dict[str, Any]):
        self.style_config = style_config
    
    def render_html(self, content: str) -> str:
        """Render content as HTML tooltip."""
        if not content:
            return self._render_empty_tooltip()
        
        # Wrap content in styled container
        html = f"""
        <div class="dynamic-tooltip" style="{self._get_tooltip_styles()}">
            {content}
        </div>
        """
        
        return html.strip()
    
    def render_fallback_html(self, object_id: str, object_type: str, error: Optional[str] = None) -> str:
        """Render fallback HTML when content generation fails."""
        content = f"""
        <div class="tooltip-content">
            <h3>{object_id}</h3>
            <p><strong>Type:</strong> {object_type}</p>
        """
        
        if error:
            content += f'<p class="error">Error: {error}</p>'
        
        content += "</div>"
        
        return self.render_html(content)
    
    def _get_tooltip_styles(self) -> str:
        """Get CSS styles for tooltip container."""
        styles = [
            f"max-width: {self.style_config.get('max_width', 400)}px",
            f"max-height: {self.style_config.get('max_height', 300)}px",
            f"background-color: {self.style_config.get('background_color', 'rgba(0, 0, 0, 0.9)')}",
            f"color: {self.style_config.get('text_color', '#ffffff')}",
            f"border-radius: {self.style_config.get('border_radius', 8)}px",
            f"padding: {self.style_config.get('padding', 12)}px",
            f"font-size: {self.style_config.get('font_size', '14px')}",
            f"font-family: {self.style_config.get('font_family', 'Arial, sans-serif')}",
            f"box-shadow: {self.style_config.get('box_shadow', '0 4px 12px rgba(0, 0, 0, 0.3)')}",
            f"z-index: {self.style_config.get('z_index', 1000)}",
            "position: absolute",
            "pointer-events: none",
            "overflow: hidden",
            "word-wrap: break-word",
            "line-height: 1.4"
        ]
        
        return "; ".join(styles)
    
    def _render_empty_tooltip(self) -> str:
        """Render empty tooltip placeholder."""
        return f"""
        <div class="dynamic-tooltip" style="{self._get_tooltip_styles()}">
            <div class="tooltip-content">
                <p>Loading...</p>
            </div>
        </div>
        """.strip()
    
    def get_javascript_code(self) -> str:
        """Get JavaScript code for tooltip positioning and interaction."""
        return """
        class DynamicTooltip {
            constructor() {
                this.tooltip = null;
                this.currentTarget = null;
                this.debounceTimer = null;
                this.debounceDelay = 150;
                this.init();
            }
            
            init() {
                // Create tooltip element
                this.tooltip = document.createElement('div');
                this.tooltip.className = 'dynamic-tooltip';
                this.tooltip.style.display = 'none';
                this.tooltip.style.position = 'fixed';
                this.tooltip.style.zIndex = '10000';
                document.body.appendChild(this.tooltip);
                
                // Add event listeners
                this.addEventListeners();
            }
            
            addEventListeners() {
                // Mouse events for tooltip targets
                document.addEventListener('mouseover', (e) => {
                    if (e.target.hasAttribute('data-tooltip')) {
                        this.handleMouseOver(e);
                    }
                });
                
                document.addEventListener('mouseout', (e) => {
                    if (e.target.hasAttribute('data-tooltip')) {
                        this.handleMouseOut(e);
                    }
                });
                
                // Prevent tooltip from interfering with mouse events
                this.tooltip.addEventListener('mouseenter', () => {
                    this.showTooltip();
                });
                
                this.tooltip.addEventListener('mouseleave', () => {
                    this.hideTooltip();
                });
                
                // Handle window resize
                window.addEventListener('resize', () => {
                    if (this.currentTarget) {
                        this.updatePosition();
                    }
                });
            }
            
            handleMouseOver(event) {
                clearTimeout(this.debounceTimer);
                
                this.debounceTimer = setTimeout(() => {
                    const target = event.target;
                    const tooltipData = this.getTooltipData(target);
                    
                    if (tooltipData) {
                        this.currentTarget = target;
                        this.showTooltip(tooltipData);
                    }
                }, this.debounceDelay);
            }
            
            handleMouseOut(event) {
                clearTimeout(this.debounceTimer);
                this.hideTooltip();
            }
            
            getTooltipData(element) {
                const tooltipAttr = element.getAttribute('data-tooltip');
                if (!tooltipAttr) return null;
                
                try {
                    return JSON.parse(tooltipAttr);
                } catch (e) {
                    return {
                        id: tooltipAttr,
                        type: 'unknown',
                        content: tooltipAttr
                    };
                }
            }
            
            async showTooltip(data) {
                try {
                    // Fetch tooltip content
                    const content = await this.fetchTooltipContent(data);
                    
                    if (content) {
                        this.tooltip.innerHTML = content;
                        this.tooltip.style.display = 'block';
                        this.updatePosition();
                    }
                } catch (error) {
                    console.error('Error showing tooltip:', error);
                    this.showFallbackTooltip(data);
                }
            }
            
            async fetchTooltipContent(data) {
                // This would call your backend API
                const response = await fetch('/api/tooltip', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    return result.html_content;
                }
                
                return null;
            }
            
            showFallbackTooltip(data) {
                this.tooltip.innerHTML = `
                    <div class="tooltip-content">
                        <h3>${data.id || 'Unknown'}</h3>
                        <p><strong>Type:</strong> ${data.type || 'unknown'}</p>
                    </div>
                `;
                this.tooltip.style.display = 'block';
                this.updatePosition();
            }
            
            updatePosition() {
                if (!this.currentTarget || !this.tooltip) return;
                
                const targetRect = this.currentTarget.getBoundingClientRect();
                const tooltipRect = this.tooltip.getBoundingClientRect();
                const viewportWidth = window.innerWidth;
                const viewportHeight = window.innerHeight;
                
                // Calculate initial position (top-right of target)
                let left = targetRect.right + 10;
                let top = targetRect.top;
                
                // Adjust horizontal position if tooltip would go off-screen
                if (left + tooltipRect.width > viewportWidth) {
                    left = targetRect.left - tooltipRect.width - 10;
                }
                
                // Adjust vertical position if tooltip would go off-screen
                if (top + tooltipRect.height > viewportHeight) {
                    top = targetRect.bottom - tooltipRect.height;
                }
                
                // Ensure tooltip stays within viewport
                if (top < 0) top = 10;
                if (left < 0) left = 10;
                
                this.tooltip.style.left = left + 'px';
                this.tooltip.style.top = top + 'px';
            }
            
            hideTooltip() {
                if (this.tooltip) {
                    this.tooltip.style.display = 'none';
                }
                this.currentTarget = null;
            }
            
            destroy() {
                if (this.tooltip) {
                    document.body.removeChild(this.tooltip);
                }
                this.tooltip = null;
            }
        }
        
        // Initialize tooltip system
        const dynamicTooltip = new DynamicTooltip();
        """.strip()
    
    def get_css_styles(self) -> str:
        """Get CSS styles for tooltip components."""
        return f"""
        .dynamic-tooltip {{
            max-width: {self.style_config.get('max_width', 400)}px;
            max-height: {self.style_config.get('max_height', 300)}px;
            background-color: {self.style_config.get('background_color', 'rgba(0, 0, 0, 0.9)')};
            color: {self.style_config.get('text_color', '#ffffff')};
            border-radius: {self.style_config.get('border_radius', 8)}px;
            padding: {self.style_config.get('padding', 12)}px;
            font-size: {self.style_config.get('font_size', '14px')};
            font-family: {self.style_config.get('font_family', 'Arial, sans-serif')};
            box-shadow: {self.style_config.get('box_shadow', '0 4px 12px rgba(0, 0, 0, 0.3)')};
            z-index: {self.style_config.get('z_index', 1000)};
            position: absolute;
            pointer-events: none;
            overflow: hidden;
            word-wrap: break-word;
            line-height: 1.4;
            opacity: 0;
            transition: opacity {self.style_config.get('animation_duration', 0.2)}s ease-in-out;
        }}
        
        .dynamic-tooltip.show {{
            opacity: 1;
        }}
        
        .tooltip-content h3 {{
            margin: 0 0 8px 0;
            font-size: 16px;
            font-weight: bold;
        }}
        
        .tooltip-content p {{
            margin: 0 0 6px 0;
        }}
        
        .tooltip-content ul {{
            margin: 4px 0;
            padding-left: 16px;
        }}
        
        .tooltip-content li {{
            margin: 2px 0;
        }}
        
        .tooltip-content .error {{
            color: #ff6b6b;
            font-style: italic;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .dynamic-tooltip {{
                max-width: 300px;
                font-size: 12px;
                padding: 8px;
            }}
        }}
        
        @media (max-width: 480px) {{
            .dynamic-tooltip {{
                max-width: 250px;
                font-size: 11px;
                padding: 6px;
            }}
        }}
        """.strip()
    
    def create_tooltip_attributes(self, object_id: str, object_type: str, 
                                 additional_data: Optional[Dict[str, Any]] = None) -> str:
        """Create HTML attributes for tooltip-enabled elements."""
        data = {
            "id": object_id,
            "type": object_type
        }
        
        if additional_data:
            data.update(additional_data)
        
        return f'data-tooltip=\'{self._dict_to_json(data)}\''
    
    def _dict_to_json(self, data: Dict[str, Any]) -> str:
        """Convert dictionary to JSON string for HTML attributes."""
        import json
        return json.dumps(data).replace("'", "&#39;")
    
    def render_d3_integration(self) -> str:
        """Get D3.js integration code for existing visualizations."""
        return """
        // D3.js integration for dynamic tooltips
        function integrateDynamicTooltips(selection) {
            selection
                .on('mouseover', function(event, d) {
                    const tooltipData = {
                        id: d.id || d.name || d.label,
                        type: d.type || 'node',
                        context: d
                    };
                    
                    // Show tooltip with dynamic content
                    dynamicTooltip.showTooltip(tooltipData);
                })
                .on('mouseout', function(event, d) {
                    dynamicTooltip.hideTooltip();
                });
        }
        
        // Apply to existing D3 elements
        d3.selectAll('.node').call(integrateDynamicTooltips);
        d3.selectAll('.link').call(integrateDynamicTooltips);
        """.strip()
