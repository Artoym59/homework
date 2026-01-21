import json
import os

# Имя файла для хранения задач
TASKS_FILE = 'tasks.json'

def load_tasks():
    """Загружает задачи из JSON-файла."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Сохраняет задачи в JSON-файл."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def add_task(tasks):
    """Добавляет новую задачу."""
    description = input("Введите описание задачи: ")
    task = {
        'id': len(tasks) + 1,
        'description': description,
        'completed': False
    }
    tasks.append(task)
    print("Задача добавлена.")

def delete_task(tasks):
    """Удаляет задачу по ID."""
    task_id = int(input("Введите ID задачи для удаления: "))
    tasks[:] = [task for task in tasks if task['id'] != task_id]
    # Пересчитываем ID, чтобы они были последовательными
    for i, task in enumerate(tasks, start=1):
        task['id'] = i
    print("Задача удалена.")

def complete_task(tasks):
    """Отмечает задачу выполненной по ID."""
    task_id = int(input("Введите ID задачи для отметки выполненной: "))
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            print("Задача отмечена выполненной.")
            return
    print("Задача не найдена.")

def list_tasks(tasks):
    """Выводит список задач."""
    if not tasks:
        print("Список задач пуст.")
        return
    for task in tasks:
        status = "Выполнено" if task['completed'] else "Не выполнено"
        print(f"ID: {task['id']}, Описание: {task['description']}, Статус: {status}")

def main():
    tasks = load_tasks()
    while True:
        print("\nМеню:")
        print("1. Добавить задачу")
        print("2. Удалить задачу")
        print("3. Отметить задачу выполненной")
        print("4. Получить список задач")
        print("5. Выход")
        choice = input("Выберите опцию: ")
        
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            delete_task(tasks)
        elif choice == '3':
            complete_task(tasks)
        elif choice == '4':
            list_tasks(tasks)
        elif choice == '5':
            save_tasks(tasks)
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
        
        # Сохраняем после каждого изменения
        if choice in ['1', '2', '3']:
            save_tasks(tasks)

if __name__ == "__main__":
    main()