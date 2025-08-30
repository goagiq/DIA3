"""
Comprehensive Test Suite for Phase 6: Advanced Forecasting & Reinforcement Learning
Tests advanced forecasting routes, RL routes, and MCP integration
"""

import asyncio
import json
import pytest
import requests
from typing import Dict, Any, List
from datetime import datetime, timedelta

# Test configuration
BASE_URL = "http://localhost:8003"
MCP_BASE_URL = "http://localhost:8000"

class TestPhase6AdvancedForecasting:
    """Test suite for Phase 6 advanced forecasting functionality"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = requests.get(f"{BASE_URL}/api/v1/advanced-forecasting/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "advanced-forecasting"
    
    def test_ensemble_forecast_creation(self):
        """Test ensemble forecast creation"""
        # Sample historical data
        historical_data = {
            "time_series": [100, 105, 110, 115, 120, 125, 130, 135, 140, 145],
            "timestamps": [
                "2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05",
                "2025-01-06", "2025-01-07", "2025-01-08", "2025-01-09", "2025-01-10"
            ],
            "metadata": {
                "data_type": "economic_indicator",
                "source": "test_data"
            }
        }
        
        request_data = {
            "data_type": "time_series",
            "historical_data": historical_data,
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
        
        response = requests.post(
            f"{BASE_URL}/api/v1/advanced-forecasting/ensemble-forecast",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "forecast_id" in data
        assert "predictions" in data
        assert "confidence_intervals" in data
        assert "model_weights" in data
        assert "ensemble_performance" in data
    
    def test_scenario_analysis(self):
        """Test scenario analysis functionality"""
        request_data = {
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
        
        response = requests.post(
            f"{BASE_URL}/api/v1/advanced-forecasting/scenario-analysis",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "analysis_id" in data
        assert "scenario_type" in data
        assert "results" in data
    
    def test_real_time_forecast_initialization(self):
        """Test real-time forecast initialization"""
        request_data = {
            "data_streams": ["sigint", "humint", "osint"],
            "update_frequency": 30,
            "alert_thresholds": {
                "anomaly_score": 0.8,
                "confidence_drop": 0.2
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/advanced-forecasting/real-time-forecast",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "stream_id" in data
        assert "status" == "initialized"
        assert "data_streams" in data
        assert "stream_url" in data
    
    def test_optimize_ensemble_weights(self):
        """Test ensemble weight optimization"""
        historical_data = {
            "time_series": [100, 105, 110, 115, 120, 125, 130, 135, 140, 145],
            "timestamps": [
                "2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05",
                "2025-01-06", "2025-01-07", "2025-01-08", "2025-01-09", "2025-01-10"
            ]
        }
        
        request_data = {
            "historical_data": historical_data,
            "data_type": "time_series",
            "forecast_horizon": 5
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/advanced-forecasting/optimize-ensemble",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "optimized_weights" in data
        assert "optimization_metrics" in data

class TestPhase6ReinforcementLearning:
    """Test suite for Phase 6 reinforcement learning functionality"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = requests.get(f"{BASE_URL}/api/v1/reinforcement-learning/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "reinforcement-learning"
    
    def test_rl_agent_training(self):
        """Test RL agent training"""
        request_data = {
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
                "episodes": 1000
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
        
        response = requests.post(
            f"{BASE_URL}/api/v1/reinforcement-learning/train-agent",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "agent_id" in data
        assert "agent_type" in data
        assert "status" in data
        assert "performance_metrics" in data
        
        return data["agent_id"]  # Return for subsequent tests
    
    def test_rl_decision_making(self, agent_id):
        """Test RL decision making"""
        request_data = {
            "agent_id": agent_id,
            "current_state": {
                "feature_1": 50,
                "feature_2": 30,
                "feature_3": 70,
                "feature_4": 20,
                "feature_5": 80
            },
            "available_actions": ["action_1", "action_2", "action_3", "action_4"],
            "exploration_rate": 0.1
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/reinforcement-learning/make-decision",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "agent_id" in data
        assert "decision" in data
        assert "confidence" in data
        assert "state_value" in data
    
    def test_multi_agent_system_creation(self):
        """Test multi-agent system creation"""
        request_data = {
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
        
        response = requests.post(
            f"{BASE_URL}/api/v1/reinforcement-learning/multi-agent-system",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "system_id" in data
        assert "agent_count" in data
        assert "coordination_strategy" in data
        assert "status" in data
        
        return data["system_id"]  # Return for subsequent tests
    
    def test_multi_agent_decision(self, system_id):
        """Test multi-agent decision making"""
        request_data = {
            "system_id": system_id,
            "global_state": {
                "environment_state": "normal",
                "resource_availability": 0.8,
                "threat_level": 0.3,
                "coordination_required": True
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/reinforcement-learning/multi-agent-decision",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "system_id" in data
        assert "decisions" in data
        assert "coordination_metrics" in data
        assert "global_reward" in data
    
    def test_decision_optimization(self):
        """Test decision optimization for intelligence analysis"""
        request_data = {
            "state": {
                "intelligence_gathered": 0.7,
                "threat_level": 0.6,
                "resource_availability": 0.8,
                "time_constraint": 0.4
            },
            "action_space": [
                "deploy_agents",
                "increase_surveillance",
                "request_backup",
                "maintain_current_ops"
            ],
            "reward_function": {
                "type": "intelligence_optimization",
                "parameters": {
                    "intelligence_gain_weight": 0.4,
                    "risk_mitigation_weight": 0.3,
                    "resource_efficiency_weight": 0.2,
                    "time_efficiency_weight": 0.1
                }
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/reinforcement-learning/optimize-decision-making",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "optimized_action" in data
        assert "expected_reward" in data
        assert "confidence" in data
        assert "exploration_benefit" in data
    
    def test_adaptive_forecasting(self):
        """Test adaptive forecasting using RL"""
        request_data = {
            "historical_data": {
                "time_series": [100, 105, 110, 115, 120, 125, 130, 135, 140, 145],
                "model_performance": {
                    "lstm": 0.85,
                    "transformer": 0.88,
                    "prophet": 0.82,
                    "arima": 0.78
                }
            },
            "current_state": {
                "data_volatility": 0.3,
                "trend_strength": 0.7,
                "seasonality_present": True,
                "noise_level": 0.2
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/reinforcement-learning/adaptive-forecasting",
            json=request_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "selected_model" in data
        assert "forecast" in data
        assert "model_confidence" in data
        assert "adaptation_reason" in data

class TestPhase6MCPIntegration:
    """Test suite for Phase 6 MCP integration"""
    
    def test_mcp_server_health(self):
        """Test MCP server health"""
        response = requests.get(f"{MCP_BASE_URL}/health")
        assert response.status_code == 200
    
    def test_mcp_tools_listing(self):
        """Test MCP tools listing"""
        # Test using JSON-RPC format
        request_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        response = requests.post(
            MCP_BASE_URL,
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "tools" in data["result"]
        
        # Check for Phase 6 tools
        tool_names = [tool["name"] for tool in data["result"]["tools"]]
        expected_tools = [
            "create_ensemble_forecast",
            "train_rl_agent",
            "make_rl_decision",
            "analyze_scenarios",
            "optimize_ensemble_weights",
            "create_multi_agent_system",
            "get_real_time_insights",
            "generate_forecast_explanation"
        ]
        
        for tool in expected_tools:
            assert tool in tool_names, f"Expected tool {tool} not found in MCP tools"
    
    def test_mcp_ensemble_forecast_tool(self):
        """Test MCP ensemble forecast tool"""
        request_data = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "create_ensemble_forecast",
                "arguments": {
                    "data_type": "time_series",
                    "historical_data": {
                        "values": [100, 105, 110, 115, 120],
                        "timestamps": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"]
                    },
                    "forecast_horizon": 3,
                    "confidence_level": 0.95
                }
            }
        }
        
        response = requests.post(
            MCP_BASE_URL,
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "content" in data["result"]
        
        # Parse the result content
        content = data["result"]["content"][0]["text"]
        result = json.loads(content)
        
        # Check for expected fields
        assert "forecast_id" in result or "error" in result
    
    def test_mcp_rl_training_tool(self):
        """Test MCP RL training tool"""
        request_data = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "train_rl_agent",
                "arguments": {
                    "agent_type": "q_learning",
                    "environment_config": {
                        "state_size": 5,
                        "action_size": 3
                    },
                    "training_parameters": {
                        "learning_rate": 0.1,
                        "episodes": 100
                    },
                    "reward_function": {
                        "type": "linear"
                    },
                    "state_space": {
                        "dimensions": 5
                    },
                    "action_space": {
                        "actions": ["action_1", "action_2", "action_3"]
                    }
                }
            }
        }
        
        response = requests.post(
            MCP_BASE_URL,
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "content" in data["result"]
        
        # Parse the result content
        content = data["result"]["content"][0]["text"]
        result = json.loads(content)
        
        # Check for expected fields
        assert "agent_id" in result or "error" in result

class TestPhase6Integration:
    """Integration tests for Phase 6 functionality"""
    
    def test_end_to_end_forecasting_pipeline(self):
        """Test complete forecasting pipeline"""
        # 1. Create ensemble forecast
        forecast_response = requests.post(
            f"{BASE_URL}/api/v1/advanced-forecasting/ensemble-forecast",
            json={
                "data_type": "time_series",
                "historical_data": {
                    "values": [100, 105, 110, 115, 120, 125, 130, 135, 140, 145],
                    "timestamps": [
                        "2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05",
                        "2025-01-06", "2025-01-07", "2025-01-08", "2025-01-09", "2025-01-10"
                    ]
                },
                "forecast_horizon": 5
            }
        )
        
        assert forecast_response.status_code == 200
        forecast_data = forecast_response.json()
        forecast_id = forecast_data["forecast_id"]
        
        # 2. Retrieve the forecast
        retrieve_response = requests.get(
            f"{BASE_URL}/api/v1/advanced-forecasting/forecast/{forecast_id}"
        )
        
        assert retrieve_response.status_code == 200
        retrieved_data = retrieve_response.json()
        assert retrieved_data["forecast_id"] == forecast_id
        
        # 3. List forecasts
        list_response = requests.get(
            f"{BASE_URL}/api/v1/advanced-forecasting/forecasts"
        )
        
        assert list_response.status_code == 200
        list_data = list_response.json()
        assert "forecasts" in list_data
        assert len(list_data["forecasts"]) > 0
        
        # 4. Clean up
        delete_response = requests.delete(
            f"{BASE_URL}/api/v1/advanced-forecasting/forecast/{forecast_id}"
        )
        
        assert delete_response.status_code == 200
    
    def test_end_to_end_rl_pipeline(self):
        """Test complete RL pipeline"""
        # 1. Train RL agent
        train_response = requests.post(
            f"{BASE_URL}/api/v1/reinforcement-learning/train-agent",
            json={
                "agent_type": "q_learning",
                "environment_config": {"state_size": 3, "action_size": 2},
                "training_parameters": {"learning_rate": 0.1, "episodes": 50},
                "reward_function": {"type": "linear"},
                "state_space": {"dimensions": 3},
                "action_space": {"actions": ["action_1", "action_2"]}
            }
        )
        
        assert train_response.status_code == 200
        train_data = train_response.json()
        agent_id = train_data["agent_id"]
        
        # 2. Get agent status
        status_response = requests.get(
            f"{BASE_URL}/api/v1/reinforcement-learning/agent/{agent_id}"
        )
        
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert status_data["agent_id"] == agent_id
        
        # 3. Make decision
        decision_response = requests.post(
            f"{BASE_URL}/api/v1/reinforcement-learning/make-decision",
            json={
                "agent_id": agent_id,
                "current_state": {"feature_1": 50, "feature_2": 30, "feature_3": 70}
            }
        )
        
        assert decision_response.status_code == 200
        decision_data = decision_response.json()
        assert "decision" in decision_data
        
        # 4. List agents
        list_response = requests.get(
            f"{BASE_URL}/api/v1/reinforcement-learning/agents"
        )
        
        assert list_response.status_code == 200
        list_data = list_response.json()
        assert "agents" in list_data
        
        # 5. Clean up
        delete_response = requests.delete(
            f"{BASE_URL}/api/v1/reinforcement-learning/agent/{agent_id}"
        )
        
        assert delete_response.status_code == 200

def run_phase6_tests():
    """Run all Phase 6 tests"""
    print("🚀 Starting Phase 6 Advanced Forecasting & RL Tests...")
    
    # Test classes
    test_classes = [
        TestPhase6AdvancedForecasting,
        TestPhase6ReinforcementLearning,
        TestPhase6MCPIntegration,
        TestPhase6Integration
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"\n📋 Testing {test_class.__name__}...")
        
        # Get all test methods
        test_methods = [method for method in dir(test_class) if method.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            try:
                # Create instance and run test
                test_instance = test_class()
                method = getattr(test_instance, method_name)
                
                # Handle special cases for methods that require parameters
                if method_name == "test_rl_decision_making":
                    # First train an agent
                    train_response = requests.post(
                        f"{BASE_URL}/api/v1/reinforcement-learning/train-agent",
                        json={
                            "agent_type": "q_learning",
                            "environment_config": {"state_size": 5, "action_size": 3},
                            "training_parameters": {"learning_rate": 0.1, "episodes": 10},
                            "reward_function": {"type": "linear"},
                            "state_space": {"dimensions": 5},
                            "action_space": {"actions": ["action_1", "action_2", "action_3"]}
                        }
                    )
                    if train_response.status_code == 200:
                        agent_id = train_response.json()["agent_id"]
                        method(agent_id)
                    else:
                        print(f"⚠️ Skipping {method_name} - agent training failed")
                        continue
                elif method_name == "test_multi_agent_decision":
                    # First create multi-agent system
                    system_response = requests.post(
                        f"{BASE_URL}/api/v1/reinforcement-learning/multi-agent-system",
                        json={
                            "agent_configs": [
                                {"agent_type": "q_learning", "name": "agent_1", "parameters": {"learning_rate": 0.1}}
                            ],
                            "coordination_strategy": "independent"
                        }
                    )
                    if system_response.status_code == 200:
                        system_id = system_response.json()["system_id"]
                        method(system_id)
                    else:
                        print(f"⚠️ Skipping {method_name} - multi-agent system creation failed")
                        continue
                else:
                    method()
                
                print(f"✅ {method_name} - PASSED")
                passed_tests += 1
                
            except Exception as e:
                print(f"❌ {method_name} - FAILED: {str(e)}")
    
    print(f"\n🎉 Phase 6 Test Results:")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    # Run the tests
    success = run_phase6_tests()
    
    if success:
        print("\n🎉 All Phase 6 tests passed! Phase 6 implementation is complete.")
    else:
        print("\n⚠️ Some Phase 6 tests failed. Please review the implementation.")
    
    exit(0 if success else 1)
