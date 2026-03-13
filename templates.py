import json
import os
from datetime import datetime


class TaskTemplate:
    
    def __init__(self, name, title, description, priority="medium", tags=None):
        self.name = name
        self.title = title
        self.description = description
        self.priority = priority
        self.tags = tags or []
    
    def to_dict(self):
        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["title"],
            data["description"],
            data.get("priority", "medium"),
            data.get("tags", [])
        )


class TemplateManager:
    
    def __init__(self, templates_file="templates.json"):
        self.templates_file = templates_file
        self.templates = {}
        self.load_templates()
        self._create_default_templates()
    
    def load_templates(self):
        if os.path.exists(self.templates_file):
            try:
                with open(self.templates_file, 'r') as f:
                    data = json.load(f)
                    self.templates = {
                        name: TaskTemplate.from_dict(template_data)
                        for name, template_data in data.items()
                    }
            except (json.JSONDecodeError, FileNotFoundError):
                self.templates = {}
        else:
            self.templates = {}
    
    def save_templates(self):
        data = {name: template.to_dict() for name, template in self.templates.items()}
        with open(self.templates_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _create_default_templates(self):
        if not self.templates:
            defaults = [
                TaskTemplate(
                    "meeting",
                    "Team Meeting",
                    "Attend team meeting",
                    "medium",
                    ["work", "meeting"]
                ),
                TaskTemplate(
                    "code_review",
                    "Code Review",
                    "Review pull request",
                    "high",
                    ["work", "development"]
                ),
                TaskTemplate(
                    "bug_fix",
                    "Bug Fix",
                    "Fix reported bug",
                    "high",
                    ["work", "bug"]
                ),
                TaskTemplate(
                    "documentation",
                    "Write Documentation",
                    "Update project documentation",
                    "medium",
                    ["work", "docs"]
                ),
                TaskTemplate(
                    "learning",
                    "Learning Task",
                    "Study new technology or skill",
                    "low",
                    ["personal", "learning"]
                )
            ]
            
            for template in defaults:
                self.templates[template.name] = template
            
            self.save_templates()
    
    def add_template(self, template):
        self.templates[template.name] = template
        self.save_templates()
        return True
    
    def get_template(self, name):
        return self.templates.get(name)
    
    def list_templates(self):
        return list(self.templates.keys())
    
    def delete_template(self, name):
        if name in self.templates:
            del self.templates[name]
            self.save_templates()
            return True
        return False
    
    def create_task_from_template(self, template_name, task_manager, custom_title=None):
        template = self.get_template(template_name)
        if not template:
            return None
        
        title = custom_title if custom_title else template.title
        task = task_manager.add_task(title, template.description, template.priority)
        
        return task
