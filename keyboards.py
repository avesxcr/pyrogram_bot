from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру главного меню.

    :return: Объект ReplyKeyboardMarkup.
    """
    return ReplyKeyboardMarkup(
        [
            ["Создать задачу", "Мои задачи"]
        ],
        resize_keyboard=True
    )

def back_menu() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру с кнопкой 'Назад'.

    :return: Объект ReplyKeyboardMarkup.
    """
    return ReplyKeyboardMarkup(
        [
            ["🔙 Назад"]
        ],
        resize_keyboard=True
    )

def task_inline_keyboard(task_id: int, status: str) -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру для управления задачей.

    :param task_id: ID задачи.
    :param status: Статус задачи ('Невыполнено' или 'Выполнено').
    :return: Объект InlineKeyboardMarkup.
    """
    buttons = []

    if status != "Выполнено":
        buttons.append(
            InlineKeyboardButton("✅ Выполнено", callback_data=f"complete_{task_id}")
        )

    buttons.append(
        InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_{task_id}")
    )

    return InlineKeyboardMarkup([buttons])
