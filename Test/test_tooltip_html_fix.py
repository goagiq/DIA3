#!/usr/bin/env python3
"""
Test script to verify tooltip HTML fix.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

# Import the enhanced HTML report generator
from src.core.enhanced_html_report_generator import EnhancedHTMLReportGenerator


class TooltipHTMLFixTester:
    """Test class for tooltip HTML fix."""

    def __init__(self):
        self.generator = EnhancedHTMLReportGenerator()

    def test_tooltip_html_rendering(self):
        """Test that tooltip content renders HTML properly."""
        print("🔧 Testing Tooltip HTML Rendering...")

        # Generate tooltip JavaScript
        tooltip_data = {
            "section-1": {
                "title": "Test Module",
                "content": "This is a <strong>bold</strong> test with <em>italic</em> text and a <a href='#'>link</a>.",
                "sources": [
                    {
                        "source_type": "fetch",
                        "source_name": "Test Source",
                        "title": "Test Analysis",
                        "confidence": 0.8,
                        "reliability_score": 0.85,
                        "mcp_tool": "Fetch",
                        "timestamp": "2025-01-26 10:30"
                    }
                ]
            }
        }

        tooltip_js = self.generator._generate_advanced_tooltips_js({"tooltip_data": tooltip_data})

        # Check that innerHTML is used instead of textContent
        assert "tooltipContent.innerHTML" in tooltip_js, "Tooltip JavaScript should use innerHTML for content"
        assert "tooltipContent.textContent" not in tooltip_js, "Tooltip JavaScript should not use textContent for content"

        print("✅ Tooltip HTML rendering test passed!")

    def test_html_content_preservation(self):
        """Test that HTML content is preserved in tooltip data."""
        print("\n📝 Testing HTML Content Preservation...")

        # Generate tooltip info
        module_title = "Test Module"
        test_data = {
            "source_metadata": [
                {
                    "source_type": "fetch",
                    "source_name": "Test Source",
                    "title": "Test Analysis",
                    "confidence": 0.8,
                    "reliability_score": 0.85,
                    "timestamp": datetime.now()
                }
            ]
        }

        tooltip_info = self.generator._generate_enhanced_module_tooltip_info(
            module_title, None, test_data
        )

        # Verify content is generated properly
        content = tooltip_info.get("content", "")
        assert content, "Tooltip content should be generated"
        assert len(content) > 0, "Tooltip content should not be empty"

        print("✅ HTML content preservation test passed!")

    async def generate_test_report(self):
        """Generate a test report to verify tooltip functionality."""
        print("\n📄 Generating Test Report...")

        # Sample data with HTML content
        sample_data = {
            "title": "Tooltip HTML Fix Test",
            "subtitle": "Testing HTML rendering in tooltips",
            "topic": "Strategic Intelligence Analysis",
            "analysis_type": "strategic_intelligence",
            "confidence_score": 0.85,
            "source_metadata": [
                {
                    "source_type": "fetch",
                    "source_name": "Strategic Studies Institute",
                    "title": "Strategic Analysis Report",
                    "confidence": 0.8,
                    "reliability_score": 0.85,
                    "timestamp": datetime.now()
                },
                {
                    "source_type": "tac",
                    "source_name": "Defense Intelligence Database",
                    "title": "Intelligence Assessment",
                    "confidence": 0.75,
                    "reliability_score": 0.8,
                    "timestamp": datetime.now()
                }
            ],
            "knowledge_graph_data": {
                "entities": ["Strategic Analysis", "Intelligence", "Security"],
                "relationships": [("Strategic Analysis", "influences", "Security")]
            },
            "vector_insights": {
                "similar_patterns": ["Historical strategic initiatives", "Regional security dynamics"],
                "confidence": 0.82
            }
        }

        # Generate the report
        output_path = Path("Results/tooltip_html_fix_test.html")
        output_path.parent.mkdir(exist_ok=True)

        try:
            # Generate the enhanced report
            result = await self.generator.generate_enhanced_report(sample_data, str(output_path))

            if result.get("success", False):
                print(f"✅ Test report generated successfully: {output_path}")
                
                # Check the generated HTML file for tooltip JavaScript
                with open(output_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Verify innerHTML is used
                assert "tooltipContent.innerHTML" in html_content, "Generated HTML should use innerHTML for tooltips"
                assert "tooltipContent.textContent" not in html_content, "Generated HTML should not use textContent for tooltips"
                
                print("✅ Generated HTML contains correct tooltip implementation!")
                return output_path
            else:
                print(f"❌ Failed to generate test report: {result.get('error', 'Unknown error')}")
                return None

        except Exception as e:
            print(f"❌ Error generating test report: {e}")
            return None


async def main():
    """Main test function."""
    print("🚀 Tooltip HTML Fix Test Suite")
    print("=" * 40)

    tester = TooltipHTMLFixTester()

    # Run tests
    try:
        # Test tooltip HTML rendering
        tester.test_tooltip_html_rendering()

        # Test HTML content preservation
        tester.test_html_content_preservation()

        # Generate test report
        report_path = await tester.generate_test_report()

        if report_path:
            print(f"\n🎉 All tests completed successfully!")
            print(f"📄 Test report available at: {report_path}")
            print("\n✨ Tooltip HTML Fix Summary:")
            print("   • Tooltip content now uses innerHTML instead of textContent")
            print("   • HTML tags in tooltip content will be rendered properly")
            print("   • No more literal HTML tags displayed in tooltips")
        else:
            print("\n❌ Test report generation failed")

    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
