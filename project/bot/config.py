import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
FERNET_KEY = os.getenv("FERNET_KEY")

if not FERNET_KEY:
    raise RuntimeError("FERNET_KEY не задан. Проверь .env файл")
