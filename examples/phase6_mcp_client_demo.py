"""
Phase 6 MCP Client Demo
Demonstrates streamable HTTP integration with enhanced MCP tools
"""

import asyncio
import json
import requests
from typing import Dict, Any, List
from datetime import datetime

# MCP Server configuration
MCP_BASE_URL = "http://localhost:8000"

class Phase6MCPClient:
    """Enhanced MCP client for Phase 6 tools with streamable HTTP support"""
    
    def __init__(self, base_url: str = MCP_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
    
    def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool using JSON-RPC format"""
        request_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        try:
            response = self.session.post(self.base_url, json=request_data)
            response.raise_for_status()
            
            data = response.json()
            if "result" in data and "content" in data["result"]:
                # Parse the result content
                content = data["result"]["content"][0]["text"]
                return json.loads(content)
            else:
                return {"error": "Invalid response format"}
                
        except Exception as e:
            return {"error": f"Tool call failed: {str(e)}"}
    
    def list_tools(self) -> List[str]:
        """List available MCP tools"""
        request_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        try:
            response = self.session.post(self.base_url, json=request_data)
            response.raise_for_status()
            
            data = response.json()
            if "result" in data and "tools" in data["result"]:
                return [tool["name"] for tool in data["result"]["tools"]]
            else:
                return []
                
        except Exception as e:
            print(f"Error listing tools: {e}")
            return []
    
    def test_ensemble_forecast(self):
        """Test ensemble forecast creation"""
        print("🔮 Testing Ensemble Forecast Creation...")
        
        arguments = {
            "data_type": "time_series",
            "historical_data": {
                "time_series": [100, 105, 110, 115, 120, 125, 130, 135, 140, 145],
                "timestamps": [
                    "2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05",
                    "2025-01-06", "2025-01-07", "2025-01-08", "2025-01-09", "2025-01-10"
                ],
                "metadata": {
                    "data_type": "economic_indicator",
                    "source": "demo_data"
                }
            },
            "forecast_horizon": 5,
            "confidence_level": 0.95,
            "ensemble_weights": {
                "lstm": 0.3,
                "transformer": 0.3,
                "prophet": 0.2,
                "arima": 0.1,
                "exponential_smoothing": 0.1
            }
        }
        
        result = self.call_mcp_tool("create_ensemble_forecast", arguments)
        
        if "error" not in result:
            print("✅ Ensemble forecast created successfully!")
            print(f"   Forecast ID: {result.get('forecast_id', 'N/A')}")
            print(f"   Models used: {list(result.get('model_weights', {}).keys())}")
            print(f"   Performance: {result.get('ensemble_performance', {})}")
        else:
            print(f"❌ Ensemble forecast failed: {result['error']}")
        
        return result
    
    def test_rl_agent_training(self):
        """Test RL agent training"""
        print("\n🤖 Testing RL Agent Training...")
        
        arguments = {
            "agent_type": "q_learning",
            "environment_config": {
                "state_size": 10,
                "action_size": 4,
                "reward_structure": "linear"
            },
            "training_parameters": {
                "learning_rate": 0.1,
                "discount_factor": 0.9,
                "epsilon": 0.1,
                "episodes": 100
            },
            "reward_function": {
                "type": "linear",
                "parameters": {
                    "positive_reward": 1.0,
                    "negative_reward": -1.0,
                    "neutral_reward": 0.0
                }
            },
            "state_space": {
                "dimensions": 10,
                "bounds": [0, 100]
            },
            "action_space": {
                "actions": ["action_1", "action_2", "action_3", "action_4"],
                "type": "discrete"
            }
        }
        
        result = self.call_mcp_tool("train_rl_agent", arguments)
        
        if "error" not in result:
            print("✅ RL agent training started successfully!")
            print(f"   Agent ID: {result.get('agent_id', 'N/A')}")
            print(f"   Agent Type: {result.get('agent_type', 'N/A')}")
            print(f"   Status: {result.get('status', 'N/A')}")
        else:
            print(f"❌ RL agent training failed: {result['error']}")
        
        return result
    
    def test_scenario_analysis(self):
        """Test scenario analysis"""
        print("\n📊 Testing Scenario Analysis...")
        
        arguments = {
            "scenario_type": "war_capability",
            "base_parameters": {
                "military_spending": 50,
                "troop_mobilization": 60,
                "weapons_modernization": 70,
                "alliance_strength": 80,
                "economic_sanctions": 30
            },
            "alternative_scenarios": [
                {
                    "name": "high_intensity",
                    "military_spending": 80,
                    "troop_mobilization": 90,
                    "weapons_modernization": 95,
                    "alliance_strength": 95,
                    "economic_sanctions": 70
                },
                {
                    "name": "low_intensity",
                    "military_spending": 20,
                    "troop_mobilization": 30,
                    "weapons_modernization": 40,
                    "alliance_strength": 60,
                    "economic_sanctions": 10
                }
            ],
            "sensitivity_analysis": True,
            "monte_carlo_simulations": 100
        }
        
        result = self.call_mcp_tool("analyze_scenarios", arguments)
        
        if "error" not in result:
            print("✅ Scenario analysis completed successfully!")
            print(f"   Analysis ID: {result.get('analysis_id', 'N/A')}")
            print(f"   Scenario Type: {result.get('scenario_type', 'N/A')}")
            print(f"   Results available: {bool(result.get('results', {}))}")
        else:
            print(f"❌ Scenario analysis failed: {result['error']}")
        
        return result
    
    def test_multi_agent_system(self):
        """Test multi-agent system creation"""
        print("\n👥 Testing Multi-Agent System Creation...")
        
        arguments = {
            "agent_configs": [
                {
                    "agent_type": "q_learning",
                    "name": "agent_1",
                    "parameters": {"learning_rate": 0.1}
                },
                {
                    "agent_type": "deep_q_network",
                    "name": "agent_2",
                    "parameters": {"learning_rate": 0.001}
                },
                {
                    "agent_type": "policy_gradient",
                    "name": "agent_3",
                    "parameters": {"learning_rate": 0.01}
                }
            ],
            "coordination_strategy": "hierarchical",
            "communication_protocol": {
                "type": "message_passing",
                "frequency": "episode_end"
            }
        }
        
        result = self.call_mcp_tool("create_multi_agent_system", arguments)
        
        if "error" not in result:
            print("✅ Multi-agent system created successfully!")
            print(f"   System ID: {result.get('system_id', 'N/A')}")
            print(f"   Agent Count: {result.get('agent_count', 'N/A')}")
            print(f"   Coordination Strategy: {result.get('coordination_strategy', 'N/A')}")
        else:
            print(f"❌ Multi-agent system creation failed: {result['error']}")
        
        return result
    
    def test_ensemble_optimization(self):
        """Test ensemble weight optimization"""
        print("\n⚙️ Testing Ensemble Weight Optimization...")
        
        arguments = {
            "historical_data": {
                "time_series": [100, 105, 110, 115, 120, 125, 130, 135, 140, 145],
                "timestamps": [
                    "2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05",
                    "2025-01-06", "2025-01-07", "2025-01-08", "2025-01-09", "2025-01-10"
                ]
            },
            "data_type": "time_series",
            "forecast_horizon": 5
        }
        
        result = self.call_mcp_tool("optimize_ensemble_weights", arguments)
        
        if "error" not in result:
            print("✅ Ensemble optimization completed successfully!")
            print(f"   Optimized Weights: {result.get('optimized_weights', {})}")
            print(f"   Optimization Metrics: {result.get('optimization_metrics', {})}")
        else:
            print(f"❌ Ensemble optimization failed: {result['error']}")
        
        return result
    
    def test_real_time_insights(self):
        """Test real-time insights"""
        print("\n📡 Testing Real-Time Insights...")
        
        arguments = {
            "feeds": ["sigint", "humint", "osint"],
            "forecast_context": {
                "current_forecast": "active",
                "confidence_level": 0.85
            }
        }
        
        result = self.call_mcp_tool("get_real_time_insights", arguments)
        
        if "error" not in result:
            print("✅ Real-time insights retrieved successfully!")
            print(f"   Feeds Processed: {result.get('feeds_processed', [])}")
            print(f"   Insights Available: {bool(result.get('insights', {}))}")
        else:
            print(f"❌ Real-time insights failed: {result['error']}")
        
        return result
    
    def run_comprehensive_demo(self):
        """Run comprehensive Phase 6 MCP demo"""
        print("🚀 Phase 6 MCP Client Demo")
        print("=" * 50)
        
        # Check MCP server health
        try:
            health_response = requests.get(f"{self.base_url}/health")
            if health_response.status_code == 200:
                print("✅ MCP server is healthy")
            else:
                print("❌ MCP server health check failed")
                return
        except Exception as e:
            print(f"❌ Cannot connect to MCP server: {e}")
            return
        
        # List available tools
        print(f"\n📋 Available MCP Tools:")
        tools = self.list_tools()
        for tool in tools:
            print(f"   - {tool}")
        
        # Run individual tests
        results = {}
        
        results["ensemble_forecast"] = self.test_ensemble_forecast()
        results["rl_training"] = self.test_rl_agent_training()
        results["scenario_analysis"] = self.test_scenario_analysis()
        results["multi_agent"] = self.test_multi_agent_system()
        results["ensemble_optimization"] = self.test_ensemble_optimization()
        results["real_time_insights"] = self.test_real_time_insights()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Demo Summary:")
        
        successful_tests = 0
        total_tests = len(results)
        
        for test_name, result in results.items():
            if "error" not in result:
                successful_tests += 1
                print(f"   ✅ {test_name}: SUCCESS")
            else:
                print(f"   ❌ {test_name}: FAILED - {result['error']}")
        
        print(f"\n🎉 Success Rate: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")
        
        if successful_tests == total_tests:
            print("🎉 All Phase 6 MCP tools are working correctly!")
        else:
            print("⚠️ Some tools need attention. Check server logs for details.")

def main():
    """Main function to run the Phase 6 MCP client demo"""
    client = Phase6MCPClient()
    client.run_comprehensive_demo()

if __name__ == "__main__":
    main()
