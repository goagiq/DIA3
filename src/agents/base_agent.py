"""
Base agent class for the agentic swarm using Strands framework.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4

from src.core.models import (
    AnalysisRequest,
    AnalysisResult,
)

logger = logging.getLogger(__name__)


class StrandsBaseAgent(ABC):
    """Base class for all Strands-compliant agents in the swarm."""
    
    def __init__(
        self, 
        agent_id: Optional[str] = None, 
        max_capacity: int = 10, 
        model_name: str = "llama3.2:latest"
    ):
        self.agent_id = (
            agent_id or f"{self.__class__.__name__}_{uuid4().hex[:8]}"
        )
        self.max_capacity = max_capacity
        self.current_load = 0
        self.status = "idle"
        self.last_heartbeat = datetime.now(timezone.utc)
        self.metadata: Dict[str, Any] = {}
        self._shutdown_event = asyncio.Event()
        
        # Create Strands Agent with MCP tools
        try:
            from strands import Agent
            self.strands_agent = Agent(
                name=self.agent_id,
                model=model_name,
                tools=self._get_tools()
            )
        except ImportError:
            # Use MCP client if real Strands not available
            from src.core.strands_mcp_client import create_mcp_agent
            self.strands_agent = create_mcp_agent(
                name=self.agent_id,
                system_prompt=f"You are a {self.__class__.__name__} agent."
            )
        
        logger.info(f"Initialized Strands agent {self.agent_id}")
    
    def _get_tools(self) -> list:
        """Get list of tools for this agent. Override in subclasses."""
        return []
    
    @abstractmethod
    async def can_process(self, request: AnalysisRequest) -> bool:
        """Check if this agent can process the given request."""
        pass
    
    @abstractmethod
    async def process(self, request: AnalysisRequest) -> AnalysisResult:
        """Process the analysis request."""
        pass
    
    async def start(self):
        """Start the agent."""
        try:
            await self.strands_agent.start()
            self.status = "running"
            logger.info(f"Agent {self.agent_id} started")
        except Exception as e:
            logger.error(f"Failed to start agent {self.agent_id}: {e}")
    
    async def stop(self):
        """Stop the agent."""
        try:
            await self.strands_agent.stop()
            self.status = "stopped"
            self._shutdown_event.set()
            logger.info(f"Agent {self.agent_id} stopped")
        except Exception as e:
            logger.error(f"Failed to stop agent {self.agent_id}: {e}")
    
    async def run(self, prompt: str, **kwargs) -> str:
        """Run the agent with a prompt."""
        try:
            if hasattr(self.strands_agent, 'invoke_async'):
                result = await self.strands_agent.invoke_async(prompt, **kwargs)
            else:
                result = await self.strands_agent.run(prompt, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error running agent {self.agent_id}: {e}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "current_load": self.current_load,
            "max_capacity": self.max_capacity,
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "metadata": self.metadata
        }
    
    def update_heartbeat(self):
        """Update the agent's heartbeat."""
        self.last_heartbeat = datetime.now(timezone.utc)
    
    def is_healthy(self) -> bool:
        """Check if the agent is healthy."""
        time_since_heartbeat = (
            datetime.now(timezone.utc) - self.last_heartbeat
        ).total_seconds()
        return time_since_heartbeat < 300  # 5 minutes timeout


# Keep the old BaseAgent for backward compatibility during transition
BaseAgent = StrandsBaseAgent
