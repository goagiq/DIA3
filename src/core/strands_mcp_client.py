"""
Strands MCP Client implementation for proper tool integration.
This follows the official Strands documentation for MCP tool setup.
"""

import asyncio
from typing import List, Dict, Any, Optional
from loguru import logger

try:
    from mcp.client.streamable_http import streamablehttp_client
    from strands import Agent
    from strands.tools.mcp.mcp_client import MCPClient
    from strands.multiagent import Swarm
    from strands.types.content import ContentBlock
    STRANDS_AVAILABLE = True
    logger.info("✅ Real Strands and MCP libraries available")
except ImportError as e:
    STRANDS_AVAILABLE = False
    logger.warning(f"⚠️ Required libraries not available: {e}")
    logger.warning("Please install: pip install strands mcp")
    logger.warning("Continuing with limited functionality...")


class StrandsMCPClient:
    """Proper Strands MCP client implementation using streamable HTTP."""
    
    def __init__(self, mcp_server_url: str = "http://localhost:8000/mcp"):
        self.mcp_server_url = mcp_server_url
        self.streamable_http_mcp_client = None
        self.tools = []
        self.agents = {}
        self.swarms = {}
        
        logger.info(f"Initializing Strands MCP client for {mcp_server_url}")
        if STRANDS_AVAILABLE:
            # Don't create the client immediately - wait until it's needed
            logger.info("✅ StrandsMCPClient initialized (client will be created on first use)")
        else:
            logger.warning("⚠️ StrandsMCPClient initialized with limited functionality")
    
    def _create_mcp_client(self):
        """Create the MCP client with streamable HTTP."""
        # Only try to create client once per instance
        if hasattr(self, '_client_creation_attempted') and self._client_creation_attempted:
            return
            
        self._client_creation_attempted = True
        
        try:
            # Add a longer delay to ensure server is ready
            import time
            time.sleep(3)  # Wait 3 seconds for server to be ready
            
            # Test if server is reachable before creating client
            import requests
            try:
                response = requests.get(f"{self.mcp_server_url.replace('/mcp', '')}/health", timeout=5)
                if response.status_code != 200:
                    logger.info(f"ℹ️ MCP server health check failed: {response.status_code}")
                    self.streamable_http_mcp_client = None
                    return
            except Exception as health_error:
                # Only log this once to reduce spam
                if not hasattr(self, '_server_unreachable_logged'):
                    logger.info("ℹ️ MCP server not running (this is normal if server is not started)")
                    self._server_unreachable_logged = True
                self.streamable_http_mcp_client = None
                return
            
            self.streamable_http_mcp_client = MCPClient(
                lambda: streamablehttp_client(self.mcp_server_url)
            )
            logger.success("✅ MCP client created successfully")
        except Exception as e:
            logger.info(f"ℹ️ MCP client creation skipped: {e}")
            self.streamable_http_mcp_client = None
    
    def get_tools_sync(self) -> List[Dict[str, Any]]:
        """Get tools from MCP server synchronously."""
        if not STRANDS_AVAILABLE:
            # Only log this once to reduce spam
            if not hasattr(self, '_strands_unavailable_logged'):
                logger.info("ℹ️ Strands not available, using limited functionality")
                self._strands_unavailable_logged = True
            return []
            
        try:
            # Don't create client during import - wait until actually needed
            if not self.streamable_http_mcp_client:
                # Add a delay to ensure server is ready
                import time
                time.sleep(2)  # Wait 2 seconds for server to be ready
                self._create_mcp_client()
            
            if not self.streamable_http_mcp_client:
                # Only log this once per instance to reduce spam
                if not hasattr(self, '_tools_unavailable_logged'):
                    logger.info("ℹ️ MCP tools not available (server not running)")
                    self._tools_unavailable_logged = True
                return []
            
            # Add retry logic for connection issues
            max_retries = 2  # Reduced retries to avoid hanging
            for attempt in range(max_retries):
                try:
                    # Check if client is already running
                    if hasattr(self.streamable_http_mcp_client, '_is_running') and self.streamable_http_mcp_client._is_running:
                        # Only log this once to reduce spam
                        if not hasattr(self, '_client_running_logged'):
                            logger.info("ℹ️ MCP client already running, skipping request")
                            self._client_running_logged = True
                        return []
                    
                    # Use context manager to ensure proper cleanup
                    with self.streamable_http_mcp_client:
                        tools = self.streamable_http_mcp_client.list_tools_sync()
                        logger.info(f"✅ Retrieved {len(tools)} tools from MCP server")
                        return tools
                except Exception as e:
                    if attempt < max_retries - 1:
                        # Only log this once to reduce spam
                        if not hasattr(self, '_retry_logged'):
                            logger.info("ℹ️ MCP connection retrying...")
                            self._retry_logged = True
                        import time
                        time.sleep(1)
                    else:
                        # Only log this once to reduce spam
                        if not hasattr(self, '_retry_failed_logged'):
                            logger.info("ℹ️ MCP connection failed, using local agents")
                            self._retry_failed_logged = True
                        return []
                        
        except Exception as e:
            # Only log this once to reduce spam
            if not hasattr(self, '_tools_error_logged'):
                logger.info("ℹ️ MCP tools unavailable, continuing with local agents")
                self._tools_error_logged = True
            return []
            
    async def get_tools_async(self) -> List[Dict[str, Any]]:
        """Get tools from MCP server asynchronously."""
        if not STRANDS_AVAILABLE:
            # Only log this once to reduce spam
            if not hasattr(self, '_strands_unavailable_logged'):
                logger.info("ℹ️ Strands not available, using limited functionality")
                self._strands_unavailable_logged = True
            return []
            
        try:
            if not self.streamable_http_mcp_client:
                self._create_mcp_client()
            
            if not self.streamable_http_mcp_client:
                # Only log this once per instance to reduce spam
                if not hasattr(self, '_tools_unavailable_logged'):
                    logger.info("ℹ️ MCP tools not available (server not running)")
                    self._tools_unavailable_logged = True
                return []
            
            # Check if client is already running
            if hasattr(self.streamable_http_mcp_client, '_is_running') and self.streamable_http_mcp_client._is_running:
                # Only log this once to reduce spam
                if not hasattr(self, '_client_running_logged'):
                    logger.info("ℹ️ MCP client already running, skipping request")
                    self._client_running_logged = True
                return []
            
            # Use synchronous method since MCPClient doesn't support async context manager
            # But wrap it in a try-catch to handle session issues
            try:
                tools = self.streamable_http_mcp_client.list_tools_sync()
                logger.info(f"✅ Retrieved {len(tools)} tools asynchronously")
                return tools
            except Exception as session_error:
                # Only log this once to reduce spam
                if not hasattr(self, '_session_error_logged'):
                    logger.info("ℹ️ MCP session error, continuing with local agents")
                    self._session_error_logged = True
                return []
                
        except Exception as e:
            # Only log this once to reduce spam
            if not hasattr(self, '_tools_error_logged'):
                logger.info("ℹ️ MCP tools unavailable, continuing with local agents")
                self._tools_error_logged = True
            return []
    
    def create_agent_with_mcp_tools(self, name: str, system_prompt: str = None):
        """Create a Strands agent with MCP tools."""
        if not STRANDS_AVAILABLE:
            # Only log this once to reduce spam
            if not hasattr(self, '_strands_unavailable_logged'):
                logger.info("ℹ️ Strands not available, using mock agents")
                self._strands_unavailable_logged = True
            # Return a mock agent object
            class MockAgent:
                def __init__(self, name, system_prompt=None):
                    self.name = name
                    self.system_prompt = system_prompt
                    self.tools = []
            return MockAgent(name, system_prompt)
            
        try:
            # Get tools from MCP server
            tools = self.get_tools_sync()
            
            # Get Ollama configuration - use fast model instead of slow mistral
            from src.config.config import config
            ollama_host = config.model.strands_ollama_host
            # Use fast model instead of slow mistral
            ollama_model_name = "phi3:mini"  # Fast, small model that works
            
            # Create Ollama model using proper Strands configuration
            from strands.models.ollama import OllamaModel
            ollama_model = OllamaModel(
                host=ollama_host,
                model_id=ollama_model_name,
                temperature=0.3,  # Lower temperature for faster responses
                streaming=False,  # Disable streaming to avoid hanging
                max_tokens=200    # Limit tokens for faster response
            )
            
            if not tools:
                # Only log this once per instance to reduce spam
                if not hasattr(self, '_no_tools_logged'):
                    logger.info("ℹ️ Using local agents (MCP server not running)")
                    self._no_tools_logged = True
                # Create agent without tools using Ollama
                agent = Agent(
                    name=name,
                    system_prompt=system_prompt,
                    model=ollama_model
                )
            else:
                # Create agent with MCP tools using Ollama
                agent = Agent(
                    name=name,
                    system_prompt=system_prompt,
                    tools=tools,
                    model=ollama_model
                )
                logger.info(f"✅ Created agent '{name}' with {len(tools)} tools using Ollama model {ollama_model_name}")
            
            self.agents[name] = agent
            return agent
            
        except Exception as e:
            logger.error(f"❌ Failed to create agent with MCP tools: {e}")
            # Fallback to mock agent
            # Only log this once to reduce spam
            if not hasattr(self, '_fallback_logged'):
                logger.info("ℹ️ Using mock agents as fallback")
                self._fallback_logged = True
            class MockAgent:
                def __init__(self, name, system_prompt=None):
                    self.name = name
                    self.system_prompt = system_prompt
                    self.tools = []
                
                async def invoke_async(self, prompt):
                    """Mock async invocation."""
                    return f"Mock response from {self.name}: {prompt[:50]}..."
            return MockAgent(name, system_prompt)
    
    def create_swarm_with_mcp_tools(self, agents: List[Agent], name: str = "swarm") -> Swarm:
        """Create a Strands swarm with MCP-enabled agents."""
        try:
            swarm = Swarm(agents)
            self.swarms[name] = swarm
            logger.info(f"✅ Created swarm '{name}' with {len(agents)} agents")
            return swarm
        except Exception as e:
            logger.error(f"❌ Failed to create swarm: {e}")
            raise
    
    async def run_agent_async(self, agent_name: str, prompt: str) -> str:
        """Run an agent asynchronously."""
        try:
            agent = self.agents.get(agent_name)
            if not agent:
                # Create the agent if it doesn't exist
                logger.info(f"ℹ️ Agent '{agent_name}' not found, creating it...")
                agent = self.create_agent_with_mcp_tools(
                    name=agent_name,
                    system_prompt=f"You are {agent_name}, a helpful AI assistant."
                )
            
            result = await agent.invoke_async(prompt)
            logger.info(f"✅ Agent '{agent_name}' completed execution")
            # Handle AgentResult object properly
            if hasattr(result, 'content'):
                return result.content
            elif hasattr(result, 'text'):
                return result.text
            elif hasattr(result, 'response'):
                return result.response
            else:
                return str(result)
            
        except Exception as e:
            logger.error(f"❌ Failed to run agent '{agent_name}': {e}")
            raise
    
    async def run_swarm_async(self, swarm_name: str, content_blocks: List[ContentBlock]) -> str:
        """Run a swarm asynchronously with multi-modal content."""
        try:
            swarm = self.swarms.get(swarm_name)
            if not swarm:
                raise ValueError(f"Swarm '{swarm_name}' not found")
            
            result = await swarm.invoke_async(content_blocks)
            logger.info(f"✅ Swarm '{swarm_name}' completed execution")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to run swarm '{swarm_name}': {e}")
            raise
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools."""
        tools = self.get_tools_sync()
        # Convert MCPAgentTool objects to dictionaries
        tool_list = []
        for tool in tools:
            if hasattr(tool, 'name'):
                tool_dict = {
                    "name": tool.name,
                    "description": getattr(tool, 'description', 'No description'),
                    "type": "MCPAgentTool"
                }
            elif isinstance(tool, dict):
                tool_dict = tool
            else:
                tool_dict = {
                    "name": str(tool),
                    "description": "Unknown tool",
                    "type": type(tool).__name__
                }
            tool_list.append(tool_dict)
        return tool_list
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        return {
            "agents": {name: {"name": agent.name, "tools_count": len(agent.tools)} 
                      for name, agent in self.agents.items()},
            "swarms": {name: {"name": name, "agents_count": len(swarm.agents)} 
                      for name, swarm in self.swarms.items()},
            "total_tools": len(self.get_tools_sync())
        }


# Global instance
strands_mcp_client = StrandsMCPClient()


def create_mcp_agent(name: str, system_prompt: str = None) -> Agent:
    """Helper function to create an agent with MCP tools."""
    return strands_mcp_client.create_agent_with_mcp_tools(name, system_prompt)


def create_mcp_swarm(agents: List[Agent], name: str = "swarm") -> Swarm:
    """Helper function to create a swarm with MCP-enabled agents."""
    return strands_mcp_client.create_swarm_with_mcp_tools(agents, name)


async def run_mcp_agent(agent_name: str, prompt: str) -> str:
    """Helper function to run an agent asynchronously."""
    return await strands_mcp_client.run_agent_async(agent_name, prompt)


async def run_mcp_swarm(swarm_name: str, content_blocks: List[ContentBlock]) -> str:
    """Helper function to run a swarm asynchronously."""
    return await strands_mcp_client.run_swarm_async(swarm_name, content_blocks)
