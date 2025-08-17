#!/usr/bin/env python3
"""
Test script to check Dynamic Tool Management API.
"""

import requests

def test_dynamic_tool_management():
    """Test the Dynamic Tool Management API."""
    print("=== TESTING DYNAMIC TOOL MANAGEMENT API ===")
    
    try:
        # Test the API endpoint
        response = requests.get(
            'http://localhost:8003/api/v1/mcp/tools/status', 
            timeout=5
        )
        print(f"✅ API Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        if response.status_code == 200:
            print("✅ Dynamic Tool Management API is working!")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Dynamic Tool Management API: {e}")
        return False

if __name__ == "__main__":
    success = test_dynamic_tool_management()
    if success:
        print("\n🎉 Dynamic Tool Management API Test PASSED!")
    else:
        print("\n❌ Dynamic Tool Management API Test FAILED!")
