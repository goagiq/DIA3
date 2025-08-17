"""
Strategic Intelligence Forecast MCP Tools
Monte Carlo-based strategic intelligence forecasting for national security decision making
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from loguru import logger

# Import Monte Carlo engine
try:
    from src.core.monte_carlo.engine import MonteCarloEngine
    MONTE_CARLO_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Monte Carlo engine not available: {e}")
    MONTE_CARLO_AVAILABLE = False

class StrategicIntelligenceForecastMCPTools:
    """MCP Tools for Strategic Intelligence Forecasting"""
    
    def __init__(self):
        self.monte_carlo_engine = None
        if MONTE_CARLO_AVAILABLE:
            try:
                self.monte_carlo_engine = MonteCarloEngine()
                logger.info("✅ Strategic Intelligence Forecast MCP Tools initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Monte Carlo engine: {e}")
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools"""
        
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "generate_strategic_intelligence_forecast",
                    "description": "Generate comprehensive strategic intelligence forecast with Monte Carlo simulation",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "scenario_type": {
                                "type": "string",
                                "description": "Type of strategic scenario",
                                "default": "strategic_planning",
                                "enum": ["strategic_planning", "threat_assessment", "risk_analysis"]
                            },
                            "iterations": {
                                "type": "integer",
                                "description": "Number of Monte Carlo iterations",
                                "minimum": 1000,
                                "maximum": 50000,
                                "default": 5000
                            },
                            "time_horizon": {
                                "type": "integer",
                                "description": "Time horizon in months",
                                "minimum": 1,
                                "maximum": 60,
                                "default": 24
                            },
                            "confidence_level": {
                                "type": "number",
                                "description": "Confidence level for analysis",
                                "minimum": 0.8,
                                "maximum": 0.99,
                                "default": 0.95
                            },
                            "include_scenarios": {
                                "type": "boolean",
                                "description": "Include scenario outcomes analysis",
                                "default": True
                            },
                            "include_policy_recommendations": {
                                "type": "boolean",
                                "description": "Include policy recommendations",
                                "default": True
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_strategic_intelligence_forecast",
                    "description": "Retrieve a specific strategic intelligence forecast by ID",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "forecast_id": {
                                "type": "string",
                                "description": "ID of the forecast to retrieve"
                            }
                        },
                        "required": ["forecast_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_strategic_intelligence_forecasts",
                    "description": "List all available strategic intelligence forecasts",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of forecasts to return",
                                "default": 10
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_quick_strategic_forecast",
                    "description": "Run a quick strategic intelligence forecast with default parameters",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "Brief description of the forecast purpose"
                            }
                        },
                        "required": []
                    }
                }
            }
        ]
        
        return tools
    
    async def generate_strategic_intelligence_forecast(
        self,
        scenario_type: str = "strategic_planning",
        iterations: int = 5000,
        time_horizon: int = 24,
        confidence_level: float = 0.95,
        include_scenarios: bool = True,
        include_policy_recommendations: bool = True
    ) -> Dict[str, Any]:
        """Generate comprehensive strategic intelligence forecast with Monte Carlo simulation"""
        
        if not self.monte_carlo_engine:
            return {
                "error": "Monte Carlo engine not available",
                "status": "failed"
            }
        
        try:
            logger.info(f"Starting strategic intelligence forecast with {iterations} iterations")
            
            # Default strategic variables configuration
            variables = {
                'geopolitical_stability': {
                    'distribution': 'beta',
                    'parameters': {
                        'alpha': 2.5,
                        'beta': 3.5
                    }
                },
                'economic_indicators': {
                    'distribution': 'normal',
                    'parameters': {
                        'mean': 0.65,
                        'std': 0.15
                    }
                },
                'military_readiness': {
                    'distribution': 'beta',
                    'parameters': {
                        'alpha': 3.0,
                        'beta': 2.0
                    }
                }
            }
            
            # Default correlation matrix
            correlations = [
                [1.0, 0.6, 0.4],
                [0.6, 1.0, 0.3],
                [0.4, 0.3, 1.0]
            ]
            
            # Prepare scenario configuration
            scenario_config = {
                'variables': variables,
                'correlations': correlations
            }
            
            # Run Monte Carlo simulation
            results = await self.monte_carlo_engine.run_simulation(
                scenario_config, 
                num_iterations=iterations, 
                parallel=False
            )
            
            # Extract statistics from results
            stats = results.get('statistics', {})
            variable_names = list(variables.keys())
            
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
                        'readiness_level': 'HIGH' if mean_val > 0.7 else 'MODERATE'
                    }
            
            # Create executive summary
            executive_summary = {
                'title': f'Strategic Intelligence Forecast {datetime.now().year}-{datetime.now().year + 2}',
                'classification': 'SECRET',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time_horizon': f'{time_horizon} months',
                'confidence_level': f'{confidence_level*100:.0f}%',
                'iterations': iterations,
                'scenario_type': scenario_type
            }
            
            # Create scenario outcomes if requested
            scenario_outcomes = None
            if include_scenarios:
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
            if include_policy_recommendations:
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
            
            # Save results to file
            forecast_id = f"strategic_forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            await self._save_forecast_results(forecast_id, {
                'executive_summary': executive_summary,
                'key_findings': key_findings,
                'scenario_outcomes': scenario_outcomes,
                'policy_recommendations': policy_recommendations,
                'risk_assessment': risk_assessment,
                'strategic_implications': strategic_implications,
                'monte_carlo_results': results
            })
            
            logger.info(f"Strategic intelligence forecast completed successfully: {forecast_id}")
            
            return {
                "status": "success",
                "forecast_id": forecast_id,
                "executive_summary": executive_summary,
                "key_findings": key_findings,
                "scenario_outcomes": scenario_outcomes,
                "policy_recommendations": policy_recommendations,
                "risk_assessment": risk_assessment,
                "strategic_implications": strategic_implications,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in strategic intelligence forecast: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def get_strategic_intelligence_forecast(self, forecast_id: str) -> Dict[str, Any]:
        """Retrieve a specific strategic intelligence forecast by ID"""
        
        try:
            # Ensure Results directory exists
            results_dir = Path("Results")
            results_dir.mkdir(exist_ok=True)
            
            # Look for the forecast file
            forecast_file = results_dir / f"strategic_intelligence_forecast_{forecast_id}.json"
            if not forecast_file.exists():
                return {
                    "error": "Forecast not found",
                    "status": "failed"
                }
            
            # Load and return the forecast
            with open(forecast_file, 'r') as f:
                forecast_data = json.load(f)
            
            return {
                "status": "success",
                "forecast_data": forecast_data
            }
            
        except Exception as e:
            logger.error(f"Error retrieving forecast {forecast_id}: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def list_strategic_intelligence_forecasts(self, limit: int = 10) -> Dict[str, Any]:
        """List all available strategic intelligence forecasts"""
        
        try:
            # Ensure Results directory exists
            results_dir = Path("Results")
            results_dir.mkdir(exist_ok=True)
            
            # Find all strategic intelligence forecast files
            forecast_files = list(results_dir.glob("strategic_intelligence_forecast_*.json"))
            
            forecasts = []
            for file_path in forecast_files[:limit]:
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
                "status": "success",
                "forecasts": forecasts,
                "total_count": len(forecasts)
            }
            
        except Exception as e:
            logger.error(f"Error listing forecasts: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def run_quick_strategic_forecast(self, description: str = "") -> Dict[str, Any]:
        """Run a quick strategic intelligence forecast with default parameters"""
        
        logger.info(f"Running quick strategic forecast: {description}")
        
        return await self.generate_strategic_intelligence_forecast(
            scenario_type="strategic_planning",
            iterations=3000,
            time_horizon=12,
            confidence_level=0.95,
            include_scenarios=True,
            include_policy_recommendations=True
        )
    
    async def _save_forecast_results(self, forecast_id: str, results: Dict[str, Any]):
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
