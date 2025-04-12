from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = {}  # Dictionary to store tasks

@app.route('/tasks/<task_id>/set-time', methods=['POST'])
def set_time(task_id):
    data = request.json
    if 'start_time' not in data or 'end_time' not in data:
        return jsonify({"error": "Missing start_time or end_time"}), 400

    tasks[task_id] = {
        "start_time": data["start_time"],
        "end_time": data["end_time"]
    }
    return jsonify({"message": "Start and end times recorded for the task."})

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    if task_id in tasks:
        return jsonify(tasks[task_id])
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
