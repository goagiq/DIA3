#!/usr/bin/env python3
"""
Test to check the correct MCP endpoint.
"""

import requests

def test_mcp_endpoints():
    """Test various MCP endpoints."""
    print("=== TESTING MCP ENDPOINTS ===")
    
    endpoints = [
        "http://localhost:8003/mcp/tools/status",
        "http://localhost:8003/api/v1/mcp/tools/status",
        "http://localhost:8003/mcp-health",
        "http://localhost:8003/health"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=5)
            print(f"✅ {endpoint}: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.text[:100]}")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")

if __name__ == "__main__":
    test_mcp_endpoints()
