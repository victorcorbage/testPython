import argparse
import sys
from task_manager import TaskManager
from statistics import Statistics
from data_handler import DataHandler


class CLI:
    
    def __init__(self):
        self.task_manager = TaskManager()
        self.parser = self.create_parser()
    
    def create_parser(self):
        parser = argparse.ArgumentParser(
            description='Task Management System - Command Line Interface',
            prog='task-manager'
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('title', help='Task title')
        add_parser.add_argument('-d', '--description', default='', help='Task description')
        add_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high'], 
                               default='medium', help='Task priority')
        
        list_parser = subparsers.add_parser('list', help='List all tasks')
        list_parser.add_argument('-s', '--status', choices=['completed', 'pending', 'all'],
                                default='all', help='Filter by status')
        list_parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high'],
                                help='Filter by priority')
        
        complete_parser = subparsers.add_parser('complete', help='Mark task as complete')
        complete_parser.add_argument('task_id', help='Task ID to complete')
        
        delete_parser = subparsers.add_parser('delete', help='Delete a task')
        delete_parser.add_argument('task_id', help='Task ID to delete')
        
        search_parser = subparsers.add_parser('search', help='Search tasks')
        search_parser.add_argument('keyword', help='Search keyword')
        
        stats_parser = subparsers.add_parser('stats', help='Show statistics')
        
        export_parser = subparsers.add_parser('export', help='Export tasks')
        export_parser.add_argument('-f', '--format', choices=['json', 'csv'],
                                  default='json', help='Export format')
        export_parser.add_argument('-o', '--output', help='Output filename')
        
        backup_parser = subparsers.add_parser('backup', help='Create backup')
        
        return parser
    
    def run(self, args=None):
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            self.parser.print_help()
            return
        
        if parsed_args.command == 'add':
            self.add_task(parsed_args)
        elif parsed_args.command == 'list':
            self.list_tasks(parsed_args)
        elif parsed_args.command == 'complete':
            self.complete_task(parsed_args)
        elif parsed_args.command == 'delete':
            self.delete_task(parsed_args)
        elif parsed_args.command == 'search':
            self.search_tasks(parsed_args)
        elif parsed_args.command == 'stats':
            self.show_stats()
        elif parsed_args.command == 'export':
            self.export_tasks(parsed_args)
        elif parsed_args.command == 'backup':
            self.create_backup()
    
    def add_task(self, args):
        task = self.task_manager.add_task(args.title, args.description, args.priority)
        print(f"✓ Task added: {task.title} (ID: {task.id[:8]})")
    
    def list_tasks(self, args):
        tasks = self.task_manager.tasks
        
        if args.status == 'completed':
            tasks = [t for t in tasks if t.completed]
        elif args.status == 'pending':
            tasks = [t for t in tasks if not t.completed]
        
        if args.priority:
            tasks = [t for t in tasks if t.priority == args.priority]
        
        if not tasks:
            print("No tasks found.")
            return
        
        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"{status} [{task.id[:8]}] {task.title} ({task.priority})")
    
    def complete_task(self, args):
        self.task_manager.complete_task(args.task_id)
    
    def delete_task(self, args):
        self.task_manager.delete_task(args.task_id)
    
    def search_tasks(self, args):
        self.task_manager.search_tasks(args.keyword)
    
    def show_stats(self):
        stats = Statistics(self.task_manager.tasks)
        stats.display_statistics()
    
    def export_tasks(self, args):
        if args.format == 'json':
            DataHandler.export_to_json(self.task_manager.tasks, args.output)
        else:
            DataHandler.export_to_csv(self.task_manager.tasks, args.output)
    
    def create_backup(self):
        DataHandler.create_backup(self.task_manager.tasks)


def main():
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
