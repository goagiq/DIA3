#!/usr/bin/env python3
"""
Test script for Phase 1 ML/DL/RL Forecasting Components
Tests all endpoints and functionality of the ML forecasting system
"""

import asyncio
import json
import time
import requests
from typing import Dict, Any, List
import numpy as np
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://127.0.0.1:8003"
WAIT_TIME = 30  # Wait 30 seconds after server restart

class MLForecastingTester:
    """Test class for ML/DL/RL Forecasting Components"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = "", error: str = ""):
        """Log test results"""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if error:
            print(f"   Error: {error}")
        print()
    
    def test_health_endpoint(self) -> bool:
        """Test the health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/ml-forecasting/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                expected_components = [
                    "reinforcement_learning_engine",
                    "enhanced_time_series_models",
                    "enhanced_causal_inference_engine",
                    "dod_threat_assessment_models",
                    "intelligence_analysis_models"
                ]
                
                if all(comp in data.get("components", []) for comp in expected_components):
                    self.log_test("Health Endpoint", True, f"All {len(expected_components)} components available")
                    return True
                else:
                    self.log_test("Health Endpoint", False, "Missing expected components")
                    return False
            else:
                self.log_test("Health Endpoint", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Endpoint", False, error=str(e))
            return False
    
    def test_models_endpoint(self) -> bool:
        """Test the models endpoint"""
        try:
            response = requests.get(f"{self.base_url}/ml-forecasting/models", timeout=10)
            if response.status_code == 200:
                data = response.json()
                expected_sections = ["time_series_models", "rl_agents", "causal_inference_methods", "domains"]
                
                if all(section in data for section in expected_sections):
                    self.log_test("Models Endpoint", True, f"All {len(expected_sections)} model sections available")
                    return True
                else:
                    self.log_test("Models Endpoint", False, "Missing expected model sections")
                    return False
            else:
                self.log_test("Models Endpoint", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Models Endpoint", False, error=str(e))
            return False
    
    def test_summary_endpoint(self) -> bool:
        """Test the summary endpoint"""
        try:
            response = requests.get(f"{self.base_url}/ml-forecasting/summary", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "service" in data and "components" in data and "endpoints" in data:
                    self.log_test("Summary Endpoint", True, f"Service: {data['service']}, Version: {data.get('version', 'N/A')}")
                    return True
                else:
                    self.log_test("Summary Endpoint", False, "Missing expected summary fields")
                    return False
            else:
                self.log_test("Summary Endpoint", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Summary Endpoint", False, error=str(e))
            return False
    
    def test_time_series_forecast(self) -> bool:
        """Test time series forecasting"""
        try:
            # Generate sample time series data
            timestamps = [(datetime.now() - timedelta(hours=i)).isoformat() for i in range(100, 0, -1)]
            values = np.random.normal(100, 10, 100).tolist()
            
            request_data = {
                "data": {
                    "values": values,
                    "timestamps": timestamps,
                    "features": {"feature1": "value1"},
                    "metadata": {"source": "test"}
                },
                "model_type": "lstm",
                "domain": "general",
                "parameters": {
                    "forecast_horizon": 10
                }
            }
            
            response = requests.post(
                f"{self.base_url}/ml-forecasting/time-series/forecast",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "forecast" in data:
                    self.log_test("Time Series Forecast", True, f"Generated {len(data['forecast'])} forecast points")
                    return True
                else:
                    self.log_test("Time Series Forecast", False, "Missing forecast data")
                    return False
            else:
                self.log_test("Time Series Forecast", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Time Series Forecast", False, error=str(e))
            return False
    
    def test_rl_optimization(self) -> bool:
        """Test reinforcement learning optimization"""
        try:
            request_data = {
                "state": {
                    "features": [1.0, 2.0, 3.0],
                    "metadata": {"context": "test"},
                    "timestamp": time.time()
                },
                "action_space": ["action1", "action2", "action3"],
                "reward_function": {"value": 1.0},
                "agent_type": "q_learning"
            }
            
            response = requests.post(
                f"{self.base_url}/ml-forecasting/reinforcement-learning/optimize",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "selected_action" in data:
                    self.log_test("RL Optimization", True, f"Selected action: {data['selected_action']}")
                    return True
                else:
                    self.log_test("RL Optimization", False, "Missing action selection")
                    return False
            else:
                self.log_test("RL Optimization", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("RL Optimization", False, error=str(e))
            return False
    
    def test_causal_inference(self) -> bool:
        """Test causal inference analysis"""
        try:
            request_data = {
                "data": {
                    "variable1": [1, 2, 3, 4, 5],
                    "variable2": [2, 4, 6, 8, 10],
                    "variable3": [1, 3, 5, 7, 9]
                },
                "variables": ["variable1", "variable2", "variable3"],
                "analysis_type": "granger"
            }
            
            response = requests.post(
                f"{self.base_url}/ml-forecasting/causal-inference/analyze",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "result" in data:
                    self.log_test("Causal Inference", True, f"Analysis type: {data['analysis_type']}")
                    return True
                else:
                    self.log_test("Causal Inference", False, "Missing analysis result")
                    return False
            else:
                self.log_test("Causal Inference", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Causal Inference", False, error=str(e))
            return False
    
    def test_defense_domain_analysis(self) -> bool:
        """Test defense domain analysis"""
        try:
            request_data = {
                "data": {
                    "threat_indicators": [0.8, 0.6, 0.9],
                    "military_capabilities": [0.7, 0.8, 0.6],
                    "geopolitical_factors": [0.5, 0.7, 0.8]
                },
                "domain": "defense",
                "analysis_type": "threat_assessment",
                "parameters": {
                    "confidence_threshold": 0.8
                }
            }
            
            response = requests.post(
                f"{self.base_url}/ml-forecasting/domain-specific/defense/analyze",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "result" in data:
                    self.log_test("Defense Domain Analysis", True, f"Analysis type: {data['analysis_type']}")
                    return True
                else:
                    self.log_test("Defense Domain Analysis", False, "Missing analysis result")
                    return False
            else:
                self.log_test("Defense Domain Analysis", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Defense Domain Analysis", False, error=str(e))
            return False
    
    def test_intelligence_domain_analysis(self) -> bool:
        """Test intelligence domain analysis"""
        try:
            request_data = {
                "data": {
                    "signals_data": [0.9, 0.7, 0.8],
                    "human_intelligence": [0.6, 0.8, 0.7],
                    "open_source": [0.5, 0.6, 0.8]
                },
                "domain": "intelligence",
                "analysis_type": "signals_intelligence",
                "parameters": {
                    "analysis_depth": "comprehensive"
                }
            }
            
            response = requests.post(
                f"{self.base_url}/ml-forecasting/domain-specific/intelligence/analyze",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "result" in data:
                    self.log_test("Intelligence Domain Analysis", True, f"Analysis type: {data['analysis_type']}")
                    return True
                else:
                    self.log_test("Intelligence Domain Analysis", False, "Missing analysis result")
                    return False
            else:
                self.log_test("Intelligence Domain Analysis", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Intelligence Domain Analysis", False, error=str(e))
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return results"""
        print("🤖 Testing Phase 1 ML/DL/RL Forecasting Components")
        print("=" * 60)
        
        # Wait for server to be ready
        print(f"⏳ Waiting {WAIT_TIME} seconds for server to be ready...")
        time.sleep(WAIT_TIME)
        
        # Run tests
        tests = [
            self.test_health_endpoint,
            self.test_models_endpoint,
            self.test_summary_endpoint,
            self.test_time_series_forecast,
            self.test_rl_optimization,
            self.test_causal_inference,
            self.test_defense_domain_analysis,
            self.test_intelligence_domain_analysis
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        # Generate summary
        summary = {
            "test_suite": "Phase 1 ML/DL/RL Forecasting Components",
            "timestamp": datetime.now().isoformat(),
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "success_rate": (passed / total) * 100 if total > 0 else 0,
            "results": self.test_results
        }
        
        print("=" * 60)
        print(f"📊 Test Summary:")
        print(f"   Total Tests: {total}")
        print(f"   Passed: {passed}")
        print(f"   Failed: {total - passed}")
        print(f"   Success Rate: {summary['success_rate']:.1f}%")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️ Some tests failed. Check the results above.")
        
        return summary

def main():
    """Main test function"""
    tester = MLForecastingTester()
    results = tester.run_all_tests()
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ml_forecasting_test_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📄 Test results saved to: {filename}")
    
    return results

if __name__ == "__main__":
    main()
