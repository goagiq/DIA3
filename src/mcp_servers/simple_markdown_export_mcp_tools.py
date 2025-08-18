"""
Simple Markdown Export MCP Tools

Provides MCP tools for exporting markdown content to PDF and Word documents
using the simplified export service that doesn't require WeasyPrint.
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from loguru import logger

# Import simple markdown export service
try:
    from src.core.export.simple_markdown_export_service import SimpleMarkdownExportService
    SIMPLE_MARKDOWN_EXPORT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Simple markdown export service not available: {e}")
    SIMPLE_MARKDOWN_EXPORT_AVAILABLE = False

class SimpleMarkdownExportMCPTools:
    """MCP tools for simple markdown export functionality."""
    
    def __init__(self):
        """Initialize simple markdown export MCP tools."""
        self.export_service = None
        self.output_dir = None
        
        if SIMPLE_MARKDOWN_EXPORT_AVAILABLE:
            try:
                # Initialize with default output directory
                self.output_dir = Path("docs/white_papers")
                self.output_dir.mkdir(parents=True, exist_ok=True)
                self.export_service = SimpleMarkdownExportService(str(self.output_dir))
                logger.info("✅ Simple markdown export MCP tools initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize simple markdown export MCP tools: {e}")
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools."""
        if not SIMPLE_MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return []
        
        return [
            {
                "type": "function",
                "function": {
                    "name": "simple_markdown_export_to_pdf",
                    "description": "Export markdown content to PDF document using simplified service (no WeasyPrint required).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "markdown_content": {
                                "type": "string",
                                "description": "Markdown content to export"
                            },
                            "filename": {
                                "type": "string",
                                "description": "Output filename (without extension)",
                                "default": None
                            },
                            "template_config": {
                                "type": "object",
                                "description": "Template configuration for styling",
                                "default": None
                            }
                        },
                        "required": ["markdown_content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "simple_markdown_export_to_word",
                    "description": "Export markdown content to Word document using simplified service.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "markdown_content": {
                                "type": "string",
                                "description": "Markdown content to export"
                            },
                            "filename": {
                                "type": "string",
                                "description": "Output filename (without extension)",
                                "default": None
                            },
                            "template_config": {
                                "type": "object",
                                "description": "Template configuration for styling",
                                "default": None
                            }
                        },
                        "required": ["markdown_content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "simple_markdown_export_to_both",
                    "description": "Export markdown content to both PDF and Word documents using simplified service.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "markdown_content": {
                                "type": "string",
                                "description": "Markdown content to export"
                            },
                            "filename": {
                                "type": "string",
                                "description": "Output filename (without extension)",
                                "default": None
                            },
                            "template_config": {
                                "type": "object",
                                "description": "Template configuration for styling",
                                "default": None
                            }
                        },
                        "required": ["markdown_content"]
                    }
                }
            }
        ]
    
    async def simple_markdown_export_to_pdf(self, markdown_content: str, filename: Optional[str] = None, template_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Export markdown content to PDF using simplified service."""
        if not SIMPLE_MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Simple markdown export service is not available"
            }
        
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"export_{timestamp}"
            
            # Export to PDF
            result = await self.export_service.export_markdown_to_pdf(
                markdown_content,
                output_filename=f"{filename}.pdf",
                template_name="whitepaper",
                custom_template=template_config
            )
            
            success = result.get("success", False)
            
            if success:
                return {
                    "success": True,
                    "message": "Successfully exported to PDF",
                    "file_path": result.get("output_path", ""),
                    "file_size": result.get("file_size", 0),
                    "filename": f"{filename}.pdf"
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Failed to export to PDF")
                }
                
        except Exception as e:
            logger.error(f"Error exporting to PDF: {e}")
            return {
                "success": False,
                "error": f"Export failed: {str(e)}"
            }
    
    async def simple_markdown_export_to_word(self, markdown_content: str, filename: Optional[str] = None, template_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Export markdown content to Word document using simplified service."""
        if not SIMPLE_MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Simple markdown export service is not available"
            }
        
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"export_{timestamp}"
            
            # Export to Word
            result = await self.export_service.export_markdown_to_word(
                markdown_content,
                output_filename=f"{filename}.docx",
                template_name="whitepaper",
                custom_template=template_config
            )
            
            success = result.get("success", False)
            
            if success:
                return {
                    "success": True,
                    "message": "Successfully exported to Word",
                    "file_path": result.get("output_path", ""),
                    "file_size": result.get("file_size", 0),
                    "filename": f"{filename}.docx"
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Failed to export to Word")
                }
                
        except Exception as e:
            logger.error(f"Error exporting to Word: {e}")
            return {
                "success": False,
                "error": f"Export failed: {str(e)}"
            }
    
    async def simple_markdown_export_to_both(self, markdown_content: str, filename: Optional[str] = None, template_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Export markdown content to both PDF and Word documents using simplified service."""
        if not SIMPLE_MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Simple markdown export service is not available"
            }
        
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"export_{timestamp}"
            
            # Export to both formats
            result = await self.export_service.export_markdown_to_both(
                markdown_content,
                output_filename=filename,
                template_name="whitepaper",
                custom_template=template_config
            )
            
            success = result.get("success", False)
            
            if success:
                pdf_result = result.get("pdf_result", {})
                word_result = result.get("word_result", {})
                
                return {
                    "success": True,
                    "message": "Successfully exported to both PDF and Word",
                    "pdf_file_path": pdf_result.get("output_path", ""),
                    "pdf_file_size": pdf_result.get("file_size", 0),
                    "word_file_path": word_result.get("output_path", ""),
                    "word_file_size": word_result.get("file_size", 0),
                    "pdf_filename": f"{filename}.pdf",
                    "word_filename": f"{filename}.docx"
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Failed to export to both formats")
                }
                
        except Exception as e:
            logger.error(f"Error exporting to both formats: {e}")
            return {
                "success": False,
                "error": f"Export failed: {str(e)}"
            }
