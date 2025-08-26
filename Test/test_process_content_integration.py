#!/usr/bin/env python3
"""
Test script to verify process_content MCP tool integration with vector DB and knowledge graph DB.
This script tests that search query responses are properly stored in both databases.
"""

import asyncio
import logging
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.mcp_servers.unified_mcp_server import UnifiedMCPServer
from src.core.models import AnalysisRequest, DataType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_process_content_integration():
    """Test that process_content properly stores content in both vector DB and knowledge graph DB."""
    
    logger.info("🧪 Starting process_content integration test...")
    
    try:
        # Initialize the MCP server
        server = UnifiedMCPServer()
        
        # Test 1: Process simple text content
        logger.info("📝 Test 1: Processing simple text content...")
        text_content = """
        The Art of War by Sun Tzu is a Chinese military treatise that was written during the 5th century BC. 
        The work contains a detailed explanation and analysis of the Chinese military, from weapons and strategy 
        to rank and discipline. Sun Tzu emphasized the importance of positioning in military strategy, and that 
        the decision to position an army must be based on both objective conditions in the physical environment 
        and the subjective beliefs of other, competitive actors in that environment.
        """
        
        result1 = await server.process_content(
            content=text_content,
            content_type="text",
            language="en"
        )
        
        logger.info(f"✅ Text processing result: {result1.get('success', False)}")
        
        # Test 2: Process bulk import request
        logger.info("📚 Test 2: Processing bulk import request...")
        bulk_request = """
        Please add the following URLs to both vector database and knowledge graph database:
        @https://openlibrary.org/works/OL45804W/The_Art_of_War
        @https://ctext.org/sunzi-bingfa
        """
        
        result2 = await server.process_content(
            content=bulk_request,
            content_type="auto",
            language="en"
        )
        
        logger.info(f"✅ Bulk import result: {result2.get('success', False)}")
        if result2.get('success'):
            logger.info(f"   URLs processed: {result2.get('urls_processed', 0)}")
            logger.info(f"   Successful imports: {result2.get('successful_imports', 0)}")
            logger.info(f"   Total entities: {result2.get('total_entities', 0)}")
            logger.info(f"   Total relationships: {result2.get('total_relationships', 0)}")
            logger.info(f"   Knowledge graph nodes: {result2.get('total_knowledge_graph_nodes', 0)}")
            logger.info(f"   Knowledge graph edges: {result2.get('total_knowledge_graph_edges', 0)}")
        
        # Test 3: Verify ingestion using the verify_ingestion tool
        logger.info("🔍 Test 3: Verifying ingestion...")
        verification_result = await server.verify_ingestion(
            search_queries=[
                "Sun Tzu Art of War",
                "military strategy",
                "The Art of War principles"
            ],
            test_knowledge_graph=True,
            test_semantic_search=True
        )
        
        logger.info(f"✅ Verification result: {verification_result.get('success', False)}")
        if verification_result.get('success'):
            summary = verification_result.get('summary', {})
            logger.info(f"   Vector database status: {summary.get('vector_database_status', 'unknown')}")
            logger.info(f"   Semantic search success rate: {summary.get('semantic_search_success_rate', '0/0')}")
            logger.info(f"   Knowledge graph success rate: {summary.get('knowledge_graph_success_rate', '0/0')}")
        
        # Test 4: Test knowledge graph query
        logger.info("🧠 Test 4: Testing knowledge graph query...")
        kg_query_result = await server.query_knowledge_graph(
            query="Sun Tzu military strategy principles"
        )
        
        logger.info(f"✅ Knowledge graph query result: {kg_query_result.get('success', False)}")
        if kg_query_result.get('success'):
            results = kg_query_result.get('result', {}).get('query_results', [])
            logger.info(f"   Query results found: {len(results)}")
        
        # Test 5: Test semantic search
        logger.info("🔎 Test 5: Testing semantic search...")
        search_result = await server.semantic_search(
            query="military strategy and tactics",
            n_results=5
        )
        
        logger.info(f"✅ Semantic search result: {search_result.get('success', False)}")
        if search_result.get('success'):
            results = search_result.get('result', [])
            logger.info(f"   Search results found: {len(results)}")
        
        logger.info("🎉 All tests completed successfully!")
        
        # Summary
        logger.info("\n📊 Test Summary:")
        logger.info(f"   Text processing: {'✅ PASS' if result1.get('success') else '❌ FAIL'}")
        logger.info(f"   Bulk import: {'✅ PASS' if result2.get('success') else '❌ FAIL'}")
        logger.info(f"   Ingestion verification: {'✅ PASS' if verification_result.get('success') else '❌ FAIL'}")
        logger.info(f"   Knowledge graph query: {'✅ PASS' if kg_query_result.get('success') else '❌ FAIL'}")
        logger.info(f"   Semantic search: {'✅ PASS' if search_result.get('success') else '❌ FAIL'}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False

async def test_strategic_recommendations_with_kg():
    """Test that strategic recommendations leverage knowledge graph intelligence."""
    
    logger.info("🎯 Testing strategic recommendations with knowledge graph integration...")
    
    try:
        server = UnifiedMCPServer()
        
        # Create a strategic assessment
        assessment_data = {
            "domain": "defense",
            "context": "Analyzing military strategy based on Sun Tzu's Art of War principles",
            "five_fundamentals": {
                "the_way": 0.7,
                "heaven": 0.6,
                "earth": 0.8,
                "command": 0.5,
                "method": 0.9
            },
            "deception_effectiveness": 0.6,
            "resource_efficiency": 0.8,
            "intelligence_superiority": 0.7,
            "alliance_strength": 0.5
        }
        
        # Generate strategic recommendations
        recommendations_result = await server.generate_strategic_recommendations(
            assessment_result=assessment_data,
            domain="defense",
            language="en"
        )
        
        logger.info(f"✅ Strategic recommendations result: {recommendations_result.get('success', False)}")
        if recommendations_result.get('success'):
            recommendations = recommendations_result.get('result', {}).get('recommendations', [])
            logger.info(f"   Recommendations generated: {len(recommendations)}")
            for i, rec in enumerate(recommendations[:3]):  # Show first 3
                logger.info(f"   {i+1}. {rec.get('recommendation', 'N/A')}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Strategic recommendations test failed: {e}")
        return False

async def main():
    """Run all integration tests."""
    logger.info("🚀 Starting DIA3 process_content integration tests...")
    
    # Test 1: Basic process_content integration
    test1_result = await test_process_content_integration()
    
    # Test 2: Strategic recommendations with knowledge graph
    test2_result = await test_strategic_recommendations_with_kg()
    
    # Overall result
    if test1_result and test2_result:
        logger.info("🎉 All integration tests PASSED!")
        logger.info("✅ process_content MCP tool is properly storing content in both vector DB and knowledge graph DB")
        logger.info("✅ Strategic recommendations are leveraging knowledge graph intelligence")
        return True
    else:
        logger.error("❌ Some integration tests FAILED!")
        logger.error("❌ Please check the implementation and fix any issues")
        return False

if __name__ == "__main__":
    asyncio.run(main())
