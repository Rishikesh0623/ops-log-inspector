from flask import Flask, jsonify
import os
from dotenv import load_dotenv
load_dotenv()
LOG_FILE = os.getenv('LOG_FILE', 'simplelogs.log')
app = Flask(__name__)

@app.route('/')
def home():
    return 'ops-log-inspector is running'

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/errors')
def geterror():
    errors = []

    if not os.path.exists(LOG_FILE):
        return jsonify({"error": "Log file not found", "file": LOG_FILE})

    with open(LOG_FILE, 'r') as file:
        for line in file:
            if 'error' in line.lower():
                errors.append(line.strip())

    return jsonify({'count': len(errors), 'errors': errors})

if __name__ == '__main__':
    app.run(debug=True)