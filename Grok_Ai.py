import json
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

TASKS_FILE = 'tasks.json'

# ─── Цветовая схема (светлая + зелёная) ───
BG_COLOR = "#f8fdf8"           # очень светлый зелёно-белый
FRAME_BG = "#f0f9f0"
BTN_BG = "#4CAF50"             # основной зелёный
BTN_ACTIVE = "#45a049"
BTN_FG = "white"
ACCENT = "#2E7D32"             # тёмный зелёный для акцентов
TEXT_COLOR = "#1B5E20"
HIGH_PRIORITY_BG = "#fff3e0"   # светлый оранжевый для high
HIGH_PRIORITY_FG = "#d84315"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Задачи — Todo Green")
        self.root.geometry("780x580")
        self.root.configure(bg=BG_COLOR)
        
        self.tasks = load_tasks()
        
        self.style = ttk.Style()
        self.style.theme_use('clam')  # современная тема
        
        self.configure_styles()
        
        self.create_widgets()
        self.update_task_list()

    def configure_styles(self):
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.map("TButton",
            background=[('active', BTN_ACTIVE)],
            foreground=[('active', 'white')])
        
        self.style.configure("Green.TButton",
            background=BTN_BG,
            foreground=BTN_FG,
            font=("Segoe UI", 10, "bold"))
        
        self.style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR)
        self.style.configure("Header.TLabel",
            font=("Segoe UI", 14, "bold"),
            background=BG_COLOR,
            foreground=ACCENT)
        
        self.style.configure("Treeview",
            background=FRAME_BG,
            fieldbackground=FRAME_BG,
            foreground=TEXT_COLOR,
            rowheight=28)
        
        self.style.map("Treeview",
            background=[('selected', ACCENT)],
            foreground=[('selected', 'white')])
        
        self.style.configure("Treeview.Heading",
            background=BTN_BG,
            foreground="white",
            font=("Segoe UI", 10, "bold"))
        
        self.style.map("Treeview.Heading",
            background=[('active', ACCENT)])

    def create_widgets(self):
        # Заголовок
        ttk.Label(self.root, text="Мои задачи", style="Header.TLabel").pack(pady=(15, 5))
        
        # Основной фрейм со списком
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ("id", "priority", "description", "deadline", "status")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="№")
        self.tree.heading("priority", text="Приоритет")
        self.tree.heading("description", text="Задача")
        self.tree.heading("deadline", text="Дедлайн")
        self.tree.heading("status", text="Статус")
        
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("priority", width=110, anchor="center")
        self.tree.column("description", width=320)
        self.tree.column("deadline", width=140, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Панель кнопок
        btn_frame = ttk.Frame(self.root, padding=12)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(btn_frame, text="Добавить задачу", style="Green.TButton",
                   command=self.add_task_dialog).pack(side=tk.LEFT, padx=6)
        
        ttk.Button(btn_frame, text="Отметить выполненной", style="Green.TButton",
                   command=self.mark_completed).pack(side=tk.LEFT, padx=6)
        
        ttk.Button(btn_frame, text="Удалить", style="Green.TButton",
                   command=self.delete_task).pack(side=tk.LEFT, padx=6)
        
        ttk.Button(btn_frame, text="Обновить", command=self.update_task_list).pack(side=tk.RIGHT, padx=6)

    def get_priority_tag(self, priority):
        if priority == "high":
            return "high"
        elif priority == "medium":
            return "medium"
        else:
            return "low"

    def update_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        now = datetime.now()
        
        for task in self.tasks:
            # Обновляем приоритет по дедлайну
            if task.get('deadline'):
                try:
                    dl = datetime.fromisoformat(task['deadline'])
                    time_left = dl - now
                    if time_left <= timedelta(hours=4) and time_left > timedelta(0):
                        task['priority'] = 'high'
                    elif time_left <= timedelta(0):
                        task['priority'] = 'high'
                except:
                    pass
            
            status = "✓ Выполнено" if task.get('completed', False) else "В работе"
            deadline_str = ""
            if task.get('deadline'):
                try:
                    dl = datetime.fromisoformat(task['deadline'])
                    deadline_str = dl.strftime("%Y-%m-%d %H:%M")
                except:
                    deadline_str = task['deadline']
            
            values = (
                task['id'],
                task['priority'].upper(),
                task['description'],
                deadline_str,
                status
            )
            
            iid = self.tree.insert("", "end", values=values)
            
            # Теги для раскраски
            prio = task['priority']
            if prio == "high":
                self.tree.item(iid, tags=("high",))
            elif prio == "medium":
                self.tree.item(iid, tags=("medium",))
            else:
                self.tree.item(iid, tags=("low",))
            
            if task.get('completed'):
                self.tree.item(iid, tags=("completed",))
        
        # Настраиваем цвета строк
        self.tree.tag_configure("high", background=HIGH_PRIORITY_BG, foreground=HIGH_PRIORITY_FG)
        self.tree.tag_configure("medium", background="#e8f5e9")
        self.tree.tag_configure("low", background="#f1f8e9")
        self.tree.tag_configure("completed", foreground="#78909c")

    def add_task_dialog(self):
        description = simpledialog.askstring("Новая задача", "Описание задачи:")
        if not description or not description.strip():
            return
            
        deadline = simpledialog.askstring("Дедлайн", 
            "Введите дедлайн (например: 2026-01-25 18:30)\nили оставьте пустым",
            initialvalue="")
            
        priority = simpledialog.askstring("Приоритет", 
            "low / medium / high  (по умолчанию medium)",
            initialvalue="medium").strip().lower()
            
        if priority not in ("low", "medium", "high"):
            priority = "medium"
            
        deadline_iso = None
        if deadline and deadline.strip():
            try:
                # Пробуем разные форматы
                for fmt in ["%Y-%m-%d %H:%M", "%d.%m.%Y %H:%M", "%Y-%m-%d"]:
                    try:
                        dt = datetime.strptime(deadline.strip(), fmt)
                        deadline_iso = dt.isoformat()
                        break
                    except:
                        continue
            except:
                messagebox.showwarning("Формат даты", "Не удалось распознать дату.\nДедлайн не установлен.")
        
        new_task = {
            'id': len(self.tasks) + 1,
            'description': description.strip(),
            'completed': False,
            'priority': priority,
            'deadline': deadline_iso
        }
        
        self.tasks.append(new_task)
        save_tasks(self.tasks)
        self.update_task_list()
        messagebox.showinfo("Успех", "Задача добавлена!")

    def mark_completed(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите задачу")
            return
            
        item = self.tree.item(selected[0])
        task_id = int(item['values'][0])
        
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']  # можно и снимать галочку
                break
                
        save_tasks(self.tasks)
        self.update_task_list()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите задачу")
            return
            
        item = self.tree.item(selected[0])
        task_id = int(item['values'][0])
        
        if messagebox.askyesno("Удаление", f"Удалить задачу №{task_id} ?"):
            self.tasks = [t for t in self.tasks if t['id'] != task_id]
            # перенумеровываем
            for i, t in enumerate(self.tasks, 1):
                t['id'] = i
            save_tasks(self.tasks)
            self.update_task_list()

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()