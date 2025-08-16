# DIA3 Project

A new Python 3.13 project created with UV package manager.

## Project Setup

This project was created using the following commands:

```bash
# Create project directory
mkdir -p /d/AI/DIA3
cd /d/AI/DIA3

# Initialize UV project
uv init

# Create virtual environment with Python 3.13
uv venv --python 3.13

# Activate the environment
source .venv/Scripts/activate
```

## Environment Information

- **Python Version**: 3.13.5
- **Package Manager**: UV
- **Virtual Environment**: `.venv/`
- **Project Location**: `/d/AI/DIA3`

## Usage

### Activating the Environment

```bash
cd /d/AI/DIA3
source .venv/Scripts/activate
```

### Installing Dependencies

```bash
# Install packages
uv pip install package_name

# Install from requirements file
uv pip install -r requirements.txt

# Sync with pyproject.toml
uv sync
```

### Running the Project

**Quick Start (Recommended):**
```bash
# Windows
start_app.bat

# Unix/Linux/Mac
./start_app.sh

# Cross-platform
python start_app.py
```

**Manual Method:**
```bash
# Activate virtual environment first
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
python main.py
```

**For more detailed instructions, see:**
- [Running the Application Guide](docs/RUNNING_THE_APPLICATION.md)

**Run tests:**
```bash
uv run pytest
```

## Project Structure

```
DIA3/
├── .venv/           # Virtual environment
├── .git/            # Git repository
├── .gitignore       # Git ignore file
├── .python-version  # Python version specification
├── main.py          # Main entry point
├── pyproject.toml   # Project configuration
└── README.md        # This file
```

## Next Steps

1. Add your source code to the project
2. Install required dependencies
3. Configure your development environment
4. Start building your application!

## Development

This project uses modern Python development practices:

- **UV** for fast dependency management
- **Python 3.13** for latest features
- **Virtual environment** for isolation
- **pyproject.toml** for project configuration

## Commands Reference

```bash
# Initialize new UV project
uv init

# Create virtual environment
uv venv --python 3.13

# Activate environment
source .venv/Scripts/activate

# Install package
uv pip install package_name

# Run command in environment
uv run python script.py

# Sync dependencies
uv sync

# Add dependency to pyproject.toml
uv add package_name
```
