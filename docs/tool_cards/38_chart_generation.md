# Chart Generation Tool

## Overview
The Chart Generation tool provides specialized capabilities for creating high-quality, publication-ready charts and graphs with advanced customization options, supporting multiple chart types and export formats for professional presentations and reports.

## Purpose
To generate professional-grade charts and graphs with precise control over styling, formatting, and output quality for use in reports, presentations, publications, and data visualization projects.

## Required Libraries

### Core Libraries
- **matplotlib** (>=3.7.0) - Core plotting and chart generation
- **seaborn** (>=0.12.0) - Statistical chart styling and themes
- **plotly** (>=5.15.0) - Interactive chart generation
- **bokeh** (>=3.1.0) - Web-based chart creation
- **altair** (>=5.0.0) - Declarative chart specification

### Optional Libraries
- **pygal** (>=2.4.0) - SVG chart generation
- **ggplot** (>=0.11.0) - Grammar of graphics implementation
- **holoviews** (>=1.17.0) - High-level plotting interface
- **datashader** (>=0.16.0) - Large dataset visualization
- **bqplot** (>=0.12.0) - Interactive plotting for Jupyter
- **pyecharts** (>=2.0.0) - ECharts Python interface
- **chart-studio** (>=1.1.0) - Plotly chart hosting
- **kaleido** (>=0.2.1) - Static image export for Plotly
- **pillow** (>=9.5.0) - Image processing and manipulation
- **svgwrite** (>=1.4.0) - SVG file generation

## Input Schema
```json
{
  "type": "object",
  "properties": {
    "chart_config": {
      "type": "object",
      "properties": {
        "chart_type": {
          "type": "string",
          "enum": ["line", "bar", "scatter", "histogram", "box", "violin", "heatmap", "pie", "area", "bubble", "radar", "funnel", "gantt", "candlestick", "waterfall"],
          "description": "Type of chart to generate"
        },
        "data_source": {
          "type": "string",
          "description": "Path to data file or database connection string"
        },
        "data_mapping": {
          "type": "object",
          "properties": {
            "x_axis": {"type": "string"},
            "y_axis": {"type": "string"},
            "color": {"type": "string"},
            "size": {"type": "string"},
            "facet": {"type": "string"},
            "group": {"type": "string"},
            "text": {"type": "string"}
          }
        },
        "styling": {
          "type": "object",
          "properties": {
            "title": {"type": "string"},
            "subtitle": {"type": "string"},
            "x_label": {"type": "string"},
            "y_label": {"type": "string"},
            "color_scheme": {"type": "string"},
            "theme": {"type": "string"},
            "figure_size": {
              "type": "object",
              "properties": {
                "width": {"type": "integer"},
                "height": {"type": "integer"}
              }
            },
            "font_family": {"type": "string"},
            "font_size": {"type": "integer"},
            "background_color": {"type": "string"},
            "grid_style": {"type": "string"}
          }
        },
        "annotations": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": {"type": "string"},
              "x": {"type": "number"},
              "y": {"type": "number"},
              "text": {"type": "string"},
              "style": {"type": "object"}
            }
          }
        },
        "legend": {
          "type": "object",
          "properties": {
            "show": {"type": "boolean"},
            "position": {"type": "string"},
            "orientation": {"type": "string"},
            "title": {"type": "string"}
          }
        }
      }
    },
    "output_config": {
      "type": "object",
      "properties": {
        "format": {
          "type": "string",
          "enum": ["png", "svg", "pdf", "jpg", "tiff", "html", "json"],
          "description": "Output format for the chart"
        },
        "dpi": {"type": "integer"},
        "transparent": {"type": "boolean"},
        "bbox_inches": {"type": "string"},
        "pad_inches": {"type": "number"}
      }
    },
    "interactivity": {
      "type": "object",
      "properties": {
        "tooltips": {"type": "boolean"},
        "hover": {"type": "boolean"},
        "zoom": {"type": "boolean"},
        "pan": {"type": "boolean"},
        "click_events": {"type": "boolean"}
      }
    }
  },
  "required": ["chart_config"]
}
```

## Output Schema
```json
{
  "type": "object",
  "properties": {
    "chart_file": {
      "type": "string",
      "description": "Path to the generated chart file"
    },
    "chart_metadata": {
      "type": "object",
      "properties": {
        "chart_type": {"type": "string"},
        "data_points": {"type": "integer"},
        "dimensions": {
          "type": "object",
          "properties": {
            "width": {"type": "integer"},
            "height": {"type": "integer"}
          }
        },
        "file_size": {"type": "string"},
        "format": {"type": "string"},
        "dpi": {"type": "integer"},
        "generation_time": {"type": "string"}
      }
    },
    "data_summary": {
      "type": "object",
      "properties": {
        "total_records": {"type": "integer"},
        "columns_used": {
          "type": "array",
          "items": {"type": "string"}
        },
        "data_range": {
          "type": "object",
          "properties": {
            "x_min": {"type": "number"},
            "x_max": {"type": "number"},
            "y_min": {"type": "number"},
            "y_max": {"type": "number"}
          }
        },
        "statistics": {
          "type": "object",
          "additionalProperties": true
        }
      }
    },
    "interactive_url": {
      "type": "string",
      "description": "URL for interactive chart (if applicable)"
    },
    "processing_time": {
      "type": "number",
      "description": "Time taken for chart generation in seconds"
    }
  }
}
```

