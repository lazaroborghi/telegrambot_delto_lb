from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, BOT_USER_NAME

app = Client(BOT_USER_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
