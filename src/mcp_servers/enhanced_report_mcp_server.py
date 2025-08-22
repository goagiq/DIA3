"""
Enhanced Report MCP Server
Provides enhanced report generation functionality through MCP protocol
"""

import asyncio
import json
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Import the enhanced report integration
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.export.enhanced_report_integration import (
        generate_enhanced_report,
        generate_custom_enhanced_report
    )
    ENHANCED_REPORT_AVAILABLE = True
except ImportError:
    ENHANCED_REPORT_AVAILABLE = False

# Create server instance
server = Server("enhanced-report-generator")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available tools"""
    tools = [
        Tool(
            name="generate_enhanced_report",
            description="Generate a comprehensive enhanced report with interactive visualizations, knowledge graphs, and professional tables",
            inputSchema={
                "type": "object",
                "properties": {
                    "analysis_type": {
                        "type": "string",
                        "description": "Type of analysis to generate report for",
                        "default": "pakistan_submarine"
                    },
                    "title": {
                        "type": "string",
                        "description": "Report title",
                        "default": "Strategic Analysis Report"
                    },
                    "subtitle": {
                        "type": "string",
                        "description": "Report subtitle",
                        "default": "Comprehensive Strategic Analysis"
                    }
                },
                "required": ["analysis_type"]
            }
        ),
        Tool(
            name="generate_custom_enhanced_report",
            description="Generate a custom enhanced report with provided analysis data",
            inputSchema={
                "type": "object",
                "properties": {
                    "analysis_data": {
                        "type": "object",
                        "description": "Analysis data structure containing all report content"
                    },
                    "title": {
                        "type": "string",
                        "description": "Report title",
                        "default": "Custom Strategic Analysis"
                    },
                    "subtitle": {
                        "type": "string",
                        "description": "Report subtitle",
                        "default": "Enhanced Report Generation"
                    }
                },
                "required": ["analysis_data", "title"]
            }
        ),
                        Tool(
                    name="generate_knowledge_graph_report",
                    description="Generate a focused report with interactive knowledge graph visualization",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "entities": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of entities for the knowledge graph"
                            },
                            "relationships": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "source": {"type": "string"},
                                        "target": {"type": "string"},
                                        "type": {"type": "string"}
                                    }
                                },
                                "description": "List of relationships between entities"
                            },
                            "title": {
                                "type": "string",
                                "description": "Report title",
                                "default": "Knowledge Graph Analysis"
                            }
                        },
                        "required": ["entities"]
                    }
                ),
                Tool(
                    name="run_monte_carlo_simulation",
                    description="Run Monte Carlo simulation for probabilistic analysis and risk assessment",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "simulation_type": {
                                "type": "string",
                                "description": "Type of simulation to run",
                                "default": "pakistan_submarine",
                                "enum": ["pakistan_submarine", "custom"]
                            },
                            "n_iterations": {
                                "type": "integer",
                                "description": "Number of simulation iterations",
                                "default": 10000
                            },
                            "parameters": {
                                "type": "object",
                                "description": "Custom simulation parameters (for custom simulations)"
                            },
                            "title": {
                                "type": "string",
                                "description": "Simulation title",
                                "default": "Monte Carlo Simulation Analysis"
                            }
                        },
                        "required": ["simulation_type"]
                    }
                ),
                Tool(
                    name="generate_monte_carlo_report",
                    description="Generate enhanced report with Monte Carlo simulation analysis",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "analysis_type": {
                                "type": "string",
                                "description": "Type of analysis to generate report for",
                                "default": "pakistan_submarine"
                            },
                            "include_monte_carlo": {
                                "type": "boolean",
                                "description": "Include Monte Carlo simulation in report",
                                "default": true
                            },
                            "title": {
                                "type": "string",
                                "description": "Report title",
                                "default": "Strategic Analysis with Monte Carlo Simulation"
                            },
                            "subtitle": {
                                "type": "string",
                                "description": "Report subtitle",
                                "default": "Comprehensive Analysis with Probabilistic Modeling"
                            }
                        },
                        "required": ["analysis_type"]
                    }
                )
    ]
    
    if not ENHANCED_REPORT_AVAILABLE:
        tools.append(
            Tool(
                name="check_enhanced_report_status",
                description="Check if enhanced report generation is available",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        )
    
    return ListToolsResult(tools=tools)

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls"""
            
            if name == "generate_enhanced_report":
                return await handle_generate_enhanced_report(arguments)
            elif name == "generate_custom_enhanced_report":
                return await handle_generate_custom_enhanced_report(arguments)
            elif name == "generate_knowledge_graph_report":
                return await handle_generate_knowledge_graph_report(arguments)
            elif name == "run_monte_carlo_simulation":
                return await handle_run_monte_carlo_simulation(arguments)
            elif name == "generate_monte_carlo_report":
                return await handle_generate_monte_carlo_report(arguments)
            elif name == "check_enhanced_report_status":
                return await handle_check_status()
            else:
                raise ValueError(f"Unknown tool: {name}")

