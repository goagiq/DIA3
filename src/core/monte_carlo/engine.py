"""
Monte Carlo Engine
Core Monte Carlo simulation engine with Phase 5 advanced features
"""

import numpy as np
import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import uuid
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

from .config import MonteCarloConfig
from .distributions import DistributionLibrary
from .correlations import CorrelationEngine
from .scenarios import ScenarioGenerator
from .analysis import ResultAnalyzer

logger = logging.getLogger(__name__)


class MonteCarloEngine:
    """Core Monte Carlo simulation engine with Phase 5 advanced features"""
    
    def __init__(self, config: Optional[MonteCarloConfig] = None):
        self.config = config or MonteCarloConfig()
        self.distributions = DistributionLibrary()
        self.correlations = CorrelationEngine()
        self.scenarios = ScenarioGenerator()
        self.analyzer = ResultAnalyzer()
        
        # Phase 5: Performance Optimization
        self.cache = self._initialize_cache()
        self.memory_cache = {}  # Simple in-memory cache fallback
        self.executor = self._initialize_executor()
        
        # Phase 5: Security & Compliance
        self.audit_log = []
        self.data_classification = "UNCLASSIFIED"
        
        # Phase 5: Dynamic Scenarios
        self.real_time_data_sources = {}
        self.event_handlers = {}
        
        # Set random seed
        np.random.seed(self.config.seed)
        
        logger.info("Monte Carlo Engine initialized with Phase 5 features")
    
    def _initialize_cache(self) -> Optional[Any]:
        """Initialize Redis cache for result caching"""
        if not REDIS_AVAILABLE:
            logger.warning("Redis module not available - caching disabled")
            self.config.cache_results = False
            return None
            
        try:
            if self.config.cache_results:
                # Test Redis connection with shorter timeout
                redis_client = redis.Redis(
                    host='localhost',
                    port=6379,
                    db=0,
                    decode_responses=True,
                    socket_connect_timeout=0.5,
                    socket_timeout=0.5,
                    retry_on_timeout=False
                )
                # Test connection
                redis_client.ping()
                logger.info("Redis cache initialized successfully")
                return redis_client
        except (redis.ConnectionError, redis.TimeoutError, Exception) as e:
            logger.warning(f"Redis cache not available: {e}")
            # Disable caching when Redis is not available
            self.config.cache_results = False
            logger.info("Caching disabled - Redis not available")
        return None
    
    def _initialize_executor(self) -> ProcessPoolExecutor:
        """Initialize process pool executor for parallel processing"""
        max_workers = min(self.config.max_workers, mp.cpu_count())
        return ProcessPoolExecutor(max_workers=max_workers)
    
    def _log_audit_event(self, event_type: str, details: Dict[str, Any]):
        """Log audit event for compliance"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details,
            "data_classification": self.data_classification
        }
        self.audit_log.append(event)
        logger.info(f"Audit event: {event_type} - {details}")
    
    def _get_cache_key(self, scenario_config: Dict[str, Any], 
                      num_iterations: int) -> str:
        """Generate cache key for scenario configuration"""
        config_hash = hashlib.md5(
            json.dumps(scenario_config, sort_keys=True).encode()
        ).hexdigest()
        return f"monte_carlo:{config_hash}:{num_iterations}"
    
    async def run_simulation(self, 
                           scenario_config: Dict[str, Any],
                           num_iterations: Optional[int] = None,
                           parallel: bool = True) -> Dict[str, Any]:
        """Run Monte Carlo simulation with Phase 5 enhancements"""
        
        start_time = datetime.now()
        simulation_id = str(uuid.uuid4())
        
        # Phase 5: Security & Compliance
        self._log_audit_event("simulation_start", {
            "simulation_id": simulation_id,
            "scenario_type": scenario_config.get("type", "custom")
        })
        
        logger.info(f"Starting Monte Carlo simulation {simulation_id}")
        
        try:
            # Phase 5: Performance Optimization - Check cache
            cache_key = self._get_cache_key(scenario_config, num_iterations or self.config.default_iterations)
            
            # Try Redis cache first
            if self.cache and self.config.cache_results:
                try:
                    cached_result = self.cache.get(cache_key)
                    if cached_result:
                        logger.info(f"Using Redis cached result for simulation {simulation_id}")
                        result = json.loads(cached_result)
                        result["cached"] = True
                        return result
                except Exception as e:
                    logger.warning(f"Failed to check Redis cache: {e}")
            
            # Try in-memory cache as fallback
            if cache_key in self.memory_cache:
                logger.info(f"Using in-memory cached result for simulation {simulation_id}")
                result = self.memory_cache[cache_key].copy()
                result["cached"] = True
                return result
            
            # Validate scenario
            if not self.scenarios.validate_scenario(scenario_config):
                raise ValueError("Invalid scenario configuration")
            
            # Set number of iterations
            if num_iterations is None:
                num_iterations = self.config.default_iterations
            
            # Phase 5: Dynamic Scenarios - Check for real-time data
            scenario_config = await self._enhance_with_real_time_data(scenario_config)
            
            # Generate samples with Phase 5 optimizations
            samples = await self._generate_samples_optimized(scenario_config, num_iterations, parallel)
            
            # Analyze results with Phase 5 advanced analytics
            results = await self._analyze_results_advanced(samples, scenario_config)
            
            # Add metadata
            results["simulation_id"] = simulation_id
            results["start_time"] = start_time.isoformat()
            results["end_time"] = datetime.now().isoformat()
            results["num_iterations"] = num_iterations
            results["scenario_config"] = scenario_config
            results["phase5_features"] = {
                "parallel_processing": parallel,
                "caching_enabled": self.config.cache_results,
                "security_compliance": True,
                "dynamic_scenarios": bool(scenario_config.get("real_time_data"))
            }
            
            # Phase 5: Performance Optimization - Cache results
            # Try Redis cache first
            if self.cache and self.config.cache_results:
                try:
                    self.cache.setex(cache_key, 3600, json.dumps(results))  # Cache for 1 hour
                    logger.info(f"Cached results in Redis for simulation {simulation_id}")
                except Exception as e:
                    logger.warning(f"Failed to cache results in Redis: {e}")
            
            # Always cache in memory as fallback
            self.memory_cache[cache_key] = results.copy()
            logger.info(f"Cached results in memory for simulation {simulation_id}")
            
            # Phase 5: Security & Compliance
            self._log_audit_event("simulation_complete", {
                "simulation_id": simulation_id,
                "duration": (datetime.now() - start_time).total_seconds()
            })
            
            logger.info(f"Monte Carlo simulation {simulation_id} completed successfully")
            
            return results
            
        except Exception as e:
            # Phase 5: Security & Compliance
            self._log_audit_event("simulation_error", {
                "simulation_id": simulation_id,
                "error": str(e)
            })
            logger.error(f"Error in Monte Carlo simulation {simulation_id}: {e}")
            raise
    
    async def _enhance_with_real_time_data(self, scenario_config: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance scenario with real-time data sources"""
        if "real_time_data_sources" in scenario_config:
            enhanced_config = scenario_config.copy()
            real_time_data = {}
            
            for source_name, source_config in scenario_config["real_time_data_sources"].items():
                if source_name in self.real_time_data_sources:
                    data = await self.real_time_data_sources[source_name].get_latest_data()
                    real_time_data[source_name] = data
            
            enhanced_config["real_time_data"] = real_time_data
            return enhanced_config
        
        return scenario_config
    
    async def _generate_samples_optimized(self, 
                                        scenario_config: Dict[str, Any],
                                        num_iterations: int,
                                        parallel: bool) -> np.ndarray:
        """Generate samples with Phase 5 performance optimizations"""
        
        if parallel and num_iterations > 10000:
            # Use parallel processing for large simulations
            return await self._generate_samples_parallel(scenario_config, num_iterations)
        else:
            # Use optimized single-threaded approach for smaller simulations
            return self._generate_samples_sync(scenario_config, num_iterations)
    
    async def _generate_samples_parallel(self, 
                                       scenario_config: Dict[str, Any],
                                       num_iterations: int) -> np.ndarray:
        """Generate samples using parallel processing"""
        
        # Split iterations across processes
        num_processes = min(self.config.max_workers, mp.cpu_count())
        iterations_per_process = num_iterations // num_processes
        
        # Create tasks for parallel execution
        tasks = []
        for i in range(num_processes):
            start_iter = i * iterations_per_process
            end_iter = start_iter + iterations_per_process if i < num_processes - 1 else num_iterations
            task = self._generate_samples_chunk(scenario_config, start_iter, end_iter)
            tasks.append(task)
        
        # Execute tasks in parallel
        results = await asyncio.gather(*tasks)
        
        # Combine results
        combined_samples = np.vstack(results)
        return combined_samples
    
    async def _generate_samples_chunk(self, 
                                    scenario_config: Dict[str, Any],
                                    start_iter: int,
                                    end_iter: int) -> np.ndarray:
        """Generate samples for a chunk of iterations"""
        
        loop = asyncio.get_event_loop()
        chunk_iterations = end_iter - start_iter
        
        # Run in process pool to avoid GIL
        return await loop.run_in_executor(
            self.executor,
            self._generate_samples_sync,
            scenario_config,
            chunk_iterations
        )
    
    async def _analyze_results_advanced(self, 
                                      samples: np.ndarray,
                                      scenario_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze results with Phase 5 advanced analytics"""
        
        results = {}
        
        # Basic statistics
        if scenario_config.get("include_statistics", True):
            results["statistics"] = self.analyzer.calculate_statistics(samples)
        
        # Phase 5: Advanced Analytics - Enhanced risk metrics
        if scenario_config.get("include_risk_metrics", True):
            results["risk_metrics"] = self.analyzer.calculate_risk_metrics(
                samples, self.config.confidence_level
            )
            
            # Phase 5: Advanced Analytics - Failure Mode Analysis
            if scenario_config.get("include_failure_analysis", True):
                results["failure_analysis"] = self.analyzer.calculate_failure_modes(samples)
            
            # Phase 5: Advanced Analytics - Risk Prioritization
            if scenario_config.get("include_risk_prioritization", True):
                results["risk_prioritization"] = self.analyzer.prioritize_risks(samples)
        
        # Phase 5: Advanced Analytics - Stress Testing
        if scenario_config.get("include_stress_testing", True):
            results["stress_testing"] = self.analyzer.perform_stress_tests(samples, scenario_config)
        
        # Variable names
        variable_names = list(scenario_config["variables"].keys())
        results["variable_names"] = variable_names
        
        # Sample summary
        results["sample_summary"] = {
            "total_samples": len(samples),
            "num_variables": len(variable_names),
            "sample_shape": samples.shape
        }
        
        # Add samples for JSON serialization
        results["samples"] = samples.tolist()
        
        return results
    
    def _run_simulation_sync(self, 
                           scenario_config: Dict[str, Any],
                           num_iterations: Optional[int] = None) -> Dict[str, Any]:
        """Run Monte Carlo simulation synchronously"""
        
        start_time = datetime.now()
        simulation_id = str(uuid.uuid4())
        
        logger.info(f"Starting Monte Carlo simulation {simulation_id}")
        
        try:
            # Validate scenario
            if not self.scenarios.validate_scenario(scenario_config):
                raise ValueError("Invalid scenario configuration")
            
            # Set number of iterations
            if num_iterations is None:
                num_iterations = self.config.default_iterations
            
            # Generate samples synchronously
            samples = self._generate_samples_sync(scenario_config, num_iterations)
            
            # Analyze results synchronously
            results = self._analyze_results_sync(samples, scenario_config)
            
            # Add metadata
            results["simulation_id"] = simulation_id
            results["start_time"] = start_time.isoformat()
            results["end_time"] = datetime.now().isoformat()
            results["num_iterations"] = num_iterations
            results["scenario_config"] = scenario_config
            
            logger.info(f"Monte Carlo simulation {simulation_id} completed successfully")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in Monte Carlo simulation {simulation_id}: {e}")
            raise
    
    def _generate_samples_sync(self, 
                              scenario_config: Dict[str, Any],
                              num_iterations: int) -> np.ndarray:
        """Generate samples for the simulation synchronously"""
        
        variables = scenario_config["variables"]
        correlations = scenario_config.get("correlations", [])
        
        # Extract distribution information
        distributions = []
        params = []
        
        for var_name, var_config in variables.items():
            distributions.append(var_config["distribution"])
            params.append(var_config["parameters"])
        
        # Generate correlated samples
        if len(distributions) > 1 and correlations:
            samples = self.correlations.generate_correlated_samples(
                distributions, params, correlations, num_iterations
            )
        else:
            # Generate independent samples
            samples = np.zeros((num_iterations, len(distributions)))
            for i, (dist, param) in enumerate(zip(distributions, params)):
                samples[:, i] = self.distributions.sample(dist, param, num_iterations)
        
        return samples
    
    def _analyze_results_sync(self, 
                            samples: np.ndarray,
                            scenario_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze simulation results synchronously"""
        
        results = {}
        
        # Basic statistics
        if scenario_config.get("include_statistics", True):
            results["statistics"] = self.analyzer.calculate_statistics(samples)
        
        # Risk metrics
        if scenario_config.get("include_risk_metrics", True):
            results["risk_metrics"] = self.analyzer.calculate_risk_metrics(
                samples, self.config.confidence_level
            )
        
        # Variable names
        variable_names = list(scenario_config["variables"].keys())
        results["variable_names"] = variable_names
        
        # Sample summary
        results["sample_summary"] = {
            "total_samples": len(samples),
            "num_variables": len(variable_names),
            "sample_shape": samples.shape
        }
        
        # Add samples for JSON serialization
        results["samples"] = samples.tolist()
        
        return results
    
    def run_scenario_simulation(self, 
                              scenario_type: str,
                              parameters: Dict[str, Any],
                              num_iterations: Optional[int] = None,
                              time_horizon: Optional[int] = None) -> Dict[str, Any]:
        """Run simulation using a predefined scenario template"""
        
        # Generate scenario
        scenario = self.scenarios.generate_scenario(scenario_type, parameters, time_horizon)
        
        # Run simulation synchronously
        return self._run_simulation_sync(scenario, num_iterations)
    
    def run_custom_simulation(self, 
                            variables: Dict[str, Dict[str, Any]],
                            correlations: Optional[List[List[float]]] = None,
                            num_iterations: Optional[int] = None) -> Dict[str, Any]:
        """Run simulation with custom variable definitions"""
        
        # Create scenario configuration
        if correlations is None:
            # Create identity correlation matrix for independent variables
            num_vars = len(variables)
            correlations = [[1.0 if i == j else 0.0 for j in range(num_vars)] for i in range(num_vars)]
        
        scenario_config = {
            "variables": variables,
            "correlations": correlations,
            "include_statistics": True,
            "include_risk_metrics": True,
            "include_visualizations": True
        }
        
        # Run simulation synchronously
        return self._run_simulation_sync(scenario_config, num_iterations)
    
    def run_time_series_simulation(self, 
                                 base_scenario: Dict[str, Any],
                                 time_steps: int,
                                 num_iterations: Optional[int] = None) -> Dict[str, Any]:
        """Run time series Monte Carlo simulation"""
        
        # Generate time series scenario
        scenario = self.scenarios.generate_time_series_scenario(base_scenario, time_steps)
        
        # Run simulation synchronously
        return self._run_simulation_sync(scenario, num_iterations)
    
    def get_simulation_status(self) -> Dict[str, Any]:
        """Get current simulation engine status"""
        
        return {
            "engine_version": "1.0.0",
            "config": {
                "max_workers": self.config.max_workers,
                "use_gpu": self.config.use_gpu,
                "cache_results": self.config.cache_results,
                "default_iterations": self.config.default_iterations,
                "confidence_level": self.config.confidence_level
            },
            "supported_distributions": self.distributions.list_supported_distributions(),
            "supported_scenarios": self.scenarios.list_scenario_types(),
            "supported_copulas": self.correlations.supported_copulas
        }
    
    def validate_configuration(self) -> bool:
        """Validate engine configuration"""
        
        try:
            # Test distribution sampling
            test_samples = self.distributions.sample("normal", {"mean": 0, "std": 1}, 10)
            if len(test_samples) != 10:
                return False
            
            # Test correlation matrix generation
            test_corr = self.correlations.generate_correlation_matrix(3, "random")
            if test_corr.shape != (3, 3):
                return False
            
            # Test scenario generation
            test_scenario = self.scenarios.generate_scenario(
                "risk_assessment", {}, None
            )
            if not self.scenarios.validate_scenario(test_scenario):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    def get_scenario_info(self, scenario_type: str) -> Dict[str, Any]:
        """Get information about available scenarios"""
        return self.scenarios.get_scenario_info(scenario_type)
    
    def get_distribution_info(self, distribution_type: str) -> Dict[str, Any]:
        """Get information about available distributions"""
        return self.distributions.get_distribution_info(distribution_type)
    
    def list_available_scenarios(self) -> List[str]:
        """List all available scenario types"""
        return self.scenarios.list_scenario_types()
    
    def list_available_distributions(self) -> List[str]:
        """List all available distribution types"""
        return self.distributions.list_supported_distributions()
    
    def estimate_correlation_matrix(self, samples: np.ndarray) -> np.ndarray:
        """Estimate correlation matrix from samples"""
        return self.correlations.estimate_correlation_matrix(samples)
    
    def test_correlation_significance(self, 
                                    samples: np.ndarray,
                                    alpha: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
        """Test significance of correlations in samples"""
        return self.correlations.test_correlation_significance(samples, alpha)
    
    def generate_correlation_matrix(self, 
                                  size: int,
                                  method: str = "random",
                                  **kwargs) -> np.ndarray:
        """Generate a valid correlation matrix"""
        return self.correlations.generate_correlation_matrix(size, method, **kwargs)
