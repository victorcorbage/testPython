from datetime import datetime, timedelta


class TaskFilter:
    
    @staticmethod
    def filter_by_priority(tasks, priority):
        return [task for task in tasks if task.priority == priority]
    
    @staticmethod
    def filter_by_status(tasks, completed=None):
        if completed is None:
            return tasks
        return [task for task in tasks if task.completed == completed]
    
    @staticmethod
    def filter_by_date_range(tasks, start_date, end_date):
        filtered = []
        for task in tasks:
            try:
                created = datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")
                if start_date <= created <= end_date:
                    filtered.append(task)
            except ValueError:
                continue
        return filtered
    
    @staticmethod
    def filter_created_today(tasks):
        today = datetime.now().date()
        filtered = []
        for task in tasks:
            try:
                created = datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S").date()
                if created == today:
                    filtered.append(task)
            except ValueError:
                continue
        return filtered
    
    @staticmethod
    def filter_created_this_week(tasks):
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        filtered = []
        for task in tasks:
            try:
                created = datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S").date()
                if created >= week_start:
                    filtered.append(task)
            except ValueError:
                continue
        return filtered
    
    @staticmethod
    def filter_by_keyword(tasks, keyword):
        keyword = keyword.lower()
        return [
            task for task in tasks
            if keyword in task.title.lower() or keyword in task.description.lower()
        ]


class TaskSorter:
    
    @staticmethod
    def sort_by_priority(tasks, reverse=False):
        priority_order = {"high": 3, "medium": 2, "low": 1}
        return sorted(tasks, key=lambda t: priority_order.get(t.priority, 0), reverse=reverse)
    
    @staticmethod
    def sort_by_created_date(tasks, reverse=False):
        return sorted(tasks, key=lambda t: t.created_at, reverse=reverse)
    
    @staticmethod
    def sort_by_title(tasks, reverse=False):
        return sorted(tasks, key=lambda t: t.title.lower(), reverse=reverse)
    
    @staticmethod
    def sort_by_status(tasks, reverse=False):
        return sorted(tasks, key=lambda t: t.completed, reverse=reverse)
    
    @staticmethod
    def sort_by_completion_date(tasks, reverse=False):
        completed_tasks = [t for t in tasks if t.completed and t.completed_at]
        pending_tasks = [t for t in tasks if not t.completed]
        
        sorted_completed = sorted(completed_tasks, key=lambda t: t.completed_at, reverse=reverse)
        
        return sorted_completed + pending_tasks if not reverse else pending_tasks + sorted_completed
