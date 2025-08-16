#!/usr/bin/env python3
"""
Environment checker for DIA3 application.
Verifies virtual environment activation and required dependencies.
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path
from typing import List, Tuple


class EnvironmentChecker:
    """Checks and validates the application environment."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.venv_path = self.project_root / ".venv"
        self.requirements_files = [
            self.project_root / "requirements_core.txt",
            self.project_root / "requirements.prod.txt"
        ]
    
    def check_virtual_environment(self) -> Tuple[bool, str]:
        """Check if running within the correct virtual environment."""
        # Check if we're in a virtual environment
        if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            return False, "Not running in a virtual environment"
        
        # Check if we're in the project's virtual environment
        if os.name == 'nt':
            expected_python = self.venv_path / "Scripts" / "python.exe"
        else:
            expected_python = self.venv_path / "bin" / "python"
        
        if not expected_python.exists():
            return False, f"Virtual environment not found at {self.venv_path}"
        
        if str(expected_python) not in sys.executable:
            return False, (f"Not using project virtual environment. "
                          f"Expected: {expected_python}, Using: {sys.executable}")
        
        return True, "Virtual environment OK"
    
    def check_required_packages(self) -> Tuple[bool, List[str]]:
        """Check if all required packages are installed."""
        required_packages = [
            'loguru',
            'fastapi',
            'uvicorn',
            'streamlit',
            'chromadb',
            'pydantic',
            'requests',
            'numpy',
            'pandas'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                importlib.import_module(package)
            except ImportError:
                missing_packages.append(package)
        
        return len(missing_packages) == 0, missing_packages
    
    def get_activation_instructions(self) -> str:
        """Get instructions for activating the virtual environment."""
        if os.name == 'nt':  # Windows
            return f"""
To activate the virtual environment:

1. Open Command Prompt or PowerShell
2. Navigate to the project directory: cd {self.project_root}
3. Activate the virtual environment: .venv\\Scripts\\activate
4. Run the application: python main.py

Or use the virtual environment's Python directly:
   .venv\\Scripts\\python.exe main.py
"""
        else:  # Unix/Linux/Mac
            return f"""
To activate the virtual environment:

1. Open terminal
2. Navigate to the project directory: cd {self.project_root}
3. Activate the virtual environment: source .venv/bin/activate
4. Run the application: python main.py

Or use the virtual environment's Python directly:
   .venv/bin/python main.py
"""
    
    def install_missing_packages(self, packages: List[str]) -> bool:
        """Install missing packages using pip."""
        try:
            pip_cmd = [sys.executable, "-m", "pip", "install"] + packages
            subprocess.run(pip_cmd, capture_output=True, text=True, check=True)
            print(f"✅ Successfully installed packages: {', '.join(packages)}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    def run_full_check(self) -> bool:
        """Run complete environment check and provide guidance."""
        print("🔍 Checking application environment...")
        print("=" * 50)
        
        # Check virtual environment
        venv_ok, venv_message = self.check_virtual_environment()
        if not venv_ok:
            print(f"❌ Virtual Environment Issue: {venv_message}")
            print(self.get_activation_instructions())
            return False
        
        print(f"✅ {venv_message}")
        
        # Check required packages
        packages_ok, missing_packages = self.check_required_packages()
        if not packages_ok:
            print(f"❌ Missing required packages: {', '.join(missing_packages)}")
            
            # Try to install missing packages
            print("🔧 Attempting to install missing packages...")
            if self.install_missing_packages(missing_packages):
                # Re-check after installation
                packages_ok, missing_packages = self.check_required_packages()
                if packages_ok:
                    print("✅ All packages installed successfully")
                else:
                    print(f"❌ Still missing packages: {', '.join(missing_packages)}")
                    return False
            else:
                print("❌ Failed to install packages automatically")
                print("Please install manually using:")
                print(f"   {sys.executable} -m pip install {' '.join(missing_packages)}")
                return False
        else:
            print("✅ All required packages are installed")
        
        print("=" * 50)
        print("✅ Environment check passed! Application can start.")
        return True


def check_environment() -> bool:
    """Convenience function to run environment check."""
    checker = EnvironmentChecker()
    return checker.run_full_check()


if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1)
