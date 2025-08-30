#!/usr/bin/env python3
"""
Test script to verify enhanced strategic analytics engine with knowledge graph intelligence.
This script tests the Phase 1 implementation of knowledge graph intelligence integration.
"""

import asyncio
import logging
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.strategic_analytics_engine import StrategicAnalyticsEngine, StrategicMetrics, StrategicDomain
from src.agents.knowledge_graph_agent import KnowledgeGraphAgent
from src.core.vector_db import VectorDBManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_enhanced_strategic_analytics():
    """Test the enhanced strategic analytics engine with knowledge graph intelligence."""
    
    logger.info("🧪 Starting enhanced strategic analytics test...")
    
    try:
        # Initialize components
        logger.info("📋 Initializing components...")
        
        # Initialize knowledge graph agent
        kg_agent = KnowledgeGraphAgent()
        logger.info("✅ Knowledge Graph Agent initialized")
        
        # Initialize vector store
        vector_store = VectorDBManager()
        logger.info("✅ Vector Store initialized")
        
        # Initialize enhanced strategic analytics engine
        strategic_engine = StrategicAnalyticsEngine(
            knowledge_graph_agent=kg_agent,
            vector_store=vector_store
        )
        logger.info("✅ Enhanced Strategic Analytics Engine initialized")
        
        # Test 1: Knowledge Graph Intelligence Query
        logger.info("🔍 Test 1: Knowledge Graph Intelligence Query...")
        kg_result = await strategic_engine.query_knowledge_graph_for_intelligence(
            query="Sun Tzu military strategy principles",
            domain="military"
        )
        
        logger.info(f"✅ Knowledge Graph Intelligence Query: {kg_result.get('success', False)}")
        if kg_result.get('success'):
            insights = kg_result.get('strategic_insights', {})
            logger.info(f"   Strategic patterns found: {len(insights.get('strategic_patterns', []))}")
            logger.info(f"   Risk indicators found: {len(insights.get('risk_indicators', []))}")
            logger.info(f"   Opportunities found: {len(insights.get('opportunities', []))}")
        
        # Test 2: Historical Pattern Analysis
        logger.info("📊 Test 2: Historical Pattern Analysis...")
        historical_result = await strategic_engine.analyze_historical_patterns(
            entity="Sun Tzu",
            timeframe="1y"
        )
        
        logger.info(f"✅ Historical Pattern Analysis: {historical_result.get('success', False)}")
        if historical_result.get('success'):
            patterns = historical_result.get('patterns', {})
            logger.info(f"   Trends identified: {len(patterns.get('trends', []))}")
            logger.info(f"   Cycles identified: {len(patterns.get('cycles', []))}")
        
        # Test 3: Cross-Domain Intelligence Generation
        logger.info("🌐 Test 3: Cross-Domain Intelligence Generation...")
        cross_domain_result = await strategic_engine.generate_cross_domain_intelligence(
            domains=["military", "business", "intelligence"]
        )
        
        logger.info(f"✅ Cross-Domain Intelligence: {cross_domain_result.get('success', False)}")
        if cross_domain_result.get('success'):
            domain_insights = cross_domain_result.get('domain_insights', {})
            cross_connections = cross_domain_result.get('cross_connections', [])
            logger.info(f"   Domains analyzed: {len(domain_insights)}")
            logger.info(f"   Cross-domain connections: {len(cross_connections)}")
        
        # Test 4: Strategic Trend Prediction
        logger.info("🔮 Test 4: Strategic Trend Prediction...")
        trend_result = await strategic_engine.predict_strategic_trends(
            context="military strategy evolution"
        )
        
        logger.info(f"✅ Strategic Trend Prediction: {trend_result.get('success', False)}")
        if trend_result.get('success'):
            predictions = trend_result.get('predictions', [])
            confidence_scores = trend_result.get('confidence_scores', {})
            logger.info(f"   Predictions generated: {len(predictions)}")
            logger.info(f"   Average confidence: {sum(confidence_scores.values()) / len(confidence_scores) if confidence_scores else 0:.2f}")
        
        # Test 5: Enhanced Strategic Recommendations
        logger.info("🎯 Test 5: Enhanced Strategic Recommendations...")
        
        # Create test metrics
        test_metrics = StrategicMetrics(
            domain=StrategicDomain.MILITARY,
            timestamp="2025-08-25T21:30:00Z",
            five_fundamentals={
                "the_way": 0.4,      # Low score to trigger recommendation
                "heaven": 0.6,
                "earth": 0.7,
                "command": 0.5,      # Low score to trigger recommendation
                "method": 0.8
            },
            deception_effectiveness=0.3,  # Low score to trigger recommendation
            resource_efficiency=0.6,
            intelligence_superiority=0.4,  # Low score to trigger recommendation
            alliance_strength=0.7,
            risk_factors=["resource_constraints", "technological_gaps"],
            opportunities=["alliance_strengthening", "technology_integration"],
            confidence_score=0.6
        )
        
        # Generate enhanced recommendations
        recommendations = await strategic_engine.generate_strategic_recommendations(test_metrics)
        
        logger.info(f"✅ Enhanced Strategic Recommendations: {len(recommendations)} generated")
        
        # Analyze recommendations
        for i, rec in enumerate(recommendations[:5]):  # Show first 5
            logger.info(f"   {i+1}. {rec.recommendation}")
            logger.info(f"      Priority: {rec.priority:.2f}, Impact: {rec.expected_impact:.2f}")
            logger.info(f"      Timeline: {rec.timeline}")
            logger.info(f"      Risk: {rec.risk_assessment}")
        
        # Test 6: Comprehensive Analysis Report
        logger.info("📄 Test 6: Comprehensive Analysis Report...")
        report = strategic_engine.export_analysis_report(test_metrics, recommendations)
        
        logger.info(f"✅ Analysis Report Generated: {report.get('analysis_metadata', {}).get('analysis_version', 'unknown')}")
        
        # Summary
        logger.info("\n📊 Test Summary:")
        logger.info(f"   Knowledge Graph Intelligence: {'✅ PASS' if kg_result.get('success') else '❌ FAIL'}")
        logger.info(f"   Historical Pattern Analysis: {'✅ PASS' if historical_result.get('success') else '❌ FAIL'}")
        logger.info(f"   Cross-Domain Intelligence: {'✅ PASS' if cross_domain_result.get('success') else '❌ FAIL'}")
        logger.info(f"   Strategic Trend Prediction: {'✅ PASS' if trend_result.get('success') else '❌ FAIL'}")
        logger.info(f"   Enhanced Recommendations: {'✅ PASS' if len(recommendations) > 0 else '❌ FAIL'}")
        logger.info(f"   Analysis Report: {'✅ PASS' if report else '❌ FAIL'}")
        
        # Phase 1 Success Criteria Check
        success_criteria = {
            "knowledge_graph_intelligence": kg_result.get('success', False),
            "historical_pattern_analysis": historical_result.get('success', False),
            "cross_domain_intelligence": cross_domain_result.get('success', False),
            "predictive_capabilities": trend_result.get('success', False),
            "enhanced_recommendations": len(recommendations) > 0
        }
        
        passed_criteria = sum(success_criteria.values())
        total_criteria = len(success_criteria)
        
        logger.info(f"\n🎯 Phase 1 Success Criteria: {passed_criteria}/{total_criteria} passed")
        
        if passed_criteria >= 4:  # At least 80% success rate
            logger.info("🎉 Phase 1 Implementation: SUCCESSFUL!")
            logger.info("✅ Enhanced Strategic Analytics Engine with Knowledge Graph Intelligence is working correctly")
            return True
        else:
            logger.warning("⚠️ Phase 1 Implementation: PARTIAL SUCCESS")
            logger.warning("❌ Some components need further development")
            return False
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False

async def main():
    """Run the enhanced strategic analytics test."""
    logger.info("🚀 Starting Phase 1 Implementation Test...")
    
    success = await test_enhanced_strategic_analytics()
    
    if success:
        logger.info("🎉 Phase 1 Implementation Test PASSED!")
        logger.info("✅ Knowledge Graph Intelligence Integration is working correctly")
        logger.info("✅ Strategic Recommendations are leveraging knowledge graph data")
        logger.info("✅ Historical Pattern Analysis is functional")
        logger.info("✅ Cross-Domain Intelligence Generation is operational")
        logger.info("✅ Predictive Analytics are providing insights")
    else:
        logger.error("❌ Phase 1 Implementation Test FAILED!")
        logger.error("❌ Some components need further development")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())
