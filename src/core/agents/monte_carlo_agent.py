"""
Monte Carlo Agent
Agent for orchestrator integration to handle Monte Carlo simulation requests
"""

import asyncio
import logging
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime

from ..monte_carlo.engine import MonteCarloEngine
from ..monte_carlo.config import MonteCarloConfig
from ..models import DataType, AnalysisRequest, AnalysisResult, ProcessingStatus
from src.agents.base_agent import StrandsBaseAgent

logger = logging.getLogger(__name__)


class MonteCarloAgent(StrandsBaseAgent):
    """Monte Carlo simulation agent for orchestrator integration"""
    
    def __init__(self, config: Optional[MonteCarloConfig] = None):
        super().__init__(agent_id=f"MonteCarloAgent_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.engine = MonteCarloEngine(config)
        self.supported_data_types = [DataType.NUMERICAL, DataType.TIME_SERIES]
        
        logger.info(f"Monte Carlo Agent {self.agent_id} initialized successfully")
    
    async def can_process(self, request: AnalysisRequest) -> bool:
        """Check if this agent can process the given request."""
        return request.data_type in self.supported_data_types
    
    async def process(self, request: AnalysisRequest) -> AnalysisResult:
        """Process Monte Carlo simulation request"""
        
        try:
            logger.info(f"Processing Monte Carlo request: {request.id}")
            
            # Extract simulation parameters from request
            simulation_params = self._extract_simulation_params(request)
            
            # Run simulation based on request type
            request_type = getattr(request, 'request_type', 'monte_carlo_scenario')
            if request_type == "monte_carlo_scenario":
                result = await self._run_scenario_simulation(simulation_params)
            elif request_type == "monte_carlo_custom":
                result = await self._run_custom_simulation(simulation_params)
            elif request_type == "monte_carlo_time_series":
                result = await self._run_time_series_simulation(simulation_params)
            elif request_type == "monte_carlo_analysis":
                result = await self._run_analysis_only(simulation_params)
            else:
                raise ValueError(f"Unsupported request type: {request_type}")
            
            # Create response
            response = AnalysisResult(
                id=request.id,
                status=ProcessingStatus.COMPLETED,
                data_type=request.data_type,
                content=request.content,
                result=result,
                metadata={
                    "simulation_type": request_type,
                    "timestamp": datetime.now().isoformat(),
                    "agent_version": "1.0.0",
                    "agent_id": self.agent_id
                }
            )
            
            logger.info(f"Monte Carlo request {request.id} completed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error processing Monte Carlo request {request.id}: {e}")
            
            return AnalysisResult(
                id=request.id,
                status=ProcessingStatus.FAILED,
                data_type=request.data_type,
                content=request.content,
                error=str(e),
                metadata={
                    "timestamp": datetime.now().isoformat(),
                    "agent_version": "1.0.0",
                    "agent_id": self.agent_id
                }
            )
    
    def _extract_simulation_params(self, request: AnalysisRequest) -> Dict[str, Any]:
        """Extract simulation parameters from request"""
        
        params = {}
        
        # Extract basic parameters from request metadata
        if hasattr(request, 'metadata') and request.metadata:
            params.update(request.metadata)
        
        # Extract specific Monte Carlo parameters from request content
        if hasattr(request, 'content') and request.content:
            if isinstance(request.content, dict):
                params.update(request.content)
        
        # Set defaults if not provided
        if "num_iterations" not in params:
            params["num_iterations"] = self.engine.config.default_iterations
        
        if "confidence_level" not in params:
            params["confidence_level"] = self.engine.config.confidence_level
        
        return params
    
    async def _run_scenario_simulation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run simulation using predefined scenario"""
        
        scenario_type = params.get("scenario_type", "risk_assessment")
        scenario_params = params.get("scenario_parameters", {})
        num_iterations = params.get("num_iterations")
        time_horizon = params.get("time_horizon")
        
        # Run simulation
        result = self.engine.run_scenario_simulation(
            scenario_type, scenario_params, num_iterations, time_horizon
        )
        
        return result
    
    async def _run_custom_simulation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run simulation with custom variable definitions"""
        
        variables = params.get("variables", {})
        correlations = params.get("correlations")
        num_iterations = params.get("num_iterations")
        
        # Run simulation
        result = self.engine.run_custom_simulation(
            variables, correlations, num_iterations
        )
        
        return result
    
    async def _run_time_series_simulation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run time series Monte Carlo simulation"""
        
        base_scenario = params.get("base_scenario", {})
        time_steps = params.get("time_steps", 100)
        num_iterations = params.get("num_iterations")
        
        # Run simulation
        result = self.engine.run_time_series_simulation(
            base_scenario, time_steps, num_iterations
        )
        
        return result
    
    async def _run_analysis_only(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Run analysis on existing data without simulation"""
        
        samples = params.get("samples")
        variable_names = params.get("variable_names")
        
        if samples is None:
            raise ValueError("Samples data required for analysis-only request")
        
        # Convert to numpy array if needed
        if not isinstance(samples, np.ndarray):
            samples = np.array(samples)
        
        # Run analysis
        result = self.engine.analyzer.generate_summary_report(samples, variable_names)
        
        return result
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information"""
        
        return {
            "agent_id": self.agent_id,
            "agent_type": "MonteCarloAgent",
            "version": "1.0.0",
            "supported_data_types": [dt.value for dt in self.supported_data_types],
            "supported_request_types": [
                "monte_carlo_scenario",
                "monte_carlo_custom", 
                "monte_carlo_time_series",
                "monte_carlo_analysis"
            ],
            "engine_status": self.engine.get_simulation_status(),
            "available_scenarios": self.engine.list_available_scenarios(),
            "available_distributions": self.engine.list_available_distributions()
        }
    
    def validate_configuration(self) -> bool:
        """Validate agent configuration"""
        
        try:
            # Validate engine configuration
            if not self.engine.validate_configuration():
                logger.error("Monte Carlo engine configuration validation failed")
                return False
            
            # Test basic functionality (synchronous version)
            test_result = self._test_basic_functionality_sync()
            if not test_result:
                logger.error("Basic functionality test failed")
                return False
            
            logger.info("Monte Carlo agent configuration validated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    async def _test_basic_functionality(self) -> bool:
        """Test basic agent functionality"""
        
        try:
            # Test scenario simulation
            test_params = {
                "scenario_type": "risk_assessment",
                "scenario_parameters": {},
                "num_iterations": 100
            }
            
            result = await self._run_scenario_simulation(test_params)
            
            # Check if result contains expected keys
            expected_keys = ["simulation_id", "statistics", "risk_metrics"]
            for key in expected_keys:
                if key not in result:
                    logger.error(f"Missing expected key in test result: {key}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Basic functionality test failed: {e}")
            return False
    
    def _test_basic_functionality_sync(self) -> bool:
        """Test basic agent functionality (synchronous version)"""
        
        try:
            # Test engine status
            status = self.engine.get_simulation_status()
            if not status:
                logger.error("Engine status check failed")
                return False
            
            # Test scenario listing
            scenarios = self.engine.list_available_scenarios()
            if not scenarios:
                logger.error("Scenario listing failed")
                return False
            
            # Test distribution listing
            distributions = self.engine.list_available_distributions()
            if not distributions:
                logger.error("Distribution listing failed")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Basic functionality test failed: {e}")
            return False
    
    def get_supported_scenarios(self) -> List[str]:
        """Get list of supported scenario types"""
        return self.engine.list_available_scenarios()
    
    def get_scenario_info(self, scenario_type: str) -> Dict[str, Any]:
        """Get information about a specific scenario type"""
        return self.engine.get_scenario_info(scenario_type)
    
    def get_supported_distributions(self) -> List[str]:
        """Get list of supported distribution types"""
        return self.engine.list_available_distributions()
    
    def get_distribution_info(self, distribution_type: str) -> Dict[str, Any]:
        """Get information about a specific distribution type"""
        return self.engine.get_distribution_info(distribution_type)
    
    def estimate_correlation_matrix(self, samples: np.ndarray) -> np.ndarray:
        """Estimate correlation matrix from samples"""
        return self.engine.estimate_correlation_matrix(samples)
    
    def test_correlation_significance(self, 
                                    samples: np.ndarray,
                                    alpha: float = 0.05) -> tuple:
        """Test significance of correlations in samples"""
        return self.engine.test_correlation_significance(samples, alpha)
    
    def generate_correlation_matrix(self, 
                                  size: int,
                                  method: str = "random",
                                  **kwargs) -> np.ndarray:
        """Generate a valid correlation matrix"""
        return self.engine.generate_correlation_matrix(size, method, **kwargs)
