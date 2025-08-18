"""
Markdown Export Service

Main service that orchestrates the entire markdown to PDF/Word export process.
"""

import asyncio
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
import logging

from .markdown_parser import MarkdownParser
from .mermaid_converter import MermaidConverter
from .pdf_exporter import PDFExporter
from .word_exporter import WordExporter
from .template_manager import TemplateManager
from .progress_tracker import ProgressTracker, ProgressManager, ExportStage

logger = logging.getLogger(__name__)


class MarkdownExportService:
    """Main service for exporting markdown content to PDF and Word documents."""
    
    def __init__(self, output_dir: str = "exports"):
        """Initialize the markdown export service.
        
        Args:
            output_dir: Base output directory for exported files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.parser = MarkdownParser()
        self.mermaid_converter = MermaidConverter()
        self.pdf_exporter = PDFExporter()
        self.word_exporter = WordExporter()
        self.template_manager = TemplateManager()
        self.progress_manager = ProgressManager()
        
        # Active export operations
        self.active_exports: Dict[str, Dict[str, Any]] = {}
    
    async def export_markdown_to_pdf(self,
                                   markdown_content: str,
                                   output_filename: Optional[str] = None,
                                   template_name: str = "whitepaper",
                                   custom_template: Optional[Dict[str, Any]] = None,
                                   progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Export markdown content to PDF.
        
        Args:
            markdown_content: Markdown content to export
            output_filename: Optional custom output filename
            template_name: Template to use for styling
            custom_template: Optional custom template configuration
            progress_callback: Optional progress callback function
            
        Returns:
            Export result dictionary
        """
        operation_id = str(uuid.uuid4())
        tracker = self.progress_manager.create_tracker(operation_id)
        
        if progress_callback:
            tracker.add_callback(progress_callback)
        
        try:
            # Initialize progress
            tracker.update_progress(ExportStage.INITIALIZING, 5, "Initializing PDF export...")
            
            # Generate output filename
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"export_{timestamp}.pdf"
            
            output_path = self.output_dir / output_filename
            
            # Get template configuration
            template_config = self._get_template_config(template_name, custom_template)
            if not template_config:
                tracker.add_error("Invalid template configuration")
                return {"success": False, "error": "Invalid template configuration"}
            
            tracker.update_progress(ExportStage.PARSING_MARKDOWN, 15, "Parsing markdown content...")
            
            # Parse markdown content
            markdown_elements = self.parser.parse(markdown_content)
            
            tracker.update_progress(ExportStage.CONVERTING_DIAGRAMS, 35, "Converting Mermaid diagrams...")
            
            # Convert Mermaid diagrams to PNG
            mermaid_diagrams = self.parser.extract_mermaid_blocks(markdown_content)
            converted_diagrams = {}
            
            for i, diagram in enumerate(mermaid_diagrams):
                diagram_name = f"diagram_{i+1}"
                png_path = self.mermaid_converter.convert_to_png(
                    diagram['content'], 
                    diagram_name,
                    width=800,
                    height=600
                )
                if png_path:
                    converted_diagrams[diagram_name] = png_path
                
                # Update progress for each diagram
                progress = 15 + (i / len(mermaid_diagrams)) * 20
                tracker.update_progress(progress, 35, f"Converting diagram {i+1}/{len(mermaid_diagrams)}")
            
            tracker.update_progress(ExportStage.PROCESSING_IMAGES, 50, "Processing images...")
            
            # Process images
            images = self._process_images(markdown_content, converted_diagrams)
            
            # Filter out image elements that don't have corresponding files
            filtered_elements = self._filter_image_elements(markdown_elements, images)
            
            tracker.update_progress(ExportStage.GENERATING_PDF, 90, "Generating PDF document...")
            
            # Generate PDF
            success = self.pdf_exporter.export_to_pdf(
                filtered_elements,
                str(output_path),
                template_config,
                images,
                lambda progress, message: tracker.update_progress(50 + progress * 0.4, 90, message)
            )
            
            if success:
                tracker.complete(True)
                
                # Clean up temporary files
                self.mermaid_converter.cleanup_temp_files()
                
                return {
                    "success": True,
                    "operation_id": operation_id,
                    "output_path": str(output_path),
                    "file_size": output_path.stat().st_size,
                    "message": "PDF export completed successfully"
                }
            else:
                tracker.complete(False)
                return {
                    "success": False,
                    "operation_id": operation_id,
                    "error": "PDF generation failed"
                }
        
        except Exception as e:
            logger.error(f"Error in PDF export: {e}")
            tracker.add_error(str(e))
            tracker.complete(False)
            return {
                "success": False,
                "operation_id": operation_id,
                "error": str(e)
            }
        finally:
            # Clean up tracker after some time
            asyncio.create_task(self._cleanup_tracker(operation_id, delay=300))
    
    async def export_markdown_to_word(self,
                                    markdown_content: str,
                                    output_filename: Optional[str] = None,
                                    template_name: str = "whitepaper",
                                    custom_template: Optional[Dict[str, Any]] = None,
                                    progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Export markdown content to Word document.
        
        Args:
            markdown_content: Markdown content to export
            output_filename: Optional custom output filename
            template_name: Template to use for styling
            custom_template: Optional custom template configuration
            progress_callback: Optional progress callback function
            
        Returns:
            Export result dictionary
        """
        operation_id = str(uuid.uuid4())
        tracker = self.progress_manager.create_tracker(operation_id)
        
        if progress_callback:
            tracker.add_callback(progress_callback)
        
        try:
            # Initialize progress
            tracker.update_progress(ExportStage.INITIALIZING, 5, "Initializing Word export...")
            
            # Generate output filename
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"export_{timestamp}.docx"
            
            output_path = self.output_dir / output_filename
            
            # Get template configuration
            template_config = self._get_template_config(template_name, custom_template)
            if not template_config:
                tracker.add_error("Invalid template configuration")
                return {"success": False, "error": "Invalid template configuration"}
            
            tracker.update_progress(ExportStage.PARSING_MARKDOWN, 15, "Parsing markdown content...")
            
            # Parse markdown content
            markdown_elements = self.parser.parse(markdown_content)
            
            tracker.update_progress(ExportStage.CONVERTING_DIAGRAMS, 35, "Converting Mermaid diagrams...")
            
            # Convert Mermaid diagrams to PNG
            mermaid_diagrams = self.parser.extract_mermaid_blocks(markdown_content)
            converted_diagrams = {}
            
            for i, diagram in enumerate(mermaid_diagrams):
                diagram_name = f"diagram_{i+1}"
                png_path = self.mermaid_converter.convert_to_png(
                    diagram['content'], 
                    diagram_name,
                    width=800,
                    height=600
                )
                if png_path:
                    converted_diagrams[diagram_name] = png_path
                
                # Update progress for each diagram
                progress = 15 + (i / len(mermaid_diagrams)) * 20
                tracker.update_progress(progress, 35, f"Converting diagram {i+1}/{len(mermaid_diagrams)}")
            
            tracker.update_progress(ExportStage.PROCESSING_IMAGES, 50, "Processing images...")
            
            # Process images
            images = self._process_images(markdown_content, converted_diagrams)
            
            # Filter out image elements that don't have corresponding files
            filtered_elements = self._filter_image_elements(markdown_elements, images)
            
            tracker.update_progress(ExportStage.GENERATING_WORD, 90, "Generating Word document...")
            
            # Generate Word document
            success = self.word_exporter.export_to_word(
                filtered_elements,
                str(output_path),
                template_config,
                images,
                lambda progress, message: tracker.update_progress(50 + progress * 0.4, 90, message)
            )
            
            if success:
                tracker.complete(True)
                
                # Clean up temporary files
                self.mermaid_converter.cleanup_temp_files()
                
                return {
                    "success": True,
                    "operation_id": operation_id,
                    "output_path": str(output_path),
                    "file_size": output_path.stat().st_size,
                    "message": "Word export completed successfully"
                }
            else:
                tracker.complete(False)
                return {
                    "success": False,
                    "operation_id": operation_id,
                    "error": "Word generation failed"
                }
        
        except Exception as e:
            logger.error(f"Error in Word export: {e}")
            tracker.add_error(str(e))
            tracker.complete(False)
            return {
                "success": False,
                "operation_id": operation_id,
                "error": str(e)
            }
        finally:
            # Clean up tracker after some time
            asyncio.create_task(self._cleanup_tracker(operation_id, delay=300))
    
    async def export_markdown_to_both(self,
                                    markdown_content: str,
                                    output_filename: Optional[str] = None,
                                    template_name: str = "whitepaper",
                                    custom_template: Optional[Dict[str, Any]] = None,
                                    progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Export markdown content to both PDF and Word documents.
        
        Args:
            markdown_content: Markdown content to export
            output_filename: Optional custom output filename (without extension)
            template_name: Template to use for styling
            custom_template: Optional custom template configuration
            progress_callback: Optional progress callback function
            
        Returns:
            Export result dictionary
        """
        operation_id = str(uuid.uuid4())
        tracker = self.progress_manager.create_tracker(operation_id)
        
        if progress_callback:
            tracker.add_callback(progress_callback)
        
        try:
            # Initialize progress
            tracker.update_progress(ExportStage.INITIALIZING, 5, "Initializing dual export...")
            
            # Generate output filenames
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"export_{timestamp}"
            
            pdf_filename = f"{output_filename}.pdf"
            word_filename = f"{output_filename}.docx"
            
            # Get template configuration
            template_config = self._get_template_config(template_name, custom_template)
            if not template_config:
                tracker.add_error("Invalid template configuration")
                return {"success": False, "error": "Invalid template configuration"}
            
            tracker.update_progress(ExportStage.PARSING_MARKDOWN, 15, "Parsing markdown content...")
            
            # Parse markdown content (shared between both exports)
            markdown_elements = self.parser.parse(markdown_content)
            
            tracker.update_progress(ExportStage.CONVERTING_DIAGRAMS, 35, "Converting Mermaid diagrams...")
            
            # Convert Mermaid diagrams to PNG (shared between both exports)
            mermaid_diagrams = self.parser.extract_mermaid_blocks(markdown_content)
            converted_diagrams = {}
            
            for i, diagram in enumerate(mermaid_diagrams):
                diagram_name = f"diagram_{i+1}"
                png_path = self.mermaid_converter.convert_to_png(
                    diagram['content'], 
                    diagram_name,
                    width=800,
                    height=600
                )
                if png_path:
                    converted_diagrams[diagram_name] = png_path
                
                # Update progress for each diagram
                progress = 15 + (i / len(mermaid_diagrams)) * 20
                tracker.update_progress(progress, 35, f"Converting diagram {i+1}/{len(mermaid_diagrams)}")
            
            tracker.update_progress(ExportStage.PROCESSING_IMAGES, 50, "Processing images...")
            
            # Process images (shared between both exports)
            images = self._process_images(markdown_content, converted_diagrams)
            
            # Export to PDF
            tracker.update_progress(50, 70, "Generating PDF document...")
            pdf_result = await self.export_markdown_to_pdf(
                markdown_content,
                pdf_filename,
                template_name,
                custom_template
            )
            
            # Export to Word
            tracker.update_progress(70, 90, "Generating Word document...")
            word_result = await self.export_markdown_to_word(
                markdown_content,
                word_filename,
                template_name,
                custom_template
            )
            
            # Check results
            if pdf_result["success"] and word_result["success"]:
                tracker.complete(True)
                
                return {
                    "success": True,
                    "operation_id": operation_id,
                    "pdf_result": pdf_result,
                    "word_result": word_result,
                    "message": "Dual export completed successfully"
                }
            else:
                tracker.complete(False)
                errors = []
                if not pdf_result["success"]:
                    errors.append(f"PDF: {pdf_result.get('error', 'Unknown error')}")
                if not word_result["success"]:
                    errors.append(f"Word: {word_result.get('error', 'Unknown error')}")
                
                return {
                    "success": False,
                    "operation_id": operation_id,
                    "error": "; ".join(errors)
                }
        
        except Exception as e:
            logger.error(f"Error in dual export: {e}")
            tracker.add_error(str(e))
            tracker.complete(False)
            return {
                "success": False,
                "operation_id": operation_id,
                "error": str(e)
            }
        finally:
            # Clean up tracker after some time
            asyncio.create_task(self._cleanup_tracker(operation_id, delay=300))
    
    def get_export_status(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of an export operation.
        
        Args:
            operation_id: Operation identifier
            
        Returns:
            Status dictionary or None if not found
        """
        tracker = self.progress_manager.get_tracker(operation_id)
        if tracker:
            return tracker.get_status()
        return None
    
    def cancel_export(self, operation_id: str) -> bool:
        """Cancel an export operation.
        
        Args:
            operation_id: Operation identifier
            
        Returns:
            True if cancelled, False if not found
        """
        tracker = self.progress_manager.get_tracker(operation_id)
        if tracker:
            tracker.cancel()
            return True
        return False
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List available templates.
        
        Returns:
            List of template information
        """
        return self.template_manager.list_templates()
    
    def create_custom_template(self, 
                             template_name: str,
                             template_config: Dict[str, Any]) -> bool:
        """Create a custom template.
        
        Args:
            template_name: Name for the template
            template_config: Template configuration
            
        Returns:
            True if successful, False otherwise
        """
        from .template_manager import TemplateConfig
        config = TemplateConfig(**template_config)
        return self.template_manager.create_custom_template(template_name, config)
    
    def _get_template_config(self, 
                           template_name: str, 
                           custom_template: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Get template configuration.
        
        Args:
            template_name: Template name
            custom_template: Optional custom template
            
        Returns:
            Template configuration or None
        """
        if custom_template:
            return custom_template
        
        template = self.template_manager.get_template(template_name)
        if template:
            return {
                "pdf_styles": template.pdf_styles,
                "word_styles": template.word_styles,
                "metadata": template.metadata
            }
        
        return None
    
    def _process_images(self, 
                       markdown_content: str, 
                       converted_diagrams: Dict[str, str]) -> Dict[str, str]:
        """Process images in markdown content.
        
        Args:
            markdown_content: Markdown content
            converted_diagrams: Dictionary of converted Mermaid diagrams
            
        Returns:
            Dictionary mapping image references to file paths
        """
        images = {}
        
        # Add converted diagrams
        images.update(converted_diagrams)
        
        # Extract other images
        extracted_images = self.parser.extract_images(markdown_content)
        for img in extracted_images:
            image_url = img['url']
            original_url = img['url']  # Keep original for mapping
            
            # Handle relative paths (common in markdown files)
            if image_url.startswith('./'):
                # Remove ./ prefix
                image_url = image_url[2:]
            
                        # Try to find the image file
            image_path = None
            
            # Check if it's a relative path from the markdown file location
            if not image_url.startswith(('http://', 'https://', '/')):
                # Check multiple possible locations relative to the output directory
                possible_paths = [
                    Path(self.output_dir) / image_url,  # Direct path in output dir
                    Path(self.output_dir) / "images" / image_url,  # In images subdirectory
                    Path(self.output_dir).parent / "images" / image_url,  # Parent images dir
                    Path(self.output_dir).parent / "white_papers" / "images" / image_url,  # Whitepaper images
                    Path("docs/white_papers/images") / image_url,  # Absolute path to whitepaper images
                    Path.cwd() / "docs/white_papers/images" / image_url,  # Current working directory
                    Path.cwd().parent / "docs/white_papers/images" / image_url,  # Parent of current dir
                ]
                
                for path in possible_paths:
                    if path.exists():
                        image_path = str(path.resolve())
                        logger.info(f"Found image: {original_url} -> {image_path}")
                        break
            
            # If we found a local image, use it; otherwise skip it
            if image_path:
                images[original_url] = image_path
            else:
                logger.warning(f"Could not find image file for: {original_url}")
                # Don't add to images dict - this will cause the image to be skipped
        
        return images
    
    def _filter_image_elements(self, markdown_elements: List[Any], images: Dict[str, str]) -> List[Any]:
        """Filter out image elements that don't have corresponding files.
        
        Args:
            markdown_elements: List of markdown elements
            images: Dictionary mapping image references to file paths
            
        Returns:
            Filtered list of markdown elements
        """
        filtered_elements = []
        
        for element in markdown_elements:
            try:
                element_type = element.element_type.value
                
                if element_type == 'image':
                    # Check if this image has a corresponding file
                    image_url = element.content
                    if image_url in images:
                        # Image file exists, keep the element
                        filtered_elements.append(element)
                    else:
                        # Image file doesn't exist, skip this element
                        logger.info(f"Skipping image element for missing file: {image_url}")
                else:
                    # Not an image element, keep it
                    filtered_elements.append(element)
                    
            except Exception as e:
                # If there's an error processing the element, keep it to be safe
                logger.warning(f"Error filtering element: {e}")
                filtered_elements.append(element)
        
        return filtered_elements
    
    async def _cleanup_tracker(self, operation_id: str, delay: int = 300):
        """Clean up tracker after delay.
        
        Args:
            operation_id: Operation identifier
            delay: Delay in seconds before cleanup
        """
        await asyncio.sleep(delay)
        self.progress_manager.remove_tracker(operation_id)
