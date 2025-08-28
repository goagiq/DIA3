#!/usr/bin/env python3
"""
Test script with proper MCP request format.
"""

import requests
import json

def test_proper_mcp_request():
    """Test MCP endpoint with proper request format."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing MCP Endpoint with Proper Request Format")
    print("=" * 60)
    
    # Test MCP initialize with proper format
    print("1. Testing MCP initialize with proper format...")
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        # Proper MCP initialize request
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = requests.post(
            f"{base_url}/mcp",
            json=initialize_request,
            headers=headers,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test MCP tools/list with proper format
    print("\n2. Testing MCP tools/list with proper format...")
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        # Proper MCP tools/list request
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        response = requests.post(
            f"{base_url}/mcp",
            json=list_tools_request,
            headers=headers,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test MCP ping with proper format
    print("\n3. Testing MCP ping with proper format...")
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        # Proper MCP ping request
        ping_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "ping"
        }
        
        response = requests.post(
            f"{base_url}/mcp",
            json=ping_request,
            headers=headers,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_proper_mcp_request()
