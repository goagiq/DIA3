# Modularized Enhanced Report System - Usage Guide

## Pakistan Submarine Acquisition Analysis Demo

This guide shows you how to generate enhanced reports using the Modularized Enhanced Report System for your topic: **"Pakistan Submarine Acquisition Analysis and Deterrence Enhancement - Impact on geopolitics, trade, balance of power, escalation"**.

## Quick Start

### 1. Run the Interactive Demo
```bash
# Activate virtual environment (Windows)
.venv\Scripts\python.exe demo_pakistan_submarine_analysis.py

# Or on Linux/Mac
.venv/bin/python demo_pakistan_submarine_analysis.py
```

This will generate multiple example reports showing different ways to use the system.

### 2. Basic Usage Pattern

```python
from src.core.modular_report_generator import ModularReportGenerator
import asyncio

async def generate_report():
    # Initialize generator
    generator = ModularReportGenerator()
    
    # Your analysis topic
    topic = "Pakistan Submarine Acquisition Analysis"
    
    # Your analysis data
    data = {
        "strategic_recommendations": {
            "intelligence_summary": {
                "total_insights": 15,
                "average_confidence": 85.0
            }
        }
    }
    
    # Select modules to use
    modules = ["strategicrecommendationsmodule", "regionalsecuritymodule"]
    
    # Generate report
    result = await generator.generate_modular_report(
        topic=topic,
        data=data,
        enabled_modules=modules
    )
    
    if result["success"]:
        print(f"Report generated: {result['filename']}")
    
asyncio.run(generate_report())
```

## Available Modules

The system includes 23 specialized analysis modules:

### Core Strategic Modules
- **strategicrecommendationsmodule** - Strategic recommendations and implementation planning
- **executivesummarymodule** - Executive summary with key findings
- **strategicanalysismodule** - Strategic analysis and implications

### Impact Analysis Modules  
- **geopoliticalimpactmodule** - Geopolitical implications and regional dynamics
- **tradeimpactmodule** - Trade and economic impact analysis
- **balanceofpowermodule** - Military balance and power dynamics
- **riskassessmentmodule** - Risk analysis and mitigation strategies

### Security & Regional Modules
- **regionalsecuritymodule** - Regional security implications
- **regionalsentimentmodule** - Regional sentiment and stakeholder analysis
- **interactivevisualizationsmodule** - Interactive charts and visualizations

### Economic & Financial Modules
- **economicanalysismodule** - Economic cost-benefit analysis
- **acquisitionprogramsmodule** - Acquisition program details
- **tradeimpactmodule** - Trade relationship impacts

### Operational Modules
- **operationalconsiderationsmodule** - Operational readiness and considerations
- **implementationtimelinemodule** - Implementation timeline and milestones
- **forecastingmodule** - Future projections and forecasting

### Advanced Analytics Modules
- **enhanceddataanalysismodule** - Advanced data analysis
- **predictiveanalyticsmodule** - Predictive modeling and analytics
- **advancedforecastingmodule** - Advanced forecasting capabilities
- **modelperformancemodule** - Model performance and validation
- **strategiccapabilitymodule** - Strategic capability assessment
- **comparisonanalysismodule** - Comparative analysis
- **scenarioanalysismodule** - Scenario analysis and planning

## Report Generation Examples

### Example 1: Strategic Focus Report
Use core strategic modules for high-level policy analysis:

```python
strategic_modules = [
    "strategicrecommendationsmodule",
    "strategicanalysismodule", 
    "regionalsecuritymodule"
]
```

### Example 2: Economic Impact Report  
Focus on economic and trade implications:

```python
economic_modules = [
    "economicanalysismodule",
    "tradeimpactmodule",
    "acquisitionprogramsmodule",
    "riskassessmentmodule"
]
```

### Example 3: Security Assessment Report
Emphasize security and risk factors:

```python
security_modules = [
    "regionalsecuritymodule",
    "riskassessmentmodule", 
    "balanceofpowermodule",
    "scenarioanalysismodule"
]
```

