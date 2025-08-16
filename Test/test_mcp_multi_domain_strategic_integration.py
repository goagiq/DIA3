#!/usr/bin/env python3
"""
Test script for MCP Multi-Domain Strategic Analysis Integration

This script tests the integration of multi-domain strategic analysis
with the MCP server and verifies that all components work together.
"""

import asyncio
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Test configuration
MCP_BASE_URL = "http://127.0.0.1:8000"
API_BASE_URL = "http://127.0.0.1:8003"

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
    }
}


class MCPMultiDomainStrategicTester:
    """Test class for MCP multi-domain strategic analysis integration."""
    
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
    
    async def test_mcp_server_health(self) -> bool:
        """Test MCP server health."""
        try:
            response = requests.get(f"{MCP_BASE_URL}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test_result(
                        "MCP Server Health",
                        True,
                        "MCP server is healthy and running"
                    )
                    return True
                else:
                    self.log_test_result(
                        "MCP Server Health",
                        False,
                        f"MCP server not healthy: {data}"
                    )
                    return False
            else:
                self.log_test_result(
                    "MCP Server Health",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "MCP Server Health",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_mcp_initialize(self) -> bool:
        """Test MCP initialize method."""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "test_client",
                        "version": "1.0.0"
                    }
                }
            }
            
            response = requests.post(
                MCP_BASE_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("result"):
                    self.log_test_result(
                        "MCP Initialize",
                        True,
                        "MCP initialize successful"
                    )
                    return True
                else:
                    self.log_test_result(
                        "MCP Initialize",
                        False,
                        f"MCP initialize failed: {data}"
                    )
                    return False
            else:
                self.log_test_result(
                    "MCP Initialize",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "MCP Initialize",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_mcp_tools_list(self) -> bool:
        """Test MCP tools/list method."""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
            
            response = requests.post(
                MCP_BASE_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("result") and data["result"].get("tools"):
                    tools = data["result"]["tools"]
                    strategic_tools = [
                        tool for tool in tools 
                        if "strategic" in tool.get("name", "").lower() or 
                           "multi-domain" in tool.get("description", "").lower()
                    ]
                    
                    if strategic_tools:
                        self.log_test_result(
                            "MCP Tools List",
                            True,
                            f"Found {len(strategic_tools)} strategic analysis tools"
                        )
                        return True
                    else:
                        self.log_test_result(
                            "MCP Tools List",
                            False,
                            "No strategic analysis tools found in MCP tools list"
                        )
                        return False
                else:
                    self.log_test_result(
                        "MCP Tools List",
                        False,
                        f"Invalid tools list response: {data}"
                    )
                    return False
            else:
                self.log_test_result(
                    "MCP Tools List",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "MCP Tools List",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_mcp_strategic_analysis(self, domain: str, test_data: Dict[str, Any]) -> bool:
        """Test MCP strategic analysis tool."""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "analyze_strategic_context",
                    "arguments": {
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
                }
            }
            
            response = requests.post(
                MCP_BASE_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("result") and data["result"].get("content"):
                    result_content = data["result"]["content"]
                    if isinstance(result_content, list) and len(result_content) > 0:
                        result = result_content[0]
                        if result.get("success"):
                            self.log_test_result(
                                f"MCP Strategic Analysis - {domain}",
                                True,
                                f"Strategic analysis completed for {domain} domain"
                            )
                            return True
                        else:
                            self.log_test_result(
                                f"MCP Strategic Analysis - {domain}",
                                False,
                                f"Strategic analysis failed: {result.get('error', 'Unknown error')}"
                            )
                            return False
                    else:
                        self.log_test_result(
                            f"MCP Strategic Analysis - {domain}",
                            False,
                            f"Invalid result content: {result_content}"
                        )
                        return False
                else:
                    self.log_test_result(
                        f"MCP Strategic Analysis - {domain}",
                        False,
                        f"Invalid response: {data}"
                    )
                    return False
            else:
                self.log_test_result(
                    f"MCP Strategic Analysis - {domain}",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                f"MCP Strategic Analysis - {domain}",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_api_strategic_endpoints(self) -> bool:
        """Test API strategic analysis endpoints."""
        try:
            # Test health endpoint
            response = requests.get(f"{API_BASE_URL}/strategic/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("engine_available"):
                    self.log_test_result(
                        "API Strategic Health",
                        True,
                        "API strategic analysis endpoints are available"
                    )
                    return True
                else:
                    self.log_test_result(
                        "API Strategic Health",
                        False,
                        f"API strategic analysis not available: {data}"
                    )
                    return False
            else:
                self.log_test_result(
                    "API Strategic Health",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "API Strategic Health",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def test_api_strategic_analysis(self, domain: str, test_data: Dict[str, Any]) -> bool:
        """Test API strategic analysis endpoint."""
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
                f"{API_BASE_URL}/strategic/analyze",
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
                        f"API Strategic Analysis - {domain}",
                        True,
                        f"Analysis completed. ID: {analysis_id}, Findings: {len(findings)}, Recommendations: {len(recommendations)}"
                    )
                    return True
                else:
                    self.log_test_result(
                        f"API Strategic Analysis - {domain}",
                        False,
                        f"Analysis failed: {data.get('error', 'Unknown error')}"
                    )
                    return False
            else:
                self.log_test_result(
                    f"API Strategic Analysis - {domain}",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                f"API Strategic Analysis - {domain}",
                False,
                f"Exception: {e}"
            )
            return False
    
    async def run_all_tests(self):
        """Run all integration tests."""
        print("🔗 MCP MULTI-DOMAIN STRATEGIC ANALYSIS INTEGRATION TEST")
        print("=" * 70)
        print("Testing integration between MCP server and multi-domain strategic analysis")
        print("=" * 70)
        
        # Test MCP server functionality
        await self.test_mcp_server_health()
        await self.test_mcp_initialize()
        await self.test_mcp_tools_list()
        
        # Test API endpoints
        await self.test_api_strategic_endpoints()
        
        # Test strategic analysis for each domain
        for domain, test_data in TEST_DATA.items():
            await self.test_mcp_strategic_analysis(domain, test_data)
            await self.test_api_strategic_analysis(domain, test_data)
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 INTEGRATION TEST SUMMARY")
        print("=" * 70)
        print(f"✅ Passed: {self.success_count}")
        print(f"❌ Failed: {self.total_tests - self.success_count}")
        print(f"📈 Success Rate: {(self.success_count / self.total_tests * 100):.1f}%")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = Path("Results") / f"mcp_multi_domain_strategic_integration_test_{timestamp}.json"
        
        results = {
            "test_name": "MCP Multi-Domain Strategic Analysis Integration Test",
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
            print("\n🎉 All integration tests passed! MCP and multi-domain strategic analysis are working together correctly.")
        else:
            print(f"\n⚠️ {self.total_tests - self.success_count} tests failed. Check the results for details.")
        
        return self.success_count == self.total_tests


async def main():
    """Main test function."""
    tester = MCPMultiDomainStrategicTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n✅ MCP multi-domain strategic analysis integration test completed successfully!")
        return 0
    else:
        print("\n❌ Some integration tests failed. Check the results above.")
        return 1


if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
