from telethon import TelegramClient
from message_observer.app.config import config

client = TelegramClient('session_name', config.API_ID, config.API_HASH)
