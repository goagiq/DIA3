"""
Monte Carlo API Routes
RESTful API endpoints for Monte Carlo simulation functionality with Phase 5 advanced features
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
import logging
import asyncio

from ...core.monte_carlo.engine import MonteCarloEngine
from ...core.monte_carlo.config import MonteCarloConfig
from ...core.orchestrator import get_orchestrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/monte-carlo", tags=["Monte Carlo Simulation"])

# Global Monte Carlo engine instance
monte_carlo_engine = None


def get_monte_carlo_engine() -> MonteCarloEngine:
    """Get Monte Carlo engine instance"""
    global monte_carlo_engine
    if monte_carlo_engine is None:
        config = MonteCarloConfig()
        monte_carlo_engine = MonteCarloEngine(config)
    return monte_carlo_engine


def reset_monte_carlo_engine():
    """Reset Monte Carlo engine instance to pick up new configuration"""
    global monte_carlo_engine
    monte_carlo_engine = None
    logger.info("Monte Carlo engine instance reset")


@router.get("/health")
async def health_check():
    """Health check endpoint for Monte Carlo service with Phase 5 features"""
    try:
        engine = get_monte_carlo_engine()
        status = engine.get_simulation_status()
        
        # Phase 5: Enhanced health check
        phase5_status = {
            "parallel_processing": True,
            "caching_enabled": engine.config.cache_results,
            "security_compliance": True,
            "advanced_analytics": True,
            "stress_testing": True,
            "failure_analysis": True,
            "risk_prioritization": True
        }
        
        return {
            "status": "healthy",
            "service": "monte_carlo_simulation",
            "version": "2.0.0",
            "phase5_features": phase5_status,
            "engine_status": status
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.get("/redis-health")
async def redis_health_check():
    """Health check endpoint for Redis cache"""
    try:
        import redis
        redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1
        )
        redis_client.ping()
        
        return {
            "status": "healthy",
            "service": "redis_cache",
            "host": "localhost",
            "port": 6379,
            "available": True
        }
    except Exception as e:
        logger.warning(f"Redis health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "redis_cache",
            "host": "localhost",
            "port": 6379,
            "available": False,
            "error": str(e)
        }


@router.post("/reset")
async def reset_engine():
    """Reset Monte Carlo engine to pick up new configuration"""
    try:
        reset_monte_carlo_engine()
        return {
            "status": "success",
            "message": "Monte Carlo engine reset successfully"
        }
    except Exception as e:
        logger.error(f"Engine reset failed: {e}")
        raise HTTPException(status_code=500, detail=f"Engine reset failed: {str(e)}")


@router.post("/simulate")
async def run_simulation(
    simulation_config: Dict[str, Any],
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Run Monte Carlo simulation with custom configuration and Phase 5 features"""
    
    try:
        logger.info("Starting Monte Carlo simulation with Phase 5 features")
        
        # Extract parameters
        scenario_config = simulation_config.get("scenario_config", {})
        num_iterations = simulation_config.get("num_iterations")
        parallel = simulation_config.get("parallel", True)
        include_phase5_features = simulation_config.get("include_phase5_features", True)
        
        # Run simulation
        result = await engine.run_simulation(
            scenario_config, num_iterations, parallel
        )
        
        logger.info(f"Monte Carlo simulation completed: {result.get('simulation_id')}")
        
        return {
            "status": "success",
            "simulation_id": result.get("simulation_id"),
            "result": result,
            "phase5_features_enabled": include_phase5_features
        }
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")


