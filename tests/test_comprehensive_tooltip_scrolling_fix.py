#!/usr/bin/env python3
"""
Comprehensive Tooltip and Scrolling Fix Test

This script tests both the advanced tooltip system and chart scrolling fixes
to ensure all issues are resolved.
"""

import asyncio
from pathlib import Path
from loguru import logger

from src.core.modular_report_generator import ModularReportGenerator


async def test_comprehensive_fixes():
    """Test comprehensive fixes for tooltips and scrolling."""
    logger.info("=== Comprehensive Tooltip and Scrolling Fix Test ===")
    
    # Initialize generator
    generator = ModularReportGenerator()
    
    # Test data with multiple modules to test both tooltips and charts
    test_data = {
        "strategic_recommendations": {
            "immediate": [
                {
                    "title": "Immediate Action Required",
                    "description": "Critical strategic response needed",
                    "priority": "High",
                    "impact": "Significant"
                }
            ],
            "short_term": [
                {
                    "title": "Short-term Strategy",
                    "description": "Medium-term strategic planning",
                    "priority": "Medium",
                    "impact": "Moderate"
                }
            ],
            "long_term": [
                {
                    "title": "Long-term Vision",
                    "description": "Strategic vision for future",
                    "priority": "Low",
                    "impact": "Long-term"
                }
            ]
        },
        "intelligence_summary": {
            "key_findings": "Critical intelligence findings",
            "threat_assessment": "High threat level",
            "recommendations": "Immediate action required"
        },
        "implementation_roadmap": {
            "phases": [
                {"phase": "Phase 1", "duration": "3 months", "actions": ["Action 1", "Action 2"]},
                {"phase": "Phase 2", "duration": "6 months", "actions": ["Action 3", "Action 4"]}
            ]
        },
        "strategic_analysis": {
            "overview": "Strategic analysis overview",
            "components": ["Component 1", "Component 2", "Component 3"],
            "insights": ["Insight 1", "Insight 2", "Insight 3"],
            "geopolitical_impact": {
                "regions": ["Region 1", "Region 2"],
                "global_implications": ["Implication 1", "Implication 2"]
            },
            "strategic_implications": ["Implication 1", "Implication 2", "Implication 3"]
        },
        "strategic_insights": {
            "key_insights": ["Insight 1", "Insight 2"],
            "trends": ["Trend 1", "Trend 2"],
            "patterns": ["Pattern 1", "Pattern 2"]
        },
        "geopolitical_impact": {
            "regional_analysis": "Regional impact analysis",
            "global_implications": "Global implications"
        },
        "strategic_implications": {
            "immediate_effects": "Immediate strategic effects",
            "long_term_effects": "Long-term strategic effects"
        }
    }
    
    try:
        # Generate report with multiple modules
        logger.info("Generating comprehensive test report...")
        result = await generator.generate_modular_report(
            topic="Comprehensive Tooltip and Scrolling Test",
            data=test_data,
            enabled_modules=["strategicrecommendationsmodule", "strategicanalysismodule"],
            report_title="Comprehensive Fix Test"
        )
        
        if result and "html_content" in result:
            html_content = result["html_content"]
            
            # Test 1: Tooltip System
            logger.info("\n🧪 Test 1: Advanced Tooltip System")
            tooltip_issues = test_tooltip_system(html_content)
            
            # Test 2: Chart Scrolling
            logger.info("\n🧪 Test 2: Chart Scrolling Fix")
            scrolling_issues = test_chart_scrolling(html_content)
            
            # Test 3: Overall Integration
            logger.info("\n🧪 Test 3: System Integration")
            integration_issues = test_system_integration(html_content)
            
            # Save test report
            output_path = Path("Results/comprehensive_fix_test.html")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Test report saved to: {output_path}")
            
            # Summary
            all_issues = tooltip_issues + scrolling_issues + integration_issues
            
            if all_issues:
                logger.warning(f"\n⚠️ Found {len(all_issues)} issues:")
                for issue in all_issues:
                    logger.warning(f"  - {issue}")
            else:
                logger.info("\n🎉 All tests passed! No issues found.")
            
            return {
                "success": True,
                "html_file": str(output_path),
                "tooltip_issues": tooltip_issues,
                "scrolling_issues": scrolling_issues,
                "integration_issues": integration_issues,
                "total_issues": len(all_issues)
            }
        else:
            logger.error("No HTML content in result")
            return {"success": False, "error": "No HTML content"}
            
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return {"success": False, "error": str(e)}


