from pydantic import BaseModel

class SendEmail(BaseModel):
    sender_email: str
    receiver_email: str
    subject: str

class SmtpConfig(BaseModel):
    port: int
    smtp_server: str
    user_name: str
    user_password: str