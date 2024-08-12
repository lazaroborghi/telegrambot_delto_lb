from pyrogram import Client, filters
from services.counter_service import increment_counter, get_counter
from bot import app
from utils.helper import COUNTER_BUTTON_TEXT
from services.openai_service import generate_image

@app.on_message(filters.regex(COUNTER_BUTTON_TEXT))
async def count(client, message):
    try:
        print("Handler de contador activado")
        user_id = message.from_user.id

        try:
            await increment_counter(user_id)
        except Exception:
            await message.reply("Ocurrió un error al incrementar el contador. Por favor, inténtalo nuevamente.")
            return

        try:
            count = await get_counter(user_id)
        except Exception:
            await message.reply("Ocurrió un error al obtener el contador. Por favor, inténtalo nuevamente.")
            return
        
        print(f"Contador para el usuario {user_id}: {count}")
        counter_message = f"Has contado {count} veces."
        if count == 1:
            counter_message = f"Has contado {count} vez."
        await message.reply(counter_message)
    
    except Exception:
        await message.reply("Ocurrió un error. Por favor, inténtalo nuevamente.")
