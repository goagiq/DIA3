# Enhanced Report Templates

This directory contains the enhanced report templates that serve as the foundation for generating comprehensive strategic analysis reports.

## 📁 Template Files

### 1. Enhanced Report Template
- **File**: `Pakistan_Submarine_Analysis_Enhanced_Report.html`
- **Size**: 120KB (2,321 lines)
- **Purpose**: Comprehensive enhanced report with all interactive visualizations
- **Features**:
  - 32 interactive charts in 4-chart grid layouts
  - All missing visualizations included
  - Interactive tooltips with source information
  - Responsive design with Chart.js and Leaflet.js
  - Complete sections for strategic analysis

### 2. Leadership Template
- **File**: `Pakistan_Submarine_Leadership_Report.html`
- **Size**: 32KB (789 lines)
- **Purpose**: Condensed executive-friendly report for leadership briefings
- **Features**:
  - Smaller, more compact charts
  - Executive-focused layout
  - Strategic insights and recommendations
  - Art of War analysis integration
  - Professional styling for executive presentations

## 🔧 Template Configuration

The templates are managed through the `TemplateConfig` class in `src/core/template_config.py`:

```python
from src.core.template_config import TemplateConfig

# Check if template exists
if TemplateConfig.template_exists("enhanced_report"):
    # Get template content
    content = TemplateConfig.get_template_content("enhanced_report")
    
# List available templates
available = TemplateConfig.list_available_templates()
```

## 🚀 Usage

### Automatic Template Selection
The system automatically selects the appropriate template based on the topic:

- **Enhanced Report**: Default template for comprehensive analysis
- **Leadership Template**: Automatically selected when "leadership" is mentioned in the topic

### Manual Template Selection
You can specify the template type when generating reports:

```python
result = await enhanced_report_template_generator.generate_enhanced_report_template(
    topic="Strategic Analysis",
    analysis_data=analysis_data,
    output_dir="Results",
    template_type="leadership"  # or "enhanced_report"
)
```

## 📊 Template Features

### Enhanced Report Template
- **Executive Summary** with key metrics
- **Strategic Assessment** with nuclear deterrence analysis
- **Forecasting & Analytics** with 4-chart grid
- **Regional Analysis** with stakeholder sentiment
- **Implementation & Timeline** with critical path analysis
- **Strategic Options** with risk-reward assessment
- **Regional Security Map** with interactive markers
- **Key Recommendations** with actionable insights

### Leadership Template
- **Executive Summary** with condensed metrics
- **Art of War Strategic Analysis** with deception insights
- **Strategic Assessment** with nuclear capabilities
- **Forecasting & Analytics** in compact format
- **Regional Analysis** with stakeholder sentiment
- **Implementation & Timeline** with critical paths
- **Strategic Options** with recommendations
- **Counter-Strategy Recommendations** for intelligence

## 🛡️ Protection

These templates are stored in the `/Results/templates/` directory to prevent accidental deletion. The system is configured to:

1. **Automatically detect** template availability
2. **Fallback gracefully** if templates are missing
3. **Use template content** when available
4. **Generate from scratch** when templates are not found

## 🔄 Template Updates

To update templates:

1. **Modify the HTML files** in this directory
2. **Test the changes** using the template configuration
3. **Update the system** to use the new templates
4. **Verify functionality** with the enhanced report generator

## 📝 Template Customization

Templates support placeholder replacement:

- `{{TOPIC}}` - Replaced with the analysis topic
- `{{TIMESTAMP}}` - Replaced with generation timestamp
- `{{ANALYSIS_DATA}}` - Replaced with JSON analysis data

## 🧪 Testing

Use the test script to verify template configuration:

```bash
python test_template_config.py
```

This will check:
- Template file existence
- Template content accessibility
- Template path resolution
- Available template listing

## 📋 Template Status

- ✅ **Enhanced Report Template**: Available and functional
- ✅ **Leadership Template**: Available and functional
- ✅ **Template Configuration**: Implemented and tested
- ✅ **Automatic Selection**: Working correctly
- ✅ **Fallback System**: Implemented for reliability

## 🎯 Next Steps

1. **Create additional templates** for different report types
2. **Add template versioning** for better management
3. **Implement template validation** for quality assurance
4. **Add template preview** functionality
5. **Create template editor** for easy customization
