# Enhanced Report Generation Guide

## Overview

The Enhanced Report Generation system provides comprehensive, interactive HTML reports that combine strategic analysis with advanced visualizations, knowledge graphs, and professional data tables. This system automatically generates reports that include:

- **Interactive Charts**: Dynamic visualizations using Chart.js
- **Knowledge Graphs**: Network visualizations using vis.js
- **Professional Tables**: Styled data tables with risk assessments
- **Responsive Design**: Mobile-friendly layouts
- **Strategic Analysis**: Comprehensive analytical frameworks

## Features

### 🎯 Core Capabilities

1. **Interactive HTML Reports**
   - Professional styling with gradient backgrounds
   - Responsive design for all screen sizes
   - Modern UI with hover effects and animations

2. **Knowledge Graph Visualization**
   - Interactive network graphs using vis.js
   - Entity relationship mapping
   - Dynamic node clustering and filtering
   - Color-coded node types (concepts, risks, recommendations)

3. **Monte Carlo Simulation Analysis**
   - Probabilistic modeling with multiple distributions
   - Risk assessment with confidence intervals
   - Cost analysis with uncertainty ranges
   - Strategic impact modeling with statistical significance
   - Interactive simulation visualizations

4. **Data Visualization**
   - Bar charts for comparative analysis
   - Doughnut charts for cost breakdowns
   - Radar charts for strategic assessments
   - Scatter plots for risk matrices
   - Monte Carlo distribution charts

5. **Professional Tables**
   - Gradient headers with professional styling
   - Risk level color coding (Low, Medium, High, Critical)
   - Hover effects and responsive design
   - Comprehensive data presentation
   - Confidence interval tables

### 📊 Report Sections

Each enhanced report includes:

1. **Executive Summary**
   - Key findings with highlighted statistics
   - Summary stat cards with metrics
   - Strategic impact assessment

2. **Strategic Context**
   - Current vs. proposed comparisons
   - Professional data tables
   - Regional impact analysis

3. **Economic Analysis**
   - Cost breakdown tables
   - Risk assessment matrices
   - Feasibility analysis

4. **Regional Security Implications**
   - Response analysis tables
   - Arms race risk assessment
   - Strategic impact evaluation

5. **Interactive Visualizations**
   - Fleet comparison charts
   - Cost breakdown analysis
   - Strategic impact radar charts
   - Risk assessment matrices

        6. **Knowledge Graph Analysis**
           - Interactive network visualization
           - Entity relationship mapping
           - Dynamic graph layout

        7. **Monte Carlo Simulation Analysis**
           - Probabilistic cost analysis
           - Risk assessment distributions
           - Strategic impact modeling
           - Confidence interval calculations
           - Interactive simulation charts

        8. **Risk Assessment**
           - Comprehensive risk matrices
           - Critical risk factor analysis
           - Mitigation strategies

        9. **Strategic Recommendations**
           - Categorized recommendations
           - Implementation guidance
           - Priority assessments

        10. **Conclusion**
            - Strategic insights summary
            - Final recommendations
            - Overall assessment

## Installation

### Prerequisites

```bash
# Install core dependencies
pip install networkx matplotlib seaborn jinja2

# Install Monte Carlo simulation dependencies
pip install numpy pandas scipy

# Install optional dependencies for enhanced features
pip install plotly dash

# Install MCP dependencies (if using MCP integration)
pip install mcp
```

### Quick Installation

```bash
# Install all dependencies from requirements file
pip install -r requirements_enhanced_reports.txt
```

## Usage

### Basic Usage

```python
from src.core.export.enhanced_report_integration import generate_enhanced_report

# Generate Pakistan submarine analysis report
report_path = generate_enhanced_report(
    analysis_type="pakistan_submarine",
    title="Pakistan's 50-Submarine Acquisition",
    subtitle="Comprehensive Strategic Analysis for Conventional Deterrence"
)

print(f"Report generated: {report_path}")
```

### Custom Report Generation

