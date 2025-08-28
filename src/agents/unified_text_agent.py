"""
Unified Text Agent for comprehensive text analysis using Strands framework.
"""

from typing import Dict, Any, List, Optional
from loguru import logger

# Import the real Strands MCP client
from src.core.strands_mcp_client import StrandsMCPClient, create_mcp_agent, create_mcp_swarm


class UnifiedTextAgent:
    """Unified text analysis agent using Strands MCP client."""
    
    def __init__(self, name: str = "unified_text_agent", agent_id: str = None):
        self.name = name
        self.agent_id = agent_id or f"unified_text_agent_{name}"
        self.strands_mcp_client = StrandsMCPClient()
        self.agent = None
        self.swarm = None
        self.metadata = {}
        
        logger.info(f"Initializing UnifiedTextAgent '{name}' with StrandsMCPClient")
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the agent with MCP tools."""
        try:
            self.agent = create_mcp_agent(
                name=self.name,
                system_prompt="You are a comprehensive text analysis expert with access to MCP tools."
            )
            logger.info(f"✅ Created unified text agent '{self.name}' with MCP tools")
        except Exception as e:
            logger.error(f"❌ Failed to create unified text agent: {e}")
            raise
    
    async def analyze_text(self, text: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Analyze text using the unified agent."""
        try:
            if not self.agent:
                self._initialize_agent()
            
            prompt = f"Analyze this text using {analysis_type} analysis: {text}"
            result = await self.agent.invoke_async(prompt)
            
            return {
                "text": text,
                "analysis_type": analysis_type,
                "result": result,
                "agent": self.name
            }
        except Exception as e:
            logger.error(f"❌ Error in text analysis: {e}")
            return {"error": str(e)}
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text."""
        return await self.analyze_text(text, "sentiment")
    
    async def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text."""
        return await self.analyze_text(text, "entity extraction")
    
    async def analyze_language(self, text: str) -> Dict[str, Any]:
        """Analyze language characteristics."""
        return await self.analyze_text(text, "language analysis")
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get available MCP tools."""
        return self.strands_mcp_client.get_available_tools()
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "name": self.name,
            "agent_created": self.agent is not None,
            "available_tools": len(self.get_available_tools()),
            "mcp_client_status": self.strands_mcp_client.get_agent_status()
        }


# Global instance
unified_text_agent = UnifiedTextAgent(agent_id="global_unified_text_agent")
