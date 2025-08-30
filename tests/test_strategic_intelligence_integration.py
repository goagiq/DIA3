#!/usr/bin/env python3
"""
Strategic Intelligence Forecast Integration Test
Tests the complete integration of strategic intelligence forecasting with API routes and MCP tools
"""

import asyncio
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.append('src')

from loguru import logger

class StrategicIntelligenceIntegrationTest:
    """Test class for strategic intelligence forecast integration"""
    
    def __init__(self):
        self.api_base_url = "http://localhost:8003"
        self.mcp_base_url = "http://localhost:8000"
        self.test_results = []
    
    async def test_api_endpoints(self):
        """Test strategic intelligence forecast API endpoints"""
        
        logger.info("🔍 Testing Strategic Intelligence Forecast API Endpoints")
        
        # Test health check
        try:
            response = requests.get(f"{self.api_base_url}/strategic-intelligence/health")
            if response.status_code == 200:
                health_data = response.json()
                logger.info(f"✅ Health check passed: {health_data}")
                self.test_results.append({
                    "test": "API Health Check",
                    "status": "PASSED",
                    "details": health_data
                })
            else:
                logger.error(f"❌ Health check failed: {response.status_code}")
                self.test_results.append({
                    "test": "API Health Check",
                    "status": "FAILED",
                    "details": f"Status code: {response.status_code}"
                })
        except Exception as e:
            logger.error(f"❌ Health check error: {e}")
            self.test_results.append({
                "test": "API Health Check",
                "status": "FAILED",
                "details": str(e)
            })
        
        # Test forecast generation
        try:
            forecast_request = {
                "scenario_type": "strategic_planning",
                "iterations": 1000,  # Small number for testing
                "time_horizon": 12,
                "confidence_level": 0.95,
                "include_scenarios": True,
                "include_policy_recommendations": True,
                "variables": {
                    "geopolitical_stability": {
                        "distribution": "beta",
                        "parameters": {
                            "alpha": 2.5,
                            "beta": 3.5
                        }
                    },
                    "economic_indicators": {
                        "distribution": "normal",
                        "parameters": {
                            "mean": 0.65,
                            "std": 0.15
                        }
                    },
                    "military_readiness": {
                        "distribution": "beta",
                        "parameters": {
                            "alpha": 3.0,
                            "beta": 2.0
                        }
                    }
                },
                "correlations": [
                    [1.0, 0.6, 0.4],
                    [0.6, 1.0, 0.3],
                    [0.4, 0.3, 1.0]
                ]
            }
            
            response = requests.post(
                f"{self.api_base_url}/strategic-intelligence/forecast",
                json=forecast_request,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                forecast_data = response.json()
                logger.info(f"✅ Forecast generation passed: {forecast_data['forecast_id']}")
                self.test_results.append({
                    "test": "API Forecast Generation",
                    "status": "PASSED",
                    "details": {
                        "forecast_id": forecast_data['forecast_id'],
                        "processing_time": forecast_data['processing_time']
                    }
                })
                
                # Test retrieving the forecast
                forecast_id = forecast_data['forecast_id']
                response = requests.get(f"{self.api_base_url}/strategic-intelligence/forecast/{forecast_id}")
                
                if response.status_code == 200:
                    retrieved_data = response.json()
                    logger.info(f"✅ Forecast retrieval passed: {forecast_id}")
                    self.test_results.append({
                        "test": "API Forecast Retrieval",
                        "status": "PASSED",
                        "details": {"forecast_id": forecast_id}
                    })
                else:
                    logger.error(f"❌ Forecast retrieval failed: {response.status_code}")
                    self.test_results.append({
                        "test": "API Forecast Retrieval",
                        "status": "FAILED",
                        "details": f"Status code: {response.status_code}"
                    })
                
            else:
                logger.error(f"❌ Forecast generation failed: {response.status_code}")
                self.test_results.append({
                    "test": "API Forecast Generation",
                    "status": "FAILED",
                    "details": f"Status code: {response.status_code}"
                })
                
        except Exception as e:
            logger.error(f"❌ Forecast generation error: {e}")
            self.test_results.append({
                "test": "API Forecast Generation",
                "status": "FAILED",
                "details": str(e)
            })
        
        # Test listing forecasts
        try:
            response = requests.get(f"{self.api_base_url}/strategic-intelligence/forecasts")
            
            if response.status_code == 200:
                forecasts_data = response.json()
                logger.info(f"✅ Forecast listing passed: {forecasts_data['total_count']} forecasts")
                self.test_results.append({
                    "test": "API Forecast Listing",
                    "status": "PASSED",
                    "details": {
                        "total_count": forecasts_data['total_count']
                    }
                })
            else:
                logger.error(f"❌ Forecast listing failed: {response.status_code}")
                self.test_results.append({
                    "test": "API Forecast Listing",
                    "status": "FAILED",
                    "details": f"Status code: {response.status_code}"
                })
                
        except Exception as e:
            logger.error(f"❌ Forecast listing error: {e}")
            self.test_results.append({
                "test": "API Forecast Listing",
                "status": "FAILED",
                "details": str(e)
            })
    
    async def test_mcp_tools(self):
        """Test strategic intelligence forecast MCP tools"""
        
        logger.info("🔍 Testing Strategic Intelligence Forecast MCP Tools")
        
        # Test MCP server connection
        try:
            response = requests.get(f"{self.mcp_base_url}/mcp", headers={
                "Accept": "application/json, text/event-stream"
            })
            
            if response.status_code in [200, 405]:  # 405 is expected for GET on POST endpoint
                logger.info("✅ MCP server connection successful")
                self.test_results.append({
                    "test": "MCP Server Connection",
                    "status": "PASSED",
                    "details": "Server responding"
                })
            else:
                logger.error(f"❌ MCP server connection failed: {response.status_code}")
                self.test_results.append({
                    "test": "MCP Server Connection",
                    "status": "FAILED",
                    "details": f"Status code: {response.status_code}"
                })
                
        except Exception as e:
            logger.error(f"❌ MCP server connection error: {e}")
            self.test_results.append({
                "test": "MCP Server Connection",
                "status": "FAILED",
                "details": str(e)
            })
    
    async def test_monte_carlo_integration(self):
        """Test Monte Carlo integration directly"""
        
        logger.info("🔍 Testing Monte Carlo Integration")
        
        try:
            from src.core.monte_carlo.engine import MonteCarloEngine
            
            # Initialize Monte Carlo engine
            monte_carlo_engine = MonteCarloEngine()
            
            # Test scenario configuration
            scenario_config = {
                'variables': {
                    'geopolitical_stability': {
                        'distribution': 'beta',
                        'parameters': {
                            'alpha': 2.5,
                            'beta': 3.5
                        }
                    },
                    'economic_indicators': {
                        'distribution': 'normal',
                        'parameters': {
                            'mean': 0.65,
                            'std': 0.15
                        }
                    },
                    'military_readiness': {
                        'distribution': 'beta',
                        'parameters': {
                            'alpha': 3.0,
                            'beta': 2.0
                        }
                    }
                },
                'correlations': [
                    [1.0, 0.6, 0.4],
                    [0.6, 1.0, 0.3],
                    [0.4, 0.3, 1.0]
                ]
            }
            
            # Run small simulation for testing
            results = await monte_carlo_engine.run_simulation(
                scenario_config, 
                num_iterations=100, 
                parallel=False
            )
            
            if results and 'statistics' in results:
                logger.info("✅ Monte Carlo integration test passed")
                self.test_results.append({
                    "test": "Monte Carlo Integration",
                    "status": "PASSED",
                    "details": {
                        "iterations": 100,
                        "variables": len(scenario_config['variables'])
                    }
                })
            else:
                logger.error("❌ Monte Carlo integration test failed")
                self.test_results.append({
                    "test": "Monte Carlo Integration",
                    "status": "FAILED",
                    "details": "No results returned"
                })
                
        except Exception as e:
            logger.error(f"❌ Monte Carlo integration error: {e}")
            self.test_results.append({
                "test": "Monte Carlo Integration",
                "status": "FAILED",
                "details": str(e)
            })
    
    async def test_file_generation(self):
        """Test file generation and storage"""
        
        logger.info("🔍 Testing File Generation and Storage")
        
        try:
            # Check if Results directory exists and has forecast files
            results_dir = Path("Results")
            if results_dir.exists():
                forecast_files = list(results_dir.glob("strategic_intelligence_forecast_*.json"))
                markdown_files = list(results_dir.glob("strategic_intelligence_forecast_*.md"))
                
                logger.info(f"✅ Found {len(forecast_files)} JSON files and {len(markdown_files)} markdown files")
                self.test_results.append({
                    "test": "File Generation",
                    "status": "PASSED",
                    "details": {
                        "json_files": len(forecast_files),
                        "markdown_files": len(markdown_files)
                    }
                })
                
                # Test reading a forecast file
                if forecast_files:
                    with open(forecast_files[0], 'r') as f:
                        data = json.load(f)
                        if 'report' in data and 'metadata' in data:
                            logger.info("✅ Forecast file format is correct")
                            self.test_results.append({
                                "test": "File Format",
                                "status": "PASSED",
                                "details": "Valid JSON structure"
                            })
                        else:
                            logger.error("❌ Forecast file format is incorrect")
                            self.test_results.append({
                                "test": "File Format",
                                "status": "FAILED",
                                "details": "Invalid JSON structure"
                            })
                else:
                    logger.warning("⚠️ No forecast files found")
                    self.test_results.append({
                        "test": "File Generation",
                        "status": "WARNING",
                        "details": "No forecast files found"
                    })
            else:
                logger.error("❌ Results directory not found")
                self.test_results.append({
                    "test": "File Generation",
                    "status": "FAILED",
                    "details": "Results directory not found"
                })
                
        except Exception as e:
            logger.error(f"❌ File generation test error: {e}")
            self.test_results.append({
                "test": "File Generation",
                "status": "FAILED",
                "details": str(e)
            })
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"Results/strategic_intelligence_integration_test_{timestamp}.json"
        
        # Ensure Results directory exists
        Path("Results").mkdir(exist_ok=True)
        
        # Calculate summary statistics
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASSED'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAILED'])
        warning_tests = len([r for r in self.test_results if r['status'] == 'WARNING'])
        
        report = {
            "test_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "warning_tests": warning_tests,
                "success_rate": f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%"
            },
            "test_results": self.test_results,
            "recommendations": []
        }
        
        # Add recommendations based on test results
        if failed_tests > 0:
            report["recommendations"].append("Review failed tests and fix integration issues")
        if warning_tests > 0:
            report["recommendations"].append("Address warnings to improve system reliability")
        if passed_tests == total_tests:
            report["recommendations"].append("All tests passed - system integration successful")
        
        # Save report
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Test report saved to: {report_file}")
        
        # Print summary
        logger.info("\n" + "="*60)
        logger.info("📊 STRATEGIC INTELLIGENCE INTEGRATION TEST SUMMARY")
        logger.info("="*60)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Warnings: {warning_tests}")
        logger.info(f"Success Rate: {report['test_summary']['success_rate']}")
        logger.info("="*60)
        
        # Print detailed results
        for result in self.test_results:
            status_icon = "✅" if result['status'] == 'PASSED' else "❌" if result['status'] == 'FAILED' else "⚠️"
            logger.info(f"{status_icon} {result['test']}: {result['status']}")
        
        return report

async def main():
    """Main test function"""
    
    logger.info("🚀 Starting Strategic Intelligence Forecast Integration Test")
    logger.info("="*60)
    
    # Wait for servers to be ready
    logger.info("⏳ Waiting 60 seconds for servers to be ready...")
    await asyncio.sleep(60)
    
    # Initialize test
    test = StrategicIntelligenceIntegrationTest()
    
    # Run tests
    await test.test_api_endpoints()
    await test.test_mcp_tools()
    await test.test_monte_carlo_integration()
    await test.test_file_generation()
    
    # Generate report
    report = test.generate_test_report()
    
    logger.info("🎯 Strategic Intelligence Forecast Integration Test completed!")

if __name__ == '__main__':
    asyncio.run(main())
