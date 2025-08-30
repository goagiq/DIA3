#!/usr/bin/env python3
"""
Simple test to verify MCP server integration works correctly.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger

def test_mcp_integration():
    """Test the exact MCP integration code from main.py."""
    try:
        logger.info("🔧 Testing MCP server creation...")
        from src.mcp_servers.unified_mcp_server import UnifiedMCPServer
        
        mcp_server = UnifiedMCPServer()
        logger.info(f"✅ MCP server created: {mcp_server is not None}")
        
        if mcp_server:
            try:
                logger.info("🔧 Testing MCP app creation...")
                mcp_app = mcp_server.get_http_app()
                logger.info(f"✅ MCP app created: {mcp_app is not None}")
                
                if mcp_app:
                    logger.info("🔧 Testing FastAPI app import...")
                    from src.api.main import app
                    logger.info(f"✅ FastAPI app imported: {app is not None}")
                    
                    logger.info("🔧 Testing MCP app mounting...")
                    app.mount("/mcp", mcp_app)
                    logger.info("✅ MCP app mounted successfully")
                    
                    logger.info("🔧 Testing health endpoint creation...")
                    @app.get("/mcp-health")
                    async def mcp_health_check():
                        return {
                            "status": "healthy", 
                            "service": "mcp_server", 
                            "endpoints": ["/mcp"],
                            "protocol": "MCP (Model Context Protocol)",
                            "note": "Use 'initialize' method to establish session"
                        }
                    
                    logger.info("✅ Health endpoint created successfully")
                    logger.info("✅ All MCP integration tests passed!")
                    return True
                    
            except Exception as e:
                logger.error(f"❌ MCP integration failed: {e}")
                logger.error(f"   Error type: {type(e).__name__}")
                logger.error(f"   Error details: {str(e)}")
                return False
        else:
            logger.error("❌ MCP server creation failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting MCP Integration Test")
    logger.info("=" * 50)
    
    success = test_mcp_integration()
    
    if success:
        logger.info("✅ MCP integration test completed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ MCP integration test failed!")
        sys.exit(1)
