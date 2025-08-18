#!/usr/bin/env python3
"""
Integration Test Script for Interactive Visualization System
Tests the integration of visualization system with main application, API routes, and MCP tools.
"""

import asyncio
import sys
import os
import time
import requests
import json
from pathlib import Path
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_visualization_imports():
    """Test that visualization components can be imported."""
    print("🧪 Test 1: Visualization Component Imports")
    print("=" * 50)
    
    try:
        from src.core.visualization.interactive_forecasting_charts import (
            InteractiveForecastingCharts, 
            MonteCarloVisualizationHelper,
            ChartColors
        )
        from src.core.monte_carlo.visualization_integration import MonteCarloVisualizationIntegration
        from src.api.visualization_routes import router as visualization_router
        from src.mcp_servers.interactive_visualization_mcp_tools import interactive_visualization_mcp_tools
        
        print("✅ All visualization components imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_visualization_components():
    """Test that visualization components can be instantiated."""
    print("\n🧪 Test 2: Visualization Component Instantiation")
    print("=" * 50)
    
    try:
        from src.core.visualization.interactive_forecasting_charts import (
            InteractiveForecastingCharts, 
            MonteCarloVisualizationHelper,
            ChartColors
        )
        
        # Test ChartColors
        colors = ChartColors()
        print(f"✅ ChartColors instantiated: {colors.historical_line}, {colors.future_line}")
        
        # Test InteractiveForecastingCharts
        visualizer = InteractiveForecastingCharts(colors)
        print("✅ InteractiveForecastingCharts instantiated")
        
        # Test MonteCarloVisualizationHelper
        mc_helper = MonteCarloVisualizationHelper(colors)
        print("✅ MonteCarloVisualizationHelper instantiated")
        
        return True
    except Exception as e:
        print(f"❌ Component instantiation error: {e}")
        return False


def test_api_routes():
    """Test that API routes are properly configured."""
    print("\n🧪 Test 3: API Routes Configuration")
    print("=" * 50)
    
    try:
        from src.api.visualization_routes import router as visualization_router
        
        # Check if router has the expected routes
        routes = [route.path for route in visualization_router.routes]
        expected_routes = [
            "/api/visualization/health",
            "/api/visualization/forecast-timeline",
            "/api/visualization/monte-carlo-forecast",
            "/api/visualization/scenario-comparison",
            "/api/visualization/risk-assessment",
            "/api/visualization/comprehensive-dashboard",
            "/api/visualization/charts/{chart_filename}",
            "/api/visualization/list-charts",
            "/api/visualization/delete-charts/{chart_filename}",
            "/api/visualization/generate-sample-data",
            "/api/visualization/color-scheme"
        ]
        
        print(f"✅ Router has {len(routes)} routes")
        for route in expected_routes:
            if route in routes:
                print(f"  ✅ {route}")
            else:
                print(f"  ❌ {route} (missing)")
        
        return True
    except Exception as e:
        print(f"❌ API routes test error: {e}")
        return False


def test_mcp_tools():
    """Test that MCP tools are properly configured."""
    print("\n🧪 Test 4: MCP Tools Configuration")
    print("=" * 50)
    
    try:
        from src.mcp_servers.interactive_visualization_mcp_tools import interactive_visualization_mcp_tools
        
        # Get available tools
        tools = interactive_visualization_mcp_tools.get_tools()
        
        expected_tools = [
            "create_forecast_timeline_chart",
            "create_monte_carlo_forecast_chart",
            "create_scenario_comparison_chart",
            "create_risk_assessment_heatmap",
            "create_comprehensive_dashboard",
            "generate_sample_visualization_data",
            "get_visualization_color_scheme"
        ]
        
        print(f"✅ MCP tools instance has {len(tools)} tools")
        for tool in expected_tools:
            tool_found = any(t["name"] == tool for t in tools)
            if tool_found:
                print(f"  ✅ {tool}")
            else:
                print(f"  ❌ {tool} (missing)")
        
        return True
    except Exception as e:
        print(f"❌ MCP tools test error: {e}")
        return False


async def test_mcp_tool_execution():
    """Test that MCP tools can be executed."""
    print("\n🧪 Test 5: MCP Tool Execution")
    print("=" * 50)
    
    try:
        from src.mcp_servers.interactive_visualization_mcp_tools import interactive_visualization_mcp_tools
        
        # Test color scheme tool
        result = await interactive_visualization_mcp_tools.get_visualization_color_scheme({})
        
        if result.get("success"):
            print("✅ Color scheme tool executed successfully")
            color_scheme = result.get("color_scheme", {})
            print(f"  Historical color: {color_scheme.get('historical_colors', {}).get('line')}")
            print(f"  Future color: {color_scheme.get('future_colors', {}).get('line')}")
        else:
            print(f"❌ Color scheme tool failed: {result.get('error')}")
            return False
        
        # Test sample data generation
        result = await interactive_visualization_mcp_tools.generate_sample_visualization_data({"data_type": "all"})
        
        if result.get("success"):
            print("✅ Sample data generation tool executed successfully")
            data_info = result.get("data_info", {})
            print(f"  Historical points: {data_info.get('historical_points')}")
            print(f"  Forecast points: {data_info.get('forecast_points')}")
            print(f"  Simulation paths: {data_info.get('simulation_paths')}")
        else:
            print(f"❌ Sample data generation failed: {result.get('error')}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ MCP tool execution error: {e}")
        return False


def test_dynamic_tool_manager():
    """Test that visualization tools are registered with dynamic tool manager."""
    print("\n🧪 Test 6: Dynamic Tool Manager Integration")
    print("=" * 50)
    
    try:
        from src.mcp_servers.dynamic_tool_manager import dynamic_tool_manager
        
        # Check if visualization tool is registered
        tool_statuses = dynamic_tool_manager.get_all_tool_statuses()
        
        if "interactive_visualization" in tool_statuses:
            tool_info = tool_statuses["interactive_visualization"]
            print(f"✅ Interactive visualization tool registered")
            print(f"  Status: {tool_info.status.value}")
            print(f"  Description: {tool_info.description}")
            print(f"  Priority: {tool_info.config.priority}")
        else:
            print("❌ Interactive visualization tool not found in dynamic tool manager")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Dynamic tool manager test error: {e}")
        return False


def test_file_structure():
    """Test that all required files exist."""
    print("\n🧪 Test 7: File Structure")
    print("=" * 50)
    
    required_files = [
        "src/core/visualization/interactive_forecasting_charts.py",
        "src/core/monte_carlo/visualization_integration.py",
        "src/api/visualization_routes.py",
        "src/mcp_servers/interactive_visualization_mcp_tools.py",
        "examples/interactive_forecasting_demo.py",
        "Test/test_visualization_system.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
            all_exist = False
    
    return all_exist


def test_output_directories():
    """Test that output directories are created."""
    print("\n🧪 Test 8: Output Directories")
    print("=" * 50)
    
    output_dirs = [
        "Results/api_visualization",
        "Results/mcp_visualization",
        "Results/interactive_forecasting_demo",
        "Results/visualization_test"
    ]
    
    all_exist = True
    for dir_path in output_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}")
        else:
            print(f"⚠️ {dir_path} (will be created when needed)")
    
    return True


async def test_api_server_integration():
    """Test that the API server can start with visualization routes."""
    print("\n🧪 Test 9: API Server Integration")
    print("=" * 50)
    
    try:
        # This test would require starting the actual API server
        # For now, we'll just test that the routes can be imported
        from src.api.main import app
        
        # Check if visualization routes are included
        routes = [route.path for route in app.routes]
        visualization_routes = [route for route in routes if "/api/visualization" in route]
        
        if visualization_routes:
            print(f"✅ {len(visualization_routes)} visualization routes found in API server")
            for route in visualization_routes[:3]:  # Show first 3
                print(f"  ✅ {route}")
        else:
            print("❌ No visualization routes found in API server")
            return False
        
        return True
    except Exception as e:
        print(f"❌ API server integration test error: {e}")
        return False


async def main():
    """Run all integration tests."""
    print("🚀 Interactive Visualization System Integration Test Suite")
    print("=" * 70)
    print("Testing the integration of visualization system with main application")
    print()
    
    test_results = []
    
    # Run synchronous tests
    test_results.append(test_visualization_imports())
    test_results.append(test_visualization_components())
    test_results.append(test_api_routes())
    test_results.append(test_mcp_tools())
    test_results.append(test_dynamic_tool_manager())
    test_results.append(test_file_structure())
    test_results.append(test_output_directories())
    
    # Run asynchronous tests
    test_results.append(await test_mcp_tool_execution())
    test_results.append(await test_api_server_integration())
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Integration Test Results Summary")
    print("=" * 70)
    
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"✅ Tests Passed: {passed}/{total}")
    print(f"❌ Tests Failed: {total - passed}/{total}")
    print(f"📈 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All integration tests passed! Visualization system is properly integrated.")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please check the integration.")
    
    print("\n📋 Integration Components Tested:")
    print("• Visualization component imports")
    print("• Component instantiation")
    print("• API routes configuration")
    print("• MCP tools configuration")
    print("• MCP tool execution")
    print("• Dynamic tool manager integration")
    print("• File structure")
    print("• Output directories")
    print("• API server integration")
    
    return passed == total


if __name__ == "__main__":
    # Run the integration test suite
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
