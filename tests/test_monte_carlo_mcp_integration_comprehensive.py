#!/usr/bin/env python3
"""
Comprehensive Monte Carlo MCP Integration Test
Tests Monte Carlo tools integration with dynamic MCP tool management and 
client communication
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from loguru import logger

# Configure logging
logging.basicConfig(level=logging.INFO)


class MonteCarloMCPIntegrationTest:
    """Comprehensive test for Monte Carlo MCP integration"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        
    async def test_mcp_server_status(self) -> bool:
        """Test if MCP server is running on port 8000"""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 8000))
            sock.close()
            
            if result == 0:
                logger.info("✅ MCP server is running on port 8000")
                self.test_results.append({
                    "test": "MCP Server Status",
                    "status": "PASS",
                    "message": "MCP server is running on port 8000"
                })
                return True
            else:
                logger.error("❌ MCP server is not running on port 8000")
                self.test_results.append({
                    "test": "MCP Server Status",
                    "status": "FAIL",
                    "message": "MCP server is not running on port 8000"
                })
                return False
        except Exception as e:
            logger.error(f"❌ Error checking MCP server status: {e}")
            self.test_results.append({
                "test": "MCP Server Status",
                "status": "ERROR",
                "message": f"Error checking MCP server status: {e}"
            })
            return False
    
    async def test_dynamic_tool_manager(self) -> bool:
        """Test dynamic MCP tool manager integration"""
        try:
            from src.mcp_servers.dynamic_tool_manager import dynamic_tool_manager
            
            # Check if Monte Carlo tools are registered
            tool_statuses = dynamic_tool_manager.get_all_tool_statuses()
            
            if "monte_carlo_simulation" in tool_statuses:
                logger.info("✅ Monte Carlo tools registered in dynamic tool manager")
                self.test_results.append({
                    "test": "Dynamic Tool Manager",
                    "status": "PASS",
                    "message": "Monte Carlo tools registered in dynamic tool manager"
                })
                return True
            else:
                logger.warning("⚠️ Monte Carlo tools not found in dynamic tool manager")
                self.test_results.append({
                    "test": "Dynamic Tool Manager",
                    "status": "WARNING",
                    "message": "Monte Carlo tools not found in dynamic tool manager"
                })
                return False
                
        except Exception as e:
            logger.error(f"❌ Error testing dynamic tool manager: {e}")
            self.test_results.append({
                "test": "Dynamic Tool Manager",
                "status": "ERROR",
                "message": f"Error testing dynamic tool manager: {e}"
            })
            return False
    
    async def test_mcp_client_communication(self) -> bool:
        """Test MCP client communication with Monte Carlo tools"""
        try:
            # Test with streamable HTTP client
            from mcp.client.streamable_http import streamablehttp_client
            from strands import Agent
            from strands.tools.mcp.mcp_client import MCPClient
            
            # Create streamable HTTP MCP client
            streamable_http_mcp_client = MCPClient(
                lambda: streamablehttp_client("http://localhost:8000/mcp")
            )
            
            with streamable_http_mcp_client:
                # Get the tools from the MCP server
                tools = streamable_http_mcp_client.list_tools_sync()
                
                # Check if Monte Carlo tools are available
                monte_carlo_tools = [tool for tool in tools if "monte_carlo" in tool.name.lower()]
                
                if monte_carlo_tools:
                    logger.info(f"✅ Found {len(monte_carlo_tools)} Monte Carlo tools")
                    
                    # Test Monte Carlo health check
                    health_check_tool = next((tool for tool in monte_carlo_tools if "health" in tool.name.lower()), None)
                    if health_check_tool:
                        result = await streamable_http_mcp_client.call_tool_sync(
                            health_check_tool.name, {}
                        )
                        logger.info(f"✅ Monte Carlo health check result: {result}")
                    
                    self.test_results.append({
                        "test": "MCP Client Communication",
                        "status": "PASS",
                        "message": f"Found {len(monte_carlo_tools)} Monte Carlo tools and tested communication"
                    })
                    return True
                else:
                    logger.warning("⚠️ No Monte Carlo tools found in MCP server")
                    self.test_results.append({
                        "test": "MCP Client Communication",
                        "status": "WARNING",
                        "message": "No Monte Carlo tools found in MCP server"
                    })
                    return False
                    
        except ImportError as e:
            logger.warning(f"⚠️ MCP client libraries not available: {e}")
            self.test_results.append({
                "test": "MCP Client Communication",
                "status": "SKIP",
                "message": f"MCP client libraries not available: {e}"
            })
            return False
        except Exception as e:
            logger.error(f"❌ Error testing MCP client communication: {e}")
            self.test_results.append({
                "test": "MCP Client Communication",
                "status": "ERROR",
                "message": f"Error testing MCP client communication: {e}"
            })
            return False
    
    async def test_monte_carlo_api_endpoints(self) -> bool:
        """Test Monte Carlo API endpoints"""
        try:
            import httpx
            
            # Test Monte Carlo health endpoint
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8004/api/v1/monte-carlo/health")
                
                if response.status_code == 200:
                    logger.info("✅ Monte Carlo API health endpoint working")
                    
                    # Test Monte Carlo simulation endpoint
                    simulation_data = {
                        "scenario_config": {
                            "variables": {
                                "revenue": {
                                    "distribution": "normal", 
                                    "parameters": {"mean": 100, "std": 10}
                                },
                                "cost": {
                                    "distribution": "normal", 
                                    "parameters": {"mean": 80, "std": 5}
                                }
                            },
                            "correlations": [
                                [1.0, 0.3],
                                [0.3, 1.0]
                            ]
                        },
                        "num_iterations": 100,
                        "parallel": True,
                        "include_phase5_features": True
                    }
                    
                    response = await client.post(
                        "http://localhost:8004/api/v1/monte-carlo/simulate",
                        json=simulation_data
                    )
                    
                    if response.status_code == 200:
                        logger.info("✅ Monte Carlo API simulation endpoint working")
                        self.test_results.append({
                            "test": "Monte Carlo API Endpoints",
                            "status": "PASS",
                            "message": "Monte Carlo API endpoints working correctly"
                        })
                        return True
                    else:
                        logger.warning(f"⚠️ Monte Carlo simulation endpoint returned {response.status_code}")
                        self.test_results.append({
                            "test": "Monte Carlo API Endpoints",
                            "status": "WARNING",
                            "message": f"Monte Carlo simulation endpoint returned {response.status_code}"
                        })
                        return False
                else:
                    logger.warning(f"⚠️ Monte Carlo health endpoint returned {response.status_code}")
                    self.test_results.append({
                        "test": "Monte Carlo API Endpoints",
                        "status": "WARNING",
                        "message": f"Monte Carlo health endpoint returned {response.status_code}"
                    })
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error testing Monte Carlo API endpoints: {e}")
            self.test_results.append({
                "test": "Monte Carlo API Endpoints",
                "status": "ERROR",
                "message": f"Error testing Monte Carlo API endpoints: {e}"
            })
            return False
    
    async def test_orchestrator_integration(self) -> bool:
        """Test Monte Carlo orchestrator integration"""
        try:
            from src.core.orchestrator import SentimentOrchestrator
            
            # Initialize orchestrator
            orchestrator = SentimentOrchestrator()
            
            # Check if Monte Carlo agent is registered
            agents = orchestrator.get_registered_agents()
            monte_carlo_agents = [agent for agent in agents if "monte" in agent.lower()]
            
            if monte_carlo_agents:
                logger.info(f"✅ Found {len(monte_carlo_agents)} Monte Carlo agents in orchestrator")
                self.test_results.append({
                    "test": "Orchestrator Integration",
                    "status": "PASS",
                    "message": f"Found {len(monte_carlo_agents)} Monte Carlo agents in orchestrator"
                })
                return True
            else:
                logger.warning("⚠️ No Monte Carlo agents found in orchestrator")
                self.test_results.append({
                    "test": "Orchestrator Integration",
                    "status": "WARNING",
                    "message": "No Monte Carlo agents found in orchestrator"
                })
                return False
                
        except Exception as e:
            logger.error(f"❌ Error testing orchestrator integration: {e}")
            self.test_results.append({
                "test": "Orchestrator Integration",
                "status": "ERROR",
                "message": f"Error testing orchestrator integration: {e}"
            })
            return False
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        logger.info("🚀 Starting comprehensive Monte Carlo MCP integration tests")
        
        # Wait for server to be ready
        logger.info("⏳ Waiting 40 seconds for server to be ready...")
        await asyncio.sleep(40)
        
        # Run tests
        tests = [
            self.test_mcp_server_status,
            self.test_dynamic_tool_manager,
            self.test_mcp_client_communication,
            self.test_monte_carlo_api_endpoints,
            self.test_orchestrator_integration
        ]
        
        results = []
        for test in tests:
            try:
                result = await test()
                results.append(result)
            except Exception as e:
                logger.error(f"❌ Test {test.__name__} failed with exception: {e}")
                results.append(False)
        
        # Generate summary
        passed = sum(results)
        total = len(results)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "test_duration": (datetime.now() - self.start_time).total_seconds(),
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": total - passed,
            "success_rate": (passed / total) * 100 if total > 0 else 0,
            "test_results": self.test_results,
            "overall_status": "PASS" if passed == total else "FAIL"
        }
        
        logger.info(f"📊 Test Summary: {passed}/{total} tests passed ({summary['success_rate']:.1f}%)")
        
        return summary

async def main():
    """Main test function"""
    test = MonteCarloMCPIntegrationTest()
    results = await test.run_all_tests()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"monte_carlo_mcp_integration_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"💾 Test results saved to {results_file}")
    
    # Print detailed results
    print("\n" + "="*80)
    print("MONTE CARLO MCP INTEGRATION TEST RESULTS")
    print("="*80)
    
    for result in results["test_results"]:
        status_icon = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "WARNING" else "❌"
        print(f"{status_icon} {result['test']}: {result['status']} - {result['message']}")
    
    print(f"\nOverall Status: {results['overall_status']}")
    print(f"Success Rate: {results['success_rate']:.1f}%")
    print(f"Test Duration: {results['test_duration']:.2f} seconds")
    
    return results["overall_status"] == "PASS"

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
