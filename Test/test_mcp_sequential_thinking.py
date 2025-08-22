#!/usr/bin/env python3
"""
Test script for sequential thinking and MCP functionality
"""

import sys
import os
import asyncio
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_mcp_config():
    """Test MCP configuration loading"""
    print("🔧 Testing MCP Configuration...")
    
    try:
        import json
        with open("mcp_tool_config.json", "r") as f:
            config = json.load(f)
        
        enabled_tools = [
            name for name, tool_config in config.get("tools", {}).items()
            if tool_config.get("enabled", False)
        ]
        
        print(f"✅ MCP Configuration loaded successfully")
        print(f"📋 Enabled tools: {', '.join(enabled_tools)}")
        return True
        
    except Exception as e:
        print(f"❌ MCP Configuration test failed: {e}")
        return False

def test_monte_carlo_engine():
    """Test Monte Carlo engine for sequential thinking"""
    print("\n🧮 Testing Monte Carlo Engine (Sequential Thinking)...")
    
    try:
        from core.monte_carlo.engine import MonteCarloEngine
        from core.monte_carlo.config import MonteCarloConfig
        
        # Initialize engine
        config = MonteCarloConfig()
        engine = MonteCarloEngine(config)
        
        print("✅ Monte Carlo Engine initialized successfully")
        
        # Test basic simulation
        result = engine.run_simulation(
            parameters={"mean": 100, "std": 20},
            num_simulations=100,
            simulation_type="normal"
        )
        
        print(f"✅ Basic simulation completed: {len(result)} results")
        return True
        
    except Exception as e:
        print(f"❌ Monte Carlo Engine test failed: {e}")
        return False

def test_mcp_server():
    """Test MCP server functionality"""
    print("\n🔌 Testing MCP Server...")
    
    try:
        from mcp_servers.unified_mcp_server import UnifiedMCPServer
        
        # Initialize server
        server = UnifiedMCPServer()
        print("✅ MCP Server initialized successfully")
        
        # Test tool availability
        available_tools = server.get_available_tools()
        print(f"✅ Available MCP tools: {len(available_tools)} tools")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP Server test failed: {e}")
        return False

def test_sequential_analysis():
    """Test sequential thinking analysis"""
    print("\n🧠 Testing Sequential Thinking Analysis...")
    
    try:
        from src.core.sequential_thinking_service import analyze_sequential_thinking_safe
        
        # Test sequential analysis with timeout handling
        async def run_analysis():
            return await analyze_sequential_thinking_safe(
                scenario="test_scenario",
                steps=3,
                iterations=10
            )
        
        # Run the async analysis
        import asyncio
        analysis_result = asyncio.run(run_analysis())
        
        if analysis_result.success:
            print("✅ Sequential analysis completed successfully")
            print(f"   Steps completed: {len(analysis_result.steps_completed)}")
            print(f"   Duration: {analysis_result.total_duration:.2f}s")
        else:
            print(f"❌ Sequential analysis failed: {analysis_result.error_messages}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Sequential thinking test failed: {e}")
        return False

def test_force_projection():
    """Test force projection engine"""
    print("\n⚔️ Testing Force Projection Engine...")
    
    try:
        from core.force_projection_engine import ForceProjectionEngine
        
        # Initialize engine
        engine = ForceProjectionEngine()
        print("✅ Force Projection Engine initialized")
        
        # Test basic analysis
        result = engine.analyze_capability(
            adversary_type="peer_adversary",
            domain_type="defense",
            capabilities=["military_strength", "technological_advantage"]
        )
        
        print(f"✅ Force projection analysis completed")
        return True
        
    except Exception as e:
        print(f"❌ Force projection test failed: {e}")
        return False

async def test_mcp_client():
    """Test MCP client functionality"""
    print("\n📡 Testing MCP Client...")
    
    try:
        from core.unified_mcp_client import call_unified_mcp_tool
        
        # Test basic MCP call
        result = await call_unified_mcp_tool(
            tool_name="test_tool",
            parameters={"test": "value"}
        )
        
        print("✅ MCP Client test completed")
        return True
        
    except Exception as e:
        print(f"❌ MCP Client test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Sequential Thinking and MCP Tests")
    print("=" * 60)
    
    # Run synchronous tests
    tests = [
        test_mcp_config,
        test_monte_carlo_engine,
        test_mcp_server,
        test_sequential_analysis,
        test_force_projection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    # Run async test
    try:
        if asyncio.run(test_mcp_client()):
            passed += 1
        total += 1
    except Exception as e:
        print(f"❌ Async test failed with exception: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Sequential thinking and MCP are working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
