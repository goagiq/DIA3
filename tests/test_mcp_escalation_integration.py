#!/usr/bin/env python3
"""
Test script for MCP escalation analysis integration.

This script tests the MCP server integration with escalation analysis functionality
to ensure proper communication and data flow.
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any
import requests
from loguru import logger

# Test configuration
MCP_BASE_URL = "http://localhost:8000"
API_BASE_URL = "http://localhost:8003"

TEST_CONTENT = """
Russia has recently increased its military presence near the EU border, 
conducting large-scale military exercises and deploying advanced weapons systems. 
The EU has responded with economic sanctions and diplomatic pressure, while 
NATO has announced plans to expand its eastern flank. This escalation follows 
a pattern of historical tensions between Russia and European powers, similar 
to the dynamics described in War and Peace during the Napoleonic era.
"""


class MCPEscalationTester:
    """Test class for MCP escalation analysis integration."""
    
    def __init__(self):
        self.mcp_base_url = MCP_BASE_URL
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
    
    def test_mcp_server_health(self) -> bool:
        """Test MCP server health."""
        try:
            url = f"{self.mcp_base_url}/health"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                self.log_test_result("MCP Server Health", True, "MCP server is healthy")
                return True
            else:
                self.log_test_result("MCP Server Health", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("MCP Server Health", False, f"Exception: {e}")
            return False
    
    def test_mcp_initialize(self) -> bool:
        """Test MCP initialize method."""
        try:
            url = f"{self.mcp_base_url}"
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "escalation_test",
                        "version": "1.0.0"
                    }
                }
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    self.log_test_result("MCP Initialize", True, "MCP initialization successful")
                    return True
                else:
                    self.log_test_result("MCP Initialize", False, f"Error: {data.get('error', 'Unknown')}")
                    return False
            else:
                self.log_test_result("MCP Initialize", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("MCP Initialize", False, f"Exception: {e}")
            return False
    
    def test_mcp_tools_list(self) -> bool:
        """Test MCP tools/list method."""
        try:
            url = f"{self.mcp_base_url}"
            payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    tools = data["result"].get("tools", [])
                    escalation_tools = [t for t in tools if "escalation" in t.get("name", "").lower()]
                    
                    self.log_test_result(
                        "MCP Tools List",
                        True,
                        f"Found {len(tools)} tools, {len(escalation_tools)} escalation-related"
                    )
                    return True
                else:
                    self.log_test_result("MCP Tools List", False, f"Error: {data.get('error', 'Unknown')}")
                    return False
            else:
                self.log_test_result("MCP Tools List", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("MCP Tools List", False, f"Exception: {e}")
            return False
    
    def test_api_escalation_health(self) -> bool:
        """Test API escalation analysis health endpoint."""
        try:
            url = f"{self.api_base_url}/escalation-analysis/health"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    domains = data.get("domains_supported", [])
                    self.log_test_result(
                        "API Escalation Health",
                        True,
                        f"Service healthy, {len(domains)} domains supported"
                    )
                    return True
                else:
                    self.log_test_result("API Escalation Health", False, f"Service unhealthy: {data}")
                    return False
            else:
                self.log_test_result("API Escalation Health", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("API Escalation Health", False, f"Exception: {e}")
            return False
    
    def test_api_escalation_analysis(self) -> bool:
        """Test API escalation analysis endpoint."""
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
                    confidence_score = data.get("confidence_score", 0)
                    scenarios = data.get("escalation_scenarios", [])
                    
                    self.log_test_result(
                        "API Escalation Analysis",
                        True,
                        f"Analysis {analysis_id} completed, confidence: {confidence_score:.2f}, "
                        f"{len(scenarios)} scenarios"
                    )
                    return True
                else:
                    self.log_test_result("API Escalation Analysis", False, "Response not successful")
                    return False
            else:
                self.log_test_result("API Escalation Analysis", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("API Escalation Analysis", False, f"Exception: {e}")
            return False
    
    def test_mcp_escalation_call(self) -> bool:
        """Test MCP escalation analysis call."""
        try:
            # First initialize
            init_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "escalation_test",
                        "version": "1.0.0"
                    }
                }
            }
            
            url = f"{self.mcp_base_url}"
            init_response = requests.post(url, json=init_payload, timeout=10)
            
            if init_response.status_code != 200:
                self.log_test_result("MCP Escalation Call", False, "Failed to initialize MCP")
                return False
            
            # Now call escalation analysis
            call_payload = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "run_comprehensive_analysis",
                    "arguments": {
                        "input_content": TEST_CONTENT,
                        "analysis_type": "deception",
                        "generate_report": True,
                        "report_format": "markdown"
                    }
                }
            }
            
            call_response = requests.post(url, json=call_payload, timeout=60)
            
            if call_response.status_code == 200:
                data = call_response.json()
                if "result" in data:
                    self.log_test_result("MCP Escalation Call", True, "MCP escalation analysis successful")
                    return True
                else:
                    error = data.get("error", {})
                    self.log_test_result(
                        "MCP Escalation Call",
                        False,
                        f"Error: {error.get('message', 'Unknown error')}"
                    )
                    return False
            else:
                self.log_test_result("MCP Escalation Call", False, f"HTTP {call_response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("MCP Escalation Call", False, f"Exception: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all MCP escalation integration tests."""
        logger.info("🚀 Starting MCP Escalation Integration Tests")
        logger.info("=" * 60)
        
        # Test MCP server functionality
        self.test_mcp_server_health()
        self.test_mcp_initialize()
        self.test_mcp_tools_list()
        
        # Test API functionality
        self.test_api_escalation_health()
        self.test_api_escalation_analysis()
        
        # Test MCP integration
        self.test_mcp_escalation_call()
        
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
        tester = MCPEscalationTester()
        
        # Run all tests
        results = tester.run_all_tests()
        
        # Save results to file
        results_file = f"Test/mcp_escalation_integration_results_{int(time.time())}.json"
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
