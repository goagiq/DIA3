# Infographic Creation Tool

## Overview
The Infographic Creation tool provides comprehensive capabilities for designing and generating professional infographics that combine data visualization, text, icons, and graphics to create compelling visual narratives for communication and storytelling.

## Purpose
To create engaging, informative infographics that effectively communicate complex information, data insights, and stories through visual design, making information more accessible and memorable for target audiences.

## Required Libraries

### Core Libraries
- **pillow** (>=9.5.0) - Image processing and manipulation
- **matplotlib** (>=3.7.0) - Data visualization and chart generation
- **seaborn** (>=0.12.0) - Statistical visualization styling
- **plotly** (>=5.15.0) - Interactive chart generation
- **reportlab** (>=4.0.0) - PDF generation and layout

### Optional Libraries
- **cairosvg** (>=2.7.0) - SVG to image conversion
- **svgwrite** (>=1.4.0) - SVG file generation
- **wordcloud** (>=1.9.0) - Text visualization
- **folium** (>=0.14.0) - Map visualization
- **geopandas** (>=0.12.0) - Geospatial data visualization
- **networkx** (>=3.1.0) - Network visualization
- **pygal** (>=2.4.0) - SVG charts and graphs
- **bokeh** (>=3.1.0) - Interactive web-based visualizations
- **jinja2** (>=3.1.0) - Template engine for infographic generation
- **weasyprint** (>=60.0) - HTML to image conversion

## Input Schema
```json
{
  "type": "object",
  "properties": {
    "infographic_config": {
      "type": "object",
      "properties": {
        "metadata": {
          "type": "object",
          "properties": {
            "title": {"type": "string"},
            "subtitle": {"type": "string"},
            "description": {"type": "string"},
            "author": {"type": "string"},
            "version": {"type": "string"},
            "theme": {
              "type": "string",
              "enum": ["business", "scientific", "creative", "minimal", "bold", "elegant"]
            }
          }
        },
        "layout": {
          "type": "object",
          "properties": {
            "layout_type": {
              "type": "string",
              "enum": ["vertical", "horizontal", "grid", "flow", "timeline", "comparison"]
            },
            "dimensions": {
              "type": "object",
              "properties": {
                "width": {"type": "integer"},
                "height": {"type": "integer"}
              }
            },
            "background": {
              "type": "object",
              "properties": {
                "color": {"type": "string"},
                "image": {"type": "string"},
                "gradient": {"type": "object"}
              }
            }
          }
        },
        "sections": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "section_id": {"type": "string"},
              "section_type": {
                "type": "string",
                "enum": ["header", "text", "chart", "image", "icon", "statistic", "timeline", "comparison", "process", "map"]
              },
              "position": {
                "type": "object",
                "properties": {
                  "x": {"type": "number"},
                  "y": {"type": "number"},
                  "width": {"type": "number"},
                  "height": {"type": "number"}
                }
              },
              "content": {
                "type": "object",
                "additionalProperties": true
              },
              "styling": {
                "type": "object",
                "properties": {
                  "font_family": {"type": "string"},
                  "font_size": {"type": "integer"},
                  "color": {"type": "string"},
                  "background_color": {"type": "string"},
                  "border": {"type": "object"},
                  "shadow": {"type": "object"}
                }
              }
            }
          }
        },
        "color_scheme": {
          "type": "object",
          "properties": {
            "primary_color": {"type": "string"},
            "secondary_color": {"type": "string"},
            "accent_colors": {
              "type": "array",
              "items": {"type": "string"}
            },
            "text_color": {"type": "string"},
            "background_color": {"type": "string"}
          }
        },
        "typography": {
          "type": "object",
          "properties": {
            "heading_font": {"type": "string"},
            "body_font": {"type": "string"},
            "heading_sizes": {
              "type": "object",
              "properties": {
                "h1": {"type": "integer"},
                "h2": {"type": "integer"},
                "h3": {"type": "integer"}
              }
            },
            "body_size": {"type": "integer"},
            "line_height": {"type": "number"}
          }
        }
      }
    },
    "data_sources": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "source_id": {"type": "string"},
          "source_type": {
            "type": "string",
            "enum": ["csv", "json", "database", "api", "image"]
          },
          "source_path": {"type": "string"},
          "data_mapping": {"type": "object"}
        }
      }
    },
    "output_config": {
      "type": "object",
      "properties": {
        "format": {
          "type": "string",
          "enum": ["png", "jpg", "pdf", "svg", "html"],
          "description": "Output format for the infographic"
        },
        "quality": {"type": "integer"},
        "dpi": {"type": "integer"},
        "compression": {"type": "boolean"}
      }
    }
  },
  "required": ["infographic_config"]
}
```

