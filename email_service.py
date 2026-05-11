import smtplib
from email.message import EmailMessage

from flask import current_app


class EmailService:
    def send(self, recipient, subject, body):
        config = current_app.config
        server = config.get("MAIL_SERVER")
        port = config.get("MAIL_PORT", 465)
        sender = config.get("MAIL_FROM") or config.get("MAIL_USERNAME")

        if not server or not sender:
            current_app.logger.warning("Email not sent. Configure MAIL_SERVER and MAIL_FROM or MAIL_USERNAME.")
            return {
                "sent": False,
                "error": "Email is not configured. Set MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD, and MAIL_FROM.",
            }

        if not config.get("MAIL_PASSWORD"):
            current_app.logger.warning("Email not sent. MAIL_PASSWORD is missing.")
            return {
                "sent": False,
                "error": "Email password is missing. Set MAIL_PASSWORD to your SMTP/app password.",
            }

        message = EmailMessage()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        try:
            if config.get("MAIL_USE_SSL", port == 465):
                with smtplib.SMTP_SSL(server, port) as smtp:
                    self.login_and_send(smtp, message, config)
            else:
                with smtplib.SMTP(server, port) as smtp:
                    if config.get("MAIL_USE_TLS", True):
                        smtp.starttls()
                    self.login_and_send(smtp, message, config)
        except Exception as error:
            current_app.logger.exception("Email send failed")
            return {"sent": False, "error": str(error)}

        return {"sent": True, "error": ""}

    @staticmethod
    def login_and_send(smtp, message, config):
        smtp.login(config.get("MAIL_USERNAME"), config.get("MAIL_PASSWORD"))
        smtp.send_message(message)
