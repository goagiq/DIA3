#!/usr/bin/env python3
"""
MCP Tool Manager
Script to enable/disable MCP tools and manage their configuration
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class MCPToolManager:
    """Manages MCP tool configuration"""
    
    def __init__(self, config_path: str = "mcp_tool_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load the MCP tool configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Configuration file not found: {self.config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in configuration file: {e}")
            sys.exit(1)
    
    def _save_config(self):
        """Save the configuration back to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"✅ Configuration saved to {self.config_path}")
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            sys.exit(1)
    
    def list_tools(self) -> None:
        """List all available tools and their status"""
        print("\n🔧 MCP Tools Status:")
        print("=" * 50)
        
        for tool_name, config in self.config.get("tools", {}).items():
            status = "🟢 ENABLED" if config.get("enabled", False) else "🔴 DISABLED"
            priority = config.get("priority", "N/A")
            print(f"{tool_name:25} | {status:12} | Priority: {priority}")
        
        print("=" * 50)
    
    def enable_tool(self, tool_name: str) -> None:
        """Enable a specific tool"""
        if tool_name not in self.config.get("tools", {}):
            print(f"❌ Tool '{tool_name}' not found")
            self._show_available_tools()
            return
        
        self.config["tools"][tool_name]["enabled"] = True
        self._save_config()
        print(f"✅ Tool '{tool_name}' enabled")
    
    def disable_tool(self, tool_name: str) -> None:
        """Disable a specific tool"""
        if tool_name not in self.config.get("tools", {}):
            print(f"❌ Tool '{tool_name}' not found")
            self._show_available_tools()
            return
        
        self.config["tools"][tool_name]["enabled"] = False
        self._save_config()
        print(f"✅ Tool '{tool_name}' disabled")
    
    def enable_all_tools(self) -> None:
        """Enable all tools"""
        for tool_name in self.config.get("tools", {}):
            self.config["tools"][tool_name]["enabled"] = True
        
        self._save_config()
        print("✅ All tools enabled")
    
    def disable_all_tools(self) -> None:
        """Disable all tools"""
        for tool_name in self.config.get("tools", {}):
            self.config["tools"][tool_name]["enabled"] = False
        
        self._save_config()
        print("✅ All tools disabled")
    
    def enable_core_tools(self) -> None:
        """Enable core tools for basic functionality"""
        core_tools = ["sentiment_analysis", "language_processing", "business_intelligence"]
        
        for tool_name in core_tools:
            if tool_name in self.config.get("tools", {}):
                self.config["tools"][tool_name]["enabled"] = True
        
        self._save_config()
        print("✅ Core tools enabled (sentiment_analysis, language_processing, business_intelligence)")
    
    def enable_advanced_tools(self) -> None:
        """Enable advanced tools for full functionality"""
        advanced_tools = ["monte_carlo", "deception_analysis", "multi_domain_monte_carlo"]
        
        for tool_name in advanced_tools:
            if tool_name in self.config.get("tools", {}):
                self.config["tools"][tool_name]["enabled"] = True
        
        self._save_config()
        print("✅ Advanced tools enabled (monte_carlo, deception_analysis, multi_domain_monte_carlo)")
    
    def _show_available_tools(self) -> None:
        """Show available tool names"""
        print("\n📋 Available tools:")
        for tool_name in self.config.get("tools", {}):
            print(f"  - {tool_name}")
    
    def show_tool_config(self, tool_name: str) -> None:
        """Show detailed configuration for a specific tool"""
        if tool_name not in self.config.get("tools", {}):
            print(f"❌ Tool '{tool_name}' not found")
            self._show_available_tools()
            return
        
        config = self.config["tools"][tool_name]
        print(f"\n🔧 Configuration for '{tool_name}':")
        print("=" * 40)
        for key, value in config.items():
            print(f"{key:25}: {value}")
    
    def test_tool_availability(self) -> None:
        """Test if enabled tools can be imported"""
        print("\n🧪 Testing tool availability...")
        
        enabled_tools = [
            name for name, config in self.config.get("tools", {}).items()
            if config.get("enabled", False)
        ]
        
        if not enabled_tools:
            print("⚠️  No tools are currently enabled")
            return
        
        for tool_name in enabled_tools:
            try:
                # Try to import the corresponding module
                if tool_name == "monte_carlo":
                    from core.monte_carlo.engine import MonteCarloEngine
                    print(f"✅ {tool_name}: MonteCarloEngine available")
                elif tool_name == "sentiment_analysis":
                    from core.semantic_similarity_analyzer import SemanticSimilarityAnalyzer
                    print(f"✅ {tool_name}: SemanticSimilarityAnalyzer available")
                elif tool_name == "language_processing":
                    from core.language_processing_service import LanguageProcessingService
                    print(f"✅ {tool_name}: LanguageProcessingService available")
                elif tool_name == "business_intelligence":
                    from core.business_metrics import BusinessMetrics
                    print(f"✅ {tool_name}: BusinessMetrics available")
                elif tool_name == "deception_analysis":
                    from core.enhanced_deception_detection_engine import EnhancedDeceptionDetectionEngine
                    print(f"✅ {tool_name}: EnhancedDeceptionDetectionEngine available")
                elif tool_name == "multi_domain_monte_carlo":
                    from core.multi_domain_monte_carlo_engine import MultiDomainMonteCarloEngine
                    print(f"✅ {tool_name}: MultiDomainMonteCarloEngine available")
                else:
                    print(f"⚠️  {tool_name}: Import test not implemented")
                    
            except ImportError as e:
                print(f"❌ {tool_name}: Import failed - {e}")
            except Exception as e:
                print(f"⚠️  {tool_name}: Error during test - {e}")


