from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory storage for tasks
tasks = {}

@app.route('/tasks/auto-schedule', methods=['POST'])
def auto_schedule():
    data = request.get_json()
    task_ids = data.get("tasks", [])
    priority = data.get("priority", "medium")
    user_availability = data.get("user_availability", False)

    scheduled_tasks = []
    start_time = datetime(2025, 3, 20, 9, 0)

    for index, task_id in enumerate(task_ids):
        if task_id not in tasks:
            continue
        assigned_time = start_time + timedelta(hours=5 * index)
        scheduled_tasks.append({
            "task_id": task_id,
            "assigned_time": assigned_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        })

    return jsonify({
        "message": "Tasks auto-scheduled based on urgency and user availability.",
        "scheduled_tasks": scheduled_tasks
    })

@app.route('/tasks/<task_id>/set-time', methods=['POST'])
def set_task_time(task_id):
    data = request.get_json()

    # Validate input fields
    if 'start_time' not in data or 'end_time' not in data:
        return jsonify({"error": "Missing start_time or end_time"}), 400

    tasks[task_id] = {
        "start_time": data['start_time'],
        "end_time": data['end_time']
    }

    return jsonify({"message": "Start and end times recorded for the task."}), 200

if __name__ == '__main__':
    app.run(debug=True)
