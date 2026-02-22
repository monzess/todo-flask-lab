import sqlite3

DB_NAME = "todo.db"


def add_is_done_column():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Добавляем поле is_done со значением по умолчанию 0 (не выполнено)
    try:
        cursor.execute("ALTER TABLE tasks ADD COLUMN is_done INTEGER DEFAULT 0")
        print("Поле is_done успешно добавлено!")
    except sqlite3.OperationalError as e:
        print("Поле уже существует или другая ошибка:", e)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    add_is_done_column()
