from flask import jsonify

def invalid_uploaded_file(expected, received):
    return jsonify({
        "error": "Invalid log file uploaded",
        "expected": expected,
        "received": received
    }), 400


def log_file_not_found(log_file):
    return jsonify({
        "error": "Log file not found",
        "file": log_file
    }), 404
