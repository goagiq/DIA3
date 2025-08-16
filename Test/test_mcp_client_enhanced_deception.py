#!/usr/bin/env python3
"""
MCP Client Test for Enhanced Deception Detection

This script tests the MCP client communication with the enhanced deception detection system.
"""

import asyncio
import json
import time
from datetime import datetime
from loguru import logger

# Test configuration
MCP_SERVER_URL = "http://localhost:8003/mcp"


class MCPClientTester:
    """Test class for MCP client communication."""
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
    
    def log_test_result(self, test_name: str, success: bool, details: str = ""):
        """Log test result."""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} {test_name}: {details}")
    
    async def test_mcp_server_health(self):
        """Test MCP server health."""
        try:
            import requests
            
            # Test basic MCP endpoint
            response = requests.get(f"{MCP_SERVER_URL}/health", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                details += f", Service: {data.get('service', 'unknown')}"
            
            self.log_test_result("MCP Server Health", success, details)
            return success
            
        except Exception as e:
            self.log_test_result("MCP Server Health", False, f"Exception: {str(e)}")
            return False
    
    async def test_enhanced_deception_detection_health(self):
        """Test enhanced deception detection health through MCP."""
        try:
            import requests
            
            # Test enhanced deception detection health
            response = requests.get("http://localhost:8000/enhanced-deception-detection/health", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                details += f", Engine: {data.get('engine_status', 'unknown')}"
            
            self.log_test_result("Enhanced Deception Detection Health", success, details)
            return success
            
        except Exception as e:
            self.log_test_result("Enhanced Deception Detection Health", False, f"Exception: {str(e)}")
            return False
    
    async def test_art_of_war_techniques(self):
        """Test Art of War techniques endpoint."""
        try:
            import requests
            
            response = requests.get("http://localhost:8000/enhanced-deception-detection/art-of-war-techniques", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                techniques = response.json()
                details += f", Techniques: {len(techniques)}"
            
            self.log_test_result("Art of War Techniques", success, details)
            return success
            
        except Exception as e:
            self.log_test_result("Art of War Techniques", False, f"Exception: {str(e)}")
            return False
    
    async def test_cultural_patterns(self):
        """Test cultural patterns endpoint."""
        try:
            import requests
            
            response = requests.get("http://localhost:8000/enhanced-deception-detection/cultural-patterns", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                patterns = response.json()
                details += f", Languages: {len(patterns)}"
            
            self.log_test_result("Cultural Patterns", success, details)
            return success
            
        except Exception as e:
            self.log_test_result("Cultural Patterns", False, f"Exception: {str(e)}")
            return False
    
    async def test_deception_analysis(self):
        """Test deception analysis endpoint."""
        try:
            import requests
            
            # Test text with Art of War deception
            test_text = "We are reducing our military capabilities and cutting defense spending."
            
            payload = {
                "content": test_text,
                "domain": "defense",
                "language": "en",
                "include_art_of_war": True,
                "include_cultural": True,
                "include_domain_specific": True,
                "include_linguistic": True,
                "include_strategic": True
            }
            
            response = requests.post("http://localhost:8000/enhanced-deception-detection/analyze", json=payload, timeout=30)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                indicators = data.get('indicators_detected', 0)
                score = data.get('overall_deception_score', 0.0)
                details += f", Indicators: {indicators}, Score: {score:.2f}"
            
            self.log_test_result("Deception Analysis", success, details)
            return success
            
        except Exception as e:
            self.log_test_result("Deception Analysis", False, f"Exception: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Run all MCP client tests."""
        logger.info("🚀 Starting MCP Client Tests for Enhanced Deception Detection")
        logger.info("=" * 80)
        
        # Test MCP server health
        await self.test_mcp_server_health()
        await asyncio.sleep(1)
        
        # Test enhanced deception detection health
        await self.test_enhanced_deception_detection_health()
        await asyncio.sleep(1)
        
        # Test Art of War techniques
        await self.test_art_of_war_techniques()
        await asyncio.sleep(1)
        
        # Test cultural patterns
        await self.test_cultural_patterns()
        await asyncio.sleep(1)
        
        # Test deception analysis
        await self.test_deception_analysis()
        
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
        logger.info("📊 MCP Client Test Summary")
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
        results_file = f"mcp_client_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
            logger.info("\n🎉 All MCP client tests passed! Enhanced deception detection system is working correctly.")
        else:
            logger.info(f"\n⚠️ {failed_tests} tests failed. Please check the failed tests above.")


async def main():
    """Main test function."""
    tester = MCPClientTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    # Wait for server to start
    logger.info("⏳ Waiting 30 seconds for server to start...")
    time.sleep(30)
    
    # Run tests
    asyncio.run(main())
