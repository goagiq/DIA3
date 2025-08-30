#!/usr/bin/env python3
"""
Test script to check Monte Carlo agent health and readiness
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.core.monte_carlo.analysis import MonteCarloAnalysis
from src.core.monte_carlo.config import MonteCarloConfig
from src.agents.monte_carlo_agent import MonteCarloAgent


async def test_monte_carlo_health():
    """Test Monte Carlo agent health and readiness"""
    print("🔍 Checking Monte Carlo Agent Health Status...")
    print("=" * 60)
    
    try:
        # Test 1: Configuration
        print("1. Testing Configuration...")
        config = MonteCarloConfig()
        print("   ✅ Configuration loaded successfully")
        print(f"   📊 Supported scenarios: {len(config.supported_scenarios)}")
        print(f"   📈 Supported distributions: "
              f"{len(config.supported_distributions)}")
        
        # Test 2: Analysis Engine
        print("\n2. Testing Analysis Engine...")
        analysis = MonteCarloAnalysis(config)
        health_status = await analysis.health_check()
        
        print(f"   Status: {health_status.get('status', 'Unknown')}")
        print(f"   Message: {health_status.get('message', 'No message')}")
        print(f"   Ready: {health_status.get('ready', False)}")
        
        components = health_status.get('components', {})
        for component, status in components.items():
            print(f"   {component}: {'✅' if status else '❌'}")
        
        # Test 3: Agent Initialization
        print("\n3. Testing Agent Initialization...")
        agent = MonteCarloAgent()
        print(f"   ✅ Agent initialized successfully")
        print(f"   Agent ID: {agent.agent_id}")
        print(f"   Supported Data Types: {agent.supported_data_types}")
        
        # Test 4: Basic Capability Test
        print("\n4. Testing Basic Capabilities...")
        capabilities = await agent.get_capabilities()
        print(f"   ✅ Capabilities retrieved: {len(capabilities)} items")
        
        # Test 5: Simple Simulation Test
        print("\n5. Testing Simple Simulation...")
        test_params = {
            "scenario_type": "risk_assessment",
            "iterations": 100,
            "variables": {
                "operational_risk": {
                    "distribution": "normal",
                    "parameters": {"mean": 0.1, "std": 0.05}
                }
            },
            "confidence_level": 0.95
        }
        
        result = await agent.process_request(test_params)
        print(f"   ✅ Simple simulation completed successfully")
        print(f"   📊 Result keys: {list(result.keys())}")
        
        # Overall Health Assessment
        print("\n" + "=" * 60)
        print("🏥 OVERALL HEALTH ASSESSMENT")
        print("=" * 60)
        
        all_healthy = (
            health_status.get('ready', False) and
            'analysis_engine' in components and
            components['analysis_engine'] and
            'configuration' in components and
            components['configuration']
        )
        
        if all_healthy:
            print("✅ Monte Carlo Agent is HEALTHY and READY to process requests")
            print("🎯 All components are functioning correctly")
            print("📈 Ready for Monte Carlo simulations")
        else:
            print("❌ Monte Carlo Agent has HEALTH ISSUES")
            print("🔧 Some components may need attention")
            print("⚠️  Review component status above")
        
        return all_healthy
        
    except Exception as e:
        print(f"\n❌ ERROR during health check: {str(e)}")
        print(f"🔍 Error type: {type(e).__name__}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")
        return False


async def test_api_health():
    """Test API endpoint health"""
    print("\n🌐 Testing API Health...")
    print("=" * 60)
    
    try:
        import requests
        import json
        
        # Test health endpoint
        base_url = "http://localhost:8003"
        health_url = f"{base_url}/health"
        
        response = requests.get(health_url, timeout=10)
        print(f"   API Status Code: {response.status_code}")
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ API is healthy")
            print(f"   📊 Status: {health_data.get('status', 'Unknown')}")
            
            # Check Monte Carlo specific endpoints
            monte_carlo_url = f"{base_url}/monte-carlo/health"
            mc_response = requests.get(monte_carlo_url, timeout=10)
            print(f"   Monte Carlo API Status: {mc_response.status_code}")
            
            if mc_response.status_code == 200:
                mc_health = mc_response.json()
                print(f"   ✅ Monte Carlo API is healthy")
                print(f"   📈 Ready: {mc_health.get('ready', False)}")
            else:
                print(f"   ❌ Monte Carlo API health check failed")
                
        else:
            print(f"   ❌ API health check failed")
            
    except Exception as e:
        print(f"   ❌ API health check error: {str(e)}")


if __name__ == "__main__":
    print("🎲 Monte Carlo Agent Health Check")
    print("=" * 60)
    
    # Run health checks
    agent_healthy = asyncio.run(test_monte_carlo_health())
    asyncio.run(test_api_health())
    
    print("\n" + "=" * 60)
    if agent_healthy:
        print("🎉 Monte Carlo Agent is ready for testing!")
        print("📋 Use the test scenarios from MONTE_CARLO_TEST_SCENARIOS.md")
    else:
        print("⚠️  Monte Carlo Agent needs attention before testing")
        print("🔧 Please review the health check results above")
    
    print("=" * 60)
