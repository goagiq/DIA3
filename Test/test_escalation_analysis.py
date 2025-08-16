#!/usr/bin/env python3
"""
Test script for escalation analysis functionality.

This script tests the escalation analysis agent and API endpoints to ensure
proper functionality across multiple domains.
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any
import requests
from loguru import logger

# Test configuration
API_BASE_URL = "http://localhost:8003"
TEST_CONTENT = """
Russia has recently increased its military presence near the EU border, 
conducting large-scale military exercises and deploying advanced weapons systems. 
The EU has responded with economic sanctions and diplomatic pressure, while 
NATO has announced plans to expand its eastern flank. This escalation follows 
a pattern of historical tensions between Russia and European powers, similar 
to the dynamics described in War and Peace during the Napoleonic era.
"""


class EscalationAnalysisTester:
    """Test class for escalation analysis functionality."""
    
    def __init__(self):
        self.api_base_url = API_BASE_URL
        self.test_results = []
        
    def log_test_result(self, test_name: str, success: bool, details: str = ""):
        """Log test result."""
        result = {
            "test_name": test_name,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} {test_name}: {details}")
    
    def test_health_check(self) -> bool:
        """Test escalation analysis health check endpoint."""
        try:
            url = f"{self.api_base_url}/escalation-analysis/health"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test_result(
                        "Health Check",
                        True,
                        f"Service healthy, {len(data.get('domains_supported', []))} domains supported"
                    )
                    return True
                else:
                    self.log_test_result("Health Check", False, f"Service unhealthy: {data}")
                    return False
            else:
                self.log_test_result("Health Check", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Health Check", False, f"Exception: {e}")
            return False
    
    def test_capabilities(self) -> bool:
        """Test escalation analysis capabilities endpoint."""
        try:
            url = f"{self.api_base_url}/escalation-analysis/capabilities"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    capabilities = data.get("capabilities", {})
                    domains = capabilities.get("supported_domains", [])
                    features = capabilities.get("features", [])
                    
                    self.log_test_result(
                        "Capabilities",
                        True,
                        f"{len(domains)} domains, {len(features)} features"
                    )
                    return True
                else:
                    self.log_test_result("Capabilities", False, "Response not successful")
                    return False
            else:
                self.log_test_result("Capabilities", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Capabilities", False, f"Exception: {e}")
            return False
    
    def test_domains(self) -> bool:
        """Test supported domains endpoint."""
        try:
            url = f"{self.api_base_url}/escalation-analysis/domains"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    domains = data.get("domains", [])
                    expected_domains = ["defense", "intelligence", "business", "cybersecurity", "geopolitical"]
                    
                    missing_domains = set(expected_domains) - set(domains)
                    if not missing_domains:
                        self.log_test_result(
                            "Domains",
                            True,
                            f"All expected domains present: {domains}"
                        )
                        return True
                    else:
                        self.log_test_result(
                            "Domains",
                            False,
                            f"Missing domains: {missing_domains}"
                        )
                        return False
                else:
                    self.log_test_result("Domains", False, "Response not successful")
                    return False
            else:
                self.log_test_result("Domains", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Domains", False, f"Exception: {e}")
            return False
    
    def test_historical_patterns(self) -> bool:
        """Test historical patterns endpoint."""
        try:
            url = f"{self.api_base_url}/escalation-analysis/historical-patterns"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    patterns = data.get("historical_patterns", {})
                    pattern_count = data.get("total_patterns", 0)
                    
                    if pattern_count > 0:
                        self.log_test_result(
                            "Historical Patterns",
                            True,
                            f"{pattern_count} patterns available"
                        )
                        return True
                    else:
                        self.log_test_result("Historical Patterns", False, "No patterns found")
                        return False
                else:
                    self.log_test_result("Historical Patterns", False, "Response not successful")
                    return False
            else:
                self.log_test_result("Historical Patterns", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Historical Patterns", False, f"Exception: {e}")
            return False
    
    def test_general_analysis(self) -> bool:
        """Test general escalation analysis endpoint."""
        try:
            url = f"{self.api_base_url}/escalation-analysis/analyze"
            payload = {
                "content": TEST_CONTENT,
                "domain": "geopolitical",
                "analysis_depth": "comprehensive",
                "include_historical_patterns": True,
                "include_warning_indicators": True,
                "include_mitigation_strategies": True
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    analysis_id = data.get("analysis_id")
                    domain = data.get("domain")
                    confidence_score = data.get("confidence_score", 0)
                    scenarios = data.get("escalation_scenarios", [])
                    
                    self.log_test_result(
                        "General Analysis",
                        True,
                        f"Analysis {analysis_id} completed for {domain} domain, "
                        f"confidence: {confidence_score:.2f}, {len(scenarios)} scenarios"
                    )
                    return True
                else:
                    self.log_test_result("General Analysis", False, "Response not successful")
                    return False
            else:
                self.log_test_result("General Analysis", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("General Analysis", False, f"Exception: {e}")
            return False
    
    def test_domain_specific_analysis(self, domain: str) -> bool:
        """Test domain-specific escalation analysis."""
        try:
            url = f"{self.api_base_url}/escalation-analysis/analyze-{domain}"
            payload = {
                "content": TEST_CONTENT,
                "analysis_depth": "comprehensive",
                "include_historical_patterns": True,
                "include_warning_indicators": True,
                "include_mitigation_strategies": True
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    analysis_id = data.get("analysis_id")
                    confidence_score = data.get("confidence_score", 0)
                    scenarios = data.get("escalation_scenarios", [])
                    
                    self.log_test_result(
                        f"{domain.title()} Analysis",
                        True,
                        f"Analysis {analysis_id} completed, confidence: {confidence_score:.2f}, "
                        f"{len(scenarios)} scenarios"
                    )
                    return True
                else:
                    self.log_test_result(f"{domain.title()} Analysis", False, "Response not successful")
                    return False
            else:
                self.log_test_result(f"{domain.title()} Analysis", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result(f"{domain.title()} Analysis", False, f"Exception: {e}")
            return False
    
    def test_all_domain_analyses(self) -> bool:
        """Test analysis for all supported domains."""
        domains = ["defense", "intelligence", "business", "cybersecurity", "geopolitical"]
        all_success = True
        
        for domain in domains:
            success = self.test_domain_specific_analysis(domain)
            if not success:
                all_success = False
                # Add delay between requests to avoid overwhelming the server
                time.sleep(1)
        
        return all_success
    
    def test_error_handling(self) -> bool:
        """Test error handling with invalid requests."""
        try:
            # Test with invalid domain
            url = f"{self.api_base_url}/escalation-analysis/analyze"
            payload = {
                "content": TEST_CONTENT,
                "domain": "invalid_domain",
                "analysis_depth": "comprehensive"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            # Should return an error for invalid domain
            if response.status_code in [400, 422, 500]:
                self.log_test_result("Error Handling", True, "Properly handled invalid domain")
                return True
            else:
                self.log_test_result("Error Handling", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Error Handling", False, f"Exception: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all escalation analysis tests."""
        logger.info("🚀 Starting Escalation Analysis Tests")
        logger.info("=" * 60)
        
        # Test basic endpoints
        self.test_health_check()
        self.test_capabilities()
        self.test_domains()
        self.test_historical_patterns()
        
        # Test analysis functionality
        self.test_general_analysis()
        self.test_all_domain_analyses()
        
        # Test error handling
        self.test_error_handling()
        
        # Calculate results
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "test_results": self.test_results,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info("=" * 60)
        logger.info(f"📊 Test Summary:")
        logger.info(f"   Total Tests: {total_tests}")
        logger.info(f"   Passed: {passed_tests}")
        logger.info(f"   Failed: {failed_tests}")
        logger.info(f"   Success Rate: {summary['success_rate']:.2%}")
        
        if failed_tests > 0:
            logger.warning("⚠️ Some tests failed. Check the results above for details.")
        else:
            logger.success("🎉 All tests passed!")
        
        return summary


def main():
    """Main test function."""
    try:
        # Create tester instance
        tester = EscalationAnalysisTester()
        
        # Run all tests
        results = tester.run_all_tests()
        
        # Save results to file
        results_file = f"Test/escalation_analysis_test_results_{int(time.time())}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"📄 Test results saved to: {results_file}")
        
        # Return exit code based on test results
        if results["failed_tests"] > 0:
            return 1
        else:
            return 0
            
    except KeyboardInterrupt:
        logger.warning("⚠️ Tests interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
