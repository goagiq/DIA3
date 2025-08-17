#!/usr/bin/env python3

"""
Resource Allocation Risk Assessment using Monte Carlo Simulation

This script assesses resource allocation risk under adverse conditions using:
- Monte Carlo simulation for scenario modeling
- Historical pattern analysis for risk quantification
- Stress testing under various adverse conditions
- Risk-adjusted performance metrics calculation
- Alternative allocation strategy recommendations

Author: DIA3 Strategic Intelligence System
Date: 2024
"""

import numpy as np
from typing import Dict

class ResourceAllocationRiskAssessment:
    """
    Monte Carlo simulation for resource allocation risk assessment under adverse conditions.
    """
    
    def __init__(self, 
                 initial_allocation: Dict[str, float],
                 time_horizon: int = 12,
                 num_simulations: int = 10000,
                 risk_free_rate: float = 0.02):
        """
        Initialize the risk assessment model.
        
        Args:
            initial_allocation: Dictionary of resource categories and their allocations
            time_horizon: Number of months for simulation
            num_simulations: Number of Monte Carlo simulations
            risk_free_rate: Risk-free rate for discounting
        """
        self.initial_allocation = initial_allocation
        self.time_horizon = time_horizon
        self.num_simulations = num_simulations
        self.risk_free_rate = risk_free_rate
        
        # Historical volatility and correlation data (simplified)
        self.historical_volatility = {
            'personnel': 0.15,
            'equipment': 0.25,
            'technology': 0.30,
            'infrastructure': 0.20,
            'intelligence': 0.35,
            'logistics': 0.18
        }
        
        # Adverse condition scenarios
        self.adverse_scenarios = {
            'budget_cuts': {'probability': 0.25, 'impact': -0.20},
            'personnel_shortage': {'probability': 0.15, 'impact': -0.30},
            'technology_failure': {'probability': 0.10, 'impact': -0.40},
            'supply_chain_disruption': {'probability': 0.20, 'impact': -0.25},
            'cyber_attack': {'probability': 0.08, 'impact': -0.50},
            'natural_disaster': {'probability': 0.05, 'impact': -0.60}
        }
        
        # Correlation matrix between resource categories
        self.correlation_matrix = np.array([
            [1.00, 0.30, 0.20, 0.40, 0.15, 0.25],  # personnel
            [0.30, 1.00, 0.45, 0.35, 0.20, 0.30],  # equipment
            [0.20, 0.45, 1.00, 0.25, 0.40, 0.15],  # technology
            [0.40, 0.35, 0.25, 1.00, 0.30, 0.45],  # infrastructure
            [0.15, 0.20, 0.40, 0.30, 1.00, 0.20],  # intelligence
            [0.25, 0.30, 0.15, 0.45, 0.20, 1.00]   # logistics
        ])
        
        self.resource_categories = list(initial_allocation.keys())
        self.results = {}

    def generate_adverse_conditions(self) -> Dict[str, float]:
        """
        Generate random adverse conditions based on historical probabilities.
        
        Returns:
            Dictionary of adverse conditions and their impacts
        """
        conditions = {}
        for scenario, params in self.adverse_scenarios.items():
            if np.random.random() < params['probability']:
                # Add some randomness to the impact
                impact_variation = np.random.normal(0, 0.1)
                conditions[scenario] = params['impact'] + impact_variation
            else:
                conditions[scenario] = 0.0
        return conditions

    def simulate_resource_evolution(self, 
                                  initial_values: np.ndarray,
                                  adverse_conditions: Dict[str, float]) -> np.ndarray:
        """
        Simulate resource evolution over time under adverse conditions.
        
        Args:
            initial_values: Initial resource allocations
            adverse_conditions: Dictionary of adverse conditions and impacts
            
        Returns:
            Array of resource values over time
        """
        # Generate correlated random walks
        n_resources = len(initial_values)
        returns = np.random.multivariate_normal(
            mean=np.zeros(n_resources),
            cov=self.correlation_matrix * np.outer(
                [self.historical_volatility[cat] for cat in self.resource_categories],
                [self.historical_volatility[cat] for cat in self.resource_categories]
            ),
            size=self.time_horizon
        )
        
        # Apply adverse condition impacts
        adverse_impact = np.zeros(n_resources)
        for condition, impact in adverse_conditions.items():
            if condition == 'budget_cuts':
                adverse_impact += impact * np.ones(n_resources)
            elif condition == 'personnel_shortage':
                adverse_impact[0] += impact  # personnel
            elif condition == 'technology_failure':
                adverse_impact[2] += impact  # technology
            elif condition == 'supply_chain_disruption':
                adverse_impact[5] += impact  # logistics
            elif condition == 'cyber_attack':
                adverse_impact[2] += impact * 0.6  # technology
                adverse_impact[4] += impact * 0.4  # intelligence
            elif condition == 'natural_disaster':
                adverse_impact[3] += impact * 0.7  # infrastructure
                adverse_impact[5] += impact * 0.3  # logistics
        
        # Simulate evolution
        values = np.zeros((self.time_horizon + 1, n_resources))
        values[0] = initial_values
        
        for t in range(self.time_horizon):
            # Apply returns and adverse impacts
            values[t + 1] = values[t] * (1 + returns[t] + adverse_impact)
            
            # Ensure non-negative values
            values[t + 1] = np.maximum(values[t + 1], 0)
            
            # Reduce adverse impact over time (recovery)
            adverse_impact *= 0.95
        
        return values

    def run_monte_carlo_simulation(self) -> Dict:
        """
        Run Monte Carlo simulation for resource allocation risk assessment.
        
        Returns:
            Dictionary containing simulation results
        """
        print("Running Monte Carlo simulation for resource allocation risk assessment...")
        
        initial_values = np.array([self.initial_allocation[cat] for cat in self.resource_categories])
        
        # Store simulation results
        all_paths = []
        final_values = []
        adverse_condition_counts = {scenario: 0 for scenario in self.adverse_scenarios.keys()}
        
        for sim in range(self.num_simulations):
            # Generate adverse conditions for this simulation
            adverse_conditions = self.generate_adverse_conditions()
            
            # Count adverse conditions
            for condition, impact in adverse_conditions.items():
                if impact < 0:
                    adverse_condition_counts[condition] += 1
            
            # Simulate resource evolution
            path = self.simulate_resource_evolution(initial_values, adverse_conditions)
            all_paths.append(path)
            final_values.append(path[-1])
            
            if (sim + 1) % 1000 == 0:
                print(f"Completed {sim + 1}/{self.num_simulations} simulations...")
        
        # Convert to numpy arrays
        all_paths = np.array(all_paths)
        final_values = np.array(final_values)
        
        # Calculate risk metrics
        risk_metrics = self.calculate_risk_metrics(all_paths, final_values, adverse_condition_counts)
        
        # Store results
        self.results = {
            'simulation_paths': all_paths,
            'final_values': final_values,
            'risk_metrics': risk_metrics,
            'adverse_condition_counts': adverse_condition_counts,
            'initial_allocation': self.initial_allocation,
            'time_horizon': self.time_horizon,
            'num_simulations': self.num_simulations
        }
        
        return self.results

    def calculate_risk_metrics(self, 
                             all_paths: np.ndarray,
                             final_values: np.ndarray,
                             adverse_condition_counts: Dict[str, int]) -> Dict:
        """
        Calculate comprehensive risk metrics from simulation results.
        
        Args:
            all_paths: Array of all simulation paths
            final_values: Array of final values for each simulation
            adverse_condition_counts: Count of adverse conditions in simulations
            
        Returns:
            Dictionary of risk metrics
        """
        metrics = {}
        
        # Basic statistics
        for i, category in enumerate(self.resource_categories):
            category_final_values = final_values[:, i]
            
            metrics[category] = {
                'mean_final_value': np.mean(category_final_values),
                'std_final_value': np.std(category_final_values),
                'min_final_value': np.min(category_final_values),
                'max_final_value': np.max(category_final_values),
                'var_95': np.percentile(category_final_values, 5),
                'var_99': np.percentile(category_final_values, 1),
                'expected_shortfall_95': np.mean(category_final_values[category_final_values <= np.percentile(category_final_values, 5)]),
                'expected_shortfall_99': np.mean(category_final_values[category_final_values <= np.percentile(category_final_values, 1)]),
                'probability_of_decline': np.mean(category_final_values < self.initial_allocation[category]),
                'probability_of_critical_decline': np.mean(category_final_values < 0.5 * self.initial_allocation[category])
            }
        
        # Portfolio-level metrics
        total_final_values = np.sum(final_values, axis=1)
        total_initial = sum(self.initial_allocation.values())
        
        metrics['portfolio'] = {
            'mean_total_final_value': np.mean(total_final_values),
            'std_total_final_value': np.std(total_final_values),
            'min_total_final_value': np.min(total_final_values),
            'max_total_final_value': np.max(total_final_values),
            'var_95': np.percentile(total_final_values, 5),
            'var_99': np.percentile(total_final_values, 1),
            'expected_shortfall_95': np.mean(total_final_values[total_final_values <= np.percentile(total_final_values, 5)]),
            'expected_shortfall_99': np.mean(total_final_values[total_final_values <= np.percentile(total_final_values, 1)]),
            'probability_of_decline': np.mean(total_final_values < total_initial),
            'probability_of_critical_decline': np.mean(total_final_values < 0.7 * total_initial),
            'sharpe_ratio': (np.mean(total_final_values) - total_initial) / np.std(total_final_values) if np.std(total_final_values) > 0 else 0
        }
        
        # Adverse condition analysis
        metrics['adverse_conditions'] = {
            scenario: {
                'frequency': count / self.num_simulations,
                'expected_impact': self.adverse_scenarios[scenario]['impact']
            }
            for scenario, count in adverse_condition_counts.items()
        }
        
        return metrics

    def generate_alternative_strategies(self) -> Dict[str, Dict[str, float]]:
        """
        Generate alternative resource allocation strategies based on risk analysis.
        
        Returns:
            Dictionary of alternative strategies
        """
        strategies = {}
        
        # Conservative strategy (reduce high-risk allocations)
        conservative = self.initial_allocation.copy()
        high_risk_categories = ['technology', 'intelligence']
        for category in high_risk_categories:
            if category in conservative:
                conservative[category] *= 0.8
                # Redistribute to lower-risk categories
                conservative['personnel'] *= 1.1
                conservative['infrastructure'] *= 1.1
        strategies['conservative'] = conservative
        
        # Aggressive strategy (increase high-return allocations)
        aggressive = self.initial_allocation.copy()
        high_return_categories = ['technology', 'intelligence']
        for category in high_return_categories:
            if category in aggressive:
                aggressive[category] *= 1.2
                # Reduce lower-return categories
                aggressive['infrastructure'] *= 0.9
                aggressive['logistics'] *= 0.9
        strategies['aggressive'] = aggressive
        
        # Balanced strategy (equal risk distribution)
        balanced = {}
        total_resources = sum(self.initial_allocation.values())
        num_categories = len(self.resource_categories)
        equal_allocation = total_resources / num_categories
        for category in self.resource_categories:
            balanced[category] = equal_allocation
        strategies['balanced'] = balanced
        
        # Risk-adjusted strategy (based on volatility)
        risk_adjusted = {}
        total_resources = sum(self.initial_allocation.values())
        inverse_volatilities = {cat: 1/vol for cat, vol in self.historical_volatility.items()}
        total_inverse_vol = sum(inverse_volatilities.values())
        
        for category in self.resource_categories:
            risk_adjusted[category] = total_resources * (inverse_volatilities[category] / total_inverse_vol)
        strategies['risk_adjusted'] = risk_adjusted
        
        return strategies


