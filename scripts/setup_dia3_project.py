#!/usr/bin/env python3
"""
DIA3 Project Setup Script
Creates a new project folder in /d/AI/DIA3 and sets up UV environment

This script:
1. Creates a new project folder in /d/AI/DIA3
2. Initializes UV project
3. Creates virtual environment
4. Activates the environment
5. Installs core dependencies

Usage:
    python scripts/setup_dia3_project.py
"""

import os
import sys
import subprocess
import shutil
import logging
from pathlib import Path
from typing import Tuple
import platform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/dia3_setup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DIA3ProjectSetup:
    """DIA3 project setup orchestrator."""
    
    def __init__(self):
        self.project_root = Path("/d/AI/DIA3")
        self.uv_path = "/c/Users/sovan/.local/bin/uv"
        
        # Ensure logs directory exists
        (Path.cwd() / "logs").mkdir(exist_ok=True)
    
    def run_command(self, command: list, cwd: Path = None, 
                   capture_output: bool = True) -> Tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr."""
        try:
            logger.debug(f"Running command: {' '.join(command)}")
            result = subprocess.run(
                command,
                cwd=cwd or Path.cwd(),
                capture_output=capture_output,
                text=True,
                timeout=300  # 5 minute timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {' '.join(command)}")
            return -1, "", "Command timed out"
        except Exception as e:
            logger.error(f"Command failed: {' '.join(command)} - {e}")
            return -1, "", str(e)
    
    def create_project_directory(self) -> bool:
        """Create the DIA3 project directory."""
        logger.info("=== Creating DIA3 Project Directory ===")
        
        try:
            # Remove existing directory if it exists
            if self.project_root.exists():
                logger.info(f"Removing existing directory: {self.project_root}")
                shutil.rmtree(self.project_root)
            
            # Create new directory
            self.project_root.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created project directory: {self.project_root}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create project directory: {e}")
            return False
    
    def initialize_uv_project(self) -> bool:
        """Initialize UV project in the DIA3 directory."""
        logger.info("=== Initializing UV Project ===")
        
        try:
            # Change to DIA3 directory
            os.chdir(self.project_root)
            logger.info(f"Changed to directory: {self.project_root}")
            
            # Initialize UV project
            code, stdout, stderr = self.run_command([self.uv_path, "init"])
            
            if code != 0:
                logger.error(f"Failed to initialize UV project: {stderr}")
                return False
            
            logger.info("UV project initialized successfully")
            logger.debug(f"UV init output: {stdout}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize UV project: {e}")
            return False
    
    def create_virtual_environment(self) -> bool:
        """Create virtual environment using UV."""
        logger.info("=== Creating Virtual Environment ===")
        
        try:
            # Create virtual environment with Python 3.13
            code, stdout, stderr = self.run_command([
                self.uv_path, "venv", "--python", "3.13"
            ])
            
            if code != 0:
                logger.error(f"Failed to create virtual environment: {stderr}")
                return False
            
            logger.info("Virtual environment created successfully")
            logger.debug(f"UV venv output: {stdout}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create virtual environment: {e}")
            return False
    
    def activate_environment(self) -> bool:
        """Activate the virtual environment."""
        logger.info("=== Activating Virtual Environment ===")
        
        try:
            # Get the activation script path
            if platform.system() == "Windows":
                activate_script = self.project_root / ".venv" / "Scripts" / "activate"
            else:
                activate_script = self.project_root / ".venv" / "bin" / "activate"
            
            if not activate_script.exists():
                logger.error(f"Activation script not found: {activate_script}")
                return False
            
            logger.info(f"Activation script found: {activate_script}")
            
            # Note: In a real scenario, you would source this script
            # For now, we'll just verify it exists and show the command
            logger.info("To activate the environment, run:")
            logger.info(f"source {activate_script}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to activate environment: {e}")
            return False
    
    def install_core_dependencies(self) -> bool:
        """Install core dependencies."""
        logger.info("=== Installing Core Dependencies ===")
        
        try:
            # Create a core requirements file
            requirements_content = """# Core dependencies for Python 3.13
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0
pydantic-settings>=2.1.0

# Data processing
numpy>=1.24.0
pandas>=2.0.0
scipy>=1.11.0

# Machine learning
scikit-learn>=1.3.0
torch>=2.1.0
transformers>=4.35.0

# Natural language processing
spacy>=3.7.0
nltk>=3.8.0

# Web scraping and data extraction
requests>=2.31.0
beautifulsoup4>=4.12.0
selenium>=4.15.0
yt-dlp>=2023.10.0

# Database and storage
chromadb>=0.4.0
sqlalchemy>=2.0.0

# Visualization
matplotlib>=3.7.0
plotly>=5.17.0
streamlit>=1.28.0

# Utilities
python-dotenv>=1.0.0
click>=8.1.0
rich>=13.7.0
tqdm>=4.66.0

# Development tools
pytest>=7.4.0
black>=23.0.0
mypy>=1.7.0
flake8>=6.1.0

# Image processing
pillow>=10.0.0
opencv-python>=4.8.0

