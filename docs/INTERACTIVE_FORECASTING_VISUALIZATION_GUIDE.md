# Interactive Forecasting Visualization Guide

## 🎯 Overview

This guide documents the enhanced interactive visualization system for forecasting and prediction charts with distinct color schemes for historical vs future values. The system provides advanced interactive capabilities for Monte Carlo simulations, scenario analysis, and predictive analytics.

## 🎨 Color Scheme Design

### Historical vs Future Color Distinction

The visualization system uses a carefully designed color scheme to distinguish between historical and future data:

#### **Historical Data Colors**
- **Primary Line**: `#1f77b4` (Blue)
- **Markers**: `#1f77b4` (Blue)
- **Fill**: `rgba(31, 119, 180, 0.1)` (Light blue)

#### **Future/Forecast Colors**
- **Primary Line**: `#ff7f0e` (Orange)
- **Markers**: `#ff7f0e` (Orange)
- **Fill**: `rgba(255, 127, 14, 0.1)` (Light orange)

#### **Confidence Intervals**
- **Upper Bound**: `#ff7f0e` (Orange)
- **Lower Bound**: `#ff7f0e` (Orange)
- **Fill**: `rgba(255, 127, 14, 0.2)` (Medium orange)

#### **Scenario Colors**
Multiple colors for different scenarios:
- `#2ca02c` (Green)
- `#d62728` (Red)
- `#9467bd` (Purple)
- `#8c564b` (Brown)
- `#e377c2` (Pink)
- `#7f7f7f` (Gray)
- `#bcbd22` (Olive)
- `#17becf` (Cyan)

## 🚀 Key Features

### **Interactive Capabilities**
- **Zoom & Pan**: Navigate through large datasets
- **Range Slider**: Quick time period selection
- **Hover Tooltips**: Detailed information on data points
- **Selection Tools**: Interactive data selection
- **Cross-filtering**: Filter data across multiple charts

### **Chart Types**

#### **1. Forecast Timeline Chart**
- Historical data in blue
- Future forecasts in orange
- Confidence intervals with shaded areas
- Interactive time navigation

#### **2. Monte Carlo Forecast Chart**
- Multiple simulation paths
- Mean forecast line
- Confidence bands (68% and 95%)
- Historical data baseline

#### **3. Scenario Comparison Chart**
- Multiple future scenarios
- Historical comparison
- Different line styles (solid vs dashed)
- Color-coded scenarios

#### **4. Risk Assessment Heatmap**
- Risk scores across scenarios and time periods
- Color scale: Red (high risk) to Green (low risk)
- Interactive hover information

#### **5. Probability Distribution Chart**
- Historical data in top subplot
- Forecast distributions in bottom subplot
- Uncertainty visualization

#### **6. Comprehensive Dashboard**
- Multiple charts in grid layout
- Unified interactive experience
- Responsive design

## 📊 Implementation

### **Core Components**

#### **InteractiveForecastingCharts Class**
```python
from src.core.visualization.interactive_forecasting_charts import (
    InteractiveForecastingCharts, 
    ChartColors
)

# Create custom color scheme
colors = ChartColors(
    historical_line="#1f77b4",  # Blue for historical
    future_line="#ff7f0e",      # Orange for future
    confidence_fill="rgba(255, 127, 14, 0.2)"
)

# Initialize visualizer
visualizer = InteractiveForecastingCharts(colors)
```

#### **Monte Carlo Integration**
```python
from src.core.monte_carlo.visualization_integration import (
    MonteCarloVisualizationIntegration
)

# Create integration instance
integration = MonteCarloVisualizationIntegration()

# Run simulation with visualization
results = integration.run_monte_carlo_with_visualization(
    simulation_config=config,
    visualization_config=vis_config,
    output_dir="Results/"
)
```

### **Usage Examples**

#### **Basic Forecast Chart**
```python
# Create forecast timeline chart
fig = visualizer.create_forecast_timeline_chart(
    historical_data=historical_df,
    forecast_data=forecast_df,
    confidence_cols=('lower_bound', 'upper_bound'),
    title="Interactive Forecast Timeline"
)

# Save as interactive HTML
fig.write_html("forecast_chart.html")
```

#### **Monte Carlo Simulation**
```python
# Create Monte Carlo visualization
fig = visualizer.create_monte_carlo_forecast_chart(
    historical_data=historical_df,
    simulation_results=simulation_paths,
    forecast_periods=365,
    title="Monte Carlo Simulation Results"
)
```

