#!/usr/bin/env python3
"""
Phase 5 Monte Carlo Integration Test Script
Comprehensive test suite for Phase 5 advanced features integration
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Test configuration
MCP_BASE_URL = "http://localhost:8000"
API_BASE_URL = "http://localhost:8000"

class TestPhase5MonteCarloIntegration:
    """Comprehensive Phase 5 Monte Carlo integration test suite"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "PASS" if success else "FAIL"
        print(f"{status} {test_name}: {details}")
    
    async def test_phase5_engine_features(self):
        """Test Phase 5 engine features"""
        try:
            # Import and test Phase 5 engine
            from src.core.monte_carlo.engine import MonteCarloEngine
            from src.core.monte_carlo.config import MonteCarloConfig
            
            # Create engine with Phase 5 features
            config = MonteCarloConfig()
            config.cache_results = True
            config.max_workers = 4
            
            engine = MonteCarloEngine(config)
            
            # Test Phase 5 features
            phase5_features = {
                "parallel_processing": hasattr(engine, 'executor'),
                "caching": hasattr(engine, 'cache'),
                "audit_logging": hasattr(engine, 'audit_log'),
                "security_compliance": hasattr(engine, 'data_classification'),
                "real_time_data": hasattr(engine, 'real_time_data_sources'),
                "event_handlers": hasattr(engine, 'event_handlers')
            }
            
            all_features_present = all(phase5_features.values())
            
            self.log_test("Phase 5 Engine Features", all_features_present, 
                         f"Features: {phase5_features}")
            
            return all_features_present
            
        except Exception as e:
            self.log_test("Phase 5 Engine Features", False, f"Error: {e}")
            return False
    
    async def test_phase5_advanced_analytics(self):
        """Test Phase 5 advanced analytics features"""
        try:
            from src.core.monte_carlo.analysis import ResultAnalyzer
            import numpy as np
            
            analyzer = ResultAnalyzer()
            
            # Create sample data
            samples = np.random.normal(100, 15, (1000, 3))
            
            # Test Phase 5 analytics methods
            phase5_analytics = {
                "failure_analysis": hasattr(analyzer, 'calculate_failure_modes'),
                "risk_prioritization": hasattr(analyzer, 'prioritize_risks'),
                "stress_testing": hasattr(analyzer, 'perform_stress_tests'),
                "failure_thresholds": hasattr(analyzer, 'failure_thresholds')
            }
            
            # Test actual method calls
            try:
                failure_analysis = analyzer.calculate_failure_modes(samples)
                risk_prioritization = analyzer.prioritize_risks(samples)
                stress_tests = analyzer.perform_stress_tests(samples, {})
                
                methods_working = all([
                    isinstance(failure_analysis, dict),
                    isinstance(risk_prioritization, dict),
                    isinstance(stress_tests, dict)
                ])
                
                all_analytics_working = all(phase5_analytics.values()) and methods_working
                
                self.log_test("Phase 5 Advanced Analytics", all_analytics_working,
                             f"Analytics: {phase5_analytics}, Methods working: {methods_working}")
                
                return all_analytics_working
                
            except Exception as e:
                self.log_test("Phase 5 Advanced Analytics", False, f"Method execution error: {e}")
                return False
                
        except Exception as e:
            self.log_test("Phase 5 Advanced Analytics", False, f"Error: {e}")
            return False
    
    async def test_phase5_mcp_tools(self):
        """Test Phase 5 MCP tools integration"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                # Test MCP server connection
                async with session.post(
                    f"{MCP_BASE_URL}/mcp",
                    json={
                        "jsonrpc": "2.0",
                        "method": "initialize",
                        "params": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {"tools": {}}
                        },
                        "id": 1
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json, text/event-stream"
                    },
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status != 200:
                        self.log_test("Phase 5 MCP Tools", False, "MCP server not responding")
                        return False
                    
                    data = await response.json()
                    
                    # Test Monte Carlo health check
                    async with session.post(
                        f"{MCP_BASE_URL}/mcp",
                        json={
                            "jsonrpc": "2.0",
                            "method": "tools/call",
                            "params": {
                                "name": "monte_carlo_health_check",
                                "arguments": {}
                            },
                            "id": 2
                        },
                        headers={"Content-Type": "application/json"}
                    ) as health_response:
                        if health_response.status == 200:
                            health_data = await health_response.json()
                            if "result" in health_data:
                                result = health_data["result"]
                                phase5_features = result.get("phase5_features", {})
                                
                                phase5_tools_working = all([
                                    phase5_features.get("parallel_processing", False),
                                    phase5_features.get("caching_enabled", False),
                                    phase5_features.get("security_compliance", False),
                                    phase5_features.get("advanced_analytics", False),
                                    phase5_features.get("stress_testing", False),
                                    phase5_features.get("failure_analysis", False),
                                    phase5_features.get("risk_prioritization", False)
                                ])
                                
                                self.log_test("Phase 5 MCP Tools", phase5_tools_working,
                                             f"Phase 5 features: {phase5_features}")
                                return phase5_tools_working
                        
                        self.log_test("Phase 5 MCP Tools", False, "Health check failed")
                        return False
                        
        except Exception as e:
            self.log_test("Phase 5 MCP Tools", False, f"Error: {e}")
            return False
    
    async def test_phase5_api_endpoints(self):
        """Test Phase 5 API endpoints"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                # Test health endpoint with Phase 5 features
                async with session.get(f"{API_BASE_URL}/api/v1/monte-carlo/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        phase5_features = data.get("phase5_features", {})
                        
                        phase5_api_working = all([
                            phase5_features.get("parallel_processing", False),
                            phase5_features.get("caching_enabled", False),
                            phase5_features.get("security_compliance", False),
                            phase5_features.get("advanced_analytics", False),
                            phase5_features.get("stress_testing", False),
                            phase5_features.get("failure_analysis", False),
                            phase5_features.get("risk_prioritization", False)
                        ])
                        
                        self.log_test("Phase 5 API Endpoints", phase5_api_working,
                                     f"Phase 5 features: {phase5_features}")
                        return phase5_api_working
                    
                    self.log_test("Phase 5 API Endpoints", False, f"API not responding: {response.status}")
                    return False
                    
        except Exception as e:
            self.log_test("Phase 5 API Endpoints", False, f"Error: {e}")
            return False
    
    async def test_phase5_performance_optimization(self):
        """Test Phase 5 performance optimization features"""
        try:
            from src.core.monte_carlo.engine import MonteCarloEngine
            from src.core.monte_carlo.config import MonteCarloConfig
            
            # Test performance optimization
            config = MonteCarloConfig()
            config.max_workers = 4
            config.cache_results = True
            
            engine = MonteCarloEngine(config)
            
            # Test parallel processing
            parallel_working = hasattr(engine, 'executor') and engine.executor is not None
            
            # Test caching
            caching_working = hasattr(engine, 'cache') and engine.cache is not None
            
            # Test memory optimization
            memory_optimization = hasattr(engine, '_generate_samples_optimized')
            
            performance_features = {
                "parallel_processing": parallel_working,
                "caching": caching_working,
                "memory_optimization": memory_optimization
            }
            
            all_performance_working = all(performance_features.values())
            
            self.log_test("Phase 5 Performance Optimization", all_performance_working,
                         f"Performance features: {performance_features}")
            
            return all_performance_working
            
        except Exception as e:
            self.log_test("Phase 5 Performance Optimization", False, f"Error: {e}")
            return False
    
    async def test_phase5_security_compliance(self):
        """Test Phase 5 security and compliance features"""
        try:
            from src.core.monte_carlo.engine import MonteCarloEngine
            
            engine = MonteCarloEngine()
            
            # Test security features
            security_features = {
                "audit_logging": hasattr(engine, 'audit_log'),
                "data_classification": hasattr(engine, 'data_classification'),
                "audit_event_logging": hasattr(engine, '_log_audit_event')
            }
            
            # Test audit logging
            if hasattr(engine, '_log_audit_event'):
                try:
                    engine._log_audit_event("test_event", {"test": "data"})
                    audit_logging_working = len(engine.audit_log) > 0
                except:
                    audit_logging_working = False
            else:
                audit_logging_working = False
            
            security_features["audit_logging_working"] = audit_logging_working
            
            all_security_working = all(security_features.values())
            
            self.log_test("Phase 5 Security Compliance", all_security_working,
                         f"Security features: {security_features}")
            
            return all_security_working
            
        except Exception as e:
            self.log_test("Phase 5 Security Compliance", False, f"Error: {e}")
            return False
    
    async def test_phase5_stress_testing(self):
        """Test Phase 5 stress testing capabilities"""
        try:
            from src.core.monte_carlo.analysis import ResultAnalyzer
            import numpy as np
            
            analyzer = ResultAnalyzer()
            samples = np.random.normal(100, 15, (1000, 3))
            
            # Test stress testing
            stress_tests = analyzer.perform_stress_tests(samples, {})
            
            expected_scenarios = [
                "extreme_market", "correlation_breakdown", "volatility_spike",
                "tail_risk_events", "systemic_risk", "aggregate"
            ]
            
            all_scenarios_present = all(
                scenario in stress_tests for scenario in expected_scenarios
            )
            
            self.log_test("Phase 5 Stress Testing", all_scenarios_present,
                         f"Stress test scenarios: {list(stress_tests.keys())}")
            
            return all_scenarios_present
            
        except Exception as e:
            self.log_test("Phase 5 Stress Testing", False, f"Error: {e}")
            return False
    
    async def test_phase5_failure_analysis(self):
        """Test Phase 5 failure mode analysis"""
        try:
            from src.core.monte_carlo.analysis import ResultAnalyzer
            import numpy as np
            
            analyzer = ResultAnalyzer()
            samples = np.random.normal(100, 15, (1000, 3))
            
            # Test failure analysis
            failure_analysis = analyzer.calculate_failure_modes(samples)
            
            expected_components = [
                "variable_0", "variable_1", "variable_2"
            ]
            
            all_components_present = all(
                component in failure_analysis for component in expected_components
            )
            
            # Check for failure modes structure
            if all_components_present:
                var_analysis = failure_analysis["variable_0"]
                has_failure_modes = "failure_modes" in var_analysis
                has_critical_failures = "critical_failures" in var_analysis
                has_failure_trends = "failure_trends" in var_analysis
                
                structure_complete = all([
                    has_failure_modes, has_critical_failures, has_failure_trends
                ])
            else:
                structure_complete = False
            
            failure_analysis_working = all_components_present and structure_complete
            
            self.log_test("Phase 5 Failure Analysis", failure_analysis_working,
                         f"Components: {all_components_present}, Structure: {structure_complete}")
            
            return failure_analysis_working
            
        except Exception as e:
            self.log_test("Phase 5 Failure Analysis", False, f"Error: {e}")
            return False
    
    async def test_phase5_risk_prioritization(self):
        """Test Phase 5 risk prioritization"""
        try:
            from src.core.monte_carlo.analysis import ResultAnalyzer
            import numpy as np
            
            analyzer = ResultAnalyzer()
            samples = np.random.normal(100, 15, (1000, 3))
            
            # Test risk prioritization
            risk_prioritization = analyzer.prioritize_risks(samples)
            
            expected_components = [
                "risk_scores", "critical_risks", "high_risks", 
                "medium_risks", "low_risks"
            ]
            
            all_components_present = all(
                component in risk_prioritization for component in expected_components
            )
            
            # Check risk scores structure
            if all_components_present:
                risk_scores = risk_prioritization["risk_scores"]
                has_risk_scores = len(risk_scores) > 0
                
                if has_risk_scores:
                    first_risk = risk_scores[0]
                    has_priority = "priority" in first_risk
                    has_risk_score = "risk_score" in first_risk
                    structure_complete = has_priority and has_risk_score
                else:
                    structure_complete = False
            else:
                structure_complete = False
            
            risk_prioritization_working = all_components_present and structure_complete
            
            self.log_test("Phase 5 Risk Prioritization", risk_prioritization_working,
                         f"Components: {all_components_present}, Structure: {structure_complete}")
            
            return risk_prioritization_working
            
        except Exception as e:
            self.log_test("Phase 5 Risk Prioritization", False, f"Error: {e}")
            return False
    
    async def test_phase5_integration_complete(self):
        """Test complete Phase 5 integration"""
        try:
            # Test all Phase 5 components together
            test_results = await asyncio.gather(
                self.test_phase5_engine_features(),
                self.test_phase5_advanced_analytics(),
                self.test_phase5_mcp_tools(),
                self.test_phase5_api_endpoints(),
                self.test_phase5_performance_optimization(),
                self.test_phase5_security_compliance(),
                self.test_phase5_stress_testing(),
                self.test_phase5_failure_analysis(),
                self.test_phase5_risk_prioritization()
            )
            
            all_tests_passed = all(test_results)
            
            self.log_test("Phase 5 Complete Integration", all_tests_passed,
                         f"Tests passed: {sum(test_results)}/{len(test_results)}")
            
            return all_tests_passed
            
        except Exception as e:
            self.log_test("Phase 5 Complete Integration", False, f"Error: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all Phase 5 integration tests"""
        print("🚀 Starting Phase 5 Monte Carlo Integration Tests")
        print("=" * 60)
        
        # Run individual tests
        await self.test_phase5_engine_features()
        await self.test_phase5_advanced_analytics()
        await self.test_phase5_mcp_tools()
        await self.test_phase5_api_endpoints()
        await self.test_phase5_performance_optimization()
        await self.test_phase5_security_compliance()
        await self.test_phase5_stress_testing()
        await self.test_phase5_failure_analysis()
        await self.test_phase5_risk_prioritization()
        
        # Run complete integration test
        await self.test_phase5_integration_complete()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 Phase 5 Monte Carlo Integration Test Summary")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"phase5_monte_carlo_integration_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                "test_suite": "Phase 5 Monte Carlo Integration",
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "success_rate": (passed_tests/total_tests)*100
                },
                "results": self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Results saved to: {filename}")
        
        if passed_tests == total_tests:
            print("\n✅ All Phase 5 Monte Carlo integration tests passed!")
            print("🎉 Phase 5 implementation is complete and ready for Phase 6")
        else:
            print(f"\n⚠️ {failed_tests} test(s) failed. Please review and fix issues.")


async def main():
    """Main test runner"""
    tester = TestPhase5MonteCarloIntegration()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
