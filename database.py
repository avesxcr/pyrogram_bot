import sqlite3
from typing import Optional, List, Tuple

class Database:
    """
    Класс для работы с базой данных SQLite.
    """
    def __init__(self, db_name: str = "tasks.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        """
        Создает таблицы users и tasks, если они не существуют.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                login TEXT NOT NULL UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'Невыполнено',
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        self.connection.commit()

    def add_user(self, user_id: int, name: str, login: str) -> None:
        """
        Добавляет нового пользователя в базу данных.

        :param user_id: ID пользователя Telegram.
        :param name: Имя пользователя.
        :param login: Уникальный логин пользователя.
        """
        self.cursor.execute(
            "INSERT INTO users (user_id, name, login) VALUES (?, ?, ?)",
            (user_id, name, login)
        )
        self.connection.commit()

    def get_user(self, user_id: int) -> Optional[Tuple[int, str, str]]:
        """
        Получает информацию о пользователе по его user_id.

        :param user_id: ID пользователя Telegram.
        :return: Кортеж с данными пользователя или None.
        """
        self.cursor.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        return self.cursor.fetchone()

    def is_login_unique(self, login: str) -> bool:
        """
        Проверяет уникальность логина.

        :param login: Логин для проверки.
        :return: True, если логин уникален, иначе False.
        """
        self.cursor.execute(
            "SELECT * FROM users WHERE login = ?",
            (login,)
        )
        return self.cursor.fetchone() is None

    def add_task(self, user_id: int, title: str, description: str) -> None:
        """
        Добавляет новую задачу в базу данных.

        :param user_id: ID пользователя Telegram.
        :param title: Название задачи.
        :param description: Описание задачи.
        """
        self.cursor.execute(
            "INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)",
            (user_id, title, description)
        )
        self.connection.commit()

    def get_tasks(self, user_id: int) -> List[Tuple]:
        """
        Получает список задач пользователя.

        :param user_id: ID пользователя Telegram.
        :return: Список кортежей с данными задач.
        """
        self.cursor.execute(
            "SELECT task_id, title, description, status FROM tasks WHERE user_id = ?",
            (user_id,)
        )
        return self.cursor.fetchall()

    def complete_task(self, task_id: int) -> None:
        """
        Помечает задачу как выполненную.

        :param task_id: ID задачи.
        """
        self.cursor.execute(
            "UPDATE tasks SET status = 'Выполнено' WHERE task_id = ?",
            (task_id,)
        )
        self.connection.commit()

    def delete_task(self, task_id: int) -> None:
        """
        Удаляет задачу из базы данных.

        :param task_id: ID задачи.
        """
        self.cursor.execute(
            "DELETE FROM tasks WHERE task_id = ?",
            (task_id,)
        )
        self.connection.commit()
        
    def get_task_by_id(self, task_id: int) -> Optional[Tuple]:
        """
        Получает задачу по ее ID.

        :param task_id: ID задачи.
        :return: Кортеж с данными задачи или None.
        """
        self.cursor.execute(
            "SELECT task_id, user_id, title, description, status FROM tasks WHERE task_id = ?",
            (task_id,)
        )
        return self.cursor.fetchone()

