"""
SMTP Email Notification setup
"""
import smtplib
from email.message import EmailMessage

def send_email(subject, body, receiver_email, smtp_server, smtp_port, smtp_user, smtp_password):
    """
    Send the extracted data to the considered email address via SMPT
    """
    message = EmailMessage()
    message.set_content(body)
    message['Subject'] = subject
    message['From'] = smtp_user
    message['To'] = receiver_email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, receiver_email, message.as_string())
