"""
HTTP-based MCP Server for Monte Carlo Visualization

This module provides an HTTP-based MCP server that can handle JSON-RPC requests
over HTTP, making it compatible with the streamable HTTP client pattern.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    method: str
    params: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

class HTTPMCPServer:
    """HTTP-based MCP server for Monte Carlo visualization tools."""
    
    def __init__(self):
        self.app = FastAPI(title="HTTP MCP Server", version="1.0.0")
        self.tools = {}
        self.setup_middleware()
        self.setup_routes()
        self.register_monte_carlo_visualization_tools()
    
    def setup_middleware(self):
        """Setup CORS middleware."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """Setup API routes."""
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {
                "status": "healthy",
                "service": "http_mcp_server",
                "tools_count": len(self.tools)
            }
        
        @self.app.post("/")
        async def mcp_endpoint(request: MCPRequest):
            """Main MCP endpoint for JSON-RPC requests."""
            try:
                if request.method == "initialize":
                    return MCPResponse(
                        id=request.id,
                        result={
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {}
                            },
                            "serverInfo": {
                                "name": "HTTP MCP Server",
                                "version": "1.0.0"
                            }
                        }
                    )
                
                elif request.method == "tools/list":
                    tools_list = []
                    for tool_name, tool_info in self.tools.items():
                        tools_list.append({
                            "name": tool_name,
                            "description": tool_info.get("description", ""),
                            "inputSchema": tool_info.get("inputSchema", {})
                        })
                    
                    return MCPResponse(
                        id=request.id,
                        result={"tools": tools_list}
                    )
                
                elif request.method == "tools/call":
                    tool_name = request.params.get("name")
                    arguments = request.params.get("arguments", {})
                    
                    if tool_name not in self.tools:
                        return MCPResponse(
                            id=request.id,
                            error={
                                "code": -32601,
                                "message": f"Tool '{tool_name}' not found"
                            }
                        )
                    
                    # Call the tool
                    tool_func = self.tools[tool_name]["function"]
                    try:
                        result = await tool_func(**arguments)
                        return MCPResponse(
                            id=request.id,
                            result={"content": [{"type": "text", "text": str(result)}]}
                        )
                    except Exception as e:
                        return MCPResponse(
                            id=request.id,
                            error={
                                "code": -32603,
                                "message": f"Tool execution failed: {str(e)}"
                            }
                        )
                
                else:
                    return MCPResponse(
                        id=request.id,
                        error={
                            "code": -32601,
                            "message": f"Method '{request.method}' not found"
                        }
                    )
                    
            except Exception as e:
                logger.error(f"Error handling MCP request: {e}")
                return MCPResponse(
                    id=request.id,
                    error={
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                )
    
    def register_monte_carlo_visualization_tools(self):
        """Register Monte Carlo visualization tools."""
        
        async def monte_carlo_visualization_health_check():
            """Health check for Monte Carlo visualization tools."""
            return "Monte Carlo visualization tools are healthy"
        
        async def monte_carlo_create_distribution_plot(data: List[float], title: str = "Distribution Plot"):
            """Create a distribution plot."""
            try:
                # Simulate creating a distribution plot
                return f"Created distribution plot '{title}' with {len(data)} data points"
            except Exception as e:
                return f"Error creating distribution plot: {str(e)}"
        
        async def monte_carlo_create_correlation_matrix(correlation_matrix: List[List[float]], variable_names: List[str]):
            """Create a correlation matrix visualization."""
            try:
                # Simulate creating a correlation matrix
                return f"Created correlation matrix with {len(variable_names)} variables"
            except Exception as e:
                return f"Error creating correlation matrix: {str(e)}"
        
        async def monte_carlo_create_real_time_dashboard(simulation_id: str, update_interval: float = 2.0):
            """Create a real-time dashboard."""
            try:
                # Simulate creating a real-time dashboard
                return f"Created real-time dashboard for simulation {simulation_id} with {update_interval}s updates"
            except Exception as e:
                return f"Error creating real-time dashboard: {str(e)}"
        
        async def monte_carlo_export_visualization(visualization_data: Dict[str, Any], format: str = "json"):
            """Export visualization."""
            try:
                # Simulate exporting visualization
                return f"Exported visualization in {format} format"
            except Exception as e:
                return f"Error exporting visualization: {str(e)}"
        
        # Register the tools
        self.tools.update({
            "monte_carlo_visualization_health_check": {
                "function": monte_carlo_visualization_health_check,
                "description": "Health check for Monte Carlo visualization tools",
                "inputSchema": {}
            },
            "monte_carlo_create_distribution_plot": {
                "function": monte_carlo_create_distribution_plot,
                "description": "Create a distribution plot for Monte Carlo simulation results",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "data": {"type": "array", "items": {"type": "number"}},
                        "title": {"type": "string"}
                    },
                    "required": ["data"]
                }
            },
            "monte_carlo_create_correlation_matrix": {
                "function": monte_carlo_create_correlation_matrix,
                "description": "Create a correlation matrix visualization",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "correlation_matrix": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
                        "variable_names": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["correlation_matrix", "variable_names"]
                }
            },
            "monte_carlo_create_real_time_dashboard": {
                "function": monte_carlo_create_real_time_dashboard,
                "description": "Create a real-time dashboard for Monte Carlo simulations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "simulation_id": {"type": "string"},
                        "update_interval": {"type": "number"}
                    },
                    "required": ["simulation_id"]
                }
            },
            "monte_carlo_export_visualization": {
                "function": monte_carlo_export_visualization,
                "description": "Export visualization in various formats",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "visualization_data": {"type": "object"},
                        "format": {"type": "string"}
                    },
                    "required": ["visualization_data"]
                }
            }
        })
        
        logger.info(f"✅ Registered {len(self.tools)} Monte Carlo visualization tools")
    
    def run(self, host: str = "localhost", port: int = 8000, debug: bool = False):
        """Run the HTTP MCP server."""
        logger.info(f"🚀 Starting HTTP MCP Server on {host}:{port}")
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level="info" if debug else "warning"
        )

def create_http_mcp_server() -> HTTPMCPServer:
    """Create and return an HTTP MCP server instance."""
    return HTTPMCPServer()

if __name__ == "__main__":
    """Run the HTTP MCP server directly."""
    server = create_http_mcp_server()
    server.run(host="localhost", port=8000, debug=True)
