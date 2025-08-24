#!/usr/bin/env python3
"""
Strategic Recommendations Module Test Script

This script tests the Strategic Recommendations Module functionality,
including advanced tooltip integration and chart generation.
"""

import asyncio
from loguru import logger

from src.core.modules.strategic_recommendations_module import StrategicRecommendationsModule


async def test_strategic_recommendations_module():
    """Test the Strategic Recommendations Module functionality."""
    logger.info("=== Testing Strategic Recommendations Module ===")
    
    # Initialize module
    module = StrategicRecommendationsModule()
    
    # Test data for strategic recommendations
    test_data = {
        "strategic_recommendations": {
            "intelligence_summary": {
                "total_insights": 18,
                "average_confidence": 87.5,
                "high_impact_insights": 9,
                "critical_findings": 4
            },
            "recommendations": {
                "immediate": [
                    {
                        "title": "Enhanced Intelligence Gathering",
                        "confidence": 0.95,
                        "impact": "High",
                        "timeline": "1-3 months",
                        "rationale": "Critical for immediate threat assessment"
                    },
                    {
                        "title": "Strategic Communication Protocol",
                        "confidence": 0.88,
                        "impact": "Medium",
                        "timeline": "2-4 months",
                        "rationale": "Essential for coordinated response"
                    }
                ],
                "short_term": [
                    {
                        "title": "Capability Enhancement Program",
                        "confidence": 0.82,
                        "impact": "High",
                        "timeline": "6-12 months",
                        "rationale": "Address identified capability gaps"
                    },
                    {
                        "title": "Partnership Development",
                        "confidence": 0.78,
                        "impact": "Medium",
                        "timeline": "8-15 months",
                        "rationale": "Strengthen regional alliances"
                    }
                ],
                "long_term": [
                    {
                        "title": "Strategic Infrastructure Investment",
                        "confidence": 0.75,
                        "impact": "High",
                        "timeline": "2-3 years",
                        "rationale": "Long-term strategic positioning"
                    },
                    {
                        "title": "Technology Modernization",
                        "confidence": 0.70,
                        "impact": "Medium",
                        "timeline": "3-5 years",
                        "rationale": "Future-proof capabilities"
                    }
                ]
            },
            "implementation_roadmap": {
                "phases": [
                    {
                        "phase": "Phase 1: Foundation",
                        "duration": "3-6 months",
                        "milestones": ["Setup infrastructure", "Establish protocols"],
                        "confidence": 0.90
                    },
                    {
                        "phase": "Phase 2: Development",
                        "duration": "6-12 months",
                        "milestones": ["Implement core systems", "Train personnel"],
                        "confidence": 0.85
                    },
                    {
                        "phase": "Phase 3: Integration",
                        "duration": "12-18 months",
                        "milestones": ["System integration", "Performance optimization"],
                        "confidence": 0.80
                    },
                    {
                        "phase": "Phase 4: Optimization",
                        "duration": "18-24 months",
                        "milestones": ["Advanced features", "Continuous improvement"],
                        "confidence": 0.75
                    }
                ]
            },
            "monitoring_plan": {
                "kpis": [
                    {
                        "metric": "Implementation Progress",
                        "target": "90%",
                        "current": "75%",
                        "status": "On Track"
                    },
                    {
                        "metric": "Resource Utilization",
                        "target": "85%",
                        "current": "82%",
                        "status": "Good"
                    },
                    {
                        "metric": "Timeline Adherence",
                        "target": "95%",
                        "current": "88%",
                        "status": "Needs Attention"
                    },
                    {
                        "metric": "Quality Standards",
                        "target": "95%",
                        "current": "92%",
                        "status": "Good"
                    }
                ],
                "evaluation_criteria": [
                    "Strategic alignment assessment",
                    "Performance metrics validation",
                    "Risk mitigation effectiveness",
                    "Stakeholder satisfaction levels"
                ]
            }
        }
    }
    
    # Generate content
    content = module.generate_content(test_data)
    
    # Verify content
    checks = [
        ("Intelligence Analysis Summary", "Intelligence analysis summary section"),
        ("Strategic Recommendations", "Strategic recommendations section"),
        ("Implementation Roadmap", "Implementation roadmap section"),
        ("Monitoring & Evaluation Plan", "Monitoring and evaluation plan section"),
        ("chart-container", "Chart containers"),
        ("data-tooltip", "Tooltip attributes"),
        ("intelligenceSummaryChart", "Intelligence summary chart"),
        ("strategicRecommendationsChart", "Strategic recommendations chart"),
        ("implementationRoadmapChart", "Implementation roadmap chart"),
        ("monitoringPlanChart", "Monitoring plan chart"),
        ("Chart.js", "Chart.js integration"),
        ("radar", "Radar chart"),
        ("bar", "Bar chart"),
        ("line", "Line chart"),
        ("pie", "Pie chart")
    ]
    
    issues = []
    for check_text, description in checks:
        if check_text not in content:
            issues.append(f"Missing {description}")
    
    # Check tooltip functionality
    tooltip_checks = [
        "intelligence_summary",
        "strategic_recommendations",
        "implementation_roadmap",
        "monitoring_plan"
    ]
    
    tooltip_issues = []
    for tooltip_id in tooltip_checks:
        if f'data-tooltip-{module.module_id}="{tooltip_id}"' not in content:
            tooltip_issues.append(f"Missing tooltip: {tooltip_id}")
    
    # Check chart functionality
    chart_checks = [
        "intelligenceSummaryChart",
        "strategicRecommendationsChart",
        "implementationRoadmapChart",
        "monitoringPlanChart"
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
        logger.info("✅ Strategic Recommendations Module test successful")
        logger.info(f"📄 Generated content length: {len(content)} characters")
        return True
    else:
        logger.warning(f"⚠️ {total_issues} issues found in Strategic Recommendations Module test")
        return False


async def test_strategic_recommendations_module_defaults():
    """Test the Strategic Recommendations Module with default data."""
    logger.info("=== Testing Strategic Recommendations Module with Defaults ===")
    
    # Initialize module
    module = StrategicRecommendationsModule()
    
    # Test with minimal data
    test_data = {
        "strategic_recommendations": {}
    }
    
    # Generate content
    content = module.generate_content(test_data)
    
    # Basic checks
    checks = [
        "Intelligence Analysis Summary",
        "Strategic Recommendations",
        "Implementation Roadmap",
        "Monitoring & Evaluation Plan"
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


async def test_strategic_recommendations_module_integration():
    """Test the Strategic Recommendations Module integration with ModularReportGenerator."""
    logger.info("=== Testing Strategic Recommendations Module Integration ===")
    
    try:
        from src.core.modular_report_generator import ModularReportGenerator
        
        # Initialize generator
        generator = ModularReportGenerator()
        
        # Test data
        test_data = {
            "strategic_recommendations": {
                "intelligence_summary": {
                    "total_insights": 15,
                    "average_confidence": 85.5,
                    "high_impact_insights": 8,
                    "critical_findings": 3
                }
            }
        }
        
        # Generate report with only strategic recommendations module
        result = await generator.generate_modular_report(
            topic="Strategic Recommendations Test",
            data=test_data,
            enabled_modules=["strategicrecommendationsmodule"]
        )
        
        if result["success"]:
            logger.info("✅ Integration test successful")
            logger.info(f"📄 Generated file: {result['filename']}")
            logger.info(f"📊 File size: {result['file_size']} bytes")
            return True
        else:
            logger.error(f"❌ Integration test failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Integration test error: {e}")
        return False


async def main():
    """Run all strategic recommendations module tests."""
    logger.info("🚀 Starting Strategic Recommendations Module Tests")
    
    # Test 1: Full functionality test
    full_test_result = await test_strategic_recommendations_module()
    
    # Test 2: Default data test
    default_test_result = await test_strategic_recommendations_module_defaults()
    
    # Test 3: Integration test
    integration_test_result = await test_strategic_recommendations_module_integration()
    
    # Summary
    logger.info("📊 Test Summary:")
    logger.info(f"  Full Test: {'✅ PASS' if full_test_result else '❌ FAIL'}")
    logger.info(f"  Default Test: {'✅ PASS' if default_test_result else '❌ FAIL'}")
    logger.info(f"  Integration Test: {'✅ PASS' if integration_test_result else '❌ FAIL'}")
    
    if full_test_result and default_test_result and integration_test_result:
        logger.info("🎉 All Strategic Recommendations Module tests passed!")
        return True
    else:
        logger.warning("⚠️ Some Strategic Recommendations Module tests failed")
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)
