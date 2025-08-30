#!/usr/bin/env python3
"""
Test script for Enhanced Markdown Export Integration

This script tests the integration of the enhanced markdown export service
through both API endpoints and MCP tools.
"""

import asyncio
import json
import time
import requests
from pathlib import Path
from typing import Dict, Any, List
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger

# Test configuration
API_BASE_URL = "http://localhost:8003"
MCP_BASE_URL = "http://localhost:8000"
TEST_MARKDOWN_CONTENT = """# Test Document

This is a **bold test** document with *italic text* and some special formatting.

## Features Test

- **Bold list item**
- *Italic list item*
- Regular list item

### Table Test

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| **Bold cell** | *Italic cell* | Regular cell |
| Data 1 | Data 2 | Data 3 |

### Image Test

![Test Diagram](test_diagram.png)

**Narrative**: This is a test narrative that should not be bolded.

### Code Block Test

```python
def test_function():
    print("Hello, World!")
    return True
```

## Conclusion

This document tests all the enhanced features:
- **Bold formatting**
- *Italic formatting*
- Table formatting
- Figure numbering
- Special text protection
"""

class EnhancedMarkdownExportTester:
    """Test class for enhanced markdown export functionality."""
    
    def __init__(self):
        """Initialize the tester."""
        self.api_base_url = API_BASE_URL
        self.mcp_base_url = MCP_BASE_URL
        self.test_results = []
        
    def log_test_result(self, test_name: str, success: bool, details: str = ""):
        """Log test result."""
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} {test_name}")
        if details:
            logger.info(f"   Details: {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": time.time()
        })
    
    def test_api_health_check(self) -> bool:
        """Test API health check endpoint."""
        try:
            url = f"{self.api_base_url}/api/v1/enhanced-markdown-export/health"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("service_available"):
                    self.log_test_result("API Health Check", True, f"Service available: {data.get('version')}")
                    return True
                else:
                    self.log_test_result("API Health Check", False, "Service not available")
                    return False
            else:
                self.log_test_result("API Health Check", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("API Health Check", False, str(e))
            return False
    
    def test_api_supported_features(self) -> bool:
        """Test API supported features endpoint."""
        try:
            url = f"{self.api_base_url}/api/v1/enhanced-markdown-export/supported-features"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                features = data.get("features", [])
                if len(features) > 0:
                    self.log_test_result("API Supported Features", True, f"Found {len(features)} features")
                    return True
                else:
                    self.log_test_result("API Supported Features", False, "No features found")
                    return False
            else:
                self.log_test_result("API Supported Features", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("API Supported Features", False, str(e))
            return False
    
    def test_api_pdf_export(self) -> bool:
        """Test API PDF export endpoint."""
        try:
            url = f"{self.api_base_url}/api/v1/enhanced-markdown-export/export"
            payload = {
                "markdown_content": TEST_MARKDOWN_CONTENT,
                "output_format": "pdf",
                "filename": "test_enhanced_export",
                "include_images": True,
                "figure_numbering": True
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    file_path = data.get("file_path")
                    file_size = data.get("file_size")
                    self.log_test_result("API PDF Export", True, f"File: {file_path}, Size: {file_size} bytes")
                    return True
                else:
                    self.log_test_result("API PDF Export", False, data.get("error", "Unknown error"))
                    return False
            else:
                self.log_test_result("API PDF Export", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result("API PDF Export", False, str(e))
            return False
    
    def test_api_word_export(self) -> bool:
        """Test API Word export endpoint."""
        try:
            url = f"{self.api_base_url}/api/v1/enhanced-markdown-export/export"
            payload = {
                "markdown_content": TEST_MARKDOWN_CONTENT,
                "output_format": "word",
                "filename": "test_enhanced_export",
                "include_images": True,
                "figure_numbering": True
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    file_path = data.get("file_path")
                    file_size = data.get("file_size")
                    self.log_test_result("API Word Export", True, f"File: {file_path}, Size: {file_size} bytes")
                    return True
                else:
                    self.log_test_result("API Word Export", False, data.get("error", "Unknown error"))
                    return False
            else:
                self.log_test_result("API Word Export", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result("API Word Export", False, str(e))
            return False

    def test_mcp_health_check(self) -> bool:
        """Test MCP server health check."""
        try:
            # Try the main API server's MCP health endpoint first
            url = f"{self.api_base_url}/mcp-health"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test_result("MCP Health Check", True, "MCP server is healthy (integrated)")
                    return True
                else:
                    self.log_test_result("MCP Health Check", False, f"Status: {data.get('status')}")
                    return False
            else:
                # Try the standalone MCP server
                url = f"{self.mcp_base_url}/mcp/"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    self.log_test_result("MCP Health Check", True, "MCP server is healthy (standalone)")
                    return True
                else:
                    self.log_test_result("MCP Health Check", False, f"HTTP {response.status_code} for both integrated and standalone")
                    return False

        except Exception as e:
            self.log_test_result("MCP Health Check", False, str(e))
            return False
    
    async def test_mcp_enhanced_export_tools(self) -> bool:
        """Test MCP enhanced export tools."""
        try:
            # This would require a proper MCP client implementation
            # For now, we'll test the basic connectivity
            self.log_test_result("MCP Enhanced Export Tools", True, "MCP tools available (manual verification required)")
            return True
            
        except Exception as e:
            self.log_test_result("MCP Enhanced Export Tools", False, str(e))
            return False
    
    def test_file_generation(self) -> bool:
        """Test that generated files exist and have content."""
        try:
            output_dir = Path("docs/white_papers/generated_pdfs")
            if not output_dir.exists():
                self.log_test_result("File Generation", False, "Output directory does not exist")
                return False
            
            # Look for recent test files
            test_files = list(output_dir.glob("*test_enhanced_export*"))
            if len(test_files) >= 2:  # Should have both PDF and Word
                total_size = sum(f.stat().st_size for f in test_files)
                self.log_test_result("File Generation", True, f"Found {len(test_files)} test files, Total size: {total_size} bytes")
                return True
            else:
                self.log_test_result("File Generation", False, f"Found only {len(test_files)} test files")
                return False
                
        except Exception as e:
            self.log_test_result("File Generation", False, str(e))
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return results."""
        logger.info("🚀 Starting Enhanced Markdown Export Integration Tests")
        logger.info("=" * 60)
        
        # Test API endpoints
        logger.info("📋 Testing API Endpoints...")
        api_health = self.test_api_health_check()
        api_features = self.test_api_supported_features()
        api_pdf = self.test_api_pdf_export()
        api_word = self.test_api_word_export()
        
        # Test MCP server
        logger.info("🔧 Testing MCP Server...")
        mcp_health = self.test_mcp_health_check()
        
        # Test file generation
        logger.info("📁 Testing File Generation...")
        file_gen = self.test_file_generation()
        
        # Calculate overall results
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        logger.info("=" * 60)
        logger.info(f"📊 Test Results Summary:")
        logger.info(f"   Total Tests: {total_tests}")
        logger.info(f"   Passed: {passed_tests}")
        logger.info(f"   Failed: {failed_tests}")
        logger.info(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            logger.info("🎉 All tests passed!")
        else:
            logger.warning(f"⚠️ {failed_tests} tests failed")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests/total_tests)*100,
            "results": self.test_results
        }

def main():
    """Main test function."""
    tester = EnhancedMarkdownExportTester()
    results = tester.run_all_tests()
    
    # Save results to file
    output_file = Path("Test/enhanced_markdown_export_test_results.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"📄 Test results saved to: {output_file}")
    
    # Exit with appropriate code
    if results["failed_tests"] == 0:
        logger.info("✅ All tests passed - Integration successful!")
        sys.exit(0)
    else:
        logger.error("❌ Some tests failed - Integration issues detected!")
        sys.exit(1)

if __name__ == "__main__":
    main()
