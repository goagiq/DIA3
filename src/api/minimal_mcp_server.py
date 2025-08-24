"""
Minimal MCP Server for port 8000 with proper MCP protocol support.
Now includes the modular report system as the default template.
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

# Import modular report generator
try:
    from src.core.modular_report_generator import modular_report_generator
    MODULAR_REPORT_AVAILABLE = True
    logger.info("✅ Modular report generator available")
except ImportError as e:
    MODULAR_REPORT_AVAILABLE = False
    logger.warning(f"⚠️ Modular report generator not available: {e}")

# Import enhanced report routes
try:
    from src.api.enhanced_report_routes import router as enhanced_report_router
    ENHANCED_REPORT_ROUTES_AVAILABLE = True
    logger.info("✅ Enhanced report routes available")
except ImportError as e:
    ENHANCED_REPORT_ROUTES_AVAILABLE = False
    logger.warning(f"⚠️ Enhanced report routes not available: {e}")

# Import unified MCP server for full tool integration
try:
    from src.mcp_servers.unified_mcp_server import UnifiedMCPServer
    unified_mcp_server = UnifiedMCPServer()
    UNIFIED_MCP_AVAILABLE = True
    logger.info("✅ Unified MCP server available")
except ImportError as e:
    UNIFIED_MCP_AVAILABLE = False
    logger.warning(f"⚠️ Unified MCP server not available: {e}")
    unified_mcp_server = None

# Initialize FastAPI app with comprehensive functionality
app = FastAPI(
    title="DIA3 Combined API with MCP Integration",
    description="AI-powered sentiment analysis with MCP server integration and modular report system on port 8000",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include enhanced report routes if available
if ENHANCED_REPORT_ROUTES_AVAILABLE:
    app.include_router(enhanced_report_router, prefix="/api/v1/enhanced-reports")
    logger.info("✅ Enhanced report routes included")

# Global session storage for MCP
mcp_sessions = {}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "DIA3 Combined Server with Modular Report System",
        "version": "2.0.0",
        "status": "running",
        "port": 8000,
        "features": {
            "modular_report_system": MODULAR_REPORT_AVAILABLE,
            "enhanced_reports": ENHANCED_REPORT_ROUTES_AVAILABLE,
            "comprehensive_reports": COMPREHENSIVE_REPORT_AVAILABLE
        },
        "endpoints": {
            "health": "/health",
            "mcp": "/mcp (with proper headers)",
            "mcp_stream": "/mcp/stream (with streaming support)",
            "enhanced_reports": "/api/v1/enhanced-reports/*",
            "modular_reports": "/api/v1/enhanced-reports/generate-modular"
        },
        "mcp_protocol": {
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            },
            "stream_headers": {
                "Content-Type": "text/event-stream",
                "Accept": "application/json, text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check system health and status."""
    return {
        "status": "healthy",
        "message": "DIA3 Combined server running with modular report system",
        "version": "2.0.0",
        "features": {
            "modular_report_system": MODULAR_REPORT_AVAILABLE,
            "enhanced_reports": ENHANCED_REPORT_ROUTES_AVAILABLE,
            "comprehensive_reports": COMPREHENSIVE_REPORT_AVAILABLE,
            "mcp_server_available": True
        }
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
                "tools_available": True,
                "modular_reports_available": MODULAR_REPORT_AVAILABLE
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
                        "name": "DIA3 Combined MCP Server",
                        "version": "2.0.0"
                    }
                }
            }
        elif method == "tools/list":
            # Handle tools/list request
            logger.info("Handling MCP tools/list request")
            
            # Use unified MCP server tools if available, otherwise fall back to basic tools
            if UNIFIED_MCP_AVAILABLE and unified_mcp_server:
                try:
                    tools_info = unified_mcp_server.get_tools_info()
                    tools = []
                    
                    # Convert unified MCP tools to MCP protocol format
                    for tool_info in tools_info:
                        tool = {
                            "name": tool_info["name"],
                            "description": tool_info["description"],
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        }
                        tools.append(tool)
                    
                    logger.info(f"✅ Using unified MCP server tools: {len(tools)} tools")
                except Exception as e:
                    logger.error(f"Error getting unified MCP tools: {e}")
                    tools = []
            else:
                # Fallback to basic tools
                tools = [
                    {
                        "name": "generate_enhanced_report",
                        "description": "Generate enhanced report with source tracking and tooltips",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "string", "description": "Content to analyze"},
                                "report_type": {"type": "string", "description": "Report type (modular, comprehensive, basic)", "default": "modular"},
                                "include_tooltips": {"type": "boolean", "description": "Include interactive tooltips", "default": True},
                                "format": {"type": "string", "description": "Output format (html, markdown)", "default": "html"}
                            },
                            "required": ["content"]
                        }
                    }
                ]
                
                # Add modular report tools if available
                if MODULAR_REPORT_AVAILABLE:
                    tools.extend([
                        {
                            "name": "generate_modular_report",
                            "description": "Generate modular enhanced report with configurable components",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "topic": {"type": "string", "description": "Analysis topic"},
                                    "data": {"type": "object", "description": "Analysis data for modules"},
                                    "enabled_modules": {"type": "array", "items": {"type": "string"}, "description": "List of module IDs to enable"},
                                    "report_title": {"type": "string", "description": "Custom report title"}
                                },
                                "required": ["topic", "data"]
                            }
                        },
                        {
                            "name": "get_modular_modules",
                            "description": "Get list of available modules and their configurations",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        }
                    ])
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": tools
                }
            }
        elif method == "tools/call":
            # Handle tools/call request
            logger.info("Handling MCP tools/call request")
            
            arguments = params.get("arguments", {})
            tool_name = params.get("name", "")
            
            # Try to delegate to unified MCP server first if available
            if UNIFIED_MCP_AVAILABLE and unified_mcp_server:
                try:
                    # Check if the tool exists in unified MCP server
                    tools_info = unified_mcp_server.get_tools_info()
                    tool_names = [tool["name"] for tool in tools_info]
                    
                    if tool_name in tool_names:
                        logger.info(f"Delegating tool call '{tool_name}' to unified MCP server")
                        # For now, return a success message indicating the tool is available
                        # In a full implementation, we would call the actual tool method
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"Tool '{tool_name}' is available in unified MCP server. Full implementation pending."
                                    }
                                ]
                            }
                        }
                except Exception as e:
                    logger.error(f"Error delegating to unified MCP server: {e}")
                    # Continue with local tool handling
            
            if tool_name == "generate_enhanced_report":
                # Generate enhanced report (modular by default)
                try:
                    content = arguments.get("content", "")
                    report_type = arguments.get("report_type", "modular")
                    include_tooltips = arguments.get("include_tooltips", True)
                    format_type = arguments.get("format", "html")
                    
                    if report_type == "modular" and MODULAR_REPORT_AVAILABLE:
                        # Use modular report system
                        result = await modular_report_generator.generate_modular_report(
                            topic=content,
                            data={},
                            report_title=f"{content} - Analysis Report"
                        )
                        
                        if result.get("success"):
                            return {
                                "jsonrpc": "2.0",
                                "id": request_id,
                                "result": {
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": f"Modular enhanced report generated successfully!\n\n📄 File: {result.get('filename')}\n📁 Path: {result.get('file_path')}\n📊 Size: {result.get('file_size')} bytes\n🔧 Modules Used: {', '.join(result.get('modules_used', []))}"
                                        }
                                    ]
                                }
                            }
                        else:
                            return {
                                "jsonrpc": "2.0",
                                "id": request_id,
                                "error": {"code": -32603, "message": f"Failed to generate modular report: {result.get('error', 'Unknown error')}"}
                            }
                    else:
                        # Fall back to comprehensive report
                        if COMPREHENSIVE_REPORT_AVAILABLE:
                            result = await comprehensive_enhanced_report_generator.generate_comprehensive_enhanced_report(
                                content=content,
                                title=f"{content} - Analysis Report",
                                subtitle="Enhanced Analysis",
                                include_all_components=True
                            )
                            
                            if result.get("success"):
                                return {
                                    "jsonrpc": "2.0",
                                    "id": request_id,
                                    "result": {
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": f"Enhanced report generated successfully. Report saved to: {result.get('report_path', 'N/A')}"
                                            }
                                        ]
                                    }
                                }
                            else:
                                return {
                                    "jsonrpc": "2.0",
                                    "id": request_id,
                                    "error": {"code": -32603, "message": f"Failed to generate report: {result.get('error', 'Unknown error')}"}
                                }
                        else:
                            return {
                                "jsonrpc": "2.0",
                                "id": request_id,
                                "error": {"code": -32603, "message": "No report generator available"}
                            }
                            
                except Exception as e:
                    logger.error(f"Error generating enhanced report: {e}")
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32603, "message": f"Internal error generating report: {str(e)}"}
                    }
            
            elif tool_name == "generate_modular_report" and MODULAR_REPORT_AVAILABLE:
                # Generate modular report
                try:
                    topic = arguments.get("topic", "")
                    data = arguments.get("data", {})
                    enabled_modules = arguments.get("enabled_modules")
                    report_title = arguments.get("report_title")
                    
                    result = await modular_report_generator.generate_modular_report(
                        topic=topic,
                        data=data,
                        enabled_modules=enabled_modules,
                        report_title=report_title
                    )
                    
                    if result.get("success"):
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"Modular report generated successfully!\n\n📄 File: {result.get('filename')}\n📁 Path: {result.get('file_path')}\n📊 Size: {result.get('file_size')} bytes\n🔧 Modules Used: {', '.join(result.get('modules_used', []))}"
                                    }
                                ]
                            }
                        }
                    else:
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {"code": -32603, "message": f"Failed to generate modular report: {result.get('error', 'Unknown error')}"}
                        }
                        
                except Exception as e:
                    logger.error(f"Error generating modular report: {e}")
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32603, "message": f"Internal error generating modular report: {str(e)}"}
                    }
            
            elif tool_name == "get_modular_modules" and MODULAR_REPORT_AVAILABLE:
                # Get available modules
                try:
                    available_modules = modular_report_generator.get_available_modules()
                    enabled_modules = [m.module_id for m in modular_report_generator.get_enabled_modules()]
                    
                    module_details = []
                    for module_id in available_modules:
                        module = modular_report_generator.get_module(module_id)
                        if module:
                            metadata = module.get_module_metadata()
                            module_details.append({
                                "module_id": module_id,
                                "name": metadata.get("name", module_id),
                                "description": metadata.get("description", ""),
                                "enabled": module_id in enabled_modules
                            })
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Available modules: {len(module_details)}\n\n" + "\n".join([f"• {m['module_id']}: {m['description']} ({'Enabled' if m['enabled'] else 'Disabled'})" for m in module_details])
                                }
                            ]
                        }
                    }
                    
                except Exception as e:
                    logger.error(f"Error getting modular modules: {e}")
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32603, "message": f"Internal error getting modules: {str(e)}"}
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



