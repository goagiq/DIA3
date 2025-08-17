#!/usr/bin/env python3
"""
MCP Tool Manager CLI
Command-line interface for managing MCP tools dynamically
"""

import sys
import os
import asyncio
import argparse
import json
from typing import List, Optional

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_servers.dynamic_tool_manager import dynamic_tool_manager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPToolManagerCLI:
    """CLI for managing MCP tools"""
    
    def __init__(self):
        self.manager = dynamic_tool_manager
    
    async def list_tools(self, show_resources: bool = False):
        """List all tools and their status"""
        try:
            tool_statuses = self.manager.get_all_tool_statuses()
            
            if not tool_statuses:
                print("No tools configured")
                return
            
            print(f"\n{'Tool Name':<20} {'Status':<12} {'Priority':<10} {'CPU %':<8} {'Memory MB':<12}")
            print("-" * 70)
            
            for tool_name, tool_info in tool_statuses.items():
                status = tool_info.status.value
                priority = tool_info.config.priority
                cpu_percent = tool_info.resource_usage.cpu_percent
                memory_mb = tool_info.resource_usage.memory_mb
                
                print(f"{tool_name:<20} {status:<12} {priority:<10} {cpu_percent:<8.1f} {memory_mb:<12.1f}")
            
            if show_resources:
                await self.show_system_resources()
                
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            print(f"Error: {e}")
    
    async def show_system_resources(self):
        """Show system resource usage"""
        try:
            resources = self.manager.get_system_resources()
            resource_level = self.manager.get_resource_level()
            
            print(f"\n{'System Resources':<20}")
            print("-" * 40)
            print(f"{'CPU Usage':<20} {resources.get('cpu_percent', 0):<10.1f}%")
            print(f"{'Memory Usage':<20} {resources.get('memory_percent', 0):<10.1f}%")
            print(f"{'Available Memory':<20} {resources.get('memory_available_mb', 0):<10.1f} MB")
            print(f"{'Disk Usage':<20} {resources.get('disk_percent', 0):<10.1f}%")
            print(f"{'Resource Level':<20} {resource_level.value}")
            
        except Exception as e:
            logger.error(f"Error showing system resources: {e}")
            print(f"Error: {e}")
    
    async def enable_tool(self, tool_name: str):
        """Enable a specific tool"""
        try:
            print(f"Enabling tool: {tool_name}")
            success = await self.manager.enable_tool(tool_name)
            
            if success:
                print(f"✅ Tool {tool_name} enabled successfully")
            else:
                print(f"❌ Failed to enable tool {tool_name}")
                
        except Exception as e:
            logger.error(f"Error enabling tool {tool_name}: {e}")
            print(f"Error: {e}")
    
    async def disable_tool(self, tool_name: str):
        """Disable a specific tool"""
        try:
            print(f"Disabling tool: {tool_name}")
            success = await self.manager.disable_tool(tool_name)
            
            if success:
                print(f"✅ Tool {tool_name} disabled successfully")
            else:
                print(f"❌ Failed to disable tool {tool_name}")
                
        except Exception as e:
            logger.error(f"Error disabling tool {tool_name}: {e}")
            print(f"Error: {e}")
    
    async def pause_tool(self, tool_name: str):
        """Pause a specific tool"""
        try:
            print(f"Pausing tool: {tool_name}")
            success = await self.manager.pause_tool(tool_name)
            
            if success:
                print(f"✅ Tool {tool_name} paused successfully")
            else:
                print(f"❌ Failed to pause tool {tool_name}")
                
        except Exception as e:
            logger.error(f"Error pausing tool {tool_name}: {e}")
            print(f"Error: {e}")
    
    async def resume_tool(self, tool_name: str):
        """Resume a specific tool"""
        try:
            print(f"Resuming tool: {tool_name}")
            success = await self.manager.resume_tool(tool_name)
            
            if success:
                print(f"✅ Tool {tool_name} resumed successfully")
            else:
                print(f"❌ Failed to resume tool {tool_name}")
                
        except Exception as e:
            logger.error(f"Error resuming tool {tool_name}: {e}")
            print(f"Error: {e}")
    
    async def enable_multiple_tools(self, tool_names: List[str]):
        """Enable multiple tools"""
        try:
            print(f"Enabling tools: {', '.join(tool_names)}")
            
            for tool_name in tool_names:
                success = await self.manager.enable_tool(tool_name)
                if success:
                    print(f"✅ {tool_name} enabled")
                else:
                    print(f"❌ {tool_name} failed to enable")
                    
        except Exception as e:
            logger.error(f"Error enabling multiple tools: {e}")
            print(f"Error: {e}")
    
    async def disable_multiple_tools(self, tool_names: List[str]):
        """Disable multiple tools"""
        try:
            print(f"Disabling tools: {', '.join(tool_names)}")
            
            for tool_name in tool_names:
                success = await self.manager.disable_tool(tool_name)
                if success:
                    print(f"✅ {tool_name} disabled")
                else:
                    print(f"❌ {tool_name} failed to disable")
                    
        except Exception as e:
            logger.error(f"Error disabling multiple tools: {e}")
            print(f"Error: {e}")
    
    async def set_auto_scaling(self, enabled: bool):
        """Enable or disable auto-scaling"""
        try:
            self.manager.set_auto_scaling(enabled)
            status = "enabled" if enabled else "disabled"
            print(f"✅ Auto-scaling {status}")
            
        except Exception as e:
            logger.error(f"Error setting auto-scaling: {e}")
            print(f"Error: {e}")
    
    async def start_monitoring(self):
        """Start resource monitoring"""
        try:
            await self.manager.start_monitoring()
            print("✅ Resource monitoring started")
            
        except Exception as e:
            logger.error(f"Error starting monitoring: {e}")
            print(f"Error: {e}")
    
    async def stop_monitoring(self):
        """Stop resource monitoring"""
        try:
            await self.manager.stop_monitoring()
            print("✅ Resource monitoring stopped")
            
        except Exception as e:
            logger.error(f"Error stopping monitoring: {e}")
            print(f"Error: {e}")
    
    async def show_health(self):
        """Show system health status"""
        try:
            tool_statuses = self.manager.get_all_tool_statuses()
            system_resources = self.manager.get_system_resources()
            
            total_tools = len(tool_statuses)
            active_tools = len([info for info in tool_statuses.values() 
                              if info.status.value in ['enabled', 'paused']])
            error_tools = len([info for info in tool_statuses.values() 
                             if info.status.value == 'error'])
            
            health_score = 100
            if total_tools > 0:
                health_score = ((active_tools - error_tools) / total_tools) * 100
            
            print(f"\n{'System Health Status':<20}")
            print("-" * 40)
            print(f"{'Health Score':<20} {health_score:<10.1f}%")
            print(f"{'Total Tools':<20} {total_tools}")
            print(f"{'Active Tools':<20} {active_tools}")
            print(f"{'Error Tools':<20} {error_tools}")
            print(f"{'CPU Usage':<20} {system_resources.get('cpu_percent', 0):<10.1f}%")
            print(f"{'Memory Usage':<20} {system_resources.get('memory_percent', 0):<10.1f}%")
            print(f"{'Monitoring':<20} {'Active' if self.manager.running else 'Inactive'}")
            print(f"{'Auto-scaling':<20} {'Enabled' if self.manager.auto_scaling_enabled else 'Disabled'}")
            
        except Exception as e:
            logger.error(f"Error showing health status: {e}")
            print(f"Error: {e}")
    
    async def update_tool_config(self, tool_name: str, **kwargs):
        """Update tool configuration"""
        try:
            success = self.manager.update_tool_config(tool_name, **kwargs)
            
            if success:
                print(f"✅ Configuration updated for {tool_name}")
            else:
                print(f"❌ Failed to update configuration for {tool_name}")
                
        except Exception as e:
            logger.error(f"Error updating tool config: {e}")
            print(f"Error: {e}")


