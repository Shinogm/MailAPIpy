from pydantic import BaseModel
from fastapi import Form

class User(BaseModel):
    name: str
    last_name: str
    email: str
    password: str

    @classmethod
    def as_form(
        cls, name: str = Form(...), 
        last_name: str = Form(...), 
        email: str = Form(...), 
        password: str = Form(...)
    ):
        return cls(
            name=name,
            last_name=last_name,
            email=email,
            password=password)