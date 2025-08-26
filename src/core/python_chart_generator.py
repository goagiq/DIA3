"""
Python Chart Generator

Pure Python chart generation system using Plotly for static HTML output.
Replaces JavaScript charts with Python-generated static charts for offline compatibility.

Features:
- Plotly static chart generation
- Multiple chart types (line, bar, scatter, pie, etc.)
- Responsive design
- Offline viewing capability
- Fast performance with large datasets
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from datetime import datetime
import logging
from dataclasses import dataclass, field

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class ChartConfig:
    """Configuration for chart generation."""
    chart_type: str = "line"  # line, bar, scatter, pie, histogram, etc.
    title: str = ""
    x_label: str = ""
    y_label: str = ""
    width: int = 800
    height: int = 500
    template: str = "plotly_white"
    show_legend: bool = True
    responsive: bool = True
    static_output: bool = True
    include_plotlyjs: bool = False  # For smaller file size


@dataclass
class ChartData:
    """Data structure for chart content."""
    chart_id: str
    config: ChartConfig
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class PythonChartGenerator:
    """Python-based chart generator with no JavaScript dependencies."""
    
    def __init__(self, output_dir: str = "Results/charts"):
        """Initialize the Python chart generator.
        
        Args:
            output_dir: Directory for generated chart files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Chart templates
        self.chart_templates = {
            'default': ChartConfig(),
            'executive': ChartConfig(
                template="plotly_white",
                width=1000,
                height=600,
                show_legend=True
            ),
            'dashboard': ChartConfig(
                template="plotly_dark",
                width=600,
                height=400,
                show_legend=False
            ),
            'presentation': ChartConfig(
                template="simple_white",
                width=1200,
                height=700,
                show_legend=True
            )
        }
        
        # Chart type handlers
        self.chart_handlers = {
            'line': self._create_line_chart,
            'bar': self._create_bar_chart,
            'scatter': self._create_scatter_chart,
            'pie': self._create_pie_chart,
            'histogram': self._create_histogram,
            'box': self._create_box_chart,
            'heatmap': self._create_heatmap,
            'area': self._create_area_chart,
            'bubble': self._create_bubble_chart,
            'funnel': self._create_funnel_chart
        }
        
        logger.info("✅ Python Chart Generator initialized successfully")
    
    def add_chart_template(self, name: str, config: ChartConfig):
        """Add a custom chart template."""
        self.chart_templates[name] = config
        logger.info(f"✅ Added custom chart template: {name}")
    
    async def generate_charts_html(self, modules_data: List[Dict[str, Any]]) -> str:
        """Generate HTML for all charts in the modules.
        
        Args:
            modules_data: List of processed module data
            
        Returns:
            HTML string containing all charts
        """
        charts_html_parts = []
        
        for module in modules_data:
            if module.get('chart_data'):
                module_charts = await self._generate_module_charts(module)
                if module_charts:
                    charts_html_parts.append(module_charts)
        
        combined_html = "\n".join(charts_html_parts)
        logger.info(f"✅ Generated charts HTML for {len(modules_data)} modules")
        
        return combined_html
    
    async def _generate_module_charts(self, module: Dict[str, Any]) -> str:
        """Generate charts for a specific module."""
        module_id = module['id']
        chart_data = module.get('chart_data', {})
        
        if not chart_data:
            return ""
        
        charts_html_parts = []
        
        for chart_id, chart_info in chart_data.items():
            try:
                # Create chart configuration
                config = self._create_chart_config(chart_info)
                
                # Create chart data structure
                chart_data_obj = ChartData(
                    chart_id=f"{module_id}_{chart_id}",
                    config=config,
                    data=chart_info.get('data', {}),
                    metadata=chart_info.get('metadata', {})
                )
                
                # Generate chart HTML
                chart_html = await self._generate_single_chart(chart_data_obj)
                if chart_html:
                    charts_html_parts.append(chart_html)
                
            except Exception as e:
                logger.error(f"Failed to generate chart {chart_id} for module {module_id}: {e}")
                continue
        
        return "\n".join(charts_html_parts)
    
    def _create_chart_config(self, chart_info: Dict[str, Any]) -> ChartConfig:
        """Create chart configuration from chart info."""
        # Get template
        template_name = chart_info.get('template', 'default')
        base_config = self.chart_templates.get(template_name, self.chart_templates['default'])
        
        # Override with chart-specific settings
        config = ChartConfig(
            chart_type=chart_info.get('type', base_config.chart_type),
            title=chart_info.get('title', base_config.title),
            x_label=chart_info.get('x_label', base_config.x_label),
            y_label=chart_info.get('y_label', base_config.y_label),
            width=chart_info.get('width', base_config.width),
            height=chart_info.get('height', base_config.height),
            template=chart_info.get('template', base_config.template),
            show_legend=chart_info.get('show_legend', base_config.show_legend),
            responsive=chart_info.get('responsive', base_config.responsive),
            static_output=chart_info.get('static_output', base_config.static_output),
            include_plotlyjs=chart_info.get('include_plotlyjs', base_config.include_plotlyjs)
        )
        
        return config
    
    async def _generate_single_chart(self, chart_data: ChartData) -> str:
        """Generate HTML for a single chart."""
        try:
            # Get chart handler
            chart_type = chart_data.config.chart_type
            handler = self.chart_handlers.get(chart_type)
            
            if not handler:
                logger.warning(f"Unknown chart type: {chart_type}")
                return ""
            
            # Create chart figure
            fig = await handler(chart_data)
            
            if fig is None:
                return ""
            
            # Configure layout
            fig.update_layout(
                title=chart_data.config.title,
                xaxis_title=chart_data.config.x_label,
                yaxis_title=chart_data.config.y_label,
                template=chart_data.config.template,
                showlegend=chart_data.config.show_legend,
                width=chart_data.config.width,
                height=chart_data.config.height
            )
            
            # Generate HTML
            html = fig.to_html(
                include_plotlyjs=chart_data.config.include_plotlyjs,
                full_html=False,
                config={'displayModeBar': False}  # Hide plotly toolbar
            )
            
            # Wrap in container
            container_html = f"""
            <div class="chart-container" id="chart-{chart_data.chart_id}">
                <div class="chart-wrapper">
                    {html}
                </div>
            </div>
            """
            
            return container_html
            
        except Exception as e:
            logger.error(f"Failed to generate chart {chart_data.chart_id}: {e}")
            return ""
    
    async def _create_line_chart(self, chart_data: ChartData) -> Optional[go.Figure]:
        """Create a line chart."""
        data = chart_data.data
        
        if 'x' not in data or 'y' not in data:
            return None
        
        fig = go.Figure()
        
        # Handle multiple series
        if isinstance(data['y'], list) and len(data['y']) > 0 and isinstance(data['y'][0], list):
            # Multiple series
            for i, y_series in enumerate(data['y']):
                name = data.get('names', [f'Series {i+1}'])[i] if 'names' in data else f'Series {i+1}'
                fig.add_trace(go.Scatter(
                    x=data['x'],
                    y=y_series,
                    mode='lines+markers',
                    name=name
                ))
        else:
            # Single series
            fig.add_trace(go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='lines+markers'
            ))
        
        return fig
    
    async def _create_bar_chart(self, chart_data: ChartData) -> Optional[go.Figure]:
        """Create a bar chart."""
        data = chart_data.data
        
        if 'x' not in data or 'y' not in data:
            return None
        
        fig = go.Figure()
        
        # Handle multiple series
        if isinstance(data['y'], list) and len(data['y']) > 0 and isinstance(data['y'][0], list):
            # Multiple series
            for i, y_series in enumerate(data['y']):
                name = data.get('names', [f'Series {i+1}'])[i] if 'names' in data else f'Series {i+1}'
                fig.add_trace(go.Bar(
                    x=data['x'],
                    y=y_series,
                    name=name
                ))
        else:
            # Single series
            fig.add_trace(go.Bar(
                x=data['x'],
                y=data['y']
            ))
        
        return fig
    
    async def _create_scatter_chart(self, chart_data: ChartData) -> Optional[go.Figure]:
        """Create a scatter chart."""
        data = chart_data.data
        
        if 'x' not in data or 'y' not in data:
            return None
        
        fig = go.Figure()
        
        # Handle multiple series
        if isinstance(data['y'], list) and len(data['y']) > 0 and isinstance(data['y'][0], list):
            # Multiple series
            for i, y_series in enumerate(data['y']):
                name = data.get('names', [f'Series {i+1}'])[i] if 'names' in data else f'Series {i+1}'
                fig.add_trace(go.Scatter(
                    x=data['x'],
                    y=y_series,
                    mode='markers',
                    name=name
                ))
        else:
            # Single series
            fig.add_trace(go.Scatter(
                x=data['x'],
                y=data['y'],
                mode='markers'
            ))
        
        return fig
    
    async def _create_pie_chart(self, chart_data: ChartData) -> Optional[go.Figure]:
        """Create a pie chart."""
        data = chart_data.data
        
        if 'values' not in data or 'labels' not in data:
            return None
        
        fig = go.Figure(data=[go.Pie(
            labels=data['labels'],
            values=data['values']
        )])
        
        return fig
    
    async def _create_histogram(self, chart_data: ChartData) -> Optional[go.Figure]:
        """Create a histogram."""
        data = chart_data.data
        
        if 'x' not in data:
            return None
        
        fig = go.Figure(data=[go.Histogram(x=data['x'])])
        
        return fig
    
    async def _create_box_chart(self, chart_data: ChartData) -> Optional[go.Figure]:
        """Create a box chart."""
        data = chart_data.data
        
        if 'y' not in data:
            return None
        
        fig = go.Figure()
        
        # Handle multiple series
        if isinstance(data['y'], list) and len(data['y']) > 0 and isinstance(data['y'][0], list):
            # Multiple series
            for i, y_series in enumerate(data['y']):
                name = data.get('names', [f'Series {i+1}'])[i] if 'names' in data else f'Series {i+1}'
                fig.add_trace(go.Box(y=y_series, name=name))
        else:
            # Single series
            fig.add_trace(go.Box(y=data['y']))
        
        return fig
    
    async def _create_heatmap(self, chart_data: ChartData) -> Optional[go.Figure]:
        """Create a heatmap."""
        data = chart_data.data
        
        if 'z' not in data:
            return None
        
        fig = go.Figure(data=go.Heatmap(
            z=data['z'],
            x=data.get('x', None),
            y=data.get('y', None)
        ))
        
        return fig
    
    async def _create_area_chart(self, chart_data: ChartData) -> Optional[go.Figure]:
        """Create an area chart."""
        data = chart_data.data
        
        if 'x' not in data or 'y' not in data:
            return None
        
        fig = go.Figure()
        
        # Handle multiple series
        if isinstance(data['y'], list) and len(data['y']) > 0 and isinstance(data['y'][0], list):
            # Multiple series
            for i, y_series in enumerate(data['y']):
                name = data.get('names', [f'Series {i+1}'])[i] if 'names' in data else f'Series {i+1}'
                fig.add_trace(go.Scatter(
                    x=data['x'],
                    y=y_series,
                    fill='tonexty',
                    name=name
                ))
        else:
            # Single series
            fig.add_trace(go.Scatter(
                x=data['x'],
                y=data['y'],
                fill='tonexty'
            ))
        
        return fig
    
    async def _create_bubble_chart(self, chart_data: ChartData) -> Optional[go.Figure]:
        """Create a bubble chart."""
        data = chart_data.data
        
        if 'x' not in data or 'y' not in data or 'size' not in data:
            return None
        
        fig = go.Figure(data=[go.Scatter(
            x=data['x'],
            y=data['y'],
            mode='markers',
            marker=dict(
                size=data['size'],
                sizemode='area',
                sizeref=2.*max(data['size'])/(40.**2),
                sizemin=4
            )
        )])
        
        return fig
    
    async def _create_funnel_chart(self, chart_data: ChartData) -> Optional[go.Figure]:
        """Create a funnel chart."""
        data = chart_data.data
        
        if 'values' not in data or 'labels' not in data:
            return None
        
        fig = go.Figure(data=[go.Funnel(
            y=data['labels'],
            x=data['values']
        )])
        
        return fig
    
    def create_sample_data(self, chart_type: str) -> Dict[str, Any]:
        """Create sample data for testing charts."""
        if chart_type == 'line':
            return {
                'x': list(range(1, 11)),
                'y': [i * 2 + np.random.normal(0, 1) for i in range(1, 11)],
                'names': ['Sample Data']
            }
        elif chart_type == 'bar':
            return {
                'x': ['A', 'B', 'C', 'D', 'E'],
                'y': [10, 20, 15, 25, 30]
            }
        elif chart_type == 'pie':
            return {
                'labels': ['A', 'B', 'C', 'D'],
                'values': [25, 30, 20, 25]
            }
        elif chart_type == 'scatter':
            return {
                'x': np.random.normal(0, 1, 50),
                'y': np.random.normal(0, 1, 50)
            }
        else:
            return {
                'x': list(range(1, 11)),
                'y': [i * 2 for i in range(1, 11)]
            }
    
    def get_chart_generator_info(self) -> Dict[str, Any]:
        """Get information about the chart generator capabilities."""
        return {
            'name': 'Python Chart Generator',
            'version': '1.0.0',
            'supported_chart_types': list(self.chart_handlers.keys()),
            'templates': list(self.chart_templates.keys()),
            'features': [
                'Pure Python implementation',
                'Static HTML output',
                'No JavaScript dependencies',
                'Responsive design',
                'Offline viewing capability',
                'Fast performance',
                'Multiple chart types'
            ],
            'dependencies': ['plotly', 'pandas', 'numpy']
        }


