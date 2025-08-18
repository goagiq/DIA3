#!/usr/bin/env python3
"""
Simple DIA3 Strategic Intelligence Question Framework Whitepaper PDF Converter

This script converts the HTML whitepaper to PDF format using weasyprint.
It's a simpler version that doesn't require Mermaid diagram rendering.

Requirements:
- weasyprint (for HTML to PDF conversion)
- requests (for downloading fonts)

Usage:
    python convert_whitepaper_simple.py
"""

import os
import sys
import subprocess
import tempfile
import requests
from pathlib import Path
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import weasyprint
        print("✓ weasyprint is installed")
    except ImportError:
        print("✗ weasyprint is not installed. Installing...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "weasyprint"
        ])
    
    try:
        import requests
        print("✓ requests is installed")
    except ImportError:
        print("✗ requests is not installed. Installing...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "requests"
        ])


def download_fonts():
    """Download required fonts for the PDF."""
    fonts_dir = Path("fonts")
    fonts_dir.mkdir(exist_ok=True)
    
    # Download Inter font family
    font_urls = {
        "Inter-Regular.ttf": (
            "https://github.com/rsms/inter/raw/master/docs/font-files/"
            "Inter-Regular.ttf"
        ),
        "Inter-Medium.ttf": (
            "https://github.com/rsms/inter/raw/master/docs/font-files/"
            "Inter-Medium.ttf"
        ),
        "Inter-SemiBold.ttf": (
            "https://github.com/rsms/inter/raw/master/docs/font-files/"
            "Inter-SemiBold.ttf"
        ),
        "Inter-Bold.ttf": (
            "https://github.com/rsms/inter/raw/master/docs/font-files/"
            "Inter-Bold.ttf"
        )
    }
    
    for font_name, font_url in font_urls.items():
        font_path = fonts_dir / font_name
        if not font_path.exists():
            print(f"Downloading {font_name}...")
            response = requests.get(font_url)
            response.raise_for_status()
            with open(font_path, 'wb') as f:
                f.write(response.content)
            print(f"✓ Downloaded {font_name}")


