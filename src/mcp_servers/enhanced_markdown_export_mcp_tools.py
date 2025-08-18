"""
Enhanced Markdown Export MCP Tools

Provides MCP tools for exporting markdown content to PDF and Word documents with enhanced formatting.
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from loguru import logger

# Import enhanced markdown export service
try:
    from src.core.export.enhanced_markdown_export_service import EnhancedMarkdownExportService
    ENHANCED_MARKDOWN_EXPORT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced markdown export service not available: {e}")
    ENHANCED_MARKDOWN_EXPORT_AVAILABLE = False

class EnhancedMarkdownExportMCPTools:
    """MCP tools for enhanced markdown export functionality."""
    
    def __init__(self):
        """Initialize enhanced markdown export MCP tools."""
        self.export_service = None
        self.output_dir = None
        
        if ENHANCED_MARKDOWN_EXPORT_AVAILABLE:
            try:
                # Initialize with default output directory
                self.output_dir = Path("docs/white_papers/generated_pdfs")
                self.output_dir.mkdir(parents=True, exist_ok=True)
                self.export_service = EnhancedMarkdownExportService(str(self.output_dir))
                logger.info("✅ Enhanced markdown export MCP tools initialized (output: docs/white_papers/generated_pdfs)")
            except Exception as e:
                logger.error(f"❌ Failed to initialize enhanced markdown export MCP tools: {e}")
                # Don't modify the global variable here
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools."""
        if not ENHANCED_MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return []
        
        return [
            {
                "type": "function",
                "function": {
                    "name": "enhanced_markdown_export_to_pdf",
                    "description": "Export markdown content to PDF document with enhanced formatting including figure numbering, proper markdown tag conversion, image embedding, and professional styling.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "markdown_content": {
                                "type": "string",
                                "description": "Markdown content to export with enhanced formatting support"
                            },
                            "filename": {
                                "type": "string",
                                "description": "Output filename (without extension)",
                                "default": None
                            },
                            "include_images": {
                                "type": "boolean",
                                "description": "Whether to include and embed images",
                                "default": True
                            },
                            "figure_numbering": {
                                "type": "boolean",
                                "description": "Whether to use sequential figure numbering",
                                "default": True
                            }
                        },
                        "required": ["markdown_content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "enhanced_markdown_export_to_word",
                    "description": "Export markdown content to Word document with enhanced formatting including figure numbering, proper markdown tag conversion, image embedding, and professional styling.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "markdown_content": {
                                "type": "string",
                                "description": "Markdown content to export with enhanced formatting support"
                            },
                            "filename": {
                                "type": "string",
                                "description": "Output filename (without extension)",
                                "default": None
                            },
                            "include_images": {
                                "type": "boolean",
                                "description": "Whether to include and embed images",
                                "default": True
                            },
                            "figure_numbering": {
                                "type": "boolean",
                                "description": "Whether to use sequential figure numbering",
                                "default": True
                            }
                        },
                        "required": ["markdown_content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "enhanced_markdown_export_both_formats",
                    "description": "Export markdown content to both PDF and Word documents with enhanced formatting.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "markdown_content": {
                                "type": "string",
                                "description": "Markdown content to export with enhanced formatting support"
                            },
                            "filename": {
                                "type": "string",
                                "description": "Output filename (without extension)",
                                "default": None
                            },
                            "include_images": {
                                "type": "boolean",
                                "description": "Whether to include and embed images",
                                "default": True
                            },
                            "figure_numbering": {
                                "type": "boolean",
                                "description": "Whether to use sequential figure numbering",
                                "default": True
                            }
                        },
                        "required": ["markdown_content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_enhanced_markdown_export_status",
                    "description": "Get status and capabilities of the enhanced markdown export service.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ]
    
    async def enhanced_markdown_export_to_pdf(self, markdown_content: str, filename: Optional[str] = None, 
                                           include_images: bool = True, figure_numbering: bool = True) -> Dict[str, Any]:
        """Export markdown content to PDF with enhanced formatting."""
        if not ENHANCED_MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Enhanced markdown export service is not available"
            }
        
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"enhanced_export_{timestamp}"
            
            # Export to PDF
            result = await self.export_service.export_markdown_to_pdf_enhanced(
                markdown_content=markdown_content,
                output_filename=f"{filename}.pdf"
            )
            
            if result.get("success"):
                return {
                    "success": True,
                    "message": "Enhanced PDF export completed successfully",
                    "file_path": result.get("output_path"),
                    "file_size": result.get("file_size"),
                    "format": "pdf",
                    "operation_id": result.get("operation_id")
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error during PDF export")
                }
                
        except Exception as e:
            logger.error(f"Error in enhanced PDF export: {e}")
            return {
                "success": False,
                "error": f"PDF export failed: {str(e)}"
            }
    
    async def enhanced_markdown_export_to_word(self, markdown_content: str, filename: Optional[str] = None,
                                             include_images: bool = True, figure_numbering: bool = True) -> Dict[str, Any]:
        """Export markdown content to Word with enhanced formatting."""
        if not ENHANCED_MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Enhanced markdown export service is not available"
            }
        
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"enhanced_export_{timestamp}"
            
            # Export to Word
            result = await self.export_service.export_markdown_to_word_enhanced(
                markdown_content=markdown_content,
                output_filename=f"{filename}.docx"
            )
            
            if result.get("success"):
                return {
                    "success": True,
                    "message": "Enhanced Word export completed successfully",
                    "file_path": result.get("output_path"),
                    "file_size": result.get("file_size"),
                    "format": "word",
                    "operation_id": result.get("operation_id")
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error during Word export")
                }
                
        except Exception as e:
            logger.error(f"Error in enhanced Word export: {e}")
            return {
                "success": False,
                "error": f"Word export failed: {str(e)}"
            }
    
    async def enhanced_markdown_export_both_formats(self, markdown_content: str, filename: Optional[str] = None,
                                                  include_images: bool = True, figure_numbering: bool = True) -> Dict[str, Any]:
        """Export markdown content to both PDF and Word formats with enhanced formatting."""
        if not ENHANCED_MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Enhanced markdown export service is not available"
            }
        
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"enhanced_export_{timestamp}"
            
            results = {}
            
            # Export to PDF
            pdf_result = await self.export_service.export_markdown_to_pdf_enhanced(
                markdown_content=markdown_content,
                output_filename=f"{filename}.pdf"
            )
            
            if pdf_result.get("success"):
                results["pdf"] = {
                    "success": True,
                    "file_path": pdf_result.get("output_path"),
                    "file_size": pdf_result.get("file_size"),
                    "operation_id": pdf_result.get("operation_id")
                }
            else:
                results["pdf"] = {
                    "success": False,
                    "error": pdf_result.get("error", "Unknown error during PDF export")
                }
            
            # Export to Word
            word_result = await self.export_service.export_markdown_to_word_enhanced(
                markdown_content=markdown_content,
                output_filename=f"{filename}.docx"
            )
            
            if word_result.get("success"):
                results["word"] = {
                    "success": True,
                    "file_path": word_result.get("output_path"),
                    "file_size": word_result.get("file_size"),
                    "operation_id": word_result.get("operation_id")
                }
            else:
                results["word"] = {
                    "success": False,
                    "error": word_result.get("error", "Unknown error during Word export")
                }
            
            # Determine overall success
            overall_success = results["pdf"]["success"] or results["word"]["success"]
            
            return {
                "success": overall_success,
                "message": "Enhanced export completed",
                "results": results,
                "pdf_success": results["pdf"]["success"],
                "word_success": results["word"]["success"]
            }
                
        except Exception as e:
            logger.error(f"Error in enhanced dual format export: {e}")
            return {
                "success": False,
                "error": f"Dual format export failed: {str(e)}"
            }
    
    async def get_enhanced_markdown_export_status(self) -> Dict[str, Any]:
        """Get status and capabilities of the enhanced markdown export service."""
        return {
            "service_available": ENHANCED_MARKDOWN_EXPORT_AVAILABLE and self.export_service is not None,
            "version": "2.3.0",
            "supported_formats": ["pdf", "word"] if ENHANCED_MARKDOWN_EXPORT_AVAILABLE else [],
            "features": [
                "Enhanced markdown formatting (bold, italic)",
                "Figure numbering with sequential numbering",
                "Image embedding with actual diagram support",
                "Table formatting with proper text wrapping",
                "Professional styling and typography",
                "Mermaid diagram support",
                "Custom paragraph and heading styles",
                "Code block formatting",
                "List formatting with bullet points",
                "Special text protection (e.g., 'Narrative' not bolded)"
            ] if ENHANCED_MARKDOWN_EXPORT_AVAILABLE else [],
            "output_directory": str(self.output_dir) if self.output_dir else None
        }
