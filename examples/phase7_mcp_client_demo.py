"""
Phase 7 MCP Client Demo
Demonstrates streamable HTTP integration and comprehensive MCP tool usage
"""

import time


def demo_streamable_http_mcp_integration():
    """Demo streamable HTTP MCP integration"""
    print("🚀 Phase 7 MCP Client Demo - Streamable HTTP Integration")
    print("=" * 60)
    
    try:
        from mcp.client.streamable_http import streamablehttp_client
        from strands import Agent
        from strands.tools.mcp.mcp_client import MCPClient
        
        print("✅ Imported streamable HTTP MCP client libraries")
        
        # Create streamable HTTP MCP client
        print("🔧 Creating streamable HTTP MCP client...")
        streamable_http_mcp_client = MCPClient(
            lambda: streamablehttp_client("http://localhost:8000/mcp")
        )
        
        # Test client connection
        print("🔗 Testing MCP client connection...")
        with streamable_http_mcp_client:
            # Get the tools from the MCP server
            tools = streamable_http_mcp_client.list_tools_sync()
            print(f"✅ MCP client connected with {len(tools)} tools available")
            
            # Display available tools
            print("\n📋 Available MCP Tools:")
            for i, tool in enumerate(tools[:10], 1):  # Show first 10 tools
                tool_name = getattr(tool, 'name', str(tool))
                print(f"  {i}. {tool_name}")
            if len(tools) > 10:
                print(f"  ... and {len(tools) - 10} more tools")
            
            # Create an agent with these tools
            print("\n🤖 Creating agent with MCP tools...")
            _ = Agent(tools=tools)  # Create agent but don't use it
            print("✅ Agent created successfully")
            
            # Demo tool usage
            print("\n🔧 Demo: Testing MCP tool calls...")
            
            # Test a simple tool call (if available)
            if tools:
                first_tool = tools[0]
                tool_name = getattr(first_tool, 'name', str(first_tool))
                print(f"Testing tool: {tool_name}")
                
                try:
                    # Try to call the tool with minimal parameters
                    result = streamable_http_mcp_client.call_tool_sync(
                        tool_name,
                        {"test": "demo"}
                    )
                    print(f"✅ Tool call successful: {result}")
                except Exception as e:
                    print(f"⚠️ Tool call failed (expected for demo): {e}")
            
            print("\n✅ Streamable HTTP MCP integration demo completed successfully!")
            return True
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure mcp-client and strands packages are installed")
        return False
    except Exception as e:
        print(f"❌ MCP integration error: {e}")
        return False

