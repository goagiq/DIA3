"""
Enhanced Markdown Export API Routes

Provides API endpoints for exporting markdown content to PDF and Word documents with enhanced formatting.
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

# Import enhanced markdown export service
try:
    from src.core.export.enhanced_markdown_export_service import EnhancedMarkdownExportService
    ENHANCED_MARKDOWN_EXPORT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced markdown export service not available: {e}")
    ENHANCED_MARKDOWN_EXPORT_AVAILABLE = False

router = APIRouter(prefix="/api/v1/enhanced-markdown-export", tags=["Enhanced Markdown Export"])

# Pydantic models
class EnhancedMarkdownExportRequest(BaseModel):
    """Request model for enhanced markdown export."""
    model_config = ConfigDict(extra="forbid")
    
    markdown_content: str
    output_format: str = "pdf"  # "pdf" or "word"
    template_config: Optional[Dict[str, Any]] = None
    filename: Optional[str] = None
    include_images: bool = True
    figure_numbering: bool = True

class EnhancedMarkdownExportResponse(BaseModel):
    """Response model for enhanced markdown export."""
    model_config = ConfigDict(extra="forbid")
    
    success: bool
    message: str
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    export_time: Optional[float] = None
    error: Optional[str] = None
    operation_id: Optional[str] = None

class EnhancedMarkdownExportStatus(BaseModel):
    """Status model for enhanced markdown export service."""
    model_config = ConfigDict(extra="forbid")
    
    service_available: bool
    supported_formats: List[str]
    version: str = "2.3.0"
    features: List[str]

# Initialize enhanced export service
enhanced_export_service = None
if ENHANCED_MARKDOWN_EXPORT_AVAILABLE:
    try:
        # Initialize with default output directory
        output_dir = Path("docs/white_papers/generated_pdfs")
        output_dir.mkdir(parents=True, exist_ok=True)
        enhanced_export_service = EnhancedMarkdownExportService(str(output_dir))
        logger.info("✅ Enhanced markdown export service initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize enhanced markdown export service: {e}")
        ENHANCED_MARKDOWN_EXPORT_AVAILABLE = False

@router.get("/health", response_model=EnhancedMarkdownExportStatus)
async def health_check():
    """Health check for enhanced markdown export service."""
    return EnhancedMarkdownExportStatus(
        service_available=ENHANCED_MARKDOWN_EXPORT_AVAILABLE and enhanced_export_service is not None,
        supported_formats=["pdf", "word"] if ENHANCED_MARKDOWN_EXPORT_AVAILABLE else [],
        version="2.3.0",
        features=[
            "Enhanced markdown formatting (bold, italic)",
            "Figure numbering",
            "Image embedding",
            "Table formatting",
            "Professional styling",
            "Mermaid diagram support"
        ] if ENHANCED_MARKDOWN_EXPORT_AVAILABLE else []
    )

@router.post("/export", response_model=EnhancedMarkdownExportResponse)
async def export_enhanced_markdown(request: EnhancedMarkdownExportRequest):
    """Export markdown content to PDF or Word document with enhanced formatting."""
    if not ENHANCED_MARKDOWN_EXPORT_AVAILABLE or enhanced_export_service is None:
        raise HTTPException(
            status_code=503,
            detail="Enhanced markdown export service is not available"
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
            request.filename = f"enhanced_export_{timestamp}"
        
        # Export based on format
        if request.output_format == "pdf":
            result = await enhanced_export_service.export_markdown_to_pdf_enhanced(
                markdown_content=request.markdown_content,
                output_filename=f"{request.filename}.pdf"
            )
        else:  # word
            result = await enhanced_export_service.export_markdown_to_word_enhanced(
                markdown_content=request.markdown_content,
                output_filename=f"{request.filename}.docx"
            )
        
        end_time = datetime.now()
        export_time = (end_time - start_time).total_seconds()
        
        if result.get("success"):
            return EnhancedMarkdownExportResponse(
                success=True,
                message=result.get("message", "Enhanced export completed successfully"),
                file_path=result.get("output_path"),
                file_size=result.get("file_size"),
                export_time=export_time,
                operation_id=result.get("operation_id")
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Export failed: {result.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        logger.error(f"Error in enhanced markdown export: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Export failed: {str(e)}"
        )

@router.post("/export-file")
async def export_enhanced_markdown_file(
    file: UploadFile = File(...),
    output_format: str = Form("pdf"),
    filename: Optional[str] = Form(None),
    include_images: bool = Form(True),
    figure_numbering: bool = Form(True)
):
    """Export markdown file to PDF or Word document with enhanced formatting."""
    if not ENHANCED_MARKDOWN_EXPORT_AVAILABLE or enhanced_export_service is None:
        raise HTTPException(
            status_code=503,
            detail="Enhanced markdown export service is not available"
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
        
        # Generate filename if not provided
        if not filename:
            base_name = Path(file.filename).stem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{base_name}_enhanced_{timestamp}"
        
        # Export based on format
        if output_format == "pdf":
            result = await enhanced_export_service.export_markdown_to_pdf_enhanced(
                markdown_content=markdown_content,
                output_filename=f"{filename}.pdf"
            )
        else:  # word
            result = await enhanced_export_service.export_markdown_to_word_enhanced(
                markdown_content=markdown_content,
                output_filename=f"{filename}.docx"
            )
        
        if result.get("success"):
            # Return the generated file
            file_path = result.get("output_path")
            if file_path and Path(file_path).exists():
                return FileResponse(
                    path=file_path,
                    filename=Path(file_path).name,
                    media_type="application/octet-stream"
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Generated file not found"
                )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Export failed: {result.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        logger.error(f"Error in enhanced markdown file export: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Export failed: {str(e)}"
        )

@router.get("/supported-features")
async def get_supported_features():
    """Get list of supported features for enhanced markdown export."""
    return {
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
        ],
        "supported_formats": ["pdf", "word"],
        "version": "2.3.0"
    }

@router.post("/batch-export")
async def batch_export_enhanced_markdown(
    files: List[UploadFile] = File(...),
    output_format: str = Form("pdf"),
    include_images: bool = Form(True),
    figure_numbering: bool = Form(True)
):
    """Batch export multiple markdown files with enhanced formatting."""
    if not ENHANCED_MARKDOWN_EXPORT_AVAILABLE or enhanced_export_service is None:
        raise HTTPException(
            status_code=503,
            detail="Enhanced markdown export service is not available"
        )
    
    if output_format not in ["pdf", "word"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported output format. Supported formats: pdf, word"
        )
    
    results = []
    
    for file in files:
        if not file.filename.endswith('.md'):
            results.append({
                "filename": file.filename,
                "success": False,
                "error": "File must be a markdown file (.md)"
            })
            continue
        
        try:
            # Read markdown content
            content = await file.read()
            markdown_content = content.decode('utf-8')
            
            # Generate filename
            base_name = Path(file.filename).stem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{base_name}_enhanced_{timestamp}"
            
            # Export based on format
            if output_format == "pdf":
                result = await enhanced_export_service.export_markdown_to_pdf_enhanced(
                    markdown_content=markdown_content,
                    output_filename=f"{filename}.pdf"
                )
            else:  # word
                result = await enhanced_export_service.export_markdown_to_word_enhanced(
                    markdown_content=markdown_content,
                    output_filename=f"{filename}.docx"
                )
            
            results.append({
                "filename": file.filename,
                "success": result.get("success", False),
                "file_path": result.get("output_path") if result.get("success") else None,
                "file_size": result.get("file_size") if result.get("success") else None,
                "error": result.get("error") if not result.get("success") else None
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return {
        "batch_results": results,
        "total_files": len(files),
        "successful_exports": len([r for r in results if r["success"]]),
        "failed_exports": len([r for r in results if not r["success"]])
    }
