import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from task import Task


class TestTask(unittest.TestCase):
    
    def test_task_creation(self):
        task = Task("Test Task", "This is a test", "high")
        
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test")
        self.assertEqual(task.priority, "high")
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.id)
        self.assertIsNotNone(task.created_at)
        self.assertIsNone(task.completed_at)
    
    def test_task_default_priority(self):
        task = Task("Test", "Description")
        self.assertEqual(task.priority, "medium")
    
    def test_mark_complete(self):
        task = Task("Test", "Description")
        self.assertFalse(task.completed)
        self.assertIsNone(task.completed_at)
        
        task.mark_complete()
        
        self.assertTrue(task.completed)
        self.assertIsNotNone(task.completed_at)
    
    def test_to_dict(self):
        task = Task("Test", "Description", "low")
        task_dict = task.to_dict()
        
        self.assertIn("id", task_dict)
        self.assertIn("title", task_dict)
        self.assertIn("description", task_dict)
        self.assertIn("priority", task_dict)
        self.assertIn("completed", task_dict)
        self.assertIn("created_at", task_dict)
        self.assertIn("completed_at", task_dict)
        
        self.assertEqual(task_dict["title"], "Test")
        self.assertEqual(task_dict["priority"], "low")
    
    def test_from_dict(self):
        data = {
            "id": "test-id-123",
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "completed": True,
            "created_at": "2026-03-13 14:00:00",
            "completed_at": "2026-03-13 15:00:00"
        }
        
        task = Task.from_dict(data)
        
        self.assertEqual(task.id, "test-id-123")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.priority, "high")
        self.assertTrue(task.completed)
        self.assertEqual(task.created_at, "2026-03-13 14:00:00")
        self.assertEqual(task.completed_at, "2026-03-13 15:00:00")
    
    def test_str_representation(self):
        task = Task("Test", "Description")
        str_repr = str(task)
        
        self.assertIn("Test", str_repr)
        self.assertIn("Description", str_repr)


if __name__ == "__main__":
    unittest.main()
