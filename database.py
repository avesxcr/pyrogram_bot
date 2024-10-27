import sqlite3

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

   

