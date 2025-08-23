#!/usr/bin/env python3
"""
Combined Server Startup Script

This script starts the combined FastAPI + MCP server on port 8000 with both
API endpoints and MCP tools available.
"""

import uvicorn
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

if __name__ == "__main__":
    try:
        # Import the minimal MCP server directly (following the working main.py pattern)
        from src.api.minimal_mcp_server import app
        
        print("🚀 Starting DIA3 Combined Server (API + MCP)...")
        print("📋 Server will be available at: http://localhost:8000")
        print("📋 API endpoints at: http://localhost:8000/api/v1/*")
        print("📋 MCP endpoint at: http://localhost:8000/mcp")
        print("📋 MCP stream endpoint at: http://localhost:8000/mcp/stream")
        print("📋 Health check at: http://localhost:8000/health")
        print("📋 Enhanced reports at: http://localhost:8000/api/v1/enhanced-reports/generate")
        print("=" * 70)
        print("🔧 Configuration:")
        print("   - HTML reports enabled by default")
        print("   - MCP tools integrated")
        print("   - Interactive tooltips and visualizations")
        print("   - Source tracking enabled")
        print("=" * 70)
        
        # Start the combined server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Combined Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start combined server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
