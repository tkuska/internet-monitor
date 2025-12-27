import smtplib
from email.message import EmailMessage
import os

MIN_DOWNLOAD = float(os.getenv("MIN_DOWNLOAD", 10))

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO")

def send_alert(download):
    if not SMTP_HOST:
        return

    msg = EmailMessage()
    msg["Subject"] = "⚠️ Internet speed alert"
    msg["From"] = SMTP_USER
    msg["To"] = ALERT_EMAIL_TO
    msg.set_content(
        f"Download speed dropped below threshold!\n\n"
        f"Current: {download:.2f} Mbps\n"
        f"Minimum: {MIN_DOWNLOAD:.2f} Mbps"
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
