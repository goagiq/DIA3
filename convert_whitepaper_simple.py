#!/usr/bin/env python3
"""
DIA3 Strategic Intelligence White Paper PDF Converter (Simple Version)
Converts the enhanced markdown whitepaper to a professional PDF format
using a simpler approach without complex dependencies.
"""

import os
import sys
import subprocess
import tempfile
from datetime import datetime

def create_html_document(markdown_content):
    """Create a complete HTML document with embedded CSS."""
    
    # Convert markdown to HTML (simple conversion)
    html_content = markdown_content.replace('# ', '<h1>').replace('\n# ', '</h1>\n<h1>')
    html_content = html_content.replace('## ', '<h2>').replace('\n## ', '</h2>\n<h2>')
    html_content = html_content.replace('### ', '<h3>').replace('\n### ', '</h3>\n<h3>')
    html_content = html_content.replace('#### ', '<h4>').replace('\n#### ', '</h4>\n<h4>')
    
    # Convert bold text
    html_content = html_content.replace('**', '<strong>').replace('**', '</strong>')
    
    # Convert italic text
    html_content = html_content.replace('*', '<em>').replace('*', '</em>')
    
    # Convert lists
    html_content = html_content.replace('- ', '<li>').replace('\n- ', '</li>\n<li>')
    
    # Convert paragraphs
    html_content = html_content.replace('\n\n', '</p>\n<p>')
    
    # Add CSS styling
    css_styles = '''
    <style>
        body {
            font-family: Arial, sans-serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #333;
            margin: 2em;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
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
        
        .mermaid-diagram {
            margin: 2em 0;
            text-align: center;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 1em;
            background-color: #fafafa;
        }
        
        .diagram-title {
            font-weight: bold;
            font-size: 11pt;
            color: #2c3e50;
            margin-bottom: 1em;
            text-align: center;
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
        
        @media print {
            body {
                margin: 1in;
            }
            
            h1, h2, h3, h4 {
                page-break-after: avoid;
            }
            
            .mermaid-diagram {
                page-break-inside: avoid;
            }
        }
    </style>
    '''
    
    html_doc = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DIA3: Decision Intelligence Agentic, Autonomous, & Adaptive</title>
    {css_styles}
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

def convert_html_to_pdf(html_file, pdf_file):
    """Convert HTML to PDF using wkhtmltopdf if available, otherwise create HTML file."""
    try:
        # Try to use wkhtmltopdf if available
        result = subprocess.run([
            'wkhtmltopdf',
            '--page-size', 'A4',
            '--margin-top', '1in',
            '--margin-bottom', '1in',
            '--margin-left', '1in',
            '--margin-right', '1in',
            '--header-center', 'DIA3: Decision Intelligence Agentic, Autonomous, & Adaptive',
            '--header-font-size', '10',
            '--footer-center', '[page] of [topage]',
            '--footer-font-size', '10',
            html_file,
            pdf_file
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            print(f"wkhtmltopdf failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("wkhtmltopdf not found. Creating HTML file instead.")
        return False

def main():
    """Main function to convert the whitepaper to PDF."""
    
    # File paths
    input_file = "docs/white_papers/DIA3_Strategic_Intelligence_White_Paper_Enhanced.md"
    output_html = "docs/white_papers/DIA3_Strategic_Intelligence_White_Paper_Enhanced.html"
    output_pdf = "docs/white_papers/DIA3_Strategic_Intelligence_White_Paper_Enhanced.pdf"
    
    print("DIA3 Strategic Intelligence White Paper Converter")
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
        
        # Create HTML document
        print("Creating HTML document...")
        html_doc = create_html_document(markdown_content)
        
        # Write HTML file
        print("Writing HTML file...")
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_doc)
        
        print(f"Successfully created HTML: {output_html}")
        
        # Try to convert to PDF
        print("Attempting to convert to PDF...")
        if convert_html_to_pdf(output_html, output_pdf):
            print(f"Successfully created PDF: {output_pdf}")
            print(f"File size: {os.path.getsize(output_pdf) / 1024 / 1024:.2f} MB")
        else:
            print("PDF conversion failed. HTML file created successfully.")
            print("You can open the HTML file in a browser and use 'Print to PDF' to create a PDF.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

