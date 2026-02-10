from flask import Flask, jsonify, request, render_template
from log_parser import extract_errors
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
LOG_FILE = os.getenv('LOG_FILE', 'simplelog.log')
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

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/analyze', methods=['POST'])
def analyze_log():
    file = request.files['logfile']
    errors = extract_errors(file)
    analysis_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for line in file:
        decoded_line = line.decode("utf-8")
        if 'error' in decoded_line.lower():
            errors.append(decoded_line.strip())
    return render_template('results.html', errors=errors, count=len(errors),analysis_time=analysis_time)


if __name__ == '__main__':
    app.run(debug=True)