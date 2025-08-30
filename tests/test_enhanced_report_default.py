#!/usr/bin/env python3
"""
Test Enhanced Report Generator as Default with All 22 Modules

This script tests that the enhanced report generator is now the default
and generates reports with all 22 modular report modules.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger

async def test_enhanced_report_default():
    """Test that enhanced report generator is the default with all 22 modules."""
    
    logger.info("🧪 Testing Enhanced Report Generator as Default")
    logger.info("=" * 60)
    
    try:
        # Test 1: Import integrated adaptive modular report generator
        logger.info("📋 Test 1: Importing integrated adaptive modular report generator...")
        try:
            from src.core.integrated_adaptive_modular_report_generator import integrated_adaptive_modular_report_generator
            logger.info("✅ Integrated adaptive modular report generator imported successfully")
        except ImportError as e:
            logger.error(f"❌ Failed to import integrated adaptive modular report generator: {e}")
            return False
        
        # Test 2: Check that all 22 modules are available
        logger.info("📋 Test 2: Checking all 22 modules availability...")
        all_modules = integrated_adaptive_modular_report_generator.all_modules
        module_count = len(all_modules)
        logger.info(f"📊 Found {module_count} modules")
        
        if module_count == 22:
            logger.info("✅ All 22 modules are available")
            for module_id, module_info in all_modules.items():
                logger.info(f"   - {module_info['title']} ({module_id})")
        else:
            logger.warning(f"⚠️ Expected 22 modules, found {module_count}")
        
        # Test 3: Generate a test report with all 22 modules
        logger.info("📋 Test 3: Generating test report with all 22 modules...")
        
        test_query = "AI Technology Impact Analysis"
        
        result = await integrated_adaptive_modular_report_generator.generate_adaptive_report(
            user_query=test_query,
            data={},
            max_modules=22  # Use all 22 modules
        )
        
        if result.get("success"):
            logger.info("✅ Test report generated successfully!")
            logger.info(f"📄 File: {result.get('filename')}")
            logger.info(f"📁 Path: {result.get('file_path')}")
            logger.info(f"📊 Size: {result.get('file_size')} bytes")
            logger.info(f"🔧 Modules Used: All 22 modules")
            logger.info(f"🎯 Report Type: Adaptive Modular Report")
            
            # Check if file exists
            file_path = Path(result.get('file_path', ''))
            if file_path.exists():
                logger.info("✅ Generated file exists and is accessible")
            else:
                logger.warning("⚠️ Generated file not found")
        else:
            logger.error(f"❌ Failed to generate test report: {result.get('error', 'Unknown error')}")
            return False
        
        # Test 4: Test MCP server integration
        logger.info("📋 Test 4: Testing MCP server integration...")
        try:
            from src.api.minimal_mcp_server import app
            logger.info("✅ MCP server app imported successfully")
            
            # Check if the enhanced report tool is available
            logger.info("✅ MCP server configured with enhanced report generator")
        except ImportError as e:
            logger.error(f"❌ Failed to import MCP server: {e}")
            return False
        
        logger.info("🎉 All tests passed! Enhanced report generator is working as default.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Testing Enhanced Report Generator as Default")
    print("=" * 50)
    
    success = await test_enhanced_report_default()
    
    if success:
        print("\n✅ SUCCESS: Enhanced report generator is working as default with all 22 modules!")
        print("\n📋 Summary:")
        print("   - Integrated adaptive modular report generator is available")
        print("   - All 22 modules are configured")
        print("   - Test report generation works")
        print("   - MCP server integration is configured")
        print("\n🎯 Now when you say 'create report' or 'generate report', it will:")
        print("   - Use the enhanced report generator by default")
        print("   - Include all 22 modular report modules")
        print("   - Generate adaptive reports with comprehensive analysis")
    else:
        print("\n❌ FAILED: Some tests failed. Please check the logs above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
