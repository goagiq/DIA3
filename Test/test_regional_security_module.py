#!/usr/bin/env python3
"""
Regional Security Module Test Script

This script tests the Regional Security Module functionality,
including advanced tooltip integration and chart generation.
"""

import asyncio
from pathlib import Path
from loguru import logger

from src.core.modular_report_generator import ModularReportGenerator
from src.core.modules.regional_security_module import RegionalSecurityModule


async def test_regional_security_module():
    """Test the Regional Security Module functionality."""
    logger.info("=== Testing Regional Security Module ===")
    
    # Initialize generator
    generator = ModularReportGenerator()
    
    # Test data for regional security analysis
    test_data = {
        "regional_security": {
            "security_assessment": {
                "threat_level": "High",
                "stability_index": 0.45,
                "conflict_probability": 0.35,
                "regional_tensions": "High",
                "cooperation_level": 0.4,
                "deterrence_effectiveness": 0.6
            },
            "dynamics_evolution": {
                "timeline": [
                    {"period": "Q1 2024", "stability": 0.6, "threat_level": 0.4, "cooperation": 0.5},
                    {"period": "Q2 2024", "stability": 0.55, "threat_level": 0.45, "cooperation": 0.48},
                    {"period": "Q3 2024", "stability": 0.5, "threat_level": 0.5, "cooperation": 0.45},
                    {"period": "Q4 2024", "stability": 0.45, "threat_level": 0.55, "cooperation": 0.4}
                ],
                "evolution_metrics": {
                    "trend_direction": "Declining",
                    "change_rate": "0.05",
                    "volatility": "High",
                    "predictability": "0.6"
                }
            },
            "regional_analysis": {
                "key_actors": [
                    {"name": "Pakistan", "role": "Primary Actor", "influence": "High"},
                    {"name": "India", "role": "Regional Power", "influence": "Very High"},
                    {"name": "China", "role": "Strategic Partner", "influence": "High"},
                    {"name": "United States", "role": "Global Power", "influence": "Medium"},
                    {"name": "Russia", "role": "Arms Supplier", "influence": "Medium"}
                ],
                "power_balance": {
                    "Pakistan": 0.6,
                    "India": 0.8,
                    "China": 0.9,
                    "United States": 0.7,
                    "Russia": 0.5
                },
                "conflict_zones": [
                    {
                        "name": "Kashmir",
                        "risk_level": "High",
                        "description": "Disputed territory with ongoing tensions"
                    },
                    {
                        "name": "Line of Control",
                        "risk_level": "Medium",
                        "description": "De facto border with periodic skirmishes"
                    },
                    {
                        "name": "Arabian Sea",
                        "risk_level": "Low",
                        "description": "Maritime domain with strategic importance"
                    }
                ]
            },
            "security_implications": {
                "strategic_implications": [
                    {
                        "title": "Nuclear Deterrence Enhancement",
                        "description": "Submarine acquisition strengthens nuclear deterrence capabilities",
                        "impact": "High"
                    },
                    {
                        "title": "Regional Power Balance Shift",
                        "description": "Significant shift in regional military capabilities",
                        "impact": "Very High"
                    },
                    {
                        "title": "Strategic Partnership Deepening",
                        "description": "Strengthening of Pakistan-China strategic partnership",
                        "impact": "High"
                    }
                ],
                "operational_implications": [
                    {
                        "title": "Naval Operations Enhancement",
                        "description": "Improved naval operational capabilities in Arabian Sea",
                        "impact": "High"
                    },
                    {
                        "title": "Intelligence Collection",
                        "description": "Enhanced intelligence collection and surveillance capabilities",
                        "impact": "Medium"
                    },
                    {
                        "title": "Force Projection",
                        "description": "Increased force projection capabilities in the region",
                        "impact": "High"
                    }
                ],
                "policy_recommendations": [
                    {
                        "title": "Enhanced Monitoring",
                        "description": "Implement enhanced monitoring of regional military developments",
                        "priority": "High",
                        "timeline": "Immediate"
                    },
                    {
                        "title": "Diplomatic Engagement",
                        "description": "Increase diplomatic engagement to reduce tensions",
                        "priority": "Medium",
                        "timeline": "Short-term"
                    },
                    {
                        "title": "Strategic Planning",
                        "description": "Update strategic planning to account for new capabilities",
                        "priority": "High",
                        "timeline": "Medium-term"
                    }
                ]
            }
        }
    }
    
    # Generate report with regional security module
    result = await generator.generate_modular_report(
        topic="Regional Security Analysis",
        data=test_data,
        enabled_modules=["regional_security"]
    )
    
    if result["success"]:
        logger.info(f"✅ Regional Security Module test successful")
        logger.info(f"📄 Report generated: {result['filename']}")
        logger.info(f"📊 File size: {result['file_size']} bytes")
        logger.info(f"🔧 Modules used: {result['modules_used']}")
        
        # Verify HTML content
        html_content = result.get("html_content", "")
        
        # Check for key components
        checks = [
            ("Regional Security Assessment", "Security assessment section"),
            ("Security Dynamics Evolution", "Dynamics evolution section"),
            ("Regional Analysis", "Regional analysis section"),
            ("Security Implications", "Security implications section"),
            ("data-tooltip", "Tooltip data attributes"),
            ("chart-container", "Chart containers"),
            ("Chart.js", "Chart.js integration"),
            ("radar", "Radar chart"),
            ("line", "Line chart"),
            ("bar", "Bar chart")
        ]
        
        issues = []
        for check_text, description in checks:
            if check_text not in html_content:
                issues.append(f"Missing {description}")
        
        if issues:
            logger.warning(f"⚠️ Found {len(issues)} issues:")
            for issue in issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info("✅ All components verified successfully")
        
        # Check tooltip functionality
        tooltip_checks = [
            "regional_security_assessment",
            "security_dynamics_evolution", 
            "regional_analysis",
            "security_implications"
        ]
        
        tooltip_issues = []
        for tooltip_id in tooltip_checks:
            if f'data-tooltip="{tooltip_id}"' not in html_content:
                tooltip_issues.append(f"Missing tooltip: {tooltip_id}")
        
        if tooltip_issues:
            logger.warning(f"⚠️ Found {len(tooltip_issues)} tooltip issues:")
            for issue in tooltip_issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info("✅ All tooltips verified successfully")
        
        # Check chart functionality
        chart_checks = [
            "regionalSecurityAssessmentChart",
            "securityDynamicsEvolutionChart",
            "regionalPowerBalanceChart"
        ]
        
        chart_issues = []
        for chart_id in chart_checks:
            if f'id="{chart_id}"' not in html_content:
                chart_issues.append(f"Missing chart: {chart_id}")
        
        if chart_issues:
            logger.warning(f"⚠️ Found {len(chart_issues)} chart issues:")
            for issue in chart_issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info("✅ All charts verified successfully")
        
        return {
            "success": True,
            "issues": len(issues) + len(tooltip_issues) + len(chart_issues),
            "file_path": result["file_path"]
        }
    
    else:
        logger.error(f"❌ Regional Security Module test failed")
        return {"success": False, "issues": 1}


