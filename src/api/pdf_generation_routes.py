"""
PDF Generation API Routes

This module provides API endpoints for PDF generation functionality
with mermaid diagram support and professional styling.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from loguru import logger

from src.core.enhanced_pdf_generation_service import enhanced_pdf_service

router = APIRouter(prefix="/pdf", tags=["PDF Generation"])


class PDFGenerationRequest(BaseModel):
    """Request model for PDF generation."""
    markdown_file: str
    output_name: Optional[str] = None
    title: Optional[str] = None
    include_diagrams: bool = True


class WhitePaperPDFRequest(BaseModel):
    """Request model for white paper PDF generation."""
    include_diagrams: bool = True
    generate_all: bool = True


class PDFGenerationResponse(BaseModel):
    """Response model for PDF generation."""
    success: bool
    html_file: Optional[str] = None
    title: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None


class WhitePaperPDFResponse(BaseModel):
    """Response model for white paper PDF generation."""
    success: bool
    total_files: int
    successful_files: int
    results: List[Dict[str, Any]]
    output_directory: str
    error: Optional[str] = None


@router.post("/generate", response_model=PDFGenerationResponse)
async def generate_pdf_from_markdown(request: PDFGenerationRequest):
    """Generate PDF-ready HTML from markdown file."""
    try:
        logger.info(f"📄 Generating PDF from markdown: {request.markdown_file}")
        
        result = await enhanced_pdf_service.generate_pdf_from_markdown(
            markdown_file=request.markdown_file,
            output_name=request.output_name,
            title=request.title
        )
        
        if result["success"]:
            return PDFGenerationResponse(
                success=True,
                html_file=result["html_file"],
                title=result["title"],
                message=result["message"]
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed: {str(e)}"
        )


@router.post("/white-papers", response_model=WhitePaperPDFResponse)
async def generate_white_paper_pdfs(request: WhitePaperPDFRequest):
    """Generate PDFs for all white papers."""
    try:
        logger.info("📄 Generating white paper PDFs")
        
        result = await enhanced_pdf_service.generate_white_paper_pdfs()
        
        if result["success"]:
            return WhitePaperPDFResponse(
                success=True,
                total_files=result["total_files"],
                successful_files=result["successful_files"],
                results=result["results"],
                output_directory=result["output_directory"]
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating white paper PDFs: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"White paper PDF generation failed: {str(e)}"
        )


@router.post("/upload-and-generate", response_model=PDFGenerationResponse)
async def upload_markdown_and_generate_pdf(
    file: UploadFile = File(...),
    output_name: Optional[str] = None,
    title: Optional[str] = None,
    include_diagrams: bool = True
):
    """Upload markdown file and generate PDF."""
    try:
        logger.info(f"📄 Uploading markdown file: {file.filename}")
        
        # Validate file type
        if not file.filename.endswith('.md'):
            raise HTTPException(
                status_code=400,
                detail="File must be a markdown (.md) file"
            )
        
        # Save uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        try:
            # Generate PDF
            result = await enhanced_pdf_service.generate_pdf_from_markdown(
                markdown_file=temp_file_path,
                output_name=output_name or file.filename.replace('.md', ''),
                title=title
            )
            
            if result["success"]:
                return PDFGenerationResponse(
                    success=True,
                    html_file=result["html_file"],
                    title=result["title"],
                    message=result["message"]
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=result["error"]
                )
                
        finally:
            # Clean up temporary file
            import os
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading and generating PDF: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Upload and PDF generation failed: {str(e)}"
        )


@router.get("/status")
async def get_pdf_generation_status():
    """Get PDF generation service status."""
    try:
        return {
            "success": True,
            "service_status": "active",
            "output_directory": str(enhanced_pdf_service.output_dir),
            "capabilities": [
                "markdown_to_html",
                "mermaid_diagram_support",
                "professional_styling",
                "print_optimized"
            ]
        }
    except Exception as e:
        logger.error(f"Error getting PDF generation status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get status: {str(e)}"
        )
