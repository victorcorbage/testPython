from datetime import datetime, timedelta
import json
import os


class ReminderManager:
    
    def __init__(self, reminders_file="reminders.json"):
        self.reminders_file = reminders_file
        self.reminders = {}
        self.load_reminders()
    
    def load_reminders(self):
        if os.path.exists(self.reminders_file):
            try:
                with open(self.reminders_file, 'r') as f:
                    self.reminders = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.reminders = {}
        else:
            self.reminders = {}
    
    def save_reminders(self):
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f, indent=2)
    
    def add_reminder(self, task_id, reminder_datetime):
        if isinstance(reminder_datetime, str):
            reminder_datetime_str = reminder_datetime
        else:
            reminder_datetime_str = reminder_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        self.reminders[task_id] = {
            "datetime": reminder_datetime_str,
            "notified": False
        }
        self.save_reminders()
        return True
    
    def remove_reminder(self, task_id):
        if task_id in self.reminders:
            del self.reminders[task_id]
            self.save_reminders()
            return True
        return False
    
    def get_reminder(self, task_id):
        return self.reminders.get(task_id)
    
    def get_due_reminders(self):
        now = datetime.now()
        due_reminders = []
        
        for task_id, reminder_data in self.reminders.items():
            if not reminder_data.get("notified", False):
                try:
                    reminder_time = datetime.strptime(reminder_data["datetime"], "%Y-%m-%d %H:%M:%S")
                    if reminder_time <= now:
                        due_reminders.append(task_id)
                except ValueError:
                    continue
        
        return due_reminders
    
    def mark_as_notified(self, task_id):
        if task_id in self.reminders:
            self.reminders[task_id]["notified"] = True
            self.save_reminders()
            return True
        return False
    
    def get_upcoming_reminders(self, hours=24):
        now = datetime.now()
        future = now + timedelta(hours=hours)
        upcoming = []
        
        for task_id, reminder_data in self.reminders.items():
            if not reminder_data.get("notified", False):
                try:
                    reminder_time = datetime.strptime(reminder_data["datetime"], "%Y-%m-%d %H:%M:%S")
                    if now <= reminder_time <= future:
                        upcoming.append({
                            "task_id": task_id,
                            "datetime": reminder_data["datetime"]
                        })
                except ValueError:
                    continue
        
        return sorted(upcoming, key=lambda x: x["datetime"])
