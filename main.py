import sys
from datetime import datetime
from task_manager import TaskManager
from utils import clear_screen, print_header, get_user_input


def display_menu():
    print("\n=== Task Management System ===")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Mark Task as Complete")
    print("4. Delete Task")
    print("5. Search Tasks")
    print("6. Exit")
    print("=" * 30)


def main():
    task_manager = TaskManager()
    
    while True:
        display_menu()
        choice = get_user_input("\nEnter your choice (1-6): ")
        
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
