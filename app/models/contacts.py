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
