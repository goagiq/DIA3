#!/usr/bin/env python3
"""
Test MCP client connectivity to verify tools are accessible.
"""
import requests
import json
import uuid


def test_mcp_connectivity():
    """Test MCP client connectivity to the server."""
    
    # MCP server endpoint
    url = "http://localhost:8000/mcp"
    headers = {
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json"
    }
    
    # Generate session ID
    session_id = str(uuid.uuid4())
    
    print("🔍 Testing MCP client connectivity...")
    print(f"📡 Connecting to: {url}")
    print(f"🆔 Session ID: {session_id}")
    
    # Step 1: Initialize session
    init_payload = {
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
    
    try:
        print("\n🔧 Initializing session...")
        response = requests.post(url, json=init_payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Session initialized successfully")
        else:
            print(f"❌ Session initialization failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error during initialization: {e}")
        return False
    
    # Step 2: List available tools
    list_tools_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    try:
        print("\n📋 Requesting tool list...")
        response = requests.post(url, json=list_tools_payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result and "tools" in result["result"]:
                tools = result["result"]["tools"]
                print(f"✅ Success! Found {len(tools)} MCP tools:")
                
                # List all tool names
                for i, tool in enumerate(tools, 1):
                    print(f"  {i:2d}. {tool.get('name', 'Unknown')}")
                
                # Look for specific tools we need
                tool_names = [tool.get('name', '') for tool in tools]
                
                if 'export_data' in tool_names:
                    print(f"\n🎯 Found 'export_data' tool!")
                else:
                    print(f"\n❌ 'export_data' tool not found")
                
                if 'generate_report' in tool_names:
                    print(f"🎯 Found 'generate_report' tool!")
                else:
                    print(f"❌ 'generate_report' tool not found")
                
                # Look for DIA3 tools
                dia3_tools = [name for name in tool_names if 'dia3' in name.lower()]
                if dia3_tools:
                    print(f"\n🔧 Found DIA3 tools: {dia3_tools}")
                else:
                    print(f"\nℹ️  No DIA3-specific tools found (this is expected)")
                
                return True
            else:
                print(f"❌ Unexpected response format: {result}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return False


def test_export_data_tool():
    """Test the export_data tool specifically."""
    
    url = "http://localhost:8000/mcp"
    headers = {
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json"
    }
    
    # Test data for Thailand-Cambodia invasion analysis
    test_data = {
        "topic": "Thailand-Cambodia Invasion Impact Analysis",
        "analysis_type": "comprehensive",
        "content": "Comprehensive analysis of the impacts and consequences of Thailand invading Cambodia, including humanitarian, economic, geopolitical, and strategic implications.",
        "key_findings": [
            "Extreme humanitarian crisis affecting 2-3 million people",
            "Economic devastation with $50-100 billion in damages",
            "Regional destabilization and international isolation",
            "Strategic failure with high casualty rates"
        ]
    }
    
    # Call export_data tool
    export_payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "export_data",
            "arguments": {
                "data": test_data,
                "format": "html",
                "include_dia3_enhanced": True,
                "analysis_type": "comprehensive",
                "include_sentiment": True,
                "include_forecasting": True,
                "include_strategic_analysis": True,
                "include_monte_carlo": True,
                "include_knowledge_graph": True,
                "include_interactive_visualizations": True,
                "output_dir": "Results"
            }
        }
    }
    
    try:
        print(f"\n🚀 Testing export_data tool...")
        response = requests.post(url, json=export_payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                print(f"✅ export_data tool call successful!")
                print(f"📄 Result: {result['result']}")
                return True
            elif "error" in result:
                print(f"❌ Tool call error: {result['error']}")
                return False
            else:
                print(f"❌ Unexpected response: {result}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return False


if __name__ == "__main__":
    print("🧪 MCP Client Connectivity Test")
    print("=" * 50)
    
    # Test connectivity
    if test_mcp_connectivity():
        print(f"\n✅ MCP client connectivity test PASSED")
        
        # Test export_data tool
        if test_export_data_tool():
            print(f"\n✅ export_data tool test PASSED")
            print(f"\n🎉 All tests passed! MCP tools are working correctly.")
        else:
            print(f"\n❌ export_data tool test FAILED")
    else:
        print(f"\n❌ MCP client connectivity test FAILED")
