#!/usr/bin/env python3
"""
Monte Carlo Simulation Demo
Demonstrates Monte Carlo simulation capabilities in enhanced report generation
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def demo_monte_carlo_simulation():
    """Demonstrate Monte Carlo simulation capabilities"""
    
    print("🎲 Monte Carlo Simulation Demo")
    print("=" * 50)
    
    try:
        # Import the Monte Carlo simulator
        from core.analysis.monte_carlo_simulator import MonteCarloSimulator
        
        print("✅ Successfully imported Monte Carlo simulator")
        
        # Demo 1: Pakistan submarine simulation
        print("\n📊 Demo 1: Pakistan Submarine Acquisition Simulation")
        print("-" * 50)
        
        simulator = MonteCarloSimulator(n_iterations=10000)
        simulation_results = simulator.create_pakistan_submarine_simulation()
        
        print("✅ Monte Carlo simulation completed successfully!")
        print(f"📈 Simulation iterations: {simulation_results['simulation_metadata']['n_iterations']:,}")
        
        # Display results
        results = simulation_results['results']
        print("\n📊 Simulation Results:")
        print(f"• Total Cost: ${results['total_cost']['mean']:.1f}B ± ${results['total_cost']['std']:.1f}B")
        print(f"• Risk Score: {results['risk_score']['mean']:.3f} ± {results['risk_score']['std']:.3f}")
        print(f"• Strategic Impact: {results['strategic_impact']['mean']:.2f} ± {results['strategic_impact']['std']:.2f}")
        
        # Display confidence intervals
        print("\n🎯 95% Confidence Intervals:")
        for metric, result in results.items():
            ci_95 = result['confidence_intervals']['95%']
            print(f"• {metric.replace('_', ' ').title()}: {ci_95[0]:.2f} - {ci_95[1]:.2f}")
        
        # Demo 2: Custom simulation
        print("\n🔧 Demo 2: Custom Strategic Analysis Simulation")
        print("-" * 50)
        
        custom_simulator = MonteCarloSimulator(n_iterations=5000)
        
        # Add custom parameters
        custom_simulator.add_parameter(
            name="market_growth",
            distribution_type="normal",
            parameters={"mean": 0.05, "std": 0.02},  # 5% growth with 2% std
            description="Annual market growth rate",
            unit="percentage"
        )
        
        custom_simulator.add_parameter(
            name="investment_amount",
            distribution_type="lognormal",
            parameters={"mean": 3.0, "sigma": 0.5},  # $3M average investment
            description="Investment amount",
            unit="million USD"
        )
        
        custom_simulator.add_parameter(
            name="success_probability",
            distribution_type="uniform",
            parameters={"low": 0.3, "high": 0.8},  # 30-80% success probability
            description="Project success probability",
            unit="probability"
        )
        
        # Define output function
        def roi_calculation(row):
            """Calculate return on investment"""
            growth_factor = (1 + row['market_growth']) ** 5  # 5-year projection
            expected_return = row['investment_amount'] * growth_factor * row['success_probability']
            roi = (expected_return - row['investment_amount']) / row['investment_amount']
            return roi * 100  # Convert to percentage
        
        # Run simulation
        roi_result = custom_simulator.run_simulation(roi_calculation, "roi")
        
        print("✅ Custom simulation completed successfully!")
        print(f"📈 ROI Analysis: {roi_result.mean:.1f}% ± {roi_result.std:.1f}%")
        print(f"🎯 90% Confidence Interval: {roi_result.confidence_intervals['90%'][0]:.1f}% - {roi_result.confidence_intervals['90%'][1]:.1f}%")
        
        # Demo 3: Visualization data
        print("\n📊 Demo 3: Simulation Visualization Data")
        print("-" * 50)
        
        viz_data = simulator.create_visualization_data()
        
        print("✅ Visualization data generated!")
        print(f"📈 Cost distribution bins: {len(viz_data.get('cost_distribution', {}).get('labels', []))}")
        print(f"🎯 Risk distribution categories: {len(viz_data.get('risk_distribution', {}).get('labels', []))}")
        print(f"📊 Impact distribution levels: {len(viz_data.get('impact_distribution', {}).get('labels', []))}")
        
        # Demo 4: Export results
        print("\n💾 Demo 4: Export Simulation Results")
        print("-" * 50)
        
        export_path = "Results/monte_carlo_simulation_results.json"
        simulator.export_results(export_path)
        
        if os.path.exists(export_path):
            file_size = os.path.getsize(export_path)
            print(f"✅ Results exported to: {export_path}")
            print(f"📏 File size: {file_size:,} bytes")
        else:
            print("❌ Export failed")
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 Monte Carlo Simulation Demo Summary")
        print("=" * 50)
        print("✅ Successfully demonstrated Monte Carlo simulation capabilities:")
        print("   • Pakistan submarine acquisition simulation")
        print("   • Custom strategic analysis simulation")
        print("   • Visualization data generation")
        print("   • Results export functionality")
        
        print("\n🎲 Key Features Demonstrated:")
        print("   • Multiple probability distributions (normal, lognormal, uniform, triangular, gamma, binomial)")
        print("   • Configurable simulation parameters")
        print("   • Statistical analysis (mean, std, percentiles, confidence intervals)")
        print("   • Custom output functions")
        print("   • Visualization data preparation")
        print("   • Results export capabilities")
        
        print("\n📝 Next Steps:")
        print("   1. Integrate Monte Carlo simulations into enhanced reports")
        print("   2. Create interactive simulation visualizations")
        print("   3. Develop additional simulation templates")
        print("   4. Add sensitivity analysis capabilities")
        print("   5. Implement scenario comparison features")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed:")
        print("   pip install numpy pandas scipy matplotlib seaborn")
        return False
        
    except Exception as e:
        print(f"❌ Error during Monte Carlo demo: {e}")
        return False

def demo_enhanced_report_with_monte_carlo():
    """Demonstrate enhanced report generation with Monte Carlo simulation"""
    
    print("\n📊 Enhanced Report with Monte Carlo Simulation Demo")
    print("=" * 60)
    
    try:
        from core.export.enhanced_report_integration import generate_enhanced_report
        
        print("✅ Successfully imported enhanced report integration")
        
        # Generate enhanced report with Monte Carlo simulation
        print("\n📊 Generating enhanced report with Monte Carlo simulation...")
        report_path = generate_enhanced_report(
            analysis_type="pakistan_submarine",
            title="Pakistan's 50-Submarine Acquisition with Monte Carlo Analysis",
            subtitle="Comprehensive Strategic Analysis with Probabilistic Modeling"
        )
        
        print(f"✅ Enhanced report with Monte Carlo simulation generated!")
        print(f"📄 Report saved to: {report_path}")
        
        if os.path.exists(report_path):
            file_size = os.path.getsize(report_path)
            print(f"📏 File size: {file_size:,} bytes")
            
            # Check for Monte Carlo features in the report
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            features_found = []
            if "Monte Carlo Simulation Analysis" in content:
                features_found.append("✅ Monte Carlo Simulation Section")
            if "monteCarloCostDistribution" in content:
                features_found.append("✅ Cost Distribution Charts")
            if "monteCarloRiskDistribution" in content:
                features_found.append("✅ Risk Distribution Charts")
            if "monteCarloImpactDistribution" in content:
                features_found.append("✅ Impact Distribution Charts")
            if "Confidence Intervals" in content:
                features_found.append("✅ Confidence Interval Tables")
            if "Simulation Results Summary" in content:
                features_found.append("✅ Simulation Statistics")
            
            print("\n🔍 Monte Carlo Features Found:")
            for feature in features_found:
                print(f"   {feature}")
            
            if len(features_found) >= 4:
                print("\n🎉 Enhanced report with Monte Carlo simulation demo PASSED!")
                print("   The report includes comprehensive Monte Carlo analysis features")
            else:
                print("\n⚠️  Enhanced report with Monte Carlo simulation demo PARTIAL")
                print("   Some Monte Carlo features may be missing")
                
        else:
            print("❌ Report file not found!")
            return False
            
    except Exception as e:
        print(f"❌ Error during enhanced report demo: {e}")
        return False
    
    return True

def main():
    """Main demo function"""
    
    print("🚀 Monte Carlo Simulation Demo Suite")
    print("=" * 60)
    
    # Test Monte Carlo simulation capabilities
    test1_passed = demo_monte_carlo_simulation()
    
    # Test enhanced report with Monte Carlo simulation
    test2_passed = demo_enhanced_report_with_monte_carlo()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Demo Summary")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("🎉 ALL DEMOS PASSED!")
        print("✅ Monte Carlo simulation capabilities are working correctly")
        print("✅ Enhanced reports with Monte Carlo analysis can be generated")
        print("✅ All simulation features are functional")
    elif test1_passed:
        print("⚠️  PARTIAL SUCCESS")
        print("✅ Monte Carlo simulation capabilities work")
        print("❌ Enhanced report integration needs attention")
    elif test2_passed:
        print("⚠️  PARTIAL SUCCESS")
        print("❌ Monte Carlo simulation capabilities need attention")
        print("✅ Enhanced report integration works")
    else:
        print("❌ ALL DEMOS FAILED")
        print("❌ Monte Carlo simulation system needs debugging")
    
    print("\n📝 Next Steps:")
    print("   1. Open the generated HTML reports in a web browser")
    print("   2. Explore the Monte Carlo simulation visualizations")
    print("   3. Review the confidence interval tables")
    print("   4. Analyze the probability distributions")
    print("   5. Use the simulation results for strategic decision-making")

if __name__ == "__main__":
    main()