def test_tooltip_system(html_content: str) -> list:
    """Test the advanced tooltip system."""
    issues = []
    
    # Check tooltip HTML structure
    required_tooltip_elements = [
        'id="enhancedTooltip"',
        'id="tooltipTitle"',
        'id="tooltipContent"',
        'id="tooltipSource"',
        'id="tooltipStrategic"',
        'id="tooltipRecommendations"',
        'id="tooltipUseCases"'
    ]
    
    for element in required_tooltip_elements:
        if element not in html_content:
            issues.append(f"Missing tooltip element: {element}")
    
    # Check tooltip CSS
    required_css_properties = [
        'position: absolute',
        'z-index: 1000',
        'display: none',
        'max-width: 400px'
    ]
    
    for property in required_css_properties:
        if property not in html_content:
            issues.append(f"Missing CSS property: {property}")
    
    # Check tooltip JavaScript
    required_js_functions = [
        'function showEnhancedTooltip',
        'function hideEnhancedTooltip',
        'mouseenter',
        'mouseleave'
    ]
    
    for function in required_js_functions:
        if function not in html_content:
            issues.append(f"Missing JavaScript function: {function}")
    
    # Check tooltip data attributes
    if 'data-tooltip-' not in html_content:
        issues.append("Missing tooltip data attributes")
    
    # Check tooltip data
    if 'TooltipData' not in html_content:
        issues.append("Missing tooltip data")
    
    logger.info(f"Tooltip system: {len(issues)} issues found")
    return issues


def test_chart_scrolling(html_content: str) -> list:
    """Test chart scrolling fixes."""
    issues = []
    
    # Check chart container CSS
    required_chart_css = [
        '.chart-container {',
        'position: relative',
        'height: 300px',
        'overflow: hidden'
    ]
    
    for css in required_chart_css:
        if css not in html_content:
            issues.append(f"Missing chart CSS: {css}")
    
    # Check canvas sizing
    required_canvas_css = [
        'width: 100% !important',
        'height: 100% !important',
        'max-width: 100% !important',
        'max-height: 100% !important'
    ]
    
    for css in required_canvas_css:
        if css not in html_content:
            issues.append(f"Missing canvas CSS: {css}")
    
    # Check chart container HTML structure
    if '<div class="chart-container">' not in html_content:
        issues.append("Missing chart container HTML structure")
    
    # Check responsive settings
    if 'maintainAspectRatio' not in html_content:
        issues.append("Missing responsive chart settings")
    
    logger.info(f"Chart scrolling: {len(issues)} issues found")
    return issues


def test_system_integration(html_content: str) -> list:
    """Test overall system integration."""
    issues = []
    
    # Check for proper HTML structure
    required_html_elements = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '<body>',
        '</html>'
    ]
    
    for element in required_html_elements:
        if element not in html_content:
            issues.append(f"Missing HTML element: {element}")
    
    # Check for Chart.js integration
    if 'chart.js' not in html_content:
        issues.append("Missing Chart.js integration")
    
    # Check for proper script loading
    if '<script src=' not in html_content:
        issues.append("Missing script loading")
    
    # Check for proper CSS loading
    if '<style>' not in html_content:
        issues.append("Missing CSS loading")
    
    # Check for module content
    if 'class="section"' not in html_content:
        issues.append("Missing module sections")
    
    # Check for proper data attributes
    if 'data-tooltip-' not in html_content:
        issues.append("Missing data attributes")
    
    logger.info(f"System integration: {len(issues)} issues found")
    return issues


async def main():
    """Run comprehensive fix test."""
    logger.info("🚀 Comprehensive Tooltip and Scrolling Fix Test")
    logger.info("=" * 55)
    
    result = await test_comprehensive_fixes()
    
    if result["success"]:
        logger.info("\n📊 Test Summary")
        logger.info("=" * 30)
        logger.info(f"Tooltip issues: {len(result['tooltip_issues'])}")
        logger.info(f"Scrolling issues: {len(result['scrolling_issues'])}")
        logger.info(f"Integration issues: {len(result['integration_issues'])}")
        logger.info(f"Total issues: {result['total_issues']}")
        
        if result['total_issues'] == 0:
            logger.info("🎉 All comprehensive tests passed!")
        else:
            logger.warning("⚠️ Some issues need attention")
    else:
        logger.error(f"❌ Test failed: {result.get('error', 'Unknown error')}")
    
    return result


if __name__ == "__main__":
    asyncio.run(main())
