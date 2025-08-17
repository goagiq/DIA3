"""
Integrated Dynamic MCP Manager
Integrates dynamic tool management with all existing MCP tools
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_servers.dynamic_tool_manager import (
    DynamicMCPToolManager, 
    ToolConfig, 
    ToolStatus,
    ResourceLevel
)

# Import all MCP tools
try:
    from mcp_servers.unified_mcp_server import UnifiedMCPServer
    UNIFIED_MCP_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Unified MCP Server not available: {e}")
    UNIFIED_MCP_AVAILABLE = False

try:
    from mcp_servers.monte_carlo_mcp_tools import MonteCarloMCPTools
    MONTE_CARLO_MCP_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Monte Carlo MCP Tools not available: {e}")
    MONTE_CARLO_MCP_AVAILABLE = False

try:
    from mcp_servers.enhanced_mcp_tools import EnhancedMCPTools
    ENHANCED_MCP_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Enhanced MCP Tools not available: {e}")
    ENHANCED_MCP_AVAILABLE = False

try:
    from mcp_servers.phase5_interpretability_mcp_tools import InterpretabilityMCPTools
    INTERPRETABILITY_MCP_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Interpretability MCP Tools not available: {e}")
    INTERPRETABILITY_MCP_AVAILABLE = False

try:
    from mcp_servers.strategic_analysis_server import StrategicAnalysisServer
    STRATEGIC_ANALYSIS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Strategic Analysis Server not available: {e}")
    STRATEGIC_ANALYSIS_AVAILABLE = False

try:
    from mcp_servers.video_processing_server import VideoProcessingServer
    VIDEO_PROCESSING_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Video Processing Server not available: {e}")
    VIDEO_PROCESSING_AVAILABLE = False

try:
    from mcp_servers.audio_processing_server import AudioProcessingServer
    AUDIO_PROCESSING_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Audio Processing Server not available: {e}")
    AUDIO_PROCESSING_AVAILABLE = False

try:
    from mcp_servers.decision_support_server import DecisionSupportServer
    DECISION_SUPPORT_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Decision Support Server not available: {e}")
    DECISION_SUPPORT_AVAILABLE = False

try:
    from mcp_servers.monitoring_server import MonitoringServer
    MONITORING_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Monitoring Server not available: {e}")
    MONITORING_AVAILABLE = False

try:
    from mcp_servers.predictive_analytics_server import PredictiveAnalyticsServer
    PREDICTIVE_ANALYTICS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Predictive Analytics Server not available: {e}")
    PREDICTIVE_ANALYTICS_AVAILABLE = False

try:
    from mcp_servers.scenario_analysis_server import ScenarioAnalysisServer
    SCENARIO_ANALYSIS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Scenario Analysis Server not available: {e}")
    SCENARIO_ANALYSIS_AVAILABLE = False

try:
    from mcp_servers.website_processing_server import WebsiteProcessingServer
    WEBSITE_PROCESSING_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Website Processing Server not available: {e}")
    WEBSITE_PROCESSING_AVAILABLE = False

try:
    from mcp_servers.pdf_processing_server import PDFProcessingServer
    PDF_PROCESSING_AVAILABLE = True
except ImportError as e:
    logging.warning(f"PDF Processing Server not available: {e}")
    PDF_PROCESSING_AVAILABLE = False

logger = logging.getLogger(__name__)


class IntegratedDynamicMCPManager:
    """
    Integrated Dynamic MCP Manager
    Manages all MCP tools with dynamic resource optimization
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.dynamic_manager = DynamicMCPToolManager(config_file)
        self.mcp_instances: Dict[str, Any] = {}
        self.tool_factories: Dict[str, Callable] = {}
        
        # Register all available MCP tools
        self._register_all_mcp_tools()
        
        # Start monitoring (will be started when needed)
        self._monitoring_started = False
    
    def _register_all_mcp_tools(self):
        """Register all available MCP tools with dynamic management"""
        
        # Unified MCP Server (High Priority - Core functionality)
        if UNIFIED_MCP_AVAILABLE:
            self._register_mcp_tool(
                "unified_mcp",
                self._create_unified_mcp_server,
                priority=10,
                max_cpu_percent=90.0,
                max_memory_mb=8192.0,
                description="Unified MCP Server with all core functionality"
            )
        
        # Monte Carlo Tools (High Priority - Resource intensive)
        if MONTE_CARLO_MCP_AVAILABLE:
            self._register_mcp_tool(
                "monte_carlo",
                self._create_monte_carlo_tools,
                priority=9,
                max_cpu_percent=95.0,
                max_memory_mb=4096.0,
                description="Monte Carlo simulation tools"
            )
        
        # Enhanced MCP Tools (Medium Priority)
        if ENHANCED_MCP_AVAILABLE:
            self._register_mcp_tool(
                "enhanced_mcp",
                self._create_enhanced_mcp_tools,
                priority=7,
                max_cpu_percent=80.0,
                max_memory_mb=3072.0,
                description="Enhanced MCP tools with advanced features"
            )
        
        # Strategic Analysis (Medium Priority)
        if STRATEGIC_ANALYSIS_AVAILABLE:
            self._register_mcp_tool(
                "strategic_analysis",
                self._create_strategic_analysis_server,
                priority=8,
                max_cpu_percent=85.0,
                max_memory_mb=4096.0,
                description="Strategic analysis and planning tools"
            )
        
        # Video Processing (Medium Priority - Resource intensive)
        if VIDEO_PROCESSING_AVAILABLE:
            self._register_mcp_tool(
                "video_processing",
                self._create_video_processing_server,
                priority=6,
                max_cpu_percent=90.0,
                max_memory_mb=6144.0,
                description="Video processing and analysis tools"
            )
        
        # Audio Processing (Medium Priority)
        if AUDIO_PROCESSING_AVAILABLE:
            self._register_mcp_tool(
                "audio_processing",
                self._create_audio_processing_server,
                priority=6,
                max_cpu_percent=75.0,
                max_memory_mb=2048.0,
                description="Audio processing and analysis tools"
            )
        
        # Decision Support (Medium Priority)
        if DECISION_SUPPORT_AVAILABLE:
            self._register_mcp_tool(
                "decision_support",
                self._create_decision_support_server,
                priority=7,
                max_cpu_percent=70.0,
                max_memory_mb=2048.0,
                description="Decision support and analysis tools"
            )
        
        # Predictive Analytics (Medium Priority)
        if PREDICTIVE_ANALYTICS_AVAILABLE:
            self._register_mcp_tool(
                "predictive_analytics",
                self._create_predictive_analytics_server,
                priority=7,
                max_cpu_percent=80.0,
                max_memory_mb=3072.0,
                description="Predictive analytics and forecasting tools"
            )
        
        # Scenario Analysis (Medium Priority)
        if SCENARIO_ANALYSIS_AVAILABLE:
            self._register_mcp_tool(
                "scenario_analysis",
                self._create_scenario_analysis_server,
                priority=6,
                max_cpu_percent=75.0,
                max_memory_mb=2048.0,
                description="Scenario analysis and planning tools"
            )
        
        # Monitoring (Low Priority - Background service)
        if MONITORING_AVAILABLE:
            self._register_mcp_tool(
                "monitoring",
                self._create_monitoring_server,
                priority=3,
                max_cpu_percent=30.0,
                max_memory_mb=1024.0,
                description="System monitoring and health check tools"
            )
        
        # Website Processing (Low Priority)
        if WEBSITE_PROCESSING_AVAILABLE:
            self._register_mcp_tool(
                "website_processing",
                self._create_website_processing_server,
                priority=4,
                max_cpu_percent=60.0,
                max_memory_mb=1536.0,
                description="Website processing and analysis tools"
            )
        
        # PDF Processing (Low Priority)
        if PDF_PROCESSING_AVAILABLE:
            self._register_mcp_tool(
                "pdf_processing",
                self._create_pdf_processing_server,
                priority=4,
                max_cpu_percent=50.0,
                max_memory_mb=1024.0,
                description="PDF processing and extraction tools"
            )
        
        # Interpretability (Low Priority - Analysis only)
        if INTERPRETABILITY_MCP_AVAILABLE:
            self._register_mcp_tool(
                "interpretability",
                self._create_interpretability_tools,
                priority=5,
                max_cpu_percent=60.0,
                max_memory_mb=1536.0,
                description="Model interpretability and explanation tools"
            )
    
    def _register_mcp_tool(self, name: str, factory: Callable, **config_kwargs):
        """Register an MCP tool with dynamic management"""
        # Create tool configuration
        config = ToolConfig(
            name=name,
            enabled=True,
            **config_kwargs
        )
        
        # Register with dynamic manager
        self.dynamic_manager.register_tool_factory(name, factory)
        
        # Store factory for later use
        self.tool_factories[name] = factory
        
        logger.info(f"Registered MCP tool: {name} with priority {config.priority}")
    
    # Factory methods for each MCP tool
    async def _create_unified_mcp_server(self):
        """Create Unified MCP Server instance"""
        if "unified_mcp" not in self.mcp_instances:
            self.mcp_instances["unified_mcp"] = UnifiedMCPServer()
        return self.mcp_instances["unified_mcp"]
    
    async def _create_monte_carlo_tools(self):
        """Create Monte Carlo MCP Tools instance"""
        if "monte_carlo" not in self.mcp_instances:
            self.mcp_instances["monte_carlo"] = MonteCarloMCPTools()
        return self.mcp_instances["monte_carlo"]
    
    async def _create_enhanced_mcp_tools(self):
        """Create Enhanced MCP Tools instance"""
        if "enhanced_mcp" not in self.mcp_instances:
            self.mcp_instances["enhanced_mcp"] = EnhancedMCPTools()
        return self.mcp_instances["enhanced_mcp"]
    
    async def _create_interpretability_tools(self):
        """Create Interpretability MCP Tools instance"""
        if "interpretability" not in self.mcp_instances:
            self.mcp_instances["interpretability"] = InterpretabilityMCPTools()
        return self.mcp_instances["interpretability"]
    
    async def _create_strategic_analysis_server(self):
        """Create Strategic Analysis Server instance"""
        if "strategic_analysis" not in self.mcp_instances:
            self.mcp_instances["strategic_analysis"] = StrategicAnalysisServer()
        return self.mcp_instances["strategic_analysis"]
    
    async def _create_video_processing_server(self):
        """Create Video Processing Server instance"""
        if "video_processing" not in self.mcp_instances:
            self.mcp_instances["video_processing"] = VideoProcessingServer()
        return self.mcp_instances["video_processing"]
    
    async def _create_audio_processing_server(self):
        """Create Audio Processing Server instance"""
        if "audio_processing" not in self.mcp_instances:
            self.mcp_instances["audio_processing"] = AudioProcessingServer()
        return self.mcp_instances["audio_processing"]
    
    async def _create_decision_support_server(self):
        """Create Decision Support Server instance"""
        if "decision_support" not in self.mcp_instances:
            self.mcp_instances["decision_support"] = DecisionSupportServer()
        return self.mcp_instances["decision_support"]
    
    async def _create_monitoring_server(self):
        """Create Monitoring Server instance"""
        if "monitoring" not in self.mcp_instances:
            self.mcp_instances["monitoring"] = MonitoringServer()
        return self.mcp_instances["monitoring"]
    
    async def _create_predictive_analytics_server(self):
        """Create Predictive Analytics Server instance"""
        if "predictive_analytics" not in self.mcp_instances:
            self.mcp_instances["predictive_analytics"] = PredictiveAnalyticsServer()
        return self.mcp_instances["predictive_analytics"]
    
    async def _create_scenario_analysis_server(self):
        """Create Scenario Analysis Server instance"""
        if "scenario_analysis" not in self.mcp_instances:
            self.mcp_instances["scenario_analysis"] = ScenarioAnalysisServer()
        return self.mcp_instances["scenario_analysis"]
    
    async def _create_website_processing_server(self):
        """Create Website Processing Server instance"""
        if "website_processing" not in self.mcp_instances:
            self.mcp_instances["website_processing"] = WebsiteProcessingServer()
        return self.mcp_instances["website_processing"]
    
    async def _create_pdf_processing_server(self):
        """Create PDF Processing Server instance"""
        if "pdf_processing" not in self.mcp_instances:
            self.mcp_instances["pdf_processing"] = PDFProcessingServer()
        return self.mcp_instances["pdf_processing"]
    
    # Public interface methods
    async def _ensure_monitoring_started(self):
        """Ensure monitoring is started"""
        if not self._monitoring_started:
            await self.dynamic_manager.start_monitoring()
            self._monitoring_started = True
    
    async def enable_tool(self, tool_name: str) -> bool:
        """Enable a specific MCP tool"""
        await self._ensure_monitoring_started()
        return await self.dynamic_manager.enable_tool(tool_name)
    
    async def disable_tool(self, tool_name: str) -> bool:
        """Disable a specific MCP tool"""
        await self._ensure_monitoring_started()
        return await self.dynamic_manager.disable_tool(tool_name)
    
    async def pause_tool(self, tool_name: str) -> bool:
        """Pause a specific MCP tool"""
        await self._ensure_monitoring_started()
        return await self.dynamic_manager.pause_tool(tool_name)
    
    async def resume_tool(self, tool_name: str) -> bool:
        """Resume a specific MCP tool"""
        await self._ensure_monitoring_started()
        return await self.dynamic_manager.resume_tool(tool_name)
    
    def get_tool_status(self, tool_name: str):
        """Get status of a specific tool"""
        return self.dynamic_manager.get_tool_status(tool_name)
    
    def get_all_tool_statuses(self):
        """Get status of all tools"""
        return self.dynamic_manager.get_all_tool_statuses()
    
    def get_system_resources(self):
        """Get current system resources"""
        return self.dynamic_manager.get_system_resources()
    
    def get_resource_level(self) -> ResourceLevel:
        """Get current resource level"""
        return self.dynamic_manager.get_resource_level()
    
    def set_auto_scaling(self, enabled: bool):
        """Enable or disable auto-scaling"""
        self.dynamic_manager.set_auto_scaling(enabled)
    
    async def get_tool_instance(self, tool_name: str):
        """Get the actual MCP tool instance"""
        if tool_name in self.mcp_instances:
            return self.mcp_instances[tool_name]
        return None
    
    async def execute_tool_method(self, tool_name: str, method_name: str, *args, **kwargs):
        """Execute a method on a specific tool"""
        tool_instance = await self.get_tool_instance(tool_name)
        if tool_instance and hasattr(tool_instance, method_name):
            method = getattr(tool_instance, method_name)
            if asyncio.iscoroutinefunction(method):
                return await method(*args, **kwargs)
            else:
                return method(*args, **kwargs)
        else:
            raise ValueError(f"Tool {tool_name} or method {method_name} not found")
    
    async def get_available_tools(self) -> List[str]:
        """Get list of all available tools"""
        return list(self.tool_factories.keys())
    
    async def get_enabled_tools(self) -> List[str]:
        """Get list of currently enabled tools"""
        statuses = self.get_all_tool_statuses()
        return [name for name, info in statuses.items() 
                if info.status == ToolStatus.ENABLED]
    
    async def optimize_for_workload(self, workload_type: str):
        """Optimize tool configuration for specific workload types"""
        workload_configs = {
            "monte_carlo_heavy": {
                "enable": ["monte_carlo", "unified_mcp"],
                "disable": ["video_processing", "audio_processing", "monitoring"],
                "priority_adjustments": {
                    "monte_carlo": 10,
                    "unified_mcp": 9
                }
            },
            "multimedia_heavy": {
                "enable": ["video_processing", "audio_processing", "unified_mcp"],
                "disable": ["monte_carlo", "predictive_analytics"],
                "priority_adjustments": {
                    "video_processing": 9,
                    "audio_processing": 8,
                    "unified_mcp": 7
                }
            },
            "analysis_heavy": {
                "enable": ["strategic_analysis", "predictive_analytics", "scenario_analysis"],
                "disable": ["video_processing", "audio_processing"],
                "priority_adjustments": {
                    "strategic_analysis": 9,
                    "predictive_analytics": 8,
                    "scenario_analysis": 7
                }
            },
            "lightweight": {
                "enable": ["unified_mcp", "monitoring"],
                "disable": ["monte_carlo", "video_processing", "audio_processing"],
                "priority_adjustments": {
                    "unified_mcp": 8,
                    "monitoring": 5
                }
            }
        }
        
        if workload_type not in workload_configs:
            raise ValueError(f"Unknown workload type: {workload_type}")
        
        config = workload_configs[workload_type]
        
        # Apply configuration
        for tool_name in config["enable"]:
            if tool_name in self.tool_factories:
                await self.enable_tool(tool_name)
        
        for tool_name in config["disable"]:
            if tool_name in self.tool_factories:
                await self.disable_tool(tool_name)
        
        # Adjust priorities
        for tool_name, priority in config["priority_adjustments"].items():
            if tool_name in self.tool_factories:
                self.dynamic_manager.update_tool_config(tool_name, priority=priority)
        
        logger.info(f"Optimized configuration for {workload_type} workload")
    
    async def cleanup(self):
        """Cleanup all tools and stop monitoring"""
        await self.dynamic_manager.cleanup()


# Global instance
integrated_mcp_manager = IntegratedDynamicMCPManager()
