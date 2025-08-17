#!/usr/bin/env python3
"""
Multi-Domain Monte Carlo Engine
A comprehensive Monte Carlo simulation engine for defense, intelligence, and business applications.
"""

import asyncio
import json
import logging
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import uuid
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DomainType(Enum):
    """Supported domain types for Monte Carlo simulations."""
    DEFENSE = "defense"
    INTELLIGENCE = "intelligence"
    BUSINESS = "business"
    FINANCIAL = "financial"
    CYBERSECURITY = "cybersecurity"
    SUPPLY_CHAIN = "supply_chain"
    RISK_MANAGEMENT = "risk_management"
    STRATEGIC_PLANNING = "strategic_planning"


class SimulationType(Enum):
    """Types of Monte Carlo simulations."""
    CAPABILITY_ASSESSMENT = "capability_assessment"
    RISK_ANALYSIS = "risk_analysis"
    SCENARIO_PLANNING = "scenario_planning"
    FORECASTING = "forecasting"
    OPTIMIZATION = "optimization"
    SENSITIVITY_ANALYSIS = "sensitivity_analysis"
    DECISION_SUPPORT = "decision_support"
    THREAT_ASSESSMENT = "threat_assessment"


@dataclass
class SimulationConfig:
    """Configuration for Monte Carlo simulations."""
    domain: DomainType
    simulation_type: SimulationType
    num_iterations: int = 10000
    confidence_level: float = 0.95
    time_horizon: int = 24  # months
    parallel_processing: bool = True
    include_advanced_analytics: bool = True
    cache_results: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationResult:
    """Results from Monte Carlo simulation."""
    simulation_id: str
    config: SimulationConfig
    samples: np.ndarray
    statistics: Dict[str, Dict[str, float]]
    risk_metrics: Dict[str, float]
    confidence_intervals: Dict[str, Dict[str, float]]
    execution_time: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class MultiDomainMonteCarloEngine:
    """Multi-domain Monte Carlo simulation engine."""
    
    def __init__(self, cache_dir: str = "cache/monte_carlo"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Domain-specific scenario templates
        self.scenario_templates = self._load_scenario_templates()
        
        # Performance tracking
        self.performance_metrics = {}
        
    def _load_scenario_templates(self) -> Dict[DomainType, Dict[str, Any]]:
        """Load domain-specific scenario templates."""
        return {
            DomainType.DEFENSE: {
                "military_capability": {
                    "variables": {
                        "military_spending": {
                            "distribution": "lognormal",
                            "parameters": {"mean": 4.5, "std": 0.3},
                            "description": "Annual military spending in billions USD"
                        },
                        "force_strength": {
                            "distribution": "normal",
                            "parameters": {"mean": 500000, "std": 50000},
                            "description": "Active military personnel"
                        },
                        "equipment_modernization": {
                            "distribution": "beta",
                            "parameters": {"alpha": 3, "beta": 7},
                            "description": "Equipment modernization rate (0-1)"
                        },
                        "training_effectiveness": {
                            "distribution": "beta",
                            "parameters": {"alpha": 4, "beta": 6},
                            "description": "Training effectiveness score (0-1)"
                        },
                        "logistics_capability": {
                            "distribution": "normal",
                            "parameters": {"mean": 0.7, "std": 0.1},
                            "description": "Logistics capability score (0-1)"
                        },
                        "intelligence_capability": {
                            "distribution": "beta",
                            "parameters": {"alpha": 2, "beta": 8},
                            "description": "Intelligence gathering capability (0-1)"
                        },
                        "cyber_capability": {
                            "distribution": "gamma",
                            "parameters": {"alpha": 2, "beta": 0.3},
                            "description": "Cyber warfare capability score"
                        },
                        "nuclear_capability": {
                            "distribution": "beta",
                            "parameters": {"alpha": 1, "beta": 9},
                            "description": "Nuclear capability score (0-1)"
                        },
                        "alliance_support": {
                            "distribution": "normal",
                            "parameters": {"mean": 0.6, "std": 0.15},
                            "description": "Alliance support level (0-1)"
                        },
                        "economic_stability": {
                            "distribution": "normal",
                            "parameters": {"mean": 0.65, "std": 0.12},
                            "description": "Economic stability score (0-1)"
                        }
                    },
                    "correlations": [
                        [1.0, 0.4, 0.3, 0.2, 0.3, 0.1, 0.2, 0.1, 0.1, 0.2],
                        [0.4, 1.0, 0.5, 0.4, 0.3, 0.2, 0.3, 0.1, 0.2, 0.3],
                        [0.3, 0.5, 1.0, 0.6, 0.4, 0.3, 0.4, 0.2, 0.2, 0.4],
                        [0.2, 0.4, 0.6, 1.0, 0.5, 0.4, 0.3, 0.1, 0.3, 0.3],
                        [0.3, 0.3, 0.4, 0.5, 1.0, 0.3, 0.2, 0.1, 0.4, 0.5],
                        [0.1, 0.2, 0.3, 0.4, 0.3, 1.0, 0.6, 0.2, 0.2, 0.2],
                        [0.2, 0.3, 0.4, 0.3, 0.2, 0.6, 1.0, 0.3, 0.1, 0.2],
                        [0.1, 0.1, 0.2, 0.1, 0.1, 0.2, 0.3, 1.0, 0.1, 0.1],
                        [0.1, 0.2, 0.2, 0.3, 0.4, 0.2, 0.1, 0.1, 1.0, 0.6],
                        [0.2, 0.3, 0.4, 0.3, 0.5, 0.2, 0.2, 0.1, 0.6, 1.0]
                    ]
                }
            },
            DomainType.BUSINESS: {
                "market_analysis": {
                    "variables": {
                        "market_size": {
                            "distribution": "lognormal",
                            "parameters": {"mean": 6.0, "std": 0.5},
                            "description": "Market size in billions USD"
                        },
                        "growth_rate": {
                            "distribution": "normal",
                            "parameters": {"mean": 0.08, "std": 0.02},
                            "description": "Annual growth rate"
                        },
                        "competition_level": {
                            "distribution": "beta",
                            "parameters": {"alpha": 2, "beta": 3},
                            "description": "Competition intensity (0-1)"
                        },
                        "customer_satisfaction": {
                            "distribution": "beta",
                            "parameters": {"alpha": 4, "beta": 1},
                            "description": "Customer satisfaction score (0-1)"
                        },
                        "operational_efficiency": {
                            "distribution": "normal",
                            "parameters": {"mean": 0.75, "std": 0.1},
                            "description": "Operational efficiency (0-1)"
                        }
                    },
                    "correlations": [
                        [1.0, 0.3, -0.2, 0.1, 0.2],
                        [0.3, 1.0, -0.1, 0.2, 0.3],
                        [-0.2, -0.1, 1.0, -0.3, -0.2],
                        [0.1, 0.2, -0.3, 1.0, 0.4],
                        [0.2, 0.3, -0.2, 0.4, 1.0]
                    ]
                }
            },
            DomainType.FINANCIAL: {
                "portfolio_risk": {
                    "variables": {
                        "market_return": {
                            "distribution": "normal",
                            "parameters": {"mean": 0.08, "std": 0.15},
                            "description": "Market return rate"
                        },
                        "interest_rate": {
                            "distribution": "normal",
                            "parameters": {"mean": 0.03, "std": 0.01},
                            "description": "Interest rate"
                        },
                        "inflation": {
                            "distribution": "normal",
                            "parameters": {"mean": 0.02, "std": 0.005},
                            "description": "Inflation rate"
                        },
                        "volatility": {
                            "distribution": "gamma",
                            "parameters": {"alpha": 2, "beta": 0.1},
                            "description": "Market volatility"
                        }
                    },
                    "correlations": [
                        [1.0, -0.2, -0.1, 0.3],
                        [-0.2, 1.0, 0.4, -0.1],
                        [-0.1, 0.4, 1.0, -0.2],
                        [0.3, -0.1, -0.2, 1.0]
                    ]
                }
            },
            DomainType.CYBERSECURITY: {
                "threat_assessment": {
                    "variables": {
                        "attack_frequency": {
                            "distribution": "poisson",
                            "parameters": {"lambda": 100},
                            "description": "Daily attack attempts"
                        },
                        "vulnerability_score": {
                            "distribution": "beta",
                            "parameters": {"alpha": 2, "beta": 5},
                            "description": "System vulnerability score (0-1)"
                        },
                        "detection_rate": {
                            "distribution": "beta",
                            "parameters": {"alpha": 7, "beta": 3},
                            "description": "Attack detection rate (0-1)"
                        },
                        "response_time": {
                            "distribution": "exponential",
                            "parameters": {"lambda": 0.1},
                            "description": "Response time in hours"
                        },
                        "recovery_time": {
                            "distribution": "lognormal",
                            "parameters": {"mean": 2.0, "std": 0.5},
                            "description": "Recovery time in days"
                        }
                    },
                    "correlations": [
                        [1.0, 0.3, -0.2, 0.1, 0.2],
                        [0.3, 1.0, -0.4, 0.2, 0.3],
                        [-0.2, -0.4, 1.0, -0.3, -0.2],
                        [0.1, 0.2, -0.3, 1.0, 0.4],
                        [0.2, 0.3, -0.2, 0.4, 1.0]
                    ]
                }
            }
        }
    
    async def run_simulation(
        self,
        config: SimulationConfig,
        scenario_name: str,
        custom_variables: Optional[Dict[str, Any]] = None
    ) -> SimulationResult:
        """Run a Monte Carlo simulation."""
        
        simulation_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        logger.info(f"Starting simulation {simulation_id} for domain {config.domain.value}")
        
        try:
            # Get scenario template
            scenario_template = self._get_scenario_template(config.domain, scenario_name)
            
            # Merge with custom variables if provided
            if custom_variables:
                scenario_template = self._merge_custom_variables(scenario_template, custom_variables)
            
            # Run the simulation
            samples = await self._run_monte_carlo_simulation(scenario_template, config)
            
            # Calculate statistics
            statistics = self._calculate_statistics(samples, scenario_template["variables"])
            
            # Calculate risk metrics
            risk_metrics = self._calculate_risk_metrics(samples)
            
            # Calculate confidence intervals
            confidence_intervals = self._calculate_confidence_intervals(samples, config.confidence_level)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = SimulationResult(
                simulation_id=simulation_id,
                config=config,
                samples=samples,
                statistics=statistics,
                risk_metrics=risk_metrics,
                confidence_intervals=confidence_intervals,
                execution_time=execution_time,
                timestamp=start_time
            )
            
            # Cache results if enabled
            if config.cache_results:
                await self._cache_result(result)
            
            # Update performance metrics
            self._update_performance_metrics(result)
            
            logger.info(f"Simulation {simulation_id} completed in {execution_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in simulation {simulation_id}: {e}")
            raise
    
    def _get_scenario_template(self, domain: DomainType, scenario_name: str) -> Dict[str, Any]:
        """Get scenario template for domain and scenario."""
        if domain not in self.scenario_templates:
            raise ValueError(f"Domain {domain.value} not supported")
        
        domain_templates = self.scenario_templates[domain]
        if scenario_name not in domain_templates:
            raise ValueError(f"Scenario {scenario_name} not found for domain {domain.value}")
        
        return domain_templates[scenario_name]
    
    def _merge_custom_variables(self, template: Dict[str, Any], custom_variables: Dict[str, Any]) -> Dict[str, Any]:
        """Merge custom variables with template."""
        merged = template.copy()
        
        if "variables" in custom_variables:
            merged["variables"].update(custom_variables["variables"])
        
        if "correlations" in custom_variables:
            # Validate correlation matrix dimensions
            new_vars = len(custom_variables.get("variables", {}))
            if new_vars > 0:
                # Extend correlation matrix for new variables
                old_size = len(merged["correlations"])
                new_size = old_size + new_vars
                
                # Create extended correlation matrix
                extended_corr = np.eye(new_size)
                extended_corr[:old_size, :old_size] = merged["correlations"]
                
                # Add custom correlations if provided
                if "correlations" in custom_variables:
                    custom_corr = custom_variables["correlations"]
                    extended_corr[old_size:, old_size:] = custom_corr
                
                merged["correlations"] = extended_corr.tolist()
        
        return merged
    
    async def _run_monte_carlo_simulation(
        self,
        scenario: Dict[str, Any],
        config: SimulationConfig
    ) -> np.ndarray:
        """Run the actual Monte Carlo simulation."""
        
        variables = scenario["variables"]
        correlations = scenario.get("correlations", [])
        
        # Generate correlated samples
        if correlations and len(correlations) > 0:
            samples = self._generate_correlated_samples(variables, correlations, config.num_iterations)
        else:
            samples = self._generate_independent_samples(variables, config.num_iterations)
        
        return samples
    
    def _generate_correlated_samples(
        self,
        variables: Dict[str, Any],
        correlations: List[List[float]],
        num_iterations: int
    ) -> np.ndarray:
        """Generate correlated samples using Cholesky decomposition."""
        
        # Convert correlation matrix to numpy array
        corr_matrix = np.array(correlations)
        
        # Ensure correlation matrix is positive definite
        try:
            cholesky_factor = np.linalg.cholesky(corr_matrix)
        except np.linalg.LinAlgError:
            # If not positive definite, use nearest positive definite matrix
            eigenvals, eigenvecs = np.linalg.eigh(corr_matrix)
            eigenvals = np.maximum(eigenvals, 1e-8)
            corr_matrix = eigenvecs @ np.diag(eigenvals) @ eigenvecs.T
            cholesky_factor = np.linalg.cholesky(corr_matrix)
        
        # Generate independent standard normal samples
        n_vars = len(variables)
        independent_samples = np.random.standard_normal((num_iterations, n_vars))
        
        # Transform to correlated samples
        correlated_normal = independent_samples @ cholesky_factor.T
        
        # Transform to desired distributions
        samples = np.zeros((num_iterations, n_vars))
        var_names = list(variables.keys())
        
        for i, var_name in enumerate(var_names):
            var_config = variables[var_name]
            distribution = var_config["distribution"]
            parameters = var_config["parameters"]
            
            # Transform normal samples to desired distribution
            samples[:, i] = self._transform_to_distribution(
                correlated_normal[:, i], distribution, parameters
            )
        
        return samples
    
    def _generate_independent_samples(
        self,
        variables: Dict[str, Any],
        num_iterations: int
    ) -> np.ndarray:
        """Generate independent samples for each variable."""
        
        n_vars = len(variables)
        samples = np.zeros((num_iterations, n_vars))
        var_names = list(variables.keys())
        
        for i, var_name in enumerate(var_names):
            var_config = variables[var_name]
            distribution = var_config["distribution"]
            parameters = var_config["parameters"]
            
            samples[:, i] = self._generate_distribution_samples(
                distribution, parameters, num_iterations
            )
        
        return samples
    
    def _generate_distribution_samples(
        self,
        distribution: str,
        parameters: Dict[str, float],
        num_iterations: int
    ) -> np.ndarray:
        """Generate samples from a specific distribution."""
        
        if distribution == "normal":
            return np.random.normal(parameters["mean"], parameters["std"], num_iterations)
        elif distribution == "lognormal":
            return np.random.lognormal(parameters["mean"], parameters["std"], num_iterations)
        elif distribution == "beta":
            return np.random.beta(parameters["alpha"], parameters["beta"], num_iterations)
        elif distribution == "gamma":
            return np.random.gamma(parameters["alpha"], parameters["beta"], num_iterations)
        elif distribution == "exponential":
            return np.random.exponential(parameters["lambda"], num_iterations)
        elif distribution == "poisson":
            return np.random.poisson(parameters["lambda"], num_iterations)
        else:
            raise ValueError(f"Distribution {distribution} not supported")
    
    def _transform_to_distribution(
        self,
        normal_samples: np.ndarray,
        target_distribution: str,
        parameters: Dict[str, float]
    ) -> np.ndarray:
        """Transform normal samples to target distribution using inverse CDF."""
        
        if target_distribution == "normal":
            return normal_samples * parameters["std"] + parameters["mean"]
        elif target_distribution == "lognormal":
            return np.exp(normal_samples * parameters["std"] + parameters["mean"])
        elif target_distribution == "beta":
            # Use Box-Muller transform for beta distribution
            from scipy.stats import beta
            return beta.ppf(norm.cdf(normal_samples), parameters["alpha"], parameters["beta"])
        elif target_distribution == "gamma":
            from scipy.stats import gamma
            return gamma.ppf(norm.cdf(normal_samples), parameters["alpha"], scale=parameters["beta"])
        else:
            # For other distributions, use direct generation
            return self._generate_distribution_samples(target_distribution, parameters, len(normal_samples))
    
    def _calculate_statistics(
        self,
        samples: np.ndarray,
        variables: Dict[str, Any]
    ) -> Dict[str, Dict[str, float]]:
        """Calculate descriptive statistics for each variable."""
        
        statistics = {}
        var_names = list(variables.keys())
        
        for i, var_name in enumerate(var_names):
            var_data = samples[:, i]
            
            statistics[var_name] = {
                "mean": float(np.mean(var_data)),
                "std": float(np.std(var_data)),
                "min": float(np.min(var_data)),
                "max": float(np.max(var_data)),
                "median": float(np.median(var_data)),
                "q25": float(np.percentile(var_data, 25)),
                "q75": float(np.percentile(var_data, 75)),
                "skewness": float(self._calculate_skewness(var_data)),
                "kurtosis": float(self._calculate_kurtosis(var_data))
            }
        
        return statistics
    
    def _calculate_risk_metrics(self, samples: np.ndarray) -> Dict[str, float]:
        """Calculate risk metrics from samples."""
        
        # Calculate portfolio-like metrics (assuming first variable is the main metric)
        main_metric = samples[:, 0]
        
        # Value at Risk (VaR)
        var_95 = np.percentile(main_metric, 5)  # 95% VaR
        var_99 = np.percentile(main_metric, 1)  # 99% VaR
        
        # Conditional Value at Risk (CVaR)
        cvar_95 = np.mean(main_metric[main_metric <= var_95])
        cvar_99 = np.mean(main_metric[main_metric <= var_99])
        
        # Expected loss
        expected_loss = np.mean(np.minimum(main_metric, 0))
        
        # Worst case scenario
        worst_case = np.min(main_metric)
        
        return {
            "var_95": float(var_95),
            "var_99": float(var_99),
            "cvar_95": float(cvar_95),
            "cvar_99": float(cvar_99),
            "expected_loss": float(expected_loss),
            "worst_case": float(worst_case)
        }
    
    def _calculate_confidence_intervals(
        self,
        samples: np.ndarray,
        confidence_level: float
    ) -> Dict[str, Dict[str, float]]:
        """Calculate confidence intervals for each variable."""
        
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        confidence_intervals = {}
        
        for i in range(samples.shape[1]):
            var_data = samples[:, i]
            
            confidence_intervals[f"variable_{i}"] = {
                "lower": float(np.percentile(var_data, lower_percentile)),
                "upper": float(np.percentile(var_data, upper_percentile)),
                "confidence_level": confidence_level
            }
        
        return confidence_intervals
    
    def _calculate_skewness(self, data: np.ndarray) -> float:
        """Calculate skewness of data."""
        mean = np.mean(data)
        std = np.std(data)
        n = len(data)
        
        if std == 0:
            return 0.0
        
        skewness = (n / ((n - 1) * (n - 2))) * np.sum(((data - mean) / std) ** 3)
        return skewness
    
    def _calculate_kurtosis(self, data: np.ndarray) -> float:
        """Calculate kurtosis of data."""
        mean = np.mean(data)
        std = np.std(data)
        n = len(data)
        
        if std == 0:
            return 0.0
        
        kurtosis = (n * (n + 1) / ((n - 1) * (n - 2) * (n - 3))) * np.sum(((data - mean) / std) ** 4) - (3 * (n - 1) ** 2 / ((n - 2) * (n - 3)))
        return kurtosis
    
    async def _cache_result(self, result: SimulationResult):
        """Cache simulation result."""
        cache_file = self.cache_dir / f"{result.simulation_id}.json"
        
        # Convert result to serializable format
        cache_data = {
            "simulation_id": result.simulation_id,
            "config": {
                "domain": result.config.domain.value,
                "simulation_type": result.config.simulation_type.value,
                "num_iterations": result.config.num_iterations,
                "confidence_level": result.config.confidence_level,
                "time_horizon": result.config.time_horizon,
                "parallel_processing": result.config.parallel_processing,
                "include_advanced_analytics": result.config.include_advanced_analytics,
                "cache_results": result.config.cache_results,
                "metadata": result.config.metadata
            },
            "samples": result.samples.tolist(),
            "statistics": result.statistics,
            "risk_metrics": result.risk_metrics,
            "confidence_intervals": result.confidence_intervals,
            "execution_time": result.execution_time,
            "timestamp": result.timestamp.isoformat(),
            "metadata": result.metadata
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
    
    def _update_performance_metrics(self, result: SimulationResult):
        """Update performance tracking metrics."""
        domain = result.config.domain.value
        sim_type = result.config.simulation_type.value
        
        if domain not in self.performance_metrics:
            self.performance_metrics[domain] = {}
        
        if sim_type not in self.performance_metrics[domain]:
            self.performance_metrics[domain][sim_type] = []
        
        self.performance_metrics[domain][sim_type].append({
            "execution_time": result.execution_time,
            "num_iterations": result.config.num_iterations,
            "timestamp": result.timestamp.isoformat()
        })
        
        # Keep only last 100 entries
        if len(self.performance_metrics[domain][sim_type]) > 100:
            self.performance_metrics[domain][sim_type] = self.performance_metrics[domain][sim_type][-100:]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary across all domains."""
        summary = {}
        
        for domain, sim_types in self.performance_metrics.items():
            summary[domain] = {}
            
            for sim_type, metrics in sim_types.items():
                if metrics:
                    execution_times = [m["execution_time"] for m in metrics]
                    summary[domain][sim_type] = {
                        "total_simulations": len(metrics),
                        "avg_execution_time": np.mean(execution_times),
                        "min_execution_time": np.min(execution_times),
                        "max_execution_time": np.max(execution_times),
                        "std_execution_time": np.std(execution_times)
                    }
        
        return summary
    
    def get_available_scenarios(self) -> Dict[str, List[str]]:
        """Get available scenarios for each domain."""
        scenarios = {}
        
        for domain, templates in self.scenario_templates.items():
            scenarios[domain.value] = list(templates.keys())
        
        return scenarios
    
    async def load_cached_result(self, simulation_id: str) -> Optional[SimulationResult]:
        """Load cached simulation result."""
        cache_file = self.cache_dir / f"{simulation_id}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Reconstruct SimulationResult object
            config = SimulationConfig(
                domain=DomainType(cache_data["config"]["domain"]),
                simulation_type=SimulationType(cache_data["config"]["simulation_type"]),
                num_iterations=cache_data["config"]["num_iterations"],
                confidence_level=cache_data["config"]["confidence_level"],
                time_horizon=cache_data["config"]["time_horizon"],
                parallel_processing=cache_data["config"]["parallel_processing"],
                include_advanced_analytics=cache_data["config"]["include_advanced_analytics"],
                cache_results=cache_data["config"]["cache_results"],
                metadata=cache_data["config"]["metadata"]
            )
            
            result = SimulationResult(
                simulation_id=cache_data["simulation_id"],
                config=config,
                samples=np.array(cache_data["samples"]),
                statistics=cache_data["statistics"],
                risk_metrics=cache_data["risk_metrics"],
                confidence_intervals=cache_data["confidence_intervals"],
                execution_time=cache_data["execution_time"],
                timestamp=datetime.fromisoformat(cache_data["timestamp"]),
                metadata=cache_data.get("metadata", {})
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error loading cached result {simulation_id}: {e}")
            return None


# Import scipy for advanced statistical functions
try:
    from scipy.stats import norm
except ImportError:
    # Fallback implementation
    def norm_cdf(x):
        return 0.5 * (1 + np.sign(x) * np.sqrt(1 - np.exp(-2 * x**2 / np.pi)))
    
    class norm:
        @staticmethod
        def cdf(x):
            return norm_cdf(x)
