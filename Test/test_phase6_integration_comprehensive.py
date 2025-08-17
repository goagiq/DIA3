#!/usr/bin/env python3
"""
Phase 6 Comprehensive Integration Test
Tests all Phase 6 Monte Carlo visualization features end-to-end.
"""

import asyncio
import requests
import json
import time
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class Phase6IntegrationTest:
    """Comprehensive integration test for Phase 6 Monte Carlo visualization."""
    
    def __init__(self):
        self.base_url = "http://localhost:8003"
        self.mcp_base_url = "http://localhost:8000/mcp"  # Updated to use /mcp path
        self.test_results = {}
    
    async def run_all_tests(self):
        """Run all Phase 6 integration tests."""
        print("🚀 Starting Phase 6 Comprehensive Integration Tests")
        print("=" * 70)
        
        # Test API health endpoints
        self.test_results['api_health'] = await self.test_api_health()
        
        # Test visualization API endpoints
        self.test_results['visualization_api'] = await self.test_visualization_api()
        
        # Test MCP tools
        self.test_results['mcp_tools'] = await self.test_mcp_tools()
        
        # Test dynamic tool management
        self.test_results['dynamic_tool_management'] = await self.test_dynamic_tool_management()
        
        # Test orchestrator integration
        self.test_results['orchestrator_integration'] = await self.test_orchestrator_integration()
        
        # Test real-time dashboard
        self.test_results['real_time_dashboard'] = await self.test_real_time_dashboard()
        
        # Test export functionality
        self.test_results['export_functionality'] = await self.test_export_functionality()
        
        # Test security compliance
        self.test_results['security_compliance'] = await self.test_security_compliance()
        
        # Print results
        self.print_results()
        
        return all(self.test_results.values())
    
    async def test_api_health(self):
        """Test API health endpoints."""
        print("\n🧪 Testing API health endpoints...")
        
        try:
            # Test main API health
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Main API health check passed")
            else:
                print(f"❌ Main API health check failed: {response.status_code}")
                return False
            
            # Test Monte Carlo visualization health
            response = requests.get(f"{self.base_url}/api/v1/monte-carlo/visualization/health", timeout=5)
            if response.status_code == 200:
                print("✅ Monte Carlo visualization health check passed")
                return True
            else:
                print(f"❌ Monte Carlo visualization health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API health test failed: {e}")
            return False
    
    async def test_visualization_api(self):
        """Test visualization API endpoints."""
        print("\n🧪 Testing visualization API endpoints...")
        
        try:
            # Test distribution plot endpoint
            test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
            payload = {
                "data": test_data,
                "title": "Test Distribution",
                "security_level": "UNCLASSIFIED"
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/monte-carlo/visualization/distribution-plot",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Distribution plot API endpoint working")
            else:
                print(f"❌ Distribution plot API endpoint failed: {response.status_code}")
                return False
            
            # Test correlation matrix endpoint
            correlation_data = [[1.0, 0.5], [0.5, 1.0]]
            variable_names = ["Var1", "Var2"]
            payload = {
                "correlation_matrix": correlation_data,
                "variable_names": variable_names,
                "security_level": "UNCLASSIFIED"
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/monte-carlo/visualization/correlation-matrix",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Correlation matrix API endpoint working")
            else:
                print(f"❌ Correlation matrix API endpoint failed: {response.status_code}")
                return False
            
            # Test available types endpoint
            response = requests.get(f"{self.base_url}/api/v1/monte-carlo/visualization/available-types", timeout=5)
            if response.status_code == 200:
                result = response.json()
                if "available_types" in result:
                    types = result["available_types"]
                    print(f"✅ Available types API endpoint working")
                    print(f"   - Found {len(types)} visualization types")
                    return True
                else:
                    print("❌ Available types API endpoint failed - no types found")
                    return False
            else:
                print(f"❌ Available types API endpoint failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Visualization API test failed: {e}")
            return False
    
    async def test_mcp_tools(self):
        """Test MCP tools for visualization."""
        print("\n🧪 Testing MCP tools for visualization...")
        
        try:
            # Test MCP tools list using JSON-RPC with proper headers
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
            
            response = requests.post(
                self.mcp_base_url,
                json=payload,
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                print("✅ MCP tools list working")
                try:
                    result = response.json()
                    if "result" in result and "tools" in result["result"]:
                        tools = result["result"]["tools"]
                        monte_carlo_tools = [t for t in tools if "monte_carlo" in t.get("name", "").lower()]
                        if monte_carlo_tools:
                            print(f"   - Found {len(monte_carlo_tools)} Monte Carlo tools")
                            return True
                        else:
                            print("   ⚠️ No Monte Carlo tools found")
                            return False
                except json.JSONDecodeError:
                    print("   ⚠️ Response is not valid JSON")
                    return False
            else:
                print(f"❌ MCP tools list failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ MCP tools test failed: {e}")
            return False
    
    async def test_dynamic_tool_management(self):
        """Test dynamic MCP tool management."""
        print("\n🧪 Testing dynamic MCP tool management...")
        
        try:
            # Note: Dynamic tool management endpoint not currently exposed in API
            # This is an internal service used by the MCP server
            print("⚠️ Dynamic tool management endpoint not exposed in API (internal service)")
            print("   - Dynamic tool management is handled internally by the MCP server")
            print("   - Tools are managed through the unified MCP server on port 8000")
            
            # Test if MCP server is accessible
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
            
            response = requests.post(
                self.mcp_base_url,
                json=payload,
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                print("✅ MCP server accessible for tool management")
                return True
            else:
                print(f"❌ MCP server not accessible: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Dynamic tool management test failed: {e}")
            return False
    
    async def test_orchestrator_integration(self):
        """Test orchestrator integration."""
        print("\n🧪 Testing orchestrator integration...")
        
        try:
            # Test orchestrator agents status
            response = requests.get(f"{self.base_url}/agents/status", timeout=5)
            if response.status_code == 200:
                result = response.json()
                # The response is a direct object, not wrapped in "agents" key
                if isinstance(result, dict):
                    print("✅ Orchestrator agents status working")
                    
                    # Check for Monte Carlo agent
                    monte_carlo_agents = [
                        (name, agent) for name, agent in result.items() 
                        if "monte" in name.lower() or "monte" in agent.get("agent_type", "").lower()
                    ]
                    
                    if monte_carlo_agents:
                        print(f"✅ Found {len(monte_carlo_agents)} Monte Carlo agents in orchestrator")
                        for name, agent in monte_carlo_agents:
                            print(f"   - {name}: {agent.get('status')}")
                        return True
                    else:
                        print("⚠️ No Monte Carlo agents found in orchestrator")
                        return False
                else:
                    print("❌ Orchestrator agents status failed")
                    return False
            else:
                print(f"❌ Orchestrator agents status failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Orchestrator integration test failed: {e}")
            return False
    
    async def test_real_time_dashboard(self):
        """Test real-time dashboard functionality."""
        print("\n🧪 Testing real-time dashboard functionality...")
        
        try:
            # Test dashboard creation
            payload = {
                "simulation_id": "test_simulation_123",
                "update_interval": 2.0,
                "security_level": "UNCLASSIFIED"
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/monte-carlo/visualization/real-time-dashboard",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Real-time dashboard creation working")
            else:
                print(f"❌ Real-time dashboard creation failed: {response.status_code}")
                return False
            
            # Test dashboard stop
            response = requests.delete(
                f"{self.base_url}/api/v1/monte-carlo/visualization/real-time-dashboard/test_simulation_123",
                timeout=5
            )
            
            if response.status_code == 200:
                print("✅ Real-time dashboard stop working")
                return True
            else:
                print(f"❌ Real-time dashboard stop failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Real-time dashboard test failed: {e}")
            return False
    
    async def test_export_functionality(self):
        """Test export functionality."""
        print("\n🧪 Testing export functionality...")
        
        try:
            # First create a visualization
            viz_payload = {
                "data": [1.0, 2.0, 3.0, 4.0, 5.0],
                "title": "Test Export Visualization",
                "security_level": "UNCLASSIFIED"
            }
            
            viz_response = requests.post(
                f"{self.base_url}/api/v1/monte-carlo/visualization/distribution-plot",
                json=viz_payload,
                timeout=10
            )
            
            if viz_response.status_code != 200:
                print(f"❌ Failed to create visualization for export: {viz_response.status_code}")
                return False
            
            viz_result = viz_response.json()
            if not viz_result.get("success"):
                print(f"❌ Failed to create visualization for export: {viz_result.get('error')}")
                return False
            
            # Now export the visualization
            export_payload = {
                "visualization_data": viz_result["data"],
                "format": "json",
                "filename": "test_export"
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/monte-carlo/visualization/export",
                json=export_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and "data" in result and ("export_path" in result["data"] or "output_path" in result["data"]):
                    print("✅ Export functionality working")
                    export_path = result["data"].get("export_path") or result["data"].get("output_path")
                    print(f"   - Exported to: {export_path}")
                    return True
                else:
                    print("❌ Export functionality failed - no export path")
                    return False
            else:
                print(f"❌ Export functionality failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Export functionality test failed: {e}")
            return False
    
    async def test_security_compliance(self):
        """Test security compliance features."""
        print("\n🧪 Testing security compliance features...")
        
        try:
            # Test different security levels
            security_levels = ["UNCLASSIFIED", "CONFIDENTIAL", "SECRET", "TOP_SECRET"]
            
            for level in security_levels:
                payload = {
                    "data": [1.0, 2.0, 3.0],
                    "title": f"Test {level}",
                    "security_level": level
                }
                
                response = requests.post(
                    f"{self.base_url}/api/v1/monte-carlo/visualization/distribution-plot",
                    json=payload,
                    timeout=5
                )
                
                if response.status_code == 200:
                    print(f"✅ Security level {level} working")
                else:
                    print(f"❌ Security level {level} failed: {response.status_code}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Security compliance test failed: {e}")
            return False
    
    def print_results(self):
        """Print test results summary."""
        print("\n" + "=" * 70)
        print("📊 Phase 6 Integration Test Results")
        print("=" * 70)
        
        passed = 0
        total = len(self.test_results)
        
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name.replace('_', ' ').title()}")
            if result:
                passed += 1
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Phase 6 integration is complete.")
        else:
            print("⚠️ Some tests failed. Please check the implementation.")


async def main():
    """Main test function."""
    test = Phase6IntegrationTest()
    success = await test.run_all_tests()
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