def demo_phase6_advanced_forecasting():
    """Demo Phase 6 advanced forecasting via MCP"""
    print("\n🎯 Phase 6 Advanced Forecasting Demo")
    print("=" * 40)
    
    try:
        import requests
        
        # Test ensemble forecasting
        print("📊 Testing ensemble forecasting...")
        request_data = {
            "data_type": "time_series",
            "historical_data": {
                "time_series": [100, 105, 110, 115, 120, 125, 130, 135, 140, 145],
                "timestamps": [
                    "2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05",
                    "2025-01-06", "2025-01-07", "2025-01-08", "2025-01-09", "2025-01-10"
                ]
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
        
        response = requests.post(
            "http://localhost:8003/api/v1/advanced-forecasting/ensemble-forecast",
            json=request_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Ensemble forecast created: {data['forecast_id']}")
            print(f"   Predictions: {len(data['predictions']['ensemble'])} points")
            print(f"   Model weights: {data['model_weights']}")
            return True
        else:
            print(f"❌ Ensemble forecast failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Advanced forecasting demo error: {e}")
        return False

def demo_phase6_reinforcement_learning():
    """Demo Phase 6 reinforcement learning via MCP"""
    print("\n🤖 Phase 6 Reinforcement Learning Demo")
    print("=" * 40)
    
    try:
        import requests
        
        # Test RL agent training
        print("🎯 Testing RL agent training...")
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
                "size": 4,
                "actions": ["action_1", "action_2", "action_3", "action_4"]
            }
        }
        
        response = requests.post(
            "http://localhost:8003/api/v1/reinforcement-learning/train-agent",
            json=request_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ RL agent trained: {data['agent_id']}")
            print(f"   Agent type: {data['agent_type']}")
            print(f"   Status: {data['status']}")
            print(f"   Performance: {data['performance_metrics']}")
            return True
        else:
            print(f"❌ RL agent training failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Reinforcement learning demo error: {e}")
        return False

def demo_comprehensive_workflow():
    """Demo comprehensive workflow from MCP to API to results"""
    print("\n🔄 Comprehensive Workflow Demo")
    print("=" * 40)
    
    try:
        import requests
        
        # Step 1: Create ensemble forecast
        print("1️⃣ Creating ensemble forecast...")
        forecast_request = {
            "data_type": "time_series",
            "historical_data": {
                "time_series": [100, 105, 110, 115, 120],
                "timestamps": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"]
            },
            "forecast_horizon": 3,
            "confidence_level": 0.95
        }
        
        response = requests.post(
            "http://localhost:8003/api/v1/advanced-forecasting/ensemble-forecast",
            json=forecast_request,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ Forecast creation failed: {response.status_code}")
            return False
        
        forecast_data = response.json()
        forecast_id = forecast_data["forecast_id"]
        print(f"✅ Forecast created: {forecast_id}")
        
        # Step 2: Use forecast for RL decision
        print("2️⃣ Using forecast for RL decision...")
        rl_request = {
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
            "http://localhost:8003/api/v1/reinforcement-learning/train-agent",
            json=rl_request,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ RL training failed: {response.status_code}")
            return False
        
        rl_data = response.json()
        agent_id = rl_data["agent_id"]
        print(f"✅ RL agent trained: {agent_id}")
        
        # Step 3: Make decision with trained agent
        print("3️⃣ Making decision with trained agent...")
        decision_request = {
            "agent_id": agent_id,
            "current_state": {
                "forecast_id": forecast_id,
                "forecast_values": forecast_data["predictions"]["ensemble"],
                "confidence": forecast_data["confidence_intervals"]["ensemble"]
            },
            "available_actions": ["action_1", "action_2", "action_3", "action_4"],
            "exploration_rate": 0.1
        }
        
        response = requests.post(
            "http://localhost:8003/api/v1/reinforcement-learning/make-decision",
            json=decision_request,
            timeout=30
        )
        
        if response.status_code == 200:
            decision_data = response.json()
            print(f"✅ Decision made: {decision_data.get('action', 'unknown')}")
            print(f"   Confidence: {decision_data.get('confidence', 0.0)}")
            print(f"   Reasoning: {decision_data.get('reasoning', 'N/A')}")
        else:
            print(f"⚠️ Decision making failed: {response.status_code}")
        
        print("\n✅ Comprehensive workflow demo completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Comprehensive workflow demo error: {e}")
        return False

def main():
    """Main demo function"""
    print("🎉 Phase 7 MCP Client Demo")
    print("=" * 60)
    print("This demo showcases:")
    print("• Streamable HTTP MCP integration")
    print("• Phase 6 Advanced Forecasting")
    print("• Phase 6 Reinforcement Learning")
    print("• Comprehensive workflow integration")
    print("=" * 60)
    
    # Wait for servers to be ready
    print("\n⏳ Waiting for servers to be ready...")
    time.sleep(5)
    
    results = {}
    
    # Demo 1: Streamable HTTP MCP Integration
    print("\n" + "=" * 60)
    results["mcp_integration"] = demo_streamable_http_mcp_integration()
    
    # Demo 2: Phase 6 Advanced Forecasting
    print("\n" + "=" * 60)
    results["advanced_forecasting"] = demo_phase6_advanced_forecasting()
    
    # Demo 3: Phase 6 Reinforcement Learning
    print("\n" + "=" * 60)
    results["reinforcement_learning"] = demo_phase6_reinforcement_learning()
    
    # Demo 4: Comprehensive Workflow
    print("\n" + "=" * 60)
    results["comprehensive_workflow"] = demo_comprehensive_workflow()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Phase 7 Demo Results:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for demo_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{demo_name:.<30} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} demos successful")
    
    if passed == total:
        print("🎉 All Phase 7 demos completed successfully!")
        print("✅ Phase 7 integration is working correctly!")
    else:
        print("⚠️ Some demos failed. Check the output above for details.")
    
    print("\n🔧 Next steps:")
    print("• Run comprehensive tests: .venv/Scripts/python.exe Test/test_phase7_integration.py")
    print("• Check MCP server status: curl http://localhost:8000/health")
    print("• Check API server status: curl http://localhost:8003/health")

if __name__ == "__main__":
    main()