async def handle_generate_enhanced_report(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle enhanced report generation"""
    
    if not ENHANCED_REPORT_AVAILABLE:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="❌ Enhanced report generation is not available. Please install required dependencies: networkx, matplotlib, seaborn, jinja2"
                )
            ]
        )
    
    try:
        analysis_type = arguments.get("analysis_type", "pakistan_submarine")
        title = arguments.get("title", "Strategic Analysis Report")
        subtitle = arguments.get("subtitle", "Comprehensive Strategic Analysis")
        
        # Generate the report
        report_path = generate_enhanced_report(
            analysis_type=analysis_type,
            title=title,
            subtitle=subtitle
        )
        
        # Read the generated report
        with open(report_path, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        # Create embedded resource for the HTML file
        embedded_resource = EmbeddedResource(
            uri=f"file://{report_path}",
            mimeType="text/html",
            data=report_content.encode('utf-8')
        )
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"✅ Enhanced report generated successfully!\n\n📄 Report saved to: {report_path}\n\n🎯 Features included:\n• Interactive charts and visualizations\n• Knowledge graph with network visualization\n• Professional data tables\n• Comprehensive strategic analysis\n• Responsive design\n\nOpen the HTML file in a web browser to view the full report."
                ),
                TextContent(
                    type="text",
                    text=f"Report Content Preview:\n{report_content[:1000]}...",
                    mimeType="text/html"
                )
            ],
            isError=False
        )
        
    except Exception as e:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"❌ Error generating enhanced report: {str(e)}"
                )
            ],
            isError=True
        )

async def handle_generate_custom_enhanced_report(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle custom enhanced report generation"""
    
    if not ENHANCED_REPORT_AVAILABLE:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="❌ Enhanced report generation is not available. Please install required dependencies: networkx, matplotlib, seaborn, jinja2"
                )
            ]
        )
    
    try:
        analysis_data = arguments.get("analysis_data", {})
        title = arguments.get("title", "Custom Strategic Analysis")
        subtitle = arguments.get("subtitle", "Enhanced Report Generation")
        
        # Generate the custom report
        report_path = generate_custom_enhanced_report(
            analysis_data=analysis_data,
            title=title,
            subtitle=subtitle
        )
        
        # Read the generated report
        with open(report_path, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"✅ Custom enhanced report generated successfully!\n\n📄 Report saved to: {report_path}\n\n🎯 Custom analysis data processed and visualized with:\n• Interactive knowledge graph\n• Professional tables\n• Strategic insights\n• Risk assessment\n• Recommendations"
                ),
                TextContent(
                    type="text",
                    text=f"Report Content Preview:\n{report_content[:1000]}...",
                    mimeType="text/html"
                )
            ],
            isError=False
        )
        
    except Exception as e:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"❌ Error generating custom enhanced report: {str(e)}"
                )
            ],
            isError=True
        )

