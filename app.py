from flask import Flask, jsonify, request, render_template
from log_parser import extract_errors
from errors import log_file_not_found, invalid_uploaded_file
from datetime import datetime
from dotenv import load_dotenv
import os

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
    if not os.path.exists(LOG_FILE):
        return log_file_not_found(LOG_FILE)

    with open(LOG_FILE, 'rb') as file:
        errors = extract_errors(file)

    return jsonify({
        'count': len(errors),
        'errors': errors
    })


@app.route('/upload')
def upload_page():
    return render_template('upload.html')


@app.route('/analyze', methods=['POST'])
def analyze_log():
    uploaded_file = request.files['logfile']

    if uploaded_file.filename != LOG_FILE:
        return invalid_uploaded_file(LOG_FILE, uploaded_file.filename)

    errors = extract_errors(uploaded_file)
    analysis_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render_template(
        'results.html',
        errors=errors,
        count=len(errors),
        analysis_time=analysis_time
    )


if __name__ == '__main__':
    app.run(debug=True)