def show_usage():
    """Show usage information"""
    print("""
🔧 MCP Tool Manager

Usage:
  python mcp_tool_manager.py [command] [tool_name]

Commands:
  list                    - List all tools and their status
  enable <tool_name>      - Enable a specific tool
  disable <tool_name>     - Disable a specific tool
  enable-all              - Enable all tools
  disable-all             - Disable all tools
  enable-core             - Enable core tools only
  enable-advanced         - Enable advanced tools only
  config <tool_name>      - Show detailed config for a tool
  test                    - Test tool availability
  help                    - Show this help message

Examples:
  python mcp_tool_manager.py list
  python mcp_tool_manager.py enable monte_carlo
  python mcp_tool_manager.py disable sentiment_analysis
  python mcp_tool_manager.py enable-core
  python mcp_tool_manager.py test
""")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        show_usage()
        return
    
    manager = MCPToolManager()
    command = sys.argv[1].lower()
    
    if command == "list":
        manager.list_tools()
    
    elif command == "enable":
        if len(sys.argv) < 3:
            print("❌ Please specify a tool name")
            manager._show_available_tools()
            return
        manager.enable_tool(sys.argv[2])
    
    elif command == "disable":
        if len(sys.argv) < 3:
            print("❌ Please specify a tool name")
            manager._show_available_tools()
            return
        manager.disable_tool(sys.argv[2])
    
    elif command == "enable-all":
        manager.enable_all_tools()
    
    elif command == "disable-all":
        manager.disable_all_tools()
    
    elif command == "enable-core":
        manager.enable_core_tools()
    
    elif command == "enable-advanced":
        manager.enable_advanced_tools()
    
    elif command == "config":
        if len(sys.argv) < 3:
            print("❌ Please specify a tool name")
            manager._show_available_tools()
            return
        manager.show_tool_config(sys.argv[2])
    
    elif command == "test":
        manager.test_tool_availability()
    
    elif command == "help":
        show_usage()
    
    else:
        print(f"❌ Unknown command: {command}")
        show_usage()


if __name__ == "__main__":
    main()
