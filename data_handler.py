import json
import csv
import os
from datetime import datetime
from config import Config


class DataHandler:
    
    @staticmethod
    def export_to_json(tasks, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tasks_export_{timestamp}.json"
        
        filepath = Config.get_backup_path(filename)
        
        with open(filepath, 'w') as f:
            json.dump([task.to_dict() for task in tasks], f, indent=2)
        
        print(f"\n✓ Tasks exported to: {filepath}")
        return filepath
    
    @staticmethod
    def export_to_csv(tasks, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tasks_export_{timestamp}.csv"
        
        filepath = Config.get_backup_path(filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if not tasks:
                print("\n✗ No tasks to export")
                return None
            
            fieldnames = ['id', 'title', 'description', 'priority', 'completed', 'created_at', 'completed_at']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for task in tasks:
                writer.writerow(task.to_dict())
        
        print(f"\n✓ Tasks exported to CSV: {filepath}")
        return filepath
    
    @staticmethod
    def import_from_json(filepath):
        if not os.path.exists(filepath):
            print(f"\n✗ File not found: {filepath}")
            return None
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            print(f"\n✓ Successfully imported {len(data)} tasks from {filepath}")
            return data
        except json.JSONDecodeError:
            print(f"\n✗ Invalid JSON file: {filepath}")
            return None
    
    @staticmethod
    def create_backup(tasks):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{timestamp}.json"
        return DataHandler.export_to_json(tasks, filename)
    
    @staticmethod
    def list_backups():
        Config.ensure_backup_dir()
        backups = [f for f in os.listdir(Config.BACKUP_DIR) if f.endswith('.json')]
        return sorted(backups, reverse=True)
    
    @staticmethod
    def restore_from_backup(backup_filename):
        filepath = Config.get_backup_path(backup_filename)
        return DataHandler.import_from_json(filepath)
