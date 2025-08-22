#!/usr/bin/env python3
"""
Test FastMCP HTTP Integration
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_fastmcp_http():
    """Test FastMCP HTTP integration."""
    print("🧪 Testing FastMCP HTTP Integration...")
    
    try:
        from fastmcp import FastMCP
        print("✅ FastMCP imported successfully")
        
        # Create a simple FastMCP server
        mcp = FastMCP("test_server", "1.0.0")
        print("✅ FastMCP server created")
        
        # Register a simple tool
        @mcp.tool(description="Test tool")
        async def test_tool():
            return {"message": "Hello from FastMCP!"}
        
        print("✅ Tool registered")
        
        # Try to get HTTP app
        try:
            http_app = mcp.http_app(path="/mcp")
            print(f"✅ HTTP app created: {http_app}")
            
            if http_app:
                print("✅ HTTP app is available")
                return True
            else:
                print("❌ HTTP app is None")
                return False
                
        except Exception as e:
            print(f"❌ Error creating HTTP app: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_fastmcp_http()
    if success:
        print("\n✅ FastMCP HTTP integration test successful")
    else:
        print("\n❌ FastMCP HTTP integration test failed")
