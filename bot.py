import asyncio
import logging
import os
import io
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import telebot
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from shazamio import Shazam
from shazamio.schemas.enums import ArtistView
from shazamio.schemas.artists import ArtistQuery

# For social media downloading, we'll use various libraries
# YouTube downloading
try:
    from pytube import YouTube
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False

# Instagram downloading
try:
    import instaloader
    INSTAGRAM_AVAILABLE = True
except ImportError:
    INSTAGRAM_AVAILABLE = False

# For general downloading
import requests

# For metadata editing
try:
    from mutagen.id3 import ID3, TIT2, TPE1, TALB
    from mutagen.mp3 import MP3
    METADATA_AVAILABLE = True
except ImportError:
    METADATA_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")  # Replace with your actual bot token
bot = AsyncTeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())

# User language storage (in production, use a database)
user_languages = {}

# Store file info for metadata editing
user_files = {}

# Supported languages
LANGUAGES = {
    'en': 'English',
    'fa': 'Persian'
}

# Texts in different languages
TEXTS = {
    'en': {
        'start': "🎵 Welcome to Music Recognition & Social Media Downloader Bot!\n\n"
                 "Features:\n"
                 "1. Send me any audio/video file (<20MB) to identify the music\n"
                 "2. Send me links from social media (YouTube, Instagram, etc.) to download content\n"
                 "3. Use inline mode to search and share music (@your_bot_username query)\n"
                 "4. Edit music metadata (title, artist, album)\n\n"
                 "Use /help to see all commands.",
        'help': "Available commands:\n"
                "/start - Start the bot\n"
                "/help - Show this help message\n"
                "/language - Change language\n"
                "/edit_metadata - Edit music file metadata\n\n"
                "Simply send me an audio/video file to identify music or a social media link to download content.",
        'choose_language': "Please choose your language:",
        'language_selected': "Language changed to English!",
        'send_audio': "Please send an audio or video file to identify the music.",
        'file_too_large': "File is too large. Please send a file smaller than 20MB.",
        'processing': "Processing your file... Please wait.",
        'no_match': "Sorry, I couldn't identify this track.",
        'result': "*Title:* {title}\n"
                  "*Artist:* {artist}\n"
                  "*Album:* {album}\n"
                  "*Link:* [Listen on Shazam](https://www.shazam.com/track/{track_id}/{title})",
        'send_link': "Please send a social media link to download content.",
        'downloading': "Downloading content... Please wait.",
        'download_complete': "Download complete! Here's your content:",
        'download_failed': "Failed to download content. Please check the link and try again.",
        'edit_metadata': "Please send the music file you want to edit.",
        'send_new_metadata': "Please send the new metadata in this format:\n"
                             "Title: New Title\n"
                             "Artist: New Artist\n"
                             "Album: New Album",
        'metadata_updated': "Metadata updated successfully!",
        'invalid_metadata_format': "Invalid format. Please use:\nTitle: ...\nArtist: ...\nAlbum: ...",
        'metadata_editing_started': "File received. Now send the new metadata in this format:\n"
                                    "Title: New Title\n"
                                    "Artist: New Artist\n"
                                    "Album: New Album"
    },
    'fa': {
        'start': "🎵 به ربات شناسایی موسیقی و دانلود از شبکه های اجتماعی خوش آمدید!\n\n"
                 "ویژگی ها:\n"
                 "1. هر فایل صوتی/تصویری کمتر از ۲۰ مگابایت بفرستید تا موسیقی آن شناسایی شود\n"
                 "2. لینک شبکه های اجتماعی (یوتیوب، اینستاگرام و ...) بفرستید تا محتوا دانلود شود\n"
                 "3. از حالت اینلاین برای جستجو و اشتراک گذاری موسیقی استفاده کنید (@نام_ربات کلمه_جستجو)\n"
                 "4. ویرایش اطلاعات فایل های موسیقی (عنوان، هنرمند، آلبوم)\n\n"
                 "برای مشاهده دستورات از /help استفاده کنید.",
        'help': "دستورات موجود:\n"
                "/start - شروع ربات\n"
                "/help - نمایش این پیام راهنما\n"
                "/language - تغییر زبان\n"
                "/edit_metadata - ویرایش اطلاعات فایل موسیقی\n\n"
                "فقط کافیست یک فایل صوتی/تصویری بفرستید تا موسیقی آن شناسایی شود یا یک لینک شبکه اجتماعی برای دانلود محتوا.",
        'choose_language': "لطفا زبان خود را انتخاب کنید:",
        'language_selected': "زبان به فارسی تغییر یافت!",
        'send_audio': "لطفا یک فایل صوتی یا تصویری برای شناسایی موسیقی بفرستید.",
        'file_too_large': "فایل بسیار بزرگ است. لطفا فایلی کوچکتر از ۲۰ مگابایت بفرستید.",
        'processing': "در حال پردازش فایل... لطفا صبر کنید.",
        'no_match': "متاسفانه نتوانستم این ترک را شناسایی کنم.",
        'result': "*عنوان:* {title}\n"
                  "*هنرمند:* {artist}\n"
                  "*آلبوم:* {album}\n"
                  "*لینک:* [گوش دادن در Shazam](https://www.shazam.com/track/{track_id}/{title})",
        'send_link': "لطفا یک لینک شبکه اجتماعی برای دانلود محتوا بفرستید.",
        'downloading': "در حال دانلود محتوا... لطفا صبر کنید.",
        'download_complete': "دانلود تکمیل شد! محتوای شما:",
        'download_failed': "دانلود محتوا ناموفق بود. لطفا لینک را بررسی کرده و دوباره تلاش کنید.",
        'edit_metadata': "لطفا فایل موسیقی که می خواهید اطلاعات آن را ویرایش کنید بفرستید.",
        'send_new_metadata': "لطفا اطلاعات جدید را به این فرمت بفرستید:\n"
                             "Title: عنوان جدید\n"
                             "Artist: هنرمند جدید\n"
                             "Album: آلبوم جدید",
        'metadata_updated': "اطلاعات با موفقیت به روز شد!",
        'invalid_metadata_format': "فرمت نامعتبر. لطفا از این فرمت استفاده کنید:\nTitle: ...\nArtist: ...\nAlbum: ...",
        'metadata_editing_started': "فایل دریافت شد. حالا اطلاعات جدید را به این فرمت بفرستید:\n"
                                    "Title: عنوان جدید\n"
                                    "Artist: هنرمند جدید\n"
                                    "Album: آلبوم جدید"
    }
}

