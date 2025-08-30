#!/usr/bin/env python3
"""
Clean MCP Server Startup Script - No Deprecation Warnings
Focuses only on the essential MCP server functionality without any console warnings.
"""

# Set environment variables to suppress ALL deprecation warnings
import os
os.environ['PYTHONWARNINGS'] = 'ignore'

# Suppress warnings at the Python level
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Suppress specific module warnings
warnings.filterwarnings("ignore", module="websockets")
warnings.filterwarnings("ignore", module="uvicorn")
warnings.filterwarnings("ignore", module="uvicorn.protocols.websockets")

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
    """Start the clean MCP server with no warnings."""
    print("🚀 Starting Clean MCP Server (No Warnings)")
    print("=" * 50)
    print("📊 Focus: MCP Server with Enhanced Report Generation")
    print("🌐 Port: 8000")
    print("🔧 Features: generate_report, process_content, analyze_content, search_content")
    print("🧹 Console: Clean output with no deprecation warnings")
    print("=" * 50)
    
    try:
        # Start the server with clean output
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
