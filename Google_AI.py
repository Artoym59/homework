import json
import os

DB_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def show_tasks(tasks):
    if not tasks:
        print("\nСписок задач пуст.")
        return
    print("\n--- СПИСОК ЗАДАЧ ---")
    for i, task in enumerate(tasks, 1):
        status = "[X]" if task['done'] else "[ ]"
        print(f"{i}. {status} {task['title']}")

def main():
    tasks = load_tasks()
    
    while True:
        print("\n1. Показать задачи\n2. Добавить задачу\n3. Удалить задачу\n4. Отметить как выполненную\n5. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            show_tasks(tasks)
        
        elif choice == '2':
            title = input("Введите название задачи: ")
            tasks.append({"title": title, "done": False})
            save_tasks(tasks)
            print("Задача добавлена!")

        elif choice == '3':
            show_tasks(tasks)
            try:
                idx = int(input("Введите номер задачи для удаления: ")) - 1
                removed = tasks.pop(idx)
                save_tasks(tasks)
                print(f"Задача '{removed['title']}' удалена.")
            except (IndexError, ValueError):
                print("Ошибка: неверный номер.")

        elif choice == '4':
            show_tasks(tasks)
            try:
                idx = int(input("Введите номер выполненной задачи: ")) - 1
                tasks[idx]['done'] = True
                save_tasks(tasks)
                print("Статус обновлен!")
            except (IndexError, ValueError):
                print("Ошибка: неверный номер.")

        elif choice == '5':
            print("До свидания!")
            break
        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()