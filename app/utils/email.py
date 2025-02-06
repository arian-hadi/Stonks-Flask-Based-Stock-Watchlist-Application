from app.extension import mail
from flask_mail import Message
from smtplib import SMTPException
import re


def is_valid_email(email):
    """Validate email format."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def send_report(email, stock_report):
    if not is_valid_email(email):
        return  # Skip invalid email without logging

    subject = "Your Daily Stock Watchlist Report"
    body = f"Hello,\n\nHere is your daily stock performance report:\n\n{stock_report}\n\nBest,\nStock Watch Team"

    msg = Message(subject, recipients=[email], body=body)
    
    try:
        mail.send(msg)
    except SMTPException as e:
        if "550" in str(e):  # Match 'No Such User' bounce error
            print(f"Invalid email skipped: {email}")
            return  # Ignore this error and stop further action
        print(f"Email sending failed for {email}: {e}")