import logging
from datetime import datetime
import os


class TaskLogger:
    
    def __init__(self, log_file="task_manager.log"):
        self.log_file = log_file
        self.setup_logger()
    
    def setup_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_task_created(self, task):
        self.logger.info(f"Task created: '{task.title}' (ID: {task.id[:8]})")
    
    def log_task_completed(self, task):
        self.logger.info(f"Task completed: '{task.title}' (ID: {task.id[:8]})")
    
    def log_task_deleted(self, task):
        self.logger.info(f"Task deleted: '{task.title}' (ID: {task.id[:8]})")
    
    def log_export(self, filepath, count):
        self.logger.info(f"Exported {count} tasks to: {filepath}")
    
    def log_import(self, filepath, count):
        self.logger.info(f"Imported {count} tasks from: {filepath}")
    
    def log_error(self, message):
        self.logger.error(message)
    
    def log_warning(self, message):
        self.logger.warning(message)
    
    def log_info(self, message):
        self.logger.info(message)
