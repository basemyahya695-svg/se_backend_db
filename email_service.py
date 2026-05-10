import smtplib
from email.message import EmailMessage

from flask import current_app


class EmailService:
    def send(self, recipient, subject, body):
        config = current_app.config
        server = config.get("MAIL_SERVER")
        sender = config.get("MAIL_FROM")

        if not server or not sender:
            current_app.logger.info("Email not configured. Would send to %s: %s", recipient, subject)
            return False

        message = EmailMessage()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP(server, config.get("MAIL_PORT", 587)) as smtp:
            if config.get("MAIL_USE_TLS", True):
                smtp.starttls()
            username = config.get("MAIL_USERNAME")
            password = config.get("MAIL_PASSWORD")
            if username and password:
                smtp.login(username, password)
            smtp.send_message(message)

        return True
