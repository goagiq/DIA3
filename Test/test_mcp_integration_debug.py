#!/usr/bin/env python3
"""
Debug script to test MCP server integration step by step.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger

def test_mcp_server_creation():
    """Test MCP server creation."""
    try:
        logger.info("🔧 Testing MCP server creation...")
        from src.mcp_servers.unified_mcp_server import UnifiedMCPServer
        
        server = UnifiedMCPServer()
        logger.info(f"✅ MCP server created: {server is not None}")
        logger.info(f"✅ MCP server has mcp attribute: {hasattr(server, 'mcp')}")
        logger.info(f"✅ MCP server mcp is not None: {server.mcp is not None}")
        
        return server
    except Exception as e:
        logger.error(f"❌ MCP server creation failed: {e}")
        return None

def test_http_app_creation(server):
    """Test HTTP app creation."""
    try:
        logger.info("🔧 Testing HTTP app creation...")
        
        http_app = server.get_http_app(path="")
        logger.info(f"✅ HTTP app created: {http_app is not None}")
        
        if http_app:
            logger.info(f"✅ HTTP app type: {type(http_app)}")
            logger.info(f"✅ HTTP app has routes: {hasattr(http_app, 'routes')}")
        
        return http_app
    except Exception as e:
        logger.error(f"❌ HTTP app creation failed: {e}")
        return None

def test_fastapi_mounting(http_app):
    """Test FastAPI mounting."""
    try:
        logger.info("🔧 Testing FastAPI mounting...")
        
        from fastapi import FastAPI
        
        app = FastAPI()
        app.mount("/mcp", http_app)
        
        logger.info("✅ FastAPI mounting successful")
        logger.info(f"✅ App routes: {len(app.routes)}")
        
        return app
    except Exception as e:
        logger.error(f"❌ FastAPI mounting failed: {e}")
        return None

def main():
    """Main test function."""
    logger.info("🚀 Starting MCP Integration Debug Tests")
    logger.info("=" * 60)
    
    # Test 1: MCP server creation
    server = test_mcp_server_creation()
    if not server:
        logger.error("❌ MCP server creation failed - stopping tests")
        return
    
    # Test 2: HTTP app creation
    http_app = test_http_app_creation(server)
    if not http_app:
        logger.error("❌ HTTP app creation failed - stopping tests")
        return
    
    # Test 3: FastAPI mounting
    app = test_fastapi_mounting(http_app)
    if not app:
        logger.error("❌ FastAPI mounting failed - stopping tests")
        return
    
    logger.info("=" * 60)
    logger.info("✅ All MCP integration tests passed!")
    logger.info("The issue must be in the main.py integration code")

if __name__ == "__main__":
    main()
