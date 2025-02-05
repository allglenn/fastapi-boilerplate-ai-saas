import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from config import settings
class MailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.sender_email = settings.SENDER_EMAIL

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str
    ) -> None:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = to_email

        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.send_message(message) 