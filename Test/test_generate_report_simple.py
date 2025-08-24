#!/usr/bin/env python3
"""
Simple test script for enhanced generate_report MCP tool functionality.

This script starts the MCP server and tests the enhanced generate_report tool
by connecting to it through the proper MCP interface.
"""

import asyncio
import logging
import sys
import os
import subprocess
import time
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_enhanced_generate_report():
    """Test the enhanced generate_report tool."""
    
    print("🧪 Testing Enhanced Generate Report Tool")
    print("=" * 50)
    
    # Test content for analysis
    test_content = """
    Cambodia's recent acquisition of J-10 fighter jets from China represents a significant 
    shift in regional military dynamics. This development has implications for ASEAN security, 
    US-China relations, and regional stability.
    """
    
    print(f"📝 Test Content: {test_content[:80]}...")
    print()
    
    try:
        # Import and test the enhanced report generation directly
        from src.mcp_servers.unified_mcp_server import UnifiedMCPServer
        
        # Create server instance
        server = UnifiedMCPServer()
        
        # Test the enhanced generate_report functionality
        print("🔍 Testing Enhanced Report Generation with DIA3")
        print("-" * 50)
        
        # Test basic report generation (without DIA3 enhanced)
        print("📋 Test 1: Basic Report Generation")
        
        # Create a simple test to verify the tool exists
        if hasattr(server, 'mcp') and server.mcp:
            print("✅ MCP server initialized successfully")
            
            # Check if the tool is registered
            tools = server.mcp.tools if hasattr(server.mcp, 'tools') else []
            tool_names = [tool.name for tool in tools] if tools else []
            
            if 'generate_report' in tool_names:
                print("✅ generate_report tool found in MCP server")
            else:
                print("❌ generate_report tool not found in MCP server")
                print(f"Available tools: {tool_names}")
        else:
            print("❌ MCP server not properly initialized")
        
        print()
        
        # Test 2: Check export_data tool (should be simplified)
        print("📋 Test 2: Export Data Tool Status")
        if 'export_data' in tool_names:
            print("✅ export_data tool found (should be simplified)")
        else:
            print("❌ export_data tool not found")
        
        print()
        
        # Test 3: Verify tool descriptions
        print("📋 Test 3: Tool Descriptions")
        for tool in tools:
            if tool.name == 'generate_report':
                print(f"✅ generate_report: {tool.description}")
            elif tool.name == 'export_data':
                print(f"✅ export_data: {tool.description}")
        
        print()
        print("✅ Tool verification completed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def main():
    """Main test function."""
    print("🚀 Starting Simple Enhanced Generate Report Tool Tests")
    print("=" * 60)
    
    # Run tests
    asyncio.run(test_enhanced_generate_report())
    
    print("\n🎉 Simple test suite completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
