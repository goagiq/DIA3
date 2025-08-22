#!/usr/bin/env python3
"""
MCP Client Test for Enhanced Report Functionality
Tests MCP client-server communication for enhanced report generation.
"""

import requests
import json
import time
from typing import Dict, Any

def test_mcp_initialize():
    """Test MCP initialize method."""
    print("🔌 Testing MCP Initialize...")
    
    try:
        # MCP initialize request
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
                    "name": "enhanced-report-test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send request to MCP server with proper headers
        response = requests.post(
            "http://localhost:8000/mcp",
            json=initialize_request,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ MCP initialize successful")
            print(f"   - Server info: {result.get('result', {}).get('serverInfo', {})}")
            return True
        else:
            print(f"❌ MCP initialize failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ MCP initialize error: {e}")
        return False

def test_mcp_list_tools():
    """Test MCP list tools method."""
    print("🔧 Testing MCP List Tools...")
    
    try:
        # MCP tools/list request
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        # Send request to MCP server with proper headers
        response = requests.post(
            "http://localhost:8000/mcp",
            json=list_tools_request,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            tools = result.get('result', {}).get('tools', [])
            
            print(f"✅ MCP list tools successful")
            print(f"   - Available tools: {len(tools)}")
            
            # Look for enhanced report tools
            enhanced_report_tools = [
                tool for tool in tools 
                if 'enhanced' in tool.get('name', '').lower() or 
                   'report' in tool.get('name', '').lower()
            ]
            
            if enhanced_report_tools:
                print(f"   - Enhanced report tools found: {len(enhanced_report_tools)}")
                for tool in enhanced_report_tools:
                    print(f"     - {tool.get('name')}: {tool.get('description', 'No description')}")
            else:
                print("   - No enhanced report tools found")
                
            return True
        else:
            print(f"❌ MCP list tools failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ MCP list tools error: {e}")
        return False

def test_mcp_call_enhanced_report_tool():
    """Test MCP call enhanced report tool."""
    print("📄 Testing MCP Call Enhanced Report Tool...")
    
    try:
        # MCP tools/call request for enhanced report
        call_tool_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "generate_enhanced_report",
                "arguments": {
                    "query": "Pakistan's proposed acquisition of 50 submarines and its strategic implications for conventional deterrence",
                    "title": "Pakistan's 50-Submarine Acquisition Analysis",
                    "subtitle": "Strategic Implications for Conventional Deterrence"
                }
            }
        }
        
        # Send request to MCP server with proper headers
        response = requests.post(
            "http://localhost:8000/mcp",
            json=call_tool_request,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            timeout=60  # Longer timeout for report generation
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if 'result' in result:
                print(f"✅ MCP enhanced report generation successful")
                print(f"   - Result: {result.get('result', {})}")
                return True
            elif 'error' in result:
                print(f"❌ MCP enhanced report generation error: {result.get('error', {})}")
                return False
            else:
                print(f"❌ Unexpected MCP response: {result}")
                return False
        else:
            print(f"❌ MCP call tool failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ MCP call tool error: {e}")
        return False

def test_mcp_streamable_http():
    """Test MCP streamable HTTP protocol."""
    print("🌊 Testing MCP Streamable HTTP...")
    
    try:
        # Test streamable HTTP endpoint
        response = requests.get(
            "http://localhost:8000/mcp/stream",
            headers={"Accept": "application/json, text/event-stream"},
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ MCP streamable HTTP endpoint accessible")
            return True
        else:
            print(f"❌ MCP streamable HTTP failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ MCP streamable HTTP error: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 MCP Client Test for Enhanced Report Functionality")
    print("=" * 60)
    
    # Wait for servers to be ready
    print("⏳ Waiting for servers to be ready...")
    time.sleep(5)
    
    # Run tests
    tests = [
        test_mcp_initialize(),
        test_mcp_list_tools(),
        test_mcp_streamable_http(),
        test_mcp_call_enhanced_report_tool()
    ]
    
    # Results
    passed = sum(tests)
    total = len(tests)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All MCP client tests passed!")
        print("✅ MCP client-server communication is working correctly")
        print("✅ Enhanced report functionality is accessible via MCP")
    else:
        print("⚠️ Some MCP client tests failed")
        print("Check the output above for details")

if __name__ == "__main__":
    main()
