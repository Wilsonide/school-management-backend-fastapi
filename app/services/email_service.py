import smtplib
from email.mime.text import MIMEText

from app.core.config import settings


class EmailService:
    def __init__(self):
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = settings.smtp_user
        self.password = settings.smtp_password

    def send_email(self, to_email: str, subject: str, message: str):
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["To"] = to_email

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)

    def send_invite(self, to_email: str, invite_code: str):
        link = f"{settings.frontend_url}/register?invite={invite_code}"

        message = f"""
        You have been invited to join LERNA.

        Click the link below to register:
        {link}

        Your invite code: {invite_code}
        """

        self.send_email(to_email, "LERNA School Invitation", message)


email_service = EmailService()