#### **Scenario Comparison**
```python
# Create scenario comparison
fig = visualizer.create_scenario_comparison_chart(
    scenarios=scenario_list,
    title="Scenario Comparison Analysis"
)
```

## 🔧 Configuration

### **Chart Colors Configuration**
```python
@dataclass
class ChartColors:
    # Historical data colors
    historical_line: str = "#1f77b4"  # Blue
    historical_marker: str = "#1f77b4"
    historical_fill: str = "rgba(31, 119, 180, 0.1)"
    
    # Future/forecast colors
    future_line: str = "#ff7f0e"  # Orange
    future_marker: str = "#ff7f0e"
    future_fill: str = "rgba(255, 127, 14, 0.1)"
    
    # Confidence interval colors
    confidence_upper: str = "#ff7f0e"
    confidence_lower: str = "#ff7f0e"
    confidence_fill: str = "rgba(255, 127, 14, 0.2)"
    
    # Scenario colors
    scenario_colors: List[str] = None
```

### **Interactive Features Configuration**
```python
interactive_features = {
    'zoom': True,
    'pan': True,
    'hover': True,
    'selection': True,
    'range_slider': True
}
```

## 📈 Data Requirements

### **Historical Data Format**
```python
historical_data = pd.DataFrame({
    'timestamp': pd.date_range('2023-01-01', '2024-01-01', freq='D'),
    'value': [100, 102, 105, ...]  # Historical values
})
```

### **Forecast Data Format**
```python
forecast_data = pd.DataFrame({
    'timestamp': pd.date_range('2024-01-02', '2024-12-31', freq='D'),
    'value': [150, 152, 155, ...],  # Forecast values
    'lower_bound': [145, 147, 150, ...],  # Confidence intervals
    'upper_bound': [155, 157, 160, ...]
})
```

### **Monte Carlo Simulation Format**
```python
simulation_paths = [
    pd.DataFrame({
        'timestamp': forecast_dates,
        'value': simulation_values
    }),
    # ... more simulation paths
]
```

### **Scenario Data Format**
```python
scenarios = [
    {
        'name': 'Baseline',
        'type': 'forecast',  # or 'historical'
        'timeline': pd.date_range(...),
        'values': [150, 152, 155, ...],
        'lower_bound': [145, 147, 150, ...],  # Optional
        'upper_bound': [155, 157, 160, ...]   # Optional
    }
]
```

## 🎯 Strategic Intelligence Applications

### **Questions That Generate Interactive Charts**

#### **1. Threat Evolution Modeling**
**Question**: "Model the evolution of [specific threat] over the next [timeframe] using Monte Carlo simulation and pattern recognition from historical conflicts."

**Interactive Charts Generated**:
- **Forecast Timeline**: Historical threat data (blue) vs future threat evolution (orange)
- **Monte Carlo Simulation**: Multiple threat evolution paths with confidence bands
- **Risk Assessment Heatmap**: Threat probability across time periods

#### **2. Multi-Scenario Risk Quantification**
**Question**: "Run Monte Carlo simulations for [3-5 specific scenarios] and quantify the probability and impact of each outcome, including worst-case scenarios."

**Interactive Charts Generated**:
- **Scenario Comparison**: Multiple scenarios with distinct colors
- **Probability Distribution**: Uncertainty visualization for each scenario
- **Comprehensive Dashboard**: All scenarios in unified view

#### **3. Technology Investment Assessment**
**Question**: "Assess the strategic value of [technology investments] using Monte Carlo simulation and compare against alternative investments for [timeframe]."

**Interactive Charts Generated**:
- **Forecast Timeline**: Historical performance (blue) vs future projections (orange)
- **Monte Carlo Simulation**: Investment return paths with confidence intervals
- **Risk Assessment**: Investment risk across different scenarios

#### **4. Emerging Threat Detection**
**Question**: "Use pattern recognition and anomaly detection to identify emerging threats from [data sources] and assess their probability using Monte Carlo simulation."

**Interactive Charts Generated**:
- **Probability Distribution**: Threat probability distributions
- **Forecast Timeline**: Historical patterns (blue) vs emerging threats (orange)
- **Risk Assessment Heatmap**: Threat risk across time and scenarios

## 🚀 Demo and Examples

### **Running the Demo**
```bash
cd examples
python interactive_forecasting_demo.py
```

### **Demo Outputs**
The demo generates several interactive HTML files:
- `forecast_timeline_demo.html`
- `monte_carlo_forecast_demo.html`
- `scenario_comparison_demo.html`
- `risk_assessment_demo.html`
- `probability_distribution_demo.html`
- `comprehensive_dashboard_demo.html`

