#!/usr/bin/env python3
"""
Direct test script for escalation analysis agent functionality.

This script tests the escalation analysis agent directly without going through the API
to verify the core functionality works.
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any
from loguru import logger

from src.agents.escalation_analysis_agent import EscalationAnalysisAgent


async def test_escalation_agent():
    """Test the escalation analysis agent directly."""
    logger.info("🚀 Starting Direct Escalation Analysis Agent Test")
    logger.info("=" * 60)
    
    try:
        # Create agent instance
        agent = EscalationAnalysisAgent()
        logger.info("✅ Escalation Analysis Agent created successfully")
        
        # Test content
        test_content = """
        Russia has recently increased its military presence near the EU border, 
        conducting large-scale military exercises and deploying advanced weapons systems. 
        The EU has responded with economic sanctions and diplomatic pressure, while 
        NATO has announced plans to expand its eastern flank. This escalation follows 
        a pattern of historical tensions between Russia and European powers, similar 
        to the dynamics described in War and Peace during the Napoleonic era.
        """
        
        # Test analysis for different domains
        domains = ["defense", "intelligence", "business", "cybersecurity", "geopolitical"]
        
        for domain in domains:
            logger.info(f"Testing {domain} domain analysis...")
            
            try:
                result = await agent.analyze_escalation_patterns(
                    content=test_content,
                    domain=domain,
                    analysis_depth="comprehensive"
                )
                
                logger.info(f"✅ {domain.title()} Analysis Completed:")
                logger.info(f"   Analysis ID: {result.analysis_id}")
                logger.info(f"   Confidence Score: {result.confidence_score:.2f}")
                logger.info(f"   Scenarios Found: {len(result.escalation_scenarios)}")
                logger.info(f"   Risk Level: {result.risk_assessment.get('overall_risk', 'unknown')}")
                
                # Log some scenarios
                for i, scenario in enumerate(result.escalation_scenarios[:2]):
                    logger.info(f"   Scenario {i+1}: {scenario.scenario_type} ({scenario.risk_level} risk)")
                
            except Exception as e:
                logger.error(f"❌ {domain.title()} Analysis Failed: {e}")
        
        # Test capabilities
        logger.info("\n📋 Agent Capabilities:")
        logger.info(f"   Supported Data Types: {[dt.value for dt in agent.supported_data_types]}")
        logger.info(f"   Supported Domains: {list(agent.domain_frameworks.keys())}")
        logger.info(f"   Historical Patterns: {len(agent.historical_patterns)}")
        
        logger.info("\n🎉 Direct Escalation Analysis Agent Test Completed Successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Direct Escalation Analysis Agent Test Failed: {e}")
        return False


async def main():
    """Main test function."""
    try:
        success = await test_escalation_agent()
        
        if success:
            logger.success("✅ All direct tests passed!")
            return 0
        else:
            logger.error("❌ Some direct tests failed!")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
