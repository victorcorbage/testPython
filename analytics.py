from datetime import datetime, timedelta
from collections import defaultdict
import json


class PerformanceAnalytics:
    
    def __init__(self, tasks):
        self.tasks = tasks
    
    def get_completion_rate_by_priority(self):
        priority_stats = defaultdict(lambda: {"total": 0, "completed": 0})
        
        for task in self.tasks:
            priority_stats[task.priority]["total"] += 1
            if task.completed:
                priority_stats[task.priority]["completed"] += 1
        
        rates = {}
        for priority, stats in priority_stats.items():
            if stats["total"] > 0:
                rates[priority] = (stats["completed"] / stats["total"]) * 100
            else:
                rates[priority] = 0
        
        return rates
    
    def get_average_completion_time(self):
        completion_times = []
        
        for task in self.tasks:
            if task.completed and task.completed_at:
                try:
                    created = datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")
                    completed = datetime.strptime(task.completed_at, "%Y-%m-%d %H:%M:%S")
                    duration = (completed - created).total_seconds() / 3600
                    completion_times.append(duration)
                except ValueError:
                    continue
        
        if completion_times:
            return sum(completion_times) / len(completion_times)
        return 0
    
    def get_productivity_by_day(self):
        daily_stats = defaultdict(lambda: {"created": 0, "completed": 0})
        
        for task in self.tasks:
            try:
                created_date = datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S").date()
                day_name = created_date.strftime("%A")
                daily_stats[day_name]["created"] += 1
                
                if task.completed and task.completed_at:
                    completed_date = datetime.strptime(task.completed_at, "%Y-%m-%d %H:%M:%S").date()
                    completed_day = completed_date.strftime("%A")
                    daily_stats[completed_day]["completed"] += 1
            except ValueError:
                continue
        
        return dict(daily_stats)
    
    def get_productivity_by_hour(self):
        hourly_stats = defaultdict(lambda: {"created": 0, "completed": 0})
        
        for task in self.tasks:
            try:
                created_time = datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")
                hour = created_time.hour
                hourly_stats[hour]["created"] += 1
                
                if task.completed and task.completed_at:
                    completed_time = datetime.strptime(task.completed_at, "%Y-%m-%d %H:%M:%S")
                    completed_hour = completed_time.hour
                    hourly_stats[completed_hour]["completed"] += 1
            except ValueError:
                continue
        
        return dict(hourly_stats)
    
    def get_task_velocity(self, days=7):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        completed_in_period = 0
        
        for task in self.tasks:
            if task.completed and task.completed_at:
                try:
                    completed_date = datetime.strptime(task.completed_at, "%Y-%m-%d %H:%M:%S")
                    if start_date <= completed_date <= end_date:
                        completed_in_period += 1
                except ValueError:
                    continue
        
        return completed_in_period / days if days > 0 else 0
    
    def get_longest_running_tasks(self, limit=5):
        pending_tasks = [t for t in self.tasks if not t.completed]
        
        tasks_with_age = []
        for task in pending_tasks:
            try:
                created = datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")
                age_days = (datetime.now() - created).days
                tasks_with_age.append((task, age_days))
            except ValueError:
                continue
        
        tasks_with_age.sort(key=lambda x: x[1], reverse=True)
        
        return tasks_with_age[:limit]
    
    def generate_report(self):
        report = {
            "total_tasks": len(self.tasks),
            "completed_tasks": sum(1 for t in self.tasks if t.completed),
            "pending_tasks": sum(1 for t in self.tasks if not t.completed),
            "completion_rate_by_priority": self.get_completion_rate_by_priority(),
            "average_completion_time_hours": round(self.get_average_completion_time(), 2),
            "task_velocity_7days": round(self.get_task_velocity(7), 2),
            "productivity_by_day": self.get_productivity_by_day(),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return report
    
    def export_report(self, filename="analytics_report.json"):
        report = self.generate_report()
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ Analytics report exported to: {filename}")
        return filename
    
    def display_report(self):
        report = self.generate_report()
        
        print("\n" + "=" * 60)
        print("  PERFORMANCE ANALYTICS REPORT")
        print("=" * 60)
        
        print(f"\n📊 Overview:")
        print(f"  Total Tasks: {report['total_tasks']}")
        print(f"  Completed: {report['completed_tasks']}")
        print(f"  Pending: {report['pending_tasks']}")
        
        print(f"\n⚡ Performance Metrics:")
        print(f"  Average Completion Time: {report['average_completion_time_hours']} hours")
        print(f"  Task Velocity (7 days): {report['task_velocity_7days']} tasks/day")
        
        print(f"\n🎯 Completion Rate by Priority:")
        for priority, rate in report['completion_rate_by_priority'].items():
            print(f"  {priority.capitalize()}: {rate:.1f}%")
        
        print(f"\n📅 Productivity by Day:")
        for day, stats in report['productivity_by_day'].items():
            print(f"  {day}: Created {stats['created']}, Completed {stats['completed']}")
        
        print(f"\nReport generated at: {report['generated_at']}")
        print("=" * 60)
