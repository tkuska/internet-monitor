import smtplib
from email.message import EmailMessage
from config import MINIMAL_SPEED
import os

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO")

def send_alert(download, upload, ping):
    if not SMTP_HOST:
        return

    msg = EmailMessage()
    msg["Subject"] = "⚠️ Internet speed alert"
    msg["From"] = SMTP_USER
    msg["To"] = ALERT_EMAIL_TO
    msg.set_content(
        f"Download speed dropped below threshold!\n\n"
        f"Current download: {download:.2f} Mbps\n"
        f"Current upload : {upload:.2f} Mbps\n"
        f"Current ping : {ping:.2f} ms\n"
        f"Minimum: {MINIMAL_SPEED:.2f} Mbps"
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
