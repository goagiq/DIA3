#!/usr/bin/env python3
"""
Test script to isolate the Regional Security Module issue.
"""

import asyncio
from loguru import logger

from src.core.modular_report_generator import ModularReportGenerator


async def test_regional_security():
    """Test just the regional security module."""
    logger.info("🔍 Testing Regional Security Module in isolation")
    
    # Initialize the modular report generator
    generator = ModularReportGenerator()
    
    # Test data with just regional security
    test_data = {
        "regional_security": {
            "security_assessment": {
                "threat_level": "Moderate to High",
                "stability_index": 0.65,
                "conflict_probability": 0.25,
                "regional_tensions": "Medium",
                "cooperation_level": 0.6,
                "deterrence_effectiveness": 0.7
            },
            "security_dynamics": {
                "threat_assessment": "Moderate to high regional threat level",
                "deterrence_effectiveness": "Significantly enhanced",
                "alliance_stability": "Mixed impact on existing alliances"
            },
            "dynamics_evolution": {
                "timeline": [
                    {"period": "2015-2017", "stability": 0.6, "threat_level": 0.4, "cooperation": 0.5},
                    {"period": "2018-2020", "stability": 0.55, "threat_level": 0.5, "cooperation": 0.45},
                    {"period": "2021-2023", "stability": 0.5, "threat_level": 0.6, "cooperation": 0.4},
                    {"period": "2024-2025", "stability": 0.65, "threat_level": 0.7, "cooperation": 0.6}
                ],
                "evolution_metrics": {
                    "trend_direction": "Improving",
                    "change_rate": "0.05",
                    "volatility": "Medium",
                    "predictability": "0.7"
                }
            },
            "regional_analysis": {
                "key_actors": [
                    {"name": "Pakistan", "role": "Acquiring Nation", "influence": "High"},
                    {"name": "India", "role": "Regional Competitor", "influence": "High"},
                    {"name": "China", "role": "Technology Provider", "influence": "High"},
                    {"name": "United States", "role": "Global Power", "influence": "Medium"}
                ],
                "power_balance": {
                    "Pakistan": 0.7,
                    "India": 0.8,
                    "China": 0.9,
                    "United States": 0.85
                },
                "conflict_zones": [
                    {"name": "Kashmir", "risk_level": "High", "description": "Long-standing territorial dispute"},
                    {"name": "Arabian Sea", "risk_level": "Medium", "description": "Maritime security competition"},
                    {"name": "Indo-Pacific", "risk_level": "Medium", "description": "Strategic competition zone"}
                ]
            },
            "security_implications": {
                "strategic_implications": [
                    {
                        "title": "Enhanced Pakistan Navy Deterrence",
                        "description": "Significant enhancement of Pakistan Navy's deterrence capabilities through submarine acquisition",
                        "impact": "High"
                    },
                    {
                        "title": "Regional Arms Competition",
                        "description": "Potential escalation of regional arms competition and military modernization",
                        "impact": "Medium"
                    },
                    {
                        "title": "Strategic Stability Impact",
                        "description": "Impact on India-Pakistan strategic stability and nuclear deterrence dynamics",
                        "impact": "High"
                    }
                ],
                "operational_implications": [
                    {
                        "title": "Maritime Domain Control",
                        "description": "Enhanced maritime domain awareness and control capabilities",
                        "impact": "High"
                    },
                    {
                        "title": "Alliance Dynamics",
                        "description": "Strengthening of China-Pakistan strategic partnership",
                        "impact": "Medium"
                    }
                ],
                "policy_recommendations": [
                    {
                        "title": "Confidence Building Measures",
                        "description": "Implement regional confidence-building measures to prevent escalation",
                        "priority": "High",
                        "timeline": "Short-term"
                    },
                    {
                        "title": "Maritime Security Cooperation",
                        "description": "Enhance maritime security cooperation with regional partners",
                        "priority": "Medium",
                        "timeline": "Medium-term"
                    }
                ]
            },
            "mitigation_measures": [
                "Confidence-building measures",
                "Maritime security cooperation",
                "Technology proliferation controls",
                "Regional dialogue mechanisms"
            ]
        }
    }
    
    # Test the module directly
    try:
        module = generator.get_module("regionalsecuritymodule")
        logger.info(f"✅ Module loaded: {module.module_id}")
        
        # Check required data keys
        required_keys = module.get_required_data_keys()
        logger.info(f"📋 Required keys: {required_keys}")
        
        # Check if data has required keys
        for key in required_keys:
            if key in test_data:
                logger.info(f"✅ Found key: {key}")
                logger.info(f"   Type: {type(test_data[key])}")
                logger.info(f"   Value: {test_data[key]}")
            else:
                logger.error(f"❌ Missing key: {key}")
        
        # Try to generate content
        content = module.generate_content(test_data)
        logger.info("✅ Content generated successfully!")
        logger.info(f"📄 Content length: {len(content)} characters")
        
    except Exception as e:
        logger.error(f"❌ Error testing regional security module: {e}")
        import traceback
        logger.error(traceback.format_exc())


async def main():
    """Main function."""
    await test_regional_security()


if __name__ == "__main__":
    asyncio.run(main())
