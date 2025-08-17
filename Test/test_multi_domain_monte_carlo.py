#!/usr/bin/env python3
"""
Multi-Domain Monte Carlo Engine Test Script
Comprehensive testing of the multi-domain Monte Carlo simulation engine.
"""

import asyncio
import json
import logging
import requests
import time
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MultiDomainMonteCarloTester:
    """Test suite for multi-domain Monte Carlo engine."""
    
    def __init__(self, base_url="http://127.0.0.1:8003"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def check_system_health(self) -> bool:
        """Check if the system is available."""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/multi-domain-monte-carlo/health")
            if response.status_code == 200:
                logger.info("✅ Multi-domain Monte Carlo service is healthy")
                return True
            else:
                logger.error(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Health check error: {e}")
            return False
    
    async def test_available_scenarios(self) -> Dict[str, Any]:
        """Test getting available scenarios."""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/multi-domain-monte-carlo/scenarios")
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Available scenarios: {result}")
                return {"status": "success", "data": result}
            else:
                logger.error(f"❌ Failed to get scenarios: {response.status_code}")
                return {"status": "failed", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"❌ Error getting scenarios: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def test_defense_simulation(self) -> Dict[str, Any]:
        """Test defense domain simulation."""
        try:
            request_data = {
                "scenario_name": "military_capability",
                "num_iterations": 1000,  # Reduced for testing
                "confidence_level": 0.95,
                "custom_variables": None
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/multi-domain-monte-carlo/simulate/defense",
                json=request_data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Defense simulation completed: {result['simulation_id']}")
                return {"status": "success", "data": result}
            else:
                logger.error(f"❌ Defense simulation failed: {response.status_code}")
                return {"status": "failed", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"❌ Error in defense simulation: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def test_business_simulation(self) -> Dict[str, Any]:
        """Test business domain simulation."""
        try:
            request_data = {
                "scenario_name": "market_analysis",
                "num_iterations": 1000,  # Reduced for testing
                "confidence_level": 0.95,
                "custom_variables": None
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/multi-domain-monte-carlo/simulate/business",
                json=request_data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Business simulation completed: {result['simulation_id']}")
                return {"status": "success", "data": result}
            else:
                logger.error(f"❌ Business simulation failed: {response.status_code}")
                return {"status": "failed", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"❌ Error in business simulation: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def test_financial_simulation(self) -> Dict[str, Any]:
        """Test financial domain simulation."""
        try:
            request_data = {
                "scenario_name": "portfolio_risk",
                "num_iterations": 1000,  # Reduced for testing
                "confidence_level": 0.95,
                "custom_variables": None
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/multi-domain-monte-carlo/simulate/financial",
                json=request_data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Financial simulation completed: {result['simulation_id']}")
                return {"status": "success", "data": result}
            else:
                logger.error(f"❌ Financial simulation failed: {response.status_code}")
                return {"status": "failed", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"❌ Error in financial simulation: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def test_cybersecurity_simulation(self) -> Dict[str, Any]:
        """Test cybersecurity domain simulation."""
        try:
            request_data = {
                "scenario_name": "threat_assessment",
                "num_iterations": 1000,  # Reduced for testing
                "confidence_level": 0.95,
                "custom_variables": None
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/multi-domain-monte-carlo/simulate/cybersecurity",
                json=request_data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Cybersecurity simulation completed: {result['simulation_id']}")
                return {"status": "success", "data": result}
            else:
                logger.error(f"❌ Cybersecurity simulation failed: {response.status_code}")
                return {"status": "failed", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"❌ Error in cybersecurity simulation: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def test_custom_simulation(self) -> Dict[str, Any]:
        """Test custom simulation with user-defined parameters."""
        try:
            request_data = {
                "domain": "defense",
                "scenario_name": "custom_military_assessment",
                "simulation_type": "capability_assessment",
                "num_iterations": 500,  # Reduced for testing
                "confidence_level": 0.95,
                "custom_variables": {
                    "military_spending": {
                        "distribution": "lognormal",
                        "parameters": {"mean": 4.0, "std": 0.2},
                        "description": "Custom military spending"
                    },
                    "force_strength": {
                        "distribution": "normal",
                        "parameters": {"mean": 400000, "std": 40000},
                        "description": "Custom force strength"
                    }
                },
                "correlations": [
                    [1.0, 0.3],
                    [0.3, 1.0]
                ]
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/multi-domain-monte-carlo/simulate/custom",
                json=request_data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Custom simulation completed: {result['simulation_id']}")
                return {"status": "success", "data": result}
            else:
                logger.error(f"❌ Custom simulation failed: {response.status_code}")
                return {"status": "failed", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"❌ Error in custom simulation: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def test_batch_simulations(self) -> Dict[str, Any]:
        """Test batch simulations."""
        try:
            request_data = [
                {
                    "domain": "defense",
                    "scenario_name": "military_capability",
                    "simulation_type": "capability_assessment",
                    "num_iterations": 500,
                    "confidence_level": 0.95
                },
                {
                    "domain": "business",
                    "scenario_name": "market_analysis",
                    "simulation_type": "risk_analysis",
                    "num_iterations": 500,
                    "confidence_level": 0.95
                }
            ]
            
            response = self.session.post(
                f"{self.base_url}/api/v1/multi-domain-monte-carlo/simulate/batch",
                json=request_data,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Batch simulations completed: {result['batch_id']}")
                return {"status": "success", "data": result}
            else:
                logger.error(f"❌ Batch simulations failed: {response.status_code}")
                return {"status": "failed", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"❌ Error in batch simulations: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def test_performance_summary(self) -> Dict[str, Any]:
        """Test getting performance summary."""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/multi-domain-monte-carlo/performance")
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Performance summary retrieved")
                return {"status": "success", "data": result}
            else:
                logger.error(f"❌ Failed to get performance summary: {response.status_code}")
                return {"status": "failed", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"❌ Error getting performance summary: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def test_report_generation(self, simulation_id: str) -> Dict[str, Any]:
        """Test report generation."""
        try:
            # Test JSON report
            request_data = {
                "simulation_id": simulation_id,
                "report_format": "json"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/multi-domain-monte-carlo/report",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ JSON report generated for {simulation_id}")
                
                # Test text report
                request_data["report_format"] = "text"
                response = self.session.post(
                    f"{self.base_url}/api/v1/multi-domain-monte-carlo/report",
                    json=request_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    logger.info(f"✅ Text report generated for {simulation_id}")
                    return {"status": "success", "data": result}
                else:
                    logger.error(f"❌ Text report generation failed: {response.status_code}")
                    return {"status": "failed", "error": f"Text report HTTP {response.status_code}"}
            else:
                logger.error(f"❌ JSON report generation failed: {response.status_code}")
                return {"status": "failed", "error": f"JSON report HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"❌ Error in report generation: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive test suite."""
        logger.info("🚀 Starting Multi-Domain Monte Carlo Comprehensive Test Suite")
        logger.info("=" * 80)
        
        start_time = time.time()
        
        # Check system health
        if not self.check_system_health():
            return {"status": "failed", "error": "System health check failed"}
        
        # Run all tests
        tests = [
            ("Available Scenarios", self.test_available_scenarios()),
            ("Defense Simulation", self.test_defense_simulation()),
            ("Business Simulation", self.test_business_simulation()),
            ("Financial Simulation", self.test_financial_simulation()),
            ("Cybersecurity Simulation", self.test_cybersecurity_simulation()),
            ("Custom Simulation", self.test_custom_simulation()),
            ("Batch Simulations", self.test_batch_simulations()),
            ("Performance Summary", self.test_performance_summary())
        ]
        
        results = {}
        simulation_ids = []
        
        for test_name, test_coro in tests:
            logger.info(f"\n🧪 Running {test_name}...")
            result = await test_coro
            results[test_name] = result
            
            if result["status"] == "success" and "data" in result:
                if "simulation_id" in result["data"]:
                    simulation_ids.append(result["data"]["simulation_id"])
                elif "batch_id" in result["data"]:
                    # Extract simulation IDs from batch results
                    for sim_result in result["data"].get("results", []):
                        if "simulation_id" in sim_result:
                            simulation_ids.append(sim_result["simulation_id"])
        
        # Test report generation for the first simulation
        if simulation_ids:
            logger.info(f"\n📊 Testing report generation for simulation {simulation_ids[0]}...")
            report_result = await self.test_report_generation(simulation_ids[0])
            results["Report Generation"] = report_result
        
        # Calculate summary
        total_tests = len(results)
        successful_tests = sum(1 for r in results.values() if r["status"] == "success")
        failed_tests = total_tests - successful_tests
        
        execution_time = time.time() - start_time
        
        summary = {
            "status": "completed",
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "success_rate": (successful_tests / total_tests) * 100 if total_tests > 0 else 0,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "simulation_ids": simulation_ids
        }
        
        logger.info("\n" + "=" * 80)
        logger.info("📊 TEST SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Successful: {successful_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Success Rate: {summary['success_rate']:.1f}%")
        logger.info(f"Execution Time: {execution_time:.2f} seconds")
        logger.info(f"Generated Simulation IDs: {len(simulation_ids)}")
        
        # Log detailed results
        for test_name, result in results.items():
            status_icon = "✅" if result["status"] == "success" else "❌"
            logger.info(f"{status_icon} {test_name}: {result['status']}")
        
        return summary


async def main():
    """Main test function."""
    tester = MultiDomainMonteCarloTester()
    
    try:
        result = await tester.run_comprehensive_test()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"Results/multi_domain_monte_carlo_test_results_{timestamp}.json"
        
        os.makedirs("Results", exist_ok=True)
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        logger.info(f"\n💾 Test results saved to: {result_file}")
        
        if result["status"] == "completed" and result["success_rate"] >= 80:
            logger.info("\n🎉 Multi-Domain Monte Carlo Test Suite PASSED!")
            return 0
        else:
            logger.error("\n❌ Multi-Domain Monte Carlo Test Suite FAILED!")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Test suite error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
