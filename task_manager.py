import json
import os
from datetime import datetime
from task import Task


class TaskManager:
    def __init__(self, data_file="tasks.json"):
        self.data_file = data_file
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        with open(self.data_file, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2)
    
    def add_task(self, title, description, priority="medium"):
        task = Task(title, description, priority)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def complete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_complete()
            self.save_tasks()
            print(f"\n✓ Task '{task.title}' marked as complete!")
            return True
        else:
            print(f"\n✗ Task with ID '{task_id}' not found.")
            return False
    
    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f"\n✓ Task '{task.title}' deleted!")
            return True
        else:
            print(f"\n✗ Task with ID '{task_id}' not found.")
            return False
    
    def display_tasks(self):
        if not self.tasks:
            print("\nNo tasks found.")
            return
        
        print(f"\nTotal tasks: {len(self.tasks)}")
        print("-" * 80)
        
        for task in self.tasks:
            status_icon = "✓" if task.completed else "○"
            priority_icon = {"low": "↓", "medium": "→", "high": "↑"}[task.priority]
            
            print(f"{status_icon} [{task.id[:8]}] {priority_icon} {task.title}")
            print(f"  Description: {task.description}")
            print(f"  Created: {task.created_at}")
            if task.completed:
                print(f"  Completed: {task.completed_at}")
            print("-" * 80)
    
    def search_tasks(self, keyword):
        keyword = keyword.lower()
        results = [
            task for task in self.tasks
            if keyword in task.title.lower() or keyword in task.description.lower()
        ]
        
        if not results:
            print(f"\nNo tasks found matching '{keyword}'")
            return
        
        print(f"\nFound {len(results)} task(s) matching '{keyword}':")
        print("-" * 80)
        
        for task in results:
            status_icon = "✓" if task.completed else "○"
            print(f"{status_icon} [{task.id[:8]}] {task.title}")
            print(f"  {task.description}")
            print("-" * 80)
    
    def get_statistics(self):
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        pending = total - completed
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }
