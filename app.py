from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for tasks
tasks = {}

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
