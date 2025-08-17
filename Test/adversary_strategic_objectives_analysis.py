#!/usr/bin/env python3
"""
Adversary Strategic Objectives Analysis
Monte Carlo simulation to calculate probability of adversary achieving 
strategic objectives within 6-month timeframe
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any

import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.monte_carlo.engine import MonteCarloEngine
from core.monte_carlo.config import MonteCarloConfig
from core.monte_carlo.scenarios import ScenarioGenerator
from core.monte_carlo.analysis import ResultAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdversaryStrategicObjectivesAnalyzer:
    """Analyzer for adversary strategic objectives using Monte Carlo simulation"""
    
    def __init__(self):
        self.config = MonteCarloConfig(
            default_iterations=10000,
            confidence_level=0.95,
            max_workers=4,
            cache_results=True
        )
        self.engine = MonteCarloEngine(self.config)
        self.scenario_generator = ScenarioGenerator()
        self.analyzer = ResultAnalyzer()
        
    def create_adversary_scenario(self, 
                                time_horizon_months: int = 6) -> Dict[str, Any]:
        """Create comprehensive adversary strategic objectives scenario"""
        
        scenario = {
            "variables": {
                # Adversary Capability Factors
                "military_capability": {
                    "distribution": "lognormal",
                    "parameters": {
                        "mean": 0.7,  # Base military capability (0-1 scale)
                        "std": 0.2    # Variability in capability
                    }
                },
                "economic_resources": {
                    "distribution": "lognormal", 
                    "parameters": {
                        "mean": 0.6,  # Economic resource availability
                        "std": 0.25
                    }
                },
                "intelligence_capability": {
                    "distribution": "beta",
                    "parameters": {
                        "alpha": 3,   # Intelligence gathering capability
                        "beta": 7
                    }
                },
                "technological_advantage": {
                    "distribution": "normal",
                    "parameters": {
                        "mean": 0.5,  # Technological superiority
                        "std": 0.15
                    }
                },
                
                # Strategic Environment Factors
                "alliance_support": {
                    "distribution": "beta",
                    "parameters": {
                        "alpha": 2,   # Support from allies
                        "beta": 8
                    }
                },
                "geopolitical_conditions": {
                    "distribution": "normal",
                    "parameters": {
                        "mean": 0.4,  # Favorable geopolitical conditions
                        "std": 0.2
                    }
                },
                "domestic_stability": {
                    "distribution": "beta",
                    "parameters": {
                        "alpha": 4,   # Internal stability
                        "beta": 6
                    }
                },
                
                # Operational Factors
                "logistics_capability": {
                    "distribution": "gamma",
                    "parameters": {
                        "alpha": 3,   # Logistics effectiveness
                        "beta": 0.3
                    }
                },
                "command_effectiveness": {
                    "distribution": "normal",
                    "parameters": {
                        "mean": 0.6,  # Command and control effectiveness
                        "std": 0.2
                    }
                },
                "training_quality": {
                    "distribution": "beta",
                    "parameters": {
                        "alpha": 3,   # Training and readiness
                        "beta": 7
                    }
                },
                
                # Countermeasures and Resistance
                "defender_capability": {
                    "distribution": "lognormal",
                    "parameters": {
                        "mean": 0.8,  # Defender's capability to resist
                        "std": 0.15
                    }
                },
                "international_response": {
                    "distribution": "beta",
                    "parameters": {
                        "alpha": 2,   # International community response
                        "beta": 8
                    }
                },
                "sanctions_effectiveness": {
                    "distribution": "normal",
                    "parameters": {
                        "mean": 0.3,  # Effectiveness of sanctions
                        "std": 0.2
                    }
                }
            },
            
            # Correlation matrix - relationships between variables
            "correlations": [
                # mil eco int tech all geo dom log com tra def int san
                [1.0, 0.4, 0.3, 0.5, 0.2, 0.1, 0.3, 0.4, 0.3, 0.2, -0.3, -0.2, -0.1],  # military_capability
                [0.4, 1.0, 0.2, 0.3, 0.4, 0.3, 0.5, 0.2, 0.1, 0.1, -0.2, -0.4, -0.3],  # economic_resources
                [0.3, 0.2, 1.0, 0.4, 0.1, 0.2, 0.1, 0.2, 0.3, 0.4, -0.1, -0.2, -0.1],  # intelligence_capability
                [0.5, 0.3, 0.4, 1.0, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, -0.2, -0.1, -0.1],  # technological_advantage
                [0.2, 0.4, 0.1, 0.2, 1.0, 0.5, 0.3, 0.1, 0.1, 0.1, -0.1, -0.3, -0.2],  # alliance_support
                [0.1, 0.3, 0.2, 0.1, 0.5, 1.0, 0.4, 0.1, 0.1, 0.1, -0.1, -0.2, -0.1],  # geopolitical_conditions
                [0.3, 0.5, 0.1, 0.2, 0.3, 0.4, 1.0, 0.2, 0.1, 0.1, -0.1, -0.2, -0.1],  # domestic_stability
                [0.4, 0.2, 0.2, 0.3, 0.1, 0.1, 0.2, 1.0, 0.3, 0.4, -0.2, -0.1, -0.1],  # logistics_capability
                [0.3, 0.1, 0.3, 0.4, 0.1, 0.1, 0.1, 0.3, 1.0, 0.5, -0.2, -0.1, -0.1],  # command_effectiveness
                [0.2, 0.1, 0.4, 0.5, 0.1, 0.1, 0.1, 0.4, 0.5, 1.0, -0.3, -0.2, -0.1],  # training_quality
                [-0.3, -0.2, -0.1, -0.2, -0.1, -0.1, -0.1, -0.2, -0.2, -0.3, 1.0, 0.4, 0.3],  # defender_capability
                [-0.2, -0.4, -0.2, -0.1, -0.3, -0.2, -0.2, -0.1, -0.1, -0.2, 0.4, 1.0, 0.5],  # international_response
                [-0.1, -0.3, -0.1, -0.1, -0.2, -0.1, -0.1, -0.1, -0.1, -0.1, 0.3, 0.5, 1.0]   # sanctions_effectiveness
            ],
            
            "time_horizon": time_horizon_months,
            "include_statistics": True,
            "include_risk_metrics": True,
            "include_visualizations": True,
            "include_correlation_analysis": True
        }
        
        return scenario
    
    def calculate_strategic_success_probability(self, samples: np.ndarray) -> Dict[str, Any]:
        """Calculate probability of achieving strategic objectives"""
        
        # Define strategic success criteria
        # Success requires multiple factors to be above certain thresholds
        
        # Factor weights for overall success calculation
        factor_weights = {
            'military_capability': 0.25,
            'economic_resources': 0.20,
            'intelligence_capability': 0.15,
            'technological_advantage': 0.15,
            'alliance_support': 0.10,
            'geopolitical_conditions': 0.10,
            'domestic_stability': 0.05
        }
        
        # Success thresholds for individual factors
        success_thresholds = {
            'military_capability': 0.6,
            'economic_resources': 0.5,
            'intelligence_capability': 0.4,
            'technological_advantage': 0.5,
            'alliance_support': 0.3,
            'geopolitical_conditions': 0.4,
            'domestic_stability': 0.4
        }
        
        # Calculate success probability
        success_count = 0
        total_iterations = len(samples)
        
        # Factor indices in the samples array
        factor_indices = {
            'military_capability': 0,
            'economic_resources': 1,
            'intelligence_capability': 2,
            'technological_advantage': 3,
            'alliance_support': 4,
            'geopolitical_conditions': 5,
            'domestic_stability': 6
        }
        
        success_scenarios = []
        
        for i in range(total_iterations):
            # Calculate weighted success score
            success_score = 0
            factor_success = {}
            
            for factor, weight in factor_weights.items():
                factor_value = samples[i][factor_indices[factor]]
                threshold = success_thresholds[factor]
                
                if factor_value >= threshold:
                    factor_success[factor] = True
                    success_score += weight
                else:
                    factor_success[factor] = False
            
            # Consider it a success if weighted score >= 0.6 (60% of factors successful)
            if success_score >= 0.6:
                success_count += 1
                success_scenarios.append({
                    'iteration': i,
                    'success_score': success_score,
                    'factor_success': factor_success,
                    'sample_values': list(samples[i])
                })
        
        success_probability = success_count / total_iterations
        
        # Calculate confidence intervals
        confidence_interval = self._calculate_binomial_confidence_interval(
            success_count, total_iterations, 0.95
        )
        
        return {
            'success_probability': success_probability,
            'success_count': success_count,
            'total_iterations': total_iterations,
            'confidence_interval_95': confidence_interval,
            'success_scenarios': success_scenarios[:10],  # First 10 successful scenarios
            'factor_weights': factor_weights,
            'success_thresholds': success_thresholds
        }
    
    def _calculate_binomial_confidence_interval(self, successes: int, total: int, confidence: float) -> Dict[str, float]:
        """Calculate confidence interval for binomial proportion"""
        from scipy import stats
        
        if total == 0:
            return {'lower': 0.0, 'upper': 1.0}
        
        # Use Wilson confidence interval for better small sample performance
        alpha = 1 - confidence
        z = stats.norm.ppf(1 - alpha/2)
        
        p_hat = successes / total
        denominator = 1 + z**2/total
        centre_adjusted_probability = (p_hat + z*z/(2*total))/denominator
        adjusted_standard_error = z * np.sqrt((p_hat*(1-p_hat) + z*z/(4*total))/total)/denominator
        
        lower_bound = max(0, centre_adjusted_probability - adjusted_standard_error)
        upper_bound = min(1, centre_adjusted_probability + adjusted_standard_error)
        
        return {
            'lower': lower_bound,
            'upper': upper_bound,
            'point_estimate': p_hat
        }
    
    def generate_comprehensive_report(self, simulation_results: Dict[str, Any], 
                                    success_analysis: Dict[str, Any]) -> str:
        """Generate comprehensive analysis report"""
        
        report = f"""
