"""
Simple Markdown Export API Routes

Provides API endpoints for exporting markdown content to PDF and Word documents
using the simplified export service that doesn't require WeasyPrint.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from pathlib import Path
import tempfile
import os
import uuid
from datetime import datetime
from loguru import logger

# Import simple markdown export service
try:
    from src.core.export.simple_markdown_export_service import SimpleMarkdownExportService
    SIMPLE_MARKDOWN_EXPORT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Simple markdown export service not available: {e}")
    SIMPLE_MARKDOWN_EXPORT_AVAILABLE = False

router = APIRouter(prefix="/api/v1/simple-markdown-export", tags=["Simple Markdown Export"])

# Pydantic models
class SimpleMarkdownExportRequest(BaseModel):
    """Request model for simple markdown export."""
    model_config = ConfigDict(extra="forbid")
    
    markdown_content: str
    output_format: str = "pdf"  # "pdf", "word", or "both"
    template_config: Optional[Dict[str, Any]] = None
    filename: Optional[str] = None

class SimpleMarkdownExportResponse(BaseModel):
    """Response model for simple markdown export."""
    model_config = ConfigDict(extra="forbid")
    
    success: bool
    message: str
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    export_time: Optional[float] = None
    error: Optional[str] = None

class SimpleMarkdownExportStatus(BaseModel):
    """Status model for simple markdown export service."""
    model_config = ConfigDict(extra="forbid")
    
    service_available: bool
    supported_formats: List[str]
    version: str = "1.0.0"

# Initialize export service
export_service = None
if SIMPLE_MARKDOWN_EXPORT_AVAILABLE:
    try:
        # Initialize with default output directory
        output_dir = Path("temp_output/simple_markdown_exports")
        output_dir.mkdir(parents=True, exist_ok=True)
        export_service = SimpleMarkdownExportService(str(output_dir))
        logger.info("✅ Simple markdown export service initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize simple markdown export service: {e}")
        SIMPLE_MARKDOWN_EXPORT_AVAILABLE = False

@router.get("/health", response_model=SimpleMarkdownExportStatus)
async def health_check():
    """Health check for simple markdown export service."""
    return SimpleMarkdownExportStatus(
        service_available=SIMPLE_MARKDOWN_EXPORT_AVAILABLE and export_service is not None,
        supported_formats=["pdf", "word", "both"] if SIMPLE_MARKDOWN_EXPORT_AVAILABLE else [],
        version="1.0.0"
    )

@router.post("/export", response_model=SimpleMarkdownExportResponse)
async def export_markdown(request: SimpleMarkdownExportRequest):
    """Export markdown content to PDF or Word document."""
    if not SIMPLE_MARKDOWN_EXPORT_AVAILABLE or export_service is None:
        raise HTTPException(
            status_code=503,
            detail="Simple markdown export service is not available"
        )
    
    if request.output_format not in ["pdf", "word", "both"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported output format. Supported formats: pdf, word, both"
        )
    
    try:
        start_time = datetime.now()
        
        # Generate filename if not provided
        if not request.filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            request.filename = f"export_{timestamp}"
        
        # Set default template config if not provided
        if request.template_config is None:
            request.template_config = {
                "page_size": "A4",
                "margins": {"top": 1, "bottom": 1, "left": 1, "right": 1}
            }
        
        # Export based on format
        if request.output_format == "pdf":
            result = await export_service.export_markdown_to_pdf(
                request.markdown_content,
                output_filename=f"{request.filename}.pdf",
                template_name="whitepaper",
                custom_template=request.template_config
            )
            file_extension = "pdf"
        elif request.output_format == "word":
            result = await export_service.export_markdown_to_word(
                request.markdown_content,
                output_filename=f"{request.filename}.docx",
                template_name="whitepaper",
                custom_template=request.template_config
            )
            file_extension = "docx"
        else:  # both
            result = await export_service.export_markdown_to_both(
                request.markdown_content,
                output_filename=request.filename,
                template_name="whitepaper",
                custom_template=request.template_config
            )
            file_extension = "both"
        
        if result.get("success", False):
            # Get file path and size
            if request.output_format == "both":
                pdf_result = result.get("pdf_result", {})
                word_result = result.get("word_result", {})
                file_path = pdf_result.get("output_path", "")
                file_size = pdf_result.get("file_size", 0)
            else:
                file_path = result.get("output_path", "")
                file_size = result.get("file_size", 0)
            
            export_time = (datetime.now() - start_time).total_seconds()
            
            return SimpleMarkdownExportResponse(
                success=True,
                message=f"Successfully exported to {request.output_format.upper()}",
                file_path=file_path,
                file_size=file_size,
                export_time=export_time
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to export markdown content: {result.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        logger.error(f"Error exporting markdown: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Export failed: {str(e)}"
        )

@router.post("/export-file")
async def export_markdown_file(
    file: UploadFile = File(...),
    output_format: str = Form("pdf"),
    template_config: Optional[str] = Form(None)
):
    """Export markdown file to PDF or Word document."""
    if not SIMPLE_MARKDOWN_EXPORT_AVAILABLE or export_service is None:
        raise HTTPException(
            status_code=503,
            detail="Simple markdown export service is not available"
        )
    
    if output_format not in ["pdf", "word", "both"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported output format. Supported formats: pdf, word, both"
        )
    
    if not file.filename.endswith('.md'):
        raise HTTPException(
            status_code=400,
            detail="File must be a markdown file (.md)"
        )
    
    try:
        # Read markdown content
        content = await file.read()
        markdown_content = content.decode('utf-8')
        
        # Parse template config if provided
        template_config_dict = None
        if template_config:
            import json
            try:
                template_config_dict = json.loads(template_config)
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid template configuration JSON"
                )
        
        # Generate filename from original file
        base_filename = Path(file.filename).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_filename = f"{base_filename}_{timestamp}"
        
        # Export
        if output_format == "pdf":
            result = await export_service.export_markdown_to_pdf(
                markdown_content,
                output_filename=f"{export_filename}.pdf",
                template_name="whitepaper",
                custom_template=template_config_dict
            )
        elif output_format == "word":
            result = await export_service.export_markdown_to_word(
                markdown_content,
                output_filename=f"{export_filename}.docx",
                template_name="whitepaper",
                custom_template=template_config_dict
            )
        else:  # both
            result = await export_service.export_markdown_to_both(
                markdown_content,
                output_filename=export_filename,
                template_name="whitepaper",
                custom_template=template_config_dict
            )
        
        if result.get("success", False):
            if output_format == "both":
                pdf_result = result.get("pdf_result", {})
                word_result = result.get("word_result", {})
                return {
                    "success": True,
                    "message": "Successfully exported to both PDF and Word",
                    "pdf_file_path": pdf_result.get("output_path", ""),
                    "pdf_file_size": pdf_result.get("file_size", 0),
                    "word_file_path": word_result.get("output_path", ""),
                    "word_file_size": word_result.get("file_size", 0)
                }
            else:
                return {
                    "success": True,
                    "message": f"Successfully exported to {output_format.upper()}",
                    "file_path": result.get("output_path", ""),
                    "file_size": result.get("file_size", 0)
                }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to export file: {result.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        logger.error(f"Error exporting file: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Export failed: {str(e)}"
        )

@router.get("/download/{filename}")
async def download_file(filename: str):
    """Download exported file."""
    if not SIMPLE_MARKDOWN_EXPORT_AVAILABLE or export_service is None:
        raise HTTPException(
            status_code=503,
            detail="Simple markdown export service is not available"
        )
    
    try:
        file_path = export_service.output_dir / filename
        
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Download failed: {str(e)}"
        )
