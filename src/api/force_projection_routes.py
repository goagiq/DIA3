"""
Force Projection API Routes
FastAPI routes for force projection simulation capabilities
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from ..core.force_projection_engine import ForceProjectionEngine, AdversaryType, DomainType

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/force-projection", tags=["Force Projection"])

# Global force projection engine instance
force_projection_engine: Optional[ForceProjectionEngine] = None


def set_force_projection_engine(engine: ForceProjectionEngine):
    """Set the global force projection engine instance"""
    global force_projection_engine
    force_projection_engine = engine


# Pydantic models for request/response
class ForceProjectionRequest(BaseModel):
    adversary_type: str = Field(..., description="Type of adversary to simulate")
    domain_type: str = Field(..., description="Domain type for analysis")
    time_horizon_months: int = Field(24, ge=1, le=60, description="Time horizon in months")
    num_iterations: int = Field(10000, ge=1000, le=50000, description="Number of Monte Carlo iterations")
    confidence_level: float = Field(0.95, ge=0.8, le=0.99, description="Confidence level")
    custom_parameters: Optional[Dict[str, Any]] = Field(None, description="Custom parameters")


class ForceProjectionResponse(BaseModel):
    success: bool
    simulation_id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    summary: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class VisualizationRequest(BaseModel):
    simulation_id: str = Field(..., description="ID of the simulation to visualize")
    save_path: Optional[str] = Field(None, description="Path to save visualization")


class HistoryRequest(BaseModel):
    limit: int = Field(50, ge=1, le=100, description="Number of recent simulations to return")


class ExportRequest(BaseModel):
    simulation_id: str = Field(..., description="ID of the simulation to export")
    format: str = Field("json", description="Export format")


class ComparisonRequest(BaseModel):
    simulation_ids: List[str] = Field(..., description="List of simulation IDs to compare")
    comparison_metrics: List[str] = Field(["effectiveness"], description="Metrics to compare")


@router.post("/simulate", response_model=ForceProjectionResponse)
async def simulate_force_projection(request: ForceProjectionRequest):
    """Simulate force projection capabilities"""
    try:
        if not force_projection_engine:
            raise HTTPException(status_code=500, detail="Force projection engine not initialized")
        
        # Validate adversary type
        valid_adversary_types = [e.value for e in AdversaryType]
        if request.adversary_type not in valid_adversary_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid adversary_type. Must be one of: {valid_adversary_types}"
            )
        
        # Validate domain type
        valid_domain_types = [e.value for e in DomainType]
        if request.domain_type not in valid_domain_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid domain_type. Must be one of: {valid_domain_types}"
            )
        
        # Run simulation
        result = await force_projection_engine.simulate_force_projection_capabilities(
            adversary_type=request.adversary_type,
            domain_type=request.domain_type,
            time_horizon_months=request.time_horizon_months,
            num_iterations=request.num_iterations,
            confidence_level=request.confidence_level,
            custom_parameters=request.custom_parameters
        )
        
        # Convert result to dict for JSON serialization
        result_dict = {
            "simulation_id": result.simulation_id,
            "adversary_type": result.adversary_type,
            "domain_type": result.domain_type,
            "capability_analysis": result.capability_analysis,
            "readiness_analysis": result.readiness_analysis,
            "environmental_analysis": result.environmental_analysis,
            "effectiveness_analysis": result.effectiveness_analysis,
            "threat_assessment": result.threat_assessment,
            "recommendations": result.recommendations,
            "metadata": result.metadata,
            "timestamp": result.timestamp.isoformat()
        }
        
        return ForceProjectionResponse(
            success=True,
            simulation_id=result.simulation_id,
            result=result_dict,
            summary={
                "threat_level": result.threat_assessment["threat_level"],
                "overall_effectiveness": result.effectiveness_analysis["overall_effectiveness"],
                "execution_time": result.metadata["execution_time_seconds"],
                "recommendations_count": len(result.recommendations)
            }
        )
        
    except Exception as e:
        logger.error(f"Error in force projection simulation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/visualize")
async def create_visualization(request: VisualizationRequest):
    """Create visualization for force projection simulation results"""
    try:
        if not force_projection_engine:
            raise HTTPException(status_code=500, detail="Force projection engine not initialized")
        
        # Find simulation in history
        history = force_projection_engine.get_simulation_history(limit=1000)
        target_simulation = None
        
        for simulation in history:
            if simulation.simulation_id == request.simulation_id:
                target_simulation = simulation
                break
        
        if not target_simulation:
            raise HTTPException(
                status_code=404, 
                detail=f"Simulation with ID {request.simulation_id} not found"
            )
        
        # Create visualization
        visualization_data = force_projection_engine.create_visualization(
            target_simulation, request.save_path
        )
        
        return {
            "success": True,
            "simulation_id": request.simulation_id,
            "visualization": visualization_data,
            "save_path": request.save_path
        }
        
    except Exception as e:
        logger.error(f"Error creating force projection visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/history")
async def get_simulation_history(request: HistoryRequest):
    """Get simulation history and performance metrics"""
    try:
        if not force_projection_engine:
            raise HTTPException(status_code=500, detail="Force projection engine not initialized")
        
        # Get simulation history
        history = force_projection_engine.get_simulation_history(limit=request.limit)
        
        # Get performance metrics
        performance_metrics = force_projection_engine.get_performance_metrics()
        
        # Convert history to serializable format
        history_data = []
        for simulation in history:
            history_data.append({
                "simulation_id": simulation.simulation_id,
                "adversary_type": simulation.adversary_type,
                "domain_type": simulation.domain_type,
                "threat_level": simulation.threat_assessment["threat_level"],
                "overall_effectiveness": simulation.effectiveness_analysis["overall_effectiveness"],
                "execution_time": simulation.metadata["execution_time_seconds"],
                "timestamp": simulation.timestamp.isoformat()
            })
        
        return {
            "success": True,
            "history": history_data,
            "performance_metrics": performance_metrics,
            "total_simulations": len(history_data)
        }
        
    except Exception as e:
        logger.error(f"Error getting force projection history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export")
async def export_simulation(request: ExportRequest):
    """Export simulation results in various formats"""
    try:
        if not force_projection_engine:
            raise HTTPException(status_code=500, detail="Force projection engine not initialized")
        
        # Validate export format
        valid_formats = ["json", "csv", "excel"]
        if request.format not in valid_formats:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid format. Must be one of: {valid_formats}"
            )
        
        # Find simulation in history
        history = force_projection_engine.get_simulation_history(limit=1000)
        target_simulation = None
        
        for simulation in history:
            if simulation.simulation_id == request.simulation_id:
                target_simulation = simulation
                break
        
        if not target_simulation:
            raise HTTPException(
                status_code=404,
                detail=f"Simulation with ID {request.simulation_id} not found"
            )
        
        # Export simulation
        export_data = force_projection_engine.export_simulation_result(
            target_simulation, request.format
        )
        
        return {
            "success": True,
            "simulation_id": request.simulation_id,
            "format": request.format,
            "export_data": export_data
        }
        
    except Exception as e:
        logger.error(f"Error exporting force projection simulation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare")
async def compare_simulations(request: ComparisonRequest):
    """Compare multiple force projection simulations"""
    try:
        if not force_projection_engine:
            raise HTTPException(status_code=500, detail="Force projection engine not initialized")
        
        if not request.simulation_ids:
            raise HTTPException(
                status_code=400,
                detail="No simulation IDs provided for comparison"
            )
        
        # Validate comparison metrics
        valid_metrics = ["effectiveness", "capabilities", "readiness", "environmental"]
        for metric in request.comparison_metrics:
            if metric not in valid_metrics:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid comparison metric: {metric}. Must be one of: {valid_metrics}"
                )
        
        # Find simulations in history
        history = force_projection_engine.get_simulation_history(limit=1000)
        target_simulations = []
        
        for simulation in history:
            if simulation.simulation_id in request.simulation_ids:
                target_simulations.append(simulation)
        
        if len(target_simulations) != len(request.simulation_ids):
            found_ids = [s.simulation_id for s in target_simulations]
            missing_ids = [sid for sid in request.simulation_ids if sid not in found_ids]
            raise HTTPException(
                status_code=404,
                detail=f"Some simulations not found: {missing_ids}"
            )
        
        # Perform comparison
        comparison_results = {}
        
        for metric in request.comparison_metrics:
            if metric == "effectiveness":
                comparison_results[metric] = {
                    sim.simulation_id: {
                        "overall_effectiveness": sim.effectiveness_analysis["overall_effectiveness"],
                        "capability_contribution": sim.effectiveness_analysis["effectiveness_breakdown"]["capability_contribution"],
                        "readiness_contribution": sim.effectiveness_analysis["effectiveness_breakdown"]["readiness_contribution"],
                        "environmental_contribution": sim.effectiveness_analysis["effectiveness_breakdown"]["environmental_contribution"]
                    }
                    for sim in target_simulations
                }
            elif metric == "capabilities":
                comparison_results[metric] = {
                    sim.simulation_id: sim.effectiveness_analysis["capability_scores"]
                    for sim in target_simulations
                }
            elif metric == "readiness":
                comparison_results[metric] = {
                    sim.simulation_id: {
                        factor: data["mean"] 
                        for factor, data in sim.readiness_analysis.items()
                    }
                    for sim in target_simulations
                }
            elif metric == "environmental":
                comparison_results[metric] = {
                    sim.simulation_id: {
                        factor: data["mean"]
                        for factor, data in sim.environmental_analysis.items()
                    }
                    for sim in target_simulations
                }
        
        # Calculate summary statistics
        summary = {
            "total_simulations": len(target_simulations),
            "adversary_types": list(set(sim.adversary_type for sim in target_simulations)),
            "domain_types": list(set(sim.domain_type for sim in target_simulations)),
            "threat_levels": list(set(sim.threat_assessment["threat_level"] for sim in target_simulations)),
            "avg_effectiveness": sum(sim.effectiveness_analysis["overall_effectiveness"] for sim in target_simulations) / len(target_simulations)
        }
        
        return {
            "success": True,
            "comparison_results": comparison_results,
            "summary": summary,
            "simulation_ids": request.simulation_ids
        }
        
    except Exception as e:
        logger.error(f"Error comparing force projection simulations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/adversary-types")
async def get_adversary_types():
    """Get available adversary types"""
    return {
        "adversary_types": [e.value for e in AdversaryType],
        "descriptions": {
            "peer_adversary": "Peer-level military adversary",
            "near_peer": "Near-peer military adversary", 
            "regional_power": "Regional power adversary",
            "emerging_threat": "Emerging threat actor",
            "non_state_actor": "Non-state actor",
            "business_competitor": "Business competitor",
            "cyber_adversary": "Cyber threat actor"
        }
    }


@router.get("/domain-types")
async def get_domain_types():
    """Get available domain types"""
    return {
        "domain_types": [e.value for e in DomainType],
        "descriptions": {
            "defense": "Military and defense analysis",
            "intelligence": "Intelligence community analysis",
            "business": "Business and competitive analysis",
            "cyber": "Cybersecurity analysis",
            "financial": "Financial market analysis",
            "geopolitical": "Geopolitical analysis"
        }
    }


@router.get("/capabilities/{domain_type}")
async def get_domain_capabilities(domain_type: str):
    """Get capability parameters for a specific domain"""
    try:
        if not force_projection_engine:
            raise HTTPException(status_code=500, detail="Force projection engine not initialized")
        
        # Validate domain type
        valid_domain_types = [e.value for e in DomainType]
        if domain_type not in valid_domain_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid domain_type. Must be one of: {valid_domain_types}"
            )
        
        # Get capability parameters for the domain
        domain_capabilities = force_projection_engine.capability_parameters.get(domain_type, {})
        
        # Convert to serializable format
        capabilities_data = {}
        for area, capabilities in domain_capabilities.items():
            capabilities_data[area] = {}
            for capability, params in capabilities.items():
                capabilities_data[area][capability] = {
                    "mu": params.mu,
                    "sigma": params.sigma,
                    "units": params.units,
                    "domain": params.domain,
                    "description": params.description
                }
        
        return {
            "domain_type": domain_type,
            "capabilities": capabilities_data
        }
        
    except Exception as e:
        logger.error(f"Error getting domain capabilities: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engine_initialized": force_projection_engine is not None
    }
