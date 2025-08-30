#!/usr/bin/env python3
"""
Advanced Tooltip Fix Test Script

This script tests and identifies issues with the advanced tooltip system
in the modular report generator and provides fixes.
"""

import asyncio
from pathlib import Path
from loguru import logger
import json

from src.core.modular_report_generator import ModularReportGenerator
from src.core.modules.base_module import BaseModule, ModuleConfig, TooltipData
from src.core.modules.strategic_recommendations_module import StrategicRecommendationsModule


async def test_tooltip_functionality():
    """Test tooltip functionality and identify issues."""
    logger.info("=== Testing Advanced Tooltip System ===")
    
    # Initialize generator
    generator = ModularReportGenerator()
    
    # Test data with tooltip information
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
        }
    }
    
    # Generate report
    logger.info("Generating test report...")
    result = await generator.generate_modular_report(
        topic="Advanced Tooltip Test",
        data=test_data,
        enabled_modules=["strategicrecommendationsmodule"],
        report_title="Advanced Tooltip System Test"
    )
    
    if result and "html_content" in result:
        html_content = result["html_content"]
        
        # Check for tooltip elements
        logger.info("Analyzing tooltip implementation...")
        
        # Check for tooltip HTML structure
        has_tooltip_div = 'id="enhancedTooltip"' in html_content
        has_tooltip_title = 'id="tooltipTitle"' in html_content
        has_tooltip_content = 'id="tooltipContent"' in html_content
        has_tooltip_source = 'id="tooltipSource"' in html_content
        has_tooltip_strategic = 'id="tooltipStrategic"' in html_content
        has_tooltip_recommendations = 'id="tooltipRecommendations"' in html_content
        has_tooltip_use_cases = 'id="tooltipUseCases"' in html_content
        
        logger.info(f"Tooltip div: {has_tooltip_div}")
        logger.info(f"Tooltip title: {has_tooltip_title}")
        logger.info(f"Tooltip content: {has_tooltip_content}")
        logger.info(f"Tooltip source: {has_tooltip_source}")
        logger.info(f"Tooltip strategic: {has_tooltip_strategic}")
        logger.info(f"Tooltip recommendations: {has_tooltip_recommendations}")
        logger.info(f"Tooltip use cases: {has_tooltip_use_cases}")
        
        # Check for tooltip CSS
        has_tooltip_css = '.enhanced-tooltip' in html_content
        has_tooltip_position = 'position: absolute' in html_content
        has_tooltip_z_index = 'z-index: 1000' in html_content
        has_tooltip_display = 'display: none' in html_content
        
        logger.info(f"Tooltip CSS: {has_tooltip_css}")
        logger.info(f"Tooltip position: {has_tooltip_position}")
        logger.info(f"Tooltip z-index: {has_tooltip_z_index}")
        logger.info(f"Tooltip display: {has_tooltip_display}")
        
        # Check for tooltip JavaScript
        has_show_tooltip_function = 'function showEnhancedTooltip' in html_content
        has_hide_tooltip_function = 'function hideEnhancedTooltip' in html_content
        has_mouseover_events = 'mouseenter' in html_content
        has_mouseleave_events = 'mouseleave' in html_content
        
        logger.info(f"Show tooltip function: {has_show_tooltip_function}")
        logger.info(f"Hide tooltip function: {has_hide_tooltip_function}")
        logger.info(f"Mouseover events: {has_mouseover_events}")
        logger.info(f"Mouseleave events: {has_mouseleave_events}")
        
        # Check for tooltip data attributes
        has_tooltip_data_attrs = 'data-tooltip-' in html_content
        
        logger.info(f"Tooltip data attributes: {has_tooltip_data_attrs}")
        
        # Identify issues
        issues = []
        
        if not has_tooltip_div:
            issues.append("Missing enhanced tooltip div")
        if not has_tooltip_css:
            issues.append("Missing tooltip CSS styles")
        if not has_show_tooltip_function:
            issues.append("Missing showEnhancedTooltip function")
        if not has_hide_tooltip_function:
            issues.append("Missing hideEnhancedTooltip function")
        if not has_tooltip_data_attrs:
            issues.append("Missing tooltip data attributes")
        
        if issues:
            logger.warning(f"Found {len(issues)} tooltip issues:")
            for issue in issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info("✅ No tooltip issues found")
        
        # Save test report
        output_path = Path("Results/advanced_tooltip_test.html")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Test report saved to: {output_path}")
        
        return {
            "success": True,
            "issues": issues,
            "html_file": str(output_path),
            "tooltip_elements": {
                "div": has_tooltip_div,
                "css": has_tooltip_css,
                "javascript": has_show_tooltip_function and has_hide_tooltip_function,
                "events": has_mouseover_events and has_mouseleave_events,
                "data_attrs": has_tooltip_data_attrs
            }
        }
    else:
        logger.error("Failed to generate test report")
        return {"success": False, "error": "Report generation failed"}


