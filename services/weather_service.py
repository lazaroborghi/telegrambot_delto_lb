import aiohttp
from config import OPENWEATHERMAP_API_KEY

async def get_weather(city):
    # Se llama a la API de openweathermap para consultar el clima de la ciudad dada
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=es"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            status_ok = False
            if response.status == 200:
                temp = data['main']['temp']
                weather = data['weather'][0]['description']
                status_ok = True
                return status_ok, f"La temperatura en {city} es {temp}°C con {weather}."
            else:
                return status_ok, "No pude obtener el clima para esa ciudad."
