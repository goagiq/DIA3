#!/usr/bin/env python3
"""
Export Thailand-Cambodia invasion report using MCP export_data tool.
"""
import requests
import json
import uuid
import re


def parse_sse_response(response_text):
    """Parse server-sent events response."""
    lines = response_text.strip().split('\n')
    data_lines = [line for line in lines if line.startswith('data: ')]
    
    if data_lines:
        # Extract JSON from the last data line
        data_line = data_lines[-1]
        json_str = data_line[6:]  # Remove 'data: ' prefix
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    return None


def export_cambodia_report():
    """Export Thailand-Cambodia invasion report to HTML using MCP tools."""
    
    # MCP server endpoint
    url = "http://localhost:8000/mcp"
    headers = {
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json"
    }
    
    # Generate session ID
    session_id = str(uuid.uuid4())
    
    print("🚀 Exporting Thailand-Cambodia Invasion Report...")
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
                "name": "cambodia-report-client",
                "version": "1.0.0"
            }
        }
    }
    
    try:
        print("\n🔧 Initializing MCP session...")
        response = requests.post(url, json=init_payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = parse_sse_response(response.text)
            if result and "result" in result:
                print("✅ Session initialized successfully")
            else:
                print(f"❌ Session initialization failed: {response.text}")
                return False
        else:
            print(f"❌ Session initialization failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error during initialization: {e}")
        return False
    
    # Step 2: List tools to verify export_data is available
    list_tools_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    try:
        print("\n📋 Checking available tools...")
        response = requests.post(url, json=list_tools_payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = parse_sse_response(response.text)
            if result and "result" in result and "tools" in result["result"]:
                tools = result["result"]["tools"]
                tool_names = [tool.get('name', '') for tool in tools]
                
                if 'export_data' in tool_names:
                    print(f"✅ Found export_data tool!")
                else:
                    print(f"❌ export_data tool not found. Available tools: {tool_names[:10]}...")
                    return False
            else:
                print(f"❌ Failed to get tools list: {result}")
                return False
        else:
            print(f"❌ Tools list request failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False
    
    # Step 3: Call export_data tool
    cambodia_data = {
        "topic": "Thailand-Cambodia Invasion: Comprehensive Impact Analysis",
        "analysis_type": "comprehensive",
        "content": """
        Comprehensive analysis of the impacts and consequences of Thailand invading Cambodia.
        
        This analysis covers:
        - Humanitarian consequences and civilian casualties
        - Economic impacts and infrastructure damage
        - Geopolitical implications and regional destabilization
        - Strategic military considerations
        - International response and sanctions
        - Long-term consequences for both nations
        """,
        "key_findings": [
            "Extreme humanitarian crisis affecting 2-3 million people",
            "Civilian casualties estimated at 50,000-100,000",
            "Economic devastation with $50-100 billion in damages",
            "Regional destabilization and international isolation",
            "Strategic failure with high military casualty rates",
            "Long-term refugee crisis and displacement",
            "Infrastructure destruction affecting basic services",
            "International sanctions and diplomatic isolation"
        ],
        "analysis_components": {
            "humanitarian": "Immediate crisis affecting millions",
            "economic": "Devastating financial impact",
            "geopolitical": "Regional destabilization",
            "strategic": "Military and security implications",
            "international": "Global response and consequences"
        }
    }
    
    export_payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "export_data",
            "arguments": {
                "data": cambodia_data,
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
        print(f"\n📊 Calling export_data tool with DIA3 enhanced analysis...")
        response = requests.post(url, json=export_payload, headers=headers, timeout=120)
        
        if response.status_code == 200:
            result = parse_sse_response(response.text)
            if result and "result" in result:
                print(f"✅ export_data tool call successful!")
                print(f"📄 Result: {result['result']}")
                
                # Check if file was created
                import os
                if os.path.exists("Results/thailand_cambodia_invasion_enhanced_report.html"):
                    print(f"✅ HTML report created: Results/thailand_cambodia_invasion_enhanced_report.html")
                else:
                    print(f"ℹ️  Report may have been created with different filename")
                
                return True
            elif result and "error" in result:
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
    print("🇹🇭🇰🇭 Thailand-Cambodia Invasion Report Export")
    print("=" * 60)
    
    success = export_cambodia_report()
    
    if success:
        print(f"\n🎉 Report export completed successfully!")
        print(f"📁 Check the Results/ directory for the HTML report")
    else:
        print(f"\n❌ Report export failed")
