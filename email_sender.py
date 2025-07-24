# email_sender.py
import os
print("Running from:", os.getcwd())

import smtplib
from email.message import EmailMessage
from datetime import datetime
from config import (
    SENDER_EMAIL,
    EMAIL_PASSWORD,
    RECIPIENT_EMAIL,
    SMTP_SERVER,
    SMTP_PORT
)

def log_email(status, error=None):
    with open("email_log.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if status == "success":
            log_file.write(f"[{timestamp}]  Email sent to {RECIPIENT_EMAIL}\n")
        else:
            log_file.write(f"[{timestamp}]  Email failed: {error}\n")

def send_outlook_email():
    msg = EmailMessage()
    msg["Subject"] = "New ticket – Bilaga"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg.set_content("En ny ticket har skapats. Filen tickets.json bifogas.")
    try:
        with open("tickets.json", "rb") as f:
            file_data = f.read()
            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="json",
                filename="tickets.json"
            )

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("📩 E-post skickat!")
            log_email("success")  #  Now called only if sending worked

    except Exception as e:
        print("Fel vid e-postskick:", e)
        log_email("fail", str(e))  #  Logs error if sending failed
