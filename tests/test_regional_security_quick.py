#!/usr/bin/env python3
"""
Quick Regional Security Module Test

Simple test to verify the Regional Security Module is working.
"""

import asyncio
from loguru import logger

from src.core.modules.regional_security_module import RegionalSecurityModule


async def quick_test():
    """Quick test of the Regional Security Module."""
    logger.info("=== Quick Regional Security Module Test ===")
    
    # Initialize module
    module = RegionalSecurityModule()
    
    # Simple test data
    test_data = {
        "regional_security": {
            "security_assessment": {
                "threat_level": "High",
                "stability_index": 0.45,
                "conflict_probability": 0.35,
                "regional_tensions": "High"
            }
        }
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Basic checks
    checks = [
        "Regional Security Assessment",
        "Security Dynamics Evolution", 
        "Regional Analysis",
        "Security Implications",
        "chart-container"
    ]
    
    success = True
    for check in checks:
        if check not in content:
            logger.error(f"Missing: {check}")
            success = False
    
    if success:
        logger.info("✅ Regional Security Module working correctly")
        logger.info(f"📄 Generated content length: {len(content)} characters")
        return True
    else:
        logger.error("❌ Regional Security Module test failed")
        return False


if __name__ == "__main__":
    result = asyncio.run(quick_test())
    exit(0 if result else 1)
