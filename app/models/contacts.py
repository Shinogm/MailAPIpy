from pydantic import BaseModel
from fastapi import Form
from datetime import date
from typing import Annotated

class Contact(BaseModel):
    name: str
    phone: str
    email: str
    birthday_data: date
    
    @classmethod
    def as_form(
            cls,
            name: Annotated[str, Form(...)],
            phone: Annotated[str, Form(...)],
            email: Annotated[str, Form(...)],
            birthday_data: Annotated[date, Form(...)],
        ):
        return cls(
            name=name,
            phone=phone,
            email=email,
            birthday_data=birthday_data
        )

class ContactUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    birthday_data: date | None = None

    @classmethod
    def as_form(
            cls,
            name: Annotated[str | None, Form(...)] = None,
            phone: Annotated[str | None, Form(...)] = None,
            email: Annotated[str | None, Form(...)] = None,
            birthday_data: Annotated[date | None, Form(...)] = None,
        ):
        return cls(
            name=name,
            phone=phone,
            email=email,
            birthday_data=birthday_data
        )