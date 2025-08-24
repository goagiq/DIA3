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

# Import adaptive data adapter
try:
    from src.core.adaptive_data_adapter import adaptive_data_adapter
    ADAPTIVE_DATA_ADAPTER_AVAILABLE = True
except ImportError as e:
    print(f"Adaptive data adapter not available: {e}")
    ADAPTIVE_DATA_ADAPTER_AVAILABLE = False

# Import modular report modules configuration
try:
    from src.config.modular_report_modules_config import modular_report_modules_config
    MODULAR_CONFIG_AVAILABLE = True
except ImportError as e:
    print(f"Modular report modules configuration not available: {e}")
    MODULAR_CONFIG_AVAILABLE = False


class ModularReportMCPTools:
    """MCP tools for modular report generation with adaptive capabilities."""
    
    def __init__(self):
        """Initialize the modular report MCP tools."""
        self.generator = modular_report_generator if MODULAR_REPORT_AVAILABLE else None
        self.adaptive_generator = integrated_adaptive_modular_report_generator if ADAPTIVE_MODULAR_REPORT_AVAILABLE else None
        self.data_adapter = adaptive_data_adapter if ADAPTIVE_DATA_ADAPTER_AVAILABLE else None
        self.config = modular_report_modules_config if MODULAR_CONFIG_AVAILABLE else None
    
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
        
        # Adaptive data handling tools
        if ADAPTIVE_DATA_ADAPTER_AVAILABLE:
            tools.extend([
                {
                    "name": "adapt_data_for_module",
                    "description": "Adapt data for specific module with contextual intelligence",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "object",
                                "description": "Input data (string or dict)"
                            },
                            "module_id": {
                                "type": "string",
                                "description": "Target module ID"
                            }
                        },
                        "required": ["data", "module_id"]
                    }
                },
                {
                    "name": "detect_data_structure",
                    "description": "Detect data structure type and context domain",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "object",
                                "description": "Input data to analyze"
                            }
                        },
                        "required": ["data"]
                    }
                }
            ])
        
        # Configuration management tools
        if MODULAR_CONFIG_AVAILABLE:
            tools.extend([
                {
                    "name": "get_modules_by_context",
                    "description": "Get modules that support a specific context domain",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "context": {
                                "type": "string",
                                "description": "Context domain (healthcare, technology, finance, geopolitical, military, economic, cybersecurity, general)"
                            }
                        },
                        "required": ["context"]
                    }
                },
                {
                    "name": "get_modules_by_data_structure",
                    "description": "Get modules that support a specific data structure",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "data_structure": {
                                "type": "string",
                                "description": "Data structure type (string, dict, mixed)"
                            }
                        },
                        "required": ["data_structure"]
                    }
                },
                {
                    "name": "save_modular_config",
                    "description": "Save modular report configuration to file",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to save configuration file"
                            }
                        },
                        "required": ["file_path"]
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
            elif name == "adapt_data_for_module":
                return await self._adapt_data_for_module(arguments)
            elif name == "detect_data_structure":
                return await self._detect_data_structure(arguments)
            elif name == "get_modules_by_context":
                return await self._get_modules_by_context(arguments)
            elif name == "get_modules_by_data_structure":
                return await self._get_modules_by_data_structure(arguments)
            elif name == "save_modular_config":
                return await self._save_modular_config(arguments)
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
    
    async def _adapt_data_for_module(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Adapt data for specific module with contextual intelligence."""
        if not ADAPTIVE_DATA_ADAPTER_AVAILABLE:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Adaptive data adapter not available"
                }]
            )
        
        data = arguments.get("data", {})
        module_id = arguments.get("module_id", "")
        
        if not data or not module_id:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Data and module_id are required for data adaptation"
                }]
            )
        
        try:
            adapted_data = self.data_adapter.adapt_for_module(data, module_id)
            
            if "error" in adapted_data:
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": f"❌ Error adapting data: {adapted_data['error']}"
                    }]
                )
            
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"✅ Successfully adapted data for module: {module_id}\n"
                           f"📊 Structure type: {adapted_data.get('structure_type', 'unknown')}\n"
                           f"🎯 Context domain: {adapted_data.get('context_domain', 'unknown')}\n"
                           f"📈 Confidence: {adapted_data.get('confidence', 0.0):.2f}"
                }]
            )
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error adapting data: {str(e)}"
                }]
            )
    
    async def _detect_data_structure(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Detect data structure type and context domain."""
        if not ADAPTIVE_DATA_ADAPTER_AVAILABLE:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Adaptive data adapter not available"
                }]
            )
        
        data = arguments.get("data", {})
        
        if not data:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Data is required for structure detection"
                }]
            )
        
        try:
            structure_info = self.data_adapter.detect_data_structure(data)
            
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"🔍 Data Structure Analysis:\n"
                           f"📊 Structure type: {structure_info.structure_type.value}\n"
                           f"🎯 Context domain: {structure_info.context_domain.value}\n"
                           f"📈 Confidence: {structure_info.confidence:.2f}\n"
                           f"🔑 Detected keys: {structure_info.detected_keys or 'N/A'}"
                }]
            )
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error detecting data structure: {str(e)}"
                }]
            )
    
    async def _get_modules_by_context(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get modules that support a specific context domain."""
        if not MODULAR_CONFIG_AVAILABLE:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Modular report modules configuration not available"
                }]
            )
        
        context = arguments.get("context", "").upper()
        
        if not context:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Context is required for module filtering"
                }]
            )
        
        try:
            from src.config.modular_report_modules_config import ContextDomain
            
            context_domain = getattr(ContextDomain, context, ContextDomain.GENERAL)
            modules = self.config.get_modules_by_context(context_domain)
            
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"📋 Modules for {context} context ({len(modules)}):\n" + "\n".join([f"• {module}" for module in modules])
                }]
            )
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error getting modules by context: {str(e)}"
                }]
            )
    
    async def _get_modules_by_data_structure(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get modules that support a specific data structure."""
        if not MODULAR_CONFIG_AVAILABLE:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Modular report modules configuration not available"
                }]
            )
        
        data_structure = arguments.get("data_structure", "").upper()
        
        if not data_structure:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Data structure is required for module filtering"
                }]
            )
        
        try:
            from src.config.modular_report_modules_config import DataStructureType
            
            structure_type = getattr(DataStructureType, data_structure, DataStructureType.STRING)
            modules = self.config.get_modules_by_data_structure(structure_type)
            
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"📋 Modules for {data_structure} data structure ({len(modules)}):\n" + "\n".join([f"• {module}" for module in modules])
                }]
            )
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error getting modules by data structure: {str(e)}"
                }]
            )
    
    async def _save_modular_config(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Save modular report configuration to file."""
        if not MODULAR_CONFIG_AVAILABLE:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Modular report modules configuration not available"
                }]
            )
        
        file_path = arguments.get("file_path", "")
        
        if not file_path:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "File path is required for saving configuration"
                }]
            )
        
        try:
            self.config.save_config(file_path)
            
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"✅ Successfully saved modular configuration to: {file_path}"
                }]
            )
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error saving configuration: {str(e)}"
                }]
            )


# Global instance for easy access
modular_report_mcp_tools = ModularReportMCPTools()
