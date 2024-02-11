import json
from flask import Flask, jsonify, request, Request
from werkzeug.datastructures import ImmutableOrderedMultiDict

class CustomRequest(Request):                  # Custom request methods that took way to long, thx hashicorp :(
    def __init__(self, environ):
        super().__init__(environ)
        if self.method in ['LOCK', 'UNLOCK']:
            self.environ['REQUEST_METHOD'] = 'POST'
            self.parameter_storage_class = ImmutableOrderedMultiDict

app = Flask(__name__)
app.request_class = CustomRequest

state = {}

@app.route('/terraform/state', methods=['GET', 'POST'])
def manage_state():
    if request.method == 'GET':
        try:
            with open("terraform.tfstate", 'r') as f:
                state = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            state = {"version": 4}  # Initialize state with a version, change as needed :( 
        return jsonify(state)
    elif request.method == 'POST':
        return set_state()

@app.route('/state', methods=['GET'])
def get_state():
    try:
        with open("terraform.tfstate", 'r') as f:
            state = json.load(f)
    except FileNotFoundError:
        state = {}  # Return an empty state if the file doesn't exist
    except json.JSONDecodeError:
        return "Error: State file is not valid JSON", 400

    return jsonify(state)

@app.route('/state', methods=['POST'])
def set_state():
    state = request.get_json()

    # Validate that the state is in the correct format
    if not isinstance(state, dict) or 'version' not in state:
        return "Error: State must be a JSON object with a 'version' attribute", 400

    try:
        with open("terraform.tfstate", 'w') as f:
            json.dump(state, f)
    except Exception as e:
        return f"Error: Could not write to state file: {e}", 500

    return jsonify(state), 200

lock = False
@app.route('/terraform/lock', methods=['GET', 'POST'])
def lock_state():
    global lock
    app.logger.info(f"URL: {request.url}")
    app.logger.info(f"Method: {request.method}")
    if request.method == 'GET':
        return jsonify({"locked": lock}), 200
    else:  # Handle both 'POST' and 'LOCK' methods
        if lock:
            return "Error: State is already locked", 409  # Conflict
        else:
            lock = True
            return jsonify({"locked": True}), 200

@app.route('/terraform/unlock', methods=['POST', 'UNLOCK'])
def unlock_state():
    global lock
    app.logger.info(f"URL: {request.url}")
    app.logger.info(f"Method: {request.method}")
    if not lock:
        return "Error: State is not locked", 409  # Conflict
    else:
        lock = False
        return jsonify({"locked": False}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=62178, debug=True) # Change your to what ever :) 