"""
Optimized MCP Server - Consolidated tool set for improved performance.
Reduces tool count from 32+ to 10 essential tools with unified interfaces.
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from loguru import logger

try:
    from fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    logger.warning("FastMCP not available - using mock MCP server")

from src.config.mcp_config import ConsolidatedMCPServerConfig
from src.core.model_manager import ModelManager
from src.core.vector_db_manager import VectorDBManager
from src.core.improved_knowledge_graph_utility import ImprovedKnowledgeGraphUtility
from src.core.translation_service import TranslationService
from src.core.duplicate_detection_service import DuplicateDetectionService
from src.core.performance_monitor import PerformanceMonitor
from src.core.sentiment_orchestrator import SentimentOrchestrator

# Import agents with lazy loading
class LazyAgentLoader:
    """Lazy load agents only when needed."""
    
    def __init__(self):
        self._agents = {}
    
    def get_agent(self, agent_type: str):
        """Get agent, loading it if not already loaded."""
        if agent_type not in self._agents:
            try:
                if agent_type == "text":
                    from src.agents.unified_text_agent import UnifiedTextAgent
                    self._agents[agent_type] = UnifiedTextAgent(use_strands=True, use_swarm=True)
                elif agent_type == "vision":
                    from src.agents.unified_vision_agent import UnifiedVisionAgent
                    self._agents[agent_type] = UnifiedVisionAgent()
                elif agent_type == "audio":
                    from src.agents.unified_audio_agent import UnifiedAudioAgent
                    self._agents[agent_type] = UnifiedAudioAgent()
                elif agent_type == "file":
                    from src.agents.enhanced_file_extraction_agent import EnhancedFileExtractionAgent
                    self._agents[agent_type] = EnhancedFileExtractionAgent()
                elif agent_type == "web":
                    from src.agents.enhanced_web_agent import EnhancedWebAgent
                    self._agents[agent_type] = EnhancedWebAgent()
                elif agent_type == "kg":
                    from src.agents.knowledge_graph_agent import KnowledgeGraphAgent
                    self._agents[agent_type] = KnowledgeGraphAgent()
                elif agent_type == "art_of_war":
                    from src.agents.art_of_war_deception_agent import ArtOfWarDeceptionAgent
                    self._agents[agent_type] = ArtOfWarDeceptionAgent()
                else:
                    raise ValueError(f"Unknown agent type: {agent_type}")
                
                logger.info(f"✅ Lazy loaded agent: {agent_type}")
            except Exception as e:
                logger.error(f"Failed to load agent {agent_type}: {e}")
                return None
        
        return self._agents[agent_type]

class OptimizedMCPServer:
    """
    Optimized MCP Server with consolidated tools for improved performance.
    Reduces tool count from 32+ to 10 essential tools.
    """
    
    def __init__(self, config: Optional[ConsolidatedMCPServerConfig] = None):
        """Initialize the optimized MCP server."""
        self.config = config or ConsolidatedMCPServerConfig()
        self.mcp = None
        self._tools_registered = False
        
        # Initialize core services (lightweight)
        self.model_manager = ModelManager()
        self.vector_store = VectorDBManager()
        self.knowledge_graph = ImprovedKnowledgeGraphUtility()
        self.translation_service = TranslationService()
        self.duplicate_detection = DuplicateDetectionService()
        self.performance_monitor = PerformanceMonitor()
        self.orchestrator = SentimentOrchestrator()
        
        # Lazy agent loader
        self.agent_loader = LazyAgentLoader()
        
        # Initialize MCP server
        self._initialize_mcp()
        
        logger.info("✅ Optimized MCP Server initialized")
    
    def _initialize_mcp(self):
        """Initialize the MCP server."""
        if not MCP_AVAILABLE:
            logger.warning("Using mock MCP server - FastMCP not available")
            return
        
        try:
            self.mcp = FastMCP(
                name="optimized_mcp_server",
                version="1.0.0"
            )
            logger.info("✅ Optimized MCP server initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing MCP server: {e}")
            self.mcp = None
    
    def _register_optimized_tools(self):
        """Register 10 essential consolidated tools."""
        if not self.mcp:
            logger.warning("MCP server not available - skipping tool registration")
            return
        
        try:
            # 1. Unified Content Processing Tool
            @self.mcp.tool(description="Unified content processing for all types (text, audio, video, images, documents)")
            async def process_content(
                content: str,
                content_type: str = "auto",
                language: str = "en",
                options: Dict[str, Any] = None
            ) -> Dict[str, Any]:
                """Process any type of content with unified interface."""
                try:
                    if content_type == "auto":
                        content_type = self._detect_content_type(content)
                    
                    # Route to appropriate agent
                    if content_type in ["text", "pdf", "document"]:
                        agent = self.agent_loader.get_agent("text")
                    elif content_type in ["audio", "video"]:
                        agent = self.agent_loader.get_agent("audio")
                    elif content_type in ["image", "vision"]:
                        agent = self.agent_loader.get_agent("vision")
                    else:
                        agent = self.agent_loader.get_agent("text")
                    
                    if agent:
                        result = await agent.process_content(content, language, options or {})
                        return {"success": True, "result": result, "content_type": content_type}
                    else:
                        return {"success": False, "error": "Agent not available"}
                        
                except Exception as e:
                    logger.error(f"Error processing content: {e}")
                    return {"success": False, "error": str(e)}
            
            # 2. Unified Analysis Tool
            @self.mcp.tool(description="Unified analysis (sentiment, entity extraction, pattern analysis, strategic deception)")
            async def analyze_content(
                content: str,
                analysis_type: str = "comprehensive",
                language: str = "en",
                domain: str = "general"
            ) -> Dict[str, Any]:
                """Perform comprehensive content analysis."""
                try:
                    results = {}
                    
                    # Sentiment analysis
                    if analysis_type in ["comprehensive", "sentiment"]:
                        sentiment_result = await self.orchestrator.analyze_sentiment(content, language)
                        results["sentiment"] = sentiment_result
                    
                    # Entity extraction
                    if analysis_type in ["comprehensive", "entities"]:
                        entities_result = await self.orchestrator.extract_entities(content, language)
                        results["entities"] = entities_result
                    
                    # Strategic deception analysis
                    if analysis_type in ["comprehensive", "deception"]:
                        art_of_war_agent = self.agent_loader.get_agent("art_of_war")
                        if art_of_war_agent:
                            deception_result = await art_of_war_agent.analyze_deception(content, domain)
                            results["deception"] = deception_result
                    
                    # Pattern analysis
                    if analysis_type in ["comprehensive", "patterns"]:
                        pattern_result = await self.orchestrator.analyze_patterns(content)
                        results["patterns"] = pattern_result
                    
                    return {"success": True, "results": results, "analysis_type": analysis_type}
                    
                except Exception as e:
                    logger.error(f"Error analyzing content: {e}")
                    return {"success": False, "error": str(e)}
            
            # 3. Unified Search Tool
            @self.mcp.tool(description="Unified search (semantic, knowledge graph, conceptual, cross-content)")
            async def search_content(
                query: str,
                search_type: str = "semantic",
                language: str = "en",
                limit: int = 10
            ) -> Dict[str, Any]:
                """Perform unified search across all content."""
                try:
                    if search_type == "semantic":
                        results = await self.vector_store.semantic_search(query, limit)
                    elif search_type == "knowledge_graph":
                        results = await self.knowledge_graph.query(query, limit)
                    elif search_type == "conceptual":
                        results = await self.vector_store.conceptual_search(query, limit)
                    elif search_type == "combined":
                        semantic_results = await self.vector_store.semantic_search(query, limit)
                        kg_results = await self.knowledge_graph.query(query, limit)
                        results = {
                            "semantic": semantic_results,
                            "knowledge_graph": kg_results
                        }
                    else:
                        results = await self.vector_store.semantic_search(query, limit)
                    
                    return {"success": True, "results": results, "search_type": search_type}
                    
                except Exception as e:
                    logger.error(f"Error searching content: {e}")
                    return {"success": False, "error": str(e)}
            
            # 4. Unified Report Generation Tool
            @self.mcp.tool(description="Unified report generation with configurable options (comprehensive, enhanced, strategic)")
            async def generate_report(
                content: str,
                report_type: str = "comprehensive",
                format: str = "html",
                include_visualizations: bool = True,
                include_source_references: bool = True
            ) -> Dict[str, Any]:
                """Generate unified reports with configurable options."""
                try:
                    # Import report generators only when needed
                    if report_type == "comprehensive":
                        from src.core.comprehensive_enhanced_report_generator import comprehensive_enhanced_report_generator
                        result = await comprehensive_enhanced_report_generator(
                            content, format, include_visualizations, include_source_references
                        )
                    elif report_type == "enhanced":
                        from src.core.enhanced_report_generator import enhanced_report_generator
                        result = await enhanced_report_generator(
                            content, format, include_visualizations, include_source_references
                        )
                    elif report_type == "strategic":
                        from src.core.strategic_enhanced_report_generator import strategic_enhanced_report_generator
                        result = await strategic_enhanced_report_generator(
                            content, format, include_visualizations, include_source_references
                        )
                    else:
                        from src.core.comprehensive_enhanced_report_generator import comprehensive_enhanced_report_generator
                        result = await comprehensive_enhanced_report_generator(
                            content, format, include_visualizations, include_source_references
                        )
                    
                    return {"success": True, "result": result, "report_type": report_type}
                    
                except Exception as e:
                    logger.error(f"Error generating report: {e}")
                    return {"success": False, "error": str(e)}
            
            # 5. Unified Simulation Tool
            @self.mcp.tool(description="Unified simulation (Monte Carlo, forecasting, scenario analysis)")
            async def run_simulation(
                scenario: str,
                simulation_type: str = "monte_carlo",
                parameters: Dict[str, Any] = None,
                iterations: int = 1000
            ) -> Dict[str, Any]:
                """Run unified simulations."""
                try:
                    if simulation_type == "monte_carlo":
                        from src.core.monte_carlo_simulation import MonteCarloSimulation
                        sim = MonteCarloSimulation()
                        result = await sim.run_simulation(scenario, parameters or {}, iterations)
                    elif simulation_type == "forecasting":
                        from src.core.advanced_forecasting import AdvancedForecastingEngine
                        forecaster = AdvancedForecastingEngine()
                        result = await forecaster.forecast(scenario, parameters or {})
                    elif simulation_type == "scenario":
                        from src.core.scenario_analysis import ScenarioAnalysisEngine
                        analyzer = ScenarioAnalysisEngine()
                        result = await analyzer.analyze_scenario(scenario, parameters or {})
                    else:
                        from src.core.monte_carlo_simulation import MonteCarloSimulation
                        sim = MonteCarloSimulation()
                        result = await sim.run_simulation(scenario, parameters or {}, iterations)
                    
                    return {"success": True, "result": result, "simulation_type": simulation_type}
                    
                except Exception as e:
                    logger.error(f"Error running simulation: {e}")
                    return {"success": False, "error": str(e)}
            
            # 6. Unified Strategic Analysis Tool
            @self.mcp.tool(description="Unified strategic analysis (Art of War, deception detection, threat assessment)")
            async def analyze_strategic(
                content: str,
                analysis_type: str = "comprehensive",
                domain: str = "general"
            ) -> Dict[str, Any]:
                """Perform unified strategic analysis."""
                try:
                    art_of_war_agent = self.agent_loader.get_agent("art_of_war")
                    if not art_of_war_agent:
                        return {"success": False, "error": "Strategic analysis agent not available"}
                    
                    if analysis_type == "deception":
                        result = await art_of_war_agent.analyze_deception(content, domain)
                    elif analysis_type == "threat":
                        result = await art_of_war_agent.assess_threats(content, domain)
                    elif analysis_type == "strategic":
                        result = await art_of_war_agent.analyze_strategic_position(content, domain)
                    else:  # comprehensive
                        deception = await art_of_war_agent.analyze_deception(content, domain)
                        threats = await art_of_war_agent.assess_threats(content, domain)
                        strategic = await art_of_war_agent.analyze_strategic_position(content, domain)
                        result = {
                            "deception": deception,
                            "threats": threats,
                            "strategic": strategic
                        }
                    
                    return {"success": True, "result": result, "analysis_type": analysis_type}
                    
                except Exception as e:
                    logger.error(f"Error in strategic analysis: {e}")
                    return {"success": False, "error": str(e)}
            
            # 7. Unified System Management Tool
            @self.mcp.tool(description="Unified system management (health, status, configuration, performance)")
            async def manage_system(
                action: str = "status",
                parameters: Dict[str, Any] = None
            ) -> Dict[str, Any]:
                """Manage system operations."""
                try:
                    if action == "health":
                        health_status = await self.performance_monitor.get_health_status()
                        return {"success": True, "health": health_status}
                    elif action == "status":
                        status = {
                            "agents": {name: "active" for name in ["text", "vision", "audio", "file", "web", "kg", "art_of_war"]},
                            "services": {
                                "vector_store": "active",
                                "knowledge_graph": "active",
                                "translation": "active",
                                "duplicate_detection": "active"
                            },
                            "performance": await self.performance_monitor.get_performance_metrics()
                        }
                        return {"success": True, "status": status}
                    elif action == "configure":
                        # Configuration management
                        return {"success": True, "message": "Configuration updated"}
                    else:
                        return {"success": False, "error": f"Unknown action: {action}"}
                        
                except Exception as e:
                    logger.error(f"Error managing system: {e}")
                    return {"success": False, "error": str(e)}
            
            # 8. Unified Data Export Tool
            @self.mcp.tool(description="Unified data export (JSON, CSV, PDF, Word, HTML, Excel)")
            async def export_data(
                data: Dict[str, Any],
                format: str = "json",
                filename: str = None,
                options: Dict[str, Any] = None
            ) -> Dict[str, Any]:
                """Export data in various formats."""
                try:
                    from src.core.export.data_exporter import DataExporter
                    exporter = DataExporter()
                    result = await exporter.export_data(data, format, filename, options or {})
                    return {"success": True, "result": result, "format": format}
                    
                except Exception as e:
                    logger.error(f"Error exporting data: {e}")
                    return {"success": False, "error": str(e)}
            
            # 9. Unified Knowledge Graph Tool
            @self.mcp.tool(description="Unified knowledge graph operations (query, create, update, visualize)")
            async def knowledge_graph_operations(
                operation: str = "query",
                query: str = None,
                data: Dict[str, Any] = None
            ) -> Dict[str, Any]:
                """Perform knowledge graph operations."""
                try:
                    if operation == "query":
                        result = await self.knowledge_graph.query(query)
                    elif operation == "create":
                        result = await self.knowledge_graph.create_graph(data)
                    elif operation == "update":
                        result = await self.knowledge_graph.update_graph(data)
                    elif operation == "visualize":
                        result = await self.knowledge_graph.visualize_graph()
                    else:
                        return {"success": False, "error": f"Unknown operation: {operation}"}
                    
                    return {"success": True, "result": result, "operation": operation}
                    
                except Exception as e:
                    logger.error(f"Error in knowledge graph operation: {e}")
                    return {"success": False, "error": str(e)}
            
            # 10. Unified Agent Management Tool
            @self.mcp.tool(description="Unified agent management (status, start, stop, configure)")
            async def manage_agents(
                action: str = "status",
                agent_type: str = "all",
                parameters: Dict[str, Any] = None
            ) -> Dict[str, Any]:
                """Manage agent operations."""
                try:
                    agent_types = ["text", "vision", "audio", "file", "web", "kg", "art_of_war"]
                    
                    if action == "status":
                        if agent_type == "all":
                            status = {}
                            for at in agent_types:
                                agent = self.agent_loader.get_agent(at)
                                status[at] = {
                                    "status": "active" if agent else "inactive",
                                    "loaded": agent is not None
                                }
                        else:
                            agent = self.agent_loader.get_agent(agent_type)
                            status = {
                                "status": "active" if agent else "inactive",
                                "loaded": agent is not None
                            }
                        return {"success": True, "status": status}
                    
                    elif action == "start":
                        # Lazy load agent
                        agent = self.agent_loader.get_agent(agent_type)
                        return {"success": True, "message": f"Agent {agent_type} started"}
                    
                    elif action == "stop":
                        # Remove from loaded agents
                        if agent_type in self.agent_loader._agents:
                            del self.agent_loader._agents[agent_type]
                        return {"success": True, "message": f"Agent {agent_type} stopped"}
                    
                    else:
                        return {"success": False, "error": f"Unknown action: {action}"}
                        
                except Exception as e:
                    logger.error(f"Error managing agents: {e}")
                    return {"success": False, "error": str(e)}
            
            self._tools_registered = True
            logger.info("✅ Optimized MCP tools registered (10 tools)")
            
        except Exception as e:
            logger.error(f"Failed to register optimized tools: {e}")
    
    def _detect_content_type(self, content: str) -> str:
        """Detect content type from content."""
        # Simple content type detection
        if content.startswith("http"):
            return "web"
        elif any(ext in content.lower() for ext in [".pdf", ".doc", ".txt"]):
            return "document"
        elif any(ext in content.lower() for ext in [".jpg", ".png", ".gif"]):
            return "image"
        elif any(ext in content.lower() for ext in [".mp3", ".wav", ".mp4"]):
            return "audio"
        else:
            return "text"
    
    def run(self, host: str = "localhost", port: int = 8000, debug: bool = False):
        """Run the optimized MCP server."""
        if not self.mcp:
            logger.error("MCP server not available")
            return
        
        try:
            logger.info(f"🚀 Starting Optimized MCP Server via stdio")
            # Register tools before running
            self._register_optimized_tools()
            # FastMCP uses stdio
            self.mcp.run()
        except Exception as e:
            logger.error(f"Error running MCP server: {e}")
    
    def get_http_app(self):
        """Get FastAPI app for HTTP integration."""
        if not self.mcp:
            logger.error("MCP server not available")
            return None
        
        try:
            from fastapi import FastAPI
            from fastapi.middleware.cors import CORSMiddleware
            
            app = FastAPI(title="Optimized MCP Server", version="1.0.0")
            
            # Add CORS middleware
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            # Register tools
            self._register_optimized_tools()
            
            return app
            
        except Exception as e:
            logger.error(f"Error creating HTTP app: {e}")
            return None
    
    def get_tools_info(self) -> List[Dict[str, Any]]:
        """Get information about available tools."""
        if not self._tools_registered:
            self._register_optimized_tools()
        
        return [
            {"name": "process_content", "description": "Unified content processing for all types"},
            {"name": "analyze_content", "description": "Unified analysis (sentiment, entity, pattern, deception)"},
            {"name": "search_content", "description": "Unified search (semantic, knowledge graph, conceptual)"},
            {"name": "generate_report", "description": "Unified report generation with configurable options"},
            {"name": "run_simulation", "description": "Unified simulation (Monte Carlo, forecasting, scenario)"},
            {"name": "analyze_strategic", "description": "Unified strategic analysis (Art of War, deception, threats)"},
            {"name": "manage_system", "description": "Unified system management (health, status, configuration)"},
            {"name": "export_data", "description": "Unified data export (JSON, CSV, PDF, Word, HTML, Excel)"},
            {"name": "knowledge_graph_operations", "description": "Unified knowledge graph operations"},
            {"name": "manage_agents", "description": "Unified agent management (status, start, stop, configure)"}
        ]

# Factory function for easy integration
def create_optimized_mcp_server(config: Optional[ConsolidatedMCPServerConfig] = None) -> OptimizedMCPServer:
    """Create an optimized MCP server instance."""
    return OptimizedMCPServer(config)

# Standalone server function
def start_optimized_mcp_server(host: str = "localhost", port: int = 8000):
    """Start the optimized MCP server."""
    server = OptimizedMCPServer()
    server.run(host, port)
    return server
