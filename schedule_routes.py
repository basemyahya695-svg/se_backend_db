from flask import Blueprint, jsonify
from datetime import datetime, timedelta

from database import db
from models import Bill
from config import REMINDER_DAYS_AHEAD, BILL_STATUS_UNPAID
from utils import get_current_user_id, login_required, format_date

schedule_bp = Blueprint('schedule', __name__)

@schedule_bp.route("/api/schedule", methods=["GET"])
@login_required
def get_schedule():
    bills = Bill.query.filter_by(
        user_id=get_current_user_id()
    ).order_by(Bill.due_date.asc()).all()

    schedule = {
        "weekly": [],
        "monthly": [],
        "yearly": [],
    }

    for bill in bills:
        if bill.frequency in schedule:
            schedule[bill.frequency].append({
                "id": bill.id,
                "name": bill.name,
                "amount": bill.amount,
                "due_date": format_date(bill.due_date),
                "status": bill.status
            })

    return jsonify(schedule), 200


@schedule_bp.route("/api/reminders", methods=["GET"])
@login_required
def get_reminders():
    today = datetime.now().date()
    reminder_deadline = today + timedelta(days=REMINDER_DAYS_AHEAD)

    upcoming_bills = Bill.query.filter(
        Bill.user_id == get_current_user_id(),
        Bill.status == BILL_STATUS_UNPAID,
        Bill.due_date >= today,
        Bill.due_date <= reminder_deadline
    ).order_by(Bill.due_date.asc()).all()

    reminders = [
        {
            "id": bill.id,
            "message": (
                f"Reminder: '{bill.name}' of ${bill.amount} "
                f"is due on {format_date(bill.due_date)}!"
            )
        }
        for bill in upcoming_bills
    ]

    return jsonify(reminders), 200