### Example 4: Comprehensive Analysis
Use all available modules (may require extensive data):

```python
# Get all available modules
generator = ModularReportGenerator()
all_modules = generator.get_available_modules()

# Use all modules
result = await generator.generate_modular_report(
    topic="Comprehensive Pakistan Submarine Analysis",
    data=comprehensive_data,
    enabled_modules=all_modules
)
```

## Data Structure Guidelines

Each module expects specific data keys. Here are the key data structures:

### Strategic Recommendations Module
```python
"strategic_recommendations": {
    "intelligence_summary": {
        "total_insights": 15,
        "average_confidence": 85.0,
        "high_impact_insights": 8
    },
    "recommendations": {
        "immediate": [{"title": "...", "confidence": 0.9, ...}],
        "short_term": [...],
        "long_term": [...]
    }
}
```

### Regional Security Module
```python
"regional_security": {
    "security_dynamics": {
        "threat_assessment": "Description...",
        "deterrence_effectiveness": "Assessment..."
    },
    "security_implications": ["Implication 1", "Implication 2"],
    "mitigation_measures": ["Measure 1", "Measure 2"]
}
```

### Economic Analysis Module
```python
"economic_analysis": {
    "cost_breakdown": {
        "acquisition_cost": "$3.5 billion",
        "technology_transfer": "$800 million"
    },
    "economic_impact": {
        "defense_industry_growth": "25% increase",
        "employment_generation": "5,000 jobs"
    }
}
```

## Features

### Interactive Elements
- **Advanced Tooltips**: Hover over elements for detailed information
- **Interactive Charts**: Chart.js visualizations with multiple chart types
- **Responsive Design**: Works on desktop and mobile devices

### Chart Types Available
- **Radar Charts**: Multi-dimensional comparisons
- **Bar Charts**: Categorical data comparison  
- **Line Charts**: Trend analysis over time
- **Pie Charts**: Proportion and distribution analysis

### Output Features
- **HTML Reports**: Self-contained HTML files with embedded CSS/JavaScript
- **Export Ready**: Can be easily shared or presented
- **Print Friendly**: Optimized for printing and PDF export

## File Locations

### Generated Reports
- **Location**: `Results/` directory
- **Format**: HTML files with timestamp
- **Naming**: `topic_modular_enhanced_analysis_YYYYMMDD_HHMMSS.html`

### Source Code
- **Main Generator**: `src/core/modular_report_generator.py`
- **Modules**: `src/core/modules/`
- **Tests**: `Test/`
- **Demos**: `demo_pakistan_submarine_analysis.py`

## Troubleshooting

### Common Issues

1. **Missing Data Keys Error**
   - Ensure your data dictionary includes the required keys for each module
   - Check module documentation for required data structure

2. **Module Not Found Error**
   - Verify module names using `generator.get_available_modules()`
   - Module names are lowercase with no spaces

3. **Empty Report Generated**
   - Check that at least one module is enabled
   - Verify data format matches module expectations

### Getting Help

1. **Check Available Modules**:
   ```python
   generator = ModularReportGenerator()
   print(generator.get_available_modules())
   ```

2. **Validate Module Data**:
   ```python
   module = generator.get_module("modulename")
   required_keys = module.get_required_data_keys()
   print(f"Required data keys: {required_keys}")
   ```

3. **Test with Minimal Data**:
   ```python
   # Start with working modules like strategicrecommendationsmodule
   # Use the demo script as a reference for data structure
   ```

## Next Steps

1. **Run the Demo**: Start with `demo_pakistan_submarine_analysis.py`
2. **Examine Output**: Open generated HTML files in your browser
3. **Customize Data**: Adapt the data structure to your specific analysis
4. **Select Modules**: Choose modules that match your analysis needs
5. **Generate Reports**: Create reports for your Pakistan submarine analysis

## Support

For technical support or questions about the system:
- Check the demo scripts for working examples
- Review module source code in `src/core/modules/`
- Test with minimal data sets first
- Use the strategic recommendations module as a reliable starting point