## Intended Use
- **Publication Charts**: Create high-quality charts for academic papers and publications
- **Business Presentations**: Generate professional charts for executive presentations
- **Report Generation**: Create standardized charts for automated reports
- **Data Visualization**: Produce clear and informative data visualizations
- **Interactive Dashboards**: Generate interactive charts for web applications
- **Print Media**: Create print-ready charts for magazines and books
- **Web Graphics**: Generate optimized charts for web display
- **Mobile Applications**: Create responsive charts for mobile apps

## Limitations
- Complex chart types may require significant processing time
- Large datasets may need aggregation for optimal performance
- Some advanced styling options may not be available in all formats
- Interactive features may have browser compatibility limitations

## Safety
- Validate data before chart generation to prevent misleading visualizations
- Ensure proper data privacy when creating charts with sensitive information
- Consider accessibility requirements for color schemes and text
- Handle missing or invalid data appropriately

## Runbook

### Setup
1. **Install Dependencies**:
   ```bash
   pip install matplotlib seaborn plotly bokeh altair pygal holoviews
   ```

2. **Verify Installation**:
   ```python
   import matplotlib.pyplot as plt
   import seaborn as sns
   import plotly.express as px
   import plotly.graph_objects as go
   import bokeh.plotting as bk
   import altair as alt
   ```

3. **Configure Chart Environment**:
   - Set up plotting backends
   - Configure default styles and themes
   - Set up font configurations

### Usage

#### Basic Chart Generation
```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load data
df = pd.read_csv("data.csv")

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create chart
fig, ax = plt.subplots(figsize=(12, 8))

# Generate chart based on type
chart_type = "line"
if chart_type == "line":
    sns.lineplot(data=df, x='x_column', y='y_column', hue='category', ax=ax)
elif chart_type == "bar":
    sns.barplot(data=df, x='x_column', y='y_column', hue='category', ax=ax)
elif chart_type == "scatter":
    sns.scatterplot(data=df, x='x_column', y='y_column', hue='category', size='size_column', ax=ax)

# Customize chart
ax.set_title('Chart Title', fontsize=16, fontweight='bold')
ax.set_xlabel('X Axis Label', fontsize=12)
ax.set_ylabel('Y Axis Label', fontsize=12)
ax.legend(title='Category', title_fontsize=12)

# Save chart
plt.tight_layout()
plt.savefig('chart.png', dpi=300, bbox_inches='tight', transparent=False)
plt.close()
```

#### Advanced Chart with Plotly
```python
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Load data
df = pd.read_csv("data.csv")

# Create advanced chart
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Line Chart', 'Bar Chart', 'Scatter Plot', 'Histogram'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}]]
)

# Add traces
fig.add_trace(
    go.Scatter(x=df['x_column'], y=df['y_column'], mode='lines+markers', name='Line'),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=df['category'], y=df['value'], name='Bar'),
    row=1, col=2
)

fig.add_trace(
    go.Scatter(x=df['x_column'], y=df['y_column'], mode='markers', name='Scatter'),
    row=2, col=1
)

fig.add_trace(
    go.Histogram(x=df['value'], name='Histogram'),
    row=2, col=2
)

# Update layout
fig.update_layout(
    title_text="Multi-Chart Dashboard",
    showlegend=True,
    height=800,
    template="plotly_white"
)

# Save chart
fig.write_html("interactive_chart.html")
fig.write_image("static_chart.png", width=1200, height=800)
```

#### Professional Publication Chart
```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set publication-quality style
plt.style.use('default')
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# Load data
df = pd.read_csv("research_data.csv")

# Create figure with subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# Chart 1: Line plot with confidence intervals
sns.lineplot(data=df, x='time', y='value', hue='group', ax=ax1)
ax1.set_title('Time Series Analysis', fontweight='bold', fontsize=14)
ax1.set_xlabel('Time (days)')
ax1.set_ylabel('Value')

# Chart 2: Box plot
sns.boxplot(data=df, x='category', y='value', ax=ax2)
ax2.set_title('Distribution by Category', fontweight='bold', fontsize=14)
ax2.set_xlabel('Category')
ax2.set_ylabel('Value')

# Chart 3: Correlation heatmap
correlation_matrix = df[['value1', 'value2', 'value3', 'value4']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax3)
ax3.set_title('Correlation Matrix', fontweight='bold', fontsize=14)

# Chart 4: Scatter plot with regression
sns.regplot(data=df, x='x_value', y='y_value', ax=ax4, scatter_kws={'alpha':0.6})
ax4.set_title('Regression Analysis', fontweight='bold', fontsize=14)
ax4.set_xlabel('X Value')
ax4.set_ylabel('Y Value')

# Adjust layout
plt.tight_layout()

# Save publication-quality chart
plt.savefig('publication_chart.pdf', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.savefig('publication_chart.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.close()
```

