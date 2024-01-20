import smtplib
from app.utils.email.models.send import SendEmail, SmtpConfig
from fastapi import HTTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.services.connection import mail_db

async def send_email(smtp_config: SmtpConfig, email: SendEmail, html_bool: bool = False, html_body: str | None = None, plane_text: str | None = None):
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

send_email1 = send_email(
    smtp_config=SmtpConfig(
        smtp_server='smtp.gmail.com',
        port=587,
        user_name='s',
        user_password='s'
    ),
    email=SendEmail(
        sender_email='s',
        receiver_email='s',
        subject='s'
    ),
    html_bool=False,
    plane_text='s'

)

async def send_massive_email(folder_id: int, user_id: str, subject: str, html_bool: bool = False, html_body: str | None = None, plane_text: str | None = None):
    user_db = mail_db.fetch_one(
        sql='SELECT BIN_TO_UUID(id) as id, name, email FROM users WHERE id = UUID_TO_BIN(%s)',
        params=(user_id,)
    )
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    folder_db = mail_db.fetch_one(
        sql='SELECT id, name FROM folders WHERE id = %s',
        params=(folder_id,)
    )
    if not folder_db:
        raise HTTPException(status_code=404, detail='Folder not found')

    smtp_config_db = mail_db.fetch_one(
        sql='SELECT * FROM user_email_smtp WHERE user_id = UUID_TO_BIN(%s)',
        params=(user_id,)
    )
    if not smtp_config_db:
        raise HTTPException(status_code=404, detail='SMTP config not found')

    contacts = mail_db.fetch_all(
        sql='SELECT * FROM contacts WHERE id IN (SELECT contact_id FROM contacts_in_user_folder WHERE user_id = UUID_TO_BIN(%s) AND folder_id = %s)',
        params=(user_id, folder_id)
    )
    if not contacts:
        raise HTTPException(status_code=404, detail='Contacts not found')

    spam = None

    if html_bool:
        for contact in contacts:
            spam = send_email(
                smtp_config=SmtpConfig(
                    smtp_server=smtp_config_db['smtp_server'],
                    port=smtp_config_db['port'],
                    user_name=smtp_config_db['user_name'],
                    user_password=smtp_config_db['user_password']
                ),
                email=SendEmail(
                    sender_email=user_db['email'],
                    receiver_email=contact['email'],
                    subject=str(subject)
                ),
                html_bool=True,
                html_body=html_body
            )

    else:
        for contact in contacts:
            spam = send_email(
                smtp_config=SmtpConfig(
                    smtp_server=smtp_config_db['smtp_server'],
                    port=smtp_config_db['port'],
                    user_name=smtp_config_db['user_name'],
                    user_password=smtp_config_db['user_password']
                ),
                email=SendEmail(
                    sender_email=user_db['email'],
                    receiver_email=contact['email'],
                    subject=str(subject)
                ),
                html_bool=False,
                plane_text=plane_text
            )
        
    
    return {
        'message': 'Email sent successfully',
        'subject': f'{folder_db["name"]} to {len(contacts)} contacts from {user_db["name"]} with {user_db["email"]}',
        'result': 'success',
        'config': spam
    }

