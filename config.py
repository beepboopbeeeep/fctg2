import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Telegram Bot Token
    BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    
    # File size limit for music recognition (20MB)
    FILE_SIZE_LIMIT = 20 * 1024 * 1024
    
    # Supported languages
    LANGUAGES = {
        'en': 'English',
        'fa': 'Persian'
    }
    
    # Default language
    DEFAULT_LANGUAGE = 'en'
    
    # Temporary directory for file processing
    TEMP_DIR = 'temp'
    
    # Data directory for persistent storage
    DATA_DIR = 'data'
    
    # Enable/disable features
    ENABLE_YOUTUBE_DOWNLOAD = True
    ENABLE_INSTAGRAM_DOWNLOAD = True
    ENABLE_METADATA_EDITING = True
    
    # Logging configuration
    LOG_LEVEL = 'INFO'
    
    # Proxy settings (if needed)
    HTTP_PROXY = os.getenv("HTTP_PROXY", None)
    HTTPS_PROXY = os.getenv("HTTPS_PROXY", None)