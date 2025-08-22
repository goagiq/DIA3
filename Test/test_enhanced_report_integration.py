#!/usr/bin/env python3
"""
Test Enhanced Report Integration with Source Tracking

This script tests the enhanced report generation with source tracking,
MCP client communication, and verifies that the Operational Capabilities
section is included in Strategic Timeline and Milestones.
"""

import asyncio
import sys
import time
import requests
from pathlib import Path
from typing import Dict, Any
from loguru import logger

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.core.enhanced_report_orchestrator import get_enhanced_report_orchestrator
from src.core.enhanced_mcp_client import get_enhanced_mcp_client


class EnhancedReportIntegrationTester:
    """Test enhanced report integration with source tracking."""
    
    def __init__(self):
        self.api_base_url = "http://localhost:8003"
        self.mcp_base_url = "http://localhost:8000"
        self.test_results = {}
        
    async def test_enhanced_report_orchestrator(self) -> bool:
        """Test enhanced report orchestrator functionality."""
        try:
            logger.info("🧪 Testing Enhanced Report Orchestrator...")
            
            # Get enhanced report orchestrator
            orchestrator = get_enhanced_report_orchestrator()
            
            # Test content with Operational Capabilities
            test_content = """
            Strategic Defense Analysis Report
            
            This report analyzes the strategic implications of submarine acquisition
            for regional security dynamics in South Asia.
            
            Key Findings:
            1. Enhanced deterrence capabilities
            2. Regional power balance shifts
            3. Operational capabilities development timeline
            4. Strategic timeline and milestones including operational capabilities
            
            Strategic Timeline and Milestones:
            - Phase 1: Initial capability development (2024-2025)
            - Phase 2: Operational capabilities assessment (2025-2026)
            - Phase 3: Full operational deployment (2026-2027)
            
            Operational Capabilities:
            - Submarine operations and maintenance
            - Strategic patrol capabilities
            - Communication and coordination systems
            - Training and personnel development
            """
            
            # Generate enhanced report
            result = await orchestrator.generate_enhanced_report(
                content=test_content,
                report_type="strategic_defense_analysis",
                include_tooltips=True,
                include_source_references=True,
                include_calculations=True,
                language="en"
            )
            
            if result.get("success"):
                logger.info("✅ Enhanced Report Orchestrator test passed")
                logger.info(f"📄 Report saved to: {result['enhanced_report']['filepath']}")
                
                # Check if Operational Capabilities are included
                report_content = result['enhanced_report']['content']
                if "Operational Capabilities" in report_content:
                    logger.info("✅ Operational Capabilities section found in report")
                    self.test_results['operational_capabilities'] = True
                else:
                    logger.warning("⚠️ Operational Capabilities section not found in report")
                    self.test_results['operational_capabilities'] = False
                
                # Check source tracking
                if result.get('source_tracking'):
                    logger.info("✅ Source tracking data included")
                    self.test_results['source_tracking'] = True
                else:
                    logger.warning("⚠️ Source tracking data missing")
                    self.test_results['source_tracking'] = False
                
                return True
            else:
                logger.error(f"❌ Enhanced Report Orchestrator test failed: {result.get('error')}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Enhanced Report Orchestrator test error: {e}")
            return False
    
    async def test_mcp_client_communication(self) -> bool:
        """Test MCP client communication."""
        try:
            logger.info("🧪 Testing MCP Client Communication...")
            
            # Get enhanced MCP client
            mcp_client = get_enhanced_mcp_client()
            
            # Test basic tool call
            test_result = await mcp_client.call_tool_with_tracking(
                tool_name="generate_report",
                parameters={
                    "content": "Test report content for MCP communication",
                    "report_type": "test",
                    "language": "en"
                }
            )
            
            if test_result.get("success"):
                logger.info("✅ MCP Client Communication test passed")
                return True
            else:
                logger.error(f"❌ MCP Client Communication test failed: {test_result.get('error')}")
                return False
                
        except Exception as e:
            logger.error(f"❌ MCP Client Communication test error: {e}")
            return False
    
    async def test_api_endpoints(self) -> bool:
        """Test API endpoints for enhanced report generation."""
        try:
            logger.info("🧪 Testing API Endpoints...")
            
            # Test enhanced report generation endpoint
            test_data = {
                "content": "API test content for enhanced report generation",
                "report_type": "api_test",
                "include_tooltips": True,
                "include_source_references": True,
                "include_calculations": True,
                "language": "en"
            }
            
            response = requests.post(
                f"{self.api_base_url}/enhanced-report/generate",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info("✅ API Enhanced Report endpoint test passed")
                    return True
                else:
                    logger.error(f"❌ API Enhanced Report endpoint failed: {result.get('error')}")
                    return False
            else:
                logger.error(f"❌ API Enhanced Report endpoint HTTP error: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ API Endpoints test error: {e}")
            return False
    
    async def test_operational_capabilities_integration(self) -> bool:
        """Test that Operational Capabilities are properly integrated."""
        try:
            logger.info("🧪 Testing Operational Capabilities Integration...")
            
            # Test content specifically mentioning Operational Capabilities
            test_content = """
            Strategic Analysis Report
            
            Strategic Timeline and Milestones:
            1. Initial Assessment Phase (2024)
            2. Operational Capabilities Development (2025)
            3. Full Deployment Phase (2026)
            
            Operational Capabilities:
            - Command and Control Systems
            - Intelligence Collection and Analysis
            - Strategic Communication Networks
            - Training and Personnel Development
            - Maintenance and Logistics Support
            """
            
            orchestrator = get_enhanced_report_orchestrator()
            result = await orchestrator.generate_enhanced_report(
                content=test_content,
                report_type="operational_capabilities_test",
                include_tooltips=True,
                include_source_references=True,
                include_calculations=True
            )
            
            if result.get("success"):
                report_content = result['enhanced_report']['content']
                
                # Check for Operational Capabilities section
                if "Operational Capabilities" in report_content:
                    logger.info("✅ Operational Capabilities section found")
                    
                    # Check for specific operational capabilities
                    capabilities = [
                        "Command and Control Systems",
                        "Intelligence Collection and Analysis",
                        "Strategic Communication Networks",
                        "Training and Personnel Development",
                        "Maintenance and Logistics Support"
                    ]
                    
                    found_capabilities = sum(1 for cap in capabilities if cap in report_content)
                    if found_capabilities >= 3:  # At least 3 capabilities should be found
                        logger.info(f"✅ Found {found_capabilities}/5 operational capabilities")
                        return True
                    else:
                        logger.warning(f"⚠️ Only found {found_capabilities}/5 operational capabilities")
                        return False
                else:
                    logger.error("❌ Operational Capabilities section not found")
                    return False
            else:
                logger.error(f"❌ Operational Capabilities test failed: {result.get('error')}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Operational Capabilities Integration test error: {e}")
            return False
    
    async def run_all_tests(self) -> Dict[str, bool]:
        """Run all integration tests."""
        logger.info("🚀 Starting Enhanced Report Integration Tests")
        logger.info("=" * 60)
        
        # Wait for servers to be ready
        logger.info("⏳ Waiting 60 seconds for servers to be ready...")
        await asyncio.sleep(60)
        
        # Run tests
        tests = [
            ("Enhanced Report Orchestrator", self.test_enhanced_report_orchestrator),
            ("MCP Client Communication", self.test_mcp_client_communication),
            ("API Endpoints", self.test_api_endpoints),
            ("Operational Capabilities Integration", self.test_operational_capabilities_integration)
        ]
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                self.test_results[test_name] = result
                if result:
                    logger.info(f"✅ {test_name} test PASSED")
                else:
                    logger.error(f"❌ {test_name} test FAILED")
            except Exception as e:
                logger.error(f"❌ {test_name} test ERROR: {e}")
                self.test_results[test_name] = False
        
        # Summary
        logger.info("=" * 60)
        logger.info("📊 Test Results Summary:")
        
        passed_tests = sum(1 for result in self.test_results.values() if result)
        total_tests = len(self.test_results)
        
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"  {test_name}: {status}")
        
        logger.info(f"Overall: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            logger.info("🎉 All tests passed! Enhanced report integration is working correctly.")
        else:
            logger.warning(f"⚠️ {total_tests - passed_tests} tests failed. Please check the implementation.")
        
        return self.test_results


async def main():
    """Main function."""
    tester = EnhancedReportIntegrationTester()
    results = await tester.run_all_tests()
    
    # Exit with appropriate code
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
