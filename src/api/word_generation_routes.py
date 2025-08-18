"""
Word Document Generation API Routes

This module provides API endpoints for Word document generation functionality
with mermaid diagram support and professional styling.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from loguru import logger

from src.core.enhanced_word_generation_service import enhanced_word_service

router = APIRouter(prefix="/word", tags=["Word Document Generation"])


class WordGenerationRequest(BaseModel):
    """Request model for Word document generation."""
    markdown_file: str
    output_name: Optional[str] = None
    title: Optional[str] = None
    include_diagrams: bool = True


class WhitePaperWordRequest(BaseModel):
    """Request model for white paper Word document generation."""
    include_diagrams: bool = True
    generate_all: bool = True


class WordGenerationResponse(BaseModel):
    """Response model for Word document generation."""
    success: bool
    word_file: Optional[str] = None
    title: Optional[str] = None
    diagrams_count: Optional[int] = None
    message: Optional[str] = None
    error: Optional[str] = None


class WhitePaperWordResponse(BaseModel):
    """Response model for white paper Word document generation."""
    success: bool
    total_files: int
    successful_files: int
    results: List[Dict[str, Any]]
    output_directory: str
    error: Optional[str] = None


@router.post("/generate", response_model=WordGenerationResponse)
async def generate_word_from_markdown(request: WordGenerationRequest):
    """Generate Word document from markdown file."""
    try:
        logger.info(f"📄 Generating Word document from markdown: {request.markdown_file}")
        
        result = await enhanced_word_service.generate_word_from_markdown(
            markdown_file=request.markdown_file,
            output_name=request.output_name,
            title=request.title
        )
        
        if result["success"]:
            return WordGenerationResponse(
                success=True,
                word_file=result["word_file"],
                title=result["title"],
                diagrams_count=result.get("diagrams_count", 0),
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
        logger.error(f"Error generating Word document: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Word document generation failed: {str(e)}"
        )


@router.post("/white-papers", response_model=WhitePaperWordResponse)
async def generate_white_paper_word_documents(request: WhitePaperWordRequest):
    """Generate Word documents for all white papers."""
    try:
        logger.info("📄 Generating white paper Word documents")
        
        result = await enhanced_word_service.generate_white_paper_word_documents()
        
        if result["success"]:
            return WhitePaperWordResponse(
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
        logger.error(f"Error generating white paper Word documents: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"White paper Word document generation failed: {str(e)}"
        )


@router.post("/upload-and-generate", response_model=WordGenerationResponse)
async def upload_markdown_and_generate_word(
    file: UploadFile = File(...),
    output_name: Optional[str] = None,
    title: Optional[str] = None,
    include_diagrams: bool = True
):
    """Upload markdown file and generate Word document."""
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
            # Generate Word document
            result = await enhanced_word_service.generate_word_from_markdown(
                markdown_file=temp_file_path,
                output_name=output_name or file.filename.replace('.md', ''),
                title=title
            )
            
            if result["success"]:
                return WordGenerationResponse(
                    success=True,
                    word_file=result["word_file"],
                    title=result["title"],
                    diagrams_count=result.get("diagrams_count", 0),
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
        logger.error(f"Error uploading and generating Word document: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Upload and Word document generation failed: {str(e)}"
        )


@router.get("/status")
async def get_word_generation_status():
    """Get Word document generation service status."""
    try:
        return {
            "success": True,
            "service_status": "active",
            "output_directory": str(enhanced_word_service.output_dir),
            "capabilities": [
                "markdown_to_word",
                "mermaid_diagram_support",
                "professional_styling",
                "embedded_images"
            ]
        }
    except Exception as e:
        logger.error(f"Error getting Word generation status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get status: {str(e)}"
        )