# Adversary Strategic Objectives Analysis Report
## Monte Carlo Simulation Results - 6-Month Timeframe

**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Simulation Iterations:** {simulation_results.get('metadata', {}).get('num_iterations', 'Unknown')}
**Time Horizon:** 6 months

## Executive Summary

The Monte Carlo simulation analyzed the probability of an adversary achieving strategic objectives within a 6-month timeframe using {simulation_results.get('metadata', {}).get('num_iterations', 'Unknown')} iterations.

### Key Findings

**Success Probability:** {success_analysis['success_probability']:.1%}
**Confidence Interval (95%):** {success_analysis['confidence_interval_95']['lower']:.1%} - {success_analysis['confidence_interval_95']['upper']:.1%}

## Detailed Analysis

### Success Criteria
The analysis considered an adversary successful if they achieve a weighted success score of 60% or higher across the following factors:

"""
        
        for factor, weight in success_analysis['factor_weights'].items():
            threshold = success_analysis['success_thresholds'][factor]
            report += f"- **{factor.replace('_', ' ').title()}**: Weight {weight:.0%}, Threshold {threshold:.1f}\n"
        
        report += f"""
### Statistical Results

- **Total Successful Scenarios:** {success_analysis['success_count']:,} out of {success_analysis['total_iterations']:,}
- **Success Rate:** {success_analysis['success_probability']:.1%}
- **95% Confidence Interval:** {success_analysis['confidence_interval_95']['lower']:.1%} - {success_analysis['confidence_interval_95']['upper']:.1%}

