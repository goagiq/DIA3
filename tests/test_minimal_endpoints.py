#!/usr/bin/env python3
"""
Minimal test script to check basic HTTP endpoints with proper headers.
"""

import requests

def test_minimal_endpoints():
    """Test minimal HTTP endpoints with proper headers."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Minimal HTTP Endpoints with Proper Headers")
    print("=" * 60)
    
    # Test root endpoint with MCP headers
    print("1. Testing root endpoint (/) with MCP headers...")
    try:
        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{base_url}/", headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test health endpoint with MCP headers
    print("\n2. Testing health endpoint (/health) with MCP headers...")
    try:
        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{base_url}/health", headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test docs endpoint
    print("\n3. Testing docs endpoint (/docs)...")
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
    print("\n4. Testing OpenAPI endpoint (/openapi.json)...")
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
    test_minimal_endpoints()
