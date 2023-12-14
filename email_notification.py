import smtplib
from email.message import EmailMessage
from config import SMTP_PASSWORD, SMTP_PORT, SMTP_SERVER, SMTP_USER, SUBJECT

def send_email(subject, body, receiver_email, smtp_server, smtp_port, smtp_user, smtp_password):
    message = EmailMessage()
    message.set_content(body)
    message['Subject'] = subject
    message['From'] = smtp_user
    message['To'] = receiver_email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, receiver_email, message.as_string())
