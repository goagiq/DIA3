"""
API routes for Phase 1 ML/DL/RL Forecasting Components
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from loguru import logger
from datetime import datetime

# Global orchestrator reference
orchestrator = None

def set_orchestrator(orch):
    """Set the orchestrator reference for the routes."""
    global orchestrator
    orchestrator = orch

router = APIRouter(prefix="/ml-forecasting", tags=["ML/DL/RL Forecasting"])

class ForecastingRequest(BaseModel):
    """Request model for forecasting operations."""
    data: Dict[str, Any]
    model_type: str = "lstm"  # lstm, transformer, tft, informer, autoformer, fedformer
    domain: str = "general"  # general, defense, intelligence, business, cybersecurity
    parameters: Optional[Dict[str, Any]] = None

class RLRequest(BaseModel):
    """Request model for reinforcement learning operations."""
    state: Dict[str, Any]
    action_space: List[str]
    reward_function: Optional[Dict[str, Any]] = None
    agent_type: str = "q_learning"  # q_learning, deep_q_network, policy_gradient, actor_critic, multi_agent

class CausalInferenceRequest(BaseModel):
    """Request model for causal inference operations."""
    data: Dict[str, Any]
    variables: List[str]
    analysis_type: str = "granger"  # granger, counterfactual, causal_discovery

class DomainSpecificRequest(BaseModel):
    """Request model for domain-specific analysis."""
    data: Dict[str, Any]
    domain: str  # defense, intelligence
    analysis_type: str
    parameters: Optional[Dict[str, Any]] = None

# Phase 2: Interactive War Capability Analysis Models
class WarCapabilityRequest(BaseModel):
    """Request model for war capability analysis."""
    country_data: Dict[str, Any]
    capability_weights: Optional[Dict[str, float]] = None

class LeverAdjustmentRequest(BaseModel):
    """Request model for interactive lever adjustments."""
    lever_name: str
    value: float

class LeverRecalculationRequest(BaseModel):
    """Request model for lever recalculation."""
    lever_changes: Dict[str, float]

class SensitivityAnalysisRequest(BaseModel):
    """Request model for sensitivity analysis."""
    lever_name: str

class ScenarioGenerationRequest(BaseModel):
    """Request model for scenario generation."""
    base_scenario: Dict[str, Any]
    scenario_type: str = "balanced"  # aggressive, economic, balanced

# Phase 4: Multi-Domain Integration Models
class DoDIntegrationRequest(BaseModel):
    """Request model for DoD domain integration."""
    intelligence_data: Dict[str, Any]
    readiness_data: Optional[Dict[str, Any]] = None
    analysis_results: Optional[Dict[str, Any]] = None

class IntelligenceCommunityRequest(BaseModel):
    """Request model for intelligence community integration."""
    intel_data: Dict[str, Any]
    available_data: Optional[Dict[str, Any]] = None
    source_data: Optional[Dict[str, Any]] = None

class FederatedLearningRequest(BaseModel):
    """Request model for federated learning operations."""
    participating_agencies: List[str]
    local_updates: Optional[Dict[str, Any]] = None
    training_data: Optional[Dict[str, Any]] = None
    round_config: Optional[Dict[str, Any]] = None

@router.get("/health")
async def health_check():
    """Health check for ML forecasting service."""
    return {
        "status": "healthy",
        "service": "ml_forecasting",
        "components": [
            "reinforcement_learning_engine",
            "enhanced_time_series_models", 
            "enhanced_causal_inference_engine",
            "dod_threat_assessment_models",
            "intelligence_analysis_models",
            "war_capability_engine",
            "interactive_capability_levers",
            "dynamic_prediction_engine"
        ],
        "available_models": [
            "lstm", "transformer", "tft", "informer", "autoformer", "fedformer"
        ],
        "available_agents": [
            "q_learning", "deep_q_network", "policy_gradient", "actor_critic", "multi_agent"
        ],
        "available_domains": [
            "general", "defense", "intelligence", "business", "cybersecurity"
        ],
        "phase4_components": [
            "dod_domain_integration",
            "intelligence_community_integration", 
            "federated_learning_engine"
        ]
    }

@router.post("/time-series/forecast")
async def time_series_forecast(request: ForecastingRequest):
    """Generate time series forecasts using enhanced models."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import the enhanced time series models
        from src.core.advanced_ml.enhanced_time_series_models import EnhancedTimeSeriesModels
        
        models = EnhancedTimeSeriesModels()
        
        # Create time series data
        from src.core.advanced_ml.enhanced_time_series_models import TimeSeriesData
        import numpy as np
        
        # Convert to numpy arrays
        values = np.array(request.data.get("values", []))
        timestamps = np.array(request.data.get("timestamps", []))
        
        ts_data = TimeSeriesData(
            timestamps=timestamps,
            values=values,
            metadata=request.data.get("metadata", {}),
            data_type="numerical"
        )
        
        # Generate forecast
        forecast_horizon = request.parameters.get("forecast_horizon", 10) if request.parameters else 10
        
        # Map simple model names to actual model names
        model_mapping = {
            "lstm": "lstm_advanced",
            "transformer": "transformer_forecast",
            "tft": "temporal_fusion",
            "informer": "informer",
            "autoformer": "autoformer",
            "fedformer": "fedformer"
        }
        
        actual_model_name = model_mapping.get(request.model_type, request.model_type)
        
        forecast_result = await models.forecast_with_model(
            model_name=actual_model_name,
            data=ts_data,
            horizon=forecast_horizon
        )
        
        return {
            "success": True,
            "model_type": request.model_type,
            "domain": request.domain,
            "forecast": forecast_result.predictions.tolist(),
            "confidence_intervals": [
                forecast_result.confidence_intervals[0].tolist(),
                forecast_result.confidence_intervals[1].tolist()
            ],
            "confidence_score": forecast_result.confidence_score,
            "metadata": forecast_result.metadata
        }
        
    except Exception as e:
        logger.error(f"Error in time series forecasting: {e}")
        raise HTTPException(status_code=500, detail=f"Forecasting error: {str(e)}")

