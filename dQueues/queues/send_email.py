# dQueues/queues/send_email.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dQueues.secret_config import EMAIL_CONFIG

def get_smtp_settings(email):
    if 'gmail.com' in email:
        return EMAIL_CONFIG['smtp_settings']['gmail']
    elif 'outlook.com' in email or 'hotmail.com' in email:
        return EMAIL_CONFIG['smtp_settings']['outlook']
    else:
        raise ValueError("Unsupported email provider")

def send_email(data):
    sender_email = data.get('sender_email')
    sender_password = EMAIL_CONFIG['senders'].get(sender_email)
    if not sender_password:
        print(f"Sender email {sender_email} not found in configuration.")
        return

    receivers = data.get('receivers')
    subject = data.get('subject')
    body = data.get('body')
    body_type = data.get('body_type', 'plain')
    attachments = data.get('attachments', [])

    smtp_settings = get_smtp_settings(sender_email)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receivers)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, body_type))

    for attachment in attachments:
        filename = attachment['filename']
        filepath = attachment['filepath']
        part = MIMEBase('application', 'octet-stream')
        with open(filepath, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_settings['smtp_server'], smtp_settings['smtp_port'])
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receivers, text)
        server.quit()
        print(f"Email sent successfully from {sender_email} to {receivers}.")
    except Exception as e:
        print(f"Failed to send email: {e}")
