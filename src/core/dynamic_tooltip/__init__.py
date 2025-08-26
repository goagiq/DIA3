"""
Dynamic Tooltip System

A comprehensive toolkit for interactive visualizations with dynamic content generation,
multiple data source support, and reliable tooltip rendering.
"""

from .tooltip_manager import DynamicTooltipManager
from .data_source_registry import DataSourceRegistry
from .content_generator import ContentGenerator
from .tooltip_renderer import TooltipRenderer
from .cache_manager import CacheManager
from .configuration import TooltipConfiguration

__all__ = [
    'DynamicTooltipManager',
    'DataSourceRegistry', 
    'ContentGenerator',
    'TooltipRenderer',
    'CacheManager',
    'TooltipConfiguration'
]

__version__ = "1.0.0"