@router.post("/reinforcement-learning/optimize")
async def rl_optimize(request: RLRequest):
    """Optimize decision-making using reinforcement learning."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import the RL engine
        from src.core.reinforcement_learning import ReinforcementLearningEngine
        from src.core.reinforcement_learning.rl_engine import State, Action
        
        rl_engine = ReinforcementLearningEngine()
        
        # Create state
        import numpy as np
        features = np.array(request.state.get("features", []))
        
        state = State(
            features=features,
            metadata=request.state.get("metadata", {}),
            timestamp=request.state.get("timestamp", 0.0)
        )
        
        # Optimize decision
        def reward_function(state, action, next_state=None):
            return request.reward_function.get("value", 0.0) if request.reward_function else 0.0
            
        action = await rl_engine.optimize_decision_making(
            state=state,
            action_space=request.action_space,
            reward_function=reward_function
        )
        
        return {
            "success": True,
            "agent_type": request.agent_type,
            "selected_action": action.action_id,
            "action_parameters": action.parameters,
            "confidence": action.confidence,
            "state": request.state
        }
        
    except Exception as e:
        logger.error(f"Error in RL optimization: {e}")
        raise HTTPException(status_code=500, detail=f"RL optimization error: {str(e)}")

@router.post("/causal-inference/analyze")
async def causal_inference_analyze(request: CausalInferenceRequest):
    """Perform causal inference analysis."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import the causal inference engine
        from src.core.advanced_analytics.enhanced_causal_inference import EnhancedCausalInferenceEngine
        
        engine = EnhancedCausalInferenceEngine()
        
        if request.analysis_type == "granger":
            # Convert data to pandas DataFrame
            import pandas as pd
            df = pd.DataFrame(request.data)
            
            result = await engine.granger_causality_test(
                time_series_data=df
            )
        elif request.analysis_type == "counterfactual":
            result = await engine.counterfactual_analysis(
                data=request.data,
                variables=request.variables
            )
        else:
            result = await engine.causal_discovery(
                data=request.data,
                variables=request.variables
            )
        
        return {
            "success": True,
            "analysis_type": request.analysis_type,
            "variables": request.variables,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error in causal inference analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Causal inference error: {str(e)}")

@router.post("/domain-specific/defense/analyze")
async def defense_domain_analyze(request: DomainSpecificRequest):
    """Perform defense domain-specific analysis."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import DoD threat assessment models
        from src.core.domain_specific.dod_threat_models import DoDThreatAssessmentModels
        
        models = DoDThreatAssessmentModels()
        
        if request.analysis_type == "military_capabilities":
            result = await models.assess_military_capabilities(request.data)
        elif request.analysis_type == "conflict_probability":
            result = await models.predict_conflict_probability(request.data)
        elif request.analysis_type == "weapons_proliferation":
            result = await models.analyze_weapons_proliferation(request.data)
        elif request.analysis_type == "threat_assessment":
            # For threat assessment, use military capabilities as the default
            result = await models.assess_military_capabilities(request.data)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown analysis type: {request.analysis_type}")
        
        return {
            "success": True,
            "domain": "defense",
            "analysis_type": request.analysis_type,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error in defense domain analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Defense domain analysis error: {str(e)}")

@router.post("/domain-specific/intelligence/analyze")
async def intelligence_domain_analyze(request: DomainSpecificRequest):
    """Perform intelligence domain-specific analysis."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import intelligence analysis models
        from src.core.domain_specific.intelligence_analysis_models import IntelligenceAnalysisModels
        
        models = IntelligenceAnalysisModels()
        
        if request.analysis_type == "signals_intelligence":
            result = await models.analyze_signal_intelligence(request.data)
        elif request.analysis_type == "human_intelligence":
            result = await models.assess_human_intelligence(request.data)
        elif request.analysis_type == "terrorist_activity":
            result = await models.predict_terrorist_activities(request.data)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown analysis type: {request.analysis_type}")
        
        return {
            "success": True,
            "domain": "intelligence",
            "analysis_type": request.analysis_type,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error in intelligence domain analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Intelligence domain analysis error: {str(e)}")

# Phase 2: Interactive War Capability Analysis Endpoints

@router.post("/war-capability/analyze")
async def war_capability_analysis(request: WarCapabilityRequest):
    """Analyze war capability for a country."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import war capability engine
        from src.core.war_capability.war_capability_engine import WarCapabilityEngine
        
        engine = WarCapabilityEngine()
        result = await engine.calculate_war_capability_score(
            request.country_data, 
            request.capability_weights
        )
        
        return {
            "success": True,
            "analysis_type": "war_capability",
            "result": {
                "overall_score": result.overall_score,
                "domain_scores": result.domain_scores,
                "confidence_level": result.confidence_level,
                "recommendations": result.recommendations,
                "risk_factors": result.risk_factors,
                "timestamp": result.timestamp.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error in war capability analysis: {e}")
        raise HTTPException(status_code=500, detail=f"War capability analysis error: {str(e)}")

@router.post("/interactive-levers/adjust")
async def adjust_interactive_lever(request: LeverAdjustmentRequest):
    """Adjust an interactive capability lever."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import interactive levers
        from src.core.war_capability.interactive_levers import InteractiveCapabilityLevers
        
        levers = InteractiveCapabilityLevers()
        result = await levers.adjust_lever(request.lever_name, request.value)
        
        return {
            "success": True,
            "operation": "lever_adjustment",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error adjusting lever: {e}")
        raise HTTPException(status_code=500, detail=f"Lever adjustment error: {str(e)}")

@router.post("/interactive-levers/recalculate")
async def recalculate_predictions(request: LeverRecalculationRequest):
    """Recalculate predictions based on lever changes."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import interactive levers
        from src.core.war_capability.interactive_levers import InteractiveCapabilityLevers
        
        levers = InteractiveCapabilityLevers()
        result = await levers.recalculate_predictions(request.lever_changes)
        
        return {
            "success": True,
            "operation": "prediction_recalculation",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error recalculating predictions: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction recalculation error: {str(e)}")

@router.post("/interactive-levers/sensitivity-analysis")
async def get_sensitivity_analysis(request: SensitivityAnalysisRequest):
    """Get sensitivity analysis for a specific lever."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import interactive levers
        from src.core.war_capability.interactive_levers import InteractiveCapabilityLevers
        
        levers = InteractiveCapabilityLevers()
        result = await levers.get_sensitivity_analysis(request.lever_name)
        
        return {
            "success": True,
            "operation": "sensitivity_analysis",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error getting sensitivity analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Sensitivity analysis error: {str(e)}")

@router.get("/interactive-levers/status")
async def get_levers_status():
    """Get status of all interactive levers."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import interactive levers
        from src.core.war_capability.interactive_levers import InteractiveCapabilityLevers
        
        levers = InteractiveCapabilityLevers()
        result = await levers.get_all_levers_status()
        
        return {
            "success": True,
            "operation": "levers_status",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error getting levers status: {e}")
        raise HTTPException(status_code=500, detail=f"Levers status error: {str(e)}")

@router.post("/interactive-levers/reset")
async def reset_levers_to_default():
    """Reset all levers to default values."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import interactive levers
        from src.core.war_capability.interactive_levers import InteractiveCapabilityLevers
        
        levers = InteractiveCapabilityLevers()
        result = await levers.reset_levers_to_default()
        
        return {
            "success": True,
            "operation": "levers_reset",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error resetting levers: {e}")
        raise HTTPException(status_code=500, detail=f"Levers reset error: {str(e)}")

@router.post("/dynamic-predictions/update")
async def update_predictions(request: LeverRecalculationRequest):
    """Update predictions based on new data and lever changes."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import dynamic prediction engine
        from src.core.predictive_analytics.dynamic_prediction_engine import DynamicPredictionEngine
        
        engine = DynamicPredictionEngine()
        result = await engine.update_predictions({}, request.lever_changes)
        
        return {
            "success": True,
            "operation": "prediction_update",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error updating predictions: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction update error: {str(e)}")

@router.post("/dynamic-predictions/scenarios")
async def generate_alternative_scenarios(request: ScenarioGenerationRequest):
    """Generate alternative scenarios based on different lever settings."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import dynamic prediction engine
        from src.core.predictive_analytics.dynamic_prediction_engine import DynamicPredictionEngine
        
        engine = DynamicPredictionEngine()
        result = await engine.generate_alternative_scenarios(request.base_scenario)
        
        return {
            "success": True,
            "operation": "scenario_generation",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error generating scenarios: {e}")
        raise HTTPException(status_code=500, detail=f"Scenario generation error: {str(e)}")

@router.get("/dynamic-predictions/current")
async def get_current_predictions():
    """Get current predictions with confidence intervals."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import dynamic prediction engine
        from src.core.predictive_analytics.dynamic_prediction_engine import DynamicPredictionEngine
        
        engine = DynamicPredictionEngine()
        result = await engine.get_current_predictions()
        
        return {
            "success": True,
            "operation": "current_predictions",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error getting current predictions: {e}")
        raise HTTPException(status_code=500, detail=f"Current predictions error: {str(e)}")

@router.get("/models")
async def get_available_models():
    """Get available models and their capabilities."""
    return {
        "time_series_models": [
            {"name": "lstm", "description": "Long Short-Term Memory networks"},
            {"name": "transformer", "description": "Transformer-based models"},
            {"name": "tft", "description": "Temporal Fusion Transformer"},
            {"name": "informer", "description": "Informer model for long sequence forecasting"},
            {"name": "autoformer", "description": "Autoformer model"},
            {"name": "fedformer", "description": "FEDformer model"}
        ],
        "rl_agents": [
            {"name": "q_learning", "description": "Q-Learning agent"},
            {"name": "deep_q_network", "description": "Deep Q-Network agent"},
            {"name": "policy_gradient", "description": "Policy Gradient agent"},
            {"name": "actor_critic", "description": "Actor-Critic agent"},
            {"name": "multi_agent", "description": "Multi-Agent System"}
        ],
        "causal_inference_methods": [
            {"name": "granger", "description": "Granger causality testing"},
            {"name": "counterfactual", "description": "Counterfactual analysis"},
            {"name": "causal_discovery", "description": "Causal discovery algorithms"}
        ],
        "domains": [
            {"name": "defense", "description": "Defense domain analysis"},
            {"name": "intelligence", "description": "Intelligence domain analysis"},
            {"name": "business", "description": "Business domain analysis"},
            {"name": "cybersecurity", "description": "Cybersecurity domain analysis"}
        ]
    }

# Phase 3: Advanced Forecasting & Prediction Endpoints

class EnsembleForecastRequest(BaseModel):
    """Request model for ensemble forecasting."""
    training_data: Dict[str, Any]
    validation_data: Optional[Dict[str, Any]] = None
    horizon: int = 10
    optimize_weights: bool = True

class ScenarioPredictionRequest(BaseModel):
    """Request model for scenario prediction."""
    capability_analysis: Dict[str, Any]
    scenario_types: Optional[List[str]] = None
    include_outcomes: bool = True
    include_escalation_paths: bool = True

class IntelligenceStreamRequest(BaseModel):
    """Request model for intelligence stream operations."""
    stream_type: str  # 'sigint', 'humint', 'osint', 'geospatial', 'cyber'
    connection_params: Dict[str, Any]
    data: Optional[Dict[str, Any]] = None

@router.post("/phase3/ensemble-forecast")
async def ensemble_forecast(request: EnsembleForecastRequest):
    """Generate ensemble forecasts using Phase 3 ensemble system."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import ensemble forecasting system
        from src.core.advanced_ml.ensemble_forecasting_system import EnsembleForecastingSystem
        from src.core.advanced_ml.enhanced_time_series_models import TimeSeriesData
        
        ensemble_system = EnsembleForecastingSystem()
        
        # Create time series data
        import numpy as np
        from datetime import datetime
        
        values = np.array(request.training_data.get("values", []))
        timestamp_strings = request.training_data.get("timestamps", [])
        
        # Convert ISO format strings to datetime objects
        timestamps = []
        for ts_str in timestamp_strings:
            try:
                ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                timestamps.append(ts)
            except Exception as e:
                logger.warning(f"Failed to parse timestamp {ts_str}: {e}")
                # Use current time as fallback
                timestamps.append(datetime.now())
        
        timestamps = np.array(timestamps)
        
        training_ts_data = TimeSeriesData(
            timestamps=timestamps,
            values=values,
            metadata=request.training_data.get("metadata", {}),
            data_type="numerical"
        )
        
        # Train ensemble
        training_result = await ensemble_system.train_ensemble(training_ts_data)
        
        # Generate predictions
        forecast_result = await ensemble_system.predict_ensemble(training_ts_data, request.horizon)
        
        # Optimize weights if requested
        optimized_weights = None
        if request.optimize_weights and request.validation_data:
            validation_values = np.array(request.validation_data.get("values", []))
            validation_timestamp_strings = request.validation_data.get("timestamps", [])
            
            # Convert ISO format strings to datetime objects
            validation_timestamps = []
            for ts_str in validation_timestamp_strings:
                try:
                    ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                    validation_timestamps.append(ts)
                except Exception as e:
                    logger.warning(f"Failed to parse validation timestamp {ts_str}: {e}")
                    # Use current time as fallback
                    validation_timestamps.append(datetime.now())
            
            validation_timestamps = np.array(validation_timestamps)
            
            validation_ts_data = TimeSeriesData(
                timestamps=validation_timestamps,
                values=validation_values,
                metadata=request.validation_data.get("metadata", {}),
                data_type="numerical"
            )
            
            optimized_weights = await ensemble_system.optimize_weights(validation_ts_data)
        
        return {
            "success": True,
            "operation": "ensemble_forecast",
            "training_result": training_result,
            "forecast": {
                "predictions": forecast_result.predictions.tolist(),
                "confidence_intervals": [
                    forecast_result.confidence_intervals[0].tolist(),
                    forecast_result.confidence_intervals[1].tolist()
                ],
                "confidence_score": forecast_result.confidence_score,
                "model_weights": forecast_result.model_weights,
                "metadata": forecast_result.metadata
            },
            "optimized_weights": optimized_weights
        }
        
    except Exception as e:
        logger.error(f"Error in ensemble forecasting: {e}")
        raise HTTPException(status_code=500, detail=f"Ensemble forecasting error: {str(e)}")

@router.post("/phase3/scenario-prediction")
async def scenario_prediction(request: ScenarioPredictionRequest):
    """Generate war scenarios and predict conflict outcomes."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import enhanced scenario predictor
        from src.core.scenario_analysis.enhanced_scenario_predictor import EnhancedScenarioPredictor
        
        scenario_predictor = EnhancedScenarioPredictor()
        
        # Generate war scenarios
        scenarios = await scenario_predictor.generate_war_scenarios(request.capability_analysis)
        
        results = {
            "scenarios": []
        }
        
        # Process each scenario
        for scenario in scenarios:
            scenario_result = {
                "scenario_id": scenario.scenario_id,
                "scenario_type": scenario.scenario_type,
                "probability": scenario.probability,
                "confidence_score": scenario.confidence_score,
                "capability_analysis": scenario.capability_analysis,
                "escalation_paths": scenario.escalation_paths
            }
            
            # Predict conflict outcomes if requested
            if request.include_outcomes:
                outcomes = await scenario_predictor.predict_conflict_outcomes({
                    'scenario_id': scenario.scenario_id,
                    'capability_analysis': scenario.capability_analysis,
                    'scenario_type': scenario.scenario_type
                })
                scenario_result["outcomes"] = [
                    {
                        "outcome_type": outcome.outcome_type,
                        "probability": outcome.probability,
                        "confidence_score": outcome.confidence_score,
                        "timeline_estimate": outcome.timeline_estimate,
                        "casualty_estimates": outcome.casualty_estimates,
                        "economic_impact": outcome.economic_impact,
                        "geopolitical_implications": outcome.geopolitical_implications
                    }
                    for outcome in outcomes
                ]
            
            results["scenarios"].append(scenario_result)
        
        # Analyze escalation paths if requested
        if request.include_escalation_paths:
            escalation_paths = await scenario_predictor.analyze_escalation_paths(request.capability_analysis)
            results["escalation_paths"] = [
                {
                    "path_id": path.path_id,
                    "trigger_events": path.trigger_events,
                    "escalation_stages": path.escalation_stages,
                    "probability": path.probability,
                    "timeline": path.timeline,
                    "mitigation_options": path.mitigation_options,
                    "confidence_score": path.confidence_score
                }
                for path in escalation_paths
            ]
        
        return {
            "success": True,
            "operation": "scenario_prediction",
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error in scenario prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Scenario prediction error: {str(e)}")

@router.post("/phase3/intelligence-stream/connect")
async def connect_intelligence_stream(request: IntelligenceStreamRequest):
    """Connect to intelligence data stream."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import intelligence data adapter
        from src.core.streaming.intelligence_data_adapter import IntelligenceDataAdapter
        
        intelligence_adapter = IntelligenceDataAdapter()
        
        # Connect to stream
        success = await intelligence_adapter.connect_to_stream(
            request.stream_type, request.connection_params
        )
        
        if success:
            # Get stream status
            stream_status = await intelligence_adapter.get_stream_status()
            
            return {
                "success": True,
                "operation": "connect_intelligence_stream",
                "stream_type": request.stream_type,
                "connected": True,
                "stream_status": stream_status
            }
        else:
            raise HTTPException(status_code=500, detail=f"Failed to connect to {request.stream_type} stream")
        
    except Exception as e:
        logger.error(f"Error connecting to intelligence stream: {e}")
        raise HTTPException(status_code=500, detail=f"Intelligence stream connection error: {str(e)}")

@router.post("/phase3/intelligence-stream/process")
async def process_intelligence_data(request: IntelligenceStreamRequest):
    """Process intelligence stream data."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        if not request.data:
            raise HTTPException(status_code=400, detail="No data provided for processing")
        
        # Import intelligence data adapter
        from src.core.streaming.intelligence_data_adapter import IntelligenceDataAdapter
        
        intelligence_adapter = IntelligenceDataAdapter()
        
        # Process stream data
        processed_data = await intelligence_adapter.process_stream_data(request.data)
        
        return {
            "success": True,
            "operation": "process_intelligence_data",
            "stream_type": request.stream_type,
            "processed_data": {
                "stream_id": processed_data.stream_id,
                "data_type": processed_data.data_type,
                "processed_data": processed_data.processed_data,
                "confidence_score": processed_data.confidence_score,
                "source_reliability": processed_data.source_reliability,
                "timestamp": processed_data.timestamp.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error processing intelligence data: {e}")
        raise HTTPException(status_code=500, detail=f"Intelligence data processing error: {str(e)}")

@router.get("/phase3/intelligence-stream/status")
async def get_intelligence_stream_status():
    """Get intelligence stream status."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import intelligence data adapter
        from src.core.streaming.intelligence_data_adapter import IntelligenceDataAdapter
        
        intelligence_adapter = IntelligenceDataAdapter()
        status = await intelligence_adapter.get_intelligence_adapter_status()
        
        return {
            "success": True,
            "operation": "get_intelligence_stream_status",
            "status": status
        }
        
    except Exception as e:
        logger.error(f"Error getting intelligence stream status: {e}")
        raise HTTPException(status_code=500, detail=f"Intelligence stream status error: {str(e)}")

@router.get("/phase3/ensemble-status")
async def get_ensemble_status():
    """Get ensemble forecasting system status."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import ensemble forecasting system
        from src.core.advanced_ml.ensemble_forecasting_system import EnsembleForecastingSystem
        
        ensemble_system = EnsembleForecastingSystem()
        status = await ensemble_system.get_ensemble_status()
        
        return {
            "success": True,
            "operation": "get_ensemble_status",
            "status": status
        }
        
    except Exception as e:
        logger.error(f"Error getting ensemble status: {e}")
        raise HTTPException(status_code=500, detail=f"Ensemble status error: {str(e)}")

@router.get("/phase3/scenario-predictor-status")
async def get_scenario_predictor_status():
    """Get scenario predictor status."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import enhanced scenario predictor
        from src.core.scenario_analysis.enhanced_scenario_predictor import EnhancedScenarioPredictor
        
        scenario_predictor = EnhancedScenarioPredictor()
        status = await scenario_predictor.get_scenario_predictor_status()
        
        return {
            "success": True,
            "operation": "get_scenario_predictor_status",
            "status": status
        }
        
    except Exception as e:
        logger.error(f"Error getting scenario predictor status: {e}")
        raise HTTPException(status_code=500, detail=f"Scenario predictor status error: {str(e)}")

@router.get("/summary")
async def get_service_summary():
    """Get ML forecasting service summary."""
    return {
        "service": "ML/DL/RL Forecasting",
        "version": "1.0.0",
        "description": "Phase 1-3 ML/DL/RL Forecasting Components for comprehensive strategic analysis",
        "components": {
            "reinforcement_learning_engine": "Decision optimization and adaptive forecasting",
            "enhanced_time_series_models": "Advanced time series forecasting models",
            "enhanced_causal_inference_engine": "Causal inference for intelligence analysis",
            "dod_threat_assessment_models": "DoD-specific threat assessment and prediction",
            "intelligence_analysis_models": "Intelligence community-specific analysis",
            "war_capability_engine": "Interactive war capability assessment",
            "interactive_capability_levers": "Dynamic capability adjustment system",
            "dynamic_prediction_engine": "Real-time prediction updates",
            "ensemble_forecasting_system": "Phase 3: Multi-model ensemble forecasting",
            "enhanced_scenario_predictor": "Phase 3: War scenario and conflict outcome prediction",
            "intelligence_data_adapter": "Phase 3: Real-time intelligence data streaming"
        },
        "endpoints": [
            "/ml-forecasting/health",
            "/ml-forecasting/time-series/forecast",
            "/ml-forecasting/reinforcement-learning/optimize",
            "/ml-forecasting/causal-inference/analyze",
            "/ml-forecasting/domain-specific/defense/analyze",
            "/ml-forecasting/domain-specific/intelligence/analyze",
            "/ml-forecasting/war-capability/analyze",
            "/ml-forecasting/interactive-levers/adjust",
            "/ml-forecasting/interactive-levers/recalculate",
            "/ml-forecasting/interactive-levers/sensitivity-analysis",
            "/ml-forecasting/interactive-levers/status",
            "/ml-forecasting/interactive-levers/reset",
            "/ml-forecasting/dynamic-predictions/update",
            "/ml-forecasting/dynamic-predictions/scenarios",
            "/ml-forecasting/dynamic-predictions/current",
            "/ml-forecasting/phase3/ensemble-forecast",
            "/ml-forecasting/phase3/scenario-prediction",
            "/ml-forecasting/phase3/intelligence-stream/connect",
            "/ml-forecasting/phase3/intelligence-stream/process",
            "/ml-forecasting/phase3/intelligence-stream/status",
            "/ml-forecasting/phase3/ensemble-status",
            "/ml-forecasting/phase3/scenario-predictor-status",
            "/ml-forecasting/phase4/dod-integration",
            "/ml-forecasting/phase4/intelligence-community-integration",
            "/ml-forecasting/phase4/federated-learning",
            "/ml-forecasting/phase4/dod-status",
            "/ml-forecasting/phase4/intelligence-community-status",
            "/ml-forecasting/phase4/federated-learning-status",
            "/ml-forecasting/models",
            "/ml-forecasting/summary"
        ]
    }

# Phase 4: Multi-Domain Integration Endpoints

@router.post("/phase4/dod-integration")
async def dod_domain_integration(request: DoDIntegrationRequest):
    """DoD domain integration for military intelligence analysis."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import DoD domain integration
        from src.core.multi_domain.dod_domain_integration import DoDDomainIntegration
        
        dod_integration = DoDDomainIntegration()
        
        # Perform military intelligence integration
        if request.intelligence_data:
            intelligence_result = await dod_integration.integrate_military_intelligence(request.intelligence_data)
        else:
            intelligence_result = {"status": "no_data", "message": "No intelligence data provided"}
        
        # Perform operational readiness analysis
        if request.readiness_data:
            readiness_result = await dod_integration.analyze_operational_readiness(request.readiness_data)
        else:
            readiness_result = {"status": "no_data", "message": "No readiness data provided"}
        
        # Perform strategic implications assessment
        if request.analysis_results:
            strategic_result = await dod_integration.assess_strategic_implications(request.analysis_results)
        else:
            strategic_result = {"status": "no_data", "message": "No analysis results provided"}
        
        return {
            "success": True,
            "operation": "dod_domain_integration",
            "intelligence_integration": intelligence_result,
            "operational_readiness": readiness_result,
            "strategic_implications": strategic_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in DoD domain integration: {e}")
        raise HTTPException(status_code=500, detail=f"DoD integration error: {str(e)}")

@router.post("/phase4/intelligence-community-integration")
async def intelligence_community_integration(request: IntelligenceCommunityRequest):
    """Intelligence community integration for all-source intelligence analysis."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import intelligence community integration
        from src.core.multi_domain.intelligence_community_integration import IntelligenceCommunityIntegration
        
        intel_integration = IntelligenceCommunityIntegration()
        
        # Perform all-source intelligence integration
        if request.intel_data:
            intel_result = await intel_integration.integrate_all_source_intelligence(request.intel_data)
        else:
            intel_result = {"status": "no_data", "message": "No intelligence data provided"}
        
        # Perform intelligence gaps analysis
        if request.available_data:
            gaps_result = await intel_integration.analyze_intelligence_gaps(request.available_data)
        else:
            gaps_result = {"status": "no_data", "message": "No available data provided"}
        
        # Perform source reliability assessment
        if request.source_data:
            reliability_result = await intel_integration.assess_source_reliability(request.source_data)
        else:
            reliability_result = {"status": "no_data", "message": "No source data provided"}
        
        return {
            "success": True,
            "operation": "intelligence_community_integration",
            "all_source_intelligence": intel_result,
            "intelligence_gaps": gaps_result,
            "source_reliability": reliability_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in intelligence community integration: {e}")
        raise HTTPException(status_code=500, detail=f"Intelligence community integration error: {str(e)}")

@router.post("/phase4/federated-learning")
async def federated_learning_operations(request: FederatedLearningRequest):
    """Federated learning operations for distributed intelligence."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import federated learning engine
        from src.core.federated_learning.federated_learning_engine import FederatedLearningEngine
        
        fed_learning_engine = FederatedLearningEngine()
        
        # Coordinate federated training
        if request.participating_agencies:
            training_result = await fed_learning_engine.coordinate_federated_training(request.participating_agencies)
        else:
            training_result = {"status": "no_agencies", "message": "No participating agencies provided"}
        
        # Aggregate model updates
        if request.local_updates:
            aggregation_result = await fed_learning_engine.aggregate_model_updates(request.local_updates)
        else:
            aggregation_result = {"status": "no_updates", "message": "No local updates provided"}
        
        # Ensure data privacy
        if request.training_data:
            privacy_result = await fed_learning_engine.ensure_data_privacy(request.training_data)
        else:
            privacy_result = {"status": "no_data", "message": "No training data provided"}
        
        # Manage learning rounds
        if request.round_config:
            rounds_result = await fed_learning_engine.manage_federated_learning_rounds(request.round_config)
        else:
            rounds_result = {"status": "no_config", "message": "No round configuration provided"}
        
        return {
            "success": True,
            "operation": "federated_learning_operations",
            "federated_training": training_result,
            "aggregation": aggregation_result,
            "data_privacy": privacy_result,
            "learning_rounds": rounds_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in federated learning operations: {e}")
        raise HTTPException(status_code=500, detail=f"Federated learning error: {str(e)}")

@router.get("/phase4/dod-status")
async def get_dod_integration_status():
    """Get DoD domain integration status."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import DoD domain integration
        from src.core.multi_domain.dod_domain_integration import DoDDomainIntegration
        
        dod_integration = DoDDomainIntegration()
        status = await dod_integration.get_integration_status()
        
        return {
            "success": True,
            "operation": "get_dod_integration_status",
            "status": status
        }
        
    except Exception as e:
        logger.error(f"Error getting DoD integration status: {e}")
        raise HTTPException(status_code=500, detail=f"DoD status error: {str(e)}")

@router.get("/phase4/intelligence-community-status")
async def get_intelligence_community_status():
    """Get intelligence community integration status."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import intelligence community integration
        from src.core.multi_domain.intelligence_community_integration import IntelligenceCommunityIntegration
        
        intel_integration = IntelligenceCommunityIntegration()
        status = await intel_integration.get_integration_status()
        
        return {
            "success": True,
            "operation": "get_intelligence_community_status",
            "status": status
        }
        
    except Exception as e:
        logger.error(f"Error getting intelligence community status: {e}")
        raise HTTPException(status_code=500, detail=f"Intelligence community status error: {str(e)}")

@router.get("/phase4/federated-learning-status")
async def get_federated_learning_status():
    """Get federated learning engine status."""
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Import federated learning engine
        from src.core.federated_learning.federated_learning_engine import FederatedLearningEngine
        
        fed_learning_engine = FederatedLearningEngine()
        status = await fed_learning_engine.get_engine_status()
        
        return {
            "success": True,
            "operation": "get_federated_learning_status",
            "status": status
        }
        
    except Exception as e:
        logger.error(f"Error getting federated learning status: {e}")
        raise HTTPException(status_code=500, detail=f"Federated learning status error: {str(e)}")
