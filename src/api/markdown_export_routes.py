"""
Markdown Export API Routes

Provides API endpoints for exporting markdown content to PDF and Word documents.
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

# Import markdown export service
try:
    from src.core.export.markdown_export_service import MarkdownExportService
    MARKDOWN_EXPORT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Markdown export service not available: {e}")
    MARKDOWN_EXPORT_AVAILABLE = False

router = APIRouter(prefix="/api/v1/markdown-export", tags=["Markdown Export"])

# Pydantic models
class MarkdownExportRequest(BaseModel):
    """Request model for markdown export."""
    model_config = ConfigDict(extra="forbid")
    
    markdown_content: str
    output_format: str = "pdf"  # "pdf" or "word"
    template_config: Optional[Dict[str, Any]] = None
    filename: Optional[str] = None

class MarkdownExportResponse(BaseModel):
    """Response model for markdown export."""
    model_config = ConfigDict(extra="forbid")
    
    success: bool
    message: str
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    export_time: Optional[float] = None
    error: Optional[str] = None

class MarkdownExportStatus(BaseModel):
    """Status model for markdown export service."""
    model_config = ConfigDict(extra="forbid")
    
    service_available: bool
    supported_formats: List[str]
    version: str = "1.0.0"

# Initialize export service
export_service = None
if MARKDOWN_EXPORT_AVAILABLE:
    try:
        # Initialize with default output directory
        output_dir = Path("temp_output/markdown_exports")
        output_dir.mkdir(parents=True, exist_ok=True)
        export_service = MarkdownExportService(str(output_dir))
        logger.info("✅ Markdown export service initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize markdown export service: {e}")
        MARKDOWN_EXPORT_AVAILABLE = False

@router.get("/health", response_model=MarkdownExportStatus)
async def health_check():
    """Health check for markdown export service."""
    return MarkdownExportStatus(
        service_available=MARKDOWN_EXPORT_AVAILABLE and export_service is not None,
        supported_formats=["pdf", "word"] if MARKDOWN_EXPORT_AVAILABLE else [],
        version="1.0.0"
    )

@router.post("/export", response_model=MarkdownExportResponse)
async def export_markdown(request: MarkdownExportRequest):
    """Export markdown content to PDF or Word document."""
    if not MARKDOWN_EXPORT_AVAILABLE or export_service is None:
        raise HTTPException(
            status_code=503,
            detail="Markdown export service is not available"
        )
    
    if request.output_format not in ["pdf", "word"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported output format. Supported formats: pdf, word"
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
            success = await export_service.export_to_pdf_async(
                request.markdown_content,
                request.filename,
                request.template_config
            )
            file_extension = "pdf"
        else:  # word
            success = await export_service.export_to_word_async(
                request.markdown_content,
                request.filename,
                request.template_config
            )
            file_extension = "docx"
        
        if success:
            # Get file path and size
            file_path = export_service.output_dir / f"{request.filename}.{file_extension}"
            file_size = file_path.stat().st_size if file_path.exists() else 0
            
            export_time = (datetime.now() - start_time).total_seconds()
            
            return MarkdownExportResponse(
                success=True,
                message=f"Successfully exported to {request.output_format.upper()}",
                file_path=str(file_path),
                file_size=file_size,
                export_time=export_time
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to export markdown content"
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
    if not MARKDOWN_EXPORT_AVAILABLE or export_service is None:
        raise HTTPException(
            status_code=503,
            detail="Markdown export service is not available"
        )
    
    if output_format not in ["pdf", "word"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported output format. Supported formats: pdf, word"
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
            success = await export_service.export_to_pdf_async(
                markdown_content,
                export_filename,
                template_config_dict
            )
            file_extension = "pdf"
        else:  # word
            success = await export_service.export_to_word_async(
                markdown_content,
                export_filename,
                template_config_dict
            )
            file_extension = "docx"
        
        if success:
            # Return the exported file
            file_path = export_service.output_dir / f"{export_filename}.{file_extension}"
            if file_path.exists():
                return FileResponse(
                    path=str(file_path),
                    filename=f"{export_filename}.{file_extension}",
                    media_type=f"application/{file_extension}"
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Exported file not found"
                )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to export markdown file"
            )
            
    except Exception as e:
        logger.error(f"Error exporting markdown file: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Export failed: {str(e)}"
        )

@router.get("/download/{filename}")
async def download_exported_file(filename: str):
    """Download an exported file."""
    if not MARKDOWN_EXPORT_AVAILABLE or export_service is None:
        raise HTTPException(
            status_code=503,
            detail="Markdown export service is not available"
        )
    
    try:
        file_path = export_service.output_dir / filename
        
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        # Determine content type
        if filename.endswith('.pdf'):
            media_type = "application/pdf"
        elif filename.endswith('.docx'):
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        else:
            media_type = "application/octet-stream"
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type=media_type
        )
        
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Download failed: {str(e)}"
        )

@router.get("/files")
async def list_exported_files():
    """List all exported files."""
    if not MARKDOWN_EXPORT_AVAILABLE or export_service is None:
        raise HTTPException(
            status_code=503,
            detail="Markdown export service is not available"
        )
    
    try:
        files = []
        for file_path in export_service.output_dir.glob("*"):
            if file_path.is_file() and file_path.suffix in ['.pdf', '.docx']:
                stat = file_path.stat()
                files.append({
                    "filename": file_path.name,
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        return {"files": files}
        
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list files: {str(e)}"
        )

@router.delete("/files/{filename}")
async def delete_exported_file(filename: str):
    """Delete an exported file."""
    if not MARKDOWN_EXPORT_AVAILABLE or export_service is None:
        raise HTTPException(
            status_code=503,
            detail="Markdown export service is not available"
        )
    
    try:
        file_path = export_service.output_dir / filename
        
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        file_path.unlink()
        return {"message": f"File {filename} deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Delete failed: {str(e)}"
        )
