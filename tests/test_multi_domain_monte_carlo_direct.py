#!/usr/bin/env python3
"""
Direct Test of Multi-Domain Monte Carlo Engine
Test the engine directly without API calls.
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


async def test_multi_domain_monte_carlo_engine():
    """Test the multi-domain Monte Carlo engine directly."""
    try:
        from src.core.multi_domain_monte_carlo_engine import (
            MultiDomainMonteCarloEngine,
            SimulationConfig,
            DomainType,
            SimulationType
        )
        
        logger.info("✅ Successfully imported multi-domain Monte Carlo engine")
        
        # Initialize engine
        engine = MultiDomainMonteCarloEngine()
        logger.info("✅ Engine initialized successfully")
        
        # Test getting available scenarios
        scenarios = engine.get_available_scenarios()
        logger.info(f"✅ Available scenarios: {scenarios}")
        
        # Test defense simulation
        config = SimulationConfig(
            domain=DomainType.DEFENSE,
            simulation_type=SimulationType.CAPABILITY_ASSESSMENT,
            num_iterations=1000,  # Reduced for testing
            confidence_level=0.95
        )
        
        logger.info("🧪 Running defense simulation...")
        result = await engine.run_simulation(config, "military_capability")
        logger.info(f"✅ Defense simulation completed: {result.simulation_id}")
        logger.info(f"   Execution time: {result.execution_time:.2f} seconds")
        logger.info(f"   Statistics: {len(result.statistics)} variables")
        logger.info(f"   Risk metrics: {len(result.risk_metrics)} metrics")
        
        # Test business simulation
        config = SimulationConfig(
            domain=DomainType.BUSINESS,
            simulation_type=SimulationType.RISK_ANALYSIS,
            num_iterations=1000,  # Reduced for testing
            confidence_level=0.95
        )
        
        logger.info("🧪 Running business simulation...")
        result = await engine.run_simulation(config, "market_analysis")
        logger.info(f"✅ Business simulation completed: {result.simulation_id}")
        logger.info(f"   Execution time: {result.execution_time:.2f} seconds")
        logger.info(f"   Statistics: {len(result.statistics)} variables")
        logger.info(f"   Risk metrics: {len(result.risk_metrics)} metrics")
        
        # Test financial simulation
        config = SimulationConfig(
            domain=DomainType.FINANCIAL,
            simulation_type=SimulationType.RISK_ANALYSIS,
            num_iterations=1000,  # Reduced for testing
            confidence_level=0.95
        )
        
        logger.info("🧪 Running financial simulation...")
        result = await engine.run_simulation(config, "portfolio_risk")
        logger.info(f"✅ Financial simulation completed: {result.simulation_id}")
        logger.info(f"   Execution time: {result.execution_time:.2f} seconds")
        logger.info(f"   Statistics: {len(result.statistics)} variables")
        logger.info(f"   Risk metrics: {len(result.risk_metrics)} metrics")
        
        # Test cybersecurity simulation
        config = SimulationConfig(
            domain=DomainType.CYBERSECURITY,
            simulation_type=SimulationType.THREAT_ASSESSMENT,
            num_iterations=1000,  # Reduced for testing
            confidence_level=0.95
        )
        
        logger.info("🧪 Running cybersecurity simulation...")
        result = await engine.run_simulation(config, "threat_assessment")
        logger.info(f"✅ Cybersecurity simulation completed: {result.simulation_id}")
        logger.info(f"   Execution time: {result.execution_time:.2f} seconds")
        logger.info(f"   Statistics: {len(result.statistics)} variables")
        logger.info(f"   Risk metrics: {len(result.risk_metrics)} metrics")
        
        # Test performance summary
        performance = engine.get_performance_summary()
        logger.info(f"✅ Performance summary: {performance}")
        
        # Test custom simulation
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
        
        config = SimulationConfig(
            domain=DomainType.DEFENSE,
            simulation_type=SimulationType.CAPABILITY_ASSESSMENT,
            num_iterations=500,  # Reduced for testing
            confidence_level=0.95
        )
        
        logger.info("🧪 Running custom simulation...")
        result = await engine.run_simulation(config, "military_capability", custom_variables)
        logger.info(f"✅ Custom simulation completed: {result.simulation_id}")
        logger.info(f"   Execution time: {result.execution_time:.2f} seconds")
        logger.info(f"   Statistics: {len(result.statistics)} variables")
        
        # Test loading cached result
        cached_result = await engine.load_cached_result(result.simulation_id)
        if cached_result:
            logger.info(f"✅ Successfully loaded cached result: {cached_result.simulation_id}")
        else:
            logger.error("❌ Failed to load cached result")
        
        logger.info("🎉 All tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    logger.info("🚀 Starting Direct Multi-Domain Monte Carlo Engine Test")
    logger.info("=" * 80)
    
    start_time = time.time()
    
    success = await test_multi_domain_monte_carlo_engine()
    
    execution_time = time.time() - start_time
    logger.info(f"⏱️ Total execution time: {execution_time:.2f} seconds")
    
    if success:
        logger.info("🎉 Direct Test PASSED!")
        return 0
    else:
        logger.error("❌ Direct Test FAILED!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
