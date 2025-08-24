#!/usr/bin/env python3
"""
Debug script to investigate MCP tools and fix Agent API issues.
"""
import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from strands import Agent
    from strands.tools.mcp.mcp_client import MCPClient
    from mcp.client.streamable_http import streamablehttp_client
    print("✅ Full Strands implementation available")
except ImportError as e:
    print(f"❌ Strands import error: {e}")
    sys.exit(1)


def debug_mcp_tools():
    """Debug the MCP tools to understand their structure."""
    
    try:
        print("🔍 Debugging MCP tools...")
        
        # Create MCP client
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Get tools from the FastMCP server
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            print(f"✅ Retrieved {len(tools)} tools")
            
            # Debug each tool
            print("\n🔧 Tool Details:")
            for i, tool in enumerate(tools, 1):
                print(f"\nTool {i}:")
                print(f"  Type: {type(tool)}")
                print(f"  Dir: {dir(tool)}")
                
                # Try different ways to access tool information
                try:
                    if hasattr(tool, 'name'):
                        print(f"  Name: {tool.name}")
                    if hasattr(tool, 'description'):
                        print(f"  Description: {tool.description}")
                    if hasattr(tool, '__dict__'):
                        print(f"  Dict: {tool.__dict__}")
                    if hasattr(tool, 'to_dict'):
                        print(f"  To Dict: {tool.to_dict()}")
                    if hasattr(tool, 'dict'):
                        print(f"  Dict Method: {tool.dict()}")
                except Exception as e:
                    print(f"  Error accessing tool: {e}")
                
                # Try to call the tool directly
                try:
                    if hasattr(tool, '__call__'):
                        print(f"  Callable: Yes")
                        # Try a simple test call
                        if hasattr(tool, 'name') and tool.name:
                            print(f"  Tool name found: {tool.name}")
                except Exception as e:
                    print(f"  Error calling tool: {e}")
    
    except Exception as e:
        print(f"❌ Error debugging tools: {e}")


def test_strands_agent_api():
    """Test the Strands Agent API to understand the correct usage."""
    
    try:
        print("\n🤖 Testing Strands Agent API...")
        
        # Create a simple agent
        agent = Agent()
        print(f"Agent type: {type(agent)}")
        print(f"Agent dir: {dir(agent)}")
        
        # Check available methods
        methods = [attr for attr in dir(agent) if not attr.startswith('_')]
        print(f"Available methods: {methods}")
        
        # Try to understand the correct API
        if hasattr(agent, 'run'):
            print("✅ Agent has 'run' method")
        elif hasattr(agent, 'invoke'):
            print("✅ Agent has 'invoke' method")
        elif hasattr(agent, 'call'):
            print("✅ Agent has 'call' method")
        else:
            print("❌ Agent doesn't have expected methods")
            
    except Exception as e:
        print(f"❌ Error testing agent API: {e}")


def test_mcp_client_direct():
    """Test direct MCP client usage."""
    
    try:
        print("\n🔧 Testing direct MCP client usage...")
        
        # Create MCP client
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Test direct tool calls
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            
            # Try to call a tool directly
            for i, tool in enumerate(tools[:3], 1):  # Test first 3 tools
                try:
                    print(f"\nTesting Tool {i}:")
                    
                    # Get tool name
                    tool_name = None
                    if hasattr(tool, 'name'):
                        tool_name = tool.name
                    elif hasattr(tool, '__dict__') and 'name' in tool.__dict__:
                        tool_name = tool.__dict__['name']
                    
                    if tool_name:
                        print(f"  Tool name: {tool_name}")
                        
                        # Try to call the tool
                        try:
                            result = mcp_client.call_tool(tool_name, {})
                            print(f"  Call result: {result}")
                        except Exception as call_error:
                            print(f"  Call error: {call_error}")
                    else:
                        print(f"  Could not determine tool name")
                        
                except Exception as e:
                    print(f"  Error testing tool {i}: {e}")
    
    except Exception as e:
        print(f"❌ Error testing direct MCP client: {e}")


if __name__ == "__main__":
    print("🚀 Starting MCP Tools Debug")
    
    # Debug MCP tools
    debug_mcp_tools()
    
    # Test Strands Agent API
    test_strands_agent_api()
    
    # Test direct MCP client
    test_mcp_client_direct()
    
    print("\n✅ Debug completed")
