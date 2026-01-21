import json
import os
from datetime import datetime, timedelta

DB_FILE = "todo_list.json"
DATE_FORMAT = "%d.%m.%Y %H:%M"

def load_tasks():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def check_priority(deadline_str):
    """Автоматически определяет приоритет на основе времени до дедлайна."""
    try:
        deadline = datetime.strptime(deadline_str, DATE_FORMAT)
        now = datetime.now()
        diff = deadline - now
        
        if diff < timedelta(hours=4):
            return "КРИТИЧЕСКИЙ (горит!)", 0
        elif diff < timedelta(days=1):
            return "Высокий", 1
        else:
            return "Обычный", 2
    except:
        return "Без срока", 3

def show_tasks(tasks):
    if not tasks:
        print("\nСписок задач пуст.")
        return []
    
    # Обновляем приоритеты перед показом (за 4 часа статус может измениться)
    for task in tasks:
        if task.get("deadline"):
            p_name, p_val = check_priority(task["deadline"])
            task["priority"] = p_name
            task["prio_val"] = p_val

    # Сортировка: сначала невыполненные, затем по весу приоритета, затем по дате
    sorted_tasks = sorted(tasks, key=lambda x: (x['done'], x.get('prio_val', 3), x.get('deadline', '')))
    
    print(f"\n--- Список задач на {datetime.now().strftime(DATE_FORMAT)} ---")
    for i, task in enumerate(sorted_tasks, 1):
        status = "[x]" if task["done"] else "[ ]"
        deadline = task.get("deadline", "нет")
        print(f"{i}. {status} [{task['priority']}] {task['text']} (Дедлайн: {deadline})")
    return sorted_tasks

def main():
    tasks = load_tasks()

    while True:
        print("\nМеню: 1.Список 2.Добавить 3.Удалить 4.Выполнить 5.Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            show_tasks(tasks)
        
        elif choice == "2":
            text = input("Текст задачи: ")
            deadline_input = input("Дедлайн (ДД.ММ.ГГГГ ЧЧ:ММ) или Enter: ")
            
            p_name, p_val = "Обычный", 2
            if deadline_input:
                try:
                    # Проверка формата
                    datetime.strptime(deadline_input, DATE_FORMAT)
                    p_name, p_val = check_priority(deadline_input)
                except ValueError:
                    print("Ошибка формата даты! Будет сохранено без дедлайна.")
                    deadline_input = None

            tasks.append({
                "text": text, 
                "done": False, 
                "deadline": deadline_input,
                "priority": p_name,
                "prio_val": p_val
            })
            save_tasks(tasks)
            print("Задача добавлена!")

        elif choice == "3":
            current = show_tasks(tasks)
            if current:
                try:
                    num = int(input("Номер для удаления: "))
                    tasks.remove(current[num - 1])
                    save_tasks(tasks)
                    print("Удалено.")
                except: print("Ошибка ввода.")

        elif choice == "4":
            current = show_tasks(tasks)
            if current:
                try:
                    num = int(input("Номер выполненной: "))
                    current[num - 1]["done"] = True
                    save_tasks(tasks)
                    print("Выполнено!")
                except: print("Ошибка ввода.")

        elif choice == "5":
            break

if __name__ == "__main__":
    main()