#!/usr/bin/env python3
"""
Install Additional Dependencies for Python 3.13
Installs essential packages compatible with Python 3.13 for sentiment analysis
"""

import subprocess
import sys

def run_command(command, cwd=None):
    """Run a command and return success status."""
    try:
        print(f"Running: {' '.join(command)}")
        result = subprocess.run(
            command, cwd=cwd, capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"✅ Success: {' '.join(command)}")
            return True
        else:
            print(f"❌ Failed: {' '.join(command)}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    """Install additional dependencies for Python 3.13."""
    print("=== Installing Additional Dependencies for Python 3.13 ===")
    
    # Python 3.13 executable
    python313 = "DIA3/Scripts/python.exe"
    
    # Essential packages that are likely compatible with Python 3.13
    essential_packages = [
        # Core ML and data science
        "scikit-learn>=1.4.0",
        "scipy>=1.12.0",
        
        # Visualization
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0",
        "plotly>=5.18.0",
        
        # Web framework and tools
        "uvicorn[standard]>=0.27.0",
        "websockets>=12.0",
        "aiohttp>=3.9.0",
        
        # Data processing
        "beautifulsoup4>=4.12.0",
        "python-multipart>=0.0.6",
        
        # Configuration and utilities
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "click>=8.1.0",
        "typer>=0.9.0",
        
        # Monitoring
        "psutil>=5.9.0",
        "prometheus-client>=0.19.0",
        
        # File processing
        "PyPDF2>=3.0.0",
        "pillow>=10.0.0",
        
        # Video processing (without problematic dependencies)
        "yt-dlp>=2024.0.0",
        
        # Security
        "slowapi>=0.1.9",
        "passlib[bcrypt]>=1.7.4",
        
        # Testing
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
    ]
    
    # Install packages one by one to handle failures gracefully
    successful_installs = []
    failed_installs = []
    
    for package in essential_packages:
        if run_command([python313, "-m", "pip", "install", package]):
            successful_installs.append(package)
        else:
            failed_installs.append(package)
    
    # Print summary
    print("\n=== Installation Summary ===")
    print(f"✅ Successfully installed: {len(successful_installs)} packages")
    print(f"❌ Failed to install: {len(failed_installs)} packages")
    
    if successful_installs:
        print("\nSuccessfully installed packages:")
        for pkg in successful_installs:
            print(f"  - {pkg}")
    
    if failed_installs:
        print("\nFailed to install packages:")
        for pkg in failed_installs:
            print(f"  - {pkg}")
    
    # Test key imports
    print("\n=== Testing Key Imports ===")
    test_imports = [
        "import numpy",
        "import pandas", 
        "import fastapi",
        "import pydantic",
        "import requests",
        "import matplotlib",
        "import scikit-learn",
        "import pytest"
    ]
    
    for import_stmt in test_imports:
        if run_command([python313, "-c", import_stmt]):
            print(f"✅ {import_stmt}")
        else:
            print(f"❌ {import_stmt}")
    
    print("\n=== Installation Complete ===")
    print("You can now use DIA3/Scripts/python.exe for Python 3.13 development!")
    
    return len(failed_installs) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
