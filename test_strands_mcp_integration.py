#!/usr/bin/env python3
"""
Test script for StrandsMCPClient integration.
This script tests the migration from mock strands agents to StrandsMCPClient.
"""

import sys
import os
import time
import asyncio

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from loguru import logger

def test_strands_mcp_client():
    """Test StrandsMCPClient integration."""
    print("🔍 Testing StrandsMCPClient Integration")
    print("=" * 60)
    
    try:
        # Test 1: Import StrandsMCPClient
        print("1. Testing StrandsMCPClient import...")
        from src.core.strands_mcp_client import StrandsMCPClient, create_mcp_agent
        
        print("   ✅ StrandsMCPClient imported successfully")
        
        # Test 2: Create MCP client
        print("\n2. Testing MCP client creation...")
        mcp_client = StrandsMCPClient()
        print("   ✅ MCP client created successfully")
        
        # Test 3: Get tools from MCP server
        print("\n3. Testing tool retrieval...")
        tools = mcp_client.get_tools_sync()
        print(f"   ✅ Retrieved {len(tools)} tools from MCP server")
        
        if tools:
            print("   📋 Available tools:")
            for i, tool in enumerate(tools[:5], 1):  # Show first 5 tools
                # Handle both dict and MCPAgentTool objects
                if hasattr(tool, 'name'):
                    tool_name = tool.name
                elif isinstance(tool, dict):
                    tool_name = tool.get('name', 'Unknown')
                else:
                    tool_name = str(tool)
                print(f"      {i}. {tool_name}")
            if len(tools) > 5:
                print(f"      ... and {len(tools) - 5} more tools")
        
        # Test 4: Create agent with MCP tools
        print("\n4. Testing agent creation...")
        agent = create_mcp_agent(
            name="test_agent",
            system_prompt="You are a test agent with MCP tools."
        )
        print("   ✅ Agent created successfully with MCP tools")
        
        # Test 5: Test agent status
        print("\n5. Testing agent status...")
        status = mcp_client.get_agent_status()
        print(f"   ✅ Agent status: {status}")
        
        print("\n✅ All StrandsMCPClient tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please ensure strands and mcp packages are installed:")
        print("   pip install strands mcp")
        return False
    except Exception as e:
        print(f"❌ Error testing StrandsMCPClient: {e}")
        return False

def test_mcp_orchestrator():
    """Test MCP orchestrator integration."""
    print("\n🔍 Testing MCP Orchestrator Integration")
    print("=" * 60)
    
    try:
        # Test 1: Import MCP orchestrator
        print("1. Testing MCP orchestrator import...")
        from src.core.mcp_orchestrator import MCPOrchestrator
        
        print("   ✅ MCP orchestrator imported successfully")
        
        # Test 2: Create orchestrator
        print("\n2. Testing orchestrator creation...")
        orchestrator = MCPOrchestrator()
        print("   ✅ MCP orchestrator created successfully")
        
        # Test 3: Get available tools
        print("\n3. Testing tool availability...")
        tools = orchestrator.get_available_tools()
        print(f"   ✅ Available tools: {len(tools)}")
        
        # Test 4: Get orchestrator status
        print("\n4. Testing orchestrator status...")
        status = orchestrator.get_orchestrator_status()
        print(f"   ✅ Orchestrator status: {status}")
        
        print("\n✅ All MCP Orchestrator tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP orchestrator: {e}")
        return False

def test_unified_text_agent():
    """Test unified text agent integration."""
    print("\n🔍 Testing Unified Text Agent Integration")
    print("=" * 60)
    
    try:
        # Test 1: Import unified text agent
        print("1. Testing unified text agent import...")
        from src.agents.unified_text_agent import UnifiedTextAgent
        
        print("   ✅ Unified text agent imported successfully")
        
        # Test 2: Create agent
        print("\n2. Testing agent creation...")
        agent = UnifiedTextAgent("test_text_agent")
        print("   ✅ Unified text agent created successfully")
        
        # Test 3: Get agent status
        print("\n3. Testing agent status...")
        status = agent.get_status()
        print(f"   ✅ Agent status: {status}")
        
        # Test 4: Get available tools
        print("\n4. Testing available tools...")
        tools = agent.get_available_tools()
        print(f"   ✅ Available tools: {len(tools)}")
        
        print("\n✅ All Unified Text Agent tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing unified text agent: {e}")
        return False

async def test_async_operations():
    """Test async operations with StrandsMCPClient."""
    print("\n🔍 Testing Async Operations")
    print("=" * 60)
    
    try:
        from src.core.strands_mcp_client import StrandsMCPClient, run_mcp_agent
        
        # Test 1: Create MCP client
        print("1. Testing async MCP client creation...")
        mcp_client = StrandsMCPClient()
        print("   ✅ Async MCP client created successfully")
        
        # Test 2: Get tools asynchronously
        print("\n2. Testing async tool retrieval...")
        tools = await mcp_client.get_tools_async()
        print(f"   ✅ Retrieved {len(tools)} tools asynchronously")
        
        # Test 3: Create and run agent asynchronously
        print("\n3. Testing async agent execution...")
        agent = mcp_client.create_agent_with_mcp_tools(
            name="async_test_agent",
            system_prompt="You are an async test agent."
        )
        
        # Test with a simple prompt
        prompt = "Hello, this is a test message."
        result = await mcp_client.run_agent_async("async_test_agent", prompt)
        print(f"   ✅ Async agent execution completed: {result[:100]}...")
        
        print("\n✅ All async operations tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing async operations: {e}")
        return False

def main():
    """Run all integration tests."""
    print("🚀 StrandsMCPClient Integration Test Suite")
    print("=" * 80)
    print("Testing migration from mock strands agents to StrandsMCPClient")
    print()
    
    # Run synchronous tests
    tests = [
        test_strands_mcp_client,
        test_mcp_orchestrator,
        test_unified_text_agent
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    # Run async tests
    try:
        async_result = asyncio.run(test_async_operations())
        results.append(async_result)
    except Exception as e:
        print(f"❌ Async test failed with exception: {e}")
        results.append(False)
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 Test Results Summary")
    print("=" * 80)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! StrandsMCPClient integration is working correctly.")
        print("✅ Migration from mock strands agents to StrandsMCPClient successful!")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        print("🔧 You may need to:")
        print("   - Install required packages: pip install strands mcp")
        print("   - Ensure the MCP server is running on port 8000")
        print("   - Check the MCP server configuration")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
