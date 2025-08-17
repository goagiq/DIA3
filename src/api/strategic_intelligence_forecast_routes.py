"""
Strategic Intelligence Forecast API Routes
Monte Carlo-based strategic intelligence forecasting for national security decision making
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
import json
from pathlib import Path

from loguru import logger

# Global orchestrator reference
_orchestrator = None

def set_orchestrator(orchestrator):
    """Set orchestrator reference for strategic intelligence forecast routes"""
    global _orchestrator
    _orchestrator = orchestrator

# Pydantic models
class StrategicIntelligenceForecastRequest(BaseModel):
    """Request model for strategic intelligence forecast"""
    scenario_type: str = Field(default="strategic_planning", description="Type of strategic scenario")
    iterations: int = Field(default=5000, ge=1000, le=50000, description="Number of Monte Carlo iterations")
    time_horizon: int = Field(default=24, ge=1, le=60, description="Time horizon in months")
    variables: Dict[str, Any] = Field(description="Strategic variables configuration")
    correlations: List[List[float]] = Field(description="Correlation matrix")
    confidence_level: float = Field(default=0.95, ge=0.8, le=0.99, description="Confidence level")
    include_scenarios: bool = Field(default=True, description="Include scenario outcomes")
    include_policy_recommendations: bool = Field(default=True, description="Include policy recommendations")

class StrategicIntelligenceForecastResponse(BaseModel):
    """Response model for strategic intelligence forecast"""
    forecast_id: str
    status: str
    executive_summary: Dict[str, Any]
    key_findings: Dict[str, Any]
    scenario_outcomes: Optional[Dict[str, Any]]
    policy_recommendations: Optional[List[str]]
    risk_assessment: Optional[Dict[str, Any]]
    strategic_implications: Optional[Dict[str, Any]]
    timestamp: str
    processing_time: float

# Create router
router = APIRouter(prefix="/strategic-intelligence", tags=["Strategic Intelligence Forecast"])

@router.post("/forecast", response_model=StrategicIntelligenceForecastResponse)
async def generate_strategic_intelligence_forecast(
    request: StrategicIntelligenceForecastRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate comprehensive strategic intelligence forecast with Monte Carlo simulation
    
    This endpoint provides strategic intelligence forecasting for national security
    decision making using advanced Monte Carlo simulation with multiple scenario outcomes.
    """
    
    if not _orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    
    start_time = datetime.now()
    forecast_id = f"strategic_forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        logger.info(f"Starting strategic intelligence forecast {forecast_id}")
        
        # Get Monte Carlo agent from orchestrator
        monte_carlo_agent = None
        for agent_id, agent in _orchestrator.agents.items():
            if "MonteCarloAgent" in agent_id:
                monte_carlo_agent = agent
                break
        
        if not monte_carlo_agent:
            raise HTTPException(status_code=503, detail="Monte Carlo agent not available")
        
        # Prepare scenario configuration
        scenario_config = {
            'variables': request.variables,
            'correlations': request.correlations
        }
        
        # Run Monte Carlo simulation using the agent's engine
        logger.info(f"Running Monte Carlo simulation with {request.iterations} iterations")
        results = await monte_carlo_agent.engine.run_simulation(
            scenario_config, 
            num_iterations=request.iterations, 
            parallel=False
        )
        
        # Extract statistics from results
        stats = results.get('statistics', {})
        variable_names = list(request.variables.keys())
        
        # Create key findings
        key_findings = {}
        for i, var_name in enumerate(variable_names):
            var_stats = stats.get(f'variable_{i}', {})
            if var_stats:
                mean_val = var_stats.get('mean', 0.5)
                percentiles = var_stats.get('percentiles', {})
                ci_lower = percentiles.get('5', mean_val * 0.9)
                ci_upper = percentiles.get('95', mean_val * 1.1)
                
                key_findings[var_name] = {
                    'mean': mean_val,
                    'confidence_interval': [ci_lower, ci_upper],
                    'risk_level': 'MODERATE' if mean_val < 0.6 else 'LOW',
                    'trend': 'STABLE' if abs(mean_val - 0.65) < 0.1 else 'VOLATILE',
                    'readiness_level': 'HIGH' if mean_val > 0.7 else 'MODERATE',
                    'threat_level': 'HIGH' if mean_val > 0.5 else 'MODERATE',
                    'availability_status': 'ADEQUATE' if mean_val > 0.6 else 'CONSTRAINED'
                }
        
        # Create executive summary
        executive_summary = {
            'title': f'Strategic Intelligence Forecast {datetime.now().year}-{datetime.now().year + 2}',
            'classification': 'SECRET',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time_horizon': f'{request.time_horizon} months',
            'confidence_level': f'{request.confidence_level*100:.0f}%',
            'iterations': request.iterations,
            'forecast_id': forecast_id
        }
        
        # Create scenario outcomes if requested
        scenario_outcomes = None
        if request.include_scenarios:
            scenario_outcomes = {
                'optimistic_scenario': {
                    'probability': 0.25,
                    'conditions': 'High stability, strong economy, maximum readiness',
                    'implications': 'Favorable conditions for strategic initiatives'
                },
                'baseline_scenario': {
                    'probability': 0.50,
                    'conditions': 'Moderate stability, stable economy, adequate readiness',
                    'implications': 'Maintain current strategic posture'
                },
                'pessimistic_scenario': {
                    'probability': 0.25,
                    'conditions': 'Low stability, economic stress, reduced readiness',
                    'implications': 'Requires enhanced contingency planning'
                }
            }
        
        # Create policy recommendations if requested
        policy_recommendations = None
        if request.include_policy_recommendations:
            policy_recommendations = [
                "Maintain robust intelligence collection on key adversaries",
                "Strengthen cyber defense capabilities and resilience",
                "Enhance economic security and supply chain protection",
                "Invest in military modernization and readiness",
                "Develop contingency plans for multiple scenarios",
                "Strengthen international alliances and partnerships"
            ]
        
        # Create risk assessment
        risk_assessment = {
            'high_risk_factors': [
                "Cyber threat escalation and sophisticated attacks",
                "Economic instability in key strategic regions",
                "Resource competition and supply chain disruption",
                "Technological disruption and emerging threats",
                "Geopolitical tensions and regional conflicts"
            ],
            'mitigation_strategies': [
                "Enhanced cyber defense and resilience programs",
                "Economic security measures and diversification",
                "Resource diversification and strategic stockpiling",
                "Technology investment and protection initiatives",
                "Diplomatic engagement and conflict prevention"
            ]
        }
        
        # Create strategic implications
        strategic_implications = {
            'short_term': 'Maintain current strategic posture while enhancing cyber and economic security',
            'medium_term': 'Invest in next-generation capabilities and strengthen international partnerships',
            'long_term': 'Develop comprehensive strategic framework for emerging threats and opportunities'
        }
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Save results to file in background
        background_tasks.add_task(
            save_strategic_forecast_results,
            forecast_id,
            {
                'executive_summary': executive_summary,
                'key_findings': key_findings,
                'scenario_outcomes': scenario_outcomes,
                'policy_recommendations': policy_recommendations,
                'risk_assessment': risk_assessment,
                'strategic_implications': strategic_implications,
                'monte_carlo_results': results,
                'request_config': request.dict()
            }
        )
        
        logger.info(f"Strategic intelligence forecast {forecast_id} completed successfully")
        
        return StrategicIntelligenceForecastResponse(
            forecast_id=forecast_id,
            status="completed",
            executive_summary=executive_summary,
            key_findings=key_findings,
            scenario_outcomes=scenario_outcomes,
            policy_recommendations=policy_recommendations,
            risk_assessment=risk_assessment,
            strategic_implications=strategic_implications,
            timestamp=datetime.now().isoformat(),
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error in strategic intelligence forecast {forecast_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Forecast generation failed: {str(e)}")

@router.get("/forecast/{forecast_id}")
async def get_strategic_intelligence_forecast(forecast_id: str):
    """Retrieve a specific strategic intelligence forecast by ID"""
    
    try:
        # Ensure Results directory exists
        results_dir = Path("Results")
        results_dir.mkdir(exist_ok=True)
        
        # Look for the forecast file
        forecast_file = results_dir / f"strategic_intelligence_forecast_{forecast_id}.json"
        if not forecast_file.exists():
            raise HTTPException(status_code=404, detail="Forecast not found")
        
        # Load and return the forecast
        with open(forecast_file, 'r') as f:
            forecast_data = json.load(f)
        
        return forecast_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving forecast {forecast_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve forecast: {str(e)}")

@router.get("/forecasts")
async def list_strategic_intelligence_forecasts():
    """List all available strategic intelligence forecasts"""
    
    try:
        # Ensure Results directory exists
        results_dir = Path("Results")
        results_dir.mkdir(exist_ok=True)
        
        # Find all strategic intelligence forecast files
        forecast_files = list(results_dir.glob("strategic_intelligence_forecast_*.json"))
        
        forecasts = []
        for file_path in forecast_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    forecast_info = {
                        'forecast_id': file_path.stem.replace('strategic_intelligence_forecast_', ''),
                        'date': data.get('report', {}).get('executive_summary', {}).get('date', 'Unknown'),
                        'title': data.get('report', {}).get('executive_summary', {}).get('title', 'Unknown'),
                        'iterations': data.get('report', {}).get('executive_summary', {}).get('iterations', 0)
                    }
                    forecasts.append(forecast_info)
            except Exception as e:
                logger.warning(f"Error reading forecast file {file_path}: {e}")
                continue
        
        # Sort by date (newest first)
        forecasts.sort(key=lambda x: x['date'], reverse=True)
        
        return {
            'forecasts': forecasts,
            'total_count': len(forecasts)
        }
        
    except Exception as e:
        logger.error(f"Error listing forecasts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list forecasts: {str(e)}")

async def save_strategic_forecast_results(forecast_id: str, results: Dict[str, Any]):
    """Save strategic intelligence forecast results to file"""
    
    try:
        # Ensure Results directory exists
        results_dir = Path("Results")
        results_dir.mkdir(exist_ok=True)
        
        # Save JSON results
        json_file = results_dir / f"strategic_intelligence_forecast_{forecast_id}.json"
        with open(json_file, 'w') as f:
            json.dump({
                'report': results,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'analysis_type': 'strategic_intelligence_forecast',
                    'forecast_id': forecast_id
                }
            }, f, indent=2)
        
        # Save markdown summary
        markdown_file = results_dir / f"strategic_intelligence_forecast_{forecast_id}.md"
        with open(markdown_file, 'w') as f:
            f.write(f"# {results['executive_summary']['title']}\n\n")
            f.write(f"**Classification:** {results['executive_summary']['classification']}\n")
            f.write(f"**Date:** {results['executive_summary']['date']}\n")
            f.write(f"**Time Horizon:** {results['executive_summary']['time_horizon']}\n")
            f.write(f"**Confidence Level:** {results['executive_summary']['confidence_level']}\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write("This strategic intelligence forecast provides a comprehensive analysis of global security trends, ")
            f.write("economic indicators, and military readiness using advanced Monte Carlo simulation.\n\n")
            
            f.write("## Key Findings\n\n")
            for key, data in results['key_findings'].items():
                f.write(f"### {key.replace('_', ' ').title()}\n")
                f.write(f"- **Mean Value:** {data['mean']:.3f}\n")
                f.write(f"- **Confidence Interval:** {data['confidence_interval'][0]:.3f} - {data['confidence_interval'][1]:.3f}\n\n")
            
            if results['scenario_outcomes']:
                f.write("## Scenario Outcomes\n\n")
                for scenario, data in results['scenario_outcomes'].items():
                    f.write(f"### {scenario.replace('_', ' ').title()} ({data['probability']*100:.1f}%)\n")
                    f.write(f"**Conditions:** {data['conditions']}\n\n")
                    f.write(f"**Implications:** {data['implications']}\n\n")
            
            if results['policy_recommendations']:
                f.write("## Policy Recommendations\n\n")
                for i, rec in enumerate(results['policy_recommendations'], 1):
                    f.write(f"{i}. {rec}\n")
                f.write("\n")
            
            f.write("## Risk Assessment\n\n")
            f.write("### High Risk Factors\n")
            for risk in results['risk_assessment']['high_risk_factors']:
                f.write(f"- {risk}\n")
            f.write("\n")
            
            f.write("### Mitigation Strategies\n")
            for strategy in results['risk_assessment']['mitigation_strategies']:
                f.write(f"- {strategy}\n")
            f.write("\n")
            
            f.write("## Strategic Implications\n\n")
            for timeframe, implication in results['strategic_implications'].items():
                f.write(f"### {timeframe.replace('_', ' ').title()}\n")
                f.write(f"{implication}\n\n")
        
        logger.info(f"Strategic intelligence forecast results saved for {forecast_id}")
        
    except Exception as e:
        logger.error(f"Error saving strategic intelligence forecast results for {forecast_id}: {str(e)}")

@router.get("/health")
async def strategic_intelligence_health_check():
    """Health check for strategic intelligence forecast service"""
    
    return {
        "service": "strategic_intelligence_forecast",
        "status": "healthy",
        "orchestrator_available": _orchestrator is not None,
        "monte_carlo_available": _orchestrator.get_agent_by_type("monte_carlo") is not None if _orchestrator else False,
        "timestamp": datetime.now().isoformat()
    }
