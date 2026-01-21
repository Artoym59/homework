import json
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

FILE_NAME = "tasks.json"
DEADLINE_PRIORITY_HOURS = 4


# ---------- Работа с данными ----------

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


# ---------- GUI ----------

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TODO список")
        self.root.geometry("720x420")
        self.root.configure(bg="#e8f5e9")

        self.tasks = load_tasks()

        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        # Заголовок
        tk.Label(
            self.root,
            text="Мой список дел",
            bg="#e8f5e9",
            fg="#1b5e20",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Список задач
        self.listbox = tk.Listbox(
            self.root,
            font=("Arial", 11),
            width=100,
            height=12,
            bg="#ffffff",
            selectbackground="#a5d6a7"
        )
        self.listbox.pack(padx=15, pady=5)

        # Форма добавления
        form = tk.Frame(self.root, bg="#e8f5e9")
        form.pack(pady=10)

        tk.Label(form, text="Задача:", bg="#e8f5e9").grid(row=0, column=0)
        self.title_entry = tk.Entry(form, width=20)
        self.title_entry.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Приоритет:", bg="#e8f5e9").grid(row=0, column=2)
        self.priority_var = tk.StringVar(value="средний")
        tk.OptionMenu(form, self.priority_var, "низкий", "средний", "высокий").grid(
            row=0, column=3, padx=5
        )

        tk.Label(form, text="Дедлайн (YYYY-MM-DD HH:MM):", bg="#e8f5e9").grid(row=0, column=4)
        self.deadline_entry = tk.Entry(form, width=18)
        self.deadline_entry.grid(row=0, column=5, padx=5)

        # Кнопки
        buttons = tk.Frame(self.root, bg="#e8f5e9")
        buttons.pack(pady=10)

        tk.Button(buttons, text="➕ Добавить", bg="#66bb6a", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(buttons, text="✅ Выполнено", bg="#81c784", command=self.complete_task).grid(row=0, column=1, padx=5)
        tk.Button(buttons, text="❌ Удалить", bg="#a5d6a7", command=self.delete_task).grid(row=0, column=2, padx=5)

    def refresh_list(self):
        update_priorities(self.tasks)
        save_tasks(self.tasks)

        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task["done"] else " "
            deadline = task["deadline"] or "—"
            self.listbox.insert(
                tk.END,
                f"[{status}] {task['title']} | {task['priority']} | дедлайн: {deadline}"
            )

    def add_task(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Ошибка", "Название задачи пустое")
            return

        deadline = None
        deadline_text = self.deadline_entry.get().strip()
        if deadline_text:
            try:
                deadline = datetime.strptime(deadline_text, "%Y-%m-%d %H:%M").isoformat()
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты")
                return

        task = {
            "title": title,
            "done": False,
            "priority": self.priority_var.get(),
            "deadline": deadline
        }

        self.tasks.append(task)
        self.title_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.refresh_list()

    def complete_task(self):
        try:
            index = self.listbox.curselection()[0]
            self.tasks[index]["done"] = True
            self.refresh_list()
        except IndexError:
            messagebox.showinfo("Информация", "Выберите задачу")

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            self.tasks.pop(index)
            self.refresh_list()
        except IndexError:
            messagebox.showinfo("Информация", "Выберите задачу")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()