"""
Base Module Interface

Abstract base class for all modular report components.
Provides standardized interface for configuration, rendering, and tooltip integration.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class ModuleConfig:
    """Configuration for a module."""
    enabled: bool = True
    title: str = ""
    description: str = ""
    order: int = 0
    tooltips_enabled: bool = True
    charts_enabled: bool = True
    custom_styles: Dict[str, str] = None
    data_sources: Dict[str, str] = None
    confidence_scores: Dict[str, float] = None


@dataclass
class TooltipData:
    """Data structure for tooltip information."""
    title: str
    description: str
    source: str
    strategic_impact: str
    recommendations: Optional[str] = None
    use_cases: Optional[str] = None
    confidence: Optional[float] = None


class BaseModule(ABC):
    """Abstract base class for all report modules."""
    
    def __init__(self, config: Optional[ModuleConfig] = None):
        """Initialize the module with configuration."""
        self.config = config or ModuleConfig()
        self.module_id = self.__class__.__name__.lower()
        self.tooltip_data: Dict[str, TooltipData] = {}
        self.chart_data: Dict[str, Any] = {}
        
    @abstractmethod
    async def generate_content(self, data: Dict[str, Any], config: Optional[ModuleConfig] = None) -> Dict[str, Any]:
        """Generate the HTML content for this module with Phase 4 enhancements."""
        pass
    
    @abstractmethod
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module."""
        pass
    
    def is_enabled(self) -> bool:
        """Check if the module is enabled."""
        return self.config.enabled
    
    def get_title(self) -> str:
        """Get the module title."""
        return self.config.title
    
    def get_description(self) -> str:
        """Get the module description."""
        return self.config.description
    
    def get_order(self) -> int:
        """Get the module display order."""
        return self.config.order
    
    def add_tooltip(self, element_id: str, tooltip_data: TooltipData):
        """Add tooltip data for an element."""
        self.tooltip_data[element_id] = tooltip_data
    
    def get_tooltip_data(self) -> Dict[str, TooltipData]:
        """Get all tooltip data for this module."""
        return self.tooltip_data
    
    def add_chart_data(self, chart_id: str, chart_config: Dict[str, Any]):
        """Add chart configuration data."""
        self.chart_data[chart_id] = chart_config
    
    def get_chart_data(self) -> Dict[str, Any]:
        """Get all chart data for this module."""
        return self.chart_data
    
    def generate_tooltip_script(self) -> str:
        """Generate JavaScript for tooltip functionality."""
        if not self.config.tooltips_enabled:
            return ""
        
        tooltip_script = """
        // Tooltip data for {module_id}
        const {module_id}TooltipData = {tooltip_data};
        
        // Initialize tooltips for {module_id}
        document.querySelectorAll('[data-tooltip-{module_id}]').forEach(element => {{
            const tooltipId = element.getAttribute('data-tooltip-{module_id}');
            const tooltipData = {module_id}TooltipData[tooltipId];
            
            if (tooltipData) {{
                element.addEventListener('mouseenter', (e) => {{
                    showEnhancedTooltip(e, tooltipData);
                }});
                
                element.addEventListener('mouseleave', () => {{
                    hideEnhancedTooltip();
                }});
            }}
        }});
        """.format(
            module_id=self.module_id,
            tooltip_data=json.dumps({
                k: {
                    'title': v.title,
                    'description': v.description,
                    'source': v.source,
                    'strategic_impact': v.strategic_impact,
                    'recommendations': v.recommendations,
                    'use_cases': v.use_cases,
                    'confidence': v.confidence
                }
                for k, v in self.tooltip_data.items()
            })
        )
        
        return tooltip_script
    
    def generate_chart_script(self) -> str:
        """Generate JavaScript for chart functionality."""
        if not self.config.charts_enabled:
            return ""
        
        chart_script = """
        // Chart data for {module_id}
        const {module_id}ChartData = {chart_data};
        
        // Initialize charts for {module_id}
        Object.keys({module_id}ChartData).forEach(chartId => {{
            const canvas = document.getElementById(chartId);
            if (canvas) {{
                const ctx = canvas.getContext('2d');
                const config = {module_id}ChartData[chartId];
                
                // Ensure responsive settings are properly configured
                if (!config.options) {{
                    config.options = {{}};
                }}
                config.options.responsive = true;
                config.options.maintainAspectRatio = false;
                
                // Add proper container sizing
                const container = canvas.parentElement;
                if (container && !container.style.height) {{
                    container.style.height = '300px';
                    container.style.position = 'relative';
                }}
                
                new Chart(ctx, config);
            }}
        }});
        """.format(
            module_id=self.module_id,
            chart_data=json.dumps(self.chart_data)
        )
        
        return chart_script
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate that required data is present."""
        required_keys = self.get_required_data_keys()
        missing_keys = [key for key in required_keys if key not in data]
        
        if missing_keys:
            raise ValueError(
                f"Missing required data keys for {self.module_id}: {missing_keys}"
            )
        
        return True
    
    def get_module_metadata(self) -> Dict[str, Any]:
        """Get metadata about this module."""
        return {
            'module_id': self.module_id,
            'title': self.get_title(),
            'description': self.get_description(),
            'enabled': self.is_enabled(),
            'order': self.get_order(),
            'required_data_keys': self.get_required_data_keys(),
            'tooltips_count': len(self.tooltip_data),
            'charts_count': len(self.chart_data)
        }
    
    def export_config(self) -> Dict[str, Any]:
        """Export module configuration."""
        return {
            'enabled': self.config.enabled,
            'title': self.config.title,
            'description': self.config.description,
            'order': self.config.order,
            'tooltips_enabled': self.config.tooltips_enabled,
            'charts_enabled': self.config.charts_enabled,
            'custom_styles': self.config.custom_styles or {},
            'data_sources': self.config.data_sources or {},
            'confidence_scores': self.config.confidence_scores or {}
        }
    
    def import_config(self, config_data: Dict[str, Any]):
        """Import module configuration."""
        self.config.enabled = config_data.get('enabled', True)
        self.config.title = config_data.get('title', '')
        self.config.description = config_data.get('description', '')
        self.config.order = config_data.get('order', 0)
        self.config.tooltips_enabled = config_data.get('tooltips_enabled', True)
        self.config.charts_enabled = config_data.get('charts_enabled', True)
        self.config.custom_styles = config_data.get('custom_styles', {})
        self.config.data_sources = config_data.get('data_sources', {})
        self.config.confidence_scores = config_data.get('confidence_scores', {})
