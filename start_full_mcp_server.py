#!/usr/bin/env python3
"""
Script to start the full standalone MCP server on port 8001.
This server has the complete DIA3 enhanced export_data tool implementation.
"""

import sys
import os
import time

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mcp_servers.standalone_mcp_server import start_standalone_mcp_server


def main():
    """Start the full standalone MCP server on port 8001."""
    print("🚀 Starting Full Standalone MCP Server on port 8001...")
    print("=" * 50)
    
    try:
        # Start the server on port 8001
        server = start_standalone_mcp_server(host="localhost", port=8001)
        
        print("✅ Full Standalone MCP Server started successfully!")
        print("📍 Server URL: http://localhost:8001/mcp/")
        print("🔧 Available tools include the complete DIA3 enhanced "
              "export_data tool")
        print("\n🔄 Server is running... Press Ctrl+C to stop")
        
        # Keep the server running
        while server.is_server_running():
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        server.stop()
        print("✅ Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