def create_pdf_css():
    """Create CSS for PDF styling."""
    return """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    @page {
        size: A4;
        margin: 2cm;
        @top-center {
            content: "DIA3 Strategic Intelligence Question Framework Whitepaper";
            font-family: 'Inter', sans-serif;
            font-size: 10pt;
            color: #64748b;
        }
        @bottom-center {
            content: "Page " counter(page) " of " counter(pages);
            font-family: 'Inter', sans-serif;
            font-size: 10pt;
            color: #64748b;
        }
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6;
        color: #333;
        background: #fff;
        font-size: 11pt;
    }
    
    .header {
        text-align: center;
        margin-bottom: 40px;
        padding: 40px 0;
        border-bottom: 3px solid #1e40af;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        page-break-after: avoid;
    }
    
    .header h1 {
        font-size: 24pt;
        font-weight: 700;
        color: #1e40af;
        margin-bottom: 10px;
    }
    
    .header h2 {
        font-size: 16pt;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 20px;
    }
    
    .subtitle {
        font-size: 12pt;
        color: #64748b;
        font-style: italic;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1e40af;
        margin: 20px 0 10px 0;
        font-weight: 600;
        page-break-after: avoid;
    }
    
    h1 {
        font-size: 18pt;
        border-bottom: 2px solid #1e40af;
        padding-bottom: 8px;
    }
    
    h2 {
        font-size: 16pt;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 6px;
    }
    
    h3 {
        font-size: 14pt;
    }
    
    h4 {
        font-size: 12pt;
    }
    
    p {
        margin-bottom: 12px;
        text-align: justify;
    }
    
    strong {
        color: #1e40af;
        font-weight: 600;
    }
    
    .mermaid {
        text-align: center;
        margin: 20px 0;
        padding: 15px;
        background: #f8fafc;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
        page-break-inside: avoid;
        font-family: monospace;
        font-size: 10pt;
        color: #64748b;
    }
    
    .mermaid::before {
        content: "[Mermaid Diagram - See HTML version for visual]";
        display: block;
        font-weight: bold;
        margin-bottom: 10px;
        color: #1e40af;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 4px solid #1e40af;
        padding: 15px;
        margin: 15px 0;
        border-radius: 0 6px 6px 0;
        page-break-inside: avoid;
    }
    
    .highlight-box strong {
        color: #1e40af;
        font-weight: 700;
    }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 50%, #1e40af 100%);
        margin: 30px 0;
        border-radius: 1px;
    }
    
    .key-points {
        background: #f0f9ff;
        border: 1px solid #0ea5e9;
        border-radius: 6px;
        padding: 15px;
        margin: 15px 0;
        page-break-inside: avoid;
    }
    
    .key-points h4 {
        color: #0ea5e9;
        margin-bottom: 12px;
    }
    
    .key-points ul {
        list-style: none;
        padding-left: 0;
    }
    
    .key-points li {
        padding: 6px 0;
        border-bottom: 1px solid #e0f2fe;
    }
    
    .key-points li:last-child {
        border-bottom: none;
    }
    
    .key-points li:before {
        content: "•";
        color: #0ea5e9;
        font-weight: bold;
        margin-right: 8px;
    }
    
    .conclusion {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 2px solid #f59e0b;
        border-radius: 6px;
        padding: 20px;
        margin: 30px 0;
        page-break-inside: avoid;
    }
    
    .conclusion h2 {
        color: #d97706;
        border-bottom: 2px solid #f59e0b;
    }
    
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 20px 0;
        border-top: 2px solid #1e40af;
        background: #f8fafc;
        border-radius: 6px;
        page-break-inside: avoid;
    }
    
    .footer p {
        margin: 4px 0;
        color: #64748b;
    }
    
    .footer strong {
        color: #1e40af;
    }
    
    /* Print-specific styles */
    @media print {
        body {
            font-size: 10pt;
        }
        
        .header h1 {
            font-size: 20pt;
        }
        
        .header h2 {
            font-size: 14pt;
        }
        
        h1 {
            font-size: 16pt;
        }
        
        h2 {
            font-size: 14pt;
        }
        
        h3 {
            font-size: 12pt;
        }
        
        .mermaid {
            page-break-inside: avoid;
        }
    }
    """


def convert_html_to_pdf(html_file, pdf_file):
    """Convert HTML file to PDF with proper styling."""
    print(f"Converting {html_file} to {pdf_file}...")
    
    # Create CSS for PDF styling
    css_content = create_pdf_css()
    
    # Configure fonts
    font_config = FontConfiguration()
    
    # Convert to PDF
    HTML(filename=html_file).write_pdf(
        pdf_file,
        stylesheets=[CSS(string=css_content)],
        font_config=font_config
    )
    
    print(f"✓ Successfully created {pdf_file}")


def main():
    """Main function to convert the whitepaper to PDF."""
    print("DIA3 Strategic Intelligence Question Framework Whitepaper PDF Converter")
    print("=" * 70)
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    check_dependencies()
    
    # Download fonts
    print("\n2. Downloading fonts...")
    download_fonts()
    
    # Define file paths
    html_file = "DIA3_Strategic_Intelligence_Question_Framework_Whitepaper.html"
    pdf_file = "DIA3_Strategic_Intelligence_Question_Framework_Whitepaper.pdf"
    
    # Check if HTML file exists
    if not os.path.exists(html_file):
        print(f"✗ HTML file {html_file} not found!")
        print("Please ensure the HTML whitepaper file exists in the current directory.")
        return 1
    
    # Convert to PDF
    print(f"\n3. Converting to PDF...")
    try:
        convert_html_to_pdf(html_file, pdf_file)
        print(f"\n✓ PDF conversion completed successfully!")
        print(f"📄 Output file: {pdf_file}")
        print("\nNote: Mermaid diagrams are shown as placeholders in the PDF.")
        print("For full visual diagrams, please view the HTML version.")
        return 0
    except Exception as e:
        print(f"\n✗ PDF conversion failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
