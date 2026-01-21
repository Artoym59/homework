import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

# Цветовые константы
BG_COLOR = '#EAF8D6'  # Светло-зелёный фон
TEXT_COLOR = '#3C7A3B'  # Тёмно-зелёный шрифт
BUTTON_BG = '#AEDFAB'  # Зелёный цвет кнопок
ACCENT_COLOR = '#7CC374'  # Акцентный оттенок зелённого

# Структура задачи
task = {
    'id': None,
    'title': '',
    'completed': False,
    'created_at': '',
    'priority': '',
    'deadline': None
}

# Загружаем задачи из файла
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Сохраняем задачи в файл
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

# Автоопределение приоритета в зависимости от дедлайна
def set_priority_by_deadline(deadline):
    now = datetime.now()
    deadline_dt = datetime.fromisoformat(deadline)
    hours_left = abs((now - deadline_dt).total_seconds()) // 3600
    if hours_left < 4:
        return 'Высокий'
    else:
        return 'Средний'

# Добавляет новую задачу
def add_task():
    title = entry_title.get()
    deadline = entry_deadline.get()
    if not title or not deadline:
        messagebox.showwarning("Предупреждение", "Необходимо заполнить название и срок!")
        return
    
    try:
        deadline_dt = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
    except ValueError:
        messagebox.showerror("Ошибка", "Неправильный формат даты. Используйте ГГГГ-ММ-ДД ЧЧ:ММ.")
        return
    
    tasks = load_tasks()
    new_task = task.copy()
    new_task['id'] = len(tasks) + 1
    new_task['title'] = title
    new_task['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_task['deadline'] = deadline_dt.isoformat()
    new_task['priority'] = set_priority_by_deadline(deadline_dt.isoformat())
    
    tasks.append(new_task)
    save_tasks(tasks)
    update_listbox()
    clear_inputs()

# Очищает поля ввода
def clear_inputs():
    entry_title.delete(0, tk.END)
    entry_deadline.delete(0, tk.END)

# Обновляет listbox с задачами
def update_listbox():
    tasks = load_tasks()
    listbox.delete(0, tk.END)
    for t in tasks:
        status = '[✓]' if t['completed'] else '[ ]'
        line = f"{t['id']} | {status} | {t['title']} | Priority: {t['priority']} | Deadline: {t['deadline']}"
        listbox.insert(tk.END, line)

# Метка задачи как выполненной
def complete_task(event=None):
    selected_idx = listbox.curselection()
    if not selected_idx:
        return
    idx = selected_idx[0]
    tasks = load_tasks()
    task_id = int(listbox.get(idx).split('|')[0].strip())
    for t in tasks:
        if t['id'] == task_id:
            t['completed'] = True
            break
    save_tasks(tasks)
    update_listbox()

# Открывает форму редактирования выбранной задачи
def edit_task(event=None):
    selected_idx = listbox.curselection()
    if not selected_idx:
        return
    idx = selected_idx[0]
    task_data = listbox.get(idx).split('|')
    task_id = int(task_data[0].strip())
    title = task_data[2].strip()
    deadline = task_data[-1].strip()[len('Deadline: '):]
    
    edit_window = tk.Toplevel(root)
    edit_window.title("Редактирование задачи")
    edit_window.configure(bg=BG_COLOR)
    
    label_edit_title = tk.Label(edit_window, text="Название:", bg=BG_COLOR, fg=TEXT_COLOR)
    label_edit_title.pack()
    entry_edit_title = tk.Entry(edit_window)
    entry_edit_title.insert(0, title)
    entry_edit_title.pack()
    
    label_edit_deadline = tk.Label(edit_window, text="Срок выполнения:", bg=BG_COLOR, fg=TEXT_COLOR)
    label_edit_deadline.pack()
    entry_edit_deadline = tk.Entry(edit_window)
    entry_edit_deadline.insert(0, deadline)
    entry_edit_deadline.pack()
    
    def save_edited_task():
        edited_title = entry_edit_title.get()
        edited_deadline = entry_edit_deadline.get()
        try:
            edited_deadline_dt = datetime.strptime(edited_deadline, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Ошибка", "Неправильный формат даты. Используйте ГГГГ-ММ-ДД ЧЧ:ММ.")
            return
            
        tasks = load_tasks()
        for t in tasks:
            if t['id'] == task_id:
                t['title'] = edited_title
                t['deadline'] = edited_deadline_dt.isoformat()
                t['priority'] = set_priority_by_deadline(edited_deadline_dt.isoformat())
                break
        save_tasks(tasks)
        update_listbox()
        edit_window.destroy()
    
    button_save = tk.Button(edit_window, text="Сохранить", command=save_edited_task, bg=BUTTON_BG, fg='white')
    button_save.pack()

# Основная логика программы
root = tk.Tk()
root.title("Менеджер задач")
root.geometry("600x400")
root.config(bg=BG_COLOR)

label_title = tk.Label(root, text="Новая задача:", font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR)
label_title.grid(row=0, column=0, sticky="W", padx=10, pady=(10, 0))

entry_title = tk.Entry(root, width=40)
entry_title.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10))

label_deadline = tk.Label(root, text="Срок выполнения (ГГГГ-ММ-ДД ЧЧ:ММ):", font=("Arial", 12), bg=BG_COLOR, fg=TEXT_COLOR)
label_deadline.grid(row=2, column=0, sticky="W", padx=10)

entry_deadline = tk.Entry(root, width=40)
entry_deadline.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10))

button_add = tk.Button(root, text="Добавить задачу", command=add_task, bg=BUTTON_BG, fg='white')
button_add.grid(row=4, column=0, columnspan=2, pady=(0, 10))

# Список задач
frame_tasks = tk.Frame(root, bg=BG_COLOR)
frame_tasks.grid(row=5, column=0, columnspan=2, sticky="WE", pady=(10, 0))

scrollbar = tk.Scrollbar(frame_tasks)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame_tasks, yscrollcommand=scrollbar.set, height=10, selectmode=tk.SINGLE, bg=BG_COLOR, fg=TEXT_COLOR)
listbox.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox.yview)

update_listbox()

# Кнопки
button_complete = tk.Button(root, text="Отметить выполнено", command=complete_task, bg=BUTTON_BG, fg='white')
button_complete.grid(row=6, column=0, pady=(10, 0))

button_edit = tk.Button(root, text="Редактировать задачу", command=edit_task, bg=BUTTON_BG, fg='white')
button_edit.grid(row=6, column=1, pady=(10, 0))

# Настройка стиля
for widget in root.winfo_children():
    widget.grid_configure(sticky="we")

# Связываем события двойного клика с редактированием задачи
listbox.bind("<Double-Button-1>", edit_task)

root.mainloop()