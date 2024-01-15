from pydantic import BaseModel
from email.mime.multipart import MIMEMultipart

class SendEmail(BaseModel):
    sender_email: str
    receiver_email: str
    subject: str
    message: MIMEMultipart

class SmtpConfig(BaseModel):
    port: int
    smtp_server: str
    login: str
    password: str
    message_type: MIMEMultipart