import os
import glob
from config import BOT_NAME, BOT_USER_NAME

WEATHER_BUTTON_TEXT = "¡Quiero saber el clima! ⛅"
COUNTER_BUTTON_TEXT = "¡Quiero contar! 🔢"
CHATBOT_BUTTON_TEXT = f"¡Quiero charlar con {BOT_NAME}! 🤖💬"
ENDCHATBOT_BUTTON_TEXT = "Terminar charla"
TRANSLATOR_BUTTON_TEXT = "¡Traducir mi voz! 🌐"
CLOSE_TRANSLATOR_BUTTON_TEXT = "Cerrar traductor"

default_keyboard = [[WEATHER_BUTTON_TEXT, COUNTER_BUTTON_TEXT],[CHATBOT_BUTTON_TEXT],[TRANSLATOR_BUTTON_TEXT]]

def clean_sessions():
    # Elimina los archivos de sesión existentes relacionados con el bot.
    session_files = glob.glob(f"{BOT_USER_NAME}.session*")
    for file in session_files:
        try:
            os.remove(file)
            print(f"Archivo {file} eliminado con éxito.")
        except Exception as e:
            print(f"No se pudo eliminar el archivo {file}: {e}")