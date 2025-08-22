"""
Dynamic MCP Tool Manager
Manages MCP tools dynamically to optimize system resources
"""

import asyncio
import logging
import psutil
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import threading
from datetime import datetime
import json
import os

logger = logging.getLogger(__name__)


class ToolStatus(Enum):
    """Tool status enumeration"""
    ENABLED = "enabled"
    DISABLED = "disabled"
    STARTING = "starting"
    STOPPING = "stopping"
    ERROR = "error"
    PAUSED = "paused"


class ResourceLevel(Enum):
    """Resource usage levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ToolResourceUsage:
    """Resource usage for a tool"""
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    gpu_percent: float = 0.0
    gpu_memory_mb: float = 0.0
    disk_io_mb: float = 0.0
    network_io_mb: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ToolConfig:
    """Configuration for a tool"""
    name: str
    enabled: bool = True
    priority: int = 5  # 1-10, higher is more important
    max_cpu_percent: float = 80.0
    max_memory_mb: float = 2048.0
    max_gpu_percent: float = 90.0
    auto_scale: bool = True
    dependencies: List[str] = field(default_factory=list)
    startup_timeout: int = 30  # seconds
    health_check_interval: int = 60  # seconds
    resource_check_interval: int = 10  # seconds
    description: str = ""


@dataclass
class ToolInfo:
    """Information about a tool"""
    name: str
    status: ToolStatus
    config: ToolConfig
    resource_usage: ToolResourceUsage
    last_health_check: datetime
    error_count: int = 0
    startup_time: Optional[datetime] = None
    description: str = ""
    version: str = "1.0.0"


class MCPToolManager:
    """MCP Tool Manager for dynamic tool management"""
    
    def __init__(self):
        self.dynamic_tool_manager = dynamic_tool_manager
    
    def list_tools(self):
        """List all available tools"""
        try:
            tool_statuses = self.dynamic_tool_manager.get_all_tool_statuses()
            tools = []
            
            for tool_name, tool_info in tool_statuses.items():
                tools.append({
                    "name": tool_name,
                    "status": tool_info.status.value,
                    "config": tool_info.config,
                    "description": tool_info.description
                })
            
            return tools
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            return []
    
    def get_tool_status(self, tool_name: str):
        """Get status of a specific tool"""
        try:
            tool_statuses = self.dynamic_tool_manager.get_all_tool_statuses()
            return tool_statuses.get(tool_name)
        except Exception as e:
            logger.error(f"Error getting tool status: {e}")
            return None
    
    def get_system_resources(self):
        """Get system resources"""
        try:
            return self.dynamic_tool_manager.get_system_resources()
        except Exception as e:
            logger.error(f"Error getting system resources: {e}")
            return {"cpu_percent": 0.0, "memory_percent": 0.0}


class ResourceMonitor:
    """Monitor system resources"""
    
    def __init__(self):
        self.last_check = time.time()
        self.cpu_history = []
        self.memory_history = []
        self.gpu_history = []
        
    def get_system_resources(self) -> Dict[str, float]:
        """Get current system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            resources = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_mb": memory.available / (1024 * 1024),
                "disk_percent": disk.percent,
                "disk_free_mb": disk.free / (1024 * 1024),
                "timestamp": time.time()
            }
            
            # Update history
            self.cpu_history.append(cpu_percent)
            self.memory_history.append(memory.percent)
            
            # Keep only last 100 entries
            if len(self.cpu_history) > 100:
                self.cpu_history.pop(0)
            if len(self.memory_history) > 100:
                self.memory_history.pop(0)
                
            return resources
            
        except Exception as e:
            logger.error(f"Error getting system resources: {e}")
            return {}
    
    def get_resource_level(self) -> ResourceLevel:
        """Get current resource level"""
        resources = self.get_system_resources()
        
        if not resources:
            return ResourceLevel.MEDIUM
            
        cpu_percent = resources.get("cpu_percent", 0)
        memory_percent = resources.get("memory_percent", 0)
        
        if cpu_percent > 90 or memory_percent > 90:
            return ResourceLevel.CRITICAL
        elif cpu_percent > 70 or memory_percent > 70:
            return ResourceLevel.HIGH
        elif cpu_percent > 50 or memory_percent > 50:
            return ResourceLevel.MEDIUM
        else:
            return ResourceLevel.LOW
    
    def get_average_cpu(self, minutes: int = 5) -> float:
        """Get average CPU usage over specified minutes"""
        if not self.cpu_history:
            return 0.0
        
        # Calculate average over last N minutes (assuming 10-second intervals)
        samples = min(len(self.cpu_history), minutes * 6)
        recent_cpu = self.cpu_history[-samples:]
        return sum(recent_cpu) / len(recent_cpu) if recent_cpu else 0.0


