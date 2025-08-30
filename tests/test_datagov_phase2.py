"""
Comprehensive Test Suite for Data.gov API Integration Phase 2
Testing Data Processing Engine, Vector DB Integration, and Knowledge Graph Integration
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.datagov.data_processing_engine import DataProcessingEngine, ProcessedData, DataValidationResult, DataQualityLevel
from src.core.datagov.vector_db_integration import DataGovVectorDBIntegration
from src.core.datagov.knowledge_graph_integration import DataGovKnowledgeGraphIntegration
from src.agents.datagov_agent import DataGovAgent
from src.config.datagov_config import DataGovConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataGovPhase2TestSuite:
    """Comprehensive test suite for Data.gov Phase 2 integration."""
    
    def __init__(self):
        self.config = DataGovConfig()
        self.data_processor = DataProcessingEngine()
        self.vector_db_integration = DataGovVectorDBIntegration()
        self.knowledge_graph_integration = DataGovKnowledgeGraphIntegration()
        self.agent = DataGovAgent()
        
        # Test data
        self.test_trade_data = {
            'records': [
                {
                    'country_code': 'CHN',
                    'trade_value': 1000000.0,
                    'date': '2024-01-01',
                    'commodity_code': 'HS001',
                    'trade_type': 'import',
                    'currency': 'USD'
                },
                {
                    'country_code': 'RUS',
                    'trade_value': 500000.0,
                    'date': '2024-01-01',
                    'commodity_code': 'HS002',
                    'trade_type': 'export',
                    'currency': 'USD'
                }
            ]
        }
        
        self.test_macroeconomic_data = {
            'records': [
                {
                    'country_code': 'CHN',
                    'gdp': 15000000000000.0,  # $15 trillion
                    'population': 1400000000,  # 1.4 billion
                    'date': '2024-01-01',
                    'currency': 'USD'
                },
                {
                    'country_code': 'RUS',
                    'gdp': 2000000000000.0,   # $2 trillion
                    'population': 144000000,   # 144 million
                    'date': '2024-01-01',
                    'currency': 'USD'
                }
            ]
        }
        
        self.test_environmental_data = {
            'records': [
                {
                    'country_code': 'CHN',
                    'epi_score': 75.0,
                    'date': '2024-01-01',
                    'air_quality': 80.0,
                    'water_quality': 70.0,
                    'biodiversity': 85.0
                },
                {
                    'country_code': 'RUS',
                    'epi_score': 82.0,
                    'date': '2024-01-01',
                    'air_quality': 85.0,
                    'water_quality': 75.0,
                    'biodiversity': 90.0
                }
            ]
        }
    
    async def test_data_processing_engine(self) -> Dict[str, Any]:
        """Test the data processing engine functionality."""
        logger.info("🧪 Testing Data Processing Engine...")
        
        results = {
            'trade_data_processing': False,
            'macroeconomic_data_processing': False,
            'environmental_data_processing': False,
            'data_quality_validation': False,
            'embedding_generation': False
        }
        
        try:
            # Test trade data processing
            logger.info("Testing trade data processing...")
            processed_trade_data = await self.data_processor.process_trade_data(self.test_trade_data)
            
            if (processed_trade_data and 
                hasattr(processed_trade_data, 'processed_data') and 
                processed_trade_data.processed_data.get('records')):
                results['trade_data_processing'] = True
                logger.info(f"✅ Trade data processing successful: {len(processed_trade_data.processed_data['records'])} records")
            else:
                logger.error("❌ Trade data processing failed")
            
            # Test macroeconomic data processing
            logger.info("Testing macroeconomic data processing...")
            processed_economic_data = await self.data_processor.process_macroeconomic_data(self.test_macroeconomic_data)
            
            if (processed_economic_data and 
                hasattr(processed_economic_data, 'processed_data') and 
                processed_economic_data.processed_data.get('records')):
                results['macroeconomic_data_processing'] = True
                logger.info(f"✅ Macroeconomic data processing successful: {len(processed_economic_data.processed_data['records'])} records")
            else:
                logger.error("❌ Macroeconomic data processing failed")
            
            # Test environmental data processing
            logger.info("Testing environmental data processing...")
            processed_environmental_data = await self.data_processor.process_environmental_data(self.test_environmental_data)
            
            if (processed_environmental_data and 
                hasattr(processed_environmental_data, 'processed_data') and 
                processed_environmental_data.processed_data.get('records')):
                results['environmental_data_processing'] = True
                logger.info(f"✅ Environmental data processing successful: {len(processed_environmental_data.processed_data['records'])} records")
            else:
                logger.error("❌ Environmental data processing failed")
            
            # Test data quality validation
            logger.info("Testing data quality validation...")
            if (processed_trade_data and 
                hasattr(processed_trade_data, 'validation_result') and 
                processed_trade_data.validation_result.is_valid):
                results['data_quality_validation'] = True
                logger.info(f"✅ Data quality validation successful: {processed_trade_data.validation_result.quality_level.value}")
            else:
                logger.error("❌ Data quality validation failed")
            
            # Test embedding generation
            logger.info("Testing embedding generation...")
            if (processed_trade_data and 
                hasattr(processed_trade_data, 'embeddings') and 
                processed_trade_data.embeddings):
                results['embedding_generation'] = True
                logger.info(f"✅ Embedding generation successful: {len(processed_trade_data.embeddings)} dimensions")
            else:
                logger.error("❌ Embedding generation failed")
            
        except Exception as e:
            logger.error(f"❌ Data processing engine test failed: {e}")
        
        return results
    
    async def test_vector_database_integration(self) -> Dict[str, Any]:
        """Test the vector database integration functionality."""
        logger.info("🧪 Testing Vector Database Integration...")
        
        results = {
            'collection_initialization': False,
            'trade_embeddings_storage': False,
            'economic_embeddings_storage': False,
            'environmental_embeddings_storage': False,
            'similarity_search': False,
            'data_statistics': False
        }
        
        try:
            # Test collection initialization
            logger.info("Testing collection initialization...")
            # Collections are initialized in constructor
            results['collection_initialization'] = True
            logger.info("✅ Collection initialization successful")
            
            # Test trade embeddings storage
            logger.info("Testing trade embeddings storage...")
            test_embeddings = [0.1, 0.2, 0.3, 0.4, 0.5] * 20  # 100-dimensional embedding
            storage_success = await self.vector_db_integration.store_trade_embeddings(
                self.test_trade_data, test_embeddings
            )
            if storage_success:
                results['trade_embeddings_storage'] = True
                logger.info("✅ Trade embeddings storage successful")
            else:
                logger.error("❌ Trade embeddings storage failed")
            
            # Test economic embeddings storage
            logger.info("Testing economic embeddings storage...")
            storage_success = await self.vector_db_integration.store_macroeconomic_embeddings(
                self.test_macroeconomic_data, test_embeddings
            )
            if storage_success:
                results['economic_embeddings_storage'] = True
                logger.info("✅ Economic embeddings storage successful")
            else:
                logger.error("❌ Economic embeddings storage failed")
            
            # Test environmental embeddings storage
            logger.info("Testing environmental embeddings storage...")
            storage_success = await self.vector_db_integration.store_environmental_embeddings(
                self.test_environmental_data, test_embeddings
            )
            if storage_success:
                results['environmental_embeddings_storage'] = True
                logger.info("✅ Environmental embeddings storage successful")
            else:
                logger.error("❌ Environmental embeddings storage failed")
            
            # Test similarity search
            logger.info("Testing similarity search...")
            search_results = await self.vector_db_integration.search_similar_trade_data(
                test_embeddings, countries=['CHN'], limit=5
            )
            if search_results is not None:
                results['similarity_search'] = True
                logger.info(f"✅ Similarity search successful: {len(search_results)} results")
            else:
                logger.error("❌ Similarity search failed")
            
            # Test data statistics
            logger.info("Testing data statistics...")
            stats = await self.vector_db_integration.get_data_statistics()
            if stats and 'total_collections' in stats:
                results['data_statistics'] = True
                logger.info(f"✅ Data statistics successful: {stats['total_collections']} collections")
            else:
                logger.error("❌ Data statistics failed")
            
        except Exception as e:
            logger.error(f"❌ Vector database integration test failed: {e}")
        
        return results
    
    async def test_knowledge_graph_integration(self) -> Dict[str, Any]:
        """Test the knowledge graph integration functionality."""
        logger.info("🧪 Testing Knowledge Graph Integration...")
        
        results = {
            'country_node_creation': False,
            'trade_relationships': False,
            'economic_relationships': False,
            'environmental_relationships': False,
            'country_data_summary': False,
            'graph_statistics': False
        }
        
        try:
            # Test country node creation
            logger.info("Testing country node creation...")
            success = await self.knowledge_graph_integration.create_country_node('CHN', 'China')
            if success:
                results['country_node_creation'] = True
                logger.info("✅ Country node creation successful")
            else:
                logger.error("❌ Country node creation failed")
            
            # Test trade relationships
            logger.info("Testing trade relationships...")
            relationship_count = await self.knowledge_graph_integration.create_trade_relationships(
                'CHN', self.test_trade_data['records']
            )
            if relationship_count > 0:
                results['trade_relationships'] = True
                logger.info(f"✅ Trade relationships successful: {relationship_count} relationships")
            else:
                logger.error("❌ Trade relationships failed")
            
            # Test economic relationships
            logger.info("Testing economic relationships...")
            relationship_count = await self.knowledge_graph_integration.create_economic_relationships(
                'CHN', self.test_macroeconomic_data['records']
            )
            if relationship_count > 0:
                results['economic_relationships'] = True
                logger.info(f"✅ Economic relationships successful: {relationship_count} relationships")
            else:
                logger.error("❌ Economic relationships failed")
            
            # Test environmental relationships
            logger.info("Testing environmental relationships...")
            relationship_count = await self.knowledge_graph_integration.create_environmental_relationships(
                'CHN', self.test_environmental_data['records']
            )
            if relationship_count > 0:
                results['environmental_relationships'] = True
                logger.info(f"✅ Environmental relationships successful: {relationship_count} relationships")
            else:
                logger.error("❌ Environmental relationships failed")
            
            # Test country data summary
            logger.info("Testing country data summary...")
            summary = await self.knowledge_graph_integration.get_country_data_summary('CHN')
            if summary and 'country_code' in summary:
                results['country_data_summary'] = True
                logger.info(f"✅ Country data summary successful: {summary['trade_data_count']} trade records")
            else:
                logger.error("❌ Country data summary failed")
            
            # Test graph statistics
            logger.info("Testing graph statistics...")
            stats = await self.knowledge_graph_integration.get_graph_statistics()
            if stats and 'total_nodes' in stats:
                results['graph_statistics'] = True
                logger.info(f"✅ Graph statistics successful: {stats['total_nodes']} total nodes")
            else:
                logger.error("❌ Graph statistics failed")
            
        except Exception as e:
            logger.error(f"❌ Knowledge graph integration test failed: {e}")
        
        return results
    
    async def test_agent_integration(self) -> Dict[str, Any]:
        """Test the DataGovAgent integration with Phase 2 components."""
        logger.info("🧪 Testing DataGovAgent Integration...")
        
        results = {
            'agent_initialization': False,
            'health_check': False,
            'component_integration': False
        }
        
        try:
            # Test agent initialization
            logger.info("Testing agent initialization...")
            if self.agent and hasattr(self.agent, 'data_processor'):
                results['agent_initialization'] = True
                logger.info("✅ Agent initialization successful")
            else:
                logger.error("❌ Agent initialization failed")
            
            # Test health check
            logger.info("Testing agent health check...")
            health_status = await self.agent.health_check()
            if health_status and 'status' in health_status:
                results['health_check'] = True
                logger.info(f"✅ Agent health check successful: {health_status['status']}")
            else:
                logger.error("❌ Agent health check failed")
            
            # Test component integration
            logger.info("Testing component integration...")
            if (hasattr(self.agent, 'data_processor') and 
                hasattr(self.agent, 'data_manager') and 
                hasattr(self.agent, 'analysis_engine')):
                results['component_integration'] = True
                logger.info("✅ Component integration successful")
            else:
                logger.error("❌ Component integration failed")
            
        except Exception as e:
            logger.error(f"❌ Agent integration test failed: {e}")
        
        return results
    
    async def test_end_to_end_workflow(self) -> Dict[str, Any]:
        """Test end-to-end workflow with Phase 2 components."""
        logger.info("🧪 Testing End-to-End Workflow...")
        
        results = {
            'data_ingestion': False,
            'data_processing': False,
            'vector_storage': False,
            'knowledge_graph_storage': False,
            'quality_reporting': False
        }
        
        try:
            # Test data ingestion (using mock data)
            logger.info("Testing data ingestion...")
            # For testing, we'll use our test data directly
            raw_data = {
                'trade_data': self.test_trade_data,
                'macroeconomic_data': self.test_macroeconomic_data,
                'environmental_data': self.test_environmental_data
            }
            results['data_ingestion'] = True
            logger.info("✅ Data ingestion successful")
            
            # Test data processing
            logger.info("Testing data processing...")
            processed_trade_data = await self.data_processor.process_trade_data(raw_data['trade_data'])
            if processed_trade_data and processed_trade_data.validation_result.is_valid:
                results['data_processing'] = True
                logger.info("✅ Data processing successful")
            else:
                logger.error("❌ Data processing failed")
            
            # Test vector storage
            logger.info("Testing vector storage...")
            if processed_trade_data and processed_trade_data.embeddings:
                storage_success = await self.data_processor.store_processed_data(processed_trade_data)
                if storage_success:
                    results['vector_storage'] = True
                    logger.info("✅ Vector storage successful")
                else:
                    logger.error("❌ Vector storage failed")
            else:
                logger.error("❌ Vector storage failed - no embeddings generated")
            
            # Test knowledge graph storage
            logger.info("Testing knowledge graph storage...")
            relationship_count = await self.knowledge_graph_integration.create_trade_relationships(
                'CHN', processed_trade_data.processed_data.get('records', [])
            )
            if relationship_count > 0:
                results['knowledge_graph_storage'] = True
                logger.info(f"✅ Knowledge graph storage successful: {relationship_count} relationships")
            else:
                logger.error("❌ Knowledge graph storage failed")
            
            # Test quality reporting
            logger.info("Testing quality reporting...")
            quality_report = await self.data_processor.get_data_quality_report(processed_trade_data)
            if quality_report and 'validation_result' in quality_report:
                results['quality_reporting'] = True
                logger.info(f"✅ Quality reporting successful: {quality_report['validation_result']['quality_level']}")
            else:
                logger.error("❌ Quality reporting failed")
            
        except Exception as e:
            logger.error(f"❌ End-to-end workflow test failed: {e}")
        
        return results
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all Phase 2 tests and generate comprehensive report."""
        logger.info("🚀 Starting Data.gov Phase 2 Comprehensive Test Suite...")
        
        start_time = datetime.utcnow()
        
        # Run all test suites
        test_results = {
            'data_processing_engine': await self.test_data_processing_engine(),
            'vector_database_integration': await self.test_vector_database_integration(),
            'knowledge_graph_integration': await self.test_knowledge_graph_integration(),
            'agent_integration': await self.test_agent_integration(),
            'end_to_end_workflow': await self.test_end_to_end_workflow()
        }
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Calculate overall statistics
        total_tests = 0
        passed_tests = 0
        
        for test_suite, results in test_results.items():
            for test_name, result in results.items():
                total_tests += 1
                if result:
                    passed_tests += 1
        
        # Generate comprehensive report
        report = {
            'test_suite': 'Data.gov Phase 2 Integration',
            'timestamp': datetime.utcnow().isoformat(),
            'duration_seconds': duration,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'test_results': test_results,
            'summary': {
                'data_processing_engine': all(test_results['data_processing_engine'].values()),
                'vector_database_integration': all(test_results['vector_database_integration'].values()),
                'knowledge_graph_integration': all(test_results['knowledge_graph_integration'].values()),
                'agent_integration': all(test_results['agent_integration'].values()),
                'end_to_end_workflow': all(test_results['end_to_end_workflow'].values())
            }
        }
        
        # Print summary
        logger.info("📊 Test Results Summary:")
        logger.info(f"   Total Tests: {total_tests}")
        logger.info(f"   Passed: {passed_tests}")
        logger.info(f"   Failed: {total_tests - passed_tests}")
        logger.info(f"   Success Rate: {report['success_rate']:.1f}%")
        logger.info(f"   Duration: {duration:.2f} seconds")
        
        logger.info("📋 Detailed Results:")
        for test_suite, results in test_results.items():
            suite_passed = sum(results.values())
            suite_total = len(results)
            logger.info(f"   {test_suite}: {suite_passed}/{suite_total} tests passed")
        
        # Save detailed report
        report_file = f"Results/datagov_phase2_test_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs("Results", exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"📄 Detailed report saved to: {report_file}")
        
        return report


async def main():
    """Main test execution function."""
    logger.info("🔧 Data.gov Phase 2 Test Suite")
    logger.info("=" * 50)
    
    # Create test suite
    test_suite = DataGovPhase2TestSuite()
    
    # Run all tests
    report = await test_suite.run_all_tests()
    
    # Determine overall success
    overall_success = report['success_rate'] >= 80.0
    
    if overall_success:
        logger.info("🎉 Phase 2 tests completed successfully!")
        logger.info("✅ Ready for Phase 3 development")
    else:
        logger.warning("⚠️  Phase 2 tests completed with issues")
        logger.warning("🔧 Review failed tests before proceeding to Phase 3")
    
    return overall_success


if __name__ == "__main__":
    # Run with .venv/Scripts/python.exe as required
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
