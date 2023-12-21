from pydantic import BaseModel
from fastapi import Form
from typing import Annotated

class User(BaseModel):
    name: str
    last_name: str
    email: str
    password: str

    @classmethod
    def as_form(
            cls,
            name: Annotated[str, Form(...)],
            last_name: Annotated[str, Form(...)],
            email: Annotated[str, Form(...)],
            password: Annotated[str, Form(...)],
        ):
        return cls(
            name=name,
            last_name=last_name,
            email=email,
            password=password
        )