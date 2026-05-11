from datetime import datetime
from functools import wraps

from flask import jsonify, request, session

from config import DATE_FORMAT, EXCHANGE_RATES, VALID_FREQUENCIES


def get_request_data():
    return request.get_json(silent=True) or {}


def get_current_user_id():
    return session.get("user_id")


def error_response(message, status_code=400):
    return jsonify({"error": message, "message": message}), status_code


def success_response(message, status_code=200, **extra):
    payload = {"message": message}
    payload.update(extra)
    return jsonify(payload), status_code


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not get_current_user_id():
            return error_response("Unauthorized access", 401)
        return view(*args, **kwargs)

    return wrapped


def parse_date(value):
    if not value:
        raise ValueError("Due date is required")
    return datetime.strptime(str(value), DATE_FORMAT).date()


def format_date(value):
    return value.strftime(DATE_FORMAT) if value else None


def validate_required_fields(data, fields):
    missing = [field for field in fields if data.get(field) in (None, "")]
    if missing:
        return f"Missing required fields: {', '.join(missing)}"
    return None


def validate_frequency(frequency):
    if frequency not in VALID_FREQUENCIES:
        return f"Invalid frequency. Use one of: {', '.join(sorted(VALID_FREQUENCIES))}"
    return None


def convert_currency(amount, currency):
    target = str(currency).upper()
    if target not in EXCHANGE_RATES:
        return None
    return round(float(amount) * EXCHANGE_RATES[target], 2)