async def test_tooltip_data_integration():
    """Test tooltip data integration in modules."""
    logger.info("=== Testing Tooltip Data Integration ===")
    
    # Create a test module with tooltips
    module = StrategicRecommendationsModule()
    
    # Add tooltip data
    tooltip_data = TooltipData(
        title="Strategic Recommendation",
        description="This is a critical strategic recommendation",
        source="Intelligence Analysis",
        strategic_impact="High impact on national security",
        recommendations="Implement immediately",
        use_cases="Military planning, policy development",
        confidence=0.95
    )
    
    module.add_tooltip("rec-1", tooltip_data)
    
    # Generate tooltip script
    tooltip_script = module.generate_tooltip_script()
    
    logger.info(f"Tooltip script generated: {len(tooltip_script)} characters")
    
    # Check script content
    has_tooltip_data = 'strategicrecommendationsmoduleTooltipData' in tooltip_script
    has_event_listeners = 'addEventListener' in tooltip_script
    has_show_function_call = 'showEnhancedTooltip' in tooltip_script
    has_hide_function_call = 'hideEnhancedTooltip' in tooltip_script
    
    logger.info(f"Tooltip data in script: {has_tooltip_data}")
    logger.info(f"Event listeners: {has_event_listeners}")
    logger.info(f"Show function call: {has_show_function_call}")
    logger.info(f"Hide function call: {has_hide_function_call}")
    
    # Check for issues
    issues = []
    
    if not has_tooltip_data:
        issues.append("Missing tooltip data in script")
    if not has_event_listeners:
        issues.append("Missing event listeners")
    if not has_show_function_call:
        issues.append("Missing showEnhancedTooltip call")
    if not has_hide_function_call:
        issues.append("Missing hideEnhancedTooltip call")
    
    if issues:
        logger.warning(f"Found {len(issues)} tooltip integration issues:")
        for issue in issues:
            logger.warning(f"  - {issue}")
    else:
        logger.info("✅ No tooltip integration issues found")
    
    return {
        "success": True,
        "issues": issues,
        "script_length": len(tooltip_script),
        "script_components": {
            "tooltip_data": has_tooltip_data,
            "event_listeners": has_event_listeners,
            "show_function": has_show_function_call,
            "hide_function": has_hide_function_call
        }
    }


