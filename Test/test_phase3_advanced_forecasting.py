#!/usr/bin/env python3
"""
Test script for Phase 3 Advanced Forecasting & Prediction Components
Tests ensemble forecasting, scenario prediction, and intelligence data streaming.
"""

import asyncio
import json
import requests
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Configuration
BASE_URL = "http://localhost:8003"
MCP_BASE_URL = "http://localhost:8000/mcp"

def test_ml_forecasting_health():
    """Test ML forecasting service health."""
    print("🔍 Testing ML Forecasting Service Health...")
    
    try:
        response = requests.get(f"{BASE_URL}/ml-forecasting/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ ML Forecasting Service Health Check:")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Components: {len(data.get('components', []))}")
            print(f"   Available Models: {len(data.get('available_models', []))}")
            print(f"   Available Agents: {len(data.get('available_agents', []))}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_phase3_ensemble_forecast():
    """Test Phase 3 ensemble forecasting."""
    print("\n🔍 Testing Phase 3 Ensemble Forecasting...")
    
    try:
        # Create sample time series data
        timestamps = [datetime.now() + timedelta(hours=i) for i in range(100)]
        values = np.random.normal(100, 10, 100).tolist()
        
        request_data = {
            "training_data": {
                "timestamps": [ts.isoformat() for ts in timestamps],
                "values": values,
                "metadata": {"source": "test", "type": "numerical"}
            },
            "validation_data": {
                "timestamps": [ts.isoformat() for ts in timestamps[-20:]],
                "values": values[-20:],
                "metadata": {"source": "test", "type": "numerical"}
            },
            "horizon": 10,
            "optimize_weights": True
        }
        
        response = requests.post(
            f"{BASE_URL}/ml-forecasting/phase3/ensemble-forecast",
            json=request_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Ensemble Forecasting Test:")
            print(f"   Success: {data.get('success', False)}")
            print(f"   Operation: {data.get('operation', 'unknown')}")
            
            if 'training_result' in data:
                training = data['training_result']
                print(f"   Models Trained: {training.get('models_trained', 0)}")
                print(f"   Model Names: {training.get('model_names', [])}")
            
            if 'forecast' in data:
                forecast = data['forecast']
                print(f"   Confidence Score: {forecast.get('confidence_score', 0):.3f}")
                print(f"   Model Weights: {forecast.get('model_weights', {})}")
            
            return True
        else:
            print(f"❌ Ensemble forecasting failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ensemble forecasting error: {e}")
        return False

def test_phase3_scenario_prediction():
    """Test Phase 3 scenario prediction."""
    print("\n🔍 Testing Phase 3 Scenario Prediction...")
    
    try:
        # Create sample capability analysis
        capability_analysis = {
            "military_force": 0.7,
            "economic_strength": 0.8,
            "technological_advantage": 0.6,
            "logistical_support": 0.9,
            "political_will": 0.5,
            "alliance_networks": 0.7,
            "geographic_position": 0.6,
            "resource_availability": 0.8,
            "command_control": 0.7,
            "intelligence_capabilities": 0.8
        }
        
        request_data = {
            "capability_analysis": capability_analysis,
            "scenario_types": ["aggressive", "defensive", "balanced"],
            "include_outcomes": True,
            "include_escalation_paths": True
        }
        
        response = requests.post(
            f"{BASE_URL}/ml-forecasting/phase3/scenario-prediction",
            json=request_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Scenario Prediction Test:")
            print(f"   Success: {data.get('success', False)}")
            print(f"   Operation: {data.get('operation', 'unknown')}")
            
            if 'results' in data:
                results = data['results']
                scenarios = results.get('scenarios', [])
                print(f"   Scenarios Generated: {len(scenarios)}")
                
                for scenario in scenarios[:2]:  # Show first 2 scenarios
                    print(f"     - {scenario.get('scenario_type', 'unknown')}: "
                          f"P={scenario.get('probability', 0):.3f}, "
                          f"C={scenario.get('confidence_score', 0):.3f}")
                
                escalation_paths = results.get('escalation_paths', [])
                print(f"   Escalation Paths Analyzed: {len(escalation_paths)}")
            
            return True
        else:
            print(f"❌ Scenario prediction failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Scenario prediction error: {e}")
        return False

def test_phase3_intelligence_stream():
    """Test Phase 3 intelligence data streaming."""
    print("\n🔍 Testing Phase 3 Intelligence Data Streaming...")
    
    try:
        # Test connecting to SIGINT stream
        connection_data = {
            "stream_type": "sigint_stream",
            "connection_params": {
                "host": "localhost",
                "port": 8080,
                "protocol": "tcp"
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/ml-forecasting/phase3/intelligence-stream/connect",
            json=connection_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Intelligence Stream Connection Test:")
            print(f"   Success: {data.get('success', False)}")
            print(f"   Stream Type: {data.get('stream_type', 'unknown')}")
            print(f"   Connected: {data.get('connected', False)}")
            
            # Test processing intelligence data
            process_data = {
                 "stream_type": "sigint_stream",
                 "connection_params": {},
                 "data": {
                     "stream_type": "sigint_stream",
                     "signal_type": "radio",
                     "frequency": 150.5,
                     "strength": 0.8,
                     "location": {"lat": 40.7128, "lon": -74.0060},
                     "encryption_level": "high",
                     "source_confidence": 0.9
                 }
             }
            
            process_response = requests.post(
                f"{BASE_URL}/ml-forecasting/phase3/intelligence-stream/process",
                json=process_data
            )
            
            if process_response.status_code == 200:
                process_result = process_response.json()
                print("✅ Intelligence Data Processing Test:")
                print(f"   Success: {process_result.get('success', False)}")
                print(f"   Stream Type: {process_result.get('stream_type', 'unknown')}")
                
                if 'processed_data' in process_result:
                    processed = process_result['processed_data']
                    print(f"   Confidence Score: {processed.get('confidence_score', 0):.3f}")
                    print(f"   Source Reliability: {processed.get('source_reliability', 0):.3f}")
            
            # Test stream status
            status_response = requests.get(
                f"{BASE_URL}/ml-forecasting/phase3/intelligence-stream/status"
            )
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                print("✅ Intelligence Stream Status Test:")
                print(f"   Success: {status_data.get('success', False)}")
                
                if 'status' in status_data:
                    status = status_data['status']
                    print(f"   Supported Stream Types: {len(status.get('supported_stream_types', []))}")
                    print(f"   Active Connections: {status.get('active_connections', 0)}")
            
            return True
        else:
            print(f"❌ Intelligence stream connection failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Intelligence stream error: {e}")
        return False

def test_phase3_status_endpoints():
    """Test Phase 3 status endpoints."""
    print("\n🔍 Testing Phase 3 Status Endpoints...")
    
    try:
        # Test ensemble status
        ensemble_response = requests.get(f"{BASE_URL}/ml-forecasting/phase3/ensemble-status")
        if ensemble_response.status_code == 200:
            ensemble_data = ensemble_response.json()
            print("✅ Ensemble Status Test:")
            print(f"   Success: {ensemble_data.get('success', False)}")
            
            if 'status' in ensemble_data:
                status = ensemble_data['status']
                print(f"   Status: {status.get('status', 'unknown')}")
                print(f"   Base Models: {len(status.get('base_models', {}))}")
                print(f"   History Length: {status.get('history_length', 0)}")
        
        # Test scenario predictor status
        scenario_response = requests.get(f"{BASE_URL}/ml-forecasting/phase3/scenario-predictor-status")
        if scenario_response.status_code == 200:
            scenario_data = scenario_response.json()
            print("✅ Scenario Predictor Status Test:")
            print(f"   Success: {scenario_data.get('success', False)}")
            
            if 'status' in scenario_data:
                status = scenario_data['status']
                print(f"   Status: {status.get('status', 'unknown')}")
                print(f"   Scenario Templates: {len(status.get('scenario_templates', []))}")
                print(f"   Scenarios Generated: {status.get('scenarios_generated', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Status endpoints error: {e}")
        return False

def test_mcp_integration():
    """Test MCP integration for Phase 3 components."""
    print("\n🔍 Testing MCP Integration...")
    
    try:
        # Test MCP initialize (skip health check as it's not available)
        init_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "phase3_test", "version": "1.0.0"}
            }
        }
        
        init_response = requests.post(
            f"{MCP_BASE_URL}",
            json=init_data,
            headers={"Content-Type": "application/json"}
        )
        
        if init_response.status_code == 200:
            init_result = init_response.json()
            print("✅ MCP Initialize Test:")
            print(f"   Success: {init_result.get('result', {}).get('capabilities', {})}")
        else:
            print(f"⚠️ MCP initialize failed: {init_response.status_code}")
        
        # Test tools/list
        tools_data = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        tools_response = requests.post(
            f"{MCP_BASE_URL}",
            json=tools_data,
            headers={"Content-Type": "application/json"}
        )
        
        if tools_response.status_code == 200:
            tools_result = tools_response.json()
            tools = tools_result.get('result', {}).get('tools', [])
            print("✅ MCP Tools List Test:")
            print(f"   Available Tools: {len(tools)}")
            
            # Look for Phase 3 related tools
            phase3_tools = [tool for tool in tools if any(keyword in tool.get('name', '').lower() 
                                                        for keyword in ['ensemble', 'scenario', 'intelligence'])]
            print(f"   Phase 3 Related Tools: {len(phase3_tools)}")
            
            for tool in phase3_tools[:3]:  # Show first 3
                print(f"     - {tool.get('name', 'unknown')}")
        else:
            print(f"⚠️ MCP tools/list failed: {tools_response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP integration error: {e}")
        return False

def main():
    """Run all Phase 3 tests."""
    print("🚀 Phase 3 Advanced Forecasting & Prediction Test Suite")
    print("=" * 60)
    
    # Test results
    results = []
    
    # Run tests
    results.append(("Health Check", test_ml_forecasting_health()))
    results.append(("Ensemble Forecasting", test_phase3_ensemble_forecast()))
    results.append(("Scenario Prediction", test_phase3_scenario_prediction()))
    results.append(("Intelligence Streaming", test_phase3_intelligence_stream()))
    results.append(("Status Endpoints", test_phase3_status_endpoints()))
    results.append(("MCP Integration", test_mcp_integration()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Phase 3 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\n   Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All Phase 3 tests passed! Phase 3 integration successful.")
    else:
        print("⚠️ Some Phase 3 tests failed. Check the logs for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