class ToolLifecycleManager:
    """Manage tool lifecycle"""
    
    def __init__(self):
        self.tools: Dict[str, ToolInfo] = {}
        self.tool_factories: Dict[str, Callable] = {}
        self.active_tools: Dict[str, Any] = {}
        self.lock = threading.Lock()
        
    def register_tool_factory(self, tool_name: str, factory: Callable):
        """Register a tool factory function"""
        self.tool_factories[tool_name] = factory
        
        # Initialize tool info if not exists
        if tool_name not in self.tools:
            self.tools[tool_name] = ToolInfo(
                name=tool_name,
                status=ToolStatus.DISABLED,
                config=ToolConfig(name=tool_name),
                resource_usage=ToolResourceUsage(),
                last_health_check=datetime.now(),
                description="Monte Carlo simulation tool",
                version="1.0.0"
            )
        
        logger.info(f"Registered tool factory for: {tool_name}")
    
    async def start_tool(self, tool_name: str, config: ToolConfig) -> bool:
        """Start a tool"""
        with self.lock:
            if tool_name in self.active_tools:
                logger.warning(f"Tool {tool_name} is already running")
                return True
                
            if tool_name not in self.tool_factories:
                logger.error(f"No factory registered for tool: {tool_name}")
                return False
            
            try:
                logger.info(f"Starting tool: {tool_name}")
                
                # Update tool status
                if tool_name in self.tools:
                    self.tools[tool_name].status = ToolStatus.STARTING
                
                # Create tool instance
                factory = self.tool_factories[tool_name]
                tool_instance = await factory()
                
                # Store active tool
                self.active_tools[tool_name] = tool_instance
                
                # Update tool info
                tool_info = ToolInfo(
                    name=tool_name,
                    status=ToolStatus.ENABLED,
                    config=config,
                    resource_usage=ToolResourceUsage(),
                    last_health_check=datetime.now(),
                    startup_time=datetime.now()
                )
                self.tools[tool_name] = tool_info
                
                logger.info(f"Successfully started tool: {tool_name}")
                return True
                
            except Exception as e:
                logger.error(f"Error starting tool {tool_name}: {e}")
                if tool_name in self.tools:
                    self.tools[tool_name].status = ToolStatus.ERROR
                return False
    
    async def stop_tool(self, tool_name: str) -> bool:
        """Stop a tool"""
        with self.lock:
            if tool_name not in self.active_tools:
                logger.warning(f"Tool {tool_name} is not running")
                return True
            
            try:
                logger.info(f"Stopping tool: {tool_name}")
                
                # Update tool status
                if tool_name in self.tools:
                    self.tools[tool_name].status = ToolStatus.STOPPING
                
                # Get tool instance
                tool_instance = self.active_tools[tool_name]
                
                # Call cleanup method if available
                if hasattr(tool_instance, 'cleanup'):
                    await tool_instance.cleanup()
                
                # Remove from active tools
                del self.active_tools[tool_name]
                
                # Update tool info
                if tool_name in self.tools:
                    self.tools[tool_name].status = ToolStatus.DISABLED
                
                logger.info(f"Successfully stopped tool: {tool_name}")
                return True
                
            except Exception as e:
                logger.error(f"Error stopping tool {tool_name}: {e}")
                if tool_name in self.tools:
                    self.tools[tool_name].status = ToolStatus.ERROR
                return False
    
    async def pause_tool(self, tool_name: str) -> bool:
        """Pause a tool (temporarily disable)"""
        with self.lock:
            if tool_name not in self.active_tools:
                logger.warning(f"Tool {tool_name} is not running")
                return False
            
            try:
                logger.info(f"Pausing tool: {tool_name}")
                
                # Update tool status
                if tool_name in self.tools:
                    self.tools[tool_name].status = ToolStatus.PAUSED
                
                # Call pause method if available
                tool_instance = self.active_tools[tool_name]
                if hasattr(tool_instance, 'pause'):
                    await tool_instance.pause()
                
                logger.info(f"Successfully paused tool: {tool_name}")
                return True
                
            except Exception as e:
                logger.error(f"Error pausing tool {tool_name}: {e}")
                return False
    
    async def resume_tool(self, tool_name: str) -> bool:
        """Resume a paused tool"""
        with self.lock:
            if tool_name not in self.active_tools:
                logger.warning(f"Tool {tool_name} is not running")
                return False
            
            try:
                logger.info(f"Resuming tool: {tool_name}")
                
                # Update tool status
                if tool_name in self.tools:
                    self.tools[tool_name].status = ToolStatus.ENABLED
                
                # Call resume method if available
                tool_instance = self.active_tools[tool_name]
                if hasattr(tool_instance, 'resume'):
                    await tool_instance.resume()
                
                logger.info(f"Successfully resumed tool: {tool_name}")
                return True
                
            except Exception as e:
                logger.error(f"Error resuming tool {tool_name}: {e}")
                return False
    
    def get_tool_status(self, tool_name: str) -> Optional[ToolInfo]:
        """Get tool status"""
        return self.tools.get(tool_name)
    
    def get_all_tool_statuses(self) -> Dict[str, ToolInfo]:
        """Get status of all tools"""
        return self.tools.copy()
    
    def is_tool_active(self, tool_name: str) -> bool:
        """Check if tool is active"""
        return tool_name in self.active_tools


