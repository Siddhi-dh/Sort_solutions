from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from tasks_data import tasks

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
