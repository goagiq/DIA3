#!/usr/bin/env python3
"""
Combined Server Startup Script

This script starts the combined FastAPI + MCP server on port 8000 with both
API endpoints and MCP tools available. Now includes the modular report system
as the default template.
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
        
        print("🚀 Starting DIA3 Combined Server (API + MCP + Modular Reports)...")
        print("📋 Server will be available at: http://localhost:8000")
        print("📋 API endpoints at: http://localhost:8000/api/v1/*")
        print("📋 MCP endpoint at: http://localhost:8000/mcp")
        print("📋 MCP stream endpoint at: http://localhost:8000/mcp/stream")
        print("📋 Health check at: http://localhost:8000/health")
        print("📋 Enhanced reports at: http://localhost:8000/api/v1/enhanced-reports/generate")
        print("📋 Modular reports at: http://localhost:8000/api/v1/enhanced-reports/generate-modular")
        print("=" * 80)
        print("🔧 New Features:")
        print("   - Modular Report System (22 configurable modules)")
        print("   - Enhanced Report API with modular integration")
        print("   - MCP tools for modular report generation")
        print("   - Generic topic support for any analysis")
        print("   - Interactive tooltips and Chart.js visualizations")
        print("   - Professional HTML output with source tracking")
        print("=" * 80)
        print("🎯 Usage Examples:")
        print("   - Generate modular report: POST /api/v1/enhanced-reports/generate-modular")
        print("   - List modules: GET /api/v1/enhanced-reports/modules")
        print("   - MCP tool: generate_modular_report")
        print("   - Generic demo: python src/applications/generic_modular_report_demo.py")
        print("=" * 80)
        
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
