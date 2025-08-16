# PowerShell script to start DIA3 with proper Python environment
Write-Host "Starting DIA3 with PowerShell..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Change to project directory
Set-Location "D:\AI\DIA3"

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

# Check Python version
Write-Host "Python version:" -ForegroundColor Cyan
python --version

# Check pip version
Write-Host "pip version:" -ForegroundColor Cyan
pip --version

# Check if uv is available
Write-Host "uv version:" -ForegroundColor Cyan
uv --version

Write-Host ""
Write-Host "✅ Environment ready! You can now run commands without terminal issues." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Keep PowerShell open
Write-Host "Type 'exit' to close this session." -ForegroundColor Yellow

