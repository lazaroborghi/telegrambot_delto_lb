import asyncio
from pathlib import Path
from pyrogram import Client, filters, ContinuePropagation
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from bot import app
from utils.user_manager import set_user_state, get_user_state, clear_user_state
from utils.helper import default_keyboard, TRANSLATOR_BUTTON_TEXT, CLOSE_TRANSLATOR_BUTTON_TEXT
from services.openai_service import transcribe, translate, generate_voice

# Lista de idiomas disponibles para la traducción
LANGUAGES = {
    "en": "Inglés",
    "es": "Español",
    "fr": "Francés",
    "de": "Alemán",
    "it": "Italiano",
    "pt": "Portugués"
}

@app.on_message(filters.regex(f"^{TRANSLATOR_BUTTON_TEXT}$") | filters.regex(f"^{CLOSE_TRANSLATOR_BUTTON_TEXT}$"))
async def handle_voicetranslator(client, message):
    user_id = message.from_user.id
    current_state = get_user_state(user_id)
    
    if current_state == "translating_voice":
        # Resetear el estado del usuario y volver a mostrar los botones originales
        clear_user_state(user_id)
        keyboard = ReplyKeyboardMarkup(
            default_keyboard,
            resize_keyboard=True
        )
        await message.reply("El traductor ha sido cerrado.", reply_markup=keyboard)
    else:
        # Cambiar el estado del usuario para seleccionar el idioma
        set_user_state(user_id, "translating_voice")
        buttons = [
            [InlineKeyboardButton(text=lang, callback_data=f"translate_{code}")]
            for code, lang in LANGUAGES.items()
        ]
        # Cambiar el botón a "Cerrar traductor" y ocultar los demás botones
        keyboard = ReplyKeyboardMarkup(
            [[CLOSE_TRANSLATOR_BUTTON_TEXT]],
            resize_keyboard=True
        )
        await message.reply(
            "Por favor, elige el idioma al cual quieres traducir tu voz:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        await message.reply(
            "El traductor de voz está activado. Puedes cerrarlo cuando desees.",
            reply_markup=keyboard
        )

    raise ContinuePropagation

@app.on_callback_query(filters.regex("^translate_"))
async def select_language(client, callback_query):
    user_id = callback_query.from_user.id
    lang_code = callback_query.data.split("_")[1]
    
    # Guardar el idioma seleccionado y actualizar el estado del usuario
    set_user_state(user_id, f"waiting_for_voice_{lang_code}")
    language_name = LANGUAGES.get(lang_code, "Unknown Language")

    # Informar al usuario que envíe un mensaje de voz para traducir
    await callback_query.message.reply(f"Has seleccionado el idioma {language_name}. Ahora, por favor, envía un mensaje de voz para traducir.")
    
    # Eliminar el teclado de selección de idioma
    await callback_query.message.delete()

@app.on_message(filters.voice)
async def handle_voice_message(client, message):
    user_id = message.from_user.id
    current_state = get_user_state(user_id)
    
    if current_state and current_state.startswith("waiting_for_voice_"):
        lang_code = current_state.split("_")[-1]
        language_name = LANGUAGES.get(lang_code, "Unknown Language")

        # Reemplazo cada audio cuando recibo uno nuevo para que no se guarden
        file_id = message.voice.file_id
        file_path = Path(__file__).parent / "../downloads" / "voice.mp3"

        try:
            await app.download_media(file_id, file_name=file_path.name)
        except Exception:
            await message.reply("Ocurrió un error al descargar el archivo de voz. Por favor, inténtalo nuevamente.")
            return

        try:
            transcription = await transcribe(file_path)
        except Exception:
            await message.reply("Ocurrió un error al transcribir el archivo de voz. Por favor, inténtalo nuevamente.")
            return
        
        # Informar al usuario que la traducción está en proceso
        await message.reply(f'Archivo de voz recibido. Intentando traducir "{transcription}" a {language_name}.')

        try:
            translation = await translate(transcription, language_name)
        except Exception:
            await message.reply("Ocurrió un error al traducir el texto. Por favor, inténtalo nuevamente.")
            return

        # Check doble por si el modelo se equivoca
        if "error" in translation and "false" in translation:
            try:
                translation = await translate(transcription, language_name)
            except Exception:
                await message.reply("Ocurrió un error al traducir el texto. Por favor, inténtalo nuevamente.")
                return

        if "error" in translation and "false" in translation:
            await message.reply("No puedo traducir al mismo idioma de la nota de voz.")
            clear_user_state(user_id)
            await handle_voicetranslator(client, message)
            return

        await message.reply(translation)

        try:
            audio_path = await generate_voice(translation)
            with open(audio_path, "rb") as audio_file:
                await app.send_voice(user_id, audio_file)
        except Exception:
            await message.reply("Ocurrió un error al generar la voz. Por favor, inténtalo nuevamente.")
            return

        # Resetear el estado del usuario
        clear_user_state(user_id)
        await handle_voicetranslator(client, message)  # Llamar al toggle para cerrar el traductor después de traducir

    raise ContinuePropagation
