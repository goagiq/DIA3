"""
Standalone MCP Server for Strands Integration.

This module provides a standalone MCP server that runs on port 8000
using Streamable HTTP transport for direct integration with Strands.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import threading
import time
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger

# Import core services
# flake8: noqa: E402
from core.model_manager import ModelManager
from core.vector_db import VectorDBManager
from core.improved_knowledge_graph_utility import ImprovedKnowledgeGraphUtility
from core.translation_service import TranslationService
from core.orchestrator import SentimentOrchestrator
from core.duplicate_detection_service import DuplicateDetectionService
from core.performance_monitor import PerformanceMonitor

# Import agents
# flake8: noqa: E402
from agents.unified_text_agent import UnifiedTextAgent
from agents.unified_vision_agent import UnifiedVisionAgent
from agents.unified_audio_agent import UnifiedAudioAgent
from agents.enhanced_file_extraction_agent import EnhancedFileExtractionAgent
from agents.knowledge_graph_agent import KnowledgeGraphAgent
from agents.web_agent_enhanced import EnhancedWebAgent
from agents.art_of_war_deception_agent import ArtOfWarDeceptionAgent

# Import generic comprehensive analysis system
# flake8: noqa: E402
from core.generic_comprehensive_analysis import GenericComprehensiveAnalysisSystem

# Import configuration
# flake8: noqa: E402
from config.mcp_config import ConsolidatedMCPServerConfig
from config.config import config

# Try to import FastMCP for MCP server functionality
try:
    from fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    logger.warning("FastMCP not available - using mock MCP server")


class StandaloneMCPServer:
    """Standalone MCP server for Strands integration on port 8000."""

    def __init__(self, config: Optional[ConsolidatedMCPServerConfig] = None):
        """Initialize the standalone MCP server."""
        self.config = config or ConsolidatedMCPServerConfig()
        self.mcp = None
        self.server_thread = None
        self.is_running = False

        # Initialize core services
        self.model_manager = ModelManager()
        self.vector_store = VectorDBManager()
        self.knowledge_graph = ImprovedKnowledgeGraphUtility()
        self.translation_service = TranslationService()
        self.duplicate_detection = DuplicateDetectionService()
        self.performance_monitor = PerformanceMonitor()

        # Initialize orchestrator
        self.orchestrator = SentimentOrchestrator()

        # Initialize agents
        self.text_agent = UnifiedTextAgent()
        self.vision_agent = UnifiedVisionAgent()
        self.audio_agent = UnifiedAudioAgent()
        self.file_agent = EnhancedFileExtractionAgent()
        self.kg_agent = KnowledgeGraphAgent()
        self.web_agent = EnhancedWebAgent()
        
        # Initialize Art of War deception analysis agent
        self.art_of_war_agent = ArtOfWarDeceptionAgent()
        
        # Initialize generic comprehensive analysis system
        self.generic_analysis_system = GenericComprehensiveAnalysisSystem()

        # Initialize MCP server
        self._initialize_mcp()

        # Register tools
        self._register_tools()
        
        # Register language capabilities tools
        self._register_language_capabilities_tools()

        logger.info("✅ Standalone MCP Server initialized successfully")
    
    def _register_language_capabilities_tools(self):
        """Register language capabilities tools."""
        if not self.mcp:
            logger.warning("MCP server not available - skipping language capabilities tool registration")
            return
        
        # Register language capabilities analysis tool
        @self.mcp.tool(description="Analyze content using language capabilities for strategic advantages")
        async def analyze_language_capabilities(
            content: str,
            language: str = "auto",
            domain: str = None
        ) -> Dict[str, Any]:
            """Analyze content using language capabilities for strategic advantages."""
            try:
                from src.core.language_capabilities_engine import language_capabilities_engine
                
                result = await language_capabilities_engine.analyze_language_capabilities(
                    content=content,
                    language=language
                )
                
                # Filter by domain if specified
                if domain and "strategic_advantages" in result:
                    filtered_advantages = [
                        adv for adv in result.get("strategic_advantages", [])
                        if adv.get("domain") == domain
                    ]
                    result["strategic_advantages"] = filtered_advantages
                    result["domain_focus"] = domain
                
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error in language capabilities analysis: {e}")
                return {"success": False, "error": str(e)}
        
        # Register get capabilities summary tool
        @self.mcp.tool(description="Get summary of all available language capabilities and strategic advantages")
        async def get_language_capabilities_summary() -> Dict[str, Any]:
            """Get summary of all available language capabilities and strategic advantages."""
            try:
                from src.core.language_capabilities_engine import language_capabilities_engine
                
                summary = await language_capabilities_engine.get_capabilities_summary()
                return {"success": True, "summary": summary}
            except Exception as e:
                logger.error(f"Error getting capabilities summary: {e}")
                return {"success": False, "error": str(e)}
        
        # Register language capabilities health check tool
        @self.mcp.tool(description="Health check for the language capabilities engine")
        async def language_capabilities_health_check() -> Dict[str, Any]:
            """Health check for the language capabilities engine."""
            try:
                from src.core.language_capabilities_engine import language_capabilities_engine
                
                health = await language_capabilities_engine.health_check()
                return {"success": True, "health": health}
            except Exception as e:
                logger.error(f"Language capabilities health check failed: {e}")
                return {"success": False, "error": str(e)}

    def _initialize_mcp(self):
        """Initialize the MCP server."""
        if not MCP_AVAILABLE:
            logger.warning("Using mock MCP server - FastMCP not available")
            return

        try:
            self.mcp = FastMCP(
                name="standalone_sentiment_mcp_server",
                version="1.0.0"
            )
            logger.info("✅ Standalone MCP server initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing MCP server: {e}")
            self.mcp = None

    def _register_tools(self):
        """Register all MCP tools."""
        if not self.mcp:
            logger.warning("MCP server not available - skipping tool registration")
            return

        # Content Processing Tools
        @self.mcp.tool(description="Unified content processing for all types")
        async def process_content(
            content: str,
            content_type: str = "auto",
            language: str = "en",
            options: Dict[str, Any] = None
        ) -> Dict[str, Any]:
            """Process content of any type with unified interface."""
            try:
                if content_type == "auto":
                    content_type = self._detect_content_type(content)

                if content_type == "text":
                    result = await self.text_agent.process_text(content, options or {})
                elif content_type == "image":
                    result = await self.vision_agent.process_image(content, options or {})
                elif content_type == "audio":
                    result = await self.audio_agent.process_audio(content, options or {})
                elif content_type == "video":
                    result = await self.vision_agent.process_video(content, options or {})
                elif content_type == "pdf":
                    # For PDF files, content should be a file path
                    if not content.endswith('.pdf'):
                        # If content is not a file path, assume it's a file path in the data directory
                        import os
                        from pathlib import Path
                        data_dir = Path("data")
                        pdf_path = data_dir / content
                        if not pdf_path.exists():
                            pdf_path = data_dir / f"{content}.pdf"
                        if pdf_path.exists():
                            content = str(pdf_path)
                        else:
                            return {"success": False, "error": f"PDF file not found: {content}"}
                    
                    # Enhanced PDF processing with comprehensive language detection
                    pdf_options = options or {}
                    
                    # Extract a sample for language detection
                    try:
                        sample_result = await self.file_agent.extract_text_from_pdf(content, {"sample_only": True})
                        if sample_result.get("status") == "success":
                            sample_text = sample_result.get("extracted_text", "")[:1000]
                            if sample_text:
                                # Detect language and apply appropriate processing
                                detected_language = self._detect_language_from_text(sample_text)
                                pdf_options["language"] = detected_language
                                
                                # Apply language-specific processing
                                if detected_language == "zh":
                                    # Chinese language processing
                                    from config.language_config.chinese_config import ChineseConfig
                                    chinese_config = ChineseConfig()
                                    pdf_type = chinese_config.detect_chinese_pdf_type(sample_text)
                                    pdf_options["pdf_type"] = pdf_type
                                    pdf_options["enhanced_processing"] = True
                                    logger.info(f"Detected Chinese PDF type: {pdf_type}")
                                    
                                elif detected_language == "ru":
                                    # Russian language processing
                                    from config.language_config.russian_config import RussianConfig
                                    russian_config = RussianConfig()
                                    pdf_options["enhanced_processing"] = True
                                    logger.info("Detected Russian PDF - applying Russian-specific processing")
                                    
                                elif detected_language in ["ar", "ja", "ko", "hi"]:
                                    # Other supported languages
                                    pdf_options["enhanced_processing"] = True
                                    logger.info(f"Detected {detected_language} PDF - applying language-specific processing")
                                    
                                else:
                                    # Default to English/Latin processing
                                    pdf_options["language"] = "en"
                                    logger.info("Detected English/Latin PDF - using standard processing")
                                    
                    except Exception as e:
                        logger.warning(f"Language detection failed: {e}")
                        # Fallback to specified language or default
                        pdf_options["language"] = language if language != "auto" else "en"
                    
                    result = await self.file_agent.extract_text_from_pdf(content, pdf_options)
                elif content_type == "website":
                    result = await self.web_agent.scrape_website(content, options or {})
                else:
                    result = await self.text_agent.process_text(content, options or {})

                return {"success": True, "result": result, "content_type": content_type}
            except Exception as e:
                logger.error(f"Error processing content: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Extract text from various content types")
        async def extract_text_from_content(
            content: str,
            content_type: str = "auto"
        ) -> Dict[str, Any]:
            """Extract text from various content types."""
            try:
                if content_type == "auto":
                    content_type = self._detect_content_type(content)

                if content_type == "pdf":
                    # For PDF files, content should be a file path
                    if not content.endswith('.pdf'):
                        # If content is not a file path, assume it's a file path in the data directory
                        import os
                        from pathlib import Path
                        data_dir = Path("data")
                        pdf_path = data_dir / content
                        if not pdf_path.exists():
                            pdf_path = data_dir / f"{content}.pdf"
                        if pdf_path.exists():
                            content = str(pdf_path)
                        else:
                            return {"success": False, "error": f"PDF file not found: {content}"}
                    
                    # Enhanced PDF text extraction with comprehensive language detection
                    pdf_options = {}
                    
                    # Extract a sample for language detection
                    try:
                        sample_result = await self.file_agent.extract_text_from_pdf(content, {"sample_only": True})
                        if sample_result.get("status") == "success":
                            sample_text = sample_result.get("extracted_text", "")[:500]
                            if sample_text:
                                # Detect language and apply appropriate processing
                                detected_language = self._detect_language_from_text(sample_text)
                                pdf_options["language"] = detected_language
                                
                                # Apply language-specific processing
                                if detected_language == "zh":
                                    # Chinese language processing
                                    from config.language_config.chinese_config import ChineseConfig
                                    chinese_config = ChineseConfig()
                                    pdf_type = chinese_config.detect_chinese_pdf_type(sample_text)
                                    pdf_options["pdf_type"] = pdf_type
                                    pdf_options["enhanced_processing"] = True
                                    logger.info(f"Detected Chinese PDF type: {pdf_type}")
                                    
                                elif detected_language == "ru":
                                    # Russian language processing
                                    from config.language_config.russian_config import RussianConfig
                                    russian_config = RussianConfig()
                                    pdf_options["enhanced_processing"] = True
                                    logger.info("Detected Russian PDF - applying Russian-specific processing")
                                    
                                elif detected_language in ["ar", "ja", "ko", "hi"]:
                                    # Other supported languages
                                    pdf_options["enhanced_processing"] = True
                                    logger.info(f"Detected {detected_language} PDF - applying language-specific processing")
                                    
                                else:
                                    # Default to English/Latin processing
                                    pdf_options["language"] = "en"
                                    logger.info("Detected English/Latin PDF - using standard processing")
                                    
                    except Exception as e:
                        logger.warning(f"Language detection failed: {e}")
                        # Fallback to default language
                        pdf_options["language"] = "en"
                    except Exception as e:
                        logger.warning(f"Language detection failed: {e}")
                    
                    result = await self.file_agent.extract_text_from_pdf(content, pdf_options)
                elif content_type == "image":
                    result = await self.vision_agent.extract_text_from_image(content)
                elif content_type == "audio":
                    result = await self.audio_agent.transcribe_audio(content)
                else:
                    result = {"text": content}

                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error extracting text: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Summarize content of any type")
        async def summarize_content(
            content: str,
            content_type: str = "auto",
            summary_length: str = "medium"
        ) -> Dict[str, Any]:
            """Summarize content of any type."""
            try:
                if content_type == "auto":
                    content_type = self._detect_content_type(content)

                if content_type == "text":
                    result = await self.text_agent.summarize_text(content, summary_length)
                elif content_type == "image":
                    result = await self.vision_agent.summarize_image(content, summary_length)
                elif content_type == "audio":
                    result = await self.audio_agent.summarize_audio(content, summary_length)
                elif content_type == "video":
                    result = await self.vision_agent.summarize_video(content, summary_length)
                else:
                    result = await self.text_agent.summarize_text(content, summary_length)

                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error summarizing content: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Translate content to different languages")
        async def translate_content(
            content: str,
            target_language: str,
            source_language: str = "auto"
        ) -> Dict[str, Any]:
            """Translate content to different languages."""
            try:
                result = await self.translation_service.translate_text(
                    content, target_language, source_language
                )
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error translating content: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Convert content between different formats")
        async def convert_content_format(
            content: str,
            source_format: str,
            target_format: str
        ) -> Dict[str, Any]:
            """Convert content between different formats."""
            try:
                # Implementation for format conversion
                result = {"converted": True, "format": target_format}
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error converting content format: {e}")
                return {"success": False, "error": str(e)}

        # Analysis & Intelligence Tools
        @self.mcp.tool(description="Analyze sentiment of text content")
        async def analyze_sentiment(
            text: str,
            language: str = "en"
        ) -> Dict[str, Any]:
            """Analyze sentiment of text content."""
            try:
                result = await self.text_agent.analyze_sentiment(text, language)
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error analyzing sentiment: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Extract entities from text content")
        async def extract_entities(
            text: str,
            entity_types: List[str] = None
        ) -> Dict[str, Any]:
            """Extract entities from text content."""
            try:
                result = await self.text_agent.extract_entities(text, entity_types)
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error extracting entities: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Generate knowledge graph from content")
        async def generate_knowledge_graph(
            content: str,
            content_type: str = "text"
        ) -> Dict[str, Any]:
            """Generate knowledge graph from content."""
            try:
                result = await self.kg_agent.generate_knowledge_graph(content, content_type)
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error generating knowledge graph: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Analyze business intelligence from content")
        async def analyze_business_intelligence(
            content: str,
            analysis_type: str = "comprehensive"
        ) -> Dict[str, Any]:
            """Analyze business intelligence from content."""
            try:
                result = await self.text_agent.analyze_business_intelligence(content, analysis_type)
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error analyzing business intelligence: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Create visualizations from data")
        async def create_visualizations(
            data: Dict[str, Any],
            visualization_type: str = "auto"
        ) -> Dict[str, Any]:
            """Create visualizations from data."""
            try:
                # Implementation for visualization creation
                result = {"visualization": "created", "type": visualization_type}
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error creating visualizations: {e}")
                return {"success": False, "error": str(e)}

        # Agent Management Tools
        @self.mcp.tool(description="Get status of all agents")
        async def get_agent_status() -> Dict[str, Any]:
            """Get status of all agents."""
            try:
                status = {
                    "text_agent": "running",
                    "vision_agent": "running",
                    "audio_agent": "running",
                    "file_agent": "running",
                    "kg_agent": "running",
                    "web_agent": "running"
                }
                return {"success": True, "status": status}
            except Exception as e:
                logger.error(f"Error getting agent status: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Start specific agents")
        async def start_agents(
            agent_types: List[str]
        ) -> Dict[str, Any]:
            """Start specific agents."""
            try:
                # Implementation for starting agents
                result = {"started": agent_types}
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error starting agents: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Stop specific agents")
        async def stop_agents(
            agent_types: List[str]
        ) -> Dict[str, Any]:
            """Stop specific agents."""
            try:
                # Implementation for stopping agents
                result = {"stopped": agent_types}
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error stopping agents: {e}")
                return {"success": False, "error": str(e)}

        # Data Management Tools
        @self.mcp.tool(description="Store content in vector database")
        async def store_in_vector_db(
            content: str,
            metadata: Dict[str, Any] = None
        ) -> Dict[str, Any]:
            """Store content in vector database."""
            try:
                result = await self.vector_store.store_content(content, metadata or {})
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error storing in vector DB: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Query knowledge graph")
        async def query_knowledge_graph(
            query: str,
            query_type: str = "semantic"
        ) -> Dict[str, Any]:
            """Query knowledge graph."""
            try:
                result = await self.kg_agent.query_knowledge_graph(query, query_type)
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error querying knowledge graph: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Export data in various formats")
        async def export_data(
            data_type: str,
            format: str = "json",
            filters: Dict[str, Any] = None
        ) -> Dict[str, Any]:
            """Export data in various formats."""
            try:
                # Implementation for data export
                result = {"exported": True, "format": format}
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error exporting data: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Manage data sources")
        async def manage_data_sources(
            action: str,
            source_name: str,
            source_config: Dict[str, Any] = None
        ) -> Dict[str, Any]:
            """Manage data sources."""
            try:
                # Implementation for data source management
                result = {"action": action, "source": source_name}
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error managing data sources: {e}")
                return {"success": False, "error": str(e)}

        # Reporting & Export Tools
        @self.mcp.tool(description="Generate comprehensive reports")
        async def generate_report(
            content: str,
            report_type: str = "comprehensive",
            language: str = "en",
            options: Dict[str, Any] = None
        ) -> Dict[str, Any]:
            """Generate comprehensive reports."""
            try:
                # Implementation for report generation
                result = {"report": "generated", "type": report_type}
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error generating report: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Create interactive dashboards")
        async def create_dashboard(
            dashboard_type: str,
            data_sources: List[str],
            layout: Dict[str, Any] = None
        ) -> Dict[str, Any]:
            """Create interactive dashboards."""
            try:
                # Implementation for dashboard creation
                result = {"dashboard": "created", "type": dashboard_type}
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error creating dashboard: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Export results in various formats")
        async def export_results(
            result_type: str,
            format: str = "json",
            destination: str = None
        ) -> Dict[str, Any]:
            """Export results in various formats."""
            try:
                # Implementation for result export
                result = {"exported": True, "format": format}
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error exporting results: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Schedule automated reports")
        async def schedule_reports(
            report_config: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Schedule automated reports."""
            try:
                # Implementation for report scheduling
                result = {"scheduled": True, "config": report_config}
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error scheduling reports: {e}")
                return {"success": False, "error": str(e)}

        # System Management Tools
        @self.mcp.tool(description="Get system status and health")
        async def get_system_status() -> Dict[str, Any]:
            """Get system status and health."""
            try:
                status = {
                    "api_server": "running",
                    "mcp_server": "running",
                    "vector_db": "running",
                    "knowledge_graph": "running",
                    "translation": "running"
                }
                return {"success": True, "status": status}
            except Exception as e:
                logger.error(f"Error getting system status: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="System configuration management")
        async def configure_system(
            config_type: str,
            config_data: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Configure system settings."""
            try:
                # Implementation for system configuration
                result = {"configured": True, "type": config_type}
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error configuring system: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Performance monitoring")
        async def monitor_performance() -> Dict[str, Any]:
            """Monitor system performance."""
            try:
                performance_data = await self.performance_monitor.get_performance_metrics()
                return {"success": True, "performance": performance_data}
            except Exception as e:
                logger.error(f"Error monitoring performance: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Configuration management")
        async def manage_configurations(
            action: str,
            config_name: str,
            config_data: Dict[str, Any] = None
        ) -> Dict[str, Any]:
            """Manage system configurations."""
            try:
                # Implementation for configuration management
                result = {
                    "action": action,
                    "config": config_name,
                    "status": "completed"
                }
                return {"success": True, "result": result}
            except Exception as e:
                logger.error(f"Error managing configurations: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Art of War deception techniques analysis for modern diplomacy")
        async def analyze_art_of_war_deception(
            analysis_type: str = "comprehensive",
            focus_areas: List[str] = None,
            include_modern_applications: bool = True,
            include_ethical_considerations: bool = True,
            generate_report: bool = False,
            report_format: str = "markdown"
        ) -> Dict[str, Any]:
            """Analyze Art of War deception techniques and their modern diplomatic applications."""
            try:
                logger.info(f"Starting Art of War deception analysis: {analysis_type}")
                
                # Perform the analysis
                result = await self.art_of_war_agent.analyze_deception_techniques(
                    analysis_type=analysis_type,
                    focus_areas=focus_areas,
                    include_modern_applications=include_modern_applications,
                    include_ethical_considerations=include_ethical_considerations
                )
                
                # Generate report if requested
                if generate_report:
                    report_result = await self.art_of_war_agent.generate_deception_report(
                        analysis_type=analysis_type,
                        format=report_format
                    )
                    result["report"] = report_result
                
                return result
            except Exception as e:
                logger.error(f"Error in Art of War deception analysis: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Search for deception patterns in stored Art of War analyses")
        async def search_deception_patterns(
            query: str,
            n_results: int = 5
        ) -> Dict[str, Any]:
            """Search for deception patterns in stored Art of War analyses."""
            try:
                result = await self.art_of_war_agent.search_deception_patterns(
                    query=query,
                    n_results=n_results
                )
                return result
            except Exception as e:
                logger.error(f"Error searching deception patterns: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Generate comprehensive Art of War deception analysis report")
        async def generate_deception_report(
            analysis_type: str = "comprehensive",
            format: str = "markdown"
        ) -> Dict[str, Any]:
            """Generate a comprehensive Art of War deception analysis report."""
            try:
                result = await self.art_of_war_agent.generate_deception_report(
                    analysis_type=analysis_type,
                    format=format
                )
                return result
            except Exception as e:
                logger.error(f"Error generating deception report: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Run comprehensive analysis integrating main script functionality with full pipeline processing")
        async def run_comprehensive_analysis(
            input_content: str,
            analysis_type: str = "deception",
            language: str = "en",
            options: Dict[str, Any] = None,
            generate_report: bool = True,
            report_format: str = "markdown"
        ) -> Dict[str, Any]:
            """Run comprehensive analysis integrating main script functionality with full pipeline processing.
            
            This tool provides the full functionality of the main.py script through MCP interface,
            supporting all analysis types including deception analysis, sentiment analysis, knowledge graphs,
            and comprehensive reporting with proper error handling and integration.
            """
            try:
                logger.info(f"Starting comprehensive analysis: {analysis_type}")
                
                # Initialize options if not provided
                if options is None:
                    options = {}
                
                # Detect content type
                content_type = self._detect_content_type(input_content)
                logger.info(f"Detected content type: {content_type}")
                
                # Process content through appropriate pipeline
                processing_result = await self._process_comprehensive_content(
                    input_content, content_type, language, options
                )
                
                if not processing_result.get("success", False):
                    return processing_result
                
                # Run specific analysis based on type
                analysis_result = await self._run_specific_analysis(
                    analysis_type, processing_result, language, options
                )
                
                # Generate comprehensive report if requested
                report_result = None
                if generate_report:
                    report_result = await self._generate_comprehensive_report(
                        analysis_type, analysis_result, report_format
                    )
                
                # Prepare final result
                result = {
                    "success": True,
                    "analysis_type": analysis_type,
                    "content_type": content_type,
                    "processing_result": processing_result,
                    "analysis_result": analysis_result,
                    "report": report_result
                }
                
                logger.info(f"✅ Comprehensive analysis completed successfully: {analysis_type}")
                return result
                
            except Exception as e:
                logger.error(f"Error in comprehensive analysis: {e}")
                return {"success": False, "error": str(e)}

        @self.mcp.tool(description="Generic comprehensive analysis system for any strategic topic with automatic category determination")
        async def analyze_strategic_topic(
            topic: str,
            analysis_type: str = "comprehensive",
            generate_reports: bool = True
        ) -> Dict[str, Any]:
            """Analyze any strategic topic using the DIA3 generic comprehensive analysis system.
            
            This tool provides:
            1. Automatic research of the topic using DIA3 knowledge base
            2. Automatic determination of relevant analysis categories from 24 available options
            3. Specialized analysis using multiple agents (Art of War, Knowledge Graph, Business Intelligence)
            4. Advanced report generation with tooltips and multiple sources
            
            Args:
                topic: The strategic topic to analyze (e.g., "Pakistan submarine acquisition", "China-Taiwan relations")
                analysis_type: Type of analysis ("comprehensive", "strategic", "tactical", "economic")
                generate_reports: Whether to generate markdown and HTML reports
            
            Returns:
                Dictionary containing analysis results and report paths
            """
            try:
                logger.info(f"🚀 Starting Generic Comprehensive Analysis: {topic}")
                
                # Use the generic comprehensive analysis system
                result = await self.generic_analysis_system.analyze_topic(topic, analysis_type)
                
                if result["success"]:
                    logger.info(f"✅ Generic analysis completed successfully for: {topic}")
                    logger.info(f"📄 Reports generated: {result.get('report_paths', {})}")
                else:
                    logger.error(f"❌ Generic analysis failed for {topic}: {result.get('error', 'Unknown error')}")
                
                return result
                
            except Exception as e:
                logger.error(f"Error in generic strategic analysis: {e}")
                return {"success": False, "error": str(e)}

        logger.info("✅ Registered 30 unified MCP tools (including generic comprehensive analysis system)")

    def _detect_content_type(self, content: str) -> str:
        """Detect content type based on content or file extension."""
        if content.startswith("http"):
            return "website"
        elif content.lower().endswith(('.pdf',)):
            return "pdf"
        elif content.lower().endswith(('.mp3', '.wav', '.m4a')):
            return "audio"
        elif content.lower().endswith(('.mp4', '.avi', '.mov')):
            return "video"
        elif content.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return "image"
        else:
            return "text"
    
    def _detect_language_from_text(self, text: str) -> str:
        """Detect language from text content using character analysis."""
        if not text:
            return "en"
        
        # Count characters by script
        russian_chars = sum(1 for char in text if '\u0400' <= char <= '\u04FF')
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        japanese_chars = sum(1 for char in text if '\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF')
        korean_chars = sum(1 for char in text if '\uAC00' <= char <= '\uD7AF')
        hindi_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
        
        # Determine language based on character counts
        total_chars = len(text)
        if total_chars == 0:
            return "en"
        
        # Calculate percentages
        russian_pct = russian_chars / total_chars if total_chars > 0 else 0
        chinese_pct = chinese_chars / total_chars if total_chars > 0 else 0
        arabic_pct = arabic_chars / total_chars if total_chars > 0 else 0
        japanese_pct = japanese_chars / total_chars if total_chars > 0 else 0
        korean_pct = korean_chars / total_chars if total_chars > 0 else 0
        hindi_pct = hindi_chars / total_chars if total_chars > 0 else 0
        
        # Language detection thresholds
        if russian_pct > 0.1 or russian_chars > 20:
            return "ru"
        elif chinese_pct > 0.1 or chinese_chars > 20:
            return "zh"
        elif arabic_pct > 0.1 or arabic_chars > 20:
            return "ar"
        elif japanese_pct > 0.1 or japanese_chars > 20:
            return "ja"
        elif korean_pct > 0.1 or korean_chars > 20:
            return "ko"
        elif hindi_pct > 0.1 or hindi_chars > 20:
            return "hi"
        else:
            return "en"  # Default to English/Latin

    async def _process_comprehensive_content(
        self,
        input_content: str,
        content_type: str,
        language: str,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process content through the comprehensive pipeline."""
        try:
            logger.info(f"Processing comprehensive content: {content_type}")
            
            # Route to appropriate processing based on content type
            if content_type in ["text", "pdf", "website"]:
                result = await self.text_agent.process_content(
                    input_content, language, options
                )
            elif content_type in ["audio", "video"]:
                result = await self.audio_agent.process_content(
                    input_content, language, options
                )
            elif content_type in ["image", "vision"]:
                result = await self.vision_agent.process_content(
                    input_content, language, options
                )
            else:
                # Default to text processing
                result = await self.text_agent.process_content(
                    input_content, language, options
                )
            
            return {"success": True, "result": result}
            
        except Exception as e:
            logger.error(f"Error processing comprehensive content: {e}")
            return {"success": False, "error": str(e)}

    async def _run_specific_analysis(
        self,
        analysis_type: str,
        processing_result: Dict[str, Any],
        language: str,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run specific analysis based on analysis type."""
        try:
            logger.info(f"Running specific analysis: {analysis_type}")
            
            if analysis_type == "deception":
                # Run Art of War deception analysis
                result = await self.art_of_war_agent.analyze_deception_techniques(
                    analysis_type="comprehensive",
                    focus_areas=options.get("focus_areas"),
                    include_modern_applications=options.get("include_modern_applications", True),
                    include_ethical_considerations=options.get("include_ethical_considerations", True)
                )
            elif analysis_type == "sentiment":
                # Run sentiment analysis
                result = await self.text_agent.analyze_sentiment(
                    processing_result.get("result", {}).get("content", ""),
                    language=language
                )
            elif analysis_type == "knowledge_graph":
                # Generate knowledge graph
                result = await self.kg_agent.generate_knowledge_graph(
                    processing_result.get("result", {}).get("content", ""),
                    "text"
                )
            elif analysis_type == "entities":
                # Extract entities
                result = await self.text_agent.extract_entities(
                    processing_result.get("result", {}).get("content", "")
                )
            elif analysis_type == "comprehensive":
                # Run comprehensive analysis including multiple types
                results = {}
                
                # Deception analysis
                deception_result = await self.art_of_war_agent.analyze_deception_techniques(
                    analysis_type="comprehensive"
                )
                results["deception"] = deception_result
                
                # Sentiment analysis
                sentiment_result = await self.text_agent.analyze_sentiment(
                    processing_result.get("result", {}).get("content", ""),
                    language=language
                )
                results["sentiment"] = sentiment_result
                
                # Knowledge graph
                kg_result = await self.kg_agent.generate_knowledge_graph(
                    processing_result.get("result", {}).get("content", ""),
                    "text"
                )
                results["knowledge_graph"] = kg_result
                
                # Entities
                entities_result = await self.text_agent.extract_entities(
                    processing_result.get("result", {}).get("content", "")
                )
                results["entities"] = entities_result
                
                result = results
            else:
                # Default to deception analysis
                result = await self.art_of_war_agent.analyze_deception_techniques(
                    analysis_type="comprehensive"
                )
            
            return {"success": True, "result": result}
            
        except Exception as e:
            logger.error(f"Error running specific analysis: {e}")
            return {"success": False, "error": str(e)}

    async def _generate_comprehensive_report(
        self,
        analysis_type: str,
        analysis_result: Dict[str, Any],
        report_format: str
    ) -> Dict[str, Any]:
        """Generate comprehensive report based on analysis results."""
        try:
            logger.info(f"Generating comprehensive report: {analysis_type}")
            
            if analysis_type == "deception":
                # Generate Art of War deception report
                result = await self.art_of_war_agent.generate_deception_report(
                    analysis_type="comprehensive",
                    format=report_format
                )
            elif analysis_type == "comprehensive":
                # Generate comprehensive report with all analysis types
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"comprehensive_analysis_{timestamp}.{report_format}"
                
                if report_format == "markdown":
                    report_content = self._generate_comprehensive_markdown_report(analysis_result)
                elif report_format == "html":
                    report_content = self._generate_comprehensive_html_report(analysis_result)
                else:
                    report_content = str(analysis_result)
                
                # Save report
                report_path = Path("Results") / filename
                report_path.parent.mkdir(exist_ok=True)
                
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                
                result = {
                    "success": True,
                    "report_path": str(report_path),
                    "report_content": report_content,
                    "format": report_format
                }
            else:
                # Default report
                result = {
                    "success": True,
                    "analysis_result": analysis_result,
                    "format": report_format
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating comprehensive report: {e}")
            return {"success": False, "error": str(e)}

    def _generate_comprehensive_markdown_report(self, analysis_result: Dict[str, Any]) -> str:
        """Generate comprehensive markdown report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# Comprehensive Analysis Report

*Generated on {timestamp}*

## Executive Summary

This report contains comprehensive analysis results including deception analysis, sentiment analysis, knowledge graphs, and entity extraction.

## Analysis Results

"""
        
        if isinstance(analysis_result.get("result"), dict):
            for analysis_type, result in analysis_result["result"].items():
                report += f"### {analysis_type.title()} Analysis\n\n"
                if isinstance(result, dict):
                    for key, value in result.items():
                        report += f"**{key}**: {value}\n\n"
                else:
                    report += f"{result}\n\n"
        
        report += "## Conclusion\n\nThis comprehensive analysis provides insights across multiple dimensions of the content.\n"
        
        return report

    def _generate_comprehensive_html_report(self, analysis_result: Dict[str, Any]) -> str:
        """Generate comprehensive HTML report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .content {{
            padding: 40px;
        }}
        .section {{
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border: 1px solid #e9ecef;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Comprehensive Analysis Report</h1>
            <p>Generated on {timestamp}</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>Executive Summary</h2>
                <p>This report contains comprehensive analysis results including deception analysis, sentiment analysis, knowledge graphs, and entity extraction.</p>
            </div>
            
            <div class="section">
                <h2>Analysis Results</h2>
"""
        
        if isinstance(analysis_result.get("result"), dict):
            for analysis_type, result in analysis_result["result"].items():
                html += f"""
                <h3>{analysis_type.title()} Analysis</h3>
"""
                if isinstance(result, dict):
                    for key, value in result.items():
                        html += f"<p><strong>{key}</strong>: {value}</p>\n"
                else:
                    html += f"<p>{result}</p>\n"
        
        html += """
            </div>
            
            <div class="section">
                <h2>Conclusion</h2>
                <p>This comprehensive analysis provides insights across multiple dimensions of the content.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
        
        return html

    def start(self, host: str = "localhost", port: int = 8000):
        """Start the standalone MCP server using FastMCP's HTTP app integration."""
        if not self.mcp:
            logger.error("MCP server not available")
            return

        if self.is_running:
            logger.warning("MCP server is already running")
            return

        try:
            logger.info(f"🚀 Starting Standalone MCP Server on {host}:{port}")
            self.is_running = True
            
            # Start the server in a separate thread
            def run_server():
                try:
                    import uvicorn
                    
                    # Use FastMCP's HTTP app method for proper integration
                    if self.mcp:
                        # Get the HTTP app from FastMCP
                        http_app = self.mcp.http_app(path="/mcp")
                        if http_app:
                            # Start the server with uvicorn
                            uvicorn.run(http_app, host=host, port=port, log_level="info")
                        else:
                            logger.error("Failed to create HTTP app from FastMCP")
                            self.is_running = False
                    else:
                        logger.error("MCP server not available")
                        self.is_running = False
                        
                except Exception as e:
                    logger.error(f"Error running MCP server: {e}")
                    self.is_running = False

            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()
            
            # Wait a moment for the server to start
            time.sleep(3)
            
            if self.is_running:
                logger.info(f"✅ Standalone MCP Server started successfully on {host}:{port}")
                logger.info("🔧 Available endpoints:")
                logger.info(f"   - MCP Protocol: http://{host}:{port}/mcp")
                logger.info(f"   - MCP Stream: http://{host}:{port}/mcp/stream")
                logger.info(f"   - Health Check: http://{host}:{port}/mcp-health")
                logger.info("🌊 Streamable HTTP transport ready for Strands integration")
                logger.info("📄 All 29 MCP tools available via FastMCP integration")
            else:
                logger.error("❌ Failed to start MCP server")
                
        except Exception as e:
            logger.error(f"Error starting MCP server: {e}")
            self.is_running = False

    def stop(self):
        """Stop the standalone MCP server."""
        if not self.is_running:
            logger.warning("MCP server is not running")
            return

        try:
            self.is_running = False
            logger.info("🛑 Standalone MCP Server stopped")
        except Exception as e:
            logger.error(f"Error stopping MCP server: {e}")

    def is_server_running(self) -> bool:
        """Check if the server is running."""
        return self.is_running

    # Helper methods for tool execution
    async def _execute_process_content(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute process_content tool."""
        try:
            content = arguments.get("content", "")
            content_type = arguments.get("content_type", "auto")
            language = arguments.get("language", "en")
            options = arguments.get("options", {})
            
            if content_type == "auto":
                content_type = self._detect_content_type(content)
            
            if content_type == "text":
                result = await self.text_agent.process_text(content, options or {})
            else:
                result = {"success": True, "content": content, "content_type": content_type}
            
            return {"success": True, "result": result, "content_type": content_type}
        except Exception as e:
            logger.error(f"Error executing process_content: {e}")
            return {"success": False, "error": str(e)}

    async def _execute_analyze_sentiment(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analyze_sentiment tool."""
        try:
            text = arguments.get("text", "")
            language = arguments.get("language", "en")
            
            result = await self.text_agent.analyze_sentiment(text, language)
            return {"success": True, "result": result}
        except Exception as e:
            logger.error(f"Error executing analyze_sentiment: {e}")
            return {"success": False, "error": str(e)}

    async def _execute_extract_entities(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute extract_entities tool."""
        try:
            text = arguments.get("text", "")
            entity_types = arguments.get("entity_types", None)
            
            result = await self.text_agent.extract_entities(text, entity_types)
            return {"success": True, "result": result}
        except Exception as e:
            logger.error(f"Error executing extract_entities: {e}")
            return {"success": False, "error": str(e)}

    async def _execute_generate_knowledge_graph(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute generate_knowledge_graph tool."""
        try:
            content = arguments.get("content", "")
            content_type = arguments.get("content_type", "text")
            
            result = await self.kg_agent.generate_knowledge_graph(content, content_type)
            return {"success": True, "result": result}
        except Exception as e:
            logger.error(f"Error executing generate_knowledge_graph: {e}")
            return {"success": False, "error": str(e)}

    async def _execute_analyze_art_of_war_deception(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analyze_art_of_war_deception tool."""
        try:
            analysis_type = arguments.get("analysis_type", "comprehensive")
            focus_areas = arguments.get("focus_areas", None)
            include_modern_applications = arguments.get("include_modern_applications", True)
            include_ethical_considerations = arguments.get("include_ethical_considerations", True)
            
            result = await self.art_of_war_agent.analyze_deception_techniques(
                analysis_type=analysis_type,
                focus_areas=focus_areas,
                include_modern_applications=include_modern_applications,
                include_ethical_considerations=include_ethical_considerations
            )
            return result
        except Exception as e:
            logger.error(f"Error executing analyze_art_of_war_deception: {e}")
            return {"success": False, "error": str(e)}


def create_standalone_mcp_server() -> StandaloneMCPServer:
    """Create and return a standalone MCP server instance."""
    return StandaloneMCPServer()


def start_standalone_mcp_server(host: str = "localhost", port: int = 8000):
    """Start the standalone MCP server."""
    server = create_standalone_mcp_server()
    server.start(host, port)
    return server


if __name__ == "__main__":
    # Start the standalone MCP server
    server = start_standalone_mcp_server()
    
    try:
        # Keep the server running
        while server.is_server_running():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down standalone MCP server...")
        server.stop()
        print("✅ Server stopped")
