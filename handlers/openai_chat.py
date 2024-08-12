import asyncio
from pathlib import Path
from pyrogram import Client, filters, ContinuePropagation
from pyrogram.types import ReplyKeyboardMarkup
from bot import app
from utils.user_manager import get_user_state, set_user_state, clear_user_state, add_user_chat, get_user_chat, clear_user_chat
from utils.helper import default_keyboard, CHATBOT_BUTTON_TEXT, ENDCHATBOT_BUTTON_TEXT
from config import BOT_NAME
from services.openai_service import transcribe, generate_chat_completion

@app.on_message(filters.text)
async def handle_message(client, message):
    user_id = message.from_user.id
    current_state = get_user_state(user_id)

    # Lógica para manejar "Quiero charlar con Delto" y "Terminar charla"
    if message.text in [CHATBOT_BUTTON_TEXT, ENDCHATBOT_BUTTON_TEXT]:
        if current_state == "chatting" and message.text == ENDCHATBOT_BUTTON_TEXT:
            # Terminar la charla
            clear_user_state(user_id)
            chat_history = get_user_chat(user_id)

            if chat_history:
                try:
                    chat_analysis = await analyze_chat(chat_history)
                    await message.reply(f"Análisis de la charla:\n{chat_analysis}")
                except Exception:
                    await message.reply("Ocurrió un error al analizar la charla. Por favor, inténtalo nuevamente.")
                finally:
                    clear_user_chat(user_id)
            
            # Actualizar el teclado para mostrar todos los botones de nuevo
            keyboard = ReplyKeyboardMarkup(
                default_keyboard,
                resize_keyboard=True
            )
            controledMessage = f"Gracias por hablar con {BOT_NAME}!"
        else:
            # Iniciar la charla
            set_user_state(user_id, "chatting")
            await message.reply(f"¡Modo charla activado! Puedes empezar a hablar con {BOT_NAME}.")
            
            # Actualizar el teclado para mostrar solo el botón de terminar charla
            keyboard = ReplyKeyboardMarkup(
                [[ENDCHATBOT_BUTTON_TEXT]],
                resize_keyboard=True
            )
            controledMessage = f"Presiona el botón [Terminar charla] para terminar de hablar con {BOT_NAME}"
        
        # Actualizar el teclado en el chat
        await message.reply(
            controledMessage,
            reply_markup=keyboard
        )
    elif current_state == "chatting":
        await handle_chat(user_id, message.text, message)

    raise ContinuePropagation

@app.on_message(filters.voice)
async def handle_voice(client, message):
    user_id = message.from_user.id
    current_state = get_user_state(user_id)
    print("handle_voice")
    print(current_state)
    if current_state == "chatting":
        file_id = message.voice.file_id
        file_path = Path(__file__).parent / "../downloads" / "voice.mp3"

        try:
            await app.download_media(file_id, file_name=file_path.name)
        except Exception:
            await message.reply("Ocurrió un error al descargar el archivo de voz. Por favor, inténtalo nuevamente.")
            return

        try:
            transcription = await asyncio.to_thread(transcribe, file_path)
        except Exception:
            await message.reply("Ocurrió un error al transcribir el archivo de voz. Por favor, inténtalo nuevamente.")
            return

        await handle_chat(user_id, transcription, message)

    raise ContinuePropagation

async def handle_chat(user_id, text_message, message):
    try:
        # Lógica para manejar el modo de charla
        add_user_chat(user_id, "user", text_message)

        system_message = {
            "role": "system",
            "content": f"Tu nombre es {BOT_NAME}. Tu finalidad es charlar con un usuario. Estas conversando con un usuario y tienes que recordar tu nombre. Tu creador es Lázaro Borghi, un desarrollador de Salto Uruguay de 23 años (comentalo solo si te preguntan)."
        }
        get_user_chat(user_id).insert(0, system_message)

        try:
            response = await asyncio.to_thread(generate_chat_completion, get_user_chat(user_id), "gpt-3.5-turbo")
        except Exception:
            await message.reply("Ocurrió un error al generar la respuesta. Por favor, inténtalo nuevamente.")
            return

        add_user_chat(user_id, "assistant", response)
        await message.reply(response)
    
    except Exception:
        await message.reply("Ocurrió un error. Por favor, inténtalo nuevamente.")

async def analyze_chat(chat_history):
    try:
        # Filtrar los mensajes que no deberían ser considerados en el análisis
        filtered_chat_history = [
            msg for msg in chat_history 
            if not (msg['role'] == 'system' or f"Your name is {BOT_NAME}" in msg['content'])
        ]
        
        # Convierte la conversación filtrada en un texto para enviarlo a OpenAI
        conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in filtered_chat_history])
        
        # Analiza el sentimiento usando OpenAI
        messages = [
            {
                "role": "user",
                "content": f"Analiza el sentimiento de la siguiente conversación. Genera una breve explicación y clasificala como positiva, negativa o neutral:\n{conversation_text}"
            }
        ]

        response = await asyncio.to_thread(generate_chat_completion, messages, "gpt-3.5-turbo")
        return response
    
    except Exception:
        return "Ocurrió un error al analizar la charla."
