"""
Minimal MCP Server for port 8000 with proper MCP protocol support.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# Import comprehensive enhanced report generator
try:
    from src.core.comprehensive_enhanced_report_generator import comprehensive_enhanced_report_generator
    COMPREHENSIVE_REPORT_AVAILABLE = True
    logger.info("✅ Comprehensive enhanced report generator available")
except ImportError as e:
    COMPREHENSIVE_REPORT_AVAILABLE = False
    logger.warning(f"⚠️ Comprehensive enhanced report generator not available: {e}")

# Initialize FastAPI app with comprehensive functionality
app = FastAPI(
    title="DIA3 Combined API with MCP Integration",
    description="AI-powered sentiment analysis with MCP server integration on port 8000",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global session storage for MCP
mcp_sessions = {}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Minimal MCP Server",
        "version": "1.0.0",
        "status": "running",
        "port": 8000,
        "endpoints": {
            "health": "/health",
            "mcp": "/mcp",
            "mcp_stream": "/mcp/stream"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check system health and status."""
    return {
        "status": "healthy",
        "message": "Minimal MCP server running",
        "mcp_server_available": True
    }

# MCP endpoint for streamable HTTP protocol
@app.post("/mcp")
async def mcp_endpoint(request: dict):
    """MCP endpoint for streamable HTTP protocol."""
    try:
        # Handle MCP protocol requests
        method = request.get("method")
        request_id = request.get("id")
        params = request.get("params", {})
        
        logger.info(f"MCP request: {method} (ID: {request_id})")
        
        if method == "initialize":
            # Handle MCP initialize request
            logger.info("Handling MCP initialize request")
            
            # Create session
            session_id = f"session_{request_id}"
            mcp_sessions[session_id] = {
                "initialized": True,
                "tools_available": True
            }
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "DIA3 Minimal MCP Server",
                        "version": "1.0.0"
                    }
                }
            }
        elif method == "tools/list":
            # Handle MCP tools/list request - Reduced to core essential tools
            tools = [
                {
                    "name": "generate_enhanced_report",
                    "description": "Generate enhanced report with source tracking",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "report_type": {"type": "string"},
                            "include_tooltips": {"type": "boolean"},
                            "include_source_references": {"type": "boolean"},
                            "include_calculations": {"type": "boolean"},
                            "language": {"type": "string"},
                            "options": {"type": "object"}
                        }
                    }
                },
                {
                    "name": "process_content",
                    "description": "Enhanced unified content processing with bulk import, Open Library support, and intelligent MCP tool detection",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "content_type": {"type": "string"},
                            "language": {"type": "string"},
                            "options": {"type": "object"}
                        }
                    }
                },
                {
                    "name": "sentiment_analysis",
                    "description": "Sentiment analysis with multilingual support",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "language": {"type": "string"},
                            "analysis_type": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "entity_extraction",
                    "description": "Entity extraction and relationship mapping",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "entity_types": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                {
                    "name": "knowledge_graph",
                    "description": "Knowledge graph creation and management",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "graph_type": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "business_intelligence",
                    "description": "Business intelligence analysis",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "analysis_type": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "data_visualization",
                    "description": "Data visualization generation",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "data": {"type": "object"},
                            "chart_type": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "semantic_search",
                    "description": "Semantic search across all content",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "search_type": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "advanced_forecasting",
                    "description": "Advanced multivariate forecasting",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "data": {"type": "object"},
                            "forecast_horizon": {"type": "integer"},
                            "confidence_level": {"type": "number"}
                        }
                    }
                },
                {
                    "name": "generate_recommendations",
                    "description": "Generate AI-powered recommendations",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "context": {"type": "string"},
                            "recommendation_type": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "get_agent_status",
                    "description": "Get status of all agents",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "start_agent_swarm",
                    "description": "Start agent swarm",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "swarm_type": {"type": "string"},
                            "parameters": {"type": "object"}
                        }
                    }
                },
                {
                    "name": "stop_agent_swarm",
                    "description": "Stop agent swarm",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "swarm_id": {"type": "string"}
                        }
                    }
                }
            ]
            
            # Add comprehensive enhanced report tool if available
            if COMPREHENSIVE_REPORT_AVAILABLE:
                tools.append({
                    "name": "generate_comprehensive_enhanced_report",
                    "description": "Generate comprehensive enhanced report with all missing components",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "title": {"type": "string"},
                            "subtitle": {"type": "string"},
                            "include_all_components": {"type": "boolean"}
                        }
                    }
                })
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": tools
                }
            }
        elif method == "tools/call":
            # Handle MCP tools/call request
            params = request.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "generate_enhanced_report":
                # Simple response for now
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Enhanced report generated for content: {arguments.get('content', 'No content')}"
                            }
                        ]
                    }
                }
            elif tool_name == "generate_comprehensive_enhanced_report" and COMPREHENSIVE_REPORT_AVAILABLE:
                # Generate comprehensive enhanced report
                try:
                    result = await comprehensive_enhanced_report_generator.generate_comprehensive_enhanced_report(
                        content=arguments.get("content", ""),
                        title=arguments.get("title", "Strategic Analysis Report"),
                        subtitle=arguments.get("subtitle", "Comprehensive Enhanced Analysis"),
                        include_all_components=arguments.get("include_all_components", True)
                    )
                    
                    if result.get("success"):
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"Comprehensive enhanced report generated successfully. Report saved to: {result.get('report_path', 'N/A')}"
                                    }
                                ],
                                "report_path": result.get("report_path"),
                                "components_count": len(result.get("components", {})),
                                "processing_time": result.get("processing_time")
                            }
                        }
                    else:
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {"code": -32603, "message": f"Failed to generate report: {result.get('error', 'Unknown error')}"}
                        }
                except Exception as e:
                    logger.error(f"Error generating comprehensive enhanced report: {e}")
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32603, "message": f"Internal error generating report: {str(e)}"}
                    }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}
                }
        else:
            # Unknown method
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            }
    except Exception as e:
        logger.error(f"Error in MCP endpoint: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }

# MCP stream endpoint with proper headers
@app.post("/mcp/stream")
async def mcp_stream_endpoint(request: dict):
    """MCP stream endpoint with proper headers for streamable HTTP protocol."""
    try:
        logger.info("Handling MCP stream request")
        # Delegate to regular MCP endpoint
        return await mcp_endpoint(request)
    except Exception as e:
        logger.error(f"Error in MCP stream endpoint: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }

# Add middleware to handle MCP headers
@app.middleware("http")
async def add_mcp_headers(request, call_next):
    """Add MCP headers to responses."""
    response = await call_next(request)
    response.headers["Accept"] = "application/json, text/event-stream"
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
