#!/usr/bin/env python3
"""
Script to check if the server is ready after restart.
"""

import requests
import time
import sys

def check_server_ready():
    """Check if the server is ready on port 8000."""
    print("🔍 Checking if server is ready on port 8000...")
    
    max_attempts = 12  # 2 minutes total (12 * 10 seconds)
    attempt = 0
    
    while attempt < max_attempts:
        try:
            # Try to connect to the health endpoint
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is ready!")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"⚠️ Server responded with status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"⏳ Server not ready yet (attempt {attempt + 1}/{max_attempts})")
        except requests.exceptions.Timeout:
            print(f"⏳ Server timeout (attempt {attempt + 1}/{max_attempts})")
        except Exception as e:
            print(f"❌ Error checking server: {e}")
        
        attempt += 1
        if attempt < max_attempts:
            print("   Waiting 10 seconds...")
            time.sleep(10)
    
    print("❌ Server not ready after 2 minutes")
    return False

def check_mcp_endpoint():
    """Check if the MCP endpoint is accessible."""
    print("\n🔍 Checking MCP endpoint...")
    
    try:
        # Try to connect to the MCP endpoint
        headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json"
        }
        
        response = requests.get("http://localhost:8000/mcp", headers=headers, timeout=5)
        print(f"✅ MCP endpoint accessible: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ MCP endpoint not accessible: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Server Readiness Check")
    print("=" * 50)
    
    server_ready = check_server_ready()
    mcp_ready = check_mcp_endpoint()
    
    print("\n📊 Summary:")
    print(f"   Server Ready: {'✅' if server_ready else '❌'}")
    print(f"   MCP Endpoint: {'✅' if mcp_ready else '❌'}")
    
    if server_ready and mcp_ready:
        print("\n🎉 Server is ready for testing!")
        sys.exit(0)
    else:
        print("\n⚠️ Server is not fully ready. Please check the server status.")
        sys.exit(1)