## Output Schema
```json
{
  "type": "object",
  "properties": {
    "infographic_file": {
      "type": "string",
      "description": "Path to the generated infographic file"
    },
    "infographic_metadata": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "dimensions": {
          "type": "object",
          "properties": {
            "width": {"type": "integer"},
            "height": {"type": "integer"}
          }
        },
        "format": {"type": "string"},
        "file_size": {"type": "string"},
        "sections_count": {"type": "integer"},
        "charts_count": {"type": "integer"},
        "images_count": {"type": "integer"},
        "generation_time": {"type": "string"}
      }
    },
    "content_summary": {
      "type": "object",
      "properties": {
        "total_text_length": {"type": "integer"},
        "data_points_visualized": {"type": "integer"},
        "sources_used": {
          "type": "array",
          "items": {"type": "string"}
        },
        "color_palette": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    },
    "interactive_url": {
      "type": "string",
      "description": "URL for interactive infographic (if applicable)"
    },
    "processing_time": {
      "type": "number",
      "description": "Time taken for infographic generation in seconds"
    }
  }
}
```

## Intended Use
- **Data Storytelling**: Create compelling visual narratives from data insights
- **Educational Content**: Design educational infographics for learning materials
- **Marketing Materials**: Generate marketing infographics for campaigns
- **Research Communication**: Create research summaries and findings visualizations
- **Process Documentation**: Design process flow and workflow infographics
- **Comparison Analysis**: Create comparison and benchmarking infographics
- **Timeline Visualization**: Design historical and project timeline infographics
- **Geographic Data**: Create location-based and mapping infographics

## Limitations
- Complex layouts may require significant processing time
- Large datasets may need aggregation for optimal performance
- Some advanced design features may be limited by the output format
- Interactive features may have browser compatibility limitations

## Safety
- Ensure proper attribution for data sources and images
- Validate data accuracy before creating infographics
- Consider copyright and licensing for visual elements
- Handle sensitive information appropriately in public infographics

## Runbook

### Setup
1. **Install Dependencies**:
   ```bash
   pip install pillow matplotlib seaborn plotly reportlab cairosvg wordcloud
   ```

2. **Verify Installation**:
   ```python
   from PIL import Image, ImageDraw, ImageFont
   import matplotlib.pyplot as plt
   import seaborn as sns
   import plotly.express as px
   from reportlab.pdfgen import canvas
   from reportlab.lib.pagesizes import letter, A4
   ```

3. **Configure Infographic Environment**:
   - Set up font directories
   - Configure image processing settings
   - Set up template directories

### Usage

#### Basic Infographic Creation
```python
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import pandas as pd

def create_basic_infographic(data, title, output_path):
    """Create a basic infographic with title and data visualization"""
    
    # Create canvas
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        body_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    # Draw title
    draw.text((50, 50), title, fill='black', font=title_font)
    
    # Create chart
    fig, ax = plt.subplots(figsize=(10, 6))
    if isinstance(data, pd.DataFrame):
        data.plot(kind='bar', ax=ax)
    else:
        ax.bar(range(len(data)), data)
    
    ax.set_title('Data Visualization')
    plt.tight_layout()
    
    # Save chart to temporary file
    chart_path = 'temp_chart.png'
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Add chart to infographic
    chart_img = Image.open(chart_path)
    chart_img = chart_img.resize((800, 500))
    img.paste(chart_img, (200, 150))
    
    # Add text elements
    draw.text((50, 700), "Source: Data Analysis", fill='gray', font=body_font)
    
    # Save infographic
    img.save(output_path, 'PNG', dpi=(300, 300))
    
    return output_path

# Usage example
data = [25, 30, 15, 20, 10]
create_basic_infographic(data, "Sample Infographic", "infographic.png")
```

