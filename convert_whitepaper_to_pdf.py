#!/usr/bin/env python3
"""
DIA3 Strategic Intelligence White Paper PDF Converter
Converts the enhanced markdown whitepaper to a professional PDF format
with Mermaid diagrams and visualizations.
"""

import os
import sys
import subprocess
import tempfile
import markdown
from weasyprint import HTML, CSS
from datetime import datetime


def generate_mermaid_diagram(mermaid_code, diagram_name):
    """Generate a Mermaid diagram and return the SVG content."""
    try:
        # Create a temporary file for the Mermaid code
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.mmd', delete=False
        ) as f:
            f.write(mermaid_code)
            temp_file = f.name
        
        # Use mermaid-cli to generate SVG
        output_file = f"{diagram_name}.svg"
        result = subprocess.run([
            'mmdc', 
            '-i', temp_file, 
            '-o', output_file,
            '-t', 'default',
            '-b', 'white'
        ], capture_output=True, text=True)
        
        # Clean up temp file
        os.unlink(temp_file)
        
        if result.returncode == 0 and os.path.exists(output_file):
            with open(output_file, 'r') as f:
                svg_content = f.read()
            os.unlink(output_file)
            return svg_content
        else:
            print(f"Warning: Could not generate diagram {diagram_name}: "
                  f"{result.stderr}")
            return None
            
    except Exception as e:
        print(f"Error generating diagram {diagram_name}: {e}")
        return None


def create_html_with_diagrams(markdown_content):
    """Convert markdown to HTML and replace Mermaid code blocks with generated diagrams."""
    
    # Extract Mermaid diagrams
    mermaid_blocks = []
    diagram_counter = 1
    
    # Find all Mermaid code blocks
    lines = markdown_content.split('\n')
    in_mermaid_block = False
    current_block = []
    current_name = ""
    
    for line in lines:
        if line.strip().startswith('```mermaid'):
            in_mermaid_block = True
            current_block = []
            current_name = f"diagram_{diagram_counter}"
            diagram_counter += 1
        elif line.strip() == '```' and in_mermaid_block:
            in_mermaid_block = False
            mermaid_blocks.append({
                'name': current_name,
                'code': '\n'.join(current_block)
            })
        elif in_mermaid_block:
            current_block.append(line)
    
    # Generate diagrams
    diagram_svgs = {}
    for block in mermaid_blocks:
        svg_content = generate_mermaid_diagram(block['code'], block['name'])
        if svg_content:
            diagram_svgs[block['name']] = svg_content
    
    # Replace Mermaid blocks with generated diagrams
    processed_content = markdown_content
    for block in mermaid_blocks:
        if block['name'] in diagram_svgs:
            # Create HTML for the diagram
            diagram_html = f'''
<div class="mermaid-diagram">
    <div class="diagram-title">Figure {block['name'].replace('diagram_', '')}: {block['name'].replace('_', ' ').title()}</div>
    <div class="diagram-content">
        {diagram_svgs[block['name']]}
    </div>
</div>
'''
            # Replace the Mermaid block
            mermaid_block_text = f"```mermaid\n{block['code']}\n```"
            processed_content = processed_content.replace(mermaid_block_text, diagram_html)
    
    # Convert to HTML
    html_content = markdown.markdown(processed_content, extensions=['tables', 'fenced_code', 'codehilite'])
    
    return html_content

