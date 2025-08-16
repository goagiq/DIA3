#!/usr/bin/env python3
"""
Test script for Phase 4 Multi-Domain Integration Components
Tests DoD Domain Integration, Intelligence Community Integration, and Federated Learning Engine
"""

import asyncio
import json
import sys
import time
from datetime import datetime
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, 'src')

import requests
from loguru import logger

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

class Phase4MultiDomainIntegrationTester:
    """Test suite for Phase 4 Multi-Domain Integration components."""
    
    def __init__(self, base_url: str = "http://localhost:8003"):
        self.base_url = base_url
        self.test_results = []
        self.start_time = datetime.now()
        
    async def run_all_tests(self):
        """Run all Phase 4 tests."""
        logger.info("🚀 Starting Phase 4 Multi-Domain Integration Tests")
        logger.info("=" * 60)
        
        # Test DoD Domain Integration
        await self.test_dod_domain_integration()
        
        # Test Intelligence Community Integration
        await self.test_intelligence_community_integration()
        
        # Test Federated Learning Engine
        await self.test_federated_learning_engine()
        
        # Test Status Endpoints
        await self.test_status_endpoints()
        
        # Generate test report
        await self.generate_test_report()
        
    async def test_dod_domain_integration(self):
        """Test DoD Domain Integration endpoints."""
        logger.info("🔍 Testing DoD Domain Integration")
        
        # Test data for DoD integration
        test_data = {
            "intelligence_data": {
                "sigint": {"source": "NSA", "confidence": 0.9, "data": "encrypted_communications"},
                "humint": {"source": "CIA", "confidence": 0.8, "data": "human_intelligence"},
                "osint": {"source": "OSINT", "confidence": 0.7, "data": "open_source_intelligence"},
                "geospatial": {"source": "NGA", "confidence": 0.95, "data": "satellite_imagery"},
                "cyber": {"source": "CYBERCOM", "confidence": 0.85, "data": "cyber_threats"}
            },
            "readiness_data": {
                "personnel": {"strength": 1000000, "training_level": "advanced", "deployment_ready": True},
                "equipment": {"operational_rate": 0.9, "maintenance_status": "excellent", "modernization_level": "current"},
                "logistics": {"supply_chain_status": "robust", "fuel_availability": 0.95, "transportation_capacity": 0.9},
                "training": {"training_completion": 0.85, "certification_status": "complete", "exercise_participation": 0.9},
                "command_control": {"communication_systems": "operational", "decision_making_capacity": "high", "coordination_ability": "effective"}
            },
            "analysis_results": {
                "threat_assessment": {"level": "medium", "confidence": 0.85},
                "capability_analysis": {"strength": "strong", "gaps": ["cyber_defense"]},
                "strategic_analysis": {"position": "advantageous", "recommendations": ["enhance_cyber_capabilities"]}
            }
        }
        
        try:
            # Test DoD integration endpoint
            response = requests.post(
                f"{self.base_url}/ml-forecasting/phase4/dod-integration",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info("✅ DoD Domain Integration test passed")
                self.test_results.append({
                    "test": "dod_domain_integration",
                    "status": "passed",
                    "response": result
                })
            else:
                logger.error(f"❌ DoD Domain Integration test failed: {response.status_code}")
                self.test_results.append({
                    "test": "dod_domain_integration",
                    "status": "failed",
                    "error": f"HTTP {response.status_code}: {response.text}"
                })
                
        except Exception as e:
            logger.error(f"❌ DoD Domain Integration test error: {e}")
            self.test_results.append({
                "test": "dod_domain_integration",
                "status": "error",
                "error": str(e)
            })
    
    async def test_intelligence_community_integration(self):
        """Test Intelligence Community Integration endpoints."""
        logger.info("🔍 Testing Intelligence Community Integration")
        
        # Test data for intelligence community integration
        test_data = {
            "intel_data": {
                "cia": {"intelligence_type": "human_intelligence", "confidence": 0.9, "data": "human_sources"},
                "nsa": {"intelligence_type": "signals_intelligence", "confidence": 0.95, "data": "signals_data"},
                "dia": {"intelligence_type": "military_intelligence", "confidence": 0.85, "data": "military_assessment"},
                "fbi": {"intelligence_type": "domestic_intelligence", "confidence": 0.8, "data": "domestic_threats"},
                "state": {"intelligence_type": "diplomatic_intelligence", "confidence": 0.75, "data": "diplomatic_relations"}
            },
            "available_data": {
                "collection_capabilities": ["sigint", "humint", "osint", "geospatial"],
                "analysis_capabilities": ["pattern_recognition", "predictive_modeling"],
                "coverage_areas": ["global", "regional", "local"],
                "technology_stack": ["ai_ml", "big_data", "cloud_computing"]
            },
            "source_data": {
                "human_sources": {"source_count": 1000, "verification_level": "high", "access_level": "classified"},
                "technical_sources": {"source_count": 5000, "verification_level": "very_high", "access_level": "top_secret"},
                "open_sources": {"source_count": 10000, "verification_level": "medium", "access_level": "public"},
                "alliance_sources": {"source_count": 500, "verification_level": "high", "access_level": "shared"}
            }
        }
        
        try:
            # Test intelligence community integration endpoint
            response = requests.post(
                f"{self.base_url}/ml-forecasting/phase4/intelligence-community-integration",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info("✅ Intelligence Community Integration test passed")
                self.test_results.append({
                    "test": "intelligence_community_integration",
                    "status": "passed",
                    "response": result
                })
            else:
                logger.error(f"❌ Intelligence Community Integration test failed: {response.status_code}")
                self.test_results.append({
                    "test": "intelligence_community_integration",
                    "status": "failed",
                    "error": f"HTTP {response.status_code}: {response.text}"
                })
                
        except Exception as e:
            logger.error(f"❌ Intelligence Community Integration test error: {e}")
            self.test_results.append({
                "test": "intelligence_community_integration",
                "status": "error",
                "error": str(e)
            })
    
    async def test_federated_learning_engine(self):
        """Test Federated Learning Engine endpoints."""
        logger.info("🔍 Testing Federated Learning Engine")
        
        # Test data for federated learning
        test_data = {
            "participating_agencies": ["CIA", "NSA", "DIA", "FBI", "State"],
            "local_updates": {
                "CIA": {
                    "model_weights": {"layer_1": [0.1, 0.2, 0.3], "layer_2": [0.4, 0.5, 0.6]},
                    "training_metrics": {"loss": 0.15, "accuracy": 0.85},
                    "update_timestamp": datetime.now().isoformat()
                },
                "NSA": {
                    "model_weights": {"layer_1": [0.2, 0.3, 0.4], "layer_2": [0.5, 0.6, 0.7]},
                    "training_metrics": {"loss": 0.12, "accuracy": 0.88},
                    "update_timestamp": datetime.now().isoformat()
                }
            },
            "training_data": {
                "data_type": "intelligence_analysis",
                "privacy_level": "high",
                "encryption": "homomorphic",
                "differential_privacy": True
            },
            "round_config": {
                "round_number": 1,
                "algorithm": "federated_averaging",
                "privacy_budget": 1.0,
                "convergence_threshold": 0.01
            }
        }
        
        try:
            # Test federated learning endpoint
            response = requests.post(
                f"{self.base_url}/ml-forecasting/phase4/federated-learning",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info("✅ Federated Learning Engine test passed")
                self.test_results.append({
                    "test": "federated_learning_engine",
                    "status": "passed",
                    "response": result
                })
            else:
                logger.error(f"❌ Federated Learning Engine test failed: {response.status_code}")
                self.test_results.append({
                    "test": "federated_learning_engine",
                    "status": "failed",
                    "error": f"HTTP {response.status_code}: {response.text}"
                })
                
        except Exception as e:
            logger.error(f"❌ Federated Learning Engine test error: {e}")
            self.test_results.append({
                "test": "federated_learning_engine",
                "status": "error",
                "error": str(e)
            })
    
    async def test_status_endpoints(self):
        """Test status endpoints for Phase 4 components."""
        logger.info("🔍 Testing Phase 4 Status Endpoints")
        
        status_endpoints = [
            "/ml-forecasting/phase4/dod-status",
            "/ml-forecasting/phase4/intelligence-community-status",
            "/ml-forecasting/phase4/federated-learning-status"
        ]
        
        for endpoint in status_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"✅ {endpoint} status test passed")
                    self.test_results.append({
                        "test": f"status_{endpoint.split('/')[-1]}",
                        "status": "passed",
                        "response": result
                    })
                else:
                    logger.error(f"❌ {endpoint} status test failed: {response.status_code}")
                    self.test_results.append({
                        "test": f"status_{endpoint.split('/')[-1]}",
                        "status": "failed",
                        "error": f"HTTP {response.status_code}: {response.text}"
                    })
                    
            except Exception as e:
                logger.error(f"❌ {endpoint} status test error: {e}")
                self.test_results.append({
                    "test": f"status_{endpoint.split('/')[-1]}",
                    "status": "error",
                    "error": str(e)
                })
    
    async def generate_test_report(self):
        """Generate comprehensive test report."""
        logger.info("📊 Generating Phase 4 Test Report")
        logger.info("=" * 60)
        
        # Calculate test statistics
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "passed"])
        failed_tests = len([r for r in self.test_results if r["status"] == "failed"])
        error_tests = len([r for r in self.test_results if r["status"] == "error"])
        
        # Calculate success rate
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Generate report
        report = {
            "test_suite": "Phase 4 Multi-Domain Integration",
            "timestamp": datetime.now().isoformat(),
            "duration": (datetime.now() - self.start_time).total_seconds(),
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "error_tests": error_tests,
                "success_rate": f"{success_rate:.1f}%"
            },
            "test_results": self.test_results,
            "phase4_components": [
                "DoD Domain Integration",
                "Intelligence Community Integration", 
                "Federated Learning Engine"
            ],
            "endpoints_tested": [
                "/ml-forecasting/phase4/dod-integration",
                "/ml-forecasting/phase4/intelligence-community-integration",
                "/ml-forecasting/phase4/federated-learning",
                "/ml-forecasting/phase4/dod-status",
                "/ml-forecasting/phase4/intelligence-community-status",
                "/ml-forecasting/phase4/federated-learning-status"
            ]
        }
        
        # Print summary
        logger.info(f"📈 Test Summary:")
        logger.info(f"   Total Tests: {total_tests}")
        logger.info(f"   Passed: {passed_tests}")
        logger.info(f"   Failed: {failed_tests}")
        logger.info(f"   Errors: {error_tests}")
        logger.info(f"   Success Rate: {success_rate:.1f}%")
        
        # Save detailed report
        report_filename = f"phase4_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Detailed report saved to: {report_filename}")
        
        # Print individual test results
        logger.info("\n📋 Individual Test Results:")
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "passed" else "❌"
            logger.info(f"   {status_icon} {result['test']}: {result['status']}")
        
        # Final verdict
        if success_rate >= 80:
            logger.info("🎉 Phase 4 Multi-Domain Integration Tests: EXCELLENT")
        elif success_rate >= 60:
            logger.info("👍 Phase 4 Multi-Domain Integration Tests: GOOD")
        elif success_rate >= 40:
            logger.info("⚠️ Phase 4 Multi-Domain Integration Tests: NEEDS IMPROVEMENT")
        else:
            logger.info("❌ Phase 4 Multi-Domain Integration Tests: FAILED")
        
        return report

async def main():
    """Main test execution function."""
    logger.info("🤖 Phase 4 Multi-Domain Integration Test Suite")
    logger.info("Testing DoD Domain Integration, Intelligence Community Integration, and Federated Learning Engine")
    logger.info("=" * 80)
    
    # Create tester instance
    tester = Phase4MultiDomainIntegrationTester()
    
    # Run all tests
    await tester.run_all_tests()
    
    logger.info("🏁 Phase 4 Multi-Domain Integration Test Suite completed")

if __name__ == "__main__":
    asyncio.run(main())