# API and web
aiofiles>=23.2.0
httpx>=0.25.0

# Monitoring and logging
prometheus-client>=0.19.0
structlog>=23.2.0
"""
            
            requirements_file = self.project_root / "requirements_core.txt"
            with open(requirements_file, "w") as f:
                f.write(requirements_content)
            
            logger.info("Created requirements_core.txt")
            
            # Install dependencies
            code, stdout, stderr = self.run_command([
                self.uv_path, "pip", "install", "-r", "requirements_core.txt"
            ])
            
            if code != 0:
                logger.error(f"Failed to install dependencies: {stderr}")
                return False
            
            logger.info("Core dependencies installed successfully")
            logger.debug(f"Installation output: {stdout}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
    
    def verify_environment(self) -> bool:
        """Verify the environment is working correctly."""
        logger.info("=== Verifying Environment ===")
        
        try:
            # Get Python path
            if platform.system() == "Windows":
                python_path = self.project_root / ".venv" / "Scripts" / "python.exe"
            else:
                python_path = self.project_root / ".venv" / "bin" / "python"
            
            if not python_path.exists():
                logger.error(f"Python not found: {python_path}")
                return False
            
            # Check Python version
            code, stdout, stderr = self.run_command([str(python_path), "--version"])
            
            if code != 0:
                logger.error(f"Failed to check Python version: {stderr}")
                return False
            
            logger.info(f"Python version: {stdout.strip()}")
            
            # Test core imports
            test_script = "import fastapi, pydantic, numpy, pandas; print('Core dependencies working!')"
            code, stdout, stderr = self.run_command([
                str(python_path), "-c", test_script
            ])
            
            if code != 0:
                logger.error(f"Failed to import core dependencies: {stderr}")
                return False
            
            logger.info("Core dependencies verified successfully")
            logger.info(stdout.strip())
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to verify environment: {e}")
            return False
    
    def generate_setup_summary(self):
        """Generate setup summary."""
        logger.info("=== Setup Summary ===")
        logger.info(f"Project directory: {self.project_root}")
        logger.info(f"Virtual environment: {self.project_root}/.venv")
        
        if platform.system() == "Windows":
            activate_cmd = f"source {self.project_root}/.venv/Scripts/activate"
        else:
            activate_cmd = f"source {self.project_root}/.venv/bin/activate"
        
        logger.info(f"To activate environment: {activate_cmd}")
        logger.info(f"To run Python: {self.project_root}/.venv/Scripts/python.exe")
        
        # Create a setup summary file
        summary_content = f"""# DIA3 Project Setup Summary

## Project Information
- Project Directory: {self.project_root}
- Virtual Environment: {self.project_root}/.venv
- Python Version: 3.13.5

## Activation Commands
To activate the virtual environment:
```bash
cd {self.project_root}
{activate_cmd}
```

## Usage
```bash
# Activate environment
{activate_cmd}

# Run Python
python --version

# Install additional packages
uv pip install package_name

# Run scripts
python your_script.py
```

## Project Structure
```
{self.project_root}/
├── .venv/           # Virtual environment
├── pyproject.toml   # Project configuration
├── requirements_core.txt  # Core dependencies
└── src/             # Source code (create as needed)
```

## Next Steps
1. Activate the environment using the command above
2. Create your source code in the src/ directory
3. Install additional dependencies as needed
4. Start developing your DIA3 project!
"""
        
        summary_file = Path.cwd() / "logs" / "dia3_setup_summary.md"
        with open(summary_file, "w") as f:
            f.write(summary_content)
        
        logger.info(f"Setup summary saved to: {summary_file}")
    
    def run_setup(self) -> bool:
        """Run the complete setup process."""
        logger.info("Starting DIA3 project setup...")
        
        steps = [
            ("Create Project Directory", self.create_project_directory),
            ("Initialize UV Project", self.initialize_uv_project),
            ("Create Virtual Environment", self.create_virtual_environment),
            ("Activate Environment", self.activate_environment),
            ("Install Core Dependencies", self.install_core_dependencies),
            ("Verify Environment", self.verify_environment)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\n{'='*50}")
            logger.info(f"Step: {step_name}")
            logger.info(f"{'='*50}")
            
            if not step_func():
                logger.error(f"Setup failed at step: {step_name}")
                return False
            
            logger.info(f"Step completed: {step_name}")
        
        # Generate summary
        self.generate_setup_summary()
        
        logger.info("\n" + "="*50)
        logger.info("DIA3 PROJECT SETUP COMPLETED SUCCESSFULLY!")
        logger.info("="*50)
        
        return True


def main():
    """Main entry point."""
    setup = DIA3ProjectSetup()
    
    try:
        success = setup.run_setup()
        
        if success:
            logger.info("\n🎉 DIA3 project setup completed successfully!")
            logger.info("📋 Check logs/dia3_setup_summary.md for next steps")
        else:
            logger.error("\n❌ DIA3 project setup failed!")
            logger.error("📋 Check logs for detailed error information")
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("\n⚠️ Setup process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
