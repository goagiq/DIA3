# Dynamic Tooltip System

## 🎯 **Overview**

The Dynamic Tooltip System is a comprehensive toolkit for interactive visualizations that provides rich, context-aware tooltips with data from multiple sources. It's designed to be highly reliable, performant, and easily extensible.

## 🚀 **Key Features**

### **Multi-Source Data Integration**
- ✅ **Knowledge Graph**: Entity relationships and semantic connections
- ✅ **Semantic Search**: Contextual information and related concepts
- ✅ **Business Intelligence**: Analytics, metrics, and insights
- ✅ **External APIs**: Real-time data from various sources
- ✅ **Custom Data Sources**: Easy integration of your own data providers

### **Intelligent Content Generation**
- ✅ **Template-Based**: Configurable templates for different object types
- ✅ **Context-Aware**: Content adapts based on object type and available data
- ✅ **Rich Formatting**: HTML, Markdown, JSON, and plain text support
- ✅ **Fallback Strategy**: Graceful degradation when data sources fail
- ✅ **Recommendations**: Actionable insights and suggestions

### **Performance & Reliability**
- ✅ **Multi-Level Caching**: Memory and disk caching with intelligent invalidation
- ✅ **Health Monitoring**: Real-time data source health checks
- ✅ **Fallback Mechanisms**: Automatic failover to backup sources
- ✅ **Debounced Events**: Optimized hover handling for smooth performance
- ✅ **Resource Management**: Automatic cleanup and memory management

### **Visual Design**
- ✅ **Responsive Design**: Adapts to different screen sizes
- ✅ **Smooth Animations**: CSS transitions and D3.js animations
- ✅ **Smart Positioning**: Automatic positioning to avoid screen edges
- ✅ **Accessibility**: ARIA labels and keyboard navigation support
- ✅ **Customizable Styling**: Configurable colors, fonts, and layouts

## 🏗️ **Architecture**

### **Core Components**

```
src/core/dynamic_tooltip/
├── __init__.py                 # Package initialization
├── tooltip_manager.py          # Main orchestrator
├── data_source_registry.py     # Data source management
├── content_generator.py        # Content generation engine
├── tooltip_renderer.py         # Visual rendering system
├── cache_manager.py            # Multi-level caching
├── configuration.py            # Configuration management
└── example_usage.py           # Usage examples
```

### **Data Flow**

```
User Hover → TooltipManager → DataSourceRegistry → ContentGenerator → TooltipRenderer → HTML Output
                ↓                    ↓                    ↓                    ↓
            Cache Check         Health Check         Template Match         Style Apply
                ↓                    ↓                    ↓                    ↓
            Cache Hit/Miss      Source Selection     Variable Binding     Position Calc
```

## 📋 **Installation & Setup**

### **1. Install Dependencies**

```bash
pip install fastapi pydantic pyyaml asyncio
```

### **2. Basic Usage**

```python
from src.core.dynamic_tooltip import DynamicTooltipManager, TooltipRequest

# Initialize the tooltip manager
tooltip_manager = DynamicTooltipManager()

# Create a tooltip request
request = TooltipRequest(
    object_id="microsoft",
    object_type="company",
    context={"domain": "technology", "region": "global"}
)

# Get tooltip content
response = await tooltip_manager.get_tooltip_content(request)

if response.success:
    print(f"HTML Content: {response.html_content}")
    print(f"Data sources used: {response.data_sources_used}")
    print(f"Response time: {response.response_time:.3f}s")
```

### **3. D3.js Integration**

```javascript
// Add dynamic tooltips to D3 elements
function integrateDynamicTooltips(selection) {
    selection
        .on('mouseover', function(event, d) {
            const tooltipData = {
                id: d.id,
                type: d.type || 'node',
                context: d
            };
            
            // Show tooltip with dynamic content
            dynamicTooltip.showTooltip(tooltipData);
        })
        .on('mouseout', function(event, d) {
            dynamicTooltip.hideTooltip();
        });
}

// Apply to existing D3 elements
d3.selectAll('.node').call(integrateDynamicTooltips);
```

## ⚙️ **Configuration**

### **Data Source Configuration**

```python
from src.core.dynamic_tooltip.configuration import DataSourceConfig, DataSourceType

# Configure a custom data source
custom_source = DataSourceConfig(
    name="my_api",
    type=DataSourceType.API,
    priority=8,
    timeout=30,
    retry_attempts=3,
    cache_ttl=300,
    description="My custom API data source"
)
```

### **Content Template Configuration**

