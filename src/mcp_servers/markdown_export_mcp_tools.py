"""
Markdown Export MCP Tools

Provides MCP tools for exporting markdown content to PDF and Word documents.
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from loguru import logger

# Import markdown export service
try:
    from src.core.export.markdown_export_service import MarkdownExportService
    MARKDOWN_EXPORT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Markdown export service not available: {e}")
    MARKDOWN_EXPORT_AVAILABLE = False

class MarkdownExportMCPTools:
    """MCP tools for markdown export functionality."""
    
    def __init__(self):
        """Initialize markdown export MCP tools."""
        self.export_service = None
        self.output_dir = None
        
        if MARKDOWN_EXPORT_AVAILABLE:
            try:
                # Initialize with default output directory
                self.output_dir = Path("docs/white_papers")
                self.output_dir.mkdir(parents=True, exist_ok=True)
                self.export_service = MarkdownExportService(str(self.output_dir))
                logger.info("✅ Markdown export MCP tools initialized (output: docs/white_papers)")
            except Exception as e:
                logger.error(f"❌ Failed to initialize markdown export MCP tools: {e}")
                # Don't modify the global variable here
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools."""
        if not MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return []
        
        return [
            {
                "type": "function",
                "function": {
                    "name": "markdown_export_to_pdf",
                    "description": "Export markdown content to PDF document with comprehensive formatting support including images, tables, and Mermaid diagrams.",
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
                    "name": "markdown_export_to_word",
                    "description": "Export markdown content to Word document with comprehensive formatting support including images, tables, and Mermaid diagrams.",
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
                    "name": "markdown_export_batch",
                    "description": "Export multiple markdown contents to both PDF and Word formats.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "exports": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "markdown_content": {
                                            "type": "string",
                                            "description": "Markdown content to export"
                                        },
                                        "filename": {
                                            "type": "string",
                                            "description": "Output filename (without extension)"
                                        },
                                        "formats": {
                                            "type": "array",
                                            "items": {
                                                "type": "string",
                                                "enum": ["pdf", "word"]
                                            },
                                            "description": "Output formats",
                                            "default": ["pdf", "word"]
                                        }
                                    },
                                    "required": ["markdown_content", "filename"]
                                },
                                "description": "List of exports to perform"
                            }
                        },
                        "required": ["exports"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "markdown_export_list_files",
                    "description": "List all exported files with metadata.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_type": {
                                "type": "string",
                                "enum": ["pdf", "word", "all"],
                                "description": "Filter by file type",
                                "default": "all"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "markdown_export_get_file_info",
                    "description": "Get detailed information about a specific exported file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": "Filename to get info for"
                            }
                        },
                        "required": ["filename"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "markdown_export_delete_file",
                    "description": "Delete a specific exported file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filename": {
                                "type": "string",
                                "description": "Filename to delete"
                            }
                        },
                        "required": ["filename"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "markdown_export_cleanup",
                    "description": "Clean up old exported files based on age or count.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "max_age_hours": {
                                "type": "integer",
                                "description": "Maximum age in hours",
                                "default": 24
                            },
                            "max_files": {
                                "type": "integer",
                                "description": "Maximum number of files to keep",
                                "default": 100
                            }
                        }
                    }
                }
            }
        ]
    
    async def markdown_export_to_pdf(self, markdown_content: str, filename: Optional[str] = None, template_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Export markdown content to PDF."""
        if not MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Markdown export service is not available"
            }
        
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"export_{timestamp}"
            
            # Set default template config if not provided
            if template_config is None:
                template_config = {
                    "page_size": "A4",
                    "margins": {"top": 1, "bottom": 1, "left": 1, "right": 1}
                }
            
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
                    "error": "Failed to export to PDF"
                }
                
        except Exception as e:
            logger.error(f"Error exporting to PDF: {e}")
            return {
                "success": False,
                "error": f"Export failed: {str(e)}"
            }
    
    async def markdown_export_to_word(self, markdown_content: str, filename: Optional[str] = None, template_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Export markdown content to Word document."""
        if not MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Markdown export service is not available"
            }
        
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"export_{timestamp}"
            
            # Set default template config if not provided
            if template_config is None:
                template_config = {
                    "page_size": "A4",
                    "margins": {"top": 1, "bottom": 1, "left": 1, "right": 1}
                }
            
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
                    "error": "Failed to export to Word"
                }
                
        except Exception as e:
            logger.error(f"Error exporting to Word: {e}")
            return {
                "success": False,
                "error": f"Export failed: {str(e)}"
            }
    
    async def markdown_export_batch(self, exports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Export multiple markdown contents to both PDF and Word formats."""
        if not MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Markdown export service is not available"
            }
        
        try:
            results = []
            total_exports = len(exports)
            
            for i, export_config in enumerate(exports):
                markdown_content = export_config["markdown_content"]
                filename = export_config["filename"]
                formats = export_config.get("formats", ["pdf", "word"])
                
                export_result = {
                    "filename": filename,
                    "formats": formats,
                    "results": {}
                }
                
                for format_type in formats:
                    if format_type == "pdf":
                        result = await self.markdown_export_to_pdf(markdown_content, filename)
                        export_result["results"]["pdf"] = result
                    elif format_type == "word":
                        result = await self.markdown_export_to_word(markdown_content, filename)
                        export_result["results"]["word"] = result
                
                results.append(export_result)
                
                # Log progress
                logger.info(f"Batch export progress: {i+1}/{total_exports}")
            
            return {
                "success": True,
                "message": f"Batch export completed: {total_exports} exports",
                "results": results
            }
                
        except Exception as e:
            logger.error(f"Error in batch export: {e}")
            return {
                "success": False,
                "error": f"Batch export failed: {str(e)}"
            }
    
    async def markdown_export_list_files(self, file_type: str = "all") -> Dict[str, Any]:
        """List all exported files with metadata."""
        if not MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Markdown export service is not available"
            }
        
        try:
            files = []
            for file_path in self.output_dir.glob("*"):
                if file_path.is_file():
                    # Filter by file type
                    if file_type == "pdf" and not file_path.suffix == ".pdf":
                        continue
                    elif file_type == "word" and not file_path.suffix == ".docx":
                        continue
                    elif file_type == "all" and file_path.suffix not in [".pdf", ".docx"]:
                        continue
                    
                    stat = file_path.stat()
                    files.append({
                        "filename": file_path.name,
                        "size": stat.st_size,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "type": file_path.suffix[1:]  # Remove the dot
                    })
            
            return {
                "success": True,
                "files": files,
                "count": len(files)
            }
                
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return {
                "success": False,
                "error": f"Failed to list files: {str(e)}"
            }
    
    async def markdown_export_get_file_info(self, filename: str) -> Dict[str, Any]:
        """Get detailed information about a specific exported file."""
        if not MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Markdown export service is not available"
            }
        
        try:
            file_path = self.output_dir / filename
            
            if not file_path.exists():
                return {
                    "success": False,
                    "error": "File not found"
                }
            
            stat = file_path.stat()
            
            return {
                "success": True,
                "file_info": {
                    "filename": file_path.name,
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "type": file_path.suffix[1:],
                    "path": str(file_path)
                }
            }
                
        except Exception as e:
            logger.error(f"Error getting file info: {e}")
            return {
                "success": False,
                "error": f"Failed to get file info: {str(e)}"
            }
    
    async def markdown_export_delete_file(self, filename: str) -> Dict[str, Any]:
        """Delete a specific exported file."""
        if not MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Markdown export service is not available"
            }
        
        try:
            file_path = self.output_dir / filename
            
            if not file_path.exists():
                return {
                    "success": False,
                    "error": "File not found"
                }
            
            file_path.unlink()
            
            return {
                "success": True,
                "message": f"File {filename} deleted successfully"
            }
                
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return {
                "success": False,
                "error": f"Delete failed: {str(e)}"
            }
    
    async def markdown_export_cleanup(self, max_age_hours: int = 24, max_files: int = 100) -> Dict[str, Any]:
        """Clean up old exported files based on age or count."""
        if not MARKDOWN_EXPORT_AVAILABLE or self.export_service is None:
            return {
                "success": False,
                "error": "Markdown export service is not available"
            }
        
        try:
            current_time = datetime.now()
            files_to_delete = []
            
            # Get all files
            all_files = []
            for file_path in self.output_dir.glob("*"):
                if file_path.is_file() and file_path.suffix in [".pdf", ".docx"]:
                    stat = file_path.stat()
                    created_time = datetime.fromtimestamp(stat.st_ctime)
                    age_hours = (current_time - created_time).total_seconds() / 3600
                    
                    all_files.append({
                        "path": file_path,
                        "created": created_time,
                        "age_hours": age_hours,
                        "size": stat.st_size
                    })
            
            # Sort by creation time (oldest first)
            all_files.sort(key=lambda x: x["created"])
            
            # Find files to delete based on age
            for file_info in all_files:
                if file_info["age_hours"] > max_age_hours:
                    files_to_delete.append(file_info["path"])
            
            # If we still have too many files, delete the oldest ones
            remaining_files = [f for f in all_files if f["path"] not in files_to_delete]
            if len(remaining_files) > max_files:
                files_to_delete.extend([f["path"] for f in remaining_files[:len(remaining_files) - max_files]])
            
            # Delete files
            deleted_count = 0
            for file_path in files_to_delete:
                try:
                    file_path.unlink()
                    deleted_count += 1
                except Exception as e:
                    logger.warning(f"Failed to delete {file_path}: {e}")
            
            return {
                "success": True,
                "message": f"Cleanup completed: {deleted_count} files deleted",
                "deleted_count": deleted_count,
                "remaining_files": len(all_files) - deleted_count
            }
                
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            return {
                "success": False,
                "error": f"Cleanup failed: {str(e)}"
            }
