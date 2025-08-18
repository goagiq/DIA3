#!/usr/bin/env python3
"""
Enhanced DIA3 Strategic Intelligence Question Framework Whitepaper Converter

This script converts the comprehensive DIA3 whitepaper from Markdown to both
Word (.docx) and PDF formats with proper handling of:
- Markdown formatting (bold, italic, etc.)
- Image references and generation
- Tables and complex formatting
- Proper document structure
"""

import asyncio
import sys
import os
import re
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


async def convert_dia3_whitepaper_enhanced():
    """Convert the DIA3 whitepaper to PDF and Word formats with enhanced formatting."""
    print("🚀 Enhanced DIA3 Strategic Intelligence Question Framework Whitepaper Converter")
    print("=" * 80)
    print("📋 Converting comprehensive whitepaper with enhanced formatting:")
    print("   • Proper Markdown formatting (bold, italic, etc.)")
    print("   • Image generation and embedding")
    print("   • Enhanced table formatting")
    print("   • Professional document structure")
    print("=" * 80)
    
    try:
        # Import the enhanced export service
        from src.core.export.enhanced_markdown_export_service import EnhancedMarkdownExportService
        
        # Initialize export service with output directory
        output_dir = "docs/white_papers/generated_pdfs"
        export_service = EnhancedMarkdownExportService(output_dir)
        
        # Read the markdown file
        markdown_file = ("docs/white_papers/"
                        "DIA3_Strategic_Intelligence_Question_Framework_Whitepaper.md")
        
        if not os.path.exists(markdown_file):
            print("❌ Markdown file not found: {}".format(markdown_file))
            print("Please ensure the whitepaper file exists in the correct location.")
            return False
        
        print("📄 Reading markdown file: {}".format(markdown_file))
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Analyze the content
        lines = markdown_content.split('\n')
        word_count = len(markdown_content.split())
        char_count = len(markdown_content)
        
        print("📊 Content Analysis:")
        print("   • Total lines: {:,}".format(len(lines)))
        print("   • Word count: {:,}".format(word_count))
        print("   • Character count: {:,}".format(char_count))
        print("   • File size: {:,} bytes".format(
            len(markdown_content.encode('utf-8'))))
        
        # Check for image references
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        images = re.findall(image_pattern, markdown_content)
        print("   • Image references found: {}".format(len(images)))
        
        # Check for markdown formatting
        bold_pattern = r'\*\*([^*]+)\*\*'
        bold_count = len(re.findall(bold_pattern, markdown_content))
        print("   • Bold text elements: {}".format(bold_count))
        
        # Check for key sections
        sections = [
            "Executive Summary",
            "System Architecture",
            "The Intelligence Question Framework",
            "Category 1: Adversary Intent & Capability Assessment",
            "Category 2: Strategic Risk Assessment",
            "Category 3: Operational Planning & Decision Support",
            "Category 4: Intelligence Fusion & Predictive Analysis",
            "Category 5: Strategic Planning & Force Development",
            "Implementation Methodology",
            "Budgetary Planning",
            "Roadmap",
            "Conclusion"
        ]
        
        print("\n📋 Document Structure Analysis:")
        for section in sections:
            if section in markdown_content:
                print("   ✅ {}".format(section))
            else:
                print("   ❌ {} (not found)".format(section))
        
        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Convert to PDF with enhanced formatting
        print("\n📄 Converting to PDF (Enhanced)...")
        pdf_filename = "DIA3_Strategic_Intelligence_Question_Framework_Whitepaper_Enhanced_{}.pdf".format(timestamp)
        
        pdf_result = await export_service.export_markdown_to_pdf_enhanced(
            markdown_content,
            output_filename=pdf_filename
        )
        
        if pdf_result["success"]:
            print("✅ Enhanced PDF conversion successful!")
            print("   📁 File: {}".format(pdf_result['output_path']))
            print("   📊 Size: {:,} bytes".format(pdf_result['file_size']))
        else:
            print("❌ Enhanced PDF conversion failed: {}".format(pdf_result['error']))
            return False
        
        # Convert to Word with enhanced formatting
        print("\n📄 Converting to Word (Enhanced)...")
        word_filename = "DIA3_Strategic_Intelligence_Question_Framework_Whitepaper_Enhanced_{}.docx".format(timestamp)
        
        word_result = await export_service.export_markdown_to_word_enhanced(
            markdown_content,
            output_filename=word_filename
        )
        
        if word_result["success"]:
            print("✅ Enhanced Word conversion successful!")
            print("   📁 File: {}".format(word_result['output_path']))
            print("   📊 Size: {:,} bytes".format(word_result['file_size']))
        else:
            print("❌ Enhanced Word conversion failed: {}".format(word_result['error']))
            return False
        
        # Summary
        print("\n🎉 Enhanced Conversion Summary:")
        print("   📄 PDF file created: {}".format(pdf_filename))
        print("   📄 Word file created: {}".format(word_filename))
        print("   📁 Output directory: {}".format(output_dir))
        print("   ⏱️  Timestamp: {}".format(timestamp))
        
        print("\n📋 Generated Files:")
        print("   1. {}".format(pdf_filename))
        print("   2. {}".format(word_filename))
        
        print("\n💡 Enhanced Features:")
        print("   • Proper Markdown formatting preserved")
        print("   • Images generated and embedded")
        print("   • Professional document styling")
        print("   • Enhanced table formatting")
        print("   • Better typography and layout")
        
        return True
        
    except ImportError as e:
        print("❌ Import error: {}".format(e))
        print("Please ensure all dependencies are installed:")
        print("pip install markdown python-docx reportlab pillow")
        return False
    except Exception as e:
        print("❌ Conversion error: {}".format(e))
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function."""
    print("Starting enhanced DIA3 whitepaper conversion...")
    success = asyncio.run(convert_dia3_whitepaper_enhanced())
    
    if success:
        print("\n✅ Enhanced conversion completed successfully!")
        return 0
    else:
        print("\n❌ Enhanced conversion failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
