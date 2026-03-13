# Task Management System

A comprehensive command-line task management application built with Python.

## Features

- ✅ **Add Tasks** - Create tasks with title, description, and priority levels
- 📋 **View Tasks** - Display all tasks with status indicators
- ✓ **Complete Tasks** - Mark tasks as completed with timestamps
- 🗑️ **Delete Tasks** - Remove tasks from the system
- 🔍 **Search Tasks** - Find tasks by keyword in title or description
- 💾 **Persistent Storage** - Tasks saved automatically to JSON file
- 📊 **Priority Levels** - Organize tasks by low, medium, or high priority

## Project Structure

```
testPython/
├── main.py              # Main application entry point
├── task_manager.py      # TaskManager class for task operations
├── task.py              # Task model class
├── utils.py             # Utility functions
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── tests/               # Unit tests
│   ├── test_task.py
│   └── test_task_manager.py
└── tasks.json           # Data storage (auto-generated)
```

## Installation

1. Clone or download this repository
2. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

### Menu Options

1. **Add Task** - Create a new task
2. **View All Tasks** - Display all tasks with details
3. **Mark Task as Complete** - Update task status
4. **Delete Task** - Remove a task permanently
5. **Search Tasks** - Find tasks by keyword
6. **Exit** - Close the application

## Task Properties

Each task contains:
- **ID** - Unique identifier (UUID)
- **Title** - Task name
- **Description** - Detailed information
- **Priority** - low, medium, or high
- **Status** - Completed or pending
- **Created At** - Timestamp of creation
- **Completed At** - Timestamp when marked complete

## Data Storage

Tasks are stored in `tasks.json` in the following format:
```json
[
  {
    "id": "uuid-string",
    "title": "Task Title",
    "description": "Task Description",
    "priority": "medium",
    "completed": false,
    "created_at": "2026-03-13 14:05:00",
    "completed_at": null
  }
]
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Structure

- **Task Class** (`task.py`) - Represents individual tasks
- **TaskManager Class** (`task_manager.py`) - Handles task operations and persistence
- **Utilities** (`utils.py`) - Helper functions for UI and input
- **Configuration** (`config.py`) - Application settings

## Requirements

- Python 3.6+
- Standard library modules (json, os, datetime, uuid)

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.
