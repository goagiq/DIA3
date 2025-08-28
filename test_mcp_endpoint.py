#!/usr/bin/env python3
"""
Test script to test the MCP endpoint with proper headers.
"""

import requests
import json

def test_mcp_endpoint():
    """Test the MCP endpoint with proper headers."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing MCP Endpoint with Proper Headers")
    print("=" * 50)
    
    # Test MCP endpoint with proper headers
    print("1. Testing MCP endpoint (/mcp) with proper headers...")
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        
        response = requests.post(
            f"{base_url}/mcp",
            json=mcp_request,
            headers=headers,
            timeout=5
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test MCP tools/list endpoint
    print("\n2. Testing MCP tools/list endpoint...")
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        response = requests.post(
            f"{base_url}/mcp",
            json=mcp_request,
            headers=headers,
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
    test_mcp_endpoint()
