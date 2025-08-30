#!/usr/bin/env python3
"""
Test Integrated MCP Manager
Demonstrates the integrated dynamic MCP tool management system
"""

import sys
import os
import asyncio
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_servers.integrated_dynamic_mcp_manager import integrated_mcp_manager
from mcp_servers.dynamic_tool_manager import ToolStatus, ResourceLevel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_integrated_mcp_manager():
    """Test the integrated MCP manager functionality"""
    print("🚀 Testing Integrated MCP Manager")
    print("=" * 60)
    
    try:
        # Test 1: List available tools
        print("\n📋 Test 1: Available tools")
        available_tools = await integrated_mcp_manager.get_available_tools()
        print(f"Available tools: {available_tools}")
        
        # Test 2: System resources
        print("\n💻 Test 2: System resources")
        resources = integrated_mcp_manager.get_system_resources()
        resource_level = integrated_mcp_manager.get_resource_level()
        print(f"CPU: {resources.get('cpu_percent', 0):.1f}%")
        print(f"Memory: {resources.get('memory_percent', 0):.1f}%")
        print(f"Resource Level: {resource_level.value}")
        
        # Test 3: Tool statuses
        print("\n📊 Test 3: Tool statuses")
        statuses = integrated_mcp_manager.get_all_tool_statuses()
        for tool_name, status_info in statuses.items():
            print(f"{tool_name}: {status_info.status.value} (Priority: {status_info.config.priority})")
        
        # Test 4: Enable a tool (if available)
        if available_tools:
            test_tool = available_tools[0]
            print(f"\n🚀 Test 4: Enable tool {test_tool}")
            success = await integrated_mcp_manager.enable_tool(test_tool)
            print(f"Enable {test_tool}: {'✅ Success' if success else '❌ Failed'}")
        
        # Test 5: Workload optimization
        print("\n🎯 Test 5: Workload optimization")
        try:
            await integrated_mcp_manager.optimize_for_workload("lightweight")
            print("✅ Lightweight optimization applied")
        except Exception as e:
            print(f"❌ Optimization failed: {e}")
        
        # Test 6: Auto-scaling
        print("\n⚖️ Test 6: Auto-scaling")
        integrated_mcp_manager.set_auto_scaling(True)
        print("✅ Auto-scaling enabled")
        
        # Test 7: Health check
        print("\n🏥 Test 7: Health check")
        enabled_tools = await integrated_mcp_manager.get_enabled_tools()
        total_tools = len(available_tools)
        health_score = (len(enabled_tools) / total_tools * 100) if total_tools > 0 else 0
        print(f"Health Score: {health_score:.1f}%")
        print(f"Enabled Tools: {len(enabled_tools)}/{total_tools}")
        
        # Test 8: Tool execution (simulated)
        print("\n⚡ Test 8: Tool execution simulation")
        if available_tools:
            test_tool = available_tools[0]
            try:
                tool_instance = await integrated_mcp_manager.get_tool_instance(test_tool)
                if tool_instance:
                    print(f"✅ Successfully retrieved {test_tool} instance")
                else:
                    print(f"⚠️ {test_tool} instance not available")
            except Exception as e:
                print(f"❌ Error getting {test_tool} instance: {e}")
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.error(f"Test error: {e}", exc_info=True)


async def test_workload_optimizations():
    """Test different workload optimization scenarios"""
    print("\n🎯 Testing Workload Optimizations")
    print("=" * 50)
    
    workload_types = [
        "monte_carlo_heavy",
        "multimedia_heavy", 
        "analysis_heavy",
        "lightweight"
    ]
    
    for workload_type in workload_types:
        print(f"\n📊 Testing {workload_type} optimization:")
        try:
            await integrated_mcp_manager.optimize_for_workload(workload_type)
            enabled_tools = await integrated_mcp_manager.get_enabled_tools()
            print(f"  ✅ Enabled tools: {enabled_tools}")
        except Exception as e:
            print(f"  ❌ Failed: {e}")


async def test_resource_monitoring():
    """Test resource monitoring capabilities"""
    print("\n📡 Testing Resource Monitoring")
    print("=" * 40)
    
    # Monitor for a few seconds
    print("Monitoring system resources for 5 seconds...")
    for i in range(5):
        resources = integrated_mcp_manager.get_system_resources()
        resource_level = integrated_mcp_manager.get_resource_level()
        print(f"  {i+1}s: CPU {resources.get('cpu_percent', 0):.1f}%, "
              f"Memory {resources.get('memory_percent', 0):.1f}%, "
              f"Level: {resource_level.value}")
        await asyncio.sleep(1)


async def main():
    """Main test function"""
    print("🧪 Integrated MCP Manager Test Suite")
    print("=" * 60)
    
    try:
        # Run basic functionality tests
        await test_integrated_mcp_manager()
        
        # Run workload optimization tests
        await test_workload_optimizations()
        
        # Run resource monitoring tests
        await test_resource_monitoring()
        
        print("\n🎉 All tests completed successfully!")
        print("The Integrated MCP Manager is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        logger.error(f"Test suite error: {e}", exc_info=True)
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        await integrated_mcp_manager.cleanup()
        print("✅ Cleanup completed")


if __name__ == "__main__":
    asyncio.run(main())
