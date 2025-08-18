#!/usr/bin/env python3
"""
Word Document Generation MCP Tools

This module provides MCP tools for Word document generation with mermaid diagram support.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from loguru import logger

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.enhanced_word_generation_service import enhanced_word_service
    WORD_GENERATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced Word generation service not available: {e}")
    WORD_GENERATION_AVAILABLE = False


class WordGenerationMCPTools:
    """MCP tools for Word document generation with mermaid diagram support."""
    
    def __init__(self):
        """Initialize the Word document generation MCP tools."""
        self.service = enhanced_word_service if WORD_GENERATION_AVAILABLE else None
        logger.info("✅ Word Document Generation MCP Tools initialized")
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available Word document generation tools."""
        if not WORD_GENERATION_AVAILABLE:
            return []
        
        return [
            {
                "name": "generate_word_from_markdown",
                "description": "Generate Word document from markdown file with mermaid diagram support",
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
                "name": "generate_white_paper_word_documents",
                "description": "Generate Word documents for all white papers with mermaid diagram support",
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
    
    async def generate_word_from_markdown(self, markdown_file: str, output_name: str = None, title: str = None) -> Dict[str, Any]:
        """Generate Word document from markdown file."""
        if not WORD_GENERATION_AVAILABLE:
            return {
                "success": False,
                "error": "Word document generation service not available"
            }
        
        try:
            logger.info(f"📄 Generating Word document from markdown: {markdown_file}")
            
            result = await self.service.generate_word_from_markdown(
                markdown_file=markdown_file,
                output_name=output_name,
                title=title
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating Word document: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_white_paper_word_documents(self) -> Dict[str, Any]:
        """Generate Word documents for all white papers."""
        if not WORD_GENERATION_AVAILABLE:
            return {
                "success": False,
                "error": "Word document generation service not available"
            }
        
        try:
            logger.info("📄 Generating white paper Word documents")
            
            result = await self.service.generate_white_paper_word_documents()
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating white paper Word documents: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_available_white_papers(self) -> Dict[str, Any]:
        """List available white paper markdown files."""
        if not WORD_GENERATION_AVAILABLE:
            return {
                "success": False,
                "error": "Word document generation service not available"
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
word_generation_mcp_tools = WordGenerationMCPTools()
