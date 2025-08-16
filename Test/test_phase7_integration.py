"""
Phase 7 Integration Test Suite
Comprehensive testing of integrated MCP tools, API endpoints, and orchestrator functionality
"""

import asyncio
import json
import pytest
import requests
import time
from typing import Dict, Any, List
from datetime import datetime, timedelta

# Test configuration
BASE_URL = "http://localhost:8003"
MCP_BASE_URL = "http://localhost:8000"

class TestPhase7Integration:
    """Comprehensive Phase 7 integration test suite"""
    
    def test_mcp_server_status(self):
        """Test MCP server status and accessibility"""
        # Test standalone MCP server health
        try:
            response = requests.get(f"{MCP_BASE_URL}/health", timeout=5)
            assert response.status_code == 200
            print("✅ Standalone MCP server is accessible")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Standalone MCP server not accessible: {e}")
            return False
        
        # Test MCP initialize
        try:
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "phase7_test", "version": "1.0.0"}
                }
            }
            response = requests.post(
                f"{MCP_BASE_URL}",
                json=init_request,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            assert response.status_code == 200
            data = response.json()
            assert "result" in data
            print("✅ MCP initialize successful")
        except Exception as e:
            print(f"❌ MCP initialize failed: {e}")
            return False
        
        # Test tools/list
        try:
            tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
            response = requests.post(
                f"{MCP_BASE_URL}",
                json=tools_request,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            assert response.status_code == 200
            data = response.json()
            assert "result" in data
            tools = data["result"].get("tools", [])
            print(f"✅ MCP tools available: {len(tools)} tools")
            return True
        except Exception as e:
            print(f"❌ MCP tools/list failed: {e}")
            return False
    
    def test_api_server_status(self):
        """Test API server status and endpoints"""
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            assert response.status_code == 200
            print("✅ API server is accessible")
            
            # Test MCP health endpoint
            response = requests.get(f"{BASE_URL}/mcp-health", timeout=5)
            assert response.status_code == 200
            print("✅ MCP health endpoint accessible")
            
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ API server not accessible: {e}")
            return False
    
    def test_phase6_advanced_forecasting_endpoints(self):
        """Test Phase 6 advanced forecasting endpoints"""
        try:
            # Test health endpoint
            response = requests.get(f"{BASE_URL}/api/v1/advanced-forecasting/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            print("✅ Phase 6 advanced forecasting health endpoint working")
            
            # Test ensemble forecast endpoint
            request_data = {
                "data_type": "time_series",
                "historical_data": {
                    "time_series": [100, 105, 110, 115, 120],
                    "timestamps": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"]
                },
                "forecast_horizon": 3,
                "confidence_level": 0.95
            }
            
            response = requests.post(
                f"{BASE_URL}/api/v1/advanced-forecasting/ensemble-forecast",
                json=request_data,
                timeout=30
            )
            assert response.status_code == 200
            data = response.json()
            assert "forecast_id" in data
            print("✅ Phase 6 ensemble forecast endpoint working")
            
            return True
        except Exception as e:
            print(f"❌ Phase 6 advanced forecasting endpoints failed: {e}")
            return False
    
    def test_phase6_reinforcement_learning_endpoints(self):
        """Test Phase 6 reinforcement learning endpoints"""
        try:
            # Test health endpoint
            response = requests.get(f"{BASE_URL}/api/v1/reinforcement-learning/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            print("✅ Phase 6 reinforcement learning health endpoint working")
            
            # Test RL agent training endpoint
            request_data = {
                "agent_type": "q_learning",
                "environment_config": {
                    "state_size": 10,
                    "action_size": 4
                },
                "training_parameters": {
                    "learning_rate": 0.1,
                    "episodes": 100
                },
                "reward_function": {
                    "type": "linear"
                },
                "state_space": {
                    "dimensions": 10
                },
                "action_space": {
                    "size": 4
                }
            }
            
            response = requests.post(
                f"{BASE_URL}/api/v1/reinforcement-learning/train-agent",
                json=request_data,
                timeout=30
            )
            assert response.status_code == 200
            data = response.json()
            assert "agent_id" in data
            print("✅ Phase 6 RL agent training endpoint working")
            
            return True
        except Exception as e:
            print(f"❌ Phase 6 reinforcement learning endpoints failed: {e}")
            return False
    
    def test_mcp_streamable_http_integration(self):
        """Test MCP streamable HTTP integration"""
        try:
            # Test streamable HTTP MCP client integration
            from mcp.client.streamable_http import streamablehttp_client
            from strands import Agent
            from strands.tools.mcp.mcp_client import MCPClient
            
            # Create streamable HTTP MCP client
            streamable_http_mcp_client = MCPClient(lambda: streamablehttp_client("http://localhost:8000/mcp"))
            
            # Test client connection
            with streamable_http_mcp_client:
                # Get the tools from the MCP server
                tools = streamable_http_mcp_client.list_tools_sync()
                assert len(tools) > 0
                print(f"✅ MCP streamable HTTP client connected with {len(tools)} tools")
                
                # Create an agent with these tools
                agent = Agent(tools=tools)
                print("✅ Agent created with MCP tools")
                
                return True
        except Exception as e:
            print(f"❌ MCP streamable HTTP integration failed: {e}")
            return False
    
    def test_orchestrator_integration(self):
        """Test orchestrator integration with Phase 6 components"""
        try:
            # Test that orchestrator has Phase 6 components
            response = requests.get(f"{BASE_URL}/api/v1/advanced-forecasting/health", timeout=5)
            assert response.status_code == 200
            
            response = requests.get(f"{BASE_URL}/api/v1/reinforcement-learning/health", timeout=5)
            assert response.status_code == 200
            
            print("✅ Orchestrator integration with Phase 6 components working")
            return True
        except Exception as e:
            print(f"❌ Orchestrator integration failed: {e}")
            return False
    
    def test_comprehensive_workflow(self):
        """Test comprehensive workflow from MCP to API to results"""
        try:
            # Step 1: Create ensemble forecast via API
            request_data = {
                "data_type": "time_series",
                "historical_data": {
                    "time_series": [100, 105, 110, 115, 120],
                    "timestamps": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"]
                },
                "forecast_horizon": 3,
                "confidence_level": 0.95
            }
            
            response = requests.post(
                f"{BASE_URL}/api/v1/advanced-forecasting/ensemble-forecast",
                json=request_data,
                timeout=30
            )
            assert response.status_code == 200
            forecast_data = response.json()
            forecast_id = forecast_data["forecast_id"]
            
            # Step 2: Use forecast results for RL decision
            rl_request_data = {
                "agent_type": "q_learning",
                "environment_config": {
                    "state_size": 10,
                    "action_size": 4
                },
                "training_parameters": {
                    "learning_rate": 0.1,
                    "episodes": 100
                },
                "reward_function": {
                    "type": "linear"
                },
                "state_space": {
                    "dimensions": 10
                },
                "action_space": {
                    "size": 4
                }
            }
            
            response = requests.post(
                f"{BASE_URL}/api/v1/reinforcement-learning/train-agent",
                json=rl_request_data,
                timeout=30
            )
            assert response.status_code == 200
            rl_data = response.json()
            agent_id = rl_data["agent_id"]
            
            print(f"✅ Comprehensive workflow completed: Forecast ID {forecast_id}, Agent ID {agent_id}")
            return True
        except Exception as e:
            print(f"❌ Comprehensive workflow failed: {e}")
            return False

def run_phase7_integration_tests():
    """Run all Phase 7 integration tests"""
    print("🚀 Starting Phase 7 Integration Tests")
    print("=" * 60)
    
    test_suite = TestPhase7Integration()
    test_results = {}
    
    # Test MCP server status
    print("\n1. Testing MCP Server Status...")
    test_results["mcp_server"] = test_suite.test_mcp_server_status()
    
    # Test API server status
    print("\n2. Testing API Server Status...")
    test_results["api_server"] = test_suite.test_api_server_status()
    
    # Test Phase 6 advanced forecasting endpoints
    print("\n3. Testing Phase 6 Advanced Forecasting Endpoints...")
    test_results["phase6_forecasting"] = test_suite.test_phase6_advanced_forecasting_endpoints()
    
    # Test Phase 6 reinforcement learning endpoints
    print("\n4. Testing Phase 6 Reinforcement Learning Endpoints...")
    test_results["phase6_rl"] = test_suite.test_phase6_reinforcement_learning_endpoints()
    
    # Test MCP streamable HTTP integration
    print("\n5. Testing MCP Streamable HTTP Integration...")
    test_results["mcp_streamable"] = test_suite.test_mcp_streamable_http_integration()
    
    # Test orchestrator integration
    print("\n6. Testing Orchestrator Integration...")
    test_results["orchestrator"] = test_suite.test_orchestrator_integration()
    
    # Test comprehensive workflow
    print("\n7. Testing Comprehensive Workflow...")
    test_results["workflow"] = test_suite.test_comprehensive_workflow()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Phase 7 Integration Test Results:")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Phase 7 integration tests passed!")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = run_phase7_integration_tests()
    exit(0 if success else 1)
