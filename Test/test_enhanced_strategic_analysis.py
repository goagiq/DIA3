#!/usr/bin/env python3
"""
Enhanced Strategic Analysis Test Script

This script tests the enhanced strategic analysis capabilities based on The Art of War principles,
covering all supported domains: defense, intelligence, business, cybersecurity, geopolitical, etc.
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any

# Test configuration
BASE_URL = "http://127.0.0.1:8003"
API_ENDPOINTS = {
    "health": f"{BASE_URL}/enhanced-strategic/health",
    "analyze": f"{BASE_URL}/enhanced-strategic/analyze",
    "analyze_defense": f"{BASE_URL}/enhanced-strategic/analyze-defense",
    "analyze_intelligence": f"{BASE_URL}/enhanced-strategic/analyze-intelligence",
    "analyze_business": f"{BASE_URL}/enhanced-strategic/analyze-business",
    "analyze_cybersecurity": f"{BASE_URL}/enhanced-strategic/analyze-cybersecurity",
    "analyze_geopolitical": f"{BASE_URL}/enhanced-strategic/analyze-geopolitical",
    "analyze_financial": f"{BASE_URL}/enhanced-strategic/analyze-financial",
    "analyze_healthcare": f"{BASE_URL}/enhanced-strategic/analyze-healthcare",
    "analyze_energy": f"{BASE_URL}/enhanced-strategic/analyze-energy",
    "analyze_transportation": f"{BASE_URL}/enhanced-strategic/analyze-transportation",
    "analyze_critical_infrastructure": f"{BASE_URL}/enhanced-strategic/analyze-critical-infrastructure",
    "domains": f"{BASE_URL}/enhanced-strategic/domains",
    "summary": f"{BASE_URL}/enhanced-strategic/summary"
}


class EnhancedStrategicAnalysisTester:
    """Test class for enhanced strategic analysis capabilities."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.test_results = []
        self.session = None
    
    async def setup_session(self):
        """Setup HTTP session for testing."""
        try:
            import aiohttp
            self.session = aiohttp.ClientSession()
            print("✅ HTTP session created")
        except ImportError:
            print("⚠️ aiohttp not available, using requests")
            self.session = None
    
    async def cleanup_session(self):
        """Cleanup HTTP session."""
        if self.session:
            await self.session.close()
            print("✅ HTTP session closed")
    
    async def make_request(self, method: str, url: str, data: Dict = None) -> Dict:
        """Make HTTP request."""
        try:
            if self.session:
                if method.upper() == "GET":
                    async with self.session.get(url) as response:
                        return await response.json()
                elif method.upper() == "POST":
                    async with self.session.post(url, json=data) as response:
                        return await response.json()
            else:
                import requests
                if method.upper() == "GET":
                    response = requests.get(url)
                elif method.upper() == "POST":
                    response = requests.post(url, json=data)
                return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def log_test_result(self, test_name: str, success: bool, details: str = "", data: Dict = None):
        """Log test result."""
        result = {
            "test_name": test_name,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "details": details,
            "data": data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
    
    async def test_health_check(self):
        """Test health check endpoint."""
        print("\n🔍 Testing Enhanced Strategic Analysis Health Check")
        print("=" * 60)
        
        try:
            result = await self.make_request("GET", API_ENDPOINTS["health"])
            
            if "status" in result and result["status"] == "healthy":
                self.log_test_result("Health Check", True, "Service is healthy", result)
            else:
                self.log_test_result("Health Check", False, f"Service not healthy: {result}", result)
                
        except Exception as e:
            self.log_test_result("Health Check", False, f"Error: {e}")
    
    async def test_supported_domains(self):
        """Test supported domains endpoint."""
        print("\n🔍 Testing Supported Domains")
        print("=" * 60)
        
        try:
            result = await self.make_request("GET", API_ENDPOINTS["domains"])
            
            if "domains" in result and isinstance(result["domains"], list):
                domains = result["domains"]
                self.log_test_result("Supported Domains", True, f"Found {len(domains)} domains", result)
                
                # Check for expected domains
                expected_domains = [
                    "defense", "intelligence", "business", "cybersecurity",
                    "geopolitical", "financial", "healthcare", "energy",
                    "transportation", "critical_infrastructure"
                ]
                
                missing_domains = [d for d in expected_domains if d not in domains]
                if missing_domains:
                    self.log_test_result("Domain Coverage", False, f"Missing domains: {missing_domains}")
                else:
                    self.log_test_result("Domain Coverage", True, "All expected domains supported")
                    
            else:
                self.log_test_result("Supported Domains", False, f"Invalid response: {result}", result)
                
        except Exception as e:
            self.log_test_result("Supported Domains", False, f"Error: {e}")
    
    async def test_defense_analysis(self):
        """Test defense domain analysis."""
        print("\n🔍 Testing Defense Domain Analysis")
        print("=" * 60)
        
        test_content = """
        Russia has announced a reduction in military spending while maintaining 
        strategic nuclear capabilities. The government claims to be withdrawing 
        troops from border regions, but intelligence sources indicate continued 
        military modernization and troop movements. Bilateral defense agreements 
        have been proposed with neighboring countries, potentially undermining 
        existing multilateral security arrangements.
        """
        
        try:
            result = await self.make_request("POST", API_ENDPOINTS["analyze_defense"], {
                "content": test_content,
                "domain": "defense",
                "language": "en",
                "analysis_depth": "comprehensive"
            })
            
            if "analysis_id" in result and "principles_detected" in result:
                principles_count = len(result["principles_detected"])
                moves_count = len(result["strategic_moves"])
                confidence = result.get("confidence_score", 0)
                
                self.log_test_result("Defense Analysis", True, 
                    f"Detected {principles_count} principles, {moves_count} moves, confidence: {confidence:.2f}", 
                    result)
                
                # Check for specific Art of War principles
                principles_found = [p["translation"] for p in result["principles_detected"]]
                expected_principles = ["Show inability when able", "Show disuse when using", "Separate when united"]
                
                found_expected = [p for p in expected_principles if any(p in found for found in principles_found)]
                if found_expected:
                    self.log_test_result("Defense Principles Detection", True, f"Found expected principles: {found_expected}")
                else:
                    self.log_test_result("Defense Principles Detection", False, "No expected principles detected")
                    
            else:
                self.log_test_result("Defense Analysis", False, f"Invalid response: {result}", result)
                
        except Exception as e:
            self.log_test_result("Defense Analysis", False, f"Error: {e}")
    
    async def test_intelligence_analysis(self):
        """Test intelligence domain analysis."""
        print("\n🔍 Testing Intelligence Domain Analysis")
        print("=" * 60)
        
        test_content = """
        Intelligence sources report increased information collection activities 
        in the region. The government has announced the termination of certain 
        surveillance operations while maintaining covert intelligence networks. 
        Bilateral information sharing agreements have been proposed, potentially 
        creating gaps in multilateral intelligence cooperation frameworks.
        """
        
        try:
            result = await self.make_request("POST", API_ENDPOINTS["analyze_intelligence"], {
                "content": test_content,
                "domain": "intelligence",
                "language": "en",
                "analysis_depth": "comprehensive"
            })
            
            if "analysis_id" in result and "principles_detected" in result:
                principles_count = len(result["principles_detected"])
                moves_count = len(result["strategic_moves"])
                confidence = result.get("confidence_score", 0)
                
                self.log_test_result("Intelligence Analysis", True, 
                    f"Detected {principles_count} principles, {moves_count} moves, confidence: {confidence:.2f}", 
                    result)
                    
            else:
                self.log_test_result("Intelligence Analysis", False, f"Invalid response: {result}", result)
                
        except Exception as e:
            self.log_test_result("Intelligence Analysis", False, f"Error: {e}")
    
    async def test_business_analysis(self):
        """Test business domain analysis."""
        print("\n🔍 Testing Business Domain Analysis")
        print("=" * 60)
        
        test_content = """
        The company has announced market exit from certain regions while 
        secretly expanding operations through subsidiaries. Strategic partnerships 
        have been proposed that appear beneficial but contain hidden competitive 
        advantages. The firm claims to be reducing market presence while 
        actually strengthening competitive positioning through alternative channels.
        """
        
        try:
            result = await self.make_request("POST", API_ENDPOINTS["analyze_business"], {
                "content": test_content,
                "domain": "business",
                "language": "en",
                "analysis_depth": "comprehensive"
            })
            
            if "analysis_id" in result and "principles_detected" in result:
                principles_count = len(result["principles_detected"])
                moves_count = len(result["strategic_moves"])
                confidence = result.get("confidence_score", 0)
                
                self.log_test_result("Business Analysis", True, 
                    f"Detected {principles_count} principles, {moves_count} moves, confidence: {confidence:.2f}", 
                    result)
                    
            else:
                self.log_test_result("Business Analysis", False, f"Invalid response: {result}", result)
                
        except Exception as e:
            self.log_test_result("Business Analysis", False, f"Error: {e}")
    
    async def test_cybersecurity_analysis(self):
        """Test cybersecurity domain analysis."""
        print("\n🔍 Testing Cybersecurity Domain Analysis")
        print("=" * 60)
        
        test_content = """
        The organization has announced the removal of certain security tools 
        while secretly deploying advanced threat detection systems. Cyber 
        collaboration offers have been made that appear beneficial but may 
        create security gaps in existing defense frameworks. The company 
        claims to be reducing security monitoring while actually enhancing 
        cyber defense capabilities through alternative means.
        """
        
        try:
            result = await self.make_request("POST", API_ENDPOINTS["analyze_cybersecurity"], {
                "content": test_content,
                "domain": "cybersecurity",
                "language": "en",
                "analysis_depth": "comprehensive"
            })
            
            if "analysis_id" in result and "principles_detected" in result:
                principles_count = len(result["principles_detected"])
                moves_count = len(result["strategic_moves"])
                confidence = result.get("confidence_score", 0)
                
                self.log_test_result("Cybersecurity Analysis", True, 
                    f"Detected {principles_count} principles, {moves_count} moves, confidence: {confidence:.2f}", 
                    result)
                    
            else:
                self.log_test_result("Cybersecurity Analysis", False, f"Invalid response: {result}", result)
                
        except Exception as e:
            self.log_test_result("Cybersecurity Analysis", False, f"Error: {e}")
    
    async def test_geopolitical_analysis(self):
        """Test geopolitical domain analysis."""
        print("\n🔍 Testing Geopolitical Domain Analysis")
        print("=" * 60)
        
        test_content = """
        The government has announced withdrawal from international agreements 
        while secretly maintaining diplomatic influence through alternative 
        channels. Bilateral trade deals have been proposed that appear 
        mutually beneficial but contain strategic advantages. The state 
        claims to be reducing international engagement while actually 
        strengthening geopolitical positioning through covert means.
        """
        
        try:
            result = await self.make_request("POST", API_ENDPOINTS["analyze_geopolitical"], {
                "content": test_content,
                "domain": "geopolitical",
                "language": "en",
                "analysis_depth": "comprehensive"
            })
            
            if "analysis_id" in result and "principles_detected" in result:
                principles_count = len(result["principles_detected"])
                moves_count = len(result["strategic_moves"])
                confidence = result.get("confidence_score", 0)
                
                self.log_test_result("Geopolitical Analysis", True, 
                    f"Detected {principles_count} principles, {moves_count} moves, confidence: {confidence:.2f}", 
                    result)
                    
            else:
                self.log_test_result("Geopolitical Analysis", False, f"Invalid response: {result}", result)
                
        except Exception as e:
            self.log_test_result("Geopolitical Analysis", False, f"Error: {e}")
    
    async def test_batch_analysis(self):
        """Test batch analysis capabilities."""
        print("\n🔍 Testing Batch Analysis")
        print("=" * 60)
        
        batch_requests = [
            {
                "content": "Russia announces military spending reduction while modernizing forces.",
                "domain": "defense",
                "language": "en",
                "analysis_depth": "comprehensive"
            },
            {
                "content": "Company claims market exit while expanding through subsidiaries.",
                "domain": "business",
                "language": "en",
                "analysis_depth": "comprehensive"
            },
            {
                "content": "Organization removes security tools while deploying advanced detection.",
                "domain": "cybersecurity",
                "language": "en",
                "analysis_depth": "comprehensive"
            }
        ]
        
        try:
            result = await self.make_request("POST", f"{BASE_URL}/enhanced-strategic/analyze-batch", batch_requests)
            
            if "batch_results" in result and "total_items" in result:
                total_items = result["total_items"]
                successful = result["successful_analyses"]
                failed = result["failed_analyses"]
                
                self.log_test_result("Batch Analysis", True, 
                    f"Processed {total_items} items: {successful} successful, {failed} failed", 
                    result)
                    
            else:
                self.log_test_result("Batch Analysis", False, f"Invalid response: {result}", result)
                
        except Exception as e:
            self.log_test_result("Batch Analysis", False, f"Error: {e}")
    
    async def test_summary(self):
        """Test summary endpoint."""
        print("\n🔍 Testing Summary Endpoint")
        print("=" * 60)
        
        try:
            result = await self.make_request("GET", API_ENDPOINTS["summary"])
            
            if "service" in result and "capabilities" in result:
                capabilities_count = len(result["capabilities"])
                domains_count = len(result["supported_domains"])
                
                self.log_test_result("Summary", True, 
                    f"Service: {result['service']}, {capabilities_count} capabilities, {domains_count} domains", 
                    result)
                    
            else:
                self.log_test_result("Summary", False, f"Invalid response: {result}", result)
                
        except Exception as e:
            self.log_test_result("Summary", False, f"Error: {e}")
    
    async def run_all_tests(self):
        """Run all enhanced strategic analysis tests."""
        print("🎯 ENHANCED STRATEGIC ANALYSIS TESTING")
        print("=" * 80)
        print("Testing comprehensive strategic analysis based on The Art of War principles")
        print("=" * 80)
        
        # Setup
        await self.setup_session()
        
        try:
            # Run tests
            await self.test_health_check()
            await self.test_supported_domains()
            await self.test_defense_analysis()
            await self.test_intelligence_analysis()
            await self.test_business_analysis()
            await self.test_cybersecurity_analysis()
            await self.test_geopolitical_analysis()
            await self.test_batch_analysis()
            await self.test_summary()
            
        finally:
            # Cleanup
            await self.cleanup_session()
        
        # Generate test report
        self.generate_test_report()
    
    def generate_test_report(self):
        """Generate comprehensive test report."""
        print("\n📊 ENHANCED STRATEGIC ANALYSIS TEST REPORT")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test_name']}: {result['details']}")
        
        print("\n✅ PASSED TESTS:")
        for result in self.test_results:
            if result["success"]:
                print(f"  - {result['test_name']}: {result['details']}")
        
        # Save detailed results
        report_file = f"enhanced_strategic_analysis_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                "test_summary": {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "success_rate": (passed_tests/total_tests)*100
                },
                "test_results": self.test_results,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\n📁 Detailed test report saved to: {report_file}")
        
        if failed_tests == 0:
            print("\n🎉 All enhanced strategic analysis tests passed!")
        else:
            print(f"\n⚠️ {failed_tests} tests failed. Please check the detailed report.")


async def main():
    """Main test function."""
    tester = EnhancedStrategicAnalysisTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    print("🚀 Starting Enhanced Strategic Analysis Testing")
    print("Make sure the server is running on http://127.0.0.1:8003")
    print("=" * 80)
    
    # Wait a moment for server startup
    time.sleep(2)
    
    # Run tests
    asyncio.run(main())
