"""
Modular Report MCP Tools

MCP tools for generating modular enhanced reports with configurable components.
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


class ModularReportMCPTools:
    """MCP tools for modular report generation."""
    
    def __init__(self):
        """Initialize the modular report MCP tools."""
        self.generator = modular_report_generator if MODULAR_REPORT_AVAILABLE else None
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools."""
        if not MODULAR_REPORT_AVAILABLE or self.generator is None:
            return []
        
        return [
            {
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
            },
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
                        "disable_others": {
                            "type": "boolean",
                            "description": "Whether to disable all other modules"
                        }
                    },
                    "required": ["module_ids"]
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> CallToolResult:
        """Call a specific MCP tool."""
        if not MODULAR_REPORT_AVAILABLE or self.generator is None:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": "Modular report generator is not available"
                }]
            )
        
        if name == "generate_modular_enhanced_report":
            return await self._handle_generate_modular_report(arguments)
        elif name == "get_modular_report_modules":
            return await self._handle_get_modules(arguments)
        elif name == "configure_modular_report_module":
            return await self._handle_configure_module(arguments)
        elif name == "enable_modular_report_modules":
            return await self._handle_enable_modules(arguments)
        else:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"Unknown tool: {name}"
                }]
            )
    
    async def _handle_generate_modular_report(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle modular report generation."""
        try:
            topic = arguments.get("topic")
            data = arguments.get("data", {})
            enabled_modules = arguments.get("enabled_modules")
            report_title = arguments.get("report_title")
            custom_config = arguments.get("custom_config")
            
            if not topic:
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": "Topic is required for report generation"
                    }]
                )
            
            result = await self.generator.generate_modular_report(
                topic=topic,
                data=data,
                enabled_modules=enabled_modules,
                report_title=report_title,
                custom_config=custom_config
            )
            
            if result.get("success"):
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": f"✅ Modular enhanced report generated successfully!\n\n"
                               f"📄 File: {result.get('filename')}\n"
                               f"📁 Path: {result.get('file_path')}\n"
                               f"📊 Size: {result.get('file_size')} bytes\n"
                               f"🔧 Modules Used: {', '.join(result.get('modules_used', []))}\n"
                               f"⏰ Generated: {result.get('generated_at')}"
                    }]
                )
            else:
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": f"❌ Failed to generate modular report: {result.get('error')}"
                    }]
                )
                
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error generating modular report: {str(e)}"
                }]
            )
    
    async def _handle_get_modules(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle getting available modules."""
        try:
            available_modules = self.generator.get_available_modules()
            enabled_modules = [m.module_id for m in self.generator.get_enabled_modules()]
            
            module_details = []
            for module_id in available_modules:
                module = self.generator.get_module(module_id)
                if module:
                    metadata = module.get_module_metadata()
                    module_details.append({
                        "module_id": module_id,
                        "title": metadata.get("title", ""),
                        "description": metadata.get("description", ""),
                        "enabled": metadata.get("enabled", False),
                        "order": metadata.get("order", 0),
                        "required_data_keys": metadata.get("required_data_keys", [])
                    })
            
            # Sort by order
            module_details.sort(key=lambda x: x["order"])
            
            modules_text = "\n".join([
                f"🔧 {m['module_id']}: {m['title']} ({'✅ Enabled' if m['enabled'] else '❌ Disabled'})"
                for m in module_details
            ])
            
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"📊 Available Modular Report Modules:\n\n{modules_text}\n\n"
                           f"Total Modules: {len(available_modules)}\n"
                           f"Enabled Modules: {len(enabled_modules)}"
                }]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error getting modules: {str(e)}"
                }]
            )
    
    async def _handle_configure_module(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle module configuration."""
        try:
            module_id = arguments.get("module_id")
            config = arguments.get("config", {})
            
            if not module_id:
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": "Module ID is required for configuration"
                    }]
                )
            
            module = self.generator.get_module(module_id)
            if not module:
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": f"Module '{module_id}' not found"
                    }]
                )
            
            self.generator.configure_module(module_id, config)
            
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"✅ Module '{module_id}' configured successfully"
                }]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error configuring module: {str(e)}"
                }]
            )
    
    async def _handle_enable_modules(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle enabling/disabling modules."""
        try:
            module_ids = arguments.get("module_ids", [])
            disable_others = arguments.get("disable_others", False)
            
            if not module_ids:
                return CallToolResult(
                    content=[{
                        "type": "text",
                        "text": "Module IDs are required"
                    }]
                )
            
            # Disable all modules first if requested
            if disable_others:
                for module_id in self.generator.get_available_modules():
                    self.generator.enable_module(module_id, False)
            
            # Enable specified modules
            for module_id in module_ids:
                self.generator.enable_module(module_id, True)
            
            enabled_modules = [m.module_id for m in self.generator.get_enabled_modules()]
            
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"✅ Modules configured successfully!\n\n"
                           f"Enabled Modules: {', '.join(enabled_modules)}"
                }]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[{
                    "type": "text",
                    "text": f"❌ Error enabling modules: {str(e)}"
                }]
            )


# Global instance for easy access
modular_report_mcp_tools = ModularReportMCPTools()
