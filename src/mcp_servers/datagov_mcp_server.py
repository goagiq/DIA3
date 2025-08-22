"""
Data.gov MCP Server
MCP server for Data.gov API integration and analysis.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource
)

from src.agents.datagov_agent import DataGovAgent
from src.config.datagov_config import DataGovConfig

logger = logging.getLogger(__name__)


class DataGovMCPServer:
    """MCP server for Data.gov API integration."""
    
    def __init__(self, port: int = 8000):
        self.port = port
        self.server = Server("datagov-mcp-server")
        self.datagov_agent = DataGovAgent()
        self.config = DataGovConfig()
        self.setup_tools()
        self.logger = logging.getLogger(__name__)
    
    def setup_tools(self):
        """Setup Data.gov MCP tools."""
        
        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            """List available Data.gov tools."""
            return ListToolsResult(
                tools=[
                    Tool(
                        name="datagov_package_search",
                        description="Search for packages (datasets) on Data.gov",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "q": {"type": "string", "description": "Search query"},
                                "sort": {"type": "string", "description": "Sort order (e.g., 'score desc, name asc')"},
                                "rows": {"type": "number", "description": "Number of results per page"},
                                "start": {"type": "number", "description": "Starting offset for results"}
                            }
                        }
                    ),
                    Tool(
                        name="datagov_package_show",
                        description="Get details for a specific package (dataset)",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "id": {"type": "string", "description": "Package ID or name"}
                            },
                            "required": ["id"]
                        }
                    ),
                    Tool(
                        name="datagov_group_list",
                        description="List groups on Data.gov",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "order_by": {"type": "string", "description": "Field to order by"},
                                "limit": {"type": "number", "description": "Maximum number of results"},
                                "offset": {"type": "number", "description": "Offset for results"},
                                "all_fields": {"type": "boolean", "description": "Return all fields"}
                            }
                        }
                    ),
                    Tool(
                        name="datagov_tag_list",
                        description="List tags on Data.gov",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Search query for tags"},
                                "all_fields": {"type": "boolean", "description": "Return all fields"}
                            }
                        }
                    ),
                    Tool(
                        name="datagov_trade_analysis",
                        description="Analyze trade data for specified countries",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "countries": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of country codes (e.g., ['CHN', 'RUS'])"
                                },
                                "time_period": {
                                    "type": "string",
                                    "description": "Time period for analysis (e.g., 'latest', '2023')"
                                }
                            }
                        }
                    ),
                    Tool(
                        name="datagov_economic_forecast",
                        description="Generate economic forecast for specified country",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "country": {
                                    "type": "string",
                                    "description": "Country code (e.g., 'CHN', 'RUS')"
                                },
                                "forecast_period": {
                                    "type": "string",
                                    "description": "Forecast period (e.g., '1Y', '6M')"
                                }
                            },
                            "required": ["country"]
                        }
                    ),
                    Tool(
                        name="datagov_environmental_analysis",
                        description="Analyze environmental data for specified countries",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "countries": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of country codes (e.g., ['CHN', 'RUS'])"
                                }
                            }
                        }
                    ),
                    Tool(
                        name="datagov_natural_language_query",
                        description="Process natural language queries against Data.gov data",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Natural language query (e.g., 'What are the trade trends between China and Russia?')"
                                }
                            },
                            "required": ["query"]
                        }
                    ),
                    Tool(
                        name="datagov_comprehensive_analysis",
                        description="Perform comprehensive analysis across all data types",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "countries": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of country codes (e.g., ['CHN', 'RUS'])"
                                }
                            }
                        }
                    ),
                    Tool(
                        name="datagov_health_check",
                        description="Check the health of Data.gov integration",
                        inputSchema={
                            "type": "object",
                            "properties": {}
                        }
                    ),
                    Tool(
                        name="datagov_get_config",
                        description="Get Data.gov configuration",
                        inputSchema={
                            "type": "object",
                            "properties": {}
                        }
                    )
                ]
            )
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Call a Data.gov tool."""
            try:
                self.logger.info(f"Calling Data.gov tool: {name} with arguments: {arguments}")
                
                if name == "datagov_package_search":
                    result = await self._package_search(arguments)
                elif name == "datagov_package_show":
                    result = await self._package_show(arguments)
                elif name == "datagov_group_list":
                    result = await self._group_list(arguments)
                elif name == "datagov_tag_list":
                    result = await self._tag_list(arguments)
                elif name == "datagov_trade_analysis":
                    result = await self._trade_analysis(arguments)
                elif name == "datagov_economic_forecast":
                    result = await self._economic_forecast(arguments)
                elif name == "datagov_environmental_analysis":
                    result = await self._environmental_analysis(arguments)
                elif name == "datagov_natural_language_query":
                    result = await self._natural_language_query(arguments)
                elif name == "datagov_comprehensive_analysis":
                    result = await self._comprehensive_analysis(arguments)
                elif name == "datagov_health_check":
                    result = await self._health_check(arguments)
                elif name == "datagov_get_config":
                    result = await self._get_config(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=json.dumps(result, indent=2)
                        )
                    ]
                )
                
            except Exception as e:
                self.logger.error(f"Tool call failed: {e}")
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=json.dumps({"error": str(e)}, indent=2)
                        )
                    ]
                )
    
    async def _package_search(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search for packages on Data.gov."""
        query = arguments.get("q", "")
        sort = arguments.get("sort", "score desc")
        rows = arguments.get("rows", 10)
        start = arguments.get("start", 0)
        
        # Mock implementation - in production, this would call the actual Data.gov API
        return {
            "query": query,
            "sort": sort,
            "rows": rows,
            "start": start,
            "results": [
                {
                    "id": "census-trade-data",
                    "name": "U.S. Census Bureau International Trade Data",
                    "description": "Monthly U.S. imports and exports by country",
                    "tags": ["trade", "census", "international"],
                    "score": 0.95
                },
                {
                    "id": "usda-economic-data",
                    "name": "USDA International Macroeconomic Data",
                    "description": "Economic indicators for 190 countries",
                    "tags": ["economics", "usda", "macroeconomic"],
                    "score": 0.92
                }
            ],
            "total": 2
        }
    
    async def _package_show(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get details for a specific package."""
        package_id = arguments.get("id", "")
        
        # Mock implementation
        if package_id == "census-trade-data":
            return {
                "id": package_id,
                "name": "U.S. Census Bureau International Trade Data",
                "description": "Comprehensive trade data from the U.S. Census Bureau",
                "resources": [
                    {
                        "name": "Monthly Imports by Country",
                        "format": "API",
                        "url": "http://api.census.gov/data/timeseries/intltrade/imports/"
                    }
                ],
                "metadata": {
                    "last_updated": "2024-01-15",
                    "frequency": "monthly",
                    "coverage": "global"
                }
            }
        else:
            return {"error": f"Package not found: {package_id}"}
    
    async def _group_list(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """List groups on Data.gov."""
        # Mock implementation
        return {
            "groups": [
                {
                    "id": "census-bureau",
                    "name": "U.S. Census Bureau",
                    "description": "Official statistics from the U.S. Census Bureau",
                    "package_count": 150
                },
                {
                    "id": "usda",
                    "name": "U.S. Department of Agriculture",
                    "description": "Agricultural and economic data from USDA",
                    "package_count": 75
                }
            ]
        }
    
    async def _tag_list(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """List tags on Data.gov."""
        query = arguments.get("query", "")
        
        # Mock implementation
        return {
            "query": query,
            "tags": [
                {"name": "trade", "count": 45},
                {"name": "economics", "count": 32},
                {"name": "census", "count": 28},
                {"name": "international", "count": 22}
            ]
        }
    
    async def _trade_analysis(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trade data."""
        countries = arguments.get("countries", ["CHN", "RUS"])
        time_period = arguments.get("time_period", "latest")
        
        result = await self.datagov_agent.get_trade_analysis(countries, time_period)
        return result
    
    async def _economic_forecast(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Generate economic forecast."""
        country = arguments.get("country", "CHN")
        forecast_period = arguments.get("forecast_period", "1Y")
        
        result = await self.datagov_agent.get_economic_forecast(country, forecast_period)
        return result
    
    async def _environmental_analysis(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze environmental data."""
        countries = arguments.get("countries", ["CHN", "RUS"])
        
        result = await self.datagov_agent.get_environmental_analysis(countries)
        return result
    
    async def _natural_language_query(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Process natural language query."""
        query = arguments.get("query", "")
        
        result = await self.datagov_agent.answer_natural_language_query(query)
        return result
    
    async def _comprehensive_analysis(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive analysis."""
        countries = arguments.get("countries", ["CHN", "RUS"])
        
        results = {}
        
        # Trade analysis
        results["trade"] = await self.datagov_agent.get_trade_analysis(countries)
        
        # Economic forecast
        economic_results = {}
        for country in countries:
            economic_results[country] = await self.datagov_agent.get_economic_forecast(country)
        results["economic"] = economic_results
        
        # Environmental analysis
        results["environmental"] = await self.datagov_agent.get_environmental_analysis(countries)
        
        return {
            "countries": countries,
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _health_check(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Check health of Data.gov integration."""
        health_status = await self.datagov_agent.health_check()
        return health_status
    
    async def _get_config(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get Data.gov configuration."""
        config_summary = self.config.get_config_summary()
        return config_summary
    
    async def start_server(self):
        """Start the MCP server on port 8000."""
        try:
            self.logger.info(f"🚀 Starting Data.gov MCP server on port {self.port}")
            
            # Initialize the server
            await self.server.run_stdio()
            
            self.logger.info("✅ Data.gov MCP server started successfully")
            
            # Sleep 60 seconds after restart as required
            self.logger.info("Sleeping 60 seconds after MCP server restart...")
            await asyncio.sleep(60)
            
        except Exception as e:
            self.logger.error(f"Failed to start Data.gov MCP server: {e}")
            raise


# Run with .venv/Scripts/python.exe
if __name__ == "__main__":
    server = DataGovMCPServer(port=8000)
    asyncio.run(server.start_server())
