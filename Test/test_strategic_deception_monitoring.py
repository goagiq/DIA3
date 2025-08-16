#!/usr/bin/env python3
"""
Test script for Strategic Deception Monitoring System

Tests comprehensive strategic deception monitoring capabilities across multiple domains:
- Defense and intelligence applications
- Business intelligence and competitive analysis
- Multi-domain threat assessment
- Real-time deception detection
- Early warning systems
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import requests
from loguru import logger

# Test configuration
API_BASE_URL = "http://localhost:8003"
STRATEGIC_DECEPTION_BASE = f"{API_BASE_URL}/strategic-deception"

# Test data for different domains
TEST_DATA = {
    "defense": {
        "content": "Our military capabilities are limited and we pose no threat to neighboring countries. We are committed to peace and stability in the region. However, we must maintain adequate defense forces for our security needs.",
        "expected_indicators": ["strategic", "linguistic"]
    },
    "intelligence": {
        "content": "I don't know much about the situation, but perhaps there might be some activity. To be honest, I'm not sure about the details. We generally try to cooperate with international partners.",
        "expected_indicators": ["linguistic", "behavioral"]
    },
    "business": {
        "content": "This is an immediate emergency requiring urgent action. Experts say this deal expires tomorrow. Everyone knows this is the best opportunity. Focus on the benefits, not the risks.",
        "expected_indicators": ["strategic", "false_urgency", "authority_appeal", "consensus_fallacy"]
    },
    "cybersecurity": {
        "content": "Officials confirm this is a critical security threat. Studies show immediate action is required. Believe me, this is an emergency situation that needs your immediate attention.",
        "expected_indicators": ["authority_appeal", "false_urgency", "overqualification"]
    },
    "geopolitical": {
        "content": "We appear to be withdrawing from the region, but we maintain our strategic interests. Perhaps there are some developments that might affect the situation. We are committed to peace while ensuring our security.",
        "expected_indicators": ["strategic", "linguistic", "cultural"]
    }
}

# Cultural deception test data
CULTURAL_TEST_DATA = {
    "chinese": {
        "content": "我们致力于和谐发展，促进和平合作，实现共赢局面。传统友谊源远流长，文化交流日益密切。",
        "language": "zh",
        "expected_indicators": ["cultural"]
    },
    "russian": {
        "content": "Мы стремимся к безопасности и стабильности, развитию и прогрессу. Традиции и культура объединяют нас.",
        "language": "ru", 
        "expected_indicators": ["cultural"]
    }
}

class StrategicDeceptionTester:
    """Test class for strategic deception monitoring functionality."""
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
    
    def log_test_result(self, test_name: str, success: bool, details: str = "", response: Dict = None):
        """Log test result."""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response": response
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} {test_name}: {details}")
    
    async def test_health_check(self) -> bool:
        """Test health check endpoint."""
        try:
            response = requests.get(f"{STRATEGIC_DECEPTION_BASE}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                expected_capabilities = [
                    "linguistic_deception_detection",
                    "strategic_deception_identification",
                    "cultural_deception_recognition",
                    "behavioral_inconsistency_analysis",
                    "cross_source_consistency_checking",
                    "real_time_alert_generation",
                    "multi_domain_support"
                ]
                
                success = all(cap in data.get("capabilities", []) for cap in expected_capabilities)
                self.log_test_result(
                    "Health Check",
                    success,
                    f"Service status: {data.get('status')}, Capabilities: {len(data.get('capabilities', []))}",
                    data
                )
                return success
            else:
                self.log_test_result("Health Check", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result("Health Check", False, f"Exception: {e}")
            return False
    
    async def test_single_domain_monitoring(self, domain: str, test_data: Dict) -> bool:
        """Test single domain deception monitoring."""
        try:
            payload = {
                "content": test_data["content"],
                "domain": domain,
                "language": "en",
                "monitoring_level": "comprehensive",
                "include_cultural_analysis": True,
                "include_behavioral_analysis": True,
                "include_strategic_analysis": True,
                "alert_threshold": 0.7
            }
            
            response = requests.post(
                f"{STRATEGIC_DECEPTION_BASE}/monitor",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check basic response structure
                required_fields = [
                    "request_id", "domain", "overall_deception_score",
                    "severity_level", "indicators_detected", "patterns_detected",
                    "critical_alerts", "indicators", "patterns", "recommendations"
                ]
                
                success = all(field in data for field in required_fields)
                
                # Check if indicators were detected
                indicators_detected = data.get("indicators_detected", 0)
                patterns_detected = data.get("patterns_detected", 0)
                
                details = f"Domain: {domain}, Indicators: {indicators_detected}, Patterns: {patterns_detected}, Score: {data.get('overall_deception_score', 0):.3f}"
                
                self.log_test_result(
                    f"Single Domain Monitoring - {domain}",
                    success,
                    details,
                    data
                )
                return success
            else:
                self.log_test_result(
                    f"Single Domain Monitoring - {domain}",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                f"Single Domain Monitoring - {domain}",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_domain_specific_endpoints(self) -> bool:
        """Test domain-specific endpoints."""
        success_count = 0
        total_tests = 0
        
        for domain in ["defense", "intelligence", "business", "cybersecurity", "geopolitical"]:
            total_tests += 1
            try:
                payload = {
                    "content": TEST_DATA[domain]["content"],
                    "language": "en",
                    "monitoring_level": "standard",
                    "include_cultural_analysis": True,
                    "include_behavioral_analysis": True,
                    "include_strategic_analysis": True,
                    "alert_threshold": 0.7
                }
                
                response = requests.post(
                    f"{STRATEGIC_DECEPTION_BASE}/{domain}/monitor",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("domain") == domain:
                        success_count += 1
                        self.log_test_result(
                            f"Domain-Specific Endpoint - {domain}",
                            True,
                            f"Domain correctly set to {domain}"
                        )
                    else:
                        self.log_test_result(
                            f"Domain-Specific Endpoint - {domain}",
                            False,
                            f"Expected domain {domain}, got {data.get('domain')}"
                        )
                else:
                    self.log_test_result(
                        f"Domain-Specific Endpoint - {domain}",
                        False,
                        f"HTTP {response.status_code}: {response.text}"
                    )
                    
            except Exception as e:
                self.log_test_result(
                    f"Domain-Specific Endpoint - {domain}",
                    False,
                    f"Exception: {e}"
                )
        
        overall_success = success_count == total_tests
        self.log_test_result(
            "Domain-Specific Endpoints Overall",
            overall_success,
            f"{success_count}/{total_tests} endpoints working correctly"
        )
        return overall_success
    
    async def test_cultural_deception_monitoring(self) -> bool:
        """Test cultural deception monitoring."""
        success_count = 0
        total_tests = 0
        
        for culture, test_data in CULTURAL_TEST_DATA.items():
            total_tests += 1
            try:
                payload = {
                    "content": test_data["content"],
                    "domain": "general",
                    "language": test_data["language"],
                    "monitoring_level": "comprehensive",
                    "include_cultural_analysis": True,
                    "include_behavioral_analysis": True,
                    "include_strategic_analysis": True,
                    "alert_threshold": 0.7
                }
                
                response = requests.post(
                    f"{STRATEGIC_DECEPTION_BASE}/monitor",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    indicators = data.get("indicators", [])
                    
                    # Check if cultural indicators were detected
                    cultural_indicators = [i for i in indicators if i.get("indicator_type") == "cultural"]
                    
                    if cultural_indicators:
                        success_count += 1
                        self.log_test_result(
                            f"Cultural Deception - {culture}",
                            True,
                            f"Detected {len(cultural_indicators)} cultural indicators"
                        )
                    else:
                        self.log_test_result(
                            f"Cultural Deception - {culture}",
                            False,
                            "No cultural indicators detected"
                        )
                else:
                    self.log_test_result(
                        f"Cultural Deception - {culture}",
                        False,
                        f"HTTP {response.status_code}: {response.text}"
                    )
                    
            except Exception as e:
                self.log_test_result(
                    f"Cultural Deception - {culture}",
                    False,
                    f"Exception: {e}"
                )
        
        overall_success = success_count == total_tests
        self.log_test_result(
            "Cultural Deception Monitoring Overall",
            overall_success,
            f"{success_count}/{total_tests} cultural tests passed"
        )
        return overall_success
    
    async def test_batch_monitoring(self) -> bool:
        """Test batch deception monitoring."""
        try:
            # Create batch of test contents
            batch_contents = [
                TEST_DATA["defense"]["content"],
                TEST_DATA["intelligence"]["content"],
                TEST_DATA["business"]["content"],
                TEST_DATA["cybersecurity"]["content"],
                TEST_DATA["geopolitical"]["content"]
            ]
            
            payload = {
                "contents": batch_contents,
                "domain": "general",
                "language": "en",
                "monitoring_level": "standard",
                "parallel_processing": True
            }
            
            response = requests.post(
                f"{STRATEGIC_DECEPTION_BASE}/monitor-batch",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check batch response structure
                required_fields = [
                    "batch_id", "total_requests", "processed_requests",
                    "failed_requests", "overall_deception_score",
                    "critical_alerts", "high_severity_alerts", "results"
                ]
                
                success = all(field in data for field in required_fields)
                
                # Check if all requests were processed
                total_requests = data.get("total_requests", 0)
                processed_requests = data.get("processed_requests", 0)
                failed_requests = data.get("failed_requests", 0)
                
                details = f"Total: {total_requests}, Processed: {processed_requests}, Failed: {failed_requests}, Score: {data.get('overall_deception_score', 0):.3f}"
                
                self.log_test_result(
                    "Batch Monitoring",
                    success and failed_requests == 0,
                    details,
                    data
                )
                return success and failed_requests == 0
            else:
                self.log_test_result(
                    "Batch Monitoring",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "Batch Monitoring",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_dashboard_data(self) -> bool:
        """Test dashboard data endpoint."""
        try:
            payload = {
                "domain": None,
                "time_range_hours": 24,
                "severity_filter": None,
                "include_patterns": True
            }
            
            response = requests.post(
                f"{STRATEGIC_DECEPTION_BASE}/dashboard",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check dashboard response structure
                required_fields = [
                    "dashboard_id", "time_range", "total_indicators",
                    "total_patterns", "severity_distribution", "domain_distribution",
                    "top_indicators", "top_patterns", "trend_analysis",
                    "alert_summary", "last_updated"
                ]
                
                success = all(field in data for field in required_fields)
                
                details = f"Dashboard ID: {data.get('dashboard_id')}, Indicators: {data.get('total_indicators')}, Patterns: {data.get('total_patterns')}"
                
                self.log_test_result(
                    "Dashboard Data",
                    success,
                    details,
                    data
                )
                return success
            else:
                self.log_test_result(
                    "Dashboard Data",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "Dashboard Data",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all strategic deception monitoring tests."""
        logger.info("🚀 Starting Strategic Deception Monitoring Tests")
        logger.info("=" * 60)
        
        # Test health check first
        health_ok = await self.test_health_check()
        if not health_ok:
            logger.error("❌ Health check failed. Stopping tests.")
            return self.get_test_summary()
        
        # Run individual tests
        await self.test_single_domain_monitoring("defense", TEST_DATA["defense"])
        await self.test_single_domain_monitoring("intelligence", TEST_DATA["intelligence"])
        await self.test_single_domain_monitoring("business", TEST_DATA["business"])
        await self.test_single_domain_monitoring("cybersecurity", TEST_DATA["cybersecurity"])
        await self.test_single_domain_monitoring("geopolitical", TEST_DATA["geopolitical"])
        
        # Run specialized tests
        await self.test_domain_specific_endpoints()
        await self.test_cultural_deception_monitoring()
        await self.test_batch_monitoring()
        await self.test_dashboard_data()
        
        # Generate summary
        summary = self.get_test_summary()
        
        logger.info("=" * 60)
        logger.info("🏁 Strategic Deception Monitoring Tests Complete")
        logger.info(f"Total Tests: {summary['total_tests']}")
        logger.info(f"Passed: {summary['passed_tests']}")
        logger.info(f"Failed: {summary['failed_tests']}")
        logger.info(f"Success Rate: {summary['success_rate']:.1f}%")
        logger.info(f"Total Time: {summary['total_time']:.2f} seconds")
        
        return summary
    
    def get_test_summary(self) -> Dict[str, Any]:
        """Get test summary statistics."""
        end_time = datetime.now()
        total_time = (end_time - self.start_time).total_seconds()
        
        passed_tests = sum(1 for result in self.test_results if result["success"])
        total_tests = len(self.test_results)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "total_time": total_time,
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "test_results": self.test_results
        }

async def main():
    """Main test function."""
    try:
        # Initialize tester
        tester = StrategicDeceptionTester()
        
        # Run all tests
        summary = await tester.run_all_tests()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"Test/results/strategic_deception_test_results_{timestamp}.json"
        
        # Ensure results directory exists
        import os
        os.makedirs("Test/results", exist_ok=True)
        
        with open(results_file, "w") as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"📄 Test results saved to: {results_file}")
        
        # Exit with appropriate code
        if summary["success_rate"] >= 80:
            logger.info("✅ Tests passed with acceptable success rate")
            return 0
        else:
            logger.error("❌ Tests failed to meet success rate threshold")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))
