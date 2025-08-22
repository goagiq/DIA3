"""
Test script for Data.gov Phase 1 Implementation
Tests the core infrastructure components of Data.gov integration.
"""

import asyncio
import sys
import os
import logging
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.agents.datagov_agent import DataGovAgent
from src.core.datagov.data_ingestion_manager import DataIngestionManager
from src.core.datagov.analysis_engine import DataGovAnalysisEngine
from src.core.datagov.query_processor import NLQueryProcessor
from src.config.datagov_config import DataGovConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_datagov_agent():
    """Test the DataGovAgent."""
    logger.info("Testing DataGovAgent...")
    
    try:
        # Create agent
        agent = DataGovAgent()
        logger.info(f"✅ DataGovAgent created successfully with ID: {agent.agent_id}")
        
        # Test health check
        health_status = await agent.health_check()
        logger.info(f"✅ Health check completed: {health_status['status']}")
        
        # Test trade analysis
        trade_result = await agent.get_trade_analysis(["CHN", "RUS"])
        logger.info(f"✅ Trade analysis completed: {len(trade_result.get('countries', {}))} countries analyzed")
        
        # Test economic forecast
        economic_result = await agent.get_economic_forecast("CHN")
        logger.info(f"✅ Economic forecast completed for China")
        
        # Test environmental analysis
        env_result = await agent.get_environmental_analysis(["CHN", "RUS"])
        logger.info(f"✅ Environmental analysis completed: {len(env_result.get('countries', {}))} countries analyzed")
        
        # Test natural language query
        nl_result = await agent.answer_natural_language_query("What are the trade trends between China and Russia?")
        logger.info(f"✅ Natural language query completed: {nl_result.get('query_type', 'unknown')}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ DataGovAgent test failed: {e}")
        return False


async def test_data_ingestion_manager():
    """Test the DataIngestionManager."""
    logger.info("Testing DataIngestionManager...")
    
    try:
        # Create manager
        manager = DataIngestionManager()
        logger.info("✅ DataIngestionManager created successfully")
        
        # Test fetching live data
        live_data = await manager.fetch_live_data(["CHN", "RUS"])
        logger.info(f"✅ Live data fetched from {len(live_data)} sources")
        
        # Test health check
        health_status = await manager.health_check()
        logger.info(f"✅ Health check completed: {health_status['status']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ DataIngestionManager test failed: {e}")
        return False


async def test_analysis_engine():
    """Test the DataGovAnalysisEngine."""
    logger.info("Testing DataGovAnalysisEngine...")
    
    try:
        # Create engine
        engine = DataGovAnalysisEngine()
        logger.info("✅ DataGovAnalysisEngine created successfully")
        
        # Test data processing
        mock_data = {
            "census": {
                "source": "census",
                "timestamp": datetime.utcnow().isoformat(),
                "countries": [
                    {
                        "code": "CHN",
                        "name": "China",
                        "trade_data": {
                            "imports": {"value": 1000000, "currency": "USD"},
                            "exports": {"value": 800000, "currency": "USD"}
                        }
                    }
                ]
            }
        }
        
        processed_data = await engine.process_data(mock_data)
        logger.info(f"✅ Data processing completed: {len(processed_data.get('sources', {}))} sources processed")
        
        # Test health check
        health_status = await engine.health_check()
        logger.info(f"✅ Health check completed: {health_status['status']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ DataGovAnalysisEngine test failed: {e}")
        return False


async def test_query_processor():
    """Test the NLQueryProcessor."""
    logger.info("Testing NLQueryProcessor...")
    
    try:
        # Create processor
        processor = NLQueryProcessor()
        logger.info("✅ NLQueryProcessor created successfully")
        
        # Test natural language query
        query = "What are the trade trends between China and Russia over the last 5 years?"
        result = await processor.process_query(query)
        logger.info(f"✅ Query processing completed: {result.get('query_type', 'unknown')}")
        
        # Test health check
        health_status = await processor.health_check()
        logger.info(f"✅ Health check completed: {health_status['status']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ NLQueryProcessor test failed: {e}")
        return False


