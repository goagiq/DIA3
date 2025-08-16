#!/bin/bash

echo "Fixing PATH and terminal issues..."

# Fix terminal control characters
export TERM=cygwin
export TERMINFO=/usr/share/terminfo

# Reset terminal settings
stty sane 2>/dev/null || true
stty -icanon 2>/dev/null || true
stty -echo 2>/dev/null || true

# Clear any pending input
read -t 0.1 -n 1000 || true

# Fix PATH for Git Bash on Windows
export PATH="/mingw64/bin:/usr/bin:/usr/local/bin:$PATH"

# Add Python paths
export PATH="/c/Python313/Scripts:/c/Python313:$PATH"

# Add common Windows paths
export PATH="/c/Windows/System32:/c/Windows:$PATH"

# Add user-specific paths
export PATH="/c/Users/sovan/AppData/Local/Programs:$PATH"
export PATH="/c/Users/sovan/.local/bin:$PATH"

# Add Git paths
export PATH="/c/Program Files/Git/bin:$PATH"
export PATH="/c/Program Files/Git/cmd:$PATH"

# Add Node.js paths
export PATH="/c/Program Files/nodejs:$PATH"

# Add other common tools
export PATH="/c/Program Files/CMake/bin:$PATH"
export PATH="/c/Program Files/Docker/Docker/resources/bin:$PATH"

echo "PATH fixed. Current PATH:"
echo "$PATH" | tr ':' '\n' | head -20

echo ""
echo "Testing basic commands..."

# Test basic commands
if command -v python &> /dev/null; then
    echo "✅ Python found: $(python --version 2>&1)"
else
    echo "❌ Python not found in PATH"
fi

if command -v pip &> /dev/null; then
    echo "✅ pip found: $(pip --version 2>&1)"
else
    echo "❌ pip not found in PATH"
fi

if command -v git &> /dev/null; then
    echo "✅ git found: $(git --version 2>&1)"
else
    echo "❌ git not found in PATH"
fi

echo ""
echo "Terminal and PATH fixes applied. Try running commands now."

