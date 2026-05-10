import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_PASSWORD_LENGTH = 8


def normalize_auth_payload(data):
    return {
        "username": str(data.get("username", "")).strip(),
        "email": str(data.get("email", "")).strip().lower(),
        "password": str(data.get("password", "")),
    }


def validate_signup(data):
    normalized = normalize_auth_payload(data)

    if not normalized["username"]:
        return None, "Full name is required"
    if len(normalized["username"]) > 80:
        return None, "Full name must be 80 characters or fewer"

    credentials, error = validate_login(data)
    if error:
        return None, error

    return {**normalized, **credentials}, None


def validate_login(data):
    normalized = normalize_auth_payload(data)

    if not normalized["email"]:
        return None, "Email is required"
    if not EMAIL_PATTERN.match(normalized["email"]):
        return None, "Enter a valid email address"
    if not normalized["password"]:
        return None, "Password is required"
    if len(normalized["password"]) < MIN_PASSWORD_LENGTH:
        return None, f"Password must be at least {MIN_PASSWORD_LENGTH} characters"

    return {
        "email": normalized["email"],
        "password": normalized["password"],
    }, None
