import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_DATABASE_URI = "sqlite:///myhome.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)

# Constants used across different files
REMINDER_DAYS_AHEAD = 3
DATE_FORMAT = "%Y-%m-%d"
BILL_STATUS_UNPAID = "unpaid"
BILL_STATUS_PAID = "paid"
VALID_FREQUENCIES = {"weekly", "monthly", "yearly", "once"}


EXCHANGE_RATES = {
    "USD": 1.0,
    "ILS": 3.70, 
    "JOD": 0.71,
    "SAR": 3.75,
    "EUR": 0.92,
    "EGP": 47.50
}