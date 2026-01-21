import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class TodoApp:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()
        self.update_priorities_based_on_deadline()  # Обновляем приоритеты при загрузке
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """Загрузить задачи из JSON файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    tasks = json.load(f)
                    # Конвертируем строки дат обратно в объекты для вычислений
                    for task in tasks:
                        if task.get('deadline'):
                            try:
                                # Парсим строку даты для вычислений
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
        # Удаляем временные поля перед сохранением
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
                    
                    # Если до дедлайна меньше 4 часов, устанавливаем высокий приоритет
                    if 0 <= time_left.total_seconds() <= 4 * 3600:
                        task['priority'] = 'high'
                        task['auto_priority'] = True  # Флаг, что приоритет установлен автоматически
                    elif time_left.total_seconds() < 0:
                        # Просроченные задачи
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
            return "⏳ Нет данных о времени"
    
    def get_priority_emoji(self, priority: str) -> str:
        """Получить эмодзи для приоритета"""
        priority_emojis = {
            'high': '🔴',
            'medium': '🟡', 
            'low': '🟢',
            'overdue': '💀'
        }
        return priority_emojis.get(priority, '⚪')
    
    def get_priority_name(self, priority: str) -> str:
        """Получить русское название приоритета"""
        priority_names = {
            'high': 'Высокий',
            'medium': 'Средний',
            'low': 'Низкий',
            'overdue': 'Просрочено'
        }
        return priority_names.get(priority, 'Не задан')
    
    def add_task(self, description: str, priority: str = 'medium', deadline: Optional[str] = None) -> None:
        """Добавить новую задачу"""
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
                # Проверяем, не близкий ли дедлайн
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
        print(f"✅ Задача добавлена (ID: {task['id']}, Приоритет: {self.get_priority_name(priority)})")
    
    def delete_task(self, task_id: int) -> None:
        """Удалить задачу по ID"""
        task_to_delete = None
        
        for task in self.tasks:
            if task["id"] == task_id:
                task_to_delete = task
                break
        
        if task_to_delete:
            self.tasks.remove(task_to_delete)
            self.save_tasks()
            print(f"🗑️ Задача удалена (ID: {task_id})")
        else:
            print(f"❌ Задача с ID {task_id} не найдена")
    
    def complete_task(self, task_id: int) -> None:
        """Отметить задачу как выполненную"""
        for task in self.tasks:
            if task["id"] == task_id:
                if not task["completed"]:
                    task["completed"] = True
                    task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_tasks()
                    print(f"✅ Задача отмечена как выполненная (ID: {task_id})")
                else:
                    print(f"ℹ️ Задача уже была выполнена ранее (ID: {task_id})")
                return
        print(f"❌ Задача с ID {task_id} не найдена")
    
    def edit_task(self, task_id: int, description: Optional[str] = None, 
                  priority: Optional[str] = None, deadline: Optional[str] = None) -> None:
        """Редактировать задачу"""
        for task in self.tasks:
            if task["id"] == task_id:
                if description is not None:
                    task["description"] = description
                
                if priority is not None:
                    task["priority"] = priority
                    task["auto_priority"] = False  # Сбрасываем авто-приоритет при ручном изменении
                
                if deadline is not None:
                    task["deadline"] = deadline
                    try:
                        task['deadline_datetime'] = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
                        # Пересчитываем приоритет на основе нового дедлайна
                        self.update_priorities_based_on_deadline()
                    except:
                        task['deadline_datetime'] = None
                
                self.save_tasks()
                print(f"✏️ Задача обновлена (ID: {task_id})")
                return
        print(f"❌ Задача с ID {task_id} не найдена")
    
    def list_tasks(self, show_completed: bool = True, sort_by: str = 'priority') -> None:
        """Вывести список задач"""
        if not self.tasks:
            print("📝 Список задач пуст")
            return
        
        # Фильтруем задачи
        filtered_tasks = [task for task in self.tasks if show_completed or not task["completed"]]
        
        if not filtered_tasks:
            print("📝 Нет задач для отображения")
            return
        
        # Сортируем задачи
        priority_order = {'overdue': 0, 'high': 1, 'medium': 2, 'low': 3}
        
        if sort_by == 'priority':
            filtered_tasks.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))
        elif sort_by == 'deadline':
            filtered_tasks.sort(key=lambda x: (
                x.get('deadline_datetime') or datetime.max,
                priority_order.get(x.get('priority', 'low'), 3)
            ))
        elif sort_by == 'id':
            filtered_tasks.sort(key=lambda x: x['id'])
        
        print("\n" + "="*70)
        print("📋 СПИСОК ЗАДАЧ")
        print("="*70)
        
        for task in filtered_tasks:
            status = "✅" if task["completed"] else "⏳"
            priority_emoji = self.get_priority_emoji(task.get('priority', 'medium'))
            task_id = task["id"]
            description = task["description"]
            
            # Отображаем информацию о дедлайне
            deadline_info = ""
            if task.get('deadline'):
                time_left = self.calculate_time_left(task['deadline'])
                deadline_info = f" | {time_left}"
            
            # Отображаем информацию об авто-приоритете
            auto_info = " (авто)" if task.get('auto_priority', False) else ""
            
            print(f"{status}{priority_emoji} ID: {task_id:3} - {description}")
            print(f"   📅 Создано: {task['created_at']}")
            
            if task.get('deadline'):
                print(f"   ⏰ Дедлайн: {task['deadline']}{deadline_info}")
            
            priority_name = self.get_priority_name(task.get('priority', 'medium'))
            print(f"   🎯 Приоритет: {priority_name}{auto_info}")
            
            if task["completed"]:
                print(f"   ✅ Выполнено: {task['completed_at']}")
            
            print(f"   {'─'*50}")
        
        print("="*70)
        
        # Статистика
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        pending = total - completed
        
        # Счетчики по приоритетам
        high_priority = sum(1 for t in self.tasks if t.get('priority') == 'high' and not t['completed'])
        medium_priority = sum(1 for t in self.tasks if t.get('priority') == 'medium' and not t['completed'])
        low_priority = sum(1 for t in self.tasks if t.get('priority') == 'low' and not t['completed'])
        overdue = sum(1 for t in self.tasks if t.get('priority') == 'overdue' and not t['completed'])
        
        print(f"📊 Всего задач: {total}")
        print(f"📈 Выполнено: {completed}")
        print(f"📉 Осталось: {pending}")
        print(f"🔴 Высокий приоритет: {high_priority}")
        print(f"🟡 Средний приоритет: {medium_priority}")
        print(f"🟢 Низкий приоритет: {low_priority}")
        if overdue > 0:
            print(f"💀 Просрочено: {overdue}")
        print("="*70)
    
    def show_menu(self) -> None:
        """Показать меню приложения"""
        print("\n" + "="*70)
        print("📝 МЕНЕДЖЕР ЗАДАЧ С ПРИОРИТЕТАМИ И ДЕДЛАЙНАМИ")
        print("="*70)
        print("1. 📋 Показать все задачи (сортировка по приоритету)")
        print("2. 📋 Показать все задачи (сортировка по дедлайну)")
        print("3. 📋 Показать только активные задачи")
        print("4. ➕ Добавить задачу")
        print("5. ✏️ Редактировать задачу")
        print("6. ✅ Отметить задачу как выполненную")
        print("7. 🗑️ Удалить задачу")
        print("8. 🔄 Обновить приоритеты (автоматически по дедлайнам)")
        print("9. 💾 Сохранить и выйти")
        print("="*70)
    
    def parse_datetime_input(self, date_str: str, time_str: str) -> Optional[str]:
        """Парсить ввод даты и времени от пользователя"""
        try:
            # Пробуем разные форматы
            formats = [
                "%Y-%m-%d %H:%M",
                "%d.%m.%Y %H:%M",
                "%d/%m/%Y %H:%M"
            ]
            
            combined = f"{date_str} {time_str}"
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(combined, fmt)
                    return dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue
            
            print("❌ Неверный формат даты/времени")
            return None
        except Exception as e:
            print(f"❌ Ошибка при обработке даты: {e}")
            return None
    
    def run(self) -> None:
        """Запуск основного цикла приложения"""
        print("🚀 Добро пожаловать в менеджер задач с приоритетами и дедлайнами!")
        print("📌 Задачи с дедлайном <4 часов автоматически получают высокий приоритет")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("\nВыберите действие (1-9): ").strip()
                
                if choice == "1":
                    self.list_tasks(show_completed=True, sort_by='priority')
                
                elif choice == "2":
                    self.list_tasks(show_completed=True, sort_by='deadline')
                
                elif choice == "3":
                    self.list_tasks(show_completed=False, sort_by='priority')
                
                elif choice == "4":
                    description = input("Введите описание задачи: ").strip()
                    if not description:
                        print("❌ Описание задачи не может быть пустым")
                        continue
                    
                    print("\nВыберите приоритет:")
                    print("1. 🔴 Высокий")
                    print("2. 🟡 Средний")
                    print("3. 🟢 Низкий")
                    
                    priority_choice = input("Приоритет (1-3, по умолчанию 2): ").strip()
                    priorities = {'1': 'high', '2': 'medium', '3': 'low'}
                    priority = priorities.get(priority_choice, 'medium')
                    
                    set_deadline = input("Установить дедлайн? (y/n): ").strip().lower()
                    deadline = None
                    
                    if set_deadline == 'y':
                        date_input = input("Дата (ГГГГ-ММ-ДД или ДД.ММ.ГГГГ): ").strip()
                        time_input = input("Время (ЧЧ:ММ): ").strip()
                        
                        deadline = self.parse_datetime_input(date_input, time_input)
                        if not deadline:
                            print("⚠️  Задача будет создана без дедлайна")
                    
                    self.add_task(description, priority, deadline)
                
                elif choice == "5":
                    try:
                        task_id = int(input("Введите ID задачи для редактирования: ").strip())
                        
                        print("\nЧто вы хотите изменить?")
                        print("1. Описание")
                        print("2. Приоритет")
                        print("3. Дедлайн")
                        print("4. Всё вместе")
                        
                        edit_choice = input("Выберите (1-4): ").strip()
                        
                        if edit_choice == "1":
                            new_desc = input("Новое описание: ").strip()
                            if new_desc:
                                self.edit_task(task_id, description=new_desc)
                            else:
                                print("❌ Описание не может быть пустым")
                        
                        elif edit_choice == "2":
                            print("\nВыберите новый приоритет:")
                            print("1. 🔴 Высокий")
                            print("2. 🟡 Средний")
                            print("3. 🟢 Низкий")
                            priority_choice = input("Приоритет (1-3): ").strip()
                            priorities = {'1': 'high', '2': 'medium', '3': 'low'}
                            if priority_choice in priorities:
                                self.edit_task(task_id, priority=priorities[priority_choice])
                        
                        elif edit_choice == "3":
                            date_input = input("Новая дата (ГГГГ-ММ-ДД или ДД.ММ.ГГГГ): ").strip()
                            time_input = input("Новое время (ЧЧ:ММ): ").strip()
                            
                            deadline = self.parse_datetime_input(date_input, time_input)
                            if deadline:
                                self.edit_task(task_id, deadline=deadline)
                        
                        elif edit_choice == "4":
                            new_desc = input("Новое описание: ").strip()
                            if not new_desc:
                                print("❌ Описание не может быть пустым")
                                continue
                            
                            print("\nВыберите новый приоритет:")
                            print("1. 🔴 Высокий")
                            print("2. 🟡 Средний")
                            print("3. 🟢 Назкий")
                            priority_choice = input("Приоритет (1-3): ").strip()
                            priorities = {'1': 'high', '2': 'medium', '3': 'low'}
                            priority = priorities.get(priority_choice, 'medium')
                            
                            date_input = input("Новая дата (ГГГГ-ММ-ДД или ДД.ММ.ГГГГ): ").strip()
                            time_input = input("Новое время (ЧЧ:ММ): ").strip()
                            
                            deadline = self.parse_datetime_input(date_input, time_input)
                            
                            self.edit_task(task_id, 
                                         description=new_desc, 
                                         priority=priority,
                                         deadline=deadline)
                        
                        else:
                            print("❌ Неверный выбор")
                    
                    except ValueError:
                        print("❌ Пожалуйста, введите числовой ID")
                
                elif choice == "6":
                    try:
                        task_id = int(input("Введите ID задачи для отметки как выполненной: ").strip())
                        self.complete_task(task_id)
                    except ValueError:
                        print("❌ Пожалуйста, введите числовой ID")
                
                elif choice == "7":
                    try:
                        task_id = int(input("Введите ID задачи для удаления: ").strip())
                        self.delete_task(task_id)
                    except ValueError:
                        print("❌ Пожалуйста, введите числовой ID")
                
                elif choice == "8":
                    self.update_priorities_based_on_deadline()
                    self.save_tasks()
                    print("✅ Приоритеты обновлены на основе дедлайнов")
                    self.list_tasks(show_completed=False, sort_by='priority')
                
                elif choice == "9":
                    print("💾 Данные сохранены. До свидания!")
                    break
                
                else:
                    print("❌ Неверный выбор. Пожалуйста, выберите от 1 до 9")
            
            except KeyboardInterrupt:
                print("\n\n💾 Данные сохранены. До свидания!")
                break
            except Exception as e:
                print(f"❌ Произошла ошибка: {e}")

def main():
    """Точка входа в приложение"""
    app = TodoApp()
    app.run()

if __name__ == "__main__":
    main()