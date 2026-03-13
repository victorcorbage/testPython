import os


class Config:
    DATA_FILE = "tasks.json"
    
    BACKUP_DIR = "backups"
    
    PRIORITY_LEVELS = ["low", "medium", "high"]
    
    PRIORITY_ICONS = {
        "low": "↓",
        "medium": "→",
        "high": "↑"
    }
    
    STATUS_ICONS = {
        "completed": "✓",
        "pending": "○"
    }
    
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    DISPLAY_DATE_FORMAT = "%b %d, %Y at %I:%M %p"
    
    MAX_TITLE_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 500
    
    SEPARATOR_LINE = "-" * 80
    HEADER_LINE = "=" * 50
    
    APP_NAME = "Task Management System"
    APP_VERSION = "1.0.0"
    
    @staticmethod
    def ensure_backup_dir():
        if not os.path.exists(Config.BACKUP_DIR):
            os.makedirs(Config.BACKUP_DIR)
    
    @staticmethod
    def get_backup_path(filename):
        Config.ensure_backup_dir()
        return os.path.join(Config.BACKUP_DIR, filename)
