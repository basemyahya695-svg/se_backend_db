from datetime import date, timedelta

from config import BILL_STATUS_UNPAID, EMAIL_REMINDER_DAYS_AHEAD, POPUP_REMINDER_DAYS_AHEAD
from email_service import EmailService
from models import Bill
from recurrence_service import RecurrenceService
from reminder_email_builder import ReminderEmailBuilder
from utils import format_date


class ReminderService:
    def __init__(self, email_service=None, recurrence_service=None, email_builder=None):
        self.email_service = email_service or EmailService()
        self.recurrence = recurrence_service or RecurrenceService()
        self.email_builder = email_builder or ReminderEmailBuilder()

    def due_or_near_due_bills(self, user_id, days_ahead):
        today = date.today()
        deadline = today + timedelta(days=days_ahead)
        return Bill.query.filter(
            Bill.user_id == user_id,
            Bill.status == BILL_STATUS_UNPAID,
            Bill.due_date <= deadline,
        ).order_by(Bill.due_date.asc()).all()

    def due_or_near_due_rent_bills(self, user_id, days_ahead):
        today = date.today()
        deadline = today + timedelta(days=days_ahead)
        return Bill.query.filter(
            Bill.user_id == user_id,
            Bill.status == BILL_STATUS_UNPAID,
            Bill.category == "rent",
            Bill.due_date <= deadline,
        ).order_by(Bill.due_date.asc()).all()

    def due_or_near_due_rent_occurrences(self, user_id, days_ahead):
        today = date.today()
        deadline = today + timedelta(days=days_ahead)
        rent_bills = Bill.query.filter(
            Bill.user_id == user_id,
            Bill.status == BILL_STATUS_UNPAID,
            Bill.category == "rent",
            Bill.due_date <= deadline,
        ).order_by(Bill.due_date.asc()).all()

        occurrences = []
        for bill in rent_bills:
            for due_date in self.recurrence.expand_due_dates(bill, today, deadline):
                if due_date <= today or due_date == deadline:
                    occurrences.append({"bill": bill, "due_date": due_date})

        return sorted(occurrences, key=lambda occurrence: occurrence["due_date"])

    def build_reminders(self, user_id):
        return [
            self.serialize_bill(bill)
            for bill in self.due_or_near_due_bills(user_id, POPUP_REMINDER_DAYS_AHEAD)
        ]

    def current_month_unpaid_bills(self, user_id, paid_occurrences=None, unpaid_occurrences=None):
        paid_occurrences = paid_occurrences or {}
        has_unpaid_occurrence_filter = unpaid_occurrences is not None
        unpaid_occurrence_keys = set(unpaid_occurrences or [])
        today = date.today()
        month_start = date(today.year, today.month, 1)
        month_end = date(today.year, today.month, self.recurrence.days_in_month(today.year, today.month))
        bills = Bill.query.filter(
            Bill.user_id == user_id,
            Bill.status == BILL_STATUS_UNPAID,
            Bill.due_date <= month_end,
        ).order_by(Bill.due_date.asc()).all()

        reminders = []
        for bill in bills:
            for due_date in self.recurrence.expand_due_dates(bill, month_start, month_end):
                occurrence_key = self.occurrence_key(bill.id, due_date)
                if has_unpaid_occurrence_filter and occurrence_key not in unpaid_occurrence_keys:
                    continue
                if self.is_occurrence_paid(occurrence_key, paid_occurrences):
                    continue
                reminders.append(self.serialize_bill(bill, due_date))

        return sorted(reminders, key=lambda reminder: reminder["due_date"])

    def send_current_month_unpaid_email(self, user, paid_occurrences=None, unpaid_occurrences=None):
        reminders = self.current_month_unpaid_bills(user.id, paid_occurrences, unpaid_occurrences)
        body = self.email_builder.monthly_unpaid_body(reminders)

        result = self.email_service.send(
            recipient=user.email,
            subject="Monthly Unpaid Bills",
            body=body,
        )
        return {
            "sent": result["sent"],
            "count": len(reminders),
            "message": "Monthly unpaid bills email sent with bill type and payment status" if result["sent"] else result["error"],
            "bills": reminders,
        }

    @staticmethod
    def occurrence_key(bill_id, due_date):
        return f"{bill_id}:{format_date(due_date)}"

    @staticmethod
    def is_occurrence_paid(occurrence_key, paid_occurrences):
        return bool(paid_occurrences.get(occurrence_key))

    def send_due_emails(self, user):
        reminders = [
            self.serialize_bill(occurrence["bill"], occurrence["due_date"])
            for occurrence in self.due_or_near_due_rent_occurrences(user.id, EMAIL_REMINDER_DAYS_AHEAD)
        ]
        if not reminders:
            return {"sent": False, "count": 0, "message": "No rent bills due in the next two weeks"}

        result = self.email_service.send(
            recipient=user.email,
            subject="MyHome rent reminder: rent due within two weeks",
            body=self.email_builder.rent_due_body(reminders),
        )
        return {
            "sent": result["sent"],
            "count": len(reminders),
            "message": "Rent reminder email sent with bill type and payment status" if result["sent"] else result["error"],
            "bills": reminders,
        }

    @staticmethod
    def serialize_bill(bill, due_date=None):
        today = date.today()
        due_date = due_date or bill.due_date
        if due_date < today:
            state = "overdue"
        elif due_date == today:
            state = "due today"
        else:
            state = "due soon"

        return {
            "id": bill.id,
            "name": bill.name,
            "category": bill.category,
            "amount": bill.amount,
            "currency": bill.currency,
            "due_date": format_date(due_date),
            "status": bill.status,
            "state": state,
        }
