from datetime import date, timedelta

from config import BILL_STATUS_UNPAID, EMAIL_REMINDER_DAYS_AHEAD, POPUP_REMINDER_DAYS_AHEAD
from email_service import EmailService
from models import Bill
from utils import format_date


class ReminderService:
    def __init__(self, email_service=None):
        self.email_service = email_service or EmailService()

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
            for due_date in self.expand_due_dates(bill, today, deadline):
                if due_date <= today or due_date == deadline:
                    occurrences.append({"bill": bill, "due_date": due_date})

        return sorted(occurrences, key=lambda item: item["due_date"])

    def expand_due_dates(self, bill, start_date, end_date):
        due_date = bill.due_date
        frequency = bill.frequency or "once"

        if frequency == "once":
            return [due_date] if due_date <= end_date else []

        current = due_date
        if frequency == "weekly":
            while current < start_date:
                current += timedelta(days=7)
            step = lambda value: value + timedelta(days=7)
        elif frequency == "monthly":
            while current < start_date:
                current = self.add_month(current)
            step = self.add_month
        elif frequency == "yearly":
            while current < start_date:
                current = self.add_year(current)
            step = self.add_year
        else:
            return [due_date] if due_date <= end_date else []

        dates = []
        while current <= end_date:
            dates.append(current)
            current = step(current)
        return dates

    @staticmethod
    def add_month(value):
        year = value.year + (1 if value.month == 12 else 0)
        month = 1 if value.month == 12 else value.month + 1
        day = min(value.day, ReminderService.days_in_month(year, month))
        return date(year, month, day)

    @staticmethod
    def add_year(value):
        year = value.year + 1
        day = min(value.day, ReminderService.days_in_month(year, value.month))
        return date(year, value.month, day)

    @staticmethod
    def days_in_month(year, month):
        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)
        return (next_month - timedelta(days=1)).day

    def build_reminders(self, user_id):
        return [
            self.serialize_bill(bill)
            for bill in self.due_or_near_due_bills(user_id, POPUP_REMINDER_DAYS_AHEAD)
        ]

    def current_month_unpaid_bills(self, user_id):
        today = date.today()
        month_start = date(today.year, today.month, 1)
        month_end = date(today.year, today.month, self.days_in_month(today.year, today.month))
        bills = Bill.query.filter(
            Bill.user_id == user_id,
            Bill.status == BILL_STATUS_UNPAID,
            Bill.due_date <= month_end,
        ).order_by(Bill.due_date.asc()).all()

        reminders = []
        for bill in bills:
            for due_date in self.expand_due_dates(bill, month_start, month_end):
                reminders.append(self.serialize_bill(bill, due_date))

        return sorted(reminders, key=lambda item: item["due_date"])

    def send_current_month_unpaid_email(self, user):
        reminders = self.current_month_unpaid_bills(user.id)

        if not reminders:
            body = "You have no unpaid bills for this month."
        else:
            lines = ["Your unpaid bills for this month:", ""]
            for item in reminders:
                lines.extend([
                    f"Bill name: {item['name']}",
                    f"Amount: {item['amount']} {item['currency']}",
                    f"Due date: {item['due_date']}",
                    "-------------------------",
                ])
            body = "\n".join(lines)

        result = self.email_service.send(
            recipient=user.email,
            subject="Monthly Unpaid Bills",
            body=body,
        )
        return {
            "sent": result["sent"],
            "count": len(reminders),
            "message": "Monthly unpaid bills email sent" if result["sent"] else result["error"],
        }

    def send_due_emails(self, user):
        reminders = [
            self.serialize_bill(item["bill"], item["due_date"])
            for item in self.due_or_near_due_rent_occurrences(user.id, EMAIL_REMINDER_DAYS_AHEAD)
        ]
        if not reminders:
            return {"sent": False, "count": 0, "message": "No rent bills due in the next two weeks"}

        lines = [
            "Hello,",
            "",
            "This is a reminder that you have rent due in 2 weeks.",
            "",
            *[
                "\n".join([
                    f"Bill name: {item['name']}",
                    f"Amount: {item['amount']} {item['currency']}",
                    f"Due date: {item['due_date']}",
                    "",
                ])
                for item in reminders
            ],
            "Please pay it before the due date.",
            "",
            "Thank you.",
        ]

        result = self.email_service.send(
            recipient=user.email,
            subject="MyHome rent reminder: rent due within two weeks",
            body="\n".join(lines),
        )
        return {
            "sent": result["sent"],
            "count": len(reminders),
            "message": "Rent reminder email sent" if result["sent"] else result["error"],
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
            "state": state,
        }
