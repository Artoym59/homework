import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font as tkFont

class TodoAppGUI:
    def __init__(self, root):
        self.root = root
        self.filename = "tasks.json"
        self.tasks = self.load_tasks()
        self.update_priorities_based_on_deadline()
        
        # Настройка цветовой схемы
        self.colors = {
            'bg_main': '#f5fff5',
            'bg_light': '#ffffff',
            'bg_dark': '#e8f5e9',
            'primary': '#6bcf7f',
            'primary_dark': '#4baf5f',
            'primary_light': '#a8e6a3',
            'text_dark': '#2d5a2d',
            'text_light': '#5a7d5a',
            'border': '#c8e6c9',
            'high_priority': '#ff6b6b',
            'medium_priority': '#ffd93d',
            'low_priority': '#6bcf7f',
            'overdue': '#8b0000',
            'completed': '#808080'
        }
        
        self.setup_ui()
        
    def load_tasks(self) -> List[Dict[str, Any]]:
        """Загрузить задачи из JSON файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    tasks = json.load(f)
                    for task in tasks:
                        if task.get('deadline'):
                            try:
                                task['deadline_datetime'] = datetime.strptime(
                                    task['deadline'], "%Y-%m-%d %H:%M:%S"
                                )
                            except:
                                task['deadline_datetime'] = None
                    return tasks
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_tasks(self) -> None:
        """Сохранить задачи в JSON файл"""
        tasks_to_save = []
        for task in self.tasks:
            task_copy = task.copy()
            if 'deadline_datetime' in task_copy:
                del task_copy['deadline_datetime']
            tasks_to_save.append(task_copy)
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(tasks_to_save, f, ensure_ascii=False, indent=2)
    
    def update_priorities_based_on_deadline(self) -> None:
        """Автоматически обновить приоритеты на основе дедлайнов"""
        now = datetime.now()
        
        for task in self.tasks:
            if task.get('deadline') and not task['completed']:
                try:
                    deadline = datetime.strptime(task['deadline'], "%Y-%m-%d %H:%M:%S")
                    time_left = deadline - now
                    
                    if 0 <= time_left.total_seconds() <= 4 * 3600:
                        task['priority'] = 'high'
                        task['auto_priority'] = True
                    elif time_left.total_seconds() < 0:
                        task['priority'] = 'overdue'
                        task['auto_priority'] = True
                except:
                    continue
    
    def calculate_time_left(self, deadline_str: str) -> str:
        """Рассчитать оставшееся время до дедлайна"""
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            time_left = deadline - now
            
            if time_left.total_seconds() < 0:
                days = abs(time_left.days)
                hours = abs(time_left.seconds // 3600)
                return f"⌛ Просрочено на {days}д {hours}ч"
            
            days = time_left.days
            hours = time_left.seconds // 3600
            minutes = (time_left.seconds % 3600) // 60
            
            if days > 0:
                return f"⏳ Осталось: {days}д {hours}ч"
            elif hours > 0:
                return f"⏳ Осталось: {hours}ч {minutes}м"
            else:
                return f"🚨 Осталось: {minutes}м"
        except:
            return "⏳ Нет данных"
    
    def get_priority_icon(self, priority: str) -> str:
        """Получить иконку для приоритета"""
        icons = {
            'high': '🔴',
            'medium': '🟡', 
            'low': '🟢',
            'overdue': '💀'
        }
        return icons.get(priority, '⚪')
    
    def get_priority_name(self, priority: str) -> str:
        """Получить русское название приоритета"""
        names = {
            'high': 'Высокий',
            'medium': 'Средний',
            'low': 'Низкий',
            'overdue': 'Просрочено'
        }
        return names.get(priority, 'Не задан')
    
    def validate_date(self, date_str: str) -> bool:
        """Проверить корректность даты в формате YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def validate_time(self, time_str: str) -> bool:
        """Проверить корректность времени в формате HH:MM"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
    
    def setup_ui(self):
        """Настройка графического интерфейса"""
        self.root.title("🌿 Менеджер задач с приоритетами")
        self.root.geometry("1300x700")
        self.root.configure(bg=self.colors['bg_main'])
        
        # Настраиваем стили
        self.setup_styles()
        
        # Создаем основной контейнер
        main_container = Frame(self.root, bg=self.colors['bg_main'])
        main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель (форма добавления/редактирования)
        left_panel = Frame(main_container, bg=self.colors['bg_main'])
        left_panel.pack(side=LEFT, fill=Y, padx=(0, 10))
        
        # Правая панель (список задач)
        right_panel = Frame(main_container, bg=self.colors['bg_main'])
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # ===== ЛЕВАЯ ПАНЕЛЬ =====
        
        # Заголовок
        title_label = Label(
            left_panel,
            text="🌿 Менеджер задач",
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark']
        )
        title_label.pack(pady=(0, 20))
        
        # Группа добавления задачи
        add_frame = LabelFrame(
            left_panel,
            text="➕ Добавить новую задачу",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            relief=GROOVE,
            bd=2
        )
        add_frame.pack(fill=X, pady=(0, 15))
        
        # Описание задачи
        Label(
            add_frame,
            text="Описание задачи:",
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 9)
        ).pack(anchor=W, padx=10, pady=(10, 5))
        
        self.description_text = Text(add_frame, height=4, width=30, font=('Segoe UI', 9))
        self.description_text.pack(padx=10, fill=X)
        
        # Приоритет
        Label(
            add_frame,
            text="Приоритет:",
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 9)
        ).pack(anchor=W, padx=10, pady=(10, 5))
        
        self.priority_var = StringVar(value="🟢 Низкий")
        priority_combo = ttk.Combobox(
            add_frame,
            textvariable=self.priority_var,
            values=["🟢 Низкий", "🟡 Средний", "🔴 Высокий"],
            state="readonly",
            font=('Segoe UI', 9)
        )
        priority_combo.pack(padx=10, fill=X, pady=(0, 10))
        
        # Дедлайн
        deadline_frame = Frame(add_frame, bg=self.colors['bg_main'])
        deadline_frame.pack(fill=X, padx=10, pady=(0, 5))
        
        self.deadline_var = BooleanVar(value=False)
        deadline_check = Checkbutton(
            deadline_frame,
            text="Установить дедлайн",
            variable=self.deadline_var,
            command=self.toggle_deadline_inputs,
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 9),
            activebackground=self.colors['bg_main']
        )
        deadline_check.pack(side=LEFT)
        
        # Поля для даты и времени
        self.datetime_frame = Frame(add_frame, bg=self.colors['bg_main'])
        self.datetime_frame.pack(fill=X, padx=10, pady=(5, 10))
        
        # Дата
        date_frame = Frame(self.datetime_frame, bg=self.colors['bg_main'])
        date_frame.pack(side=LEFT, padx=(0, 15))
        
        Label(
            date_frame,
            text="Дата (ГГГГ-ММ-ДД):",
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 8)
        ).pack(anchor=W)
        
        # Получаем текущую дату для подсказки
        today = datetime.now().strftime("%Y-%m-%d")
        self.date_var = StringVar(value=today)
        date_entry = Entry(
            date_frame,
            textvariable=self.date_var,
            width=12,
            font=('Segoe UI', 9)
        )
        date_entry.pack()
        
        # Время
        time_frame = Frame(self.datetime_frame, bg=self.colors['bg_main'])
        time_frame.pack(side=LEFT)
        
        Label(
            time_frame,
            text="Время (ЧЧ:ММ):",
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 8)
        ).pack(anchor=W)
        
        self.time_var = StringVar(value="12:00")
        time_entry = Entry(
            time_frame,
            textvariable=self.time_var,
            width=8,
            font=('Segoe UI', 9)
        )
        time_entry.pack()
        
        self.datetime_frame.pack_forget()  # Скрываем по умолчанию
        
        # Кнопка добавления
        add_button = Button(
            add_frame,
            text="➕ Добавить задачу",
            command=self.add_task,
            bg=self.colors['primary'],
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief=FLAT,
            padx=20,
            pady=8
        )
        add_button.pack(pady=(5, 15), padx=10, fill=X)
        
        # Группа редактирования задачи
        edit_frame = LabelFrame(
            left_panel,
            text="✏️ Редактировать задачу",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            relief=GROOVE,
            bd=2
        )
        edit_frame.pack(fill=X, pady=(0, 15))
        
        # ID задачи
        Label(
            edit_frame,
            text="ID задачи для редактирования:",
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 9)
        ).pack(anchor=W, padx=10, pady=(10, 5))
        
        self.edit_id_var = StringVar()
        edit_id_entry = Entry(
            edit_frame,
            textvariable=self.edit_id_var,
            font=('Segoe UI', 9)
        )
        edit_id_entry.pack(padx=10, fill=X, pady=(0, 10))
        
        # Кнопки редактирования
        button_frame = Frame(edit_frame, bg=self.colors['bg_main'])
        button_frame.pack(fill=X, padx=10, pady=(0, 10))
        
        Button(
            button_frame,
            text="✏️ Редактировать",
            command=self.edit_task_dialog,
            bg=self.colors['primary_light'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 9, 'bold'),
            relief=FLAT,
            width=12
        ).pack(side=LEFT, padx=(0, 5))
        
        Button(
            button_frame,
            text="✅ Выполнено",
            command=self.complete_task,
            bg=self.colors['primary_light'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 9, 'bold'),
            relief=FLAT,
            width=12
        ).pack(side=LEFT, padx=5)
        
        Button(
            button_frame,
            text="🗑️ Удалить",
            command=self.delete_task,
            bg=self.colors['high_priority'],
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief=FLAT,
            width=12
        ).pack(side=LEFT, padx=(5, 0))
        
        # Статистика
        stats_frame = LabelFrame(
            left_panel,
            text="📊 Статистика",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            relief=GROOVE,
            bd=2
        )
        stats_frame.pack(fill=X, pady=(0, 15))
        
        self.stats_label = Label(
            stats_frame,
            text="",
            bg=self.colors['bg_dark'],
            fg=self.colors['text_light'],
            font=('Segoe UI', 9),
            justify=LEFT,
            relief=SUNKEN,
            bd=1,
            padx=10,
            pady=10
        )
        self.stats_label.pack(fill=X, padx=5, pady=5)
        
        # Кнопка обновления
        refresh_button = Button(
            left_panel,
            text="🔄 Обновить приоритеты",
            command=self.refresh_tasks,
            bg=self.colors['primary_light'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 10, 'bold'),
            relief=FLAT,
            pady=8
        )
        refresh_button.pack(fill=X, pady=(0, 10))
        
        # ===== ПРАВАЯ ПАНЕЛЬ =====
        
        # Панель фильтров
        filter_frame = Frame(right_panel, bg=self.colors['bg_main'])
        filter_frame.pack(fill=X, pady=(0, 10))
        
        Label(
            filter_frame,
            text="Фильтры:",
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 10, 'bold')
        ).pack(side=LEFT, padx=(0, 10))
        
        self.show_completed_var = BooleanVar(value=True)
        show_completed_check = Checkbutton(
            filter_frame,
            text="Показать выполненные",
            variable=self.show_completed_var,
            command=self.refresh_task_list,
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 9),
            activebackground=self.colors['bg_main']
        )
        show_completed_check.pack(side=LEFT, padx=(0, 20))
        
        Label(
            filter_frame,
            text="Сортировка:",
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 10, 'bold')
        ).pack(side=LEFT, padx=(0, 10))
        
        self.sort_var = StringVar(value="По приоритету")
        sort_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.sort_var,
            values=["По приоритету", "По дедлайну", "По ID"],
            state="readonly",
            font=('Segoe UI', 9),
            width=15
        )
        sort_combo.pack(side=LEFT)
        sort_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_task_list())
        
        # Список задач
        list_frame = Frame(right_panel, bg=self.colors['bg_main'])
        list_frame.pack(fill=BOTH, expand=True)
        
        # Scrollbar для списка
        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Treeview для отображения задач
        self.task_tree = ttk.Treeview(
            list_frame,
            columns=('ID', 'Статус', 'Приоритет', 'Описание', 'Дедлайн', 'Осталось', 'Создано'),
            show='headings',
            yscrollcommand=scrollbar.set,
            height=20
        )
        
        # Настройка колонок
        columns = [
            ('ID', 50),
            ('Статус', 60),
            ('Приоритет', 100),
            ('Описание', 300),
            ('Дедлайн', 150),
            ('Осталось', 150),
            ('Создано', 150)
        ]
        
        for col, width in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=width, minwidth=width)
        
        self.task_tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.task_tree.yview)
        
        # Настройка стилей Treeview
        self.setup_treeview_style()
        
        # Привязываем двойной клик для редактирования
        self.task_tree.bind('<Double-Button-1>', self.on_task_double_click)
        
        # Обновляем список задач
        self.refresh_task_list()
        
        # Связываем закрытие окна с сохранением
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настройка Treeview
        style.configure(
            "Treeview",
            background=self.colors['bg_light'],
            foreground=self.colors['text_dark'],
            rowheight=25,
            fieldbackground=self.colors['bg_light'],
            borderwidth=1,
            relief="solid"
        )
        
        style.map(
            "Treeview",
            background=[('selected', self.colors['primary_light'])],
            foreground=[('selected', self.colors['text_dark'])]
        )
        
        style.configure(
            "Treeview.Heading",
            background=self.colors['primary'],
            foreground='white',
            relief="flat",
            font=('Segoe UI', 9, 'bold')
        )
        
        style.map(
            "Treeview.Heading",
            background=[('active', self.colors['primary_dark'])]
        )
    
    def setup_treeview_style(self):
        """Настройка тегов для Treeview"""
        self.task_tree.tag_configure('completed', foreground=self.colors['completed'])
        self.task_tree.tag_configure('high', background='#fff0f0')
        self.task_tree.tag_configure('medium', background='#fff8e6')
        self.task_tree.tag_configure('low', background='#f0fff0')
        self.task_tree.tag_configure('overdue', background='#ffe6e6', foreground='#8b0000')
    
    def toggle_deadline_inputs(self):
        """Включить/выключить поля для ввода дедлайна"""
        if self.deadline_var.get():
            self.datetime_frame.pack(fill=X, padx=10, pady=(5, 10))
        else:
            self.datetime_frame.pack_forget()
    
    def refresh_task_list(self):
        """Обновить список задач"""
        # Очищаем текущий список
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        show_completed = self.show_completed_var.get()
        sort_by = self.sort_var.get()
        
        # Фильтруем задачи
        filtered_tasks = [task for task in self.tasks if show_completed or not task["completed"]]
        
        # Сортируем
        priority_order = {'overdue': 0, 'high': 1, 'medium': 2, 'low': 3}
        
        if sort_by == "По приоритету":
            filtered_tasks.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))
        elif sort_by == "По дедлайну":
            filtered_tasks.sort(key=lambda x: (
                x.get('deadline_datetime') or datetime.max,
                priority_order.get(x.get('priority', 'low'), 3)
            ))
        elif sort_by == "По ID":
            filtered_tasks.sort(key=lambda x: x['id'])
        
        # Добавляем задачи в Treeview
        for task in filtered_tasks:
            status = "✅" if task["completed"] else "⏳"
            priority_icon = self.get_priority_icon(task.get('priority', 'medium'))
            priority_name = self.get_priority_name(task.get('priority', 'medium'))
            
            # Форматируем дедлайн и оставшееся время
            deadline_text = task.get('deadline', 'Нет')
            time_left_text = ""
            
            if task.get('deadline'):
                time_left_text = self.calculate_time_left(task['deadline'])
            
            # Определяем теги для стилизации
            tags = []
            if task["completed"]:
                tags.append('completed')
            else:
                priority = task.get('priority', 'low')
                tags.append(priority)
                if task.get('auto_priority'):
                    priority_name += " (авто)"
            
            # Добавляем запись
            self.task_tree.insert(
                '', 'end',
                values=(
                    task['id'],
                    status,
                    f"{priority_icon} {priority_name}",
                    task['description'],
                    deadline_text,
                    time_left_text,
                    task['created_at']
                ),
                tags=tags
            )
        
        # Обновляем статистику
        self.update_stats()
    
    def update_stats(self):
        """Обновить статистику"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        pending = total - completed
        
        high_priority = sum(1 for t in self.tasks if t.get('priority') == 'high' and not t['completed'])
        medium_priority = sum(1 for t in self.tasks if t.get('priority') == 'medium' and not t['completed'])
        low_priority = sum(1 for t in self.tasks if t.get('priority') == 'low' and not t['completed'])
        overdue = sum(1 for t in self.tasks if t.get('priority') == 'overdue' and not t['completed'])
        
        stats_text = f"📊 Всего задач: {total}\n"
        stats_text += f"📈 Выполнено: {completed}\n"
        stats_text += f"📉 Осталось: {pending}\n"
        stats_text += f"🔴 Высокий приоритет: {high_priority}\n"
        stats_text += f"🟡 Средний приоритет: {medium_priority}\n"
        stats_text += f"🟢 Низкий приоритет: {low_priority}"
        
        if overdue > 0:
            stats_text += f"\n💀 Просрочено: {overdue}"
        
        self.stats_label.config(text=stats_text)
    
    def add_task(self):
        """Добавить новую задачу"""
        description = self.description_text.get("1.0", "end-1c").strip()
        if not description:
            messagebox.showwarning("Ошибка", "Описание задачи не может быть пустым!")
            return
        
        # Получаем приоритет
        priority_text = self.priority_var.get()
        priority_map = {
            "🟢 Низкий": "low",
            "🟡 Средний": "medium", 
            "🔴 Высокий": "high"
        }
        priority = priority_map.get(priority_text, "medium")
        
        # Получаем дедлайн
        deadline = None
        if self.deadline_var.get():
            date_str = self.date_var.get().strip()
            time_str = self.time_var.get().strip()
            
            # Проверяем формат даты и времени
            if not self.validate_date(date_str):
                messagebox.showwarning("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
                return
            
            if not self.validate_time(time_str):
                messagebox.showwarning("Ошибка", "Неверный формат времени! Используйте ЧЧ:ММ")
                return
            
            deadline = f"{date_str} {time_str}:00"
        
        # Добавляем задачу
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "completed": False,
            "priority": priority,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": None,
            "deadline": deadline,
            "auto_priority": False
        }
        
        if deadline:
            try:
                task['deadline_datetime'] = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
                now = datetime.now()
                deadline_dt = task['deadline_datetime']
                time_left = deadline_dt - now
                
                if 0 <= time_left.total_seconds() <= 4 * 3600:
                    task['priority'] = 'high'
                    task['auto_priority'] = True
                elif time_left.total_seconds() < 0:
                    task['priority'] = 'overdue'
                    task['auto_priority'] = True
            except:
                task['deadline_datetime'] = None
        
        self.tasks.append(task)
        self.save_tasks()
        
        # Очищаем поля ввода
        self.description_text.delete("1.0", END)
        self.deadline_var.set(False)
        self.toggle_deadline_inputs()
        
        # Обновляем список
        self.refresh_task_list()
        
        messagebox.showinfo("Успех", f"✅ Задача добавлена (ID: {task['id']})")
    
    def on_task_double_click(self, event):
        """Обработчик двойного клика по задаче"""
        selection = self.task_tree.selection()
        if selection:
            item = self.task_tree.item(selection[0])
            task_id = int(item['values'][0])
            self.edit_id_var.set(str(task_id))
            self.edit_task_dialog()
    
    def edit_task_dialog(self):
        """Открыть диалог редактирования задачи"""
        try:
            task_id = int(self.edit_id_var.get().strip())
        except ValueError:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите числовой ID")
            return
        
        # Ищем задачу
        task = None
        for t in self.tasks:
            if t["id"] == task_id:
                task = t
                break
        
        if not task:
            messagebox.showwarning("Ошибка", f"Задача с ID {task_id} не найдена")
            return
        
        # Создаем диалоговое окно
        dialog = Toplevel(self.root)
        dialog.title(f"✏️ Редактирование задачи ID: {task_id}")
        dialog.geometry("500x500")
        dialog.configure(bg=self.colors['bg_main'])
        dialog.resizable(False, False)
        
        # Центрируем диалог
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Заголовок
        Label(
            dialog,
            text=f"Редактирование задачи ID: {task_id}",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark']
        ).pack(pady=(20, 10))
        
        # Форма редактирования
        form_frame = Frame(dialog, bg=self.colors['bg_main'])
        form_frame.pack(fill=BOTH, expand=True, padx=30, pady=10)
        
        # Описание
        Label(
            form_frame,
            text="Описание:",
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 9)
        ).pack(anchor=W, pady=(0, 5))
        
        desc_text = Text(form_frame, height=4, font=('Segoe UI', 9))
        desc_text.insert("1.0", task["description"])
        desc_text.pack(fill=X, pady=(0, 15))
        
        # Приоритет
        Label(
            form_frame,
            text="Приоритет:",
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 9)
        ).pack(anchor=W, pady=(0, 5))
        
        priority_var = StringVar()
        priority_combo = ttk.Combobox(
            form_frame,
            textvariable=priority_var,
            values=["🟢 Низкий", "🟡 Средний", "🔴 Высокий"],
            state="readonly",
            font=('Segoe UI', 9)
        )
        
        priority_map_reverse = {'low': "🟢 Низкий", 'medium': "🟡 Средний", 'high': "🔴 Высокий"}
        priority_var.set(priority_map_reverse.get(task.get('priority', 'medium'), "🟡 Средний"))
        priority_combo.pack(fill=X, pady=(0, 15))
        
        # Дедлайн
        deadline_frame = Frame(form_frame, bg=self.colors['bg_main'])
        deadline_frame.pack(fill=X, pady=(0, 5))
        
        deadline_var = BooleanVar(value=bool(task.get('deadline')))
        deadline_check = Checkbutton(
            deadline_frame,
            text="Установить дедлайн",
            variable=deadline_var,
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 9),
            activebackground=self.colors['bg_main']
        )
        deadline_check.pack(side=LEFT)
        
        # Поля для даты и времени
        datetime_frame = Frame(form_frame, bg=self.colors['bg_main'])
        
        # Дата
        date_frame = Frame(datetime_frame, bg=self.colors['bg_main'])
        date_frame.pack(side=LEFT, padx=(0, 15))
        
        Label(
            date_frame,
            text="Дата (ГГГГ-ММ-ДД):",
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 8)
        ).pack(anchor=W)
        
        date_var = StringVar()
        date_entry = Entry(
            date_frame,
            textvariable=date_var,
            width=12,
            font=('Segoe UI', 9)
        )
        date_entry.pack()
        
        # Время
        time_frame = Frame(datetime_frame, bg=self.colors['bg_main'])
        time_frame.pack(side=LEFT)
        
        Label(
            time_frame,
            text="Время (ЧЧ:ММ):",
            bg=self.colors['bg_main'],
            fg=self.colors['text_dark'],
            font=('Segoe UI', 8)
        ).pack(anchor=W)
        
        time_var = StringVar()
        time_entry = Entry(
            time_frame,
            textvariable=time_var,
            width=8,
            font=('Segoe UI', 9)
        )
        time_entry.pack()
        
        # Заполняем значения, если дедлайн уже установлен
        if task.get('deadline'):
            try:
                dt = datetime.strptime(task['deadline'], "%Y-%m-%d %H:%M:%S")
                date_var.set(dt.strftime("%Y-%m-%d"))
                time_var.set(dt.strftime("%H:%M"))
                datetime_frame.pack(fill=X, pady=(5, 15))
            except:
                date_var.set(datetime.now().strftime("%Y-%m-%d"))
                time_var.set("12:00")
                if deadline_var.get():
                    datetime_frame.pack(fill=X, pady=(5, 15))
        else:
            date_var.set(datetime.now().strftime("%Y-%m-%d"))
            time_var.set("12:00")
            datetime_frame.pack_forget()
        
        # Функция для показа/скрытия полей даты
        def toggle_datetime():
            if deadline_var.get():
                datetime_frame.pack(fill=X, pady=(5, 15))
            else:
                datetime_frame.pack_forget()
        
        deadline_check.config(command=toggle_datetime)
        
        # Кнопки
        button_frame = Frame(dialog, bg=self.colors['bg_main'])
        button_frame.pack(fill=X, padx=30, pady=(0, 20))
        
        def save_changes():
            # Валидация даты и времени
            if deadline_var.get():
                if not self.validate_date(date_var.get()):
                    messagebox.showwarning("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
                    return
                
                if not self.validate_time(time_var.get()):
                    messagebox.showwarning("Ошибка", "Неверный формат времени! Используйте ЧЧ:ММ")
                    return
            
            self.save_edit(
                task_id,
                desc_text.get("1.0", "end-1c"),
                priority_var.get(),
                deadline_var.get(),
                date_var.get(),
                time_var.get(),
                dialog
            )
        
        Button(
            button_frame,
            text="💾 Сохранить",
            command=save_changes,
            bg=self.colors['primary'],
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief=FLAT,
            width=15
        ).pack(side=LEFT, padx=(0, 10))
        
        Button(
            button_frame,
            text="❌ Отмена",
            command=dialog.destroy,
            bg=self.colors['high_priority'],
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief=FLAT,
            width=15
        ).pack(side=LEFT)
    
    def save_edit(self, task_id, description, priority_text, has_deadline, date_str, time_str, dialog):
        """Сохранить изменения в задаче"""
        if not description.strip():
            messagebox.showwarning("Ошибка", "Описание задачи не может быть пустым!")
            return
        
        # Находим задачу
        for task in self.tasks:
            if task["id"] == task_id:
                task["description"] = description.strip()
                
                priority_map = {
                    "🟢 Низкий": "low",
                    "🟡 Средний": "medium", 
                    "🔴 Высокий": "high"
                }
                task["priority"] = priority_map.get(priority_text, "medium")
                task["auto_priority"] = False
                
                if has_deadline:
                    deadline = f"{date_str} {time_str}:00"
                    try:
                        task["deadline"] = deadline
                        task['deadline_datetime'] = datetime.strptime(
                            task["deadline"], "%Y-%m-%d %H:%M:%S"
                        )
                    except ValueError:
                        messagebox.showwarning("Ошибка", "Неверный формат даты или времени!")
                        return
                else:
                    task["deadline"] = None
                    task['deadline_datetime'] = None
                
                self.update_priorities_based_on_deadline()
                self.save_tasks()
                self.refresh_task_list()
                
                dialog.destroy()
                messagebox.showinfo("Успех", "✅ Задача обновлена!")
                return
    
    def complete_task(self):
        """Отметить задачу как выполненную"""
        try:
            task_id = int(self.edit_id_var.get().strip())
        except ValueError:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите числовой ID")
            return
        
        for task in self.tasks:
            if task["id"] == task_id:
                if not task["completed"]:
                    task["completed"] = True
                    task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_tasks()
                    self.refresh_task_list()
                    messagebox.showinfo("Успех", f"✅ Задача ID {task_id} отмечена как выполненная!")
                else:
                    messagebox.showinfo("Информация", f"ℹ️ Задача ID {task_id} уже была выполнена")
                return
        
        messagebox.showwarning("Ошибка", f"Задача с ID {task_id} не найдена")
    
    def delete_task(self):
        """Удалить задачу"""
        try:
            task_id = int(self.edit_id_var.get().strip())
        except ValueError:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите числовой ID")
            return
        
        confirm = messagebox.askyesno(
            "Подтверждение",
            f"Вы действительно хотите удалить задачу ID {task_id}?"
        )
        
        if confirm:
            for i, task in enumerate(self.tasks):
                if task["id"] == task_id:
                    self.tasks.pop(i)
                    self.save_tasks()
                    self.refresh_task_list()
                    messagebox.showinfo("Успех", f"🗑️ Задача ID {task_id} удалена!")
                    return
        
        messagebox.showwarning("Ошибка", f"Задача с ID {task_id} не найдена")
    
    def refresh_tasks(self):
        """Обновить приоритеты и список задач"""
        self.update_priorities_based_on_deadline()
        self.save_tasks()
        self.refresh_task_list()
        messagebox.showinfo("Успех", "🔄 Приоритеты обновлены на основе дедлайнов!")
    
    def on_closing(self):
        """Обработчик закрытия окна"""
        self.save_tasks()
        self.root.destroy()

def main():
    root = Tk()
    app = TodoAppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()