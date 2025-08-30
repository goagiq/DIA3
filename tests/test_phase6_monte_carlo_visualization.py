"""
Test script for Phase 6 Monte Carlo Visualization

This script tests the Phase 6 visualization features including:
- Interactive distribution plots
- Correlation matrix visualizations
- Scenario comparison charts
- Risk assessment dashboards
- DoD/IC specific visualizations
- Real-time dashboards
- Export capabilities
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.monte_carlo.visualization import (
    MonteCarloVisualization,
    VisualizationConfig,
    SecurityLevel,
    create_monte_carlo_visualization
)
from core.monte_carlo.engine import MonteCarloEngine
import numpy as np


async def test_visualization_creation():
    """Test basic visualization creation."""
    print("🧪 Testing visualization creation...")
    
    try:
        # Create engine and visualization instance
        engine = MonteCarloEngine()
        config = VisualizationConfig()
        viz = await create_monte_carlo_visualization(engine, config)
        
        # Generate sample data
        sample_data = np.random.normal(100, 15, 1000).tolist()
        
        # Test distribution plot
        result = await viz.create_distribution_plot(
            data=sample_data,
            title="Test Distribution Plot",
            show_stats=True
        )
        
        if "error" in result:
            print(f"❌ Distribution plot creation failed: {result['error']}")
            return False
        
        print("✅ Distribution plot created successfully")
        print(f"   - Data points: {result['metadata']['data_points']}")
        print(f"   - Mean: {result['metadata']['statistics']['mean']:.4f}")
        print(f"   - Std: {result['metadata']['statistics']['std']:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Visualization creation test failed: {e}")
        return False


async def test_correlation_matrix():
    """Test correlation matrix visualization."""
    print("\n🧪 Testing correlation matrix visualization...")
    
    try:
        engine = MonteCarloEngine()
        config = VisualizationConfig()
        viz = await create_monte_carlo_visualization(engine, config)
        
        # Create sample correlation matrix
        np.random.seed(42)
        data = np.random.randn(100, 4)
        correlation_matrix = np.corrcoef(data.T).tolist()
        variable_names = ["Variable_A", "Variable_B", "Variable_C", "Variable_D"]
        
        result = await viz.create_correlation_matrix(
            correlation_matrix=correlation_matrix,
            variable_names=variable_names,
            title="Test Correlation Matrix"
        )
        
        if "error" in result:
            print(f"❌ Correlation matrix creation failed: {result['error']}")
            return False
        
        print("✅ Correlation matrix created successfully")
        print(f"   - Matrix size: {result['metadata']['matrix_size']}")
        print(f"   - Variables: {result['metadata']['variable_names']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Correlation matrix test failed: {e}")
        return False


async def test_scenario_comparison():
    """Test scenario comparison visualization."""
    print("\n🧪 Testing scenario comparison visualization...")
    
    try:
        engine = MonteCarloEngine()
        config = VisualizationConfig()
        viz = await create_monte_carlo_visualization(engine, config)
        
        # Create sample scenario data
        np.random.seed(42)
        scenario_results = {
            "Baseline": np.random.normal(100, 10, 500).tolist(),
            "Optimistic": np.random.normal(120, 8, 500).tolist(),
            "Pessimistic": np.random.normal(80, 12, 500).tolist()
        }
        
        result = await viz.create_scenario_comparison(
            scenario_results=scenario_results,
            title="Test Scenario Comparison",
            metric_name="Performance Score"
        )
        
        if "error" in result:
            print(f"❌ Scenario comparison creation failed: {result['error']}")
            return False
        
        print("✅ Scenario comparison created successfully")
        print(f"   - Scenarios: {result['metadata']['scenarios']}")
        print(f"   - Total scenarios: {result['metadata']['total_scenarios']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Scenario comparison test failed: {e}")
        return False


async def test_risk_dashboard():
    """Test risk dashboard visualization."""
    print("\n🧪 Testing risk dashboard visualization...")
    
    try:
        engine = MonteCarloEngine()
        config = VisualizationConfig()
        viz = await create_monte_carlo_visualization(engine, config)
        
        # Create sample risk metrics
        risk_metrics = {
            "Operational Risk": 0.35,
            "Financial Risk": 0.42,
            "Strategic Risk": 0.28,
            "Compliance Risk": 0.15
        }
        
        result = await viz.create_risk_dashboard(
            risk_metrics=risk_metrics,
            title="Test Risk Assessment Dashboard"
        )
        
        if "error" in result:
            print(f"❌ Risk dashboard creation failed: {result['error']}")
            return False
        
        print("✅ Risk dashboard created successfully")
        print(f"   - Risk metrics: {result['metadata']['risk_metrics']}")
        print(f"   - Total metrics: {result['metadata']['total_metrics']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Risk dashboard test failed: {e}")
        return False


async def test_threat_assessment():
    """Test DoD/IC threat assessment visualization."""
    print("\n🧪 Testing threat assessment visualization...")
    
    try:
        engine = MonteCarloEngine()
        config = VisualizationConfig()
        viz = await create_monte_carlo_visualization(engine, config)
        
        # Create sample threat data
        threat_data = {
            "capabilities": {
                "Cyber Capability": 0.75,
                "Physical Capability": 0.45,
                "Intelligence Capability": 0.60,
                "Financial Capability": 0.30,
                "Political Capability": 0.55
            },
            "threat_level": "HIGH",
            "confidence": 0.85
        }
        
        result = await viz.create_threat_assessment_visualization(
            threat_data=threat_data,
            title="Test Threat Assessment"
        )
        
        if "error" in result:
            print(f"❌ Threat assessment creation failed: {result['error']}")
            return False
        
        print("✅ Threat assessment created successfully")
        print(f"   - Threat level: {result['metadata']['threat_level']}")
        print(f"   - Confidence: {result['metadata']['confidence']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Threat assessment test failed: {e}")
        return False


async def test_export_capabilities():
    """Test visualization export capabilities."""
    print("\n🧪 Testing export capabilities...")
    
    try:
        engine = MonteCarloEngine()
        config = VisualizationConfig()
        viz = await create_monte_carlo_visualization(engine, config)
        
        # Create a simple visualization first
        sample_data = np.random.normal(100, 15, 100).tolist()
        viz_data = await viz.create_distribution_plot(
            data=sample_data,
            title="Export Test Plot"
        )
        
        if "error" in viz_data:
            print(f"❌ Failed to create visualization for export test: {viz_data['error']}")
            return False
        
        # Test JSON export
        export_result = await viz.export_visualization(
            visualization_data=viz_data,
            format="json",
            filename="test_export"
        )
        
        if "error" in export_result:
            print(f"❌ Export failed: {export_result['error']}")
            return False
        
        print("✅ Export test successful")
        print(f"   - Format: {export_result['format']}")
        print(f"   - Filename: {export_result['filename']}")
        print(f"   - Output path: {export_result['output_path']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Export test failed: {e}")
        return False


async def test_visualization_status():
    """Test visualization status functionality."""
    print("\n🧪 Testing visualization status...")
    
    try:
        engine = MonteCarloEngine()
        config = VisualizationConfig()
        viz = await create_monte_carlo_visualization(engine, config)
        
        status = await viz.get_visualization_status()
        
        if "error" in status:
            print(f"❌ Status check failed: {status['error']}")
            return False
        
        print("✅ Visualization status retrieved successfully")
        print(f"   - Active streams: {status['active_streams']}")
        print(f"   - Cached visualizations: {status['cached_visualizations']}")
        print(f"   - Theme: {status['config']['theme']}")
        print(f"   - Security level: {status['config']['security_level']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Status test failed: {e}")
        return False


async def test_security_levels():
    """Test different security levels."""
    print("\n🧪 Testing security levels...")
    
    try:
        engine = MonteCarloEngine()
        
        # Test different security levels
        security_levels = [
            SecurityLevel.UNCLASSIFIED,
            SecurityLevel.CONFIDENTIAL,
            SecurityLevel.SECRET,
            SecurityLevel.TOP_SECRET
        ]
        
        for security_level in security_levels:
            config = VisualizationConfig(security_level=security_level)
            viz = await create_monte_carlo_visualization(engine, config)
            
            sample_data = np.random.normal(100, 15, 50).tolist()
            result = await viz.create_distribution_plot(
                data=sample_data,
                title=f"Test Plot - {security_level.value}"
            )
            
            if "error" in result:
                print(f"❌ Security level {security_level.value} failed: {result['error']}")
                return False
            
            print(f"✅ Security level {security_level.value} working")
        
        return True
        
    except Exception as e:
        print(f"❌ Security levels test failed: {e}")
        return False


async def main():
    """Run all Phase 6 visualization tests."""
    print("🚀 Starting Phase 6 Monte Carlo Visualization Tests")
    print("=" * 60)
    
    test_results = []
    
    # Run all tests
    tests = [
        ("Visualization Creation", test_visualization_creation),
        ("Correlation Matrix", test_correlation_matrix),
        ("Scenario Comparison", test_scenario_comparison),
        ("Risk Dashboard", test_risk_dashboard),
        ("Threat Assessment", test_threat_assessment),
        ("Export Capabilities", test_export_capabilities),
        ("Visualization Status", test_visualization_status),
        ("Security Levels", test_security_levels)
    ]
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            test_results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Phase 6 Visualization Test Results")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Phase 6 visualization tests passed!")
        return True
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
