import smtplib
from app.utils.email.models.send import SendEmail, SmtpConfig
from fastapi import HTTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.services.connection import mail_db
async def send_email(email: SendEmail, smtp_config: SmtpConfig, html_bool: bool = False, html_body: str | None = None, plane_text: str | None = None):
    """
    Server configuration
    """
    port = smtp_config.port
    smtp_server = smtp_config.smtp_server
    user = smtp_config.user_name
    password = smtp_config.user_password
    """
    Email configuration
    """
    sender = email.sender_email
    receiver = email.receiver_email
    subject = email.subject

    message = MIMEMultipart()

    try:
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = subject

        if html_bool:
            body = html_body or ""
            message.attach(MIMEText(body, 'html'))
        else:
            body = plane_text or ""
            message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(sender, receiver, message.as_string())

        return {
            'message': 'Email sent successfully',
            'subject': f'{subject} to {receiver} from {sender}',
            'result': 'success',
            'server_response': server.noop(), 
        }
    except smtplib.SMTPException as e:
        raise HTTPException(status_code=500, detail=f'Error sending email: {str(e)}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error sending email other: {str(e)}')

async def send_massive_email(folder_id: int, user_id: str):
    pass