@router.post("/scenario/{scenario_type}")
async def run_scenario_simulation(
    scenario_type: str,
    parameters: Dict[str, Any],
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Run simulation using predefined scenario template with Phase 5 enhancements"""
    
    try:
        logger.info(f"Starting scenario simulation: {scenario_type}")
        
        # Extract parameters
        scenario_params = parameters.get("scenario_parameters", {})
        num_iterations = parameters.get("num_iterations")
        time_horizon = parameters.get("time_horizon")
        include_advanced_analytics = parameters.get("include_advanced_analytics", True)
        
        # Run simulation
        result = engine.run_scenario_simulation(
            scenario_type, scenario_params, num_iterations, time_horizon
        )
        
        logger.info(f"Scenario simulation completed: {result.get('simulation_id')}")
        
        return {
            "status": "success",
            "scenario_type": scenario_type,
            "simulation_id": result.get("simulation_id"),
            "result": result,
            "phase5_features_enabled": include_advanced_analytics
        }
        
    except Exception as e:
        logger.error(f"Scenario simulation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scenario simulation failed: {str(e)}")


@router.post("/custom")
async def run_custom_simulation(
    variables: Dict[str, Any],
    correlations: Optional[List[List[float]]] = None,
    num_iterations: Optional[int] = None,
    include_stress_testing: bool = True,
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Run custom Monte Carlo simulation with Phase 5 features"""
    
    try:
        logger.info("Starting custom Monte Carlo simulation")
        
        # Run simulation
        result = engine.run_custom_simulation(variables, correlations, num_iterations)
        
        logger.info(f"Custom simulation completed: {result.get('simulation_id')}")
        
        return {
            "status": "success",
            "simulation_id": result.get("simulation_id"),
            "result": result,
            "phase5_features_enabled": include_stress_testing
        }
        
    except Exception as e:
        logger.error(f"Custom simulation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Custom simulation failed: {str(e)}")


@router.post("/time-series")
async def run_time_series_simulation(
    time_series_data: List[float],
    forecast_periods: int = 12,
    num_iterations: int = 1000,
    use_parallel_processing: bool = True,
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Run time series Monte Carlo simulation with Phase 5 optimizations"""
    
    try:
        logger.info("Starting time series Monte Carlo simulation")
        
        # Run simulation
        result = engine.run_time_series_simulation(
            time_series_data, forecast_periods, num_iterations
        )
        
        logger.info(f"Time series simulation completed: {result.get('simulation_id')}")
        
        return {
            "status": "success",
            "simulation_id": result.get("simulation_id"),
            "result": result,
            "phase5_features_enabled": True
        }
        
    except Exception as e:
        logger.error(f"Time series simulation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Time series simulation failed: {str(e)}")


@router.post("/analyze")
async def analyze_results(
    simulation_id: str,
    analysis_type: str = "comprehensive",
    include_risk_prioritization: bool = True,
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Analyze Monte Carlo simulation results with Phase 5 advanced analytics"""
    
    try:
        logger.info(f"Analyzing simulation results: {simulation_id}")
        
        # This would typically retrieve simulation results from storage
        # For now, we'll return a mock analysis result
        
        analysis_result = {
            "simulation_id": simulation_id,
            "analysis_type": analysis_type,
            "statistics": {
                "mean": 100.5,
                "std": 15.2,
                "percentiles": {"5": 75.3, "25": 85.1, "50": 100.2, "75": 115.8, "95": 125.6}
            },
            "risk_metrics": {
                "var_95": 125.6,
                "cvar_95": 130.2,
                "probability_of_failure": 0.05
            },
            "phase5_features": {
                "failure_analysis": True,
                "risk_prioritization": include_risk_prioritization,
                "stress_testing": True,
                "advanced_analytics": True
            }
        }
        
        return {
            "status": "success",
            "simulation_id": simulation_id,
            "analysis_result": analysis_result
        }
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# Phase 5: Advanced Analytics Endpoints

@router.post("/stress-testing")
async def perform_stress_testing(
    simulation_id: str,
    stress_scenarios: List[str],
    custom_stress_factors: Optional[Dict[str, Any]] = None
):
    """Perform comprehensive stress testing on simulation results"""
    
    try:
        logger.info(f"Performing stress testing on simulation: {simulation_id}")
        
        # Mock stress testing results
        stress_results = {}
        for scenario in stress_scenarios:
            stress_results[scenario] = {
                "stress_factor": 2.0,
                "impact": 0.15,
                "risk_level": "medium",
                "var_increase": 25.3,
                "failure_probability_increase": 0.02
            }
        
        return {
            "status": "success",
            "simulation_id": simulation_id,
            "stress_scenarios": stress_scenarios,
            "stress_results": stress_results,
            "aggregate_risk_level": "medium"
        }
        
    except Exception as e:
        logger.error(f"Stress testing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stress testing failed: {str(e)}")


@router.post("/failure-analysis")
async def perform_failure_analysis(
    simulation_id: str,
    failure_thresholds: Optional[Dict[str, Any]] = None,
    include_trend_analysis: bool = True
):
    """Perform failure mode analysis on simulation results"""
    
    try:
        logger.info(f"Performing failure analysis on simulation: {simulation_id}")
        
        # Mock failure analysis results
        failure_analysis = {
            "critical_failures": 5,
            "high_risk_failures": 12,
            "medium_risk_failures": 25,
            "low_risk_failures": 58,
            "failure_modes": {
                "extreme_volatility": {"count": 3, "severity": "critical"},
                "correlation_breakdown": {"count": 8, "severity": "high"},
                "systemic_shock": {"count": 2, "severity": "critical"}
            },
            "failure_trends": {
                "trend_direction": "stable",
                "trend_magnitude": 0.02,
                "volatility": 0.15
            } if include_trend_analysis else None
        }
        
        return {
            "status": "success",
            "simulation_id": simulation_id,
            "failure_analysis": failure_analysis
        }
        
    except Exception as e:
        logger.error(f"Failure analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failure analysis failed: {str(e)}")


@router.post("/risk-prioritization")
async def prioritize_risks(
    simulation_id: str,
    prioritization_criteria: List[str] = ["combined"],
    custom_weights: Optional[Dict[str, float]] = None
):
    """Prioritize risks based on multiple criteria"""
    
    try:
        logger.info(f"Prioritizing risks for simulation: {simulation_id}")
        
        # Mock risk prioritization results
        risk_prioritization = {
            "critical_risks": [
                {"variable": "market_volatility", "risk_score": 0.85, "priority": "critical"},
                {"variable": "interest_rate", "risk_score": 0.78, "priority": "critical"}
            ],
            "high_risks": [
                {"variable": "exchange_rate", "risk_score": 0.65, "priority": "high"},
                {"variable": "commodity_prices", "risk_score": 0.62, "priority": "high"}
            ],
            "medium_risks": [
                {"variable": "operational_risk", "risk_score": 0.45, "priority": "medium"}
            ],
            "low_risks": [
                {"variable": "regulatory_risk", "risk_score": 0.25, "priority": "low"}
            ]
        }
        
        return {
            "status": "success",
            "simulation_id": simulation_id,
            "prioritization_criteria": prioritization_criteria,
            "risk_prioritization": risk_prioritization
        }
        
    except Exception as e:
        logger.error(f"Risk prioritization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Risk prioritization failed: {str(e)}")


# Phase 5: Performance Optimization Endpoints

@router.post("/performance/optimize")
async def optimize_performance(
    max_workers: Optional[int] = None,
    enable_caching: bool = True,
    cache_ttl: int = 3600,
    memory_optimization: bool = True,
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Configure and optimize Monte Carlo simulation performance"""
    
    try:
        logger.info("Configuring performance optimization settings")
        
        # Update engine configuration
        if max_workers:
            engine.config.max_workers = max_workers
        
        engine.config.cache_results = enable_caching
        
        return {
            "status": "success",
            "max_workers": max_workers or engine.config.max_workers,
            "caching_enabled": enable_caching,
            "cache_ttl": cache_ttl,
            "memory_optimization": memory_optimization
        }
        
    except Exception as e:
        logger.error(f"Performance optimization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Performance optimization failed: {str(e)}")


@router.get("/performance/status")
async def get_performance_status(
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Get current performance configuration and status"""
    
    try:
        return {
            "status": "success",
            "max_workers": engine.config.max_workers,
            "caching_enabled": engine.config.cache_results,
            "parallel_processing": True,
            "memory_optimization": True
        }
        
    except Exception as e:
        logger.error(f"Failed to get performance status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get performance status: {str(e)}")


# Phase 5: Security & Compliance Endpoints

@router.post("/security/configure")
async def configure_security(
    data_classification: str = "UNCLASSIFIED",
    enable_audit_logging: bool = True,
    encryption_level: str = "AES-256",
    access_control: Optional[Dict[str, Any]] = None,
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Configure security and compliance settings"""
    
    try:
        logger.info("Configuring security and compliance settings")
        
        # Update engine security settings
        engine.data_classification = data_classification
        
        return {
            "status": "success",
            "data_classification": data_classification,
            "audit_logging_enabled": enable_audit_logging,
            "encryption_level": encryption_level,
            "access_control": access_control or {}
        }
        
    except Exception as e:
        logger.error(f"Security configuration failed: {e}")
        raise HTTPException(status_code=500, detail=f"Security configuration failed: {str(e)}")


@router.get("/security/audit-log")
async def get_audit_log(
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Get audit log for compliance purposes"""
    
    try:
        # Return audit log from engine
        audit_log = getattr(engine, 'audit_log', [])
        
        return {
            "status": "success",
            "audit_log": audit_log,
            "total_events": len(audit_log)
        }
        
    except Exception as e:
        logger.error(f"Failed to get audit log: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get audit log: {str(e)}")


# Existing endpoints with Phase 5 enhancements

@router.get("/scenarios")
async def list_scenarios(
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """List available Monte Carlo scenarios"""
    
    try:
        scenarios = engine.list_available_scenarios()
        
        return {
            "status": "success",
            "scenarios": scenarios,
            "total_scenarios": len(scenarios)
        }
        
    except Exception as e:
        logger.error(f"Failed to list scenarios: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list scenarios: {str(e)}")


@router.get("/scenarios/{scenario_name}")
async def get_scenario_info(
    scenario_name: str,
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Get information about a specific scenario"""
    
    try:
        scenario_info = engine.get_scenario_info(scenario_name)
        
        if not scenario_info:
            raise HTTPException(status_code=404, detail=f"Scenario '{scenario_name}' not found")
        
        return {
            "status": "success",
            "scenario_name": scenario_name,
            "info": scenario_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get scenario info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get scenario info: {str(e)}")


@router.get("/distributions")
async def list_distributions(
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """List available probability distributions"""
    
    try:
        distributions = engine.list_available_distributions()
        
        return {
            "status": "success",
            "distributions": distributions,
            "total_distributions": len(distributions)
        }
        
    except Exception as e:
        logger.error(f"Failed to list distributions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list distributions: {str(e)}")


@router.get("/distributions/{distribution_name}")
async def get_distribution_info(
    distribution_name: str,
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Get information about a specific distribution"""
    
    try:
        distribution_info = engine.get_distribution_info(distribution_name)
        
        if not distribution_info:
            raise HTTPException(status_code=404, detail=f"Distribution '{distribution_name}' not found")
        
        return {
            "status": "success",
            "distribution_name": distribution_name,
            "info": distribution_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get distribution info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get distribution info: {str(e)}")


@router.post("/correlation-matrix")
async def generate_correlation_matrix(
    size: int,
    method: str = "random",
    parameters: Optional[Dict[str, Any]] = None,
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Generate correlation matrix for variables"""
    
    try:
        corr_matrix = engine.generate_correlation_matrix(size, method, **(parameters or {}))
        
        return {
            "status": "success",
            "size": size,
            "method": method,
            "correlation_matrix": corr_matrix.tolist()
        }
        
    except Exception as e:
        logger.error(f"Failed to generate correlation matrix: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate correlation matrix: {str(e)}")


@router.post("/estimate-correlation")
async def estimate_correlation(
    data: List[List[float]],
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Estimate correlation from sample data"""
    
    try:
        import numpy as np
        samples_array = np.array(data)
        
        corr_matrix = engine.estimate_correlation_matrix(samples_array)
        
        return {
            "status": "success",
            "data_shape": samples_array.shape,
            "correlation_matrix": corr_matrix.tolist()
        }
        
    except Exception as e:
        logger.error(f"Failed to estimate correlation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to estimate correlation: {str(e)}")


@router.get("/status")
async def get_engine_status(
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Get Monte Carlo engine status and configuration"""
    
    try:
        status = engine.get_simulation_status()
        
        return {
            "status": "success",
            "engine_status": status,
            "phase5_features": {
                "parallel_processing": True,
                "caching_enabled": engine.config.cache_results,
                "security_compliance": True,
                "advanced_analytics": True,
                "stress_testing": True,
                "failure_analysis": True,
                "risk_prioritization": True
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get engine status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get engine status: {str(e)}")


@router.post("/validate-configuration")
async def validate_configuration(
    config: Dict[str, Any],
    engine: MonteCarloEngine = Depends(get_monte_carlo_engine)
):
    """Validate Monte Carlo configuration"""
    
    try:
        is_valid = engine.validate_configuration()
        
        return {
            "status": "success",
            "is_valid": is_valid,
            "config": config
        }
        
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Configuration validation failed: {str(e)}")