def get_text(user_id, key):
    """Get text in user's language"""
    lang = user_languages.get(user_id, 'en')
    return TEXTS[lang][key]

# Bot commands
@bot.message_handler(commands=['start'])
async def start_command(message):
    """Handle /start command"""
    user_languages[message.from_user.id] = 'en'  # Default language
    await bot.reply_to(message, get_text(message.from_user.id, 'start'), parse_mode='Markdown')

@bot.message_handler(commands=['help'])
async def help_command(message):
    """Handle /help command"""
    await bot.reply_to(message, get_text(message.from_user.id, 'help'))

@bot.message_handler(commands=['language'])
async def language_command(message):
    """Handle /language command"""
    markup = types.InlineKeyboardMarkup()
    for code, name in LANGUAGES.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f'lang_{code}'))
    
    await bot.reply_to(message, get_text(message.from_user.id, 'choose_language'), reply_markup=markup)

@bot.message_handler(commands=['edit_metadata'])
async def edit_metadata_command(message):
    """Handle /edit_metadata command"""
    await bot.reply_to(message, get_text(message.from_user.id, 'edit_metadata'))

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
async def language_callback(call):
    """Handle language selection"""
    lang_code = call.data.split('_')[1]
    if lang_code in LANGUAGES:
        user_languages[call.from_user.id] = lang_code
        await bot.answer_callback_query(call.id, get_text(call.from_user.id, 'language_selected'))
        await bot.edit_message_text(
            get_text(call.from_user.id, 'start'), 
            call.message.chat.id, 
            call.message.message_id,
            parse_mode='Markdown'
        )

