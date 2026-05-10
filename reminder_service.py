from datetime import date, timedelta

from config import BILL_STATUS_UNPAID, REMINDER_DAYS_AHEAD
from email_service import EmailService
from models import Bill
from utils import format_date


class ReminderService:
    def __init__(self, email_service=None):
        self.email_service = email_service or EmailService()

    def due_or_near_due_bills(self, user_id):
        today = date.today()
        deadline = today + timedelta(days=REMINDER_DAYS_AHEAD)
        return Bill.query.filter(
            Bill.user_id == user_id,
            Bill.status == BILL_STATUS_UNPAID,
            Bill.due_date <= deadline,
        ).order_by(Bill.due_date.asc()).all()

    def build_reminders(self, user_id):
        return [self.serialize_bill(bill) for bill in self.due_or_near_due_bills(user_id)]

    def send_due_emails(self, user):
        reminders = self.build_reminders(user.id)
        if not reminders:
            return {"sent": False, "count": 0, "message": "No due or near-due bills"}

        lines = [
            "Your MyHome bill reminders:",
            "",
            *[
                f"- {item['name']}: {item['amount']} {item['currency']} due {item['due_date']} ({item['state']})"
                for item in reminders
            ],
        ]

        sent = self.email_service.send(
            recipient=user.email,
            subject="MyHome bill reminder",
            body="\n".join(lines),
        )
        return {"sent": sent, "count": len(reminders), "message": "Reminder email processed"}

    @staticmethod
    def serialize_bill(bill):
        today = date.today()
        if bill.due_date < today:
            state = "overdue"
        elif bill.due_date == today:
            state = "due today"
        else:
            state = "due soon"

        return {
            "id": bill.id,
            "name": bill.name,
            "category": bill.category,
            "amount": bill.amount,
            "currency": bill.currency,
            "due_date": format_date(bill.due_date),
            "state": state,
        }
