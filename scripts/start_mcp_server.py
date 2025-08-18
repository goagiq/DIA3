#!/usr/bin/env python3
"""
MCP Server Startup Script

This script starts the MCP server with proper endpoint (/mcp) and headers
for the streamable HTTP protocol.
"""

import uvicorn
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

if __name__ == "__main__":
    try:
        # Import the MCP server
        from src.mcp_servers.unified_mcp_server import create_unified_mcp_server
        
        print("🚀 Starting DIA3 MCP Server...")
        print("📋 Server will be available at: http://localhost:8000")
        print("📋 MCP endpoint at: http://localhost:8000/mcp")
        print("📋 MCP stream endpoint at: http://localhost:8000/mcp/stream")
        print("📋 Health check at: http://localhost:8000/health")
        print("=" * 60)
        
        # Create MCP server
        server = create_unified_mcp_server()
        app = server.get_http_app()
        
        if app is None:
            print("❌ Failed to create MCP server app")
            sys.exit(1)
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False
        )
        
    except KeyboardInterrupt:
        print("\n🛑 MCP Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")
        sys.exit(1)
