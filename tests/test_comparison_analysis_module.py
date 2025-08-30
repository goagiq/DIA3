#!/usr/bin/env python3
"""
Comparison Analysis Module Test Script

This script tests the Comparison Analysis Module functionality,
including advanced tooltip integration and chart generation.
"""

import asyncio
from loguru import logger

from src.core.modules.comparison_analysis_module import ComparisonAnalysisModule


async def test_comparison_analysis_module():
    """Test the Comparison Analysis Module functionality."""
    logger.info("=== Testing Comparison Analysis Module ===")
    
    # Initialize module
    module = ComparisonAnalysisModule()
    
    # Test data for comparison analysis
    test_data = {
        "comparison_analysis": {
            "strategic_options": {
                "options": [
                    {
                        "name": "Option A: Full Acquisition",
                        "cost": 5000000000,
                        "timeline": 5,
                        "risk": 0.3,
                        "benefit": 0.8,
                        "feasibility": 0.7
                    },
                    {
                        "name": "Option B: Phased Implementation",
                        "cost": 3500000000,
                        "timeline": 7,
                        "risk": 0.2,
                        "benefit": 0.6,
                        "feasibility": 0.9
                    },
                    {
                        "name": "Option C: Joint Development",
                        "cost": 2500000000,
                        "timeline": 8,
                        "risk": 0.4,
                        "benefit": 0.7,
                        "feasibility": 0.6
                    },
                    {
                        "name": "Option D: Technology Transfer",
                        "cost": 1500000000,
                        "timeline": 3,
                        "risk": 0.1,
                        "benefit": 0.4,
                        "feasibility": 0.95
                    }
                ]
            },
            "options_assessment": {
                "criteria": [
                    {"criterion": "Strategic Alignment", "weight": 0.25},
                    {"criterion": "Cost Effectiveness", "weight": 0.20},
                    {"criterion": "Risk Management", "weight": 0.20},
                    {"criterion": "Implementation Feasibility", "weight": 0.15},
                    {"criterion": "Long-term Sustainability", "weight": 0.10},
                    {"criterion": "Technology Readiness", "weight": 0.10}
                ],
                "option_scores": {
                    "Option A": [0.8, 0.6, 0.7, 0.7, 0.8, 0.9],
                    "Option B": [0.7, 0.8, 0.8, 0.9, 0.7, 0.6],
                    "Option C": [0.6, 0.9, 0.6, 0.6, 0.6, 0.7],
                    "Option D": [0.5, 0.9, 0.9, 0.9, 0.5, 0.5]
                }
            },
            "comparative_analysis": {
                "metrics": [
                    {"metric": "Total Cost", "unit": "USD", "options": {"A": 5000000000, "B": 3500000000, "C": 2500000000, "D": 1500000000}},
                    {"metric": "Implementation Time", "unit": "Years", "options": {"A": 5, "B": 7, "C": 8, "D": 3}},
                    {"metric": "Risk Level", "unit": "Score", "options": {"A": 0.3, "B": 0.2, "C": 0.4, "D": 0.1}},
                    {"metric": "Strategic Value", "unit": "Score", "options": {"A": 0.8, "B": 0.6, "C": 0.7, "D": 0.4}},
                    {"metric": "Technology Maturity", "unit": "Score", "options": {"A": 0.9, "B": 0.6, "C": 0.7, "D": 0.5}}
                ]
            },
            "option_evaluation": {
                "evaluations": [
                    {
                        "option": "Option A: Full Acquisition",
                        "overall_score": 0.75,
                        "strengths": ["High strategic value", "Advanced technology", "Complete control"],
                        "weaknesses": ["High cost", "Long timeline", "High risk"],
                        "recommendation": "Consider for high-priority strategic needs"
                    },
                    {
                        "option": "Option B: Phased Implementation",
                        "overall_score": 0.82,
                        "strengths": ["Manageable cost", "Reduced risk", "Flexible timeline"],
                        "weaknesses": ["Longer total timeline", "Complex coordination"],
                        "recommendation": "Recommended for balanced approach"
                    },
                    {
                        "option": "Option C: Joint Development",
                        "overall_score": 0.68,
                        "strengths": ["Cost sharing", "International cooperation", "Technology transfer"],
                        "weaknesses": ["Complex partnerships", "Shared control", "Coordination challenges"],
                        "recommendation": "Consider for international collaboration"
                    },
                    {
                        "option": "Option D: Technology Transfer",
                        "overall_score": 0.58,
                        "strengths": ["Lowest cost", "Quick implementation", "Low risk"],
                        "weaknesses": ["Limited strategic value", "Dependency on others", "Limited control"],
                        "recommendation": "Consider for immediate needs with limited resources"
                    }
                ]
            }
        }
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Verify content
    checks = [
        ("Strategic Options Comparison", "Options comparison section"),
        ("Strategic Options Assessment", "Options assessment section"),
        ("Comparative Analysis", "Comparative analysis section"),
        ("Option Evaluation", "Option evaluation section"),
        ("chart-container", "Chart containers"),
        ("data-tooltip", "Tooltip attributes"),
        ("strategicOptionsComparisonChart", "Options comparison chart"),
        ("strategicOptionsAssessmentChart", "Options assessment chart"),
        ("comparativeAnalysisChart", "Comparative analysis chart"),
        ("optionEvaluationChart", "Option evaluation chart"),
        ("Chart.js", "Chart.js integration"),
        ("radar", "Radar chart"),
        ("bar", "Bar chart")
    ]
    
    issues = []
    for check_text, description in checks:
        if check_text not in content:
            issues.append(f"Missing {description}")
    
    # Check tooltip functionality
    tooltip_checks = [
        "strategic_options_comparison",
        "strategic_options_assessment",
        "comparative_analysis",
        "option_evaluation"
    ]
    
    tooltip_issues = []
    for tooltip_id in tooltip_checks:
        if f'data-tooltip-{module.module_id}="{tooltip_id}"' not in content:
            tooltip_issues.append(f"Missing tooltip: {tooltip_id}")
    
    # Check chart functionality
    chart_checks = [
        "strategicOptionsComparisonChart",
        "strategicOptionsAssessmentChart",
        "comparativeAnalysisChart",
        "optionEvaluationChart"
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
        logger.info("✅ Comparison Analysis Module test successful")
        logger.info(f"📄 Generated content length: {len(content)} characters")
        return True
    else:
        logger.warning(f"⚠️ {total_issues} issues found in Comparison Analysis Module test")
        return False


async def test_comparison_analysis_module_defaults():
    """Test the Comparison Analysis Module with default data."""
    logger.info("=== Testing Comparison Analysis Module with Defaults ===")
    
    # Initialize module
    module = ComparisonAnalysisModule()
    
    # Test with minimal data
    test_data = {
        "comparison_analysis": {}
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Basic checks
    checks = [
        "Strategic Options Comparison",
        "Strategic Options Assessment",
        "Comparative Analysis",
        "Option Evaluation"
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
    """Run all comparison analysis module tests."""
    logger.info("🚀 Starting Comparison Analysis Module Tests")
    
    # Test 1: Full functionality test
    full_test_result = await test_comparison_analysis_module()
    
    # Test 2: Default data test
    default_test_result = await test_comparison_analysis_module_defaults()
    
    # Summary
    logger.info("📊 Test Summary:")
    logger.info(f"  Full Test: {'✅ PASS' if full_test_result else '❌ FAIL'}")
    logger.info(f"  Default Test: {'✅ PASS' if default_test_result else '❌ FAIL'}")
    
    if full_test_result and default_test_result:
        logger.info("🎉 All Comparison Analysis Module tests passed!")
        return True
    else:
        logger.warning("⚠️ Some Comparison Analysis Module tests failed")
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)
