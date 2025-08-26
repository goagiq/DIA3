"""
Tooltip Configuration Management

Configuration settings for the dynamic tooltip system including data sources,
content generation, caching, and rendering options.
"""

import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import yaml
import json


class DataSourceType(Enum):
    """Supported data source types."""
    API = "api"
    DATABASE = "database"
    FILE = "file"
    STREAM = "stream"
    WEBHOOK = "webhook"
    MESSAGE_QUEUE = "message_queue"
    MCP_TOOL = "mcp_tool"


class ContentType(Enum):
    """Supported content types for tooltips."""
    TEXT = "text"
    HTML = "html"
    MARKDOWN = "markdown"
    JSON = "json"
    RICH_TEXT = "rich_text"


@dataclass
class DataSourceConfig:
    """Configuration for a data source."""
    name: str
    type: DataSourceType
    enabled: bool = True
    priority: int = 5  # 1-10, higher is more important
    timeout: int = 30
    retry_attempts: int = 3
    retry_delay: float = 1.0
    cache_ttl: int = 300  # 5 minutes
    connection_config: Dict[str, Any] = field(default_factory=dict)
    authentication: Optional[Dict[str, Any]] = None
    rate_limit: Optional[int] = None
    description: str = ""


@dataclass
class ContentTemplate:
    """Template for content generation."""
    name: str
    content_type: ContentType
    template: str
    variables: List[str] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)
    fallback_template: Optional[str] = None


@dataclass
class TooltipStyle:
    """Styling configuration for tooltips."""
    max_width: int = 400
    max_height: int = 300
    background_color: str = "rgba(0, 0, 0, 0.9)"
    text_color: str = "#ffffff"
    border_radius: int = 8
    padding: int = 12
    font_size: str = "14px"
    font_family: str = "Arial, sans-serif"
    box_shadow: str = "0 4px 12px rgba(0, 0, 0, 0.3)"
    animation_duration: float = 0.2
    z_index: int = 1000


@dataclass
class CacheConfig:
    """Caching configuration."""
    enabled: bool = True
    memory_cache_size: int = 1000
    disk_cache_size_mb: int = 100
    cache_ttl_default: int = 300
    cache_directory: str = "cache/tooltips"
    compression_enabled: bool = True
    cache_key_prefix: str = "tooltip_"


@dataclass
class PerformanceConfig:
    """Performance optimization settings."""
    debounce_delay: int = 150  # milliseconds
    lazy_loading_enabled: bool = True
    preload_distance: int = 50  # pixels
    max_concurrent_requests: int = 5
    request_timeout: int = 10
    enable_progressive_loading: bool = True


