"""
PDF Exporter

Generates PDF documents from markdown content using ReportLab with comprehensive styling support.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, Preformatted, Indenter, HRFlowable
)
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
import logging

logger = logging.getLogger(__name__)


class PDFExporter:
    """Generates PDF documents from markdown content using ReportLab."""
    
    def __init__(self):
        """Initialize PDF exporter."""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _create_page_template(self, page_size, margins):
        """Create a page template with footer.
        
        Args:
            page_size: ReportLab page size
            margins: Margin dictionary
            
        Returns:
            PageTemplate with footer
        """
        def footer(canvas, doc):
            canvas.saveState()
            # Get footer text
            footer_text = "Copyright (c) 2025 Boeing Intelligence & Analytics All right reserved."
            
            # Calculate footer position
            footer_y = margins['bottom'] * inch - 0.3 * inch  # 0.3 inches from bottom margin
            
            # Draw footer text
            canvas.setFont("Helvetica", 9)
            canvas.setFillColor(HexColor('#666666'))
            
            # Center the footer text
            text_width = canvas.stringWidth(footer_text, "Helvetica", 9)
            page_width = page_size[0]
            footer_x = (page_width - text_width) / 2
            
            canvas.drawString(footer_x, footer_y, footer_text)
            canvas.restoreState()
        
        # Create frame for content (excluding footer area)
        frame = Frame(
            margins['left'] * inch,
            margins['bottom'] * inch + 0.5 * inch,  # Extra space for footer
            page_size[0] - (margins['left'] + margins['right']) * inch,
            page_size[1] - (margins['top'] + margins['bottom']) * inch - 0.5 * inch,
            leftPadding=0,
            bottomPadding=0,
            rightPadding=0,
            topPadding=0
        )
        
        return PageTemplate(id='normal', frames=frame, onPage=footer)
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Custom title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=HexColor('#2c3e50')
        ))
        
        # Custom heading styles
        for i in range(1, 7):
            self.styles.add(ParagraphStyle(
                name=f'CustomHeading{i}',
                parent=self.styles[f'Heading{i}'],
                fontSize=20 - (i * 2),
                spaceAfter=15 - (i * 2),
                textColor=HexColor('#34495e')
            ))
        
        # Custom body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            textColor=HexColor('#2c3e50')
        ))
        
        # Custom code style
        self.styles.add(ParagraphStyle(
            name='CustomCode',
            parent=self.styles['Code'],
            fontSize=10,
            fontName='Courier',
            leftIndent=20,
            rightIndent=20,
            backColor=HexColor('#f8f9fa'),
            borderColor=HexColor('#dee2e6'),
            borderWidth=1,
            borderPadding=10
        ))
        
        # Custom blockquote style
        self.styles.add(ParagraphStyle(
            name='CustomBlockquote',
            parent=self.styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Oblique',
            leftIndent=20,
            rightIndent=20,
            textColor=HexColor('#555'),
            borderColor=HexColor('#3498db'),
            borderWidth=4,
            borderPadding=10
        ))
        
        # Custom footer style
        self.styles.add(ParagraphStyle(
            name='CustomFooter',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=HexColor('#666'),
            spaceBefore=20
        ))
    
    def export_to_pdf(self, 
                     markdown_elements: List[Any],
                     output_path: str,
                     template_config: Dict[str, Any],
                     images: Dict[str, str] = None,
                     progress_callback=None) -> bool:
        """Export markdown elements to PDF.
        
        Args:
            markdown_elements: List of parsed markdown elements
            output_path: Output PDF file path
            template_config: Template configuration
            images: Dictionary mapping image references to file paths
            progress_callback: Optional progress callback function
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create output directory if it doesn't exist
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Setup document with page template
            page_size = self._get_page_size(template_config.get('page_size', 'A4'))
            margins = template_config.get('margins', {'top': 1, 'bottom': 1, 'left': 1, 'right': 1})
            
            # Create document with page template
            doc = BaseDocTemplate(
                output_path,
                pagesize=page_size,
                topMargin=margins['top'] * inch,
                bottomMargin=margins['bottom'] * inch,
                leftMargin=margins['left'] * inch,
                rightMargin=margins['right'] * inch
            )
            
            # Add page template with footer
            page_template = self._create_page_template(page_size, margins)
            doc.addPageTemplates([page_template])
            
            # Build story (content)
            story = []
            total_elements = len(markdown_elements)
            
            for i, element in enumerate(markdown_elements):
                if progress_callback:
                    progress = (i / total_elements) * 100
                    progress_callback(progress, f"Processing element {i+1}/{total_elements}")
                
                # Convert element to PDF content
                pdf_content = self._element_to_pdf(element, template_config, images)
                if pdf_content:
                    story.extend(pdf_content)
            
            # Build PDF
            if progress_callback:
                progress_callback(90, "Building PDF document...")
            
            doc.build(story)
            
            if progress_callback:
                progress_callback(100, "PDF generation completed")
            
            logger.info(f"Successfully generated PDF: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            return False
    
    def _get_page_size(self, page_size_name: str):
        """Get ReportLab page size.
        
        Args:
            page_size_name: Page size name
            
        Returns:
            ReportLab page size
        """
        page_sizes = {
            'A4': A4,
            'letter': letter
        }
        return page_sizes.get(page_size_name, A4)
    
    def _element_to_pdf(self, 
                       element: Any, 
                       template_config: Dict[str, Any],
                       images: Dict[str, str] = None) -> List[Any]:
        """Convert a markdown element to PDF content.
        
        Args:
            element: Markdown element
            template_config: Template configuration
            images: Dictionary mapping image references to file paths
            
        Returns:
            List of PDF content elements
        """
        content = []
        
        try:
            element_type = element.element_type.value
            
            if element_type == 'header':
                content.extend(self._header_to_pdf(element, template_config))
            elif element_type == 'paragraph':
                content.extend(self._paragraph_to_pdf(element, template_config))
            elif element_type == 'list':
                content.extend(self._list_to_pdf(element, template_config))
            elif element_type == 'table':
                content.extend(self._table_to_pdf(element, template_config))
            elif element_type == 'code_block':
                content.extend(self._code_block_to_pdf(element, template_config))
            elif element_type == 'mermaid':
                content.extend(self._mermaid_to_pdf(element, template_config, images))
            elif element_type == 'image':
                content.extend(self._image_to_pdf(element, template_config, images))
            elif element_type == 'blockquote':
                content.extend(self._blockquote_to_pdf(element, template_config))
            elif element_type == 'horizontal_rule':
                content.append(HRFlowable(width="100%", thickness=1, color=HexColor('#bdc3c7')))
            elif element_type == 'text':
                content.extend(self._text_to_pdf(element, template_config))
            elif element_type == 'link':
                content.extend(self._link_to_pdf(element, template_config))
            else:
                logger.warning(f"Unsupported element type: {element_type}")
        
        except Exception as e:
            logger.error(f"Error converting element to PDF: {e}")
        
        return content
    
    def _header_to_pdf(self, element: Any, template_config: Dict[str, Any]) -> List[Any]:
        """Convert header element to PDF.
        
        Args:
            element: Header element
            template_config: Template configuration
            
        Returns:
            List of PDF content elements
        """
        content = []
        
        level = element.level or 1
        text = element.content
        
        # Get style based on level
        if level == 1:
            style = self.styles['CustomTitle']
        else:
            style = self.styles[f'CustomHeading{min(level, 6)}']
        
        # Apply template styling
        if 'heading1' in template_config.get('pdf_styles', {}):
            heading_styles = template_config['pdf_styles']['heading1']
            if 'font_size' in heading_styles:
                style.fontSize = heading_styles['font_size']
            if 'color' in heading_styles:
                style.textColor = HexColor(heading_styles['color'])
        
        content.append(Paragraph(text, style))
        content.append(Spacer(1, 12))
        
        return content
    
    def _paragraph_to_pdf(self, element: Any, template_config: Dict[str, Any]) -> List[Any]:
        """Convert paragraph element to PDF.
        
        Args:
            element: Paragraph element
            template_config: Template configuration
            
        Returns:
            List of PDF content elements
        """
        content = []
        
        text = element.content
        
        # Process inline elements (images, links)
        processed_text = self._process_inline_elements(text, template_config)
        
        # Create paragraph with inline formatting
        paragraph = self._create_formatted_paragraph(processed_text, template_config)
        content.append(paragraph)
        content.append(Spacer(1, 6))
        
        return content
    
    def _create_formatted_paragraph(self, text: str, template_config: Dict[str, Any]) -> Paragraph:
        """Create a paragraph with inline formatting.
        
        Args:
            text: Text with HTML tags
            template_config: Template configuration
            
        Returns:
            Formatted paragraph
        """
        import re
        
        # Split text by HTML tags and process each part
        parts = re.split(r'(<[^>]+>.*?</[^>]+>)', text)
        
        # Create paragraph with mixed formatting
        paragraph_parts = []
        
        for part in parts:
            if part.startswith('<b>') and part.endswith('</b>'):
                # Bold text - just use the text content, ReportLab will handle <b> tags
                bold_text = part[3:-4]  # Remove <b> and </b>
                paragraph_parts.append(f'<b>{bold_text}</b>')
            elif part.startswith('<i>') and part.endswith('</i>'):
                # Italic text
                italic_text = part[3:-4]  # Remove <i> and </i>
                paragraph_parts.append(f'<i>{italic_text}</i>')
            elif part.startswith('<code>') and part.endswith('</code>'):
                # Inline code
                code_text = part[6:-7]  # Remove <code> and </code>
                paragraph_parts.append(f'<code>{code_text}</code>')
            elif part.startswith('<strike>') and part.endswith('</strike>'):
                # Strikethrough text
                strike_text = part[8:-9]  # Remove <strike> and </strike>
                paragraph_parts.append(f'<strike>{strike_text}</strike>')
            else:
                # Regular text - process any remaining markdown syntax
                processed_part = self._process_inline_elements(part, template_config)
                paragraph_parts.append(processed_part)
        
        # Join parts and create paragraph
        formatted_text = ''.join(paragraph_parts)
        
        style = self.styles['CustomBody']
        
        # Apply template styling
        if 'body' in template_config.get('pdf_styles', {}):
            body_styles = template_config['pdf_styles']['body']
            if 'font_size' in body_styles:
                style.fontSize = body_styles['font_size']
            if 'color' in body_styles:
                style.textColor = HexColor(body_styles['color'])
        
        return Paragraph(formatted_text, style)
    
    def _list_to_pdf(self, element: Any, template_config: Dict[str, Any]) -> List[Any]:
        """Convert list element to PDF.
        
        Args:
            element: List element
            template_config: Template configuration
            
        Returns:
            List of PDF content elements
        """
        content = []
        
        list_items = element.attributes.get('list_items', [])
        
        for item in list_items:
            indent = item['indent']
            marker = item['marker']
            item_text = item['content']
            
            # Remove numbering from the content (e.g., "1. " or "1.	" from the beginning)
            import re
            # Remove numbered list markers like "1. ", "2. ", etc. from the beginning
            cleaned_text = re.sub(r'^\d+\.\s*', '', item_text.strip())
            
            # Process inline markdown formatting in list items
            processed_text = self._process_inline_elements(cleaned_text, template_config)
            
            # Create bullet for all lists (remove numbering)
            bullet = '•'
            
            # Apply indentation and create formatted paragraph
            indent_space = '&nbsp;' * (indent * 4)
            formatted_text = f"{indent_space}{bullet} {processed_text}"
            
            # Create paragraph with inline formatting
            paragraph = self._create_formatted_paragraph(formatted_text, template_config)
            content.append(paragraph)
        
        content.append(Spacer(1, 6))
        
        return content
    
    def _table_to_pdf(self, element: Any, template_config: Dict[str, Any]) -> List[Any]:
        """Convert table element to PDF.
        
        Args:
            element: Table element
            template_config: Template configuration
            
        Returns:
            List of PDF content elements
        """
        content = []
        
        table_data = element.attributes.get('table_data', {})
        headers = table_data.get('headers', [])
        data_rows = table_data.get('data', [])
        
        if not headers:
            return content
        
        # Process headers and data to remove HTML/markdown tags
        processed_headers = []
        for header in headers:
            processed_header = self._process_inline_elements(header, template_config)
            processed_headers.append(processed_header)
        
        processed_data_rows = []
        for row in data_rows:
            processed_row = []
            for cell in row:
                processed_cell = self._process_inline_elements(str(cell), template_config)
                processed_row.append(processed_cell)
            processed_data_rows.append(processed_row)
        
        # Create table data with processed content as Paragraph objects
        # Convert headers to Paragraph objects
        header_paragraphs = []
        for header in processed_headers:
            header_para = Paragraph(header, self.styles['CustomBody'])
            header_paragraphs.append(header_para)
        
        # Convert data rows to Paragraph objects
        data_paragraphs = []
        for row in processed_data_rows:
            row_paragraphs = []
            for cell in row:
                cell_para = Paragraph(cell, self.styles['CustomBody'])
                row_paragraphs.append(cell_para)
            data_paragraphs.append(row_paragraphs)
        
        # Create table data with Paragraph objects
        table_content = [header_paragraphs] + data_paragraphs
        
        # Calculate available page width (assuming A4 with 1-inch margins)
        available_width = 8.5 - 2  # 8.5 inches - 2 inches for margins = 6.5 inches
        available_width_points = available_width * 72  # Convert to points
        
        # Create table with proper column widths and text wrapping
        # Use equal column widths for better text wrapping
        num_cols = len(processed_headers)
        col_width = available_width_points / num_cols
        col_widths = [col_width] * num_cols
        
        table = Table(table_content, colWidths=col_widths, repeatRows=1)
        
        # Apply table styling with proper alignment, sizing, and text wrapping
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Header alignment
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),  # Smaller font for headers
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),  # Smaller font for data
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),  # Data alignment
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Top alignment for better text wrapping
            ('LEFTPADDING', (0, 0), (-1, -1), 4),  # Reduced padding
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),  # Reduced padding
            ('TOPPADDING', (0, 0), (-1, -1), 4),  # Reduced padding
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),  # Reduced padding
            ('WORDWRAP', (0, 0), (-1, -1), True),  # Enable word wrapping
        ])
        
        table.setStyle(table_style)
        content.append(table)
        content.append(Spacer(1, 12))
        
        return content
    
    def _code_block_to_pdf(self, element: Any, template_config: Dict[str, Any]) -> List[Any]:
        """Convert code block element to PDF.
        
        Args:
            element: Code block element
            template_config: Template configuration
            
        Returns:
            List of PDF content elements
        """
        content = []
        
        code_text = element.content
        language = element.language or 'text'
        
        # Create preformatted text
        preformatted = Preformatted(code_text, self.styles['CustomCode'])
        content.append(preformatted)
        content.append(Spacer(1, 12))
        
        return content
    
    def _mermaid_to_pdf(self, 
                       element: Any, 
                       template_config: Dict[str, Any],
                       images: Dict[str, str] = None) -> List[Any]:
        """Convert Mermaid diagram element to PDF.
        
        Args:
            element: Mermaid element
            template_config: Template configuration
            images: Dictionary mapping image references to file paths
            
        Returns:
            List of PDF content elements
        """
        content = []
        
        # Try to find the corresponding image
        if images:
            # Look for the diagram image
            diagram_name = f"diagram_{len(content)}"  # Simple naming
            image_path = images.get(diagram_name)
            
            if image_path and os.path.exists(image_path):
                try:
                    # Add image to PDF
                    img = Image(image_path, width=6*inch, height=4*inch)
                    content.append(img)
                    content.append(Spacer(1, 12))
                except Exception as e:
                    logger.warning(f"Could not add Mermaid diagram image: {e}")
                    # Fallback to code block
                    content.extend(self._code_block_to_pdf(element, template_config))
            else:
                # Fallback to code block
                content.extend(self._code_block_to_pdf(element, template_config))
        else:
            # Fallback to code block
            content.extend(self._code_block_to_pdf(element, template_config))
        
        return content
    
    def _image_to_pdf(self, 
                     element: Any, 
                     template_config: Dict[str, Any],
                     images: Dict[str, str] = None) -> List[Any]:
        """Convert image element to PDF.
        
        Args:
            element: Image element
            template_config: Template configuration
            images: Dictionary mapping image references to file paths
            
        Returns:
            List of PDF content elements
        """
        content = []
        
        image_url = element.content
        alt_text = element.attributes.get('alt_text', '')
        
        # Try to find the image file
        image_path = None
        if images and image_url in images:
            image_path = images[image_url]
        elif os.path.exists(image_url):
            image_path = image_url
        
        if image_path and os.path.exists(image_path):
            try:
                # Add image to PDF
                img = Image(image_path, width=5*inch, height=3*inch)
                content.append(img)
                
                # Add alt text as caption
                if alt_text:
                    caption_style = ParagraphStyle(
                        'Caption',
                        parent=self.styles['Normal'],
                        fontSize=9,
                        alignment=TA_CENTER,
                        textColor=HexColor('#666')
                    )
                    content.append(Paragraph(alt_text, caption_style))
                
                content.append(Spacer(1, 12))
            except Exception as e:
                logger.warning(f"Could not add image {image_path}: {e}")
                # Don't add any placeholder text - just skip the image
                pass
        else:
            # Don't add any placeholder text - just skip the image
            logger.warning(f"Image not found: {image_url}")
            pass
        
        return content
    
    def _blockquote_to_pdf(self, element: Any, template_config: Dict[str, Any]) -> List[Any]:
        """Convert blockquote element to PDF.
        
        Args:
            element: Blockquote element
            template_config: Template configuration
            
        Returns:
            List of PDF content elements
        """
        content = []
        
        text = element.content
        
        # Create blockquote using Indenter for left margin and custom styling
        content.append(Indenter(left=20))
        content.append(Paragraph(text, self.styles['CustomBlockquote']))
        content.append(Indenter(left=-20))
        content.append(Spacer(1, 12))
        
        return content
    
    def _text_to_pdf(self, element: Any, template_config: Dict[str, Any]) -> List[Any]:
        """Convert text element to PDF.
        
        Args:
            element: Text element
            template_config: Template configuration
            
        Returns:
            List of PDF content elements
        """
        content = []
        
        text = element.content
        
        # Process inline elements
        processed_text = self._process_inline_elements(text, template_config)
        
        style = self.styles['CustomBody']
        content.append(Paragraph(processed_text, style))
        
        return content
    
    def _process_inline_elements(self, text: str, template_config: Dict[str, Any]) -> str:
        """Process inline elements in text.
        
        Args:
            text: Text to process
            template_config: Template configuration
            
        Returns:
            Processed text with inline elements
        """
        import re
        
        # Process bold text (**text** or __text__)
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.*?)__', r'<b>\1</b>', text)
        
        # Process italic text (*text* or _text_)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)
        
        # Process inline code (`code`)
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
        
        # Process strikethrough (~~text~~)
        text = re.sub(r'~~(.*?)~~', r'<strike>\1</strike>', text)
        
        return text
    
    def _link_to_pdf(self, element: Any, template_config: Dict[str, Any]) -> List[Any]:
        """Convert link element to PDF.
        
        Args:
            element: Link element
            template_config: Template configuration
            
        Returns:
            List of PDF content elements
        """
        content = []
        
        link_text = element.content
        link_url = element.attributes.get('url', '')
        
        # Create link style
        link_style = ParagraphStyle(
            'Link',
            parent=self.styles['CustomBody'],
            textColor=HexColor('#3498db'),
            underline=True
        )
        
        # Create link text with URL
        if link_url:
            link_content = f"{link_text} ({link_url})"
        else:
            link_content = link_text
        
        content.append(Paragraph(link_content, link_style))
        
        return content
