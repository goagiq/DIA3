#!/bin/bash

# MCP Tool Manager - Unix/Linux Shell Script
# Easy management of MCP tools

echo ""
echo "========================================"
echo "    MCP Tool Manager - Unix/Linux"
echo "========================================"
echo ""

# Function to show help
show_help() {
    echo "Usage: ./mcp_manager.sh [command] [tool_name]"
    echo ""
    echo "Commands:"
    echo "  list                    - List all tools and their status"
    echo "  enable <tool_name>      - Enable a specific tool"
    echo "  disable <tool_name>     - Disable a specific tool"
    echo "  enable-all              - Enable all tools"
    echo "  disable-all             - Disable all tools"
    echo "  enable-core             - Enable core tools only"
    echo "  enable-advanced         - Enable advanced tools only"
    echo "  config <tool_name>      - Show detailed config for a tool"
    echo "  test                    - Test tool availability"
    echo "  help                    - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./mcp_manager.sh list"
    echo "  ./mcp_manager.sh enable monte_carlo"
    echo "  ./mcp_manager.sh disable sentiment_analysis"
    echo "  ./mcp_manager.sh enable-core"
    echo "  ./mcp_manager.sh test"
    echo ""
}

# Check if command is provided
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

COMMAND=$1
TOOL_NAME=$2

case $COMMAND in
    "list")
        python scripts/mcp_tool_manager.py list
        ;;
    "enable")
        if [ -z "$TOOL_NAME" ]; then
            echo "Error: Please specify a tool name"
            echo "Example: ./mcp_manager.sh enable monte_carlo"
            exit 1
        fi
        python scripts/mcp_tool_manager.py enable "$TOOL_NAME"
        ;;
    "disable")
        if [ -z "$TOOL_NAME" ]; then
            echo "Error: Please specify a tool name"
            echo "Example: ./mcp_manager.sh disable sentiment_analysis"
            exit 1
        fi
        python scripts/mcp_tool_manager.py disable "$TOOL_NAME"
        ;;
    "enable-all")
        python scripts/mcp_tool_manager.py enable-all
        ;;
    "disable-all")
        python scripts/mcp_tool_manager.py disable-all
        ;;
    "enable-core")
        python scripts/mcp_tool_manager.py enable-core
        ;;
    "enable-advanced")
        python scripts/mcp_tool_manager.py enable-advanced
        ;;
    "test")
        python scripts/mcp_tool_manager.py test
        ;;
    "config")
        if [ -z "$TOOL_NAME" ]; then
            echo "Error: Please specify a tool name"
            echo "Example: ./mcp_manager.sh config monte_carlo"
            exit 1
        fi
        python scripts/mcp_tool_manager.py config "$TOOL_NAME"
        ;;
    "help")
        show_help
        ;;
    *)
        echo "Error: Unknown command '$COMMAND'"
        show_help
        exit 1
        ;;
esac
