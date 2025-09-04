@echo off
TITLE SongID Bot Runner
echo ==========================================
echo        SongID Bot Setup and Run
echo ==========================================

echo.
echo Checking if Python is installed...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.9 or later and try again.
    pause
    exit /b
)

echo Checking if pip is installed...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed or not in PATH.
    echo Please install pip and try again.
    pause
    exit /b
)

echo.
echo Installing pyacrcloud from GitHub...
pip install git+https://github.com/acrcloud/acrcloud_sdk_python.git
if %errorlevel% neq 0 (
    echo Failed to install pyacrcloud from GitHub.
    echo Trying alternative installation method...
    pip install https://github.com/acrcloud/acrcloud_sdk_python/archive/master.zip
    if %errorlevel% neq 0 (
        echo Failed to install pyacrcloud.
        echo Please manually download and install it from https://github.com/acrcloud/acrcloud_sdk_python
        pause
        exit /b
    )
)

echo.
echo Installing other required dependencies...
pip install python-telegram-bot==13.7
if %errorlevel% neq 0 (
    echo Failed to install python-telegram-bot.
    pause
    exit /b
)

echo.
echo Installing sentry-sdk...
pip install sentry-sdk==2.8.0
if %errorlevel% neq 0 (
    echo Failed to install sentry-sdk.
    pause
    exit /b
)

echo.
echo Checking if python-dotenv is installed...
pip show python-dotenv >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing python-dotenv for environment variable support...
    pip install python-dotenv
)

echo.
echo Creating .env file if it doesn't exist...
if not exist .env (
    echo # SongID Bot Environment Variables > .env
    echo # Telegram Configuration >> .env
    echo SONGID_TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here >> .env
    echo SONGID_TELEGRAM_DEV_ID=your_telegram_user_id_here >> .env
    echo SONGID_TELEGRAM_DEV_USERNAME=your_telegram_username_here >> .env
    echo. >> .env
    echo # Logging Configuration >> .env
    echo SONGID_LOG_LEVEL=INFO >> .env
    echo SONGID_ENVIRONMENT=production >> .env
    echo. >> .env
    echo # Sentry Configuration ^(optional^) >> .env
    echo SONGID_SENTRY_DSN= >> .env
    echo. >> .env
    echo # ACRCloud Configuration ^(Clear Audio Recognition - Currently Unused^) >> .env
    echo SONGID_ACR_CLEAR_HOST= >> .env
    echo SONGID_ACR_CLEAR_ACCESS_KEY= >> .env
    echo SONGID_ACR_CLEAR_ACCESS_SECRET= >> .env
    echo SONGID_ACR_CLEAR_RECOGNIZE_TYPE= >> .env
    echo SONGID_ACR_CLEAR_TIMEOUT=10 >> .env
    echo. >> .env
    echo # ACRCloud Configuration ^(Noisy Audio Recognition^) >> .env
    echo SONGID_ACR_NOISY_HOST=identify-eu-west-1.acrcloud.com >> .env
    echo SONGID_ACR_NOISY_ACCESS_KEY=your_acrcloud_access_key_here >> .env
    echo SONGID_ACR_NOISY_ACCESS_SECRET=your_acrcloud_secret_here >> .env
    echo SONGID_ACR_NOISY_RECOGNIZE_TYPE= >> .env
    echo SONGID_ACR_NOISY_TIMEOUT=30 >> .env
    echo. >> .env
    echo # ACRCloud Configuration ^(Humming Recognition^) >> .env
    echo SONGID_ACR_HUM_HOST=identify-eu-west-1.acrcloud.com >> .env
    echo SONGID_ACR_HUM_ACCESS_KEY=your_acrcloud_access_key_here >> .env
    echo SONGID_ACR_HUM_ACCESS_SECRET=your_acrcloud_secret_here >> .env
    echo SONGID_ACR_HUM_RECOGNIZE_TYPE= >> .env
    echo SONGID_ACR_HUM_TIMEOUT=30 >> .env
    echo. >> .env
    echo Created .env file. Please edit it with your actual credentials.
    echo.
)

echo.
echo Creating downloads directory if it doesn't exist...
if not exist app\downloads (
    mkdir app\downloads
)

echo.
echo Creating data directory if it doesn't exist...
if not exist app\data (
    mkdir app\data
)

echo.
echo Checking if userdata.json exists...
if not exist app\data\userdata.json (
    echo {"0000000": {"username": "JohnD", "name": "John Doe", "api_calls": "0", "last_call": "0"}, "0000001": {"username": "JohnS", "name": "John Smith", "api_calls": "0", "last_call": "0"}} > app\data\userdata.json
    echo Created sample userdata.json file.
)

echo.
echo Setup complete! 
echo.
echo Before running the bot, please:
echo 1. Edit the .env file with your actual credentials
echo 2. Make sure Docker is installed if you want to run with Docker
echo.
echo Press any key to run the bot...
pause >nul

echo.
echo Starting the SongID bot...
cd app
python SongID.py

pause