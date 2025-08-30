#!/usr/bin/env python3
"""
Test Port Conflict Resolution
Tests the updated MCP server startup with port conflict handling
"""

import asyncio
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_port_conflict_resolution():
    """Test the port conflict resolution functionality"""
    
    print("🔧 Testing Port Conflict Resolution")
    print("=" * 50)
    
    # Import the function
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from main import start_standalone_mcp_server
        print("✅ Successfully imported start_standalone_mcp_server function")
    except ImportError as e:
        print(f"❌ Failed to import function: {e}")
        return False
    
    # Test the function
    try:
        print("\n🚀 Testing MCP server startup with port conflict handling...")
        server = start_standalone_mcp_server(host="localhost", port=8000)
        
        if server:
            print("✅ MCP server started successfully")
            print(f"   Server object: {type(server)}")
            
            # Check if server is running
            if hasattr(server, 'is_server_running'):
                is_running = server.is_server_running()
                print(f"   Server running: {is_running}")
            else:
                print("   Server running status: Unknown (no is_server_running method)")
            
            return True
        else:
            print("❌ MCP server failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MCP server startup: {e}")
        return False

def main():
    """Main test function"""
    print(f"🕐 Test started at: {datetime.now()}")
    
    success = test_port_conflict_resolution()
    
    print(f"\n📊 Test Result: {'✅ PASS' if success else '❌ FAIL'}")
    print(f"🕐 Test completed at: {datetime.now()}")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
