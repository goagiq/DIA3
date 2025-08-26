"""
Performance Optimized Chart Generator

High-performance chart generation system with caching and optimization.
Part of Phase 3: Performance Optimization - Task 3.2

Features:
- Chart caching and optimization
- Parallel chart generation
- Memory-efficient rendering
- Chart generation < 1 second per chart
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

logger = logging.getLogger(__name__)


@dataclass
class ChartConfig:
    """Configuration for chart generation optimization."""
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    max_workers: int = 4
    parallel_generation: bool = True
    chart_quality: str = "medium"  # low, medium, high
    target_generation_time: float = 1.0  # seconds per chart
    memory_limit_mb: int = 100
    enable_compression: bool = True


@dataclass
class ChartData:
    """Data structure for chart information."""
    chart_id: str
    chart_type: str
    data: Dict[str, Any]
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    cache_key: Optional[str] = None


class PerformanceOptimizedChartGenerator:
    """High-performance chart generator with caching and optimization."""
    
    def __init__(self, config: Optional[ChartConfig] = None):
        """Initialize the performance-optimized chart generator."""
        self.config = config or ChartConfig()
        self.cache_dir = Path("cache/charts")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Performance monitoring
        self.generation_stats = {
            "total_charts": 0,
            "total_time": 0.0,
            "cache_hits": 0,
            "cache_misses": 0,
            "parallel_generations": 0,
            "memory_usage": 0.0
        }
        
        # Thread pool for parallel generation
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_workers)
        
        # Chart templates for common types
        self.chart_templates = self._initialize_chart_templates()
        
        logger.info("✅ Performance Optimized Chart Generator initialized")
        logger.info(f"   Target generation time: {self.config.target_generation_time}s per chart")
        logger.info(f"   Max workers: {self.config.max_workers}")
        logger.info(f"   Cache enabled: {self.config.cache_enabled}")
    
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
                "config": {"displayModeBar": False}
            },
            "line": {
                "layout": {
                    "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
                    "showlegend": False,
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "paper_bgcolor": "rgba(0,0,0,0)"
                },
                "config": {"displayModeBar": False}
            },
            "pie": {
                "layout": {
                    "margin": {"l": 20, "r": 20, "t": 20, "b": 20},
                    "showlegend": True,
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "paper_bgcolor": "rgba(0,0,0,0)"
                },
                "config": {"displayModeBar": False}
            },
            "scatter": {
                "layout": {
                    "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
                    "showlegend": False,
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "paper_bgcolor": "rgba(0,0,0,0)"
                },
                "config": {"displayModeBar": False}
            },
            "heatmap": {
                "layout": {
                    "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
                    "showlegend": False,
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "paper_bgcolor": "rgba(0,0,0,0)"
                },
                "config": {"displayModeBar": False}
            }
        }
    
    async def generate_charts_batch(self, charts_data: List[ChartData]) -> List[Dict[str, Any]]:
        """Generate multiple charts efficiently with caching and parallel processing."""
        start_time = time.time()
        
        try:
            logger.info(f"Generating {len(charts_data)} charts in batch")
            
            # Check cache for all charts
            cached_charts = []
            charts_to_generate = []
            
            for chart_data in charts_data:
                if self.config.cache_enabled:
                    cached_chart = await self._get_cached_chart(chart_data)
                    if cached_chart:
                        cached_charts.append(cached_chart)
                        self.generation_stats["cache_hits"] += 1
                        continue
                
                self.generation_stats["cache_misses"] += 1
                charts_to_generate.append(chart_data)
            
            # Generate remaining charts
            generated_charts = []
            if charts_to_generate:
                if self.config.parallel_generation and len(charts_to_generate) > 1:
                    generated_charts = await self._generate_charts_parallel(charts_to_generate)
                    self.generation_stats["parallel_generations"] += len(charts_to_generate)
                else:
                    generated_charts = await self._generate_charts_sequential(charts_to_generate)
            
            # Combine cached and generated charts
            all_charts = cached_charts + generated_charts
            
            # Update performance stats
            generation_time = time.time() - start_time
            self.generation_stats["total_charts"] += len(charts_data)
            self.generation_stats["total_time"] += generation_time
            
            avg_time_per_chart = generation_time / len(charts_data) if charts_data else 0
            logger.info(f"✅ Generated {len(charts_data)} charts in {generation_time:.2f}s")
            logger.info(f"   Average time per chart: {avg_time_per_chart:.2f}s")
            
            # Validate performance targets
            if avg_time_per_chart > self.config.target_generation_time:
                logger.warning(f"⚠️ Average generation time ({avg_time_per_chart:.2f}s) exceeds target ({self.config.target_generation_time}s)")
            
            return all_charts
            
        except Exception as e:
            logger.error(f"Error generating charts batch: {e}")
            raise
    
    async def _generate_charts_parallel(self, charts_data: List[ChartData]) -> List[Dict[str, Any]]:
        """Generate charts in parallel using thread pool."""
        loop = asyncio.get_event_loop()
        
        # Submit chart generation tasks
        tasks = []
        for chart_data in charts_data:
            task = loop.run_in_executor(self.executor, self._generate_single_chart, chart_data)
            tasks.append(task)
        
        # Wait for all charts to complete
        generated_charts = await asyncio.gather(*tasks)
        logger.info(f"✅ Generated {len(generated_charts)} charts in parallel")
        
        return generated_charts
    
    async def _generate_charts_sequential(self, charts_data: List[ChartData]) -> List[Dict[str, Any]]:
        """Generate charts sequentially."""
        generated_charts = []
        
        for chart_data in charts_data:
            generated_chart = await asyncio.get_event_loop().run_in_executor(
                self.executor, self._generate_single_chart, chart_data
            )
            generated_charts.append(generated_chart)
        
        logger.info(f"✅ Generated {len(generated_charts)} charts sequentially")
        return generated_charts
    
    def _generate_single_chart(self, chart_data: ChartData) -> Dict[str, Any]:
        """Generate a single chart with optimization."""
        start_time = time.time()
        
        try:
            # Generate chart based on type
            if chart_data.chart_type == "bar":
                chart_html = self._generate_bar_chart(chart_data)
            elif chart_data.chart_type == "line":
                chart_html = self._generate_line_chart(chart_data)
            elif chart_data.chart_type == "pie":
                chart_html = self._generate_pie_chart(chart_data)
            elif chart_data.chart_type == "scatter":
                chart_html = self._generate_scatter_chart(chart_data)
            elif chart_data.chart_type == "heatmap":
                chart_html = self._generate_heatmap_chart(chart_data)
            elif chart_data.chart_type == "timeline":
                chart_html = self._generate_timeline_chart(chart_data)
            else:
                chart_html = self._generate_generic_chart(chart_data)
            
            # Cache the generated chart
            if self.config.cache_enabled:
                asyncio.create_task(self._cache_chart(chart_data, chart_html))
            
            generation_time = time.time() - start_time
            
            return {
                "chart_id": chart_data.chart_id,
                "chart_type": chart_data.chart_type,
                "html": chart_html,
                "generation_time": generation_time,
                "metadata": {
                    **chart_data.metadata,
                    "generated_at": datetime.now().isoformat(),
                    "optimized": True
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating chart {chart_data.chart_id}: {e}")
            return {
                "chart_id": chart_data.chart_id,
                "chart_type": chart_data.chart_type,
                "html": f"<div class='chart-error'>Error generating chart: {e}</div>",
                "generation_time": time.time() - start_time,
                "error": str(e)
            }
    
    def _generate_bar_chart(self, chart_data: ChartData) -> str:
        """Generate optimized bar chart."""
        data = chart_data.data
        config = chart_data.config
        
        # Extract data
        x_values = data.get("categories", [])
        y_values = data.get("values", [])
        title = config.get("title", "Bar Chart")
        
        # Create optimized figure
        fig = go.Figure(data=[
            go.Bar(
                x=x_values,
                y=y_values,
                marker_color='rgba(58, 200, 225, 0.8)',
                marker_line_color='rgba(58, 200, 225, 1)',
                marker_line_width=1,
                opacity=0.8
            )
        ])
        
        # Apply template
        template = self.chart_templates["bar"]
        fig.update_layout(
            title=title,
            **template["layout"]
        )
        
        return fig.to_html(
            include_plotlyjs=False,
            full_html=False,
            config=template["config"]
        )
    
    def _generate_line_chart(self, chart_data: ChartData) -> str:
        """Generate optimized line chart."""
        data = chart_data.data
        config = chart_data.config
        
        # Extract data
        x_values = data.get("x", [])
        y_values = data.get("y", [])
        title = config.get("title", "Line Chart")
        
        # Create optimized figure
        fig = go.Figure(data=[
            go.Scatter(
                x=x_values,
                y=y_values,
                mode='lines+markers',
                line=dict(color='rgba(58, 200, 225, 1)', width=2),
                marker=dict(size=6, color='rgba(58, 200, 225, 0.8)')
            )
        ])
        
        # Apply template
        template = self.chart_templates["line"]
        fig.update_layout(
            title=title,
            **template["layout"]
        )
        
        return fig.to_html(
            include_plotlyjs=False,
            full_html=False,
            config=template["config"]
        )
    
    def _generate_pie_chart(self, chart_data: ChartData) -> str:
        """Generate optimized pie chart."""
        data = chart_data.data
        config = chart_data.config
        
        # Extract data
        labels = data.get("labels", [])
        values = data.get("values", [])
        title = config.get("title", "Pie Chart")
        
        # Create optimized figure
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                marker_colors=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            )
        ])
        
        # Apply template
        template = self.chart_templates["pie"]
        fig.update_layout(
            title=title,
            **template["layout"]
        )
        
        return fig.to_html(
            include_plotlyjs=False,
            full_html=False,
            config=template["config"]
        )
    
    def _generate_scatter_chart(self, chart_data: ChartData) -> str:
        """Generate optimized scatter chart."""
        data = chart_data.data
        config = chart_data.config
        
        # Extract data
        x_values = data.get("x", [])
        y_values = data.get("y", [])
        title = config.get("title", "Scatter Chart")
        
        # Create optimized figure
        fig = go.Figure(data=[
            go.Scatter(
                x=x_values,
                y=y_values,
                mode='markers',
                marker=dict(
                    size=8,
                    color='rgba(58, 200, 225, 0.8)',
                    line=dict(color='rgba(58, 200, 225, 1)', width=1)
                )
            )
        ])
        
        # Apply template
        template = self.chart_templates["scatter"]
        fig.update_layout(
            title=title,
            **template["layout"]
        )
        
        return fig.to_html(
            include_plotlyjs=False,
            full_html=False,
            config=template["config"]
        )
    
    def _generate_heatmap_chart(self, chart_data: ChartData) -> str:
        """Generate optimized heatmap chart."""
        data = chart_data.data
        config = chart_data.config
        
        # Extract data
        values = data.get("values", [])
        x_labels = data.get("x_labels", [])
        y_labels = data.get("y_labels", [])
        title = config.get("title", "Heatmap Chart")
        
        # Create optimized figure
        fig = go.Figure(data=[
            go.Heatmap(
                z=values,
                x=x_labels,
                y=y_labels,
                colorscale='Viridis',
                showscale=True
            )
        ])
        
        # Apply template
        template = self.chart_templates["heatmap"]
        fig.update_layout(
            title=title,
            **template["layout"]
        )
        
        return fig.to_html(
            include_plotlyjs=False,
            full_html=False,
            config=template["config"]
        )
    
    def _generate_timeline_chart(self, chart_data: ChartData) -> str:
        """Generate optimized timeline chart."""
        data = chart_data.data
        config = chart_data.config
        
        # Extract data
        categories = data.get("categories", [])
        values = data.get("values", [])
        labels = data.get("labels", [])
        title = config.get("title", "Timeline Chart")
        
        # Create optimized figure
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                text=labels,
                textposition='auto',
                marker_color='rgba(58, 200, 225, 0.8)',
                marker_line_color='rgba(58, 200, 225, 1)',
                marker_line_width=1
            )
        ])
        
        # Apply template
        template = self.chart_templates["bar"]
        fig.update_layout(
            title=title,
            **template["layout"]
        )
        
        return fig.to_html(
            include_plotlyjs=False,
            full_html=False,
            config=template["config"]
        )
    
    def _generate_generic_chart(self, chart_data: ChartData) -> str:
        """Generate generic chart for unknown types."""
        return f"""
        <div class="chart-container">
            <h3>{chart_data.config.get('title', 'Chart')}</h3>
            <p>Chart type '{chart_data.chart_type}' not implemented. Data: {len(str(chart_data.data))} characters</p>
        </div>
        """
    
    def _generate_cache_key(self, chart_data: ChartData) -> str:
        """Generate cache key for chart."""
        data_hash = hashlib.md5(str(chart_data.data).encode()).hexdigest()
        config_hash = hashlib.md5(str(chart_data.config).encode()).hexdigest()
        return f"{chart_data.chart_type}_{data_hash}_{config_hash}"
    
    async def _get_cached_chart(self, chart_data: ChartData) -> Optional[Dict[str, Any]]:
        """Get cached chart if available and not expired."""
        cache_key = self._generate_cache_key(chart_data)
        cache_file = self.cache_dir / f"{cache_key}.pkl.gz"
        
        if not cache_file.exists():
            return None
        
        # Check if cache is expired
        if time.time() - cache_file.stat().st_mtime > self.config.cache_ttl:
            cache_file.unlink()  # Remove expired cache
            return None
        
        try:
            with gzip.open(cache_file, 'rb') as f:
                cached_chart = pickle.load(f)
            logger.info(f"Retrieved cached chart: {cache_file}")
            return cached_chart
        except Exception as e:
            logger.warning(f"Failed to load cached chart {cache_file}: {e}")
            return None
    
    async def _cache_chart(self, chart_data: ChartData, chart_html: str):
        """Cache generated chart."""
        cache_key = self._generate_cache_key(chart_data)
        cache_file = self.cache_dir / f"{cache_key}.pkl.gz"
        
        try:
            cached_data = {
                "chart_id": chart_data.chart_id,
                "chart_type": chart_data.chart_type,
                "html": chart_html,
                "cached_at": datetime.now().isoformat()
            }
            
            with gzip.open(cache_file, 'wb') as f:
                pickle.dump(cached_data, f)
            logger.info(f"Cached chart: {cache_file}")
        except Exception as e:
            logger.warning(f"Failed to cache chart {cache_file}: {e}")
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        total_charts = self.generation_stats["total_charts"]
        total_time = self.generation_stats["total_time"]
        
        return {
            **self.generation_stats,
            "average_generation_time": total_time / max(1, total_charts),
            "cache_hit_rate": (
                self.generation_stats["cache_hits"] / 
                max(1, self.generation_stats["cache_hits"] + self.generation_stats["cache_misses"])
            ),
            "charts_per_second": total_charts / max(1, total_time),
            "memory_usage_mb": self.generation_stats["memory_usage"] / 1024 / 1024
        }
    
    def clear_cache(self):
        """Clear all cached charts."""
        try:
            for cache_file in self.cache_dir.glob("*.pkl.gz"):
                cache_file.unlink()
            logger.info("✅ Chart cache cleared")
        except Exception as e:
            logger.error(f"Error clearing chart cache: {e}")
    
    def __del__(self):
        """Cleanup on destruction."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)


# Global instance for easy access
performance_chart_generator = PerformanceOptimizedChartGenerator()
