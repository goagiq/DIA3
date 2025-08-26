"""
Example Usage of Dynamic Tooltip System

This file demonstrates how to integrate the dynamic tooltip system
with existing D3.js visualizations and other interactive components.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any

from .tooltip_manager import DynamicTooltipManager, TooltipRequest
from .configuration import TooltipConfiguration, DataSourceConfig, DataSourceType, ContentTemplate, ContentType


async def example_basic_usage():
    """Basic example of using the dynamic tooltip system."""
    print("=== Dynamic Tooltip System - Basic Usage Example ===")
    
    # Initialize the tooltip manager
    config = TooltipConfiguration()
    tooltip_manager = DynamicTooltipManager(config)
    
    # Example 1: Simple tooltip request
    request = TooltipRequest(
        object_id="microsoft",
        object_type="company",
        context={"domain": "technology", "region": "global"}
    )
    
    response = await tooltip_manager.get_tooltip_content(request)
    
    if response.success:
        print(f"✅ Tooltip generated successfully")
        print(f"📊 Data sources used: {response.data_sources_used}")
        print(f"⚡ Response time: {response.response_time:.3f}s")
        print(f"💾 Cached: {response.cached}")
        print(f"📄 HTML Content:\n{response.html_content}")
    else:
        print(f"❌ Failed to generate tooltip: {response.error}")
    
    await tooltip_manager.close()


async def example_d3_integration():
    """Example of integrating with D3.js visualizations."""
    print("\n=== D3.js Integration Example ===")
    
    # Create enhanced HTML with dynamic tooltips
    html_content = create_d3_visualization_with_tooltips()
    
    # Save the enhanced visualization
    output_path = Path("Results/enhanced_visualization_with_dynamic_tooltips.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Enhanced visualization saved to: {output_path}")
    print("🔗 Open the HTML file in a browser to see the dynamic tooltips in action!")


def create_d3_visualization_with_tooltips() -> str:
    """Create a D3.js visualization with integrated dynamic tooltips."""
    
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Visualization with Dynamic Tooltips</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        
        .content {
            padding: 30px;
        }
        
        .graph-container {
            border: 2px solid #ecf0f1;
            border-radius: 10px;
            padding: 20px;
            background: #f8f9fa;
            margin-bottom: 20px;
            position: relative;
            height: 600px;
        }
        
        .node {
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .node:hover {
            stroke-width: 3px;
        }
        
        .link {
            stroke: #95a5a6;
            stroke-width: 2px;
            transition: all 0.3s ease;
        }
        
        .link:hover {
            stroke: #e74c3c;
            stroke-width: 4px;
        }
        
        .node-label {
            font-size: 12px;
            font-weight: bold;
            text-anchor: middle;
            pointer-events: none;
        }
        
        .controls {
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .control-btn {
            background: rgba(255, 255, 255, 0.9);
            border: none;
            border-radius: 8px;
            padding: 10px 15px;
            cursor: pointer;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        }
        
        .control-btn:hover {
            background: rgba(255, 255, 255, 1);
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        }
        
        .info-panel {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .info-panel h3 {
            margin-top: 0;
            color: #2c3e50;
        }
        
        .feature-list {
            list-style: none;
            padding: 0;
        }
        
        .feature-list li {
            padding: 8px 0;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .feature-list li:before {
            content: "✅ ";
            color: #27ae60;
        }
        
        /* Dynamic Tooltip Styles */
        .dynamic-tooltip {
            max-width: 400px;
            max-height: 300px;
            background-color: rgba(0, 0, 0, 0.9);
            color: #ffffff;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            font-family: Arial, sans-serif;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            position: absolute;
            pointer-events: none;
            overflow: hidden;
            word-wrap: break-word;
            line-height: 1.4;
            opacity: 0;
            transition: opacity 0.2s ease-in-out;
        }
        
        .dynamic-tooltip.show {
            opacity: 1;
        }
        
        .tooltip-content h3 {
            margin: 0 0 8px 0;
            font-size: 16px;
            font-weight: bold;
        }
        
        .tooltip-content p {
            margin: 0 0 6px 0;
        }
        
        .tooltip-content ul {
            margin: 4px 0;
            padding-left: 16px;
        }
        
        .tooltip-content li {
            margin: 2px 0;
        }
        
        .tooltip-content .error {
            color: #ff6b6b;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Enhanced Visualization with Dynamic Tooltips</h1>
            <p>Interactive Graph with Comprehensive Tooltip Information</p>
        </div>
        
        <div class="content">
            <div class="graph-container">
                <div class="controls">
                    <button class="control-btn" onclick="resetView()">🔄 Reset View</button>
                    <button class="control-btn" onclick="fitAll()">📐 Fit All Nodes</button>
                    <button class="control-btn" onclick="zoomIn()">➕ Zoom In</button>
                    <button class="control-btn" onclick="zoomOut()">➖ Zoom Out</button>
                    <button class="control-btn" onclick="toggleTooltips()">💡 Toggle Tooltips</button>
                </div>
                <div id="graph"></div>
            </div>
            
            <div class="info-panel">
                <h3>Dynamic Tooltip Features</h3>
                <ul class="feature-list">
                    <li><strong>Multi-Source Data:</strong> Integrates knowledge graph, semantic search, business intelligence, and external APIs</li>
                    <li><strong>Intelligent Caching:</strong> Multi-level caching (memory + disk) with automatic invalidation</li>
                    <li><strong>Fallback Strategy:</strong> Graceful degradation when data sources are unavailable</li>
                    <li><strong>Responsive Design:</strong> Adapts to different screen sizes and orientations</li>
                    <li><strong>Performance Optimized:</strong> Debounced hover events and lazy loading</li>
                    <li><strong>Rich Content:</strong> HTML formatting with relationships, recommendations, and insights</li>
                    <li><strong>Health Monitoring:</strong> Real-time data source health checks and status reporting</li>
                    <li><strong>Configurable Templates:</strong> Customizable content templates for different object types</li>
                </ul>
                
                <h3>How to Use</h3>
                <p>Hover over any node or link in the visualization to see comprehensive information including:</p>
                <ul>
                    <li>Entity details and relationships</li>
                    <li>Business intelligence metrics</li>
                    <li>Semantic search results</li>
                    <li>External data and recent events</li>
                    <li>Actionable recommendations</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // Sample graph data with enhanced information
        const graphData = {
            nodes: [
                {
                    id: "microsoft",
                    name: "Microsoft Corporation",
                    type: "company",
                    group: 0,
                    size: 15,
                    domain: "technology",
                    region: "global",
                    confidence: 0.95
                },
                {
                    id: "azure",
                    name: "Microsoft Azure",
                    type: "service",
                    group: 0,
                    size: 12,
                    domain: "cloud_computing",
                    confidence: 0.88
                },
                {
                    id: "office365",
                    name: "Office 365",
                    type: "service",
                    group: 0,
                    size: 10,
                    domain: "productivity",
                    confidence: 0.92
                },
                {
                    id: "satya_nadella",
                    name: "Satya Nadella",
                    type: "person",
                    group: 1,
                    size: 8,
                    domain: "leadership",
                    confidence: 0.85
                },
                {
                    id: "openai",
                    name: "OpenAI",
                    type: "company",
                    group: 2,
                    size: 12,
                    domain: "ai_research",
                    confidence: 0.90
                },
                {
                    id: "chatgpt",
                    name: "ChatGPT",
                    type: "product",
                    group: 2,
                    size: 10,
                    domain: "ai_application",
                    confidence: 0.87
                }
            ],
            links: [
                { source: "microsoft", target: "azure", value: 8, type: "owns" },
                { source: "microsoft", target: "office365", value: 7, type: "owns" },
                { source: "microsoft", target: "satya_nadella", value: 6, type: "employs" },
                { source: "microsoft", target: "openai", value: 5, type: "invests_in" },
                { source: "openai", target: "chatgpt", value: 9, type: "develops" },
                { source: "azure", target: "chatgpt", value: 4, type: "hosts" }
            ]
        };

        const colors = ["#e74c3c", "#3498db", "#f39c12", "#27ae60", "#9b59b6"];
        let simulation, svg, links, nodes;
        let tooltipsEnabled = true;

        function createGraph() {
            const width = 800;
            const height = 500;
            
            svg = d3.select("#graph")
                .append("svg")
                .attr("width", width)
                .attr("height", height);
            
            // Add zoom behavior
            const zoom = d3.zoom()
                .scaleExtent([0.1, 15])
                .on("zoom", (event) => {
                    svg.selectAll("g").attr("transform", event.transform);
                });
            
            svg.call(zoom);
            
            // Create links
            links = svg.append("g")
                .selectAll("line")
                .data(graphData.links)
                .enter().append("line")
                .attr("class", "link")
                .style("stroke-width", d => Math.sqrt(d.value || 1) * 2);
            
            // Create nodes
            nodes = svg.append("g")
                .selectAll("circle")
                .data(graphData.nodes)
                .enter().append("circle")
                .attr("class", "node")
                .attr("r", d => d.size || 10)
                .style("fill", d => colors[d.group || 0])
                .style("stroke", "#fff")
                .style("stroke-width", 2)
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));
            
            // Add labels
            svg.append("g")
                .selectAll("text")
                .data(graphData.nodes)
                .enter().append("text")
                .attr("class", "node-label")
                .text(d => d.name.length > 15 ? d.name.substring(0, 15) + "..." : d.name)
                .style("fill", "#2c3e50");
            
            // Create simulation
            simulation = d3.forceSimulation(graphData.nodes)
                .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(150))
                .force("charge", d3.forceManyBody().strength(-400))
                .force("center", d3.forceCenter(width / 2, height / 2))
                .force("collision", d3.forceCollide().radius(d => (d.size || 10) + 5))
                .on("tick", ticked);
            
            // Add dynamic tooltip functionality
            integrateDynamicTooltips(nodes);
            integrateDynamicTooltips(links);
        }

        function integrateDynamicTooltips(selection) {
            selection
                .on("mouseover", function(event, d) {
                    if (!tooltipsEnabled) return;
                    
                    const tooltipData = {
                        id: d.id,
                        type: d.type || 'node',
                        context: d
                    };
                    
                    // Show tooltip with dynamic content
                    showDynamicTooltip(tooltipData, event);
                })
                .on("mouseout", function(event, d) {
                    hideDynamicTooltip();
                });
        }

        function showDynamicTooltip(data, event) {
            // Create tooltip content based on data
            const content = generateTooltipContent(data);
            
            // Show tooltip
            const tooltip = d3.select("body")
                .append("div")
                .attr("class", "dynamic-tooltip")
                .style("opacity", 0)
                .html(content);
            
            // Position tooltip
            const tooltipNode = tooltip.node();
            const tooltipRect = tooltipNode.getBoundingClientRect();
            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;
            
            let left = event.pageX + 10;
            let top = event.pageY - 10;
            
            // Adjust if tooltip would go off-screen
            if (left + tooltipRect.width > viewportWidth) {
                left = event.pageX - tooltipRect.width - 10;
            }
            
            if (top + tooltipRect.height > viewportHeight) {
                top = event.pageY - tooltipRect.height - 10;
            }
            
            tooltip
                .style("left", left + "px")
                .style("top", top + "px")
                .transition()
                .duration(200)
                .style("opacity", 1);
        }

        function hideDynamicTooltip() {
            d3.selectAll(".dynamic-tooltip")
                .transition()
                .duration(200)
                .style("opacity", 0)
                .remove();
        }

        function generateTooltipContent(data) {
            const node = graphData.nodes.find(n => n.id === data.id);
            const links = graphData.links.filter(l => l.source.id === data.id || l.target.id === data.id);
            
            let content = `<div class="tooltip-content">`;
            content += `<h3>${node ? node.name : data.id}</h3>`;
            
            if (node) {
                content += `<p><strong>Type:</strong> ${node.type}</p>`;
                content += `<p><strong>Domain:</strong> ${node.domain || 'Unknown'}</p>`;
                content += `<p><strong>Confidence:</strong> ${(node.confidence * 100).toFixed(1)}%</p>`;
                
                if (links.length > 0) {
                    content += `<p><strong>Relationships:</strong></p><ul>`;
                    links.forEach(link => {
                        const target = link.source.id === data.id ? link.target : link.source;
                        content += `<li>${link.type} → ${target.name || target.id}</li>`;
                    });
                    content += `</ul>`;
                }
                
                // Add recommendations based on type
                content += `<p><strong>Recommendations:</strong></p><ul>`;
                if (node.type === 'company') {
                    content += `<li>Explore company relationships</li>`;
                    content += `<li>Check recent news and events</li>`;
                    content += `<li>Analyze market position</li>`;
                } else if (node.type === 'person') {
                    content += `<li>View professional background</li>`;
                    content += `<li>Check current role and responsibilities</li>`;
                    content += `<li>Explore network connections</li>`;
                } else if (node.type === 'service' || node.type === 'product') {
                    content += `<li>Review features and capabilities</li>`;
                    content += `<li>Check pricing and availability</li>`;
                    content += `<li>Compare with alternatives</li>`;
                }
                content += `</ul>`;
            }
            
            content += `</div>`;
            return content;
        }

        function ticked() {
            links
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            
            nodes
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
            
            svg.selectAll(".node-label")
                .attr("x", d => d.x)
                .attr("y", d => d.y + 5);
        }

        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }

        function resetView() {
            if (svg) {
                svg.transition().duration(750).call(
                    d3.zoom().transform,
                    d3.zoomIdentity
                );
            }
        }

        function fitAll() {
            if (svg && simulation) {
                const bounds = svg.node().getBBox();
                const fullWidth = 800;
                const fullHeight = 500;
                const width = bounds.width;
                const height = bounds.height;
                const midX = bounds.x + width / 2;
                const midY = bounds.y + height / 2;
                
                if (width == 0 || height == 0) return;
                
                const scale = 0.8 / Math.max(width / fullWidth, height / fullHeight);
                const translate = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY];
                
                svg.transition().duration(750).call(
                    d3.zoom().transform,
                    d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
                );
            }
        }

        function zoomIn() {
            if (svg) {
                svg.transition().duration(300).call(
                    d3.zoom().scaleBy,
                    1.3
                );
            }
        }

        function zoomOut() {
            if (svg) {
                svg.transition().duration(300).call(
                    d3.zoom().scaleBy,
                    0.7
                );
            }
        }

        function toggleTooltips() {
            tooltipsEnabled = !tooltipsEnabled;
            const button = event.target;
            if (tooltipsEnabled) {
                button.textContent = "💡 Disable Tooltips";
                button.style.background = "rgba(39, 174, 96, 0.9)";
            } else {
                button.textContent = "💡 Enable Tooltips";
                button.style.background = "rgba(255, 255, 255, 0.9)";
                hideDynamicTooltip();
            }
        }

        // Initialize the graph
        createGraph();
    </script>
</body>
</html>"""
    
    return html_template


