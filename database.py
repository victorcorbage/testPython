import sqlite3
from datetime import datetime
from task import Task


class DatabaseManager:
    
    def __init__(self, db_file="tasks.db"):
        self.db_file = db_file
        self.connection = None
        self.create_tables()
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_file)
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        if self.connection:
            self.connection.close()
    
    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'medium',
                completed INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                completed_at TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                tag TEXT NOT NULL,
                FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE,
                UNIQUE(task_id, tag)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                reminder_datetime TEXT NOT NULL,
                notified INTEGER DEFAULT 0,
                FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        self.close()
    
    def save_task(self, task):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO tasks (id, title, description, priority, completed, created_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            task.id,
            task.title,
            task.description,
            task.priority,
            1 if task.completed else 0,
            task.created_at,
            task.completed_at
        ))
        
        conn.commit()
        self.close()
    
    def get_task(self, task_id):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        
        self.close()
        
        if row:
            return self._row_to_task(row)
        return None
    
    def get_all_tasks(self):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        rows = cursor.fetchall()
        
        self.close()
        
        return [self._row_to_task(row) for row in rows]
    
    def delete_task(self, task_id):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        
        conn.commit()
        self.close()
        
        return cursor.rowcount > 0
    
    def search_tasks(self, keyword):
        conn = self.connect()
        cursor = conn.cursor()
        
        keyword_pattern = f"%{keyword}%"
        cursor.execute('''
            SELECT * FROM tasks 
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY created_at DESC
        ''', (keyword_pattern, keyword_pattern))
        
        rows = cursor.fetchall()
        self.close()
        
        return [self._row_to_task(row) for row in rows]
    
    def _row_to_task(self, row):
        task_data = {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "priority": row["priority"],
            "completed": bool(row["completed"]),
            "created_at": row["created_at"],
            "completed_at": row["completed_at"]
        }
        return Task.from_dict(task_data)
    
    def add_tag(self, task_id, tag):
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO tags (task_id, tag) VALUES (?, ?)', (task_id, tag))
            conn.commit()
            self.close()
            return True
        except sqlite3.IntegrityError:
            self.close()
            return False
    
    def get_tags_for_task(self, task_id):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT tag FROM tags WHERE task_id = ?', (task_id,))
        rows = cursor.fetchall()
        
        self.close()
        
        return [row["tag"] for row in rows]
