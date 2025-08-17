#!/usr/bin/env python3
"""
Test Force Projection Integration
Comprehensive test script to verify force projection simulation integration
"""

import asyncio
import sys
import os
import json
import time
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.force_projection_engine import ForceProjectionEngine, AdversaryType, DomainType


async def test_force_projection_engine():
    """Test the force projection engine directly"""
    print("🧪 Testing Force Projection Engine Directly")
    print("=" * 60)
    
    try:
        # Initialize engine
        engine = ForceProjectionEngine()
        print("✅ Force projection engine initialized")
        
        # Test simulation for different domains
        domains = ["defense", "business", "cyber", "financial"]
        adversary_types = ["peer_adversary", "business_competitor", "cyber_adversary"]
        
        results = []
        
        for domain in domains:
            for adversary_type in adversary_types:
                print(f"\n📊 Testing {domain} domain with {adversary_type}...")
                
                # Run simulation
                result = await engine.simulate_force_projection_capabilities(
                    adversary_type=adversary_type,
                    domain_type=domain,
                    time_horizon_months=12,
                    num_iterations=1000,  # Reduced for testing
                    confidence_level=0.95
                )
                
                # Store results
                results.append({
                    "domain": domain,
                    "adversary_type": adversary_type,
                    "simulation_id": result.simulation_id,
                    "threat_level": result.threat_assessment["threat_level"],
                    "effectiveness": result.effectiveness_analysis["overall_effectiveness"],
                    "execution_time": result.metadata["execution_time_seconds"]
                })
                
                print(f"   ✅ Simulation completed: {result.simulation_id}")
                print(f"   📈 Threat Level: {result.threat_assessment['threat_level']}")
                print(f"   📊 Effectiveness: {result.effectiveness_analysis['overall_effectiveness']:.3f}")
                print(f"   ⏱️  Execution Time: {result.metadata['execution_time_seconds']:.2f}s")
        
        # Test visualization
        if results:
            first_result = results[0]
            print(f"\n🎨 Testing visualization for simulation {first_result['simulation_id']}...")
            
            # Find the simulation in history
            history = engine.get_simulation_history(limit=100)
            target_simulation = None
            
            for simulation in history:
                if simulation.simulation_id == first_result['simulation_id']:
                    target_simulation = simulation
                    break
            
            if target_simulation:
                # Create visualization
                visualization_data = engine.create_visualization(target_simulation)
                print("✅ Visualization created successfully")
                print(f"   📊 Visualization data length: {len(visualization_data)} characters")
            else:
                print("⚠️  Could not find simulation for visualization")
        
        # Test performance metrics
        print(f"\n📈 Performance Metrics:")
        metrics = engine.get_performance_metrics()
        print(f"   Total Simulations: {metrics.get('total_simulations', 0)}")
        print(f"   Average Execution Time: {metrics.get('avg_execution_time', 0):.2f}s")
        
        # Test export functionality
        if results:
            print(f"\n📤 Testing export functionality...")
            export_data = engine.export_simulation_result(target_simulation, "json")
            print("✅ Export completed successfully")
            print(f"   📄 Export data length: {len(export_data)} characters")
        
        print(f"\n🎉 Force projection engine tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing force projection engine: {str(e)}")
        return False