@bot.message_handler(content_types=['audio', 'voice', 'video', 'video_note', 'document'])
async def handle_media(message):
    """Handle audio/video files for music recognition"""
    # Check if user is in metadata editing mode
    if message.from_user.id in user_files:
        await handle_metadata_file(message)
        return
    
    # Check file size
    if message.content_type == 'document':
        file_size = message.document.file_size
    elif message.content_type == 'audio':
        file_size = message.audio.file_size
    elif message.content_type == 'voice':
        file_size = message.voice.file_size
    elif message.content_type == 'video':
        file_size = message.video.file_size
    elif message.content_type == 'video_note':
        file_size = message.video_note.file_size
    
    if file_size > 20 * 1024 * 1024:  # 20MB limit
        await bot.reply_to(message, get_text(message.from_user.id, 'file_too_large'))
        return
    
    # Notify user about processing
    processing_msg = await bot.reply_to(message, get_text(message.from_user.id, 'processing'))
    
    try:
        # Download file
        if message.content_type == 'document':
            file_info = await bot.get_file(message.document.file_id)
        elif message.content_type == 'audio':
            file_info = await bot.get_file(message.audio.file_id)
        elif message.content_type == 'voice':
            file_info = await bot.get_file(message.voice.file_id)
        elif message.content_type == 'video':
            file_info = await bot.get_file(message.video.file_id)
        elif message.content_type == 'video_note':
            file_info = await bot.get_file(message.video_note.file_id)
        
        downloaded_file = await bot.download_file(file_info.file_path)
        
        # Save file temporarily
        temp_file_path = f"temp_{message.from_user.id}_{message.id}.tmp"
        with open(temp_file_path, 'wb') as f:
            f.write(downloaded_file)
        
        # Recognize music using ShazamIO
        shazam = Shazam()
        recognized = await shazam.recognize(temp_file_path)
        
        # Remove temporary file
        os.remove(temp_file_path)
        
        # Check if recognition was successful
        if recognized and 'track' in recognized:
            track = recognized['track']
            title = track.get('title', 'Unknown')
            artists = track.get('subtitle', 'Unknown')
            track_id = track.get('key', '')
            
            # Try to get album info
            album = 'Unknown'
            if 'sections' in track:
                for section in track['sections']:
                    if 'metadata' in section:
                        for meta in section['metadata']:
                            if meta.get('title') == 'Album':
                                album = meta.get('text', 'Unknown')
                                break
            
            # Send result
            result_text = get_text(message.from_user.id, 'result').format(
                title=title,
                artist=artists,
                album=album,
                track_id=track_id,
                title_lower=title.lower().replace(' ', '-')
            )
            
            await bot.edit_message_text(
                result_text,
                message.chat.id,
                processing_msg.message_id,
                parse_mode='Markdown'
            )
        else:
            await bot.edit_message_text(
                get_text(message.from_user.id, 'no_match'),
                message.chat.id,
                processing_msg.message_id
            )
    except Exception as e:
        logger.error(f"Error processing media: {e}")
        await bot.edit_message_text(
            get_text(message.from_user.id, 'no_match'),
            message.chat.id,
            processing_msg.message_id
        )

async def handle_metadata_file(message):
    """Handle file for metadata editing"""
    try:
        # Download file
        if message.content_type == 'document':
            file_info = await bot.get_file(message.document.file_id)
            file_name = message.document.file_name
        elif message.content_type == 'audio':
            file_info = await bot.get_file(message.audio.file_id)
            file_name = message.audio.file_name
        else:
            await bot.reply_to(message, get_text(message.from_user.id, 'send_audio'))
            return
        
        downloaded_file = await bot.download_file(file_info.file_path)
        
        # Save file temporarily
        temp_file_path = f"temp_metadata_{message.from_user.id}_{message.id}_{file_name}"
        with open(temp_file_path, 'wb') as f:
            f.write(downloaded_file)
        
        # Store file info
        user_files[message.from_user.id] = {
            'file_path': temp_file_path,
            'file_name': file_name
        }
        
        await bot.reply_to(message, get_text(message.from_user.id, 'metadata_editing_started'))
    except Exception as e:
        logger.error(f"Error handling metadata file: {e}")
        await bot.reply_to(message, get_text(message.from_user.id, 'download_failed'))

