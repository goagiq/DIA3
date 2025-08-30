#!/usr/bin/env python3
"""
Test script for Multi-Domain Strategic Analysis

This script tests the comprehensive strategic analysis capabilities
across multiple domains including defense, intelligence, and business applications.
"""

import asyncio
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Test configuration
API_BASE_URL = "http://127.0.0.1:8003"
STRATEGIC_BASE = f"{API_BASE_URL}/strategic"

# Test data for different domains
TEST_DATA = {
    "defense": {
        "domain": "defense",
        "region": "Eastern Europe",
        "timeframe": "current",
        "stakeholders": ["NATO", "EU", "Ukraine", "Russia"],
        "objectives": ["deterrence", "defense", "stability"],
        "constraints": ["budget", "political", "alliance_coordination"],
        "resources": {"military": "high", "economic": "medium", "diplomatic": "high"},
        "analysis_types": ["threat_assessment", "cultural_analysis", "deception_detection"],
        "content_data": "Recent military posturing in Eastern Europe suggests strategic deception operations."
    },
    "intelligence": {
        "domain": "intelligence",
        "region": "Global",
        "timeframe": "ongoing",
        "stakeholders": ["intelligence_agencies", "policy_makers", "military"],
        "objectives": ["information_collection", "threat_detection", "strategic_analysis"],
        "constraints": ["legal", "resource", "coordination"],
        "resources": {"human": "high", "technical": "high", "analytical": "high"},
        "analysis_types": ["threat_assessment", "deception_detection", "cultural_analysis"],
        "content_data": "Intelligence reports indicate sophisticated information operations."
    },
    "business": {
        "domain": "business",
        "region": "Global Markets",
        "timeframe": "quarterly",
        "stakeholders": ["investors", "customers", "competitors", "regulators"],
        "objectives": ["market_expansion", "competitive_advantage", "risk_mitigation"],
        "constraints": ["regulatory", "market", "resource"],
        "resources": {"financial": "high", "human": "medium", "technological": "high"},
        "analysis_types": ["competitive_intelligence", "opportunity_analysis", "strategic_positioning"],
        "content_data": "Market analysis reveals emerging competitive threats and opportunities."
    },
    "cyber": {
        "domain": "cyber",
        "region": "Digital",
        "timeframe": "real_time",
        "stakeholders": ["cyber_defense", "critical_infrastructure", "government"],
        "objectives": ["cyber_security", "threat_detection", "incident_response"],
        "constraints": ["technical", "legal", "resource"],
        "resources": {"technical": "high", "analytical": "high", "coordination": "medium"},
        "analysis_types": ["threat_assessment", "deception_detection", "risk_analysis"],
        "content_data": "Cybersecurity threats are becoming more sophisticated and targeted."
    }
}