```python
from src.core.dynamic_tooltip.configuration import ContentTemplate, ContentType

# Create a custom template
custom_template = ContentTemplate(
    name="my_entity",
    content_type=ContentType.RICH_TEXT,
    template="""
    <div class="tooltip-content">
        <h3>{name}</h3>
        <p><strong>Type:</strong> {type}</p>
        <p><strong>Custom Field:</strong> {custom_field}</p>
        {description}
        {recommendations}
    </div>
    """,
    variables=["name", "type", "custom_field", "description", "recommendations"]
)
```

### **Styling Configuration**

```python
from src.core.dynamic_tooltip.configuration import TooltipStyle

# Customize tooltip appearance
style = TooltipStyle(
    max_width=500,
    max_height=400,
    background_color="rgba(44, 62, 80, 0.95)",
    text_color="#ecf0f1",
    border_radius=12,
    padding=16,
    font_size="16px",
    font_family="'Segoe UI', Arial, sans-serif"
)
```

## 🔌 **API Integration**

### **FastAPI Endpoint**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from src.core.dynamic_tooltip.tooltip_manager import get_tooltip_manager, TooltipRequest

app = FastAPI(title="Dynamic Tooltip API")

class TooltipRequestModel(BaseModel):
    object_id: str
    object_type: str
    context: Optional[Dict[str, Any]] = None
    template_name: Optional[str] = None
    data_sources: Optional[list[str]] = None
    cache_ttl: Optional[int] = None

