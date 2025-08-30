"""
Test script for Phase 5: Model Interpretability & Explainable AI
Advanced forecasting & prediction system for DoD/Intelligence Community
"""

import asyncio
import json
import requests
from datetime import datetime
from typing import Dict, Any, List
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger

# Test configuration
API_BASE_URL = "http://localhost:8003"
MCP_BASE_URL = "http://localhost:8000"

class Phase5InterpretabilityTester:
    """Test suite for Phase 5 Model Interpretability & Explainable AI"""
    
    def __init__(self):
        """Initialize the tester"""
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        self.total_tests = 0
        
        logger.info("🧪 Phase 5 Interpretability Test Suite Initialized")
    
    async def run_all_tests(self):
        """Run all Phase 5 tests"""
        logger.info("🚀 Starting Phase 5 Interpretability Test Suite")
        
        # Test API endpoints
        await self.test_api_endpoints()
        
        # Test MCP tools
        await self.test_mcp_tools()
        
        # Test component functionality
        await self.test_component_functionality()
        
        # Generate test report
        await self.generate_test_report()
    
    async def test_api_endpoints(self):
        """Test Phase 5 API endpoints"""
        logger.info("🔍 Testing Phase 5 API endpoints")
        
        # Test health check
        await self.test_endpoint(
            "Phase 5 Health Check",
            f"{API_BASE_URL}/ml-forecasting/phase5/health",
            "GET"
        )
        
        # Test status check
        await self.test_endpoint(
            "Phase 5 Status Check",
            f"{API_BASE_URL}/ml-forecasting/phase5/status",
            "GET"
        )
        
        # Test model explanation
        await self.test_model_explanation()
        
        # Test intelligence explanation
        await self.test_intelligence_explanation()
        
        # Test threat assessment explanation
        await self.test_threat_assessment_explanation()
        
        # Test capability analysis explanation
        await self.test_capability_analysis_explanation()
        
        # Test executive summary generation
        await self.test_executive_summary_generation()
        
        # Test intelligence domain explanation
        await self.test_intelligence_domain_explanation()
        
        # Test feature importance generation
        await self.test_feature_importance_generation()
        
        # Test decision paths creation
        await self.test_decision_paths_creation()
    
    async def test_mcp_tools(self):
        """Test Phase 5 MCP tools"""
        logger.info("🔍 Testing Phase 5 MCP tools")
        
        # Test MCP health check
        await self.test_mcp_tool(
            "Phase 5 MCP Health Check",
            "phase5_health_check",
            {}
        )
        
        # Test model explanation MCP tool
        await self.test_mcp_tool(
            "Model Explanation MCP Tool",
            "explain_model_predictions",
            {
                "model_output": json.dumps({
                    "model_name": "TestModel",
                    "prediction": {"risk_level": "medium", "confidence": 0.75},
                    "confidence": 0.75
                }),
                "input_data": json.dumps({
                    "features": {
                        "military_capability": 0.8,
                        "economic_strength": 0.6,
                        "political_stability": 0.7
                    }
                }),
                "explanation_type": "comprehensive"
            }
        )
        
        # Test intelligence explanation MCP tool
        await self.test_mcp_tool(
            "Intelligence Explanation MCP Tool",
            "explain_intelligence_analysis",
            {
                "analysis_type": "threat_assessment",
                "analysis_results": json.dumps({
                    "threat_level": "medium",
                    "confidence": 0.7,
                    "indicators": ["military_buildup", "economic_sanctions"]
                })
            }
        )
        
        # Test threat assessment explanation MCP tool
        await self.test_mcp_tool(
            "Threat Assessment Explanation MCP Tool",
            "explain_threat_assessment",
            {
                "threat_analysis": json.dumps({
                    "threat_level": "high",
                    "threat_type": "military",
                    "confidence": 0.8,
                    "indicators": ["troop_mobilization", "weapons_deployment"]
                })
            }
        )
        
        # Test capability analysis explanation MCP tool
        await self.test_mcp_tool(
            "Capability Analysis Explanation MCP Tool",
            "explain_capability_analysis",
            {
                "capability_results": json.dumps({
                    "capability_score": 0.75,
                    "capability_domains": ["military", "economic"],
                    "strengths": ["advanced_technology", "strong_economy"],
                    "weaknesses": ["geographic_constraints"]
                })
            }
        )
        
        # Test executive summary MCP tool
        await self.test_mcp_tool(
            "Executive Summary MCP Tool",
            "generate_executive_summary",
            {
                "detailed_analysis": json.dumps({
                    "analysis_type": "threat_assessment",
                    "confidence": 0.8,
                    "key_findings": ["High threat level detected", "Immediate action required"],
                    "recommendations": ["Enhance monitoring", "Develop response plans"]
                }),
                "summary_type": "intelligence"
            }
        )
        
        # Test intelligence domain explanation MCP tool
        await self.test_mcp_tool(
            "Intelligence Domain Explanation MCP Tool",
            "explain_intelligence_domain",
            {
                "domain": "military",
                "analysis_results": json.dumps({
                    "capabilities": ["advanced_weapons", "trained_personnel"],
                    "readiness": 0.8,
                    "deployment": "active"
                })
            }
        )
        
        # Test feature importance MCP tool
        await self.test_mcp_tool(
            "Feature Importance MCP Tool",
            "generate_feature_importance",
            {
                "model_output": json.dumps({
                    "model_name": "TestModel",
                    "confidence": 0.75
                }),
                "data": json.dumps({
                    "features": {
                        "military_capability": 0.8,
                        "economic_strength": 0.6,
                        "political_stability": 0.7
                    }
                })
            }
        )
        
        # Test decision paths MCP tool
        await self.test_mcp_tool(
            "Decision Paths MCP Tool",
            "create_decision_paths",
            {
                "model_output": json.dumps({
                    "model_name": "TestModel",
                    "confidence": 0.75
                }),
                "data": json.dumps({
                    "features": {
                        "military_capability": 0.8,
                        "economic_strength": 0.6,
                        "political_stability": 0.7
                    }
                })
            }
        )
    
    async def test_component_functionality(self):
        """Test Phase 5 component functionality"""
        logger.info("🔍 Testing Phase 5 component functionality")
        
        try:
            # Test Model Interpretability Engine
            from src.core.interpretability.model_interpretability_engine import ModelInterpretabilityEngine
            
            engine = ModelInterpretabilityEngine()
            
            # Test explanation generation
            model_output = {
                "model_name": "TestModel",
                "prediction": {"risk_level": "medium", "confidence": 0.75},
                "confidence": 0.75
            }
            
            input_data = {
                "features": {
                    "military_capability": 0.8,
                    "economic_strength": 0.6,
                    "political_stability": 0.7
                }
            }
            
            explanation = await engine.explain_predictions(model_output, input_data)
            
            if explanation and hasattr(explanation, 'model_name'):
                await self.record_test_result(
                    "Model Interpretability Engine - Explanation Generation",
                    True,
                    "Successfully generated model explanation"
                )
            else:
                await self.record_test_result(
                    "Model Interpretability Engine - Explanation Generation",
                    False,
                    "Failed to generate model explanation"
                )
            
            # Test Intelligence Explanations Engine
            from src.core.interpretability.intelligence_explanations import IntelligenceExplanations
            
            intel_engine = IntelligenceExplanations()
            
            # Test threat assessment explanation
            threat_analysis = {
                "threat_level": "high",
                "threat_type": "military",
                "confidence": 0.8
            }
            
            threat_explanation = await intel_engine.explain_threat_assessment(threat_analysis)
            
            if threat_explanation and hasattr(threat_explanation, 'threat_level'):
                await self.record_test_result(
                    "Intelligence Explanations Engine - Threat Assessment",
                    True,
                    "Successfully generated threat assessment explanation"
                )
            else:
                await self.record_test_result(
                    "Intelligence Explanations Engine - Threat Assessment",
                    False,
                    "Failed to generate threat assessment explanation"
                )
            
            # Test capability analysis explanation
            capability_results = {
                "capability_score": 0.75,
                "capability_domains": ["military", "economic"]
            }
            
            capability_explanation = await intel_engine.explain_capability_analysis(capability_results)
            
            if capability_explanation and hasattr(capability_explanation, 'capability_score'):
                await self.record_test_result(
                    "Intelligence Explanations Engine - Capability Analysis",
                    True,
                    "Successfully generated capability analysis explanation"
                )
            else:
                await self.record_test_result(
                    "Intelligence Explanations Engine - Capability Analysis",
                    False,
                    "Failed to generate capability analysis explanation"
                )
            
            # Test executive summary generation
            detailed_analysis = {
                "analysis_type": "threat_assessment",
                "confidence": 0.8,
                "key_findings": ["High threat level detected"],
                "recommendations": ["Enhance monitoring"]
            }
            
            executive_summary = await intel_engine.generate_executive_summary(detailed_analysis)
            
            if executive_summary and "executive_summary" in executive_summary:
                await self.record_test_result(
                    "Intelligence Explanations Engine - Executive Summary",
                    True,
                    "Successfully generated executive summary"
                )
            else:
                await self.record_test_result(
                    "Intelligence Explanations Engine - Executive Summary",
                    False,
                    "Failed to generate executive summary"
                )
            
        except Exception as e:
            logger.error(f"❌ Component functionality test failed: {e}")
            await self.record_test_result(
                "Component Functionality Test",
                False,
                f"Component test failed: {str(e)}"
            )
    
    async def test_endpoint(self, test_name: str, url: str, method: str = "GET", data: Dict[str, Any] = None):
        """Test a specific API endpoint"""
        try:
            logger.info(f"🔍 Testing {test_name}")
            
            if method == "GET":
                response = requests.get(url, timeout=30)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success", True):
                    await self.record_test_result(
                        test_name,
                        True,
                        f"Endpoint {url} responded successfully"
                    )
                else:
                    await self.record_test_result(
                        test_name,
                        False,
                        f"Endpoint {url} returned error: {result.get('error', 'Unknown error')}"
                    )
            else:
                await self.record_test_result(
                    test_name,
                    False,
                    f"Endpoint {url} returned status code {response.status_code}"
                )
                
        except Exception as e:
            logger.error(f"❌ {test_name} failed: {e}")
            await self.record_test_result(
                test_name,
                False,
                f"Test failed with exception: {str(e)}"
            )
    
    async def test_mcp_tool(self, test_name: str, tool_name: str, parameters: Dict[str, Any]):
        """Test a specific MCP tool"""
        try:
            logger.info(f"🔍 Testing MCP tool: {test_name}")
            
            # Create MCP request
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": parameters
                }
            }
            
            # Send request to MCP server
            response = requests.post(
                MCP_BASE_URL,
                json=mcp_request,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result and result["result"].get("success", True):
                    await self.record_test_result(
                        test_name,
                        True,
                        f"MCP tool {tool_name} executed successfully"
                    )
                else:
                    await self.record_test_result(
                        test_name,
                        False,
                        f"MCP tool {tool_name} returned error: {result.get('error', 'Unknown error')}"
                    )
            else:
                await self.record_test_result(
                    test_name,
                    False,
                    f"MCP tool {tool_name} returned status code {response.status_code}"
                )
                
        except Exception as e:
            logger.error(f"❌ MCP tool {test_name} failed: {e}")
            await self.record_test_result(
                test_name,
                False,
                f"MCP tool test failed with exception: {str(e)}"
            )
    
    async def test_model_explanation(self):
        """Test model explanation endpoint"""
        test_data = {
            "model_output": {
                "model_name": "TestModel",
                "prediction": {"risk_level": "medium", "confidence": 0.75},
                "confidence": 0.75
            },
            "input_data": {
                "features": {
                    "military_capability": 0.8,
                    "economic_strength": 0.6,
                    "political_stability": 0.7
                }
            },
            "explanation_type": "comprehensive"
        }
        
        await self.test_endpoint(
            "Model Explanation Endpoint",
            f"{API_BASE_URL}/ml-forecasting/phase5/explain-model-predictions",
            "POST",
            test_data
        )
    
    async def test_intelligence_explanation(self):
        """Test intelligence explanation endpoint"""
        test_data = {
            "analysis_type": "threat_assessment",
            "analysis_results": {
                "threat_level": "medium",
                "confidence": 0.7,
                "indicators": ["military_buildup", "economic_sanctions"]
            }
        }
        
        await self.test_endpoint(
            "Intelligence Explanation Endpoint",
            f"{API_BASE_URL}/ml-forecasting/phase5/explain-intelligence-analysis",
            "POST",
            test_data
        )
    
    async def test_threat_assessment_explanation(self):
        """Test threat assessment explanation endpoint"""
        test_data = {
            "threat_analysis": {
                "threat_level": "high",
                "threat_type": "military",
                "confidence": 0.8,
                "indicators": ["troop_mobilization", "weapons_deployment"]
            }
        }
        
        await self.test_endpoint(
            "Threat Assessment Explanation Endpoint",
            f"{API_BASE_URL}/ml-forecasting/phase5/explain-threat-assessment",
            "POST",
            test_data
        )
    
    async def test_capability_analysis_explanation(self):
        """Test capability analysis explanation endpoint"""
        test_data = {
            "capability_results": {
                "capability_score": 0.75,
                "capability_domains": ["military", "economic"],
                "strengths": ["advanced_technology", "strong_economy"],
                "weaknesses": ["geographic_constraints"]
            }
        }
        
        await self.test_endpoint(
            "Capability Analysis Explanation Endpoint",
            f"{API_BASE_URL}/ml-forecasting/phase5/explain-capability-analysis",
            "POST",
            test_data
        )
    
    async def test_executive_summary_generation(self):
        """Test executive summary generation endpoint"""
        test_data = {
            "detailed_analysis": {
                "analysis_type": "threat_assessment",
                "confidence": 0.8,
                "key_findings": ["High threat level detected", "Immediate action required"],
                "recommendations": ["Enhance monitoring", "Develop response plans"]
            },
            "summary_type": "intelligence"
        }
        
        await self.test_endpoint(
            "Executive Summary Generation Endpoint",
            f"{API_BASE_URL}/ml-forecasting/phase5/generate-executive-summary",
            "POST",
            test_data
        )
    
    async def test_intelligence_domain_explanation(self):
        """Test intelligence domain explanation endpoint"""
        test_data = {
            "domain": "military",
            "analysis_results": {
                "capabilities": ["advanced_weapons", "trained_personnel"],
                "readiness": 0.8,
                "deployment": "active"
            }
        }
        
        await self.test_endpoint(
            "Intelligence Domain Explanation Endpoint",
            f"{API_BASE_URL}/ml-forecasting/phase5/explain-intelligence-domain",
            "POST",
            test_data
        )
    
    async def test_feature_importance_generation(self):
        """Test feature importance generation endpoint"""
        test_data = {
            "model_output": {
                "model_name": "TestModel",
                "confidence": 0.75
            },
            "data": {
                "features": {
                    "military_capability": 0.8,
                    "economic_strength": 0.6,
                    "political_stability": 0.7
                }
            }
        }
        
        await self.test_endpoint(
            "Feature Importance Generation Endpoint",
            f"{API_BASE_URL}/ml-forecasting/phase5/generate-feature-importance",
            "POST",
            test_data
        )
    
    async def test_decision_paths_creation(self):
        """Test decision paths creation endpoint"""
        test_data = {
            "model_output": {
                "model_name": "TestModel",
                "confidence": 0.75
            },
            "data": {
                "features": {
                    "military_capability": 0.8,
                    "economic_strength": 0.6,
                    "political_stability": 0.7
                }
            }
        }
        
        await self.test_endpoint(
            "Decision Paths Creation Endpoint",
            f"{API_BASE_URL}/ml-forecasting/phase5/create-decision-paths",
            "POST",
            test_data
        )
    
    async def record_test_result(self, test_name: str, passed: bool, message: str):
        """Record a test result"""
        self.total_tests += 1
        
        if passed:
            self.passed_tests += 1
            logger.info(f"✅ {test_name}: {message}")
        else:
            self.failed_tests += 1
            logger.error(f"❌ {test_name}: {message}")
        
        self.test_results.append({
            "test_name": test_name,
            "passed": passed,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    async def generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("📊 Generating Phase 5 Test Report")
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        report = {
            "phase": "Phase 5: Model Interpretability & Explainable AI",
            "test_summary": {
                "total_tests": self.total_tests,
                "passed_tests": self.passed_tests,
                "failed_tests": self.failed_tests,
                "success_rate": f"{success_rate:.1f}%"
            },
            "test_results": self.test_results,
            "timestamp": datetime.now().isoformat(),
            "status": "PASSED" if success_rate >= 80 else "FAILED"
        }
        
        # Save report to file
        report_filename = f"phase5_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        logger.info("=" * 80)
        logger.info("📊 PHASE 5 TEST SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total Tests: {self.total_tests}")
        logger.info(f"Passed: {self.passed_tests}")
        logger.info(f"Failed: {self.failed_tests}")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        logger.info(f"Status: {report['status']}")
        logger.info(f"Report saved to: {report_filename}")
        logger.info("=" * 80)
        
        if success_rate >= 80:
            logger.info("🎉 Phase 5 Model Interpretability & Explainable AI tests PASSED!")
        else:
            logger.error("❌ Phase 5 Model Interpretability & Explainable AI tests FAILED!")
        
        return report


async def main():
    """Main test function"""
    logger.info("🚀 Starting Phase 5 Interpretability Test Suite")
    
    # Create tester instance
    tester = Phase5InterpretabilityTester()
    
    # Run all tests
    await tester.run_all_tests()
    
    logger.info("🏁 Phase 5 Interpretability Test Suite completed")


if __name__ == "__main__":
    # Run the test suite
    asyncio.run(main())
