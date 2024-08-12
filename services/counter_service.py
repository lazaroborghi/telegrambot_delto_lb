import json
from pathlib import Path
import aiofiles
import asyncio

COUNTER_FILE = Path(__file__).parent.parent / 'data' / 'counter.json'

COUNTER_DIR = COUNTER_FILE.parent
if not COUNTER_DIR.exists():
    COUNTER_DIR.mkdir(parents=True)

# Crear el archivo JSON si no existe
if not COUNTER_FILE.exists():
    async def create_counter_file():
        async with aiofiles.open(COUNTER_FILE, 'w') as f:
            await f.write('{}')

    asyncio.run(create_counter_file())

async def increment_counter(user_id):
    async with aiofiles.open(COUNTER_FILE, 'r+') as f:
        content = await f.read()
        counters = json.loads(content)
        counters[str(user_id)] = counters.get(str(user_id), 0) + 1
        await f.seek(0)
        await f.write(json.dumps(counters, indent=4))
        await f.truncate()

async def get_counter(user_id):
    async with aiofiles.open(COUNTER_FILE, 'r') as f:
        content = await f.read()
        counters = json.loads(content)
        return counters.get(str(user_id), 0)
