#!/usr/bin/env python3
"""
Simple DIA3 Whitepaper Converter

Quick script to convert the DIA3 Strategic Intelligence Question Framework 
Whitepaper from Markdown to Word and PDF formats.

Usage:
    python convert_whitepaper.py
"""

import subprocess
import sys
import os


def main():
    """Run the whitepaper conversion."""
    print("🔄 Running DIA3 whitepaper conversion...")
    
    # Check if the conversion script exists
    conversion_script = "convert_dia3_whitepaper.py"
    if not os.path.exists(conversion_script):
        print("❌ Conversion script not found: {}".format(conversion_script))
        return 1
    
    # Run the conversion script
    try:
        result = subprocess.run([
            sys.executable, conversion_script
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n✅ Whitepaper conversion completed successfully!")
            print("\n📁 Generated files are in: docs/white_papers/generated_pdfs/")
            return 0
        else:
            print("\n❌ Conversion failed with exit code: {}".format(
                result.returncode))
            return 1
            
    except Exception as e:
        print("❌ Error running conversion: {}".format(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
