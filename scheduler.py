import schedule
import time
from datetime import datetime
from threading import Thread


class TaskScheduler:
    
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.running = False
        self.thread = None
    
    def start(self):
        if not self.running:
            self.running = True
            self.thread = Thread(target=self._run_scheduler, daemon=True)
            self.thread.start()
            print("✓ Scheduler started")
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        print("✓ Scheduler stopped")
    
    def _run_scheduler(self):
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def schedule_daily_backup(self, time_str="00:00"):
        from data_handler import DataHandler
        
        def backup_job():
            DataHandler.create_backup(self.task_manager.tasks)
            print(f"✓ Automatic backup completed at {datetime.now()}")
        
        schedule.every().day.at(time_str).do(backup_job)
        print(f"✓ Daily backup scheduled at {time_str}")
    
    def schedule_reminder_check(self, interval_minutes=15):
        from reminders import ReminderManager
        from notifications import NotificationSystem
        
        reminder_manager = ReminderManager()
        
        def check_reminders():
            due_reminders = reminder_manager.get_due_reminders()
            for task_id in due_reminders:
                task = self.task_manager.get_task_by_id(task_id)
                if task:
                    NotificationSystem.notify_task_due(task)
                    reminder_manager.mark_as_notified(task_id)
        
        schedule.every(interval_minutes).minutes.do(check_reminders)
        print(f"✓ Reminder check scheduled every {interval_minutes} minutes")
    
    def schedule_daily_summary(self, time_str="18:00"):
        from notifications import NotificationSystem
        from statistics import Statistics
        
        def daily_summary():
            stats = Statistics(self.task_manager.tasks)
            overview = stats.get_overview()
            NotificationSystem.notify_daily_summary(
                overview['total'],
                overview['completed'],
                overview['pending']
            )
        
        schedule.every().day.at(time_str).do(daily_summary)
        print(f"✓ Daily summary scheduled at {time_str}")
    
    def schedule_auto_cleanup(self, days=30):
        from datetime import timedelta
        
        def cleanup_old_completed():
            cutoff_date = datetime.now() - timedelta(days=days)
            removed = 0
            
            for task in self.task_manager.tasks[:]:
                if task.completed and task.completed_at:
                    try:
                        completed_date = datetime.strptime(task.completed_at, "%Y-%m-%d %H:%M:%S")
                        if completed_date < cutoff_date:
                            self.task_manager.tasks.remove(task)
                            removed += 1
                    except ValueError:
                        continue
            
            if removed > 0:
                self.task_manager.save_tasks()
                print(f"✓ Auto-cleanup: Removed {removed} old completed tasks")
        
        schedule.every().week.do(cleanup_old_completed)
        print(f"✓ Auto-cleanup scheduled (removes tasks completed > {days} days ago)")
