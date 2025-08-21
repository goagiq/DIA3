#!/usr/bin/env python3
"""
File Generation Demo

Demonstrates the new file generation utilities that automatically prepend
file:///D:/AI/DIA3/ to all generated files.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.utils.file_generator import (
    file_generator,
    save_json,
    save_text,
    save_binary,
    save_report,
    save_visualization
)
from core.utils.file_path_utils import FilePathUtils


def demo_file_generation():
    """Demonstrate file generation with protocol prefix."""
    print("🚀 File Generation Demo with file:///D:/AI/DIA3/ prefix")
    print("=" * 60)
    
    # Demo 1: Save JSON file
    print("\n1. Saving JSON file...")
    data = {
        "analysis_type": "demo",
        "timestamp": "2025-01-17T10:00:00",
        "results": {
            "accuracy": 0.95,
            "precision": 0.92,
            "recall": 0.88
        }
    }
    
    result = save_json(data, "demo_analysis_results.json", "Results/demo")
    if result["success"]:
        print(f"✅ JSON saved: {result['file_info']['file_url']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Demo 2: Save text file
    print("\n2. Saving text file...")
    content = """
# Analysis Report

This is a demo analysis report generated with the new file generation utilities.

## Key Findings
- All files now have file:///D:/AI/DIA3/ prefix
- Centralized file generation system
- Automatic protocol prefix prepending

## Benefits
- Consistent file URLs across the system
- Easy file access and sharing
- Standardized file management
"""
    
    result = save_text(content, "demo_report.md", "Results/demo")
    if result["success"]:
        print(f"✅ Text saved: {result['file_info']['file_url']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Demo 3: Save binary file
    print("\n3. Saving binary file...")
    binary_data = b"This is binary data for demonstration purposes."
    
    result = save_binary(binary_data, "demo_binary.bin", "Results/demo")
    if result["success"]:
        print(f"✅ Binary saved: {result['file_info']['file_url']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Demo 4: Save report
    print("\n4. Saving report...")
    report_content = """
# Comprehensive Analysis Report

## Executive Summary
This report demonstrates the new file generation capabilities.

## Technical Details
- File protocol prefix: file:///D:/AI/DIA3/
- Automatic directory creation
- Metadata tracking
- URL generation

## Results
All files are now accessible via standardized URLs.
"""
    
    result = save_report(report_content, "comprehensive_analysis.md", "demo_report")
    if result["success"]:
        print(f"✅ Report saved: {result['file_info']['file_url']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Demo 5: Save visualization
    print("\n5. Saving visualization...")
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Demo Visualization</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .chart { width: 600px; height: 400px; background: #f0f0f0; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <h1>Demo Visualization</h1>
    <div class="chart">
        <h2>Sample Chart</h2>
        <p>This is a demo visualization saved with protocol prefix.</p>
    </div>
</body>
</html>
"""
    
    result = save_visualization(html_content, "Demo Analysis Chart")
    if result["success"]:
        print(f"✅ Visualization saved: {result['file_info']['file_url']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Demo 6: Show all generated files
    print("\n6. All generated files:")
    generated_files = file_generator.get_generated_files()
    for i, file_info in enumerate(generated_files, 1):
        print(f"   {i}. {file_info['filename']}")
        print(f"      URL: {file_info['file_url']}")
        print(f"      Size: {file_info['size_kb']} KB")
        print()
    
    # Demo 7: File path utilities
    print("7. File path utilities:")
    test_path = "Results/demo/test_file.txt"
    prefixed_path = FilePathUtils.prepend_file_protocol(test_path)
    print(f"   Original: {test_path}")
    print(f"   With prefix: {prefixed_path}")
    
    # Demo 8: Directory-specific paths
    print("\n8. Directory-specific paths:")
    print(f"   Results: {FilePathUtils.get_results_path('test.json')}")
    print(f"   Reports: {FilePathUtils.get_reports_path('test.md')}")
    print(f"   Docs: {FilePathUtils.get_docs_path('test.pdf')}")
    print(f"   White papers: {FilePathUtils.get_white_papers_path('test.docx')}")
    
    print("\n🎉 Demo completed successfully!")
    print(f"Total files generated: {len(generated_files)}")


if __name__ == "__main__":
    demo_file_generation()
