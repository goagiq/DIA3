"""
Force Projection MCP Tools
MCP tools for force projection simulation capabilities using Monte Carlo analysis
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from ..core.force_projection_engine import ForceProjectionEngine, AdversaryType, DomainType

logger = logging.getLogger(__name__)


class ForceProjectionMCPTools:
    """MCP tools for force projection simulation capabilities"""
    
    def __init__(self, orchestrator=None):
        """Initialize force projection MCP tools"""
        self.force_projection_engine = ForceProjectionEngine(orchestrator)
        self.tools = self._initialize_tools()
        
        logger.info("Force Projection MCP Tools initialized successfully")
    
    def _initialize_tools(self) -> Dict[str, Any]:
        """Initialize MCP tools for force projection simulation"""
        return {
            "force_projection_simulation": {
                "name": "force_projection_simulation",
                "description": "Simulate adversary force projection capabilities using log-normal distribution Monte Carlo analysis",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "adversary_type": {
                            "type": "string",
                            "enum": [e.value for e in AdversaryType],
                            "description": "Type of adversary to simulate"
                        },
                        "domain_type": {
                            "type": "string", 
                            "enum": [e.value for e in DomainType],
                            "description": "Domain type for analysis (defense, business, cyber, financial)"
                        },
                        "time_horizon_months": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 60,
                            "default": 24,
                            "description": "Time horizon for projection analysis in months"
                        },
                        "num_iterations": {
                            "type": "integer",
                            "minimum": 1000,
                            "maximum": 50000,
                            "default": 10000,
                            "description": "Number of Monte Carlo iterations"
                        },
                        "confidence_level": {
                            "type": "number",
                            "minimum": 0.8,
                            "maximum": 0.99,
                            "default": 0.95,
                            "description": "Confidence level for statistical analysis"
                        },
                        "custom_parameters": {
                            "type": "object",
                            "description": "Custom parameters for simulation (optional)"
                        }
                    },
                    "required": ["adversary_type", "domain_type"]
                }
            },
            "force_projection_visualization": {
                "name": "force_projection_visualization",
                "description": "Create visualization for force projection simulation results",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "simulation_id": {
                            "type": "string",
                            "description": "ID of the simulation to visualize"
                        },
                        "save_path": {
                            "type": "string",
                            "description": "Path to save visualization (optional)"
                        }
                    },
                    "required": ["simulation_id"]
                }
            },
            "force_projection_history": {
                "name": "force_projection_history",
                "description": "Get simulation history and performance metrics",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 100,
                            "default": 50,
                            "description": "Number of recent simulations to return"
                        }
                    }
                }
            },
            "force_projection_export": {
                "name": "force_projection_export",
                "description": "Export simulation results in various formats",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "simulation_id": {
                            "type": "string",
                            "description": "ID of the simulation to export"
                        },
                        "format": {
                            "type": "string",
                            "enum": ["json", "csv", "excel"],
                            "default": "json",
                            "description": "Export format"
                        }
                    },
                    "required": ["simulation_id"]
                }
            },
            "force_projection_comparison": {
                "name": "force_projection_comparison",
                "description": "Compare multiple force projection simulations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "simulation_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of simulation IDs to compare"
                        },
                        "comparison_metrics": {
                            "type": "array",
                            "items": {"type": "string"},
                            "enum": ["effectiveness", "capabilities", "readiness", "environmental"],
                            "default": ["effectiveness"],
                            "description": "Metrics to compare"
                        }
                    },
                    "required": ["simulation_ids"]
                }
            }
        }
    
    async def force_projection_simulation(self, **kwargs) -> Dict[str, Any]:
        """Execute force projection simulation"""
        try:
            logger.info(f"Starting force projection simulation with parameters: {kwargs}")
            
            # Extract parameters
            adversary_type = kwargs.get("adversary_type", "peer_adversary")
            domain_type = kwargs.get("domain_type", "defense")
            time_horizon_months = kwargs.get("time_horizon_months", 24)
            num_iterations = kwargs.get("num_iterations", 10000)
            confidence_level = kwargs.get("confidence_level", 0.95)
            custom_parameters = kwargs.get("custom_parameters")
            
            # Run simulation
            result = await self.force_projection_engine.simulate_force_projection_capabilities(
                adversary_type=adversary_type,
                domain_type=domain_type,
                time_horizon_months=time_horizon_months,
                num_iterations=num_iterations,
                confidence_level=confidence_level,
                custom_parameters=custom_parameters
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
            
            logger.info(f"Force projection simulation completed: {result.simulation_id}")
            
            return {
                "success": True,
                "simulation_id": result.simulation_id,
                "result": result_dict,
                "summary": {
                    "threat_level": result.threat_assessment["threat_level"],
                    "overall_effectiveness": result.effectiveness_analysis["overall_effectiveness"],
                    "execution_time": result.metadata["execution_time_seconds"],
                    "recommendations_count": len(result.recommendations)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in force projection simulation: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "simulation_id": None
            }
    
    async def force_projection_visualization(self, **kwargs) -> Dict[str, Any]:
        """Create visualization for force projection simulation results"""
        try:
            simulation_id = kwargs.get("simulation_id")
            save_path = kwargs.get("save_path")
            
            # Find simulation in history
            history = self.force_projection_engine.get_simulation_history(limit=1000)
            target_simulation = None
            
            for simulation in history:
                if simulation.simulation_id == simulation_id:
                    target_simulation = simulation
                    break
            
            if not target_simulation:
                return {
                    "success": False,
                    "error": f"Simulation with ID {simulation_id} not found"
                }
            
            # Create visualization
            visualization_data = self.force_projection_engine.create_visualization(
                target_simulation, save_path
            )
            
            return {
                "success": True,
                "simulation_id": simulation_id,
                "visualization": visualization_data,
                "save_path": save_path
            }
            
        except Exception as e:
            logger.error(f"Error creating force projection visualization: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def force_projection_history(self, **kwargs) -> Dict[str, Any]:
        """Get simulation history and performance metrics"""
        try:
            limit = kwargs.get("limit", 50)
            
            # Get simulation history
            history = self.force_projection_engine.get_simulation_history(limit=limit)
            
            # Get performance metrics
            performance_metrics = self.force_projection_engine.get_performance_metrics()
            
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
            return {
                "success": False,
                "error": str(e)
            }
    
    async def force_projection_export(self, **kwargs) -> Dict[str, Any]:
        """Export simulation results in various formats"""
        try:
            simulation_id = kwargs.get("simulation_id")
            export_format = kwargs.get("format", "json")
            
            # Find simulation in history
            history = self.force_projection_engine.get_simulation_history(limit=1000)
            target_simulation = None
            
            for simulation in history:
                if simulation.simulation_id == simulation_id:
                    target_simulation = simulation
                    break
            
            if not target_simulation:
                return {
                    "success": False,
                    "error": f"Simulation with ID {simulation_id} not found"
                }
            
            # Export simulation
            export_data = self.force_projection_engine.export_simulation_result(
                target_simulation, export_format
            )
            
            return {
                "success": True,
                "simulation_id": simulation_id,
                "format": export_format,
                "export_data": export_data
            }
            
        except Exception as e:
            logger.error(f"Error exporting force projection simulation: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def force_projection_comparison(self, **kwargs) -> Dict[str, Any]:
        """Compare multiple force projection simulations"""
        try:
            simulation_ids = kwargs.get("simulation_ids", [])
            comparison_metrics = kwargs.get("comparison_metrics", ["effectiveness"])
            
            if not simulation_ids:
                return {
                    "success": False,
                    "error": "No simulation IDs provided for comparison"
                }
            
            # Find simulations in history
            history = self.force_projection_engine.get_simulation_history(limit=1000)
            target_simulations = []
            
            for simulation in history:
                if simulation.simulation_id in simulation_ids:
                    target_simulations.append(simulation)
            
            if len(target_simulations) != len(simulation_ids):
                found_ids = [s.simulation_id for s in target_simulations]
                missing_ids = [sid for sid in simulation_ids if sid not in found_ids]
                return {
                    "success": False,
                    "error": f"Some simulations not found: {missing_ids}"
                }
            
            # Perform comparison
            comparison_results = {}
            
            for metric in comparison_metrics:
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
                "simulation_ids": simulation_ids
            }
            
        except Exception as e:
            logger.error(f"Error comparing force projection simulations: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_tools(self) -> Dict[str, Any]:
        """Get all available tools"""
        return self.tools
    
    def get_tool_names(self) -> List[str]:
        """Get list of available tool names"""
        return list(self.tools.keys())
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a specific tool by name"""
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found. Available tools: {self.get_tool_names()}"
            }
        
        # Map tool names to methods
        tool_methods = {
            "force_projection_simulation": self.force_projection_simulation,
            "force_projection_visualization": self.force_projection_visualization,
            "force_projection_history": self.force_projection_history,
            "force_projection_export": self.force_projection_export,
            "force_projection_comparison": self.force_projection_comparison
        }
        
        method = tool_methods.get(tool_name)
        if method:
            return await method(**kwargs)
        else:
            return {
                "success": False,
                "error": f"Method for tool '{tool_name}' not implemented"
            }
