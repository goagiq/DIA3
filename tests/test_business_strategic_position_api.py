#!/usr/bin/env python3
"""
Simple API test for Business Strategic Position Analysis endpoint.
Tests the endpoint without importing internal modules.
"""

import asyncio
import json
import sys
from datetime import datetime
import httpx


class BusinessStrategicPositionAPITester:
    """Simple API test suite for business strategic position analysis."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8004"):
        self.base_url = base_url
        self.results = {
            "test_timestamp": datetime.now().isoformat(),
            "base_url": base_url,
            "tests": [],
            "summary": {}
        }
    
    async def test_health_check(self) -> bool:
        """Test system health check."""
        print("🔍 Testing system health check...")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/health")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Health check passed: {data.get('status', 'unknown')}")
                    
                    self.results["tests"].append({
                        "test": "health_check",
                        "status": "passed",
                        "response": data
                    })
                    return True
                else:
                    print(f"❌ Health check failed: {response.status_code}")
                    
                    self.results["tests"].append({
                        "test": "health_check",
                        "status": "failed",
                        "error": f"HTTP {response.status_code}"
                    })
                    return False
                    
        except Exception as e:
            print(f"❌ Health check error: {e}")
            
            self.results["tests"].append({
                "test": "health_check",
                "status": "error",
                "error": str(e)
            })
            return False
    
    async def test_business_strategic_position_analysis(self) -> bool:
        """Test the main business strategic position analysis endpoint."""
        print("\n🎯 Testing Business Strategic Position Analysis...")
        
        test_content = "Analyze our business strategic position in current market conditions including competitive landscape, market opportunities, and strategic recommendations"
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                payload = {
                    "content": test_content,
                    "language": "en",
                    "model_preference": None,
                    "reflection_enabled": True,
                    "max_iterations": 3,
                    "confidence_threshold": 0.8
                }
                
                response = await client.post(
                    f"{self.base_url}/business/strategic-position-analysis",
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Analyze results
                    success = data.get("success", False)
                    components = data.get("components", [])
                    summary = data.get("summary", {})
                    
                    print(f"✅ Business strategic analysis completed")
                    print(f"   - Success: {success}")
                    print(f"   - Components: {len(components)}")
                    print(f"   - Analysis Status: {summary.get('analysis_status', 'unknown')}")
                    
                    # Check individual components
                    successful_components = [
                        comp for comp in components 
                        if comp.get("status") == "success"
                    ]
                    
                    print(f"   - Successful Components: {len(successful_components)}")
                    
                    for comp in components:
                        comp_name = comp.get("name", "unknown")
                        comp_status = comp.get("status", "unknown")
                        print(f"     • {comp_name}: {comp_status}")
                    
                    # Check if we have the key components
                    component_names = [comp.get("name", "") for comp in components]
                    expected_components = [
                        "art_of_war_scenario_analysis",
                        "multi_domain_strategic_analysis", 
                        "market_data_analysis",
                        "business_intelligence_analysis"
                    ]
                    
                    missing_components = [
                        name for name in expected_components 
                        if name not in component_names
                    ]
                    
                    if missing_components:
                        print(f"   - Missing Components: {missing_components}")
                    
                    self.results["tests"].append({
                        "test": "business_strategic_position_analysis",
                        "status": "passed" if success else "partial",
                        "response": {
                            "success": success,
                            "components_count": len(components),
                            "successful_components": len(successful_components),
                            "analysis_status": summary.get("analysis_status"),
                            "recommendations": summary.get("recommendations", []),
                            "component_names": component_names,
                            "missing_components": missing_components
                        }
                    })
                    
                    return success
                    
                else:
                    print(f"❌ Business strategic analysis failed: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
                    self.results["tests"].append({
                        "test": "business_strategic_position_analysis",
                        "status": "failed",
                        "error": f"HTTP {response.status_code}",
                        "response": response.text
                    })
                    return False
                    
        except Exception as e:
            print(f"❌ Business strategic analysis error: {e}")
            
            self.results["tests"].append({
                "test": "business_strategic_position_analysis",
                "status": "error",
                "error": str(e)
            })
            return False
    
    async def test_endpoint_documentation(self) -> bool:
        """Test if the endpoint is properly documented."""
        print("\n📚 Testing endpoint documentation...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test the root endpoint to see available endpoints
                response = await client.get(f"{self.base_url}/")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ API root endpoint accessible")
                    print(f"   - Name: {data.get('name', 'unknown')}")
                    print(f"   - Version: {data.get('version', 'unknown')}")
                    
                    self.results["tests"].append({
                        "test": "endpoint_documentation",
                        "status": "passed",
                        "response": data
                    })
                    return True
                else:
                    print(f"❌ API root endpoint failed: {response.status_code}")
                    
                    self.results["tests"].append({
                        "test": "endpoint_documentation",
                        "status": "failed",
                        "error": f"HTTP {response.status_code}"
                    })
                    return False
                    
        except Exception as e:
            print(f"❌ Endpoint documentation error: {e}")
            
            self.results["tests"].append({
                "test": "endpoint_documentation",
                "status": "error",
                "error": str(e)
            })
            return False
    
    def generate_summary(self):
        """Generate test summary."""
        total_tests = len(self.results["tests"])
        passed_tests = len([t for t in self.results["tests"] if t["status"] == "passed"])
        failed_tests = len([t for t in self.results["tests"] if t["status"] == "failed"])
        error_tests = len([t for t in self.results["tests"] if t["status"] == "error"])
        partial_tests = len([t for t in self.results["tests"] if t["status"] == "partial"])
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "partial": partial_tests,
            "success_rate": (passed_tests + partial_tests) / total_tests if total_tests > 0 else 0
        }
        
        print(f"\n📋 Test Summary:")
        print(f"   - Total Tests: {total_tests}")
        print(f"   - Passed: {passed_tests}")
        print(f"   - Partial: {partial_tests}")
        print(f"   - Failed: {failed_tests}")
        print(f"   - Errors: {error_tests}")
        print(f"   - Success Rate: {self.results['summary']['success_rate']:.1%}")
    
    def save_results(self):
        """Save test results to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Test/business_strategic_position_api_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n💾 Test results saved to: {filename}")
        return filename
    
    async def run_all_tests(self):
        """Run all tests."""
        print("🚀 Business Strategic Position Analysis API Test Suite")
        print("=" * 60)
        
        # Test 1: Health check
        health_ok = await self.test_health_check()
        
        if not health_ok:
            print("❌ System health check failed. Stopping tests.")
            return False
        
        # Test 2: Endpoint documentation
        await self.test_endpoint_documentation()
        
        # Test 3: Main business strategic position analysis endpoint
        await self.test_business_strategic_position_analysis()
        
        # Generate summary and save results
        self.generate_summary()
        self.save_results()
        
        return self.results["summary"]["success_rate"] > 0.5


async def main():
    """Main test function."""
    tester = BusinessStrategicPositionAPITester()
    
    success = await tester.run_all_tests()
    
    if success:
        print("\n✅ API test suite completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ API test suite failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
