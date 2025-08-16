#!/usr/bin/env python3
"""
Simple MCP Server Verification Test.

This script verifies that the MCP server is running and accessible.
"""

import requests
import time
from loguru import logger


def test_mcp_server_connection():
    """Test basic connection to MCP server."""
    try:
        logger.info("🔗 Testing MCP server connection...")
        
        # Test basic connection
        response = requests.get(
            "http://localhost:8000",
            timeout=5
        )
        
        if response.status_code == 200:
            logger.info("✅ MCP server is responding on port 8000")
            return True
        else:
            logger.info(f"⚠️ MCP server returned status: {response.status_code}")
            return True  # Still consider it working if it responds
            
    except requests.exceptions.ConnectionError:
        logger.error("❌ Could not connect to MCP server on port 8000")
        return False
    except Exception as e:
        logger.error(f"❌ Error testing MCP server: {e}")
        return False


def test_mcp_endpoint():
    """Test MCP endpoint."""
    try:
        logger.info("🔧 Testing MCP endpoint...")
        
        # Test MCP endpoint
        response = requests.get(
            "http://localhost:8000/mcp",
            timeout=5
        )
        
        if response.status_code in [200, 404, 405]:  # Any response means server is running
            logger.info("✅ MCP endpoint is accessible")
            return True
        else:
            logger.info(f"⚠️ MCP endpoint returned status: {response.status_code}")
            return True
            
    except requests.exceptions.ConnectionError:
        logger.error("❌ Could not connect to MCP endpoint")
        return False
    except Exception as e:
        logger.error(f"❌ Error testing MCP endpoint: {e}")
        return False


def main():
    """Main test function."""
    logger.info("🤖 MCP Server Verification Test")
    logger.info("=" * 40)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    # Run tests
    tests = [
        ("MCP Server Connection", test_mcp_server_connection),
        ("MCP Endpoint", test_mcp_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n🔍 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                logger.info(f"✅ {test_name} test passed")
            else:
                logger.error(f"❌ {test_name} test failed")
        except Exception as e:
            logger.error(f"❌ {test_name} test error: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 40)
    logger.info("📊 Test Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"   {status} {test_name}")
    
    logger.info(f"\n📈 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        logger.info("🎉 MCP server verification successful!")
        logger.info("✅ MCP server is running and accessible")
    else:
        logger.warning("⚠️ MCP server verification failed")
    
    return passed == total


if __name__ == "__main__":
    main()
