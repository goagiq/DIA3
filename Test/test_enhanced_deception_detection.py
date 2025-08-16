#!/usr/bin/env python3
"""
Test script for Enhanced Deception Detection System

This script tests the enhanced deception detection capabilities including:
- Art of War deception techniques
- Multi-domain support (defense, intelligence, business, cybersecurity, geopolitical)
- Cultural deception patterns
- Strategic misdirection detection
- Early warning indicators
- Real-time monitoring capabilities
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any, List
import requests
from loguru import logger

# Test configuration
BASE_URL = "http://localhost:8003"
ENHANCED_DECEPTION_BASE = f"{BASE_URL}/enhanced-deception-detection"

# Test data
TEST_TEXTS = {
    "art_of_war": [
        "We are reducing our military capabilities and cutting defense spending.",
        "We are discontinuing our involvement in the region, but we continue to maintain unofficial contacts.",
        "We have no interest in this matter, but we are actively participating behind the scenes.",
        "We are very close to the situation and have full control, but actually we are far away.",
        "This is an exceptionally generous offer that will benefit everyone greatly.",
        "We are exploiting the chaos and disorder to advance our interests.",
        "We are offering bilateral deals that will strengthen individual partnerships.",
        "This is a sudden announcement that will catch everyone off guard."
    ],
    "cultural": {
        "chinese": [
            "我们致力于和谐发展，促进和平合作。传统友谊和历史文化纽带将指引我们前进。稳定和安全是我们的共同目标。",
            "发展进步现代化是我们的首要任务。传统文化和历史遗产是我们的宝贵财富。"
        ],
        "russian": [
            "Мы стремимся к безопасности и стабильности. Развитие и прогресс - наши общие цели.",
            "Традиции и культура объединяют нас. Защита и оборона - наш приоритет."
        ]
    },
    "domain_specific": {
        "defense": [
            "We are reducing our military capabilities and cutting defense spending while maintaining offensive capabilities.",
            "Our posture is purely defensive and peaceful, but we have aggressive capabilities."
        ],
        "intelligence": [
            "We are completely transparent and open, but we maintain classified operations.",
            "We share all information, but we conceal sensitive data."
        ],
        "business": [
            "Our company is highly profitable and growing, but we have significant losses.",
            "We are financially strong and stable, but we face serious risks."
        ],
        "cybersecurity": [
            "Our systems are completely secure and protected, but we have vulnerabilities.",
            "There are no threats or risks, but we are under active attack."
        ],
        "geopolitical": [
            "We have peaceful intentions and seek cooperation, but we are preparing for conflict.",
            "We have no plans for aggression, but we are actively planning military operations."
        ]
    },
    "linguistic": [
        "Perhaps we might consider this proposal, but I'm not entirely sure about the details.",
        "To be honest, this is completely true and you can trust me.",
        "Experts say this is the best approach and everyone knows it's right.",
        "This is an immediate emergency that requires urgent action right away."
    ]
}


class EnhancedDeceptionDetectionTester:
    """Test class for enhanced deception detection system."""
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
    
    def log_test_result(self, test_name: str, success: bool, details: str = "", response: Dict[str, Any] = None):
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
    
    async def test_health_check(self):
        """Test health check endpoint."""
        try:
            response = requests.get(f"{ENHANCED_DECEPTION_BASE}/health", timeout=30)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                details += f", Engine: {data.get('engine_status', 'unknown')}"
            
            self.log_test_result("Health Check", success, details, response.json() if success else None)
            return success
            
        except Exception as e:
            self.log_test_result("Health Check", False, f"Exception: {str(e)}")
            return False
    
    async def test_service_summary(self):
        """Test service summary endpoint."""
        try:
            response = requests.get(f"{ENHANCED_DECEPTION_BASE}/summary", timeout=30)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                details += f", Service: {data.get('service_name', 'unknown')}"
            
            self.log_test_result("Service Summary", success, details, response.json() if success else None)
            return success
            
        except Exception as e:
            self.log_test_result("Service Summary", False, f"Exception: {str(e)}")
            return False
    
    async def test_supported_domains(self):
        """Test supported domains endpoint."""
        try:
            response = requests.get(f"{ENHANCED_DECEPTION_BASE}/domains", timeout=30)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                domains = response.json()
                details += f", Domains: {len(domains)} ({', '.join(domains)})"
            
            self.log_test_result("Supported Domains", success, details, response.json() if success else None)
            return success
            
        except Exception as e:
            self.log_test_result("Supported Domains", False, f"Exception: {str(e)}")
            return False
    
    async def test_art_of_war_techniques(self):
        """Test Art of War techniques endpoint."""
        try:
            response = requests.get(f"{ENHANCED_DECEPTION_BASE}/art-of-war-techniques", timeout=30)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                techniques = response.json()
                details += f", Techniques: {len(techniques)}"
            
            self.log_test_result("Art of War Techniques", success, details, response.json() if success else None)
            return success
            
        except Exception as e:
            self.log_test_result("Art of War Techniques", False, f"Exception: {str(e)}")
            return False
    
    async def test_cultural_patterns(self):
        """Test cultural patterns endpoint."""
        try:
            response = requests.get(f"{ENHANCED_DECEPTION_BASE}/cultural-patterns", timeout=30)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                patterns = response.json()
                details += f", Languages: {len(patterns)}"
            
            self.log_test_result("Cultural Patterns", success, details, response.json() if success else None)
            return success
            
        except Exception as e:
            self.log_test_result("Cultural Patterns", False, f"Exception: {str(e)}")
            return False
    
    async def test_domain_capabilities(self, domain: str):
        """Test domain capabilities endpoint."""
        try:
            response = requests.get(f"{ENHANCED_DECEPTION_BASE}/domain-capabilities/{domain}", timeout=30)
            success = response.status_code == 200
            details = f"Domain: {domain}, Status: {response.status_code}"
            
            if success:
                capabilities = response.json()
                details += f", Art of War: {len(capabilities.get('art_of_war_techniques', []))}"
            
            self.log_test_result(f"Domain Capabilities ({domain})", success, details, response.json() if success else None)
            return success
            
        except Exception as e:
            self.log_test_result(f"Domain Capabilities ({domain})", False, f"Exception: {str(e)}")
            return False
    
    async def test_comprehensive_analysis(self, text: str, domain: str = "general"):
        """Test comprehensive deception analysis."""
        try:
            payload = {
                "content": text,
                "domain": domain,
                "language": "en",
                "include_art_of_war": True,
                "include_cultural": True,
                "include_domain_specific": True,
                "include_linguistic": True,
                "include_strategic": True
            }
            
            response = requests.post(f"{ENHANCED_DECEPTION_BASE}/analyze", json=payload, timeout=30)
            success = response.status_code == 200
            details = f"Domain: {domain}, Status: {response.status_code}"
            
            if success:
                data = response.json()
                indicators = data.get('indicators_detected', 0)
                patterns = data.get('patterns_detected', 0)
                score = data.get('overall_deception_score', 0.0)
                details += f", Indicators: {indicators}, Patterns: {patterns}, Score: {score:.2f}"
            
            self.log_test_result(f"Comprehensive Analysis ({domain})", success, details, response.json() if success else None)
            return success
            
        except Exception as e:
            self.log_test_result(f"Comprehensive Analysis ({domain})", False, f"Exception: {str(e)}")
            return False
    
    async def test_domain_specific_analysis(self, domain: str, text: str):
        """Test domain-specific analysis."""
        try:
            endpoint = f"{ENHANCED_DECEPTION_BASE}/analyze-{domain}"
            payload = {
                "content": text,
                "domain": domain,
                "language": "en",
                "include_art_of_war": True,
                "include_cultural": True,
                "include_domain_specific": True,
                "include_linguistic": True,
                "include_strategic": True
            }
            
            response = requests.post(endpoint, json=payload, timeout=30)
            success = response.status_code == 200
            details = f"Domain: {domain}, Status: {response.status_code}"
            
            if success:
                data = response.json()
                indicators = data.get('indicators_detected', 0)
                score = data.get('overall_deception_score', 0.0)
                details += f", Indicators: {indicators}, Score: {score:.2f}"
            
            self.log_test_result(f"Domain Analysis ({domain})", success, details, response.json() if success else None)
            return success
            
        except Exception as e:
            self.log_test_result(f"Domain Analysis ({domain})", False, f"Exception: {str(e)}")
            return False
    
    async def test_batch_analysis(self):
        """Test batch analysis endpoint."""
        try:
            payload = {
                "contents": TEST_TEXTS["linguistic"][:3],  # Test with 3 texts
                "domain": "general",
                "language": "en",
                "include_art_of_war": True,
                "include_cultural": True,
                "include_domain_specific": True,
                "include_linguistic": True,
                "include_strategic": True,
                "parallel_processing": True
            }
            
            response = requests.post(f"{ENHANCED_DECEPTION_BASE}/analyze-batch", json=payload, timeout=60)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                total = data.get('total_requests', 0)
                processed = data.get('processed_requests', 0)
                failed = data.get('failed_requests', 0)
                details += f", Total: {total}, Processed: {processed}, Failed: {failed}"
            
            self.log_test_result("Batch Analysis", success, details, response.json() if success else None)
            return success
            
        except Exception as e:
            self.log_test_result("Batch Analysis", False, f"Exception: {str(e)}")
            return False
    
    async def test_art_of_war_detection(self):
        """Test Art of War deception detection."""
        for i, text in enumerate(TEST_TEXTS["art_of_war"]):
            await self.test_comprehensive_analysis(text, "general")
            await asyncio.sleep(1)  # Small delay between requests
    
    async def test_cultural_detection(self):
        """Test cultural deception detection."""
        for language, texts in TEST_TEXTS["cultural"].items():
            for text in texts:
                payload = {
                    "content": text,
                    "domain": "general",
                    "language": language,
                    "include_art_of_war": True,
                    "include_cultural": True,
                    "include_domain_specific": False,
                    "include_linguistic": True,
                    "include_strategic": True
                }
                
                try:
                    response = requests.post(f"{ENHANCED_DECEPTION_BASE}/analyze", json=payload, timeout=30)
                    success = response.status_code == 200
                    details = f"Language: {language}, Status: {response.status_code}"
                    
                    if success:
                        data = response.json()
                        indicators = data.get('indicators_detected', 0)
                        cultural_patterns = data.get('cultural_patterns_detected', [])
                        details += f", Indicators: {indicators}, Cultural: {len(cultural_patterns)}"
                    
                    self.log_test_result(f"Cultural Detection ({language})", success, details, response.json() if success else None)
                    
                except Exception as e:
                    self.log_test_result(f"Cultural Detection ({language})", False, f"Exception: {str(e)}")
                
                await asyncio.sleep(1)
    
    async def test_domain_specific_detection(self):
        """Test domain-specific deception detection."""
        for domain, texts in TEST_TEXTS["domain_specific"].items():
            for text in texts:
                await self.test_domain_specific_analysis(domain, text)
                await asyncio.sleep(1)
    
    async def run_all_tests(self):
        """Run all tests."""
        logger.info("🚀 Starting Enhanced Deception Detection System Tests")
        logger.info("=" * 80)
        
        # Test basic endpoints
        await self.test_health_check()
        await asyncio.sleep(1)
        
        await self.test_service_summary()
        await asyncio.sleep(1)
        
        await self.test_supported_domains()
        await asyncio.sleep(1)
        
        await self.test_art_of_war_techniques()
        await asyncio.sleep(1)
        
        await self.test_cultural_patterns()
        await asyncio.sleep(1)
        
        # Test domain capabilities
        domains = ["defense", "intelligence", "business", "cybersecurity", "geopolitical"]
        for domain in domains:
            await self.test_domain_capabilities(domain)
            await asyncio.sleep(1)
        
        # Test comprehensive analysis
        await self.test_comprehensive_analysis(TEST_TEXTS["linguistic"][0], "general")
        await asyncio.sleep(1)
        
        # Test Art of War detection
        logger.info("Testing Art of War deception detection...")
        await self.test_art_of_war_detection()
        
        # Test cultural detection
        logger.info("Testing cultural deception detection...")
        await self.test_cultural_detection()
        
        # Test domain-specific detection
        logger.info("Testing domain-specific deception detection...")
        await self.test_domain_specific_detection()
        
        # Test batch analysis
        await self.test_batch_analysis()
        
        # Generate test summary
        self.generate_test_summary()
    
    def generate_test_summary(self):
        """Generate test summary."""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        logger.info("=" * 80)
        logger.info("📊 Enhanced Deception Detection System Test Summary")
        logger.info("=" * 80)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests} ✅")
        logger.info(f"Failed: {failed_tests} ❌")
        logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        logger.info(f"Duration: {duration:.2f} seconds")
        
        if failed_tests > 0:
            logger.info("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    logger.info(f"  - {result['test_name']}: {result['details']}")
        
        # Save detailed results
        results_file = f"enhanced_deception_detection_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump({
                "test_summary": {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "success_rate": (passed_tests/total_tests)*100,
                    "duration_seconds": duration,
                    "start_time": self.start_time.isoformat(),
                    "end_time": end_time.isoformat()
                },
                "test_results": self.test_results
            }, f, indent=2)
        
        logger.info(f"\n📄 Detailed results saved to: {results_file}")
        
        if failed_tests == 0:
            logger.info("\n🎉 All tests passed! Enhanced deception detection system is working correctly.")
        else:
            logger.info(f"\n⚠️ {failed_tests} tests failed. Please check the failed tests above.")


async def main():
    """Main test function."""
    tester = EnhancedDeceptionDetectionTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    # Wait for server to start
    logger.info("⏳ Waiting 30 seconds for server to start...")
    time.sleep(30)
    
    # Run tests
    asyncio.run(main())
