#!/bin/bash

# SongID Bot Runner
# For Linux and macOS systems

echo "=========================================="
echo "       SongID Bot Setup and Run"
echo "=========================================="

echo ""
echo "Checking if Python is installed..."
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed"
    exit 1
fi

echo "Checking if pip is installed..."
if ! command -v pip3 &> /dev/null
then
    echo "pip3 is not installed"
    exit 1
fi

echo ""
echo "Installing pyacrcloud from GitHub..."
pip3 install git+https://github.com/acrcloud/acrcloud_sdk_python.git
if [ $? -ne 0 ]; then
    echo "Failed to install pyacrcloud from GitHub."
    echo "Trying alternative installation method..."
    pip3 install https://github.com/acrcloud/acrcloud_sdk_python/archive/master.zip
    if [ $? -ne 0 ]; then
        echo "Failed to install pyacrcloud."
        echo "Please manually download and install it from https://github.com/acrcloud/acrcloud_sdk_python"
        exit 1
    fi
fi

echo ""
echo "Installing other required dependencies..."
pip3 install python-telegram-bot==13.7
if [ $? -ne 0 ]; then
    echo "Failed to install python-telegram-bot."
    exit 1
fi

echo ""
echo "Installing sentry-sdk..."
pip3 install sentry-sdk==2.8.0
if [ $? -ne 0 ]; then
    echo "Failed to install sentry-sdk."
    exit 1
fi

echo ""
echo "Checking if python-dotenv is installed..."
if ! pip3 show python-dotenv &> /dev/null
then
    echo "Installing python-dotenv for environment variable support..."
    pip3 install python-dotenv
fi

echo ""
echo "Creating .env file if it doesn't exist..."
if [ ! -f .env ]; then
    cat > .env << EOL
# SongID Bot Environment Variables
# Telegram Configuration
SONGID_TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
SONGID_TELEGRAM_DEV_ID=your_telegram_user_id_here
SONGID_TELEGRAM_DEV_USERNAME=your_telegram_username_here

# Logging Configuration
SONGID_LOG_LEVEL=INFO
SONGID_ENVIRONMENT=production

# Sentry Configuration (optional)
SONGID_SENTRY_DSN=

# ACRCloud Configuration (Clear Audio Recognition - Currently Unused)
SONGID_ACR_CLEAR_HOST=
SONGID_ACR_CLEAR_ACCESS_KEY=
SONGID_ACR_CLEAR_ACCESS_SECRET=
SONGID_ACR_CLEAR_RECOGNIZE_TYPE=
SONGID_ACR_CLEAR_TIMEOUT=10

# ACRCloud Configuration (Noisy Audio Recognition)
SONGID_ACR_NOISY_HOST=identify-eu-west-1.acrcloud.com
SONGID_ACR_NOISY_ACCESS_KEY=your_acrcloud_access_key_here
SONGID_ACR_NOISY_ACCESS_SECRET=your_acrcloud_secret_here
SONGID_ACR_NOISY_RECOGNIZE_TYPE=
SONGID_ACR_NOISY_TIMEOUT=30

# ACRCloud Configuration (Humming Recognition)
SONGID_ACR_HUM_HOST=identify-eu-west-1.acrcloud.com
SONGID_ACR_HUM_ACCESS_KEY=your_acrcloud_access_key_here
SONGID_ACR_HUM_ACCESS_SECRET=your_acrcloud_secret_here
SONGID_ACR_HUM_RECOGNIZE_TYPE=
SONGID_ACR_HUM_TIMEOUT=30
EOL
    echo "Created .env file. Please edit it with your actual credentials."
    echo ""
fi

echo ""
echo "Creating downloads directory if it doesn't exist..."
mkdir -p app/downloads

echo ""
echo "Creating data directory if it doesn't exist..."
mkdir -p app/data

echo ""
echo "Checking if userdata.json exists..."
if [ ! -f app/data/userdata.json ]; then
    echo '{"0000000": {"username": "JohnD", "name": "John Doe", "api_calls": "0", "last_call": "0"}, "0000001": {"username": "JohnS", "name": "John Smith", "api_calls": "0", "last_call": "0"}}' > app/data/userdata.json
    echo "Created sample userdata.json file."
fi

echo ""
echo "Setup complete!"
echo ""
echo "Before running the bot, please:"
echo "1. Edit the .env file with your actual credentials"
echo "2. Make sure Docker is installed if you want to run with Docker"
echo ""
echo "Press any key to run the bot..."
read -n 1 -s

echo ""
echo "Starting the SongID bot..."
cd app
python3 SongID.py