async def test_configuration():
    """Test the DataGovConfig."""
    logger.info("Testing DataGovConfig...")
    
    try:
        # Create config
        config = DataGovConfig()
        logger.info("✅ DataGovConfig created successfully")
        
        # Test configuration methods
        api_key = config.get_api_key("census")
        logger.info(f"✅ API key retrieved: {'configured' if api_key else 'not configured'}")
        
        base_url = config.get_base_url("census")
        logger.info(f"✅ Base URL retrieved: {base_url}")
        
        is_enabled = config.is_data_source_enabled("census")
        logger.info(f"✅ Data source enabled check: {is_enabled}")
        
        rate_limit = config.get_rate_limit("census")
        logger.info(f"✅ Rate limit retrieved: {rate_limit}")
        
        config_summary = config.get_config_summary()
        logger.info(f"✅ Config summary generated: {len(config_summary)} sections")
        
        validation_issues = config.validate_config()
        if validation_issues:
            logger.warning(f"⚠️ Configuration validation issues: {validation_issues}")
        else:
            logger.info("✅ Configuration validation passed")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ DataGovConfig test failed: {e}")
        return False


async def test_integration():
    """Test the complete integration."""
    logger.info("Testing complete Data.gov integration...")
    
    try:
        # Create all components
        agent = DataGovAgent()
        manager = DataIngestionManager()
        engine = DataGovAnalysisEngine()
        processor = NLQueryProcessor()
        config = DataGovConfig()
        
        logger.info("✅ All components created successfully")
        
        # Test end-to-end workflow
        # 1. Fetch data
        live_data = await manager.fetch_live_data(["CHN", "RUS"])
        logger.info(f"✅ Step 1: Data fetched from {len(live_data)} sources")
        
        # 2. Process data
        processed_data = await engine.process_data(live_data)
        logger.info(f"✅ Step 2: Data processed for {len(processed_data.get('sources', {}))} sources")
        
        # 3. Generate embeddings and relationships
        embeddings = await manager.store_embeddings(processed_data)
        relationships = await manager.create_relationships(processed_data)
        logger.info(f"✅ Step 3: {len(embeddings)} embeddings and {len(relationships)} relationships created")
        
        # 4. Process natural language query
        query_result = await processor.process_query("Compare economic performance between China and Russia")
        logger.info(f"✅ Step 4: Natural language query processed: {query_result.get('query_type', 'unknown')}")
        
        # 5. Agent analysis
        analysis_result = await agent.get_trade_analysis(["CHN", "RUS"])
        logger.info(f"✅ Step 5: Agent analysis completed")
        
        logger.info("✅ Complete integration test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        return False


async def main():
    """Run all tests."""
    logger.info("🚀 Starting Data.gov Phase 1 Implementation Tests")
    logger.info("=" * 60)
    
    test_results = {}
    
    # Run individual component tests
    test_results["agent"] = await test_datagov_agent()
    test_results["ingestion_manager"] = await test_data_ingestion_manager()
    test_results["analysis_engine"] = await test_analysis_engine()
    test_results["query_processor"] = await test_query_processor()
    test_results["configuration"] = await test_configuration()
    
    # Run integration test
    test_results["integration"] = await test_integration()
    
    # Report results
    logger.info("=" * 60)
    logger.info("📊 Test Results Summary:")
    logger.info("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    logger.info("=" * 60)
    logger.info(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Phase 1 implementation is working correctly.")
        return True
    else:
        logger.error(f"⚠️ {total - passed} tests failed. Please review the implementation.")
        return False


if __name__ == "__main__":
    # Run with .venv/Scripts/python.exe as required
    success = asyncio.run(main())
    
    if success:
        logger.info("✅ Phase 1 implementation verification completed successfully")
        sys.exit(0)
    else:
        logger.error("❌ Phase 1 implementation verification failed")
        sys.exit(1)
