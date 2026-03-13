import unittest
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from task_manager import TaskManager
from task import Task


class TestTaskManager(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "test_tasks.json"
        self.manager = TaskManager(data_file=self.test_file)
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_initialization(self):
        self.assertEqual(self.manager.data_file, self.test_file)
        self.assertIsInstance(self.manager.tasks, list)
    
    def test_add_task(self):
        task = self.manager.add_task("Test Task", "Description", "high")
        
        self.assertIsInstance(task, Task)
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.priority, "high")
    
    def test_save_and_load_tasks(self):
        self.manager.add_task("Task 1", "Desc 1", "low")
        self.manager.add_task("Task 2", "Desc 2", "high")
        
        new_manager = TaskManager(data_file=self.test_file)
        
        self.assertEqual(len(new_manager.tasks), 2)
        self.assertEqual(new_manager.tasks[0].title, "Task 1")
        self.assertEqual(new_manager.tasks[1].title, "Task 2")
    
    def test_get_task_by_id(self):
        task = self.manager.add_task("Test", "Description")
        
        found_task = self.manager.get_task_by_id(task.id)
        
        self.assertIsNotNone(found_task)
        self.assertEqual(found_task.id, task.id)
        self.assertEqual(found_task.title, "Test")
    
    def test_get_task_by_invalid_id(self):
        result = self.manager.get_task_by_id("invalid-id")
        self.assertIsNone(result)
    
    def test_complete_task(self):
        task = self.manager.add_task("Test", "Description")
        
        result = self.manager.complete_task(task.id)
        
        self.assertTrue(result)
        self.assertTrue(task.completed)
        self.assertIsNotNone(task.completed_at)
    
    def test_complete_invalid_task(self):
        result = self.manager.complete_task("invalid-id")
        self.assertFalse(result)
    
    def test_delete_task(self):
        task = self.manager.add_task("Test", "Description")
        self.assertEqual(len(self.manager.tasks), 1)
        
        result = self.manager.delete_task(task.id)
        
        self.assertTrue(result)
        self.assertEqual(len(self.manager.tasks), 0)
    
    def test_delete_invalid_task(self):
        result = self.manager.delete_task("invalid-id")
        self.assertFalse(result)
    
    def test_search_tasks(self):
        self.manager.add_task("Python Project", "Build a web app")
        self.manager.add_task("Java Project", "Create REST API")
        self.manager.add_task("Python Script", "Automation tool")
        
        self.manager.search_tasks("Python")
    
    def test_get_statistics(self):
        self.manager.add_task("Task 1", "Desc 1")
        task2 = self.manager.add_task("Task 2", "Desc 2")
        self.manager.add_task("Task 3", "Desc 3")
        
        self.manager.complete_task(task2.id)
        
        stats = self.manager.get_statistics()
        
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["pending"], 2)


if __name__ == "__main__":
    unittest.main()