def main():
    """
    Main function to demonstrate the resource allocation risk assessment.
    """
    print("Resource Allocation Risk Assessment - Monte Carlo Simulation")
    print("=" * 60)
    
    # Example resource allocation
    initial_allocation = {
        'personnel': 1000000,      # $1M
        'equipment': 800000,       # $800K
        'technology': 1200000,     # $1.2M
        'infrastructure': 600000,  # $600K
        'intelligence': 900000,    # $900K
        'logistics': 500000        # $500K
    }
    
    print(f"Initial Resource Allocation: ${sum(initial_allocation.values()):,}")
    for category, amount in initial_allocation.items():
        print(f"  {category.title()}: ${amount:,}")
    
    print("\nInitializing risk assessment model...")
    
    # Initialize the risk assessment model
    risk_assessor = ResourceAllocationRiskAssessment(
        initial_allocation=initial_allocation,
        time_horizon=12,  # 12 months
        num_simulations=1000,  # 1,000 simulations for faster execution
        risk_free_rate=0.02  # 2% risk-free rate
    )
    
    # Run Monte Carlo simulation
    results = risk_assessor.run_monte_carlo_simulation()
    
    print("\nSimulation completed successfully!")
    print(f"Total simulations run: {results['num_simulations']:,}")
    
    # Display key results
    print("\nKey Risk Metrics:")
    print("-" * 40)
    
    portfolio_metrics = results['risk_metrics']['portfolio']
    print(f"Portfolio Probability of Decline: {portfolio_metrics['probability_of_decline']:.2%}")
    print(f"Portfolio Probability of Critical Decline: {portfolio_metrics['probability_of_critical_decline']:.2%}")
    print(f"Portfolio Value at Risk (95%): ${portfolio_metrics['var_95']:,.2f}")
    print(f"Portfolio Expected Shortfall (95%): ${portfolio_metrics['expected_shortfall_95']:,.2f}")
    
    # Generate alternative strategies
    strategies = risk_assessor.generate_alternative_strategies()
    print("\nAlternative Strategies Generated:")
    print("-" * 40)
    for strategy_name, allocation in strategies.items():
        print(f"\n{strategy_name.title()} Strategy:")
        for category, amount in allocation.items():
            print(f"  {category.title()}: ${amount:,.2f}")
    
    print(f"\nAnalysis complete!")
    
    return risk_assessor


if __name__ == "__main__":
    # Run the risk assessment
    risk_assessor = main()
