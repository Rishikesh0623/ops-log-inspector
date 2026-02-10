from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return 'ops-log-inspector is running'

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/errors')
def geterrror():
    errors = []
    with open('simplelogs.log','r') as file:
        for line in file:
            if 'error' in line:
                errors.append(line.strip())
    return jsonify({'count': len(errors), 'errors': errors})

if __name__ == '__main__':
    app.run(debug=True)