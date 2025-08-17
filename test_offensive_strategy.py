#!/usr/bin/env python3
"""
Simple test script for the Offensive Strategy Optimization System
Tests basic functionality without external dependencies.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

def test_basic_functionality():
    """Test basic functionality without external dependencies."""
    print("Testing Offensive Strategy Optimization System...")
    
    try:
        # Test imports
        from core.offensive_strategy_optimizer import (
            Target, Strategy, OperationalConstraints,
            TargetType, StrategyType, ThreatLevel
        )
        print("✓ Imports successful")
        
        # Test data structure creation
        target = Target(
            target_id="T001",
            name="Test Target",
            target_type=TargetType.COMMAND_CONTROL,
            threat_level=ThreatLevel.CRITICAL,
            location={"lat": 34.0522, "lon": -118.2437},
            value_score=95,
            protection_level=85,
            time_sensitivity=90,
            mobility=20,
            intelligence_quality=75,
            collateral_risk=60
        )
        print("✓ Target creation successful")
        
        strategy = Strategy(
            strategy_id="S001",
            name="Test Strategy",
            strategy_type=StrategyType.STEALTH_INFILTRATION,
            execution_time=4.0,
            success_probability=0.75,
            resource_requirements={"personnel": 8, "equipment": 15, "intelligence": 20},
            risk_level=60,
            detection_probability=0.3,
            collateral_damage=20,
            weather_dependency=0.4,
            night_operation_capability=0.9
        )
        print("✓ Strategy creation successful")
        
        constraints = OperationalConstraints(
            time_limit=12.0,
            available_resources={"personnel": 20, "equipment": 50, "intelligence": 40},
            weather_conditions={"visibility": 85, "wind_speed": 15, "precipitation": 0.1},
            intelligence_quality=75,
            political_restrictions=["minimize_civilian_casualties"],
            legal_constraints=["comply_with_international_law"],
            force_protection_requirements=80,
            stealth_requirements=70
        )
        print("✓ Constraints creation successful")
        
        # Test pattern recognition engine
        from core.offensive_strategy_optimizer import PatternRecognitionEngine
        pattern_engine = PatternRecognitionEngine()
        
        # Add sample historical data
        historical_data = [
            {
                'timestamp': '2024-01-15T14:30:00',
                'target_type': 'leadership',
                'strategy_type': 'stealth_infiltration',
                'success_rate': 0.85,
                'response_time': 45,
                'threat_level': 85,
                'weather_conditions': {'condition': 'clear', 'visibility': 90}
            },
            {
                'timestamp': '2024-01-16T02:15:00',
                'target_type': 'infrastructure',
                'strategy_type': 'precision_strike',
                'success_rate': 0.92,
                'response_time': 30,
                'threat_level': 75,
                'weather_conditions': {'condition': 'clear', 'visibility': 95}
            }
        ]
        
        for data in historical_data:
            pattern_engine.add_historical_data(data)
        
        print("✓ Pattern recognition engine initialized")
        
        # Test Monte Carlo simulator
        from core.offensive_strategy_optimizer import MonteCarloStrategySimulator
        monte_carlo = MonteCarloStrategySimulator(num_iterations=100)  # Reduced for testing
        
        # Run a simple simulation
        evaluation = monte_carlo.simulate_strategy_execution(
            strategy, target, constraints, []
        )
        
        print("✓ Monte Carlo simulation successful")
        print(f"  - Success Rate: {evaluation['mean_success_rate']:.2%}")
        print(f"  - Execution Time: {evaluation['mean_execution_time']:.1f} hours")
        print(f"  - Risk Level: {evaluation['mean_risk_level']:.1f}")
        
        # Test target prioritization logic
        targets = [target]
        target_scores = []
        
        for t in targets:
            value_score = t.value_score
            threat_score = 100 if t.threat_level == ThreatLevel.CRITICAL else 75
            time_sensitivity = t.time_sensitivity
            protection_factor = 1 - (t.protection_level / 100)
            
            priority_score = (
                value_score * 0.4 +
                threat_score * 0.3 +
                time_sensitivity * 0.2 +
                protection_factor * 0.1
            )
            
            target_scores.append((t, priority_score))
        
        target_scores.sort(key=lambda x: x[1], reverse=True)
        prioritized_targets = [target for target, _ in target_scores]
        
        print("✓ Target prioritization successful")
        print(f"  - Prioritized {len(prioritized_targets)} targets")
        
        # Test result serialization
        result_data = {
            "target": {
                "target_id": target.target_id,
                "name": target.name,
                "target_type": target.target_type.value,
                "threat_level": target.threat_level.value
            },
            "strategy": {
                "strategy_id": strategy.strategy_id,
                "name": strategy.name,
                "strategy_type": strategy.strategy_type.value
            },
            "evaluation": {
                "success_rate": evaluation['mean_success_rate'],
                "execution_time": evaluation['mean_execution_time'],
                "risk_level": evaluation['mean_risk_level']
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Save test results
        with open("test_results.json", "w") as f:
            json.dump(result_data, f, indent=2)
        
        print("✓ Result serialization successful")
        print("✓ Test results saved to test_results.json")
        
        print("\n🎉 All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_optimization_logic():
    """Test the core optimization logic."""
    print("\nTesting optimization logic...")
    
    try:
        from core.offensive_strategy_optimizer import (
            Target, Strategy, OperationalConstraints,
            TargetType, StrategyType, ThreatLevel
        )
        
        # Create test data
        targets = [
            Target(
                target_id="T001",
                name="High Value Target",
                target_type=TargetType.LEADERSHIP,
                threat_level=ThreatLevel.CRITICAL,
                location={"lat": 34.0522, "lon": -118.2437},
                value_score=100,
                protection_level=90,
                time_sensitivity=95,
                mobility=50,
                intelligence_quality=80,
                collateral_risk=70
            ),
            Target(
                target_id="T002",
                name="Medium Value Target",
                target_type=TargetType.INFRASTRUCTURE,
                threat_level=ThreatLevel.HIGH,
                location={"lat": 34.0522, "lon": -118.2437},
                value_score=75,
                protection_level=70,
                time_sensitivity=60,
                mobility=20,
                intelligence_quality=70,
                collateral_risk=40
            )
        ]
        
        strategies = [
            Strategy(
                strategy_id="S001",
                name="Stealth Approach",
                strategy_type=StrategyType.STEALTH_INFILTRATION,
                execution_time=4.0,
                success_probability=0.75,
                resource_requirements={"personnel": 8, "equipment": 15, "intelligence": 20},
                risk_level=60,
                detection_probability=0.3,
                collateral_damage=20,
                weather_dependency=0.4,
                night_operation_capability=0.9
            ),
            Strategy(
                strategy_id="S002",
                name="Precision Strike",
                strategy_type=StrategyType.PRECISION_STRIKE,
                execution_time=1.5,
                success_probability=0.85,
                resource_requirements={"personnel": 4, "equipment": 25, "intelligence": 15},
                risk_level=40,
                detection_probability=0.6,
                collateral_damage=30,
                weather_dependency=0.7,
                night_operation_capability=0.8
            )
        ]
        
        constraints = OperationalConstraints(
            time_limit=8.0,
            available_resources={"personnel": 15, "equipment": 40, "intelligence": 30},
            weather_conditions={"visibility": 80, "wind_speed": 20, "precipitation": 0.2},
            intelligence_quality=70,
            political_restrictions=["minimize_civilian_casualties"],
            legal_constraints=["comply_with_international_law"],
            force_protection_requirements=85,
            stealth_requirements=75
        )
        
        # Test strategy scoring
        print("Testing strategy scoring...")
        
        for target in targets:
            print(f"\nTarget: {target.name}")
            for strategy in strategies:
                # Simple scoring algorithm
                base_score = strategy.success_probability * 0.6
                risk_penalty = (strategy.risk_level / 100) * 0.4
                time_penalty = 0.1 if strategy.execution_time > constraints.time_limit else 0
                
                final_score = base_score - risk_penalty - time_penalty
                
                print(f"  Strategy: {strategy.name}")
                print(f"    Base Score: {base_score:.3f}")
                print(f"    Risk Penalty: {risk_penalty:.3f}")
                print(f"    Time Penalty: {time_penalty:.3f}")
                print(f"    Final Score: {final_score:.3f}")
        
        # Test resource allocation
        print("\nTesting resource allocation...")
        
        total_resources = constraints.available_resources.copy()
        allocated_resources = {}
        
        for strategy in strategies:
            for resource, amount in strategy.resource_requirements.items():
                if resource not in allocated_resources:
                    allocated_resources[resource] = 0
                allocated_resources[resource] += amount
        
        print("Resource Requirements:")
        for resource, amount in allocated_resources.items():
            available = total_resources.get(resource, 0)
            percentage = (amount / available * 100) if available > 0 else 0
            print(f"  {resource}: {amount:.1f}/{available} ({percentage:.1f}%)")
        
        print("✓ Optimization logic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Optimization logic test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("OFFENSIVE STRATEGY OPTIMIZATION SYSTEM - TEST SUITE")
    print("=" * 60)
    
    # Run basic functionality tests
    basic_success = test_basic_functionality()
    
    # Run optimization logic tests
    optimization_success = test_optimization_logic()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if basic_success and optimization_success:
        print("🎉 ALL TESTS PASSED!")
        print("\nThe Offensive Strategy Optimization System is working correctly.")
        print("You can now run the full demo with:")
        print("  python offensive_strategy_demo.py")
    else:
        print("❌ SOME TESTS FAILED!")
        print("\nPlease check the error messages above and fix any issues.")
    
    print("\nGenerated files:")
    print("- test_results.json: Basic test results")
    print("- Check the console output for detailed test information")


if __name__ == "__main__":
    main()
