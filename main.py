from bot import app
import handlers.start
import handlers.counter
import handlers.weather
import handlers.openai_chat
import handlers.openai_translator
import asyncio

if __name__ == "__main__":

    try:
        app.run()
    except Exception as e:
        print(f"Error inesperado al iniciar el bot: {e}")