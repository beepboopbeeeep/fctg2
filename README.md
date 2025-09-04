# 🎵 ShazamIO Telegram Bot

A powerful Telegram bot that combines music recognition capabilities with social media content downloading.

## Features

1. **Music Recognition**:
   - Send any audio/video file (<20MB) to identify the music
   - Get detailed information about tracks (title, artist, album)

2. **Social Media Downloading**:
   - Download content from YouTube, Instagram, and other social media platforms
   - Support for various content types (videos, images, etc.)

3. **Inline Mode**:
   - Search and share music in any chat using inline mode (@your_bot_username query)

4. **Metadata Editing**:
   - Edit music file metadata (title, artist, album)

5. **Multilingual Support**:
   - English and Persian language support

## Requirements

- Python 3.13
- Telegram Bot Token (get from @BotFather on Telegram)

## Installation

### Method 1: Manual Installation

1. Clone or download this repository

2. Create a virtual environment:
   ```bash
   python -m venv bot_env
   ```

3. Activate the virtual environment:
   
   On Linux/macOS:
   ```bash
   source bot_env/bin/activate
   ```
   
   On Windows:
   ```cmd
   bot_env\Scripts\activate
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your bot token:
   ```bash
   cp env.example .env
   ```
   Then edit the `.env` file and replace `YOUR_BOT_TOKEN_HERE` with your actual bot token from @BotFather.

### Method 2: Using Setup Scripts

#### On Linux/macOS:

1. Clone or download this repository
2. Make the setup script executable:
   ```bash
   chmod +x setup.sh
   ```
3. Run the setup script:
   ```bash
   ./setup.sh
   ```
4. Follow the prompts to enter your Telegram Bot Token

#### On Windows:

1. Clone or download this repository
2. Run the setup batch file:
   ```
   setup.bat
   ```
3. Follow the prompts to enter your Telegram Bot Token

## Running the Bot

### Method 1: Direct Execution

```bash
python bot.py
```

### Method 2: Using Start Scripts

#### On Linux/macOS:

```bash
./start.sh
```

#### On Windows:

```
start.bat
```

### Method 3: Using Docker

1. Build the Docker image:
   ```bash
   docker build -t shazamio-bot .
   ```

2. Run the container:
   ```bash
   docker run -d --name shazamio-bot --env-file .env shazamio-bot
   ```

### Method 4: Using Docker Compose

1. Set up your bot token in the `.env` file

2. Run with docker-compose:
   ```bash
   docker-compose up -d
   ```

## Deploying to PythonAnywhere

1. Create an account at [PythonAnywhere](https://www.pythonanywhere.com/)

2. Navigate to the "Files" tab and upload all the bot files:
   - [bot.py](file:///c%3A/Users/M.R.co/Desktop/New%20folder%20%283%29/bot.py)
   - [requirements.txt](file:///c%3A/Users/M.R.co/Desktop/New%20folder%20%283%29/requirements.txt)
   - [.env](file:///C:/Users/M.R.co/Desktop/New%20folder%20(3)/.env)

3. Go to the "Consoles" tab and start a new bash console

4. In the console, create a virtual environment:
   ```bash
   mkvirtualenv bot_env --python=/usr/bin/python3.13
   pip install -r requirements.txt
   ```

5. Edit the [.env](file:///C:/Users/M.R.co/Desktop/New%20folder%20(3)/.env) file to add your Telegram Bot Token:
   ```bash
   nano .env
   ```
   Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token.

6. Test the bot:
   ```bash
   python bot.py
   ```

7. Go to the "Tasks" tab and add a new scheduled task:
   - Set time to `@reboot`
   - Enter command: `/home/yourusername/bot_env/bin/python /home/yourusername/bot.py`

## Usage

1. Start a chat with your bot on Telegram
2. Use `/start` to see the welcome message and features
3. Send an audio or video file to identify music
4. Send a social media link to download content
5. Use `/language` to change the bot language
6. Use `/edit_metadata` to edit music file metadata
7. In any chat, type `@your_bot_username` followed by a search query to use inline mode

## Supported Social Media Platforms

- YouTube
- Instagram
- Twitter
- Facebook
- TikTok
- And more...

## Notes

- Files larger than 20MB are not supported for music recognition
- Some social media platforms may have restrictions on downloading
- For Instagram downloading, you may need to configure Instagram credentials
- The bot requires an active internet connection to function properly

## Troubleshooting

If you encounter issues:

1. Make sure all dependencies are installed correctly:
   ```bash
   pip install -r requirements.txt
   ```

2. Check that your Telegram Bot Token is correct in the [.env](file:///C:/Users/M.R.co/Desktop/New%20folder%20(3)/.env) file

3. Ensure the bot has proper internet access

4. Check the logs for any error messages:
   ```bash
   python bot.py
   ```

## Features in Detail

### Music Recognition
Send any audio or video file (less than 20MB) to the bot, and it will identify the music using the ShazamIO library. You'll get detailed information about the track including title, artist, and album.

### Social Media Downloading
Send links from supported social media platforms to download content. The bot will automatically detect the platform and download the content in the best available quality.

### Inline Mode
Use the bot in any chat via inline mode. Simply type `@your_bot_username` followed by your search query to find and share music.

### Metadata Editing
Use the `/edit_metadata` command to edit the metadata of MP3 files. Send the file, then provide the new metadata in the format:
```
Title: New Title
Artist: New Artist
Album: New Album
```

### Multilingual Support
The bot supports both English and Persian languages. Use the `/language` command to switch between them.

## License

This project is licensed under the MIT License - see the [LICENSE](file:///c%3A/Users/M.R.co/Desktop/New%20folder%20%283%29/LICENSE) file for details.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## Support

If you have any questions or need help, feel free to open an issue on GitHub.