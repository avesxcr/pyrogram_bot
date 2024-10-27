from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from typing import Dict

from database import Database
from states import State
from keyboards import main_menu, task_inline_keyboard, back_menu
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

@app.on_message(filters.command("start"))
def start(client: Client, message: Message) -> None:
    """
    Обработчик команды /start.

    :param client: Клиент Pyrogram.
    :param message: Объект сообщения.
    """
    user_id = message.from_user.id
    user = db.get_user(user_id)

    if user:
        message.reply_text(
            "Вы уже зарегистрированы!",
            reply_markup=main_menu()
        )
    else:
        message.reply_text("Добро пожаловать! Пожалуйста, введите ваше имя:")
        user_states[user_id] = State.REGISTRATION_NAME

@app.on_message(filters.text & ~filters.regex(r'^/'))
def handle_text(client: Client, message: Message) -> None:
    """
    Обработчик текстовых сообщений.

    :param client: Клиент Pyrogram.
    :param message: Объект сообщения.
    """
    user_id = message.from_user.id
    state = user_states.get(user_id, State.NONE)
    text = message.text.strip()

    if state == State.REGISTRATION_NAME:
        temp_data[user_id] = {"name": text}
        message.reply_text("Введите уникальный логин:")
        user_states[user_id] = State.REGISTRATION_LOGIN

    elif state == State.REGISTRATION_LOGIN:
        if db.is_login_unique(text):
            temp_data[user_id]["login"] = text
            db.add_user(user_id, temp_data[user_id]["name"], temp_data[user_id]["login"])
            message.reply_text(
                "Регистрация завершена!",
                reply_markup=main_menu()
            )
            user_states[user_id] = State.NONE
            temp_data.pop(user_id, None)
        else:
            message.reply_text("Этот логин уже занят, попробуйте другой.")

    elif text == "Создать задачу":
        message.reply_text("Введите название задачи:")
        user_states[user_id] = State.CREATE_TASK_TITLE

    elif text == "Мои задачи":
        tasks = db.get_tasks(user_id)
        if tasks:

            message.reply_text(
                "Ваши задачи:",
                reply_markup=back_menu()
            )
            for task in tasks:
                task_id, title, description, status = task
                message.reply_text(
                    f"**{title}**\n{description}\nСтатус: {status}",
                    reply_markup=task_inline_keyboard(task_id, status)
                )
        else:
            message.reply_text("У вас нет задач.", reply_markup=back_menu())


    elif text == "🔙 Назад":
        message.reply_text(
            "Вы вернулись в главное меню.",
            reply_markup=main_menu()
        )

    elif state == State.CREATE_TASK_TITLE:
        temp_data[user_id] = {"title": text}
        message.reply_text("Введите описание задачи:")
        user_states[user_id] = State.CREATE_TASK_DESCRIPTION

    elif state == State.CREATE_TASK_DESCRIPTION:
        temp_data[user_id]["description"] = text
        db.add_task(user_id, temp_data[user_id]["title"], temp_data[user_id]["description"])
        message.reply_text(
            "Задача добавлена!",
            reply_markup=main_menu()
        )
        user_states[user_id] = State.NONE
        temp_data.pop(user_id, None)

    else:
        message.reply_text(
            "Пожалуйста, выберите действие из меню.",
            reply_markup=main_menu()
        )

@app.on_callback_query()
def handle_callback_query(client: Client, callback_query: CallbackQuery) -> None:
    """
    Обработчик нажатий на inline-кнопки.

    :param client: Клиент Pyrogram.
    :param callback_query: Объект callback-запроса.
    """
    data = callback_query.data
    user_id = callback_query.from_user.id

    if data.startswith("complete_"):
        task_id = int(data.split("_")[1])
        db.complete_task(task_id)

        task = db.get_task_by_id(task_id)
        if task:
            _, _, title, description, status = task

            callback_query.message.edit_text(
                f"**{title}**\n{description}\nСтатус: {status}",
                reply_markup=task_inline_keyboard(task_id, status)
            )
        callback_query.answer("Задача помечена как выполненная.")

        callback_query.message.reply_text(
            "Действие выполнено. Выберите дальнейшее действие:",
            reply_markup=back_menu()
        )

    elif data.startswith("delete_"):
        task_id = int(data.split("_")[1])
        db.delete_task(task_id)
        callback_query.message.delete()
        callback_query.answer("Задача удалена.")

        callback_query.message.reply_text(
            "Действие выполнено. Выберите дальнейшее действие:",
            reply_markup=back_menu()
        )


if __name__ == "__main__":
    print("Бот запущен...")
    app.run()