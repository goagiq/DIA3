#!/usr/bin/env python3
"""
Multi-Domain Monte Carlo MCP Integration Test
Test the MCP integration for multi-domain Monte Carlo tools.
"""

import asyncio
import json
import logging
import time
from datetime import datetime
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_mcp_integration():
    """Test the MCP integration for multi-domain Monte Carlo tools."""
    try:
        from src.mcp_servers.multi_domain_monte_carlo_mcp_tools import MultiDomainMonteCarloMCPTools
        
        logger.info("✅ Successfully imported Multi-Domain Monte Carlo MCP tools")
        
        # Initialize MCP tools
        mcp_tools = MultiDomainMonteCarloMCPTools()
        logger.info("✅ MCP tools initialized successfully")
        
        # Test getting available scenarios
        logger.info("🧪 Testing get_available_scenarios...")
        scenarios_result = await mcp_tools.get_available_scenarios()
        logger.info(f"✅ Available scenarios: {scenarios_result}")
        
        # Test defense simulation
        logger.info("🧪 Testing defense simulation...")
        defense_result = await mcp_tools.run_defense_simulation(
            scenario_name="military_capability",
            num_iterations=1000,  # Reduced for testing
            confidence_level=0.95
        )
        logger.info(f"✅ Defense simulation result: {defense_result['status']}")
        if defense_result['status'] == 'completed':
            logger.info(f"   Simulation ID: {defense_result['simulation_id']}")
            logger.info(f"   Execution time: {defense_result['execution_time']:.2f} seconds")
        
        # Test business simulation
        logger.info("🧪 Testing business simulation...")
        business_result = await mcp_tools.run_business_simulation(
            scenario_name="market_analysis",
            num_iterations=1000,  # Reduced for testing
            confidence_level=0.95
        )
        logger.info(f"✅ Business simulation result: {business_result['status']}")
        if business_result['status'] == 'completed':
            logger.info(f"   Simulation ID: {business_result['simulation_id']}")
            logger.info(f"   Execution time: {business_result['execution_time']:.2f} seconds")
        
        # Test financial simulation
        logger.info("🧪 Testing financial simulation...")
        financial_result = await mcp_tools.run_financial_simulation(
            scenario_name="portfolio_risk",
            num_iterations=1000,  # Reduced for testing
            confidence_level=0.95
        )
        logger.info(f"✅ Financial simulation result: {financial_result['status']}")
        if financial_result['status'] == 'completed':
            logger.info(f"   Simulation ID: {financial_result['simulation_id']}")
            logger.info(f"   Execution time: {financial_result['execution_time']:.2f} seconds")
        
        # Test cybersecurity simulation
        logger.info("🧪 Testing cybersecurity simulation...")
        cybersecurity_result = await mcp_tools.run_cybersecurity_simulation(
            scenario_name="threat_assessment",
            num_iterations=1000,  # Reduced for testing
            confidence_level=0.95
        )
        logger.info(f"✅ Cybersecurity simulation result: {cybersecurity_result['status']}")
        if cybersecurity_result['status'] == 'completed':
            logger.info(f"   Simulation ID: {cybersecurity_result['simulation_id']}")
            logger.info(f"   Execution time: {cybersecurity_result['execution_time']:.2f} seconds")
        
        # Test custom simulation
        logger.info("🧪 Testing custom simulation...")
        custom_variables = {
            "custom_variable_1": {
                "distribution": "normal",
                "parameters": {"mean": 100, "std": 10},
                "description": "Custom variable 1"
            },
            "custom_variable_2": {
                "distribution": "lognormal",
                "parameters": {"mean": 2.0, "std": 0.5},
                "description": "Custom variable 2"
            }
        }
        
        custom_result = await mcp_tools.run_custom_simulation(
            domain="defense",
            scenario_name="military_capability",
            simulation_type="capability_assessment",
            variables=custom_variables,
            correlations=[[1.0, 0.3], [0.3, 1.0]],
            num_iterations=500,  # Reduced for testing
            confidence_level=0.95
        )
        logger.info(f"✅ Custom simulation result: {custom_result['status']}")
        if custom_result['status'] == 'completed':
            logger.info(f"   Simulation ID: {custom_result['simulation_id']}")
            logger.info(f"   Execution time: {custom_result['execution_time']:.2f} seconds")
        
        # Test performance summary
        logger.info("🧪 Testing performance summary...")
        performance_result = await mcp_tools.get_performance_summary()
        logger.info(f"✅ Performance summary result: {performance_result['status']}")
        
        # Test report generation if we have a simulation ID
        simulation_id = None
        for result in [defense_result, business_result, financial_result, cybersecurity_result, custom_result]:
            if result.get('status') == 'completed' and 'simulation_id' in result:
                simulation_id = result['simulation_id']
                break
        
        if simulation_id:
            logger.info(f"🧪 Testing report generation for simulation {simulation_id}...")
            report_result = await mcp_tools.generate_simulation_report(simulation_id, "json")
            logger.info(f"✅ Report generation result: {report_result['status']}")
        
        logger.info("🎉 All MCP integration tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ MCP integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    logger.info("🚀 Starting Multi-Domain Monte Carlo MCP Integration Test")
    logger.info("=" * 80)
    
    start_time = time.time()
    
    success = await test_mcp_integration()
    
    execution_time = time.time() - start_time
    logger.info(f"⏱️ Total execution time: {execution_time:.2f} seconds")
    
    if success:
        logger.info("🎉 MCP Integration Test PASSED!")
        return 0
    else:
        logger.error("❌ MCP Integration Test FAILED!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
