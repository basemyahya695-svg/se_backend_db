from flask import Blueprint, jsonify

from auth_service import AuthService
from auth_validation import validate_login, validate_signup
from reminder_service import ReminderService
from utils import get_request_data, error_response, success_response

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()
reminder_service = ReminderService()


def auth_response(message, user, status_code=200):
    return jsonify({
        "message": message,
        "user": user.to_dict(),
    }), status_code


@auth_bp.route("/api/register", methods=["POST"])
def register_user():
    credentials, validation_error = validate_signup(get_request_data())
    if validation_error:
        return error_response(validation_error, 400)

    try:
        user = auth_service.register(
            username=credentials["username"],
            email=credentials["email"],
            password=credentials["password"],
        )
    except ValueError as error:
        return error_response(str(error), 409)

    return auth_response("User registered successfully", user, 201)


@auth_bp.route("/api/login", methods=["POST"])
def login_user():
    credentials, validation_error = validate_login(get_request_data())
    if validation_error:
        return error_response(validation_error, 400)

    try:
        user = auth_service.login(
            email=credentials["email"],
            password=credentials["password"],
        )
    except ValueError as error:
        return error_response(str(error), 401)

    reminder_service.send_due_emails(user)
    return auth_response("Login successful", user)


@auth_bp.route("/api/me", methods=["GET"])
def get_current_user():
    user = auth_service.current_user()
    if not user:
        return error_response("Unauthorized access", 401)

    return jsonify({"user": user.to_dict()}), 200


@auth_bp.route("/api/logout", methods=["POST"])
def logout_user():
    auth_service.logout()
    return success_response("Logged out successfully")
