#!/bin/bash

# ShazamIO Telegram Bot Setup Script
# This script helps set up and run the Telegram bot

echo "🎵 Setting up ShazamIO Telegram Bot..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.13 and try again."
    exit 1
fi

echo "✅ Python 3 is installed"

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv bot_env
echo "✅ Virtual environment created"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source bot_env/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip
echo "✅ Pip upgraded"

# Install required packages
echo "🔧 Installing required packages..."
pip install -r requirements.txt
echo "✅ Required packages installed"

# Get bot token from user
echo "🔑 Please enter your Telegram Bot Token (get it from @BotFather on Telegram):"
read BOT_TOKEN

# Replace placeholder in bot.py
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/YOUR_BOT_TOKEN_HERE/$BOT_TOKEN/g" bot.py
else
    # Linux and others
    sed -i "s/YOUR_BOT_TOKEN_HERE/$BOT_TOKEN/g" bot.py
fi

echo "✅ Bot token updated in bot.py"

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🚀 To run the bot, execute the following command:"
echo "   source bot_env/bin/activate && python bot.py"
echo ""
echo "📝 To run the bot in the future, you can use the start.sh script:"
echo "   ./start.sh"