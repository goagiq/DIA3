"""
MCP Orchestrator implementation based on sentiment-swarm-agents pattern.
This follows the proper MCP tool integration and swarm orchestration approach.
"""

from typing import List, Dict, Any, Optional
from loguru import logger

# Import the real Strands MCP client
from src.core.strands_mcp_client import (
    StrandsMCPClient, create_mcp_agent, create_mcp_swarm
)


class MCPOrchestrator:
    """MCP Orchestrator following the sentiment-swarm-agents pattern."""
    
    def __init__(self):
        self.strands_mcp_client = StrandsMCPClient()
        self.agents = {}
        self.swarms = {}
        self.tools = {}
        self.mcp_servers = {}
        
        logger.info("✅ Initializing MCP Orchestrator with StrandsMCPClient")
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default MCP tools following the pattern."""
        logger.info("Registering default MCP tools...")
        
        # Get tools from MCP server
        tools = self.strands_mcp_client.get_tools_sync()
        if tools:
            logger.info(f"✅ Retrieved {len(tools)} tools from MCP server")
            for tool in tools:
                # Handle both dict and MCPAgentTool objects
                if hasattr(tool, 'name'):
                    tool_name = tool.name
                elif isinstance(tool, dict):
                    tool_name = tool.get('name', 'unknown')
                else:
                    tool_name = str(tool)
                self.tools[tool_name] = tool
        else:
            logger.warning("⚠️ No tools available from MCP server")
    
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
    
    async def run_swarm(self, swarm_name: str, content: str) -> str:
        """Run a swarm asynchronously."""
        try:
            from src.core.strands_mcp_client import run_mcp_swarm
            from strands.types.content import ContentBlock
            
            # Create content block from text
            content_block = ContentBlock(type="text", text=content)
            result = await run_mcp_swarm(swarm_name, [content_block])
            logger.info(f"✅ Swarm '{swarm_name}' completed execution")
            return result
        except Exception as e:
            logger.error(f"❌ Failed to run swarm '{swarm_name}': {e}")
            raise
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools."""
        return self.strands_mcp_client.get_available_tools()
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents and swarms."""
        return self.strands_mcp_client.get_agent_status()
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get comprehensive orchestrator status."""
        return {
            "orchestrator": "MCP Orchestrator with StrandsMCPClient",
            "agents": {name: {"name": agent.name} for name, agent in self.agents.items()},
            "swarms": {name: {"name": name, "agents_count": len(swarm.agents)} 
                      for name, swarm in self.swarms.items()},
                                     "tools": {
                name: {
                    "name": tool.name if hasattr(tool, 'name') else tool.get('name', 'unknown'),
                    "description": tool.description if hasattr(tool, 'description') else tool.get('description', 'No description')
                }
                for name, tool in self.tools.items()
            },
            "mcp_client_status": self.strands_mcp_client.get_agent_status()
        }


# Global orchestrator instance
mcp_orchestrator = MCPOrchestrator()
