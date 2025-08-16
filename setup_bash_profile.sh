#!/bin/bash

echo "Setting up permanent bash configuration..."

# Create or update .bash_profile
cat >> ~/.bash_profile << 'EOF'

# Fix terminal control character issues
export TERM=cygwin
export TERMINFO=/usr/share/terminfo

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

# Disable problematic terminal features
stty sane 2>/dev/null || true
stty -icanon 2>/dev/null || true
stty -echo 2>/dev/null || true

EOF

echo "✅ .bash_profile updated with PATH and terminal fixes"
echo "Restart your terminal or run: source ~/.bash_profile"

