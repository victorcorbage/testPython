from flask import Flask, request, jsonify
from flask_cors import CORS
from task_manager import TaskManager
from statistics import Statistics
from data_handler import DataHandler
from filters import TaskFilter, TaskSorter
from tags import TagManager
from datetime import datetime


app = Flask(__name__)
CORS(app)

task_manager = TaskManager()
tag_manager = TagManager()


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    priority = request.args.get('priority')
    status = request.args.get('status')
    sort_by = request.args.get('sort_by', 'created_date')
    
    tasks = task_manager.tasks
    
    if priority:
        tasks = TaskFilter.filter_by_priority(tasks, priority)
    
    if status == 'completed':
        tasks = TaskFilter.filter_by_status(tasks, completed=True)
    elif status == 'pending':
        tasks = TaskFilter.filter_by_status(tasks, completed=False)
    
    if sort_by == 'priority':
        tasks = TaskSorter.sort_by_priority(tasks, reverse=True)
    elif sort_by == 'title':
        tasks = TaskSorter.sort_by_title(tasks)
    else:
        tasks = TaskSorter.sort_by_created_date(tasks, reverse=True)
    
    return jsonify([task.to_dict() for task in tasks])


@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    title = data['title']
    description = data.get('description', '')
    priority = data.get('priority', 'medium')
    
    task = task_manager.add_task(title, description, priority)
    
    if 'tags' in data:
        for tag in data['tags']:
            tag_manager.add_tag_to_task(task.id, tag)
    
    return jsonify(task.to_dict()), 201


@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = task_manager.get_task_by_id(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    task_dict = task.to_dict()
    task_dict['tags'] = tag_manager.get_tags_for_task(task_id)
    
    return jsonify(task_dict)


@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = task_manager.get_task_by_id(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'priority' in data:
        task.priority = data['priority']
    
    task_manager.save_tasks()
    
    return jsonify(task.to_dict())


@app.route('/api/tasks/<task_id>/complete', methods=['POST'])
def complete_task(task_id):
    success = task_manager.complete_task(task_id)
    
    if not success:
        return jsonify({"error": "Task not found"}), 404
    
    task = task_manager.get_task_by_id(task_id)
    return jsonify(task.to_dict())


@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    success = task_manager.delete_task(task_id)
    
    if not success:
        return jsonify({"error": "Task not found"}), 404
    
    tag_manager.delete_task_tags(task_id)
    
    return jsonify({"message": "Task deleted successfully"})


@app.route('/api/tasks/search', methods=['GET'])
def search_tasks():
    keyword = request.args.get('q', '')
    
    if not keyword:
        return jsonify({"error": "Search query required"}), 400
    
    results = TaskFilter.filter_by_keyword(task_manager.tasks, keyword)
    
    return jsonify([task.to_dict() for task in results])


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    stats = Statistics(task_manager.tasks)
    overview = stats.get_overview()
    priority_breakdown = stats.get_priority_breakdown()
    
    return jsonify({
        "overview": overview,
        "priority_breakdown": priority_breakdown,
        "completed_today": len(stats.get_completed_today()),
        "created_this_week": len(stats.get_created_this_week())
    })


@app.route('/api/tags', methods=['GET'])
def get_all_tags():
    tags = tag_manager.get_all_tags()
    tag_stats = tag_manager.get_tag_statistics()
    
    return jsonify({
        "tags": tags,
        "statistics": tag_stats
    })


@app.route('/api/tasks/<task_id>/tags', methods=['POST'])
def add_tag(task_id):
    data = request.get_json()
    
    if not data or 'tag' not in data:
        return jsonify({"error": "Tag is required"}), 400
    
    success = tag_manager.add_tag_to_task(task_id, data['tag'])
    
    if not success:
        return jsonify({"error": "Tag already exists or invalid"}), 400
    
    return jsonify({"message": "Tag added successfully"})


@app.route('/api/tasks/<task_id>/tags/<tag>', methods=['DELETE'])
def remove_tag(task_id, tag):
    success = tag_manager.remove_tag_from_task(task_id, tag)
    
    if not success:
        return jsonify({"error": "Tag not found"}), 404
    
    return jsonify({"message": "Tag removed successfully"})


@app.route('/api/export', methods=['GET'])
def export_tasks():
    format_type = request.args.get('format', 'json')
    
    if format_type == 'csv':
        filepath = DataHandler.export_to_csv(task_manager.tasks)
    else:
        filepath = DataHandler.export_to_json(task_manager.tasks)
    
    return jsonify({"message": "Export successful", "file": filepath})


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_tasks": len(task_manager.tasks)
    })


def run_api(host='0.0.0.0', port=5000, debug=False):
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    print("Starting Task Management API Server...")
    print("API available at http://localhost:5000")
    run_api(debug=True)
