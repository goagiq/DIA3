"""
Modular Report MCP Tools

MCP tools for generating modular enhanced reports with configurable components.
Now includes integrated adaptive system for automatic data structure generation.
"""

from typing import Dict, Any, List, Optional
from mcp.types import CallToolResult

# Import modular report generator
try:
    from src.core.modular_report_generator import modular_report_generator
    MODULAR_REPORT_AVAILABLE = True
except ImportError as e:
    print(f"Modular report generator not available: {e}")
    MODULAR_REPORT_AVAILABLE = False

# Import integrated adaptive modular report generator
try:
    from src.core.integrated_adaptive_modular_report_generator import integrated_adaptive_modular_report_generator
    ADAPTIVE_MODULAR_REPORT_AVAILABLE = True
except ImportError as e:
    print(f"Integrated adaptive modular report generator not available: {e}")
    ADAPTIVE_MODULAR_REPORT_AVAILABLE = False


class ModularReportMCPTools:
    """MCP tools for modular report generation with adaptive capabilities."""
    
    def __init__(self):
        """Initialize the modular report MCP tools."""
        self.generator = modular_report_generator if MODULAR_REPORT_AVAILABLE else None
        self.adaptive_generator = integrated_adaptive_modular_report_generator if ADAPTIVE_MODULAR_REPORT_AVAILABLE else None
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools."""
        tools = []
        
        # Adaptive report generation (default)
        if ADAPTIVE_MODULAR_REPORT_AVAILABLE:
            tools.append({
                "name": "generate_adaptive_modular_report",
                "description": "Generate enhanced adaptive modular report with contextual intelligence and interactive visualizations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The analysis query with automatic context detection (e.g., 'AI Healthcare Innovation', 'Cybersecurity Strategy', 'Economic Analysis')"
                        },
                        "data": {
                            "type": "object",
                            "description": "Optional analysis data (system will generate adaptive data if not provided)"
                        },
                        "max_modules": {
                            "type": "integer",
                            "description": "Maximum number of modules to generate (e.g., 5 for top 5 most relevant modules)"
                        },
                        "modules": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific modules to include (e.g., ['executive_summary', 'risk_assessment'])"
                        },
                        "module_categories": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Module categories to include (e.g., ['strategic', 'operational'])"
                        }
                    },
                    "required": ["query"]
                }
            })
        
        # Original modular report generation
        if MODULAR_REPORT_AVAILABLE:
            tools.append({
                "name": "generate_modular_enhanced_report",
                "description": "Generate a modular enhanced report with configurable components",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "The analysis topic"
                        },
                        "data": {
                            "type": "object",
                            "description": "Analysis data for all modules"
                        },
                        "enabled_modules": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of module IDs to enable (optional)"
                        },
                        "report_title": {
                            "type": "string",
                            "description": "Custom report title (optional)"
                        },
                        "custom_config": {
                            "type": "object",
                            "description": "Custom configuration for modules (optional)"
                        }
                    },
                    "required": ["topic", "data"]
                }
            })
        
        # Module management tools
        if MODULAR_REPORT_AVAILABLE:
            tools.extend([
                {
                    "name": "get_modular_report_modules",
                    "description": "Get list of available modules and their configurations",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                {
                    "name": "configure_modular_report_module",
                    "description": "Configure a specific module with custom settings",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "module_id": {
                                "type": "string",
                                "description": "Module ID to configure"
                            },
                            "config": {
                                "type": "object",
                                "description": "Configuration settings for the module"
                            }
                        },
                        "required": ["module_id", "config"]
                    }
                },
                {
                    "name": "enable_modular_report_modules",
                    "description": "Enable or disable specific modules",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "module_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of module IDs to enable"
                            },
                            "enabled": {
                                "type": "boolean",
                                "description": "Whether to enable or disable the modules"
                            }
                        },
                        "required": ["module_ids", "enabled"]
                    }
                }
            ])
        
        return tools
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> CallToolResult:
        """Call the specified tool with the given arguments."""
        
        try:
            if name == "generate_adaptive_modular_report":
                return await self._generate_adaptive_modular_report(arguments)
            elif name == "generate_modular_enhanced_report":
                return await self._generate_modular_enhanced_report(arguments)
            elif name == "get_modular_report_modules":
                return await self._get_modular_report_modules(arguments)
            elif name == "configure_modular_report_module":
                return await self._configure_modular_report_module(arguments)
            elif name == "enable_modular_report_modules":
                return await self._enable_modular_report_modules(arguments)
            else:
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": f"Unknown tool: {name}"
                    }]
                )
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"Error calling tool {name}: {str(e)}"
                }]
            )
    
    async def _generate_adaptive_modular_report(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Generate adaptive modular report with configurable module selection."""
        if not ADAPTIVE_MODULAR_REPORT_AVAILABLE:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Adaptive modular report generator not available"
                }]
            )
        
        query = arguments.get("query", "")
        data = arguments.get("data", {})
        max_modules = arguments.get("max_modules")
        modules = arguments.get("modules")
        module_categories = arguments.get("module_categories")
        
        if not query:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Query is required for adaptive report generation"
                }]
            )
        
        try:
            result = await self.adaptive_generator.generate_adaptive_report(
                query, data, max_modules, modules, module_categories
            )
            
            if result['success']:
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": f"✅ Successfully generated adaptive modular report\n"
                               f"📁 File: {result['file_path']}\n"
                               f"📊 Data sections: {result['universal_data_sections']}\n"
                               f"🔄 Modules generated: {result['modules_generated']}\n"
                               f"🎯 Query: {result['query']}"
                    }]
                )
            else:
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": f"❌ Failed to generate adaptive report: {result.get('error', 'Unknown error')}"
                    }]
                )
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error generating adaptive report: {str(e)}"
                }]
            )
    
    async def _generate_modular_enhanced_report(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Generate modular enhanced report with configurable components."""
        if not MODULAR_REPORT_AVAILABLE:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Modular report generator not available"
                }]
            )
        
        topic = arguments.get("topic", "")
        data = arguments.get("data", {})
        enabled_modules = arguments.get("enabled_modules", [])
        report_title = arguments.get("report_title", "")
        custom_config = arguments.get("custom_config", {})
        
        if not topic or not data:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Topic and data are required for modular report generation"
                }]
            )
        
        try:
            result = await self.generator.generate_modular_report(
                topic=topic,
                data=data,
                enabled_modules=enabled_modules,
                report_title=report_title,
                custom_config=custom_config
            )
            
            if result['success']:
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": f"✅ Successfully generated modular enhanced report\n"
                               f"📁 File: {result['file_path']}\n"
                               f"📊 Modules: {len(result.get('modules', []))}\n"
                               f"🎯 Topic: {topic}"
                    }]
                )
            else:
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": f"❌ Failed to generate modular report: {result.get('error', 'Unknown error')}"
                    }]
                )
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error generating modular report: {str(e)}"
                }]
            )
    
    async def _get_modular_report_modules(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get list of available modules and their configurations."""
        if not MODULAR_REPORT_AVAILABLE:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Modular report generator not available"
                }]
            )
        
        try:
            modules = self.generator.get_available_modules()
            module_info = []
            
            for module_id, module in modules.items():
                module_info.append(f"• {module_id}: {module.get('title', 'No title')}")
            
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"📋 Available Modules ({len(modules)}):\n" + "\n".join(module_info)
                }]
            )
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error getting modules: {str(e)}"
                }]
            )
    
    async def _configure_modular_report_module(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Configure a specific module with custom settings."""
        if not MODULAR_REPORT_AVAILABLE:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Modular report generator not available"
                }]
            )
        
        module_id = arguments.get("module_id", "")
        config = arguments.get("config", {})
        
        if not module_id or not config:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Module ID and config are required for module configuration"
                }]
            )
        
        try:
            # Configure the module
            self.generator.configure_module(module_id, config)
            
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"✅ Successfully configured module: {module_id}"
                }]
            )
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error configuring module: {str(e)}"
                }]
            )
    
    async def _enable_modular_report_modules(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Enable or disable specific modules."""
        if not MODULAR_REPORT_AVAILABLE:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Modular report generator not available"
                }]
            )
        
        module_ids = arguments.get("module_ids", [])
        enabled = arguments.get("enabled", True)
        
        if not module_ids:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Module IDs are required for enabling/disabling modules"
                }]
            )
        
        try:
            for module_id in module_ids:
                self.generator.set_module_enabled(module_id, enabled)
            
            status = "enabled" if enabled else "disabled"
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"✅ Successfully {status} modules: {', '.join(module_ids)}"
                }]
            )
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error enabling/disabling modules: {str(e)}"
                }]
            )


# Global instance for easy access
modular_report_mcp_tools = ModularReportMCPTools()
