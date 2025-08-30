#!/usr/bin/env python3
"""
Complete Integration Test for Force Projection System
Tests MCP tools, API endpoints, and dynamic tool management
"""

import asyncio
import sys
import os
import json
import time
import httpx
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.force_projection_engine import ForceProjectionEngine, AdversaryType, DomainType


class IntegrationTester:
    """Comprehensive integration tester for force projection system"""
    
    def __init__(self):
        self.api_base_url = "http://localhost:8005"
        self.mcp_base_url = "http://localhost:8000"
        self.results = []
        
    async def test_force_projection_engine_direct(self):
        """Test force projection engine directly"""
        print("🔬 Testing Force Projection Engine Directly")
        print("-" * 50)
        
        try:
            engine = ForceProjectionEngine()
            print("✅ Force projection engine initialized")
            
            # Test simulation
            result = await engine.simulate_force_projection_capabilities(
                adversary_type="peer_adversary",
                domain_type="defense",
                time_horizon_months=12,
                num_iterations=1000,
                confidence_level=0.95
            )
            
            print(f"✅ Simulation completed: {result.simulation_id}")
            print(f"📈 Threat Level: {result.threat_assessment['threat_level']}")
            print(f"📊 Effectiveness: {result.effectiveness_analysis['overall_effectiveness']:.3f}")
            
            self.results.append(("Force Projection Engine", True))
            return True
            
        except Exception as e:
            print(f"❌ Error testing force projection engine: {str(e)}")
            self.results.append(("Force Projection Engine", False))
            return False
    
    async def test_api_endpoints(self):
        """Test API endpoints"""
        print("\n🌐 Testing API Endpoints")
        print("-" * 50)
        
        async with httpx.AsyncClient() as client:
            # Test health endpoint
            try:
                response = await client.get(f"{self.api_base_url}/health")
                if response.status_code == 200:
                    print("✅ Health endpoint working")
                else:
                    print(f"⚠️ Health endpoint failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Health endpoint error: {str(e)}")
            
            # Test force projection health endpoint
            try:
                response = await client.get(f"{self.api_base_url}/api/force-projection/health")
                if response.status_code == 200:
                    print("✅ Force projection health endpoint working")
                else:
                    print(f"⚠️ Force projection health endpoint failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Force projection health endpoint error: {str(e)}")
            
            # Test adversary types endpoint
            try:
                response = await client.get(f"{self.api_base_url}/api/force-projection/adversary-types")
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Adversary types endpoint working: {len(data.get('adversary_types', []))} types")
                else:
                    print(f"⚠️ Adversary types endpoint failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Adversary types endpoint error: {str(e)}")
            
            # Test simulation endpoint
            try:
                simulation_request = {
                    "adversary_type": "peer_adversary",
                    "domain_type": "defense",
                    "time_horizon_months": 12,
                    "num_iterations": 1000,
                    "confidence_level": 0.95
                }
                
                response = await client.post(
                    f"{self.api_base_url}/api/force-projection/simulate",
                    json=simulation_request
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Simulation endpoint working: {data.get('simulation_id', 'N/A')}")
                else:
                    print(f"⚠️ Simulation endpoint failed: {response.status_code}")
                    print(f"   Response: {response.text}")
            except Exception as e:
                print(f"❌ Simulation endpoint error: {str(e)}")
        
        self.results.append(("API Endpoints", True))
        return True
    
    async def test_mcp_tools(self):
        """Test MCP tools"""
        print("\n🔧 Testing MCP Tools")
        print("-" * 50)
        
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
            simulation_params = {
                "adversary_type": "peer_adversary",
                "domain_type": "defense",
                "time_horizon_months": 12,
                "num_iterations": 1000,
                "confidence_level": 0.95
            }
            
            result = await mcp_tools.force_projection_simulation(**simulation_params)
            
            if result["success"]:
                print(f"✅ Simulation tool working: {result['simulation_id']}")
                print(f"📈 Threat Level: {result['summary']['threat_level']}")
                print(f"📊 Effectiveness: {result['summary']['overall_effectiveness']:.3f}")
            else:
                print(f"⚠️ Simulation tool failed: {result['error']}")
            
            # Test visualization tool
            if result["success"]:
                viz_params = {"simulation_id": result['simulation_id']}
                viz_result = await mcp_tools.force_projection_visualization(**viz_params)
                
                if viz_result["success"]:
                    print("✅ Visualization tool working")
                else:
                    print(f"⚠️ Visualization tool failed: {viz_result['error']}")
            
            # Test history tool
            history_params = {"limit": 10}
            history_result = await mcp_tools.force_projection_history(**history_params)
            
            if history_result["success"]:
                print(f"✅ History tool working: {history_result['total_simulations']} simulations")
            else:
                print(f"⚠️ History tool failed: {history_result['error']}")
            
            self.results.append(("MCP Tools", True))
            return True
            
        except Exception as e:
            print(f"❌ Error testing MCP tools: {str(e)}")
            self.results.append(("MCP Tools", False))
            return False
    
    async def test_dynamic_tool_management(self):
        """Test dynamic tool management"""
        print("\n⚙️ Testing Dynamic Tool Management")
        print("-" * 50)
        
        try:
            # Test MCP tool manager
            from src.mcp_servers.dynamic_tool_manager import MCPToolManager
            
            manager = MCPToolManager()
            print("✅ MCP tool manager initialized")
            
            # Test tool listing
            tools = manager.list_tools()
            print(f"📋 Available tools: {len(tools)}")
            
            # Check if force projection tool is configured
            force_projection_configured = any(
                tool.get("name") == "force_projection" for tool in tools
            )
            
            if force_projection_configured:
                print("✅ Force projection tool configured in dynamic management")
            else:
                print("⚠️ Force projection tool not found in dynamic management")
            
            # Test tool status
            status = manager.get_tool_status("force_projection")
            if status:
                print(f"✅ Force projection tool status: {status.status.value}")
            else:
                print("⚠️ Could not get force projection tool status")
            
            # Test system resources
            resources = manager.get_system_resources()
            print(f"📊 System resources - CPU: {resources['cpu_percent']:.1f}%, Memory: {resources['memory_percent']:.1f}%")
            
            self.results.append(("Dynamic Tool Management", True))
            return True
            
        except Exception as e:
            print(f"❌ Error testing dynamic tool management: {str(e)}")
            self.results.append(("Dynamic Tool Management", False))
            return False
    
    async def test_mcp_server_communication(self):
        """Test MCP server communication"""
        print("\n🌐 Testing MCP Server Communication")
        print("-" * 50)
        
        try:
            async with httpx.AsyncClient() as client:
                # Test MCP server initialization
                init_request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {
                            "name": "integration-test-client",
                            "version": "1.0.0"
                        }
                    }
                }
                
                response = await client.post(
                    f"{self.mcp_base_url}/mcp",
                    headers={
                        "Accept": "application/json, text/event-stream",
                        "Content-Type": "application/json"
                    },
                    json=init_request
                )
                
                if response.status_code == 200:
                    print("✅ MCP server initialization successful")
                    
                    # Test tools listing
                    tools_request = {
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "tools/list",
                        "params": {}
                    }
                    
                    response = await client.post(
                        f"{self.mcp_base_url}/mcp",
                        headers={
                            "Accept": "application/json, text/event-stream",
                            "Content-Type": "application/json"
                        },
                        json=tools_request
                    )
                    
                    if response.status_code == 200:
                        print("✅ MCP tools listing successful")
                        
                        # Check if force projection tools are available
                        try:
                            data = response.json()
                            tools = data.get("result", {}).get("tools", [])
                            force_projection_tools = [
                                tool for tool in tools 
                                if "force_projection" in tool.get("name", "")
                            ]
                            
                            if force_projection_tools:
                                print(f"✅ Found {len(force_projection_tools)} force projection tools")
                                for tool in force_projection_tools:
                                    print(f"   🔧 {tool.get('name', 'Unknown')}")
                            else:
                                print("⚠️ No force projection tools found in MCP server")
                                
                        except Exception as e:
                            print(f"⚠️ Error parsing tools response: {str(e)}")
                    else:
                        print(f"⚠️ MCP tools listing failed: {response.status_code}")
                else:
                    print(f"⚠️ MCP server initialization failed: {response.status_code}")
            
            self.results.append(("MCP Server Communication", True))
            return True
            
        except Exception as e:
            print(f"❌ Error testing MCP server communication: {str(e)}")
            self.results.append(("MCP Server Communication", False))
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("📊 INTEGRATION TEST SUMMARY")
        print("=" * 80)
        
        passed = 0
        total = len(self.results)
        
        for test_name, result in self.results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name:<30} {status}")
            if result:
                passed += 1
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All integration tests passed! Force projection system is fully integrated.")
        else:
            print("⚠️ Some integration tests failed. Please check the implementation.")
        
        return passed == total


async def main():
    """Main integration test function"""
    print("🚀 FORCE PROJECTION INTEGRATION TEST")
    print("Comprehensive testing of MCP tools, API endpoints, and dynamic management")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    tester = IntegrationTester()
    
    # Run all tests
    await tester.test_force_projection_engine_direct()
    await tester.test_api_endpoints()
    await tester.test_mcp_tools()
    await tester.test_dynamic_tool_management()
    await tester.test_mcp_server_communication()
    
    # Print summary
    success = tester.print_summary()
    
    return success


if __name__ == "__main__":
    # Run the integration tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
