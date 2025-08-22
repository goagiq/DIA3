#!/usr/bin/env python3
"""
Start MCP Server Only
This script starts only the standalone MCP server and keeps it running.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Start the standalone MCP server."""
    try:
        from src.mcp_servers.standalone_mcp_server import start_standalone_mcp_server
        
        print("🚀 Starting Standalone MCP Server...")
        print("📋 Server will be available at: http://localhost:8000")
        print("📋 MCP endpoint at: http://localhost:8000/mcp")
        print("📋 MCP stream endpoint at: http://localhost:8000/mcp/stream")
        print("📋 Health check at: http://localhost:8000/mcp-health")
        print("=" * 60)
        
        # Start the MCP server
        server = start_standalone_mcp_server(host="localhost", port=8000)
        
        if server and server.is_server_running():
            print("✅ MCP Server started successfully!")
            print("🔧 Available for Strands integration with Streamable HTTP transport")
            print("📄 Enhanced report generation available via MCP tools")
            print("\n🔄 Server is running. Press Ctrl+C to stop.")
            
            # Keep the server running
            try:
                while server.is_server_running():
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down MCP server...")
                server.stop()
                print("✅ Server stopped")
        else:
            print("❌ Failed to start MCP server")
            return 1
            
    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

