#!/usr/bin/env python3
"""
Test script for Business Strategic Position Analysis endpoint.
Tests the comprehensive business strategic analysis functionality including:
- Art of War scenario analysis
- Multi-domain strategic analysis
- Market data analysis
- Business intelligence analysis
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path
import httpx

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class BusinessStrategicPositionAnalysisTester:
    """Test suite for business strategic position analysis."""
    
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
                    
                    self.results["tests"].append({
                        "test": "business_strategic_position_analysis",
                        "status": "passed" if success else "partial",
                        "response": {
                            "success": success,
                            "components_count": len(components),
                            "successful_components": len(successful_components),
                            "analysis_status": summary.get("analysis_status"),
                            "recommendations": summary.get("recommendations", [])
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
    
    async def test_art_of_war_scenario_analysis(self) -> bool:
        """Test Art of War scenario analysis directly."""
        print("\n⚔️ Testing Art of War Scenario Analysis...")
        
        try:
            from Test.art_of_war_scenario_analysis import ArtOfWarScenarioAnalysis
            
            analyzer = ArtOfWarScenarioAnalysis()
            results = analyzer.run_complete_analysis()
            
            if results:
                print("✅ Art of War scenario analysis completed")
                print(f"   - Primary Strategy: {results.get('primary_strategy', 'unknown')}")
                print(f"   - Secondary Strategy: {results.get('secondary_strategy', 'unknown')}")
                
                self.results["tests"].append({
                    "test": "art_of_war_scenario_analysis",
                    "status": "passed",
                    "response": {
                        "primary_strategy": results.get('primary_strategy'),
                        "secondary_strategy": results.get('secondary_strategy'),
                        "strategic_data": results.get('strategic_data', {})
                    }
                })
                return True
            else:
                print("❌ Art of War scenario analysis failed")
                
                self.results["tests"].append({
                    "test": "art_of_war_scenario_analysis",
                    "status": "failed",
                    "error": "No results returned"
                })
                return False
                
        except Exception as e:
            print(f"❌ Art of War scenario analysis error: {e}")
            
            self.results["tests"].append({
                "test": "art_of_war_scenario_analysis",
                "status": "error",
                "error": str(e)
            })
            return False
    
    async def test_multi_domain_strategic_analysis(self) -> bool:
        """Test multi-domain strategic analysis directly."""
        print("\n🌐 Testing Multi-Domain Strategic Analysis...")
        
        try:
            from src.core.multi_domain_strategic_analyzer import (
                MultiDomainStrategicAnalyzer, DomainType, AnalysisType
            )
            
            analyzer = MultiDomainStrategicAnalyzer()
            results = await analyzer.analyze_strategic_position(
                content="Analyze our business strategic position in current market conditions",
                domain=DomainType.BUSINESS,
                analysis_type=AnalysisType.COMPREHENSIVE,
                include_art_of_war=True,
                include_recommendations=True
            )
            
            if results:
                print("✅ Multi-domain strategic analysis completed")
                print(f"   - Domain: {results.get('metadata', {}).get('domain', 'unknown')}")
                print(f"   - Analysis Type: {results.get('metadata', {}).get('analysis_type', 'unknown')}")
                print(f"   - Components: {len(results.get('domain_analysis', {}))}")
                
                self.results["tests"].append({
                    "test": "multi_domain_strategic_analysis",
                    "status": "passed",
                    "response": {
                        "domain": results.get('metadata', {}).get('domain'),
                        "analysis_type": results.get('metadata', {}).get('analysis_type'),
                        "components_count": len(results.get('domain_analysis', {}))
                    }
                })
                return True
            else:
                print("❌ Multi-domain strategic analysis failed")
                
                self.results["tests"].append({
                    "test": "multi_domain_strategic_analysis",
                    "status": "failed",
                    "error": "No results returned"
                })
                return False
                
        except Exception as e:
            print(f"❌ Multi-domain strategic analysis error: {e}")
            
            self.results["tests"].append({
                "test": "multi_domain_strategic_analysis",
                "status": "error",
                "error": str(e)
            })
            return False
    
    async def test_market_data_analysis(self) -> bool:
        """Test market data analysis directly."""
        print("\n📊 Testing Market Data Analysis...")
        
        try:
            from src.agents.market_data_agent import MarketDataManager
            
            manager = MarketDataManager()
            results = await manager.analyze_market_data(
                market_sector="technology",
                data_types=["sentiment", "trends"],
                time_range="30d",
                include_competitors=True
            )
            
            if results and not results.get("error"):
                print("✅ Market data analysis completed")
                print(f"   - Market Sector: {results.get('market_sector', 'unknown')}")
                print(f"   - Data Types: {len(results.get('data_types', []))}")
                
                combined_analysis = results.get('combined_analysis', {})
                if combined_analysis:
                    print(f"   - Market Health Score: {combined_analysis.get('market_health_score', 'unknown')}")
                    print(f"   - Market Outlook: {combined_analysis.get('market_outlook', 'unknown')}")
                
                self.results["tests"].append({
                    "test": "market_data_analysis",
                    "status": "passed",
                    "response": {
                        "market_sector": results.get('market_sector'),
                        "data_types": results.get('data_types'),
                        "market_health_score": combined_analysis.get('market_health_score'),
                        "market_outlook": combined_analysis.get('market_outlook')
                    }
                })
                return True
            else:
                print("❌ Market data analysis failed")
                error_msg = results.get("error", "Unknown error") if results else "No results"
                
                self.results["tests"].append({
                    "test": "market_data_analysis",
                    "status": "failed",
                    "error": error_msg
                })
                return False
                
        except Exception as e:
            print(f"❌ Market data analysis error: {e}")
            
            self.results["tests"].append({
                "test": "market_data_analysis",
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
        filename = f"Test/business_strategic_position_analysis_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n💾 Test results saved to: {filename}")
        return filename
    
    async def run_all_tests(self):
        """Run all tests."""
        print("🚀 Business Strategic Position Analysis Test Suite")
        print("=" * 60)
        
        # Test 1: Health check
        health_ok = await self.test_health_check()
        
        if not health_ok:
            print("❌ System health check failed. Stopping tests.")
            return False
        
        # Test 2: Art of War scenario analysis
        await self.test_art_of_war_scenario_analysis()
        
        # Test 3: Multi-domain strategic analysis
        await self.test_multi_domain_strategic_analysis()
        
        # Test 4: Market data analysis
        await self.test_market_data_analysis()
        
        # Test 5: Main business strategic position analysis endpoint
        await self.test_business_strategic_position_analysis()
        
        # Generate summary and save results
        self.generate_summary()
        self.save_results()
        
        return self.results["summary"]["success_rate"] > 0.5


async def main():
    """Main test function."""
    tester = BusinessStrategicPositionAnalysisTester()
    
    success = await tester.run_all_tests()
    
    if success:
        print("\n✅ Test suite completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test suite failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
