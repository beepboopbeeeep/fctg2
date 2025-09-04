#!/bin/bash

# ShazamIO Telegram Bot Start Script
# This script activates the virtual environment and starts the bot

echo "🎵 Starting ShazamIO Telegram Bot..."

# Check if virtual environment exists
if [ ! -d "bot_env" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source bot_env/bin/activate

# Check if bot.py exists
if [ ! -f "bot.py" ]; then
    echo "❌ bot.py not found. Please make sure all files are in place."
    exit 1
fi

echo "✅ Starting the bot..."
python bot.py