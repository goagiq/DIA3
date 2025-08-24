#!/usr/bin/env python3
"""
Strategic Capability Module Test Script

This script tests the Strategic Capability Module functionality,
including advanced tooltip integration and chart generation.
"""

import asyncio
from loguru import logger

from src.core.modules.strategic_capability_module import StrategicCapabilityModule


async def test_strategic_capability_module():
    """Test the Strategic Capability Module functionality."""
    logger.info("=== Testing Strategic Capability Module ===")
    
    # Initialize module
    module = StrategicCapabilityModule()
    
    # Test data for strategic capability
    test_data = {
        "strategic_capability": {
            "capability_forecasts": {
                "forecasts": [
                    {"capability": "Naval Power Projection", "current": 0.65, "year_1": 0.70, "year_2": 0.75, "year_3": 0.80, "year_4": 0.85, "year_5": 0.90},
                    {"capability": "Strategic Deterrence", "current": 0.75, "year_1": 0.78, "year_2": 0.82, "year_3": 0.85, "year_4": 0.88, "year_5": 0.92},
                    {"capability": "Operational Readiness", "current": 0.70, "year_1": 0.73, "year_2": 0.76, "year_3": 0.79, "year_4": 0.82, "year_5": 0.85},
                    {"capability": "Technological Superiority", "current": 0.60, "year_1": 0.65, "year_2": 0.70, "year_3": 0.75, "year_4": 0.80, "year_5": 0.85},
                    {"capability": "Strategic Mobility", "current": 0.55, "year_1": 0.60, "year_2": 0.65, "year_3": 0.70, "year_4": 0.75, "year_5": 0.80}
                ]
            },
            "five_year_horizon": {
                "horizon_metrics": [
                    {"dimension": "Strategic Reach", "baseline": 0.60, "target": 0.85, "confidence": 0.80},
                    {"dimension": "Operational Flexibility", "baseline": 0.65, "target": 0.90, "confidence": 0.85},
                    {"dimension": "Technological Edge", "baseline": 0.55, "target": 0.80, "confidence": 0.75},
                    {"dimension": "Strategic Deterrence", "baseline": 0.75, "target": 0.95, "confidence": 0.90},
                    {"dimension": "Regional Influence", "baseline": 0.70, "target": 0.88, "confidence": 0.82}
                ]
            },
            "capability_planning": {
                "planning_phases": [
                    {"phase": "Phase 1: Foundation (Years 1-2)", "focus": "Infrastructure Development", "priority": "High", "resources": "40%", "success_metrics": "Infrastructure readiness, basic capabilities"},
                    {"phase": "Phase 2: Enhancement (Years 2-3)", "focus": "Capability Enhancement", "priority": "High", "resources": "35%", "success_metrics": "Enhanced capabilities, operational readiness"},
                    {"phase": "Phase 3: Optimization (Years 3-4)", "focus": "Advanced Capabilities", "priority": "Medium", "resources": "20%", "success_metrics": "Advanced capabilities, technological edge"},
                    {"phase": "Phase 4: Excellence (Years 4-5)", "focus": "Strategic Excellence", "priority": "Medium", "resources": "5%", "success_metrics": "Strategic superiority, regional leadership"}
                ],
                "summary": {
                    "total_phases": 4,
                    "total_duration": "5 years",
                    "total_investment": "$15.2B",
                    "expected_outcome": "Strategic superiority"
                }
            },
            "strategic_development": {
                "development_areas": [
                    {"area": "Technological Innovation", "current_level": 0.65, "target_level": 0.90, "investment": "$4.2B", "timeline": "3-5 years"},
                    {"area": "Operational Excellence", "current_level": 0.75, "target_level": 0.95, "investment": "$3.8B", "timeline": "2-4 years"},
                    {"area": "Strategic Partnerships", "current_level": 0.60, "target_level": 0.85, "investment": "$2.1B", "timeline": "1-3 years"},
                    {"area": "Human Capital Development", "current_level": 0.70, "target_level": 0.88, "investment": "$1.5B", "timeline": "2-3 years"},
                    {"area": "Infrastructure Modernization", "current_level": 0.55, "target_level": 0.80, "investment": "$3.6B", "timeline": "3-4 years"}
                ]
            }
        }
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Verify content
    checks = [
        ("Capability Forecasts", "Capability forecasts section"),
        ("5-Year Strategic Horizon", "5-year strategic horizon section"),
        ("Capability Planning", "Capability planning section"),
        ("Strategic Development", "Strategic development section"),
        ("chart-container", "Chart containers"),
        ("data-tooltip", "Tooltip attributes"),
        ("capabilityForecastsChart", "Capability forecasts chart"),
        ("fiveYearHorizonChart", "5-year horizon chart"),
        ("strategicDevelopmentChart", "Strategic development chart"),
        ("Chart.js", "Chart.js integration"),
        ("line", "Line chart"),
        ("radar", "Radar chart"),
        ("bar", "Bar chart")
    ]
    
    issues = []
    for check_text, description in checks:
        if check_text not in content:
            issues.append(f"Missing {description}")
    
    # Check tooltip functionality
    tooltip_checks = [
        "capability_forecasts",
        "five_year_horizon",
        "capability_planning",
        "strategic_development"
    ]
    
    tooltip_issues = []
    for tooltip_id in tooltip_checks:
        if f'data-tooltip-{module.module_id}="{tooltip_id}"' not in content:
            tooltip_issues.append(f"Missing tooltip: {tooltip_id}")
    
    # Check chart functionality
    chart_checks = [
        "capabilityForecastsChart",
        "fiveYearHorizonChart",
        "strategicDevelopmentChart"
    ]
    
    chart_issues = []
    for chart_id in chart_checks:
        if f'id="{chart_id}"' not in content:
            chart_issues.append(f"Missing chart: {chart_id}")
    
    total_issues = len(issues) + len(tooltip_issues) + len(chart_issues)
    
    if issues:
        logger.warning(f"⚠️ Found {len(issues)} content issues:")
        for issue in issues:
            logger.warning(f"  - {issue}")
    else:
        logger.info("✅ All content components verified successfully")
    
    if tooltip_issues:
        logger.warning(f"⚠️ Found {len(tooltip_issues)} tooltip issues:")
        for issue in tooltip_issues:
            logger.warning(f"  - {issue}")
    else:
        logger.info("✅ All tooltips verified successfully")
    
    if chart_issues:
        logger.warning(f"⚠️ Found {len(chart_issues)} chart issues:")
        for issue in chart_issues:
            logger.warning(f"  - {issue}")
    else:
        logger.info("✅ All charts verified successfully")
    
    if total_issues == 0:
        logger.info("✅ Strategic Capability Module test successful")
        logger.info(f"📄 Generated content length: {len(content)} characters")
        return True
    else:
        logger.warning(f"⚠️ {total_issues} issues found in Strategic Capability Module test")
        return False


async def test_strategic_capability_module_defaults():
    """Test the Strategic Capability Module with default data."""
    logger.info("=== Testing Strategic Capability Module with Defaults ===")
    
    # Initialize module
    module = StrategicCapabilityModule()
    
    # Test with minimal data
    test_data = {
        "strategic_capability": {}
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Basic checks
    checks = [
        "Capability Forecasts",
        "5-Year Strategic Horizon",
        "Capability Planning",
        "Strategic Development"
    ]
    
    success = True
    for check in checks:
        if check not in content:
            logger.error(f"Missing: {check}")
            success = False
    
    if success:
        logger.info("✅ Default data test successful")
        logger.info(f"📄 Generated content length: {len(content)} characters")
        return True
    else:
        logger.error("❌ Default data test failed")
        return False


async def main():
    """Run all strategic capability module tests."""
    logger.info("🚀 Starting Strategic Capability Module Tests")
    
    # Test 1: Full functionality test
    full_test_result = await test_strategic_capability_module()
    
    # Test 2: Default data test
    default_test_result = await test_strategic_capability_module_defaults()
    
    # Summary
    logger.info("📊 Test Summary:")
    logger.info(f"  Full Test: {'✅ PASS' if full_test_result else '❌ FAIL'}")
    logger.info(f"  Default Test: {'✅ PASS' if default_test_result else '❌ FAIL'}")
    
    if full_test_result and default_test_result:
        logger.info("🎉 All Strategic Capability Module tests passed!")
        return True
    else:
        logger.warning("⚠️ Some Strategic Capability Module tests failed")
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)
