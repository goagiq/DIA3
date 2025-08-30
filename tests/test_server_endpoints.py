#!/usr/bin/env python3
"""
Test script to check server endpoints.
"""

import requests
import json

def test_server_endpoints():
    """Test various server endpoints."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Server Endpoints")
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
        response = requests.get(f"{base_url}/mcp", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test MCP POST endpoint
    print("\n4. Testing MCP POST endpoint (/mcp)...")
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
    
    # Test docs endpoint
    print("\n5. Testing docs endpoint (/docs)...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Docs endpoint available")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test openapi endpoint
    print("\n6. Testing OpenAPI endpoint (/openapi.json)...")
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ OpenAPI endpoint available")
            try:
                openapi_data = response.json()
                paths = openapi_data.get("paths", {})
                print(f"   Available paths: {list(paths.keys())}")
            except:
                print("   Could not parse OpenAPI data")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_server_endpoints()
