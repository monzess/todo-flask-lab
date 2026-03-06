import json
import os
from datetime import datetime

DATA_FILE = "library.json"

def load_books():
    """Загружает список книг из JSON-файла."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_books(books):
    """Сохраняет список книг в JSON-файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def get_next_id(books):
    """Возвращает следующий свободный ID."""
    if not books:
        return 1
    return max(b["id"] for b in books) + 1

def add_book(books):
    """Добавляет новую книгу."""
    print("\n--- Добавление книги ---")
    title = input("Название книги: ").strip()
    if not title:
        print("Название не может быть пустым.")
        return
    author = input("Автор: ").strip()
    if not author:
        print("Автор не может быть пустым.")
        return
    shelf = input("Полка (например, 'верхняя', '3'): ").strip()
    if not shelf:
        print("Полка не может быть пустой.")
        return
    status = input("Статус (взял/вернул): ").strip().lower()
    if status not in ("взял", "вернул"):
        print("Статус должен быть 'взял' или 'вернул'.")
        return
    date = input("Дата (ГГГГ-ММ-ДД, Enter для сегодня): ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        # простая проверка формата
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Неверный формат даты. Используется сегодняшняя.")
            date = datetime.now().strftime("%Y-%m-%d")

    new_book = {
        "id": get_next_id(books),
        "title": title,
        "author": author,
        "shelf": shelf,
        "status": status,
        "date": date
    }
    books.append(new_book)
    save_books(books)
    print(f"Книга '{title}' добавлена с ID {new_book['id']}.")

def list_books(books):
    """Показывает все книги."""
    if not books:
        print("\nБиблиотека пуста.")
        return
    print("\n--- Список книг ---")
    for b in books:
        print(f"ID: {b['id']} | {b['title']} — {b['author']} | Полка: {b['shelf']} | Статус: {b['status']} | Дата: {b['date']}")

def search_books(books):
    """Поиск по названию или автору (частичное совпадение)."""
    query = input("\nВведите часть названия или автора: ").strip().lower()
    if not query:
        print("Пустой запрос.")
        return
    found = [b for b in books if query in b["title"].lower() or query in b["author"].lower()]
    if found:
        print(f"\nНайдено книг: {len(found)}")
        for b in found:
            print(f"ID: {b['id']} | {b['title']} — {b['author']} | Полка: {b['shelf']} | Статус: {b['status']} | Дата: {b['date']}")
    else:
        print("Ничего не найдено.")

def filter_by_status(books):
    """Фильтр по статусу (взял/вернул)."""
    status = input("\nВведите статус для фильтра (взял/вернул): ").strip().lower()
    if status not in ("взял", "вернул"):
        print("Статус должен быть 'взял' или 'вернул'.")
        return
    filtered = [b for b in books if b["status"] == status]
    if filtered:
        print(f"\nКниги со статусом '{status}':")
        for b in filtered:
            print(f"ID: {b['id']} | {b['title']} — {b['author']} | Полка: {b['shelf']} | Дата: {b['date']}")
    else:
        print(f"Нет книг со статусом '{status}'.")

def edit_book(books):
    """Редактирование книги по ID."""
    list_books(books)
    try:
        book_id = int(input("\nВведите ID книги для редактирования: "))
    except ValueError:
        print("Некорректный ID.")
        return
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        print(f"Книга с ID {book_id} не найдена.")
        return
    print(f"Редактирование: {book['title']} (оставьте поле пустым, чтобы не менять)")
    new_title = input(f"Новое название [{book['title']}]: ").strip()
    if new_title:
        book["title"] = new_title
    new_author = input(f"Новый автор [{book['author']}]: ").strip()
    if new_author:
        book["author"] = new_author
    new_shelf = input(f"Новая полка [{book['shelf']}]: ").strip()
    if new_shelf:
        book["shelf"] = new_shelf
    new_status = input(f"Новый статус (взял/вернул) [{book['status']}]: ").strip().lower()
    if new_status in ("взял", "вернул"):
        book["status"] = new_status
    new_date = input(f"Новая дата [{book['date']}]: ").strip()
    if new_date:
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
            book["date"] = new_date
        except ValueError:
            print("Неверный формат даты, оставлена прежняя.")
    save_books(books)
    print("Книга обновлена.")

def delete_book(books):
    """Удаление книги по ID."""
    list_books(books)
    try:
        book_id = int(input("\nВведите ID книги для удаления: "))
    except ValueError:
        print("Некорректный ID.")
        return
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        print(f"Книга с ID {book_id} не найдена.")
        return
    confirm = input(f"Удалить книгу '{book['title']}'? (да/нет): ").strip().lower()
    if confirm == "да":
        books.remove(book)
        save_books(books)
        print("Книга удалена.")
    else:
        print("Удаление отменено.")

def main():
    books = load_books()
    while True:
        print("\n=== Домашняя библиотека ===")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Поиск по названию или автору")
        print("4. Фильтр по статусу (взял/вернул)")
        print("5. Редактировать книгу")
        print("6. Удалить книгу")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            add_book(books)
        elif choice == "2":
            list_books(books)
        elif choice == "3":
            search_books(books)
        elif choice == "4":
            filter_by_status(books)
        elif choice == "5":
            edit_book(books)
        elif choice == "6":
            delete_book(books)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()