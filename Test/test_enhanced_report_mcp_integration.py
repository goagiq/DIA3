#!/usr/bin/env .venv/Scripts/python.exe
"""
Test Enhanced Report MCP Integration
Verifies that enhanced report tools are properly integrated with MCP server.
"""

import asyncio
import sys
import os
import time
from typing import Dict, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.models import EnhancedReportRequest
from core.enhanced_report_orchestrator import EnhancedReportOrchestrator
from mcp_servers.enhanced_report_mcp_tools import EnhancedReportMCPTools


class EnhancedReportMCPIntegrationTester:
    """Test suite for enhanced report MCP integration."""
    
    def __init__(self):
        self.orchestrator = EnhancedReportOrchestrator()
        self.mcp_tools = EnhancedReportMCPTools()
        
    async def run_integration_tests(self):
        """Run all MCP integration tests."""
        print("🧪 Testing Enhanced Report MCP Integration")
        print("=" * 50)
        
        tests = [
            ("MCP Tools Registration", self.test_mcp_tools_registration),
            ("Enhanced Report Generation", self.test_enhanced_report_generation),
            ("Monte Carlo Simulation", self.test_monte_carlo_simulation),
            ("Stress Testing", self.test_stress_testing),
            ("Knowledge Graph Analysis", self.test_knowledge_graph_analysis),
            ("Visualization Generation", self.test_visualization_generation),
            ("Anomaly Detection", self.test_anomaly_detection),
            ("Pattern Analysis", self.test_pattern_analysis),
            ("Risk Assessment", self.test_risk_assessment),
            ("Geopolitical Mapping", self.test_geopolitical_mapping)
        ]
        
        results = {}
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            try:
                start_time = time.time()
                result = await test_func()
                end_time = time.time()
                
                if result:
                    print(f"✅ {test_name}: PASSED ({end_time - start_time:.2f}s)")
                    results[test_name] = {"status": "PASSED", "time": end_time - start_time}
                else:
                    print(f"❌ {test_name}: FAILED ({end_time - start_time:.2f}s)")
                    results[test_name] = {"status": "FAILED", "time": end_time - start_time}
                    
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {str(e)}")
                results[test_name] = {"status": "ERROR", "error": str(e)}
        
        self.print_summary(results)
    
    async def test_mcp_tools_registration(self) -> bool:
        """Test that MCP tools are properly registered."""
        try:
            tools = self.mcp_tools.get_tools()
            
            # Check that all expected tools are registered
            expected_tools = [
                "generate_enhanced_report",
                "run_monte_carlo_simulation",
                "run_stress_testing",
                "generate_knowledge_graph",
                "generate_visualizations",
                "detect_anomalies",
                "analyze_patterns",
                "assess_risks",
                "create_geopolitical_map"
            ]
            
            tool_names = [tool["name"] for tool in tools]
            
            for expected_tool in expected_tools:
                if expected_tool not in tool_names:
                    print(f"Missing tool: {expected_tool}")
                    return False
            
            print(f"✅ All {len(expected_tools)} expected tools are registered")
            return True
            
        except Exception as e:
            print(f"MCP tools registration test failed: {e}")
            return False
    
    async def test_enhanced_report_generation(self) -> bool:
        """Test enhanced report generation through MCP tools."""
        try:
            # Test the enhanced report generation
            arguments = {
                "query": "MCP integration test query",
                "components": ["executive_summary", "monte_carlo_simulation"],
                "include_monte_carlo": True,
                "include_visualizations": True
            }
            
            result = await self.mcp_tools._generate_enhanced_report(arguments)
            
            # Check that the result is valid
            assert result.get("success", False), "Report generation failed"
            assert "report_id" in result or "id" in result, "No report ID returned"
            
            print(f"✅ Enhanced report generated successfully: {result.get('report_id', result.get('id', 'N/A'))}")
            return True
            
        except Exception as e:
            print(f"Enhanced report generation test failed: {e}")
            return False
    
    async def test_monte_carlo_simulation(self) -> bool:
        """Test Monte Carlo simulation through MCP tools."""
        try:
            # Test Monte Carlo simulation
            arguments = {
                "scenario_name": "MCP integration test",
                "iterations": 100,
                "confidence_level": 0.95,
                "variables": ["revenue", "cost"],
                "distributions": {"revenue": "normal", "cost": "lognormal"}
            }
            
            result = await self.mcp_tools._run_monte_carlo_simulation(arguments)
            
            # Check that the result is valid
            assert result.get("success", False), "Monte Carlo simulation failed"
            assert "simulation_id" in result or "id" in result, "No simulation ID returned"
            
            print(f"✅ Monte Carlo simulation completed successfully: {result.get('simulation_id', result.get('id', 'N/A'))}")
            return True
            
        except Exception as e:
            print(f"Monte Carlo simulation test failed: {e}")
            return False
    
    async def test_stress_testing(self) -> bool:
        """Test stress testing through MCP tools."""
        try:
            # Test stress testing
            arguments = {
                "scenarios": ["worst_case", "average_case", "best_case"],
                "severity_levels": ["low", "medium", "high"],
                "time_periods": [3, 6, 12],
                "variables": ["revenue", "cost", "profit"]
            }
            
            result = await self.mcp_tools._run_stress_testing(arguments)
            
            # Check that the result is valid
            assert result.get("success", False), "Stress testing failed"
            
            print("✅ Stress testing completed successfully")
            return True
            
        except Exception as e:
            print(f"Stress testing test failed: {e}")
            return False
    
    async def test_knowledge_graph_analysis(self) -> bool:
        """Test knowledge graph analysis through MCP tools."""
        try:
            # Test knowledge graph analysis
            arguments = {
                "max_nodes": 100,
                "max_relationships": 200,
                "include_metadata": True,
                "relationship_types": ["correlation", "causation", "association"],
                "node_types": ["entity", "concept", "event"]
            }
            
            result = await self.mcp_tools._generate_knowledge_graph(arguments)
            
            # Check that the result is valid
            assert result.get("success", False), "Knowledge graph analysis failed"
            
            print("✅ Knowledge graph analysis completed successfully")
            return True
            
        except Exception as e:
            print(f"Knowledge graph analysis test failed: {e}")
            return False
    
    async def test_visualization_generation(self) -> bool:
        """Test visualization generation through MCP tools."""
        try:
            # Test visualization generation
            arguments = {
                "chart_types": ["line", "bar", "scatter", "heatmap"],
                "interactive": True,
                "drill_down_enabled": True,
                "export_formats": ["png", "svg", "pdf"]
            }
            
            result = await self.mcp_tools._generate_visualizations(arguments)
            
            # Check that the result is valid
            assert result.get("success", False), "Visualization generation failed"
            
            print("✅ Visualization generation completed successfully")
            return True
            
        except Exception as e:
            print(f"Visualization generation test failed: {e}")
            return False
    
    async def test_anomaly_detection(self) -> bool:
        """Test anomaly detection through MCP tools."""
        try:
            # Test anomaly detection
            arguments = {
                "data": {"test": "data"},
                "detection_methods": ["statistical", "machine_learning"],
                "confidence_threshold": 0.95
            }
            
            result = await self.mcp_tools._detect_anomalies(arguments)
            
            # Check that the result is valid
            assert result.get("success", False), "Anomaly detection failed"
            
            print("✅ Anomaly detection completed successfully")
            return True
            
        except Exception as e:
            print(f"Anomaly detection test failed: {e}")
            return False
    
    async def test_pattern_analysis(self) -> bool:
        """Test pattern analysis through MCP tools."""
        try:
            # Test pattern analysis
            arguments = {
                "data": {"test": "data"},
                "pattern_types": ["temporal", "spatial", "behavioral"],
                "time_window": 30
            }
            
            result = await self.mcp_tools._analyze_patterns(arguments)
            
            # Check that the result is valid
            assert result.get("success", False), "Pattern analysis failed"
            
            print("✅ Pattern analysis completed successfully")
            return True
            
        except Exception as e:
            print(f"Pattern analysis test failed: {e}")
            return False
    
    async def test_risk_assessment(self) -> bool:
        """Test risk assessment through MCP tools."""
        try:
            # Test risk assessment
            arguments = {
                "risk_categories": ["financial", "operational", "strategic"],
                "assessment_method": "quantitative",
                "include_mitigation": True
            }
            
            result = await self.mcp_tools._assess_risks(arguments)
            
            # Check that the result is valid
            assert result.get("success", False), "Risk assessment failed"
            
            print("✅ Risk assessment completed successfully")
            return True
            
        except Exception as e:
            print(f"Risk assessment test failed: {e}")
            return False
    
    async def test_geopolitical_mapping(self) -> bool:
        """Test geopolitical mapping through MCP tools."""
        try:
            # Test geopolitical mapping
            arguments = {
                "regions": ["Asia", "Europe", "Americas"],
                "analysis_frameworks": ["political", "economic", "security"],
                "include_trends": True
            }
            
            result = await self.mcp_tools._create_geopolitical_map(arguments)
            
            # Check that the result is valid
            assert result.get("success", False), "Geopolitical mapping failed"
            
            print("✅ Geopolitical mapping completed successfully")
            return True
            
        except Exception as e:
            print(f"Geopolitical mapping test failed: {e}")
            return False
    
    def print_summary(self, results: Dict[str, Any]):
        """Print test summary."""
        print("\n" + "=" * 50)
        print("📊 ENHANCED REPORT MCP INTEGRATION TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(results)
        passed_tests = sum(1 for result in results.values() if result["status"] == "PASSED")
        failed_tests = sum(1 for result in results.values() if result["status"] == "FAILED")
        error_tests = sum(1 for result in results.values() if result["status"] == "ERROR")
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️ Errors: {error_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0 or error_tests > 0:
            print("\n🔍 Failed/Error Details:")
            for test_name, result in results.items():
                if result["status"] != "PASSED":
                    print(f"  - {test_name}: {result['status']}")
                    if "error" in result:
                        print(f"    Error: {result['error']}")
        
        print("\n" + "=" * 50)


async def main():
    """Main test runner."""
    tester = EnhancedReportMCPIntegrationTester()
    await tester.run_integration_tests()


if __name__ == "__main__":
    asyncio.run(main())
