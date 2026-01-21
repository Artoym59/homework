import json
import os

FILE_NAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def show_tasks(tasks):
    if not tasks:
        print("Список задач пуст.")
        return

    for i, task in enumerate(tasks, start=1):
        status = "✓" if task["done"] else " "
        print(f"{i}. [{status}] {task['title']}")


def add_task(tasks):
    title = input("Введите название задачи: ").strip()
    if title:
        tasks.append({"title": title, "done": False})
        save_tasks(tasks)
        print("Задача добавлена.")
    else:
        print("Название не может быть пустым.")


def delete_task(tasks):
    show_tasks(tasks)
    try:
        index = int(input("Введите номер задачи для удаления: ")) - 1
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"Задача '{removed['title']}' удалена.")
    except (ValueError, IndexError):
        print("Неверный номер задачи.")


def complete_task(tasks):
    show_tasks(tasks)
    try:
        index = int(input("Введите номер выполненной задачи: ")) - 1
        tasks[index]["done"] = True
        save_tasks(tasks)
        print("Задача отмечена как выполненная.")
    except (ValueError, IndexError):
        print("Неверный номер задачи.")


def main():
    tasks = load_tasks()

    while True:
        print("\nМеню:")
        print("1. Показать задачи")
        print("2. Добавить задачу")
        print("3. Удалить задачу")
        print("4. Отметить задачу выполненной")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            complete_task(tasks)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()