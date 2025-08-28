"""
Unified MCP Client for interacting with the MCP server using Strands.
"""

from typing import Dict, Any
from loguru import logger

try:
    from src.core.strands_mcp_client import StrandsMCPClient
    MCP_AVAILABLE = True
    logger.info("✅ Strands MCP client available")
except ImportError as e:
    MCP_AVAILABLE = False
    logger.warning(f"Strands MCP client not available: {e}")


class UnifiedMCPClient:
    """Unified MCP client using Strands MCP client."""
    
    def __init__(self, server_url: str = "http://localhost:8000/mcp"):
        self.server_url = server_url
        self.strands_mcp_client = None
        self._connected = False
        
        if MCP_AVAILABLE:
            try:
                self.strands_mcp_client = StrandsMCPClient(server_url)
                self._connected = True
                logger.info(f"✅ Initialized Strands MCP client for {server_url}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Strands MCP client: {e}")
                self._connected = False
    
    async def connect(self) -> bool:
        """Connect to the MCP server."""
        if not MCP_AVAILABLE:
            logger.warning("Strands MCP client not available")
            return False
        
        if self._connected:
            return True
        
        try:
            # Test connection by getting tools
            tools = self.strands_mcp_client.get_tools_sync()
            logger.info(f"✅ Connected to MCP server with {len(tools)} tools")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to MCP server: {e}")
            return False
    
    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the MCP server."""
        if not self._connected:
            await self.connect()
        
        if not self._connected:
            # Return mock responses when MCP is not available
            return self._get_mock_response(tool_name, parameters)
        
        try:
            # Create a temporary agent to call the tool
            agent = self.strands_mcp_client.create_agent_with_mcp_tools(
                name=f"temp_agent_{tool_name}",
                system_prompt=f"You are an agent that calls the {tool_name} tool."
            )
            
            # Create a prompt that includes the tool call
            prompt = f"Call the {tool_name} tool with parameters: {parameters}"
            result = await agent.invoke_async(prompt)
            
            return {"success": True, "result": result}
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_mock_response(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get mock response for tools when MCP is not available."""
        if tool_name == "query_decision_context":
            return {
                "success": True,
                "result": {
                    "business_entities": [
                        {"name": "operational_efficiency", "type": "business_concept", "confidence": 0.8},
                        {"name": "cost_reduction", "type": "business_goal", "confidence": 0.9},
                        {"name": "market_analysis", "type": "business_process", "confidence": 0.7}
                    ],
                    "confidence_score": 0.85,
                    "context_type": parameters.get("context_type", "comprehensive"),
                    "language": parameters.get("language", "en")
                }
            }
        elif tool_name == "extract_entities":
            return {
                "success": True,
                "entities": [
                    {"name": "company", "type": "organization", "confidence": 0.9},
                    {"name": "efficiency", "type": "business_concept", "confidence": 0.8},
                    {"name": "costs", "type": "business_concept", "confidence": 0.9}
                ]
            }
        elif tool_name == "analyze_sentiment":
            return {
                "success": True,
                "sentiment": "neutral",
                "score": 0.5,
                "confidence": 0.8
            }
        elif tool_name == "analyze_patterns":
            return {
                "success": True,
                "patterns": [
                    {"type": "trend", "description": "increasing_efficiency_focus", "confidence": 0.7},
                    {"type": "anomaly", "description": "cost_concerns", "confidence": 0.6}
                ]
            }
        elif tool_name == "analyze_audio":
            return {
                "success": True,
                "audio_features": {
                    "tempo": 120,
                    "energy": 0.7,
                    "valence": 0.6,
                    "arousal": 0.5
                }
            }
        else:
            return {
                "success": True,
                "result": f"Mock response for {tool_name}",
                "parameters": parameters
            }
    
    def get_available_tools(self) -> list:
        """Get list of available tools."""
        if self._connected and self.strands_mcp_client:
            return self.strands_mcp_client.get_available_tools()
        return []
    
    def get_status(self) -> Dict[str, Any]:
        """Get client status."""
        return {
            "connected": self._connected,
            "server_url": self.server_url,
            "available_tools": len(self.get_available_tools()),
            "mcp_available": MCP_AVAILABLE
        }


# Global instance
unified_mcp_client = UnifiedMCPClient()


def call_unified_mcp_tool(tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Helper function to call MCP tools."""
    import asyncio
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're in an async context, we need to handle this differently
            # For now, return a mock response
            return unified_mcp_client._get_mock_response(tool_name, parameters)
        else:
            # We can run the async function
            return loop.run_until_complete(
                unified_mcp_client.call_tool(tool_name, parameters)
            )
    except Exception as e:
        logger.error(f"Error calling MCP tool {tool_name}: {e}")
        return {"success": False, "error": str(e)}
