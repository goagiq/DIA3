#!/usr/bin/env python3
"""
Enhanced PDF Generation Service for DIA3

This service provides PDF generation capabilities for white papers and reports
with mermaid diagram support and professional styling.
"""

import sys
import markdown
from pathlib import Path
from jinja2 import Template
import re
import base64
import requests
import hashlib
import asyncio
from typing import Dict, Any, Optional, List
from loguru import logger

# CSS template for professional styling with diagram support
CSS_TEMPLATE = """
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    background-color: white;
}

h1 {
    color: #1a365d;
    font-size: 28px;
    font-weight: bold;
    margin-top: 0;
    margin-bottom: 20px;
    border-bottom: 3px solid #3182ce;
    padding-bottom: 10px;
}

h2 {
    color: #2d3748;
    font-size: 20px;
    font-weight: bold;
    margin-top: 30px;
    margin-bottom: 15px;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 5px;
}

h3 {
    color: #4a5568;
    font-size: 16px;
    font-weight: bold;
    margin-top: 25px;
    margin-bottom: 10px;
}

h4 {
    color: #718096;
    font-size: 14px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 8px;
}

p {
    margin-bottom: 12px;
    text-align: justify;
}

ul, ol {
    margin-bottom: 15px;
    padding-left: 20px;
}

li {
    margin-bottom: 5px;
}

blockquote {
    border-left: 4px solid #3182ce;
    margin: 20px 0;
    padding: 10px 20px;
    background-color: #f7fafc;
    font-style: italic;
}

code {
    background-color: #f1f5f9;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
}

pre {
    background-color: #f1f5f9;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
    margin: 15px 0;
}

pre code {
    background-color: transparent;
    padding: 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

th, td {
    border: 1px solid #e2e8f0;
    padding: 8px 12px;
    text-align: left;
}

th {
    background-color: #3182ce;
    color: white;
    font-weight: bold;
}

tr:nth-child(even) {
    background-color: #f7fafc;
}

.diagram-container {
    text-align: center;
    margin: 30px 0;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
}

.diagram-title {
    font-weight: bold;
    color: #2d3748;
    margin-bottom: 15px;
    font-size: 16px;
}

.diagram-image {
    max-width: 100%;
    height: auto;
    border-radius: 5px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.diagram-description {
    margin-top: 15px;
    font-style: italic;
    color: #666;
    font-size: 14px;
    line-height: 1.4;
}

.case-study {
    background-color: #f0f9ff;
    border: 1px solid #bfdbfe;
    border-radius: 5px;
    padding: 15px;
    margin: 15px 0;
}

.key-takeaways {
    background-color: #fef5e7;
    border: 2px solid #ed8936;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
}

.about-section {
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 15px;
    margin: 20px 0;
    text-align: center;
}

hr {
    border: none;
    border-top: 2px solid #e2e8f0;
    margin: 30px 0;
}

@media print {
    body {
        margin: 0;
        padding: 10px;
    }
    
    h1, h2, h3 {
        page-break-after: avoid;
    }
    
    p, ul, ol {
        page-break-inside: avoid;
    }
    
    .diagram-container {
        page-break-inside: avoid;
        margin: 20px 0;
    }
    
    .diagram-image {
        max-width: 100%;
        height: auto;
    }
}
"""

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        {{ css }}
    </style>
</head>
<body>
    <div class="document">
        {{ content }}
    </div>
