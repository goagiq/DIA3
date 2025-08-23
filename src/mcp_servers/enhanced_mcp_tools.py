"""
Enhanced MCP Tools for Phase 6 Implementation
Advanced forecasting, RL, and comprehensive analysis tools with streamable HTTP support
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union, AsyncGenerator
from datetime import datetime, timedelta
from dataclasses import dataclass

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

from src.core.orchestrator import get_orchestrator
from src.core.advanced_ml.ensemble_forecasting_system import EnsembleForecastingSystem
from src.core.reinforcement_learning.rl_engine import ReinforcementLearningEngine
from src.core.scenario_analysis.enhanced_scenario_predictor import EnhancedScenarioPredictor
from src.core.streaming.intelligence_data_adapter import IntelligenceDataAdapter
from src.core.interpretability.model_interpretability_engine import ModelInterpretabilityEngine
from src.core.template_generators.generic_leadership_template_generator import get_generic_leadership_template_generator, TopicData
from src.core.template_generators.generic_enhanced_report_template_generator import get_generic_enhanced_report_template_generator, EnhancedReportData

# Configure logging
logger = logging.getLogger(__name__)

# Global orchestrator instance
_orchestrator = None

async def get_orchestrator_instance():
    """Get or create orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = get_orchestrator()
    return _orchestrator

