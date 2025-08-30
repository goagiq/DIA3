#!/usr/bin/env python3
"""
Simple test to isolate async issues in the enhanced HTML report generator.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.enhanced_html_report_generator import EnhancedHTMLReportGenerator

async def test_simple_async():
    """Test simple async operations to isolate the issue."""
    
    print("🔍 Testing Simple Async Operations")
    print("=" * 40)
    
    # Initialize the generator
    generator = EnhancedHTMLReportGenerator()
    
    # Test data
    test_data = {
        "sections": [
            {
                "title": "Test Section",
                "content": "Test content"
            }
        ]
    }
    
    print("📊 Testing data normalization...")
    normalized_data = generator._validate_and_normalize(test_data)
    print(f"✅ Normalized data: {type(normalized_data)}")
    
    print("📄 Testing sections HTML generation...")
    sections_html = await generator._generate_sections_html(normalized_data)
    print(f"✅ Sections HTML length: {len(sections_html)}")
    
    print("📈 Testing charts HTML generation...")
    charts_html = await generator._generate_charts_html(normalized_data)
    print(f"✅ Charts HTML length: {len(charts_html)}")
    
    print("💡 Testing tooltips JS generation...")
    tooltips_js = await generator._generate_advanced_tooltips_js(normalized_data)
    print(f"✅ Tooltips JS length: {len(tooltips_js)}")
    
    print("🧭 Testing navigation HTML generation...")
    navigation_html = generator._generate_navigation_html()
    print(f"✅ Navigation HTML length: {len(navigation_html)}")
    
    print("🎉 All async operations completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_simple_async())
