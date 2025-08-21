#!/bin/bash

# Startup script for vocab_ai monorepo
# Opens terminals using native macOS Terminal app and then opens Cursor

set -e

echo "🚀 Starting vocab_ai development environment..."

# Get the current directory
PROJECT_DIR=$(pwd)

# Function to open terminal tab and run commands
open_terminal_tab() {
    local tab_name="$1"
    local commands="$2"
    
    echo "Opening $tab_name terminal tab..."
    
    osascript -e "
        tell application \"Terminal\"
            activate
            tell application \"System Events\" to keystroke \"t\" using {command down}
            delay 1
            do script \"echo 'Starting $tab_name...' && cd '$PROJECT_DIR' && $commands\" in front window
        end tell
    "
}

# Open Cursor in the background
echo "📱 Opening Cursor..."
open -a "Cursor" . &

# Wait a moment for Cursor to start
sleep 2

# Start agent terminal
echo "📱 Starting agent terminal..."
open_terminal_tab "Agent" "cd agent && uv sync && uv run python src/agent.py console"

# Small delay between terminal creation
sleep 2

# Start app terminal  
echo "🌐 Starting app terminal..."
open_terminal_tab "App" "cd app && npm install && npm run dev"

echo "✅ Development environment started!"
echo "   - Cursor: Opened with project"
echo "   - Agent terminal: Running in Terminal app"
echo "   - App terminal: Running in Terminal app"
echo ""
echo "💡 You now have:"
echo "   • Cursor open for editing"
echo "   • Terminal tabs running your services"