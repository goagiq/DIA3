#!/usr/bin/env python3
"""
Integrated MCP Manager CLI
Command-line interface for managing all MCP tools with dynamic resource optimization
"""

import sys
import os
import asyncio
import argparse
import logging
from typing import List, Optional

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_servers.integrated_dynamic_mcp_manager import integrated_mcp_manager
from mcp_servers.dynamic_tool_manager import ToolStatus, ResourceLevel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntegratedMCPManagerCLI:
    """CLI for managing all MCP tools with integrated dynamic management"""

    def __init__(self):
        self.manager = integrated_mcp_manager

    async def list_tools(self, show_resources: bool = False):
        """List all available tools and their status"""
        print("\n🔧 Available MCP Tools")
        print("=" * 80)
        
        statuses = self.manager.get_all_tool_statuses()
        available_tools = await self.manager.get_available_tools()
        
        if not available_tools:
            print("No tools available")
            return
        
        # Print header
        header = f"{'Tool Name':<20} {'Status':<12} {'Priority':<10}"
        if show_resources:
            header += f"{'CPU %':<8} {'Memory MB':<12}"
        print(header)
        print("-" * 80)
        
        for tool_name in available_tools:
            status_info = statuses.get(tool_name)
            if status_info:
                status = status_info.status.value
                priority = status_info.config.priority
                line = f"{tool_name:<20} {status:<12} {priority:<10}"
                
                if show_resources:
                    cpu = status_info.resource_usage.cpu_percent
                    memory = status_info.resource_usage.memory_mb
                    line += f"{cpu:<8.1f} {memory:<12.1f}"
                
                print(line)
            else:
                print(f"{tool_name:<20} {'Not Configured':<12} {'N/A':<10}")
        
        print(f"\nTotal Tools: {len(available_tools)}")
        enabled_count = len([s for s in statuses.values() if s.status == ToolStatus.ENABLED])
        print(f"Enabled: {enabled_count}")

    async def show_resources(self):
        """Show system resources"""
        resources = self.manager.get_system_resources()
        resource_level = self.manager.get_resource_level()
        
        print("\n💻 System Resources")
        print("=" * 40)
        print(f"CPU Usage:        {resources.get('cpu_percent', 0):.1f}%")
        print(f"Memory Usage:     {resources.get('memory_percent', 0):.1f}%")
        print(f"Available Memory: {resources.get('memory_available_mb', 0):.1f} MB")
        print(f"Resource Level:   {resource_level.value}")
        
        # Show resource level indicators
        level_indicators = {
            ResourceLevel.LOW: "🟢 Low",
            ResourceLevel.MEDIUM: "🟡 Medium", 
            ResourceLevel.HIGH: "🟠 High",
            ResourceLevel.CRITICAL: "🔴 Critical"
        }
        print(f"Status:           {level_indicators.get(resource_level, 'Unknown')}")

    async def show_health(self):
        """Show system health status"""
        statuses = self.manager.get_all_tool_statuses()
        resources = self.manager.get_system_resources()
        
        print("\n🏥 System Health")
        print("=" * 40)
        
        # Calculate health metrics
        total_tools = len(statuses)
        enabled_tools = len([s for s in statuses.values() if s.status == ToolStatus.ENABLED])
        error_tools = len([s for s in statuses.values() if s.status == ToolStatus.ERROR])
        paused_tools = len([s for s in statuses.values() if s.status == ToolStatus.PAUSED])
        
        # Health score calculation
        health_score = 0
        if total_tools > 0:
            health_score = ((enabled_tools / total_tools) * 0.6 + 
                          (1 - (error_tools / total_tools)) * 0.4) * 100
        
        print(f"Health Score:     {health_score:.1f}%")
        print(f"Active Tools:     {enabled_tools}/{total_tools}")
        print(f"Error Tools:      {error_tools}")
        print(f"Paused Tools:     {paused_tools}")
        print(f"CPU Usage:        {resources.get('cpu_percent', 0):.1f}%")
        print(f"Memory Usage:     {resources.get('memory_percent', 0):.1f}%")

    async def enable_tool(self, tool_name: str):
        """Enable a specific tool"""
        print(f"\n🚀 Enabling tool: {tool_name}")
        success = await self.manager.enable_tool(tool_name)
        if success:
            print(f"✅ Successfully enabled {tool_name}")
        else:
            print(f"❌ Failed to enable {tool_name}")

    async def disable_tool(self, tool_name: str):
        """Disable a specific tool"""
        print(f"\n🛑 Disabling tool: {tool_name}")
        success = await self.manager.disable_tool(tool_name)
        if success:
            print(f"✅ Successfully disabled {tool_name}")
        else:
            print(f"❌ Failed to disable {tool_name}")

    async def pause_tool(self, tool_name: str):
        """Pause a specific tool"""
        print(f"\n⏸️ Pausing tool: {tool_name}")
        success = await self.manager.pause_tool(tool_name)
        if success:
            print(f"✅ Successfully paused {tool_name}")
        else:
            print(f"❌ Failed to pause {tool_name}")

    async def resume_tool(self, tool_name: str):
        """Resume a specific tool"""
        print(f"\n▶️ Resuming tool: {tool_name}")
        success = await self.manager.resume_tool(tool_name)
        if success:
            print(f"✅ Successfully resumed {tool_name}")
        else:
            print(f"❌ Failed to resume {tool_name}")

    async def enable_multiple_tools(self, tool_names: List[str]):
        """Enable multiple tools"""
        print(f"\n🚀 Enabling multiple tools: {', '.join(tool_names)}")
        for tool_name in tool_names:
            success = await self.manager.enable_tool(tool_name)
            status = "✅" if success else "❌"
            print(f"{status} {tool_name}")

    async def disable_multiple_tools(self, tool_names: List[str]):
        """Disable multiple tools"""
        print(f"\n🛑 Disabling multiple tools: {', '.join(tool_names)}")
        for tool_name in tool_names:
            success = await self.manager.disable_tool(tool_name)
            status = "✅" if success else "❌"
            print(f"{status} {tool_name}")

    async def set_auto_scaling(self, enabled: bool):
        """Enable or disable auto-scaling"""
        self.manager.set_auto_scaling(enabled)
        status = "enabled" if enabled else "disabled"
        print(f"\n⚖️ Auto-scaling {status}")

    async def optimize_workload(self, workload_type: str):
        """Optimize for specific workload type"""
        print(f"\n🎯 Optimizing for {workload_type} workload")
        try:
            await self.manager.optimize_for_workload(workload_type)
            print(f"✅ Successfully optimized for {workload_type}")
        except ValueError as e:
            print(f"❌ {e}")
            print("Available workload types: monte_carlo_heavy, multimedia_heavy, analysis_heavy, lightweight")

    async def start_monitoring(self):
        """Start resource monitoring"""
        print("\n📡 Starting resource monitoring...")
        # Monitoring is already started in the manager
        print("✅ Monitoring is active")

    async def stop_monitoring(self):
        """Stop resource monitoring"""
        print("\n🛑 Stopping resource monitoring...")
        await self.manager.dynamic_manager.stop_monitoring()
        print("✅ Monitoring stopped")

    async def show_config(self):
        """Show current configuration"""
        print("\n⚙️ Current Configuration")
        print("=" * 40)
        
        statuses = self.manager.get_all_tool_statuses()
        for tool_name, status_info in statuses.items():
            config = status_info.config
            print(f"\n{tool_name}:")
            print(f"  Priority: {config.priority}")
            print(f"  Max CPU: {config.max_cpu_percent}%")
            print(f"  Max Memory: {config.max_memory_mb} MB")
            print(f"  Auto-scale: {config.auto_scale}")
            print(f"  Description: {config.description}")


