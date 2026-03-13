from datetime import datetime, timedelta
from collections import Counter


class Statistics:
    
    def __init__(self, tasks):
        self.tasks = tasks
    
    def get_overview(self):
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        pending = total - completed
        
        if total > 0:
            completion_rate = (completed / total) * 100
        else:
            completion_rate = 0
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": completion_rate
        }
    
    def get_priority_breakdown(self):
        priorities = [task.priority for task in self.tasks]
        return dict(Counter(priorities))
    
    def get_completed_today(self):
        today = datetime.now().date()
        completed_today = []
        
        for task in self.tasks:
            if task.completed and task.completed_at:
                try:
                    completed_date = datetime.strptime(task.completed_at, "%Y-%m-%d %H:%M:%S").date()
                    if completed_date == today:
                        completed_today.append(task)
                except ValueError:
                    continue
        
        return completed_today
    
    def get_created_this_week(self):
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        created_this_week = []
        
        for task in self.tasks:
            try:
                created_date = datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S").date()
                if created_date >= week_start:
                    created_this_week.append(task)
            except ValueError:
                continue
        
        return created_this_week
    
    def get_overdue_tasks(self):
        return [task for task in self.tasks if not task.completed]
    
    def display_statistics(self):
        overview = self.get_overview()
        priority_breakdown = self.get_priority_breakdown()
        completed_today = self.get_completed_today()
        created_this_week = self.get_created_this_week()
        
        print("\n" + "=" * 50)
        print("  TASK STATISTICS")
        print("=" * 50)
        
        print(f"\n📊 Overview:")
        print(f"  Total Tasks: {overview['total']}")
        print(f"  Completed: {overview['completed']}")
        print(f"  Pending: {overview['pending']}")
        print(f"  Completion Rate: {overview['completion_rate']:.1f}%")
        
        print(f"\n📈 Priority Breakdown:")
        for priority, count in priority_breakdown.items():
            icon = {"low": "↓", "medium": "→", "high": "↑"}.get(priority, "•")
            print(f"  {icon} {priority.capitalize()}: {count}")
        
        print(f"\n✓ Completed Today: {len(completed_today)}")
        print(f"📅 Created This Week: {len(created_this_week)}")
        
        print("\n" + "=" * 50)
