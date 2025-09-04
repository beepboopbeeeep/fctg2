@echo off
title ShazamIO Telegram Bot

echo 🎵 Starting ShazamIO Telegram Bot...
echo.

REM Check if virtual environment exists
if not exist "bot_env" (
    echo ❌ Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call bot_env\Scripts\activate.bat

REM Check if bot.py exists
if not exist "bot.py" (
    echo ❌ bot.py not found. Please make sure all files are in place.
    pause
    exit /b 1
)

echo ✅ Starting the bot...
python bot.py

pause