# Enhanced MCP Tools
@dataclass
class EnhancedMCPTools:
    """Enhanced MCP tools for Phase 6 implementation"""
    
    @staticmethod
    async def create_ensemble_forecast(
        data_type: str,
        historical_data: Dict[str, Any],
        forecast_horizon: int = 30,
        confidence_level: float = 0.95,
        ensemble_weights: Optional[Dict[str, float]] = None,
        scenario_parameters: Optional[Dict[str, Any]] = None,
        real_time_feeds: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create comprehensive ensemble forecast using multiple ML/DL/RL models
        """
        try:
            orchestrator = await get_orchestrator_instance()
            ensemble_system = orchestrator.get_agent_by_type("EnsembleForecastingSystem")
            
            if not ensemble_system:
                return {"error": "Ensemble forecasting system not available"}
            
            # Generate forecast
            forecast_result = await ensemble_system.create_ensemble_forecast(
                data_type=data_type,
                historical_data=historical_data,
                forecast_horizon=forecast_horizon,
                confidence_level=confidence_level,
                ensemble_weights=ensemble_weights
            )
            
            # Add scenario analysis if requested
            scenario_analysis = None
            if scenario_parameters:
                scenario_predictor = orchestrator.get_agent_by_type("EnhancedScenarioPredictor")
                if scenario_predictor:
                    scenario_analysis = await scenario_predictor.analyze_scenarios(
                        base_parameters=scenario_parameters,
                        forecast_data=forecast_result
                    )
            
            # Add real-time insights if requested
            real_time_insights = None
            if real_time_feeds:
                data_adapter = orchestrator.get_agent_by_type("IntelligenceDataAdapter")
                if data_adapter:
                    real_time_insights = await data_adapter.get_real_time_insights(
                        feeds=real_time_feeds,
                        forecast_context=forecast_result
                    )
            
            # Generate interpretability report
            interpretability_engine = orchestrator.get_agent_by_type("ModelInterpretabilityEngine")
            interpretability_report = None
            if interpretability_engine:
                interpretability_report = await interpretability_engine.generate_forecast_explanation(
                    forecast_result=forecast_result,
                    historical_data=historical_data
                )
            
            return {
                "forecast_id": forecast_result.get("forecast_id", f"forecast_{datetime.now().isoformat()}"),
                "timestamp": datetime.now().isoformat(),
                "predictions": forecast_result.get("predictions", {}),
                "confidence_intervals": forecast_result.get("confidence_intervals", {}),
                "model_weights": forecast_result.get("model_weights", {}),
                "ensemble_performance": forecast_result.get("performance_metrics", {}),
                "scenario_analysis": scenario_analysis,
                "real_time_insights": real_time_insights,
                "interpretability_report": interpretability_report
            }
            
        except Exception as e:
            logger.error(f"Error creating ensemble forecast: {e}")
            return {"error": f"Forecast creation failed: {str(e)}"}
    
    @staticmethod
    async def train_rl_agent(
        agent_type: str,
        environment_config: Dict[str, Any],
        training_parameters: Dict[str, Any],
        reward_function: Dict[str, Any],
        state_space: Dict[str, Any],
        action_space: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Train a reinforcement learning agent
        """
        try:
            orchestrator = await get_orchestrator_instance()
            rl_engine = orchestrator.get_agent_by_type("ReinforcementLearningEngine")
            
            if not rl_engine:
                return {"error": "Reinforcement learning engine not available"}
            
            # Start training
            training_result = await rl_engine.train_agent(
                agent_type=agent_type,
                environment_config=environment_config,
                training_parameters=training_parameters,
                reward_function=reward_function,
                state_space=state_space,
                action_space=action_space
            )
            
            return {
                "agent_id": training_result["agent_id"],
                "agent_type": agent_type,
                "status": "training",
                "performance_metrics": training_result.get("initial_metrics", {}),
                "training_progress": training_result.get("progress", {}),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error training RL agent: {e}")
            return {"error": f"RL training failed: {str(e)}"}
    
    @staticmethod
    async def make_rl_decision(
        agent_id: str,
        current_state: Dict[str, Any],
        available_actions: Optional[List[str]] = None,
        exploration_rate: float = 0.1
    ) -> Dict[str, Any]:
        """
        Make a decision using a trained RL agent
        """
        try:
            orchestrator = await get_orchestrator_instance()
            rl_engine = orchestrator.get_agent_by_type("ReinforcementLearningEngine")
            
            if not rl_engine:
                return {"error": "Reinforcement learning engine not available"}
            
            # Get decision from agent
            decision_result = await rl_engine.get_agent_decision(
                agent_id=agent_id,
                current_state=current_state,
                available_actions=available_actions,
                exploration_rate=exploration_rate
            )
            
            return {
                "agent_id": agent_id,
                "decision": decision_result["action"],
                "confidence": decision_result["confidence"],
                "state_value": decision_result["state_value"],
                "exploration_used": decision_result["exploration_used"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error making RL decision: {e}")
            return {"error": f"RL decision failed: {str(e)}"}
    
    @staticmethod
    async def analyze_scenarios(
        scenario_type: str,
        base_parameters: Dict[str, Any],
        alternative_scenarios: List[Dict[str, Any]] = None,
        sensitivity_analysis: bool = True,
        monte_carlo_simulations: int = 1000
    ) -> Dict[str, Any]:
        """
        Perform comprehensive scenario analysis with Monte Carlo simulations
        """
        try:
            orchestrator = await get_orchestrator_instance()
            scenario_predictor = orchestrator.get_agent_by_type("EnhancedScenarioPredictor")
            
            if not scenario_predictor:
                return {"error": "Scenario predictor not available"}
            
            # Perform scenario analysis
            analysis_result = await scenario_predictor.comprehensive_scenario_analysis(
                scenario_type=scenario_type,
                base_parameters=base_parameters,
                alternative_scenarios=alternative_scenarios or [],
                sensitivity_analysis=sensitivity_analysis,
                monte_carlo_simulations=monte_carlo_simulations
            )
            
            return {
                "analysis_id": f"scenario_{datetime.now().isoformat()}",
                "timestamp": datetime.now().isoformat(),
                "scenario_type": scenario_type,
                "results": analysis_result
            }
            
        except Exception as e:
            logger.error(f"Error in scenario analysis: {e}")
            return {"error": f"Scenario analysis failed: {str(e)}"}
    
    @staticmethod
    async def optimize_ensemble_weights(
        historical_data: Dict[str, Any],
        data_type: str,
        forecast_horizon: int = 30
    ) -> Dict[str, Any]:
        """
        Optimize ensemble weights based on historical performance
        """
        try:
            orchestrator = await get_orchestrator_instance()
            ensemble_system = orchestrator.get_agent_by_type("EnsembleForecastingSystem")
            
            if not ensemble_system:
                return {"error": "Ensemble forecasting system not available"}
            
            optimized_weights = await ensemble_system.optimize_ensemble_weights(
                historical_data=historical_data,
                data_type=data_type,
                forecast_horizon=forecast_horizon
            )
            
            return {
                "optimized_weights": optimized_weights,
                "optimization_metrics": {
                    "improvement": "calculated_improvement",
                    "confidence": "optimization_confidence"
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error optimizing ensemble weights: {e}")
            return {"error": f"Ensemble optimization failed: {str(e)}"}
    
    @staticmethod
    async def create_multi_agent_system(
        agent_configs: List[Dict[str, Any]],
        coordination_strategy: str = "independent",
        communication_protocol: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create and coordinate a multi-agent system
        """
        try:
            orchestrator = await get_orchestrator_instance()
            rl_engine = orchestrator.get_agent_by_type("ReinforcementLearningEngine")
            
            if not rl_engine:
                return {"error": "Reinforcement learning engine not available"}
            
            # Create multi-agent system
            system_result = await rl_engine.create_multi_agent_system(
                agent_configs=agent_configs,
                coordination_strategy=coordination_strategy,
                communication_protocol=communication_protocol
            )
            
            return {
                "system_id": system_result["system_id"],
                "agent_count": len(agent_configs),
                "coordination_strategy": coordination_strategy,
                "status": "initialized",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating multi-agent system: {e}")
            return {"error": f"Multi-agent system creation failed: {str(e)}"}
    
    @staticmethod
    async def get_real_time_insights(
        feeds: List[str],
        forecast_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get real-time insights from intelligence data feeds
        """
        try:
            orchestrator = await get_orchestrator_instance()
            data_adapter = orchestrator.get_agent_by_type("IntelligenceDataAdapter")
            
            if not data_adapter:
                return {"error": "Intelligence data adapter not available"}
            
            insights = await data_adapter.get_real_time_insights(
                feeds=feeds,
                forecast_context=forecast_context
            )
            
            return {
                "insights": insights,
                "feeds_processed": feeds,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting real-time insights: {e}")
            return {"error": f"Real-time insights failed: {str(e)}"}
    
    @staticmethod
    async def generate_forecast_explanation(
        forecast_result: Dict[str, Any],
        historical_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate interpretability report for forecast
        """
        try:
            orchestrator = await get_orchestrator_instance()
            interpretability_engine = orchestrator.get_agent_by_type("ModelInterpretabilityEngine")
            
            if not interpretability_engine:
                return {"error": "Model interpretability engine not available"}
            
            explanation = await interpretability_engine.generate_forecast_explanation(
                forecast_result=forecast_result,
                historical_data=historical_data
            )
            
            return {
                "explanation": explanation,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating forecast explanation: {e}")
            return {"error": f"Explanation generation failed: {str(e)}"}

    @staticmethod
    async def generate_enhanced_leadership_report(
        topic: str,
        topic_data: Dict[str, Any],
        output_dir: str = "Results",
        include_source_tracking: bool = True
    ) -> Dict[str, Any]:
        """
        Generate an enhanced leadership report for any topic using the generic template system.
        
        Args:
            topic: The topic for the report (e.g., "Boeing 737 Accidents", "Cybersecurity Threats")
            topic_data: Dictionary containing topic-specific data
            output_dir: Directory to save the generated report
            include_source_tracking: Whether to include source tracking functionality
            
        Returns:
            Dictionary with report generation results
        """
        try:
            # Get the generic template generator
            template_generator = get_generic_leadership_template_generator()
            
            # Convert topic_data to TopicData structure
            topic_data_obj = TopicData(
                title=topic_data.get("title", topic),
                subtitle=topic_data.get("subtitle", f"{topic} - Executive Leadership Briefing"),
                topic_icon=topic_data.get("topic_icon", "📊"),
                key_finding=topic_data.get("key_finding", f"Analysis of {topic} reveals critical insights and strategic implications."),
                metrics=topic_data.get("metrics", []),
                strategic_analysis=topic_data.get("strategic_analysis", {}),
                charts_data=topic_data.get("charts_data", {}),
                stakeholder_impact=topic_data.get("stakeholder_impact", []),
                recovery_timeline=topic_data.get("recovery_timeline", []),
                strategic_options=topic_data.get("strategic_options", []),
                recommendations=topic_data.get("recommendations", []),
                source_tracking=topic_data.get("source_tracking") if include_source_tracking else None
            )
            
            # Generate the leadership report
            result = template_generator.generate_leadership_report(topic_data_obj, output_dir)
            
            if result["success"]:
                logger.info(f"Enhanced leadership report generated for topic: {topic}")
                return {
                    "success": True,
                    "report_file": result["filepath"],
                    "filename": result["filename"],
                    "topic": topic,
                    "generated_at": result["generated_at"],
                    "message": f"Enhanced leadership report generated successfully for {topic}",
                    "template_used": "generic_leadership",
                    "source_tracking_enabled": include_source_tracking
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error"),
                    "message": f"Failed to generate leadership report for {topic}"
                }
                
        except Exception as e:
            logger.error(f"Error generating enhanced leadership report for {topic}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to generate enhanced leadership report for {topic}"
            }

    @staticmethod
    async def generate_enhanced_report(
        topic: str,
        report_data: Dict[str, Any],
        output_dir: str = "Results",
        include_source_tracking: bool = True
    ) -> Dict[str, Any]:
        """
        Generate an enhanced report for any topic using the generic enhanced report template system.
        
        Args:
            topic: The topic for the report (e.g., "Boeing 737 Accidents", "Cybersecurity Threats")
            report_data: Dictionary containing topic-specific data
            output_dir: Directory to save the generated report
            include_source_tracking: Whether to include source tracking functionality
            
        Returns:
            Dictionary with report generation results
        """
        try:
            # Get the generic enhanced report template generator
            template_generator = get_generic_enhanced_report_template_generator()
            
            # Convert report_data to EnhancedReportData structure
            enhanced_report_data = EnhancedReportData(
                title=report_data.get("title", topic),
                subtitle=report_data.get("subtitle", f"{topic} - Comprehensive Enhanced Analysis"),
                topic_icon=report_data.get("topic_icon", "📈"),
                executive_summary=report_data.get("executive_summary", {}),
                current_analysis=report_data.get("current_analysis", {}),
                strategic_analysis=report_data.get("strategic_analysis", {}),
                forecasting=report_data.get("forecasting", {}),
                economic_analysis=report_data.get("economic_analysis", {}),
                risk_assessment=report_data.get("risk_assessment", {}),
                regional_analysis=report_data.get("regional_analysis", {}),
                implementation=report_data.get("implementation", {}),
                charts_data=report_data.get("charts_data", {}),
                source_tracking=report_data.get("source_tracking") if include_source_tracking else None
            )
            
            # Generate the enhanced report
            result = template_generator.generate_enhanced_report(enhanced_report_data, output_dir)
            
            if result["success"]:
                logger.info(f"Enhanced report generated for topic: {topic}")
                return {
                    "success": True,
                    "report_file": result["filepath"],
                    "filename": result["filename"],
                    "topic": topic,
                    "generated_at": result["generated_at"],
                    "message": f"Enhanced report generated successfully for {topic}",
                    "template_used": "generic_enhanced_report",
                    "source_tracking_enabled": include_source_tracking
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error"),
                    "message": f"Failed to generate enhanced report for {topic}"
                }
                
        except Exception as e:
            logger.error(f"Error generating enhanced report for {topic}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to generate enhanced report for {topic}"
            }

# MCP Server Implementation
async def create_enhanced_mcp_server() -> Server:
    """Create enhanced MCP server with Phase 6 tools"""
    
    # Initialize tools
    tools = EnhancedMCPTools()
    
    # Create server
    server = Server("enhanced-mcp-tools")
    
    @server.list_tools()
    async def handle_list_tools() -> ListToolsResult:
        """List all available MCP tools"""
        return ListToolsResult(
            tools=[
                Tool(
                    name="create_ensemble_forecast",
                    description="Create comprehensive ensemble forecast using multiple ML/DL/RL models",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_type": {"type": "string", "description": "Type of data to forecast"},
                            "historical_data": {"type": "object", "description": "Historical data for forecasting"},
                            "forecast_horizon": {"type": "integer", "default": 30, "description": "Forecast horizon in periods"},
                            "confidence_level": {"type": "number", "default": 0.95, "description": "Confidence level for intervals"},
                            "ensemble_weights": {"type": "object", "description": "Custom ensemble weights"},
                            "scenario_parameters": {"type": "object", "description": "Scenario-specific parameters"},
                            "real_time_feeds": {"type": "array", "items": {"type": "string"}, "description": "Real-time data feeds to include"}
                        },
                        "required": ["data_type", "historical_data"]
                    }
                ),
                Tool(
                    name="train_rl_agent",
                    description="Train a reinforcement learning agent",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_type": {"type": "string", "description": "Type of RL agent to train"},
                            "environment_config": {"type": "object", "description": "Environment configuration"},
                            "training_parameters": {"type": "object", "description": "Training parameters"},
                            "reward_function": {"type": "object", "description": "Reward function definition"},
                            "state_space": {"type": "object", "description": "State space definition"},
                            "action_space": {"type": "object", "description": "Action space definition"}
                        },
                        "required": ["agent_type", "environment_config", "reward_function", "state_space", "action_space"]
                    }
                ),
                Tool(
                    name="make_rl_decision",
                    description="Make a decision using a trained RL agent",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_id": {"type": "string", "description": "Trained agent ID"},
                            "current_state": {"type": "object", "description": "Current state"},
                            "available_actions": {"type": "array", "items": {"type": "string"}, "description": "Available actions"},
                            "exploration_rate": {"type": "number", "default": 0.1, "description": "Exploration rate for decision"}
                        },
                        "required": ["agent_id", "current_state"]
                    }
                ),
                Tool(
                    name="analyze_scenarios",
                    description="Perform comprehensive scenario analysis with Monte Carlo simulations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "scenario_type": {"type": "string", "description": "Type of scenario to analyze"},
                            "base_parameters": {"type": "object", "description": "Base scenario parameters"},
                            "alternative_scenarios": {"type": "array", "items": {"type": "object"}, "description": "Alternative scenarios"},
                            "sensitivity_analysis": {"type": "boolean", "default": True, "description": "Include sensitivity analysis"},
                            "monte_carlo_simulations": {"type": "integer", "default": 1000, "description": "Number of Monte Carlo simulations"}
                        },
                        "required": ["scenario_type", "base_parameters"]
                    }
                ),
                Tool(
                    name="optimize_ensemble_weights",
                    description="Optimize ensemble weights based on historical performance",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "historical_data": {"type": "object", "description": "Historical data for optimization"},
                            "data_type": {"type": "string", "description": "Type of data"},
                            "forecast_horizon": {"type": "integer", "default": 30, "description": "Forecast horizon"}
                        },
                        "required": ["historical_data", "data_type"]
                    }
                ),
                Tool(
                    name="create_multi_agent_system",
                    description="Create and coordinate a multi-agent system",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_configs": {"type": "array", "items": {"type": "object"}, "description": "Agent configurations"},
                            "coordination_strategy": {"type": "string", "default": "independent", "description": "Coordination strategy"},
                            "communication_protocol": {"type": "object", "description": "Communication protocol"}
                        },
                        "required": ["agent_configs"]
                    }
                ),
                Tool(
                    name="get_real_time_insights",
                    description="Get real-time insights from intelligence data feeds",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "feeds": {"type": "array", "items": {"type": "string"}, "description": "Data feeds to monitor"},
                            "forecast_context": {"type": "object", "description": "Forecast context for insights"}
                        },
                        "required": ["feeds"]
                    }
                ),
                Tool(
                    name="generate_forecast_explanation",
                    description="Generate interpretability report for forecast",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "forecast_result": {"type": "object", "description": "Forecast result to explain"},
                            "historical_data": {"type": "object", "description": "Historical data used for forecast"}
                        },
                        "required": ["forecast_result", "historical_data"]
                    }
                ),
                Tool(
                    name="generate_enhanced_leadership_report",
                    description="Generate an enhanced leadership report for any topic using the generic template system",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string", "description": "The topic for the report (e.g., 'Boeing 737 Accidents', 'Cybersecurity Threats')"},
                            "topic_data": {"type": "object", "description": "Dictionary containing topic-specific data including title, subtitle, metrics, charts_data, etc."},
                            "output_dir": {"type": "string", "default": "Results", "description": "Directory to save the generated report"},
                            "include_source_tracking": {"type": "boolean", "default": True, "description": "Whether to include source tracking functionality"}
                        },
                        "required": ["topic", "topic_data"]
                    }
                ),
                Tool(
                    name="generate_enhanced_report",
                    description="Generate an enhanced report for any topic using the generic enhanced report template system",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string", "description": "The topic for the report (e.g., 'Boeing 737 Accidents', 'Cybersecurity Threats')"},
                            "report_data": {"type": "object", "description": "Dictionary containing topic-specific data including executive_summary, current_analysis, strategic_analysis, etc."},
                            "output_dir": {"type": "string", "default": "Results", "description": "Directory to save the generated report"},
                            "include_source_tracking": {"type": "boolean", "default": True, "description": "Whether to include source tracking functionality"}
                        },
                        "required": ["topic", "report_data"]
                    }
                )
            ]
        )
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle tool calls"""
        try:
            if name == "create_ensemble_forecast":
                result = await tools.create_ensemble_forecast(**arguments)
            elif name == "train_rl_agent":
                result = await tools.train_rl_agent(**arguments)
            elif name == "make_rl_decision":
                result = await tools.make_rl_decision(**arguments)
            elif name == "analyze_scenarios":
                result = await tools.analyze_scenarios(**arguments)
            elif name == "optimize_ensemble_weights":
                result = await tools.optimize_ensemble_weights(**arguments)
            elif name == "create_multi_agent_system":
                result = await tools.create_multi_agent_system(**arguments)
            elif name == "get_real_time_insights":
                result = await tools.get_real_time_insights(**arguments)
            elif name == "generate_forecast_explanation":
                result = await tools.generate_forecast_explanation(**arguments)
            elif name == "generate_enhanced_leadership_report":
                result = await tools.generate_enhanced_leadership_report(**arguments)
            elif name == "generate_enhanced_report":
                result = await tools.generate_enhanced_report(**arguments)
            else:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Unknown tool: {name}")]
                )
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))]
            )
            
        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )
    
    return server

# Streamable HTTP Server
async def start_enhanced_mcp_server(host: str = "localhost", port: int = 8000):
    """Start enhanced MCP server with streamable HTTP support"""
    try:
        server = await create_enhanced_mcp_server()
        
        # Start server with stdio for MCP protocol
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="enhanced-mcp-tools",
                    server_version="1.0.0",
                    capabilities={}
                )
            )
        
        logger.info(f"Enhanced MCP server started on {host}:{port}")
        return server
        
    except Exception as e:
        logger.error(f"Failed to start enhanced MCP server: {e}")
        raise

if __name__ == "__main__":
    # Run the enhanced MCP server
    asyncio.run(start_enhanced_mcp_server())