async def test_regional_security_module_standalone():
    """Test the Regional Security Module in standalone mode."""
    logger.info("=== Testing Regional Security Module Standalone ===")
    
    # Initialize module
    module = RegionalSecurityModule()
    
    # Test data
    test_data = {
        "regional_security": {
            "security_assessment": {
                "threat_level": "Moderate",
                "stability_index": 0.7,
                "conflict_probability": 0.2,
                "regional_tensions": "Medium"
            }
        }
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Verify content
    checks = [
        ("Regional Security Assessment", "Security assessment"),
        ("Security Dynamics Evolution", "Dynamics evolution"),
        ("Regional Analysis", "Regional analysis"),
        ("Security Implications", "Security implications"),
        ("chart-container", "Chart containers"),
        ("data-tooltip", "Tooltip attributes")
    ]
    
    issues = []
    for check_text, description in checks:
        if check_text not in content:
            issues.append(f"Missing {description}")
    
    if issues:
        logger.warning(f"⚠️ Found {len(issues)} issues in standalone test:")
        for issue in issues:
            logger.warning(f"  - {issue}")
    else:
        logger.info("✅ Standalone test successful")
    
    return {"success": len(issues) == 0, "issues": len(issues)}


async def main():
    """Run all regional security module tests."""
    logger.info("🚀 Starting Regional Security Module Tests")
    
    # Test 1: Full integration test
    integration_result = await test_regional_security_module()
    
    # Test 2: Standalone module test
    standalone_result = await test_regional_security_module_standalone()
    
    # Summary
    total_issues = integration_result["issues"] + standalone_result["issues"]
    
    logger.info("📊 Test Summary:")
    logger.info(f"  Integration Test: {'✅ PASS' if integration_result['success'] else '❌ FAIL'}")
    logger.info(f"  Standalone Test: {'✅ PASS' if standalone_result['success'] else '❌ FAIL'}")
    logger.info(f"  Total Issues: {total_issues}")
    
    if total_issues == 0:
        logger.info("🎉 All Regional Security Module tests passed!")
    else:
        logger.warning(f"⚠️ {total_issues} issues found in Regional Security Module tests")
    
    return total_issues == 0


if __name__ == "__main__":
    asyncio.run(main())