# Add proper headers for MCP protocol
from fastapi import Response
from fastapi.responses import StreamingResponse
import json

@app.post("/mcp")
async def mcp_endpoint_with_headers(request: dict, response: Response):
    """MCP endpoint with proper headers for MCP protocol."""
    # Set proper headers for MCP protocol
    response.headers["Content-Type"] = "application/json"
    response.headers["Accept"] = "application/json, text/event-stream"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    
    try:
        logger.info("Handling MCP request with proper headers")
        return await mcp_endpoint(request)
    except Exception as e:
        logger.error(f"Error in MCP endpoint with headers: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }

@app.post("/mcp/stream")
async def mcp_stream_endpoint_with_headers(request: dict, response: Response):
    """MCP stream endpoint with proper headers for streamable HTTP protocol."""
    # Set proper headers for MCP stream protocol
    response.headers["Content-Type"] = "text/event-stream"
    response.headers["Accept"] = "application/json, text/event-stream"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Cache-Control"
    
    try:
        logger.info("Handling MCP stream request with proper headers")
        
        # Handle streaming response
        async def generate_stream():
            try:
                result = await mcp_endpoint(request)
                yield f"data: {json.dumps(result)}\n\n"
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
                }
                yield f"data: {json.dumps(error_response)}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Content-Type": "text/event-stream",
                "Accept": "application/json, text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Cache-Control"
            }
        )
    except Exception as e:
        logger.error(f"Error in MCP stream endpoint with headers: {e}")
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
