@echo off
title ShazamIO Telegram Bot Setup

echo 🎵 Setting up ShazamIO Telegram Bot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.13 and try again.
    pause
    exit /b 1
)

echo ✅ Python is installed

REM Get Python version
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION%

REM Create virtual environment
echo 🔧 Creating virtual environment...
python -m venv bot_env
echo ✅ Virtual environment created

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call bot_env\Scripts\activate.bat
echo ✅ Virtual environment activated

REM Upgrade pip
echo 🔧 Upgrading pip...
python -m pip install --upgrade pip
echo ✅ Pip upgraded

REM Install required packages
echo 🔧 Installing required packages...
pip install -r requirements.txt
echo ✅ Required packages installed

REM Get bot token from user
echo 🔑 Please enter your Telegram Bot Token (get it from @BotFather on Telegram):
set /p BOT_TOKEN=""

REM Replace placeholder in bot.py
powershell -Command "(gc bot.py) -replace 'YOUR_BOT_TOKEN_HERE', '%BOT_TOKEN%' | Out-File -encoding ASCII bot.py"

echo ✅ Bot token updated in bot.py

echo.
echo ✅ Setup completed successfully!
echo.
echo 🚀 To run the bot, execute the following command:
echo    call bot_env\Scripts\activate.bat && python bot.py
echo.
echo 📝 To run the bot in the future, you can use the start.bat script:
echo    start.bat
echo.
pause