### Risk Assessment

Based on the simulation results:

"""
        
        prob = success_analysis['success_probability']
        if prob < 0.2:
            risk_level = "LOW"
            risk_description = "Adversary has minimal probability of achieving strategic objectives"
        elif prob < 0.4:
            risk_level = "MODERATE"
            risk_description = "Adversary has moderate probability of achieving strategic objectives"
        elif prob < 0.6:
            risk_level = "HIGH"
            risk_description = "Adversary has high probability of achieving strategic objectives"
        else:
            risk_level = "CRITICAL"
            risk_description = "Adversary has critical probability of achieving strategic objectives"
        
        report += f"""
**Risk Level:** {risk_level}
**Risk Assessment:** {risk_description}

### Strategic Implications

1. **Current Threat Level:** {risk_level}
2. **Recommended Response:** {'Immediate countermeasures required' if prob > 0.4 else 'Enhanced monitoring recommended'}
3. **Resource Allocation:** {'High priority' if prob > 0.4 else 'Standard priority'}

### Methodology

The analysis used Monte Carlo simulation with the following key factors:
- Military capability and readiness
- Economic resources and sustainability
- Intelligence gathering capabilities
- Technological advantages
- Alliance support and geopolitical conditions
- Domestic stability and political support
- Logistics and command effectiveness
- Training quality and operational readiness

Correlations between factors were modeled to reflect realistic interdependencies in strategic planning.

### Limitations

- Analysis assumes current conditions remain relatively stable
- Does not account for unexpected events or black swan scenarios
- Based on historical patterns and expert assessments
- Confidence intervals reflect statistical uncertainty

## Recommendations