@dataclass
class TooltipConfiguration:
    """Main configuration for the dynamic tooltip system."""
    
    # Data sources
    data_sources: Dict[str, DataSourceConfig] = field(default_factory=dict)
    
    # Content templates
    content_templates: Dict[str, ContentTemplate] = field(default_factory=dict)
    
    # Styling
    style: TooltipStyle = field(default_factory=TooltipStyle)
    
    # Caching
    cache: CacheConfig = field(default_factory=CacheConfig)
    
    # Performance
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    
    # General settings
    enabled: bool = True
    debug_mode: bool = False
    log_level: str = "INFO"
    config_file: Optional[str] = None
    
    def __post_init__(self):
        """Initialize default configurations after object creation."""
        if not self.data_sources:
            self._load_default_data_sources()
        
        if not self.content_templates:
            self._load_default_templates()
    
    def _load_default_data_sources(self):
        """Load default data source configurations."""
        self.data_sources = {
            "knowledge_graph": DataSourceConfig(
                name="knowledge_graph",
                type=DataSourceType.MCP_TOOL,
                priority=9,
                description="Knowledge graph data for entity relationships"
            ),
            "semantic_search": DataSourceConfig(
                name="semantic_search", 
                type=DataSourceType.MCP_TOOL,
                priority=8,
                description="Semantic search for contextual information"
            ),
            "business_intelligence": DataSourceConfig(
                name="business_intelligence",
                type=DataSourceType.MCP_TOOL,
                priority=7,
                description="Business intelligence and analytics data"
            ),
            "external_api": DataSourceConfig(
                name="external_api",
                type=DataSourceType.API,
                priority=6,
                timeout=15,
                retry_attempts=2,
                description="External API data sources"
            )
        }
    
    def _load_default_templates(self):
        """Load default content templates."""
        self.content_templates = {
            "entity": ContentTemplate(
                name="entity",
                content_type=ContentType.RICH_TEXT,
                template="""
                <div class="tooltip-content">
                    <h3>{name}</h3>
                    <p><strong>Type:</strong> {type}</p>
                    <p><strong>Confidence:</strong> {confidence}%</p>
                    {description}
                    {relationships}
                    {recommendations}
                </div>
                """,
                variables=["name", "type", "confidence", "description", "relationships", "recommendations"]
            ),
            "relationship": ContentTemplate(
                name="relationship",
                content_type=ContentType.RICH_TEXT,
                template="""
                <div class="tooltip-content">
                    <h3>{source} → {target}</h3>
                    <p><strong>Type:</strong> {relationship_type}</p>
                    <p><strong>Strength:</strong> {strength}</p>
                    {description}
                    {evidence}
                </div>
                """,
                variables=["source", "target", "relationship_type", "strength", "description", "evidence"]
            ),
            "simple": ContentTemplate(
                name="simple",
                content_type=ContentType.TEXT,
                template="{title}: {description}",
                variables=["title", "description"]
            )
        }
    
    @classmethod
    def from_file(cls, config_path: str) -> 'TooltipConfiguration':
        """Load configuration from file."""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.suffix.lower() == '.yaml':
                config_data = yaml.safe_load(f)
            else:
                config_data = json.load(f)
        
        return cls(**config_data)
    
    def save_to_file(self, config_path: str):
        """Save configuration to file."""
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        config_data = {
            'data_sources': {
                name: {
                    'name': ds.name,
                    'type': ds.type.value,
                    'enabled': ds.enabled,
                    'priority': ds.priority,
                    'timeout': ds.timeout,
                    'retry_attempts': ds.retry_attempts,
                    'retry_delay': ds.retry_delay,
                    'cache_ttl': ds.cache_ttl,
                    'connection_config': ds.connection_config,
                    'authentication': ds.authentication,
                    'rate_limit': ds.rate_limit,
                    'description': ds.description
                }
                for name, ds in self.data_sources.items()
            },
            'content_templates': {
                name: {
                    'name': ct.name,
                    'content_type': ct.content_type.value,
                    'template': ct.template,
                    'variables': ct.variables,
                    'conditions': ct.conditions,
                    'fallback_template': ct.fallback_template
                }
                for name, ct in self.content_templates.items()
            },
            'style': {
                'max_width': self.style.max_width,
                'max_height': self.style.max_height,
                'background_color': self.style.background_color,
                'text_color': self.style.text_color,
                'border_radius': self.style.border_radius,
                'padding': self.style.padding,
                'font_size': self.style.font_size,
                'font_family': self.style.font_family,
                'box_shadow': self.style.box_shadow,
                'animation_duration': self.style.animation_duration,
                'z_index': self.style.z_index
            },
            'cache': {
                'enabled': self.cache.enabled,
                'memory_cache_size': self.cache.memory_cache_size,
                'disk_cache_size_mb': self.cache.disk_cache_size_mb,
                'cache_ttl_default': self.cache.cache_ttl_default,
                'cache_directory': self.cache.cache_directory,
                'compression_enabled': self.cache.compression_enabled,
                'cache_key_prefix': self.cache.cache_key_prefix
            },
            'performance': {
                'debounce_delay': self.performance.debounce_delay,
                'lazy_loading_enabled': self.performance.lazy_loading_enabled,
                'preload_distance': self.performance.preload_distance,
                'max_concurrent_requests': self.performance.max_concurrent_requests,
                'request_timeout': self.performance.request_timeout,
                'enable_progressive_loading': self.performance.enable_progressive_loading
            },
            'enabled': self.enabled,
            'debug_mode': self.debug_mode,
            'log_level': self.log_level
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            if config_path.suffix.lower() == '.yaml':
                yaml.dump(config_data, f, default_flow_style=False, indent=2)
            else:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    def get_data_source(self, name: str) -> Optional[DataSourceConfig]:
        """Get data source configuration by name."""
        return self.data_sources.get(name)
    
    def get_template(self, name: str) -> Optional[ContentTemplate]:
        """Get content template by name."""
        return self.content_templates.get(name)
    
    def add_data_source(self, name: str, config: DataSourceConfig):
        """Add a new data source configuration."""
        self.data_sources[name] = config
    
    def add_template(self, name: str, template: ContentTemplate):
        """Add a new content template."""
        self.content_templates[name] = template
    
    def enable_data_source(self, name: str):
        """Enable a data source."""
        if name in self.data_sources:
            self.data_sources[name].enabled = True
    
    def disable_data_source(self, name: str):
        """Disable a data source."""
        if name in self.data_sources:
            self.data_sources[name].enabled = False