async def test_tooltip_positioning():
    """Test tooltip positioning and display."""
    logger.info("=== Testing Tooltip Positioning ===")
    
    # Create test HTML with tooltip positioning
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        .enhanced-tooltip {
            position: absolute;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            font-size: 0.95em;
            z-index: 1000;
            max-width: 400px;
            display: none;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255,255,255,0.2);
        }
        </style>
    </head>
    <body>
        <div class="enhanced-tooltip" id="enhancedTooltip">
            <div class="tooltip-title" id="tooltipTitle"></div>
            <div class="tooltip-content" id="tooltipContent"></div>
            <div class="tooltip-source" id="tooltipSource"></div>
            <div class="tooltip-strategic" id="tooltipStrategic"></div>
            <div class="tooltip-recommendations" id="tooltipRecommendations"></div>
            <div class="tooltip-use-cases" id="tooltipUseCases"></div>
        </div>
        
        <script>
        function showEnhancedTooltip(event, tooltipData) {
            const tooltip = document.getElementById('enhancedTooltip');
            const title = document.getElementById('tooltipTitle');
            const content = document.getElementById('tooltipContent');
            const source = document.getElementById('tooltipSource');
            const strategic = document.getElementById('tooltipStrategic');
            const recommendations = document.getElementById('tooltipRecommendations');
            const useCases = document.getElementById('tooltipUseCases');
            
            title.textContent = tooltipData.title;
            content.innerHTML = tooltipData.description;
            source.innerHTML = tooltipData.source;
            strategic.innerHTML = tooltipData.strategic_impact;
            
            if (tooltipData.recommendations) {
                recommendations.innerHTML = '<strong>💡 Recommendations:</strong><br/>' + tooltipData.recommendations;
                recommendations.style.display = 'block';
            } else {
                recommendations.style.display = 'none';
            }
            
            if (tooltipData.use_cases) {
                useCases.innerHTML = '<strong>🎯 Use Cases:</strong><br/>' + tooltipData.use_cases;
                useCases.style.display = 'block';
            } else {
                useCases.style.display = 'none';
            }
            
            tooltip.style.display = 'block';
            tooltip.style.left = event.pageX + 10 + 'px';
            tooltip.style.top = event.pageY - 10 + 'px';
        }
        
        function hideEnhancedTooltip() {
            document.getElementById('enhancedTooltip').style.display = 'none';
        }
        </script>
    </body>
    </html>
    """
    
    # Save test HTML
    output_path = Path("Results/tooltip_positioning_test.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    logger.info(f"Tooltip positioning test saved to: {output_path}")
    
    # Check for positioning issues
    has_position_absolute = 'position: absolute' in test_html
    has_z_index = 'z-index: 1000' in test_html
    has_pageX_positioning = 'event.pageX' in test_html
    has_pageY_positioning = 'event.pageY' in test_html
    has_display_block = 'display: \'block\'' in test_html
    has_display_none = 'display: \'none\'' in test_html
    
    logger.info(f"Position absolute: {has_position_absolute}")
    logger.info(f"Z-index: {has_z_index}")
    logger.info(f"PageX positioning: {has_pageX_positioning}")
    logger.info(f"PageY positioning: {has_pageY_positioning}")
    logger.info(f"Display block: {has_display_block}")
    logger.info(f"Display none: {has_display_none}")
    
    issues = []
    
    if not has_position_absolute:
        issues.append("Missing position: absolute")
    if not has_z_index:
        issues.append("Missing z-index")
    if not has_pageX_positioning:
        issues.append("Missing pageX positioning")
    if not has_pageY_positioning:
        issues.append("Missing pageY positioning")
    if not has_display_block:
        issues.append("Missing display: block")
    if not has_display_none:
        issues.append("Missing display: none")
    
    if issues:
        logger.warning(f"Found {len(issues)} positioning issues:")
        for issue in issues:
            logger.warning(f"  - {issue}")
    else:
        logger.info("✅ No positioning issues found")
    
    return {
        "success": True,
        "issues": issues,
        "html_file": str(output_path),
        "positioning_components": {
            "position_absolute": has_position_absolute,
            "z_index": has_z_index,
            "pageX": has_pageX_positioning,
            "pageY": has_pageY_positioning,
            "display_block": has_display_block,
            "display_none": has_display_none
        }
    }


async def main():
    """Run all tooltip tests."""
    logger.info("🚀 Advanced Tooltip Fix Test Suite")
    logger.info("=" * 50)
    
    # Run tests
    results = {}
    
    # Test 1: Tooltip functionality
    logger.info("\n🧪 Test 1: Tooltip Functionality")
    results["functionality"] = await test_tooltip_functionality()
    
    # Test 2: Tooltip data integration
    logger.info("\n🧪 Test 2: Tooltip Data Integration")
    results["integration"] = await test_tooltip_data_integration()
    
    # Test 3: Tooltip positioning
    logger.info("\n🧪 Test 3: Tooltip Positioning")
    results["positioning"] = await test_tooltip_positioning()
    
    # Summary
    logger.info("\n📊 Test Summary")
    logger.info("=" * 50)
    
    total_issues = 0
    for test_name, result in results.items():
        if result["success"]:
            issues = result.get("issues", [])
            total_issues += len(issues)
            logger.info(f"✅ {test_name}: {len(issues)} issues found")
        else:
            logger.error(f"❌ {test_name}: Failed")
    
    if total_issues == 0:
        logger.info("🎉 All tooltip tests passed! No issues found.")
    else:
        logger.warning(f"⚠️ Found {total_issues} total tooltip issues that need fixing.")
    
    return results


if __name__ == "__main__":
    asyncio.run(main())
