from flask import jsonify, request, session
from functools import wraps
from datetime import datetime
from config import DATE_FORMAT, VALID_FREQUENCIES

def error_response(message, status_code):
    return jsonify({"error": message}), status_code

def success_response(message, status_code=200):
    return jsonify({"message": message}), status_code

def get_request_data():
    return request.get_json(silent=True) or {}

def get_current_user_id():
    return session.get("user_id")

def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if not get_current_user_id():
            return error_response("Unauthorized access", 401)
        return route_function(*args, **kwargs)
    return wrapper

def parse_date(date_text):
    return datetime.strptime(date_text, DATE_FORMAT).date()

def format_date(date_value):
    return date_value.strftime(DATE_FORMAT)

def validate_required_fields(data, required_fields):
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}"
    return None

def validate_frequency(frequency):
    if frequency not in VALID_FREQUENCIES:
        return f"Invalid frequency. Use one of: {', '.join(VALID_FREQUENCIES)}"
    return None