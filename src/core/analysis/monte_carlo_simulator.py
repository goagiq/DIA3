"""
Monte Carlo Simulation Engine
Provides probabilistic analysis for strategic assessments and risk modeling
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from scipy import stats
import json
import datetime

@dataclass
class SimulationParameter:
    """Represents a parameter for Monte Carlo simulation"""
    name: str
    distribution_type: str  # 'normal', 'triangular', 'uniform', 'lognormal', 'binomial'
    parameters: Dict[str, float]  # Distribution-specific parameters
    description: str = ""
    unit: str = ""

@dataclass
class SimulationResult:
    """Represents the results of a Monte Carlo simulation"""
    parameter_name: str
    values: np.ndarray
    mean: float
    std: float
    percentiles: Dict[str, float]
    confidence_intervals: Dict[str, Tuple[float, float]]
    description: str = ""

class MonteCarloSimulator:
    """Monte Carlo simulation engine for strategic analysis"""
    
    def __init__(self, n_iterations: int = 10000, random_seed: Optional[int] = None):
        """
        Initialize the Monte Carlo simulator
        
        Args:
            n_iterations: Number of simulation iterations
            random_seed: Random seed for reproducibility
        """
        self.n_iterations = n_iterations
        if random_seed is not None:
            np.random.seed(random_seed)
        
        # Store simulation parameters and results
        self.parameters: Dict[str, SimulationParameter] = {}
        self.results: Dict[str, SimulationResult] = {}
        self.simulation_data: Optional[pd.DataFrame] = None
        
    def add_parameter(self, name: str, distribution_type: str, 
                     parameters: Dict[str, float], description: str = "", unit: str = "") -> None:
        """
        Add a parameter to the simulation
        
        Args:
            name: Parameter name
            distribution_type: Type of probability distribution
            parameters: Distribution parameters
            description: Parameter description
            unit: Unit of measurement
        """
        self.parameters[name] = SimulationParameter(
            name=name,
            distribution_type=distribution_type,
            parameters=parameters,
            description=description,
            unit=unit
        )
    
    def generate_samples(self, parameter: SimulationParameter) -> np.ndarray:
        """
        Generate random samples for a parameter based on its distribution
        
        Args:
            parameter: Simulation parameter
            
        Returns:
            Array of random samples
        """
        dist_type = parameter.distribution_type.lower()
        params = parameter.parameters
        
        if dist_type == 'normal':
            return np.random.normal(params['mean'], params['std'], self.n_iterations)
        elif dist_type == 'triangular':
            return np.random.triangular(params['left'], params['mode'], params['right'], self.n_iterations)
        elif dist_type == 'uniform':
            return np.random.uniform(params['low'], params['high'], self.n_iterations)
        elif dist_type == 'lognormal':
            return np.random.lognormal(params['mean'], params['sigma'], self.n_iterations)
        elif dist_type == 'binomial':
            return np.random.binomial(params['n'], params['p'], self.n_iterations)
        elif dist_type == 'exponential':
            return np.random.exponential(params['scale'], self.n_iterations)
        elif dist_type == 'gamma':
            return np.random.gamma(params['shape'], params['scale'], self.n_iterations)
        else:
            raise ValueError(f"Unsupported distribution type: {dist_type}")
    
    def run_simulation(self, output_function: callable, 
                      output_name: str = "output") -> SimulationResult:
        """
        Run Monte Carlo simulation
        
        Args:
            output_function: Function that computes output from input parameters
            output_name: Name for the output result
            
        Returns:
            Simulation result
        """
        # Generate samples for all parameters
        samples = {}
        for name, param in self.parameters.items():
            samples[name] = self.generate_samples(param)
        
        # Create DataFrame for easier manipulation
        self.simulation_data = pd.DataFrame(samples)
        
        # Compute output for each iteration
        outputs = []
        for i in range(self.n_iterations):
            row = self.simulation_data.iloc[i]
            output = output_function(row)
            outputs.append(output)
        
        outputs = np.array(outputs)
        
        # Calculate statistics
        mean_val = np.mean(outputs)
        std_val = np.std(outputs)
        
        # Calculate percentiles
        percentiles = {
            '5%': np.percentile(outputs, 5),
            '25%': np.percentile(outputs, 25),
            '50%': np.percentile(outputs, 50),
            '75%': np.percentile(outputs, 75),
            '95%': np.percentile(outputs, 95)
        }
        
        # Calculate confidence intervals
        confidence_intervals = {
            '90%': (np.percentile(outputs, 5), np.percentile(outputs, 95)),
            '95%': (np.percentile(outputs, 2.5), np.percentile(outputs, 97.5)),
            '99%': (np.percentile(outputs, 0.5), np.percentile(outputs, 99.5))
        }
        
        # Store result
        result = SimulationResult(
            parameter_name=output_name,
            values=outputs,
            mean=mean_val,
            std=std_val,
            percentiles=percentiles,
            confidence_intervals=confidence_intervals
        )
        
        self.results[output_name] = result
        return result
    
    def create_pakistan_submarine_simulation(self) -> Dict[str, Any]:
        """
        Create a Monte Carlo simulation for Pakistan submarine acquisition
        
        Returns:
            Dictionary with simulation setup and results
        """
        # Clear previous parameters
        self.parameters.clear()
        self.results.clear()
        
        # Add parameters for Pakistan submarine simulation
        self.add_parameter(
            name="submarine_cost_per_unit",
            distribution_type="lognormal",
            parameters={"mean": 3.5, "sigma": 0.3},  # $3.5B per submarine with uncertainty
            description="Cost per submarine (billions USD)",
            unit="billion USD"
        )
        
        self.add_parameter(
            name="infrastructure_cost",
            distribution_type="triangular",
            parameters={"left": 4.0, "mode": 6.0, "right": 8.0},
            description="Infrastructure development cost",
            unit="billion USD"
        )
        
        self.add_parameter(
            name="training_cost",
            distribution_type="normal",
            parameters={"mean": 4.0, "std": 0.8},
            description="Training and personnel cost",
            unit="billion USD"
        )
        
        self.add_parameter(
            name="weapons_cost",
            distribution_type="uniform",
            parameters={"low": 1.5, "high": 3.0},
            description="Weapons systems cost",
            unit="billion USD"
        )
        
        self.add_parameter(
            name="annual_maintenance",
            distribution_type="gamma",
            parameters={"shape": 2.0, "scale": 1.2},
            description="Annual maintenance cost",
            unit="billion USD"
        )
        
        self.add_parameter(
            name="implementation_timeline",
            distribution_type="triangular",
            parameters={"left": 12, "mode": 18, "right": 25},
            description="Implementation timeline",
            unit="years"
        )
        
        self.add_parameter(
            name="regional_response_probability",
            distribution_type="binomial",
            parameters={"n": 1, "p": 0.85},
            description="Probability of regional response",
            unit="probability"
        )
        
        self.add_parameter(
            name="economic_impact_factor",
            distribution_type="normal",
            parameters={"mean": 1.0, "std": 0.2},
            description="Economic impact multiplier",
            unit="multiplier"
        )
        
        # Define output function
        def total_cost_calculation(row):
            """Calculate total cost including all components"""
            submarine_cost = row['submarine_cost_per_unit'] * 50  # 50 submarines
            total_initial = submarine_cost + row['infrastructure_cost'] + row['training_cost'] + row['weapons_cost']
            annual_maintenance_total = row['annual_maintenance'] * row['implementation_timeline']
            return total_initial + annual_maintenance_total
        
        def risk_score_calculation(row):
            """Calculate overall risk score"""
            cost_risk = min(1.0, row['submarine_cost_per_unit'] * 50 / 100)  # Normalize to 0-1
            timeline_risk = min(1.0, row['implementation_timeline'] / 30)  # Normalize to 0-1
            response_risk = row['regional_response_probability']
            economic_risk = abs(row['economic_impact_factor'] - 1.0)
            
            # Weighted risk score
            risk_score = (0.3 * cost_risk + 0.2 * timeline_risk + 0.3 * response_risk + 0.2 * economic_risk)
            return risk_score
        
        def strategic_impact_calculation(row):
            """Calculate strategic impact score"""
            fleet_increase = 50 / 5  # 10x increase
            cost_efficiency = 1.0 / (row['submarine_cost_per_unit'] / 3.5)  # Normalize to baseline
            timeline_factor = 1.0 / (row['implementation_timeline'] / 18)  # Normalize to expected timeline
            
            strategic_score = (0.4 * fleet_increase + 0.3 * cost_efficiency + 0.3 * timeline_factor)
            return strategic_score
        
        # Run simulations
        cost_result = self.run_simulation(total_cost_calculation, "total_cost")
        risk_result = self.run_simulation(risk_score_calculation, "risk_score")
        impact_result = self.run_simulation(strategic_impact_calculation, "strategic_impact")
        
        # Create comprehensive results
        simulation_results = {
            'parameters': {name: {
                'distribution_type': param.distribution_type,
                'parameters': param.parameters,
                'description': param.description,
                'unit': param.unit
            } for name, param in self.parameters.items()},
            
            'results': {
                'total_cost': {
                    'mean': cost_result.mean,
                    'std': cost_result.std,
                    'percentiles': cost_result.percentiles,
                    'confidence_intervals': cost_result.confidence_intervals,
                    'unit': 'billion USD',
                    'description': 'Total cost including all components'
                },
                'risk_score': {
                    'mean': risk_result.mean,
                    'std': risk_result.std,
                    'percentiles': risk_result.percentiles,
                    'confidence_intervals': risk_result.confidence_intervals,
                    'unit': 'risk score (0-1)',
                    'description': 'Overall risk assessment score'
                },
                'strategic_impact': {
                    'mean': impact_result.mean,
                    'std': impact_result.std,
                    'percentiles': impact_result.percentiles,
                    'confidence_intervals': impact_result.confidence_intervals,
                    'unit': 'impact score',
                    'description': 'Strategic impact assessment score'
                }
            },
            
            'simulation_metadata': {
                'n_iterations': self.n_iterations,
                'timestamp': datetime.datetime.now().isoformat(),
                'description': 'Pakistan submarine acquisition Monte Carlo simulation'
            }
        }
        
        return simulation_results
    
    def create_visualization_data(self) -> Dict[str, Any]:
        """
        Create data for visualization of simulation results
        
        Returns:
            Dictionary with chart data for visualization
        """
        if self.simulation_data is None or not self.results:
            return {}
        
        viz_data = {}
        
        # Cost distribution data
        if 'total_cost' in self.results:
            cost_values = self.results['total_cost'].values
            # Calculate appropriate bins based on actual data range
            min_cost = np.min(cost_values)
            max_cost = np.max(cost_values)
            mean_cost = np.mean(cost_values)
            
            # Create bins that cover the actual data range
            if max_cost > 1000:  # If costs are in thousands of billions
                # Use larger bins for high cost values
                bins = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
                labels = ['$0-500B', '$500-1000B', '$1000-1500B', '$1500-2000B', '$2000-2500B', '$2500-3000B', '$3000-3500B', '$3500-4000B']
            else:
                # Use smaller bins for lower cost values
                bins = [0, 100, 200, 300, 400, 500, 600, 700, 800]
                labels = ['$0-100B', '$100-200B', '$200-300B', '$300-400B', '$400-500B', '$500-600B', '$600-700B', '$700-800B']
            
            # Calculate histogram data
            hist_data = []
            for i in range(len(bins) - 1):
                count = np.sum((cost_values >= bins[i]) & (cost_values < bins[i + 1]))
                hist_data.append(int(count))
            
            viz_data['cost_distribution'] = {
                'labels': labels,
                'data': hist_data
            }
        
        # Risk score distribution
        if 'risk_score' in self.results:
            risk_values = self.results['risk_score'].values
            viz_data['risk_distribution'] = {
                'labels': ['Low (0-0.2)', 'Medium (0.2-0.4)', 'High (0.4-0.6)', 'Very High (0.6-0.8)', 'Critical (0.8-1.0)'],
                'data': [
                    np.sum((risk_values >= 0) & (risk_values < 0.2)),
                    np.sum((risk_values >= 0.2) & (risk_values < 0.4)),
                    np.sum((risk_values >= 0.4) & (risk_values < 0.6)),
                    np.sum((risk_values >= 0.6) & (risk_values < 0.8)),
                    np.sum((risk_values >= 0.8) & (risk_values <= 1.0))
                ]
            }
        
        # Strategic impact distribution
        if 'strategic_impact' in self.results:
            impact_values = self.results['strategic_impact'].values
            viz_data['impact_distribution'] = {
                'labels': ['Low (0-2)', 'Medium (2-4)', 'High (4-6)', 'Very High (6-8)', 'Exceptional (8-10)'],
                'data': [
                    np.sum((impact_values >= 0) & (impact_values < 2)),
                    np.sum((impact_values >= 2) & (impact_values < 4)),
                    np.sum((impact_values >= 4) & (impact_values < 6)),
                    np.sum((impact_values >= 6) & (impact_values < 8)),
                    np.sum((impact_values >= 8) & (impact_values <= 10))
                ]
            }
        
        # Confidence intervals data
        viz_data['confidence_intervals'] = {}
        for result_name, result in self.results.items():
            viz_data['confidence_intervals'][result_name] = {
                'mean': result.mean,
                'std': result.std,
                'intervals': result.confidence_intervals
            }
        
        return viz_data
    
    def export_results(self, filepath: str) -> None:
        """
        Export simulation results to JSON file
        
        Args:
            filepath: Path to save the results
        """
        export_data = {
            'parameters': {name: {
                'distribution_type': param.distribution_type,
                'parameters': param.parameters,
                'description': param.description,
                'unit': param.unit
            } for name, param in self.parameters.items()},
            
            'results': {name: {
                'mean': result.mean,
                'std': result.std,
                'percentiles': result.percentiles,
                'confidence_intervals': result.confidence_intervals
            } for name, result in self.results.items()},
            
            'simulation_metadata': {
                'n_iterations': self.n_iterations,
                'timestamp': datetime.datetime.now().isoformat()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)

def create_custom_simulation(parameters: Dict[str, Dict[str, Any]], 
                           output_function: callable,
                           n_iterations: int = 10000) -> MonteCarloSimulator:
    """
    Create a custom Monte Carlo simulation
    
    Args:
        parameters: Dictionary of parameter definitions
        output_function: Function to compute output
        n_iterations: Number of simulation iterations
        
    Returns:
        Configured MonteCarloSimulator instance
    """
    simulator = MonteCarloSimulator(n_iterations=n_iterations)
    
    for name, param_def in parameters.items():
        simulator.add_parameter(
            name=name,
            distribution_type=param_def['distribution_type'],
            parameters=param_def['parameters'],
            description=param_def.get('description', ''),
            unit=param_def.get('unit', '')
        )
    
    simulator.run_simulation(output_function)
    return simulator
