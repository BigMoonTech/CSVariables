
from flask_mail import Message, Mail
from flask import current_app


def send_email(to, subject, template):
    mail = Mail(current_app)
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