1. **Immediate Actions:**
   - {'Implement enhanced defensive measures' if prob > 0.4 else 'Maintain current defensive posture'}
   - {'Increase intelligence gathering efforts' if prob > 0.3 else 'Continue standard intelligence operations'}
   - {'Strengthen international alliances' if prob > 0.4 else 'Maintain current alliance relationships'}

2. **Strategic Planning:**
   - {'Develop contingency plans for high-threat scenarios' if prob > 0.4 else 'Review existing contingency plans'}
   - {'Allocate additional resources to defense capabilities' if prob > 0.4 else 'Maintain current resource allocation'}
   - {'Enhance early warning systems' if prob > 0.3 else 'Continue monitoring current systems'}

3. **Long-term Considerations:**
   - Monitor changes in adversary capabilities
   - Track geopolitical developments
   - Assess technological advancements
   - Evaluate economic indicators

---
*Report generated by Monte Carlo Strategic Analysis System*
"""
        
        return report
    
    async def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive adversary strategic objectives analysis"""
        
        logger.info("Starting comprehensive adversary strategic objectives analysis")
        
        # Create scenario
        scenario = self.create_adversary_scenario(time_horizon_months=6)
        
        # Run Monte Carlo simulation
        logger.info("Running Monte Carlo simulation...")
        simulation_results = self.engine.run_custom_simulation(
            variables=scenario['variables'],
            correlations=scenario['correlations'],
            num_iterations=10000
        )
        
        # Extract samples for analysis
        samples = simulation_results.get('samples', np.array([]))
        if len(samples) == 0:
            raise ValueError("No samples generated from simulation")
        
        # Calculate success probability
        logger.info("Calculating strategic success probability...")
        success_analysis = self.calculate_strategic_success_probability(samples)
        
        # Generate comprehensive report
        logger.info("Generating comprehensive report...")
        report = self.generate_comprehensive_report(simulation_results, success_analysis)
        
        # Prepare results
        results = {
            'simulation_results': simulation_results,
            'success_analysis': success_analysis,
            'comprehensive_report': report,
            'scenario_config': scenario,
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'time_horizon_months': 6,
                'num_iterations': 10000,
                'confidence_level': 0.95
            }
        }
        
        logger.info("Comprehensive analysis completed successfully")
        return results


async def main():
    """Main execution function"""
    
    print("=" * 80)
    print("ADVERSARY STRATEGIC OBJECTIVES ANALYSIS")
    print("Monte Carlo Simulation - 6-Month Timeframe")
    print("=" * 80)
    
    try:
        # Initialize analyzer
        analyzer = AdversaryStrategicObjectivesAnalyzer()
        
        # Run comprehensive analysis
        results = await analyzer.run_comprehensive_analysis()
        
        # Display key results
        success_prob = results['success_analysis']['success_probability']
        confidence_interval = results['success_analysis']['confidence_interval_95']
        
        print(f"\n🎯 KEY RESULTS:")
        print(f"Success Probability: {success_prob:.1%}")
        print(f"95% Confidence Interval: {confidence_interval['lower']:.1%} - {confidence_interval['upper']:.1%}")
        print(f"Successful Scenarios: {results['success_analysis']['success_count']:,} out of {results['success_analysis']['total_iterations']:,}")
        
        # Determine risk level
        if success_prob < 0.2:
            risk_level = "🟢 LOW"
        elif success_prob < 0.4:
            risk_level = "🟡 MODERATE"
        elif success_prob < 0.6:
            risk_level = "🟠 HIGH"
        else:
            risk_level = "🔴 CRITICAL"
        
        print(f"Risk Level: {risk_level}")
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f"Results/adversary_strategic_objectives_analysis_{timestamp}.json"
        report_file = f"Results/adversary_strategic_objectives_report_{timestamp}.md"
        
        # Ensure Results directory exists
        os.makedirs('Results', exist_ok=True)
        
        # Save JSON results
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save markdown report
        with open(report_file, 'w') as f:
            f.write(results['comprehensive_report'])
        
        print(f"\n📊 Results saved to:")
        print(f"   JSON: {results_file}")
        print(f"   Report: {report_file}")
        
        # Display summary statistics
        if 'statistics' in results['simulation_results']:
            stats = results['simulation_results']['statistics']
            print(f"\n📈 SUMMARY STATISTICS:")
            for var_name, var_stats in stats.items():
                if isinstance(var_stats, dict) and 'mean' in var_stats:
                    print(f"   {var_name}: Mean={var_stats['mean']:.3f}, Std={var_stats['std']:.3f}")
        
        print(f"\n✅ Analysis completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