```python
from src.core.export.enhanced_report_integration import generate_custom_enhanced_report

# Create custom analysis data
custom_data = {
    'main_entity': 'Strategic Intelligence Analysis',
    'key_concepts': ['Intelligence Collection', 'Analysis Methods', 'Strategic Planning'],
    'risk_factors': ['Data Quality Issues', 'Analysis Bias', 'Timeline Constraints'],
    'recommendations': ['Enhanced Data Validation', 'Multi-Source Analysis', 'Automated Processing'],
    'executive_summary': {
        'description': 'Comprehensive strategic intelligence analysis framework.',
        'key_findings': {
            'Intelligence Quality': 'High-quality intelligence requires multiple validation layers',
            'Analysis Efficiency': 'Automated tools can improve analysis speed by 60%'
        },
        'summary_stats': [
            {'label': 'Analysis Speed', 'value': '+60%', 'description': 'Improvement with automation'},
            {'label': 'Risk Reduction', 'value': '40%', 'description': 'Failure rate reduction'}
        ]
    }
}

# Generate custom report
report_path = generate_custom_enhanced_report(
    analysis_data=custom_data,
    title="Strategic Intelligence Analysis Framework",
    subtitle="Enhanced Intelligence Capabilities"
)
```

### Knowledge Graph Focused Reports

```python
# Create knowledge graph analysis data
kg_data = {
    'main_entity': 'Cybersecurity Threat Intelligence',
    'key_concepts': ['Threat Actors', 'Attack Vectors', 'Vulnerabilities', 'Mitigation Strategies'],
    'risk_factors': ['Zero-day Exploits', 'Advanced Persistent Threats', 'Supply Chain Attacks'],
    'recommendations': ['Threat Hunting', 'Vulnerability Management', 'Security Awareness Training'],
    'executive_summary': {
        'description': 'Comprehensive cybersecurity threat intelligence analysis.',
        'key_findings': {
            'Threat Landscape': 'Increasingly sophisticated attack vectors',
            'Response Time': 'Critical for minimizing damage'
        },
        'summary_stats': [
            {'label': 'Threat Detection', 'value': '95%', 'description': 'Detection rate'},
            {'label': 'Response Time', 'value': '<2hrs', 'description': 'Average response'}
        ]
    }
}

# Generate knowledge graph report
report_path = generate_custom_enhanced_report(
    analysis_data=kg_data,
    title="Cybersecurity Threat Intelligence Analysis",
    subtitle="Interactive Knowledge Graph of Threat Landscape"
)
```

## MCP Integration

### Running the MCP Server

```bash
# Start the enhanced report MCP server
python src/mcp_servers/enhanced_report_mcp_server.py
```

### Available MCP Tools

1. **generate_enhanced_report**
   - Generates standard enhanced reports
   - Parameters: analysis_type, title, subtitle

2. **generate_custom_enhanced_report**
   - Generates custom reports with provided data
   - Parameters: analysis_data, title, subtitle

3. **generate_knowledge_graph_report**
   - Generates focused knowledge graph reports
   - Parameters: entities, relationships, title

4. **run_monte_carlo_simulation**
   - Runs Monte Carlo simulation for probabilistic analysis
   - Parameters: simulation_type, n_iterations, parameters, title

5. **generate_monte_carlo_report**
   - Generates enhanced reports with Monte Carlo simulation analysis
   - Parameters: analysis_type, include_monte_carlo, title, subtitle

6. **check_enhanced_report_status**
   - Checks if enhanced report generation is available
   - No parameters required

## Testing

### Run Demo

```bash
# Run the enhanced report generation demo
python examples/enhanced_report_demo.py

# Run the Monte Carlo simulation demo
python examples/monte_carlo_simulation_demo.py
```

### Run Tests

```bash
# Run the test suite
python Test/test_enhanced_report_generation.py
```

## Data Structure

### Analysis Data Format

```python
analysis_data = {
    'main_entity': 'Primary entity name',
    'key_concepts': ['Concept 1', 'Concept 2', 'Concept 3'],
    'risk_factors': ['Risk 1', 'Risk 2', 'Risk 3'],
    'recommendations': ['Recommendation 1', 'Recommendation 2'],
    'executive_summary': {
        'description': 'Executive summary description',
        'key_findings': {
            'Finding 1': 'Description of finding 1',
            'Finding 2': 'Description of finding 2'
        },
        'summary_stats': [
            {
                'label': 'Stat Label',
                'value': 'Stat Value',
                'description': 'Stat description'
            }
        ]
    },
    'strategic_context': {
        'table_headers': ['Header 1', 'Header 2', 'Header 3'],
        'table_data': [
            ['Row 1 Col 1', 'Row 1 Col 2', 'Row 1 Col 3'],
            ['Row 2 Col 1', 'Row 2 Col 2', 'Row 2 Col 3']
        ]
    },
    'fleet_data': {
        'labels': ['Label 1', 'Label 2', 'Label 3'],
        'data': [10, 20, 30]
    },
    'cost_data': {
        'labels': ['Cost 1', 'Cost 2', 'Cost 3'],
        'data': [25, 15, 10]
    },
    'strategic_data': {
        'labels': ['Strategic 1', 'Strategic 2', 'Strategic 3'],
        'data': [85, 75, 65]
    }
}
```

