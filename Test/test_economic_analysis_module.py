#!/usr/bin/env python3
"""
Economic Analysis Module Test Script

This script tests the Economic Analysis Module functionality,
including advanced tooltip integration and chart generation.
"""

import asyncio
from loguru import logger

from src.core.modules.economic_analysis_module import EconomicAnalysisModule


async def test_economic_analysis_module():
    """Test the Economic Analysis Module functionality."""
    logger.info("=== Testing Economic Analysis Module ===")
    
    # Initialize module
    module = EconomicAnalysisModule()
    
    # Test data for economic analysis
    test_data = {
        "economic_analysis": {
            "cost_breakdown": {
                "acquisition_cost": 3000000000,
                "operational_cost": 600000000,
                "maintenance_cost": 800000000,
                "training_cost": 150000000,
                "infrastructure_cost": 350000000
            },
            "financial_implications": {
                "budget_impact": 0.18,
                "gdp_impact": 0.009,
                "debt_ratio": 0.14,
                "economic_multiplier": 1.6,
                "timeline": [
                    {"year": "Year 1", "cost": 900000000, "impact": 0.06},
                    {"year": "Year 2", "cost": 1400000000, "impact": 0.09},
                    {"year": "Year 3", "cost": 1100000000, "impact": 0.07},
                    {"year": "Year 4", "cost": 700000000, "impact": 0.05},
                    {"year": "Year 5", "cost": 800000000, "impact": 0.055}
                ]
            },
            "economic_planning": {
                "funding_sources": [
                    {"source": "Defense Budget", "amount": 2400000000, "percentage": 55},
                    {"source": "Special Allocation", "amount": 1200000000, "percentage": 27},
                    {"source": "International Financing", "amount": 500000000, "percentage": 11},
                    {"source": "Private Investment", "amount": 300000000, "percentage": 7}
                ],
                "cost_mitigation": [
                    {"strategy": "Phased Implementation", "savings": 250000000},
                    {"strategy": "Local Manufacturing", "savings": 400000000},
                    {"strategy": "Technology Transfer", "savings": 200000000},
                    {"strategy": "Bulk Procurement", "savings": 150000000}
                ],
                "economic_benefits": [
                    {"benefit": "Job Creation", "value": 18000, "unit": "jobs"},
                    {"benefit": "Technology Transfer", "value": 30, "unit": "technologies"},
                    {"benefit": "Industrial Capacity", "value": 35, "unit": "% increase"},
                    {"benefit": "Export Potential", "value": 750, "unit": "million USD"}
                ]
            },
            "budget_analysis": {
                "annual_defense_budget": 18000000000,
                "program_annual_cost": 1000000000,
                "budget_utilization": 0.88,
                "cost_efficiency": 0.94
            }
        }
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Verify content
    checks = [
        ("Economic Cost Breakdown", "Cost breakdown section"),
        ("Financial Implications", "Financial implications section"),
        ("Economic Planning", "Economic planning section"),
        ("Budget Analysis", "Budget analysis section"),
        ("chart-container", "Chart containers"),
        ("data-tooltip", "Tooltip attributes"),
        ("economicCostBreakdownChart", "Cost breakdown chart"),
        ("financialImplicationsChart", "Financial implications chart"),
        ("budgetAnalysisChart", "Budget analysis chart"),
        ("Chart.js", "Chart.js integration"),
        ("pie", "Pie chart"),
        ("line", "Line chart"),
        ("bar", "Bar chart")
    ]
    
    issues = []
    for check_text, description in checks:
        if check_text not in content:
            issues.append(f"Missing {description}")
    
    # Check tooltip functionality
    tooltip_checks = [
        "economic_cost_breakdown",
        "financial_implications",
        "economic_planning",
        "budget_analysis",
        "economic_benefit"
    ]
    
    tooltip_issues = []
    for tooltip_id in tooltip_checks:
        if f'data-tooltip-{module.module_id}="{tooltip_id}"' not in content:
            tooltip_issues.append(f"Missing tooltip: {tooltip_id}")
    
    # Check chart functionality
    chart_checks = [
        "economicCostBreakdownChart",
        "financialImplicationsChart", 
        "budgetAnalysisChart"
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
        logger.info("✅ Economic Analysis Module test successful")
        logger.info(f"📄 Generated content length: {len(content)} characters")
        return True
    else:
        logger.warning(f"⚠️ {total_issues} issues found in Economic Analysis Module test")
        return False


async def test_economic_analysis_module_defaults():
    """Test the Economic Analysis Module with default data."""
    logger.info("=== Testing Economic Analysis Module with Defaults ===")
    
    # Initialize module
    module = EconomicAnalysisModule()
    
    # Test with minimal data
    test_data = {
        "economic_analysis": {}
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Basic checks
    checks = [
        "Economic Cost Breakdown",
        "Financial Implications",
        "Economic Planning", 
        "Budget Analysis"
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
    """Run all economic analysis module tests."""
    logger.info("🚀 Starting Economic Analysis Module Tests")
    
    # Test 1: Full functionality test
    full_test_result = await test_economic_analysis_module()
    
    # Test 2: Default data test
    default_test_result = await test_economic_analysis_module_defaults()
    
    # Summary
    logger.info("📊 Test Summary:")
    logger.info(f"  Full Test: {'✅ PASS' if full_test_result else '❌ FAIL'}")
    logger.info(f"  Default Test: {'✅ PASS' if default_test_result else '❌ FAIL'}")
    
    if full_test_result and default_test_result:
        logger.info("🎉 All Economic Analysis Module tests passed!")
        return True
    else:
        logger.warning("⚠️ Some Economic Analysis Module tests failed")
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)
