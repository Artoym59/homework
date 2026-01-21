import json
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

DB_FILE = "todo_gui_light.json"
DATE_FORMAT = "%d.%m.%Y %H:%M"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Green Task Manager 2026")
        self.root.geometry("650x550")
        
        # Цветовая палитра (Светлая)
        self.bg_main = "#FFFFFF"        # Чистый белый фон
        self.bg_accent = "#F0F9F0"      # Очень светлый зеленый для полей
        self.fg_main = "#2D3436"        # Темно-серый текст (лучше читается, чем черный)
        self.brand_green = "#27AE60"    # Насыщенный зеленый акцент
        self.light_green = "#DFF9FB"    # Цвет выделения
        
        self.root.configure(bg=self.bg_main)
        self.tasks = self.load_tasks()
        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        # Заголовок
        header_frame = tk.Frame(self.root, bg=self.brand_green)
        header_frame.pack(fill="x", pady=(0, 20))
        
        label = tk.Label(header_frame, text="Мои Задачи", font=("Segoe UI", 18, "bold"),
                         bg=self.brand_green, fg="white", pady=15)
        label.pack()

        # Фрейм для ввода
        input_frame = tk.Frame(self.root, bg=self.bg_main)
        input_frame.pack(pady=10, padx=30, fill="x")

        # Поле задачи
        tk.Label(input_frame, text="Что нужно сделать?", font=("Segoe UI", 10),
                 bg=self.bg_main, fg=self.fg_main).grid(row=0, column=0, sticky="w")
        self.task_entry = tk.Entry(input_frame, bg=self.bg_accent, fg=self.fg_main, 
                                   font=("Segoe UI", 11), borderwidth=1, relief="flat")
        self.task_entry.grid(row=1, column=0, padx=(0, 10), pady=(5, 15), sticky="ew")

        # Поле дедлайна
        tk.Label(input_frame, text="Дедлайн (ДД.ММ.ГГГГ ЧЧ:ММ)", font=("Segoe UI", 10),
                 bg=self.bg_main, fg=self.fg_main).grid(row=0, column=1, sticky="w")
        self.deadline_entry = tk.Entry(input_frame, bg=self.bg_accent, fg=self.fg_main, 
                                       font=("Segoe UI", 11), borderwidth=1, relief="flat")
        self.deadline_entry.grid(row=1, column=1, pady=(5, 15), sticky="ew")
        
        input_frame.columnconfigure(0, weight=3)
        input_frame.columnconfigure(1, weight=2)

        # Кнопки управления
        btn_frame = tk.Frame(self.root, bg=self.bg_main)
        btn_frame.pack(pady=10)

        style_btn = {"font": ("Segoe UI", 9, "bold"), "fg": "white", "relief": "flat", "padx": 15, "pady": 5}

        self.add_btn = tk.Button(btn_frame, text="ДОБАВИТЬ", command=self.add_task, 
                                 bg=self.brand_green, activebackground="#219150", **style_btn)
        self.add_btn.pack(side="left", padx=5)

        self.done_btn = tk.Button(btn_frame, text="ВЫПОЛНЕНО", command=self.mark_done, 
                                  bg="#2980B9", activebackground="#2471A3", **style_btn)
        self.done_btn.pack(side="left", padx=5)

        self.del_btn = tk.Button(btn_frame, text="УДАЛИТЬ", command=self.delete_task, 
                                 bg="#E74C3C", activebackground="#C0392B", **style_btn)
        self.del_btn.pack(side="left", padx=5)

        # Список задач
        list_frame = tk.Frame(self.root, bg=self.bg_main)
        list_frame.pack(pady=10, padx=30, fill="both", expand=True)

        self.listbox = tk.Listbox(list_frame, bg=self.bg_accent, fg=self.fg_main, 
                                  selectbackground=self.brand_green, selectforeground="white",
                                  font=("Segoe UI", 11), borderwidth=0, highlightthickness=0)
        self.listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

    def load_tasks(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_tasks(self):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def check_priority(self, deadline_str):
        if not deadline_str: return "ПЛАН", 3
        try:
            deadline = datetime.strptime(deadline_str, DATE_FORMAT)
            diff = deadline - datetime.now()
            if diff < timedelta(hours=4):
                return "СРОЧНО!", 1
            return "В СРОК", 2
        except:
            return "БЕЗ ДАТЫ", 4

    def add_task(self):
        text = self.task_entry.get()
        deadline = self.deadline_entry.get()
        if not text:
            messagebox.showwarning("Ввод", "Напишите, что нужно сделать")
            return

        p_name, p_val = self.check_priority(deadline)
        self.tasks.append({
            "text": text,
            "deadline": deadline,
            "done": False
        })
        self.save_tasks()
        self.task_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        # Сортировка по дедлайну и статусу выполнения
        self.tasks.sort(key=lambda x: (x['done'], self.check_priority(x['deadline'])[1]))
        
        for task in self.tasks:
            status = "✓" if task["done"] else "○"
            p_name, _ = self.check_priority(task["deadline"])
            deadline_info = f" [до {task['deadline']}]" if task['deadline'] else ""
            
            # Визуальный разделитель
            display_text = f" {status}  {p_name.ljust(8)} | {task['text']}{deadline_info}"
            self.listbox.insert(tk.END, display_text)
            
            # Подкрашиваем срочные задачи красным в списке (опционально)
            if p_name == "СРОЧНО!" and not task["done"]:
                self.listbox.itemconfig(tk.END, fg="#E67E22")

    def mark_done(self):
        try:
            index = self.listbox.curselection()[0]
            # Нужно найти задачу в исходном списке, так как индексы Listbox и self.tasks совпадают после сортировки
            self.tasks[index]["done"] = True
            self.save_tasks()
            self.refresh_list()
        except IndexError:
            messagebox.showwarning("Выбор", "Выберите задачу для отметки")

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            del self.tasks[index]
            self.save_tasks()
            self.refresh_list()
        except IndexError:
            messagebox.showwarning("Выбор", "Выберите задачу для удаления")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()