# Convenience functions for quick chart creation
async def create_line_chart(data: Dict[str, Any], title: str = "Line Chart") -> str:
    """Create a quick line chart."""
    generator = PythonChartGenerator()
    chart_data = ChartData(
        chart_id="quick_line",
        config=ChartConfig(chart_type="line", title=title),
        data=data
    )
    return await generator._generate_single_chart(chart_data)


async def create_bar_chart(data: Dict[str, Any], title: str = "Bar Chart") -> str:
    """Create a quick bar chart."""
    generator = PythonChartGenerator()
    chart_data = ChartData(
        chart_id="quick_bar",
        config=ChartConfig(chart_type="bar", title=title),
        data=data
    )
    return await generator._generate_single_chart(chart_data)


async def create_pie_chart(data: Dict[str, Any], title: str = "Pie Chart") -> str:
    """Create a quick pie chart."""
    generator = PythonChartGenerator()
    chart_data = ChartData(
        chart_id="quick_pie",
        config=ChartConfig(chart_type="pie", title=title),
        data=data
    )
    return await generator._generate_single_chart(chart_data)


if __name__ == "__main__":
    # Example usage
    async def main():
        generator = PythonChartGenerator()
        
        # Create sample line chart
        sample_data = generator.create_sample_data('line')
        chart_html = await create_line_chart(sample_data, "Sample Line Chart")
        print("Generated line chart HTML:")
        print(chart_html[:500] + "..." if len(chart_html) > 500 else chart_html)
        
        # Create sample bar chart
        bar_data = generator.create_sample_data('bar')
        bar_html = await create_bar_chart(bar_data, "Sample Bar Chart")
        print("\nGenerated bar chart HTML:")
        print(bar_html[:500] + "..." if len(bar_html) > 500 else bar_html)
    
    asyncio.run(main())
