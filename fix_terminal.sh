#!/bin/bash

# Fix terminal control character issues in Git Bash
export TERM=cygwin
export TERMINFO=/usr/share/terminfo

# Disable problematic terminal features
stty sane 2>/dev/null || true
stty -icanon 2>/dev/null || true
stty -echo 2>/dev/null || true

# Clear any pending input
read -t 0.1 -n 1000 || true

echo "Terminal fixed. Control characters should be disabled."
echo "You can now run commands normally."
