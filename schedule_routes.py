from flask import Blueprint, jsonify

from models import Bill
from auth_service import UserRepository
from reminder_service import ReminderService
from utils import get_current_user_id, get_request_data, login_required, format_date

schedule_bp = Blueprint('schedule', __name__)
reminders = ReminderService()
users = UserRepository()

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
                "category": bill.category,
                "amount": bill.amount,
                "currency": bill.currency,
                "due_date": format_date(bill.due_date),
                "status": bill.status
            })

    return jsonify(schedule), 200


@schedule_bp.route("/api/reminders", methods=["GET"])
@login_required
def get_reminders():
    return jsonify(reminders.build_reminders(get_current_user_id())), 200


@schedule_bp.route("/api/reminders/send", methods=["POST"])
@login_required
def send_reminder_email():
    user = users.find_by_id(get_current_user_id())
    request_data = get_request_data()
    result = reminders.send_current_month_unpaid_email(
        user,
        paid_occurrences=request_data.get("paid_occurrences", {}),
        unpaid_occurrences=request_data.get("unpaid_occurrences"),
    )
    return jsonify(result), 200
