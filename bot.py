from pyrogram import Client
from typing import Dict

from database import Database
from states import State
from dotenv import load_dotenv

import os

load_dotenv()

app = Client(
    "task_manager_bot",
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)


db = Database()
user_states: Dict[int, State] = {}
temp_data: Dict[int, Dict] = {}


if __name__ == "__main__":
    print("Бот запущен...")
    app.run()