import json
import os
from datetime import datetime
from typing import List, Dict, Any

class TodoApp:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """Загрузить задачи из JSON файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_tasks(self) -> None:
        """Сохранить задачи в JSON файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def add_task(self, description: str) -> None:
        """Добавить новую задачу"""
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": None
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✅ Задача добавлена (ID: {task['id']})")
    
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
    
    def list_tasks(self, show_completed: bool = True) -> None:
        """Вывести список задач"""
        if not self.tasks:
            print("📝 Список задач пуст")
            return
        
        print("\n" + "="*50)
        print("📋 СПИСОК ЗАДАЧ")
        print("="*50)
        
        for task in self.tasks:
            if not show_completed and task["completed"]:
                continue
                
            status = "✅" if task["completed"] else "⏳"
            task_id = task["id"]
            description = task["description"]
            
            if task["completed"]:
                completed_date = f" (выполнено: {task['completed_at']})"
            else:
                completed_date = ""
            
            print(f"{status} ID: {task_id:3} - {description}{completed_date}")
            print(f"   📅 Создано: {task['created_at']}")
        
        print("="*50)
        
        # Статистика
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        pending = total - completed
        
        print(f"📊 Всего задач: {total}")
        print(f"📈 Выполнено: {completed}")
        print(f"📉 Осталось: {pending}")
        print("="*50)
    
    def show_menu(self) -> None:
        """Показать меню приложения"""
        print("\n" + "="*50)
        print("📝 МЕНЕДЖЕР ЗАДАЧ")
        print("="*50)
        print("1. 📋 Показать все задачи")
        print("2. 📋 Показать только активные задачи")
        print("3. ➕ Добавить задачу")
        print("4. ✅ Отметить задачу как выполненную")
        print("5. 🗑️ Удалить задачу")
        print("6. 💾 Сохранить и выйти")
        print("="*50)
    
    def run(self) -> None:
        """Запуск основного цикла приложения"""
        print("🚀 Добро пожаловать в менеджер задач!")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("\nВыберите действие (1-6): ").strip()
                
                if choice == "1":
                    self.list_tasks(show_completed=True)
                
                elif choice == "2":
                    self.list_tasks(show_completed=False)
                
                elif choice == "3":
                    description = input("Введите описание задачи: ").strip()
                    if description:
                        self.add_task(description)
                    else:
                        print("❌ Описание задачи не может быть пустым")
                
                elif choice == "4":
                    self.list_tasks(show_completed=False)
                    try:
                        task_id = int(input("Введите ID задачи для отметки как выполненной: ").strip())
                        self.complete_task(task_id)
                    except ValueError:
                        print("❌ Пожалуйста, введите числовой ID")
                
                elif choice == "5":
                    self.list_tasks(show_completed=True)
                    try:
                        task_id = int(input("Введите ID задачи для удаления: ").strip())
                        self.delete_task(task_id)
                    except ValueError:
                        print("❌ Пожалуйста, введите числовой ID")
                
                elif choice == "6":
                    print("💾 Данные сохранены. До свидания!")
                    break
                
                else:
                    print("❌ Неверный выбор. Пожалуйста, выберите от 1 до 6")
            
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