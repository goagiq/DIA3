#!/usr/bin/env python3
"""
Enhanced Strategic Analysis MCP Client Test

This script tests the MCP client communication with enhanced strategic analysis tools.
"""

import asyncio
import json
import time
from datetime import datetime


class EnhancedStrategicMCPTester:
    """Test class for enhanced strategic analysis MCP client communication."""
    
    def __init__(self):
        self.test_results = []
    
    def log_test_result(self, test_name: str, success: bool, details: str = "", data: dict = None):
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
    
    async def test_mcp_enhanced_strategic_analysis(self):
        """Test MCP enhanced strategic analysis tool."""
        print("\n🔍 Testing MCP Enhanced Strategic Analysis Tool")
        print("=" * 60)
        
        try:
            # Import MCP client
            from src.mcp_servers.client_example import call_mcp_tool
            
            # Test content
            test_content = """
            Russia has announced a reduction in military spending while maintaining 
            strategic nuclear capabilities. The government claims to be withdrawing 
            troops from border regions, but intelligence sources indicate continued 
            military modernization and troop movements. Bilateral defense agreements 
            have been proposed with neighboring countries, potentially undermining 
            existing multilateral security arrangements.
            """
            
            # Call MCP tool
            result = await call_mcp_tool(
                "analyze_enhanced_strategic_content",
                {
                    "content": test_content,
                    "domain": "defense",
                    "language": "en",
                    "analysis_depth": "comprehensive"
                }
            )
            
            if result and "success" in result and result["success"]:
                analysis_id = result.get("analysis_id", "unknown")
                confidence = result.get("confidence_score", 0)
                principles_count = len(result.get("principles_detected", []))
                moves_count = len(result.get("strategic_moves", []))
                
                self.log_test_result("MCP Enhanced Strategic Analysis", True,
                    f"Analysis ID: {analysis_id}, Confidence: {confidence:.2f}, "
                    f"Principles: {principles_count}, Moves: {moves_count}", result)
                
                # Check for specific Art of War principles
                principles_found = [p.get("translation", "") for p in result.get("principles_detected", [])]
                expected_principles = ["Show inability when able", "Show disuse when using", "Separate when united"]
                
                found_expected = [p for p in expected_principles if any(p in found for found in principles_found)]
                if found_expected:
                    self.log_test_result("MCP Principles Detection", True, f"Found expected principles: {found_expected}")
                else:
                    self.log_test_result("MCP Principles Detection", False, "No expected principles detected")
                    
            else:
                self.log_test_result("MCP Enhanced Strategic Analysis", False, f"Tool call failed: {result}")
                
        except Exception as e:
            self.log_test_result("MCP Enhanced Strategic Analysis", False, f"Error: {e}")
    
    async def test_mcp_enhanced_strategic_domains(self):
        """Test MCP enhanced strategic domains tool."""
        print("\n🔍 Testing MCP Enhanced Strategic Domains Tool")
        print("=" * 60)
        
        try:
            from src.mcp_servers.client_example import call_mcp_tool
            
            result = await call_mcp_tool("get_enhanced_strategic_domains", {})
            
            if result and "success" in result and result["success"]:
                domains = result.get("domains", [])
                count = result.get("count", 0)
                
                self.log_test_result("MCP Enhanced Strategic Domains", True,
                    f"Found {count} domains: {domains}", result)
                
                # Check for expected domains
                expected_domains = [
                    "defense", "intelligence", "business", "cybersecurity",
                    "geopolitical", "financial", "healthcare", "energy",
                    "transportation", "critical_infrastructure"
                ]
                
                missing_domains = [d for d in expected_domains if d not in domains]
                if missing_domains:
                    self.log_test_result("MCP Domain Coverage", False, f"Missing domains: {missing_domains}")
                else:
                    self.log_test_result("MCP Domain Coverage", True, "All expected domains supported")
                    
            else:
                self.log_test_result("MCP Enhanced Strategic Domains", False, f"Tool call failed: {result}")
                
        except Exception as e:
            self.log_test_result("MCP Enhanced Strategic Domains", False, f"Error: {e}")
    
    async def test_mcp_enhanced_strategic_domain_capabilities(self):
        """Test MCP enhanced strategic domain capabilities tool."""
        print("\n🔍 Testing MCP Enhanced Strategic Domain Capabilities Tool")
        print("=" * 60)
        
        try:
            from src.mcp_servers.client_example import call_mcp_tool
            
            result = await call_mcp_tool("get_enhanced_strategic_domain_capabilities", {"domain": "defense"})
            
            if result and "success" in result and result["success"]:
                capabilities = result.get("capabilities", {})
                domain = capabilities.get("domain", "unknown")
                principles = capabilities.get("supported_principles", [])
                
                self.log_test_result("MCP Enhanced Strategic Domain Capabilities", True,
                    f"Domain: {domain}, Principles: {len(principles)}", result)
                    
            else:
                self.log_test_result("MCP Enhanced Strategic Domain Capabilities", False, f"Tool call failed: {result}")
                
        except Exception as e:
            self.log_test_result("MCP Enhanced Strategic Domain Capabilities", False, f"Error: {e}")
    
    async def test_mcp_enhanced_strategic_history(self):
        """Test MCP enhanced strategic history tool."""
        print("\n🔍 Testing MCP Enhanced Strategic History Tool")
        print("=" * 60)
        
        try:
            from src.mcp_servers.client_example import call_mcp_tool
            
            result = await call_mcp_tool("get_enhanced_strategic_history", {})
            
            if result and "success" in result and result["success"]:
                history = result.get("history", [])
                total_analyses = result.get("total_analyses", 0)
                
                self.log_test_result("MCP Enhanced Strategic History", True,
                    f"Total analyses: {total_analyses}, History entries: {len(history)}", result)
                    
            else:
                self.log_test_result("MCP Enhanced Strategic History", False, f"Tool call failed: {result}")
                
        except Exception as e:
            self.log_test_result("MCP Enhanced Strategic History", False, f"Error: {e}")
    
    async def run_all_tests(self):
        """Run all MCP enhanced strategic analysis tests."""
        print("🎯 ENHANCED STRATEGIC ANALYSIS MCP CLIENT TESTING")
        print("=" * 80)
        print("Testing MCP client communication with enhanced strategic analysis tools")
        print("=" * 80)
        
        # Run tests
        await self.test_mcp_enhanced_strategic_analysis()
        await self.test_mcp_enhanced_strategic_domains()
        await self.test_mcp_enhanced_strategic_domain_capabilities()
        await self.test_mcp_enhanced_strategic_history()
        
        # Generate test report
        self.generate_test_report()
    
    def generate_test_report(self):
        """Generate comprehensive test report."""
        print("\n📊 ENHANCED STRATEGIC ANALYSIS MCP CLIENT TEST REPORT")
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
        report_file = f"enhanced_strategic_mcp_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
            print("\n🎉 All enhanced strategic analysis MCP client tests passed!")
        else:
            print(f"\n⚠️ {failed_tests} tests failed. Please check the detailed report.")


async def main():
    """Main test function."""
    tester = EnhancedStrategicMCPTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    print("🚀 Starting Enhanced Strategic Analysis MCP Client Testing")
    print("Make sure the MCP server is running on port 8000")
    print("=" * 80)
    
    # Wait a moment for server startup
    time.sleep(2)
    
    # Run tests
    asyncio.run(main())
