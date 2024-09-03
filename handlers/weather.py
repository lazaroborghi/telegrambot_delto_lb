import asyncio
from pyrogram import Client, filters, ContinuePropagation
from services.weather_service import get_weather
from bot import app
from utils.user_manager import get_user_state, set_user_state, clear_user_state
from utils.helper import WEATHER_BUTTON_TEXT, TRANSLATOR_BUTTON_TEXT, COUNTER_BUTTON_TEXT, CHATBOT_BUTTON_TEXT
from services.openai_service import generate_image, generate_chat_completion

@app.on_message(filters.regex(WEATHER_BUTTON_TEXT))
async def ask_city(client, message):
    try:
        user_id = message.from_user.id
        set_user_state(user_id, "waiting_for_city")
        await message.reply("Por favor, ingresa el nombre de la ciudad para obtener el clima:")
    except Exception as e:
        await message.reply("Ocurrió un error al intentar configurar el estado. Por favor, inténtalo nuevamente.")

@app.on_message()
async def weather(client, message):
    user_id = message.from_user.id
    
    # Verificar si el usuario está en el estado de esperar la ciudad
    if get_user_state(user_id) == "waiting_for_city":
        city = message.text

        try:
            # Llamar a la API de OpenAI para formatear la ciudad usando asyncio.to_thread
            messages = [
                {
                    "role": "user",
                    "content": f"Analiza esta ciudad: ({city}). Si te proporcioné un nombre de ciudad devuélveme el nombre de la ciudad seguido por el nombre del país en el formato Ciudad, País. Si solo te proporcioné el nombre de un país sin una ciudad, devuélveme solo el nombre del país. No devuelvas nada más que eso. TEXTO: {city}"
                }
            ]

            response = await generate_chat_completion(messages, "gpt-4o-mini", 0.1)
            city = response

        except Exception as e:
            await message.reply("Ocurrió un error al analizar el nombre de la ciudad. Por favor, inténtalo nuevamente.")
            print(e)
            return

        print(city)
        
        try:
            # Llamar a la API de OpenWeatherMap para obtener el clima de la ciudad
            owmstatus_ok, weather_info = await get_weather(city)
        except Exception as e:
            await message.reply("Ocurrió un error al obtener el clima. Por favor, inténtalo nuevamente.")
            print(e)
            return

        if owmstatus_ok:
            try:
                # Llamar a la API de OpenAI para agregar información sobre el clima y una breve descripción del lugar usando asyncio.to_thread
                messages = [
                    {
                        "role": "user",
                        "content": f"Agrega información adicional sobre el clima al siguiente mensaje: ({weather_info}). Primero menciona el clima, la temperatura y un consejo de cómo pasar el día (por ejemplo si tiene que usar paraguas, si se tiene que abrigar o si simplemente tiene que disfrutar del día). Agrega un poco de información interesante sobre el lugar del cual se está consultando el clima. Sé breve."
                    }
                ]
                response = await generate_chat_completion(messages, "gpt-3.5-turbo")
                await message.reply(response)
            except Exception as e:
                await message.reply("Ocurrió un error al procesar la información del clima. Por favor, inténtalo nuevamente.")
                return

            try:
                # Llamar a la API de OpenAI para generar una imagen de un paisaje del lugar usando asyncio.to_thread
                prompt = f"Crea una fotografía con realismo de la ciudad: {city}. El propósito de la imagen es mostrar cómo se ve la ciudad de la cual se está hablando."
                image_url = await generate_image(prompt)

                if image_url:
                    caption = f"Una imagen ilustrativa de {city}. (La imagen no representa la realidad, está generada con OpenAI)"
                    await app.send_photo(message.chat.id, image_url, caption)
            except Exception as e:
                await message.reply("Ocurrió un error al generar la imagen. Por favor, inténtalo nuevamente.")
                return
        else:
            if COUNTER_BUTTON_TEXT != message.text and CHATBOT_BUTTON_TEXT != message.text and TRANSLATOR_BUTTON_TEXT != message.text:
                await message.reply("La ciudad no existe o no he encontrado el clima de esa ciudad.")

        # Resetea el estado del usuario
        clear_user_state(user_id)

    raise ContinuePropagation