### **Demo Features**
- **7 Different Chart Types**: Showcasing all visualization capabilities
- **Sample Data Generation**: Realistic time series with trends and seasonality
- **Monte Carlo Simulations**: Multiple simulation paths with uncertainty
- **Interactive Features**: Zoom, pan, hover, range slider
- **Color Distinction**: Clear visual separation of historical vs future data

## 🔗 Integration with Existing Systems

### **Monte Carlo Engine Integration**
```python
# Enhanced Monte Carlo engine with visualization
from src.core.monte_carlo.visualization_integration import (
    MonteCarloVisualizationIntegration
)

# Run simulation with integrated visualization
integration = MonteCarloVisualizationIntegration()
results = integration.run_monte_carlo_with_visualization(
    simulation_config={
        'num_simulations': 1000,
        'forecast_periods': 365,
        'variables': ['threat_level', 'capability', 'intent']
    },
    visualization_config={
        'create_forecast_chart': True,
        'create_monte_carlo_chart': True,
        'create_risk_chart': True,
        'create_dashboard': True
    },
    output_dir="Results/monte_carlo_analysis/"
)
```

### **API Integration**
```python
# API endpoint for interactive visualizations
@app.post("/api/v1/visualization/forecast")
async def create_forecast_visualization(
    historical_data: pd.DataFrame,
    forecast_data: pd.DataFrame,
    confidence_intervals: Optional[Tuple[str, str]] = None
):
    visualizer = InteractiveForecastingCharts()
    result = visualizer.create_forecast_timeline_chart(
        historical_data=historical_data,
        forecast_data=forecast_data,
        confidence_cols=confidence_intervals
    )
    return result
```

## 📊 Best Practices

### **Color Usage**
1. **Consistency**: Always use blue for historical data
2. **Clarity**: Use orange for future/forecast data
3. **Contrast**: Ensure sufficient contrast for accessibility
4. **Meaning**: Use color to convey meaning, not just decoration

### **Interactive Design**
1. **Intuitive Navigation**: Make zoom and pan controls obvious
2. **Responsive Feedback**: Provide immediate visual feedback
3. **Information Density**: Balance detail with readability
4. **Performance**: Optimize for large datasets

### **Data Visualization**
1. **Clear Labels**: Use descriptive titles and axis labels
2. **Legend**: Include clear legends for all data series
3. **Confidence Intervals**: Show uncertainty when available
4. **Context**: Provide historical context for forecasts

## 🔧 Customization

### **Custom Color Schemes**
```python
# Create custom color scheme
custom_colors = ChartColors(
    historical_line="#2E86AB",  # Custom blue
    future_line="#A23B72",      # Custom purple
    confidence_fill="rgba(162, 59, 114, 0.2)"
)

visualizer = InteractiveForecastingCharts(custom_colors)
```

### **Custom Interactive Features**
```python
# Configure interactive features
visualizer.interactive_features = {
    'zoom': True,
    'pan': False,  # Disable panning
    'hover': True,
    'selection': True,
    'range_slider': False  # Disable range slider
}
```

## 📈 Performance Considerations

### **Large Datasets**
- Use data sampling for very large datasets
- Implement progressive loading for real-time data
- Optimize chart rendering for performance

### **Memory Management**
- Clear chart objects when no longer needed
- Use efficient data structures
- Monitor memory usage for long-running applications

## 🔒 Security and Compliance

### **Data Protection**
- Ensure sensitive data is not exposed in visualizations
- Implement proper access controls
- Follow data classification guidelines

### **Export Controls**
- Validate data before export
- Implement proper file permissions
- Log visualization exports for audit

## 📚 Additional Resources

### **Documentation**
- [Monte Carlo Engine Guide](docs/monte_carlo_engine_guide.md)
- [Strategic Intelligence Framework](docs/plans/strategic_intelligence_question_framework.md)
- [API Documentation](docs/API_DOCUMENTATION.md)

### **Examples**
- [Interactive Forecasting Demo](examples/interactive_forecasting_demo.py)
- [Monte Carlo Integration Examples](examples/monte_carlo_examples.py)
- [Scenario Analysis Examples](examples/scenario_analysis_examples.py)

### **Tools and Libraries**
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NumPy Documentation](https://numpy.org/doc/)

---

**Version**: 1.0  
**Last Updated**: 2025-01-17  
**Classification**: UNCLASSIFIED  
**Distribution**: Intelligence Community, Department of Defense
