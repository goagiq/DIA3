#!/usr/bin/env python3
"""
Simple Tooltip Fix Test

This script tests the basic tooltip functionality to identify specific issues.
"""

import asyncio
from pathlib import Path
from loguru import logger

from src.core.modular_report_generator import ModularReportGenerator


async def test_simple_tooltip():
    """Test simple tooltip functionality."""
    logger.info("=== Simple Tooltip Test ===")
    
    # Initialize generator
    generator = ModularReportGenerator()
    
    # Simple test data
    test_data = {
        "strategic_recommendations": {
            "immediate": [
                {
                    "title": "Test Recommendation",
                    "description": "Test description",
                    "priority": "High"
                }
            ],
            "short_term": [],
            "long_term": []
        },
        "intelligence_summary": {
            "key_findings": "Test findings",
            "threat_assessment": "Low"
        },
        "implementation_roadmap": {
            "phases": []
        }
    }
    
    try:
        # Generate report
        logger.info("Generating simple test report...")
        result = await generator.generate_modular_report(
            topic="Simple Tooltip Test",
            data=test_data,
            enabled_modules=["strategicrecommendationsmodule"],
            report_title="Simple Tooltip Test"
        )
        
        if result and "html_content" in result:
            html_content = result["html_content"]
            
            # Check for basic tooltip elements
            has_tooltip_div = 'id="enhancedTooltip"' in html_content
            has_tooltip_css = '.enhanced-tooltip' in html_content
            has_tooltip_js = 'function showEnhancedTooltip' in html_content
            
            logger.info(f"Tooltip div: {has_tooltip_div}")
            logger.info(f"Tooltip CSS: {has_tooltip_css}")
            logger.info(f"Tooltip JS: {has_tooltip_js}")
            
            # Save test report
            output_path = Path("Results/simple_tooltip_test.html")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Test report saved to: {output_path}")
            
            return {
                "success": True,
                "html_file": str(output_path),
                "tooltip_elements": {
                    "div": has_tooltip_div,
                    "css": has_tooltip_css,
                    "js": has_tooltip_js
                }
            }
        else:
            logger.error("No HTML content in result")
            return {"success": False, "error": "No HTML content"}
            
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return {"success": False, "error": str(e)}


async def main():
    """Run simple tooltip test."""
    logger.info("🚀 Simple Tooltip Fix Test")
    logger.info("=" * 30)
    
    result = await test_simple_tooltip()
    
    if result["success"]:
        logger.info("✅ Simple tooltip test completed successfully")
        logger.info(f"Tooltip elements: {result['tooltip_elements']}")
    else:
        logger.error(f"❌ Simple tooltip test failed: {result.get('error', 'Unknown error')}")
    
    return result


if __name__ == "__main__":
    asyncio.run(main())
