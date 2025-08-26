"""
Redis-Enhanced Chart Generator

Enhanced chart generation system with Redis caching for optimal performance.
Part of Phase 3.5: Performance Optimization with Redis Integration

Features:
- Redis-based caching for chart generation
- Fixed async/await issues from Phase 3
- Enhanced memory management
- Chart generation < 1 second per chart
- Comprehensive performance monitoring
"""

import asyncio
import json
import pickle
import gzip
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from datetime import datetime
import logging
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import hashlib
import time
import base64
from io import BytesIO

# Import Redis manager
try:
    from config.redis_config import get_redis_manager
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    get_redis_manager = None

logger = logging.getLogger(__name__)


@dataclass
class ChartConfig:
    """Configuration for Redis-enhanced chart generation."""
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    max_workers: int = 4
    parallel_generation: bool = True
    chart_quality: str = "medium"  # low, medium, high
    target_generation_time: float = 1.0  # seconds per chart
    memory_limit_mb: int = 100
    enable_compression: bool = True
    use_redis: bool = True
    fallback_to_disk: bool = True


@dataclass
class ChartData:
    """Data structure for chart information."""
    chart_id: str
    chart_type: str
    data: Dict[str, Any]
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    cache_key: Optional[str] = None


class RedisEnhancedChartGenerator:
    """High-performance chart generator with Redis caching."""
    
    def __init__(self, config: Optional[ChartConfig] = None):
        """Initialize the Redis-enhanced chart generator."""
        self.config = config or ChartConfig()
        self.cache_dir = Path("cache/charts")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Redis manager
        self.redis_manager = None
        if self.config.use_redis and REDIS_AVAILABLE:
            self.redis_manager = get_redis_manager()
            logger.info("✅ Redis manager initialized for chart generation")
        else:
            logger.info("⚠️ Redis not available, using disk caching")
        
        # Performance monitoring
        self.generation_stats = {
            "total_charts": 0,
            "total_time": 0.0,
            "cache_hits": 0,
            "cache_misses": 0,
            "redis_hits": 0,
            "redis_misses": 0,
            "disk_hits": 0,
            "disk_misses": 0,
            "parallel_generations": 0,
            "memory_usage": 0.0
        }
        
        # Thread pool for parallel generation
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_workers)
        
        # Chart templates for common types
        self.chart_templates = self._initialize_chart_templates()
        
        logger.info("✅ Redis-Enhanced Chart Generator initialized")
        logger.info(f"   Target generation time: {self.config.target_generation_time}s per chart")
        logger.info(f"   Max workers: {self.config.max_workers}")
        logger.info(f"   Cache enabled: {self.config.cache_enabled}")
        logger.info(f"   Redis enabled: {self.redis_manager is not None}")
    
    def _initialize_chart_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize optimized chart templates."""
        return {
            "bar": {
                "layout": {
                    "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
                    "showlegend": False,
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "paper_bgcolor": "rgba(0,0,0,0)"
                },
                "config": {
                    "displayModeBar": False,
                    "responsive": True
                }
            },
            "line": {
                "layout": {
                    "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
                    "showlegend": False,
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "paper_bgcolor": "rgba(0,0,0,0)"
                },
                "config": {
                    "displayModeBar": False,
                    "responsive": True
                }
            },
            "pie": {
                "layout": {
                    "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
                    "showlegend": True,
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "paper_bgcolor": "rgba(0,0,0,0)"
                },
                "config": {
                    "displayModeBar": False,
                    "responsive": True
                }
            },
            "scatter": {
                "layout": {
                    "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
                    "showlegend": False,
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "paper_bgcolor": "rgba(0,0,0,0)"
                },
                "config": {
                    "displayModeBar": False,
                    "responsive": True
                }
            },
            "heatmap": {
                "layout": {
                    "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
                    "showlegend": False,
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "paper_bgcolor": "rgba(0,0,0,0)"
                },
                "config": {
                    "displayModeBar": False,
                    "responsive": True
                }
            }
        }
    
    def _generate_cache_key(self, chart_data: ChartData) -> str:
        """Generate cache key for chart."""
        # Create a hash of the chart data and configuration
        data_str = json.dumps(chart_data.data, sort_keys=True)
        config_str = json.dumps(chart_data.config, sort_keys=True)
        content = f"{chart_data.chart_id}:{chart_data.chart_type}:{data_str}:{config_str}"
        return f"chart_generator:{hashlib.md5(content.encode()).hexdigest()}"
    
    async def _get_cached_chart(self, cache_key: str) -> Optional[str]:
        """Get cached chart from Redis or disk."""
        if not self.config.cache_enabled:
            return None
        
        # Try Redis first
        if self.redis_manager and self.redis_manager.is_available():
            try:
                cached_chart = await self.redis_manager.get(cache_key)
                if cached_chart:
                    self.generation_stats["redis_hits"] += 1
                    self.generation_stats["cache_hits"] += 1
                    logger.debug(f"Redis cache hit for chart: {cache_key}")
                    return cached_chart
                else:
                    self.generation_stats["redis_misses"] += 1
                    self.generation_stats["cache_misses"] += 1
            except Exception as e:
                logger.warning(f"Redis cache error: {e}")
                self.generation_stats["redis_misses"] += 1
        
        # Fallback to disk cache
        if self.config.fallback_to_disk:
            try:
                cache_file = self.cache_dir / f"{cache_key}.html"
                if cache_file.exists():
                    # Check if cache is still valid
                    if time.time() - cache_file.stat().st_mtime < self.config.cache_ttl:
                        with open(cache_file, 'r', encoding='utf-8') as f:
                            cached_chart = f.read()
                        self.generation_stats["disk_hits"] += 1
                        self.generation_stats["cache_hits"] += 1
                        logger.debug(f"Disk cache hit for chart: {cache_key}")
                        return cached_chart
                    else:
                        # Cache expired, remove file
                        cache_file.unlink()
            except Exception as e:
                logger.warning(f"Disk cache error: {e}")
        
        self.generation_stats["disk_misses"] += 1
        self.generation_stats["cache_misses"] += 1
        return None
    
    async def _save_cached_chart(self, cache_key: str, chart_html: str) -> bool:
        """Save chart to Redis and/or disk cache."""
        if not self.config.cache_enabled:
            return False
        
        success = False
        
        # Try Redis first
        if self.redis_manager and self.redis_manager.is_available():
            try:
                await self.redis_manager.set(cache_key, chart_html, self.config.cache_ttl)
                success = True
                logger.debug(f"Saved chart to Redis cache: {cache_key}")
            except Exception as e:
                logger.warning(f"Redis cache save error: {e}")
        
        # Fallback to disk cache
        if self.config.fallback_to_disk:
            try:
                cache_file = self.cache_dir / f"{cache_key}.html"
                with open(cache_file, 'w', encoding='utf-8') as f:
                    f.write(chart_html)
                success = True
                logger.debug(f"Saved chart to disk cache: {cache_key}")
            except Exception as e:
                logger.warning(f"Disk cache save error: {e}")
        
        return success
    
    async def generate_chart(self, chart_data: ChartData) -> str:
        """Generate chart with Redis caching."""
        start_time = time.time()
        
        try:
            logger.info(f"Generating chart: {chart_data.chart_id}")
            
            # Generate cache key
            cache_key = self._generate_cache_key(chart_data)
            chart_data.cache_key = cache_key
            
            # Check cache first
            if self.config.cache_enabled:
                cached_chart = await self._get_cached_chart(cache_key)
                if cached_chart:
                    generation_time = time.time() - start_time
                    self.generation_stats["total_time"] += generation_time
                    logger.info(f"✅ Cache hit for chart {chart_data.chart_id} (took {generation_time:.3f}s)")
                    return cached_chart
            
            # Generate chart if not cached
            logger.info(f"Generating chart {chart_data.chart_id} (not cached)")
            
            # Generate chart in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            chart_html = await loop.run_in_executor(
                self.executor, self._generate_chart_sync, chart_data
            )
            
            # Cache the generated chart
            if self.config.cache_enabled:
                await self._save_cached_chart(cache_key, chart_html)
            
            # Update statistics
            generation_time = time.time() - start_time
            self.generation_stats["total_charts"] += 1
            self.generation_stats["total_time"] += generation_time
            
            logger.info(f"✅ Generated chart {chart_data.chart_id} in {generation_time:.3f}s")
            return chart_html
            
        except Exception as e:
            logger.error(f"Error generating chart {chart_data.chart_id}: {e}")
            raise
    
    def _generate_chart_sync(self, chart_data: ChartData) -> str:
        """Generate chart synchronously (called from thread pool)."""
        try:
            chart_type = chart_data.chart_type
            data = chart_data.data
            config = chart_data.config
            
            # Get template for chart type
            template = self.chart_templates.get(chart_type, {})
            
            # Create chart based on type
            if chart_type == "bar":
                fig = self._create_bar_chart(data, config, template)
            elif chart_type == "line":
                fig = self._create_line_chart(data, config, template)
            elif chart_type == "pie":
                fig = self._create_pie_chart(data, config, template)
            elif chart_type == "scatter":
                fig = self._create_scatter_chart(data, config, template)
            elif chart_type == "heatmap":
                fig = self._create_heatmap_chart(data, config, template)
            else:
                raise ValueError(f"Unsupported chart type: {chart_type}")
            
            # Convert to HTML
            chart_html = fig.to_html(
                include_plotlyjs=False,
                full_html=False,
                config=template.get("config", {})
            )
            
            return chart_html
            
        except Exception as e:
            logger.error(f"Error in chart generation: {e}")
            raise
    
    def _create_bar_chart(self, data: Dict[str, Any], config: Dict[str, Any], template: Dict[str, Any]) -> go.Figure:
        """Create bar chart."""
        categories = data.get("categories", [])
        values = data.get("values", [])
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color=config.get("color", "steelblue"),
                opacity=config.get("opacity", 0.8)
            )
        ])
        
        # Apply template layout
        fig.update_layout(**template.get("layout", {}))
        
        return fig
    
    def _create_line_chart(self, data: Dict[str, Any], config: Dict[str, Any], template: Dict[str, Any]) -> go.Figure:
        """Create line chart."""
        x = data.get("x", [])
        y = data.get("y", [])
        
        fig = go.Figure(data=[
            go.Scatter(
                x=x,
                y=y,
                mode="lines+markers",
                line=dict(color=config.get("color", "steelblue"), width=2),
                marker=dict(size=6)
            )
        ])
        
        # Apply template layout
        fig.update_layout(**template.get("layout", {}))
        
        return fig
    
    def _create_pie_chart(self, data: Dict[str, Any], config: Dict[str, Any], template: Dict[str, Any]) -> go.Figure:
        """Create pie chart."""
        labels = data.get("labels", [])
        values = data.get("values", [])
        
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=config.get("hole", 0.3)
            )
        ])
        
        # Apply template layout
        fig.update_layout(**template.get("layout", {}))
        
        return fig
    
    def _create_scatter_chart(self, data: Dict[str, Any], config: Dict[str, Any], template: Dict[str, Any]) -> go.Figure:
        """Create scatter chart."""
        x = data.get("x", [])
        y = data.get("y", [])
        
        fig = go.Figure(data=[
            go.Scatter(
                x=x,
                y=y,
                mode="markers",
                marker=dict(
                    size=config.get("marker_size", 8),
                    color=config.get("color", "steelblue"),
                    opacity=config.get("opacity", 0.7)
                )
            )
        ])
        
        # Apply template layout
        fig.update_layout(**template.get("layout", {}))
        
        return fig
    
    def _create_heatmap_chart(self, data: Dict[str, Any], config: Dict[str, Any], template: Dict[str, Any]) -> go.Figure:
        """Create heatmap chart."""
        values = data.get("values", [])
        x_labels = data.get("x_labels", [])
        y_labels = data.get("y_labels", [])
        
        fig = go.Figure(data=[
            go.Heatmap(
                z=values,
                x=x_labels,
                y=y_labels,
                colorscale=config.get("colorscale", "Viridis")
            )
        ])
        
        # Apply template layout
        fig.update_layout(**template.get("layout", {}))
        
        return fig
    
    async def generate_multiple_charts(self, charts_data: List[ChartData]) -> List[str]:
        """Generate multiple charts in parallel."""
        if not self.config.parallel_generation:
            # Sequential generation
            results = []
            for chart_data in charts_data:
                result = await self.generate_chart(chart_data)
                results.append(result)
            return results
        
        # Parallel generation
        self.generation_stats["parallel_generations"] += 1
        
        # Create tasks for all charts
        tasks = [self.generate_chart(chart_data) for chart_data in charts_data]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error generating chart {charts_data[i].chart_id}: {result}")
                processed_results.append(f"<div>Error generating chart: {result}</div>")
            else:
                processed_results.append(result)
        
        return processed_results
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics."""
        stats = {
            **self.generation_stats,
            "redis_stats": self.redis_manager.get_stats() if self.redis_manager else None,
            "config": {
                "target_generation_time": self.config.target_generation_time,
                "max_workers": self.config.max_workers,
                "cache_ttl": self.config.cache_ttl,
                "use_redis": self.redis_manager is not None,
                "fallback_to_disk": self.config.fallback_to_disk
            }
        }
        
        if self.generation_stats["total_charts"] > 0:
            stats["average_generation_time"] = (
                self.generation_stats["total_time"] / self.generation_stats["total_charts"]
            )
        
        return stats
    
    def cleanup(self):
        """Cleanup resources."""
        if self.executor:
            self.executor.shutdown(wait=True)
        logger.info("Redis-Enhanced Chart Generator cleanup completed")


# Global instance
redis_enhanced_chart_generator = RedisEnhancedChartGenerator()
