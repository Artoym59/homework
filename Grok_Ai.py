import json
import os
from datetime import datetime, timedelta

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def parse_deadline(deadline_str):
    """Пытается распарсить строку дедлайна в datetime"""
    if not deadline_str or deadline_str.strip() == "":
        return None
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%d.%m.%Y %H:%M",
        "%d.%m.%Y"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(deadline_str.strip(), fmt)
        except ValueError:
            continue
    return None

def update_task_priority(task):
    """Обновляет приоритет задачи в зависимости от дедлайна"""
    if not task.get('deadline'):
        task['priority'] = task.get('priority', 'medium')
        return

    try:
        deadline = datetime.fromisoformat(task['deadline'])
        now = datetime.now()
        time_left = deadline - now
        
        if time_left <= timedelta(hours=4) and time_left > timedelta(0):
            task['priority'] = 'high'
        elif time_left <= timedelta(0):
            task['priority'] = 'high'  # просрочено — тоже высокий приоритет
        else:
            # оставляем как было, если пользователь сам установил
            if task.get('priority') not in ('low', 'medium', 'high'):
                task['priority'] = 'medium'
    except:
        task['priority'] = 'medium'

def add_task(tasks):
    description = input("Описание задачи: ").strip()
    
    deadline_str = input("Дедлайн (например 2026-01-22 18:30 или оставьте пустым): ").strip()
    deadline = parse_deadline(deadline_str)
    
    priority = input("Приоритет (low / medium / high) [по умолчанию medium]: ").strip().lower()
    if priority not in ('low', 'medium', 'high'):
        priority = 'medium'
    
    task = {
        'id': len(tasks) + 1,
        'description': description,
        'completed': False,
        'priority': priority,
        'deadline': deadline.isoformat() if deadline else None
    }
    
    # Первоначальная проверка на срочность
    update_task_priority(task)
    
    tasks.append(task)
    print("Задача добавлена.")

def delete_task(tasks):
    try:
        task_id = int(input("ID задачи для удаления: "))
        tasks[:] = [t for t in tasks if t['id'] != task_id]
        # перенумеровываем
        for i, t in enumerate(tasks, 1):
            t['id'] = i
        print("Задача удалена.")
    except:
        print("Ошибка ввода ID.")

def complete_task(tasks):
    try:
        task_id = int(input("ID задачи для завершения: "))
        for task in tasks:
            if task['id'] == task_id:
                task['completed'] = True
                print("Задача отмечена как выполненная.")
                return
        print("Задача не найдена.")
    except:
        print("Ошибка ввода ID.")

def list_tasks(tasks):
    if not tasks:
        print("Список задач пуст.")
        return

    # Обновляем приоритеты перед выводом
    for task in tasks:
        update_task_priority(task)

    print("\nСписок задач:")
    print("-" * 80)
    for task in tasks:
        status = "✓" if task['completed'] else " "
        deadline_str = ""
        if task.get('deadline'):
            dl = datetime.fromisoformat(task['deadline'])
            deadline_str = f"  до {dl.strftime('%Y-%m-%d %H:%M')}"
        
        prio = task['priority'].upper()
        if prio == 'HIGH':
            prio = f"!!! {prio} !!!"
        
        print(f"[{status}]  ID: {task['id']:3d}  |  {prio:>8}  |  {task['description']}{deadline_str}")
    print("-" * 80)

def main():
    tasks = load_tasks()
    
    while True:
        print("\nМеню:")
        print("1. Добавить задачу")
        print("2. Удалить задачу")
        print("3. Отметить выполненной")
        print("4. Показать список задач")
        print("5. Выход")
        
        choice = input("\nВыбор: ").strip()
        
        if choice == '1':
            add_task(tasks)
            save_tasks(tasks)
        elif choice == '2':
            delete_task(tasks)
            save_tasks(tasks)
        elif choice == '3':
            complete_task(tasks)
            save_tasks(tasks)
        elif choice == '4':
            list_tasks(tasks)
        elif choice == '5':
            save_tasks(tasks)
            print("До встречи!")
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()