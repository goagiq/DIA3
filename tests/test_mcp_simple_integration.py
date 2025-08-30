#!/usr/bin/env python3
"""
Simple MCP Integration Test

This script tests basic MCP integration to identify issues with the MCP server.
"""

import requests
import json
from loguru import logger

# Test configuration
API_BASE_URL = "http://localhost:8003"
MCP_BASE_URL = f"{API_BASE_URL}/mcp"

def test_mcp_endpoint_access():
    """Test basic access to MCP endpoints."""
    logger.info("🔍 Testing MCP endpoint access...")
    
    # Test different MCP endpoint variations
    endpoints = [
        "/mcp",
        "/mcp/",
        "/mcp/initialize",
        "/mcp/tools/list"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{API_BASE_URL}{endpoint}"
            logger.info(f"Testing endpoint: {url}")
            
            # Try GET request first
            response = requests.get(url, timeout=5)
            logger.info(f"  GET {endpoint}: {response.status_code}")
            
            # Try POST request with empty JSON
            response = requests.post(url, json={}, timeout=5)
            logger.info(f"  POST {endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                logger.info(f"  Response: {response.text[:200]}...")
            
        except Exception as e:
            logger.error(f"  Error accessing {endpoint}: {e}")

def test_mcp_health():
    """Test MCP health endpoint."""
    logger.info("🔍 Testing MCP health endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/mcp-health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ MCP health check successful")
            logger.info(f"   Status: {data.get('status')}")
            logger.info(f"   Service: {data.get('service')}")
            logger.info(f"   Endpoints: {data.get('endpoints')}")
            return True
        else:
            logger.error(f"❌ MCP health check failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ MCP health check failed: {e}")
        return False

def test_mcp_initialize_simple():
    """Test simple MCP initialize request."""
    logger.info("🔍 Testing simple MCP initialize...")
    
    try:
        # Simple initialize request
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test_client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Try different endpoints
        endpoints = ["/mcp", "/mcp/"]
        
        for endpoint in endpoints:
            url = f"{API_BASE_URL}{endpoint}"
            logger.info(f"Testing initialize at: {url}")
            
            response = requests.post(url, json=initialize_request, timeout=10)
            logger.info(f"  Status: {response.status_code}")
            logger.info(f"  Response: {response.text[:500]}...")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.info(f"  JSON Response: {json.dumps(data, indent=2)}")
                except:
                    logger.info(f"  Non-JSON Response: {response.text}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ MCP initialize test failed: {e}")
        return False

def test_fastapi_mounting():
    """Test if FastAPI is properly mounting the MCP server."""
    logger.info("🔍 Testing FastAPI MCP mounting...")
    
    try:
        # Check if the main FastAPI app is accessible
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Main FastAPI app is accessible")
        else:
            logger.error(f"❌ Main FastAPI app not accessible: {response.status_code}")
            return False
        
        # Check if MCP endpoints are mounted
        response = requests.get(f"{API_BASE_URL}/mcp", timeout=5)
        logger.info(f"MCP endpoint response: {response.status_code}")
        logger.info(f"MCP endpoint content: {response.text[:200]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ FastAPI mounting test failed: {e}")
        return False

def main():
    """Run all MCP integration tests."""
    logger.info("🚀 Testing MCP Integration")
    logger.info("=" * 50)
    
    # Run tests
    test_fastapi_mounting()
    test_mcp_health()
    test_mcp_endpoint_access()
    test_mcp_initialize_simple()
    
    logger.info("\n" + "=" * 50)
    logger.info("📊 MCP Integration Test Complete")
    logger.info("=" * 50)

if __name__ == "__main__":
    main()