#### Interactive Dashboard Chart
```python
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Initialize Dash app
app = dash.Dash(__name__)

# Load data
df = pd.read_csv("dashboard_data.csv")

# Define layout
app.layout = html.Div([
    html.H1("Interactive Chart Dashboard"),
    
    # Controls
    html.Div([
        dcc.Dropdown(
            id='chart-type',
            options=[
                {'label': 'Line Chart', 'value': 'line'},
                {'label': 'Bar Chart', 'value': 'bar'},
                {'label': 'Scatter Plot', 'value': 'scatter'},
                {'label': 'Heatmap', 'value': 'heatmap'}
            ],
            value='line'
        ),
        dcc.DatePickerRange(
            id='date-range',
            start_date=df['date'].min(),
            end_date=df['date'].max()
        )
    ]),
    
    # Chart
    dcc.Graph(id='interactive-chart')
])

# Callback to update chart
@app.callback(
    Output('interactive-chart', 'figure'),
    [Input('chart-type', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_chart(chart_type, start_date, end_date):
    # Filter data
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    if chart_type == 'line':
        fig = px.line(filtered_df, x='date', y='value', color='category',
                     title='Time Series Chart')
    elif chart_type == 'bar':
        fig = px.bar(filtered_df, x='category', y='value',
                    title='Bar Chart')
    elif chart_type == 'scatter':
        fig = px.scatter(filtered_df, x='x_value', y='y_value', color='category',
                        title='Scatter Plot')
    elif chart_type == 'heatmap':
        pivot_table = filtered_df.pivot_table(values='value', 
                                            index='category', 
                                            columns='date', 
                                            aggfunc='mean')
        fig = px.imshow(pivot_table, title='Heatmap')
    
    fig.update_layout(
        template="plotly_white",
        height=600
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
```

### Error Handling

#### Common Issues
1. **Data Format Errors**: Handle incorrect data types and missing values
2. **Memory Issues**: Manage large datasets with sampling or aggregation
3. **Styling Conflicts**: Resolve conflicting style configurations
4. **Export Errors**: Handle format-specific export issues

#### Troubleshooting
```python
# Handle data format errors
def prepare_data_for_chart(df):
    """Prepare data for chart generation"""
    try:
        # Convert date columns
        date_columns = df.select_dtypes(include=['object']).columns
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass
        
        # Handle missing values
        df = df.dropna(subset=['x_column', 'y_column'])
        
        # Convert numeric columns
        numeric_columns = ['x_column', 'y_column']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    except Exception as e:
        print(f"Data preparation error: {e}")
        return pd.DataFrame()

# Handle memory issues
def create_chart_large_data(df, sample_size=10000):
    """Create chart for large datasets"""
    if len(df) > sample_size:
        df_sample = df.sample(n=sample_size, random_state=42)
    else:
        df_sample = df
    
    return create_chart(df_sample)

# Handle export errors
def safe_chart_export(fig, filename, format='png'):
    """Safely export chart in various formats"""
    try:
        if format == 'png':
            fig.write_image(filename, width=1200, height=800)
        elif format == 'svg':
            fig.write_image(filename, format='svg')
        elif format == 'pdf':
            fig.write_image(filename, format='pdf')
        elif format == 'html':
            fig.write_html(filename)
        else:
            print(f"Unsupported format: {format}")
    except Exception as e:
        print(f"Export error: {e}")
        # Fallback to PNG
        try:
            fig.write_image(f"{filename}.png")
        except:
            print("Fallback export also failed")
```

### Monitoring
- Monitor chart generation performance and success rates
- Track chart file sizes and storage usage
- Monitor interactive chart usage and engagement
- Alert on chart generation failures

### Best Practices
1. **Choose Appropriate Chart Types**: Select charts that best represent your data
2. **Use Consistent Styling**: Maintain consistent colors, fonts, and themes
3. **Optimize for Performance**: Use sampling for large datasets
4. **Ensure Accessibility**: Use colorblind-friendly palettes and clear labels
5. **Add Context**: Include titles, labels, legends, and annotations
6. **Test Interactivity**: Verify interactive features work correctly
7. **Optimize File Sizes**: Balance quality with file size for web use
8. **Version Control**: Track chart configurations and data sources
