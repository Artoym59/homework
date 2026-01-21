import json
import os
from datetime import datetime, timedelta

FILE_NAME = "tasks.json"
DEADLINE_PRIORITY_HOURS = 4


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def update_priorities(tasks):
    now = datetime.now()
    for task in tasks:
        if task["deadline"] and not task["done"]:
            deadline = datetime.fromisoformat(task["deadline"])
            if deadline - now <= timedelta(hours=DEADLINE_PRIORITY_HOURS):
                task["priority"] = "высокий"


def show_tasks(tasks):
    update_priorities(tasks)

    if not tasks:
        print("Список задач пуст.")
        return

    for i, task in enumerate(tasks, start=1):
        status = "✓" if task["done"] else " "
        deadline = task["deadline"] or "—"
        print(
            f"{i}. [{status}] {task['title']} | "
            f"приоритет: {task['priority']} | дедлайн: {deadline}"
        )


def add_task(tasks):
    title = input("Название задачи: ").strip()
    if not title:
        print("Название не может быть пустым.")
        return

    priority = input("Приоритет (низкий/средний/высокий) [средний]: ").strip().lower()
    if priority not in ("низкий", "средний", "высокий"):
        priority = "средний"

    deadline_input = input("Дедлайн (YYYY-MM-DD HH:MM) или Enter: ").strip()
    deadline = None

    if deadline_input:
        try:
            deadline = datetime.strptime(deadline_input, "%Y-%m-%d %H:%M")
            deadline = deadline.isoformat()
        except ValueError:
            print("Неверный формат даты.")
            return

    task = {
        "title": title,
        "done": False,
        "priority": priority,
        "deadline": deadline
    }

    tasks.append(task)
    update_priorities(tasks)
    save_tasks(tasks)
    print("Задача добавлена.")


def delete_task(tasks):
    show_tasks(tasks)
    try:
        index = int(input("Номер задачи для удаления: ")) - 1
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"Задача '{removed['title']}' удалена.")
    except (ValueError, IndexError):
        print("Неверный номер задачи.")


def complete_task(tasks):
    show_tasks(tasks)
    try:
        index = int(input("Номер выполненной задачи: ")) - 1
        tasks[index]["done"] = True
        save_tasks(tasks)
        print("Задача отмечена выполненной.")
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

        choice = input("Выбор: ")

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            complete_task(tasks)
        elif choice == "0":
            save_tasks(tasks)
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()