async def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="MCP Tool Manager CLI")
    parser.add_argument("command", choices=[
        "list", "enable", "disable", "pause", "resume", 
        "enable-multiple", "disable-multiple", "resources", "health",
        "auto-scale", "start-monitoring", "stop-monitoring", "config"
    ], help="Command to execute")
    
    parser.add_argument("--tool", "-t", help="Tool name")
    parser.add_argument("--tools", "-T", nargs="+", help="Multiple tool names")
    parser.add_argument("--show-resources", "-r", action="store_true", help="Show system resources")
    parser.add_argument("--enabled", "-e", type=bool, help="Enable/disable auto-scaling")
    parser.add_argument("--priority", "-p", type=int, help="Tool priority (1-10)")
    parser.add_argument("--max-cpu", type=float, help="Maximum CPU percentage")
    parser.add_argument("--max-memory", type=float, help="Maximum memory in MB")
    
    args = parser.parse_args()
    
    cli = MCPToolManagerCLI()
    
    try:
        if args.command == "list":
            await cli.list_tools(args.show_resources)
            
        elif args.command == "enable":
            if not args.tool:
                print("Error: Tool name required")
                return
            await cli.enable_tool(args.tool)
            
        elif args.command == "disable":
            if not args.tool:
                print("Error: Tool name required")
                return
            await cli.disable_tool(args.tool)
            
        elif args.command == "pause":
            if not args.tool:
                print("Error: Tool name required")
                return
            await cli.pause_tool(args.tool)
            
        elif args.command == "resume":
            if not args.tool:
                print("Error: Tool name required")
                return
            await cli.resume_tool(args.tool)
            
        elif args.command == "enable-multiple":
            if not args.tools:
                print("Error: Tool names required")
                return
            await cli.enable_multiple_tools(args.tools)
            
        elif args.command == "disable-multiple":
            if not args.tools:
                print("Error: Tool names required")
                return
            await cli.disable_multiple_tools(args.tools)
            
        elif args.command == "resources":
            await cli.show_system_resources()
            
        elif args.command == "health":
            await cli.show_health()
            
        elif args.command == "auto-scale":
            if args.enabled is None:
                print("Error: --enabled parameter required")
                return
            await cli.set_auto_scaling(args.enabled)
            
        elif args.command == "start-monitoring":
            await cli.start_monitoring()
            
        elif args.command == "stop-monitoring":
            await cli.stop_monitoring()
            
        elif args.command == "config":
            if not args.tool:
                print("Error: Tool name required")
                return
            
            config_updates = {}
            if args.priority is not None:
                config_updates["priority"] = args.priority
            if args.max_cpu is not None:
                config_updates["max_cpu_percent"] = args.max_cpu
            if args.max_memory is not None:
                config_updates["max_memory_mb"] = args.max_memory
            
            if not config_updates:
                print("Error: No configuration updates specified")
                return
                
            await cli.update_tool_config(args.tool, **config_updates)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"CLI error: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
