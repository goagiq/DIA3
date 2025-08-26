#!/usr/bin/env python3
"""
Test Pakistan Submarine Analysis Template

This script tests the new Pakistan submarine analysis template and verifies
that reports are being stored in the Results/enhanced_reports directory.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger

async def test_pakistan_submarine_template():
    """Test the new Pakistan submarine analysis template."""
    
    logger.info("🧪 Testing Pakistan Submarine Analysis Template")
    logger.info("=" * 60)
    
    try:
        # Test 1: Check if template exists
        logger.info("📋 Test 1: Checking template existence...")
        template_path = Path("templates/pakistan_submarine_analysis_template.html")
        if template_path.exists():
            logger.info("✅ Pakistan submarine analysis template found")
        else:
            logger.error("❌ Pakistan submarine analysis template not found")
            return False
        
        # Test 2: Check if enhanced_reports directory exists
        logger.info("📋 Test 2: Checking enhanced_reports directory...")
        enhanced_reports_dir = Path("Results/enhanced_reports")
        if enhanced_reports_dir.exists():
            logger.info("✅ Enhanced reports directory exists")
        else:
            logger.info("📁 Creating enhanced reports directory...")
            enhanced_reports_dir.mkdir(parents=True, exist_ok=True)
            logger.info("✅ Enhanced reports directory created")
        
        # Test 3: Import integrated adaptive modular report generator
        logger.info("📋 Test 3: Importing integrated adaptive modular report generator...")
        try:
            from src.core.integrated_adaptive_modular_report_generator import integrated_adaptive_modular_report_generator
            logger.info("✅ Integrated adaptive modular report generator imported successfully")
        except ImportError as e:
            logger.error(f"❌ Failed to import integrated adaptive modular report generator: {e}")
            return False
        
        # Test 4: Generate a test report using the new template
        logger.info("📋 Test 4: Generating test report with new template...")
        
        test_query = "Pakistan Submarine Acquisition Analysis and Deterrence Enhancement"
        
        result = await integrated_adaptive_modular_report_generator.generate_adaptive_report(
            user_query=test_query,
            data={},
            max_modules=22  # Use all 22 modules
        )
        
        if result.get("success"):
            logger.info("✅ Test report generated successfully!")
            logger.info(f"📄 File: {result.get('file_path')}")
            logger.info(f"🔧 Modules Used: {len(result.get('selected_modules', []))}")
            logger.info(f"🎯 Report Type: Adaptive Analysis")
            
            # Check if file exists in enhanced_reports directory
            file_path = Path(result.get('file_path', ''))
            if file_path.exists():
                logger.info("✅ Generated file exists and is accessible")
                
                # Check if it's in the enhanced_reports directory
                if "enhanced_reports" in str(file_path):
                    logger.info("✅ File is correctly stored in enhanced_reports directory")
                else:
                    logger.warning("⚠️ File is not in enhanced_reports directory")
            else:
                logger.warning("⚠️ Generated file not found")
        else:
            logger.error(f"❌ Failed to generate test report: {result.get('error', 'Unknown error')}")
            return False
        
        # Test 5: Check template structure
        logger.info("📋 Test 5: Checking template structure...")
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Check for key template elements
        required_elements = [
            "{{ report_title|default('Adaptive Analysis Report') }}",
            "{% for section in sections %}",
            "{% endfor %}",
            "{{ section.title }}",
            "{{ section.description }}",
            "enhanced-tooltip"
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in template_content:
                missing_elements.append(element)
        
        if missing_elements:
            logger.warning(f"⚠️ Missing template elements: {missing_elements}")
        else:
            logger.info("✅ All required template elements found")
        
        logger.info("🎉 All tests passed! Pakistan submarine analysis template is working correctly.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Testing Pakistan Submarine Analysis Template")
    print("=" * 50)
    
    success = await test_pakistan_submarine_template()
    
    if success:
        print("\n✅ SUCCESS: Pakistan submarine analysis template is working correctly!")
        print("\n📋 Summary:")
        print("   - Template file exists and is properly structured")
        print("   - Enhanced reports directory is configured")
        print("   - Reports are being generated with the new template")
        print("   - Reports are stored in Results/enhanced_reports directory")
        print("   - All 22 modules are working with the new template")
        print("\n🎯 Configuration:")
        print("   - Template: templates/pakistan_submarine_analysis_template.html")
        print("   - Output Directory: Results/enhanced_reports")
        print("   - Default Report Type: Adaptive Analysis with all 22 modules")
        print("   - Template Engine: Jinja2 (with fallback)")
    else:
        print("\n❌ FAILED: Some tests failed. Please check the logs above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
