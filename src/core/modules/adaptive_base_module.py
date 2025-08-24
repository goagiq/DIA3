"""
Adaptive Base Module Interface

Enhanced base class for all modular report components that can adapt to any data structure.
Provides intelligent data handling, dynamic content generation, and flexible configuration.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from pathlib import Path
import json
import re


@dataclass
class AdaptiveModuleConfig:
    """Enhanced configuration for adaptive modules."""
    enabled: bool = True
    title: str = ""
    description: str = ""
    order: int = 0
    tooltips_enabled: bool = True
    charts_enabled: bool = True
    custom_styles: Dict[str, str] = None
    data_sources: Dict[str, str] = None
    confidence_scores: Dict[str, float] = None
    adaptive_mode: bool = True  # Enable adaptive data handling
    fallback_content: bool = True  # Generate content even with missing data
    data_patterns: Dict[str, List[str]] = None  # Flexible data key patterns


@dataclass
class AdaptiveTooltipData:
    """Enhanced data structure for adaptive tooltip information."""
    title: str
    description: str
    source: str
    strategic_impact: str
    recommendations: Optional[str] = None
    use_cases: Optional[str] = None
    confidence: Optional[float] = None
    data_type: Optional[str] = None  # Type of data this tooltip represents


class AdaptiveBaseModule(ABC):
    """Enhanced abstract base class for adaptive report modules."""
    
    def __init__(self, config: Optional[AdaptiveModuleConfig] = None):
        """Initialize the adaptive module with configuration."""
        self.config = config or AdaptiveModuleConfig()
        self.module_id = self.__class__.__name__.lower()
        self.tooltip_data: Dict[str, AdaptiveTooltipData] = {}
        self.chart_data: Dict[str, Any] = {}
        self.adaptive_data_cache: Dict[str, Any] = {}
        
    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate adaptive HTML content for this module."""
        if not self.is_enabled():
            return ""
        
        # Cache the data for adaptive processing
        self.adaptive_data_cache = data
        
        # Generate content with adaptive data handling
        try:
            content = self._generate_adaptive_content(data)
            return content
        except Exception as e:
            if self.config.fallback_content:
                return self._generate_fallback_content(data, str(e))
            else:
                raise e
    
    def _generate_adaptive_content(self, data: Dict[str, Any]) -> str:
        """Generate content with adaptive data handling."""
        # Extract relevant data using adaptive patterns
        relevant_data = self._extract_relevant_data(data)
        
        # Generate the main content
        main_content = self._generate_main_content(relevant_data)
        
        # Generate adaptive tooltips
        tooltips_content = self._generate_adaptive_tooltips(relevant_data)
        
        # Generate adaptive visualizations
        visualizations_content = self._generate_adaptive_visualizations(relevant_data)
        
        return f"""
        <div class="section adaptive-module" id="{self.module_id}">
            <h2>{self.get_title()}</h2>
            <p>{self.get_description()}</p>
            
            {main_content}
            {tooltips_content}
            {visualizations_content}
        </div>
        """
    
    def _extract_relevant_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant data using adaptive patterns."""
        relevant_data = {}
        
        # Get module-specific data patterns
        patterns = self._get_data_patterns()
        
        for pattern_name, pattern_keys in patterns.items():
            for key in pattern_keys:
                if key in data:
                    relevant_data[pattern_name] = data[key]
                    break
        
        # If no specific patterns match, try generic extraction
        if not relevant_data:
            relevant_data = self._extract_generic_data(data)
        
        return relevant_data
    
    def _get_data_patterns(self) -> Dict[str, List[str]]:
        """Get flexible data patterns for this module."""
        if self.config.data_patterns:
            return self.config.data_patterns
        
        # Default adaptive patterns based on module type
        module_type = self._get_module_type()
        
        patterns = {
            'overview': [f'{module_type}_overview', f'{module_type}_summary', 'overview', 'summary'],
            'analysis': [f'{module_type}_analysis', f'{module_type}_assessment', 'analysis', 'assessment'],
            'metrics': [f'{module_type}_metrics', f'{module_type}_indicators', 'metrics', 'indicators'],
            'trends': [f'{module_type}_trends', f'{module_type}_patterns', 'trends', 'patterns'],
            'insights': [f'{module_type}_insights', f'{module_type}_findings', 'insights', 'findings'],
            'recommendations': [f'{module_type}_recommendations', f'{module_type}_suggestions', 'recommendations', 'suggestions']
        }
        
        return patterns
    
    def _get_module_type(self) -> str:
        """Get the module type for pattern matching."""
        # Extract module type from class name
        class_name = self.__class__.__name__.lower()
        if 'module' in class_name:
            class_name = class_name.replace('module', '')
        return class_name
    
    def _extract_generic_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract generic data when specific patterns don't match."""
        generic_data = {}
        
        # Look for common data structures
        for key, value in data.items():
            if isinstance(value, dict):
                # Check if this dict contains relevant information
                if self._is_relevant_data(value):
                    generic_data[key] = value
            elif isinstance(value, list) and len(value) > 0:
                # Check if this list contains relevant information
                if self._is_relevant_data(value):
                    generic_data[key] = value
            elif isinstance(value, str) and len(value) > 10:
                # Check if this string contains relevant information
                if self._is_relevant_text(value):
                    generic_data[key] = value
        
        return generic_data
    
    def _is_relevant_data(self, data: Union[Dict, List]) -> bool:
        """Check if data is relevant to this module."""
        if isinstance(data, dict):
            # Check for relevant keys
            relevant_keywords = self._get_relevant_keywords()
            for key in data.keys():
                if any(keyword in key.lower() for keyword in relevant_keywords):
                    return True
        elif isinstance(data, list):
            # Check first few items
            for item in data[:3]:
                if isinstance(item, dict):
                    if self._is_relevant_data(item):
                        return True
                elif isinstance(item, str):
                    if self._is_relevant_text(item):
                        return True
        
        return False
    
    def _is_relevant_text(self, text: str) -> bool:
        """Check if text is relevant to this module."""
        relevant_keywords = self._get_relevant_keywords()
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in relevant_keywords)
    
    def _get_relevant_keywords(self) -> List[str]:
        """Get relevant keywords for this module."""
        module_type = self._get_module_type()
        
        # Define keywords based on module type
        keyword_mappings = {
            'executive': ['summary', 'overview', 'findings', 'insights', 'metrics'],
            'geopolitical': ['geopolitical', 'political', 'regional', 'diplomatic', 'alliance'],
            'economic': ['economic', 'financial', 'trade', 'market', 'investment'],
            'military': ['military', 'defense', 'capability', 'weapon', 'strategic'],
            'security': ['security', 'threat', 'risk', 'vulnerability', 'protection'],
            'trade': ['trade', 'commerce', 'import', 'export', 'market'],
            'technology': ['technology', 'technical', 'innovation', 'digital', 'ai'],
            'strategic': ['strategic', 'strategy', 'planning', 'vision', 'objective'],
            'operational': ['operational', 'tactical', 'implementation', 'execution'],
            'risk': ['risk', 'threat', 'vulnerability', 'mitigation', 'assessment'],
            'forecasting': ['forecast', 'prediction', 'trend', 'future', 'scenario'],
            'comparison': ['comparison', 'benchmark', 'ranking', 'competitive', 'analysis'],
            'sentiment': ['sentiment', 'opinion', 'perception', 'reaction', 'response'],
            'timeline': ['timeline', 'schedule', 'milestone', 'deadline', 'phase'],
            'acquisition': ['acquisition', 'procurement', 'program', 'modernization', 'upgrade']
        }
        
        return keyword_mappings.get(module_type, ['analysis', 'assessment', 'evaluation'])
    
    def _generate_main_content(self, relevant_data: Dict[str, Any]) -> str:
        """Generate the main content section."""
        if not relevant_data:
            return self._generate_empty_content()
        
        content_sections = []
        
        for data_type, data_value in relevant_data.items():
            section_html = self._generate_data_section(data_type, data_value)
            if section_html:
                content_sections.append(section_html)
        
        if not content_sections:
            return self._generate_empty_content()
        
        return '\n'.join(content_sections)
    
    def _generate_data_section(self, data_type: str, data_value: Any) -> str:
        """Generate HTML for a specific data section."""
        if isinstance(data_value, dict):
            return self._generate_dict_section(data_type, data_value)
        elif isinstance(data_value, list):
            return self._generate_list_section(data_type, data_value)
        elif isinstance(data_value, str):
            return self._generate_text_section(data_type, data_value)
        else:
            return self._generate_value_section(data_type, str(data_value))
    
    def _generate_dict_section(self, data_type: str, data_dict: Dict[str, Any]) -> str:
        """Generate HTML for dictionary data."""
        title = self._format_section_title(data_type)
        
        items_html = []
        for key, value in data_dict.items():
            if isinstance(value, str):
                items_html.append(f"""
                <div class="data-item">
                    <strong>{self._format_key(key)}:</strong> {value}
                </div>
                """)
            elif isinstance(value, (int, float)):
                items_html.append(f"""
                <div class="data-item">
                    <strong>{self._format_key(key)}:</strong> {value}
                </div>
                """)
            elif isinstance(value, list):
                items_html.append(f"""
                <div class="data-item">
                    <strong>{self._format_key(key)}:</strong>
                    <ul>
                        {''.join(f'<li>{item}</li>' for item in value[:5])}
                    </ul>
                </div>
                """)
        
        return f"""
        <div class="data-section">
            <h3>{title}</h3>
            <div class="data-content">
                {''.join(items_html)}
            </div>
        </div>
        """
    
    def _generate_list_section(self, data_type: str, data_list: List[Any]) -> str:
        """Generate HTML for list data."""
        title = self._format_section_title(data_type)
        
        items_html = []
        for i, item in enumerate(data_list[:10]):  # Limit to 10 items
            if isinstance(item, dict):
                item_html = self._generate_dict_item(item)
            elif isinstance(item, str):
                item_html = f'<li>{item}</li>'
            else:
                item_html = f'<li>{str(item)}</li>'
            items_html.append(item_html)
        
        return f"""
        <div class="data-section">
            <h3>{title}</h3>
            <ul class="data-list">
                {''.join(items_html)}
            </ul>
        </div>
        """
    
    def _generate_dict_item(self, item_dict: Dict[str, Any]) -> str:
        """Generate HTML for a dictionary item in a list."""
        item_html = '<li><div class="dict-item">'
        for key, value in item_dict.items():
            if isinstance(value, str):
                item_html += f'<strong>{self._format_key(key)}:</strong> {value}<br>'
            else:
                item_html += f'<strong>{self._format_key(key)}:</strong> {str(value)}<br>'
        item_html += '</div></li>'
        return item_html
    
    def _generate_text_section(self, data_type: str, text: str) -> str:
        """Generate HTML for text data."""
        title = self._format_section_title(data_type)
        
        return f"""
        <div class="data-section">
            <h3>{title}</h3>
            <div class="text-content">
                <p>{text}</p>
            </div>
        </div>
        """
    
    def _generate_value_section(self, data_type: str, value: str) -> str:
        """Generate HTML for simple value data."""
        title = self._format_section_title(data_type)
        
        return f"""
        <div class="data-section">
            <h3>{title}</h3>
            <div class="value-content">
                <p>{value}</p>
            </div>
        </div>
        """
    
    def _format_section_title(self, data_type: str) -> str:
        """Format a data type into a readable section title."""
        return data_type.replace('_', ' ').title()
    
    def _format_key(self, key: str) -> str:
        """Format a key into a readable label."""
        return key.replace('_', ' ').title()
    
    def _generate_empty_content(self) -> str:
        """Generate content when no relevant data is found."""
        return f"""
        <div class="empty-content">
            <p>No specific {self._get_module_type()} data available for this analysis.</p>
            <p>This module adapts to available data and will display content when relevant information is provided.</p>
        </div>
        """
    
    def _generate_fallback_content(self, data: Dict[str, Any], error: str) -> str:
        """Generate fallback content when errors occur."""
        return f"""
        <div class="fallback-content">
            <h3>⚠️ Adaptive Content Generation</h3>
            <p>This module is operating in adaptive mode and encountered an issue: {error}</p>
            <p>Available data keys: {', '.join(data.keys())}</p>
            <div class="adaptive-info">
                <p><strong>Adaptive Mode:</strong> This module automatically adapts to any data structure.</p>
                <p><strong>Fallback Content:</strong> Generated when specific data patterns are not found.</p>
            </div>
        </div>
        """
    
    def _generate_adaptive_tooltips(self, relevant_data: Dict[str, Any]) -> str:
        """Generate adaptive tooltips based on available data."""
        if not self.config.tooltips_enabled:
            return ""
        
        tooltips_html = []
        for data_type, data_value in relevant_data.items():
            tooltip_id = f"{self.module_id}_{data_type}"
            tooltip_content = self._generate_tooltip_content(data_type, data_value)
            
            tooltips_html.append(f"""
            <div class="tooltip-container" data-tooltip-{self.module_id}="{tooltip_id}">
                <div class="tooltip-content">
                    {tooltip_content}
                </div>
            </div>
            """)
        
        return '\n'.join(tooltips_html)
    
    def _generate_tooltip_content(self, data_type: str, data_value: Any) -> str:
        """Generate tooltip content for a data section."""
        return f"""
        <h4>{self._format_section_title(data_type)}</h4>
        <p>This section contains {data_type} information relevant to the analysis.</p>
        <p><strong>Data Type:</strong> {type(data_value).__name__}</p>
        <p><strong>Module:</strong> {self.get_title()}</p>
        """
    
    def _generate_adaptive_visualizations(self, relevant_data: Dict[str, Any]) -> str:
        """Generate adaptive visualizations based on available data."""
        if not self.config.charts_enabled:
            return ""
        
        visualizations_html = []
        
        for data_type, data_value in relevant_data.items():
            chart_html = self._generate_adaptive_chart(data_type, data_value)
            if chart_html:
                visualizations_html.append(chart_html)
        
        if not visualizations_html:
            return ""
        
        return f"""
        <div class="visualizations-section">
            <h3>📊 Adaptive Visualizations</h3>
            {''.join(visualizations_html)}
        </div>
        """
    
    def _generate_adaptive_chart(self, data_type: str, data_value: Any) -> str:
        """Generate an adaptive chart based on data type and value."""
        if isinstance(data_value, dict):
            return self._generate_dict_chart(data_type, data_value)
        elif isinstance(data_value, list):
            return self._generate_list_chart(data_type, data_value)
        else:
            return ""
    
    def _generate_dict_chart(self, data_type: str, data_dict: Dict[str, Any]) -> str:
        """Generate a chart for dictionary data."""
        # Simple bar chart for numeric values
        numeric_data = {k: v for k, v in data_dict.items() if isinstance(v, (int, float))}
        
        if not numeric_data:
            return ""
        
        chart_id = f"chart_{self.module_id}_{data_type}"
        
        return f"""
        <div class="chart-container">
            <h4>{self._format_section_title(data_type)} Chart</h4>
            <canvas id="{chart_id}" width="400" height="200"></canvas>
            <script>
                // Chart configuration for {chart_id}
                const {chart_id}Data = {json.dumps(numeric_data)};
                // Chart rendering logic would go here
            </script>
        </div>
        """
    
    def _generate_list_chart(self, data_type: str, data_list: List[Any]) -> str:
        """Generate a chart for list data."""
        if not data_list:
            return ""
        
        chart_id = f"chart_{self.module_id}_{data_type}"
        
        return f"""
        <div class="chart-container">
            <h4>{self._format_section_title(data_type)} Overview</h4>
            <div class="list-summary">
                <p><strong>Total Items:</strong> {len(data_list)}</p>
                <p><strong>Data Type:</strong> {type(data_list[0]).__name__}</p>
            </div>
        </div>
        """
    
    # Abstract methods that subclasses can override for custom behavior
    @abstractmethod
    def get_required_data_keys(self) -> List[str]:
        """Get list of required data keys for this module (for backward compatibility)."""
        return []  # Adaptive modules don't require specific keys
    
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
    
    def add_tooltip(self, element_id: str, tooltip_data: AdaptiveTooltipData):
        """Add tooltip data for an element."""
        self.tooltip_data[element_id] = tooltip_data
    
    def get_tooltip_data(self) -> Dict[str, AdaptiveTooltipData]:
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
        
        tooltip_script = f"""
        // Adaptive tooltip data for {self.module_id}
        const {self.module_id}TooltipData = {json.dumps(self.tooltip_data, default=str)};
        
        // Initialize tooltips for {self.module_id}
        document.addEventListener('DOMContentLoaded', function() {{
            initializeTooltips('{self.module_id}', {self.module_id}TooltipData);
        }});
        """
        
        return tooltip_script
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate data for this module (always returns True for adaptive modules)."""
        return True  # Adaptive modules accept any data structure
