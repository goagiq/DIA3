@echo off
REM Clean MCP Server Startup Script - No Warnings
REM Sets environment variables to suppress all deprecation warnings

echo 🚀 Starting Clean MCP Server (No Warnings)
echo ==================================================
echo 📊 Focus: MCP Server with Enhanced Report Generation
echo 🌐 Port: 8000
echo 🔧 Features: generate_report, process_content, analyze_content, search_content
echo 🧹 Console: Clean output with no deprecation warnings
echo ==================================================

REM Set environment variables to suppress all warnings
set PYTHONWARNINGS=ignore
set PYTHONDONTWRITEBYTECODE=1

REM Start the server with clean environment
D:\AI\DIA3\.venv\Scripts\python.exe start_mcp_server_clean.py

pause