@bot.message_handler(func=lambda message: message.from_user.id in user_files and message.text)
async def handle_metadata_text(message):
    """Handle metadata text input"""
    try:
        # Parse metadata from text
        lines = message.text.strip().split('\n')
        metadata = {}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip()
        
        if 'title' not in metadata or 'artist' not in metadata or 'album' not in metadata:
            await bot.reply_to(message, get_text(message.from_user.id, 'invalid_metadata_format'))
            return
        
        # Get file info
        file_info = user_files[message.from_user.id]
        file_path = file_info['file_path']
        
        # Update metadata
        if file_path.endswith('.mp3') and METADATA_AVAILABLE:
            # Load MP3 file
            audio_file = MP3(file_path, ID3=ID3)
            
            # Add ID3 tag if it doesn't exist
            try:
                audio_file.add_tags()
            except Exception:
                pass  # Tags already exist
            
            # Update metadata
            audio_file.tags.add(TIT2(encoding=3, text=metadata['title']))
            audio_file.tags.add(TPE1(encoding=3, text=metadata['artist']))
            audio_file.tags.add(TALB(encoding=3, text=metadata['album']))
            
            # Save file
            audio_file.save()
            
            # Send updated file
            with open(file_path, 'rb') as audio:
                await bot.send_audio(message.chat.id, audio)
            
            # Clean up
            del user_files[message.from_user.id]
            os.remove(file_path)
            
            await bot.reply_to(message, get_text(message.from_user.id, 'metadata_updated'))
        else:
            await bot.reply_to(message, get_text(message.from_user.id, 'download_failed'))
    except Exception as e:
        logger.error(f"Error updating metadata: {e}")
        await bot.reply_to(message, get_text(message.from_user.id, 'download_failed'))

@bot.message_handler(func=lambda message: message.text and message.text.startswith('http'))
async def handle_link(message):
    """Handle social media links"""
    url = message.text
    
    # Notify user about downloading
    downloading_msg = await bot.reply_to(message, get_text(message.from_user.id, 'downloading'))
    
    try:
        # Try to download based on URL
        if 'youtube.com' in url or 'youtu.be' in url:
            if YOUTUBE_AVAILABLE:
                await download_youtube_video(message, url, downloading_msg)
            else:
                await download_generic_file(message, url, downloading_msg)
        elif 'instagram.com' in url:
            if INSTAGRAM_AVAILABLE:
                await download_instagram_content(message, url, downloading_msg)
            else:
                await download_generic_file(message, url, downloading_msg)
        else:
            await download_generic_file(message, url, downloading_msg)
    except Exception as e:
        logger.error(f"Error downloading content: {e}")
        await bot.edit_message_text(
            get_text(message.from_user.id, 'download_failed'),
            message.chat.id,
            downloading_msg.message_id
        )

async def download_youtube_video(message, url, downloading_msg):
    """Download YouTube video"""
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if stream:
            video_path = f"temp_yt_{message.from_user.id}_{message.id}.mp4"
            stream.download(filename=video_path)
            
            # Send the downloaded video
            with open(video_path, 'rb') as video:
                await bot.edit_message_text(
                    get_text(message.from_user.id, 'download_complete'),
                    message.chat.id,
                    downloading_msg.message_id
                )
                await bot.send_video(message.chat.id, video)
            
            # Remove temporary file
            os.remove(video_path)
        else:
            await bot.edit_message_text(
                get_text(message.from_user.id, 'download_failed'),
                message.chat.id,
                downloading_msg.message_id
            )
    except Exception as e:
        logger.error(f"YouTube download error: {e}")
        await bot.edit_message_text(
            get_text(message.from_user.id, 'download_failed'),
            message.chat.id,
            downloading_msg.message_id
        )

async def download_instagram_content(message, url, downloading_msg):
    """Download Instagram content"""
    try:
        loader = instaloader.Instaloader()
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        
        # For simplicity, we'll download the post's image/video
        loader.download_post(post, target_profile_name="temp")
        
        # Find the downloaded file
        import glob
        files = glob.glob(f"temp/{shortcode}*")
        if files:
            file_path = files[0]
            with open(file_path, 'rb') as f:
                if file_path.endswith('.mp4'):
                    await bot.edit_message_text(
                        get_text(message.from_user.id, 'download_complete'),
                        message.chat.id,
                        downloading_msg.message_id
                    )
                    await bot.send_video(message.chat.id, f)
                else:
                    await bot.edit_message_text(
                        get_text(message.from_user.id, 'download_complete'),
                        message.chat.id,
                        downloading_msg.message_id
                    )
                    await bot.send_photo(message.chat.id, f)
            
            # Clean up
            import shutil
            shutil.rmtree("temp")
        else:
            await bot.edit_message_text(
                get_text(message.from_user.id, 'download_failed'),
                message.chat.id,
                downloading_msg.message_id
            )
    except Exception as e:
        logger.error(f"Instagram download error: {e}")
        await bot.edit_message_text(
            get_text(message.from_user.id, 'download_failed'),
            message.chat.id,
            downloading_msg.message_id
        )

