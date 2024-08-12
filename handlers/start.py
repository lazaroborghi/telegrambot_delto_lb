from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from bot import app
from utils.user_manager import get_user_state
from utils.helper import default_keyboard, CHATBOT_BUTTON_TEXT, ENDCHATBOT_BUTTON_TEXT

@app.on_message(filters.command("start"))
def start(client, message):
    user_id = message.from_user.id
    current_state = get_user_state(user_id)
    
    # Determina el texto del botón basado en el estado actual
    if current_state == "chatting":
        button_text = ENDCHATBOT_BUTTON_TEXT
    else:
        button_text = CHATBOT_BUTTON_TEXT
    
    # Crear el teclado dinámico con todos los botones o solo el de charla
    if current_state == "chatting":
        keyboard = ReplyKeyboardMarkup(
            [[button_text]],
            resize_keyboard=True
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            [
                default_keyboard[0],
                [button_text],
                default_keyboard[2]
            ],
            resize_keyboard=True
        )
    
    # Enviar mensaje de bienvenida con el teclado de opciones dinámico
    message.reply(
        "Bienvenido a DeltoBot. ¿Qué te gustaría hacer?",
        reply_markup=keyboard
    )