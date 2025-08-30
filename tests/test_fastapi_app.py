#!/usr/bin/env python3
"""
Simple test script to verify FastAPI app is working correctly.
"""

import requests
import time

def test_fastapi_app():
    """Test the FastAPI app endpoints."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing FastAPI App")
    print("=" * 50)
    
    # Test root endpoint
    print("1. Testing root endpoint (/)...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test health endpoint
    print("\n2. Testing health endpoint (/health)...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test MCP endpoint
    print("\n3. Testing MCP endpoint (/mcp)...")
    try:
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        response = requests.post(
            f"{base_url}/mcp",
            json=mcp_request,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_fastapi_app()
