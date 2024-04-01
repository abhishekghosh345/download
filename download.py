import requests
import re
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Telegram bot token
TOKEN = 'BOT_TOKEN'

# Terabox URL
TERABOX_URL = 'https://terabox.com/'

# Regular expression to extract video URLs
VIDEO_URL_REGEX = r'"(https://terabox.com/\w+/file/\w+)"'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Terabox video downloader bot!')

def download_video(update: Update, context: CallbackContext) -> None:
    # Get the chat ID and message text
    chat_id = update.message.chat_id
    message_text = update.message.text

    # Extract the Terabox video URL from the message text
    video_url_match = re.search(VIDEO_URL_REGEX, message_text)
    if video_url_match:
        video_url = video_url_match.group(1)

        # Download the video
        download_path = f'./downloads/{chat_id}.mp4'  # Change the path as needed
        download_video_from_terabox(video_url, download_path)

        # Send the downloaded video to the user
        context.bot.send_video(chat_id=chat_id, video=open(download_path, 'rb'))
    else:
        update.message.reply_text('Invalid Terabox video URL provided.')

def download_video_from_terabox(video_url: str, download_path: str) -> None:
    # Send a GET request to Terabox URL
    response = requests.get(video_url)

    # Extract the direct download link from the HTML content
    direct_download_link_match = re.search(r'"(https://terabox.com/[^"]+)"', response.text)
    if direct_download_link_match:
        direct_download_link = direct_download_link_match.group(1)

        # Download the video
        with open(download_path, 'wb') as f:
            video_response = requests.get(direct_download_link)
            f.write(video_response.content)
    else:
        raise Exception('Direct download link not found.')

def main() -> None:
    # Create the updater and dispatcher
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('download', download_video))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
