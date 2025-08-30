#!/usr/bin/env python3
"""
Ultimate Clean MCP Server Startup Script - No Warnings
Uses multiple approaches to completely suppress all deprecation warnings.
"""

# Set environment variables BEFORE any imports
import os
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Monkey patch warnings module before any other imports
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Suppress specific module warnings
warnings.filterwarnings("ignore", module="websockets")
warnings.filterwarnings("ignore", module="uvicorn")
warnings.filterwarnings("ignore", module="uvicorn.protocols.websockets")

# Monkey patch the warnings module to completely disable it
def _showwarning(*args, **kwargs):
    pass

warnings.showwarning = _showwarning

# Now import the rest
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
    """Start the ultimate clean MCP server with no warnings."""
    print("🚀 Starting Ultimate Clean MCP Server (No Warnings)")
    print("=" * 60)
    print("📊 Focus: MCP Server with Enhanced Report Generation")
    print("🌐 Port: 8000")
    print("🔧 Features: generate_report, process_content, analyze_content, search_content")
    print("🧹 Console: Completely clean output with no warnings")
    print("🛡️ Multiple warning suppression methods applied")
    print("=" * 60)
    
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
