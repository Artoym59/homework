import json
from datetime import datetime

# Структура задачи
task = {
    'id': None,
    'title': '',
    'completed': False,
    'created_at': ''
}

#Функция проверки наличия JSON файла
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

#Функция сохранения задачи
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

#Функция добавления задачи
def add_task(title):
    tasks = load_tasks()
    new_task = task.copy()
    new_task['id'] = len(tasks) + 1
    new_task['title'] = title
    new_task['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f'Задача "{title}" успешно добавлена.')

#Функция удаления задачи
def remove_task(task_id):
    tasks = load_tasks()
    for index, task in enumerate(tasks):
        if task['id'] == task_id:
            del tasks[index]
            save_tasks(tasks)
            print(f'Задача с ID {task_id} удалена.')
            return
    print(f'Задача с ID {task_id} не найдена.')

#Функция отметки выполнения
def mark_completed(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            save_tasks(tasks)
            print(f'Задача с ID {task_id} отмечена как выполненная.')
            return
    print(f'Задача с ID {task_id} не найдена.')

#Функция получения списка задач
def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print('Нет задач.')
        return
    
    for task in tasks:
        status = '[X]' if task['completed'] else '[ ]'
        print(f"{task['id']} | {status} | {task['title']} | Создана: {task['created_at']}")

#Функция консольного приложения реализованная через цикл while
def main():
    while True:
        print("\nМенеджер задач:")
        print("1. Добавить задачу")
        print("2. Удалить задачу")
        print("3. Отметить задачу выполненной")
        print("4. Показать список задач")
        print("5. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            title = input("Введите название задачи: ")
            add_task(title)
        elif choice == '2':
            task_id = int(input("Введите ID задачи для удаления: "))
            remove_task(task_id)
        elif choice == '3':
            task_id = int(input("Введите ID задачи для отметки выполнения: "))
            mark_completed(task_id)
        elif choice == '4':
            list_tasks()
        elif choice == '5':
            break
        else:
            print("Недопустимый выбор.")

if __name__ == "__main__":
    main()