#### Advanced Infographic with Multiple Sections
```python
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def create_advanced_infographic(config, output_path):
    """Create an advanced infographic with multiple sections"""
    
    # Create canvas
    width, height = config['dimensions']['width'], config['dimensions']['height']
    img = Image.new('RGB', (width, height), color=config['color_scheme']['background_color'])
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        heading_font = ImageFont.truetype("arial.ttf", 36)
        body_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    # Draw header
    header_y = 50
    draw.text((50, header_y), config['metadata']['title'], 
              fill=config['color_scheme']['primary_color'], font=title_font)
    
    if config['metadata']['subtitle']:
        draw.text((50, header_y + 80), config['metadata']['subtitle'], 
                  fill=config['color_scheme']['secondary_color'], font=heading_font)
    
    # Process sections
    current_y = header_y + 150
    
    for section in config['sections']:
        section_y = current_y + section['position']['y']
        
        if section['section_type'] == 'text':
            # Draw text section
            draw.text((section['position']['x'], section_y), 
                     section['content']['text'], 
                     fill=section['styling']['color'], 
                     font=body_font)
            
        elif section['section_type'] == 'statistic':
            # Draw statistic with icon
            stat_text = f"{section['content']['value']} {section['content']['unit']}"
            draw.text((section['position']['x'], section_y), 
                     stat_text, 
                     fill=section['styling']['color'], 
                     font=heading_font)
            
            # Draw label
            draw.text((section['position']['x'], section_y + 50), 
                     section['content']['label'], 
                     fill=section['styling']['color'], 
                     font=body_font)
            
        elif section['section_type'] == 'chart':
            # Create and add chart
            create_chart_section(section, img, section['position']['x'], section_y)
    
    # Save infographic
    img.save(output_path, 'PNG', dpi=(300, 300))
    return output_path

def create_chart_section(section_config, img, x, y):
    """Create a chart section for the infographic"""
    
    # Create chart based on data
    fig, ax = plt.subplots(figsize=(8, 6))
    
    data = section_config['content']['data']
    chart_type = section_config['content']['chart_type']
    
    if chart_type == 'bar':
        ax.bar(range(len(data)), data, color=section_config['styling']['color'])
    elif chart_type == 'pie':
        ax.pie(data, labels=section_config['content']['labels'])
    elif chart_type == 'line':
        ax.plot(data, color=section_config['styling']['color'])
    
    ax.set_title(section_config['content']['title'])
    plt.tight_layout()
    
    # Save chart
    chart_path = f'temp_chart_{section_config["section_id"]}.png'
    plt.savefig(chart_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    
    # Add to infographic
    chart_img = Image.open(chart_path)
    chart_img = chart_img.resize((section_config['position']['width'], 
                                 section_config['position']['height']))
    img.paste(chart_img, (x, y), chart_img if chart_img.mode == 'RGBA' else None)

# Usage example
config = {
    'metadata': {
        'title': 'Data Insights Report',
        'subtitle': 'Key Findings and Trends'
    },
    'dimensions': {'width': 1200, 'height': 1600},
    'color_scheme': {
        'primary_color': '#2E86AB',
        'secondary_color': '#A23B72',
        'background_color': '#F8F9FA'
    },
    'sections': [
        {
            'section_id': 'stat1',
            'section_type': 'statistic',
            'position': {'x': 50, 'y': 200},
            'content': {'value': '85%', 'unit': '', 'label': 'Customer Satisfaction'},
            'styling': {'color': '#2E86AB'}
        },
        {
            'section_id': 'chart1',
            'section_type': 'chart',
            'position': {'x': 400, 'y': 200, 'width': 600, 'height': 400},
            'content': {
                'data': [25, 30, 15, 20, 10],
                'chart_type': 'bar',
                'title': 'Monthly Performance'
            },
            'styling': {'color': '#A23B72'}
        }
    ]
}

create_advanced_infographic(config, 'advanced_infographic.png')
```

#### Timeline Infographic
```python
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def create_timeline_infographic(events, output_path):
    """Create a timeline infographic"""
    
    # Create canvas
    width, height = 1400, 800
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        date_font = ImageFont.truetype("arial.ttf", 20)
        event_font = ImageFont.truetype("arial.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        date_font = ImageFont.load_default()
        event_font = ImageFont.load_default()
    
    # Draw title
    draw.text((50, 50), "Project Timeline", fill='black', font=title_font)
    
    # Draw timeline line
    timeline_y = 200
    draw.line([(100, timeline_y), (width-100, timeline_y)], fill='gray', width=3)
    
    # Calculate date range
    dates = [datetime.strptime(event['date'], '%Y-%m-%d') for event in events]
    min_date = min(dates)
    max_date = max(dates)
    date_range = (max_date - min_date).days
    
    # Draw events
    for i, event in enumerate(events):
        event_date = datetime.strptime(event['date'], '%Y-%m-%d')
        days_from_start = (event_date - min_date).days
        x_position = 100 + (days_from_start / date_range) * (width - 200)
        
        # Draw event marker
        marker_size = 15
        draw.ellipse([x_position-marker_size, timeline_y-marker_size, 
                     x_position+marker_size, timeline_y+marker_size], 
                    fill='blue', outline='black')
        
        # Draw date
        draw.text((x_position-30, timeline_y+20), 
                 event['date'], fill='black', font=date_font)
        
        # Draw event description
        draw.text((x_position-50, timeline_y+50), 
                 event['description'], fill='black', font=event_font)
    
    # Save infographic
    img.save(output_path, 'PNG', dpi=(300, 300))
    return output_path

# Usage example
events = [
    {'date': '2023-01-15', 'description': 'Project Start'},
    {'date': '2023-03-20', 'description': 'Phase 1 Complete'},
    {'date': '2023-06-10', 'description': 'Phase 2 Complete'},
    {'date': '2023-09-30', 'description': 'Project Launch'}
]

create_timeline_infographic(events, 'timeline_infographic.png')
```

