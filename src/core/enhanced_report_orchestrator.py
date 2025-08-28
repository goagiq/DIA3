"""
Enhanced Report Orchestrator with Source Tracking

This module provides an enhanced report orchestrator that automatically tracks sources,
calculations, and generates comprehensive tooltips for all data points in reports.
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from pathlib import Path
from loguru import logger

from src.core.source_tracking import (
    SourceTracker, SourceReference, CalculationStep, DataPoint,
    track_source, track_calculation, create_tracked_data_point
)
# Import enhanced MCP client if available
try:
    from src.core.enhanced_mcp_client import get_enhanced_mcp_client
    ENHANCED_MCP_CLIENT_AVAILABLE = True
except ImportError:
    ENHANCED_MCP_CLIENT_AVAILABLE = False
    logger.info("ℹ️ Enhanced MCP client not available")


class EnhancedReportOrchestrator:
    """Enhanced report orchestrator with comprehensive source tracking."""
    
    def __init__(self, output_dir: str = "Results/enhanced_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.source_tracker = SourceTracker()
        
        # Initialize MCP client if available
        if ENHANCED_MCP_CLIENT_AVAILABLE:
            self.mcp_client = get_enhanced_mcp_client()
        else:
            self.mcp_client = None
            logger.info("ℹ️ Enhanced MCP client not available, some features may be limited")
        
        logger.info(f"Enhanced Report Orchestrator initialized with output dir: {output_dir}")
    
    async def generate_enhanced_report(
        self, 
        content: str,
        report_type: str = "comprehensive",
        include_tooltips: bool = True,
        include_source_references: bool = True,
        include_calculations: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate an enhanced report with comprehensive source tracking."""
        
        start_time = time.time()
        
        # Track the report generation request
        report_request_source = track_source(
            source_type="report_request",
            source_path=f"report_{report_type}_{int(time.time())}",
            metadata={
                "report_type": report_type,
                "content_length": len(content),
                "include_tooltips": include_tooltips,
                "include_source_references": include_source_references,
                "include_calculations": include_calculations,
                "parameters": kwargs
            }
        )
        
        try:
            # Generate the base report using MCP tools if available
            if self.mcp_client is not None:
                base_report_result = await self.mcp_client.generate_report_with_tracking(
                    content, report_type, **kwargs
                )
            else:
                # Fallback when MCP client is not available
                base_report_result = {
                    "success": True,
                    "result": {
                        "content": f"# Enhanced Report ({report_type})\n\n{content}\n\n*Note: MCP client not available, using fallback generation*"
                    }
                }
            
            # Track the base report generation
            base_report_calc = track_calculation(
                step_name=f"Base Report Generation: {report_type}",
                parameters={
                    "calculation_type": "mcp_report_generation",
                    "report_type": report_type,
                    "success": base_report_result.get("success", False)
                },
                execution_time=time.time() - start_time
            )
            
            # Extract report content
            if isinstance(base_report_result, dict):
                report_content = base_report_result.get("result", {}).get("content", "")
                if not report_content:
                    report_content = str(base_report_result.get("result", ""))
            else:
                # Handle case where MCP client returns a string
                report_content = str(base_report_result)
            
            # Enhance the report with source tracking information
            enhanced_content = await self._enhance_report_with_tracking(
                report_content,
                base_report_result,
                include_tooltips,
                include_source_references,
                include_calculations
            )
            
            # Track the enhancement process
            enhancement_calc = track_calculation(
                step_name="Report Enhancement with Source Tracking",
                parameters={
                    "calculation_type": "report_enhancement",
                    "enhancement_features": {
                        "tooltips": include_tooltips,
                        "source_references": include_source_references,
                        "calculations": include_calculations
                    }
                }
            )
            
            # Create the final enhanced report data point
            enhanced_report_data_point = create_tracked_data_point(
                data_type="enhanced_report",
                value=enhanced_content,
                sources=[report_request_source],
                calculations=[base_report_calc, enhancement_calc],
                confidence=1.0 if base_report_result.get("success", False) else 0.0,
                metadata={
                    "report_type": report_type,
                    "content_length": len(content),
                    "enhanced_content_length": len(enhanced_content)
                }
            )
            
            # Save the enhanced report
            report_filename = f"enhanced_report_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            report_filepath = self.output_dir / report_filename
            
            with open(report_filepath, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            
            # Save source tracking data
            tracking_filename = f"source_tracking_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            tracking_filepath = self.source_tracker.save_session_data(tracking_filename)
            
            # Generate tooltip data for frontend integration
            tooltip_data = self.source_tracker.export_tooltip_data([enhanced_report_data_point])
            
            # Create comprehensive result
            result = {
                "success": True,
                "enhanced_report": {
                    "content": enhanced_content,
                    "filepath": str(report_filepath),
                    "filename": report_filename
                },
                "source_tracking": {
                    "session_id": self.source_tracker.session_id,
                    "tracking_filepath": tracking_filepath,
                    "tooltip_data": tooltip_data
                },
                "base_report": base_report_result,
                "enhancement_features": {
                    "tooltips": include_tooltips,
                    "source_references": include_source_references,
                    "calculations": include_calculations
                },
                "metadata": {
                    "report_type": report_type,
                    "generated_at": datetime.now().isoformat(),
                    "execution_time": time.time() - start_time
                }
            }
            
            logger.info(f"Enhanced report generated successfully: {report_filepath}")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # Track the error
            error_calc = track_calculation(
                step_name=f"Enhanced Report Generation Error: {report_type}",
                parameters={
                    "calculation_type": "error",
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                },
                execution_time=execution_time
            )
            
            logger.error(f"Error generating enhanced report: {e}")
            return {
                "success": False,
                "error": str(e),
                "report_type": report_type,
                "source_tracking": {
                    "session_id": self.source_tracker.session_id,
                    "execution_time": execution_time
                }
            }
    
    async def _enhance_report_with_tracking(
        self,
        report_content: str,
        base_report_result: Dict[str, Any],
        include_tooltips: bool,
        include_source_references: bool,
        include_calculations: bool
    ) -> str:
        """Enhance report content with source tracking information."""
        
        enhanced_parts = []
        
        # Add header with source tracking info
        enhanced_parts.append("# Enhanced Report with Source Tracking")
        enhanced_parts.append("")
        enhanced_parts.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        enhanced_parts.append(f"**Session ID:** {self.source_tracker.session_id}")
        enhanced_parts.append("")
        
        # Add source tracking summary
        if include_source_references:
            enhanced_parts.append("## Source References")
            enhanced_parts.append("")
            
            # Extract source tracking info from base report
            source_tracking = base_report_result.get("source_tracking", {})
            if source_tracking:
                enhanced_parts.append("### MCP Tool Sources")
                enhanced_parts.append("")
                enhanced_parts.append(f"- **Tool Source ID:** {source_tracking.get('tool_source_id', 'N/A')}")
                enhanced_parts.append(f"- **Calculation ID:** {source_tracking.get('calculation_id', 'N/A')}")
                enhanced_parts.append(f"- **Data Point ID:** {source_tracking.get('data_point_id', 'N/A')}")
                enhanced_parts.append(f"- **Execution Time:** {source_tracking.get('execution_time', 0):.3f}s")
                enhanced_parts.append("")
            
            # Add report tracking info
            report_tracking = base_report_result.get("report_tracking", {})
            if report_tracking:
                enhanced_parts.append("### Report Generation Sources")
                enhanced_parts.append("")
                enhanced_parts.append(f"- **Report Source ID:** {report_tracking.get('report_source_id', 'N/A')}")
                enhanced_parts.append(f"- **Report Data Point ID:** {report_tracking.get('report_data_point_id', 'N/A')}")
                enhanced_parts.append("")
        
        # Add calculations section
        if include_calculations:
            enhanced_parts.append("## Calculations and Processing Steps")
            enhanced_parts.append("")
            
            # Extract calculation info from base report
            source_tracking = base_report_result.get("source_tracking", {})
            if source_tracking:
                enhanced_parts.append("### MCP Tool Calculations")
                enhanced_parts.append("")
                enhanced_parts.append(f"- **Tool Name:** {base_report_result.get('tool_name', 'N/A')}")
                enhanced_parts.append(f"- **Calculation Type:** MCP Tool Execution")
                enhanced_parts.append(f"- **Success:** {base_report_result.get('success', False)}")
                enhanced_parts.append("")
        
        # Add tooltips section
        if include_tooltips:
            enhanced_parts.append("## Interactive Tooltips")
            enhanced_parts.append("")
            enhanced_parts.append("The following data points include interactive tooltips with detailed source information:")
            enhanced_parts.append("")
            
            # Extract tooltip content from base report
            source_tracking = base_report_result.get("source_tracking", {})
            if source_tracking and source_tracking.get("tooltip_content"):
                enhanced_parts.append("### Tooltip Content")
                enhanced_parts.append("")
                enhanced_parts.append("```html")
                enhanced_parts.append(source_tracking["tooltip_content"])
                enhanced_parts.append("```")
                enhanced_parts.append("")
        
        # Add the original report content
        enhanced_parts.append("## Report Content")
        enhanced_parts.append("")
        enhanced_parts.append(report_content)
        
        # Add footer with metadata
        enhanced_parts.append("")
        enhanced_parts.append("---")
        enhanced_parts.append("")
        enhanced_parts.append("### Report Metadata")
        enhanced_parts.append("")
        enhanced_parts.append(f"- **Report Type:** {base_report_result.get('report_type', 'N/A')}")
        enhanced_parts.append(f"- **Generated At:** {datetime.now().isoformat()}")
        enhanced_parts.append(f"- **Source Tracking Session:** {self.source_tracker.session_id}")
        enhanced_parts.append(f"- **Enhanced Features:** Tooltips, Source References, Calculations")
        
        return "\n".join(enhanced_parts)
    
    async def generate_visualization_with_tooltips(
        self, 
        data: Dict[str, Any],
        visualization_type: str = "interactive",
        **kwargs
    ) -> Dict[str, Any]:
        """Generate visualization with tooltip integration."""
        
        # Track the visualization request
        viz_source = track_source(
            source_type="visualization_request",
            source_path=f"viz_{visualization_type}_{int(time.time())}",
            metadata={
                "visualization_type": visualization_type,
                "data_keys": list(data.keys()) if isinstance(data, dict) else [],
                "parameters": kwargs
            }
        )
        
        try:
            # Generate visualization using MCP tools
            viz_result = await self.mcp_client.call_tool_with_tracking(
                "create_visualizations",
                {
                    "data": data,
                    "visualization_type": visualization_type,
                    **kwargs
                }
            )
            
            # Track the visualization generation
            viz_calc = track_calculation(
                step_name=f"Visualization Generation: {visualization_type}",
                parameters={
                    "calculation_type": "visualization_generation",
                    "visualization_type": visualization_type,
                    "success": viz_result.get("success", False)
                }
            )
            
            # Create data point for the visualization
            viz_data_point = create_tracked_data_point(
                data_type="visualization",
                value=viz_result.get("result", {}),
                sources=[viz_source],
                calculations=[viz_calc],
                confidence=1.0 if viz_result.get("success", False) else 0.0,
                metadata={
                    "visualization_type": visualization_type,
                    "data_size": len(str(data))
                }
            )
            
            # Enhance visualization with tooltip data
            tooltip_data = self.source_tracker.export_tooltip_data([viz_data_point])
            
            result = {
                "success": True,
                "visualization": viz_result.get("result", {}),
                "tooltip_data": tooltip_data,
                "source_tracking": {
                    "session_id": self.source_tracker.tracking_session,
                    "data_point_id": viz_data_point.data_id,
                    "tooltip_content": viz_data_point.tooltip_content
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating visualization: {e}")
        return {
                "success": False,
                "error": str(e),
                "visualization_type": visualization_type
            }
    
    def get_tooltip_data(self) -> Dict[str, Any]:
        """Get tooltip data for frontend integration."""
        return self.source_tracker.export_tooltip_data([])
    
    def save_tracking_session(self, filename: Optional[str] = None) -> str:
        """Save the current tracking session to file."""
        return self.source_tracker.save_session_data(filename)
    
    def generate_source_report(self) -> Dict[str, Any]:
        """Generate a comprehensive source report."""
        return self.source_tracker.generate_source_report([])


# Global enhanced report orchestrator instance
_enhanced_report_orchestrator: Optional[EnhancedReportOrchestrator] = None


def get_enhanced_report_orchestrator() -> EnhancedReportOrchestrator:
    """Get the global enhanced report orchestrator instance."""
    global _enhanced_report_orchestrator
    if _enhanced_report_orchestrator is None:
        _enhanced_report_orchestrator = EnhancedReportOrchestrator()
    return _enhanced_report_orchestrator


async def generate_enhanced_report_with_tracking(
    content: str,
    report_type: str = "comprehensive",
    include_tooltips: bool = True,
    include_source_references: bool = True,
    include_calculations: bool = True,
    **kwargs
) -> Dict[str, Any]:
    """Convenience function to generate enhanced report with tracking."""
    orchestrator = get_enhanced_report_orchestrator()
    return await orchestrator.generate_enhanced_report(
        content, report_type, include_tooltips, include_source_references, include_calculations, **kwargs
    )


async def generate_visualization_with_enhanced_tooltips(
    data: Dict[str, Any],
    visualization_type: str = "interactive",
    **kwargs
    ) -> Dict[str, Any]:
    """Convenience function to generate visualization with tooltips."""
    orchestrator = get_enhanced_report_orchestrator()
    return await orchestrator.generate_visualization_with_tooltips(data, visualization_type, **kwargs)
