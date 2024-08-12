from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

PORT = int(os.getenv("PORT", 3000))
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENWEATHERMAP_API_KEY = os.getenv("OWM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_NAME = os.getenv("BOT_NAME")
BOT_USER_NAME = os.getenv("BOT_USER_NAME")
GENERATE_IMAGES = int(os.getenv("GENERATE_IMAGES"))

openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)
