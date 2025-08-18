#!/usr/bin/env python3
"""
Dedicated API Server Startup Script
Starts the FastAPI application on port 8003
"""

import sys
import uvicorn
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from src.api.main import app
    
    print("🚀 Starting API Server on port 8003...")
    print("📡 API Endpoints:")
    print("   - Health: http://localhost:8003/health")
    print("   - PDF Status: http://localhost:8003/api/pdf/status")
    print("   - Word Status: http://localhost:8003/api/word/status")
    print("   - PDF Generate: http://localhost:8003/api/pdf/generate")
    print("   - Word Generate: http://localhost:8003/api/word/generate")
    
    # Start the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8003,
        reload=False
    )
    
except Exception as e:
    print(f"❌ Failed to start API server: {e}")
    sys.exit(1)
