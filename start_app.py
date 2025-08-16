#!/usr/bin/env python3
"""
Startup script for DIA3 application.
Automatically handles virtual environment activation and dependency checks.
"""

import os
import sys
import subprocess
from pathlib import Path


def get_venv_python():
    """Get the Python executable from the virtual environment."""
    project_root = Path(__file__).parent
    if os.name == 'nt':  # Windows
        return project_root / ".venv" / "Scripts" / "python.exe"
    else:  # Unix/Linux/Mac
        return project_root / ".venv" / "bin" / "python"


def run_with_venv():
    """Run the application using the virtual environment's Python."""
    venv_python = get_venv_python()
    
    if not venv_python.exists():
        print("❌ Virtual environment not found!")
        print(f"Expected location: {venv_python}")
        print("\nTo create the virtual environment:")
        print("1. python -m venv .venv")
        print("2. .venv\\Scripts\\activate  # Windows")
        print("   source .venv/bin/activate  # Unix/Linux/Mac")
        print("3. pip install -r requirements_core.txt")
        return False
    
    # Check if we're already using the virtual environment
    if str(venv_python) in sys.executable:
        print("✅ Already using virtual environment")
        return True
    
    # Run the environment checker first
    print("🔍 Running environment check...")
    try:
        result = subprocess.run([
            str(venv_python), 
            "src/core/environment_checker.py"
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Environment check failed:")
        print(e.stdout)
        print(e.stderr)
        return False


def main():
    """Main startup function."""
    print("🚀 Starting DIA3 Application...")
    print("=" * 50)
    
    # Check if we should run with virtual environment
    if len(sys.argv) > 1 and sys.argv[1] == "--no-venv":
        print("⚠️ Skipping virtual environment check (--no-venv flag)")
        # Run main.py directly
        subprocess.run([sys.executable, "main.py"] + sys.argv[2:])
        return
    
    # Try to run with virtual environment
    if run_with_venv():
        venv_python = get_venv_python()
        print(f"✅ Using virtual environment: {venv_python}")
        print("🚀 Starting main application...")
        print("=" * 50)
        
        # Run main.py with the virtual environment's Python
        try:
            subprocess.run([str(venv_python), "main.py"] + sys.argv[1:])
        except KeyboardInterrupt:
            print("\n🛑 Application stopped by user")
    else:
        print("❌ Failed to start application")
        sys.exit(1)


if __name__ == "__main__":
    main()