def create_pdf_stylesheet():
    """Create CSS stylesheet for the PDF."""
    return '''
    @page {
        size: A4;
        margin: 1in;
        @top-center {
            content: "DIA3: Decision Intelligence Agentic, Autonomous, & Adaptive";
            font-size: 10pt;
            color: #666;
        }
        @bottom-center {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 10pt;
            color: #666;
        }
    }
    
    body {
        font-family: 'Times New Roman', serif;
        font-size: 12pt;
        line-height: 1.6;
        color: #333;
        margin: 0;
        padding: 0;
    }
    
    h1 {
        font-size: 24pt;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-top: 2em;
        margin-bottom: 1em;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5em;
    }
    
    h2 {
        font-size: 18pt;
        font-weight: bold;
        color: #34495e;
        margin-top: 2em;
        margin-bottom: 1em;
        border-left: 4px solid #3498db;
        padding-left: 1em;
    }
    
    h3 {
        font-size: 14pt;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }
    
    h4 {
        font-size: 12pt;
        font-weight: bold;
        color: #34495e;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    
    p {
        margin-bottom: 1em;
        text-align: justify;
    }
    
    ul, ol {
        margin-bottom: 1em;
        padding-left: 2em;
    }
    
    li {
        margin-bottom: 0.5em;
    }
    
    blockquote {
        border-left: 4px solid #3498db;
        padding-left: 1em;
        margin: 1em 0;
        font-style: italic;
        color: #555;
    }
    
    code {
        font-family: 'Courier New', monospace;
        background-color: #f8f9fa;
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-size: 0.9em;
    }
    
    pre {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 5px;
        padding: 1em;
        overflow-x: auto;
        margin: 1em 0;
    }
    
    pre code {
        background-color: transparent;
        padding: 0;
    }
    
    .mermaid-diagram {
        margin: 2em 0;
        text-align: center;
        page-break-inside: avoid;
    }
    
    .diagram-title {
        font-weight: bold;
        font-size: 11pt;
        color: #2c3e50;
        margin-bottom: 1em;
        text-align: center;
    }
    
    .diagram-content {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 1em;
        background-color: #fafafa;
    }
    
    .diagram-content svg {
        max-width: 100%;
        height: auto;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1em 0;
        page-break-inside: avoid;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 0.5em;
        text-align: left;
    }
    
    th {
        background-color: #f8f9fa;
        font-weight: bold;
    }
    
    .executive-summary {
        background-color: #f8f9fa;
        border: 2px solid #3498db;
        border-radius: 5px;
        padding: 1.5em;
        margin: 2em 0;
    }
    
    .key-capabilities {
        background-color: #e8f4fd;
        border-left: 4px solid #3498db;
        padding: 1em;
        margin: 1em 0;
    }
    
    .key-capabilities ul {
        margin: 0.5em 0;
    }
    
    .key-capabilities li {
        margin-bottom: 0.3em;
    }
    
    .conclusion {
        background-color: #f0f8ff;
        border: 2px solid #2c3e50;
        border-radius: 5px;
        padding: 1.5em;
        margin: 2em 0;
    }
    
    .footer {
        text-align: center;
        font-size: 10pt;
        color: #666;
        margin-top: 2em;
        border-top: 1px solid #ddd;
        padding-top: 1em;
    }
    '''

def create_html_document(html_content):
    """Create a complete HTML document with proper structure."""
    stylesheet = create_pdf_stylesheet()
    
    html_doc = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DIA3: Decision Intelligence Agentic, Autonomous, & Adaptive</title>
    <style>
        {stylesheet}
    </style>
</head>
<body>
    <div class="document">
        {html_content}
        
        <div class="footer">
            <p><strong>Document Version:</strong> 2.0 | <strong>Last Updated:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
            <p><strong>Classification:</strong> UNCLASSIFIED | <strong>Distribution:</strong> Intelligence Community, Department of Defense, Strategic Partners</p>
            <p><em>DIA3: Decision Intelligence Agentic, Autonomous, & Adaptive - Transforming Intelligence Analysis for the Digital Age</em></p>
        </div>
    </div>
</body>
</html>
'''
    return html_doc

def main():
    """Main function to convert the whitepaper to PDF."""
    
    # File paths
    input_file = "docs/white_papers/DIA3_Strategic_Intelligence_White_Paper_Enhanced.md"
    output_file = "docs/white_papers/DIA3_Strategic_Intelligence_White_Paper_Enhanced.pdf"
    
    print("DIA3 Strategic Intelligence White Paper PDF Converter")
    print("=" * 60)
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    try:
        # Read the markdown content
        print("Reading markdown content...")
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert markdown to HTML with diagrams
        print("Converting markdown to HTML and generating diagrams...")
        html_content = create_html_with_diagrams(markdown_content)
        
        # Create complete HTML document
        print("Creating HTML document...")
        html_doc = create_html_document(html_content)
        
        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_doc)
            temp_html = f.name
        
        # Convert HTML to PDF
        print("Converting HTML to PDF...")
        html = HTML(filename=temp_html)
        css = CSS(string=create_pdf_stylesheet())
        html.write_pdf(output_file, stylesheets=[css])
        
        # Clean up temporary file
        os.unlink(temp_html)
        
        print(f"Successfully created PDF: {output_file}")
        print(f"File size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
