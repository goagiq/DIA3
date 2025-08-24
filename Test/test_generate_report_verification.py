#!/usr/bin/env python3
"""
Test script to verify generate_report tool functionality after removing export_data.
"""

import asyncio
import logging
import sys
import os
import aiohttp
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_generate_report_verification():
    """Test the generate_report tool verification."""
    
    print("🧪 Testing Generate Report Tool Verification")
    print("=" * 50)
    
    # Test content
    test_content = """
    Cambodia's recent acquisition of J-10 fighter jets from China represents a significant 
    shift in regional military dynamics. This development has implications for ASEAN security, 
    US-China relations, and regional stability.
    """
    
    print(f"📝 Test Content: {test_content[:80]}...")
    print()
    
    # MCP server endpoint
    mcp_url = "http://localhost:8000/mcp"
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test 1: Check available tools
            print("🔍 Test 1: Available Tools Check")
            print("-" * 30)
            
            tools_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            
            async with session.post(mcp_url, json=tools_request) as response:
                if response.status == 200:
                    result = await response.json()
                    if "result" in result:
                        tools = result["result"].get("tools", [])
                        tool_names = [tool['name'] for tool in tools]
                        
                        print(f"✅ Found {len(tools)} tools:")
                        for i, tool in enumerate(tools, 1):
                            print(f"   {i:2d}. {tool['name']}: {tool['description'][:50]}...")
                        
                        # Check if generate_report tool is available
                        if 'generate_report' in tool_names:
                            print("✅ generate_report tool found")
                        else:
                            print("❌ generate_report tool not found")
                        
                        # Check if export_data tool has been removed
                        if 'export_data' in tool_names:
                            print("❌ export_data tool still present (should be removed)")
                        else:
                            print("✅ export_data tool successfully removed")
                        
                    else:
                        print(f"❌ Failed to get tools: {result}")
                else:
                    print(f"❌ HTTP error: {response.status}")
            
            print()
            
            # Test 2: Basic generate_report test
            print("🔍 Test 2: Basic Generate Report Test")
            print("-" * 35)
            
            basic_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "generate_report",
                    "arguments": {
                        "content": test_content,
                        "report_type": "basic",
                        "language": "en",
                        "include_dia3_enhanced": False
                    }
                }
            }
            
            async with session.post(mcp_url, json=basic_request) as response:
                if response.status == 200:
                    result = await response.json()
                    if "result" in result:
                        print("✅ Basic generate_report test successful")
                        print(f"   Result: {result['result']}")
                    else:
                        print(f"❌ Basic generate_report test failed: {result}")
                else:
                    print(f"❌ HTTP error: {response.status}")
            
            print()
            print("✅ All verification tests completed!")
            
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def main():
    """Main test function."""
    print("🚀 Starting Generate Report Tool Verification")
    print("=" * 60)
    
    # Run tests
    asyncio.run(test_generate_report_verification())
    
    print("\n🎉 Verification test suite completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
