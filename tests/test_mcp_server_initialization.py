#!/usr/bin/env python3
"""
Test MCP Server Initialization

This script tests if the MCP server can be properly initialized and if the HTTP app can be created.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger

def test_mcp_imports():
    """Test if MCP dependencies can be imported."""
    logger.info("🔍 Testing MCP imports...")
    
    try:
        # Test FastMCP import
        from fastmcp import FastMCP
        logger.info("✅ FastMCP imported successfully")
        
        # Test UnifiedMCPServer import
        from src.mcp_servers.unified_mcp_server import UnifiedMCPServer
        logger.info("✅ UnifiedMCPServer imported successfully")
        
        return True
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False

def test_mcp_server_creation():
    """Test if MCP server can be created."""
    logger.info("🔍 Testing MCP server creation...")
    
    try:
        from src.mcp_servers.unified_mcp_server import UnifiedMCPServer
        
        # Create MCP server
        mcp_server = UnifiedMCPServer()
        logger.info("✅ MCP server created successfully")
        
        # Check if MCP instance exists
        if hasattr(mcp_server, 'mcp') and mcp_server.mcp is not None:
            logger.info("✅ MCP instance exists")
            logger.info(f"   MCP name: {mcp_server.mcp.name}")
            logger.info(f"   MCP version: {mcp_server.mcp.version}")
        else:
            logger.error("❌ MCP instance is None")
            return False
        
        return True
    except Exception as e:
        logger.error(f"❌ Error creating MCP server: {e}")
        return False

def test_mcp_http_app_creation():
    """Test if MCP HTTP app can be created."""
    logger.info("🔍 Testing MCP HTTP app creation...")
    
    try:
        from src.mcp_servers.unified_mcp_server import UnifiedMCPServer
        
        # Create MCP server
        mcp_server = UnifiedMCPServer()
        
        # Create HTTP app
        http_app = mcp_server.get_http_app(path="/mcp")
        
        if http_app is not None:
            logger.info("✅ MCP HTTP app created successfully")
            logger.info(f"   HTTP app type: {type(http_app)}")
            return True
        else:
            logger.error("❌ MCP HTTP app is None")
            return False
    except Exception as e:
        logger.error(f"❌ Error creating MCP HTTP app: {e}")
        return False

def test_mcp_tools_registration():
    """Test if MCP tools are registered."""
    logger.info("🔍 Testing MCP tools registration...")
    
    try:
        from src.mcp_servers.unified_mcp_server import UnifiedMCPServer
        
        # Create MCP server
        mcp_server = UnifiedMCPServer()
        
        # Check if tools are registered
        if hasattr(mcp_server, 'mcp') and mcp_server.mcp is not None:
            # Try to get tools list
            try:
                tools = mcp_server.mcp.tools
                logger.info(f"✅ MCP tools available: {len(tools)} tools")
                
                # Check for strategic deception tools
                deception_tools = [tool for tool in tools if 'deception' in tool.get('description', '').lower()]
                logger.info(f"   Strategic deception tools: {len(deception_tools)}")
                
                for tool in deception_tools:
                    logger.info(f"     - {tool.get('name')}: {tool.get('description')}")
                
                return len(tools) > 0
            except Exception as e:
                logger.error(f"❌ Error accessing MCP tools: {e}")
                return False
        else:
            logger.error("❌ MCP instance not available")
            return False
    except Exception as e:
        logger.error(f"❌ Error testing MCP tools: {e}")
        return False

def main():
    """Run all MCP initialization tests."""
    logger.info("🚀 Testing MCP Server Initialization")
    logger.info("=" * 50)
    
    test_results = []
    
    # Run tests
    tests = [
        ("MCP Imports", test_mcp_imports),
        ("MCP Server Creation", test_mcp_server_creation),
        ("MCP HTTP App Creation", test_mcp_http_app_creation),
        ("MCP Tools Registration", test_mcp_tools_registration)
    ]
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running {test_name}...")
        try:
            result = test_func()
            test_results.append(result)
        except Exception as e:
            logger.error(f"❌ {test_name} failed with exception: {e}")
            test_results.append(False)
    
    # Calculate results
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    
    logger.info("\n" + "=" * 50)
    logger.info("📊 MCP Initialization Test Results")
    logger.info("=" * 50)
    logger.info(f"✅ Passed: {passed_tests}/{total_tests}")
    logger.info(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    logger.info(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        logger.info("\n🎉 All MCP initialization tests passed!")
        logger.info("✅ MCP server can be properly initialized")
        return True
    else:
        logger.error("\n❌ Some MCP initialization tests failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
