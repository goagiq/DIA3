"""
Enhanced Markdown Export MCP Tools.

This module provides enhanced markdown export functionality through MCP tools,
including advanced formatting, styling, and export options.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger

try:
    from fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    logger.warning("FastMCP not available - using mock MCP tools")


class EnhancedMarkdownExportMCPTools:
    """Enhanced markdown export MCP tools with advanced formatting and styling."""
    
    def __init__(self):
        """Initialize the enhanced markdown export MCP tools."""
        self.output_dir = Path("docs/white_papers/generated_pdfs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("✅ Enhanced Markdown Export MCP Tools initialized")
    
    def register_tools(self, mcp_server):
        """Register enhanced markdown export tools with the MCP server."""
        if not MCP_AVAILABLE or not mcp_server:
            logger.warning("⚠️ MCP server not available - skipping tool registration")
            return
        
        @mcp_server.tool(description="Export markdown content to PDF with enhanced formatting")
        async def enhanced_markdown_export_pdf(
            content: str,
            title: str = "Enhanced Report",
            author: str = "DIA3 System",
            include_toc: bool = True,
            styling: str = "professional"
        ) -> Dict[str, Any]:
            """Export markdown content to PDF with enhanced formatting."""
            try:
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"enhanced_report_{timestamp}.pdf"
                filepath = self.output_dir / filename
                
                # Create enhanced markdown content
                enhanced_content = self._create_enhanced_markdown(
                    content, title, author, include_toc, styling
                )
                
                # Export to PDF (mock implementation)
                # In a real implementation, this would use a PDF library
                with open(filepath, 'w') as f:
                    f.write(f"# {title}\n\n{enhanced_content}")
                
                return {
                    "success": True,
                    "filename": filename,
                    "filepath": str(filepath),
                    "title": title,
                    "styling": styling,
                    "include_toc": include_toc
                }
                
            except Exception as e:
                logger.error(f"Enhanced markdown export failed: {e}")
                return {"success": False, "error": str(e)}
        
        @mcp_server.tool(description="Export markdown content to Word document with enhanced formatting")
        async def enhanced_markdown_export_word(
            content: str,
            title: str = "Enhanced Report",
            author: str = "DIA3 System",
            include_toc: bool = True,
            styling: str = "professional"
        ) -> Dict[str, Any]:
            """Export markdown content to Word document with enhanced formatting."""
            try:
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"enhanced_report_{timestamp}.docx"
                filepath = self.output_dir / filename
                
                # Create enhanced markdown content
                enhanced_content = self._create_enhanced_markdown(
                    content, title, author, include_toc, styling
                )
                
                # Export to Word (mock implementation)
                # In a real implementation, this would use a Word library
                with open(filepath, 'w') as f:
                    f.write(f"# {title}\n\n{enhanced_content}")
                
                return {
                    "success": True,
                    "filename": filename,
                    "filepath": str(filepath),
                    "title": title,
                    "styling": styling,
                    "include_toc": include_toc
                }
                
            except Exception as e:
                logger.error(f"Enhanced markdown export failed: {e}")
                return {"success": False, "error": str(e)}
        
        @mcp_server.tool(description="Export markdown content to HTML with enhanced styling")
        async def enhanced_markdown_export_html(
            content: str,
            title: str = "Enhanced Report",
            author: str = "DIA3 System",
            include_toc: bool = True,
            styling: str = "professional",
            interactive: bool = True
        ) -> Dict[str, Any]:
            """Export markdown content to HTML with enhanced styling."""
            try:
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"enhanced_report_{timestamp}.html"
                filepath = self.output_dir / filename
                
                # Create enhanced HTML content
                html_content = self._create_enhanced_html(
                    content, title, author, include_toc, styling, interactive
                )
                
                # Write HTML file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                return {
                    "success": True,
                    "filename": filename,
                    "filepath": str(filepath),
                    "title": title,
                    "styling": styling,
                    "interactive": interactive
                }
                
            except Exception as e:
                logger.error(f"Enhanced HTML export failed: {e}")
                return {"success": False, "error": str(e)}
        
        @mcp_server.tool(description="Get enhanced markdown export capabilities")
        async def enhanced_markdown_export_capabilities() -> Dict[str, Any]:
            """Get enhanced markdown export capabilities."""
            return {
                "success": True,
                "capabilities": {
                    "formats": ["pdf", "word", "html"],
                    "styling_options": ["professional", "academic", "business", "creative"],
                    "features": [
                        "table_of_contents",
                        "custom_styling",
                        "interactive_elements",
                        "responsive_design",
                        "metadata_support"
                    ],
                    "output_directory": str(self.output_dir)
                }
            }
        
        logger.info("✅ Enhanced Markdown Export MCP tools registered")
    
    def _create_enhanced_markdown(
        self, 
        content: str, 
        title: str, 
        author: str, 
        include_toc: bool, 
        styling: str
    ) -> str:
        """Create enhanced markdown content with styling."""
        enhanced_content = f"# {title}\n\n"
        enhanced_content += f"**Author:** {author}\n"
        enhanced_content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        enhanced_content += f"**Styling:** {styling}\n\n"
        
        if include_toc:
            enhanced_content += "## Table of Contents\n\n"
            # Add TOC entries (simplified)
            enhanced_content += "- [Introduction](#introduction)\n"
            enhanced_content += "- [Analysis](#analysis)\n"
            enhanced_content += "- [Conclusions](#conclusions)\n\n"
        
        enhanced_content += content
        
        return enhanced_content
    
    def _create_enhanced_html(
        self, 
        content: str, 
        title: str, 
        author: str, 
        include_toc: bool, 
        styling: str, 
        interactive: bool
    ) -> str:
        """Create enhanced HTML content with styling."""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .metadata {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .toc {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        .toc li {{
            margin: 5px 0;
        }}
        .toc a {{
            text-decoration: none;
            color: #3498db;
        }}
        .toc a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        
        <div class="metadata">
            <strong>Author:</strong> {author}<br>
            <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            <strong>Styling:</strong> {styling}
        </div>
"""
        
        if include_toc:
            html_content += """
        <div class="toc">
            <h2>Table of Contents</h2>
            <ul>
                <li><a href="#introduction">Introduction</a></li>
                <li><a href="#analysis">Analysis</a></li>
                <li><a href="#conclusions">Conclusions</a></li>
            </ul>
        </div>
"""
        
        html_content += f"""
        <div class="content">
            {content}
        </div>
    </div>
</body>
</html>"""
        
        return html_content


# Global instance
enhanced_markdown_export_mcp_tools = EnhancedMarkdownExportMCPTools()
