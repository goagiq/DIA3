#!/usr/bin/env python3
"""
Offensive Strategy Optimization Demo
Demonstrates the comprehensive offensive strategy optimization system that combines
pattern recognition and Monte Carlo simulation to identify optimal strategies for
eliminating high-value targets under time constraints.
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from core.offensive_strategy_optimizer import (
    OffensiveStrategyOptimizer,
    Target, Strategy, OperationalConstraints,
    TargetType, StrategyType, ThreatLevel,
    create_sample_targets, create_sample_strategies, create_sample_constraints
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('offensive_strategy_demo.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class OffensiveStrategyDemo:
    """Demonstration class for offensive strategy optimization."""
    
    def __init__(self):
        self.optimizer = OffensiveStrategyOptimizer()
        self.results = []
        
    async def run_basic_demo(self):
        """Run basic demonstration with sample data."""
        logger.info("=== OFFENSIVE STRATEGY OPTIMIZATION DEMO ===")
        logger.info("Starting basic demonstration...")
        
        # Create sample data
        targets = create_sample_targets()
        strategies = create_sample_strategies()
        constraints = create_sample_constraints()
        
        # Display input data
        self._display_input_data(targets, strategies, constraints)
        
        # Run optimization
        logger.info("Running strategy optimization...")
        result = await self._run_optimization(targets, strategies, constraints)
        
        # Display results
        self._display_results(result)
        
        # Generate visualization
        self.optimizer.generate_visualization(result)
        
        return result
    
    async def run_advanced_scenarios(self):
        """Run advanced scenarios with different constraints."""
        logger.info("\n=== ADVANCED SCENARIOS ===")
        
        scenarios = [
            {
                "name": "Time-Critical Operation",
                "constraints": OperationalConstraints(
                    time_limit=6.0,  # 6 hours
                    available_resources={"personnel": 15, "equipment": 30, "intelligence": 25},
                    weather_conditions={"visibility": 70, "wind_speed": 25, "precipitation": 0.3},
                    intelligence_quality=60,
                    political_restrictions=["minimize_civilian_casualties", "stealth_required"],
                    legal_constraints=["comply_with_international_law"],
                    force_protection_requirements=90,
                    stealth_requirements=85
                )
            },
            {
                "name": "High-Resource Operation",
                "constraints": OperationalConstraints(
                    time_limit=24.0,  # 24 hours
                    available_resources={"personnel": 50, "equipment": 100, "intelligence": 80},
                    weather_conditions={"visibility": 95, "wind_speed": 10, "precipitation": 0.0},
                    intelligence_quality=90,
                    political_restrictions=["minimize_civilian_casualties"],
                    legal_constraints=["comply_with_international_law"],
                    force_protection_requirements=70,
                    stealth_requirements=50
                )
            },
            {
                "name": "Stealth-Focused Operation",
                "constraints": OperationalConstraints(
                    time_limit=8.0,  # 8 hours
                    available_resources={"personnel": 12, "equipment": 20, "intelligence": 35},
                    weather_conditions={"visibility": 80, "wind_speed": 15, "precipitation": 0.1},
                    intelligence_quality=85,
                    political_restrictions=["absolute_stealth", "zero_civilian_casualties"],
                    legal_constraints=["comply_with_international_law", "deniability_required"],
                    force_protection_requirements=95,
                    stealth_requirements=95
                )
            }
        ]
        
        for scenario in scenarios:
            logger.info(f"\nRunning scenario: {scenario['name']}")
            
            targets = create_sample_targets()
            strategies = create_sample_strategies()
            
            result = await self._run_optimization(targets, strategies, scenario['constraints'])
            
            logger.info(f"Scenario {scenario['name']} Results:")
            logger.info(f"  Success Rate: {result.expected_success_rate:.2%}")
            logger.info(f"  Total Risk: {result.risk_assessment['total_risk']:.1f}")
            logger.info(f"  Execution Time: {result.execution_time:.2f} seconds")
            
            self.results.append({
                "scenario": scenario['name'],
                "result": result
            })
    
    async def run_pattern_analysis_demo(self):
        """Demonstrate pattern recognition capabilities."""
        logger.info("\n=== PATTERN RECOGNITION DEMO ===")
        
        # Add more historical data to demonstrate pattern recognition
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
            },
            {
                'timestamp': '2024-01-17T10:00:00',
                'target_type': 'leadership',
                'strategy_type': 'cyber_attack',
                'success_rate': 0.78,
                'response_time': 60,
                'threat_level': 90,
                'weather_conditions': {'condition': 'rainy', 'visibility': 40}
            },
            {
                'timestamp': '2024-01-18T03:30:00',
                'target_type': 'military_asset',
                'strategy_type': 'precision_strike',
                'success_rate': 0.88,
                'response_time': 25,
                'threat_level': 70,
                'weather_conditions': {'condition': 'clear', 'visibility': 85}
            },
            {
                'timestamp': '2024-01-19T22:00:00',
                'target_type': 'leadership',
                'strategy_type': 'stealth_infiltration',
                'success_rate': 0.82,
                'response_time': 50,
                'threat_level': 88,
                'weather_conditions': {'condition': 'clear', 'visibility': 92}
            }
        ]
        
        # Add data to pattern engine
        for data in historical_data:
            self.optimizer.pattern_engine.add_historical_data(data)
        
        # Analyze patterns
        logger.info("Analyzing historical patterns...")
        
        for target_type in TargetType:
            temporal_patterns = self.optimizer.pattern_engine.identify_temporal_patterns(target_type)
            behavioral_patterns = self.optimizer.pattern_engine.identify_behavioral_patterns(target_type)
            
            if temporal_patterns:
                logger.info(f"Temporal patterns for {target_type.value}:")
                for pattern in temporal_patterns:
                    logger.info(f"  - {pattern.pattern_type}: confidence={pattern.confidence:.2f}")
            
            if behavioral_patterns:
                logger.info(f"Behavioral patterns for {target_type.value}:")
                for pattern in behavioral_patterns:
                    logger.info(f"  - {pattern.pattern_type}: confidence={pattern.confidence:.2f}")
        
        environmental_patterns = self.optimizer.pattern_engine.identify_environmental_patterns()
        if environmental_patterns:
            logger.info("Environmental patterns:")
            for pattern in environmental_patterns:
                logger.info(f"  - {pattern.pattern_type}: confidence={pattern.confidence:.2f}")
    
    async def run_monte_carlo_demo(self):
        """Demonstrate Monte Carlo simulation capabilities."""
        logger.info("\n=== MONTE CARLO SIMULATION DEMO ===")
        
        targets = create_sample_targets()
        strategies = create_sample_strategies()
        constraints = create_sample_constraints()
        
        # Run detailed Monte Carlo analysis
        logger.info("Running detailed Monte Carlo simulations...")
        
        for target in targets:
            logger.info(f"\nAnalyzing target: {target.name}")
            
            for strategy in strategies:
                logger.info(f"  Strategy: {strategy.name}")
                
                # Run simulation
                evaluation = self.optimizer.monte_carlo_simulator.simulate_strategy_execution(
                    strategy, target, constraints, []
                )
                
                logger.info(f"    Success Rate: {evaluation['mean_success_rate']:.2%} ± {evaluation['success_rate_std']:.2%}")
                logger.info(f"    Execution Time: {evaluation['mean_execution_time']:.1f} ± {evaluation['execution_time_std']:.1f} hours")
                logger.info(f"    Risk Level: {evaluation['mean_risk_level']:.1f}")
                logger.info(f"    Detection Probability: {evaluation['mean_detection_probability']:.2%}")
                logger.info(f"    Collateral Damage: {evaluation['mean_collateral_damage']:.1f}")
    
    async def run_sensitivity_analysis(self):
        """Run sensitivity analysis on key parameters."""
        logger.info("\n=== SENSITIVITY ANALYSIS ===")
        
        targets = create_sample_targets()
        strategies = create_sample_strategies()
        base_constraints = create_sample_constraints()
        
        # Test different time constraints
        time_constraints = [4.0, 8.0, 12.0, 16.0, 20.0]
        
        logger.info("Testing sensitivity to time constraints...")
        for time_limit in time_constraints:
            constraints = OperationalConstraints(
                time_limit=time_limit,
                available_resources=base_constraints.available_resources,
                weather_conditions=base_constraints.weather_conditions,
                intelligence_quality=base_constraints.intelligence_quality,
                political_restrictions=base_constraints.political_restrictions,
                legal_constraints=base_constraints.legal_constraints,
                force_protection_requirements=base_constraints.force_protection_requirements,
                stealth_requirements=base_constraints.stealth_requirements
            )
            
            result = await self._run_optimization(targets, strategies, constraints)
            
            logger.info(f"Time Limit: {time_limit}h - Success Rate: {result.expected_success_rate:.2%}")
        
        # Test different intelligence quality levels
        intel_levels = [30, 50, 70, 90]
        
        logger.info("\nTesting sensitivity to intelligence quality...")
        for intel_quality in intel_levels:
            constraints = OperationalConstraints(
                time_limit=base_constraints.time_limit,
                available_resources=base_constraints.available_resources,
                weather_conditions=base_constraints.weather_conditions,
                intelligence_quality=intel_quality,
                political_restrictions=base_constraints.political_restrictions,
                legal_constraints=base_constraints.legal_constraints,
                force_protection_requirements=base_constraints.force_protection_requirements,
                stealth_requirements=base_constraints.stealth_requirements
            )
            
            result = await self._run_optimization(targets, strategies, constraints)
            
            logger.info(f"Intel Quality: {intel_quality}% - Success Rate: {result.expected_success_rate:.2%}")
    
    async def _run_optimization(self, targets, strategies, constraints):
        """Run optimization and return results."""
        try:
            result = self.optimizer.optimize_strategy(targets, strategies, constraints)
            return result
        except Exception as e:
            logger.error(f"Optimization failed: {e}")
            raise
    
    def _display_input_data(self, targets, strategies, constraints):
        """Display input data for the optimization."""
        logger.info("\n=== INPUT DATA ===")
        
        logger.info("Targets:")
        for target in targets:
            logger.info(f"  {target.name} ({target.target_type.value})")
            logger.info(f"    Threat Level: {target.threat_level.value}")
            logger.info(f"    Value Score: {target.value_score}")
            logger.info(f"    Protection Level: {target.protection_level}")
            logger.info(f"    Time Sensitivity: {target.time_sensitivity}")
        
        logger.info("\nStrategies:")
        for strategy in strategies:
            logger.info(f"  {strategy.name} ({strategy.strategy_type.value})")
            logger.info(f"    Success Probability: {strategy.success_probability:.2%}")
            logger.info(f"    Execution Time: {strategy.execution_time} hours")
            logger.info(f"    Risk Level: {strategy.risk_level}")
        
        logger.info(f"\nConstraints:")
        logger.info(f"  Time Limit: {constraints.time_limit} hours")
        logger.info(f"  Intelligence Quality: {constraints.intelligence_quality}%")
        logger.info(f"  Available Resources: {constraints.available_resources}")
    
    def _display_results(self, result):
        """Display optimization results."""
        logger.info("\n=== OPTIMIZATION RESULTS ===")
        logger.info(f"Optimal Strategy: {result.optimal_strategy.name}")
        logger.info(f"Expected Success Rate: {result.expected_success_rate:.2%}")
        logger.info(f"Total Risk: {result.risk_assessment['total_risk']:.1f}")
        logger.info(f"Detection Risk: {result.risk_assessment['detection_risk']:.2%}")
        logger.info(f"Collateral Risk: {result.risk_assessment['collateral_risk']:.1f}")
        
        logger.info("\nExecution Sequence:")
        for step in result.timeline:
            logger.info(f"  Step {step['step']}: {step['target_name']} - {step['strategy_name']}")
            logger.info(f"    Duration: {step['duration']:.1f} hours")
            logger.info(f"    Success Rate: {step['expected_success_rate']:.2%}")
            logger.info(f"    Risk Level: {step['risk_level']:.1f}")
        
        logger.info("\nResource Allocation:")
        for resource, amount in result.resource_allocation.items():
            logger.info(f"  {resource}: {amount:.1f}")
        
        logger.info(f"\nPattern Insights: {len(result.pattern_insights)} patterns identified")
        for pattern in result.pattern_insights:
            logger.info(f"  - {pattern.pattern_type}: confidence={pattern.confidence:.2f}")
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive report of all results."""
        report_file = Path("offensive_strategy_report.json")
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_scenarios": len(self.results),
                "average_success_rate": sum(r["result"].expected_success_rate for r in self.results) / len(self.results) if self.results else 0,
                "average_risk": sum(r["result"].risk_assessment['total_risk'] for r in self.results) / len(self.results) if self.results else 0
            },
            "scenarios": [
                {
                    "name": r["scenario"],
                    "success_rate": r["result"].expected_success_rate,
                    "risk_assessment": r["result"].risk_assessment,
                    "resource_allocation": r["result"].resource_allocation,
                    "execution_time": r["result"].execution_time
                }
                for r in self.results
            ]
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"Comprehensive report saved to {report_file}")


async def main():
    """Main demonstration function."""
    try:
        demo = OffensiveStrategyDemo()
        
        # Run basic demo
        await demo.run_basic_demo()
        
        # Run advanced scenarios
        await demo.run_advanced_scenarios()
        
        # Run pattern analysis demo
        await demo.run_pattern_analysis_demo()
        
        # Run Monte Carlo demo
        await demo.run_monte_carlo_demo()
        
        # Run sensitivity analysis
        await demo.run_sensitivity_analysis()
        
        # Generate comprehensive report
        demo.generate_comprehensive_report()
        
        logger.info("\n=== DEMO COMPLETED SUCCESSFULLY ===")
        logger.info("Check the generated files for detailed results:")
        logger.info("- offensive_strategy_demo.log: Detailed execution log")
        logger.info("- offensive_strategy_report.json: Comprehensive results report")
        logger.info("- cache/offensive_strategy/: Optimization results and visualizations")
        
    except Exception as e:
        logger.error(f"Demo failed with error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
