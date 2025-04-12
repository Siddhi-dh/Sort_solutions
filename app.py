from flask import Flask, jsonify

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Hello, Flask is running!"})

# API route that returns some static data
@app.route('/data')
def get_data():
    return jsonify([
        {"id": 1, "name": "John Doe", "role": "Intern"},
        {"id": 2, "name": "Jane Smith", "role": "Manager"},
        {"id": 3, "name": "Alice Brown", "role": "Developer"}
    ])

if __name__ == '__main__':
    app.run(debug=True)