async def example_api_integration():
    """Example of creating an API endpoint for tooltip requests."""
    print("\n=== API Integration Example ===")
    
    # This would be part of your FastAPI or Flask application
    api_code = """
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

@app.get("/api/tooltip/status")
async def get_tooltip_status():
    tooltip_manager = get_tooltip_manager()
    return tooltip_manager.get_system_status()

@app.post("/api/tooltip/cache/clear")
async def clear_tooltip_cache():
    tooltip_manager = get_tooltip_manager()
    await tooltip_manager.clear_cache()
    return {"message": "Cache cleared successfully"}
"""
    
    # Save API example
    api_path = Path("src/api/tooltip_api_example.py")
    api_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(api_path, 'w', encoding='utf-8') as f:
        f.write(api_code)
    
    print(f"✅ API integration example saved to: {api_path}")
    print("🚀 Use this code as a starting point for your FastAPI integration")


async def example_custom_configuration():
    """Example of custom configuration for specific use cases."""
    print("\n=== Custom Configuration Example ===")
    
    # Create custom configuration
    config = TooltipConfiguration()
    
    # Add custom data source
    custom_source = DataSourceConfig(
        name="custom_analytics",
        type=DataSourceType.API,
        priority=9,
        timeout=20,
        description="Custom analytics data source"
    )
    config.add_data_source("custom_analytics", custom_source)
    
    # Add custom template
    custom_template = ContentTemplate(
        name="custom_entity",
        content_type=ContentType.RICH_TEXT,
        template="""
        <div class="tooltip-content">
            <h3>{name}</h3>
            <p><strong>Type:</strong> {type}</p>
            <p><strong>Custom Field:</strong> {custom_field}</p>
            {description}
            {custom_insights}
        </div>
        """,
        variables=["name", "type", "custom_field", "description", "custom_insights"]
    )
    config.add_template("custom_entity", custom_template)
    
    # Customize styling
    config.style.max_width = 500
    config.style.background_color = "rgba(44, 62, 80, 0.95)"
    config.style.text_color = "#ecf0f1"
    
    # Save custom configuration
    config_path = Path("config/custom_tooltip_config.json")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config.save_to_file(str(config_path))
    
    print(f"✅ Custom configuration saved to: {config_path}")
    print("🔧 Use this configuration for specialized tooltip requirements")


async def main():
    """Run all examples."""
    try:
        await example_basic_usage()
        await example_d3_integration()
        await example_api_integration()
        await example_custom_configuration()
        
        print("\n🎉 All examples completed successfully!")
        print("\n📚 Next Steps:")
        print("1. Open the enhanced visualization HTML file in your browser")
        print("2. Hover over nodes and links to see dynamic tooltips")
        print("3. Integrate the API endpoints into your application")
        print("4. Customize configurations for your specific needs")
        print("5. Add your own data sources and templates")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    asyncio.run(main())
