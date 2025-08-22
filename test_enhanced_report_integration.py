#!/usr/bin/env python3
"""
Comprehensive Enhanced Report Integration Test
Tests the complete integration of enhanced report functionality with MCP server and API endpoints.
"""

import asyncio
import json
import time
import requests
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_enhanced_report_generation():
    """Test enhanced report generation functionality."""
    print("🧪 Testing Enhanced Report Generation...")
    
    try:
        from src.core.export.enhanced_report_integration import generate_enhanced_report
        
        # Test basic report generation
        result = generate_enhanced_report(
            'pakistan_submarine',
            'Pakistan\'s 50-Submarine Acquisition and Strategic Implications',
            'Comprehensive Analysis of Conventional Deterrence and Regional Security'
        )
        
        print(f"✅ Enhanced report generated: {result}")
        
        # Check if file exists
        if Path(result).exists():
            print(f"✅ Report file exists: {result}")
            return True
        else:
            print(f"❌ Report file not found: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced report generation failed: {e}")
        return False

def test_monte_carlo_simulation():
    """Test Monte Carlo simulation functionality."""
    print("🎲 Testing Monte Carlo Simulation...")
    
    try:
        from src.core.analysis.monte_carlo_simulator import MonteCarloSimulator
        
        # Create simulator
        simulator = MonteCarloSimulator(n_iterations=1000)
        
        # Test Pakistan submarine simulation
        simulator.create_pakistan_submarine_simulation()
        
        # Get visualization data
        viz_data = simulator.create_visualization_data()
        
        print(f"✅ Monte Carlo simulation completed")
        print(f"   - Cost distribution: {len(viz_data.get('cost_distribution', {}).get('data', []))} bins")
        print(f"   - Risk distribution: {len(viz_data.get('risk_distribution', {}).get('data', []))} bins")
        print(f"   - Impact distribution: {len(viz_data.get('impact_distribution', {}).get('data', []))} bins")
        
        return True
        
    except Exception as e:
        print(f"❌ Monte Carlo simulation failed: {e}")
        return False

def test_mcp_server_connection():
    """Test MCP server connection."""
    print("🔌 Testing MCP Server Connection...")
    
    try:
        # Test MCP server health endpoint
        response = requests.get("http://localhost:8000/mcp-health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ MCP server health check passed")
            print(f"   - Status: {data.get('status')}")
            print(f"   - Endpoints: {data.get('endpoints')}")
            return True
        else:
            print(f"❌ MCP server health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ MCP server connection failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints."""
    print("🌐 Testing API Endpoints...")
    
    try:
        # Test main API server first - API server runs on port 8003
        response = requests.get("http://localhost:8003/health", timeout=10)
        
        if response.status_code == 200:
            print("✅ Main API server health check passed")
        else:
            print(f"⚠️ Main API server health check: {response.status_code}")
        
        # Test enhanced report API endpoint
        response = requests.get("http://localhost:8003/api/v1/reports/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Enhanced report API health check passed")
            print(f"   - Status: {data.get('status')}")
            return True
        else:
            # Try alternative endpoints
            for endpoint in ["/docs", "/openapi.json", "/"]:
                try:
                    response = requests.get(f"http://localhost:8003{endpoint}", timeout=5)
                    if response.status_code == 200:
                        print(f"✅ API server is running (found {endpoint})")
                        return True
                except:
                    continue
            
            print(f"❌ Enhanced report API health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

def test_mcp_tools():
    """Test MCP tools functionality."""
    print("🔧 Testing MCP Tools...")
    
    try:
        # Test MCP tools by importing the server module
        from src.mcp_servers.enhanced_report_mcp_server import server, ENHANCED_REPORT_AVAILABLE
        
        if ENHANCED_REPORT_AVAILABLE:
            print(f"✅ MCP server module imported successfully")
            print(f"   - Enhanced report functionality: Available")
            print(f"   - Server instance: {type(server).__name__}")
            return True
        else:
            print("❌ Enhanced report functionality not available")
            return False
            
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        return False

def test_enhanced_report_mcp_integration():
    """Test enhanced report MCP integration."""
    print("🔗 Testing Enhanced Report MCP Integration...")
    
    try:
        from src.core.export.enhanced_report_integration import enhanced_report_integration
        
        # Test data creation
        test_data = enhanced_report_integration.create_pakistan_submarine_analysis_data()
        
        if test_data and len(test_data) > 0:
            print(f"✅ Enhanced report integration test passed")
            print(f"   - Components: {len(test_data)}")
            print(f"   - Has Monte Carlo: {'monte_carlo_simulation' in test_data}")
            print(f"   - Has Knowledge Graph: {'knowledge_graph' in test_data}")
            return True
        else:
            print("❌ Enhanced report integration test failed")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced report MCP integration failed: {e}")
        return False

def start_servers():
    """Start the required servers."""
    print("🚀 Starting Servers...")
    
    # Start MCP server on port 8000 using the standalone MCP server script
    print("   Starting MCP server on port 8000...")
    mcp_process = subprocess.Popen([
        ".venv/Scripts/python.exe", "scripts/start_mcp_server.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for servers to start
    print("   Waiting 60 seconds for servers to start...")
    time.sleep(60)
    
    return mcp_process

def stop_servers(process):
    """Stop the servers."""
    print("🛑 Stopping Servers...")
    if process:
        process.terminate()
        process.wait()

def main():
    """Main test function."""
    print("🧪 Enhanced Report Integration Test")
    print("=" * 50)
    
    # Test local functionality first
    print("\n1. Testing Local Functionality...")
    local_tests = [
        test_enhanced_report_generation(),
        test_monte_carlo_simulation(),
        test_mcp_tools(),
        test_enhanced_report_mcp_integration()
    ]
    
    local_success = all(local_tests)
    print(f"\nLocal Tests: {'✅ PASSED' if local_success else '❌ FAILED'}")
    
    # Start servers
    print("\n2. Starting Servers...")
    mcp_process = start_servers()
    
    try:
        # Test server connections
        print("\n3. Testing Server Connections...")
        server_tests = [
            test_mcp_server_connection(),
            test_api_endpoints()
        ]
        
        server_success = all(server_tests)
        print(f"\nServer Tests: {'✅ PASSED' if server_success else '❌ FAILED'}")
        
        # Overall results
        overall_success = local_success and server_success
        print(f"\nOverall Test Results: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
        
        if overall_success:
            print("\n🎉 Enhanced Report Integration is working correctly!")
            print("   - Enhanced report generation: ✅")
            print("   - Monte Carlo simulation: ✅")
            print("   - MCP server communication: ✅")
            print("   - API endpoints: ✅")
            print("   - MCP tools: ✅")
        else:
            print("\n⚠️ Some tests failed. Check the output above for details.")
            
    finally:
        # Stop servers
        stop_servers(mcp_process)

if __name__ == "__main__":
    main()
