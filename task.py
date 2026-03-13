import uuid
from datetime import datetime


class Task:
    def __init__(self, title, description, priority="medium"):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed_at = None
    
    def mark_complete(self):
        self.completed = True
        self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data):
        task = cls(data["title"], data["description"], data["priority"])
        task.id = data["id"]
        task.completed = data["completed"]
        task.created_at = data["created_at"]
        task.completed_at = data.get("completed_at")
        return task
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} [{self.id[:8]}] {self.title} - {self.description}"