class DynamicMCPToolManager:
    """Dynamic MCP tool manager for resource optimization"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.resource_monitor = ResourceMonitor()
        self.lifecycle_manager = ToolLifecycleManager()
        self.config_file = config_file or "mcp_tool_config.json"
        self.configs: Dict[str, ToolConfig] = {}
        self.auto_scaling_enabled = True
        self.monitoring_task: Optional[asyncio.Task] = None
        self.running = False
        
        # Load configuration
        self.load_configuration()
        
        # Register default tools
        self._register_default_tools()
    
    def load_configuration(self):
        """Load tool configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                
                for tool_name, config_dict in config_data.get("tools", {}).items():
                    config = ToolConfig(
                        name=tool_name,
                        enabled=config_dict.get("enabled", True),
                        priority=config_dict.get("priority", 5),
                        max_cpu_percent=config_dict.get("max_cpu_percent", 80.0),
                        max_memory_mb=config_dict.get("max_memory_mb", 2048.0),
                        max_gpu_percent=config_dict.get("max_gpu_percent", 90.0),
                        auto_scale=config_dict.get("auto_scale", True),
                        dependencies=config_dict.get("dependencies", []),
                        startup_timeout=config_dict.get("startup_timeout", 30),
                        health_check_interval=config_dict.get("health_check_interval", 60),
                        resource_check_interval=config_dict.get("resource_check_interval", 10)
                    )
                    self.configs[tool_name] = config
                
                self.auto_scaling_enabled = config_data.get("auto_scaling_enabled", True)
                logger.info(f"Loaded configuration for {len(self.configs)} tools")
            else:
                logger.info("No configuration file found, using defaults")
                
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    def save_configuration(self):
        """Save tool configuration to file"""
        try:
            config_data = {
                "auto_scaling_enabled": self.auto_scaling_enabled,
                "tools": {}
            }
            
            for tool_name, config in self.configs.items():
                config_data["tools"][tool_name] = {
                    "enabled": config.enabled,
                    "priority": config.priority,
                    "max_cpu_percent": config.max_cpu_percent,
                    "max_memory_mb": config.max_memory_mb,
                    "max_gpu_percent": config.max_gpu_percent,
                    "auto_scale": config.auto_scale,
                    "dependencies": config.dependencies,
                    "startup_timeout": config.startup_timeout,
                    "health_check_interval": config.health_check_interval,
                    "resource_check_interval": config.resource_check_interval
                }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            logger.info("Configuration saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def _register_default_tools(self):
        """Register default tool factories"""
        # Register Monte Carlo tools
        try:
            from src.mcp_servers.monte_carlo_mcp_tools import get_monte_carlo_mcp_tools
            from src.mcp_servers.monte_carlo_visualization_mcp_tools import get_monte_carlo_visualization_mcp_tools
            
            # Register Monte Carlo tool factory
            self.register_tool_factory("monte_carlo_simulation", 
                lambda: get_monte_carlo_mcp_tools())
            
            # Add Monte Carlo tool configuration
            if "monte_carlo_simulation" not in self.configs:
                self.configs["monte_carlo_simulation"] = ToolConfig(
                    name="monte_carlo_simulation",
                    enabled=True,
                    priority=7,  # High priority for Monte Carlo
                    max_cpu_percent=90.0,  # Allow high CPU usage for simulations
                    max_memory_mb=4096.0,  # Allow more memory for large simulations
                    max_gpu_percent=95.0,  # Allow GPU usage if available
                    auto_scale=True,
                    dependencies=[],
                    startup_timeout=60,  # Longer startup time for Monte Carlo engine
                    health_check_interval=30,  # More frequent health checks
                    resource_check_interval=5,  # More frequent resource checks
                    description="Monte Carlo simulation engine with Phase 5 advanced features"
                )
            
            logger.info("✅ Monte Carlo tools registered with dynamic tool manager")
            
            # Register Monte Carlo visualization tool factory
            self.register_tool_factory("monte_carlo_visualization", 
                lambda: get_monte_carlo_visualization_mcp_tools())
            
            # Add Monte Carlo visualization tool configuration
            if "monte_carlo_visualization" not in self.configs:
                self.configs["monte_carlo_visualization"] = ToolConfig(
                    name="monte_carlo_visualization",
                    enabled=True,
                    priority=6,  # High priority for visualization
                    max_cpu_percent=70.0,  # Moderate CPU usage for visualization
                    max_memory_mb=2048.0,  # Moderate memory for visualization
                    max_gpu_percent=80.0,  # Allow GPU usage for rendering
                    auto_scale=True,
                    dependencies=["monte_carlo_simulation"],
                    startup_timeout=30,  # Shorter startup time for visualization
                    health_check_interval=60,  # Less frequent health checks
                    resource_check_interval=10,  # Less frequent resource checks
                    description="Monte Carlo visualization engine with Phase 6 interactive dashboards"
                )
            
            logger.info("✅ Monte Carlo visualization tools registered with dynamic tool manager")
            
        except ImportError as e:
            logger.warning(f"⚠️ Monte Carlo tools not available for dynamic management: {e}")
        except Exception as e:
            logger.error(f"❌ Error registering Monte Carlo tools: {e}")
        
        # Register other tool factories here as needed
        # This will be populated by specific tool implementations
    
    async def start_monitoring(self):
        """Start resource monitoring and auto-scaling"""
        if self.running:
            return
        
        self.running = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        logger.info("Started dynamic tool monitoring")
    
    async def stop_monitoring(self):
        """Stop resource monitoring"""
        if not self.running:
            return
        
        self.running = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Stopped dynamic tool monitoring")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                # Check system resources
                resource_level = self.resource_monitor.get_resource_level()
                
                # Auto-scaling logic
                if self.auto_scaling_enabled:
                    await self._auto_scale_tools(resource_level)
                
                # Health checks
                await self._perform_health_checks()
                
                # Update resource usage
                await self._update_resource_usage()
                
                # Wait for next check
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(30)
    
    async def _auto_scale_tools(self, resource_level: ResourceLevel):
        """Auto-scale tools based on resource level"""
        if resource_level == ResourceLevel.CRITICAL:
            # Disable low-priority tools
            await self._disable_low_priority_tools()
        elif resource_level == ResourceLevel.HIGH:
            # Pause non-essential tools
            await self._pause_non_essential_tools()
        elif resource_level == ResourceLevel.LOW:
            # Re-enable paused tools
            await self._resume_paused_tools()
    
    async def _disable_low_priority_tools(self):
        """Disable low-priority tools"""
        for tool_name, tool_info in self.lifecycle_manager.tools.items():
            if (tool_info.status == ToolStatus.ENABLED and 
                tool_info.config.priority <= 3):
                logger.info(f"Auto-disabling low-priority tool: {tool_name}")
                await self.disable_tool(tool_name)
    
    async def _pause_non_essential_tools(self):
        """Pause non-essential tools"""
        for tool_name, tool_info in self.lifecycle_manager.tools.items():
            if (tool_info.status == ToolStatus.ENABLED and 
                tool_info.config.priority <= 5):
                logger.info(f"Auto-pausing non-essential tool: {tool_name}")
                await self.pause_tool(tool_name)
    
    async def _resume_paused_tools(self):
        """Resume paused tools"""
        for tool_name, tool_info in self.lifecycle_manager.tools.items():
            if tool_info.status == ToolStatus.PAUSED:
                logger.info(f"Auto-resuming tool: {tool_name}")
                await self.resume_tool(tool_name)
    
    async def _perform_health_checks(self):
        """Perform health checks on active tools"""
        for tool_name, tool_info in self.lifecycle_manager.tools.items():
            if tool_info.status in [ToolStatus.ENABLED, ToolStatus.PAUSED]:
                # Update health check time
                tool_info.last_health_check = datetime.now()
                
                # Check for errors
                if tool_info.error_count > 3:
                    logger.warning(f"Tool {tool_name} has too many errors, disabling")
                    await self.disable_tool(tool_name)
    
    async def _update_resource_usage(self):
        """Update resource usage for active tools"""
        system_resources = self.resource_monitor.get_system_resources()
        
        # Distribute system resources among active tools
        active_tools = [name for name, info in self.lifecycle_manager.tools.items() 
                       if info.status in [ToolStatus.ENABLED, ToolStatus.PAUSED]]
        
        if active_tools:
            cpu_per_tool = system_resources.get("cpu_percent", 0) / len(active_tools)
            memory_per_tool = system_resources.get("memory_available_mb", 0) / len(active_tools)
            
            for tool_name in active_tools:
                tool_info = self.lifecycle_manager.tools[tool_name]
                tool_info.resource_usage = ToolResourceUsage(
                    cpu_percent=cpu_per_tool,
                    memory_mb=memory_per_tool,
                    timestamp=datetime.now()
                )
    
    async def enable_tool(self, tool_name: str) -> bool:
        """Enable a tool"""
        if tool_name not in self.configs:
            logger.error(f"Tool {tool_name} not found in configuration")
            return False
        
        config = self.configs[tool_name]
        config.enabled = True
        
        # Check dependencies
        for dep in config.dependencies:
            if not self.lifecycle_manager.is_tool_active(dep):
                logger.warning(f"Tool {tool_name} depends on {dep}, enabling dependency first")
                await self.enable_tool(dep)
        
        success = await self.lifecycle_manager.start_tool(tool_name, config)
        if success:
            self.save_configuration()
        
        return success
    
    async def disable_tool(self, tool_name: str) -> bool:
        """Disable a tool"""
        if tool_name not in self.configs:
            logger.error(f"Tool {tool_name} not found in configuration")
            return False
        
        config = self.configs[tool_name]
        config.enabled = False
        
        success = await self.lifecycle_manager.stop_tool(tool_name)
        if success:
            self.save_configuration()
        
        return success
    
    async def pause_tool(self, tool_name: str) -> bool:
        """Pause a tool"""
        return await self.lifecycle_manager.pause_tool(tool_name)
    
    async def resume_tool(self, tool_name: str) -> bool:
        """Resume a tool"""
        return await self.lifecycle_manager.resume_tool(tool_name)
    
    def get_tool_status(self, tool_name: str) -> Optional[ToolInfo]:
        """Get tool status"""
        return self.lifecycle_manager.get_tool_status(tool_name)
    
    def get_all_tool_statuses(self) -> Dict[str, ToolInfo]:
        """Get status of all tools"""
        return self.lifecycle_manager.get_all_tool_statuses()
    
    def get_system_resources(self) -> Dict[str, float]:
        """Get current system resources"""
        return self.resource_monitor.get_system_resources()
    
    def get_resource_level(self) -> ResourceLevel:
        """Get current resource level"""
        return self.resource_monitor.get_resource_level()
    
    def set_auto_scaling(self, enabled: bool):
        """Enable or disable auto-scaling"""
        self.auto_scaling_enabled = enabled
        self.save_configuration()
        logger.info(f"Auto-scaling {'enabled' if enabled else 'disabled'}")
    
    def update_tool_config(self, tool_name: str, **kwargs) -> bool:
        """Update tool configuration"""
        if tool_name not in self.configs:
            return False
        
        config = self.configs[tool_name]
        
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        self.save_configuration()
        logger.info(f"Updated configuration for tool: {tool_name}")
        return True
    
    def register_tool_factory(self, tool_name: str, factory: Callable):
        """Register a tool factory"""
        self.lifecycle_manager.register_tool_factory(tool_name, factory)
    
    async def cleanup(self):
        """Cleanup all tools and stop monitoring"""
        await self.stop_monitoring()
        
        # Stop all active tools
        for tool_name in list(self.lifecycle_manager.active_tools.keys()):
            await self.disable_tool(tool_name)
        
        logger.info("Dynamic MCP tool manager cleanup completed")


# Global instance
dynamic_tool_manager = DynamicMCPToolManager()

# Comprehensive tool registration system
def register_all_mcp_tools():
    """Register all available MCP tools with the dynamic tool manager."""
    
    # Tool mapping: config_name -> (module_path, class_name, description)
    tool_mappings = {
        # Monte Carlo and Simulation Tools
        "monte_carlo": ("src.mcp_servers.monte_carlo_mcp_tools", "MonteCarloMCPTools", "Monte Carlo simulation engine for risk assessment and scenario analysis"),
        "monte_carlo_visualization": ("src.mcp_servers.monte_carlo_visualization_mcp_tools", "get_monte_carlo_visualization_mcp_tools", "Monte Carlo visualization and charting tools"),
        "multi_domain_monte_carlo": ("src.mcp_servers.multi_domain_monte_carlo_mcp_tools", "MultiDomainMonteCarloMCPTools", "Multi-domain Monte Carlo simulation tools"),
        
        # Markdown Export Tools
        "simple_markdown_export": ("src.mcp_servers.simple_markdown_export_mcp_tools", "SimpleMarkdownExportMCPTools", "Simple markdown export tools for PDF and Word conversion"),
        "enhanced_markdown_export": ("src.mcp_servers.enhanced_markdown_export_mcp_tools", "EnhancedMarkdownExportMCPTools", "Enhanced markdown export tools with advanced formatting"),
        "markdown_export": ("src.mcp_servers.markdown_export_mcp_tools", "MarkdownExportMCPTools", "Comprehensive markdown export tools"),
        
        # Strategic and Intelligence Tools
        "strategic_intelligence_forecast": ("src.mcp_servers.strategic_intelligence_forecast_mcp_tools", "StrategicIntelligenceForecastMCPTools", "Strategic intelligence forecasting tools"),
        "force_projection": ("src.mcp_servers.force_projection_mcp_tools", "ForceProjectionMCPTools", "Force projection and military analysis tools"),
        "enhanced_analytics": ("src.mcp_servers.enhanced_mcp_tools", "EnhancedMCPTools", "Enhanced analytics and advanced features"),
        "interpretability": ("src.mcp_servers.phase5_interpretability_mcp_tools", "Phase5InterpretabilityMCPTools", "Interpretability and explainability tools"),
        
        # Visualization Tools
        "interactive_visualization": ("src.mcp_servers.interactive_visualization_mcp_tools", "InteractiveVisualizationMCPTools", "Interactive visualization and dashboard tools"),
        
        # Removed all problematic tools that cause import errors:
        # - audio_processing (consolidated_mcp_server import error)
        # - video_processing (consolidated_mcp_server import error)
        # - pdf_processing (consolidated_mcp_server import error)
        # - website_processing (consolidated_mcp_server import error)
        # - strategic_analysis (class not found)
        # - predictive_analytics (Position import error)
        # - scenario_analysis (Position import error)
        # - decision_support (Position import error)
        # - monitoring (Position import error)
        # - sentiment_analysis (class not found)
        # - language_processing (class not found)
        # - business_intelligence (class not found)
        # - deception_analysis (class not found)
        # - data_ingestion (class not found)
    }
    
    registered_count = 0
    failed_count = 0
    
    for tool_name, (module_path, class_name, description) in tool_mappings.items():
        try:
            # Import the module and class
            module = __import__(module_path, fromlist=[class_name])
            tool_class = getattr(module, class_name)
            
            # Create tool factory
            def create_tool_factory(tool_class):
                def factory():
                    return tool_class()
                return factory
            
            # Register the tool factory
            dynamic_tool_manager.register_tool_factory(tool_name, create_tool_factory(tool_class))
            
            # Add configuration if not already present
            if tool_name not in dynamic_tool_manager.configs:
                # Get default config from the configuration file
                config_data = dynamic_tool_manager.configs.get(tool_name, {})
                config = ToolConfig(
                    name=tool_name,
                    enabled=config_data.get("enabled", True),
                    priority=config_data.get("priority", 5),
                    max_cpu_percent=config_data.get("max_cpu_percent", 80.0),
                    max_memory_mb=config_data.get("max_memory_mb", 2048.0),
                    max_gpu_percent=config_data.get("max_gpu_percent", 90.0),
                    auto_scale=config_data.get("auto_scale", True),
                    dependencies=config_data.get("dependencies", []),
                    startup_timeout=config_data.get("startup_timeout", 30),
                    health_check_interval=config_data.get("health_check_interval", 60),
                    resource_check_interval=config_data.get("resource_check_interval", 10),
                    description=description
                )
                dynamic_tool_manager.configs[tool_name] = config
            
            registered_count += 1
            logger.info(f"✅ Registered MCP tool: {tool_name}")
            
        except ImportError as e:
            logger.warning(f"⚠️ Could not import {tool_name} from {module_path}.{class_name}: {e}")
            failed_count += 1
        except AttributeError as e:
            logger.warning(f"⚠️ Could not find class {class_name} in {module_path}: {e}")
            failed_count += 1
        except Exception as e:
            logger.error(f"❌ Error registering tool {tool_name}: {e}")
            failed_count += 1
    
    logger.info(f"✅ Registered {registered_count} MCP tools, {failed_count} failed")
    return registered_count, failed_count

# Register all available MCP tools
try:
    registered_count, failed_count = register_all_mcp_tools()
    logger.info(f"🎯 Total MCP tools registered: {registered_count}")
    if failed_count > 0:
        logger.warning(f"⚠️ {failed_count} tools failed to register")
except Exception as e:
    logger.error(f"❌ Error in comprehensive tool registration: {e}")

# Legacy registration for backward compatibility
try:
    from src.mcp_servers.interactive_visualization_mcp_tools import interactive_visualization_mcp_tools
    
    # Add visualization tools to the dynamic tool manager
    visualization_tools = [
        {
            "name": "interactive_visualization",
            "description": "Interactive visualization system for forecasting and prediction charts",
            "enabled": True,
            "priority": 7,
            "max_cpu_percent": 60.0,
            "max_memory_mb": 1024.0,
            "auto_scale": True,
            "dependencies": [],
            "startup_timeout": 30,
            "health_check_interval": 60,
            "resource_check_interval": 10
        }
    ]
    
    for tool_config in visualization_tools:
        config = ToolConfig(**tool_config)
        dynamic_tool_manager.configs[tool_config["name"]] = config
        
        # Register the tool factory
        def create_visualization_tool():
            return interactive_visualization_mcp_tools
        
        dynamic_tool_manager.register_tool_factory(tool_config["name"], create_visualization_tool)
    
    logger.info("✅ Interactive visualization tools registered with dynamic tool manager")
    
except ImportError as e:
    logger.warning(f"⚠️ Interactive visualization tools not available: {e}")
