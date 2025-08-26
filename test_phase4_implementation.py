#!/usr/bin/env python3
"""
Phase 4 Implementation Test Suite
Comprehensive testing for Phase 4 Strategic Recommendations Integration.
Tests all Phase 4 components and their integration capabilities.
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from loguru import logger

# Import Phase 4 components
try:
    from src.core.strategic_intelligence_engine import StrategicIntelligenceEngine
    from src.core.enhanced_strategic_recommendations import EnhancedStrategicRecommendations
    from src.core.strategic_analytics_dashboard import StrategicAnalyticsDashboard, AlertConfig, AlertLevel
    PHASE4_COMPONENTS_AVAILABLE = True
    logger.info("✅ Phase 4 components imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import Phase 4 components: {e}")
    PHASE4_COMPONENTS_AVAILABLE = False

# Import API routes
try:
    from src.api.phase4_strategic_routes import router as phase4_router
    API_ROUTES_AVAILABLE = True
    logger.info("✅ Phase 4 API routes imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import Phase 4 API routes: {e}")
    API_ROUTES_AVAILABLE = False


class Phase4TestSuite:
    """Comprehensive test suite for Phase 4 implementation."""
    
    def __init__(self):
        """Initialize the test suite."""
        self.test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": []
        }
        
        # Initialize Phase 4 components
        if PHASE4_COMPONENTS_AVAILABLE:
            try:
                self.strategic_intelligence_engine = StrategicIntelligenceEngine()
                self.enhanced_recommendations = EnhancedStrategicRecommendations()
                self.strategic_dashboard = StrategicAnalyticsDashboard()
                logger.info("✅ Phase 4 components initialized for testing")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Phase 4 components: {e}")
                self.strategic_intelligence_engine = None
                self.enhanced_recommendations = None
                self.strategic_dashboard = None
        else:
            self.strategic_intelligence_engine = None
            self.enhanced_recommendations = None
            self.strategic_dashboard = None

    async def run_all_tests(self):
        """Run all Phase 4 tests."""
        logger.info("🚀 Starting Phase 4 Implementation Test Suite")
        logger.info("=" * 60)
        
        # Test Phase 4 Task 4.1: Knowledge Graph Intelligence Integration
        await self.test_task_4_1_knowledge_graph_intelligence()
        
        # Test Phase 4 Task 4.2: Enhanced Strategic Recommendations
        await self.test_task_4_2_enhanced_strategic_recommendations()
        
        # Test Phase 4 Task 4.3: Strategic Analytics Dashboard
        await self.test_task_4_3_strategic_analytics_dashboard()
        
        # Test Phase 4 Integration
        await self.test_phase4_integration()
        
        # Test API Routes
        await self.test_api_routes()
        
        # Generate test report
        await self.generate_test_report()

    async def test_task_4_1_knowledge_graph_intelligence(self):
        """Test Phase 4 Task 4.1: Knowledge Graph Intelligence Integration."""
        logger.info("📋 Testing Task 4.1: Knowledge Graph Intelligence Integration")
        
        if not self.strategic_intelligence_engine:
            await self.record_test_result("Task 4.1 - Component Availability", False, "Strategic intelligence engine not available")
            return
        
        # Test 4.1.1: Query knowledge graph for strategic intelligence
        await self.test_knowledge_graph_query()
        
        # Test 4.1.2: Analyze historical patterns
        await self.test_historical_pattern_analysis()
        
        # Test 4.1.3: Generate cross-domain intelligence
        await self.test_cross_domain_intelligence()
        
        # Test 4.1.4: Predict strategic trends
        await self.test_strategic_trend_prediction()
        
        # Test 4.1.5: Assess strategic risks from knowledge graph
        await self.test_strategic_risk_assessment()
        
        # Test 4.1.6: Identify strategic opportunities
        await self.test_strategic_opportunity_identification()

    async def test_task_4_2_enhanced_strategic_recommendations(self):
        """Test Phase 4 Task 4.2: Enhanced Strategic Recommendations."""
        logger.info("📋 Testing Task 4.2: Enhanced Strategic Recommendations")
        
        if not self.enhanced_recommendations:
            await self.record_test_result("Task 4.2 - Component Availability", False, "Enhanced recommendations not available")
            return
        
        # Test 4.2.1: Generate intelligence-driven recommendations
        await self.test_intelligence_driven_recommendations()
        
        # Test 4.2.2: Generate multi-domain recommendations
        await self.test_multi_domain_recommendations()
        
        # Test 4.2.3: Adjust recommendations by risk
        await self.test_risk_adjusted_recommendations()
        
        # Test 4.2.4: Weight recommendations by confidence
        await self.test_confidence_weighted_recommendations()
        
        # Test 4.2.5: Generate temporal recommendations
        await self.test_temporal_recommendations()
        
        # Test 4.2.6: Generate scenario-based recommendations
        await self.test_scenario_based_recommendations()

    async def test_task_4_3_strategic_analytics_dashboard(self):
        """Test Phase 4 Task 4.3: Strategic Analytics Dashboard."""
        logger.info("📋 Testing Task 4.3: Strategic Analytics Dashboard")
        
        if not self.strategic_dashboard:
            await self.record_test_result("Task 4.3 - Component Availability", False, "Strategic dashboard not available")
            return
        
        # Test 4.3.1: Get strategic metrics
        await self.test_strategic_metrics()
        
        # Test 4.3.2: Track recommendations
        await self.test_recommendation_tracking()
        
        # Test 4.3.3: Monitor risks
        await self.test_risk_monitoring()
        
        # Test 4.3.4: Track opportunities
        await self.test_opportunity_tracking()
        
        # Test 4.3.5: Analyze performance
        await self.test_performance_analysis()
        
        # Test 4.3.6: Setup alerts
        await self.test_alert_setup()
        
        # Test 4.3.7: Get dashboard summary
        await self.test_dashboard_summary()

    async def test_phase4_integration(self):
        """Test Phase 4 integration capabilities."""
        logger.info("📋 Testing Phase 4 Integration")
        
        # Test integration between components
        await self.test_component_integration()
        
        # Test end-to-end workflows
        await self.test_end_to_end_workflows()

    async def test_api_routes(self):
        """Test Phase 4 API routes."""
        logger.info("📋 Testing Phase 4 API Routes")
        
        if not API_ROUTES_AVAILABLE:
            await self.record_test_result("API Routes - Availability", False, "API routes not available")
            return
        
        # Test API route availability
        await self.test_api_route_availability()

    # Task 4.1 Test Methods
    
    async def test_knowledge_graph_query(self):
        """Test knowledge graph query for strategic intelligence."""
        try:
            result = await self.strategic_intelligence_engine.query_knowledge_graph_for_intelligence(
                "strategic market analysis", "business"
            )
            
            success = result.get("success", False)
            await self.record_test_result(
                "Task 4.1.1 - Knowledge Graph Query",
                success,
                f"Query result: {result.get('error', 'Success')}"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.1.1 - Knowledge Graph Query",
                False,
                f"Exception: {str(e)}"
            )

    async def test_historical_pattern_analysis(self):
        """Test historical pattern analysis."""
        try:
            result = await self.strategic_intelligence_engine.analyze_historical_patterns(
                "market expansion", "12 months"
            )
            
            success = result.get("success", False)
            await self.record_test_result(
                "Task 4.1.2 - Historical Pattern Analysis",
                success,
                f"Analysis result: {result.get('error', 'Success')}"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.1.2 - Historical Pattern Analysis",
                False,
                f"Exception: {str(e)}"
            )

    async def test_cross_domain_intelligence(self):
        """Test cross-domain intelligence generation."""
        try:
            result = await self.strategic_intelligence_engine.generate_cross_domain_intelligence(
                ["business", "technology", "finance"]
            )
            
            success = result.get("success", False)
            await self.record_test_result(
                "Task 4.1.3 - Cross-Domain Intelligence",
                success,
                f"Cross-domain result: {result.get('error', 'Success')}"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.1.3 - Cross-Domain Intelligence",
                False,
                f"Exception: {str(e)}"
            )

    async def test_strategic_trend_prediction(self):
        """Test strategic trend prediction."""
        try:
            result = await self.strategic_intelligence_engine.predict_strategic_trends(
                "market growth in technology sector"
            )
            
            success = result.get("success", False)
            await self.record_test_result(
                "Task 4.1.4 - Strategic Trend Prediction",
                success,
                f"Prediction result: {result.get('error', 'Success')}"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.1.4 - Strategic Trend Prediction",
                False,
                f"Exception: {str(e)}"
            )

    async def test_strategic_risk_assessment(self):
        """Test strategic risk assessment."""
        try:
            result = await self.strategic_intelligence_engine.assess_strategic_risks_from_kg(
                "market entry in competitive environment"
            )
            
            success = result.get("success", False)
            await self.record_test_result(
                "Task 4.1.5 - Strategic Risk Assessment",
                success,
                f"Risk assessment result: {result.get('error', 'Success')}"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.1.5 - Strategic Risk Assessment",
                False,
                f"Exception: {str(e)}"
            )

    async def test_strategic_opportunity_identification(self):
        """Test strategic opportunity identification."""
        try:
            result = await self.strategic_intelligence_engine.identify_strategic_opportunities(
                "emerging market opportunities"
            )
            
            success = result.get("success", False)
            await self.record_test_result(
                "Task 4.1.6 - Strategic Opportunity Identification",
                success,
                f"Opportunity identification result: {result.get('error', 'Success')}"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.1.6 - Strategic Opportunity Identification",
                False,
                f"Exception: {str(e)}"
            )

    # Task 4.2 Test Methods
    
    async def test_intelligence_driven_recommendations(self):
        """Test intelligence-driven recommendations."""
        try:
            result = await self.enhanced_recommendations.generate_intelligence_driven_recommendations(
                "strategic business expansion"
            )
            
            success = isinstance(result, list)
            await self.record_test_result(
                "Task 4.2.1 - Intelligence-Driven Recommendations",
                success,
                f"Generated {len(result)} recommendations"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.2.1 - Intelligence-Driven Recommendations",
                False,
                f"Exception: {str(e)}"
            )

    async def test_multi_domain_recommendations(self):
        """Test multi-domain recommendations."""
        try:
            result = await self.enhanced_recommendations.generate_multi_domain_recommendations(
                ["business", "technology"]
            )
            
            success = isinstance(result, list)
            await self.record_test_result(
                "Task 4.2.2 - Multi-Domain Recommendations",
                success,
                f"Generated {len(result)} multi-domain recommendations"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.2.2 - Multi-Domain Recommendations",
                False,
                f"Exception: {str(e)}"
            )

    async def test_risk_adjusted_recommendations(self):
        """Test risk-adjusted recommendations."""
        try:
            # Create sample recommendations
            sample_recommendations = [
                {"title": "Market Expansion", "priority": "high", "description": "Expand to new markets"}
            ]
            risk_assessment = {"overall_risk": 0.6, "market_risk": 0.7}
            
            result = await self.enhanced_recommendations.adjust_recommendations_by_risk(
                sample_recommendations, risk_assessment
            )
            
            success = isinstance(result, list)
            await self.record_test_result(
                "Task 4.2.3 - Risk-Adjusted Recommendations",
                success,
                f"Generated {len(result)} risk-adjusted recommendations"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.2.3 - Risk-Adjusted Recommendations",
                False,
                f"Exception: {str(e)}"
            )

    async def test_confidence_weighted_recommendations(self):
        """Test confidence-weighted recommendations."""
        try:
            # Create sample recommendations
            sample_recommendations = [
                {"title": "Technology Investment", "priority": "medium", "description": "Invest in new technology"}
            ]
            
            result = await self.enhanced_recommendations.weight_recommendations_by_confidence(
                sample_recommendations
            )
            
            success = isinstance(result, list)
            await self.record_test_result(
                "Task 4.2.4 - Confidence-Weighted Recommendations",
                success,
                f"Generated {len(result)} confidence-weighted recommendations"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.2.4 - Confidence-Weighted Recommendations",
                False,
                f"Exception: {str(e)}"
            )

    async def test_temporal_recommendations(self):
        """Test temporal recommendations."""
        try:
            result = await self.enhanced_recommendations.generate_temporal_recommendations(
                "market timing analysis", "6 months"
            )
            
            success = isinstance(result, list)
            await self.record_test_result(
                "Task 4.2.5 - Temporal Recommendations",
                success,
                f"Generated {len(result)} temporal recommendations"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.2.5 - Temporal Recommendations",
                False,
                f"Exception: {str(e)}"
            )

    async def test_scenario_based_recommendations(self):
        """Test scenario-based recommendations."""
        try:
            result = await self.enhanced_recommendations.generate_scenario_recommendations(
                ["optimistic", "baseline", "pessimistic"]
            )
            
            success = isinstance(result, dict)
            await self.record_test_result(
                "Task 4.2.6 - Scenario-Based Recommendations",
                success,
                f"Generated recommendations for {len(result)} scenarios"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.2.6 - Scenario-Based Recommendations",
                False,
                f"Exception: {str(e)}"
            )

    # Task 4.3 Test Methods
    
    async def test_strategic_metrics(self):
        """Test strategic metrics dashboard."""
        try:
            result = await self.strategic_dashboard.get_strategic_metrics()
            
            success = isinstance(result, dict) and "error" not in result
            await self.record_test_result(
                "Task 4.3.1 - Strategic Metrics",
                success,
                f"Retrieved {len(result)} metric categories"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.3.1 - Strategic Metrics",
                False,
                f"Exception: {str(e)}"
            )

    async def test_recommendation_tracking(self):
        """Test recommendation tracking."""
        try:
            sample_recommendations = [
                {"title": "Strategic Initiative A", "description": "Implement new strategy"}
            ]
            
            result = await self.strategic_dashboard.track_recommendations(sample_recommendations)
            
            success = isinstance(result, dict)
            await self.record_test_result(
                "Task 4.3.2 - Recommendation Tracking",
                success,
                f"Tracking {len(result)} recommendations"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.3.2 - Recommendation Tracking",
                False,
                f"Exception: {str(e)}"
            )

    async def test_risk_monitoring(self):
        """Test risk monitoring."""
        try:
            risk_assessment = {
                "risk_factors": [
                    {"factor": "Market volatility", "level": "medium", "score": 0.6}
                ]
            }
            
            result = await self.strategic_dashboard.monitor_risks(risk_assessment)
            
            success = isinstance(result, dict)
            await self.record_test_result(
                "Task 4.3.3 - Risk Monitoring",
                success,
                f"Monitoring {len(result)} risks"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.3.3 - Risk Monitoring",
                False,
                f"Exception: {str(e)}"
            )

    async def test_opportunity_tracking(self):
        """Test opportunity tracking."""
        try:
            opportunities = [
                {"opportunity": "Market expansion", "probability": 0.8, "impact_score": 0.9}
            ]
            
            result = await self.strategic_dashboard.track_opportunities(opportunities)
            
            success = isinstance(result, dict)
            await self.record_test_result(
                "Task 4.3.4 - Opportunity Tracking",
                success,
                f"Tracking {len(result)} opportunities"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.3.4 - Opportunity Tracking",
                False,
                f"Exception: {str(e)}"
            )

    async def test_performance_analysis(self):
        """Test performance analysis."""
        try:
            initiatives = [
                {"name": "Digital Transformation", "description": "Implement digital solutions"}
            ]
            
            result = await self.strategic_dashboard.analyze_performance(initiatives)
            
            success = isinstance(result, dict)
            await self.record_test_result(
                "Task 4.3.5 - Performance Analysis",
                success,
                f"Analyzed {len(result)} initiatives"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.3.5 - Performance Analysis",
                False,
                f"Exception: {str(e)}"
            )

    async def test_alert_setup(self):
        """Test alert setup."""
        try:
            import uuid
            alert_config = AlertConfig(
                alert_id=str(uuid.uuid4()),
                alert_name="Test Alert",
                alert_level=AlertLevel.WARNING,
                trigger_conditions={"threshold": 0.8},
                notification_channels=["email"],
                escalation_rules={},
                auto_resolve=True,
                enabled=True,
                created_date=datetime.now()
            )
            
            result = await self.strategic_dashboard.setup_alerts(alert_config)
            
            success = result.get("success", False)
            await self.record_test_result(
                "Task 4.3.6 - Alert Setup",
                success,
                f"Alert setup result: {result.get('error', 'Success')}"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.3.6 - Alert Setup",
                False,
                f"Exception: {str(e)}"
            )

    async def test_dashboard_summary(self):
        """Test dashboard summary."""
        try:
            result = await self.strategic_dashboard.get_dashboard_summary()
            
            success = hasattr(result, 'total_metrics')
            await self.record_test_result(
                "Task 4.3.7 - Dashboard Summary",
                success,
                f"Dashboard summary generated with {result.total_metrics} metrics"
            )
        except Exception as e:
            await self.record_test_result(
                "Task 4.3.7 - Dashboard Summary",
                False,
                f"Exception: {str(e)}"
            )

    # Integration Test Methods
    
    async def test_component_integration(self):
        """Test integration between Phase 4 components."""
        try:
            # Test integration between strategic intelligence engine and enhanced recommendations
            kg_result = await self.strategic_intelligence_engine.query_knowledge_graph_for_intelligence(
                "integration test", "business"
            )
            
            if kg_result.get("success"):
                recommendations = await self.enhanced_recommendations.generate_intelligence_driven_recommendations(
                    "integration test"
                )
                
                success = isinstance(recommendations, list)
                await self.record_test_result(
                    "Integration - Components Integration",
                    success,
                    f"Generated {len(recommendations)} recommendations from KG intelligence"
                )
            else:
                await self.record_test_result(
                    "Integration - Components Integration",
                    False,
                    "Knowledge graph query failed"
                )
        except Exception as e:
            await self.record_test_result(
                "Integration - Components Integration",
                False,
                f"Exception: {str(e)}"
            )

    async def test_end_to_end_workflows(self):
        """Test end-to-end workflows."""
        try:
            # Test complete workflow: KG query -> recommendations -> dashboard tracking
            kg_result = await self.strategic_intelligence_engine.query_knowledge_graph_for_intelligence(
                "workflow test", "business"
            )
            
            if kg_result.get("success"):
                recommendations = await self.enhanced_recommendations.generate_intelligence_driven_recommendations(
                    "workflow test"
                )
                
                if recommendations:
                    tracking_result = await self.strategic_dashboard.track_recommendations(recommendations)
                    
                    success = isinstance(tracking_result, dict)
                    await self.record_test_result(
                        "Integration - End-to-End Workflow",
                        success,
                        f"Completed workflow with {len(tracking_result)} tracked recommendations"
                    )
                else:
                    await self.record_test_result(
                        "Integration - End-to-End Workflow",
                        False,
                        "No recommendations generated"
                    )
            else:
                await self.record_test_result(
                    "Integration - End-to-End Workflow",
                    False,
                    "Knowledge graph query failed"
                )
        except Exception as e:
            await self.record_test_result(
                "Integration - End-to-End Workflow",
                False,
                f"Exception: {str(e)}"
            )

    async def test_api_route_availability(self):
        """Test API route availability."""
        try:
            # Check if router has the expected routes
            routes = [route for route in phase4_router.routes]
            
            success = len(routes) > 0
            await self.record_test_result(
                "API Routes - Availability",
                success,
                f"Found {len(routes)} API routes"
            )
        except Exception as e:
            await self.record_test_result(
                "API Routes - Availability",
                False,
                f"Exception: {str(e)}"
            )

    # Utility Methods
    
    async def record_test_result(self, test_name: str, passed: bool, details: str):
        """Record a test result."""
        self.test_results["total_tests"] += 1
        
        if passed:
            self.test_results["passed_tests"] += 1
            logger.info(f"✅ {test_name}: PASSED - {details}")
        else:
            self.test_results["failed_tests"] += 1
            logger.error(f"❌ {test_name}: FAILED - {details}")
        
        self.test_results["test_details"].append({
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

    async def generate_test_report(self):
        """Generate comprehensive test report."""
        logger.info("=" * 60)
        logger.info("📊 PHASE 4 IMPLEMENTATION TEST REPORT")
        logger.info("=" * 60)
        
        total = self.test_results["total_tests"]
        passed = self.test_results["passed_tests"]
        failed = self.test_results["failed_tests"]
        
        logger.info(f"Total Tests: {total}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "N/A")
        
        # Phase 4 Success Criteria Check
        phase4_success_criteria = [
            "Task 4.1.1 - Knowledge Graph Query",
            "Task 4.1.2 - Historical Pattern Analysis", 
            "Task 4.1.3 - Cross-Domain Intelligence",
            "Task 4.1.4 - Strategic Trend Prediction",
            "Task 4.1.5 - Strategic Risk Assessment",
            "Task 4.1.6 - Strategic Opportunity Identification",
            "Task 4.2.1 - Intelligence-Driven Recommendations",
            "Task 4.2.2 - Multi-Domain Recommendations",
            "Task 4.2.3 - Risk-Adjusted Recommendations",
            "Task 4.2.4 - Confidence-Weighted Recommendations",
            "Task 4.2.5 - Temporal Recommendations",
            "Task 4.2.6 - Scenario-Based Recommendations",
            "Task 4.3.1 - Strategic Metrics",
            "Task 4.3.2 - Recommendation Tracking",
            "Task 4.3.3 - Risk Monitoring",
            "Task 4.3.4 - Opportunity Tracking",
            "Task 4.3.5 - Performance Analysis",
            "Task 4.3.6 - Alert Setup",
            "Task 4.3.7 - Dashboard Summary"
        ]
        
        passed_criteria = 0
        for criterion in phase4_success_criteria:
            for test_detail in self.test_results["test_details"]:
                if test_detail["test_name"] == criterion and test_detail["passed"]:
                    passed_criteria += 1
                    break
        
        logger.info(f"Phase 4 Success Criteria Met: {passed_criteria}/{len(phase4_success_criteria)}")
        
        if passed_criteria >= len(phase4_success_criteria) * 0.8:  # 80% threshold
            logger.info("🎉 PHASE 4 IMPLEMENTATION: SUCCESS")
            logger.info("✅ All major Phase 4 capabilities are functional")
        else:
            logger.warning("⚠️ PHASE 4 IMPLEMENTATION: PARTIAL SUCCESS")
            logger.warning("Some Phase 4 capabilities need attention")
        
        # Save detailed report
        report_file = Path("Results/phase4_implementation_test_report.json")
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        logger.info(f"📄 Detailed test report saved to: {report_file}")
        
        return self.test_results


async def main():
    """Main test execution function."""
    logger.info("🚀 Starting Phase 4 Implementation Test Suite")
    
    test_suite = Phase4TestSuite()
    results = await test_suite.run_all_tests()
    
    logger.info("🏁 Phase 4 Implementation Test Suite completed")
    return results


if __name__ == "__main__":
    asyncio.run(main())
