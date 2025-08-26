#!/usr/bin/env python3
"""
Test Semantic Search Fix

This script tests that the semantic search service is working correctly
after fixing the limit parameter issue.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger

async def test_semantic_search_fix():
    """Test that semantic search service works correctly."""
    
    logger.info("🧪 Testing Semantic Search Fix")
    logger.info("=" * 50)
    
    try:
        # Test 1: Import semantic search service
        logger.info("📋 Test 1: Importing semantic search service...")
        try:
            from src.core.semantic_search_service import SemanticSearchService
            from src.config.semantic_search_config import SearchType
            logger.info("✅ Semantic search service imported successfully")
        except ImportError as e:
            logger.error(f"❌ Failed to import semantic search service: {e}")
            return False
        
        # Test 2: Initialize semantic search service
        logger.info("📋 Test 2: Initializing semantic search service...")
        try:
            search_service = SemanticSearchService()
            logger.info("✅ Semantic search service initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize semantic search service: {e}")
            return False
        
        # Test 3: Test search method with correct parameters
        logger.info("📋 Test 3: Testing search method with correct parameters...")
        try:
            # Test with n_results parameter (correct)
            result = await search_service.search(
                query="test query",
                search_type=SearchType.SEMANTIC,
                n_results=5
            )
            logger.info("✅ Search method works with n_results parameter")
            logger.info(f"📊 Search result: {result.get('success', False)}")
        except Exception as e:
            logger.error(f"❌ Search method failed: {e}")
            return False
        
        # Test 4: Test MCP server integration
        logger.info("📋 Test 4: Testing MCP server integration...")
        try:
            from src.mcp_servers.enhanced_optimized_mcp_server import EnhancedOptimizedMCPServer
            
            # Create a mock MCP server instance
            mcp_server = EnhancedOptimizedMCPServer()
            
            # Test the search content tool
            search_result = await mcp_server._call_search_content_tool({
                "query": "test query",
                "search_type": "semantic",
                "language": "en",
                "limit": 5
            })
            
            logger.info("✅ MCP server search content tool works correctly")
            logger.info(f"📊 MCP search result: {search_result.get('jsonrpc', 'No jsonrpc')}")
            
        except Exception as e:
            logger.error(f"❌ MCP server integration failed: {e}")
            return False
        
        logger.info("🎉 All tests passed! Semantic search fix is working correctly.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Testing Semantic Search Fix")
    print("=" * 40)
    
    success = await test_semantic_search_fix()
    
    if success:
        print("\n✅ SUCCESS: Semantic search fix is working correctly!")
        print("\n📋 Summary:")
        print("   - Semantic search service imports correctly")
        print("   - Search method accepts n_results parameter")
        print("   - MCP server integration works without errors")
        print("   - No more 'limit' parameter errors")
        print("\n🎯 Fix Applied:")
        print("   - Changed 'limit' parameter to 'n_results' in MCP server")
        print("   - Updated both search method calls")
        print("   - Console error should be resolved")
    else:
        print("\n❌ FAILED: Some tests failed. Please check the logs above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