## Customization

### Styling

The HTML reports use CSS classes that can be customized:

- `.professional-table`: Data table styling
- `.stat-card`: Summary statistics cards
- `.chart-section`: Chart container styling
- `.knowledge-graph-section`: Knowledge graph container
- `.risk-assessment`: Risk assessment styling

### Templates

The system uses Jinja2 templates for HTML generation. Templates can be modified in:
- `src/core/export/enhanced_report_generator.py`

### Charts

Chart configurations can be customized in the `create_charts_script` method:
- Chart types (bar, doughnut, radar, scatter)
- Colors and styling
- Interactive features
- Data formatting

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Install missing dependencies
   pip install networkx matplotlib seaborn jinja2
   ```

2. **Chart Not Displaying**
   - Check internet connection (Chart.js and vis.js are loaded from CDN)
   - Verify JavaScript is enabled in browser
   - Check browser console for errors

3. **Knowledge Graph Not Loading**
   - Ensure vis.js library is loading correctly
   - Check data format for nodes and edges
   - Verify container element exists

4. **Tables Not Styled**
   - Check CSS is loading correctly
   - Verify table structure matches expected format
   - Ensure risk level classes are applied correctly

### Debug Mode

Enable debug mode by setting environment variable:
```bash
export ENHANCED_REPORT_DEBUG=1
```

## Examples

### Pakistan Submarine Analysis

The system includes a pre-built template for Pakistan submarine acquisition analysis:

```python
report_path = generate_enhanced_report(
    analysis_type="pakistan_submarine",
    title="Pakistan's 50-Submarine Acquisition",
    subtitle="Comprehensive Strategic Analysis for Conventional Deterrence"
)
```

This generates a comprehensive report with:
- Current vs. proposed submarine fleet comparison
- Economic cost analysis
- Regional security implications
- Risk assessment matrix
- Strategic recommendations

### Custom Strategic Analysis

Create custom strategic analysis reports:

```python
custom_data = {
    'main_entity': 'Your Strategic Analysis',
    'key_concepts': ['Your concepts here'],
    'risk_factors': ['Your risk factors'],
    'recommendations': ['Your recommendations'],
    'executive_summary': {
        'description': 'Your analysis description',
        'key_findings': {'Finding': 'Description'},
        'summary_stats': [{'label': 'Label', 'value': 'Value', 'description': 'Desc'}]
    }
}

report_path = generate_custom_enhanced_report(
    analysis_data=custom_data,
    title="Your Analysis Title",
    subtitle="Your Analysis Subtitle"
)
```

## Performance

### Optimization Tips

1. **Large Datasets**
   - Limit knowledge graph nodes to < 100 for optimal performance
   - Use pagination for large tables
   - Optimize chart data points

2. **File Size**
   - Compress images before embedding
   - Minimize CSS and JavaScript
   - Use external CDN resources

3. **Loading Speed**
   - Load libraries from CDN
   - Optimize chart rendering
   - Use lazy loading for large visualizations

## Security

### Best Practices

1. **Data Sanitization**
   - Validate all input data
   - Sanitize HTML content
   - Escape special characters

2. **File Access**
   - Restrict file write permissions
   - Validate file paths
   - Use secure file naming

3. **Content Security**
   - Implement CSP headers
   - Validate external resources
   - Sanitize user-generated content

## Support

### Getting Help

1. **Documentation**
   - Check this guide for common issues
   - Review example code
   - Examine test files

2. **Debugging**
   - Enable debug mode
   - Check browser console
   - Review generated HTML

3. **Issues**
   - Check dependency versions
   - Verify file permissions
   - Test with minimal data

## Future Enhancements

### Planned Features

1. **Additional Chart Types**
   - Timeline charts
   - Sankey diagrams
   - 3D visualizations

2. **Export Options**
   - PDF export
   - PowerPoint integration
   - Word document generation

3. **Advanced Analytics**
   - Machine learning integration
   - Predictive analytics
   - Real-time data updates

4. **Enhanced Monte Carlo Features**
   - Sensitivity analysis
   - Scenario comparison
   - Advanced probability distributions
   - Real-time simulation updates

5. **Collaboration Features**
   - Multi-user editing
   - Comment systems
   - Version control

---

For more information, see the main project documentation or contact the development team.
