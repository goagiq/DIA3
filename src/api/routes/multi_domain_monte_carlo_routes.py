#!/usr/bin/env python3
"""
Multi-Domain Monte Carlo API Routes
FastAPI routes for multi-domain Monte Carlo simulation capabilities.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Union
import asyncio
import json
from datetime import datetime

# Import the multi-domain Monte Carlo engine
from src.core.multi_domain_monte_carlo_engine import (
    MultiDomainMonteCarloEngine,
    SimulationConfig,
    DomainType,
    SimulationType
)

# Create router
router = APIRouter(prefix="/api/v1/multi-domain-monte-carlo", tags=["Multi-Domain Monte Carlo"])

# Initialize engine
engine = MultiDomainMonteCarloEngine()


# Pydantic models for request/response
class SimulationRequest(BaseModel):
    """Request model for Monte Carlo simulations."""
    domain: str = Field(..., description="Domain type (defense, business, financial, cybersecurity)")
    scenario_name: str = Field(..., description="Name of the scenario to run")
    simulation_type: str = Field(..., description="Type of simulation")
    num_iterations: int = Field(default=10000, description="Number of Monte Carlo iterations")
    confidence_level: float = Field(default=0.95, description="Confidence level for intervals")
    custom_variables: Optional[Dict[str, Any]] = Field(default=None, description="Custom variables")
    correlations: Optional[List[List[float]]] = Field(default=None, description="Correlation matrix")


class DefenseSimulationRequest(BaseModel):
    """Request model for defense simulations."""
    scenario_name: str = Field(default="military_capability", description="Name of the scenario")
    num_iterations: int = Field(default=10000, description="Number of iterations")
    confidence_level: float = Field(default=0.95, description="Confidence level")
    custom_variables: Optional[Dict[str, Any]] = Field(default=None, description="Custom variables")


class BusinessSimulationRequest(BaseModel):
    """Request model for business simulations."""
    scenario_name: str = Field(default="market_analysis", description="Name of the scenario")
    num_iterations: int = Field(default=10000, description="Number of iterations")
    confidence_level: float = Field(default=0.95, description="Confidence level")
    custom_variables: Optional[Dict[str, Any]] = Field(default=None, description="Custom variables")


class FinancialSimulationRequest(BaseModel):
    """Request model for financial simulations."""
    scenario_name: str = Field(default="portfolio_risk", description="Name of the scenario")
    num_iterations: int = Field(default=10000, description="Number of iterations")
    confidence_level: float = Field(default=0.95, description="Confidence level")
    custom_variables: Optional[Dict[str, Any]] = Field(default=None, description="Custom variables")


class CybersecuritySimulationRequest(BaseModel):
    """Request model for cybersecurity simulations."""
    scenario_name: str = Field(default="threat_assessment", description="Name of the scenario")
    num_iterations: int = Field(default=10000, description="Number of iterations")
    confidence_level: float = Field(default=0.95, description="Confidence level")
    custom_variables: Optional[Dict[str, Any]] = Field(default=None, description="Custom variables")


class ReportRequest(BaseModel):
    """Request model for report generation."""
    simulation_id: str = Field(..., description="ID of the simulation")
    report_format: str = Field(default="json", description="Report format (json, text, html)")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "multi-domain-monte-carlo",
        "timestamp": datetime.now().isoformat(),
        "available_domains": [domain.value for domain in DomainType]
    }


@router.get("/scenarios")
async def get_available_scenarios():
    """Get available scenarios for all domains."""
    try:
        scenarios = engine.get_available_scenarios()
        return {
            "available_scenarios": scenarios,
            "total_domains": len(scenarios),
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting scenarios: {str(e)}")


@router.get("/performance")
async def get_performance_summary():
    """Get performance summary across all domains."""
    try:
        performance = engine.get_performance_summary()
        return {
            "performance_summary": performance,
            "total_domains": len(performance),
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting performance: {str(e)}")


@router.post("/simulate/defense")
async def run_defense_simulation(request: DefenseSimulationRequest):
    """Run Monte Carlo simulation for defense domain."""
    try:
        config = SimulationConfig(
            domain=DomainType.DEFENSE,
            simulation_type=SimulationType.CAPABILITY_ASSESSMENT,
            num_iterations=request.num_iterations,
            confidence_level=request.confidence_level
        )
        
        result = await engine.run_simulation(config, request.scenario_name, request.custom_variables)
        
        return {
            "simulation_id": result.simulation_id,
            "domain": "defense",
            "scenario": request.scenario_name,
            "iterations": result.config.num_iterations,
            "execution_time": result.execution_time,
            "statistics": result.statistics,
            "risk_metrics": result.risk_metrics,
            "confidence_intervals": result.confidence_intervals,
            "timestamp": result.timestamp.isoformat(),
            "status": "completed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Defense simulation failed: {str(e)}")


@router.post("/simulate/business")
async def run_business_simulation(request: BusinessSimulationRequest):
    """Run Monte Carlo simulation for business domain."""
    try:
        config = SimulationConfig(
            domain=DomainType.BUSINESS,
            simulation_type=SimulationType.RISK_ANALYSIS,
            num_iterations=request.num_iterations,
            confidence_level=request.confidence_level
        )
        
        result = await engine.run_simulation(config, request.scenario_name, request.custom_variables)
        
        return {
            "simulation_id": result.simulation_id,
            "domain": "business",
            "scenario": request.scenario_name,
            "iterations": result.config.num_iterations,
            "execution_time": result.execution_time,
            "statistics": result.statistics,
            "risk_metrics": result.risk_metrics,
            "confidence_intervals": result.confidence_intervals,
            "timestamp": result.timestamp.isoformat(),
            "status": "completed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Business simulation failed: {str(e)}")


@router.post("/simulate/financial")
async def run_financial_simulation(request: FinancialSimulationRequest):
    """Run Monte Carlo simulation for financial domain."""
    try:
        config = SimulationConfig(
            domain=DomainType.FINANCIAL,
            simulation_type=SimulationType.RISK_ANALYSIS,
            num_iterations=request.num_iterations,
            confidence_level=request.confidence_level
        )
        
        result = await engine.run_simulation(config, request.scenario_name, request.custom_variables)
        
        return {
            "simulation_id": result.simulation_id,
            "domain": "financial",
            "scenario": request.scenario_name,
            "iterations": result.config.num_iterations,
            "execution_time": result.execution_time,
            "statistics": result.statistics,
            "risk_metrics": result.risk_metrics,
            "confidence_intervals": result.confidence_intervals,
            "timestamp": result.timestamp.isoformat(),
            "status": "completed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Financial simulation failed: {str(e)}")


@router.post("/simulate/cybersecurity")
async def run_cybersecurity_simulation(request: CybersecuritySimulationRequest):
    """Run Monte Carlo simulation for cybersecurity domain."""
    try:
        config = SimulationConfig(
            domain=DomainType.CYBERSECURITY,
            simulation_type=SimulationType.THREAT_ASSESSMENT,
            num_iterations=request.num_iterations,
            confidence_level=request.confidence_level
        )
        
        result = await engine.run_simulation(config, request.scenario_name, request.custom_variables)
        
        return {
            "simulation_id": result.simulation_id,
            "domain": "cybersecurity",
            "scenario": request.scenario_name,
            "iterations": result.config.num_iterations,
            "execution_time": result.execution_time,
            "statistics": result.statistics,
            "risk_metrics": result.risk_metrics,
            "confidence_intervals": result.confidence_intervals,
            "timestamp": result.timestamp.isoformat(),
            "status": "completed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cybersecurity simulation failed: {str(e)}")


@router.post("/simulate/custom")
async def run_custom_simulation(request: SimulationRequest):
    """Run custom Monte Carlo simulation with user-defined parameters."""
    try:
        # Validate domain
        try:
            domain_enum = DomainType(request.domain)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid domain: {request.domain}. Supported domains: {[d.value for d in DomainType]}"
            )
        
        # Validate simulation type
        try:
            sim_type_enum = SimulationType(request.simulation_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid simulation type: {request.simulation_type}. Supported types: {[s.value for s in SimulationType]}"
            )
        
        config = SimulationConfig(
            domain=domain_enum,
            simulation_type=sim_type_enum,
            num_iterations=request.num_iterations,
            confidence_level=request.confidence_level
        )
        
        # Create custom scenario
        custom_scenario = {
            "variables": request.custom_variables or {},
            "correlations": request.correlations or []
        }
        
        result = await engine.run_simulation(config, request.scenario_name, custom_scenario)
        
        return {
            "simulation_id": result.simulation_id,
            "domain": request.domain,
            "scenario": request.scenario_name,
            "simulation_type": request.simulation_type,
            "iterations": result.config.num_iterations,
            "execution_time": result.execution_time,
            "statistics": result.statistics,
            "risk_metrics": result.risk_metrics,
            "confidence_intervals": result.confidence_intervals,
            "timestamp": result.timestamp.isoformat(),
            "status": "completed"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Custom simulation failed: {str(e)}")


@router.get("/simulation/{simulation_id}")
async def get_simulation_result(simulation_id: str):
    """Get cached simulation result."""
    try:
        result = await engine.load_cached_result(simulation_id)
        
        if result is None:
            raise HTTPException(status_code=404, detail=f"Simulation {simulation_id} not found")
        
        return {
            "simulation_id": result.simulation_id,
            "domain": result.config.domain.value,
            "simulation_type": result.config.simulation_type.value,
            "iterations": result.config.num_iterations,
            "execution_time": result.execution_time,
            "statistics": result.statistics,
            "risk_metrics": result.risk_metrics,
            "confidence_intervals": result.confidence_intervals,
            "timestamp": result.timestamp.isoformat(),
            "status": "loaded"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading simulation: {str(e)}")


@router.post("/report")
async def generate_simulation_report(request: ReportRequest):
    """Generate comprehensive report for a simulation."""
    try:
        # Load simulation result
        result = await engine.load_cached_result(request.simulation_id)
        
        if result is None:
            raise HTTPException(status_code=404, detail=f"Simulation {request.simulation_id} not found")
        
        # Generate report based on format
        if request.report_format == "json":
            report = _generate_json_report(result)
        elif request.report_format == "text":
            report = _generate_text_report(result)
        elif request.report_format == "html":
            report = _generate_html_report(result)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported report format: {request.report_format}. Supported formats: json, text, html"
            )
        
        return {
            "simulation_id": request.simulation_id,
            "report_format": request.report_format,
            "report": report,
            "timestamp": datetime.now().isoformat(),
            "status": "generated"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@router.post("/simulate/batch")
async def run_batch_simulations(requests: List[SimulationRequest], background_tasks: BackgroundTasks):
    """Run multiple simulations in batch."""
    try:
        batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        results = []
        
        for i, request in enumerate(requests):
            try:
                # Validate domain
                try:
                    domain_enum = DomainType(request.domain)
                except ValueError:
                    results.append({
                        "index": i,
                        "error": f"Invalid domain: {request.domain}",
                        "status": "failed"
                    })
                    continue
                
                # Validate simulation type
                try:
                    sim_type_enum = SimulationType(request.simulation_type)
                except ValueError:
                    results.append({
                        "index": i,
                        "error": f"Invalid simulation type: {request.simulation_type}",
                        "status": "failed"
                    })
                    continue
                
                config = SimulationConfig(
                    domain=domain_enum,
                    simulation_type=sim_type_enum,
                    num_iterations=request.num_iterations,
                    confidence_level=request.confidence_level
                )
                
                # Create custom scenario
                custom_scenario = {
                    "variables": request.custom_variables or {},
                    "correlations": request.correlations or []
                }
                
                result = await engine.run_simulation(config, request.scenario_name, custom_scenario)
                
                results.append({
                    "index": i,
                    "simulation_id": result.simulation_id,
                    "domain": request.domain,
                    "scenario": request.scenario_name,
                    "simulation_type": request.simulation_type,
                    "iterations": result.config.num_iterations,
                    "execution_time": result.execution_time,
                    "status": "completed"
                })
                
            except Exception as e:
                results.append({
                    "index": i,
                    "error": str(e),
                    "status": "failed"
                })
        
        return {
            "batch_id": batch_id,
            "total_requests": len(requests),
            "completed": len([r for r in results if r["status"] == "completed"]),
            "failed": len([r for r in results if r["status"] == "failed"]),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch simulation failed: {str(e)}")


# Helper functions for report generation
def _generate_json_report(result) -> Dict[str, Any]:
    """Generate JSON format report."""
    return {
        "simulation_summary": {
            "simulation_id": result.simulation_id,
            "domain": result.config.domain.value,
            "simulation_type": result.config.simulation_type.value,
            "iterations": result.config.num_iterations,
            "confidence_level": result.config.confidence_level,
            "execution_time": result.execution_time,
            "timestamp": result.timestamp.isoformat()
        },
        "statistics": result.statistics,
        "risk_metrics": result.risk_metrics,
        "confidence_intervals": result.confidence_intervals,
        "recommendations": _generate_recommendations(result)
    }


def _generate_text_report(result) -> str:
    """Generate text format report."""
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("MULTI-DOMAIN MONTE CARLO SIMULATION REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"Simulation ID: {result.simulation_id}")
    report_lines.append(f"Domain: {result.config.domain.value}")
    report_lines.append(f"Type: {result.config.simulation_type.value}")
    report_lines.append(f"Iterations: {result.config.num_iterations:,}")
    report_lines.append(f"Execution Time: {result.execution_time:.2f} seconds")
    report_lines.append("")
    
    # Statistics
    report_lines.append("STATISTICS")
    report_lines.append("-" * 40)
    for var_name, stats in result.statistics.items():
        report_lines.append(f"{var_name}:")
        report_lines.append(f"  Mean: {stats['mean']:.3f}")
        report_lines.append(f"  Std Dev: {stats['std']:.3f}")
        report_lines.append(f"  Range: {stats['min']:.3f} - {stats['max']:.3f}")
        report_lines.append("")
    
    # Risk Metrics
    report_lines.append("RISK METRICS")
    report_lines.append("-" * 40)
    for metric, value in result.risk_metrics.items():
        report_lines.append(f"{metric}: {value:.3f}")
    report_lines.append("")
    
    # Recommendations
    report_lines.append("RECOMMENDATIONS")
    report_lines.append("-" * 40)
    recommendations = _generate_recommendations(result)
    for i, rec in enumerate(recommendations, 1):
        report_lines.append(f"{i}. {rec}")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 80)
    
    return "\n".join(report_lines)


def _generate_html_report(result) -> str:
    """Generate HTML format report."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Monte Carlo Simulation Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
            .section {{ margin: 20px 0; }}
            .section h2 {{ color: #333; border-bottom: 2px solid #333; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .metric {{ background-color: #e8f4f8; padding: 10px; margin: 5px 0; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Multi-Domain Monte Carlo Simulation Report</h1>
            <p><strong>Simulation ID:</strong> {result.simulation_id}</p>
            <p><strong>Domain:</strong> {result.config.domain.value}</p>
            <p><strong>Type:</strong> {result.config.simulation_type.value}</p>
            <p><strong>Iterations:</strong> {result.config.num_iterations:,}</p>
            <p><strong>Execution Time:</strong> {result.execution_time:.2f} seconds</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="section">
            <h2>Statistics</h2>
            <table>
                <tr>
                    <th>Variable</th>
                    <th>Mean</th>
                    <th>Std Dev</th>
                    <th>Min</th>
                    <th>Max</th>
                </tr>
    """
    
    for var_name, stats in result.statistics.items():
        html += f"""
                <tr>
                    <td>{var_name}</td>
                    <td>{stats['mean']:.3f}</td>
                    <td>{stats['std']:.3f}</td>
                    <td>{stats['min']:.3f}</td>
                    <td>{stats['max']:.3f}</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>Risk Metrics</h2>
    """
    
    for metric, value in result.risk_metrics.items():
        html += f'<div class="metric"><strong>{metric}:</strong> {value:.3f}</div>'
    
    html += """
        </div>
        
        <div class="section">
            <h2>Recommendations</h2>
    """
    
    recommendations = _generate_recommendations(result)
    for i, rec in enumerate(recommendations, 1):
        html += f'<p><strong>{i}.</strong> {rec}</p>'
    
    html += """
        </div>
    </body>
    </html>
    """
    
    return html


def _generate_recommendations(result) -> List[str]:
    """Generate recommendations based on simulation results."""
    recommendations = []
    
    # Domain-specific recommendations
    if result.config.domain == DomainType.DEFENSE:
        if result.risk_metrics.get("var_95", 0) > 0.7:
            recommendations.append("HIGH THREAT LEVEL: Adversary demonstrates significant military capability requiring immediate attention")
        elif result.risk_metrics.get("var_95", 0) > 0.4:
            recommendations.append("MEDIUM THREAT LEVEL: Adversary has moderate military capability requiring monitoring")
        else:
            recommendations.append("LOW THREAT LEVEL: Adversary has limited military capability")
    
    elif result.config.domain == DomainType.BUSINESS:
        market_size = result.statistics.get("market_size", {}).get("mean", 0)
        if market_size > 100:  # 100 billion USD
            recommendations.append("LARGE MARKET OPPORTUNITY: Significant market size indicates high growth potential")
        elif market_size > 10:
            recommendations.append("MODERATE MARKET OPPORTUNITY: Stable market with growth potential")
        else:
            recommendations.append("SMALL MARKET: Consider niche strategies or market expansion")
    
    elif result.config.domain == DomainType.FINANCIAL:
        var_95 = result.risk_metrics.get("var_95", 0)
        if var_95 < -0.1:
            recommendations.append("HIGH RISK: Portfolio shows significant downside risk - consider risk mitigation strategies")
        elif var_95 < -0.05:
            recommendations.append("MODERATE RISK: Portfolio has moderate downside risk - monitor closely")
        else:
            recommendations.append("LOW RISK: Portfolio shows low downside risk")
    
    elif result.config.domain == DomainType.CYBERSECURITY:
        attack_freq = result.statistics.get("attack_frequency", {}).get("mean", 0)
        if attack_freq > 1000:
            recommendations.append("HIGH THREAT ENVIRONMENT: Frequent attacks detected - enhance security measures")
        elif attack_freq > 100:
            recommendations.append("MODERATE THREAT ENVIRONMENT: Regular attacks - maintain security posture")
        else:
            recommendations.append("LOW THREAT ENVIRONMENT: Minimal attack activity")
    
    # General recommendations
    recommendations.append("Continue monitoring and periodic reassessment")
    recommendations.append("Consider scenario planning for extreme cases")
    recommendations.append("Maintain data quality and update parameters regularly")
    
    return recommendations
