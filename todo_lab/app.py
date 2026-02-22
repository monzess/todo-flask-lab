import sqlite3  # sqlite3 будет работать с тем же файлом БД, что и в консольном этапе.
from flask import Flask, render_template, request, redirect, url_for  # Базовые функции Flask: шаблоны, формы, редирект, сборка URL.

app = Flask(__name__)  # Создаём Flask-приложение; __name__ помогает Flask найти templates и другие ресурсы.

DB_NAME = "todo.db"  # Файл БД (он уже создан скриптом db_setup.py).

def get_connection():  # Простая функция, чтобы не копировать connect() в каждой строке.
    return sqlite3.connect(DB_NAME)  # Возвращаем новое соединение с БД.

@app.route("/")  # Главная страница: покажем список задач.
def index():
    conn = get_connection()  # Открываем соединение с базой.
    cursor = conn.cursor()  # Создаём курсор для выполнения SQL.
    cursor.execute("SELECT id, title, is_done FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    conn.close()

    # Отладочный вывод в консоль
    print("Текущие задачи:")
    for task in tasks:
        print(f"ID: {task[0]}, Название: {task[1]}, Статус: {task[2]}")

    return render_template('index.html', tasks=tasks)




@app.route("/add", methods=["POST"])  # Этот роут принимает данные формы (POST) и добавляет задачу.
def add_task():
    title = request.form.get("title", "").strip()  # Берём поле title из формы; get безопаснее, чем form[«title»].
    if title == "":  # Простая проверка: если пусто - ничего не добавляем.
        return redirect(url_for("index"))  # Возвращаем пользователя на главную.

    conn = get_connection()  # Открываем соединение с БД.
    cursor = conn.cursor()  # Создаём курсор.
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))  # Добавляем задачу; (title,) - кортеж из 1 элемента.
    conn.commit()  # Сохраняем изменения, иначе новая строка может не записаться в файл.
    conn.close()  # Закрываем соединение.

    return redirect(url_for("index"))  # После добавления возвращаемся на главную страницу.


# кнопка удалить

@app.route('/delete/<int:task_id>', methods=['POST'])  # <int:task_id> - динамическая часть URL
def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))  # Удаляем задачу по ID
    conn.commit()
    conn.close()

    return redirect(url_for('index'))  # Возвращаемся на главную после удаления



# переключения статуса

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Получаем текущий статус
    cursor.execute("SELECT is_done FROM tasks WHERE id = ?", (task_id,))
    result = cursor.fetchone()

    if result is not None:  # Проверяем, что задача существует
        current_status = result[0]
        new_status = 1 if current_status == 0 else 0

        # Обновляем статус
        cursor.execute("UPDATE tasks SET is_done = ? WHERE id = ?", (new_status, task_id))
        conn.commit()
        print(f"Задача {task_id}: статус изменен с {current_status} на {new_status}")  # Для отладки

    conn.close()
    return redirect(url_for('index'))




if __name__ == "__main__":  # Стандартная проверка: код ниже выполнится только при запуске файла напрямую.
    app.run(debug=True)  # Запускаем сервер разработки; debug=True удобен на практике (показывает ошибки).