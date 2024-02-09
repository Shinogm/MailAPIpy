from pydantic import BaseModel
from fastapi import Form
from typing import Annotated

class SendEmail(BaseModel):
    sender_email: str
    receiver_email: str
    subject: str

    @classmethod
    def as_form(
            cls,
            sender_email: Annotated[str, Form(...)],
            receiver_email: Annotated[str, Form(...)],
            subject: Annotated[str, Form(...)]
        ):
        return cls(
            sender_email=sender_email,
            receiver_email=receiver_email,
            subject=subject
        )


class SmtpConfig(BaseModel):
    port: int
    smtp_server: str
    user_name: str
    user_password: str

    @classmethod
    def as_form(
            cls,
            port: Annotated[int, Form(...)],
            smtp_server: Annotated[str, Form(...)],
            user_name: Annotated[str, Form(...)],
            user_password: Annotated[str, Form(...)]
        ):
        return cls(
            port=port,
            smtp_server=smtp_server,
            user_name=user_name,
            user_password=user_password
        )