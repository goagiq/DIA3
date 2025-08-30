#!/usr/bin/env python3
"""
Test to verify MCP client fixes work.
"""

import asyncio
import time
from loguru import logger

def test_mcp_client_fixes():
    """Test if MCP client fixes work."""
    try:
        from src.core.strands_mcp_client import StrandsMCPClient
        
        # Create MCP client
        client = StrandsMCPClient()
        logger.info("✅ MCP client created successfully")
        
        # Test tool retrieval with timeout
        logger.info("Testing tool retrieval...")
        start_time = time.time()
        tools = client.get_tools_sync()
        elapsed = time.time() - start_time
        logger.info(f"✅ Tool retrieval completed in {elapsed:.2f}s: {len(tools)} tools")
        
        # Test agent creation
        logger.info("Testing agent creation...")
        start_time = time.time()
        agent = client.create_agent_with_mcp_tools("test_agent", "Test agent")
        elapsed = time.time() - start_time
        logger.info(f"✅ Agent creation completed in {elapsed:.2f}s: {agent.name}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ MCP client test failed: {e}")
        return False

async def test_async_operations():
    """Test async operations."""
    try:
        from src.core.strands_mcp_client import StrandsMCPClient
        
        # Create MCP client
        client = StrandsMCPClient()
        
        # Test async tool retrieval with timeout
        logger.info("Testing async tool retrieval...")
        start_time = time.time()
        tools = await client.get_tools_async()
        elapsed = time.time() - start_time
        logger.info(f"✅ Async tool retrieval completed in {elapsed:.2f}s: {len(tools)} tools")
        
        # Test async agent execution with timeout
        logger.info("Testing async agent execution...")
        start_time = time.time()
        result = await client.run_agent_async("test_agent", "Hello")
        elapsed = time.time() - start_time
        logger.info(f"✅ Async agent execution completed in {elapsed:.2f}s: {result[:50]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Async operations test failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("🔧 MCP Client Fixes Test")
    logger.info("=" * 40)
    
    # Test 1: Basic MCP client functionality
    logger.info("1. Testing MCP client fixes...")
    start_time = time.time()
    if test_mcp_client_fixes():
        elapsed = time.time() - start_time
        logger.info(f"✅ MCP client fixes working (took {elapsed:.2f}s)")
    else:
        elapsed = time.time() - start_time
        logger.error(f"❌ MCP client fixes failed (took {elapsed:.2f}s)")
        return
    
    # Test 2: Async operations
    logger.info("2. Testing async operations...")
    start_time = time.time()
    success = asyncio.run(test_async_operations())
    elapsed = time.time() - start_time
    
    if success:
        logger.info(f"✅ Async operations working (took {elapsed:.2f}s)")
        logger.info("🎉 All MCP client fixes are working!")
    else:
        logger.error(f"❌ Async operations failed (took {elapsed:.2f}s)")
    
    logger.info("✅ All tests completed!")

if __name__ == "__main__":
    main()
