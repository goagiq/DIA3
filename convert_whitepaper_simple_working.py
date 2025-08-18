#!/usr/bin/env python3
"""
Simple DIA3 Strategic Intelligence Question Framework Whitepaper Converter

This script converts the markdown whitepaper to PDF and DOC formats using the
simplified export service that doesn't require WeasyPrint.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def convert_whitepaper():
    """Convert the whitepaper to PDF and DOC formats."""
    print("🚀 DIA3 Strategic Intelligence Question Framework Whitepaper Converter")
    print("=" * 70)
    
    try:
        # Import the simple export service
        from src.core.export.simple_markdown_export_service import SimpleMarkdownExportService
        
        # Initialize export service
        output_dir = "docs/white_papers"
        export_service = SimpleMarkdownExportService(output_dir)
        
        # Read the markdown file
        markdown_file = "docs/white_papers/DIA3_Strategic_Intelligence_Question_Framework_Whitepaper.md"
        
        if not os.path.exists(markdown_file):
            print(f"❌ Markdown file not found: {markdown_file}")
            return False
        
        print(f"📄 Reading markdown file: {markdown_file}")
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        print(f"📊 File size: {len(markdown_content)} characters")
        
        # Convert to PDF
        print("\n📄 Converting to PDF...")
        pdf_result = await export_service.export_markdown_to_pdf(
            markdown_content,
            output_filename="DIA3_Strategic_Intelligence_Question_Framework_Whitepaper.pdf"
        )
        
        if pdf_result["success"]:
            print(f"✅ PDF conversion successful: {pdf_result['output_path']}")
            print(f"📊 PDF file size: {pdf_result['file_size']} bytes")
        else:
            print(f"❌ PDF conversion failed: {pdf_result['error']}")
            return False
        
        # Convert to Word
        print("\n📄 Converting to Word...")
        word_result = await export_service.export_markdown_to_word(
            markdown_content,
            output_filename="DIA3_Strategic_Intelligence_Question_Framework_Whitepaper.docx"
        )
        
        if word_result["success"]:
            print(f"✅ Word conversion successful: {word_result['output_path']}")
            print(f"📊 Word file size: {word_result['file_size']} bytes")
        else:
            print(f"❌ Word conversion failed: {word_result['error']}")
            return False
        
        # Convert to both formats
        print("\n📄 Converting to both formats...")
        both_result = await export_service.export_markdown_to_both(
            markdown_content,
            output_filename="DIA3_Strategic_Intelligence_Question_Framework_Whitepaper_Both"
        )
        
        if both_result["success"]:
            print(f"✅ Dual conversion successful")
            print(f"📊 PDF: {both_result['pdf_result']['output_path']}")
            print(f"📊 Word: {both_result['word_result']['output_path']}")
        else:
            print(f"❌ Dual conversion failed: {both_result['error']}")
            return False
        
        print("\n🎉 All conversions completed successfully!")
        print("\n📁 Output files:")
        print(f"  - {pdf_result['output_path']}")
        print(f"  - {word_result['output_path']}")
        print(f"  - {both_result['pdf_result']['output_path']}")
        print(f"  - {both_result['word_result']['output_path']}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements_markdown_export.txt")
        return False
    except Exception as e:
        print(f"❌ Conversion error: {e}")
        return False

def main():
    """Main function."""
    success = asyncio.run(convert_whitepaper())
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
