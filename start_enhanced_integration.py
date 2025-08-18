#!/usr/bin/env python3
"""
Enhanced Markdown Export Integration Script

This script starts the main server, waits for it to be ready, and runs comprehensive tests
to verify the enhanced markdown export integration.
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path
from loguru import logger

def wait_for_server(url: str, max_wait: int = 120) -> bool:
    """Wait for server to be ready."""
    logger.info(f"⏳ Waiting for server at {url} to be ready...")
    
    for i in range(max_wait):
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ Server is ready after {i+1} seconds")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        if (i + 1) % 10 == 0:
            logger.info(f"   Still waiting... ({i+1}/{max_wait} seconds)")
    
    logger.error(f"❌ Server did not become ready within {max_wait} seconds")
    return False

def start_server() -> subprocess.Popen:
    """Start the main server."""
    logger.info("🚀 Starting main server...")
    
    try:
        # Start the server using the virtual environment Python
        process = subprocess.Popen([
            ".venv/Scripts/python.exe", "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        logger.info(f"✅ Server started with PID: {process.pid}")
        return process
        
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        return None

def run_tests() -> bool:
    """Run the integration tests."""
    logger.info("🧪 Running integration tests...")
    
    try:
        # Run the test script
        result = subprocess.run([
            ".venv/Scripts/python.exe", "Test/test_enhanced_markdown_export_integration.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ All tests passed!")
            return True
        else:
            logger.error(f"❌ Tests failed with return code: {result.returncode}")
            logger.error(f"STDOUT: {result.stdout}")
            logger.error(f"STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to run tests: {e}")
        return False

def test_mcp_client_connection() -> bool:
    """Test MCP client connection using the sample code."""
    logger.info("🔧 Testing MCP client connection...")
    
    try:
        # Test basic MCP endpoint
        response = requests.get("http://localhost:8000/mcp-health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ MCP server is healthy: {data}")
            return True
        else:
            logger.error(f"❌ MCP server health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ MCP client connection test failed: {e}")
        return False

def main():
    """Main integration function."""
    logger.info("🎯 Enhanced Markdown Export Integration Test")
    logger.info("=" * 60)
    
    # Start server
    server_process = start_server()
    if not server_process:
        logger.error("❌ Failed to start server")
        sys.exit(1)
    
    try:
        # Wait for server to be ready
        if not wait_for_server("http://localhost:8003"):
            logger.error("❌ Server did not become ready")
            sys.exit(1)
        
        # Wait additional time for MCP server
        logger.info("⏳ Waiting 60 seconds for MCP server to fully initialize...")
        time.sleep(60)
        
        # Test MCP client connection
        if not test_mcp_client_connection():
            logger.warning("⚠️ MCP client connection test failed")
        
        # Run integration tests
        if not run_tests():
            logger.error("❌ Integration tests failed")
            sys.exit(1)
        
        logger.info("🎉 Integration test completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("⚠️ Interrupted by user")
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        sys.exit(1)
    finally:
        # Clean up
        if server_process:
            logger.info("🛑 Stopping server...")
            server_process.terminate()
            try:
                server_process.wait(timeout=10)
                logger.info("✅ Server stopped gracefully")
            except subprocess.TimeoutExpired:
                logger.warning("⚠️ Server did not stop gracefully, forcing...")
                server_process.kill()

if __name__ == "__main__":
    main()
