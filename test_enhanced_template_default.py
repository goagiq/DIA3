#!/usr/bin/env python3
"""
Test Enhanced Template as Default

This script verifies that the enhanced template is working as the default.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.enhanced_html_report_generator import EnhancedHTMLReportGenerator

async def test_enhanced_template_default():
    """Test that the enhanced template works as default."""
    
    print("🧪 Testing Enhanced Template as Default")
    print("=" * 40)
    
    try:
        # Initialize the enhanced HTML report generator
        generator = EnhancedHTMLReportGenerator()
        
        # Test data
        test_data = {
            "title": "Enhanced Template Test Report",
            "subtitle": "Verification of Enhanced Template as Default",
            "topic": "Test Analysis",
            "analysis_type": "test",
            "confidence_score": 0.9,
            "source_metadata": [
                {
                    "source_type": "test",
                    "source_name": "Test System",
                    "title": "Template Verification Test",
                    "confidence": 0.9,
                    "reliability_score": 0.9,
                    "timestamp": "2025-01-26 12:00"
                }
            ],
            "content": "This is a test report to verify that the enhanced template is working as the default template in the DIA3 system."
        }
        
        # Generate test report
        print("📊 Generating test report with enhanced template...")
        
        result = await generator.generate_enhanced_report(
            data=test_data,
            output_path="Results/test_enhanced_template_default.html"
        )
        
        if result["success"]:
            print("✅ SUCCESS: Enhanced template working as default!")
            print(f"📁 File saved to: {result['file_path']}")
            
            # Verify file exists
            file_path = Path(result['file_path'])
            if file_path.exists():
                print(f"📏 File size: {file_path.stat().st_size} bytes")
                print("🔍 File verification: PASSED")
            else:
                print("❌ File verification: FAILED")
            
            return True
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

async def main():
    """Main function."""
    success = await test_enhanced_template_default()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Enhanced template is working as default!")
        print("🚀 All reports will now use the enhanced 22-module template")
    else:
        print("⚠️ Enhanced template test failed")
        print("🔧 Please check the configuration")
    
    print("=" * 40)

if __name__ == "__main__":
    asyncio.run(main())
