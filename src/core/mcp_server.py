"""
MCP Server implementation for the sentiment analysis system.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from loguru import logger

# Import the real Strands MCP client
from src.core.strands_mcp_client import StrandsMCPClient, create_mcp_agent, create_mcp_swarm


class MCPServer:
    """MCP Server implementation using Strands MCP client."""
    
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.host = host
        self.port = port
        self.strands_mcp_client = StrandsMCPClient()
        self.agents = {}
        self.swarms = {}
        self.is_running = False
        
        logger.info(f"Initializing MCP Server on {host}:{port} with StrandsMCPClient")
    
    def get_tools_info(self) -> List[Dict[str, Any]]:
        """Get information about available MCP tools."""
        try:
            tools = self.strands_mcp_client.get_tools_sync()
            logger.info(f"✅ Retrieved {len(tools)} tools from MCP server")
            return tools
                except Exception as e:
            logger.error(f"❌ Failed to get tools info: {e}")
            return []
    
    def create_agent(self, name: str, system_prompt: str = None) -> Any:
        """Create an agent with MCP tools."""
        try:
            agent = create_mcp_agent(name, system_prompt)
            self.agents[name] = agent
            logger.info(f"✅ Created agent '{name}' with MCP tools")
            return agent
        except Exception as e:
            logger.error(f"❌ Failed to create agent '{name}': {e}")
            raise
    
    def create_swarm(self, agents: List[Any], name: str = "swarm") -> Any:
        """Create a swarm with MCP-enabled agents."""
        try:
            swarm = create_mcp_swarm(agents, name)
            self.swarms[name] = swarm
            logger.info(f"✅ Created swarm '{name}' with {len(agents)} agents")
            return swarm
                except Exception as e:
            logger.error(f"❌ Failed to create swarm '{name}': {e}")
            raise
    
    async def run_agent(self, agent_name: str, prompt: str) -> str:
        """Run an agent asynchronously."""
        try:
            from src.core.strands_mcp_client import run_mcp_agent
            result = await run_mcp_agent(agent_name, prompt)
            logger.info(f"✅ Agent '{agent_name}' completed execution")
            return result
                        except Exception as e:
            logger.error(f"❌ Failed to run agent '{agent_name}': {e}")
            raise
                    
    def get_server_status(self) -> Dict[str, Any]:
        """Get server status."""
                    return {
            "host": self.host,
            "port": self.port,
            "is_running": self.is_running,
            "agents_count": len(self.agents),
            "swarms_count": len(self.swarms),
            "available_tools": len(self.get_tools_info()),
            "mcp_client_status": self.strands_mcp_client.get_agent_status()
        }
    
    def start(self):
        """Start the MCP server."""
        self.is_running = True
        logger.info(f"✅ MCP Server started on {self.host}:{self.port}")
    
    def stop(self):
        """Stop the MCP server."""
        self.is_running = False
        logger.info("✅ MCP Server stopped")


# Global MCP server instance
mcp_server = MCPServer()
