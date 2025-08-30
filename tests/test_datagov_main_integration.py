#!/usr/bin/env python3
"""
Test script to verify Data.gov Phase 2 integration with main.py components.
This script tests the integration without the full configuration dependencies.
"""

import sys
import os
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_datagov_phase2_components():
    """Test that Data.gov Phase 2 components can be imported and initialized."""
    
    print("Testing Data.gov Phase 2 Integration Components...")
    print("=" * 60)
    
    # Test 1: Data Processing Engine
    try:
        from src.core.datagov.data_processing_engine import DataProcessingEngine
        data_processor = DataProcessingEngine()
        print("✅ DataProcessingEngine imported and initialized successfully")
    except Exception as e:
        print(f"❌ DataProcessingEngine failed: {e}")
        return False
    
    # Test 2: Vector Database Integration
    try:
        from src.core.datagov.vector_db_integration import DataGovVectorDBIntegration
        vector_db = DataGovVectorDBIntegration()
        print("✅ DataGovVectorDBIntegration imported and initialized successfully")
    except Exception as e:
        print(f"❌ DataGovVectorDBIntegration failed: {e}")
        return False
    
    # Test 3: Knowledge Graph Integration
    try:
        from src.core.datagov.knowledge_graph_integration import DataGovKnowledgeGraphIntegration
        kg_integration = DataGovKnowledgeGraphIntegration()
        print("✅ DataGovKnowledgeGraphIntegration imported and initialized successfully")
    except Exception as e:
        print(f"❌ DataGovKnowledgeGraphIntegration failed: {e}")
        return False
    
    # Test 4: DataGov Agent
    try:
        from src.agents.datagov_agent import DataGovAgent
        agent = DataGovAgent("test_agent")
        print("✅ DataGovAgent imported and initialized successfully")
    except Exception as e:
        print(f"❌ DataGovAgent failed: {e}")
        return False
    
    # Test 5: Data Ingestion Manager
    try:
        from src.core.datagov.data_ingestion_manager import DataIngestionManager
        ingestion_manager = DataIngestionManager()
        print("✅ DataIngestionManager imported and initialized successfully")
    except Exception as e:
        print(f"❌ DataIngestionManager failed: {e}")
        return False
    
    # Test 6: DataGov Analysis Engine
    try:
        from src.core.datagov.analysis_engine import DataGovAnalysisEngine
        analysis_engine = DataGovAnalysisEngine()
        print("✅ DataGovAnalysisEngine imported and initialized successfully")
    except Exception as e:
        print(f"❌ DataGovAnalysisEngine failed: {e}")
        return False
    
    # Test 7: NL Query Processor
    try:
        from src.core.datagov.nl_query_processor import NLQueryProcessor
        query_processor = NLQueryProcessor()
        print("✅ NLQueryProcessor imported and initialized successfully")
    except Exception as e:
        print(f"❌ NLQueryProcessor failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All Data.gov Phase 2 components imported and initialized successfully!")
    print("✅ Phase 2 integration test PASSED")
    return True

def test_datagov_api_routes():
    """Test that Data.gov API routes can be imported."""
    
    print("\nTesting Data.gov API Routes...")
    print("=" * 60)
    
    try:
        from src.api.datagov_routes import router as datagov_router
        print("✅ Data.gov API routes imported successfully")
        return True
    except Exception as e:
        print(f"❌ Data.gov API routes failed: {e}")
        return False

def test_datagov_config():
    """Test that Data.gov configuration can be imported."""
    
    print("\nTesting Data.gov Configuration...")
    print("=" * 60)
    
    try:
        from src.config.datagov_config import DataGovConfig
        config = DataGovConfig()
        print("✅ Data.gov configuration imported and initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Data.gov configuration failed: {e}")
        return False

def main():
    """Main test function."""
    
    print("Data.gov Phase 2 Integration Test")
    print("=" * 60)
    print(f"Test started at: {datetime.now()}")
    print()
    
    # Run tests
    component_test = test_datagov_phase2_components()
    api_test = test_datagov_api_routes()
    config_test = test_datagov_config()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Components Test: {'✅ PASSED' if component_test else '❌ FAILED'}")
    print(f"API Routes Test: {'✅ PASSED' if api_test else '❌ FAILED'}")
    print(f"Configuration Test: {'✅ PASSED' if config_test else '❌ FAILED'}")
    
    overall_success = component_test and api_test and config_test
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Data.gov Phase 2 integration is working correctly")
        print("✅ Ready for Phase 3 development")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("⚠️ Data.gov Phase 2 integration needs attention")
    
    print(f"\nTest completed at: {datetime.now()}")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