#### Comparison Infographic
```python
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import pandas as pd

def create_comparison_infographic(data1, data2, labels, output_path):
    """Create a comparison infographic"""
    
    # Create canvas
    width, height = 1200, 1000
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        heading_font = ImageFont.truetype("arial.ttf", 32)
        body_font = ImageFont.truetype("arial.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    # Draw title
    draw.text((50, 50), "Comparison Analysis", fill='black', font=title_font)
    
    # Create comparison chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    
    # Left side - Data 1
    ax1.bar(range(len(data1)), data1, color='blue', alpha=0.7)
    ax1.set_title(labels[0], fontsize=16)
    ax1.set_xticks(range(len(data1)))
    ax1.set_xticklabels([f'Item {i+1}' for i in range(len(data1))])
    
    # Right side - Data 2
    ax2.bar(range(len(data2)), data2, color='red', alpha=0.7)
    ax2.set_title(labels[1], fontsize=16)
    ax2.set_xticks(range(len(data2)))
    ax2.set_xticklabels([f'Item {i+1}' for i in range(len(data2))])
    
    plt.tight_layout()
    
    # Save chart
    chart_path = 'temp_comparison_chart.png'
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Add chart to infographic
    chart_img = Image.open(chart_path)
    chart_img = chart_img.resize((1000, 600))
    img.paste(chart_img, (100, 150))
    
    # Add summary statistics
    summary_y = 800
    draw.text((100, summary_y), f"Average {labels[0]}: {sum(data1)/len(data1):.2f}", 
              fill='blue', font=heading_font)
    draw.text((600, summary_y), f"Average {labels[1]}: {sum(data2)/len(data2):.2f}", 
              fill='red', font=heading_font)
    
    # Save infographic
    img.save(output_path, 'PNG', dpi=(300, 300))
    return output_path

# Usage example
data1 = [25, 30, 15, 20, 10]
data2 = [20, 35, 18, 22, 12]
labels = ['Before', 'After']

create_comparison_infographic(data1, data2, labels, 'comparison_infographic.png')
```

### Error Handling

#### Common Issues
1. **Font Loading Errors**: Handle missing fonts gracefully
2. **Image Processing Errors**: Manage memory and file size issues
3. **Layout Conflicts**: Resolve positioning and sizing conflicts
4. **Data Format Errors**: Handle incorrect data types and missing values

#### Troubleshooting
```python
# Handle font loading errors
def safe_font_loading(font_path, size):
    """Safely load fonts with fallback"""
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

# Handle image processing errors
def safe_image_resize(image, size):
    """Safely resize images"""
    try:
        return image.resize(size, Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"Image resize error: {e}")
        return image

# Handle layout conflicts
def validate_layout(sections, canvas_size):
    """Validate layout to prevent overlaps"""
    for i, section1 in enumerate(sections):
        for j, section2 in enumerate(sections[i+1:], i+1):
            if check_overlap(section1['position'], section2['position']):
                print(f"Warning: Sections {i} and {j} overlap")
                # Adjust positions automatically
                adjust_position(section2, canvas_size)

def check_overlap(pos1, pos2):
    """Check if two sections overlap"""
    return not (pos1['x'] + pos1['width'] < pos2['x'] or 
                pos2['x'] + pos2['width'] < pos1['x'] or
                pos1['y'] + pos1['height'] < pos2['y'] or 
                pos2['y'] + pos2['height'] < pos1['y'])

# Handle data format errors
def prepare_data_for_infographic(data):
    """Prepare data for infographic creation"""
    try:
        if isinstance(data, pd.DataFrame):
            return data.to_dict('records')
        elif isinstance(data, list):
            return data
        else:
            print("Unsupported data format")
            return []
    except Exception as e:
        print(f"Data preparation error: {e}")
        return []
```

### Monitoring
- Monitor infographic generation performance and success rates
- Track file sizes and storage usage
- Monitor design consistency and quality
- Alert on generation failures and errors

### Best Practices
1. **Clear Hierarchy**: Use typography and spacing to create clear information hierarchy
2. **Consistent Design**: Maintain consistent colors, fonts, and styling
3. **Data Accuracy**: Ensure all data and statistics are accurate and up-to-date
4. **Accessibility**: Use colorblind-friendly palettes and readable fonts
5. **Mobile Optimization**: Consider mobile viewing for web infographics
6. **Source Attribution**: Always include data sources and attributions
7. **File Optimization**: Balance quality with file size for web use
8. **Version Control**: Track infographic versions and design iterations
