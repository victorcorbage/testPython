import re
from datetime import datetime


class TaskValidator:
    
    @staticmethod
    def validate_title(title):
        if not title or not title.strip():
            return False, "Title cannot be empty"
        
        if len(title) > 100:
            return False, "Title must be 100 characters or less"
        
        return True, "Valid"
    
    @staticmethod
    def validate_description(description):
        if len(description) > 500:
            return False, "Description must be 500 characters or less"
        
        return True, "Valid"
    
    @staticmethod
    def validate_priority(priority):
        valid_priorities = ["low", "medium", "high"]
        
        if priority.lower() not in valid_priorities:
            return False, f"Priority must be one of: {', '.join(valid_priorities)}"
        
        return True, "Valid"
    
    @staticmethod
    def validate_task_id(task_id):
        if not task_id or not task_id.strip():
            return False, "Task ID cannot be empty"
        
        uuid_pattern = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', re.IGNORECASE)
        
        if not uuid_pattern.match(task_id) and len(task_id) < 8:
            return False, "Invalid task ID format"
        
        return True, "Valid"
    
    @staticmethod
    def validate_date(date_string, date_format="%Y-%m-%d %H:%M:%S"):
        try:
            datetime.strptime(date_string, date_format)
            return True, "Valid"
        except ValueError:
            return False, f"Invalid date format. Expected: {date_format}"
    
    @staticmethod
    def validate_tag(tag):
        if not tag or not tag.strip():
            return False, "Tag cannot be empty"
        
        if len(tag) > 50:
            return False, "Tag must be 50 characters or less"
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', tag):
            return False, "Tag can only contain letters, numbers, hyphens, and underscores"
        
        return True, "Valid"
    
    @staticmethod
    def validate_email(email):
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
        if not email_pattern.match(email):
            return False, "Invalid email format"
        
        return True, "Valid"
    
    @staticmethod
    def sanitize_input(text):
        if not text:
            return ""
        
        text = text.strip()
        text = re.sub(r'[<>]', '', text)
        
        return text


class ErrorHandler:
    
    @staticmethod
    def handle_file_error(error, filename):
        error_messages = {
            FileNotFoundError: f"File not found: {filename}",
            PermissionError: f"Permission denied: {filename}",
            IOError: f"I/O error occurred with file: {filename}"
        }
        
        message = error_messages.get(type(error), f"Error with file {filename}: {str(error)}")
        return message
    
    @staticmethod
    def handle_json_error(error):
        return f"JSON parsing error: {str(error)}"
    
    @staticmethod
    def handle_database_error(error):
        return f"Database error: {str(error)}"
    
    @staticmethod
    def log_error(error, context=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_msg = f"[{timestamp}] ERROR in {context}: {type(error).__name__} - {str(error)}"
        
        with open("errors.log", "a") as f:
            f.write(error_msg + "\n")
        
        return error_msg
