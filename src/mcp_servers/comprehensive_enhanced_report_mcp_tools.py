"""
Comprehensive Enhanced Report MCP Tools

MCP tools for generating comprehensive enhanced reports with all missing components:
- Probability Distribution Charts (Normal, Lognormal, Beta)
- Interactive Knowledge Graph Visualization
- Interactive Dashboard with cost distribution, timeline analysis, regional comparisons
- Sentiment Analysis
- Tooltips with reference to sources
- Conclusion
- Advanced Forecasting Analysis
- Predictive Analytics & Feature Importance
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from loguru import logger

from src.core.comprehensive_enhanced_report_generator import comprehensive_enhanced_report_generator


class ComprehensiveEnhancedReportMCPTools:
    """MCP tools for comprehensive enhanced report generation."""
    
    def __init__(self):
        self.generator = comprehensive_enhanced_report_generator
        logger.info("Comprehensive Enhanced Report MCP Tools initialized")
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools."""
        return [
            {
                "name": "generate_comprehensive_enhanced_report",
                "description": "Generate comprehensive enhanced report with all missing components: probability distributions, knowledge graph, interactive dashboard, sentiment analysis, tooltips, conclusion, forecasting, and predictive analytics",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "The content to analyze for the enhanced report"
                        },
                        "title": {
                            "type": "string",
                            "description": "Report title",
                            "default": "Strategic Analysis Report"
                        },
                        "subtitle": {
                            "type": "string",
                            "description": "Report subtitle",
                            "default": "Comprehensive Enhanced Analysis"
                        },
                        "include_all_components": {
                            "type": "boolean",
                            "description": "Include all analysis components",
                            "default": True
                        }
                    },
                    "required": ["content"]
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call the specified MCP tool."""
        try:
            if name == "generate_comprehensive_enhanced_report":
                return await self._generate_comprehensive_enhanced_report(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
                
        except Exception as e:
            logger.error(f"Error calling MCP tool {name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": name
            }
    
    async def _generate_comprehensive_enhanced_report(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive enhanced report with all missing components."""
        try:
            content = arguments.get("content", "")
            title = arguments.get("title", "Strategic Analysis Report")
            subtitle = arguments.get("subtitle", "Comprehensive Enhanced Analysis")
            include_all_components = arguments.get("include_all_components", True)
            
            if not content:
                return {
                    "success": False,
                    "error": "Content is required for report generation"
                }
            
            logger.info(f"Generating comprehensive enhanced report: {title}")
            
            # Generate the comprehensive enhanced report
            result = await self.generator.generate_comprehensive_enhanced_report(
                content=content,
                title=title,
                subtitle=subtitle,
                include_all_components=include_all_components
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Comprehensive enhanced report generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Global instance
comprehensive_enhanced_report_mcp_tools = ComprehensiveEnhancedReportMCPTools()
