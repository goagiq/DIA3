#!/usr/bin/env python3
"""
Strategic Intelligence Forecast System Startup Script
Starts the API server, MCP server, and runs integration tests
"""

import asyncio
import subprocess
import sys
import time
import signal
import os
from pathlib import Path

from loguru import logger

class StrategicIntelligenceSystem:
    """Strategic Intelligence Forecast System Manager"""
    
    def __init__(self):
        self.api_process = None
        self.mcp_process = None
        self.test_process = None
        
    async def start_api_server(self):
        """Start the FastAPI server"""
        logger.info("🚀 Starting FastAPI server on port 8003...")
        
        try:
            # Start API server
            self.api_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "src.api.main:app", 
                "--host", "0.0.0.0", 
                "--port", "8003",
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            logger.info("✅ FastAPI server started successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start FastAPI server: {e}")
            return False
    
    async def start_mcp_server(self):
        """Start the MCP server"""
        logger.info("🚀 Starting MCP server on port 8000...")
        
        try:
            # Start MCP server
            self.mcp_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "src.mcp_servers.unified_mcp_server:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            logger.info("✅ MCP server started successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start MCP server: {e}")
            return False
    
    async def wait_for_servers(self, timeout=120):
        """Wait for servers to be ready"""
        logger.info(f"⏳ Waiting up to {timeout} seconds for servers to be ready...")
        
        start_time = time.time()
        api_ready = False
        mcp_ready = False
        
        while time.time() - start_time < timeout:
            try:
                # Check API server
                if not api_ready:
                    import requests
                    response = requests.get("http://localhost:8003/health", timeout=5)
                    if response.status_code == 200:
                        logger.info("✅ API server is ready")
                        api_ready = True
                
                # Check MCP server
                if not mcp_ready:
                    response = requests.get("http://localhost:8000/mcp", timeout=5)
                    if response.status_code in [200, 405]:  # 405 is expected for GET on POST endpoint
                        logger.info("✅ MCP server is ready")
                        mcp_ready = True
                
                if api_ready and mcp_ready:
                    logger.info("🎯 All servers are ready!")
                    return True
                    
            except Exception as e:
                pass
            
            await asyncio.sleep(2)
        
        logger.error("❌ Timeout waiting for servers to be ready")
        return False
    
    async def run_integration_test(self):
        """Run the integration test"""
        logger.info("🧪 Running Strategic Intelligence Forecast Integration Test...")
        
        try:
            # Run the integration test
            self.test_process = subprocess.Popen([
                sys.executable, "Test/test_strategic_intelligence_integration.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for test to complete
            stdout, stderr = self.test_process.communicate()
            
            if self.test_process.returncode == 0:
                logger.info("✅ Integration test completed successfully")
                logger.info("📊 Test output:")
                print(stdout.decode())
                return True
            else:
                logger.error("❌ Integration test failed")
                logger.error("Error output:")
                print(stderr.decode())
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to run integration test: {e}")
            return False
    
    async def run_quick_test(self):
        """Run a quick test using the MCP tools directly"""
        logger.info("🧪 Running Quick Strategic Intelligence Forecast Test...")
        
        try:
            # Import and test the MCP tools directly
            from src.mcp_servers.strategic_intelligence_forecast_mcp_tools import StrategicIntelligenceForecastMCPTools
            
            # Initialize tools
            tools = StrategicIntelligenceForecastMCPTools()
            
            # Test quick forecast
            result = await tools.run_quick_strategic_forecast("Integration test forecast")
            
            if result.get("status") == "success":
                logger.info("✅ Quick test completed successfully")
                logger.info(f"📊 Forecast ID: {result.get('forecast_id')}")
                return True
            else:
                logger.error(f"❌ Quick test failed: {result.get('error')}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to run quick test: {e}")
            return False
    
    def cleanup(self):
        """Cleanup processes"""
        logger.info("🧹 Cleaning up processes...")
        
        if self.test_process:
            self.test_process.terminate()
            self.test_process.wait()
        
        if self.mcp_process:
            self.mcp_process.terminate()
            self.mcp_process.wait()
        
        if self.api_process:
            self.api_process.terminate()
            self.api_process.wait()
        
        logger.info("✅ Cleanup completed")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"🛑 Received signal {signum}, shutting down...")
        self.cleanup()
        sys.exit(0)

async def main():
    """Main function"""
    
    logger.info("🎯 Strategic Intelligence Forecast System Startup")
    logger.info("="*60)
    
    # Initialize system
    system = StrategicIntelligenceSystem()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, system.signal_handler)
    signal.signal(signal.SIGTERM, system.signal_handler)
    
    try:
        # Start servers
        api_started = await system.start_api_server()
        if not api_started:
            logger.error("❌ Failed to start API server")
            return
        
        mcp_started = await system.start_mcp_server()
        if not mcp_started:
            logger.error("❌ Failed to start MCP server")
            return
        
        # Wait for servers to be ready
        servers_ready = await system.wait_for_servers()
        if not servers_ready:
            logger.error("❌ Servers not ready within timeout")
            return
        
        # Run quick test first
        quick_test_passed = await system.run_quick_test()
        if quick_test_passed:
            logger.info("✅ Quick test passed, proceeding with full integration test")
        else:
            logger.warning("⚠️ Quick test failed, but continuing with integration test")
        
        # Run full integration test
        integration_test_passed = await system.run_integration_test()
        
        if integration_test_passed:
            logger.info("🎉 All tests passed! Strategic Intelligence Forecast System is ready.")
        else:
            logger.error("❌ Integration test failed")
        
        # Keep servers running for manual testing
        logger.info("🔄 Servers will continue running. Press Ctrl+C to stop.")
        
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 Keyboard interrupt received")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
    finally:
        system.cleanup()

if __name__ == '__main__':
    asyncio.run(main())
