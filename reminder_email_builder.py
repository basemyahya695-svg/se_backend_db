class ReminderEmailBuilder:
    @staticmethod
    def monthly_unpaid_body(reminders):
        if not reminders:
            return "You have no unpaid bills for this month."

        lines = ["Your unpaid bills for this month:", ""]
        for reminder in reminders:
            lines.extend([
                f"Bill name: {reminder['name']}",
                f"Bill type: {reminder['category']}",
                f"Amount: {reminder['amount']} {reminder['currency']}",
                f"Due date: {reminder['due_date']}",
                f"Payment status: {reminder.get('status', 'unpaid')}",
                "-------------------------",
            ])
        return "\n".join(lines)

    @staticmethod
    def rent_due_body(reminders):
        lines = [
            "Hello,",
            "",
            "This is a reminder that you have rent due in 2 weeks.",
            "",
        ]

        for reminder in reminders:
            lines.extend([
                f"Bill name: {reminder['name']}",
                f"Bill type: {reminder['category']}",
                f"Amount: {reminder['amount']} {reminder['currency']}",
                f"Due date: {reminder['due_date']}",
                f"Payment status: {reminder.get('status', 'unpaid')}",
                "",
            ])

        lines.extend([
            "Please pay it before the due date.",
            "",
            "Thank you.",
        ])
        return "\n".join(lines)
