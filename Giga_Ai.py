import json
from datetime import datetime

# Структура задачи с добавлением поля deadline
task = {
    'id': None,
    'title': '',
    'completed': False,
    'created_at': '',
    'priority': '',
    'deadline': None
}

# Загрузка задач из файла
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Сохранение задач в файл
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

# Добавление задачи с заданием приоритета в зависимости от дедлайна
def add_task(title):
    tasks = load_tasks()
    new_task = task.copy()
    new_task['id'] = len(tasks) + 1
    new_task['title'] = title
    new_task['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Запрашиваем deadline
    deadline_input = input("Введите срок выполнения задачи (формат ГГГГ-ММ-ДД ЧЧ:ММ): ")
    if deadline_input.strip():  # Проверяем, введён ли срок
        try:
            new_task['deadline'] = datetime.strptime(deadline_input, '%Y-%m-%d %H:%M').isoformat()
        except ValueError:
            print("Неверный формат даты. Срок установлен не будет.")
    else:
        print("Срок не указан.")

    # Устанавливаем приоритет исходя из близости дедлайна
    current_time = datetime.now()
    deadline_time = datetime.fromisoformat(new_task.get('deadline')) if new_task.get('deadline') else None
    if deadline_time is not None and abs((current_time - deadline_time).total_seconds()) / 3600 < 4:
        new_task['priority'] = 'высокий'
    else:
        # По умолчанию задаём низший приоритет
        new_task['priority'] = 'низкий'

    tasks.append(new_task)
    save_tasks(tasks)
    print(f'Задача "{title}" успешно добавлена.')

# Удаление задачи
def remove_task(task_id):
    tasks = load_tasks()
    for index, task in enumerate(tasks):
        if task['id'] == task_id:
            del tasks[index]
            save_tasks(tasks)
            print(f'Задача с ID {task_id} удалена.')
            return
    print(f'Задача с ID {task_id} не найдена.')

# Отметка задачи как выполненной
def mark_completed(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            save_tasks(tasks)
            print(f'Задача с ID {task_id} отмечена как выполненная.')
            return
    print(f'Задача с ID {task_id} не найдена.')

# Список всех задач с учётом дедлайна
def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print('Нет задач.')
        return
    
    for task in tasks:
        status = '[X]' if task['completed'] else '[ ]'
        deadline_str = f"(Deadline: {task['deadline']})" if task['deadline'] else ""
        print(f"{task['id']} | {status} | {task['title']} ({task['priority'].capitalize()} {deadline_str}) | Создана: {task['created_at']}")

# Основной цикл программы
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