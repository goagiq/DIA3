#!/usr/bin/env python3
"""
Enhanced Report System Startup Script
Starts the complete enhanced report system with MCP server and API integration.
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def start_mcp_server():
    """Start the MCP server on port 8000."""
    print("🚀 Starting MCP Server on port 8000...")
    
    try:
        # Start MCP server using main.py
        mcp_process = subprocess.Popen([
            ".venv/Scripts/python.exe", "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ MCP server process started")
        return mcp_process
        
    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")
        return None

def start_api_server():
    """Start the API server on port 8001."""
    print("🌐 Starting API Server on port 8001...")
    
    try:
        # Start API server using uvicorn
        api_process = subprocess.Popen([
            ".venv/Scripts/python.exe", "-m", "uvicorn", 
            "src.api.main:app", "--host", "0.0.0.0", "--port", "8001"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ API server process started")
        return api_process
        
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None

def test_enhanced_report_functionality():
    """Test the enhanced report functionality."""
    print("🧪 Testing Enhanced Report Functionality...")
    
    try:
        # Test enhanced report generation
        result = subprocess.run([
            ".venv/Scripts/python.exe", "-c",
            "from src.core.export.enhanced_report_integration import generate_enhanced_report; "
            "result = generate_enhanced_report('pakistan_submarine', "
            "'Pakistan\\'s 50-Submarine Acquisition Analysis', "
            "'Strategic Implications for Conventional Deterrence'); "
            "print(f'Enhanced report generated: {result}')"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Enhanced report generation test passed")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Enhanced report generation test failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced report functionality test failed: {e}")
        return False

def test_monte_carlo_simulation():
    """Test Monte Carlo simulation functionality."""
    print("🎲 Testing Monte Carlo Simulation...")
    
    try:
        # Test Monte Carlo simulation
        result = subprocess.run([
            ".venv/Scripts/python.exe", "-c",
            "from src.core.analysis.monte_carlo_simulator import MonteCarloSimulator; "
            "simulator = MonteCarloSimulator(n_iterations=1000); "
            "simulator.create_pakistan_submarine_simulation(); "
            "viz_data = simulator.create_visualization_data(); "
            "print(f'Monte Carlo simulation completed with {len(viz_data)} components')"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Monte Carlo simulation test passed")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Monte Carlo simulation test failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Monte Carlo simulation test failed: {e}")
        return False

def test_mcp_tools():
    """Test MCP tools functionality."""
    print("🔧 Testing MCP Tools...")
    
    try:
        # Test MCP tools
        result = subprocess.run([
            ".venv/Scripts/python.exe", "-c",
            "from src.mcp_servers.enhanced_report_mcp_server import server, ENHANCED_REPORT_AVAILABLE; "
            "print(f'Enhanced report available: {ENHANCED_REPORT_AVAILABLE}'); "
            "print(f'Server type: {type(server).__name__}')"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ MCP tools test passed")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ MCP tools test failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        return False

def main():
    """Main startup function."""
    print("🚀 Enhanced Report System Startup")
    print("=" * 50)
    
    # Test local functionality first
    print("\n1. Testing Local Functionality...")
    local_tests = [
        test_enhanced_report_functionality(),
        test_monte_carlo_simulation(),
        test_mcp_tools()
    ]
    
    local_success = all(local_tests)
    print(f"\nLocal Tests: {'✅ PASSED' if local_success else '❌ FAILED'}")
    
    if not local_success:
        print("❌ Local tests failed. Please check the errors above.")
        return
    
    # Start servers
    print("\n2. Starting Servers...")
    mcp_process = start_mcp_server()
    api_process = start_api_server()
    
    if not mcp_process or not api_process:
        print("❌ Failed to start servers. Exiting.")
        return
    
    # Wait for servers to start
    print("\n3. Waiting for servers to start (60 seconds)...")
    time.sleep(60)
    
    print("\n4. Server Status:")
    print("   - MCP Server: http://localhost:8000")
    print("   - API Server: http://localhost:8001")
    print("   - MCP Health: http://localhost:8000/mcp-health")
    print("   - API Health: http://localhost:8001/api/v1/reports/health")
    
    print("\n5. Available Endpoints:")
    print("   - MCP Tools: http://localhost:8000/mcp")
    print("   - Enhanced Reports: http://localhost:8001/api/v1/reports")
    print("   - Monte Carlo: http://localhost:8001/api/v1/monte-carlo")
    
    print("\n6. Test Commands:")
    print("   - MCP Client Test: .venv/Scripts/python.exe test_mcp_client_enhanced_report.py")
    print("   - Integration Test: .venv/Scripts/python.exe test_enhanced_report_integration.py")
    print("   - Enhanced Report Demo: .venv/Scripts/python.exe examples/monte_carlo_simulation_demo.py")
    
    print("\n🎉 Enhanced Report System is running!")
    print("Press Ctrl+C to stop the servers...")
    
    try:
        # Keep the servers running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        
        if mcp_process:
            mcp_process.terminate()
            mcp_process.wait()
            print("✅ MCP server stopped")
            
        if api_process:
            api_process.terminate()
            api_process.wait()
            print("✅ API server stopped")
            
        print("✅ All servers stopped")

if __name__ == "__main__":
    main()