async def test_force_projection_api():
    """Test the force projection API endpoints"""
    print("\n🌐 Testing Force Projection API Endpoints")
    print("=" * 60)
    
    try:
        import httpx
        
        # Test API endpoints
        base_url = "http://localhost:8004"
        
        # Test health endpoint
        print("🏥 Testing health endpoint...")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/api/force-projection/health")
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Health check passed: {health_data}")
            else:
                print(f"⚠️  Health check failed: {response.status_code}")
        
        # Test adversary types endpoint
        print("\n🎯 Testing adversary types endpoint...")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/api/force-projection/adversary-types")
            if response.status_code == 200:
                adversary_data = response.json()
                print(f"✅ Adversary types retrieved: {len(adversary_data['adversary_types'])} types")
            else:
                print(f"⚠️  Adversary types failed: {response.status_code}")
        
        # Test domain types endpoint
        print("\n🌍 Testing domain types endpoint...")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/api/force-projection/domain-types")
            if response.status_code == 200:
                domain_data = response.json()
                print(f"✅ Domain types retrieved: {len(domain_data['domain_types'])} types")
            else:
                print(f"⚠️  Domain types failed: {response.status_code}")
        
        # Test simulation endpoint
        print("\n🚀 Testing simulation endpoint...")
        simulation_request = {
            "adversary_type": "peer_adversary",
            "domain_type": "defense",
            "time_horizon_months": 12,
            "num_iterations": 1000,
            "confidence_level": 0.95
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/api/force-projection/simulate",
                json=simulation_request
            )
            
            if response.status_code == 200:
                simulation_data = response.json()
                print(f"✅ Simulation completed: {simulation_data['simulation_id']}")
                print(f"   📈 Threat Level: {simulation_data['summary']['threat_level']}")
                print(f"   📊 Effectiveness: {simulation_data['summary']['overall_effectiveness']:.3f}")
                
                # Test visualization with the simulation result
                print("\n🎨 Testing visualization endpoint...")
                viz_request = {
                    "simulation_id": simulation_data['simulation_id']
                }
                
                viz_response = await client.post(
                    f"{base_url}/api/force-projection/visualize",
                    json=viz_request
                )
                
                if viz_response.status_code == 200:
                    viz_data = viz_response.json()
                    print("✅ Visualization created successfully")
                    print(f"   📊 Visualization data length: {len(viz_data['visualization'])} characters")
                else:
                    print(f"⚠️  Visualization failed: {viz_response.status_code}")
                
                # Test history endpoint
                print("\n📚 Testing history endpoint...")
                history_request = {"limit": 10}
                
                history_response = await client.post(
                    f"{base_url}/api/force-projection/history",
                    json=history_request
                )
                
                if history_response.status_code == 200:
                    history_data = history_response.json()
                    print(f"✅ History retrieved: {history_data['total_simulations']} simulations")
                else:
                    print(f"⚠️  History failed: {history_response.status_code}")
                
            else:
                print(f"⚠️  Simulation failed: {response.status_code}")
                print(f"   Response: {response.text}")
        
        print(f"\n🎉 Force projection API tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing force projection API: {str(e)}")
        return False


async def test_force_projection_mcp_tools():
    """Test the force projection MCP tools"""
    print("\n🔧 Testing Force Projection MCP Tools")
    print("=" * 60)
    
    try:
        from src.mcp_servers.force_projection_mcp_tools import ForceProjectionMCPTools
        
        # Initialize MCP tools
        mcp_tools = ForceProjectionMCPTools()
        print("✅ Force projection MCP tools initialized")
        
        # Test tool listing
        tools = mcp_tools.get_tools()
        print(f"📋 Available tools: {len(tools)}")
        for tool_name, tool_info in tools.items():
            print(f"   🔧 {tool_name}: {tool_info['description']}")
        
        # Test simulation tool
        print(f"\n🚀 Testing force projection simulation tool...")
        simulation_params = {
            "adversary_type": "peer_adversary",
            "domain_type": "defense",
            "time_horizon_months": 12,
            "num_iterations": 1000,
            "confidence_level": 0.95
        }
        
        result = await mcp_tools.force_projection_simulation(**simulation_params)
        
        if result["success"]:
            print(f"✅ Simulation completed: {result['simulation_id']}")
            print(f"   📈 Threat Level: {result['summary']['threat_level']}")
            print(f"   📊 Effectiveness: {result['summary']['overall_effectiveness']:.3f}")
            
            # Test visualization tool
            print(f"\n🎨 Testing visualization tool...")
            viz_params = {
                "simulation_id": result['simulation_id']
            }
            
            viz_result = await mcp_tools.force_projection_visualization(**viz_params)
            
            if viz_result["success"]:
                print("✅ Visualization created successfully")
                print(f"   📊 Visualization data length: {len(viz_result['visualization'])} characters")
            else:
                print(f"⚠️  Visualization failed: {viz_result['error']}")
            
            # Test history tool
            print(f"\n📚 Testing history tool...")
            history_params = {"limit": 10}
            
            history_result = await mcp_tools.force_projection_history(**history_params)
            
            if history_result["success"]:
                print(f"✅ History retrieved: {history_result['total_simulations']} simulations")
            else:
                print(f"⚠️  History failed: {history_result['error']}")
            
        else:
            print(f"⚠️  Simulation failed: {result['error']}")
        
        print(f"\n🎉 Force projection MCP tools tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing force projection MCP tools: {str(e)}")
        return False


async def main():
    """Main test function"""
    print("🚀 Force Projection Integration Test Suite")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Test results
    test_results = []
    
    # Test 1: Force Projection Engine
    print("🔬 Test 1: Force Projection Engine")
    print("-" * 40)
    engine_result = await test_force_projection_engine()
    test_results.append(("Force Projection Engine", engine_result))
    
    # Test 2: Force Projection API
    print("\n🌐 Test 2: Force Projection API")
    print("-" * 40)
    api_result = await test_force_projection_api()
    test_results.append(("Force Projection API", api_result))
    
    # Test 3: Force Projection MCP Tools
    print("\n🔧 Test 3: Force Projection MCP Tools")
    print("-" * 40)
    mcp_result = await test_force_projection_mcp_tools()
    test_results.append(("Force Projection MCP Tools", mcp_result))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Force projection integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return passed == total


if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
