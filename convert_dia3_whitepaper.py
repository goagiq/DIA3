#!/usr/bin/env python3
"""
DIA3 Strategic Intelligence Question Framework Whitepaper Converter

This script converts the comprehensive DIA3 whitepaper from Markdown to both
Word (.docx) and PDF formats using the existing export service infrastructure.

The whitepaper contains:
- Executive Summary and Strategic Impact
- System Architecture and Intelligence Framework
- 5 Framework Categories with detailed analysis
- Implementation Methodology and Best Practices
- Budgetary Planning and Strategic Roadmap
- Comprehensive tables and visualizations
"""

import asyncio
import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


async def convert_dia3_whitepaper():
    """Convert the DIA3 whitepaper to PDF and Word formats."""
    print("🚀 DIA3 Strategic Intelligence Question Framework Whitepaper Converter")
    print("=" * 80)
    print("📋 Converting comprehensive whitepaper with:")
    print("   • Executive Summary and Strategic Impact")
    print("   • System Architecture and Intelligence Framework")
    print("   • 5 Framework Categories with detailed analysis")
    print("   • Implementation Methodology and Best Practices")
    print("   • Budgetary Planning and Strategic Roadmap")
    print("   • Comprehensive tables and visualizations")
    print("=" * 80)
    
    try:
        # Import the simple export service
        from src.core.export.simple_markdown_export_service import SimpleMarkdownExportService
        
        # Initialize export service with output directory
        output_dir = "docs/white_papers/generated_pdfs"
        export_service = SimpleMarkdownExportService(output_dir)
        
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
        
        print(f"\n📋 Document Structure Analysis:")
        for section in sections:
            if section in markdown_content:
                print(f"   ✅ {section}")
            else:
                print(f"   ❌ {section} (not found)")
        
        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Convert to PDF
        print(f"\n📄 Converting to PDF...")
        pdf_filename = f"DIA3_Strategic_Intelligence_Question_Framework_Whitepaper_{timestamp}.pdf"
        
        pdf_result = await export_service.export_markdown_to_pdf(
            markdown_content,
            output_filename=pdf_filename
        )
        
        if pdf_result["success"]:
            print(f"✅ PDF conversion successful!")
            print(f"   📁 File: {pdf_result['output_path']}")
            print(f"   📊 Size: {pdf_result['file_size']:,} bytes")
        else:
            print(f"❌ PDF conversion failed: {pdf_result['error']}")
            return False
        
        # Convert to Word
        print(f"\n📄 Converting to Word...")
        word_filename = f"DIA3_Strategic_Intelligence_Question_Framework_Whitepaper_{timestamp}.docx"
        
        word_result = await export_service.export_markdown_to_word(
            markdown_content,
            output_filename=word_filename
        )
        
        if word_result["success"]:
            print(f"✅ Word conversion successful!")
            print(f"   📁 File: {word_result['output_path']}")
            print(f"   📊 Size: {word_result['file_size']:,} bytes")
        else:
            print(f"❌ Word conversion failed: {word_result['error']}")
            return False
        
        # Convert to both formats using the combined method
        print(f"\n📄 Converting to both formats (combined method)...")
        combined_filename = f"DIA3_Strategic_Intelligence_Question_Framework_Whitepaper_Combined_{timestamp}"
        
        both_result = await export_service.export_markdown_to_both(
            markdown_content,
            output_filename=combined_filename
        )
        
        if both_result["success"]:
            print(f"✅ Combined conversion successful!")
            print(f"   📁 PDF: {both_result['pdf_result']['output_path']}")
            print(f"   📁 Word: {both_result['word_result']['output_path']}")
        else:
            print(f"❌ Combined conversion failed: {both_result['error']}")
            # Don't return False here as individual conversions succeeded
        
        # Summary
        print(f"\n🎉 Conversion Summary:")
        print(f"   📄 PDF files created: 2")
        print(f"   📄 Word files created: 2")
        print(f"   📁 Output directory: {output_dir}")
        print(f"   ⏱️  Timestamp: {timestamp}")
        
        print(f"\n📋 Generated Files:")
        print(f"   1. {pdf_filename}")
        print(f"   2. {word_filename}")
        print(f"   3. {combined_filename}.pdf")
        print(f"   4. {combined_filename}.docx")
        
        print(f"\n💡 Next Steps:")
        print(f"   • Review the generated files for formatting")
        print(f"   • Check that all sections are properly converted")
        print(f"   • Verify tables and special formatting")
        print(f"   • Share the documents with stakeholders")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install markdown python-docx reportlab")
        return False
    except Exception as e:
        print(f"❌ Conversion error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    print("Starting DIA3 whitepaper conversion...")
    success = asyncio.run(convert_dia3_whitepaper())
    
    if success:
        print("\n✅ Conversion completed successfully!")
        return 0
    else:
        print("\n❌ Conversion failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