async def download_generic_file(message, url, downloading_msg):
    """Download generic file"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Try to get file extension from URL or content type
        content_type = response.headers.get('content-type', '')
        file_extension = '.mp4'  # default
        
        if 'video' in content_type:
            file_extension = '.mp4'
        elif 'audio' in content_type:
            file_extension = '.mp3'
        elif 'image' in content_type:
            file_extension = '.jpg'
        
        file_path = f"temp_generic_{message.from_user.id}_{message.id}{file_extension}"
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        # Send the downloaded file
        with open(file_path, 'rb') as f:
            await bot.edit_message_text(
                get_text(message.from_user.id, 'download_complete'),
                message.chat.id,
                downloading_msg.message_id
            )
            
            if file_extension == '.mp4':
                await bot.send_video(message.chat.id, f)
            elif file_extension == '.mp3':
                await bot.send_audio(message.chat.id, f)
            else:
                await bot.send_photo(message.chat.id, f)
        
        # Remove temporary file
        os.remove(file_path)
    except Exception as e:
        logger.error(f"Generic download error: {e}")
        await bot.edit_message_text(
            get_text(message.from_user.id, 'download_failed'),
            message.chat.id,
            downloading_msg.message_id
        )

# Inline mode handler
@bot.inline_handler(lambda query: True)
async def inline_query_handler(inline_query):
    """Handle inline queries for music search"""
    query_text = inline_query.query
    
    try:
        if query_text:
            # Search for tracks using ShazamIO
            shazam = Shazam()
            search_result = await shazam.search_track(query=query_text, limit=10)
            
            results = []
            if 'tracks' in search_result:
                for i, track in enumerate(search_result['tracks']):
                    # Create result item
                    title = track.get('title', 'Unknown Track')
                    artist = track.get('subtitle', 'Unknown Artist')
                    track_id = track.get('key', '')
                    
                    # Create article result
                    result = types.InlineQueryResultArticle(
                        str(i),
                        title=f"{title} - {artist}",
                        description=artist,
                        input_message_content=types.InputTextMessageContent(
                            f"🎵 {title}\n👤 {artist}\n🔗 [Listen on Shazam](https://www.shazam.com/track/{track_id})",
                            parse_mode='Markdown'
                        )
                    )
                    results.append(result)
            
            # Answer the inline query
            await bot.answer_inline_query(inline_query.id, results, cache_time=1, is_personal=True)
        else:
            # Show trending tracks if no query
            shazam = Shazam()
            trending = await shazam.top_world_tracks(limit=10)
            
            results = []
            if 'tracks' in trending:
                for i, track in enumerate(trending['tracks']):
                    title = track.get('title', 'Unknown Track')
                    artist = track.get('subtitle', 'Unknown Artist')
                    track_id = track.get('key', '')
                    
                    result = types.InlineQueryResultArticle(
                        str(i),
                        title=f"{title} - {artist}",
                        description="Trending track",
                        input_message_content=types.InputTextMessageContent(
                            f"🔥 Trending: {title}\n👤 {artist}\n🔗 [Listen on Shazam](https://www.shazam.com/track/{track_id})",
                            parse_mode='Markdown'
                        )
                    )
                    results.append(result)
            
            await bot.answer_inline_query(inline_query.id, results, cache_time=1, is_personal=True)
    except Exception as e:
        logger.error(f"Inline query error: {e}")

# Run the bot
if __name__ == '__main__':
    print("Bot is starting...")
    print(f"Bot token: {BOT_TOKEN[:5]}...")
    asyncio.run(bot.polling())