class MultiDomainStrategicTester:
    """Test class for multi-domain strategic analysis."""
    
    def __init__(self):
        self.test_results = []
        self.success_count = 0
        self.total_tests = 0
    
    def log_test_result(self, test_name: str, success: bool, message: str):
        """Log test result."""
        self.total_tests += 1
        if success:
            self.success_count += 1
        
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
    
    async def test_health_check(self) -> bool:
        """Test strategic analysis health check."""
        try:
            response = requests.get(f"{STRATEGIC_BASE}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("engine_available"):
                    self.log_test_result(
                        "Health Check",
                        True,
                        "Strategic analysis engine is healthy and available"
                    )
                    return True
                else:
                    self.log_test_result(
                        "Health Check",
                        False,
                        f"Engine not available: {data}"
                    )
                    return False
            else:
                self.log_test_result(
                    "Health Check",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "Health Check",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_get_domains(self) -> bool:
        """Test getting supported domains."""
        try:
            response = requests.get(f"{STRATEGIC_BASE}/domains", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("domains"):
                    domains = data["domains"]
                    expected_domains = ["defense", "intelligence", "business", "cyber"]
                    found_domains = [d["domain"] for d in domains]
                    
                    if all(domain in found_domains for domain in expected_domains):
                        self.log_test_result(
                            "Get Domains",
                            True,
                            f"Found {len(domains)} domains: {found_domains}"
                        )
                        return True
                    else:
                        self.log_test_result(
                            "Get Domains",
                            False,
                            f"Missing domains. Expected: {expected_domains}, Found: {found_domains}"
                        )
                        return False
                else:
                    self.log_test_result(
                        "Get Domains",
                        False,
                        f"Invalid response: {data}"
                    )
                    return False
            else:
                self.log_test_result(
                    "Get Domains",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "Get Domains",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_get_analysis_types(self) -> bool:
        """Test getting analysis types."""
        try:
            response = requests.get(f"{STRATEGIC_BASE}/analysis-types", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("analysis_types"):
                    analysis_types = data["analysis_types"]
                    expected_types = [
                        "threat_assessment", "competitive_intelligence", 
                        "cultural_analysis", "deception_detection"
                    ]
                    found_types = [at["type"] for at in analysis_types]
                    
                    if all(at in found_types for at in expected_types):
                        self.log_test_result(
                            "Get Analysis Types",
                            True,
                            f"Found {len(analysis_types)} analysis types: {found_types}"
                        )
                        return True
                    else:
                        self.log_test_result(
                            "Get Analysis Types",
                            False,
                            f"Missing types. Expected: {expected_types}, Found: {found_types}"
                        )
                        return False
                else:
                    self.log_test_result(
                        "Get Analysis Types",
                        False,
                        f"Invalid response: {data}"
                    )
                    return False
            else:
                self.log_test_result(
                    "Get Analysis Types",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "Get Analysis Types",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_strategic_context(self, domain: str) -> bool:
        """Test getting strategic context for a domain."""
        try:
            response = requests.get(f"{STRATEGIC_BASE}/context/{domain}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("context"):
                    context = data["context"]
                    if context.get("domain") == domain:
                        self.log_test_result(
                            f"Strategic Context - {domain}",
                            True,
                            f"Retrieved context for {domain} domain"
                        )
                        return True
                    else:
                        self.log_test_result(
                            f"Strategic Context - {domain}",
                            False,
                            f"Wrong domain in response: {context.get('domain')}"
                        )
                        return False
                else:
                    self.log_test_result(
                        f"Strategic Context - {domain}",
                        False,
                        f"Invalid response: {data}"
                    )
                    return False
            else:
                self.log_test_result(
                    f"Strategic Context - {domain}",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                f"Strategic Context - {domain}",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_strategic_analysis(self, domain: str, test_data: Dict[str, Any]) -> bool:
        """Test comprehensive strategic analysis for a domain."""
        try:
            payload = {
                "domain": test_data["domain"],
                "region": test_data["region"],
                "timeframe": test_data["timeframe"],
                "stakeholders": test_data["stakeholders"],
                "objectives": test_data["objectives"],
                "constraints": test_data["constraints"],
                "resources": test_data["resources"],
                "analysis_types": test_data["analysis_types"],
                "content_data": test_data["content_data"]
            }
            
            response = requests.post(
                f"{STRATEGIC_BASE}/analyze",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    analysis_id = data.get("analysis_id")
                    findings = data.get("findings", [])
                    recommendations = data.get("recommendations", [])
                    
                    self.log_test_result(
                        f"Strategic Analysis - {domain}",
                        True,
                        f"Analysis completed. ID: {analysis_id}, Findings: {len(findings)}, Recommendations: {len(recommendations)}"
                    )
                    return True
                else:
                    self.log_test_result(
                        f"Strategic Analysis - {domain}",
                        False,
                        f"Analysis failed: {data.get('error', 'Unknown error')}"
                    )
                    return False
            else:
                self.log_test_result(
                    f"Strategic Analysis - {domain}",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                f"Strategic Analysis - {domain}",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_deception_detection(self) -> bool:
        """Test deception detection functionality."""
        try:
            content = "This is a test message that may contain deception patterns."
            
            response = requests.post(
                f"{STRATEGIC_BASE}/deception-detection",
                params={"content": content},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    deception_analysis = data.get("deception_analysis", {})
                    self.log_test_result(
                        "Deception Detection",
                        True,
                        f"Deception analysis completed: {len(deception_analysis)} indicators"
                    )
                    return True
                else:
                    self.log_test_result(
                        "Deception Detection",
                        False,
                        f"Deception detection failed: {data.get('error', 'Unknown error')}"
                    )
                    return False
            else:
                self.log_test_result(
                    "Deception Detection",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "Deception Detection",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_cultural_analysis(self, domain: str) -> bool:
        """Test cultural analysis functionality."""
        try:
            # Use query parameters instead of JSON payload
            params = {
                "domain": domain,
                "region": "Global",
                "content_data": "Cultural analysis test content."
            }
            
            response = requests.post(
                f"{STRATEGIC_BASE}/cultural-analysis",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    cultural_analysis = data.get("cultural_analysis", {})
                    self.log_test_result(
                        f"Cultural Analysis - {domain}",
                        True,
                        f"Cultural analysis completed for {domain} domain"
                    )
                    return True
                else:
                    self.log_test_result(
                        f"Cultural Analysis - {domain}",
                        False,
                        f"Cultural analysis failed: {data.get('error', 'Unknown error')}"
                    )
                    return False
            else:
                self.log_test_result(
                    f"Cultural Analysis - {domain}",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                f"Cultural Analysis - {domain}",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_art_of_war_analysis(self, domain: str) -> bool:
        """Test Art of War analysis functionality."""
        try:
            # Use query parameters for domain and region, JSON body for context_data
            params = {
                "domain": domain,
                "region": "Global"
            }
            
            payload = {
                "context_data": {
                    "timeframe": "current",
                    "stakeholders": ["test"],
                    "objectives": ["test"],
                    "constraints": ["test"],
                    "resources": {"test": "medium"}
                }
            }
            
            response = requests.post(
                f"{STRATEGIC_BASE}/art-of-war-analysis",
                params=params,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    art_of_war_analysis = data.get("art_of_war_analysis", {})
                    self.log_test_result(
                        f"Art of War Analysis - {domain}",
                        True,
                        f"Art of War analysis completed for {domain} domain"
                    )
                    return True
                else:
                    self.log_test_result(
                        f"Art of War Analysis - {domain}",
                        False,
                        f"Art of War analysis failed: {data.get('error', 'Unknown error')}"
                    )
                    return False
            else:
                self.log_test_result(
                    f"Art of War Analysis - {domain}",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                f"Art of War Analysis - {domain}",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def run_all_tests(self):
        """Run all strategic analysis tests."""
        print("🎯 MULTI-DOMAIN STRATEGIC ANALYSIS TEST")
        print("=" * 60)
        print("Testing comprehensive strategic analysis capabilities")
        print("=" * 60)
        
        # Test basic functionality
        await self.test_health_check()
        await self.test_get_domains()
        await self.test_get_analysis_types()
        await self.test_deception_detection()
        
        # Test domain-specific functionality
        for domain, test_data in TEST_DATA.items():
            await self.test_strategic_context(domain)
            await self.test_strategic_analysis(domain, test_data)
            await self.test_cultural_analysis(domain)
            await self.test_art_of_war_analysis(domain)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.success_count}")
        print(f"❌ Failed: {self.total_tests - self.success_count}")
        print(f"📈 Success Rate: {(self.success_count / self.total_tests * 100):.1f}%")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = Path("Results") / f"multi_domain_strategic_test_{timestamp}.json"
        
        results = {
            "test_name": "Multi-Domain Strategic Analysis Test",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": self.total_tests,
                "passed": self.success_count,
                "failed": self.total_tests - self.success_count,
                "success_rate": self.success_count / self.total_tests if self.total_tests > 0 else 0
            },
            "results": self.test_results
        }
        
        results_file.parent.mkdir(parents=True, exist_ok=True)
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Results saved to: {results_file}")
        
        if self.success_count == self.total_tests:
            print("\n🎉 All tests passed! Multi-domain strategic analysis is working correctly.")
        else:
            print(f"\n⚠️ {self.total_tests - self.success_count} tests failed. Check the results for details.")
        
        return self.success_count == self.total_tests


async def main():
    """Main test function."""
    tester = MultiDomainStrategicTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n✅ Multi-domain strategic analysis test completed successfully!")
        return 0
    else:
        print("\n❌ Some tests failed. Check the results above.")
        return 1


if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
