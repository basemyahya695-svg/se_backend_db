from flask import Blueprint, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from database import db
from models import User
from utils import (
    get_request_data, 
    validate_required_fields, 
    error_response, 
    success_response
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/api/register", methods=["POST"])
def register_user():
    data = get_request_data()

    required_error = validate_required_fields(data, ["username", "email", "password"])
    if required_error:
        return error_response(required_error, 400)

    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return error_response("Email already exists", 400)

    new_user = User(
        username=data["username"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"], method="pbkdf2:sha256")
    )

    db.session.add(new_user)
    db.session.commit()

    return success_response("User registered successfully", 201)


@auth_bp.route("/api/login", methods=["POST"])
def login_user():
    data = get_request_data()

    required_error = validate_required_fields(data, ["email", "password"])
    if required_error:
        return error_response(required_error, 400)

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password_hash, data["password"]):
        return error_response("Invalid email or password", 401)

    session["user_id"] = user.id
    session.permanent = True

    return jsonify({
        "message": "Login successful",
        "username": user.username
    }), 200


@auth_bp.route("/api/logout", methods=["POST"])
def logout_user():
    session.pop("user_id", None)
    return success_response("Logged out successfully")