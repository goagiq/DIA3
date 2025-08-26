#!/usr/bin/env python3
"""
Simplified MCP Server Startup Script
Focuses only on the essential MCP server functionality without complex initialization.
"""

# Set environment variables to suppress deprecation warnings
import os
os.environ['PYTHONWARNINGS'] = 'ignore::DeprecationWarning:websockets.*,ignore::DeprecationWarning:uvicorn.*'

# Suppress deprecation warnings BEFORE any other imports
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="websockets")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="uvicorn.protocols.websockets")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="uvicorn")

import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# Import the minimal MCP server
try:
    from src.api.minimal_mcp_server import app
    logger.info("✅ Minimal MCP server imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import minimal MCP server: {e}")
    exit(1)

def main():
    """Start the simplified MCP server."""
    print("🚀 Starting Simplified MCP Server")
    print("=" * 50)
    print("📊 Focus: MCP Server with Enhanced Report Generation")
    print("🌐 Port: 8000")
    print("🔧 Features: generate_report, process_content, analyze_content, search_content")
    print("=" * 50)
    
    try:
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        exit(1)

if __name__ == "__main__":
    main()