</body>
</html>
"""


class EnhancedPDFGenerationService:
    """Enhanced service for generating PDFs from markdown content with mermaid diagrams."""
    
    def __init__(self):
        """Initialize the PDF generation service."""
        self.base_dir = Path(__file__).parent.parent.parent
        self.output_dir = self.base_dir / "docs" / "white_papers" / "generated_pdfs"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("✅ Enhanced PDF Generation Service initialized")
    
    def generate_mermaid_image_sync(self, mermaid_code: str, diagram_type: str = "flowchart") -> Optional[bytes]:
        """Generate PNG image from mermaid code using mermaid.ink API (synchronous)."""
        try:
            # Encode the mermaid code for URL
            encoded_code = base64.b64encode(mermaid_code.encode()).decode()
            
            # Use mermaid.ink API to generate PNG
            url = f"https://mermaid.ink/img/{encoded_code}?type=png&theme=default"
            
            logger.info(f"  Generating {diagram_type} diagram...")
            
            # Download the image
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.content
            else:
                logger.warning(f"  Warning: Failed to generate {diagram_type} diagram "
                              f"(HTTP {response.status_code})")
                return None
                
        except Exception as e:
            logger.warning(f"  Warning: Error generating {diagram_type} diagram: {e}")
            return None
    
    def convert_mermaid_to_images(self, markdown_content: str, output_dir: Path) -> str:
        """Convert mermaid diagrams to embedded images."""
        mermaid_pattern = r'```mermaid\s*\n(.*?)\n```'
        
        def replace_mermaid(match):
            diagram_content = match.group(1)
            
            # Determine diagram type
            if 'flowchart' in diagram_content:
                diagram_type = "System Architecture"
                description = "This diagram shows the system architecture and data flow for the DIA3 Strategic Intelligence Framework."
            elif 'graph' in diagram_content:
                diagram_type = "Component Relationship"
                description = "This diagram illustrates the relationships between different system components."
            else:
                diagram_type = "Process Flow"
                description = "This diagram demonstrates the analysis process flow and decision points."
            
            # Generate image synchronously
            image_data = self.generate_mermaid_image_sync(diagram_content, diagram_type.lower())
            
            if image_data:
                # Save image to file
                content_hash = hashlib.md5(diagram_content.encode()).hexdigest()[:8]
                image_filename = f"diagram_{diagram_type.lower().replace(' ', '_')}_{content_hash}.png"
                image_path = output_dir / image_filename
                
                with open(image_path, 'wb') as f:
                    f.write(image_data)
                
                # Return HTML with embedded image
                return f'''
<div class="diagram-container">
    <div class="diagram-title">{diagram_type} Diagram</div>
    <img src="{image_filename}" alt="{diagram_type} Diagram" class="diagram-image">
    <div class="diagram-description">{description}</div>
</div>
'''
            else:
                # Fallback to text description if image generation fails
                return f'''
<div class="diagram-container">
    <div class="diagram-title">{diagram_type} Diagram</div>
    <div class="diagram-description">
        <strong>Note:</strong> Diagram could not be generated automatically.<br>
        {description}
    </div>
</div>
'''
        
        return re.sub(mermaid_pattern, replace_mermaid, markdown_content, flags=re.DOTALL)
    
    def markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown to HTML with extensions."""
        extensions = [
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.footnotes',
        ]
        
        html = markdown.markdown(markdown_content, extensions=extensions)
        
        # Add CSS classes for styling
        html = html.replace('<h1>', '<h1 class="main-title">')
        html = html.replace('<h2>', '<h2 class="section-title">')
        html = html.replace('<h3>', '<h3 class="subsection-title">')
        
        return html
    
    async def generate_html_with_diagrams(self, markdown_file: Path, output_file: Path, title: str) -> bool:
        """Generate HTML from markdown file with embedded mermaid diagrams."""
        logger.info(f"Processing: {markdown_file}")
        
        # Read markdown content
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            logger.error(f"✗ File not found: {markdown_file}")
            return False
        except Exception as e:
            logger.error(f"✗ Error reading file {markdown_file}: {e}")
            return False
        
        # Create images directory
        images_dir = output_file.parent / "images"
        images_dir.mkdir(exist_ok=True)
        
        # Convert mermaid diagrams to images
        logger.info("Converting mermaid diagrams to images...")
        content = self.convert_mermaid_to_images(content, images_dir)
        
        # Convert markdown to HTML
        html_content = self.markdown_to_html(content)
        
        # Create HTML document
        template = Template(HTML_TEMPLATE)
        html_doc = template.render(
            title=title,
            css=CSS_TEMPLATE,
            content=html_content
        )
        
        try:
            # Write HTML file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_doc)
            
            logger.success(f"✓ Successfully generated: {output_file}")
            return True
        except Exception as e:
            logger.error(f"✗ Error generating HTML: {e}")
            return False
    
    async def generate_pdf_from_markdown(self, markdown_file: str, output_name: str = None, title: str = None) -> Dict[str, Any]:
        """Generate PDF-ready HTML from markdown file."""
        try:
            markdown_path = Path(markdown_file)
            if not markdown_path.exists():
                return {
                    "success": False,
                    "error": f"Markdown file not found: {markdown_file}"
                }
            
            # Determine output name
            if output_name is None:
                output_name = markdown_path.stem
            
            # Determine title
            if title is None:
                title = f"DIA3: {output_name.replace('_', ' ').title()}"
            
            # Generate output path
            output_file = self.output_dir / f"{output_name}.html"
            
            # Generate HTML with diagrams
            success = await self.generate_html_with_diagrams(markdown_path, output_file, title)
            
            if success:
                return {
                    "success": True,
                    "html_file": str(output_file),
                    "title": title,
                    "message": "PDF-ready HTML generated successfully. Use browser print function to convert to PDF."
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to generate HTML file"
                }
                
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_white_paper_pdfs(self) -> Dict[str, Any]:
        """Generate PDFs for all white papers."""
        try:
            docs_dir = self.base_dir / "docs" / "white_papers"
            
            # Define files to convert
            files_to_convert = [
                {
                    'input': docs_dir / "DIA3_Strategic_Intelligence_White_Paper.md",
                    'output_name': "DIA3_Strategic_Intelligence_White_Paper",
                    'title': "DIA3: Decision Intelligence Agentic, Autonomous, & Adaptive - Strategic Intelligence Framework White Paper"
                },
                {
                    'input': docs_dir / "DIA3_White_Paper_Summary.md",
                    'output_name': "DIA3_White_Paper_Executive_Summary",
                    'title': "DIA3 Strategic Intelligence Framework - Executive Summary"
                }
            ]
            
            results = []
            success_count = 0
            
            for file_info in files_to_convert:
                if file_info['input'].exists():
                    result = await self.generate_pdf_from_markdown(
                        str(file_info['input']),
                        file_info['output_name'],
                        file_info['title']
                    )
                    results.append(result)
                    if result['success']:
                        success_count += 1
                else:
                    results.append({
                        "success": False,
                        "error": f"File not found: {file_info['input']}"
                    })
            
            return {
                "success": success_count > 0,
                "total_files": len(files_to_convert),
                "successful_files": success_count,
                "results": results,
                "output_directory": str(self.output_dir)
            }
            
        except Exception as e:
            logger.error(f"Error generating white paper PDFs: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Global service instance
enhanced_pdf_service = EnhancedPDFGenerationService()
