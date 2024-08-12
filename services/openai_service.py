import os
from config import openai_client, GENERATE_IMAGES
from pathlib import Path

def transcribe(file_path):
    audio_file = open(file_path,"rb")

    # Llamar a api de OpenAi para transcribir un audio
    transcription = openai_client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
    )
    return transcription

def translate(transcription, language_name):
    content = (
        f"Por favor, traduce el siguiente texto al idioma {language_name}. "
        f"Si el texto ya está en {language_name}, responde con 'errorfalse'. "
        f"Aquí está el texto: \"{transcription}\"."
    )

    # Llamar a la API de OpenAI para traducir (es un chat completion con instrucciones de traducción)
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )
    return response.choices[0].message.content

def generate_voice(translation):
    data_folder = Path(__file__).parent / "data"
    os.makedirs(data_folder, exist_ok=True)
    
    speech_file_path = data_folder / "speech.mp3"

    # Llamar a la API de OpenAI para generar un audio
    response =  openai_client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=translation
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path

def generate_image(prompt):
    if GENERATE_IMAGES == 0:
        return
    # Llamar a la API de OpenAI para generar una imagen
    response = openai_client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

def generate_chat_completion(messages, model, temperature=1):
    # Llamar a la API de OpenAI para generar chat completion
    response = openai_client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature
    )
    return response.choices[0].message.content
