#!/usr/bin/env python3
"""
Predictive Analytics Module Test Script

This script tests the Predictive Analytics Module functionality,
including advanced tooltip integration and chart generation.
"""

import asyncio
from loguru import logger

from src.core.modules.predictive_analytics_module import PredictiveAnalyticsModule


async def test_predictive_analytics_module():
    """Test the Predictive Analytics Module functionality."""
    logger.info("=== Testing Predictive Analytics Module ===")
    
    # Initialize module
    module = PredictiveAnalyticsModule()
    
    # Test data for predictive analytics
    test_data = {
        "predictive_analytics": {
            "feature_importance": {
                "features": [
                    {"feature": "Submarine Delivery Timeline", "importance": 0.95, "category": "Timeline", "impact": "Critical"},
                    {"feature": "Crew Training Programs", "importance": 0.88, "category": "Personnel", "impact": "High"},
                    {"feature": "Strategic Partnership China", "importance": 0.85, "category": "Diplomatic", "impact": "High"},
                    {"feature": "Regional Military Competition", "importance": 0.82, "category": "Strategic", "impact": "High"},
                    {"feature": "Economic Sustainability", "importance": 0.78, "category": "Economic", "impact": "Medium"}
                ]
            },
            "predictive_insights": {
                "insights": [
                    {"insight": "Timeline Criticality", "confidence": 0.95, "impact": "Critical", "recommendation": "Accelerate delivery timeline"},
                    {"insight": "Training Dependency", "confidence": 0.88, "impact": "High", "recommendation": "Enhance training programs"},
                    {"insight": "Partnership Leverage", "confidence": 0.85, "impact": "High", "recommendation": "Strengthen strategic partnerships"},
                    {"insight": "Competition Response", "confidence": 0.82, "impact": "High", "recommendation": "Monitor regional dynamics"},
                    {"insight": "Economic Viability", "confidence": 0.78, "impact": "Medium", "recommendation": "Ensure economic sustainability"}
                ]
            },
            "analytics_results": {
                "results": [
                    {"metric": "Model Accuracy", "value": 0.94, "unit": "%", "trend": "Improving"},
                    {"metric": "Prediction Confidence", "value": 0.95, "unit": "%", "trend": "High"},
                    {"metric": "Feature Count", "value": 8, "unit": "", "trend": "Optimal"},
                    {"metric": "Training Data Size", "value": 20000, "unit": "samples", "trend": "Sufficient"},
                    {"metric": "Validation Score", "value": 0.92, "unit": "%", "trend": "Excellent"},
                    {"metric": "Cross-Validation", "value": 0.91, "unit": "%", "trend": "Stable"}
                ]
            },
            "predictive_modeling": {
                "scenarios": [
                    {"scenario": "Optimistic", "probability": 0.25, "capability": 0.95, "risk": "Low", "factors": "Accelerated delivery, Enhanced training"},
                    {"scenario": "Baseline", "probability": 0.50, "capability": 0.85, "risk": "Medium", "factors": "Standard delivery, Normal training"},
                    {"scenario": "Pessimistic", "probability": 0.25, "capability": 0.65, "risk": "High", "factors": "Delivery delays, Training challenges"}
                ]
            }
        }
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Verify content
    checks = [
        ("Feature Importance Analysis", "Feature importance analysis section"),
        ("Predictive Analytics Insights", "Predictive analytics insights section"),
        ("Analytics Results", "Analytics results section"),
        ("Predictive Modeling", "Predictive modeling section"),
        ("chart-container", "Chart containers"),
        ("data-tooltip", "Tooltip attributes"),
        ("featureImportanceChart", "Feature importance chart"),
        ("predictiveInsightsChart", "Predictive insights chart"),
        ("analyticsResultsChart", "Analytics results chart"),
        ("predictiveModelingChart", "Predictive modeling chart"),
        ("Chart.js", "Chart.js integration"),
        ("bar", "Bar chart"),
        ("radar", "Radar chart"),
        ("line", "Line chart"),
        ("pie", "Pie chart")
    ]
    
    issues = []
    for check_text, description in checks:
        if check_text not in content:
            issues.append(f"Missing {description}")
    
    # Check tooltip functionality
    tooltip_checks = [
        "feature_importance",
        "predictive_insights",
        "analytics_results",
        "predictive_modeling"
    ]
    
    tooltip_issues = []
    for tooltip_id in tooltip_checks:
        if f'data-tooltip-{module.module_id}="{tooltip_id}"' not in content:
            tooltip_issues.append(f"Missing tooltip: {tooltip_id}")
    
    # Check chart functionality
    chart_checks = [
        "featureImportanceChart",
        "predictiveInsightsChart",
        "analyticsResultsChart",
        "predictiveModelingChart"
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
        logger.info("✅ Predictive Analytics Module test successful")
        logger.info(f"📄 Generated content length: {len(content)} characters")
        return True
    else:
        logger.warning(f"⚠️ {total_issues} issues found in Predictive Analytics Module test")
        return False


async def test_predictive_analytics_module_defaults():
    """Test the Predictive Analytics Module with default data."""
    logger.info("=== Testing Predictive Analytics Module with Defaults ===")
    
    # Initialize module
    module = PredictiveAnalyticsModule()
    
    # Test with minimal data
    test_data = {
        "predictive_analytics": {}
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Basic checks
    checks = [
        "Feature Importance Analysis",
        "Predictive Analytics Insights",
        "Analytics Results",
        "Predictive Modeling"
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
    """Run all predictive analytics module tests."""
    logger.info("🚀 Starting Predictive Analytics Module Tests")
    
    # Test 1: Full functionality test
    full_test_result = await test_predictive_analytics_module()
    
    # Test 2: Default data test
    default_test_result = await test_predictive_analytics_module_defaults()
    
    # Summary
    logger.info("📊 Test Summary:")
    logger.info(f"  Full Test: {'✅ PASS' if full_test_result else '❌ FAIL'}")
    logger.info(f"  Default Test: {'✅ PASS' if default_test_result else '❌ FAIL'}")
    
    if full_test_result and default_test_result:
        logger.info("🎉 All Predictive Analytics Module tests passed!")
        return True
    else:
        logger.warning("⚠️ Some Predictive Analytics Module tests failed")
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)
