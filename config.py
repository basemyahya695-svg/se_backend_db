import os
from datetime import timedelta


def load_local_env(filename=".env"):
    env_path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(env_path):
        return

    with open(env_path, encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_local_env()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_DATABASE_URI = "sqlite:///myhome.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_FROM = os.environ.get("MAIL_FROM", os.environ.get("MAIL_USERNAME", ""))
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"

# Constants used across different files
EMAIL_REMINDER_DAYS_AHEAD = 14
POPUP_REMINDER_DAYS_AHEAD = 3
DATE_FORMAT = "%Y-%m-%d"
BILL_STATUS_UNPAID = "unpaid"
BILL_STATUS_PAID = "paid"
VALID_FREQUENCIES = {"weekly", "monthly", "yearly", "once"}
VALID_CURRENCIES = {"USD", "ILS", "JOD", "SAR", "EUR", "EGP"}
VALID_BILL_CATEGORIES = {"rent", "water", "gas", "wifi", "electricity", "other"}


EXCHANGE_RATES = {
    "USD": 1.0,
    "ILS": 3.70, 
    "JOD": 0.71,
    "SAR": 3.75,
    "EUR": 0.92,
    "EGP": 47.50
}
