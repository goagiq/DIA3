# Running the DIA3 Application

This guide explains how to run the DIA3 application and avoid common issues like missing dependencies or virtual environment problems.

## Quick Start

### Option 1: Automatic Startup (Recommended)

**Windows:**
```bash
start_app.bat
```

**Unix/Linux/Mac:**
```bash
./start_app.sh
```

**Cross-platform:**
```bash
python start_app.py
```

These scripts automatically:
- Check if the virtual environment exists
- Activate the virtual environment
- Verify all dependencies are installed
- Start the application

### Option 2: Manual Virtual Environment Activation

**Windows:**
```bash
.venv\Scripts\activate
python main.py
```

**Unix/Linux/Mac:**
```bash
source .venv/bin/activate
python main.py
```

### Option 3: Direct Virtual Environment Python

**Windows:**
```bash
.venv\Scripts\python.exe main.py
```

**Unix/Linux/Mac:**
```bash
.venv/bin/python main.py
```

## Common Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'loguru'"

**Cause:** Running the application without activating the virtual environment.

**Solution:** Use one of the startup methods above, or manually activate the virtual environment.

### Issue: "Virtual environment not found"

**Cause:** The `.venv` directory doesn't exist or is corrupted.

**Solution:** Recreate the virtual environment:
```bash
# Remove old environment
rm -rf .venv  # Unix/Linux/Mac
# or
rmdir /s .venv  # Windows

# Create new environment
python -m venv .venv

# Activate and install dependencies
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Unix/Linux/Mac

pip install -r requirements_core.txt
```

### Issue: "Permission denied" on startup scripts

**Unix/Linux/Mac only:**
```bash
chmod +x start_app.sh
```

### Issue: Application hangs or doesn't start

**Cause:** The application is designed to run continuously and start multiple services.

**Solution:** This is normal behavior. The application starts:
- FastAPI server on port 8003
- Streamlit UI on port 8501
- Landing page on port 8502
- MCP servers on various ports

Wait for the startup messages to complete. You should see:
```
🎉 All services are now running!
🌐 Access URLs:
   📊 Main UI:        http://localhost:8501
   🏠 Landing Page:   http://localhost:8502
   🔗 API Docs:       http://localhost:8003/docs
```

## Environment Checker

The application includes an automatic environment checker that:

1. **Verifies Virtual Environment:** Ensures you're using the project's virtual environment
2. **Checks Dependencies:** Verifies all required packages are installed
3. **Auto-Installation:** Attempts to install missing packages automatically
4. **Clear Instructions:** Provides step-by-step guidance if issues are found

To run the environment checker manually:
```bash
python src/core/environment_checker.py
```

## Development Mode

For development, you can skip the environment check:
```bash
python start_app.py --no-venv
```

## Troubleshooting

### Check if services are running:
```bash
# Check if ports are in use
netstat -an | grep 8003  # FastAPI
netstat -an | grep 8501  # Streamlit UI
```

### Stop the application:
- Press `Ctrl+C` in the terminal where it's running
- Or use `taskkill //F //IM python.exe` (Windows)

### View logs:
- Check the `logs/` directory for detailed application logs
- Use `tail -f logs/app.log` to follow logs in real-time

## System Requirements

- Python 3.8 or higher
- Virtual environment support
- Internet connection (for package installation)
- Sufficient disk space for dependencies (~2GB)

## Port Usage

The application uses these ports:
- **8003:** FastAPI server and API documentation
- **8501:** Main Streamlit UI
- **8502:** Landing page
- **8000:** Standalone MCP server
- **Various:** Additional MCP and service ports

Make sure these ports are available on your system.

