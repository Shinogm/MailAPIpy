from pydantic import BaseModel
from fastapi import Form

class Contact(BaseModel):
    name: str
    last_name: str
    phone: str
    email: str
    birthday: str | None = None

    @classmethod
    def as_form(
        cls, name: str = Form(...), 
        last_name: str = Form(...), 
        phone: str = Form(...), 
        email: str = Form(...), 
        birthday: str | None = Form(None)
    ):
        return cls(
            name=name,
            last_name=last_name,
            phone=phone,
            email=email,
            birthday=birthday
        )
    
class EditConatact(BaseModel):
    name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    email: str  | None = None
    birthday: str | None = None

    @classmethod
    def as_form(
        cls, name: str | None = Form(None), 
        last_name: str | None = Form(None), 
        phone: str | None = Form(None), 
        email: str | None = Form(None), 
        birthday: str | None = Form(None)
    ):
        return cls(
            name=name,
            last_name=last_name,
            phone=phone,
            email=email,
            birthday=birthday
        )


