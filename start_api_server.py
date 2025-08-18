#!/usr/bin/env python3
"""
Simple API Server Startup Script

This script starts the FastAPI server for testing purposes.
"""

import uvicorn
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    try:
        # Import the FastAPI app
        from src.api.main import app
        
        print("🚀 Starting DIA3 API Server...")
        print("📋 Server will be available at: http://localhost:8000")
        print("📋 API documentation at: http://localhost:8000/docs")
        print("📋 Health check at: http://localhost:8000/health")
        print("=" * 60)
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            debug=True,
            reload=False
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)
