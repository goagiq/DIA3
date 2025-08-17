"""
Scenario Generation
Dynamic scenario generation for Monte Carlo simulations
"""

import numpy as np
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ScenarioGenerator:
    """Generate scenarios for Monte Carlo simulations"""
    
    def __init__(self):
        self.scenario_templates = {
            "risk_assessment": self._risk_assessment_template,
            "project_planning": self._project_planning_template,
            "supply_chain": self._supply_chain_template,
            "technology_risk": self._technology_risk_template,
            "environmental": self._environmental_template,
            "compliance": self._compliance_template
        }
    
    def generate_scenario(self, 
                         scenario_type: str,
                         parameters: Dict[str, Any],
                         time_horizon: Optional[int] = None) -> Dict[str, Any]:
        """Generate a scenario based on type and parameters"""
        
        if scenario_type not in self.scenario_templates:
            raise ValueError(f"Unknown scenario type: {scenario_type}")
        
        try:
            scenario = self.scenario_templates[scenario_type](parameters, time_horizon)
            scenario["scenario_type"] = scenario_type
            scenario["generated_at"] = datetime.now().isoformat()
            return scenario
        except Exception as e:
            logger.error(f"Error generating scenario {scenario_type}: {e}")
            raise
    
    def _risk_assessment_template(self, 
                                 parameters: Dict[str, Any],
                                 time_horizon: Optional[int]) -> Dict[str, Any]:
        """Risk assessment scenario template"""
        
        scenario = {
            "variables": {
                "operational_risk": {
                    "distribution": "normal",
                    "parameters": {
                        "mean": parameters.get("operational_risk_mean", 0.1),
                        "std": parameters.get("operational_risk_std", 0.05)
                    }
                },
                "market_risk": {
                    "distribution": "lognormal",
                    "parameters": {
                        "mean": parameters.get("market_risk_mean", 0.15),
                        "std": parameters.get("market_risk_std", 0.1)
                    }
                },
                "credit_risk": {
                    "distribution": "beta",
                    "parameters": {
                        "alpha": parameters.get("credit_risk_alpha", 2),
                        "beta": parameters.get("credit_risk_beta", 8)
                    }
                }
            },
            "correlations": [
                [1.0, 0.3, 0.1],
                [0.3, 1.0, 0.2],
                [0.1, 0.2, 1.0]
            ],
            "risk_metrics": ["var_95", "cvar_95", "expected_loss"],
            "time_series": time_horizon is not None
        }
        
        if time_horizon:
            scenario["time_horizon"] = time_horizon
            scenario["time_series_parameters"] = {
                "volatility_decay": parameters.get("volatility_decay", 0.95),
                "mean_reversion": parameters.get("mean_reversion", 0.1)
            }
        
        return scenario
    
    def _project_planning_template(self, 
                                  parameters: Dict[str, Any],
                                  time_horizon: Optional[int]) -> Dict[str, Any]:
        """Project planning scenario template"""
        
        scenario = {
            "variables": {
                "task_duration": {
                    "distribution": "gamma",
                    "parameters": {
                        "shape": parameters.get("task_duration_shape", 3),
                        "scale": parameters.get("task_duration_scale", 5)
                    }
                },
                "resource_cost": {
                    "distribution": "lognormal",
                    "parameters": {
                        "mean": parameters.get("resource_cost_mean", 1000),
                        "std": parameters.get("resource_cost_std", 200)
                    }
                },
                "quality_score": {
                    "distribution": "beta",
                    "parameters": {
                        "alpha": parameters.get("quality_alpha", 5),
                        "beta": parameters.get("quality_beta", 2)
                    }
                }
            },
            "correlations": [
                [1.0, 0.4, -0.2],
                [0.4, 1.0, -0.1],
                [-0.2, -0.1, 1.0]
            ],
            "project_metrics": ["completion_time", "total_cost", "quality_level"],
            "time_series": time_horizon is not None
        }
        
        if time_horizon:
            scenario["time_horizon"] = time_horizon
            scenario["milestones"] = parameters.get("milestones", [])
        
        return scenario
    
    def _supply_chain_template(self, 
                              parameters: Dict[str, Any],
                              time_horizon: Optional[int]) -> Dict[str, Any]:
        """Supply chain scenario template"""
        
        scenario = {
            "variables": {
                "demand": {
                    "distribution": "normal",
                    "parameters": {
                        "mean": parameters.get("demand_mean", 1000),
                        "std": parameters.get("demand_std", 100)
                    }
                },
                "lead_time": {
                    "distribution": "exponential",
                    "parameters": {
                        "scale": parameters.get("lead_time_scale", 7)
                    }
                },
                "supplier_reliability": {
                    "distribution": "beta",
                    "parameters": {
                        "alpha": parameters.get("reliability_alpha", 8),
                        "beta": parameters.get("reliability_beta", 2)
                    }
                }
            },
            "correlations": [
                [1.0, -0.3, 0.1],
                [-0.3, 1.0, -0.2],
                [0.1, -0.2, 1.0]
            ],
            "supply_chain_metrics": ["inventory_level", "service_level", "total_cost"],
            "time_series": time_horizon is not None
        }
        
        if time_horizon:
            scenario["time_horizon"] = time_horizon
            scenario["seasonality"] = parameters.get("seasonality", {})
        
        return scenario
    
    def _technology_risk_template(self, 
                                 parameters: Dict[str, Any],
                                 time_horizon: Optional[int]) -> Dict[str, Any]:
        """Technology risk scenario template"""
        
        scenario = {
            "variables": {
                "system_failure_rate": {
                    "distribution": "exponential",
                    "parameters": {
                        "scale": parameters.get("failure_rate_scale", 1000)
                    }
                },
                "cyber_attack_probability": {
                    "distribution": "beta",
                    "parameters": {
                        "alpha": parameters.get("attack_alpha", 1),
                        "beta": parameters.get("attack_beta", 99)
                    }
                },
                "performance_degradation": {
                    "distribution": "normal",
                    "parameters": {
                        "mean": parameters.get("degradation_mean", 0.05),
                        "std": parameters.get("degradation_std", 0.02)
                    }
                }
            },
            "correlations": [
                [1.0, 0.1, 0.3],
                [0.1, 1.0, 0.1],
                [0.3, 0.1, 1.0]
            ],
            "technology_metrics": ["uptime", "security_score", "performance"],
            "time_series": time_horizon is not None
        }
        
        if time_horizon:
            scenario["time_horizon"] = time_horizon
            scenario["maintenance_schedule"] = parameters.get("maintenance_schedule", [])
        
        return scenario
    
    def _environmental_template(self, 
                               parameters: Dict[str, Any],
                               time_horizon: Optional[int]) -> Dict[str, Any]:
        """Environmental risk scenario template"""
        
        scenario = {
            "variables": {
                "temperature_change": {
                    "distribution": "normal",
                    "parameters": {
                        "mean": parameters.get("temp_change_mean", 2.0),
                        "std": parameters.get("temp_change_std", 0.5)
                    }
                },
                "sea_level_rise": {
                    "distribution": "lognormal",
                    "parameters": {
                        "mean": parameters.get("sea_level_mean", 0.5),
                        "std": parameters.get("sea_level_std", 0.2)
                    }
                },
                "extreme_weather_frequency": {
                    "distribution": "poisson",
                    "parameters": {
                        "lambda": parameters.get("weather_lambda", 5)
                    }
                }
            },
            "correlations": [
                [1.0, 0.6, 0.3],
                [0.6, 1.0, 0.2],
                [0.3, 0.2, 1.0]
            ],
            "environmental_metrics": ["carbon_footprint", "adaptation_cost", "impact_score"],
            "time_series": time_horizon is not None
        }
        
        if time_horizon:
            scenario["time_horizon"] = time_horizon
            scenario["climate_scenarios"] = parameters.get("climate_scenarios", [])
        
        return scenario
    
    def _compliance_template(self, 
                            parameters: Dict[str, Any],
                            time_horizon: Optional[int]) -> Dict[str, Any]:
        """Compliance risk scenario template"""
        
        scenario = {
            "variables": {
                "regulatory_change_probability": {
                    "distribution": "beta",
                    "parameters": {
                        "alpha": parameters.get("reg_change_alpha", 2),
                        "beta": parameters.get("reg_change_beta", 8)
                    }
                },
                "compliance_cost": {
                    "distribution": "lognormal",
                    "parameters": {
                        "mean": parameters.get("compliance_cost_mean", 100000),
                        "std": parameters.get("compliance_cost_std", 50000)
                    }
                },
                "audit_findings": {
                    "distribution": "poisson",
                    "parameters": {
                        "lambda": parameters.get("audit_lambda", 2)
                    }
                }
            },
            "correlations": [
                [1.0, 0.4, 0.2],
                [0.4, 1.0, 0.3],
                [0.2, 0.3, 1.0]
            ],
            "compliance_metrics": ["compliance_score", "penalty_risk", "remediation_cost"],
            "time_series": time_horizon is not None
        }
        
        if time_horizon:
            scenario["time_horizon"] = time_horizon
            scenario["regulatory_timeline"] = parameters.get("regulatory_timeline", [])
        
        return scenario
    
    def generate_time_series_scenario(self, 
                                    base_scenario: Dict[str, Any],
                                    time_steps: int) -> Dict[str, Any]:
        """Generate time series scenario from base scenario"""
        
        scenario = base_scenario.copy()
        scenario["time_series"] = True
        scenario["time_steps"] = time_steps
        
        # Add time series parameters
        for var_name, var_config in scenario["variables"].items():
            if "time_series_parameters" not in var_config:
                var_config["time_series_parameters"] = {
                    "volatility_decay": 0.95,
                    "mean_reversion": 0.1,
                    "trend": 0.0
                }
        
        return scenario
    
    def validate_scenario(self, scenario: Dict[str, Any]) -> bool:
        """Validate scenario configuration"""
        
        required_keys = ["variables", "correlations"]
        
        # Check required keys
        for key in required_keys:
            if key not in scenario:
                logger.error(f"Missing required key: {key}")
                return False
        
        # Check variables
        if not isinstance(scenario["variables"], dict):
            logger.error("Variables must be a dictionary")
            return False
        
        for var_name, var_config in scenario["variables"].items():
            if not isinstance(var_config, dict):
                logger.error(f"Variable config for {var_name} must be a dictionary")
                return False
            
            if "distribution" not in var_config or "parameters" not in var_config:
                logger.error(f"Variable {var_name} missing distribution or parameters")
                return False
        
        # Check correlations
        if not isinstance(scenario["correlations"], list):
            logger.error("Correlations must be a list")
            return False
        
        # Validate correlation matrix
        try:
            corr_matrix = np.array(scenario["correlations"])
            if corr_matrix.shape[0] != corr_matrix.shape[1]:
                logger.error("Correlation matrix must be square")
                return False
            
            if len(scenario["variables"]) != corr_matrix.shape[0]:
                logger.error("Correlation matrix size must match number of variables")
                return False
        except Exception as e:
            logger.error(f"Error validating correlation matrix: {e}")
            return False
        
        return True
    
    def list_scenario_types(self) -> List[str]:
        """List available scenario types"""
        return list(self.scenario_templates.keys())
    
    def get_scenario_info(self, scenario_type: str) -> Dict[str, Any]:
        """Get information about a scenario type"""
        
        if scenario_type not in self.scenario_templates:
            return {}
        
        info = {
            "risk_assessment": {
                "description": "Operational, market, and credit risk assessment",
                "variables": ["operational_risk", "market_risk", "credit_risk"],
                "metrics": ["var_95", "cvar_95", "expected_loss"]
            },
            "project_planning": {
                "description": "Project timeline and resource planning",
                "variables": ["task_duration", "resource_cost", "quality_score"],
                "metrics": ["completion_time", "total_cost", "quality_level"]
            },
            "supply_chain": {
                "description": "Supply chain optimization and risk",
                "variables": ["demand", "lead_time", "supplier_reliability"],
                "metrics": ["inventory_level", "service_level", "total_cost"]
            },
            "technology_risk": {
                "description": "Technology system reliability and security",
                "variables": ["system_failure_rate", "cyber_attack_probability", "performance_degradation"],
                "metrics": ["uptime", "security_score", "performance"]
            },
            "environmental": {
                "description": "Environmental and climate risk assessment",
                "variables": ["temperature_change", "sea_level_rise", "extreme_weather_frequency"],
                "metrics": ["carbon_footprint", "adaptation_cost", "impact_score"]
            },
            "compliance": {
                "description": "Regulatory compliance and audit risk",
                "variables": ["regulatory_change_probability", "compliance_cost", "audit_findings"],
                "metrics": ["compliance_score", "penalty_risk", "remediation_cost"]
            }
        }
        
        return info.get(scenario_type, {})
