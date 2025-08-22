#!/usr/bin/env .venv/Scripts/python.exe
"""
Test script for Enhanced Report Generation System
Tests all 25+ analysis components and integration.
"""

import asyncio
import sys
import os
import time
from typing import Dict, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.models import (
    EnhancedReportRequest, ReportComponent, MonteCarloConfig,
    StressTestConfig, VisualizationConfig, KnowledgeGraphConfig
)
from core.enhanced_report_orchestrator import EnhancedReportOrchestrator


class EnhancedReportTester:
    """Test suite for enhanced report generation system."""
    
    def __init__(self):
        self.orchestrator = EnhancedReportOrchestrator()
        self.test_results = {}
        
    async def run_all_tests(self):
        """Run all tests for the enhanced report system."""
        print("🧪 Starting Enhanced Report Generation System Tests")
        print("=" * 60)
        
        tests = [
            ("Enhanced Report Orchestrator", self.test_orchestrator_initialization),
            ("Monte Carlo Engine", self.test_monte_carlo_engine),
            ("Stress Testing Engine", self.test_stress_testing_engine),
            ("Interactive Visualization Engine", self.test_visualization_engine),
            ("Knowledge Graph Analyzer", self.test_knowledge_graph_analyzer),
            ("Strategic Analyzer", self.test_strategic_analyzer),
            ("Anomaly Detector", self.test_anomaly_detector),
            ("Pattern Analyzer", self.test_pattern_analyzer),
            ("Risk Assessor", self.test_risk_assessor),
            ("Geopolitical Mapper", self.test_geopolitical_mapper),
            ("Audit Trail Service", self.test_audit_trail_service),
            ("Full Report Generation", self.test_full_report_generation),
            ("Component Integration", self.test_component_integration),
            ("Performance Testing", self.test_performance),
            ("Error Handling", self.test_error_handling)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            try:
                start_time = time.time()
                result = await test_func()
                end_time = time.time()
                
                if result:
                    print(f"✅ {test_name}: PASSED ({end_time - start_time:.2f}s)")
                    self.test_results[test_name] = {"status": "PASSED", "time": end_time - start_time}
                else:
                    print(f"❌ {test_name}: FAILED ({end_time - start_time:.2f}s)")
                    self.test_results[test_name] = {"status": "FAILED", "time": end_time - start_time}
                    
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {str(e)}")
                self.test_results[test_name] = {"status": "ERROR", "error": str(e)}
        
        self.print_test_summary()
    
    async def test_orchestrator_initialization(self) -> bool:
        """Test orchestrator initialization."""
        try:
            # Check if all engines are initialized
            assert self.orchestrator.monte_carlo_engine is not None
            assert self.orchestrator.stress_testing_engine is not None
            assert self.orchestrator.visualization_engine is not None
            assert self.orchestrator.knowledge_graph_analyzer is not None
            assert self.orchestrator.strategic_analyzer is not None
            assert self.orchestrator.anomaly_detector is not None
            assert self.orchestrator.pattern_analyzer is not None
            assert self.orchestrator.risk_assessor is not None
            assert self.orchestrator.geopolitical_mapper is not None
            assert self.orchestrator.audit_trail is not None
            
            return True
        except Exception as e:
            print(f"Orchestrator initialization failed: {e}")
            return False
    
    async def test_monte_carlo_engine(self) -> bool:
        """Test Monte Carlo engine."""
        try:
            config = MonteCarloConfig(
                iterations=1000,
                confidence_level=0.95,
                variables=["revenue", "cost", "profit"],
                distributions={"revenue": "normal", "cost": "lognormal"}
            )
            
            result = await self.orchestrator.monte_carlo_engine.run_simulation(config, "test_scenario")
            
            # Verify result structure
            assert result.scenario_name == "test_scenario"
            assert result.iterations == 1000
            assert result.mean_value > 0
            assert result.standard_deviation > 0
            assert "95%" in result.confidence_intervals
            
            return True
        except Exception as e:
            print(f"Monte Carlo engine test failed: {e}")
            return False
    
    async def test_stress_testing_engine(self) -> bool:
        """Test stress testing engine."""
        try:
            config = StressTestConfig(
                scenarios=["worst_case", "average_case", "best_case"],
                severity_levels=["low", "medium", "high"],
                time_periods=[1, 3, 6]
            )
            
            base_data = {
                "metrics": {"revenue": 1000000, "growth": 0.15},
                "trends": [0.1, 0.15, 0.2, 0.18, 0.25, 0.3]
            }
            
            results = await self.orchestrator.stress_testing_engine.run_stress_tests(config, base_data)
            
            # Verify results
            assert len(results) > 0
            for result in results:
                assert result.scenario in ["worst_case", "average_case", "best_case"]
                assert result.severity_level in ["low", "medium", "high"]
                assert result.time_period in [1, 3, 6]
                assert len(result.impact_scores) > 0
            
            return True
        except Exception as e:
            print(f"Stress testing engine test failed: {e}")
            return False
    
    async def test_visualization_engine(self) -> bool:
        """Test visualization engine."""
        try:
            config = VisualizationConfig(
                chart_types=["line", "bar", "scatter"],
                interactive=True,
                drill_down_enabled=True
            )
            
            data = {
                "trends": [0.1, 0.15, 0.2, 0.18, 0.25, 0.3],
                "comparisons": {"baseline": 100, "current": 120, "target": 150},
                "correlations": [[1.0, 0.8, 0.6], [0.8, 1.0, 0.7], [0.6, 0.7, 1.0]]
            }
            
            result = await self.orchestrator.visualization_engine.generate_visualizations(config, data)
            
            # Verify result structure
            assert result.chart_data is not None
            assert len(result.drill_down_options) > 0
            assert len(result.interactive_features) > 0
            assert len(result.mermaid_diagrams) > 0
            
            return True
        except Exception as e:
            print(f"Visualization engine test failed: {e}")
            return False
    
    async def test_knowledge_graph_analyzer(self) -> bool:
        """Test knowledge graph analyzer."""
        try:
            config = KnowledgeGraphConfig(
                max_nodes=100,
                max_relationships=500,
                include_metadata=True
            )
            
            data = {
                "entities": ["Company A", "Company B", "Market X"],
                "relationships": [("Company A", "employs", "John Doe")]
            }
            
            result = await self.orchestrator.knowledge_graph_analyzer.analyze_knowledge_graph(config, data)
            
            # Verify result structure
            assert len(result.nodes) > 0
            assert len(result.relationships) > 0
            assert len(result.centrality_scores) > 0
            assert len(result.key_entities) > 0
            
            return True
        except Exception as e:
            print(f"Knowledge graph analyzer test failed: {e}")
            return False
    
    async def test_strategic_analyzer(self) -> bool:
        """Test strategic analyzer."""
        try:
            data = {
                "query": "market analysis",
                "entities": ["Company A", "Competitor B"],
                "metrics": {"market_share": 0.25, "growth_rate": 0.15}
            }
            
            result = await self.orchestrator.strategic_analyzer.analyze_strategic_position(data)
            
            # Verify result structure
            assert "geopolitical_risks" in result
            assert "competitive_advantages" in result
            assert "strategic_vulnerabilities" in result
            assert "strategic_metrics" in result
            
            return True
        except Exception as e:
            print(f"Strategic analyzer test failed: {e}")
            return False
    
    async def test_anomaly_detector(self) -> bool:
        """Test anomaly detector."""
        try:
            data = {
                "metrics": [100, 110, 120, 130, 140, 150, 200],  # Anomaly at the end
                "timestamps": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-06", "2024-01-07"]
            }
            
            anomalies = await self.orchestrator.anomaly_detector.detect_anomalies(data)
            
            # Verify result structure
            assert isinstance(anomalies, list)
            for anomaly in anomalies:
                assert "type" in anomaly
                assert "severity" in anomaly
                assert "description" in anomaly
            
            return True
        except Exception as e:
            print(f"Anomaly detector test failed: {e}")
            return False
    
    async def test_pattern_analyzer(self) -> bool:
        """Test pattern analyzer."""
        try:
            data = {
                "time_series": [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
                "categories": ["Q1", "Q2", "Q3", "Q4"] * 3
            }
            
            patterns = await self.orchestrator.pattern_analyzer.analyze_patterns(data)
            
            # Verify result structure
            assert isinstance(patterns, list)
            for pattern in patterns:
                assert "type" in pattern
                assert "pattern" in pattern
                assert "confidence" in pattern
            
            return True
        except Exception as e:
            print(f"Pattern analyzer test failed: {e}")
            return False
    
    async def test_risk_assessor(self) -> bool:
        """Test risk assessor."""
        try:
            data = {
                "risk_categories": ["financial", "operational", "strategic"],
                "metrics": {"revenue": 1000000, "growth": 0.15}
            }
            
            result = await self.orchestrator.risk_assessor.assess_risks(data)
            
            # Verify result structure
            assert len(result.risk_categories) > 0
            assert len(result.likelihood_scores) > 0
            assert len(result.impact_scores) > 0
            assert len(result.risk_scores) > 0
            assert len(result.mitigation_priorities) > 0
            
            return True
        except Exception as e:
            print(f"Risk assessor test failed: {e}")
            return False
    
    async def test_geopolitical_mapper(self) -> bool:
        """Test geopolitical mapper."""
        try:
            data = {
                "regions": ["north_america", "europe", "asia_pacific"],
                "analysis_frameworks": ["swot", "pestle"]
            }
            
            result = await self.orchestrator.geopolitical_mapper.create_geopolitical_map(data)
            
            # Verify result structure
            assert "regions" in result
            assert "global_trends" in result
            assert "key_risks" in result
            
            return True
        except Exception as e:
            print(f"Geopolitical mapper test failed: {e}")
            return False
    
    async def test_audit_trail_service(self) -> bool:
        """Test audit trail service."""
        try:
            # Test logging activity
            await self.orchestrator.audit_trail.log_activity(
                user_id="test_user",
                action="test_action",
                details={"test": "data"}
            )
            
            # Verify audit log has entries
            assert len(self.orchestrator.audit_trail.audit_log) > 0
            
            latest_entry = self.orchestrator.audit_trail.audit_log[-1]
            assert latest_entry["user_id"] == "test_user"
            assert latest_entry["action"] == "test_action"
            assert "timestamp" in latest_entry
            
            return True
        except Exception as e:
            print(f"Audit trail service test failed: {e}")
            return False
    
    async def test_full_report_generation(self) -> bool:
        """Test full report generation with all components."""
        try:
            request = EnhancedReportRequest(
                query="Comprehensive market analysis for technology sector",
                components=[
                    ReportComponent.EXECUTIVE_SUMMARY,
                    ReportComponent.COMPARATIVE_ANALYSIS,
                    ReportComponent.IMPACT_ANALYSIS,
                    ReportComponent.PREDICTIVE_ANALYSIS,
                    ReportComponent.MONTE_CARLO_SIMULATION,
                    ReportComponent.STRESS_TESTING,
                    ReportComponent.RISK_ASSESSMENT,
                    ReportComponent.KNOWLEDGE_GRAPH,
                    ReportComponent.INTERACTIVE_VISUALIZATIONS
                ],
                export_formats=["pdf", "excel"],
                language="en"
            )
            
            result = await self.orchestrator.generate_report(request)
            
            # Verify result structure
            assert result.status.value == "completed"
            assert result.processing_time > 0
            assert len(result.components_generated) > 0
            assert result.success is True
            
            # Verify components were generated
            assert result.executive_summary is not None
            assert result.comparative_analysis is not None
            assert result.impact_analysis is not None
            assert result.predictive_analysis is not None
            assert len(result.monte_carlo_results) > 0
            assert len(result.stress_test_results) > 0
            assert result.risk_assessment_matrix is not None
            assert result.knowledge_graph_result is not None
            assert result.visualization_result is not None
            
            return True
        except Exception as e:
            print(f"Full report generation test failed: {e}")
            return False
    
    async def test_component_integration(self) -> bool:
        """Test component integration."""
        try:
            # Test that components can work together
            base_data = await self.orchestrator._generate_base_data(
                EnhancedReportRequest(query="test", components=[])
            )
            
            # Test executive summary generation
            exec_summary = await self.orchestrator._generate_executive_summary(
                EnhancedReportRequest(query="test", components=[]), base_data
            )
            assert exec_summary is not None
            
            # Test comparative analysis generation
            comp_analysis = await self.orchestrator._generate_comparative_analysis(
                EnhancedReportRequest(query="test", components=[]), base_data
            )
            assert comp_analysis is not None
            
            # Test impact analysis generation
            impact_analysis = await self.orchestrator._generate_impact_analysis(
                EnhancedReportRequest(query="test", components=[]), base_data
            )
            assert impact_analysis is not None
            
            return True
        except Exception as e:
            print(f"Component integration test failed: {e}")
            return False
    
    async def test_performance(self) -> bool:
        """Test performance requirements."""
        try:
            # Test that report generation completes within 30 seconds
            start_time = time.time()
            
            request = EnhancedReportRequest(
                query="Performance test",
                components=[
                    ReportComponent.EXECUTIVE_SUMMARY,
                    ReportComponent.COMPARATIVE_ANALYSIS,
                    ReportComponent.IMPACT_ANALYSIS
                ]
            )
            
            result = await self.orchestrator.generate_report(request)
            end_time = time.time()
            
            processing_time = end_time - start_time
            
            # Should complete within 30 seconds
            assert processing_time < 30, f"Report generation took {processing_time:.2f}s, expected < 30s"
            
            # Should have reasonable processing time
            assert result.processing_time > 0
            assert result.processing_time < 30
            
            return True
        except Exception as e:
            print(f"Performance test failed: {e}")
            return False
    
    async def test_error_handling(self) -> bool:
        """Test error handling."""
        try:
            # Test with invalid component
            request = EnhancedReportRequest(
                query="Error test",
                components=["invalid_component"]  # This should be handled gracefully
            )
            
            result = await self.orchestrator.generate_report(request)
            
            # Should still complete successfully
            assert result.success is True
            assert result.status.value == "completed"
            
            return True
        except Exception as e:
            print(f"Error handling test failed: {e}")
            return False
    
    def print_test_summary(self):
        """Print test summary."""
        print("\n" + "=" * 60)
        print("📊 ENHANCED REPORT SYSTEM TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result["status"] == "PASSED")
        failed_tests = sum(1 for result in self.test_results.values() if result["status"] == "FAILED")
        error_tests = sum(1 for result in self.test_results.values() if result["status"] == "ERROR")
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️ Errors: {error_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0 or error_tests > 0:
            print("\n🔍 Failed/Error Details:")
            for test_name, result in self.test_results.items():
                if result["status"] != "PASSED":
                    print(f"  - {test_name}: {result['status']}")
                    if "error" in result:
                        print(f"    Error: {result['error']}")
        
        print("\n" + "=" * 60)
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED! Enhanced Report System is ready.")
        else:
            print("⚠️ Some tests failed. Please review the errors above.")


async def main():
    """Main test function."""
    tester = EnhancedReportTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
