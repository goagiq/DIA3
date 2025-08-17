#!/usr/bin/env python3
"""
Multi-Domain Monte Carlo MCP Tools
MCP tools for comprehensive Monte Carlo simulation across defense, intelligence, and business domains.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.core.multi_domain_monte_carlo_engine import (
    MultiDomainMonteCarloEngine,
    SimulationConfig,
    DomainType,
    SimulationType
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MultiDomainMonteCarloMCPTools:
    """MCP tools for multi-domain Monte Carlo simulations."""
    
    def __init__(self):
        self.engine = MultiDomainMonteCarloEngine()
        self.active_simulations: Dict[str, Any] = {}
        
    async def run_defense_simulation(
        self,
        scenario_name: str = "military_capability",
        num_iterations: int = 10000,
        confidence_level: float = 0.95,
        custom_variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation for defense domain.
        
        Args:
            scenario_name: Name of the scenario to run
            num_iterations: Number of Monte Carlo iterations
            confidence_level: Confidence level for intervals
            custom_variables: Custom variables to override defaults
            
        Returns:
            Simulation results
        """
        try:
            config = SimulationConfig(
                domain=DomainType.DEFENSE,
                simulation_type=SimulationType.CAPABILITY_ASSESSMENT,
                num_iterations=num_iterations,
                confidence_level=confidence_level
            )
            
            result = await self.engine.run_simulation(config, scenario_name, custom_variables)
            
            return {
                "simulation_id": result.simulation_id,
                "domain": "defense",
                "scenario": scenario_name,
                "iterations": result.config.num_iterations,
                "execution_time": result.execution_time,
                "statistics": result.statistics,
                "risk_metrics": result.risk_metrics,
                "confidence_intervals": result.confidence_intervals,
                "timestamp": result.timestamp.isoformat(),
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error in defense simulation: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def run_business_simulation(
        self,
        scenario_name: str = "market_analysis",
        num_iterations: int = 10000,
        confidence_level: float = 0.95,
        custom_variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation for business domain.
        
        Args:
            scenario_name: Name of the scenario to run
            num_iterations: Number of Monte Carlo iterations
            confidence_level: Confidence level for intervals
            custom_variables: Custom variables to override defaults
            
        Returns:
            Simulation results
        """
        try:
            config = SimulationConfig(
                domain=DomainType.BUSINESS,
                simulation_type=SimulationType.RISK_ANALYSIS,
                num_iterations=num_iterations,
                confidence_level=confidence_level
            )
            
            result = await self.engine.run_simulation(config, scenario_name, custom_variables)
            
            return {
                "simulation_id": result.simulation_id,
                "domain": "business",
                "scenario": scenario_name,
                "iterations": result.config.num_iterations,
                "execution_time": result.execution_time,
                "statistics": result.statistics,
                "risk_metrics": result.risk_metrics,
                "confidence_intervals": result.confidence_intervals,
                "timestamp": result.timestamp.isoformat(),
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error in business simulation: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def run_financial_simulation(
        self,
        scenario_name: str = "portfolio_risk",
        num_iterations: int = 10000,
        confidence_level: float = 0.95,
        custom_variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation for financial domain.
        
        Args:
            scenario_name: Name of the scenario to run
            num_iterations: Number of Monte Carlo iterations
            confidence_level: Confidence level for intervals
            custom_variables: Custom variables to override defaults
            
        Returns:
            Simulation results
        """
        try:
            config = SimulationConfig(
                domain=DomainType.FINANCIAL,
                simulation_type=SimulationType.RISK_ANALYSIS,
                num_iterations=num_iterations,
                confidence_level=confidence_level
            )
            
            result = await self.engine.run_simulation(config, scenario_name, custom_variables)
            
            return {
                "simulation_id": result.simulation_id,
                "domain": "financial",
                "scenario": scenario_name,
                "iterations": result.config.num_iterations,
                "execution_time": result.execution_time,
                "statistics": result.statistics,
                "risk_metrics": result.risk_metrics,
                "confidence_intervals": result.confidence_intervals,
                "timestamp": result.timestamp.isoformat(),
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error in financial simulation: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def run_cybersecurity_simulation(
        self,
        scenario_name: str = "threat_assessment",
        num_iterations: int = 10000,
        confidence_level: float = 0.95,
        custom_variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation for cybersecurity domain.
        
        Args:
            scenario_name: Name of the scenario to run
            num_iterations: Number of Monte Carlo iterations
            confidence_level: Confidence level for intervals
            custom_variables: Custom variables to override defaults
            
        Returns:
            Simulation results
        """
        try:
            config = SimulationConfig(
                domain=DomainType.CYBERSECURITY,
                simulation_type=SimulationType.THREAT_ASSESSMENT,
                num_iterations=num_iterations,
                confidence_level=confidence_level
            )
            
            result = await self.engine.run_simulation(config, scenario_name, custom_variables)
            
            return {
                "simulation_id": result.simulation_id,
                "domain": "cybersecurity",
                "scenario": scenario_name,
                "iterations": result.config.num_iterations,
                "execution_time": result.execution_time,
                "statistics": result.statistics,
                "risk_metrics": result.risk_metrics,
                "confidence_intervals": result.confidence_intervals,
                "timestamp": result.timestamp.isoformat(),
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error in cybersecurity simulation: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def run_custom_simulation(
        self,
        domain: str,
        scenario_name: str,
        simulation_type: str,
        variables: Dict[str, Any],
        correlations: Optional[List[List[float]]] = None,
        num_iterations: int = 10000,
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        Run custom Monte Carlo simulation with user-defined parameters.
        
        Args:
            domain: Domain type (defense, business, financial, cybersecurity)
            scenario_name: Name of the scenario
            simulation_type: Type of simulation
            variables: Variable definitions
            correlations: Correlation matrix
            num_iterations: Number of Monte Carlo iterations
            confidence_level: Confidence level for intervals
            
        Returns:
            Simulation results
        """
        try:
            # Validate domain
            try:
                domain_enum = DomainType(domain)
            except ValueError:
                return {
                    "error": f"Invalid domain: {domain}. Supported domains: {[d.value for d in DomainType]}",
                    "status": "failed"
                }
            
            # Validate simulation type
            try:
                sim_type_enum = SimulationType(simulation_type)
            except ValueError:
                return {
                    "error": f"Invalid simulation type: {simulation_type}. Supported types: {[s.value for s in SimulationType]}",
                    "status": "failed"
                }
            
            config = SimulationConfig(
                domain=domain_enum,
                simulation_type=sim_type_enum,
                num_iterations=num_iterations,
                confidence_level=confidence_level
            )
            
            # Create custom scenario
            custom_scenario = {
                "variables": variables,
                "correlations": correlations or []
            }
            
            result = await self.engine.run_simulation(config, scenario_name, custom_scenario)
            
            return {
                "simulation_id": result.simulation_id,
                "domain": domain,
                "scenario": scenario_name,
                "simulation_type": simulation_type,
                "iterations": result.config.num_iterations,
                "execution_time": result.execution_time,
                "statistics": result.statistics,
                "risk_metrics": result.risk_metrics,
                "confidence_intervals": result.confidence_intervals,
                "timestamp": result.timestamp.isoformat(),
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error in custom simulation: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def get_available_scenarios(self) -> Dict[str, Any]:
        """
        Get available scenarios for all domains.
        
        Returns:
            Dictionary of available scenarios by domain
        """
        try:
            scenarios = self.engine.get_available_scenarios()
            
            return {
                "available_scenarios": scenarios,
                "total_domains": len(scenarios),
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error getting available scenarios: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get performance summary across all domains.
        
        Returns:
            Performance summary
        """
        try:
            performance = self.engine.get_performance_summary()
            
            return {
                "performance_summary": performance,
                "total_domains": len(performance),
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error getting performance summary: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def load_cached_simulation(self, simulation_id: str) -> Dict[str, Any]:
        """
        Load cached simulation result.
        
        Args:
            simulation_id: ID of the cached simulation
            
        Returns:
            Cached simulation result
        """
        try:
            result = await self.engine.load_cached_result(simulation_id)
            
            if result is None:
                return {
                    "error": f"Simulation {simulation_id} not found in cache",
                    "status": "not_found"
                }
            
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
            
        except Exception as e:
            logger.error(f"Error loading cached simulation: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def generate_simulation_report(
        self,
        simulation_id: str,
        report_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Generate comprehensive report for a simulation.
        
        Args:
            simulation_id: ID of the simulation
            report_format: Format of the report (json, text, html)
            
        Returns:
            Generated report
        """
        try:
            # Load simulation result
            result = await self.engine.load_cached_result(simulation_id)
            
            if result is None:
                return {
                    "error": f"Simulation {simulation_id} not found",
                    "status": "not_found"
                }
            
            # Generate report based on format
            if report_format == "json":
                report = self._generate_json_report(result)
            elif report_format == "text":
                report = self._generate_text_report(result)
            elif report_format == "html":
                report = self._generate_html_report(result)
            else:
                return {
                    "error": f"Unsupported report format: {report_format}",
                    "status": "failed"
                }
            
            return {
                "simulation_id": simulation_id,
                "report_format": report_format,
                "report": report,
                "timestamp": datetime.now().isoformat(),
                "status": "generated"
            }
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _generate_json_report(self, result) -> Dict[str, Any]:
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
            "recommendations": self._generate_recommendations(result)
        }
    
    def _generate_text_report(self, result) -> str:
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
        recommendations = self._generate_recommendations(result)
        for i, rec in enumerate(recommendations, 1):
            report_lines.append(f"{i}. {rec}")
        
        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def _generate_html_report(self, result) -> str:
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
        
        recommendations = self._generate_recommendations(result)
        for i, rec in enumerate(recommendations, 1):
            html += f'<p><strong>{i}.</strong> {rec}</p>'
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generate_recommendations(self, result) -> List[str]:
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


# Create global instance
multi_domain_monte_carlo_tools = MultiDomainMonteCarloMCPTools()


# MCP Tool Functions
async def run_defense_simulation(
    scenario_name: str = "military_capability",
    num_iterations: int = 10000,
    confidence_level: float = 0.95,
    custom_variables: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Run Monte Carlo simulation for defense domain."""
    return await multi_domain_monte_carlo_tools.run_defense_simulation(
        scenario_name, num_iterations, confidence_level, custom_variables
    )


async def run_business_simulation(
    scenario_name: str = "market_analysis",
    num_iterations: int = 10000,
    confidence_level: float = 0.95,
    custom_variables: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Run Monte Carlo simulation for business domain."""
    return await multi_domain_monte_carlo_tools.run_business_simulation(
        scenario_name, num_iterations, confidence_level, custom_variables
    )


async def run_financial_simulation(
    scenario_name: str = "portfolio_risk",
    num_iterations: int = 10000,
    confidence_level: float = 0.95,
    custom_variables: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Run Monte Carlo simulation for financial domain."""
    return await multi_domain_monte_carlo_tools.run_financial_simulation(
        scenario_name, num_iterations, confidence_level, custom_variables
    )


async def run_cybersecurity_simulation(
    scenario_name: str = "threat_assessment",
    num_iterations: int = 10000,
    confidence_level: float = 0.95,
    custom_variables: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Run Monte Carlo simulation for cybersecurity domain."""
    return await multi_domain_monte_carlo_tools.run_cybersecurity_simulation(
        scenario_name, num_iterations, confidence_level, custom_variables
    )


async def run_custom_simulation(
    domain: str,
    scenario_name: str,
    simulation_type: str,
    variables: Dict[str, Any],
    correlations: Optional[List[List[float]]] = None,
    num_iterations: int = 10000,
    confidence_level: float = 0.95
) -> Dict[str, Any]:
    """Run custom Monte Carlo simulation with user-defined parameters."""
    return await multi_domain_monte_carlo_tools.run_custom_simulation(
        domain, scenario_name, simulation_type, variables, correlations, num_iterations, confidence_level
    )


async def get_available_scenarios() -> Dict[str, Any]:
    """Get available scenarios for all domains."""
    return await multi_domain_monte_carlo_tools.get_available_scenarios()


async def get_performance_summary() -> Dict[str, Any]:
    """Get performance summary across all domains."""
    return await multi_domain_monte_carlo_tools.get_performance_summary()


async def load_cached_simulation(simulation_id: str) -> Dict[str, Any]:
    """Load cached simulation result."""
    return await multi_domain_monte_carlo_tools.load_cached_simulation(simulation_id)


async def generate_simulation_report(
    simulation_id: str,
    report_format: str = "json"
) -> Dict[str, Any]:
    """Generate comprehensive report for a simulation."""
    return await multi_domain_monte_carlo_tools.generate_simulation_report(simulation_id, report_format)
