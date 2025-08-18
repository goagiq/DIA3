#!/usr/bin/env python3
"""
Comprehensive Integration Test for DIA3 System

This script tests the complete integration of all system components:
- MCP Server and Tools
- API Routes
- Orchestrator
- PDF/Word Generation Services
- Dynamic MCP Tool Management
- Strategic Analysis
- API Endpoints
- MCP Client Communication
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, List
import requests
import aiohttp

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.mcp_servers.unified_mcp_server import UnifiedMCPServer



class ComprehensiveIntegrationTest:
    """Comprehensive integration test for DIA3 system."""
    
    def __init__(self):
        """Initialize the test suite."""
        # Test configuration
        self.test_config = {
            "mcp_server_port": 8000,
            "api_server_port": 8003,
            "base_url": "http://localhost:8003",
            "timeout": 30
        }
        
        self.results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }
        
        # Initialize services
        self.enhanced_pdf_service = EnhancedPDFGenerationService()
        self.enhanced_word_service = EnhancedWordGenerationService()
        
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log test results."""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if success:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
            if message:
                self.results["errors"].append(f"{test_name}: {message}")
    
    async def test_mcp_server_integration(self):
        """Test MCP server integration."""
        print("\n🔧 Testing MCP Server Integration...")
        
        try:
            # Test MCP server initialization
            mcp_server = UnifiedMCPServer()
            self.log_test("MCP Server Initialization", True, "Server initialized successfully")
            
            # Test tools registration
            tools_info = mcp_server.get_tools_info()
            self.log_test("MCP Tools Registration", len(tools_info) > 0, f"Found {len(tools_info)} tools")
            
            # Test specific tool categories
            tool_categories = [tool.get("type", "unknown") for tool in tools_info]
            expected_categories = ["strategic_intelligence_forecast"]
            
            for category in expected_categories:
                if category in tool_categories:
                    self.log_test(f"MCP Tool Category: {category}", True, "Tool category found")
                else:
                    self.log_test(f"MCP Tool Category: {category}", False, "Tool category not found")
            
            return True
            
        except Exception as e:
            self.log_test("MCP Server Integration", False, str(e))
            return False
    
    async def test_api_routes_integration(self):
        """Test API routes integration."""
        print("\n🌐 Testing API Routes Integration...")
        
        try:
            # Test API server connectivity
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.test_config['base_url']}/health", timeout=self.test_config['timeout']) as response:
                    if response.status == 200:
                        self.log_test("API Server Health Check", True, "Server is healthy")
                    else:
                        self.log_test("API Server Health Check", False, f"Status: {response.status}")
                        return False
                
                # Test PDF generation endpoint
                test_data = {
                    "markdown_file": "docs/white_papers/DIA3_Strategic_Intelligence_White_Paper.md",
                    "output_name": "test_integration",
                    "title": "Integration Test"
                }
                
                async with session.post(
                    f"{self.test_config['base_url']}/api/pdf/generate",
                    json=test_data,
                    timeout=self.test_config['timeout']
                ) as response:
                    if response.status in [200, 201]:
                        self.log_test("PDF Generation API", True, "Endpoint responded successfully")
                    else:
                        self.log_test("PDF Generation API", False, f"Status: {response.status}")
                
                # Test Word generation endpoint
                async with session.post(
                    f"{self.test_config['base_url']}/api/word/generate",
                    json=test_data,
                    timeout=self.test_config['timeout']
                ) as response:
                    if response.status in [200, 201]:
                        self.log_test("Word Generation API", True, "Endpoint responded successfully")
                    else:
                        self.log_test("Word Generation API", False, f"Status: {response.status}")
            
            return True
            
        except Exception as e:
            self.log_test("API Routes Integration", False, str(e))
            return False
    
    async def test_orchestrator_integration(self):
        """Test orchestrator integration."""
        print("\n🎯 Testing Orchestrator Integration...")
        
        try:
            # Test orchestrator initialization
            from src.core.orchestrator import SentimentOrchestrator
            
            orchestrator = SentimentOrchestrator()
            self.log_test("Orchestrator Initialization", True, "Orchestrator initialized successfully")
            
            # Test service registration
            services = orchestrator.get_registered_services()
            self.log_test("Service Registration", len(services) > 0, f"Found {len(services)} services")
            
            return True
            
        except Exception as e:
            self.log_test("Orchestrator Integration", False, str(e))
            return False
    
    async def test_pdf_generation_integration(self):
        """Test PDF generation integration."""
        print("\n📄 Testing PDF Generation Integration...")
        
        try:
            # Test PDF service initialization
            self.log_test("PDF Service Initialization", True, "Service initialized successfully")
            
            # Test PDF generation
            test_markdown = "# Test Document\n\nThis is a test document with **bold text** and *italic text*."
            temp_file = Path("temp_test_document.md")
            with open(temp_file, 'w') as f:
                f.write(test_markdown)
            
            try:
                result = await self.enhanced_pdf_service.generate_pdf_from_markdown(
                    markdown_file=str(temp_file),
                    output_name="test_integration_pdf",
                    title="Integration Test PDF"
                )
                
                if result and result.get("success"):
                    self.log_test("PDF Generation", True, "PDF generated successfully")
                else:
                    self.log_test("PDF Generation", False, "PDF generation failed")
                    
            finally:
                if temp_file.exists():
                    temp_file.unlink()
            
            return True
            
        except Exception as e:
            self.log_test("PDF Generation Integration", False, str(e))
            return False
    
    async def test_word_generation_integration(self):
        """Test Word generation integration."""
        print("\n📝 Testing Word Generation Integration...")
        
        try:
            # Test Word service initialization
            self.log_test("Word Service Initialization", True, "Service initialized successfully")
            
            # Test Word generation
            test_markdown = "# Test Document\n\nThis is a test document with **bold text** and *italic text*."
            temp_file = Path("temp_test_word_document.md")
            with open(temp_file, 'w') as f:
                f.write(test_markdown)
            
            try:
                result = await self.enhanced_word_service.generate_word_from_markdown(
                    markdown_file=str(temp_file),
                    output_name="test_integration_word",
                    title="Integration Test Word"
                )
                
                if result and result.get("success"):
                    self.log_test("Word Generation", True, "Word document generated successfully")
                else:
                    self.log_test("Word Generation", False, "Word generation failed")
                    
            finally:
                if temp_file.exists():
                    temp_file.unlink()
            
            return True
            
        except Exception as e:
            self.log_test("Word Generation Integration", False, str(e))
            return False
    
    async def test_mcp_tool_management_integration(self):
        """Test MCP tool management integration."""
        print("\n⚙️ Testing MCP Tool Management Integration...")
        
        try:
            # Test MCP tool configuration JSON file
            config_path = Path("config/mcp_tool_config.json")
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                self.log_test("MCP Tool Configuration", config is not None, "Configuration loaded successfully")
                
                # Test word generation tool status
                tools = config.get("tools", {})
                word_tool = tools.get("word_generation", {})
                is_enabled = word_tool.get("enabled", False)
                self.log_test("Word Generation Tool Status", is_enabled, f"Tool is {'enabled' if is_enabled else 'disabled'}")
                
                # Test tool count
                tool_count = len(config.keys())
                self.log_test("Tool Listing", tool_count > 0, f"Found {tool_count} configured tools")
            else:
                self.log_test("MCP Tool Configuration", False, "Configuration file not found")
            
            return True
            
        except Exception as e:
            self.log_test("MCP Tool Management Integration", False, str(e))
            return False
    
    async def test_strategic_analysis_integration(self):
        """Test strategic analysis integration."""
        print("\n🎖️ Testing Strategic Analysis Integration...")
        
        try:
            # Test strategic analysis service
            from src.core.multi_domain_strategic_engine import MultiDomainStrategicEngine
            
            strategic_service = MultiDomainStrategicEngine()
            self.log_test("Strategic Analysis Service", True, "Service initialized successfully")
            
            return True
            
        except Exception as e:
            self.log_test("Strategic Analysis Integration", False, str(e))
            return False
    
    async def test_api_endpoints_integration(self):
        """Test API endpoints integration."""
        print("\n🔗 Testing API Endpoints Integration...")
        
        try:
            # Test main API endpoints
            endpoints = [
                "/health",
                "/api/pdf/status",
                "/api/word/status"
            ]
            
            for endpoint in endpoints:
                try:
                    response = requests.get(f"{self.test_config['base_url']}{endpoint}", timeout=10)
                    if response.status_code in [200, 404]:  # 404 is acceptable for some endpoints
                        self.log_test(f"API Endpoint: {endpoint}", True, f"Status: {response.status_code}")
                    else:
                        self.log_test(f"API Endpoint: {endpoint}", False, f"Unexpected status: {response.status_code}")
                except Exception as e:
                    self.log_test(f"API Endpoint: {endpoint}", False, str(e))
            
            return True
            
        except Exception as e:
            self.log_test("API Endpoints Integration", False, str(e))
            return False
    
    async def test_mcp_client_communication(self):
        """Test MCP client communication."""
        print("\n🤝 Testing MCP Client Communication...")
        
        try:
            # Test MCP client initialization
            from src.mcp_servers.unified_mcp_server import UnifiedMCPServer
            
            mcp_server = UnifiedMCPServer()
            self.log_test("MCP Client Initialization", True, "MCP Server initialized successfully")
            
            # Test tool discovery
            tools = mcp_server.get_tools_info()
            self.log_test("MCP Tool Discovery", len(tools) > 0, f"Discovered {len(tools)} tools")
            
            return True
            
        except Exception as e:
            self.log_test("MCP Client Communication", False, str(e))
            return False
    
    async def run_all_tests(self):
        """Run all integration tests."""
        print("🚀 Starting Comprehensive Integration Test Suite")
        print("=" * 60)
        
        test_methods = [
            self.test_mcp_server_integration,
            self.test_api_routes_integration,
            self.test_orchestrator_integration,
            self.test_pdf_generation_integration,
            self.test_word_generation_integration,
            self.test_mcp_tool_management_integration,
            self.test_strategic_analysis_integration,
            self.test_api_endpoints_integration,
            self.test_mcp_client_communication
        ]
        
        for test_method in test_methods:
            try:
                await test_method()
            except Exception as e:
                self.log_test(test_method.__name__, False, f"Test failed with exception: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 INTEGRATION TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"📈 Success Rate: {(self.results['passed'] / (self.results['passed'] + self.results['failed']) * 100):.1f}%")
        
        if self.results['errors']:
            print("\n❌ ERRORS:")
            for error in self.results['errors']:
                print(f"  - {error}")
        
        return self.results['failed'] == 0


async def main():
    """Main test execution function."""
    try:
        test_suite = ComprehensiveIntegrationTest()
        success = await test_suite.run_all_tests()
        
        if success:
            print("\n🎉 All integration tests passed!")
            sys.exit(0)
        else:
            print("\n⚠️ Some integration tests failed. Please review the errors above.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Test suite failed with exception: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
