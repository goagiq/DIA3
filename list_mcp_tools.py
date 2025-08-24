#!/usr/bin/env python3
"""
List all available MCP tools from the FastMCP server.
"""
import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from strands.tools.mcp.mcp_client import MCPClient
    from mcp.client.streamable_http import streamablehttp_client
    print("✅ MCP client available")
except ImportError as e:
    print(f"❌ MCP client import error: {e}")
    sys.exit(1)


async def list_mcp_tools():
    """List all available MCP tools from the FastMCP server."""
    
    print("🔍 Listing MCP tools from FastMCP server...")
    print("=" * 50)
    
    try:
        # Create MCP client
        mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Get tools
        with mcp_client:
            tools = mcp_client.list_tools_sync()
            print(f"📋 Found {len(tools)} tools")
            print()
            
            # Categorize tools
            export_tools = []
            dia3_tools = []
            analysis_tools = []
            utility_tools = []
            other_tools = []
            
            for i, tool in enumerate(tools, 1):
                name = tool.get('name', 'Unknown')
                description = tool.get('description', 'No description')
                
                print(f"{i:2d}. {name}")
                print(f"    {description}")
                print()
                
                # Categorize
                if 'export' in name.lower():
                    export_tools.append((name, description))
                elif 'dia3' in name.lower():
                    dia3_tools.append((name, description))
                elif any(keyword in name.lower() for keyword in ['analyze', 'analysis', 'report', 'generate']):
                    analysis_tools.append((name, description))
                elif any(keyword in name.lower() for keyword in ['get', 'list', 'search', 'query', 'fetch']):
                    utility_tools.append((name, description))
                else:
                    other_tools.append((name, description))
            
            # Print summary
            print("=" * 50)
            print("📊 TOOL CATEGORIES:")
            print(f"📤 Export tools: {len(export_tools)}")
            print(f"🔬 DIA3 tools: {len(dia3_tools)}")
            print(f"📊 Analysis tools: {len(analysis_tools)}")
            print(f"🔧 Utility tools: {len(utility_tools)}")
            print(f"📦 Other tools: {len(other_tools)}")
            print()
            
            # Show essential tools
            print("🎯 ESSENTIAL TOOLS FOR CAMBODIA ANALYSIS:")
            essential_tools = []
            
            # Add export tools
            for name, desc in export_tools:
                essential_tools.append((name, desc, "Export"))
            
            # Add key DIA3 tools
            for name, desc in dia3_tools[:3]:  # Top 3 DIA3 tools
                essential_tools.append((name, desc, "DIA3"))
            
            # Add key analysis tools
            for name, desc in analysis_tools[:2]:  # Top 2 analysis tools
                essential_tools.append((name, desc, "Analysis"))
            
            # Add key utility tools
            for name, desc in utility_tools[:3]:  # Top 3 utility tools
                essential_tools.append((name, desc, "Utility"))
            
            print(f"📋 Recommended {len(essential_tools)} essential tools:")
            for i, (name, desc, category) in enumerate(essential_tools, 1):
                print(f"  {i:2d}. [{category}] {name}")
            
            return tools
            
    except Exception as e:
        print(f"❌ Error listing tools: {e}")
        return []


if __name__ == "__main__":
    asyncio.run(list_mcp_tools())