@app.post("/api/tooltip")
async def get_tooltip(request: TooltipRequestModel):
    try:
        tooltip_manager = get_tooltip_manager()
        
        tooltip_request = TooltipRequest(
            object_id=request.object_id,
            object_type=request.object_type,
            context=request.context or {},
            template_name=request.template_name,
            data_sources=request.data_sources,
            cache_ttl=request.cache_ttl
        )
        
        response = await tooltip_manager.get_tooltip_content(tooltip_request)
        
        return {
            "success": response.success,
            "html_content": response.html_content,
            "data_sources_used": response.data_sources_used,
            "response_time": response.response_time,
            "cached": response.cached,
            "error": response.error
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## 📊 **Performance Monitoring**

### **System Status**

```python
# Get system status and health information
status = tooltip_manager.get_system_status()

print("Data Sources:")
for name, info in status["data_sources"].items():
    print(f"  {name}: {info['health']['status']}")

print(f"Cache Hit Rate: {status['performance']['cache_hit_rate']:.2%}")
print(f"Average Response Time: {status['performance']['average_response_time']:.3f}s")
```

### **Cache Statistics**

```python
# Get cache performance metrics
cache_stats = await tooltip_manager.cache_manager.get_cache_stats()

print(f"Memory Cache Size: {cache_stats['memory_cache_size']}")
print(f"Disk Cache Entries: {cache_stats['disk_cache_entries']}")
print(f"Disk Cache Size: {cache_stats['disk_cache_total_size_mb']:.2f} MB")
```

## 🎨 **Customization Examples**

### **Custom Data Source**

```python
async def my_custom_query(entity_id: str, **kwargs) -> Dict[str, Any]:
    """Custom data source query function."""
    # Your custom logic here
    return {
        "entity_id": entity_id,
        "custom_data": "Your custom information",
        "metrics": {"custom_metric": 0.85},
        "insights": ["Custom insight 1", "Custom insight 2"]
    }

# Register the custom data source
tooltip_manager.data_source_registry.register_data_source(
    "my_custom_source",
    custom_source_config,
    my_custom_query
)
```

### **Custom Template**

```python
# Add a custom template for specific object types
custom_template = ContentTemplate(
    name="financial_entity",
    content_type=ContentType.RICH_TEXT,
    template="""
    <div class="tooltip-content">
        <h3>{name}</h3>
        <p><strong>Type:</strong> {type}</p>
        <p><strong>Market Cap:</strong> ${market_cap:,.0f}</p>
        <p><strong>P/E Ratio:</strong> {pe_ratio:.2f}</p>
        {financial_metrics}
        {market_analysis}
        {investment_recommendations}
    </div>
    """,
    variables=["name", "type", "market_cap", "pe_ratio", "financial_metrics", "market_analysis", "investment_recommendations"]
)

tooltip_manager.content_generator.add_template("financial_entity", custom_template)
```

## 🔧 **Advanced Features**

### **Preloading Tooltips**

```python
# Preload tooltips for better performance
objects_to_preload = [
    {"id": "microsoft", "type": "company", "context": {"domain": "technology"}},
    {"id": "apple", "type": "company", "context": {"domain": "technology"}},
    {"id": "google", "type": "company", "context": {"domain": "technology"}}
]

await tooltip_manager.preload_tooltips(objects_to_preload)
```

### **Dynamic Configuration Updates**

```python
# Update configuration at runtime
new_config = TooltipConfiguration()
new_config.style.max_width = 600
new_config.cache.memory_cache_size = 2000

await tooltip_manager.update_configuration(new_config)
```

### **Health Monitoring**

```python
# Monitor data source health
health_status = tooltip_manager.data_source_registry.get_health_status()

for source_name, health in health_status.items():
    print(f"{source_name}: {health.status.value}")
    print(f"  Response Time: {health.response_time:.3f}s")
    print(f"  Success Rate: {health.success_count / (health.success_count + health.error_count):.2%}")
```

## 🚀 **Best Practices**

### **Performance Optimization**

1. **Use Caching**: Leverage the built-in multi-level caching system
2. **Preload Data**: Preload tooltips for frequently accessed objects
3. **Debounce Events**: Use the built-in debouncing for hover events
4. **Monitor Health**: Regularly check data source health status
5. **Optimize Templates**: Keep templates lightweight and efficient

### **Reliability**

1. **Fallback Strategy**: Always provide fallback content
2. **Error Handling**: Implement proper error handling for data sources
3. **Health Checks**: Monitor data source health and performance
4. **Graceful Degradation**: Ensure system works even when some sources fail
5. **Resource Management**: Properly close and cleanup resources

### **User Experience**

1. **Responsive Design**: Ensure tooltips work on all screen sizes
2. **Smooth Animations**: Use CSS transitions for smooth interactions
3. **Smart Positioning**: Avoid tooltips going off-screen
4. **Accessibility**: Include proper ARIA labels and keyboard support
5. **Loading States**: Show loading indicators for slow data sources

## 📈 **Monitoring & Analytics**

### **Performance Metrics**

- **Response Time**: Average time to generate tooltip content
- **Cache Hit Rate**: Percentage of requests served from cache
- **Data Source Health**: Status and performance of each data source
- **Error Rates**: Frequency of failures and errors
- **User Engagement**: Tooltip interaction patterns

### **Health Checks**

```python
# Automated health monitoring
async def monitor_system_health():
    while True:
        status = tooltip_manager.get_system_status()
        
        # Check data source health
        for name, info in status["data_sources"].items():
            if info["health"]["status"] == "unhealthy":
                logger.warning(f"Data source {name} is unhealthy")
        
        # Check cache performance
        if status["performance"]["cache_hit_rate"] < 0.5:
            logger.warning("Cache hit rate is low")
        
        await asyncio.sleep(300)  # Check every 5 minutes
```

## 🔮 **Future Enhancements**

### **Planned Features**

- **Machine Learning**: Intelligent content personalization
- **Real-time Updates**: Live data streaming and updates
- **Advanced Analytics**: Detailed usage analytics and insights
- **Plugin System**: Extensible plugin architecture
- **Multi-language Support**: Internationalization and localization
- **Advanced Styling**: CSS-in-JS and theme system
- **Mobile Optimization**: Touch-friendly interactions
- **Voice Integration**: Voice-activated tooltip system

### **Integration Roadmap**

- **GraphQL Support**: GraphQL API integration
- **Microservices**: Distributed tooltip service architecture
- **Cloud Integration**: AWS, Azure, and GCP integrations
- **CDN Support**: Global content delivery optimization
- **Real-time Collaboration**: Multi-user tooltip interactions

## 📚 **Additional Resources**

### **Documentation**

- [API Reference](docs/API_REFERENCE.md)
- [Configuration Guide](docs/CONFIGURATION_GUIDE.md)
- [Integration Examples](docs/INTEGRATION_EXAMPLES.md)
- [Performance Tuning](docs/PERFORMANCE_TUNING.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

### **Examples**

- [Basic Usage](src/core/dynamic_tooltip/example_usage.py)
- [D3.js Integration](examples/d3_integration.html)
- [API Integration](examples/api_integration.py)
- [Custom Templates](examples/custom_templates.py)

### **Community**

- [GitHub Issues](https://github.com/your-repo/issues)
- [Discussions](https://github.com/your-repo/discussions)
- [Contributing Guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

---

## 🎉 **Getting Started**

1. **Install the system**: Follow the installation instructions above
2. **Run the examples**: Execute `python src/core/dynamic_tooltip/example_usage.py`
3. **Explore the visualization**: Open the generated HTML file in your browser
4. **Customize for your needs**: Modify configurations and add custom data sources
5. **Integrate into your application**: Use the API endpoints or direct integration

The Dynamic Tooltip System provides a robust, scalable, and highly customizable solution for creating rich, interactive tooltips that enhance user experience and provide valuable insights from multiple data sources.
