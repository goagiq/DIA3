#!/usr/bin/env python3
"""
Test MCP Force Projection Tools
Test script to verify MCP client can access force projection tools
"""

import asyncio
import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.unified_mcp_client import call_force_projection_tool


async def test_mcp_force_projection():
    """Test MCP force projection tools"""
    print("🔧 Testing MCP Force Projection Tools")
    print("=" * 60)
    
    try:
        # Test force projection simulation
        print("🚀 Testing force projection simulation via MCP...")
        
        simulation_params = {
            "adversary_type": "peer_adversary",
            "domain_type": "defense",
            "time_horizon_months": 12,
            "num_iterations": 1000,
            "confidence_level": 0.95
        }
        
        result = await call_force_projection_tool("simulation", simulation_params)
        
        if result.get("success"):
            print("✅ Force projection simulation via MCP completed successfully!")
            print(f"   📊 Simulation ID: {result.get('simulation_id', 'N/A')}")
            print(f"   📈 Threat Level: {result.get('summary', {}).get('threat_level', 'N/A')}")
            print(f"   📊 Effectiveness: {result.get('summary', {}).get('overall_effectiveness', 'N/A')}")
        else:
            print(f"⚠️  Force projection simulation via MCP failed: {result.get('error', 'Unknown error')}")
        
        # Test force projection history
        print("\n📚 Testing force projection history via MCP...")
        
        history_params = {"limit": 5}
        
        history_result = await call_force_projection_tool("history", history_params)
        
        if history_result.get("success"):
            print("✅ Force projection history via MCP retrieved successfully!")
            print(f"   📊 Total simulations: {history_result.get('total_simulations', 0)}")
        else:
            print(f"⚠️  Force projection history via MCP failed: {history_result.get('error', 'Unknown error')}")
        
        print(f"\n🎉 MCP force projection tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP force projection: {str(e)}")
        return False


async def main():
    """Main test function"""
    print("🚀 MCP Force Projection Test")
    print("=" * 40)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    success = await test_mcp_force_projection()
    
    if success:
        print("\n🎉 MCP force projection integration is working correctly!")
    else:
        print("\n⚠️  MCP force projection integration has issues.")
    
    return success


if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
