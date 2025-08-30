#!/usr/bin/env python3
"""
Scenario Analysis Module Test Script

This script tests the Scenario Analysis Module functionality,
including advanced tooltip integration and chart generation.
"""

import asyncio
from loguru import logger

from src.core.modules.scenario_analysis_module import ScenarioAnalysisModule


async def test_scenario_analysis_module():
    """Test the Scenario Analysis Module functionality."""
    logger.info("=== Testing Scenario Analysis Module ===")
    
    # Initialize module
    module = ScenarioAnalysisModule()
    
    # Test data for scenario analysis
    test_data = {
        "scenario_analysis": {
            "scenario_overview": {
                "scenarios": [
                    {"scenario": "Optimistic", "probability": 0.25, "impact": "High", "timeline": "2-3 years", "key_factors": "Accelerated delivery, Enhanced training"},
                    {"scenario": "Baseline", "probability": 0.50, "impact": "Medium", "timeline": "3-4 years", "key_factors": "Standard delivery, Normal training"},
                    {"scenario": "Pessimistic", "probability": 0.25, "impact": "Low", "timeline": "4-5 years", "key_factors": "Delivery delays, Training challenges"}
                ]
            },
            "prediction_scenarios": {
                "predictions": [
                    {"prediction": "Submarine Delivery", "confidence": 0.85, "timeline": "2025-2027", "factors": "Manufacturing capacity, Training programs"},
                    {"prediction": "Regional Response", "confidence": 0.78, "timeline": "2025-2026", "factors": "Diplomatic relations, Military posture"},
                    {"prediction": "Economic Impact", "confidence": 0.72, "timeline": "2025-2028", "factors": "Trade patterns, Investment flows"},
                    {"prediction": "Strategic Balance", "confidence": 0.80, "timeline": "2026-2029", "factors": "Military capabilities, Alliances"}
                ]
            },
            "multi_scenario_analysis": {
                "metrics": [
                    {"metric": "Scenario Coverage", "value": 0.95, "unit": "%", "status": "Excellent"},
                    {"metric": "Prediction Accuracy", "value": 0.88, "unit": "%", "status": "Good"},
                    {"metric": "Risk Assessment", "value": 0.82, "unit": "%", "status": "Good"},
                    {"metric": "Timeline Reliability", "value": 0.85, "unit": "%", "status": "Good"},
                    {"metric": "Factor Analysis", "value": 0.90, "unit": "%", "status": "Excellent"},
                    {"metric": "Strategic Alignment", "value": 0.87, "unit": "%", "status": "Good"}
                ]
            },
            "risk_assessment": {
                "risk_factors": [
                    {"factor": "Delivery Delays", "probability": 0.35, "impact": "High", "mitigation": "Enhanced project management"},
                    {"factor": "Training Challenges", "probability": 0.45, "impact": "Medium", "mitigation": "Comprehensive training programs"},
                    {"factor": "Regional Tensions", "probability": 0.25, "impact": "High", "mitigation": "Diplomatic engagement"},
                    {"factor": "Economic Constraints", "probability": 0.30, "impact": "Medium", "mitigation": "Budget optimization"},
                    {"factor": "Technical Issues", "probability": 0.20, "impact": "Medium", "mitigation": "Quality assurance protocols"}
                ]
            }
        }
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Verify content
    checks = [
        ("Scenario Analysis Overview", "Scenario analysis overview section"),
        ("Prediction Scenarios", "Prediction scenarios section"),
        ("Multi-Scenario Analysis", "Multi-scenario analysis section"),
        ("Risk Assessment", "Risk assessment section"),
        ("chart-container", "Chart containers"),
        ("data-tooltip", "Tooltip attributes"),
        ("scenarioOverviewChart", "Scenario overview chart"),
        ("predictionScenariosChart", "Prediction scenarios chart"),
        ("multiScenarioAnalysisChart", "Multi-scenario analysis chart"),
        ("riskAssessmentChart", "Risk assessment chart"),
        ("Chart.js", "Chart.js integration"),
        ("radar", "Radar chart"),
        ("line", "Line chart"),
        ("bar", "Bar chart"),
        ("pie", "Pie chart")
    ]
    
    issues = []
    for check_text, description in checks:
        if check_text not in content:
            issues.append(f"Missing {description}")
    
    # Check tooltip functionality
    tooltip_checks = [
        "scenario_overview",
        "prediction_scenarios",
        "multi_scenario_analysis",
        "risk_assessment"
    ]
    
    tooltip_issues = []
    for tooltip_id in tooltip_checks:
        if f'data-tooltip-{module.module_id}="{tooltip_id}"' not in content:
            tooltip_issues.append(f"Missing tooltip: {tooltip_id}")
    
    # Check chart functionality
    chart_checks = [
        "scenarioOverviewChart",
        "predictionScenariosChart",
        "multiScenarioAnalysisChart",
        "riskAssessmentChart"
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
        logger.info("✅ Scenario Analysis Module test successful")
        logger.info(f"📄 Generated content length: {len(content)} characters")
        return True
    else:
        logger.warning(f"⚠️ {total_issues} issues found in Scenario Analysis Module test")
        return False


async def test_scenario_analysis_module_defaults():
    """Test the Scenario Analysis Module with default data."""
    logger.info("=== Testing Scenario Analysis Module with Defaults ===")
    
    # Initialize module
    module = ScenarioAnalysisModule()
    
    # Test with minimal data
    test_data = {
        "scenario_analysis": {}
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Basic checks
    checks = [
        "Scenario Analysis Overview",
        "Prediction Scenarios",
        "Multi-Scenario Analysis",
        "Risk Assessment"
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
    """Run all scenario analysis module tests."""
    logger.info("🚀 Starting Scenario Analysis Module Tests")
    
    # Test 1: Full functionality test
    full_test_result = await test_scenario_analysis_module()
    
    # Test 2: Default data test
    default_test_result = await test_scenario_analysis_module_defaults()
    
    # Summary
    logger.info("📊 Test Summary:")
    logger.info(f"  Full Test: {'✅ PASS' if full_test_result else '❌ FAIL'}")
    logger.info(f"  Default Test: {'✅ PASS' if default_test_result else '❌ FAIL'}")
    
    if full_test_result and default_test_result:
        logger.info("🎉 All Scenario Analysis Module tests passed!")
        return True
    else:
        logger.warning("⚠️ Some Scenario Analysis Module tests failed")
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)
