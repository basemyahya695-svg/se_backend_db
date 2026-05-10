from database import db
from config import BILL_STATUS_UNPAID

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    bills = db.relationship("Bill", backref="owner", lazy=True)


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(30), nullable=False, default="other")
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="USD")
    due_date = db.Column(db.Date, nullable=False)
    frequency = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default=BILL_STATUS_UNPAID)