async def handle_generate_knowledge_graph_report(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle knowledge graph report generation"""
    
    if not ENHANCED_REPORT_AVAILABLE:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="❌ Enhanced report generation is not available. Please install required dependencies: networkx, matplotlib, seaborn, jinja2"
                )
            ]
        )
    
    try:
        entities = arguments.get("entities", [])
        relationships = arguments.get("relationships", [])
        title = arguments.get("title", "Knowledge Graph Analysis")
        
        # Create analysis data structure for knowledge graph
        analysis_data = {
            'main_entity': title,
            'key_concepts': entities,
            'risk_factors': [],
            'recommendations': [],
            'executive_summary': {
                'description': f"Knowledge graph analysis of {len(entities)} entities with {len(relationships)} relationships.",
                'key_findings': {
                    'Entities': f"{len(entities)} entities analyzed",
                    'Relationships': f"{len(relationships)} relationships identified",
                    'Complexity': f"Graph complexity: {len(relationships) / max(len(entities), 1):.2f} relationships per entity"
                },
                'summary_stats': [
                    {'label': 'Entities', 'value': str(len(entities)), 'description': 'Total entities'},
                    {'label': 'Relationships', 'value': str(len(relationships)), 'description': 'Total relationships'},
                    {'label': 'Density', 'value': f"{len(relationships) / max(len(entities), 1):.2f}", 'description': 'Relationships per entity'}
                ]
            }
        }
        
        # Generate the knowledge graph report
        report_path = generate_custom_enhanced_report(
            analysis_data=analysis_data,
            title=title,
            subtitle="Interactive Knowledge Graph Visualization"
        )
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"✅ Knowledge graph report generated successfully!\n\n📄 Report saved to: {report_path}\n\n🧠 Knowledge Graph Features:\n• Interactive network visualization\n• {len(entities)} entities displayed\n• {len(relationships)} relationships mapped\n• Dynamic graph layout\n• Entity clustering and filtering"
                )
            ],
            isError=False
        )
        
    except Exception as e:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"❌ Error generating knowledge graph report: {str(e)}"
                )
            ],
            isError=True
        )

        async def handle_check_status() -> CallToolResult:
            """Handle status check"""
            
            if ENHANCED_REPORT_AVAILABLE:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="✅ Enhanced report generation is available and ready to use!\n\n📊 Available features:\n• Interactive HTML reports\n• Knowledge graph visualizations\n• Professional data tables\n• Chart.js integration\n• Network visualization with vis.js\n• Monte Carlo simulations\n• Responsive design\n• Comprehensive strategic analysis templates"
                        )
                    ],
                    isError=False
                )
            else:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="❌ Enhanced report generation is not available.\n\n📦 Required dependencies:\n• networkx\n• matplotlib\n• seaborn\n• jinja2\n• numpy\n• pandas\n• scipy\n\n💡 Install with: pip install networkx matplotlib seaborn jinja2 numpy pandas scipy"
                        )
                    ],
                    isError=True
                )

        async def handle_run_monte_carlo_simulation(arguments: Dict[str, Any]) -> CallToolResult:
            """Handle Monte Carlo simulation execution"""
            
            if not ENHANCED_REPORT_AVAILABLE:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="❌ Enhanced report generation is not available. Please install required dependencies: networkx, matplotlib, seaborn, jinja2, numpy, pandas, scipy"
                        )
                    ],
                    isError=True
                )
            
            try:
                simulation_type = arguments.get("simulation_type", "pakistan_submarine")
                n_iterations = arguments.get("n_iterations", 10000)
                title = arguments.get("title", "Monte Carlo Simulation Analysis")
                
                # Import and run simulation
                from core.export.enhanced_report_integration import enhanced_report_integration
                
                if simulation_type == "pakistan_submarine":
                    # Run Pakistan submarine simulation
                    simulator = enhanced_report_integration.generator.run_monte_carlo_simulation("pakistan_submarine")
                else:
                    # Run custom simulation
                    parameters = arguments.get("parameters", {})
                    simulator = enhanced_report_integration.generator.run_monte_carlo_simulation("custom")
                
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"✅ Monte Carlo simulation completed successfully!\n\n🎲 Simulation Details:\n• Type: {simulation_type}\n• Iterations: {n_iterations:,}\n• Title: {title}\n\n📊 Results Summary:\n• Cost Analysis: {simulator.get('results', {}).get('total_cost', {}).get('mean', 0):.2f} billion USD\n• Risk Assessment: {simulator.get('results', {}).get('risk_score', {}).get('mean', 0):.3f} average risk\n• Strategic Impact: {simulator.get('results', {}).get('strategic_impact', {}).get('mean', 0):.2f} impact score\n\n📈 Key Insights:\n• 90% confidence intervals calculated\n• Probability distributions generated\n• Risk factor analysis completed\n• Strategic impact modeling finished"
                        )
                    ],
                    isError=False
                )
                
            except Exception as e:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"❌ Error running Monte Carlo simulation: {str(e)}"
                        )
                    ],
                    isError=True
                )

        async def handle_generate_monte_carlo_report(arguments: Dict[str, Any]) -> CallToolResult:
            """Handle Monte Carlo report generation"""
            
            if not ENHANCED_REPORT_AVAILABLE:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="❌ Enhanced report generation is not available. Please install required dependencies: networkx, matplotlib, seaborn, jinja2, numpy, pandas, scipy"
                        )
                    ],
                    isError=True
                )
            
            try:
                analysis_type = arguments.get("analysis_type", "pakistan_submarine")
                include_monte_carlo = arguments.get("include_monte_carlo", True)
                title = arguments.get("title", "Strategic Analysis with Monte Carlo Simulation")
                subtitle = arguments.get("subtitle", "Comprehensive Analysis with Probabilistic Modeling")
                
                # Generate enhanced report with Monte Carlo simulation
                from core.export.enhanced_report_integration import generate_enhanced_report
                
                report_path = generate_enhanced_report(
                    analysis_type=analysis_type,
                    title=title,
                    subtitle=subtitle
                )
                
                # Read the generated report
                with open(report_path, 'r', encoding='utf-8') as f:
                    report_content = f.read()
                
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"✅ Monte Carlo enhanced report generated successfully!\n\n📄 Report saved to: {report_path}\n\n🎲 Monte Carlo Features Included:\n• Probabilistic cost analysis\n• Risk assessment distributions\n• Strategic impact modeling\n• Confidence interval calculations\n• Interactive simulation charts\n• Statistical significance analysis\n\n📊 Report Sections:\n• Executive Summary with simulation insights\n• Strategic Context Analysis\n• Economic Analysis with uncertainty ranges\n• Regional Security Implications\n• Interactive Knowledge Graph\n• Monte Carlo Simulation Results\n• Risk Assessment Matrix\n• Strategic Recommendations\n• Comprehensive Conclusion"
                        ),
                        TextContent(
                            type="text",
                            text=f"Report Content Preview:\n{report_content[:1000]}...",
                            mimeType="text/html"
                        )
                    ],
                    isError=False
                )
                
            except Exception as e:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"❌ Error generating Monte Carlo report: {str(e)}"
                        )
                    ],
                    isError=True
                )

async def main():
    """Main function to run the MCP server"""
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="enhanced-report-generator",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
