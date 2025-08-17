@echo off
REM MCP Tool Manager - Windows Batch Script
REM Easy management of MCP tools

echo.
echo ========================================
echo    MCP Tool Manager - Windows
echo ========================================
echo.

if "%1"=="" goto :show_help

if "%1"=="list" (
    python scripts/mcp_tool_manager.py list
    goto :end
)

if "%1"=="enable" (
    if "%2"=="" (
        echo Error: Please specify a tool name
        echo Example: mcp_manager.bat enable monte_carlo
        goto :end
    )
    python scripts/mcp_tool_manager.py enable %2
    goto :end
)

if "%1"=="disable" (
    if "%2"=="" (
        echo Error: Please specify a tool name
        echo Example: mcp_manager.bat disable sentiment_analysis
        goto :end
    )
    python scripts/mcp_tool_manager.py disable %2
    goto :end
)

if "%1"=="enable-all" (
    python scripts/mcp_tool_manager.py enable-all
    goto :end
)

if "%1"=="disable-all" (
    python scripts/mcp_tool_manager.py disable-all
    goto :end
)

if "%1"=="enable-core" (
    python scripts/mcp_tool_manager.py enable-core
    goto :end
)

if "%1"=="enable-advanced" (
    python scripts/mcp_tool_manager.py enable-advanced
    goto :end
)

if "%1"=="test" (
    python scripts/mcp_tool_manager.py test
    goto :end
)

if "%1"=="config" (
    if "%2"=="" (
        echo Error: Please specify a tool name
        echo Example: mcp_manager.bat config monte_carlo
        goto :end
    )
    python scripts/mcp_tool_manager.py config %2
    goto :end
)

if "%1"=="help" (
    goto :show_help
)

echo Error: Unknown command '%1'
goto :show_help

:show_help
echo Usage: mcp_manager.bat [command] [tool_name]
echo.
echo Commands:
echo   list                    - List all tools and their status
echo   enable ^<tool_name^>      - Enable a specific tool
echo   disable ^<tool_name^>     - Disable a specific tool
echo   enable-all              - Enable all tools
echo   disable-all             - Disable all tools
echo   enable-core             - Enable core tools only
echo   enable-advanced         - Enable advanced tools only
echo   config ^<tool_name^>      - Show detailed config for a tool
echo   test                    - Test tool availability
echo   help                    - Show this help message
echo.
echo Examples:
echo   mcp_manager.bat list
echo   mcp_manager.bat enable monte_carlo
echo   mcp_manager.bat disable sentiment_analysis
echo   mcp_manager.bat enable-core
echo   mcp_manager.bat test
echo.

:end
pause
