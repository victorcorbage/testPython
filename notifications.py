import os
import platform
from datetime import datetime


class NotificationSystem:
    
    @staticmethod
    def send_notification(title, message):
        system = platform.system()
        
        if system == "Windows":
            NotificationSystem._windows_notification(title, message)
        elif system == "Darwin":
            NotificationSystem._mac_notification(title, message)
        elif system == "Linux":
            NotificationSystem._linux_notification(title, message)
        else:
            print(f"\n[NOTIFICATION] {title}: {message}")
    
    @staticmethod
    def _windows_notification(title, message):
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=10, threaded=True)
        except ImportError:
            print(f"\n[NOTIFICATION] {title}: {message}")
            print("Install 'win10toast' for native Windows notifications: pip install win10toast")
    
    @staticmethod
    def _mac_notification(title, message):
        os.system(f'''
            osascript -e 'display notification "{message}" with title "{title}"'
        ''')
    
    @staticmethod
    def _linux_notification(title, message):
        os.system(f'notify-send "{title}" "{message}"')
    
    @staticmethod
    def notify_task_due(task):
        NotificationSystem.send_notification(
            "Task Reminder",
            f"Task due: {task.title}"
        )
    
    @staticmethod
    def notify_task_completed(task):
        NotificationSystem.send_notification(
            "Task Completed",
            f"Great job! You completed: {task.title}"
        )
    
    @staticmethod
    def notify_daily_summary(total, completed, pending):
        message = f"Total: {total} | Completed: {completed} | Pending: {pending}"
        NotificationSystem.send_notification(
            "Daily Task Summary",
            message
        )


class EmailNotifier:
    
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = None
        self.password = None
    
    def configure(self, email, password):
        self.email = email
        self.password = password
    
    def send_email(self, to_email, subject, body):
        if not self.email or not self.password:
            print("Email not configured. Use configure() method first.")
            return False
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            
            server.send_message(msg)
            server.quit()
            
            print(f"✓ Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send email: {str(e)}")
            return False
    
    def send_task_reminder(self, to_email, task):
        subject = f"Task Reminder: {task.title}"
        body = f"""
Task Reminder
-------------
Title: {task.title}
Description: {task.description}
Priority: {task.priority}
Created: {task.created_at}

This is an automated reminder from your Task Management System.
"""
        return self.send_email(to_email, subject, body)
    
    def send_daily_report(self, to_email, tasks):
        completed = sum(1 for t in tasks if t.completed)
        pending = len(tasks) - completed
        
        subject = f"Daily Task Report - {datetime.now().strftime('%Y-%m-%d')}"
        body = f"""
Daily Task Report
-----------------
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Summary:
- Total Tasks: {len(tasks)}
- Completed: {completed}
- Pending: {pending}

Pending Tasks:
"""
        
        for task in tasks:
            if not task.completed:
                body += f"\n- [{task.priority.upper()}] {task.title}"
        
        body += "\n\nThis is an automated report from your Task Management System."
        
        return self.send_email(to_email, subject, body)
