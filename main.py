from bot import app
import handlers.start
import handlers.counter
import handlers.weather
import handlers.openai_chat
import handlers.openai_translator
import asyncio

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(app.run())
    except Exception as e:
        print(f"Error inesperado al iniciar el bot: {e}")
    finally:
        loop.close()