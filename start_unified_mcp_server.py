#!/usr/bin/env python3
"""
Script to start the unified MCP server on port 8002.
This server has the complete DIA3 enhanced export_data tool implementation.
"""

import sys
import os
import time
import threading

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mcp_servers.unified_mcp_server import create_unified_mcp_server


def run_unified_server():
    """Run the unified MCP server on port 8002."""
    try:
        server = create_unified_mcp_server()
        server.run(host="localhost", port=8002, debug=True)
    except Exception as e:
        print(f"Error running unified MCP server: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Start the unified MCP server on port 8002."""
    print("🚀 Starting Unified MCP Server on port 8002...")
    print("=" * 50)
    
    try:
        # Run server in a separate thread to avoid asyncio conflicts
        server_thread = threading.Thread(target=run_unified_server, daemon=True)
        server_thread.start()
        
        print("✅ Unified MCP Server started successfully!")
        print("📍 Server URL: http://localhost:8002/mcp/")
        print("🔧 Available tools include the complete DIA3 enhanced export_data tool")
        print("\n🔄 Server is running... Press Ctrl+C to stop")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        print("✅ Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
