#!/usr/bin/env python3
"""
PDF Generation MCP Tools

This module provides MCP tools for PDF generation with mermaid diagram support.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from loguru import logger

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.enhanced_pdf_generation_service import enhanced_pdf_service
    PDF_GENERATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced PDF generation service not available: {e}")
    PDF_GENERATION_AVAILABLE = False


class PDFGenerationMCPTools:
    """MCP tools for PDF generation with mermaid diagram support."""
    
    def __init__(self):
        """Initialize the PDF generation MCP tools."""
        self.service = enhanced_pdf_service if PDF_GENERATION_AVAILABLE else None
        logger.info("✅ PDF Generation MCP Tools initialized")
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available PDF generation tools."""
        if not PDF_GENERATION_AVAILABLE:
            return []
        
        return [
            {
                "name": "generate_pdf_from_markdown",
                "description": "Generate PDF-ready HTML from markdown file with mermaid diagram support",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "markdown_file": {
                            "type": "string",
                            "description": "Path to the markdown file to convert"
                        },
                        "output_name": {
                            "type": "string",
                            "description": "Optional output name for the generated file"
                        },
                        "title": {
                            "type": "string",
                            "description": "Optional title for the document"
                        }
                    },
                    "required": ["markdown_file"]
                }
            },
            {
                "name": "generate_white_paper_pdfs",
                "description": "Generate PDFs for all white papers with mermaid diagram support",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "list_available_white_papers",
                "description": "List available white paper markdown files",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]
    
    async def generate_pdf_from_markdown(self, markdown_file: str, output_name: str = None, title: str = None) -> Dict[str, Any]:
        """Generate PDF-ready HTML from markdown file."""
        if not PDF_GENERATION_AVAILABLE:
            return {
                "success": False,
                "error": "PDF generation service not available"
            }
        
        try:
            logger.info(f"📄 Generating PDF from markdown: {markdown_file}")
            
            result = await self.service.generate_pdf_from_markdown(
                markdown_file=markdown_file,
                output_name=output_name,
                title=title
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_white_paper_pdfs(self) -> Dict[str, Any]:
        """Generate PDFs for all white papers."""
        if not PDF_GENERATION_AVAILABLE:
            return {
                "success": False,
                "error": "PDF generation service not available"
            }
        
        try:
            logger.info("📄 Generating white paper PDFs")
            
            result = await self.service.generate_white_paper_pdfs()
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating white paper PDFs: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_available_white_papers(self) -> Dict[str, Any]:
        """List available white paper markdown files."""
        if not PDF_GENERATION_AVAILABLE:
            return {
                "success": False,
                "error": "PDF generation service not available"
            }
        
        try:
            docs_dir = Path(__file__).parent.parent.parent / "docs" / "white_papers"
            
            white_papers = []
            if docs_dir.exists():
                for file in docs_dir.glob("*.md"):
                    white_papers.append({
                        "filename": file.name,
                        "path": str(file),
                        "size": file.stat().st_size,
                        "modified": file.stat().st_mtime
                    })
            
            return {
                "success": True,
                "white_papers": white_papers,
                "count": len(white_papers)
            }
            
        except Exception as e:
            logger.error(f"Error listing white papers: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Global instance
pdf_generation_mcp_tools = PDFGenerationMCPTools()
