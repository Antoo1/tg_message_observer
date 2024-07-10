from telethon import TelegramClient
from telegram_message_remover.app.config import config

client = TelegramClient('session_name', config.API_ID, config.API_HASH)
