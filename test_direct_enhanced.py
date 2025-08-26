#!/usr/bin/env python3
"""
Direct test of the enhanced HTML report generator without modular system.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_direct_enhanced():
    """Test the enhanced HTML report generator directly."""
    
    print("🔍 Testing Direct Enhanced HTML Report Generator")
    print("=" * 50)
    
    try:
        print("📋 Importing EnhancedHTMLReportGenerator...")
        from core.enhanced_html_report_generator import EnhancedHTMLReportGenerator
        print("✅ Import successful")
        
        print("📋 Creating instance...")
        generator = EnhancedHTMLReportGenerator()
        print("✅ Instance created")
        
        # Test data
        test_data = {
            "sections": [
                {
                    "title": "Test Section",
                    "content": "Test content"
                }
            ]
        }
        
        # Generate the report
        output_path = "Results/Test_Direct_Enhanced_20250825_192000.html"
        
        print(f"📊 Generating report...")
        print(f"📁 Output file: {output_path}")
        
        result = await generator.generate_enhanced_report(test_data, output_path)
        
        if result["success"]:
            print("✅ Report generated successfully!")
            print(f"📄 File: {result['file_path']}")
            
            # Check validation results
            validation = result.get("validation_results", {})
            if validation:
                print(f"📋 Validation: {validation.get('summary', 'No summary')}")
                print(f"📊 Overall Success: {validation.get('overall_success', False)}")
            
        else:
            print(f"❌ Report generation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print("🎉 Test completed!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_direct_enhanced())