async def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Integrated MCP Tool Manager CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python integrated_mcp_manager.py list                    # List all tools
  python integrated_mcp_manager.py list --show-resources   # List with resource usage
  python integrated_mcp_manager.py enable monte_carlo      # Enable Monte Carlo tools
  python integrated_mcp_manager.py disable video_processing # Disable video processing
  python integrated_mcp_manager.py optimize monte_carlo_heavy # Optimize for Monte Carlo workload
  python integrated_mcp_manager.py resources               # Show system resources
  python integrated_mcp_manager.py health                  # Show system health
        """
    )
    
    parser.add_argument(
        'command',
        choices=[
            'list', 'enable', 'disable', 'pause', 'resume',
            'enable-multiple', 'disable-multiple', 'resources', 'health',
            'auto-scale', 'optimize', 'start-monitoring', 'stop-monitoring', 'config'
        ],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--tool', '-t',
        help='Tool name'
    )
    
    parser.add_argument(
        '--tools', '-T',
        nargs='+',
        help='Multiple tool names'
    )
    
    parser.add_argument(
        '--show-resources', '-r',
        action='store_true',
        help='Show system resources'
    )
    
    parser.add_argument(
        '--enabled', '-e',
        type=str,
        choices=['true', 'false'],
        help='Enable/disable auto-scaling'
    )
    
    parser.add_argument(
        '--workload-type', '-w',
        help='Workload type for optimization'
    )
    
    args = parser.parse_args()
    
    cli = IntegratedMCPManagerCLI()
    
    try:
        if args.command == 'list':
            await cli.list_tools(args.show_resources)
        
        elif args.command == 'resources':
            await cli.show_resources()
        
        elif args.command == 'health':
            await cli.show_health()
        
        elif args.command == 'enable':
            if not args.tool:
                print("❌ Error: --tool argument required")
                return
            await cli.enable_tool(args.tool)
        
        elif args.command == 'disable':
            if not args.tool:
                print("❌ Error: --tool argument required")
                return
            await cli.disable_tool(args.tool)
        
        elif args.command == 'pause':
            if not args.tool:
                print("❌ Error: --tool argument required")
                return
            await cli.pause_tool(args.tool)
        
        elif args.command == 'resume':
            if not args.tool:
                print("❌ Error: --tool argument required")
                return
            await cli.resume_tool(args.tool)
        
        elif args.command == 'enable-multiple':
            if not args.tools:
                print("❌ Error: --tools argument required")
                return
            await cli.enable_multiple_tools(args.tools)
        
        elif args.command == 'disable-multiple':
            if not args.tools:
                print("❌ Error: --tools argument required")
                return
            await cli.disable_multiple_tools(args.tools)
        
        elif args.command == 'auto-scale':
            if not args.enabled:
                print("❌ Error: --enabled argument required (true/false)")
                return
            enabled = args.enabled.lower() == 'true'
            await cli.set_auto_scaling(enabled)
        
        elif args.command == 'optimize':
            if not args.workload_type:
                print("❌ Error: --workload-type argument required")
                return
            await cli.optimize_workload(args.workload_type)
        
        elif args.command == 'start-monitoring':
            await cli.start_monitoring()
        
        elif args.command == 'stop-monitoring':
            await cli.stop_monitoring()
        
        elif args.command == 'config':
            await cli.show_config()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"CLI error: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
