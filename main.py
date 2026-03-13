import sys
from datetime import datetime
from task_manager import TaskManager
from utils import clear_screen, print_header, get_user_input
from statistics import Statistics
from data_handler import DataHandler
from logger import TaskLogger


def display_menu():
    print("\n=== Task Management System ===")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Mark Task as Complete")
    print("4. Delete Task")
    print("5. Search Tasks")
    print("6. View Statistics")
    print("7. Export Tasks")
    print("8. Import Tasks")
    print("9. Create Backup")
    print("10. Restore from Backup")
    print("0. Exit")
    print("=" * 30)


def main():
    task_manager = TaskManager()
    logger = TaskLogger()
    
    while True:
        display_menu()
        choice = get_user_input("\nEnter your choice (0-10): ")
        
        if choice == "1":
            clear_screen()
            print_header("Add New Task")
            title = get_user_input("Task title: ")
            description = get_user_input("Task description: ")
            priority = get_user_input("Priority (low/medium/high): ").lower()
            
            if priority not in ["low", "medium", "high"]:
                print("Invalid priority. Setting to 'medium'")
                priority = "medium"
            
            task_manager.add_task(title, description, priority)
            print("\n✓ Task added successfully!")
        
        elif choice == "2":
            clear_screen()
            print_header("All Tasks")
            task_manager.display_tasks()
        
        elif choice == "3":
            clear_screen()
            print_header("Mark Task as Complete")
            task_manager.display_tasks()
            task_id = get_user_input("\nEnter task ID to mark as complete: ")
            task_manager.complete_task(task_id)
        
        elif choice == "4":
            clear_screen()
            print_header("Delete Task")
            task_manager.display_tasks()
            task_id = get_user_input("\nEnter task ID to delete: ")
            task_manager.delete_task(task_id)
        
        elif choice == "5":
            clear_screen()
            print_header("Search Tasks")
            keyword = get_user_input("Enter search keyword: ")
            task_manager.search_tasks(keyword)
        
        elif choice == "6":
            clear_screen()
            print_header("Task Statistics")
            stats = Statistics(task_manager.tasks)
            stats.display_statistics()
        
        elif choice == "7":
            clear_screen()
            print_header("Export Tasks")
            print("1. Export to JSON")
            print("2. Export to CSV")
            export_choice = get_user_input("\nChoose export format: ")
            
            if export_choice == "1":
                DataHandler.export_to_json(task_manager.tasks)
            elif export_choice == "2":
                DataHandler.export_to_csv(task_manager.tasks)
            else:
                print("\n✗ Invalid choice")
        
        elif choice == "8":
            clear_screen()
            print_header("Import Tasks")
            filepath = get_user_input("Enter file path to import: ")
            data = DataHandler.import_from_json(filepath)
            if data:
                task_manager.tasks = [task_manager._dict_to_task(task_data) for task_data in data]
                task_manager.save_tasks()
        
        elif choice == "9":
            clear_screen()
            print_header("Create Backup")
            DataHandler.create_backup(task_manager.tasks)
        
        elif choice == "10":
            clear_screen()
            print_header("Restore from Backup")
            backups = DataHandler.list_backups()
            
            if not backups:
                print("\n✗ No backups found")
            else:
                print("\nAvailable backups:")
                for idx, backup in enumerate(backups, 1):
                    print(f"{idx}. {backup}")
                
                backup_choice = get_user_input("\nEnter backup number to restore: ")
                try:
                    backup_idx = int(backup_choice) - 1
                    if 0 <= backup_idx < len(backups):
                        data = DataHandler.restore_from_backup(backups[backup_idx])
                        if data:
                            task_manager.tasks = [task_manager._dict_to_task(task_data) for task_data in data]
                            task_manager.save_tasks()
                    else:
                        print("\n✗ Invalid backup number")
                except ValueError:
                    print("\n✗ Invalid input")
        
        elif choice == "0":
            print("\nThank you for using Task Management System!")
            sys.exit(0)
        
        else:
            print("\n✗ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        clear_screen()


if __name__ == "__main__":
    clear_screen()
    print_header("Welcome to Task Management System")
    main()
