#!/usr/bin/env python3
"""
Simple server connectivity test
"""

import requests
import sys

def test_server_connectivity():
    """Test if the server is running and responding."""
    base_url = "http://localhost:8004"
    
    print("🔍 Testing server connectivity...")
    
    # Test basic health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responding")
            data = response.json()
            print(f"   Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Server responded with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Server may not be running.")
        return False
    except requests.exceptions.Timeout:
        print("❌ Server connection timed out.")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False

def test_threat_assessment_health():
    """Test threat assessment health endpoint."""
    base_url = "http://localhost:8004"
    
    print("\n🔍 Testing threat assessment health...")
    
    try:
        response = requests.get(f"{base_url}/threat-assessment/health", timeout=5)
        if response.status_code == 200:
            print("✅ Threat assessment endpoint is working")
            data = response.json()
            print(f"   Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Threat assessment endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing threat assessment endpoint: {e}")
        return False

if __name__ == "__main__":
    print("Simple Server Connectivity Test")
    print("=" * 40)
    
    # Test basic connectivity
    server_ok = test_server_connectivity()
    
    if server_ok:
        # Test threat assessment endpoint
        threat_ok = test_threat_assessment_health()
        
        print("\n" + "=" * 40)
        print("🎯 Results:")
        print(f"   - Server Connectivity: {'✅ PASSED' if server_ok else '❌ FAILED'}")
        print(f"   - Threat Assessment: {'✅ PASSED' if threat_ok else '❌ FAILED'}")
        
        if server_ok and threat_ok:
            print("\n🎉 Server is ready for testing!")
        else:
            print("\n⚠️ Some issues detected.")
    else:
        print("\n❌ Server is not running. Please start the server first:")
        print("   .venv/Scripts/python.exe main.py")
        sys.exit(1)
